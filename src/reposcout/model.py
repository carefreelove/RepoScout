"""One metered model for main-agent, summarization and repair calls."""

import json

import anthropic
from langchain_anthropic import ChatAnthropic
from pydantic import PrivateAttr

from reposcout.domain import ResearchError
from reposcout.storage import Deadline, Store


class MeteredAnthropic(ChatAnthropic):
    _store: Store = PrivateAttr()
    _run_id: str = PrivateAttr()
    _deadline: Deadline = PrivateAttr()
    _role: str = PrivateAttr(default="research")

    def attach(self, store: Store, run_id: str, deadline: Deadline, role: str = "research"):
        self._store, self._run_id, self._deadline = store, run_id, deadline
        self._role = role
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        # JSON UTF-8 bytes are a conservative token bound, plus protocol/schema overhead.
        payload = json.dumps({"messages": [m.model_dump() for m in messages], "options": kwargs},
                             default=str, ensure_ascii=False).encode("utf-8")
        if len(payload) > 160_000:
            raise ResearchError("context_limit", "模型上下文超过 160 KB 限制，证据已保存")
        input_bound = len(payload) * 2 + 8192
        rates = {"deepseek-flash": (2, 8), "deepseek-v4-pro": (9, 27)}
        if self.model not in rates:
            raise ResearchError("configuration", "该模型没有已核对的价格快照")
        input_rate, output_rate = rates[self.model]
        reserve = input_bound * input_rate + self.max_tokens * output_rate
        for attempt in range(3):
            self._deadline.check()
            ticket = self._store.reserve(self._run_id, reserve, self.model, self._role, input_rate, output_rate)
            try:
                result = super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)
            except anthropic.RateLimitError as exc:
                self._store.settle(ticket, "rejected", 0)
                headers = exc.response.headers
                try:
                    delay = float(headers.get("retry-after", 2 ** attempt))
                except ValueError:
                    delay = 60
                if attempt == 2 or delay > 5 or delay >= self._deadline.remaining():
                    raise ResearchError("model_rate_limit", "模型服务限流，请稍后恢复") from exc
                import time
                time.sleep(max(0, delay))
                continue
            except (anthropic.AuthenticationError, anthropic.PermissionDeniedError, anthropic.BadRequestError) as exc:
                self._store.settle(ticket, "rejected", 0)
                raise ResearchError("model_request", f"模型请求被拒绝，HTTP {exc.status_code}，请检查配置") from exc
            except KeyboardInterrupt:
                self._store.settle(ticket, "uncertain")
                raise
            except Exception as exc:
                self._store.settle(ticket, "uncertain")
                self._store.event(self._run_id, "model_failure", f"{self._role} 请求中断，类型 {type(exc).__name__}，用量待确认")
                raise ResearchError("uncertain_usage", f"模型请求中断，用量未确认，记录 {ticket}，保留预留费用并停止付费调用") from exc
            usage = result.generations[0].message.usage_metadata
            if not usage or not all(isinstance(usage.get(k), int) and usage[k] >= 0
                                    for k in ("input_tokens", "output_tokens")):
                self._store.settle(ticket, "uncertain")
                raise ResearchError("uncertain_usage", f"模型未返回完整用量，记录 {ticket}，已停止后续付费调用")
            cost = usage["input_tokens"] * input_rate + usage["output_tokens"] * output_rate
            if cost > reserve:
                self._store.settle(ticket, "uncertain", cost, usage["input_tokens"], usage["output_tokens"])
                raise ResearchError("pricing_bound", "实际用量超过预留上界，已停止后续付费调用")
            self._store.settle(ticket, "settled", cost, usage["input_tokens"], usage["output_tokens"])
            return result
        raise AssertionError("unreachable")

    async def _agenerate(self, *args, **kwargs):
        raise ResearchError("unsupported_mode", "当前仅提供同步执行，避免绕过预算统计")

    def _stream(self, *args, **kwargs):
        raise ResearchError("unsupported_mode", "当前仅提供非流式执行，避免绕过预算统计")

    def _astream(self, *args, **kwargs):
        raise ResearchError("unsupported_mode", "当前仅提供非流式执行，避免绕过预算统计")


def create_model(store: Store, run_id: str, deadline: Deadline, role: str = "research") -> MeteredAnthropic:
    settings = store.settings
    name = settings.review_model if role == "review" else settings.model
    return MeteredAnthropic(model_name=name, api_key=settings.api_key(),
                            base_url=settings.base_url, max_tokens=settings.max_output_tokens,
                            timeout=min(90 if role == "review" else 45, deadline.remaining()), max_retries=0,
                            streaming=False, thinking={"type": "disabled"}, temperature=0).attach(store, run_id, deadline, role)

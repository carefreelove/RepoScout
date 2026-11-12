"""Fixed smoke suite with clearly separated synthetic and live execution."""

import base64
import json
import time
from pathlib import Path

import httpx
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import PrivateAttr

from reposcout.agent import execute
from reposcout.domain import ReportDraft, now
from reposcout.model import create_model
from reposcout.reporting import atomic_write
from reposcout.storage import Deadline, Store

SUITE = [
    {"id": "stack", "criterion": "Java 技术栈", "verdict": "满足",
     "request": "搜索支持 Java 的开源 LLM Agent 框架，重点调研 langchain4j/langchain4j，给出依赖或源码依据。"},
    {"id": "maintenance", "criterion": "近 180 天维护", "verdict": "满足",
     "request": "搜索 Java Agent 项目，重点检查 langchain4j/langchain4j 最近 180 天的维护情况，说明提交与发布证据。"},
    {"id": "deployment", "criterion": "部署文档", "verdict": "满足",
     "request": "搜索可用于 Java 后端的 Agent 项目，重点调研 spring-ai-alibaba/spring-ai-alibaba 的使用与部署资料，区分文档和实测。"},
    {"id": "comparison", "criterion": "Java 技术栈", "verdict": "满足",
     "request": "搜索 Java Agent 框架，比较 langchain4j/langchain4j 与 spring-ai-alibaba/spring-ai-alibaba 的技术栈与使用方式，给出来源。"},
    {"id": "insufficient", "criterion": "性能经过独立验证", "verdict": "未确认",
     "request": "搜索 Java Agent 框架，检查 langchain4j/langchain4j 是否有可证明单机 1 万 QPS 的独立基准，资料不足时明确未确认。"},
]

FIXTURE_REPO = "fixture/demo-agent"
FIXTURE_SHA = "a" * 40


def fixture_response(request: httpx.Request) -> httpx.Response:
    """Synthetic inputs only. Never represent these as fetched public repository facts."""
    path = request.url.path
    if path == "/search/repositories":
        data = {"items": [{"full_name": FIXTURE_REPO, "private": False, "language": "Java"}]}
    elif path == f"/repos/{FIXTURE_REPO}":
        data = {"full_name": FIXTURE_REPO, "private": False, "language": "Java", "archived": False}
    elif path.endswith("/commits"):
        data = [{"sha": FIXTURE_SHA, "commit": {"committer": {"date": now()}, "message": "Synthetic test commit"}}]
    elif path.endswith("/releases"):
        data = []
    elif path.endswith("/contents/README.md"):
        data = {"type": "file", "size": 75, "encoding": "base64",
                "content": base64.b64encode(b"# Synthetic Agent\nJava 21. Deployment documentation: run java -jar app.jar.\n").decode()}
    else:
        return httpx.Response(404, json={"message": "synthetic missing file"})
    return httpx.Response(200, json=data)


def fixture_draft(store: Store, run_id: str, case: dict) -> ReportDraft:
    ids = [e["id"] for e in store.objects(run_id, "evidence") if e["repository"] == FIXTURE_REPO]
    unknown = case["verdict"] == "未确认"
    return ReportDraft(interpreted_request=case["request"], criteria=[{"name": case["criterion"]}],
        candidates=[{"repository": FIXTURE_REPO, "summary": "合成测试仓库",
            "assessments": [{"criterion": case["criterion"], "verdict": case["verdict"],
                             "reason": "根据合成输入判定，供流程回归使用", "evidence_ids": ids}],
            "decision": "待确认" if unknown else "推荐", "decision_reason": "合成回放预期结果",
            "evidence_ids": ids, "unknowns": ["缺少性能实测"] if unknown else []}],
        conclusion="合成回放完成", unknowns=["此结果用于离线流程验证"])


class ScriptedModel(BaseChatModel):
    """Deterministic tool transcript that exercises the real Deep Agents graph."""
    model_name: str = "deepseek-flash"
    _step: int = PrivateAttr(default=0)
    _store: Store = PrivateAttr()
    _run_id: str = PrivateAttr()
    _case: dict = PrivateAttr()
    _tool_names: set = PrivateAttr(default_factory=set)

    @property
    def _llm_type(self):
        return "anthropic-chat"

    def _get_ls_params(self, stop=None, **kwargs):
        return {"ls_provider": "anthropic", "ls_model_name": self.model_name, "ls_model_type": "chat"}

    def attach(self, store: Store, run_id: str, case: dict):
        self._store, self._run_id, self._case = store, run_id, case
        return self

    def bind_tools(self, tools, **kwargs):
        self._tool_names = {t.name if hasattr(t, "name") else t["name"] for t in tools}
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        steps = [
            ("search_repositories", {"query": "agent language:Java"}),
            ("inspect_repository", {"repository": FIXTURE_REPO}),
            ("read_repository_file", {"repository": FIXTURE_REPO, "path": "missing.md" if self._case["id"] == "insufficient" else "README.md"}),
        ]
        if self._step < len(steps):
            name, args = steps[self._step]
        elif self._step == len(steps):
            name, args = "submit_report", {"report": fixture_draft(self._store, self._run_id, self._case).model_dump()}
        else:
            return ChatResult(generations=[ChatGeneration(message=AIMessage(content="报告已保存"))])
        self._step += 1
        message = AIMessage(content="", tool_calls=[{"name": name, "args": args,
                           "id": f"fixture-{self._step}", "type": "tool_call"}])
        return ChatResult(generations=[ChatGeneration(message=message)])


def evaluate(store: Store, live: bool = False) -> Path:
    results = []
    for case in SUITE:
        # The suite names one target, except the explicit two-target comparison.
        case_store = Store(store.settings.model_copy(update={
            "analyze_limit": 2 if case["id"] == "comparison" else 1,
        }))
        run_id = case_store.create(case["request"], "live" if live else "offline")
        model = None if live else ScriptedModel().attach(case_store, run_id, case)
        transport = None if live else httpx.MockTransport(fixture_response)
        path = execute(case_store, run_id, model=model, transport=transport)
        report = json.loads((path / "report.json").read_text())
        checks = {
            "valid_report": report["status"] == "completed",
            "source_coverage": coverage(report),
            "fact_correctness": None, "condition_correctness": None,
        }
        if not live:
            checks["expected_verdict"] = bool(report["candidates"]) and report["candidates"][0]["assessments"][0]["verdict"] == case["verdict"]
        record = {"case_id": case["id"], "request": case["request"], "mode": "live" if live else "offline_synthetic",
                  "run_id": run_id, "statistics": report["statistics"], "checks": checks}
        if live:
            record["baseline"] = baseline(store, case["request"])
        results.append(record)
        print(f"{case['id']} {record['mode']} {report['status']}", flush=True)
        if live and store.statistics(run_id)["unconfirmed_calls"]:
            break
    path = store.settings.home / ("evaluation-live.json" if live else "evaluation-offline.json")
    atomic_write(path, json.dumps({"suite": "smoke", "generated_at": now(),
        "note": "离线模式使用合成 HTTP 与脚本模型，正确性人工评分为 null 时表示尚未评分。对照模型仅收到原始问题，缺少实时 GitHub 工具。",
        "results": results}, ensure_ascii=False, indent=2))
    return path


def coverage(report: dict) -> float | None:
    statements = [a for c in report["candidates"] for a in c["assessments"] if a["verdict"] != "未确认"]
    statements += [claim for c in report["candidates"] for claim in c["claims"] if claim["basis"] != "unknown"]
    return sum(bool(s["evidence_ids"]) for s in statements) / len(statements) if statements else None


def baseline(store: Store, request: str) -> dict:
    run_id = store.create(request)
    started = time.monotonic()
    try:
        answer = create_model(store, run_id, Deadline(90)).invoke(request)
        blocks = answer.content
        text = blocks if isinstance(blocks, str) else "\n".join(b.get("text", "") for b in blocks if b.get("type") == "text")
        store.update(run_id, status="completed")
    except Exception as exc:
        text = "对照调用中断，错误类型 " + type(exc).__name__
        store.update(run_id, status="failed")
    store.update(run_id, elapsed=time.monotonic() - started)
    directory = store.settings.home / "runs" / run_id
    directory.mkdir(parents=True, exist_ok=True)
    atomic_write(directory / "baseline.md", text + "\n")
    return {"run_id": run_id, "status": store.run(run_id)["status"], "statistics": store.statistics(run_id),
            "information_access": "同模型，仅原始问题，单次调用，无 GitHub 工具",
            "fact_correctness": None, "condition_correctness": None}

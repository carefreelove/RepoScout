"""Run a controlled-error regression with real GitHub data, Flash and Pro.

The Java 8 assertion is deliberately injected, so the artifact records an
explicit fault-injection test rather than claiming a naturally occurring error.
"""

import json
import time
from pathlib import Path

from dotenv import load_dotenv

from reposcout.agent import execute
from reposcout.domain import ReportDraft
from reposcout.github import GitHub
from reposcout.reporting import export
from reposcout.settings import Settings
from reposcout.storage import Deadline, Store
from reposcout.verification import Verifier


def main():
    load_dotenv()
    store = Store(Settings(analyze_limit=1))
    repository = "langchain4j/langchain4j"
    request = "确认 langchain4j/langchain4j 的 Java 构建目标。请使用全文检索工具检索 java.version，补齐源码依据，再修正草稿并提交。"
    run_id = store.create(request)
    started = time.monotonic()
    initial = None
    draft = None
    try:
        github = GitHub(store, run_id, Deadline(600))
        try:
            github.inspect(repository)
            readme = github.file(repository, "README.md", 1, 85)
        finally:
            github.close()
        draft = ReportDraft(interpreted_request=request, criteria=[{"name": "确认 Java 构建目标"}],
            candidates=[{"repository": repository, "summary": "已定位公开 Java Agent 仓库。",
                "claims": [{"text": "该项目的 Java 构建目标为 8。", "basis": "source", "evidence_ids": [readme["id"]]}],
                "assessments": [{"criterion": "确认 Java 构建目标", "verdict": "满足", "reason": "已确认构建目标为 Java 8。", "evidence_ids": [readme["id"]]}],
                "decision": "推荐", "decision_reason": "构建版本已获得源码依据。", "evidence_ids": [readme["id"]]}],
            conclusion="该项目的 Java 构建目标为 8。")
        initial = Verifier(store, run_id, Deadline(600), None).submit(draft, call_id="controlled-initial-draft")
        if initial["status"] != "needs_evidence":
            raise AssertionError("Injected unsupported assertion was not rejected")
        store.update(run_id, elapsed=time.monotonic() - started, status="partial")
        result = execute(store, run_id, resume=True)
    except Exception:
        store.update(run_id, status="partial", elapsed=time.monotonic() - started)
        result = export(store, run_id)
        raise
    finally:
        target = Path("examples/v0.2/repair-demo")
        target.mkdir(parents=True, exist_ok=True)
        if draft:
            (target / "initial-draft.json").write_text(draft.model_dump_json(indent=2))
        if initial:
            (target / "initial-review.json").write_text(json.dumps(initial, ensure_ascii=False, indent=2))
        manifest = {"run_id": run_id, "mode": "live_models_live_github_controlled_error",
                    "injected_error": "Java 8 assertion with README-only citation",
                    "status": store.run(run_id)["status"], "statistics": store.statistics(run_id)}
        (target / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
        source = store.settings.home / "runs" / run_id
        for name in ("report.json", "report.md", "review.json", "events.jsonl"):
            if (source / name).exists():
                (target / name).write_bytes((source / name).read_bytes())
    print(result.resolve())
    if store.run(run_id)["status"] != "completed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

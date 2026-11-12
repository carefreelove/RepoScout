"""Retrieval, review and compatibility regression scenarios."""

import json
import sqlite3
from pathlib import Path

import httpx
import pytest
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from reposcout.agent import create_tools, execute
from reposcout.domain import Claim, Report, ResearchError
from reposcout.evaluation import (
    FIXTURE_REPO,
    FIXTURE_SHA,
    SUITE,
    ScriptedModel,
    ScriptedReviewer,
    fixture_draft,
    fixture_response,
)
from reposcout.github import GitHub
from reposcout.model import MeteredAnthropic
from reposcout.reporting import export, markdown
from reposcout.retrieval import RepositoryIndex, chunks
from reposcout.settings import Settings
from reposcout.storage import Deadline, Store
from reposcout.verification import Verifier


@pytest.fixture
def research(tmp_path):
    store = Store(Settings(home=tmp_path / "state"))
    run_id = store.create("查找 Java Agent", "offline")
    github = GitHub(store, run_id, Deadline(60), httpx.MockTransport(fixture_response))
    github.inspect(FIXTURE_REPO)
    github.file(FIXTURE_REPO, "README.md")
    yield store, run_id, github
    github.close()


class ReviewStub(ScriptedReviewer):
    def __init__(self, rejected_calls=0, failure_call=0):
        self.calls = 0
        self.rejected_calls = rejected_calls
        self.failure_call = failure_call
        self.payloads = []

    def invoke(self, messages):
        self.calls += 1
        if self.calls == self.failure_call:
            raise TimeoutError("synthetic review timeout")
        self.payloads.append(json.loads(messages[-1]["content"]))
        response = super().invoke(messages)
        if self.calls <= self.rejected_calls:
            response.findings[0].verdict = "insufficient"
            response.findings[0].reason = "需要定向补证"
            response.findings[0].needed_query = "java.version"
        return response


def test_index_idempotency_and_commit_isolation(research):
    store, run_id, _ = research
    index = RepositoryIndex(store)
    index.add(FIXTURE_REPO, FIXTURE_SHA, "src/X.java", "class CheckpointStore {}")
    index.add(FIXTURE_REPO, FIXTURE_SHA, "src/X.java", "class CheckpointStore {}")
    index.add(FIXTURE_REPO, "b" * 40, "src/Secret.java", "OnlyOtherCommit")
    index.add("other/repo", FIXTURE_SHA, "src/Secret.java", "OnlyOtherRepo")
    assert len(index.search(run_id, FIXTURE_REPO, "CheckpointStore")["hits"]) == 1
    assert index.search(run_id, FIXTURE_REPO, "OnlyOtherCommit")["hits"] == []
    assert index.search(run_id, FIXTURE_REPO, "OnlyOtherRepo")["hits"] == []
    first = index.search(run_id, FIXTURE_REPO, "CheckpointStore")["hits"][0]
    assert index.search(run_id, FIXTURE_REPO, "CheckpointStore")["hits"][0]["id"] == first["id"]
    with pytest.raises(ResearchError, match="不一致"):
        index.add(FIXTURE_REPO, FIXTURE_SHA, "src/X.java", "changed content")


def test_chunk_limits_overlap_and_line_numbers():
    content = "\n".join(f"line {i}" for i in range(200))
    parts = list(chunks(content))
    assert parts[0][:2] == (1, 80)
    assert parts[1][0] == 71
    assert parts[-1][1] == 200
    assert all(len(body.encode()) <= 8000 and last - first < 80 for first, last, body, _ in parts)
    oversized = list(chunks("汉" * 6000))
    assert oversized[0][3]
    assert len(oversized[0][2].encode()) < 8000


def test_chinese_substring_and_keyword_escaping(research):
    store, run_id, _ = research
    index = RepositoryIndex(store)
    index.add(FIXTURE_REPO, FIXTURE_SHA, "docs/恢复.md", "系统支持断点恢复及任务取消。\n100% deterministic")
    assert index.search(run_id, FIXTURE_REPO, "断点恢复")["hits"][0]["path"] == "docs/恢复.md"
    assert index.search(run_id, FIXTURE_REPO, 'missing " OR anything')["hits"] == []
    assert index.search(run_id, FIXTURE_REPO, "不存在内容")["hits"] == []


def test_full_document_indexed_from_partial_read(research):
    store, run_id, github = research
    github.file(FIXTURE_REPO, "README.md", 1, 1)
    result = RepositoryIndex(store).search(run_id, FIXTURE_REPO, "Deployment")
    assert result["hits"]
    assert "2: Java" in result["hits"][0]["content"]
    assert result["returned_bytes"] <= 16000


def test_legacy_excerpt_keeps_original_lines_and_filename(research):
    store, run_id, _ = research
    store.evidence(run_id, repository=FIXTURE_REPO, kind="file", commit=FIXTURE_SHA,
                   path="docs/a#legacy-name.md", start_line=101, end_line=102,
                   url="https://github.com/fixture/demo-agent", summary="旧片段",
                   content="101: special_recovery_keyword\n102: retained")
    result = RepositoryIndex(store).search(run_id, FIXTURE_REPO, "special_recovery_keyword")
    assert result["hits"][0]["path"] == "docs/a#legacy-name.md"
    assert result["hits"][0]["start_line"] == 101
    assert "#L101-L102" in result["hits"][0]["url"]
    assert "%23legacy" in result["hits"][0]["url"]


def test_directory_scoped_filter_and_pagination(research):
    store, run_id, github = research
    github.client.close()
    data = [{"name": f"doc{i}.md", "path": f"docs/doc{i}.md", "type": "file", "size": 1} for i in range(205)]
    github.client = httpx.Client(base_url="https://api.github.com", transport=httpx.MockTransport(lambda r: httpx.Response(200, json=data)))
    before = store.statistics(run_id)["github_requests"]
    first = github.directory(FIXTURE_REPO, "docs", "*.MD")
    second = github.directory(FIXTURE_REPO, "docs", "*.MD", 200)
    assert first["next_offset"] == 200
    assert len(json.loads(first["evidence"]["content"])) == 200
    assert len(json.loads(second["evidence"]["content"])) == 5
    assert store.statistics(run_id)["github_requests"] == before + 1


def test_evidence_retrieval_is_run_scoped(research):
    store, run_id, github = research
    item = store.objects(run_id, "evidence")[0]
    tool = create_tools(github, store, run_id)[7]
    assert tool.invoke({"evidence_id": item["id"]})["data"] == item
    another = store.create("other")
    assert create_tools(github, store, another)[7].invoke({"evidence_id": item["id"]})["code"] == "not_found"


def test_review_and_targeted_repair(research):
    store, run_id, _ = research
    reviewer = ReviewStub(rejected_calls=1)
    verifier = Verifier(store, run_id, Deadline(60), reviewer)
    draft = fixture_draft(store, run_id, SUITE[0])
    assert verifier.submit(draft)["status"] == "needs_evidence"
    draft.candidates[0].summary = "修正后准确表述"
    assert verifier.submit(draft)["status"] == "saved"
    assert verifier.state().rounds == 2
    assert verifier.state().supplement_rounds == 1
    assert verifier.passed()
    assert all("messages" not in p and p["evidence"] for p in reviewer.payloads)
    assert export(store, run_id).joinpath("review.json").exists()


def test_no_progress_and_replayed_tool_call(research):
    store, run_id, _ = research
    reviewer = ReviewStub(rejected_calls=100)
    verifier = Verifier(store, run_id, Deadline(60), reviewer)
    draft = fixture_draft(store, run_id, SUITE[0])
    response = verifier.submit(draft, call_id="tool-1")
    assert verifier.submit(draft, call_id="tool-1") == response
    assert reviewer.calls == 1
    with pytest.raises(ResearchError) as error:
        verifier.submit(draft, call_id="tool-2")
    assert error.value.code == "no_progress"


def test_two_supplement_rounds_stop(research):
    store, run_id, _ = research
    verifier = Verifier(store, run_id, Deadline(60), ReviewStub(rejected_calls=100))
    draft = fixture_draft(store, run_id, SUITE[0])
    for i in range(2):
        draft.conclusion = f"修订{i}"
        assert verifier.submit(draft)["status"] == "needs_evidence"
    draft.conclusion = "第三轮"
    with pytest.raises(ResearchError) as error:
        verifier.submit(draft)
    assert error.value.code == "review_limit"
    assert verifier.state().rounds == 3


def test_failed_batch_resumes_without_repeating_successful_batch(research):
    store, run_id, _ = research
    reviewer = ReviewStub(failure_call=2)
    verifier = Verifier(store, run_id, Deadline(60), reviewer)
    draft = fixture_draft(store, run_id, SUITE[0])
    ids = draft.candidates[0].evidence_ids
    draft.candidates[0].claims = [Claim(text=f"合成事实{i}", basis="documentation", evidence_ids=ids) for i in range(10)]
    with pytest.raises(TimeoutError):
        verifier.submit(draft)
    assert verifier.state().status == "failed"
    assert verifier.submit(draft)["status"] == "saved"
    assert reviewer.calls == 3
    assert verifier.state().rounds == 1


@pytest.mark.parametrize("bad_mode", ["missing_item", "fake_evidence", "missing_reference"])
def test_bad_review_output_is_rejected(research, bad_mode):
    store, run_id, _ = research

    class BrokenReviewer(ScriptedReviewer):
        def invoke(self, messages):
            result = super().invoke(messages)
            if bad_mode == "missing_item":
                result.findings.pop()
            elif bad_mode == "fake_evidence":
                result.findings[0].evidence_ids = ["fake-id"]
            else:
                result.findings[0].evidence_ids = []
            return result

    verifier = Verifier(store, run_id, Deadline(60), BrokenReviewer())
    with pytest.raises(ResearchError, match="审查"):
        verifier.submit(fixture_draft(store, run_id, SUITE[0]))
    assert not verifier.passed()


def test_rule_rejects_outdated_maintenance(research):
    store, run_id, _ = research
    pin = store.get(run_id, "repository", FIXTURE_REPO)
    pin["maintenance"] = {"recent_commits": [{"date": "2020-01-01T00:00:00Z"}], "recent_releases": []}
    store.put(run_id, "repository", FIXTURE_REPO, pin)
    verifier = Verifier(store, run_id, Deadline(60), ScriptedReviewer())
    assert verifier.submit(fixture_draft(store, run_id, SUITE[1]))["status"] == "needs_evidence"
    assert any("时间窗口" in item.reason for item in verifier.state().findings)


def test_review_timeout_exports_partial_and_preserves_draft(research):
    store, run_id, _ = research
    path = execute(store, run_id, model=ScriptedModel().attach(store, run_id, SUITE[0]),
                   transport=httpx.MockTransport(fixture_response), reviewer=ReviewStub(failure_call=1))
    report = json.loads((path / "report.json").read_text())
    assert report["status"] == "partial" and report["review"]["status"] == "failed"
    assert report["candidates"]


def test_legacy_ledger_migration_preserves_cost(tmp_path):
    home = tmp_path / "old"
    home.mkdir()
    with sqlite3.connect(home / "state.sqlite") as db:
        db.execute("CREATE TABLE ledger(id TEXT PRIMARY KEY,run_id TEXT,state TEXT,cost INTEGER,input_tokens INTEGER,output_tokens INTEGER,at TEXT)")
        db.execute("INSERT INTO ledger VALUES('old','legacy','settled',123,20,10,'2026-11-12')")
    store = Store(Settings(home=home))
    with store.connect() as db:
        row = db.execute("SELECT * FROM ledger WHERE id='old'").fetchone()
        assert row["cost"] == 123 and row["model"] == "deepseek-flash"
        assert row["input_rate"] == 2 and row["output_rate"] == 8


def test_pro_rate_and_shared_budget(research, monkeypatch):
    store, run_id, _ = research
    monkeypatch.setattr(ChatAnthropic, "_generate", lambda *a, **k: ChatResult(generations=[ChatGeneration(message=AIMessage(
        content="ok", usage_metadata={"input_tokens": 100, "output_tokens": 20, "total_tokens": 120}))]))
    model = MeteredAnthropic(model="deepseek-v4-pro", api_key="synthetic", max_tokens=4096).attach(store, run_id, Deadline(60), role="review")
    model.invoke("review")
    assert store.statistics(run_id)["estimated_cost_cny_upper_bound"] == 0.00144
    assert store.statistics(run_id)["models"][0]["role"] == "review"
    store.settings.max_cost_cny = 0.0015
    with pytest.raises(ResearchError) as error:
        model.invoke("review again")
    assert error.value.code == "cost_budget"


def test_old_report_reader_preserves_markdown():
    path = Path("examples/live/stack/report.json")
    report = Report.model_validate_json(path.read_text())
    assert report.schema_version == "1.0" and report.review.status == "not_reviewed"
    assert markdown(report) == path.with_suffix(".md").read_text()


def test_multiple_legacy_fragments_and_full_document(research):
    store, run_id, _ = research
    for content, end in (("101: overlap_term", 101), ("101: overlap_term\n102: expanded_term", 102)):
        store.evidence(run_id, repository=FIXTURE_REPO, kind="file", commit=FIXTURE_SHA,
                       path="old.md", start_line=101, end_line=end, url="https://example.invalid",
                       summary="旧片段", content=content)
    index = RepositoryIndex(store)
    assert index.search(run_id, FIXTURE_REPO, "expanded_term")["hits"]
    index.add(FIXTURE_REPO, FIXTURE_SHA, "old.md", "full_document_term")
    assert index.search(run_id, FIXTURE_REPO, "expanded_term")["hits"] == []
    assert index.search(run_id, FIXTURE_REPO, "full_document_term")["hits"][0]["start_line"] == 1


def test_review_cancellation_is_persistent(research):
    store, run_id, _ = research

    class CancelReviewer(ScriptedReviewer):
        def invoke(self, messages):
            raise KeyboardInterrupt

    verifier = Verifier(store, run_id, Deadline(60), CancelReviewer())
    draft = fixture_draft(store, run_id, SUITE[0])
    with pytest.raises(KeyboardInterrupt):
        verifier.submit(draft)
    assert store.run(run_id)["draft"] and verifier.state().status == "failed"
    assert Verifier(store, run_id, Deadline(60), ScriptedReviewer()).submit(draft)["status"] == "saved"


def test_completed_requires_matching_reviewed_draft(research):
    store, run_id, _ = research
    verifier = Verifier(store, run_id, Deadline(60), ScriptedReviewer())
    draft = fixture_draft(store, run_id, SUITE[0])
    verifier.submit(draft)
    assert verifier.passed()
    draft.conclusion = "未经核验的新结论"
    store.update(run_id, draft=draft.model_dump_json())
    assert not verifier.passed()


def test_oversized_review_item_requires_smaller_citations(research):
    store, run_id, _ = research
    draft = fixture_draft(store, run_id, SUITE[0])
    huge = store.evidence(run_id, repository=FIXTURE_REPO, kind="file", commit=FIXTURE_SHA,
        path="huge.md", start_line=1, end_line=1, url="https://example.invalid", summary="大证据", content="x" * 100000)
    draft.candidates[0].evidence_ids.append(huge["id"])
    reviewer = ReviewStub()
    verifier = Verifier(store, run_id, Deadline(60), reviewer)
    assert verifier.submit(draft)["status"] == "needs_evidence"
    assert any("体积上限" in f.reason for f in verifier.state().findings)
    assert all(len(json.dumps({"content": json.dumps(p, ensure_ascii=False)}, ensure_ascii=False).encode()) <= 96000 for p in reviewer.payloads)


def test_retrieval_and_reviewer_protocol_suite(research):
    from reposcout.evidence_evaluation import evaluate_evidence
    value = json.loads(evaluate_evidence(research[0]).read_text())
    assert value["passed"]
    assert len(value["retrieval"]) == 8 and len(value["reviews"]) == 6
    assert all(item["mode"] == "offline_protocol_replay" for item in value["reviews"])


def test_acknowledgment_preserves_upper_bound_and_unknown_usage(research):
    store, run_id, _ = research
    ticket = store.reserve(run_id, 500000)
    store.settle(ticket, "uncertain")
    assert store.statistics(run_id)["billing_blocked"]
    with pytest.raises(ResearchError):
        store.reserve(run_id, 1)
    assert store.acknowledge_uncertain(ticket) == 500000
    statistics = store.statistics(run_id)
    assert not statistics["billing_blocked"] and not statistics["usage_complete"]
    assert statistics["global_reserved_and_spent_cny"] == 0.5
    followup = store.reserve(run_id, 100)
    store.settle(followup, "settled", 10)
    assert store.statistics(run_id)["global_reserved_and_spent_cny"] == 0.50001
    with pytest.raises(ResearchError):
        store.acknowledge_uncertain(ticket)

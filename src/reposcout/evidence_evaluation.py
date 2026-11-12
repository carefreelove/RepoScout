"""Reproducible retrieval fixtures and reviewer negative cases."""

import json
import time

from reposcout.domain import ReviewBatch, now
from reposcout.model import create_model
from reposcout.reporting import atomic_write
from reposcout.retrieval import RepositoryIndex
from reposcout.storage import Deadline, Store
from reposcout.verification import REVIEW_PROMPT

NEGATIVES = [
    {"id": "unrelated_citation", "text": "该框架支持断点恢复。", "basis": "source",
     "content": "public String greet() { return \"Hello\"; }", "expected": "insufficient"},
    {"id": "documentation_as_test", "text": "已经实际部署并验证支持 Docker。", "basis": "documentation",
     "content": "README: We provide a Dockerfile for deployment. This document contains no execution logs.", "expected": "insufficient"},
    {"id": "version_conflict", "text": "此 POM 中 java.version 等于 8。", "basis": "source",
     "content": "<properties><java.version>17</java.version></properties>", "expected": "contradicted"},
    {"id": "outdated_maintenance", "text": "2026-11-12之前180天内有提交。", "basis": "metadata",
     "content": '{"recent_commits":[{"date":"2020-01-01T00:00:00Z"}],"complete_for_requested_window":true}', "expected": "contradicted"},
    {"id": "unsupported_performance", "text": "已独立实测单机达到10000 QPS。", "basis": "source",
     "content": "class Agent { void run() {} } // No benchmark results are provided.", "expected": "insufficient"},
    {"id": "supported_version", "text": "此 POM 声明 java.version 为 17。", "basis": "source",
     "content": "<properties><java.version>17</java.version></properties>", "expected": "supported"},
]


def evaluate_evidence(store: Store, live: bool = False):
    run_id = store.create("合成仓库资料检索回归", "offline")
    repository, commit = "fixture/retrieval", "a" * 40
    store.put(run_id, "repository", repository, {"repository": repository, "commit": commit})
    index = RepositoryIndex(store)
    documents = {"src/SqliteSaver.java": "class SqliteSaver { void checkpoint() {} }",
                 "docs/recovery.md": "任务支持断点恢复和失败重试。",
                 "docs/deploy.md": "Docker deployment requires JAVA_HOME and a JDBC connection.",
                 "README.md": "Java Agent framework supporting tool calling."}
    for path, text in documents.items():
        index.add(repository, commit, path, text)
    index.add(repository, "b" * 40, "old.md", "only_old_commit")
    queries = [("SqliteSaver", ["src/SqliteSaver.java"]), ("checkpoint", ["src/SqliteSaver.java"]),
               ("断点恢复", ["docs/recovery.md"]), ("失败重试", ["docs/recovery.md"]),
               ("Docker", ["docs/deploy.md"]), ("JAVA_HOME", ["docs/deploy.md"]),
               ("only_old_commit", []), ("not_present_anywhere", [])]
    retrieval = []
    for query, expected in queries:
        result = index.search(run_id, repository, query)
        actual = {hit["path"] for hit in result["hits"]}
        recall = len(actual & set(expected)) / len(expected) if expected else None
        retrieval.append({"query": query, "expected_paths": expected, "actual_paths": sorted(actual),
                          "recall_at_5": recall, "empty_result_correct": not actual if not expected else None,
                          "returned_bytes": result["returned_bytes"], "seconds": result["elapsed_seconds"]})
    store.update(run_id, status="completed")
    reviews = []
    for case in NEGATIVES:
        probe_id = store.create("核验负例 " + case["id"], "live" if live else "offline")
        store.put(probe_id, "purpose", "kind", "synthetic_review_evaluation")
        started = time.monotonic()
        if live:
            payload = {"request": "仅核对所给合成证据", "items": [{"target": "/probe", "text": case["text"],
                       "basis": case["basis"], "evidence_ids": ["synthetic-evidence"]}],
                       "evidence": [{"id": "synthetic-evidence", "content": case["content"]}]}
            try:
                answer = create_model(store, probe_id, Deadline(90), role="review").with_structured_output(ReviewBatch).invoke([
                    {"role": "system", "content": REVIEW_PROMPT}, {"role": "user", "content": json.dumps(payload, ensure_ascii=False)}])
                if len(answer.findings) != 1 or answer.findings[0].target != "/probe" or not set(answer.findings[0].evidence_ids) <= {"synthetic-evidence"}:
                    raise ValueError("审查结果未遵守条目与引用范围")
                actual = answer.findings[0].verdict
                reason = answer.findings[0].reason
            except Exception as exc:
                actual, reason = "error", type(exc).__name__
        else:
            actual, reason = case["expected"], "预置标签，仅用于离线协议回放"
        store.update(probe_id, status="completed" if actual == case["expected"] else "failed", elapsed=time.monotonic() - started)
        reviews.append({**case, "actual": actual, "reason": reason, "matches_expected": actual == case["expected"],
                        "mode": "live_model_synthetic_evidence" if live else "offline_protocol_replay",
                        "run_id": probe_id, "statistics": store.statistics(probe_id)})
        if live and store.statistics(probe_id)["billing_blocked"]:
            break
    value = {"suite": "evidence", "generated_at": now(), "retrieval_mode": "offline_synthetic_documents",
             "retrieval": retrieval, "reviews": reviews,
             "note": "检索采用固定合成语料；离线审查采用预置标签。--live 使用真实Pro审查合成证据，不代表真实仓库的整体正确率。"}
    value["passed"] = all(item["recall_at_5"] == 1.0 if item["expected_paths"] else item["empty_result_correct"] for item in retrieval) and all(item["matches_expected"] for item in reviews)
    path = store.settings.home / ("evidence-live.json" if live else "evidence-offline.json")
    atomic_write(path, json.dumps(value, ensure_ascii=False, indent=2))
    return path

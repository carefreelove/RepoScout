"""Evidence integrity checks and deterministic Markdown/JSON export."""

import json
import os
from pathlib import Path

from reposcout.domain import Evidence, Report, ReportDraft, ReviewSummary
from reposcout.storage import Store


def validate_draft(store: Store, run_id: str, draft: ReportDraft):
    evidence = {e["id"]: Evidence.model_validate(e) for e in store.objects(run_id, "evidence")}
    pins = {r["repository"]: r["commit"] for r in store.objects(run_id, "repository")}
    names = [c.name for c in draft.criteria]
    if len(names) != len(set(names)):
        raise ValueError("条件名称不能重复")
    repositories = [c.repository for c in draft.candidates]
    if len(repositories) != len(set(repositories)):
        raise ValueError("候选仓库不能重复")
    if pins and not draft.candidates:
        raise ValueError("已读取仓库证据，报告必须包含候选分析")
    if not draft.candidates and not store.objects(run_id, "search"):
        raise ValueError("空候选报告必须先执行搜索")
    for candidate in draft.candidates:
        if candidate.repository not in pins:
            raise ValueError("候选必须经过 inspect_repository")
        assessments = {a.criterion: a for a in candidate.assessments}
        if set(assessments) != set(names) or len(assessments) != len(candidate.assessments):
            raise ValueError("每个候选必须逐项评估全部条件")
        required = [assessments[c.name].verdict for c in draft.criteria if c.required]
        if candidate.decision == "推荐" and any(x != "满足" for x in required):
            raise ValueError("硬性条件未全部满足时只能排除或待确认")
        groups = [candidate.evidence_ids]
        if not candidate.evidence_ids:
            raise ValueError("推荐或排除理由需要证据")
        for assessment in candidate.assessments:
            if assessment.verdict != "未确认" and not assessment.evidence_ids:
                raise ValueError("确定的条件判定需要证据")
            groups.append(assessment.evidence_ids)
        for claim in candidate.claims:
            if claim.basis != "unknown" and not claim.evidence_ids:
                raise ValueError("确定事实需要证据")
            groups.append(claim.evidence_ids)
            if claim.basis == "source" and not any(
                evidence.get(eid) and evidence[eid].kind in ("file", "tree") for eid in claim.evidence_ids
            ):
                raise ValueError(f"源码事实需要文件或目录证据，问题条目为 {claim.text[:100]}")
        for group in groups:
            for eid in group:
                item = evidence.get(eid)
                if item is None:
                    raise ValueError("引用了不存在的证据 ID")
                if item.repository != candidate.repository or item.commit != pins[candidate.repository]:
                    raise ValueError("证据与候选仓库或固定 commit 不一致")


def build_report(store: Store, run_id: str) -> Report:
    run = store.run(run_id)
    if run["draft"]:
        draft = ReportDraft.model_validate_json(run["draft"])
        validate_draft(store, run_id, draft)
    else:
        # Export collected evidence even if the model stopped before producing a valid report.
        draft = ReportDraft(interpreted_request=run["request"], criteria=[{"name": "原始需求"}],
                            candidates=[], conclusion="调研中断，现有证据已保存，尚未形成有效比较结论。",
                            unknowns=["候选条件判定尚未完成"])
    errors = [e for e in store.events(run_id) if e["code"] not in ("stage", "submitted")]
    return Report(**draft.model_dump(), run_id=run_id, original_request=run["request"],
                  schema_version=store.get(run_id, "format", "schema_version") or "1.0",
                  review=ReviewSummary.model_validate(store.get(run_id, "review", "current") or {}),
                  status=run["status"], execution_mode=run["mode"],
                  commits={r["repository"]: r["commit"] for r in store.objects(run_id, "repository")},
                  evidence=store.objects(run_id, "evidence"), errors=errors,
                  statistics=store.statistics(run_id))


def markdown(report: Report) -> str:
    links = {e.id: f"[{e.id}]({e.url})" for e in report.evidence}

    def refs(ids):
        return " ".join(links[eid] for eid in ids)

    lines = ["# RepoScout 调研报告", "", report.original_request, "",
             f"任务 `{report.run_id}` · 状态 `{report.status}` · 模式 `{report.execution_mode}`", "",
             f"生成时间 `{report.generated_at}` · 维护判断窗口 {report.maintenance_window_days} 天", "",
             "## 需求与条件", "", report.interpreted_request, ""]
    lines += [f"- {c.name}（{'硬性条件' if c.required else '偏好'}）" for c in report.criteria]
    for candidate in report.candidates:
        lines += ["", f"## {candidate.repository}", "", candidate.summary, "",
                  f"固定 commit `{report.commits[candidate.repository]}`", ""]
        for assessment in candidate.assessments:
            lines += [f"- **{assessment.criterion} · {assessment.verdict}**。{assessment.reason} {refs(assessment.evidence_ids)}"]
        lines += ["", f"**{candidate.decision}**。{candidate.decision_reason} {refs(candidate.evidence_ids)}", ""]
        lines += [f"- {claim.text}（依据 `{claim.basis}`） {refs(claim.evidence_ids)}" for claim in candidate.claims]
        lines += [f"- 未确认项 — {item}" for item in candidate.unknowns]
    lines += ["", "## 结论", "", report.conclusion, "", "## 未确认项", ""]
    lines += [f"- {item}" for item in report.unknowns] or ["无额外未确认项。"]
    if report.schema_version == "1.1":
        lines += ["", "## 模型辅助核验", "",
                  f"状态 `{report.review.status}` · 模型 `{report.review.model}` · 核验 {report.review.rounds} 轮 · 补证 {report.review.supplement_rounds} 轮", "",
                  report.review.note, ""]
        lines += [f"- `{item.target}` · `{item.verdict}` · {item.reason}" for item in report.review.findings if item.verdict != "supported"]
    lines += ["", "## 证据索引", ""]
    for item in report.evidence:
        lines += [f"- {links[item.id]} · {item.summary} · 读取时间 `{item.retrieved_at}`"
                  + (" · 内容已截断" if item.truncated else "")]
    lines += ["", "## 执行统计", "", "```json", json.dumps(report.statistics, ensure_ascii=False, indent=2), "```"]
    if report.errors:
        lines += ["", "## 异常记录", ""]
        lines += [f"- `{error['code']}` {error['detail']}" for error in report.errors]
    return "\n".join(lines) + "\n"


def atomic_write(path: Path, text: str):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def export(store: Store, run_id: str) -> Path:
    report = build_report(store, run_id)
    directory = store.settings.home / "runs" / run_id
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    atomic_write(directory / "report.json", report.model_dump_json(indent=2))
    atomic_write(directory / "report.md", markdown(report))
    atomic_write(directory / "events.jsonl", "".join(json.dumps(e, ensure_ascii=False) + "\n" for e in store.events(run_id)))
    if report.schema_version == "1.1":
        atomic_write(directory / "review.json", json.dumps({"current": report.review.model_dump(),
                     "history": store.objects(run_id, "review_history")}, ensure_ascii=False, indent=2))
    return directory

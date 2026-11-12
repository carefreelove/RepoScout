"""Validated public report structures."""

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


def now() -> str:
    return datetime.now(UTC).isoformat()


class Record(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Evidence(Record):
    id: str
    repository: str | None = None
    kind: Literal["search", "metadata", "maintenance", "tree", "file"]
    url: str
    retrieved_at: str = Field(default_factory=now)
    commit: str | None = None
    path: str | None = None
    start_line: int | None = None
    end_line: int | None = None
    query: str | None = None
    summary: str
    content: str
    truncated: bool = False


class Criterion(Record):
    name: str
    required: bool = True


class Claim(Record):
    text: str
    basis: Literal["metadata", "source", "documentation", "unknown"]
    evidence_ids: list[str]


class Assessment(Record):
    criterion: str
    verdict: Literal["满足", "不满足", "未确认"]
    reason: str
    evidence_ids: list[str]


class Candidate(Record):
    repository: str
    summary: str
    claims: list[Claim] = Field(default_factory=list)
    assessments: list[Assessment]
    decision: Literal["推荐", "排除", "待确认"]
    decision_reason: str
    evidence_ids: list[str] = Field(min_length=1)
    unknowns: list[str] = Field(default_factory=list)


class ReportDraft(Record):
    interpreted_request: str
    criteria: list[Criterion] = Field(min_length=1)
    maintenance_window_days: int = Field(default=180, ge=1, le=3650)
    candidates: list[Candidate]
    conclusion: str
    unknowns: list[str] = Field(default_factory=list)


class Finding(Record):
    target: str
    verdict: Literal["supported", "insufficient", "contradicted"]
    reason: str
    evidence_ids: list[str]
    needed_query: str = ""


class ReviewBatch(Record):
    findings: list[Finding]


class ReviewSummary(Record):
    status: Literal["not_reviewed", "pending", "passed", "needs_evidence", "failed", "stopped"] = "not_reviewed"
    model: str = ""
    rounds: int = 0
    supplement_rounds: int = 0
    draft_hash: str = ""
    findings: list[Finding] = Field(default_factory=list)
    note: str = "模型辅助审查，事实语义需结合引用原文复核"


class Report(ReportDraft):
    schema_version: Literal["1.0", "1.1"] = "1.1"
    run_id: str
    original_request: str
    generated_at: str = Field(default_factory=now)
    status: str
    execution_mode: Literal["live", "offline"]
    commits: dict[str, str]
    evidence: list[Evidence]
    errors: list[dict]
    statistics: dict
    review: ReviewSummary = Field(default_factory=ReviewSummary)


class ResearchError(Exception):
    """A recoverable, user-visible research interruption."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code

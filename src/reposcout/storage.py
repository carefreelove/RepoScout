"""SQLite persistence, atomic budget accounting and per-run process locks."""

import fcntl
import json
import os
import sqlite3
import time
import uuid
from collections.abc import Callable
from contextlib import contextmanager

from reposcout.domain import Evidence, ResearchError, now
from reposcout.settings import Settings


class Store:
    def __init__(self, settings: Settings, on_event: Callable[[str], None] | None = None):
        self.settings = settings
        self.on_event = on_event
        settings.home.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.path = settings.home / "state.sqlite"
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY, request TEXT NOT NULL, status TEXT NOT NULL,
                    mode TEXT NOT NULL, created_at TEXT NOT NULL, config TEXT NOT NULL,
                    draft TEXT, github_requests INTEGER NOT NULL DEFAULT 0,
                    elapsed REAL NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS objects (
                    run_id TEXT, kind TEXT, key TEXT, value TEXT NOT NULL,
                    PRIMARY KEY(run_id, kind, key)
                );
                CREATE TABLE IF NOT EXISTS events (
                    seq INTEGER PRIMARY KEY, run_id TEXT, at TEXT, code TEXT, detail TEXT
                );
                CREATE TABLE IF NOT EXISTS ledger (
                    id TEXT PRIMARY KEY, run_id TEXT, state TEXT, cost INTEGER,
                    input_tokens INTEGER DEFAULT 0, output_tokens INTEGER DEFAULT 0,
                    at TEXT
                );
            """)
            db.execute("BEGIN IMMEDIATE")
            columns = {row[1] for row in db.execute("PRAGMA table_info(ledger)")}
            additions = {"model": "TEXT NOT NULL DEFAULT 'deepseek-flash'",
                         "role": "TEXT NOT NULL DEFAULT 'research'",
                         "input_rate": "INTEGER NOT NULL DEFAULT 2",
                         "output_rate": "INTEGER NOT NULL DEFAULT 8",
                         "price_date": "TEXT NOT NULL DEFAULT '2026-11-12'"}
            for column, declaration in additions.items():
                if column not in columns:
                    db.execute(f"ALTER TABLE ledger ADD COLUMN {column} {declaration}")
        os.chmod(self.path, 0o600)

    @contextmanager
    def connect(self):
        db = sqlite3.connect(self.path, timeout=10)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA busy_timeout=10000")
        try:
            with db:
                yield db
        finally:
            db.close()

    def create(self, request: str, mode: str = "live") -> str:
        run_id = uuid.uuid4().hex[:12]
        with self.connect() as db:
            db.execute("INSERT INTO runs(id,request,status,mode,created_at,config) VALUES(?,?,?,?,?,?)",
                       (run_id, request, "running", mode, now(), self.settings.model_dump_json()))
        self.put(run_id, "format", "schema_version", "1.1")
        return run_id

    def run(self, run_id: str) -> dict:
        with self.connect() as db:
            row = db.execute("SELECT * FROM runs WHERE id=?", (run_id,)).fetchone()
        if row is None:
            raise ResearchError("not_found", "任务不存在")
        return dict(row)

    def update(self, run_id: str, **values):
        allowed = {"status", "draft", "elapsed"}
        if not values.keys() <= allowed:
            raise ValueError("Unsupported run fields")
        with self.connect() as db:
            db.execute(f"UPDATE runs SET {','.join(f'{key}=?' for key in values)} WHERE id=?",
                       (*values.values(), run_id))

    def put(self, run_id: str, kind: str, key: str, value):
        with self.connect() as db:
            db.execute("INSERT OR REPLACE INTO objects VALUES(?,?,?,?)",
                       (run_id, kind, key, json.dumps(value, ensure_ascii=False)))

    def get(self, run_id: str, kind: str, key: str):
        with self.connect() as db:
            row = db.execute("SELECT value FROM objects WHERE run_id=? AND kind=? AND key=?",
                             (run_id, kind, key)).fetchone()
        return json.loads(row[0]) if row else None

    def objects(self, run_id: str, kind: str) -> list:
        with self.connect() as db:
            rows = db.execute("SELECT value FROM objects WHERE run_id=? AND kind=? ORDER BY key",
                              (run_id, kind)).fetchall()
        return [json.loads(row[0]) for row in rows]

    def evidence(self, run_id: str, **values) -> dict:
        item = Evidence(id="ev-" + uuid.uuid4().hex[:12], **values).model_dump()
        self.put(run_id, "evidence", item["id"], item)
        return item

    def event(self, run_id: str, code: str, detail: str):
        # Callers supply bounded, classified messages, never raw HTTP exceptions or prompts.
        with self.connect() as db:
            db.execute("INSERT INTO events(run_id,at,code,detail) VALUES(?,?,?,?)",
                       (run_id, now(), code, detail[:2000]))
        if self.on_event and code in ("stage", "review_issues"):
            self.on_event(detail[:500])

    def events(self, run_id: str) -> list[dict]:
        with self.connect() as db:
            return [dict(row) for row in db.execute(
                "SELECT at,code,detail FROM events WHERE run_id=? ORDER BY seq", (run_id,))]

    def github_request(self, run_id: str):
        with self.connect() as db:
            cursor = db.execute("UPDATE runs SET github_requests=github_requests+1 WHERE id=? AND github_requests<?",
                                (run_id, self.settings.max_github_requests))
            if cursor.rowcount != 1:
                raise ResearchError("github_budget", "GitHub 请求次数达到上限")

    def reserve(self, run_id: str, cost: int, model: str = "deepseek-flash",
                role: str = "research", input_rate: int = 2, output_rate: int = 8) -> str:
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            blocking = db.execute("SELECT id,state FROM ledger WHERE state IN ('pending','uncertain') LIMIT 1").fetchone()
            if blocking:
                raise ResearchError("uncertain_usage", f"存在未确认模型用量，记录 {blocking['id']}，状态 {blocking['state']}，已暂停新的付费调用")
            spent = db.execute("SELECT COALESCE(SUM(cost),0) FROM ledger").fetchone()[0]
            calls = db.execute("SELECT COUNT(*) FROM ledger WHERE run_id=?", (run_id,)).fetchone()[0]
            if calls >= self.settings.max_model_calls:
                raise ResearchError("model_budget", "模型调用次数达到上限")
            if spent + cost > int(self.settings.max_cost_cny * 1_000_000):
                raise ResearchError("cost_budget", "累计费用预算不足以预留下一次调用")
            ticket = uuid.uuid4().hex
            db.execute("INSERT INTO ledger(id,run_id,state,cost,at,model,role,input_rate,output_rate,price_date) VALUES(?,?,?,?,?,?,?,?,?,?)",
                       (ticket, run_id, "pending", cost, now(), model, role, input_rate, output_rate, "2026-11-12"))
            return ticket

    def settle(self, ticket: str, state: str, cost: int | None = None,
               input_tokens: int = 0, output_tokens: int = 0):
        with self.connect() as db:
            db.execute("UPDATE ledger SET state=?,cost=COALESCE(?,cost),input_tokens=?,output_tokens=? WHERE id=?",
                       (state, cost, input_tokens, output_tokens, ticket))

    def acknowledge_uncertain(self, ticket: str) -> int:
        """Keep the full reserved upper bound after an explicit operator decision."""
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT run_id,state,cost FROM ledger WHERE id=?", (ticket,)).fetchone()
            if row is None or row["state"] != "uncertain":
                raise ResearchError("invalid_ticket", "该记录不存在或不处于用量待确认状态")
            db.execute("UPDATE ledger SET state='reserved_unknown' WHERE id=?", (ticket,))
        self.event(row["run_id"], "budget_acknowledged", f"人工接受最高预留 {row['cost'] / 1e6:.6f} 元，实际用量仍未确认")
        return row["cost"]

    def statistics(self, run_id: str) -> dict:
        with self.connect() as db:
            row = db.execute("SELECT COUNT(*) calls,COALESCE(SUM(cost),0) cost,COALESCE(SUM(input_tokens),0) input_tokens,COALESCE(SUM(output_tokens),0) output_tokens FROM ledger WHERE run_id=?", (run_id,)).fetchone()
            total = db.execute("SELECT COALESCE(SUM(cost),0) FROM ledger").fetchone()[0]
            uncertain = db.execute("SELECT COUNT(*) FROM ledger WHERE state IN ('pending','uncertain','reserved_unknown')").fetchone()[0]
            blocked = db.execute("SELECT COUNT(*) FROM ledger WHERE state IN ('pending','uncertain')").fetchone()[0]
            run_unknown = db.execute("SELECT COUNT(*) FROM ledger WHERE run_id=? AND state IN ('pending','uncertain','reserved_unknown')", (run_id,)).fetchone()[0]
            roles = [dict(item) for item in db.execute(
                "SELECT model,role,COUNT(*) calls,SUM(cost)/1000000.0 cost_cny,SUM(input_tokens) input_tokens,SUM(output_tokens) output_tokens FROM ledger WHERE run_id=? GROUP BY model,role", (run_id,))]
        return {"model_calls": row["calls"], "input_tokens": row["input_tokens"],
                "output_tokens": row["output_tokens"], "estimated_cost_cny_upper_bound": row["cost"] / 1e6,
                "global_reserved_and_spent_cny": total / 1e6, "unconfirmed_calls": uncertain,
                "billing_blocked": bool(blocked), "usage_complete": run_unknown == 0,
                "run_unconfirmed_calls": run_unknown,
                "github_requests": self.run(run_id)["github_requests"],
                "elapsed_seconds": round(self.run(run_id)["elapsed"], 3), "models": roles,
                "retrieval": self.get(run_id, "retrieval", "statistics") or {}}

    @contextmanager
    def lock(self, run_id: str):
        self.run(run_id)
        with (self.settings.home / f"{run_id}.lock").open("w") as handle:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise ResearchError("run_locked", "该任务已由其他进程执行") from exc
            try:
                yield
            finally:
                fcntl.flock(handle, fcntl.LOCK_UN)


class Deadline:
    def __init__(self, seconds: float):
        self.end = time.monotonic() + seconds

    def check(self):
        if time.monotonic() >= self.end:
            raise ResearchError("timeout", "任务运行时间达到上限")

    def remaining(self) -> float:
        self.check()
        return self.end - time.monotonic()

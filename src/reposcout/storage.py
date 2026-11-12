"""SQLite persistence, atomic budget accounting and per-run process locks."""

import fcntl
import json
import os
import sqlite3
import time
import uuid
from contextlib import contextmanager

from reposcout.domain import Evidence, ResearchError, now
from reposcout.settings import Settings


class Store:
    def __init__(self, settings: Settings):
        self.settings = settings
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

    def reserve(self, run_id: str, cost: int) -> str:
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            if db.execute("SELECT 1 FROM ledger WHERE state IN ('pending','uncertain') LIMIT 1").fetchone():
                raise ResearchError("uncertain_usage", "存在未确认模型用量，已暂停新的付费调用")
            spent = db.execute("SELECT COALESCE(SUM(cost),0) FROM ledger").fetchone()[0]
            calls = db.execute("SELECT COUNT(*) FROM ledger WHERE run_id=?", (run_id,)).fetchone()[0]
            if calls >= self.settings.max_model_calls:
                raise ResearchError("model_budget", "模型调用次数达到上限")
            if spent + cost > int(self.settings.max_cost_cny * 1_000_000):
                raise ResearchError("cost_budget", "累计费用预算不足以预留下一次调用")
            ticket = uuid.uuid4().hex
            db.execute("INSERT INTO ledger(id,run_id,state,cost,at) VALUES(?,?,?,?,?)",
                       (ticket, run_id, "pending", cost, now()))
            return ticket

    def settle(self, ticket: str, state: str, cost: int | None = None,
               input_tokens: int = 0, output_tokens: int = 0):
        with self.connect() as db:
            db.execute("UPDATE ledger SET state=?,cost=COALESCE(?,cost),input_tokens=?,output_tokens=? WHERE id=?",
                       (state, cost, input_tokens, output_tokens, ticket))

    def statistics(self, run_id: str) -> dict:
        with self.connect() as db:
            row = db.execute("SELECT COUNT(*) calls,COALESCE(SUM(cost),0) cost,COALESCE(SUM(input_tokens),0) input_tokens,COALESCE(SUM(output_tokens),0) output_tokens FROM ledger WHERE run_id=?", (run_id,)).fetchone()
            total = db.execute("SELECT COALESCE(SUM(cost),0) FROM ledger").fetchone()[0]
            uncertain = db.execute("SELECT COUNT(*) FROM ledger WHERE state IN ('pending','uncertain')").fetchone()[0]
        return {"model_calls": row["calls"], "input_tokens": row["input_tokens"],
                "output_tokens": row["output_tokens"], "estimated_cost_cny_upper_bound": row["cost"] / 1e6,
                "global_reserved_and_spent_cny": total / 1e6, "unconfirmed_calls": uncertain,
                "github_requests": self.run(run_id)["github_requests"],
                "elapsed_seconds": round(self.run(run_id)["elapsed"], 3)}

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

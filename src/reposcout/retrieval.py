"""Commit-scoped document chunks and SQLite FTS5/BM25 retrieval."""

import hashlib
import json
import re
import time
from urllib.parse import quote

from reposcout.domain import ResearchError, now
from reposcout.storage import Store


class RepositoryIndex:
    def __init__(self, store: Store):
        self.store = store
        with store.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS source_documents (
                    id INTEGER PRIMARY KEY, repository TEXT, commit_sha TEXT, path TEXT,
                    content TEXT, digest TEXT, retrieved_at TEXT, source_start INTEGER,
                    is_fragment INTEGER NOT NULL DEFAULT 0,
                    UNIQUE(repository,commit_sha,path,source_start,is_fragment,digest)
                );
                CREATE TABLE IF NOT EXISTS source_chunks (
                    id INTEGER PRIMARY KEY, document_id INTEGER NOT NULL,
                    start_line INTEGER, end_line INTEGER, body TEXT, truncated INTEGER,
                    UNIQUE(document_id,start_line)
                );
                CREATE VIRTUAL TABLE IF NOT EXISTS source_fts USING fts5(path,body);
            """)

    def summary(self, repository: str, commit: str) -> dict:
        with self.store.connect() as db:
            paths = [row[0] for row in db.execute("SELECT DISTINCT path FROM source_documents WHERE repository=? AND commit_sha=? ORDER BY path", (repository, commit))]
        return {"paths": paths[:20], "count": len(paths), "truncated": len(paths) > 20}

    def add(self, repository: str, commit: str, path: str, content: str,
            retrieved_at: str | None = None, start_line: int = 1, fragment: bool = False):
        digest = hashlib.sha256(content.encode()).hexdigest()
        with self.store.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            condition = " AND digest=?" if fragment else ""
            values = (repository, commit, path, start_line, int(fragment))
            if fragment:
                values += (digest,)
            existing = db.execute("SELECT id,digest FROM source_documents WHERE repository=? AND commit_sha=? AND path=? AND source_start=? AND is_fragment=?" + condition, values).fetchone()
            if existing:
                if existing["digest"] != digest:
                    raise ResearchError("immutable_source", "同一 commit 的文件内容不一致，已停止更新索引")
                return
            cursor = db.execute("INSERT INTO source_documents(repository,commit_sha,path,content,digest,retrieved_at,source_start,is_fragment) VALUES(?,?,?,?,?,?,?,?)",
                                (repository, commit, path, content, digest, retrieved_at or now(), start_line, int(fragment)))
            document_id = cursor.lastrowid
            for first, last, body, truncated in chunks(content, start_line):
                cursor = db.execute("INSERT INTO source_chunks(document_id,start_line,end_line,body,truncated) VALUES(?,?,?,?,?)",
                                    (document_id, first, last, body, truncated))
                db.execute("INSERT INTO source_fts(rowid,path,body) VALUES(?,?,?)", (cursor.lastrowid, path, body))

    def legacy(self, run_id: str, repository: str, commit: str):
        """Index older line-numbered evidence without inventing missing source lines."""
        for item in self.store.objects(run_id, "evidence"):
            if item["kind"] != "file" or item["repository"] != repository or item["commit"] != commit:
                continue
            key = item["path"]
            with self.store.connect() as db:
                present = db.execute("SELECT 1 FROM source_documents WHERE repository=? AND commit_sha=? AND path=? AND is_fragment=0",
                                     (repository, commit, key)).fetchone()
            if present:
                continue
            lines = [re.sub(r"^\d+: ", "", line) for line in item["content"].splitlines()]
            self.add(repository, commit, key, "\n".join(lines), item["retrieved_at"],
                     item["start_line"] or 1, fragment=True)

    def search(self, run_id: str, repository: str, query: str, limit: int = 5) -> dict:
        started = time.monotonic()
        pin = self.store.get(run_id, "repository", repository)
        if not pin:
            raise ResearchError("not_pinned", "请先固定仓库 commit")
        if not query.strip() or len(query) > 256 or not 1 <= limit <= 5:
            raise ResearchError("invalid_query", "检索词长度应为 1 至 256，返回条数应为 1 至 5")
        commit = pin["commit"]
        self.legacy(run_id, repository, commit)
        terms = re.findall(r"\w+", query, flags=re.UNICODE)[:16]
        if not terms:
            raise ResearchError("invalid_query", "检索词至少包含一个文字或标识符")
        match = " OR ".join('"' + term.replace('"', '""') + '"' for term in terms)
        base = "SELECT c.*,d.path,d.retrieved_at,d.is_fragment,d.content AS source_content FROM source_chunks c JOIN source_documents d ON d.id=c.document_id "
        scope = "d.repository=? AND d.commit_sha=? AND (d.is_fragment=0 OR NOT EXISTS (SELECT 1 FROM source_documents complete WHERE complete.repository=d.repository AND complete.commit_sha=d.commit_sha AND complete.path=d.path AND complete.is_fragment=0))"
        with self.store.connect() as db:
            rows = list(db.execute(base + f"JOIN source_fts ON source_fts.rowid=c.id WHERE source_fts MATCH ? AND {scope} ORDER BY bm25(source_fts),c.id LIMIT ?",
                                   (match, repository, commit, limit)))
            # Substring matching supports short Chinese terms and fragments of code identifiers.
            clauses = " OR ".join("(c.body LIKE ? ESCAPE '\\' OR d.path LIKE ? ESCAPE '\\')" for _ in terms)
            parameters = []
            for term in terms:
                escaped = term.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
                parameters.extend((f"%{escaped}%", f"%{escaped}%"))
            fallback = db.execute(base + f"WHERE {scope} AND ({clauses}) ORDER BY c.id LIMIT ?",
                                  (repository, commit, *parameters, limit)).fetchall()
            count = db.execute("SELECT COUNT(DISTINCT path) FROM source_documents WHERE repository=? AND commit_sha=?", (repository, commit)).fetchone()[0]
        ids = {row["id"] for row in rows}
        rows += [row for row in fallback if row["id"] not in ids]
        results, used_bytes = [], 0
        for row in rows[:limit]:
            path = row["path"]
            content = "\n".join(f"{i}: {line}" for i, line in enumerate(row["body"].splitlines(), row["start_line"]))
            if used_bytes + len(content.encode()) > 16000:
                break
            used_bytes += len(content.encode())
            key = f"{repository}:{commit}:{row['id']}"
            item = self.store.get(run_id, "retrieval_evidence", key)
            if item is None:
                item = self.store.evidence(run_id, repository=repository, kind="file", commit=commit,
                    path=path, start_line=row["start_line"], end_line=row["end_line"],
                    retrieved_at=row["retrieved_at"], query=query,
                    url=f"https://github.com/{repository}/blob/{commit}/{quote(path, safe='/')}#L{row['start_line']}-L{row['end_line']}",
                    summary=f"全文检索命中 {path} 第 {row['start_line']} 至 {row['end_line']} 行",
                    content=content, truncated=bool(row["truncated"]) or bool(row["is_fragment"]) or row["start_line"] > 1 or row["end_line"] < len(row["source_content"].splitlines()))
                self.store.put(run_id, "retrieval_evidence", key, item)
            results.append(item)
        elapsed = time.monotonic() - started
        metrics = self.store.get(run_id, "retrieval", "statistics") or {"queries": 0, "returned_bytes": 0, "seconds": 0}
        metrics["queries"] += 1
        metrics["returned_bytes"] += used_bytes
        metrics["seconds"] = round(metrics["seconds"] + elapsed, 6)
        self.store.put(run_id, "retrieval", "statistics", metrics)
        self.store.event(run_id, "retrieval", json.dumps({"repository": repository, "query": query, "hits": len(results), "bytes": used_bytes}, ensure_ascii=False))
        return {"query": query, "repository": repository, "commit": commit, "indexed_documents": count,
                "scope": "已采集的固定 commit 文本", "hits": results, "returned_bytes": used_bytes,
                "truncated": len(results) < len(rows), "elapsed_seconds": round(elapsed, 6)}


def chunks(content: str, start_line: int = 1):
    lines = content.splitlines()
    start = 0
    while start < len(lines):
        selected, size = [], 0
        for line in lines[start:start + 80]:
            byte_count = len(line.encode()) + 1
            if size + byte_count > 8000:
                break
            selected.append(line)
            size += byte_count
        truncated = False
        if not selected:
            selected = [lines[start].encode()[:7999].decode("utf-8", errors="ignore")]
            truncated = True
        end = start + len(selected)
        yield start_line + start, start_line + end - 1, "\n".join(selected), truncated
        if end >= len(lines):
            break
        start = max(start + 1, end - 10)

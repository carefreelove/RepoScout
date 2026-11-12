"""Read-only GitHub REST tools with bounded, commit-pinned evidence."""

import base64
import binascii
import fnmatch
import hashlib
import json
import os
import re
import time
from urllib.parse import quote, urlencode

import httpx

from reposcout.domain import ResearchError
from reposcout.retrieval import RepositoryIndex
from reposcout.storage import Deadline, Store

REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
SHA = re.compile(r"[0-9a-f]{40}\Z")


class GitHub:
    def __init__(self, store: Store, run_id: str, deadline: Deadline,
                 transport: httpx.BaseTransport | None = None):
        self.store, self.run_id, self.deadline = store, run_id, deadline
        headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
                   "User-Agent": "RepoScout/0.2.0"}
        if token := os.getenv("GITHUB_TOKEN"):
            headers["Authorization"] = "Bearer " + token
        self.client = httpx.Client(base_url="https://api.github.com", headers=headers,
                                   transport=transport, follow_redirects=False)

    def close(self):
        self.client.close()

    def request(self, path: str, params: dict | None = None):
        self.deadline.check()
        key = path + "?" + urlencode(sorted((params or {}).items()))
        cached = self.store.get(self.run_id, "cache", key)
        if cached is not None:
            return cached
        for attempt in range(3):
            self.deadline.check()
            self.store.github_request(self.run_id)
            try:
                # Bound the HTTP body before decoding JSON, including base64 blobs and trees.
                with self.client.stream("GET", path, params=params,
                                        timeout=min(15, self.deadline.remaining())) as response:
                    body = bytearray()
                    for chunk in response.iter_bytes():
                        self.deadline.check()
                        body.extend(chunk)
                        if len(body) > 2_000_000:
                            raise ResearchError("response_too_large", "GitHub 响应超过 2 MB 限制")
                    status, headers = response.status_code, response.headers
            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                if attempt == 2:
                    raise ResearchError("network", "GitHub 网络请求失败，已重试 2 次") from exc
                self.pause(2 ** attempt)
                continue
            if status == 404:
                raise ResearchError("not_found", "仓库或文件不存在，或当前凭据无法读取")
            limited = status == 429 or (status == 403 and (
                headers.get("x-ratelimit-remaining") == "0" or "retry-after" in headers
                or b"rate limit" in bytes(body).lower()))
            if limited or status >= 500:
                if attempt == 2:
                    raise ResearchError("rate_limit" if limited else "github_unavailable", "GitHub 暂时不可用，已保存任务，可稍后恢复")
                delay = self.retry_delay(headers, attempt)
                if delay > 5 or delay >= self.deadline.remaining():
                    raise ResearchError("rate_limit", "GitHub 要求较长等待，已保存任务，可稍后恢复")
                self.pause(delay)
                continue
            if status != 200:
                raise ResearchError("github_http", f"GitHub 返回 HTTP {status}")
            try:
                result = json.loads(body)
            except ValueError as exc:
                raise ResearchError("github_format", "GitHub 返回无法解析的数据") from exc
            self.store.put(self.run_id, "cache", key, result)
            return result
        raise AssertionError("unreachable")

    @staticmethod
    def retry_delay(headers: httpx.Headers, attempt: int) -> float:
        try:
            if "retry-after" in headers:
                return max(0, float(headers["retry-after"]))
            if "x-ratelimit-reset" in headers:
                return max(0, float(headers["x-ratelimit-reset"]) - time.time() + 1)
        except ValueError:
            return 60  # Unknown server delay must not trigger an immediate retry.
        return 2 ** attempt

    def pause(self, seconds: float):
        self.deadline.check()
        time.sleep(min(seconds, self.deadline.remaining()))
        self.deadline.check()

    @staticmethod
    def validate_repository(repository: str):
        if not REPOSITORY.fullmatch(repository):
            raise ResearchError("invalid_repository", "仓库必须使用 owner/name 格式")

    def search(self, query: str) -> dict:
        if not query.strip() or len(query) > 256:
            raise ResearchError("invalid_query", "搜索表达式长度必须为 1 至 256")
        key = hashlib.sha256(query.encode()).hexdigest()
        if previous := self.store.get(self.run_id, "search", key):
            return previous
        seen = {item["full_name"] for search in self.store.objects(self.run_id, "search") for item in search["items"]}
        remaining = self.store.settings.search_limit - len(seen)
        if remaining <= 0:
            raise ResearchError("search_limit", "候选数量达到上限，请分析已有候选")
        result = self.request("/search/repositories", {"q": query, "per_page": remaining,
                                                       "sort": "updated", "order": "desc"})
        items = [{key: item.get(key) for key in (
            "full_name", "description", "language", "stargazers_count", "archived", "pushed_at")}
            for item in result.get("items", []) if not item.get("private", False)]
        evidence = self.store.evidence(self.run_id, kind="search", query=query,
            url="https://github.com/search?" + urlencode({"q": query, "type": "repositories"}),
            summary=f"GitHub 搜索，返回 {len(items)} 个公开候选",
            content=json.dumps(items, ensure_ascii=False), truncated=bool(result.get("incomplete_results")))
        value = {"query": query, "items": items, "evidence_id": evidence["id"]}
        self.store.put(self.run_id, "search", key, value)
        return value

    def inspect(self, repository: str) -> dict:
        self.validate_repository(repository)
        if existing := self.store.get(self.run_id, "repository", repository):
            return existing if "maintenance" in existing else self.maintenance(repository)
        if len(self.store.objects(self.run_id, "repository")) >= self.store.settings.analyze_limit:
            raise ResearchError("analysis_limit", "深入分析的仓库数量达到上限")
        data = self.request(f"/repos/{repository}")
        if data.get("private", True):
            raise ResearchError("private_repository", "仅支持公开仓库")
        commits = self.request(f"/repos/{repository}/commits", {"per_page": 5})
        if not commits or not SHA.fullmatch(commits[0].get("sha", "")):
            raise ResearchError("empty_repository", "仓库缺少可固定的 commit")
        sha = commits[0]["sha"]
        metadata = {key: data.get(key) for key in (
            "full_name", "description", "language", "archived", "disabled", "license",
            "pushed_at", "updated_at", "stargazers_count", "default_branch", "open_issues_count")}
        ev = self.store.evidence(self.run_id, repository=repository, kind="metadata",
            url=f"https://github.com/{repository}", commit=sha,
            summary="仓库元数据快照，状态适用于读取时间", content=json.dumps(metadata, ensure_ascii=False))
        value = {"repository": repository, "commit": sha, "metadata": metadata,
                 "evidence_ids": [ev["id"]]}
        # Persist the pin before optional release/maintenance requests can fail.
        self.store.put(self.run_id, "repository", repository, value)
        return self.maintenance(repository)

    def pinned(self, repository: str) -> dict:
        self.validate_repository(repository)
        value = self.store.get(self.run_id, "repository", repository)
        if not value:
            raise ResearchError("not_pinned", "请先调用 inspect_repository 固定仓库 commit")
        return value

    def maintenance(self, repository: str) -> dict:
        value = self.pinned(repository)
        if "maintenance" in value:
            return value
        commits = self.request(f"/repos/{repository}/commits", {"sha": value["commit"], "per_page": 5})
        releases = self.request(f"/repos/{repository}/releases", {"per_page": 3})
        info = {"recent_commits": [{"sha": c["sha"], "date": c["commit"]["committer"]["date"],
                                   "message": c["commit"]["message"][:300]} for c in commits],
                "recent_releases": [{"tag": r["tag_name"], "published_at": r["published_at"],
                                     "prerelease": r["prerelease"]} for r in releases]}
        ev = self.store.evidence(self.run_id, repository=repository, kind="maintenance",
            url=f"https://github.com/{repository}/commits/{value['commit']}", commit=value["commit"],
            summary="近期提交及 release 快照，维护判断需结合时间窗口", content=json.dumps(info, ensure_ascii=False))
        value["maintenance"] = info
        value["evidence_ids"].append(ev["id"])
        self.store.put(self.run_id, "repository", repository, value)
        return value

    def tree(self, repository: str) -> dict:
        pin = self.pinned(repository)
        data = self.request(f"/repos/{repository}/git/trees/{pin['commit']}", {"recursive": 1})
        entries = [{"path": x["path"], "type": x["type"], "size": x.get("size")}
                   for x in data.get("tree", [])[:300]]
        ev = self.store.evidence(self.run_id, repository=repository, kind="tree", commit=pin["commit"],
            url=f"https://github.com/{repository}/tree/{pin['commit']}", summary="最多展示前 300 个目录项",
            content=json.dumps(entries, ensure_ascii=False),
            truncated=bool(data.get("truncated")) or len(data.get("tree", [])) > 300)
        return ev

    def file(self, repository: str, path: str, start_line: int = 1, end_line: int = 120) -> dict:
        pin = self.pinned(repository)
        if not path or len(path) > 512 or path.startswith("/") or any(p in ("..", ".", "") for p in path.split("/")):
            raise ResearchError("invalid_path", "请使用仓库内的相对文件路径")
        if start_line < 1 or end_line < start_line or end_line - start_line >= 200:
            raise ResearchError("invalid_range", "每次最多读取 200 行，行号从 1 开始")
        data = self.request(f"/repos/{repository}/contents/{quote(path, safe='/')}", {"ref": pin["commit"]})
        if not isinstance(data, dict) or data.get("type") != "file":
            raise ResearchError("not_file", "目标不是普通文件")
        if data.get("size", 0) > 256_000 or data.get("encoding") != "base64":
            raise ResearchError("file_too_large", "文件超过 256 KB 或 GitHub 未返回可读内容")
        try:
            raw = base64.b64decode(data["content"])
            if b"\0" in raw:
                raise ValueError("binary")
            text = raw.decode("utf-8")
        except (UnicodeError, ValueError, binascii.Error, KeyError) as exc:
            raise ResearchError("binary_file", "文件不是可读取的 UTF-8 文本") from exc
        lines = text.splitlines()
        if start_line > len(lines):
            raise ResearchError("invalid_range", "起始行超过文件长度")
        selected = lines[start_line - 1:end_line]
        kept, size = [], 0
        for line in selected:
            size += len(line.encode("utf-8")) + 1
            if size > 24_000:
                break
            kept.append(line)
        if not kept:
            raise ResearchError("line_too_large", "单行内容超过 24 KB 限制")
        last = start_line + len(kept) - 1
        RepositoryIndex(self.store).add(repository, pin["commit"], path, text)
        return self.store.evidence(self.run_id, repository=repository, kind="file", commit=pin["commit"],
            path=path, start_line=start_line, end_line=last,
            url=f"https://github.com/{repository}/blob/{pin['commit']}/{quote(path, safe='/')}#L{start_line}-L{last}",
            summary=f"{path} 第 {start_line} 至 {last} 行，共 {len(lines)} 行",
            content="\n".join(f"{i}: {line}" for i, line in enumerate(kept, start_line)),
            truncated=start_line > 1 or last < len(lines))

    def directory(self, repository: str, path: str = "", pattern: str = "*", offset: int = 0) -> dict:
        pin = self.pinned(repository)
        if path and (len(path) > 512 or path.startswith("/") or any(p in ("..", ".", "") for p in path.split("/"))):
            raise ResearchError("invalid_path", "请使用仓库内的相对目录路径")
        if offset < 0 or len(pattern) > 128:
            raise ResearchError("invalid_range", "目录偏移必须非负，文件名模式最多128字符")
        data = self.request(f"/repos/{repository}/contents/{quote(path, safe='/')}", {"ref": pin["commit"]})
        if not isinstance(data, list):
            raise ResearchError("not_directory", "目标不是目录")
        matches = [item for item in data if fnmatch.fnmatchcase(item["name"].lower(), pattern.lower())]
        items = [{key: item.get(key) for key in ("name", "path", "type", "size")} for item in matches[offset:offset + 200]]
        evidence = self.store.evidence(self.run_id, repository=repository, kind="tree", commit=pin["commit"], path=path,
            url=f"https://github.com/{repository}/tree/{pin['commit']}/{quote(path, safe='/')}",
            summary=f"目录 {path or '/'}，文件名匹配 {pattern}，展示偏移 {offset} 后最多200项",
            content=json.dumps(items, ensure_ascii=False), truncated=offset + 200 < len(matches) or len(data) >= 1000)
        return {"evidence": evidence, "next_offset": offset + 200 if offset + 200 < len(matches) else None,
                "api_limit_possible": len(data) >= 1000}

#!/usr/bin/env python3
"""
挑下一个要分析的仓库 —— 合并 trending + starred 两路信号。

候选来源（以 url 为主键 union，信号叠加）：
  - Trending：src/trending_repo/all_repos_deduped.json（trending_days / stars）
  - Starred ：src/data/starred.json（跨大牛聚合的 star_users = 多少个白名单用户 Star 过）
    * 注意：CI 里 select 这步之前不重建 db.sqlite，所以读 git 跟踪的 starred.json
      自己聚合，而不是依赖 v_starred_frequency 视图。

去重逻辑（全部大小写不敏感，slug / url 统一归一为小写后比较）：
  - 命中 src/analysis_report/{owner}_{repo}.md 的视为已分析
  - 命中 src/data/publish_history.jsonl 里记录过的 slug 也视为已分析
    （即使报告 .md 被删，已分析/已发表过的仓库仍不会被重新选中）
  - 命中 src/analysis_report/repos.md 里 "❌ <url>" 的视为黑名单

打分排序：score = trending_days + star_users * STAR_WEIGHT，tie-break 用 stars。
  - starred-only 候选需 star_users >= STAR_MIN_USERS（默认 2，过滤单人 Star 噪声）
  - trending 候选不受该阈值限制（上榜本身即信号）
  - 可用环境变量 STAR_WEIGHT（默认 8）/ STAR_MIN_USERS（默认 2）调权

输出：
  - stdout: 选中的 URL（一行）
  - $GITHUB_OUTPUT: repo_url / repo_name / repo_slug / repo_stars / repo_star_users
  - 无候选: exit 78（GitHub Actions 视为 neutral skip）
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TRENDING_JSON = ROOT / "src" / "trending_repo" / "all_repos_deduped.json"
STARRED_JSON = ROOT / "src" / "data" / "starred.json"
ANALYSIS_DIR = ROOT / "src" / "analysis_report"
BLACKLIST_FILE = ROOT / "src" / "analysis_report" / "repos.md"
PUBLISH_JSONL = ROOT / "src" / "data" / "publish_history.jsonl"

STAR_WEIGHT = int(os.environ.get("STAR_WEIGHT", "8"))
STAR_MIN_USERS = int(os.environ.get("STAR_MIN_USERS", "2"))


def load_trending() -> list[dict]:
    if not TRENDING_JSON.exists():
        print(f"ERR: 找不到候选源 {TRENDING_JSON}", file=sys.stderr)
        sys.exit(1)
    with TRENDING_JSON.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        print(f"ERR: {TRENDING_JSON} 顶层不是 list", file=sys.stderr)
        sys.exit(1)
    return data


def load_starred_frequency() -> dict[str, dict]:
    """聚合 starred.json → {url: {name, stars, star_users}}。

    star_users = 有多少个不同的白名单用户 Star 过该仓库（跨 user 去重）。
    starred.json 不存在时返回空（退化为纯 trending 选题，保持旧行为）。"""
    if not STARRED_JSON.exists():
        return {}
    with STARRED_JSON.open(encoding="utf-8") as f:
        data = json.load(f)
    agg: dict[str, dict] = {}
    seen_pairs: set[tuple[str, str]] = set()  # (login, url) 去重，防同一用户重复计数
    for user in data.get("users", []):
        login = (user.get("login") or "").strip()
        for item in user.get("items", []):
            url = (item.get("url") or "").strip().rstrip("/")
            name = (item.get("name") or "").strip()
            if not url or "/" not in name:
                continue
            entry = agg.setdefault(
                url, {"name": name, "stars": 0, "star_users": 0}
            )
            entry["stars"] = max(entry["stars"], int(item.get("stars") or 0))
            if (login, url) not in seen_pairs:
                seen_pairs.add((login, url))
                entry["star_users"] += 1
    return agg


def load_analyzed_slugs() -> set[str]:
    """已分析仓库的 slug 集合（小写）：现存报告 .md ∪ publish_history 记录。

    纳入 publish_history.jsonl 是为了在报告 .md 被删后，已分析/已发表过的
    仓库仍不会被重新选中（贴合「发表过的不重复发布」）。"""
    slugs: set[str] = set()
    if ANALYSIS_DIR.exists():
        slugs |= {p.stem.lower() for p in ANALYSIS_DIR.glob("*.md")}
    if PUBLISH_JSONL.exists():
        for line in PUBLISH_JSONL.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue  # 容错坏行，不让单条脏数据拖垮选题
            s = (rec.get("slug") or "").strip().lower()
            if s:
                slugs.add(s)
    return slugs


def load_blacklist_urls() -> set[str]:
    if not BLACKLIST_FILE.exists():
        return set()
    urls: set[str] = set()
    pattern = re.compile(r"^[❌×x]\s+(https?://github\.com/[\w.-]+/[\w.-]+)")
    for line in BLACKLIST_FILE.read_text(encoding="utf-8").splitlines():
        m = pattern.match(line.strip())
        if m:
            urls.add(m.group(1).rstrip("/").lower())
    return urls


def slug_of(name: str) -> str:
    # 归一为小写：报告文件名是全小写，去重 key 必须大小写不敏感才能命中
    return name.replace("/", "_").lower()


def score_of(item: dict) -> int:
    return int(item.get("trending_days") or 0) + int(
        item.get("star_users") or 0
    ) * STAR_WEIGHT


def build_pool(
    trending: list[dict],
    starred: dict[str, dict],
    analyzed: set[str],
    blacklist: set[str],
) -> list[dict]:
    """以 url 为主键 union trending + starred，叠加信号，再过滤去重/黑名单。"""
    merged: dict[str, dict] = {}

    for item in trending:
        name = (item.get("name") or "").strip()
        url = (item.get("url") or "").strip().rstrip("/")
        if not name or not url or "/" not in name:
            continue
        merged[url] = {
            "name": name,
            "url": url,
            "stars": int(item.get("stars") or 0),
            "trending_days": int(item.get("trending_days") or 0),
            "star_users": 0,
            "sources": ["trending"],
        }

    for url, sdata in starred.items():
        if url in merged:
            entry = merged[url]
            entry["star_users"] = sdata["star_users"]
            entry["stars"] = max(entry["stars"], sdata["stars"])
            entry["sources"].append("starred")
        else:
            # starred-only：需达到多人 Star 阈值才入池
            if sdata["star_users"] < STAR_MIN_USERS:
                continue
            merged[url] = {
                "name": sdata["name"],
                "url": url,
                "stars": sdata["stars"],
                "trending_days": 0,
                "star_users": sdata["star_users"],
                "sources": ["starred"],
            }

    pool = []
    for url, item in merged.items():
        if slug_of(item["name"]) in analyzed:
            continue
        if url.lower() in blacklist:
            continue
        pool.append(item)

    pool.sort(key=lambda x: (score_of(x), int(x.get("stars") or 0)), reverse=True)
    return pool


def emit_github_output(picked: dict) -> None:
    out_path = os.environ.get("GITHUB_OUTPUT")
    if not out_path:
        return
    name = picked["name"]
    with open(out_path, "a", encoding="utf-8") as f:
        f.write(f"repo_url={picked['url']}\n")
        f.write(f"repo_name={name}\n")
        f.write(f"repo_slug={slug_of(name)}\n")
        f.write(f"repo_stars={picked.get('stars', 0)}\n")
        f.write(f"repo_star_users={picked.get('star_users', 0)}\n")


def main() -> int:
    trending = load_trending()
    starred = load_starred_frequency()
    analyzed = load_analyzed_slugs()
    blacklist = load_blacklist_urls()

    pool = build_pool(trending, starred, analyzed, blacklist)

    print(
        f"trending {len(trending)} | starred {len(starred)} | "
        f"已分析 {len(analyzed)} | 黑名单 {len(blacklist)} | "
        f"候选池 {len(pool)} (STAR_WEIGHT={STAR_WEIGHT}, STAR_MIN_USERS={STAR_MIN_USERS})",
        file=sys.stderr,
    )

    if not pool:
        print("没有可分析的新仓库", file=sys.stderr)
        return 78

    picked = pool[0]
    print(
        f"选中: {picked['name']} (score={score_of(picked)}, "
        f"stars={picked.get('stars')}, trending_days={picked.get('trending_days')}, "
        f"star_users={picked.get('star_users')}, sources={'+'.join(picked['sources'])})",
        file=sys.stderr,
    )
    print(picked["url"])
    emit_github_output(picked)
    return 0


if __name__ == "__main__":
    sys.exit(main())

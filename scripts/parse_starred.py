#!/usr/bin/env python3
"""
解析 src/starred_repo/{login}.md 数据快照，结合 src/data/users.yaml 配置，
输出 src/data/starred.json 供站点使用。

输入格式（每行）：
    - [owner/repo](url) ⭐stars — description [YYYY-MM-DD]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
USERS_FILE = ROOT / "src" / "data" / "users.yaml"
STARRED_DIR = ROOT / "src" / "starred_repo"
REPORTS_FILE = ROOT / "src" / "data" / "reports.json"
OUTPUT_FILE = ROOT / "src" / "data" / "starred.json"

LINE_RE = re.compile(
    r"^\s*[-*]\s+\[([^\]]+)\]\(([^)]+)\)\s*⭐\s*(\d+)\s*(?:—|--|-)\s*(.*?)\s*\[(\d{4}-\d{2}-\d{2})\]\s*$"
)
HEADER_RE = re.compile(r"^数据获取日期:\s*(\d{4}-\d{2}-\d{2})\s*\|\s*筛选范围:\s*(\d{4}-\d{2}-\d{2})\s*至今")


def parse_starred_file(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fetched_at = None
    range_start = None
    items: list[dict] = []

    for line in text.splitlines():
        if fetched_at is None:
            m = HEADER_RE.match(line.strip())
            if m:
                fetched_at, range_start = m.group(1), m.group(2)
                continue
        m = LINE_RE.match(line)
        if m:
            name, url, stars, desc, star_date = m.groups()
            items.append({
                "name": name.strip(),
                "url": url.strip(),
                "stars": int(stars),
                "description": desc.strip(),
                "starredAt": star_date,
            })

    return {
        "fetchedAt": fetched_at,
        "rangeStart": range_start,
        "items": items,
    }


def main() -> int:
    if not USERS_FILE.exists():
        print(f"❌ 缺少 {USERS_FILE}", file=sys.stderr)
        return 1
    users_doc = yaml.safe_load(USERS_FILE.read_text(encoding="utf-8")) or {}
    users = users_doc.get("users", []) or []

    # 反查表：URL → 报告 slug（reports.json 已是 lowercase slug）
    analyzed: dict[str, str] = {}
    if REPORTS_FILE.exists():
        for r in json.loads(REPORTS_FILE.read_text(encoding="utf-8")):
            if r.get("originalUrl"):
                analyzed[r["originalUrl"].rstrip("/").lower()] = r["slug"]

    output: dict = {"users": []}
    total_items = 0
    total_analyzed = 0

    for u in users:
        login = u.get("login")
        if not login:
            continue
        path = STARRED_DIR / f"{login}.md"
        if not path.exists():
            print(f"⚠️  {login}: 缺少 starred 快照 {path.relative_to(ROOT)}")
            output["users"].append({**u, "fetchedAt": None, "rangeStart": None, "items": []})
            continue

        parsed = parse_starred_file(path)
        for item in parsed["items"]:
            key = item["url"].rstrip("/").lower()
            if key in analyzed:
                item["reportSlug"] = analyzed[key]
                total_analyzed += 1

        total_items += len(parsed["items"])
        output["users"].append({
            **u,
            "fetchedAt": parsed["fetchedAt"],
            "rangeStart": parsed["rangeStart"],
            "items": parsed["items"],
        })

    OUTPUT_FILE.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"✅ 解析 {len(output['users'])} 位大牛 → {OUTPUT_FILE.relative_to(ROOT)}")
    print(f"   总 starred 条目: {total_items}")
    print(f"   其中已分析（命中报告）: {total_analyzed}")
    for u in output["users"]:
        print(f"     {u['login']:<14} fetched={u['fetchedAt']}  items={len(u['items'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

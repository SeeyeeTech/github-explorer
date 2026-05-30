#!/usr/bin/env python3
"""
基于 src/data/tag-rules.yaml 的关键词，对 src/data/reports.json 自动打标签，
输出 src/data/tags.yaml。

人工校正保护：tags.yaml 顶部的 manual 列表中的 slug 不会被脚本覆盖。
示例：
    manual:
      - continuedev_continue   # 人工已校正，跳过自动覆盖
    entries:
      continuedev_continue: [ai-coding, devtools]
      ...
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REPORTS_FILE = ROOT / "src" / "data" / "reports.json"
RULES_FILE = ROOT / "src" / "data" / "tag-rules.yaml"
OUTPUT_FILE = ROOT / "src" / "data" / "tags.yaml"


def load_rules() -> list[dict]:
    rules = yaml.safe_load(RULES_FILE.read_text(encoding="utf-8")) or []
    if not isinstance(rules, list):
        raise SystemExit("tag-rules.yaml 顶层必须是 list")
    return rules


def load_existing() -> tuple[set[str], dict[str, list[str]]]:
    if not OUTPUT_FILE.exists():
        return set(), {}
    doc = yaml.safe_load(OUTPUT_FILE.read_text(encoding="utf-8")) or {}
    manual = set(doc.get("manual", []) or [])
    entries = doc.get("entries", {}) or {}
    return manual, entries


def assemble_searchtext(report: dict) -> str:
    parts: list[str] = []
    for key in ("title", "summary", "originalUrl", "heat", "stage"):
        v = report.get(key)
        if v:
            parts.append(str(v))
    parts.extend(report.get("highlights") or [])
    return " ".join(parts).lower()


def match_tags(text: str, rules: list[dict]) -> list[str]:
    tags: list[str] = []
    for rule in rules:
        tag = rule.get("tag")
        kws = rule.get("match", []) or []
        if not tag or not kws:
            continue
        if any(kw.lower() in text for kw in kws):
            tags.append(tag)
    return tags or ["uncategorized"]


def main() -> int:
    if not REPORTS_FILE.exists():
        print(f"❌ 请先运行 build_reports_index.py 生成 {REPORTS_FILE}", file=sys.stderr)
        return 1

    rules = load_rules()
    manual, existing = load_existing()
    reports = json.loads(REPORTS_FILE.read_text(encoding="utf-8"))

    entries: dict[str, list[str]] = {}
    stats = {"auto": 0, "manual_kept": 0, "uncategorized": 0}

    for r in reports:
        slug = r["slug"]
        if slug in manual and slug in existing:
            entries[slug] = existing[slug]
            stats["manual_kept"] += 1
            continue
        text = assemble_searchtext(r)
        tags = match_tags(text, rules)
        if tags == ["uncategorized"]:
            stats["uncategorized"] += 1
        else:
            stats["auto"] += 1
        entries[slug] = tags

    # 按 slug 排序输出，便于 diff
    sorted_entries = {k: entries[k] for k in sorted(entries.keys())}
    doc = {
        "manual": sorted(manual),
        "entries": sorted_entries,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        "# 自动生成 + 人工保护混合维护。要保护某条手工标注，把 slug 加入 manual 列表。\n"
        + yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, default_flow_style=False),
        encoding="utf-8",
    )

    # 反向统计：每个 tag 命中的报告数
    tag_count: dict[str, int] = {}
    for tags in sorted_entries.values():
        for t in tags:
            tag_count[t] = tag_count.get(t, 0) + 1

    print(f"✅ 标签结果写入 {OUTPUT_FILE.relative_to(ROOT)}")
    print(f"   自动命中: {stats['auto']}, 保留人工: {stats['manual_kept']}, 未分类: {stats['uncategorized']}")
    print("   各标签分布（命中报告数）:")
    for t, n in sorted(tag_count.items(), key=lambda kv: -kv[1]):
        print(f"     {t:<22} {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

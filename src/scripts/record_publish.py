#!/usr/bin/env python3
"""Append 一条发布历史到 src/data/publish_history.jsonl。

由 auto-analyze.yml 调用：每次自动分析跑完后，记录该报告的发布状态。

示例：
    # 自动生成的草稿
    python3 scripts/record_publish.py \\
        --slug elastic_elasticsearch \\
        --state pending \\
        --reason "自动生成" \\
        --published-at 2026-06-01 \\
        --ci-run-id "$GITHUB_RUN_ID"

    # 手工指定公众号发布
    python3 scripts/record_publish.py \\
        --slug bytedance_deer-flow --state published \\
        --title "DeerFlow 深度分析报告" --published-at 2026-04-01

jsonl 是 append-only：手工编辑同 slug 的最新状态会被 v_publish_latest 视图自动识别。
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUBLISH_JSONL = ROOT / "src" / "data" / "publish_history.jsonl"

VALID_STATES = {"pending", "draft", "excluded", "published"}


def _already_recorded(out: Path, slug: str, state: str) -> bool:
    """jsonl 里是否已有完全相同的 (slug, state) 记录。

    幂等粒度按 (slug, state)：保留状态机语义（同 slug 的 pending→published
    仍可追加），只拦截完全重复的同状态行。slug 比较大小写不敏感。"""
    if not out.exists():
        return False
    for line in out.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue  # 容错坏行
        if (rec.get("slug") or "").strip().lower() == slug and rec.get("state") == state:
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--slug", required=True, help="报告 slug（lowercase，与 reports.slug 一致）")
    p.add_argument("--state", required=True, choices=sorted(VALID_STATES))
    p.add_argument("--title", default=None, help="公众号标题（可与 reports.title 不同）")
    p.add_argument("--published-at", default=None, help="发布日期 YYYY-MM-DD（state=published 时必填）")
    p.add_argument("--reason", default=None, help="原因/备注（excluded/draft 用）")
    p.add_argument("--ci-run-id", default=None, help="GitHub Actions runId，便于审计")
    p.add_argument("--out", type=Path, default=PUBLISH_JSONL)
    args = p.parse_args(argv)

    if args.state == "published" and not args.published_at:
        print("❌ state=published 时必须 --published-at YYYY-MM-DD", file=sys.stderr)
        return 1

    slug = args.slug.lower()
    if _already_recorded(args.out, slug, args.state):
        print(f"⏭ 跳过：{slug} 已有 state={args.state} 记录（幂等）")
        return 0

    record = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "slug": slug,
        "title": args.title,
        "state": args.state,
        "published_at": args.published_at,
        "reason": args.reason,
        "ci_run_id": args.ci_run_id,
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    # 确保文件以 newline 结尾，避免拼接成一行
    if args.out.exists() and args.out.stat().st_size > 0:
        with args.out.open("rb") as f:
            f.seek(-1, 2)
            if f.read(1) != b"\n":
                with args.out.open("a", encoding="utf-8") as af:
                    af.write("\n")
    with args.out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"✅ append → {args.out.relative_to(ROOT)}: slug={record['slug']} state={record['state']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

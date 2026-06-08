"""publish_history.jsonl 的 per-channel 读写 + 幂等查询。

publish_history.jsonl 是 append-only SoR（入 Git，CI 据此重建 db.sqlite）。
本模块在原有字段（recorded_at/slug/title/state/published_at/reason/ci_run_id）
基础上新增三个可选字段：
  - channel  渠道 id（缺省视为 'wechat'，兼容历史记录）
  - post_id  远端文章 id（幂等更新用，避免重复发文）
  - url      远端文章 URL

幂等查询直接读 jsonl —— 不依赖 db.sqlite（后者是 gitignore 的 CI 产物，重建才有）。
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .base import ROOT

PUBLISH_JSONL = ROOT / "src" / "data" / "publish_history.jsonl"
VALID_STATES = {"pending", "draft", "excluded", "published"}


def _iter_records(path: Path):
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            continue  # 容错坏行


def latest_record(slug: str, channel: str, *, path: Path = PUBLISH_JSONL) -> dict | None:
    """返回某 (slug, channel) 的最新记录（按 recorded_at），无则 None。

    历史记录缺 channel 字段时视为 'wechat'，与 init_db 的 DEFAULT 一致。
    """
    slug = slug.lower()
    best: dict | None = None
    for rec in _iter_records(path):
        if (rec.get("slug") or "").strip().lower() != slug:
            continue
        if (rec.get("channel") or "wechat") != channel:
            continue
        if best is None or (rec.get("recorded_at") or "") >= (best.get("recorded_at") or ""):
            best = rec
    return best


def append_record(
    *,
    slug: str,
    channel: str,
    state: str,
    title: str | None = None,
    post_id: str | None = None,
    url: str | None = None,
    published_at: str | None = None,
    reason: str | None = None,
    ci_run_id: str | None = None,
    path: Path = PUBLISH_JSONL,
) -> dict:
    """Append 一条发布记录。返回写入的 dict。"""
    if state not in VALID_STATES:
        raise ValueError(f"非法 state: {state}")
    record = {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "slug": slug.lower(),
        "channel": channel,
        "title": title,
        "state": state,
        "published_at": published_at,
        "post_id": post_id,
        "url": url,
        "reason": reason,
        "ci_run_id": ci_run_id,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    # 确保文件以 newline 结尾，避免拼接成一行（同 src/scripts/record_publish.py）
    if path.exists() and path.stat().st_size > 0:
        with path.open("rb") as f:
            f.seek(-1, 2)
            need_nl = f.read(1) != b"\n"
        if need_nl:
            with path.open("a", encoding="utf-8") as af:
                af.write("\n")
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record

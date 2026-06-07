#!/usr/bin/env python3
"""AI 日报 L1 确定性去重 + 30 天 cache 滚动（两篇共用）。

L1 仅做「URL 归一精确去重」与「对照 cache 剔旧闻」；L2/L3 语义去重由主对话 LLM 完成。
cache：src/data/ai-daily/cache/<type>.json，per-type 互不影响（见 dedup-rules.md）。

子命令：
    normalize <url>                          打印归一 key（调试用）
    check    --type T                        打印 cache 统计
    prune    --type T                        剔除 date_seen 超 window_days 的条目（就地写回）
    filter   --type T --in cand.json [--out] 输入条目列表 → 输出「池内去重 + 不在 cache」的条目
    commit   --type T --in adopted.json --date D   把今日采纳条目追加进 cache（更新 last_run）

cand.json / adopted.json：JSON 数组，每元素至少含 "url"（可含 "event_date"）。
filter 默认把结果打印到 stdout（或 --out 写文件），并把「去掉了几条」打到 stderr。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = ROOT / "src" / "data" / "ai-daily" / "cache"

_TRACKING = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
             "ref", "referrer", "fbclid", "gclid", "spm", "from", "share_token"}
_HF_RESERVED = {"papers", "models", "datasets", "spaces", "blog", "docs"}


def normalize_url(url: str) -> str:
    """把 URL 归一成稳定去重 key（见 dedup-rules.md L1）。"""
    raw = (url or "").strip()
    if not raw:
        return ""
    if raw.startswith("//"):
        raw = "https:" + raw
    if "://" not in raw:
        raw = "https://" + raw
    try:
        p = urlparse(raw)
    except ValueError:
        return raw.lower().rstrip("/")
    host = (p.netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]
    path = p.path.rstrip("/")
    segs = [s for s in path.split("/") if s]

    if host.endswith("github.com") and len(segs) >= 2:
        return f"github.com/{segs[0].lower()}/{segs[1].lower()}"
    if host.endswith("arxiv.org") and len(segs) >= 2 and segs[0] in {"abs", "pdf"}:
        aid = segs[1]
        if aid.endswith(".pdf"):
            aid = aid[:-4]
        aid = re.sub(r"v\d+$", "", aid)  # 去版本号：abs/123 与 pdf/123v2 视为同一篇
        return f"arxiv:{aid.lower()}"
    if host.endswith("huggingface.co") and len(segs) >= 2 and segs[0] not in _HF_RESERVED:
        return f"hf:{segs[0].lower()}/{segs[1].lower()}"

    # 通用：去 fragment + 去 tracking query，保留有效 query
    q = [(k, v) for k, v in parse_qsl(p.query) if k.lower() not in _TRACKING]
    clean = urlunparse(("https", host, path, "", urlencode(q), ""))
    return clean.lower().rstrip("/")


def _cache_path(t: str) -> Path:
    return CACHE_DIR / f"{t}.json"


def _load_cache(t: str) -> dict:
    path = _cache_path(t)
    if not path.exists():
        return {"meta": {"last_run": None, "window_days": 30}, "entries": []}
    try:
        with path.open(encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return {"meta": {"last_run": None, "window_days": 30}, "entries": []}
    data.setdefault("meta", {"last_run": None, "window_days": 30})
    data.setdefault("entries", [])
    data["meta"].setdefault("window_days", 30)
    return data


def _save_cache(t: str, data: dict) -> None:
    path = _cache_path(t)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def _prune(data: dict, today: str) -> int:
    window = int(data["meta"].get("window_days", 30))
    cutoff = (datetime.strptime(today, "%Y-%m-%d") - timedelta(days=window)).strftime("%Y-%m-%d")
    before = len(data["entries"])
    data["entries"] = [e for e in data["entries"] if (e.get("date_seen") or "") >= cutoff]
    return before - len(data["entries"])


def _read_items(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [x if isinstance(x, dict) else {"url": str(x)} for x in data]
    if isinstance(data, dict) and isinstance(data.get("items"), list):
        return data["items"]
    raise SystemExit(f"ERR: {path} 不是条目数组")


def cmd_normalize(args) -> int:
    print(normalize_url(args.url))
    return 0


def cmd_check(args) -> int:
    data = _load_cache(args.type)
    print(f"type={args.type} last_run={data['meta'].get('last_run')} "
          f"window_days={data['meta'].get('window_days')} entries={len(data['entries'])}")
    return 0


def cmd_prune(args) -> int:
    data = _load_cache(args.type)
    today = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    removed = _prune(data, today)
    _save_cache(args.type, data)
    print(f"prune {args.type}: 剔除 {removed} 条，剩 {len(data['entries'])}", file=sys.stderr)
    return 0


def cmd_filter(args) -> int:
    data = _load_cache(args.type)
    seen = {e.get("key") for e in data["entries"] if e.get("key")}
    items = _read_items(args.infile)
    out, pool_seen = [], set()
    dropped_cache = dropped_dup = 0
    for it in items:
        key = normalize_url(it.get("url", ""))
        if not key:
            out.append(it)
            continue
        if key in seen:
            dropped_cache += 1
            continue
        if key in pool_seen:
            dropped_dup += 1
            continue
        pool_seen.add(key)
        it = dict(it)
        it["_dedup_key"] = key
        out.append(it)
    text = json.dumps(out, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    print(f"filter {args.type}: 入 {len(items)} → 出 {len(out)}（cache 剔 {dropped_cache}，"
          f"池内重复剔 {dropped_dup}）", file=sys.stderr)
    return 0


def cmd_commit(args) -> int:
    data = _load_cache(args.type)
    today = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    _prune(data, today)
    existing = {e.get("key") for e in data["entries"] if e.get("key")}
    items = _read_items(args.infile)
    added = 0
    for it in items:
        key = normalize_url(it.get("url", ""))
        if not key or key in existing:
            continue
        existing.add(key)
        data["entries"].append({
            "key": key,
            "canonical_url": it.get("url"),
            "event_date": it.get("event_date"),
            "date_seen": today,
        })
        added += 1
    data["meta"]["last_run"] = today
    _save_cache(args.type, data)
    print(f"commit {args.type}: 追加 {added} 条，cache 共 {len(data['entries'])}（last_run={today}）",
          file=sys.stderr)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("normalize"); p.add_argument("url"); p.set_defaults(func=cmd_normalize)
    p = sub.add_parser("check"); p.add_argument("--type", required=True, choices=["ecosystem", "frontier"]); p.set_defaults(func=cmd_check)
    p = sub.add_parser("prune"); p.add_argument("--type", required=True, choices=["ecosystem", "frontier"]); p.add_argument("--date"); p.set_defaults(func=cmd_prune)
    p = sub.add_parser("filter")
    p.add_argument("--type", required=True, choices=["ecosystem", "frontier"])
    p.add_argument("--in", dest="infile", type=Path, required=True)
    p.add_argument("--out", type=Path)
    p.set_defaults(func=cmd_filter)
    p = sub.add_parser("commit")
    p.add_argument("--type", required=True, choices=["ecosystem", "frontier"])
    p.add_argument("--in", dest="infile", type=Path, required=True)
    p.add_argument("--date")
    p.set_defaults(func=cmd_commit)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())

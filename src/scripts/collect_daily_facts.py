#!/usr/bin/env python3
"""AI 日报确定性数据采集（两篇 skill 共用，对标 collect_repo_facts.py）。

把本项目独有的「开源信号层」一次性算成结构化 JSON，子 agent 不再现场跑逻辑：
  - rising_repos : 最新一期 GitHub Trending(daily) 榜，标注 AI 相关 + 回链已有报告
  - pro_stars    : 白名单大牛自上次同类日报以来的新 star，跨大牛聚合 star_users
  - heating_up   : 跨窗口持续升温的仓库（all_repos_deduped 的 trending_days / last_seen）
  - resurface    : 与今日主题相关、值得旧文重读的历史报告（导流位）

脚本只把这份 JSON 写到 tmp/ 并把路径打印到 stdout（主对话 context 保持干净）。
reports.json 的 originalUrl→slug 全表单独落 tmp 文件（供篇B 外部条目回链），路径写进 facts。

复用 select_next_repo.py 的成熟逻辑：load_starred_frequency / load_analyzed_slugs / slug_of。
所有指标单独 try，缺失记 null 并写入 _warnings，绝不因单项失败中断整体采集。

用法：
    python3 src/scripts/collect_daily_facts.py <date> [--type ecosystem|frontier] [--out PATH]
- <date>：日报日期 YYYY-MM-DD（缺省今天 UTC）
- --type：ecosystem(默认，开源信号为主) / frontier(只产内部信号层供回链与增强)
- --out：JSON 落地路径，缺省 tmp/daily-facts-<type>-<date>.json
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

# 复用 select_next_repo 的聚合/归一逻辑（同目录模块）
from select_next_repo import (  # noqa: E402
    load_analyzed_slugs,
    slug_of,
)

DATA = ROOT / "src" / "data"
TRENDING_SNAPSHOTS = DATA / "trending_snapshots.jsonl"
TRENDING_DEDUPED = ROOT / "src" / "trending_repo" / "all_repos_deduped.json"
STARRED_JSON = DATA / "starred.json"
STARRED_SEED = DATA / "starred_seed.json"
REPORTS_JSON = DATA / "reports.json"
ENTITIES_YAML = DATA / "ai-daily" / "entities.yaml"
SCORING_YAML = DATA / "ai-daily" / "scoring.yaml"
DIGESTS_JSONL = DATA / "daily_digests.jsonl"
CACHE_DIR = DATA / "ai-daily" / "cache"

WARNINGS: list[str] = []


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"[collect_daily_facts] warn: {msg}", file=sys.stderr)


def _load_json(path: Path, default):
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        warn(f"缺失数据源 {path.relative_to(ROOT)}，降级为空")
        return default
    except (json.JSONDecodeError, OSError) as e:
        warn(f"读取 {path.relative_to(ROOT)} 失败: {e}")
        return default


def _load_yaml(path: Path, default):
    try:
        import yaml
        with path.open(encoding="utf-8") as f:
            return yaml.safe_load(f) or default
    except FileNotFoundError:
        warn(f"缺失配置 {path.relative_to(ROOT)}，用默认值")
        return default
    except Exception as e:  # noqa: BLE001  — 配置坏不致命
        warn(f"读取 {path.relative_to(ROOT)} 失败: {e}")
        return default


def norm_url(url: str) -> str:
    return (url or "").strip().rstrip("/").lower()


# ----------------------------------------------------------------- AI 相关性
def build_ai_matcher(entities: dict):
    h = (entities or {}).get("heuristics", {}) or {}
    keywords = [k.lower() for k in (h.get("keywords") or [])]
    owners = {o.lower() for o in (h.get("owners") or [])}
    ai_langs = set(h.get("languages") or [])

    def is_ai(name: str, description: str, language: str | None = None) -> bool:
        owner = (name or "").split("/")[0].strip().lower()
        if owner and owner in owners:
            return True
        text = f"{name} {description or ''}".lower()
        for kw in keywords:
            if kw and kw in text:
                return True
        return False

    return is_ai, ai_langs


# ----------------------------------------------------------------- 报告回链索引
def build_report_url_index() -> dict[str, str]:
    """reports.json originalUrl(归一) → slug。Python 版 data.ts:getAnalyzedUrlIndex。"""
    reports = _load_json(REPORTS_JSON, [])
    idx: dict[str, str] = {}
    for r in reports if isinstance(reports, list) else []:
        ou = r.get("originalUrl")
        slug = r.get("slug")
        if ou and slug:
            idx[norm_url(ou)] = slug
    return idx


# ----------------------------------------------------------------- since 窗口
def resolve_since(digest_type: str, date: str, default_days: int = 7) -> str:
    """同类日报上次产出日期；无则 date - default_days。"""
    fallback = (
        datetime.strptime(date, "%Y-%m-%d") - timedelta(days=default_days)
    ).strftime("%Y-%m-%d")
    if not DIGESTS_JSONL.exists():
        return fallback
    last = None
    for line in DIGESTS_JSONL.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if rec.get("type") == digest_type and rec.get("date"):
            d = rec["date"]
            if last is None or d > last:
                last = d
    return last or fallback


# ----------------------------------------------------------------- rising_repos（今日 Trending daily）
def load_rising_repos(date: str, idx: dict[str, str], is_ai) -> tuple[list[dict], dict]:
    """最新一期 daily 榜（period_key ≤ date 的最大值），标注 rank_delta / ai / 回链。"""
    if not TRENDING_SNAPSHOTS.exists():
        warn("缺失 trending_snapshots.jsonl，rising_repos 为空")
        return [], {}
    daily: dict[str, list[dict]] = {}
    for line in TRENDING_SNAPSHOTS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if r.get("period_type") == "daily" and r.get("period_key"):
            daily.setdefault(r["period_key"], []).append(r)
    if not daily:
        return [], {}
    keys = sorted(daily)
    le = [k for k in keys if k <= date]
    today_key = le[-1] if le else keys[-1]
    prev_key = None
    pos = keys.index(today_key)
    if pos > 0:
        prev_key = keys[pos - 1]
    prev_rank = {norm_url(r.get("url", "")): r.get("rank") for r in daily.get(prev_key, [])} if prev_key else {}

    out = []
    non_ai = 0
    for r in sorted(daily[today_key], key=lambda x: x.get("rank") or 999):
        name = (r.get("name") or "").strip()
        url = (r.get("url") or "").strip().rstrip("/")
        if not name or not url:
            continue
        nu = norm_url(url)
        rank = r.get("rank")
        pr = prev_rank.get(nu)
        rank_delta = (pr - rank) if (isinstance(pr, int) and isinstance(rank, int)) else None
        ai = is_ai(name, r.get("description"), r.get("language"))
        if not ai:
            non_ai += 1
        out.append({
            "name": name,
            "url": url,
            "language": r.get("language"),
            "stars": int(r.get("stars") or 0),
            "forks": int(r.get("forks") or 0),
            "rank": rank,
            "rank_delta": rank_delta,        # 正=排名上升；None=新进榜
            "is_new": pr is None,
            "description": r.get("description"),
            "ai": ai,
            "report_slug": idx.get(nu),
        })
    meta = {"period_key": today_key, "prev_key": prev_key, "total": len(out), "non_ai": non_ai}
    return out, meta


# ----------------------------------------------------------------- pro_stars（大牛新 star）
def load_new_pro_stars(since: str, idx: dict[str, str], is_ai) -> list[dict]:
    """读 starred.json（缺则 starred_seed.json），取 starredAt ≥ since 的项，按 url 聚合。"""
    data = _load_json(STARRED_JSON, None)
    if not data:
        data = _load_json(STARRED_SEED, {"users": []})
    agg: dict[str, dict] = {}
    seen_pairs: set[tuple[str, str]] = set()
    for user in (data or {}).get("users", []):
        login = (user.get("login") or "").strip()
        uname = (user.get("name") or login).strip()
        for item in user.get("items", []):
            starred_at = (item.get("starredAt") or "").strip()
            if not starred_at or starred_at < since:
                continue
            url = (item.get("url") or "").strip().rstrip("/")
            name = (item.get("name") or "").strip()
            if not url or "/" not in name:
                continue
            nu = norm_url(url)
            entry = agg.setdefault(nu, {
                "name": name,
                "url": url,
                "stars": 0,
                "star_users": 0,
                "starred_by": [],
                "latest_starred_at": starred_at,
                "description": item.get("description"),
                "report_slug": idx.get(nu),
                "ai": is_ai(name, item.get("description"), None),
            })
            entry["stars"] = max(entry["stars"], int(item.get("stars") or 0))
            entry["latest_starred_at"] = max(entry["latest_starred_at"], starred_at)
            if (login, nu) not in seen_pairs:
                seen_pairs.add((login, nu))
                entry["star_users"] += 1
                entry["starred_by"].append({"login": login, "name": uname})
    rows = list(agg.values())
    # 多人 star 优先；其次 star 数；其次最近
    rows.sort(key=lambda x: (x["star_users"], x["stars"], x["latest_starred_at"]), reverse=True)
    return rows


# ----------------------------------------------------------------- heating_up（跨窗口升温）
def load_heating_up(idx: dict[str, str], is_ai, limit: int = 30) -> list[dict]:
    data = _load_json(TRENDING_DEDUPED, [])
    rows = []
    for r in data if isinstance(data, list) else []:
        name = (r.get("name") or "").strip()
        url = (r.get("url") or "").strip().rstrip("/")
        if not name or not url:
            continue
        nu = norm_url(url)
        rows.append({
            "name": name,
            "url": url,
            "language": r.get("language"),
            "stars": int(r.get("stars") or 0),
            "trending_days": int(r.get("trending_days") or 0),
            "last_seen": r.get("last_seen"),
            "description": r.get("description"),
            "ai": is_ai(name, r.get("description"), r.get("language")),
            "report_slug": idx.get(nu),
        })
    rows.sort(key=lambda x: (x["trending_days"], x["stars"]), reverse=True)
    return rows[:limit]


# ----------------------------------------------------------------- resurface（旧文重读）
def pick_resurface_reports(rising: list[dict], exclude_urls: set[str], is_ai, n: int = 4) -> list[dict]:
    """从已有报告里召回与今日 AI 主题相关、可重读的历史篇。

    优先级：AI 相关 > 语言命中今日 AI rising 主流语言 > star 高。
    用 is_ai(报告标题+摘要+owner) 过滤掉非 AI 报告（避免 public-apis 这类混进 AI 日报）。"""
    reports = _load_json(REPORTS_JSON, [])
    if not isinstance(reports, list):
        return []
    langs = [r.get("language") for r in rising if r.get("ai") and r.get("language")]
    top_langs = {l for l in langs}
    cand = []
    for r in reports:
        ou = norm_url(r.get("originalUrl") or "")
        if not ou or ou in exclude_urls:
            continue
        # 用 owner/repo + 标题 + 摘要 判 AI 相关
        owner_repo = ""
        if r.get("originalUrl"):
            parts = [p for p in (r["originalUrl"].split("github.com/")[-1]).split("/") if p]
            owner_repo = "/".join(parts[:2])
        ai_hit = is_ai(owner_repo, f"{r.get('title') or ''} {r.get('summary') or ''}", r.get("language"))
        lang_hit = (r.get("language") in top_langs) if top_langs else False
        cand.append((ai_hit, lang_hit, int(r.get("stars") or 0), r))
    # AI 相关优先 → 语言命中 → star
    cand = [c for c in cand if c[0]] or cand  # 有 AI 报告就只用 AI 的；否则退回全部
    cand.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
    out = []
    for _, _, _, r in cand[:n]:
        out.append({
            "slug": r.get("slug"),
            "title": r.get("title"),
            "summary": r.get("summary"),
            "language": r.get("language"),
            "stars": r.get("stars"),
            "originalUrl": r.get("originalUrl"),
        })
    return out


# ----------------------------------------------------------------- cache 提示
def load_cache_seen_keys(digest_type: str) -> list[str]:
    cache = _load_json(CACHE_DIR / f"{digest_type}.json", {"entries": []})
    return [e.get("key") for e in cache.get("entries", []) if e.get("key")]


# ----------------------------------------------------------------- 组装
def build_facts(date: str, digest_type: str) -> tuple[dict, dict]:
    entities = _load_yaml(ENTITIES_YAML, {})
    scoring = _load_yaml(SCORING_YAML, {})
    is_ai, _ai_langs = build_ai_matcher(entities)
    idx = build_report_url_index()
    since = resolve_since(digest_type, date)

    rising, rising_meta = load_rising_repos(date, idx, is_ai)
    pro_stars = load_new_pro_stars(since, idx, is_ai)
    heating = load_heating_up(idx, is_ai)
    exclude = {norm_url(x["url"]) for x in rising} | {norm_url(x["url"]) for x in pro_stars}
    resurface = pick_resurface_reports(rising, exclude, is_ai)

    facts = {
        "schema_version": 1,
        "type": digest_type,
        "date": date,
        "since": since,
        "after_date": since,  # 外部采集时效起点（篇B 用）
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "config": {
            "concurrency_cap": int((scoring or {}).get("concurrency_cap", 10)),
            "min_non_seed_ratio": float((scoring or {}).get("min_non_seed_ratio", 0.2)),
        },
        "trending_period_key": rising_meta.get("period_key"),
        "stats": {
            "rising_total": rising_meta.get("total", 0),
            "rising_ai": sum(1 for x in rising if x["ai"]),
            "rising_non_ai": rising_meta.get("non_ai", 0),
            "pro_stars": len(pro_stars),
            "pro_stars_multi": sum(1 for x in pro_stars if x["star_users"] >= 2),
            "heating": len(heating),
            "resurface": len(resurface),
            "report_index": len(idx),
        },
        "rising_repos": rising,
        "pro_stars": pro_stars,
        "heating_up": heating,
        "resurface": resurface,
        "cache_seen_keys": load_cache_seen_keys(digest_type),
        "_warnings": WARNINGS,
    }
    return facts, idx


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="AI 日报确定性数据采集（开源信号层）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("date", nargs="?", help="日报日期 YYYY-MM-DD（缺省今天 UTC）")
    ap.add_argument("--type", choices=["ecosystem", "frontier"], default="ecosystem")
    ap.add_argument("--out", type=Path, help="JSON 落地路径，缺省 tmp/daily-facts-<type>-<date>.json")
    args = ap.parse_args(argv)

    date = args.date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        print(f"ERR: 非法日期 {date}（应为 YYYY-MM-DD）", file=sys.stderr)
        return 1

    facts, idx = build_facts(date, args.type)

    out_path = args.out or (ROOT / "tmp" / f"daily-facts-{args.type}-{date}.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(facts, f, ensure_ascii=False, indent=2)

    # 报告回链全表单独落文件（供篇B 外部条目反查，不塞进主对话）
    idx_path = ROOT / "tmp" / f"daily-report-index-{date}.json"
    with idx_path.open("w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
    facts["report_url_index_path"] = str(idx_path.relative_to(ROOT))
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(facts, f, ensure_ascii=False, indent=2)

    st = facts["stats"]
    print(
        f"[collect_daily_facts] type={args.type} date={date} since={facts['since']} | "
        f"rising {st['rising_ai']}/{st['rising_total']} AI | pro_stars {st['pro_stars']} "
        f"(多人 {st['pro_stars_multi']}) | heating {st['heating']} | resurface {st['resurface']} | "
        f"warnings {len(WARNINGS)}",
        file=sys.stderr,
    )
    print(out_path)  # stdout 只打印路径（同 collect_repo_facts.py）
    return 0


if __name__ == "__main__":
    sys.exit(main())

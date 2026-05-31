#!/usr/bin/env python3
"""把公众号侧的「已发布」事实同步回 src/publish.md。

拉 freepublish/batchget（可选 material/batchget_material 的草稿箱）→ 对每条文章按
归一化标题匹配项目侧报告 → dry-run 打印待变更摘要 → --apply 时改写 publish.md：

  - 状态列：'待发布' → 公众号 update_time 的日期 (YYYY-MM-DD)；已是日期则保留
  - 标题列：命中行始终用公众号侧标题覆盖（按用户要求）

环境变量：见 _wechat_api.load_wechat_env()。本地建议把 WECHAT_APPID/APPSECRET 写在 .env，
然后 `set -a && source .env && set +a && python3 scripts/sync_wechat_status.py` 注入。

用法：
  scripts/sync_wechat_status.py                        # dry-run, --min-confidence medium
  scripts/sync_wechat_status.py --include-drafts       # 同时看草稿箱（草稿无 url）
  scripts/sync_wechat_status.py --apply                # 真改 publish.md
  scripts/sync_wechat_status.py --min-confidence low   # 含低置信度（仅 dry-run，不能配 --apply）
"""
from __future__ import annotations

import argparse
import difflib
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from _wechat_api import (
    check_wechat_ok,
    get_access_token,
    load_wechat_env,
    wechat_post,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
PUBLISH_MD = REPO_ROOT / "src" / "publish.md"
ANALYSIS_DIR = REPO_ROOT / "src" / "analysis_report"

# 归一化时去除的尾缀（顺序：长→短，否则短的会先匹配掉）
TITLE_SUFFIXES = ["深度分析报告", "深度分析", "分析报告"]
# 归一化时去除的引号 / 装饰字符
STRIP_CHARS = "「」『』\"\"''《》()【】[]"

# 匹配阈值
THRESHOLD_HIGH = 1.0      # 归一化后精确相等
THRESHOLD_MEDIUM = 0.85
THRESHOLD_LOW = 0.6
GAP_REQUIRED = 0.1        # 最佳与次优至少要差这么多（避免歧义匹配）


@dataclass
class WechatArticle:
    title: str
    url: str | None        # 草稿没有 url
    update_time: int       # unix ts
    media_id: str
    digest: str = ""
    source: str = "freepublish"   # 'freepublish' | 'draft'


@dataclass
class MatchResult:
    article: WechatArticle
    slug: str | None
    matched_title: str | None     # 项目侧命中的标题（归一化前）
    ratio: float
    confidence: str               # 'high' | 'medium' | 'low' | 'none'
    candidates: list[tuple[str, float]] = field(default_factory=list)  # (slug, ratio) top-3


# ─── 归一化与匹配 ──────────────────────────────────────────────────────────

def normalize(s: str) -> str:
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", s)
    s = s.lower()
    for ch in STRIP_CHARS:
        s = s.replace(ch, "")
    s = re.sub(r"\s+", " ", s).strip()
    for suf in TITLE_SUFFIXES:
        if s.endswith(suf):
            s = s[: -len(suf)].strip()
            break
    return s


def classify(ratio: float, gap: float) -> str:
    if ratio >= THRESHOLD_HIGH:
        return "high"
    if ratio >= THRESHOLD_MEDIUM and gap >= GAP_REQUIRED:
        return "medium"
    if ratio >= THRESHOLD_LOW:
        return "low"
    return "none"


def best_match(query: str, candidates: dict[str, str]) -> tuple[str | None, float, list[tuple[str, float]]]:
    """candidates: normalized_title -> slug。返回 (slug, ratio, top3)。"""
    if not candidates:
        return None, 0.0, []
    scored = [
        (slug, difflib.SequenceMatcher(None, query, ntitle).ratio())
        for ntitle, slug in candidates.items()
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:3]
    return top[0][0], top[0][1], top


# ─── 项目侧数据加载 ────────────────────────────────────────────────────────

PUBLISH_ROW_RE = re.compile(
    r"^\|\s*\[(?P<filename>[^\]]+\.md)\]\([^)]*\)\s*\|\s*(?P<title>[^|]+?)\s*\|\s*(?P<status>[^|]+?)\s*\|\s*$"
)


@dataclass
class PublishRow:
    line_no: int          # 1-based
    raw: str
    filename: str         # 如 'bytedance_deer-flow.md'
    title: str
    status: str           # '待发布' 或 'YYYY-MM-DD' 等


def parse_publish_md(text: str) -> tuple[list[PublishRow], list[str]]:
    """返回 (已发布表的行列表, 原始所有行)。
    遇到 '## 不发布列表' 终止收集——之后的表不参与同步。
    """
    lines = text.splitlines(keepends=True)
    rows: list[PublishRow] = []
    in_not_publish_section = False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("## 不发布列表"):
            in_not_publish_section = True
            continue
        if in_not_publish_section:
            continue
        m = PUBLISH_ROW_RE.match(line)
        if not m:
            continue
        rows.append(PublishRow(
            line_no=i,
            raw=line,
            filename=m.group("filename").strip(),
            title=m.group("title").strip(),
            status=m.group("status").strip(),
        ))
    return rows, lines


H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def load_analysis_h1s() -> dict[str, str]:
    """slug → H1 标题（去掉 '# '）。slug 即 basename 去 .md。"""
    out: dict[str, str] = {}
    for md in ANALYSIS_DIR.glob("*.md"):
        try:
            head = md.read_text(encoding="utf-8", errors="ignore").splitlines()[:5]
        except OSError:
            continue
        for line in head:
            m = H1_RE.match(line)
            if m:
                out[md.stem] = m.group(1).strip()
                break
    return out


def build_match_dict(rows: list[PublishRow], h1s: dict[str, str]) -> dict[str, str]:
    """normalized_title → slug（去 .md）。publish.md 标题优先，H1 兜底。"""
    out: dict[str, str] = {}
    # 先放兜底
    for slug, h1 in h1s.items():
        key = normalize(h1)
        if key:
            out[key] = slug
    # 再放主源（覆盖兜底）
    for row in rows:
        slug = row.filename[:-3] if row.filename.endswith(".md") else row.filename
        key = normalize(row.title)
        if key:
            out[key] = slug
    return out


# ─── 微信 API：拉文章列表 ──────────────────────────────────────────────────

def fetch_all(env_dict, access_token, path: str, body_extra: dict | None = None) -> list[dict]:
    """通用分页拉取，返回 item 列表。"""
    items: list[dict] = []
    offset = 0
    page = 20
    while True:
        body = {"offset": offset, "count": page}
        if body_extra:
            body.update(body_extra)
        resp = wechat_post(env_dict, path, body, access_token, timeout=30)
        check_wechat_ok(resp, f"batchget {path}")
        page_items = resp.get("item") or []
        items.extend(page_items)
        total = resp.get("total_count")
        if len(page_items) < page or (total is not None and offset + page >= total):
            break
        offset += page
    return items


def parse_freepublish(items: list[dict]) -> list[WechatArticle]:
    """freepublish/batchget 返回结构:
      item[].article_id (= media_id), update_time,
            content.news_item[].{title, url, content_source_url, digest, thumb_url, ...}
    """
    out: list[WechatArticle] = []
    for it in items:
        media_id = it.get("article_id") or it.get("media_id") or ""
        update_time = int(it.get("update_time") or 0)
        news_items = (it.get("content") or {}).get("news_item") or []
        for n in news_items:
            title = (n.get("title") or "").strip()
            if not title:
                continue
            out.append(WechatArticle(
                title=title,
                url=n.get("url") or None,
                update_time=update_time,
                media_id=media_id,
                digest=(n.get("digest") or "").strip(),
                source="freepublish",
            ))
    return out


def parse_drafts(items: list[dict]) -> list[WechatArticle]:
    """material/batchget_material type=news 返回结构:
      item[].media_id, update_time, content.news_item[].{title, digest, content_source_url, ...}
    （草稿无 url）
    """
    out: list[WechatArticle] = []
    for it in items:
        media_id = it.get("media_id") or ""
        update_time = int(it.get("update_time") or 0)
        news_items = (it.get("content") or {}).get("news_item") or []
        for n in news_items:
            title = (n.get("title") or "").strip()
            if not title:
                continue
            out.append(WechatArticle(
                title=title,
                url=None,
                update_time=update_time,
                media_id=media_id,
                digest=(n.get("digest") or "").strip(),
                source="draft",
            ))
    return out


# ─── 匹配 + 决策 ───────────────────────────────────────────────────────────

def match_articles(
    articles: list[WechatArticle],
    match_dict: dict[str, str],
) -> list[MatchResult]:
    results: list[MatchResult] = []
    inverse: dict[str, str] = {slug: ntitle for ntitle, slug in match_dict.items()}
    for art in articles:
        q = normalize(art.title)
        slug, ratio, top3 = best_match(q, match_dict)
        gap = (top3[0][1] - top3[1][1]) if len(top3) >= 2 else 1.0
        conf = classify(ratio, gap)
        results.append(MatchResult(
            article=art,
            slug=slug if conf != "none" else None,
            matched_title=inverse.get(slug) if (slug and conf != "none") else None,
            ratio=ratio,
            confidence=conf,
            candidates=top3,
        ))
    return results


# 同一 slug 多次命中：取 update_time 最大者
def dedupe_by_slug(results: list[MatchResult]) -> dict[str, MatchResult]:
    out: dict[str, MatchResult] = {}
    for r in results:
        if not r.slug:
            continue
        prev = out.get(r.slug)
        if prev is None or r.article.update_time > prev.article.update_time:
            out[r.slug] = r
    return out


# ─── publish.md 改写 ──────────────────────────────────────────────────────

def date_from_ts(ts: int) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d") if ts else ""


def rewrite_row(row: PublishRow, new_title: str, new_status: str) -> str:
    """保留链接列原样，只替换标题列和状态列。"""
    return PUBLISH_ROW_RE.sub(
        lambda m: (
            f"| [{m.group('filename')}]"
            f"(analysis_report/{m.group('filename')}) "
            f"| {new_title} | {new_status} |\n"
        ),
        row.raw,
    )


def apply_changes(
    lines: list[str],
    rows: list[PublishRow],
    decisions: dict[str, MatchResult],
) -> tuple[list[str], list[dict]]:
    """改写 lines。返回 (新 lines, 变更记录列表 for log)。"""
    rows_by_line = {r.line_no: r for r in rows}
    slug_to_decision = decisions
    changes: list[dict] = []
    new_lines = list(lines)
    for r in rows:
        slug = r.filename[:-3] if r.filename.endswith(".md") else r.filename
        decision = slug_to_decision.get(slug)
        if not decision:
            continue
        # 状态：仅"待发布"→ 日期；已是日期则保留
        is_pending = r.status == "待发布"
        new_status = date_from_ts(decision.article.update_time) if is_pending else r.status
        # 标题：始终用公众号侧覆盖（用户要求）
        new_title = decision.article.title
        if new_status == r.status and new_title == r.title:
            continue
        new_lines[r.line_no - 1] = rewrite_row(r, new_title, new_status)
        changes.append({
            "slug": slug,
            "old_title": r.title,
            "new_title": new_title,
            "old_status": r.status,
            "new_status": new_status,
            "confidence": decision.confidence,
            "ratio": round(decision.ratio, 3),
        })
    return new_lines, changes


def atomic_write(path: Path, lines: list[str]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text("".join(lines), encoding="utf-8")
    tmp.replace(path)


# ─── CLI / 主流程 ──────────────────────────────────────────────────────────

def fmt_pct(x: float) -> str:
    return f"{x*100:.0f}%"


def print_dry_run(
    matched: dict[str, MatchResult],
    unmatched: list[MatchResult],
    low_conf: list[MatchResult],
    rows: list[PublishRow],
    decisions_will_apply: dict[str, MatchResult],
    will_change: list[dict],
) -> None:
    print()
    print("=" * 70)
    print(f"公众号侧文章: {sum(1 for _ in matched.values()) + len(unmatched) + len(low_conf)} 篇")
    print(f"  ↳ high/medium 命中且会触发变更: {len(will_change)} 条")
    print(f"  ↳ low 置信度（默认不 apply）: {len(low_conf)} 条")
    print(f"  ↳ 未匹配到项目报告: {len(unmatched)} 条")
    print("=" * 70)

    if will_change:
        print("\n[将会写入 publish.md 的变更]")
        for c in will_change:
            marks = []
            if c["old_status"] != c["new_status"]:
                marks.append(f"状态 {c['old_status']!r} → {c['new_status']!r}")
            if c["old_title"] != c["new_title"]:
                marks.append(f"标题 {c['old_title']!r} → {c['new_title']!r}")
            print(f"  · {c['slug']}  [{c['confidence']} ratio={c['ratio']}]")
            for m in marks:
                print(f"      {m}")

    matched_no_change = [
        (slug, r) for slug, r in decisions_will_apply.items()
        if not any(c["slug"] == slug for c in will_change)
    ]
    if matched_no_change:
        print(f"\n[命中但 publish.md 无需变化] {len(matched_no_change)} 条（标题与状态都已对齐）")

    if low_conf:
        print("\n[低置信度命中 — 默认不 apply，需 --min-confidence low + 人工 review]")
        for r in low_conf:
            print(f"  · 公众号 {r.article.title!r}")
            print(f"      update_time={date_from_ts(r.article.update_time)}  url={r.article.url}")
            for slug, ratio in r.candidates[:3]:
                print(f"      候选 slug={slug}  ratio={ratio:.3f}")

    if unmatched:
        print("\n[完全未匹配 — 公众号上有，但项目里找不到对应报告]")
        for r in unmatched:
            print(f"  · {r.article.title!r}")
            print(f"      update_time={date_from_ts(r.article.update_time)}  url={r.article.url}")

    # 反向：publish.md 上仍标"待发布"但没被公众号侧的任何文章命中
    matched_slugs = set(decisions_will_apply.keys())
    pending_unhit = [
        r for r in rows
        if r.status == "待发布"
        and (r.filename[:-3] if r.filename.endswith(".md") else r.filename) not in matched_slugs
    ]
    if pending_unhit:
        print(f"\n[publish.md 待发布但本次同步未命中] {len(pending_unhit)} 条（公众号上可能确实还没发）")
        for r in pending_unhit:
            print(f"  · {r.filename}  «{r.title}»")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--apply", action="store_true",
                   help="真改 publish.md；默认 dry-run")
    p.add_argument("--include-drafts", action="store_true",
                   help="同时拉草稿箱 material/batchget_material（草稿无 url）")
    p.add_argument("--min-confidence", choices=["high", "medium", "low"], default="medium",
                   help="apply 的最低置信度。--min-confidence low 仅 dry-run 时允许")
    args = p.parse_args()

    if args.apply and args.min_confidence == "low":
        sys.exit("ERR: --min-confidence low 不能配 --apply（低置信度需人工 review）")

    wx_env = load_wechat_env()
    print(f"[1/4] 获取 access_token（{wx_env['api_base']}）")
    access_token = get_access_token(wx_env)
    print("  ✓ token 就绪")

    print("[2/4] 拉公众号已群发图文（freepublish/batchget）")
    raw_items = fetch_all(wx_env, access_token, "/cgi-bin/freepublish/batchget", {"no_content": 1})
    articles = parse_freepublish(raw_items)
    print(f"  ✓ 已群发 {len(raw_items)} 个素材，包含 {len(articles)} 篇文章")

    if args.include_drafts:
        print("[2b] 拉草稿箱（material/batchget_material type=news）")
        raw_drafts = fetch_all(
            wx_env, access_token, "/cgi-bin/material/batchget_material", {"type": "news"},
        )
        drafts = parse_drafts(raw_drafts)
        articles.extend(drafts)
        print(f"  ✓ 草稿 {len(raw_drafts)} 个素材，包含 {len(drafts)} 篇文章")

    print("[3/4] 加载项目侧标题字典")
    text = PUBLISH_MD.read_text(encoding="utf-8")
    rows, lines = parse_publish_md(text)
    h1s = load_analysis_h1s()
    match_dict = build_match_dict(rows, h1s)
    print(f"  ✓ publish.md 行 {len(rows)} 条 + analysis_report H1 {len(h1s)} 篇 = 字典 {len(match_dict)} 项")

    print("[4/4] 匹配 + 决策")
    results = match_articles(articles, match_dict)

    min_conf = args.min_confidence
    conf_rank = {"high": 3, "medium": 2, "low": 1, "none": 0}
    threshold = conf_rank[min_conf]
    decisions_will_apply = dedupe_by_slug([r for r in results if conf_rank[r.confidence] >= threshold])
    low_conf = [r for r in results if r.confidence == "low" and conf_rank[r.confidence] < threshold]
    unmatched = [r for r in results if r.confidence == "none"]

    new_lines, will_change = apply_changes(lines, rows, decisions_will_apply)
    print_dry_run(decisions_will_apply, unmatched, low_conf, rows, decisions_will_apply, will_change)

    if not args.apply:
        print("\n(dry-run。加 --apply 真正写入 publish.md。)")
        return 0

    if not will_change:
        print("\n没有需要写入的变更。")
        return 0

    atomic_write(PUBLISH_MD, new_lines)
    print(f"\n✅ 已写入 {PUBLISH_MD.relative_to(REPO_ROOT)}（{len(will_change)} 条变更）")
    print("后续：python3 scripts/build_reports_index.py  # 同步进 reports.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""扫描 src/analysis_report/*.md，从约定的标题/表格/段落提取元数据，写入 db.sqlite。

数据流：
    Markdown 报告 + publish.md → parse → INSERT into reports + report_highlights
    （阶段 4 后 publish.md 的 SoR 身份会被 src/data/publish_history.jsonl 接管）

reports.json 不再由本脚本写出，统一由 `scripts/init_db.py export-json` 从 DB dump。
site/ 仍读 JSON 不变。

DB schema 约束（详见 scripts/init_db.py）自动保证：
    - slug 唯一（PRIMARY KEY）
    - original_url 唯一（UNIQUE，防重复抓取）
    - published_state ∈ {pending, draft, excluded, published} 或 NULL（CHECK）
    - stars/forks/age_months 非负（CHECK）
"""
from __future__ import annotations

import json
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORTS_DIR = ROOT / "src" / "analysis_report"
ENRICH_JSON = ROOT / "src" / "data" / "repo_enrich.json"

# init_db.py 与本文件同目录，import 直读
sys.path.insert(0, str(ROOT / "src" / "scripts"))
from init_db import get_connection, ensure_schema, normalize_url  # noqa: E402


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


# 注：阶段 4 起 publish 字段不再从 publish.md 解析（该文件已删除），
# 而由 init_db.py 从 src/data/publish_history.jsonl → v_publish_latest 反查回填。


# ---------- 单篇报告解析（纯函数，无 I/O） ----------
H1_SUFFIX_RE = re.compile(r"\s*深度分析报告\s*$")
GITHUB_URL_RE = re.compile(r"^>\s*GitHub:\s*(https?://github\.com/\S+)", re.I)
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$")
TABLE_ROW_RE = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$")


def parse_int_with_commas(s: str) -> int | None:
    m = re.search(r"([\d,]+)", s)
    if not m:
        return None
    try:
        return int(m.group(1).replace(",", ""))
    except ValueError:
        return None


def parse_age_months(raw: str) -> float | None:
    m = re.search(r"([\d.]+)\s*个月", raw)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None
    m = re.search(r"([\d.]+)\s*年", raw)
    if m:
        try:
            return round(float(m.group(1)) * 12, 1)
        except ValueError:
            return None
    return None


KNOWN_LANGUAGES = (
    "TypeScript", "JavaScript", "Python", "Rust", "Go", "Java", "Kotlin", "Swift",
    "C++", "C#", "C", "Ruby", "PHP", "Shell", "Bash", "Lua", "Scala", "Clojure",
    "TSX", "Vue", "Svelte", "GLSL", "HLSL", "CUDA", "Markdown", "HTML", "CSS",
    "Dart", "Zig", "Elixir", "Haskell", "OCaml", "PowerShell", "Batchfile",
    "ReStructuredText", "C Header", "Objective-C",
)


def parse_language(raw: str) -> str | None:
    m = re.search(r"[（(]\s*([A-Za-z+#./_-]+(?:\s*[A-Za-z+#./_-]+)?)\s+[\d.]+%", raw)
    if m:
        return m.group(1).strip()
    m = re.search(r"\d+(?:[,，]\d+)*\s*行\s*([A-Za-z+#./_-]+)", raw)
    if m:
        return m.group(1).strip()
    for lang in sorted(KNOWN_LANGUAGES, key=len, reverse=True):
        if re.search(rf"\b{re.escape(lang)}\b", raw):
            return lang
    return None


def parse_heat(raw: str) -> str | None:
    m = re.match(r"\s*([^（(:：]+)", raw)
    return m.group(1).strip() if m else None


def split_section_body(lines: list[str], start: int) -> list[str]:
    body: list[str] = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        body.append(line)
    return body


def extract_summary(body_lines: list[str]) -> str | None:
    for line in body_lines:
        s = line.strip()
        if s:
            return s
    return None


def extract_highlights(body_lines: list[str], n: int = 3) -> list[str]:
    items: list[str] = []
    for line in body_lines:
        s = line.strip()
        if not s:
            continue
        m = re.match(r"^(?:\d+[.)]|\-|\*)\s+(.*)$", s)
        if not m:
            continue
        text = m.group(1).strip()
        text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
        text = re.split(r"——|--|—", text, maxsplit=1)[0].strip()
        text = re.split(r"[。；;]", text, maxsplit=1)[0].strip()
        if text:
            items.append(text)
        if len(items) >= n:
            break
    return items


def extract_cover(body_lines: list[str]) -> str | None:
    for line in body_lines:
        m = IMG_RE.search(line)
        if m:
            url = m.group(1).strip().split()[0]
            if url.startswith("http"):
                return url
    return None


def parse_profile_table(body_lines: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in body_lines:
        if "---" in line:
            continue
        m = TABLE_ROW_RE.match(line.rstrip())
        if not m:
            continue
        key, val = m.group(1).strip(), m.group(2).strip()
        if key in {"维度", ""} or key.lower() == "key":
            continue
        out[key] = val
    return out


def parse_report(path: Path, publish_index: dict[str, dict]) -> dict | None:
    slug = path.stem.lower()
    # 门禁：三阶段分析的中间产物（如 *_phase3.md / *.phase3.md）不应入库，
    # 正式合并版才是报告。文件名以 phase[N] 结尾者一律跳过，防止污染 reports。
    if re.search(r"[._-]phase\d*$", path.stem, re.I):
        print(f"⚠️  跳过疑似中间产物（phase 文件）: {path.name}", file=sys.stderr)
        return None
    text = read_text(path)
    lines = text.splitlines()

    title: str | None = None
    original_url: str | None = None
    sections: dict[str, list[str]] = {}

    for i, raw_line in enumerate(lines):
        if title is None and raw_line.startswith("# "):
            title = H1_SUFFIX_RE.sub("", raw_line[2:].strip())
        if original_url is None:
            m = GITHUB_URL_RE.match(raw_line)
            if m:
                # 先去掉常见尾部标点，再走全局 normalize_url（rstrip('/').lower()）
                original_url = normalize_url(m.group(1).rstrip(".,;"))
        m = SECTION_RE.match(raw_line)
        if m:
            sections[m.group(1).strip()] = split_section_body(lines, i)

    if not title:
        return None

    summary = extract_summary(sections.get("一句话总结", []))
    highlights = extract_highlights(sections.get("值得关注的理由", []))
    cover = extract_cover(sections.get("项目展示", []))
    profile_raw = parse_profile_table(sections.get("项目画像", []))

    stars = forks = None
    star_fork_raw = profile_raw.get("Star / Fork") or profile_raw.get("Star/Fork")
    if star_fork_raw:
        parts = re.split(r"[/／]", star_fork_raw, maxsplit=1)
        if len(parts) == 2:
            stars = parse_int_with_commas(parts[0])
            forks = parse_int_with_commas(parts[1])

    loc_raw = profile_raw.get("代码行数")
    language = parse_language(loc_raw) if loc_raw else None

    age_raw = profile_raw.get("项目年龄")
    age_months = parse_age_months(age_raw) if age_raw else None

    heat_raw = profile_raw.get("热度定位")
    heat = parse_heat(heat_raw) if heat_raw else None

    mtime = datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d")

    pub = publish_index.get(slug, {})

    return {
        "slug": slug,
        "title": title,
        "original_url": original_url,
        "summary": summary,
        "highlights": highlights,
        "stars": stars,
        "forks": forks,
        "language": language,
        "loc_raw": loc_raw,
        "age_months": age_months,
        "age_raw": age_raw,
        "stage": profile_raw.get("开发阶段"),
        "contribution": profile_raw.get("贡献模式"),
        "heat": heat,
        "heat_raw": heat_raw,
        "quality": profile_raw.get("质量评级"),
        "license": profile_raw.get("许可证"),
        "cover": cover,
        "mtime": mtime,
        "published_state": pub.get("state"),
        "published_at": pub.get("at"),
        "published_title": pub.get("title"),
    }


# ---------- enrich 兜底（gh api 缓存补 md 解析不到的客观字段） ----------

def load_enrich() -> dict[str, dict]:
    """读 repo_enrich.json（fetch_repo_enrich.py 产出的 gh api 缓存）。
    key 为 normalize_url(original_url)，与 reports.original_url 对齐。不存在则空 dict。"""
    if not ENRICH_JSON.exists():
        return {}
    try:
        return json.loads(ENRICH_JSON.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}


# 仅客观、有 gh api 等价物的字段才兜底；loc_raw/stage/quality 等主观字段不补
ENRICH_FIELDS = ("stars", "forks", "language", "license", "age_months")


def apply_enrich(reports: list[dict], enrich: dict[str, dict]) -> int:
    """对每篇报告，若某字段为 None 且缓存有值则补上（md/SoR 优先，只填 None）。
    返回补全的字段总数（供日志）。"""
    filled = 0
    for r in reports:
        e = enrich.get(r.get("original_url") or "")
        if not e:
            continue
        for f in ENRICH_FIELDS:
            if r.get(f) is None and e.get(f) is not None:
                r[f] = e[f]
                filled += 1
    return filled


# ---------- 写入 DB ----------

REPORT_COLS = (
    "slug", "title", "original_url", "summary", "stars", "forks",
    "language", "loc_raw", "age_months", "age_raw", "stage", "contribution",
    "heat", "heat_raw", "quality", "license", "cover", "mtime",
    "published_state", "published_at", "published_title",
)


def write_reports(conn: sqlite3.Connection, reports: list[dict]) -> None:
    """事务内全量重写 reports + report_highlights。"""
    placeholders = ",".join("?" * len(REPORT_COLS))
    insert_sql = f"INSERT INTO reports ({','.join(REPORT_COLS)}) VALUES ({placeholders})"
    with conn:  # auto-commit on success, rollback on exception
        conn.execute("DELETE FROM report_highlights")
        conn.execute("DELETE FROM reports")
        for r in reports:
            row = tuple(r[c] for c in REPORT_COLS)
            conn.execute(insert_sql, row)
            for pos, text in enumerate(r["highlights"]):
                conn.execute(
                    "INSERT INTO report_highlights (slug, position, text) VALUES (?, ?, ?)",
                    (r["slug"], pos, text),
                )


def main() -> int:
    if not REPORTS_DIR.is_dir():
        print(f"❌ 找不到报告目录: {REPORTS_DIR}", file=sys.stderr)
        return 1

    # 阶段 4 起：publish 字段不再从 publish.md 解析，由 init_db.py reconcile-published
    # 在本脚本之后从 v_publish_latest 反查更新。这里给 parse_report 传空 publish_index
    # 即可（其余 parse 逻辑不变）。
    publish_index: dict[str, dict] = {}
    md_files = sorted(REPORTS_DIR.glob("*.md"))
    NON_REPORT = {"repos", "README"}
    reports: list[dict] = []
    skipped = 0

    for p in md_files:
        if p.stem in NON_REPORT:
            skipped += 1
            continue
        rep = parse_report(p, publish_index)
        if rep is None:
            skipped += 1
            continue
        reports.append(rep)

    # enrich 兜底：md 解析不到的客观字段（stars/forks/language/license/age_months）
    # 用 gh api 缓存补全（md/SoR 优先，只填 None）。缓存由 fetch_repo_enrich.py 维护。
    n_enriched = apply_enrich(reports, load_enrich())

    conn = get_connection()
    ensure_schema(conn)
    try:
        write_reports(conn, reports)
        # 阶段 4：写完 reports 后立即从 v_publish_latest 反查回填 published_* 字段。
        # 前提是 init_db.py seed-publish 已在本脚本之前跑过（CI workflow 已编排）。
        sys.path.insert(0, str(ROOT / "src" / "scripts"))
        from init_db import reconcile_reports_published
        n_reconciled = reconcile_reports_published(conn)
    except sqlite3.IntegrityError as e:
        print(f"❌ 写入 DB 失败（schema 约束违规）: {e}", file=sys.stderr)
        return 2
    finally:
        conn.close()

    keys = ("stars", "forks", "language", "license", "age_months", "heat", "summary", "cover", "original_url")
    print(f"✅ 写入 {len(reports)} 篇报告，跳过 {skipped} 篇 → db.sqlite (reports + report_highlights)")
    print(f"   enrich 兜底补全字段数（stars/forks/language/license/age_months）: {n_enriched}")
    print(f"   从 v_publish_latest 反查回填 published_* 字段: {n_reconciled} 篇")
    print("   字段非空率:")
    for k in keys:
        n = sum(1 for r in reports if r.get(k) is not None)
        pct = n * 100 / max(len(reports), 1)
        print(f"     {k:<14} {n:>4} / {len(reports)} ({pct:5.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
扫描 src/analysis_report/*.md，从已有 Markdown 结构提取元数据，输出 src/data/reports.json。
报告原文不做修改 —— 所有元数据来自约定的标题/表格/段落。

字段说明（缺失时设为 null）：
    slug          文件名去 .md
    title         一级标题去掉「深度分析报告」尾缀
    originalUrl   `> GitHub: <url>` 行
    summary       「一句话总结」段首
    highlights    「值得关注的理由」前 3 条要点的纯文本
    stars / forks 项目画像表「Star / Fork」拆分（int）
    language      项目画像表「代码行数」中识别到的主语言
    locKept       项目画像表「代码行数」原文（人类可读）
    ageMonths     项目画像表「项目年龄」按月折算（float）
    ageRaw        原文
    stage         开发阶段
    contribution  贡献模式
    heat          热度定位（取冒号前级别）
    quality       质量评级原文
    license       许可证（若表中有）
    cover         「项目展示」段首张图片 URL
    mtime         文件 mtime（YYYY-MM-DD）
    published     在 src/publish.md 命中的发布状态（"已发布:{date}" / "待发布" / null）
    publishedTitle 在 publish.md 的标题列文本
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "src" / "analysis_report"
PUBLISH_FILE = ROOT / "src" / "publish.md"
OUTPUT_FILE = ROOT / "src" / "data" / "reports.json"


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


# ---------- publish.md 解析 ----------
def parse_publish_index() -> dict[str, dict]:
    if not PUBLISH_FILE.exists():
        return {}
    out: dict[str, dict] = {}
    in_excluded = False
    for line in read_text(PUBLISH_FILE).splitlines():
        line = line.strip()
        if line.startswith("## 不发布"):
            in_excluded = True
            continue
        m = re.match(r"\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", line)
        if not m:
            continue
        link_text, link_path, title, status = m.groups()
        slug = link_text.replace(".md", "").strip()
        if "/" in link_path:
            slug = Path(link_path).stem
        slug = slug.lower()  # 与 Astro 一致
        info = {"title": title.strip()}
        if in_excluded:
            info["published"] = "excluded"
            info["reason"] = status.strip()
        elif re.match(r"\d{4}-\d{2}-\d{2}", status):
            info["published"] = f"published:{status.strip()}"
        else:
            info["published"] = "pending"
        out[slug] = info
    return out


# ---------- 单篇报告解析 ----------
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
    """从 '35 个月（2023-05 至今）' / '5.4 年' / '17.5 个月（首次提交 2024-10-07）' 提取月数"""
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
    """从 '23,288 行（Python 84.3%, GLSL 3.4%）' 之类提取主语言。
    顺序：百分比格式 → 「N 行 Python」格式 → 已知语言名兜底。"""
    m = re.search(r"[（(]\s*([A-Za-z+#./_-]+(?:\s*[A-Za-z+#./_-]+)?)\s+[\d.]+%", raw)
    if m:
        return m.group(1).strip()
    m = re.search(r"\d+(?:[,，]\d+)*\s*行\s*([A-Za-z+#./_-]+)", raw)
    if m:
        return m.group(1).strip()
    # 兜底：扫已知语言名（按长度倒序避免 C 被截到 C++）
    for lang in sorted(KNOWN_LANGUAGES, key=len, reverse=True):
        if re.search(rf"\b{re.escape(lang)}\b", raw):
            return lang
    return None


def parse_heat(raw: str) -> str | None:
    """从 '大众热门（32K+ Star，AI coding 赛道头部）' 取「大众热门」"""
    m = re.match(r"\s*([^（(:：]+)", raw)
    return m.group(1).strip() if m else None


def split_section_body(lines: list[str], start: int) -> list[str]:
    """返回从 start+1 行起到下一个二级标题之前的内容（已去除空白行首尾）"""
    body: list[str] = []
    for line in lines[start + 1 :]:
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
    """从「值得关注的理由」抽前 n 条要点，去掉编号和加粗符"""
    items: list[str] = []
    for line in body_lines:
        s = line.strip()
        if not s:
            continue
        # 兼容 "1. **xxx**" / "- **xxx**" / "1) xxx"
        m = re.match(r"^(?:\d+[.)]|\-|\*)\s+(.*)$", s)
        if not m:
            continue
        text = m.group(1).strip()
        # 取首句（句号前）并清除粗体
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
            url = m.group(1).strip().split()[0]  # 去掉可能的 " title"
            if url.startswith("http"):
                return url
    return None


def parse_profile_table(body_lines: list[str]) -> dict[str, str]:
    """项目画像表 → {标题列文本: 数据列文本}"""
    out: dict[str, str] = {}
    for line in body_lines:
        if "---" in line:  # 表头分隔
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
    # Astro 的 content collection 会把文件名 lowercase 作为 entry.id；
    # 此处保持一致，避免站点侧反查元数据时大小写不匹配。
    slug = path.stem.lower()
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
                original_url = m.group(1).rstrip(".,;")
        m = SECTION_RE.match(raw_line)
        if m:
            sections[m.group(1).strip()] = split_section_body(lines, i)

    if not title:
        # 无 h1，跳过
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
        "originalUrl": original_url,
        "summary": summary,
        "highlights": highlights,
        "stars": stars,
        "forks": forks,
        "language": language,
        "locRaw": loc_raw,
        "ageMonths": age_months,
        "ageRaw": age_raw,
        "stage": profile_raw.get("开发阶段"),
        "contribution": profile_raw.get("贡献模式"),
        "heat": heat,
        "heatRaw": heat_raw,
        "quality": profile_raw.get("质量评级"),
        "license": profile_raw.get("许可证"),
        "cover": cover,
        "mtime": mtime,
        "published": pub.get("published"),
        "publishedTitle": pub.get("title"),
    }


def main() -> int:
    if not REPORTS_DIR.is_dir():
        print(f"❌ 找不到报告目录: {REPORTS_DIR}", file=sys.stderr)
        return 1

    publish_index = parse_publish_index()
    md_files = sorted(REPORTS_DIR.glob("*.md"))
    # 显式排除：非报告文件
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

    # 统计字段非空率
    if reports:
        keys = ("stars", "language", "ageMonths", "heat", "summary", "cover", "originalUrl")
        coverage = {k: sum(1 for r in reports if r.get(k) is not None) for k in keys}
    else:
        coverage = {}

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(reports, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"✅ 解析 {len(reports)} 篇报告，跳过 {skipped} 篇 → {OUTPUT_FILE.relative_to(ROOT)}")
    print("   字段非空率:")
    for k, n in coverage.items():
        pct = n * 100 / max(len(reports), 1)
        print(f"     {k:<14} {n:>4} / {len(reports)} ({pct:5.1f}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

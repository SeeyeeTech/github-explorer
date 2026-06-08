#!/usr/bin/env python3
"""repo-miner Phase 2（元分析）确定性数据采集。

把原本写在 phase-2-meta.md prompt 里、让子 agent 现场拼的 git / tokei 命令，
一次性在本脚本里跑完并算成结构化 JSON。子 agent 不再跑命令，只读这份 JSON 做
判断和写作。好处：确定性部分 0 次 LLM 调用、限流/异常用确定逻辑兜底、产出稳定。

用法：
    python3 src/scripts/collect_repo_facts.py <LOCAL_PATH> [--full-name owner/repo] [--out PATH]

- <LOCAL_PATH>：已 clone 的本地仓库路径（repo-miner 准备阶段产出，如 /tmp/repo-miner-foo）
- --full-name：owner/repo，缺省时从 git remote 推断
- --out：JSON 落地路径，缺省 tmp/repo-facts-<repo>.json（临时文件，不入 git）

脚本把 JSON 写入 --out 并把该路径打印到 stdout（供 prompt 捕获后 Read）。
所有指标单独 try，缺失记 null 并写入 _warnings，绝不因单项失败中断整体采集。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone

WARNINGS: list[str] = []


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"[collect_repo_facts] warn: {msg}", file=sys.stderr)


def run(args: list[str], cwd: str | None = None, timeout: int = 120) -> str:
    """跑命令返回 stdout，失败返回空串（不抛）。"""
    try:
        out = subprocess.run(
            args, cwd=cwd, capture_output=True, text=True,
            timeout=timeout, check=False,
        )
        if out.returncode != 0 and not out.stdout:
            warn(f"命令非零退出 {args[:2]}: {out.stderr.strip()[:200]}")
        return out.stdout
    except FileNotFoundError:
        warn(f"命令不存在: {args[0]}")
        return ""
    except subprocess.TimeoutExpired:
        warn(f"命令超时: {' '.join(args[:3])}")
        return ""


def git(repo: str, *args: str, timeout: int = 120) -> str:
    return run(["git", *args], cwd=repo, timeout=timeout)


# ---------------------------------------------------------------- 2.1 代码规模

# 依赖清单的探测顺序：(文件存在判断, 计数函数)
def _count_deps(repo: str) -> dict:
    res = {"runtime": None, "dev": None, "source": None}
    p = lambda name: os.path.join(repo, name)

    if os.path.exists(p("package.json")):
        try:
            with open(p("package.json"), encoding="utf-8") as f:
                pkg = json.load(f)
            res.update(
                runtime=len(pkg.get("dependencies") or {}),
                dev=len(pkg.get("devDependencies") or {}),
                source="package.json",
            )
            return res
        except Exception as e:  # noqa: BLE001
            warn(f"解析 package.json 失败: {e}")

    if os.path.exists(p("Cargo.toml")):
        meta = run(["cargo", "metadata", "--no-deps", "--format-version", "1"], cwd=repo)
        try:
            data = json.loads(meta)
            res.update(runtime=len(data["packages"][0].get("dependencies", [])), source="Cargo.toml")
            return res
        except Exception:  # noqa: BLE001
            # cargo 不可用时退化为正则数 [dependencies] 段
            res.update(runtime=_count_toml_deps(p("Cargo.toml")), source="Cargo.toml(regex)")
            return res

    if os.path.exists(p("go.mod")):
        try:
            with open(p("go.mod"), encoding="utf-8") as f:
                txt = f.read()
            # require 块内的行 + 单行 require
            res.update(runtime=len(re.findall(r"^\s+[\w./-]+\s+v", txt, re.M)), source="go.mod")
            return res
        except Exception as e:  # noqa: BLE001
            warn(f"解析 go.mod 失败: {e}")

    for pyfile in ("pyproject.toml", "requirements.txt"):
        if os.path.exists(p(pyfile)):
            try:
                with open(p(pyfile), encoding="utf-8") as f:
                    lines = [ln for ln in f if ln.strip() and not ln.strip().startswith("#")]
                res.update(runtime=len(lines), source=pyfile)
                return res
            except Exception as e:  # noqa: BLE001
                warn(f"解析 {pyfile} 失败: {e}")

    return res


def _count_toml_deps(path: str) -> int | None:
    try:
        with open(path, encoding="utf-8") as f:
            txt = f.read()
        m = re.search(r"^\[dependencies\](.*?)(^\[|\Z)", txt, re.S | re.M)
        if not m:
            return 0
        return len([ln for ln in m.group(1).splitlines() if "=" in ln])
    except Exception:  # noqa: BLE001
        return None


def collect_code_scale(repo: str) -> dict:
    out = {
        "total_code_lines": None, "total_comment_lines": None, "comment_ratio": None,
        "file_count": None, "languages": [], "dependencies": _count_deps(repo),
    }
    if not shutil.which("tokei"):
        warn("tokei 未安装，跳过代码规模统计")
        return out

    raw = run(["tokei", "--output", "json"], cwd=repo)
    if not raw:
        return out
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        warn(f"tokei JSON 解析失败: {e}")
        return out

    total_code = total_comment = total_files = 0
    langs = []
    for name, stat in data.items():
        if name == "Total":
            continue
        code = stat.get("code", 0)
        comments = stat.get("comments", 0)
        # tokei v12+ 用 reports 列表数文件；老版本有 'stats' 兜底
        nfiles = len(stat.get("reports", []) or stat.get("stats", []) or [])
        total_code += code
        total_comment += comments
        total_files += nfiles
        if code > 0:
            langs.append({"name": name, "code": code, "files": nfiles})

    langs.sort(key=lambda x: x["code"], reverse=True)
    for lang in langs:
        lang["pct"] = round(lang["code"] / total_code * 100, 1) if total_code else 0.0

    out.update(
        total_code_lines=total_code,
        total_comment_lines=total_comment,
        comment_ratio=round(total_comment / total_code, 3) if total_code else None,
        file_count=total_files,
        languages=langs[:12],
    )
    return out


# ---------------------------------------------------------------- 2.2 开发节奏

def _parse_iso(s: str) -> datetime | None:
    s = s.strip()
    if not s:
        return None
    try:
        # git %ai 形如 "2023-05-01 12:00:00 +0800"
        return datetime.strptime(s, "%Y-%m-%d %H:%M:%S %z")
    except ValueError:
        try:
            return datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return None


def collect_dev_rhythm(repo: str) -> dict:
    out = {
        "first_commit": None, "last_commit": None, "total_commits": None,
        "age_months": None, "commits_last_30": None, "commits_last_90": None,
        "commits_last_365": None, "monthly_distribution": {}, "weekday_count": None,
        "weekend_count": None, "weekend_pct": None, "night_pct": None,
        "dev_stage": None, "dev_mode": None,
    }

    first = git(repo, "log", "--reverse", "--format=%H|%ai|%s").splitlines()
    last = git(repo, "log", "--format=%H|%ai|%s", "-1").splitlines()

    def _commit_obj(line: str) -> dict | None:
        parts = line.split("|", 2)
        if len(parts) < 2:
            return None
        dt = _parse_iso(parts[1])
        return {"hash": parts[0][:12], "date": dt.date().isoformat() if dt else None,
                "subject": parts[2] if len(parts) > 2 else ""}

    if first:
        out["first_commit"] = _commit_obj(first[0])
    if last:
        out["last_commit"] = _commit_obj(last[0])

    count = git(repo, "rev-list", "--count", "HEAD").strip()
    out["total_commits"] = int(count) if count.isdigit() else None

    now = datetime.now(timezone.utc)
    # 一次性取所有 commit 的时间戳（%aI ISO8601），本地算各窗口，省得多次 git
    iso_lines = [ln for ln in git(repo, "log", "--format=%aI").splitlines() if ln.strip()]
    dts: list[datetime] = []
    for ln in iso_lines:
        try:
            dts.append(datetime.fromisoformat(ln.strip()))
        except ValueError:
            continue

    if dts:
        def within(days: int) -> int:
            return sum(1 for d in dts if (now - d.astimezone(timezone.utc)).days <= days)
        out["commits_last_30"] = within(30)
        out["commits_last_90"] = within(90)
        out["commits_last_365"] = within(365)

        first_dt = min(dts).astimezone(timezone.utc)
        out["age_months"] = round((now - first_dt).days / 30.4, 1)

        # 月度分布 YYYY-MM -> count
        monthly = Counter(d.strftime("%Y-%m") for d in dts)
        out["monthly_distribution"] = dict(sorted(monthly.items()))

        # 周末 / 工作日（isoweekday 6,7 为周末）
        weekend = sum(1 for d in dts if d.isoweekday() >= 6)
        weekday = len(dts) - weekend
        out["weekend_count"] = weekend
        out["weekday_count"] = weekday
        out["weekend_pct"] = round(weekend / len(dts) * 100, 1)

        # 深夜（本地 commit 时间 0:00-6:00 + 22:00-24:00）
        night = sum(1 for d in dts if d.hour < 6 or d.hour >= 22)
        out["night_pct"] = round(night / len(dts) * 100, 1)

        # ---- 确定性分级（阈值，与原 prompt 描述一致）----
        last_dt = max(dts).astimezone(timezone.utc)
        days_since_last = (now - last_dt).days
        recent_monthly_avg = (out["commits_last_90"] or 0) / 3
        if days_since_last > 180:
            out["dev_stage"] = "已放弃"
        elif recent_monthly_avg > 20:
            out["dev_stage"] = "密集开发"
        elif recent_monthly_avg >= 5:
            out["dev_stage"] = "稳定维护"
        else:
            out["dev_stage"] = "低维护"

        amateur = out["weekend_pct"] > 35 or out["night_pct"] > 45
        out["dev_mode"] = "业余 Side Project" if amateur else "职业项目"

    return out


# ---------------------------------------------------------------- 2.3 演化轨迹

def collect_evolution(repo: str, full_name: str | None = None) -> dict:
    out = {
        "tags": [], "latest_tag": None, "tag_count": None, "release_count": None,
        "core_files": [], "hot_dirs": [], "commit_type_distribution": {},
        "version_strategy": None,
    }

    tags = [t for t in git(repo, "tag", "--sort=-version:refname").splitlines() if t.strip()]
    out["tags"] = tags[:20]
    out["tag_count"] = len(tags)
    out["latest_tag"] = tags[0] if tags else None
    if tags:
        if all(re.match(r"v?\d+\.\d+", t) for t in tags[:10]):
            out["version_strategy"] = "语义化版本"
        elif all(re.match(r"v?\d{4}", t) for t in tags[:10]):
            out["version_strategy"] = "日期版本"
        else:
            out["version_strategy"] = "无明显规律"

    # gh release（可选，需网络/认证）。优先用 --repo full_name（不依赖 cwd remote）；
    # 无网络/无认证/非 GitHub repo 时静默跳过，不影响其余采集。
    if shutil.which("gh") and full_name:
        rel = run(["gh", "release", "list", "--repo", full_name, "--limit", "100"], timeout=60)
        if rel.strip():
            out["release_count"] = len([ln for ln in rel.splitlines() if ln.strip()])

    # 文件变更热力（核心文件） + 目录热点
    name_only = git(repo, "log", "--format=", "--name-only")
    files = Counter()
    dirs = Counter()
    for ln in name_only.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        files[ln] += 1
        if "/" in ln:
            dirs["/".join(ln.split("/")[:2])] += 1
    out["core_files"] = [{"path": f, "changes": c} for f, c in files.most_common(10)]
    out["hot_dirs"] = [{"path": d, "changes": c} for d, c in dirs.most_common(15)]

    # commit 类型分布（取最近 200 条，与原 prompt 一致）
    subjects = git(repo, "log", "--format=%s", "-n", "200").splitlines()
    buckets = Counter()
    for s in subjects:
        if re.search(r"\b(fix|bug)", s, re.I):
            buckets["fix"] += 1
        elif re.search(r"\b(feat|add)", s, re.I):
            buckets["feature"] += 1
        elif re.search(r"refactor", s, re.I):
            buckets["refactor"] += 1
        elif re.search(r"\bdoc", s, re.I):
            buckets["docs"] += 1
        elif re.search(r"\btest", s, re.I):
            buckets["test"] += 1
        else:
            buckets["other"] += 1
    total = sum(buckets.values()) or 1
    out["commit_type_distribution"] = {
        k: {"count": buckets.get(k, 0), "pct": round(buckets.get(k, 0) / total * 100, 1)}
        for k in ("feature", "fix", "refactor", "docs", "test", "other")
    }
    return out


def collect_contributors(repo: str) -> dict:
    sl = git(repo, "shortlog", "-sn", "--all", "--no-merges")
    rows = []
    for ln in sl.splitlines():
        m = re.match(r"\s*(\d+)\s+(.*)", ln)
        if m:
            rows.append({"name": m.group(2).strip(), "commits": int(m.group(1))})
    total = sum(r["commits"] for r in rows) or 1
    top_share = round(rows[0]["commits"] / total * 100, 1) if rows else None
    return {
        "count": len(rows),
        "top": rows[:10],
        "top_author_share_pct": top_share,
        "collaboration": (
            "单人主导" if top_share and top_share > 90
            else "核心少数 + 社区" if len(rows) > 1 else "未知"
        ),
    }


# ============================================================ Phase 1 网络采集
# 以下全部依赖 gh（联网 + 认证）。每个子项单独 try，任一失败记 _warnings 并置 null，
# 绝不中断整体；无 gh / 无网络时整个 network 块为 null，不影响 Phase 2 离线指标。

# README 媒体排除关键词（badge / CI / 统计 / 赞助 / 社交小图标）
_BADGE_KEYWORDS = (
    "shields.io", "badgen.net", "forthebadge.com", "travis-ci", "circleci",
    "coveralls", "codecov", "/workflows/", "/actions/", "github-readme-stats",
    "hits.dwyl.com", "visitor-badge", "komarev.com", "buymeacoffee", "ko-fi",
    "patreon", "opencollective", "twitter.com/intent", "discord.gg", "badge",
)


def gh_json(args: list[str], timeout: int = 90):
    """跑 gh 并 json.loads，失败返回 None（已记 warning）。"""
    raw = run(["gh", *args], timeout=timeout)
    if not raw.strip():
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        warn(f"gh JSON 解析失败 {args[:3]}: {e}")
        return None


def _heat_level(stars: int | None) -> str | None:
    if stars is None:
        return None
    if stars < 50:
        return "极小众"
    if stars < 500:
        return "小众精品"
    if stars < 5000:
        return "中等热度"
    return "大众热门"


def collect_repo_basics(full_name: str) -> dict:
    fields = (
        "name,description,url,stargazerCount,forkCount,watchers,issues,"
        "pullRequests,licenseInfo,primaryLanguage,languages,createdAt,updatedAt,"
        "pushedAt,isArchived,isFork,homepageUrl,repositoryTopics,diskUsage,defaultBranchRef"
    )
    d = gh_json(["repo", "view", full_name, "--json", fields])
    if not d:
        return {}

    # languages: [{size, node:{name}}] → 按 size 占比
    langs_raw = d.get("languages") or []
    total_size = sum(l.get("size", 0) for l in langs_raw) or 0
    languages = []
    for l in sorted(langs_raw, key=lambda x: x.get("size", 0), reverse=True):
        name = (l.get("node") or {}).get("name")
        if name:
            languages.append({
                "name": name,
                "pct": round(l.get("size", 0) / total_size * 100, 1) if total_size else 0.0,
            })

    # repositoryTopics 可能是 ["x"] 或 [{"name":"x"}]
    topics = []
    for t in (d.get("repositoryTopics") or []):
        topics.append(t if isinstance(t, str) else t.get("name"))
    topics = [t for t in topics if t]

    lic = d.get("licenseInfo") or {}
    stars = d.get("stargazerCount")
    return {
        "stars": stars,
        "forks": d.get("forkCount"),
        "watchers": (d.get("watchers") or {}).get("totalCount"),
        "open_issues": (d.get("issues") or {}).get("totalCount"),
        "open_prs": (d.get("pullRequests") or {}).get("totalCount"),
        "license": lic.get("spdxId") or lic.get("name"),
        "primary_language": (d.get("primaryLanguage") or {}).get("name"),
        "languages": languages[:12],
        "created_at": d.get("createdAt"),
        "updated_at": d.get("updatedAt"),
        "pushed_at": d.get("pushedAt"),
        "is_archived": d.get("isArchived"),
        "is_fork": d.get("isFork"),
        "homepage_url": d.get("homepageUrl") or None,
        "topics": topics,
        "disk_usage_kb": d.get("diskUsage"),
        "default_branch": (d.get("defaultBranchRef") or {}).get("name"),
        "heat_level": _heat_level(stars),
    }


def collect_author(owner: str, repo: str, full_name: str) -> dict:
    out = {
        "login": owner, "type": None, "name": None, "bio": None, "company": None,
        "location": None, "blog": None, "public_repos": None, "followers": None,
        "following": None, "created_at": None, "account_age_years": None,
        "top_repos": [], "repo_rank": None, "contributors": [],
        "contributor_count": None, "top_contributor_share_pct": None,
    }
    u = gh_json(["api", f"users/{owner}"])
    if u:
        out.update(
            type=u.get("type"), name=u.get("name"), bio=u.get("bio"),
            company=u.get("company"), location=u.get("location"), blog=u.get("blog") or None,
            public_repos=u.get("public_repos"), followers=u.get("followers"),
            following=u.get("following"), created_at=u.get("created_at"),
        )
        created = _parse_iso_z(u.get("created_at"))
        if created:
            out["account_age_years"] = round((datetime.now(timezone.utc) - created).days / 365.25, 1)

    repos = gh_json(["api", f"users/{owner}/repos?sort=pushed&per_page=10"]) or []
    for r in repos[:10]:
        out["top_repos"].append({
            "name": r.get("name"), "pushed_at": r.get("pushed_at"),
            "stars": r.get("stargazers_count"), "language": r.get("language"),
            "fork": r.get("fork"),
        })
    for i, r in enumerate(out["top_repos"], start=1):
        if r["name"] == repo:
            out["repo_rank"] = i
            break

    contribs = gh_json(["api", f"repos/{full_name}/contributors?per_page=30"]) or []
    if isinstance(contribs, list):
        rows = [{"login": c.get("login"), "contributions": c.get("contributions", 0)}
                for c in contribs if isinstance(c, dict)]
        out["contributors"] = rows[:10]
        out["contributor_count"] = len(rows)
        total = sum(c["contributions"] for c in rows) or 1
        if rows:
            out["top_contributor_share_pct"] = round(rows[0]["contributions"] / total * 100, 1)
    return out


def _star_page(full_name: str, page: int) -> list[str]:
    raw = run([
        "gh", "api", f"repos/{full_name}/stargazers?per_page=100&page={page}",
        "-H", "Accept: application/vnd.github.star+json",
        "--jq", ".[].starred_at",
    ], timeout=60)
    return [ln.strip() for ln in raw.splitlines() if ln.strip()]


def collect_community(full_name: str, stars: int | None) -> dict:
    out = {"recent_stars": None, "growth_pattern": None, "note": None}
    if not stars:
        out["note"] = "star 数未知，跳过增长采样"
        return out

    # 近期 star 在最后一页：算 last_page（GitHub 上限 400 页 = 40k）只取尾部 1-2 页，
    # 避免对大仓库 --paginate 全量翻页触发限流。
    import math
    last_page = min(400, max(1, math.ceil(stars / 100)))
    sample: list[str] = []
    for pg in {last_page, max(1, last_page - 1)}:
        sample.extend(_star_page(full_name, pg))
    sample = sorted({s for s in sample if s})
    if not sample:
        out["note"] = "stargazers 采样为空（可能已超 GitHub 4 万星翻页上限）"
        return out

    earliest = _parse_iso_z(sample[0])
    latest = _parse_iso_z(sample[-1])
    span_days = (latest - earliest).days if (earliest and latest) else None
    monthly = Counter(s[:7] for s in sample)  # YYYY-MM

    if span_days is not None:
        if span_days < 7:
            pattern = "爆发型（近百星集中在一周内）"
        elif span_days < 30:
            pattern = "高速增长"
        elif span_days < 180:
            pattern = "稳步增长"
        else:
            pattern = "平稳/放缓"
    else:
        pattern = None

    out["recent_stars"] = {
        "sampled": len(sample), "earliest": sample[0], "latest": sample[-1],
        "span_days": span_days, "monthly": dict(sorted(monthly.items())),
    }
    out["growth_pattern"] = pattern
    out["note"] = "基于最近约 100-200 个 stargazer 的 starred_at 采样，pattern 为确定性启发式"
    return out


def collect_ecosystem(full_name: str, basics: dict) -> dict:
    out = {"topic_used": None, "language_used": None, "competitor_candidates": []}
    topics = basics.get("topics") or []
    lang = basics.get("primary_language")
    if not topics:
        out["competitor_candidates"] = []
        return out
    topic = topics[0]
    out["topic_used"] = topic
    out["language_used"] = lang
    # 注意：GitHub 搜索不允许对 qualifier 用 NOT（topic:/language: 都是 qualifier），
    # 所以不能写 NOT repo:self，改为查完在结果里滤掉自身。用 -f 让 gh 正确编码空格。
    q = f"topic:{topic}"
    if lang:
        q += f" language:{lang}"
    res = gh_json(["api", "-X", "GET", "search/repositories",
                   "-f", f"q={q}", "-f", "sort=stars", "-f", "per_page=9"])
    for it in ((res or {}).get("items") or []):
        if it.get("full_name") == full_name:  # 滤掉自身
            continue
        out["competitor_candidates"].append({
            "full_name": it.get("full_name"), "stars": it.get("stargazers_count"),
            "description": it.get("description"), "language": it.get("language"),
        })
        if len(out["competitor_candidates"]) >= 8:
            break
    return out


def collect_issues(full_name: str) -> dict:
    res = gh_json([
        "api",
        f"repos/{full_name}/issues?sort=comments&direction=desc&state=all&per_page=15",
    ])
    top = []
    for it in (res or []):
        if not isinstance(it, dict) or "pull_request" in it:  # 滤掉 PR
            continue
        top.append({
            "number": it.get("number"), "title": it.get("title"),
            "comments": it.get("comments"), "state": it.get("state"),
            "labels": [l.get("name") for l in (it.get("labels") or []) if isinstance(l, dict)],
            "url": it.get("html_url"),
        })
        if len(top) >= 10:
            break
    return {"top": top}


# ---- 1.9 README 媒体提取 + URL 验证 ----

def _read_readme(repo: str) -> tuple[str | None, str]:
    for name in ("README.md", "readme.md", "Readme.md", "README", "README.rst", "docs/README.md"):
        path = os.path.join(repo, name)
        if os.path.isfile(path):
            try:
                with open(path, encoding="utf-8", errors="ignore") as f:
                    return name, "".join(f.readlines()[:500])
            except Exception as e:  # noqa: BLE001
                warn(f"读取 {name} 失败: {e}")
    return None, ""


def _is_badge(url: str) -> bool:
    low = url.lower()
    return any(k in low for k in _BADGE_KEYWORDS)


def _to_raw_url(url: str, owner: str, repo: str, branch: str) -> tuple[str, str | None]:
    """返回 (绝对URL, raw_path)。raw_path 仅当指向本仓库 raw 文件时非空，用于校验。"""
    if url.startswith(("http://", "https://")):
        m = re.match(r"https?://github\.com/([^/]+)/([^/]+)/(?:blob|raw)/([^/]+)/(.+)", url)
        if m:
            o, r, br, path = m.groups()
            return f"https://raw.githubusercontent.com/{o}/{r}/{br}/{path}", path
        m2 = re.match(r"https?://raw\.githubusercontent\.com/[^/]+/[^/]+/[^/]+/(.+)", url)
        if m2:
            return url, m2.group(1)
        return url, None  # 外链，无法用 gh 校验
    path = url.lstrip("./").lstrip("/")
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}", path


def _guess_media_type(alt: str, url: str, idx: int) -> str:
    s = (alt + " " + url).lower()
    if any(k in s for k in ("youtube", "youtu.be", "vimeo", "bilibili", ".mp4", "<video", "<source")):
        return "video"
    if "architecture" in s or "diagram" in s or "arch " in s:
        return "architecture"
    if url.lower().endswith(".gif") or "demo" in s:
        return "demo"
    if "screenshot" in s or "screen" in s or "preview" in s or "example" in s:
        return "screenshot"
    if idx == 0 or "hero" in s or "banner" in s:
        return "hero"
    return "screenshot"


def _validate_raw_path(owner: str, repo: str, path: str, tree: dict) -> bool:
    """先直接验证 contents API；失败再用全库 tree 按 basename 兜底。"""
    size = run(["gh", "api", f"/repos/{owner}/{repo}/contents/{path}", "--jq", ".size"], timeout=30)
    if size.strip().isdigit():
        return True
    # basename 兜底：tree 是 {basename: realpath}
    base = path.rsplit("/", 1)[-1]
    return base in tree


def collect_media(repo: str, owner: str, repo_name: str, branch: str) -> dict:
    readme_path, text = _read_readme(repo)
    out = {"readme_path": readme_path, "candidates": [], "total_found": 0, "excluded_count": 0}
    if not text:
        out["note"] = "未找到 README"
        return out

    found: list[tuple[str, str]] = []  # (alt, url)
    for m in re.finditer(r"!\[([^\]]*)\]\(([^)\s]+)", text):  # markdown 图片
        found.append((m.group(1), m.group(2)))
    for m in re.finditer(r"<img\b([^>]*)>", text, re.I):  # html img
        attrs = m.group(1)
        src = re.search(r'src=["\']([^"\']+)["\']', attrs, re.I)
        alt = re.search(r'alt=["\']([^"\']*)["\']', attrs, re.I)
        if src:
            found.append((alt.group(1) if alt else "", src.group(1)))
    for m in re.finditer(r'<source\b[^>]*src=["\']([^"\']+)["\']', text, re.I):  # html video
        found.append(("video", m.group(1)))
    for m in re.finditer(r'https?://(?:www\.)?(?:youtube\.com/watch\?[^\s)]+|youtu\.be/[^\s)]+|vimeo\.com/\d+|bilibili\.com/[^\s)]+)', text):
        found.append(("video", m.group(0)))

    out["total_found"] = len(found)
    # 去重 + 去 badge
    seen = set()
    filtered: list[tuple[str, str]] = []
    for alt, url in found:
        if url in seen:
            continue
        seen.add(url)
        if _is_badge(url):
            out["excluded_count"] += 1
            continue
        filtered.append((alt, url))

    # 需要兜底校验时只取一次全库 tree
    tree: dict[str, str] = {}
    need_tree = any(
        not u.startswith(("http://", "https://")) or "github" in u.lower() for _, u in filtered
    )
    if need_tree and filtered:
        tdata = gh_json(["api", f"/repos/{owner}/{repo_name}/git/trees/{branch}?recursive=1"], timeout=60)
        for node in ((tdata or {}).get("tree") or []):
            p = node.get("path", "")
            if p:
                tree[p.rsplit("/", 1)[-1]] = p

    for idx, (alt, url) in enumerate(filtered[:12]):
        abs_url, raw_path = _to_raw_url(url, owner, repo_name, branch)
        is_video = _guess_media_type(alt, url, idx) == "video"
        if raw_path and not is_video:
            verified = _validate_raw_path(owner, repo_name, raw_path, tree)
            # basename 兜底命中时，用真实路径修正 URL
            if not verified:
                pass
            elif raw_path.rsplit("/", 1)[-1] in tree and tree[raw_path.rsplit("/", 1)[-1]] != raw_path:
                real = tree[raw_path.rsplit("/", 1)[-1]]
                size = run(["gh", "api", f"/repos/{owner}/{repo_name}/contents/{raw_path}", "--jq", ".size"], timeout=20)
                if not size.strip().isdigit():
                    abs_url = f"https://raw.githubusercontent.com/{owner}/{repo_name}/{branch}/{real}"
        else:
            verified = None  # 外链/视频，gh 无法校验，交给下游
        out["candidates"].append({
            "alt": alt, "url": abs_url, "type_guess": _guess_media_type(alt, url, idx),
            "source": "readme", "verified": verified, "raw_path": raw_path,
        })
    return out


def _parse_iso_z(s: str | None) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def collect_network(full_name: str, repo: str) -> dict | None:
    if not shutil.which("gh"):
        warn("gh 未安装，跳过 Phase 1 网络采集")
        return None
    owner, _, repo_name = full_name.partition("/")
    basics = collect_repo_basics(full_name)
    if not basics:
        warn("gh repo view 失败，network 块置空（可能无网络/无认证/仓库不可见）")
        return None
    branch = basics.get("default_branch") or "main"
    return {
        "repo_basics": basics,
        "author": collect_author(owner, repo_name, full_name),
        "community": collect_community(full_name, basics.get("stars")),
        "ecosystem": collect_ecosystem(full_name, basics),
        "issues": collect_issues(full_name),
        "media": collect_media(repo, owner, repo_name, branch),
    }


def infer_full_name(repo: str, override: str | None) -> str | None:
    if override:
        return override.strip()
    url = git(repo, "config", "--get", "remote.origin.url").strip()
    m = re.search(r"[:/]([^/]+/[^/]+?)(?:\.git)?$", url)
    return m.group(1) if m else None


def main() -> int:
    ap = argparse.ArgumentParser(description="repo-miner Phase 2 确定性数据采集")
    ap.add_argument("local_path", help="已 clone 的本地仓库路径")
    ap.add_argument("--full-name", help="owner/repo，缺省从 git remote 推断")
    ap.add_argument("--out", help="JSON 落地路径，缺省 tmp/repo-facts-<repo>.json")
    ap.add_argument("--no-network", action="store_true",
                    help="只采离线指标（git/tokei），跳过 Phase 1 的 gh 联网采集")
    args = ap.parse_args()

    repo = os.path.abspath(args.local_path)
    if not os.path.isdir(os.path.join(repo, ".git")):
        print(f"ERR: {repo} 不是 git 仓库（缺 .git）", file=sys.stderr)
        return 2

    full_name = infer_full_name(repo, args.full_name)
    repo_short = (full_name.split("/")[-1] if full_name else os.path.basename(repo))

    facts = {
        "schema_version": 2,
        "full_name": full_name,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        # Phase 2（离线：git / tokei）
        "code_scale": collect_code_scale(repo),
        "dev_rhythm": collect_dev_rhythm(repo),
        "evolution": collect_evolution(repo, full_name if not args.no_network else None),
        "contributors": collect_contributors(repo),
        # Phase 1（联网：gh api）—— 无 gh/无网络/无 full_name 时为 null
        "network": None,
        "_warnings": WARNINGS,
    }
    if not args.no_network and full_name:
        facts["network"] = collect_network(full_name, repo)
    elif not full_name:
        warn("无法确定 full_name（owner/repo），跳过 Phase 1 网络采集")

    out_path = args.out or os.path.join("tmp", f"repo-facts-{repo_short}.json")
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(facts, f, ensure_ascii=False, indent=2)

    # stdout 只打印路径，供 prompt 捕获
    print(out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())

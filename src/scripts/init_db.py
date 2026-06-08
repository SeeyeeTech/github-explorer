#!/usr/bin/env python3
"""SQLite 数据库初始化、schema 迁移与 JSON 兼容产物 dump 工具。

设计要点（详见 .claude/plans/splendid-swinging-meteor.md）：
- DB 是 SoR，通过 schema 约束（外键/CHECK/UNIQUE/NOT NULL）从源头保证数据规整
- DB 文件不入 Git（src/data/db.sqlite，加 .gitignore），CI 期由本脚本与各 ETL 脚本重建
- reports.json / tags.yaml / starred.json 是 DB dump 出的兼容产物，仍入 Git 供 site/ 读取
- 脚本以「子命令 + 可被 import 的工具集」两种身份共存

子命令：
  init          建库 + 应用 schema migration（idempotent）
  export-json   从 DB dump → reports.json / tags.yaml.entries / starred.json
  verify        dump 到内存后与 git 工作区现有文件做字典级比对
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "src" / "data"
DB_PATH = DATA_DIR / "db.sqlite"
REPORTS_JSON = DATA_DIR / "reports.json"
TAGS_YAML = DATA_DIR / "tags.yaml"
STARRED_JSON = DATA_DIR / "starred.json"
TRENDING_DEDUP_JSON = ROOT / "src" / "trending_repo" / "all_repos_deduped.json"
PUBLISH_JSONL = DATA_DIR / "publish_history.jsonl"


# ---------------------------------------------------------------- schema migrations

MIGRATIONS: dict[int, str] = {
    1: """
        -- 阶段 1：reports + tags
        CREATE TABLE reports (
          slug              TEXT    PRIMARY KEY,
          title             TEXT    NOT NULL,
          original_url      TEXT    UNIQUE,
          summary           TEXT,
          stars             INTEGER CHECK (stars IS NULL OR stars >= 0),
          forks             INTEGER CHECK (forks IS NULL OR forks >= 0),
          language          TEXT,
          loc_raw           TEXT,
          age_months        REAL    CHECK (age_months IS NULL OR age_months >= 0),
          age_raw           TEXT,
          stage             TEXT,
          contribution      TEXT,
          heat              TEXT,
          heat_raw          TEXT,
          quality           TEXT,
          license           TEXT,
          cover             TEXT,
          mtime             TEXT    NOT NULL,
          published_state   TEXT    CHECK (published_state IN ('pending','draft','excluded','published') OR published_state IS NULL),
          published_at      TEXT,
          published_title   TEXT,
          created_at        TEXT    DEFAULT (datetime('now')),
          updated_at        TEXT    DEFAULT (datetime('now'))
        );
        CREATE INDEX idx_reports_mtime ON reports(mtime DESC);
        CREATE INDEX idx_reports_stars ON reports(stars DESC) WHERE stars IS NOT NULL;
        CREATE INDEX idx_reports_lang  ON reports(language)   WHERE language IS NOT NULL;

        CREATE TABLE report_highlights (
          slug      TEXT    NOT NULL,
          position  INTEGER NOT NULL CHECK (position >= 0),
          text      TEXT    NOT NULL,
          PRIMARY KEY (slug, position),
          FOREIGN KEY (slug) REFERENCES reports(slug) ON DELETE CASCADE
        );

        CREATE TABLE tags (
          tag         TEXT    PRIMARY KEY,
          label       TEXT    NOT NULL,
          sort_order  INTEGER NOT NULL DEFAULT 1000
        );

        CREATE TABLE tag_rules (
          tag      TEXT NOT NULL,
          keyword  TEXT NOT NULL,
          PRIMARY KEY (tag, keyword),
          FOREIGN KEY (tag) REFERENCES tags(tag) ON DELETE CASCADE
        );

        CREATE TABLE report_tags (
          slug  TEXT NOT NULL,
          tag   TEXT NOT NULL,
          PRIMARY KEY (slug, tag),
          FOREIGN KEY (slug) REFERENCES reports(slug) ON DELETE CASCADE,
          FOREIGN KEY (tag)  REFERENCES tags(tag)    ON DELETE CASCADE
        );
        CREATE INDEX idx_report_tags_tag ON report_tags(tag);

        CREATE TABLE report_tag_locks (
          slug TEXT PRIMARY KEY,
          FOREIGN KEY (slug) REFERENCES reports(slug) ON DELETE CASCADE
        );
    """,
    2: """
        -- 阶段 2：大牛 + Star
        CREATE TABLE users (
          login       TEXT    PRIMARY KEY,
          name        TEXT    NOT NULL,
          bio         TEXT,
          sort_order  INTEGER NOT NULL DEFAULT 1000
        );

        -- user_tags.tag 是弱引用（users.yaml 里写的 tag 不一定在 tag-rules.yaml），
        -- 因此不加外键约束到 tags 表。position 维持 YAML 字面顺序便于 dump 时还原。
        CREATE TABLE user_tags (
          login    TEXT NOT NULL,
          tag      TEXT NOT NULL,
          position INTEGER NOT NULL DEFAULT 0,
          PRIMARY KEY (login, tag),
          FOREIGN KEY (login) REFERENCES users(login) ON DELETE CASCADE
        );

        CREATE TABLE user_starred_snapshot (
          login        TEXT    PRIMARY KEY,
          fetched_at   TEXT,
          range_start  TEXT,
          FOREIGN KEY (login) REFERENCES users(login) ON DELETE CASCADE
        );

        CREATE TABLE user_starred (
          login        TEXT    NOT NULL,
          url          TEXT    NOT NULL,  -- 入库前 rstrip('/').lower() 规范化
          name         TEXT    NOT NULL,
          stars        INTEGER NOT NULL CHECK (stars >= 0),
          description  TEXT    NOT NULL DEFAULT '',
          starred_at   TEXT    NOT NULL,
          position     INTEGER NOT NULL DEFAULT 0,  -- .md 中原始顺序，dump 时维持文件顺序减少 diff
          PRIMARY KEY (login, url),
          FOREIGN KEY (login) REFERENCES users(login) ON DELETE CASCADE
        );
        CREATE INDEX idx_user_starred_url ON user_starred(url);
        CREATE INDEX idx_user_starred_pos ON user_starred(login, position);

        -- reportSlug 派生视图：URL 已规范化，直接 = 即可
        CREATE VIEW v_user_starred AS
        SELECT us.*, r.slug AS report_slug
        FROM user_starred us
        LEFT JOIN reports r ON r.original_url = us.url;
    """,
    3: """
        -- 阶段 3：Trending 时间序列
        CREATE TABLE trending_repos (
          url         TEXT    PRIMARY KEY,  -- 入库前 rstrip('/').lower() 规范化
          name        TEXT    NOT NULL,     -- 'owner/repo' 原始大小写
          language    TEXT,
          description TEXT    NOT NULL DEFAULT ''
        );

        CREATE TABLE trending_snapshots (
          period_type  TEXT    NOT NULL CHECK (period_type IN ('daily','weekly','monthly')),
          period_key   TEXT    NOT NULL,    -- daily=YYYY-MM-DD / weekly=YYYY-Www / monthly=YYYY-MM
          url          TEXT    NOT NULL,
          stars        INTEGER NOT NULL CHECK (stars >= 0),
          forks        INTEGER NOT NULL DEFAULT 0 CHECK (forks >= 0),
          rank         INTEGER,             -- 当时榜单位置（由 parse_trending enumerate(start=1) 推导填充，已全量有值）
          PRIMARY KEY (period_type, period_key, url),
          FOREIGN KEY (url) REFERENCES trending_repos(url) ON DELETE CASCADE
        );
        CREATE INDEX idx_trending_snap_url ON trending_snapshots(url, period_type, period_key);
        CREATE INDEX idx_trending_snap_pk  ON trending_snapshots(period_type, period_key);

        -- 上榜窗口（首次/最后出现日期）
        CREATE VIEW v_trending_repo_window AS
        SELECT
          url,
          MIN(period_key) FILTER (WHERE period_type='daily')  AS first_daily,
          MAX(period_key) FILTER (WHERE period_type='daily')  AS last_daily,
          MIN(period_key) AS first_seen,
          MAX(period_key) AS last_seen
        FROM trending_snapshots GROUP BY url;

        -- 上榜次数轨迹（按 period_type 分桶）
        CREATE VIEW v_trending_days AS
        SELECT
          url,
          SUM(CASE WHEN period_type='daily'   THEN 1 ELSE 0 END) AS daily_count,
          SUM(CASE WHEN period_type='weekly'  THEN 1 ELSE 0 END) AS weekly_count,
          SUM(CASE WHEN period_type='monthly' THEN 1 ELSE 0 END) AS monthly_count
        FROM trending_snapshots GROUP BY url;
    """,
    4: """
        -- 阶段 4：发布历史（替代 publish.md 手工表格）
        -- SoR 是 src/data/publish_history.jsonl（append-only，入 Git）
        -- 本表是该 jsonl 的查询索引，由 init_db.py seed-publish 重建
        CREATE TABLE publish_history (
          id            INTEGER PRIMARY KEY AUTOINCREMENT,
          recorded_at   TEXT    NOT NULL,        -- ISO 8601
          slug          TEXT    NOT NULL,        -- 报告 slug（弱引用，允许指向已删除的报告）
          title         TEXT,                    -- 公众号标题（可能与 reports.title 不同）
          state         TEXT    NOT NULL CHECK (state IN ('pending','draft','excluded','published')),
          published_at  TEXT,                    -- 'YYYY-MM-DD' 或 NULL
          reason        TEXT,
          ci_run_id     TEXT
        );
        CREATE INDEX idx_publish_slug  ON publish_history(slug);
        CREATE INDEX idx_publish_state ON publish_history(state, published_at DESC);

        -- 每个 slug 的最新状态（被 reports.published_* 字段反查）
        -- 当同一 slug 多次记录时，recorded_at 最大的胜出
        CREATE VIEW v_publish_latest AS
        SELECT slug, state, published_at, title, reason, recorded_at
        FROM (
          SELECT *, ROW_NUMBER() OVER (PARTITION BY slug ORDER BY recorded_at DESC, id DESC) AS rn
          FROM publish_history
        )
        WHERE rn = 1;
    """,
    5: """
        -- 阶段 5：跨用户 Star 频次（替代 starred_repo/repo-frequency.md 的"多人 Star"选题信号）
        -- 按 user_count DESC 查询即为原 repo-frequency.md 的"被多人 Star 的仓库"表
        CREATE VIEW v_starred_frequency AS
        SELECT
          us.url,
          COUNT(DISTINCT us.login) AS user_count,
          MAX(us.name)             AS name,
          (SELECT r.slug FROM reports r WHERE r.original_url = us.url LIMIT 1) AS report_slug
        FROM user_starred us
        GROUP BY us.url;
    """,
    6: """
        -- 阶段 6：多渠道发布（一文多发）。给 publish_history 增加 channel 维度，
        -- 让公众号之外的渠道（博客园等）也能记录发布历史，而不污染
        -- reports.published_*（后者语义保持 = 公众号发布状态）。
        ALTER TABLE publish_history ADD COLUMN channel TEXT NOT NULL DEFAULT 'wechat';
        ALTER TABLE publish_history ADD COLUMN post_id TEXT;   -- 远端文章 id（幂等更新用）
        ALTER TABLE publish_history ADD COLUMN url     TEXT;   -- 远端文章 URL
        CREATE INDEX idx_publish_channel ON publish_history(slug, channel);

        -- v_publish_latest 收窄为「仅公众号」，保持 reports.published_* 原语义不变
        -- （历史记录无 channel 字段 → 入库时 DEFAULT 'wechat'，集合与改动前一致）
        DROP VIEW IF EXISTS v_publish_latest;
        CREATE VIEW v_publish_latest AS
        SELECT slug, state, published_at, title, reason, recorded_at
        FROM (
          SELECT *, ROW_NUMBER() OVER (PARTITION BY slug ORDER BY recorded_at DESC, id DESC) AS rn
          FROM publish_history
          WHERE channel = 'wechat'
        )
        WHERE rn = 1;

        -- 每个 (slug, channel) 的最新状态，供多渠道发布查询 / 幂等校验
        CREATE VIEW v_publish_channel_latest AS
        SELECT slug, channel, state, published_at, title, post_id, url, recorded_at
        FROM (
          SELECT *, ROW_NUMBER() OVER (PARTITION BY slug, channel ORDER BY recorded_at DESC, id DESC) AS rn
          FROM publish_history
        )
        WHERE rn = 1;
    """,
}


# ---------------------------------------------------------------- core helpers

def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    # 不用 = DB_PATH 作默认值（闭包在函数定义时绑定，无法被测试 monkey-patch）。
    target = db_path if db_path is not None else DB_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(target)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def ensure_schema(conn: sqlite3.Connection) -> int:
    """Apply pending migrations. Returns the new schema version."""
    conn.executescript(
        "CREATE TABLE IF NOT EXISTS schema_version ("
        "  version INTEGER PRIMARY KEY,"
        "  applied_at TEXT DEFAULT (datetime('now')),"
        "  note TEXT"
        ")"
    )
    current = conn.execute("SELECT COALESCE(MAX(version), 0) FROM schema_version").fetchone()[0]
    for v in sorted(MIGRATIONS):
        if v > current:
            conn.executescript(MIGRATIONS[v])
            conn.execute("INSERT INTO schema_version(version) VALUES (?)", (v,))
            conn.commit()
            current = v
    return current


def normalize_url(url: str | None) -> str | None:
    """全局 URL 规范化：rstrip('/') + lower。
    在 schema 之外用 Python 端统一处理，避免 SQLite TRIM(url, '/') 误剥 '//' 字符。"""
    if url is None:
        return None
    return url.rstrip("/").lower()


def compose_published(state: str | None, at: str | None) -> str | None:
    """把 DB 拆分后的 (state, at) 拼回 site/ 期望的字符串字段。"""
    if state is None:
        return None
    if state == "published" and at:
        return f"published:{at}"
    # pending / draft / excluded / published-without-at 都直接输出 state 名
    return state


# ---------------------------------------------------------------- export-json

def dump_reports() -> list[dict[str, Any]]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT slug, title, original_url, summary, stars, forks, language, loc_raw, "
        "age_months, age_raw, stage, contribution, heat, heat_raw, quality, license, "
        "cover, mtime, published_state, published_at, published_title "
        "FROM reports ORDER BY slug"
    ).fetchall()
    out: list[dict[str, Any]] = []
    for r in rows:
        slug = r[0]
        hl_rows = conn.execute(
            "SELECT text FROM report_highlights WHERE slug=? ORDER BY position", (slug,)
        ).fetchall()
        out.append({
            "slug": slug,
            "title": r[1],
            "originalUrl": r[2],
            "summary": r[3],
            "highlights": [h[0] for h in hl_rows],
            "stars": r[4],
            "forks": r[5],
            "language": r[6],
            "locRaw": r[7],
            "ageMonths": r[8],
            "ageRaw": r[9],
            "stage": r[10],
            "contribution": r[11],
            "heat": r[12],
            "heatRaw": r[13],
            "quality": r[14],
            "license": r[15],
            "cover": r[16],
            "mtime": r[17],
            "published": compose_published(r[18], r[19]),
            "publishedTitle": r[20],
        })
    conn.close()
    return out


def dump_tags_entries() -> dict[str, list[str]]:
    """{slug: [tag, ...]}。tag 按 sort_order 后字母排序；空标签集 fallback 为 ['uncategorized']。"""
    conn = get_connection()
    slugs = [r[0] for r in conn.execute("SELECT slug FROM reports ORDER BY slug").fetchall()]
    tag_rows = conn.execute(
        "SELECT rt.slug, rt.tag FROM report_tags rt "
        "JOIN tags t ON t.tag = rt.tag "
        "ORDER BY rt.slug, t.sort_order, rt.tag"
    ).fetchall()
    grouped: dict[str, list[str]] = {}
    for slug, tag in tag_rows:
        grouped.setdefault(slug, []).append(tag)
    conn.close()
    out: dict[str, list[str]] = {}
    for slug in slugs:
        out[slug] = grouped.get(slug) or ["uncategorized"]
    return out


def dump_tags_manual() -> list[str]:
    conn = get_connection()
    rows = conn.execute("SELECT slug FROM report_tag_locks ORDER BY slug").fetchall()
    conn.close()
    return [r[0] for r in rows]


def write_reports_json(path: Path = REPORTS_JSON) -> int:
    data = dump_reports()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(data)


def dump_starred() -> dict[str, Any]:
    """从 DB dump 成 starred.json 结构（users[].items[]，含 v_user_starred 派生的 reportSlug）。

    users 按 sort_order 排；items 按 starred_at DESC（与原 .md 列表顺序对齐）。"""
    conn = get_connection()
    user_rows = conn.execute(
        "SELECT login, name, bio FROM users ORDER BY sort_order"
    ).fetchall()
    out_users: list[dict[str, Any]] = []
    for login, name, bio in user_rows:
        tags = [r[0] for r in conn.execute(
            "SELECT tag FROM user_tags WHERE login=? ORDER BY position", (login,)
        ).fetchall()]
        snap = conn.execute(
            "SELECT fetched_at, range_start FROM user_starred_snapshot WHERE login=?",
            (login,),
        ).fetchone()
        fetched_at = snap[0] if snap else None
        range_start = snap[1] if snap else None
        items_rows = conn.execute(
            "SELECT url, name, stars, description, starred_at, report_slug "
            "FROM v_user_starred WHERE login=? ORDER BY position",
            (login,),
        ).fetchall()
        items: list[dict[str, Any]] = []
        for url, iname, stars, desc, starred_at, report_slug in items_rows:
            it: dict[str, Any] = {
                "name": iname,
                "url": url,
                "stars": stars,
                "description": desc,
                "starredAt": starred_at,
            }
            if report_slug is not None:
                it["reportSlug"] = report_slug
            items.append(it)
        user_entry: dict[str, Any] = {
            "login": login,
            "name": name,
        }
        if bio is not None:
            user_entry["bio"] = bio
        if tags:
            user_entry["tags"] = tags
        user_entry["fetchedAt"] = fetched_at
        user_entry["rangeStart"] = range_start
        user_entry["items"] = items
        out_users.append(user_entry)
    conn.close()
    return {"users": out_users}


def write_starred_json(path: Path = STARRED_JSON) -> int:
    data = dump_starred()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return sum(len(u["items"]) for u in data["users"])


def dump_trending_deduped() -> list[dict[str, Any]]:
    """从 DB 派生 all_repos_deduped.json：
        - trending_days = daily 上榜天数（与 parse_trending.py 原语义一致）
        - last_seen = 最后一次在 daily 出现的日期
        - stars/forks = 历次快照中最高 stars 那次的值（与 parse_trending.py 原语义一致）
        - 排序：trending_days DESC（与现状一致）
    """
    conn = get_connection()
    rows = conn.execute(
        """
        SELECT
          tr.url, tr.name, tr.language, tr.description,
          td.daily_count AS trending_days,
          w.last_daily AS last_seen,
          (SELECT stars FROM trending_snapshots ts
             WHERE ts.url = tr.url ORDER BY ts.stars DESC LIMIT 1) AS stars,
          (SELECT forks FROM trending_snapshots ts
             WHERE ts.url = tr.url ORDER BY ts.stars DESC LIMIT 1) AS forks
        FROM trending_repos tr
        JOIN v_trending_days td        USING(url)
        JOIN v_trending_repo_window w  USING(url)
        ORDER BY trending_days DESC, tr.url
        """
    ).fetchall()
    conn.close()
    out: list[dict[str, Any]] = []
    for url, name, language, desc, td, last_seen, stars, forks in rows:
        out.append({
            "name": name,
            "url": url,
            "language": language,
            "stars": stars,
            "forks": forks,
            "description": desc,
            "last_seen": last_seen,
            "trending_days": td,
        })
    return out


def write_trending_deduped(path: Path = TRENDING_DEDUP_JSON) -> int:
    data = dump_trending_deduped()
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(data)


def write_tags_yaml(path: Path = TAGS_YAML) -> int:
    import yaml
    entries = dump_tags_entries()
    manual = dump_tags_manual()
    doc = {"manual": manual, "entries": entries}
    body = yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, default_flow_style=False)
    header = "# 自动生成 + 人工保护混合维护。要保护某条手工标注，把 slug 加入 manual 列表。\n"
    path.write_text(header + body, encoding="utf-8")
    return len(entries)


def cmd_export_json(args: argparse.Namespace) -> int:
    n_reports = write_reports_json()
    n_tags = write_tags_yaml()
    n_starred = write_starred_json()
    print(f"✅ 导出 reports.json  ({n_reports} 篇)")
    print(f"✅ 导出 tags.yaml     ({n_tags} 篇)")
    print(f"✅ 导出 starred.json  ({n_starred} 条 starred items)")
    # trending dedup 只在 trending_repos 有数据时 dump（避免阶段 3 未应用时清空文件）
    conn = get_connection()
    has_trending = conn.execute("SELECT COUNT(*) FROM trending_repos").fetchone()[0]
    conn.close()
    if has_trending:
        n_trending = write_trending_deduped()
        print(f"✅ 导出 all_repos_deduped.json ({n_trending} 个仓库)")
    return 0


# ---------------------------------------------------------------- verify

def _normalize_for_compare(v: Any) -> Any:
    """归一化：None ↔ 缺失键、[] ↔ None、int ↔ float 视为等价。"""
    if v is None:
        return None
    if isinstance(v, list) and len(v) == 0:
        return None
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return v


def _diff_records(
    expected: dict[str, Any],
    actual: dict[str, Any],
    pk: str,
    skip_fields: set[str] | None = None,
) -> list[str]:
    """返回 ['slug=X.field=Y: expected=... actual=...', ...]"""
    skip_fields = skip_fields or set()
    diffs: list[str] = []
    keys = set(expected.keys()) | set(actual.keys())
    pk_val = expected.get(pk) or actual.get(pk)
    for k in sorted(keys):
        if k in skip_fields:
            continue
        ev = _normalize_for_compare(expected.get(k))
        av = _normalize_for_compare(actual.get(k))
        if ev != av:
            diffs.append(f"{pk}={pk_val}.{k}: expected={ev!r} actual={av!r}")
    return diffs


def verify_reports(*, allow_url_case_diff: bool = True) -> list[str]:
    if not REPORTS_JSON.exists():
        return [f"现有 {REPORTS_JSON.name} 不存在，无法 verify"]
    existing = json.loads(REPORTS_JSON.read_text(encoding="utf-8"))
    actual = dump_reports()
    diffs: list[str] = []
    by_slug_exp = {r["slug"]: r for r in existing}
    by_slug_act = {r["slug"]: r for r in actual}
    only_exp = set(by_slug_exp) - set(by_slug_act)
    only_act = set(by_slug_act) - set(by_slug_exp)
    for s in sorted(only_exp):
        diffs.append(f"reports.slug={s}: 仅 expected 存在")
    for s in sorted(only_act):
        diffs.append(f"reports.slug={s}: 仅 actual 存在")
    for slug in sorted(set(by_slug_exp) & set(by_slug_act)):
        exp = by_slug_exp[slug]
        act = by_slug_act[slug]
        if allow_url_case_diff and exp.get("originalUrl") and act.get("originalUrl"):
            # URL 规范化产生的大小写差异允许通过；其他字段照常比对
            if exp["originalUrl"].rstrip("/").lower() == act["originalUrl"]:
                exp = {**exp, "originalUrl": act["originalUrl"]}
        # 「已入草稿」slug 在修复隐 bug 后 published 从 null → 'pending'，是预期的行为修复
        if exp.get("published") is None and act.get("published") == "pending":
            exp = {**exp, "published": "pending"}
        diffs.extend(_diff_records(exp, act, pk="slug"))
    return diffs


def verify_tags() -> list[str]:
    if not TAGS_YAML.exists():
        return [f"现有 {TAGS_YAML.name} 不存在，无法 verify"]
    import yaml
    existing = yaml.safe_load(TAGS_YAML.read_text(encoding="utf-8")) or {}
    existing_entries = existing.get("entries") or {}
    actual_entries = dump_tags_entries()
    diffs: list[str] = []
    only_exp = set(existing_entries) - set(actual_entries)
    only_act = set(actual_entries) - set(existing_entries)
    for s in sorted(only_exp):
        diffs.append(f"tags.entries.{s}: 仅 expected 存在")
    for s in sorted(only_act):
        diffs.append(f"tags.entries.{s}: 仅 actual 存在")
    for slug in sorted(set(existing_entries) & set(actual_entries)):
        e = sorted(existing_entries[slug] or [])
        a = sorted(actual_entries[slug] or [])
        if e != a:
            diffs.append(f"tags.entries.{slug}: expected={e} actual={a}")
    return diffs


def verify_starred(*, allow_url_case_diff: bool = True) -> list[str]:
    if not STARRED_JSON.exists():
        return [f"现有 {STARRED_JSON.name} 不存在，无法 verify"]
    existing = json.loads(STARRED_JSON.read_text(encoding="utf-8"))
    actual = dump_starred()
    diffs: list[str] = []
    exp_users = {u["login"]: u for u in existing.get("users", [])}
    act_users = {u["login"]: u for u in actual["users"]}
    only_exp = set(exp_users) - set(act_users)
    only_act = set(act_users) - set(exp_users)
    for s in sorted(only_exp):
        diffs.append(f"starred.users.{s}: 仅 expected 存在")
    for s in sorted(only_act):
        diffs.append(f"starred.users.{s}: 仅 actual 存在")
    for login in sorted(set(exp_users) & set(act_users)):
        eu = exp_users[login]
        au = act_users[login]
        # user 级字段
        for k in ("name", "bio", "tags", "fetchedAt", "rangeStart"):
            ev = _normalize_for_compare(eu.get(k))
            av = _normalize_for_compare(au.get(k))
            if ev != av:
                diffs.append(f"starred.users.{login}.{k}: expected={ev!r} actual={av!r}")
        # items 级：按 url 索引
        e_items = {i["url"].rstrip("/").lower() if allow_url_case_diff else i["url"]: i
                   for i in eu.get("items", [])}
        a_items = {i["url"]: i for i in au.get("items", [])}
        only_e = set(e_items) - set(a_items)
        only_a = set(a_items) - set(e_items)
        for u in sorted(only_e):
            diffs.append(f"starred.users.{login}.items[url={u}]: 仅 expected 存在")
        for u in sorted(only_a):
            diffs.append(f"starred.users.{login}.items[url={u}]: 仅 actual 存在")
        for url in sorted(set(e_items) & set(a_items)):
            ei = e_items[url]
            ai = a_items[url]
            for k in ("name", "stars", "description", "starredAt", "reportSlug"):
                ev = _normalize_for_compare(ei.get(k))
                av = _normalize_for_compare(ai.get(k))
                if k == "reportSlug" and ev is None and av is not None:
                    # 新分析的报告反查命中（DB 是最新），expected 滞后 → 跳过
                    continue
                if ev != av:
                    diffs.append(f"starred.users.{login}.items[{url}].{k}: expected={ev!r} actual={av!r}")
    return diffs


def verify_trending(*, allow_url_case_diff: bool = True) -> list[str]:
    if not TRENDING_DEDUP_JSON.exists():
        return []  # 文件不存在表示阶段 3 未跑过，不阻塞
    existing = json.loads(TRENDING_DEDUP_JSON.read_text(encoding="utf-8"))
    actual = dump_trending_deduped()
    if not actual:
        return []  # DB 内无数据，跳过
    diffs: list[str] = []
    # 用 normalized url 作为索引（原 JSON 可能有大小写）
    def _norm(u: str | None) -> str | None:
        if u is None:
            return None
        return u.rstrip("/").lower() if allow_url_case_diff else u
    exp = {_norm(r.get("url")): r for r in existing if r.get("url")}
    act = {r["url"]: r for r in actual}
    only_e = set(exp) - set(act)
    only_a = set(act) - set(exp)
    for u in sorted(only_e):
        diffs.append(f"trending.url={u}: 仅 expected 存在")
    for u in sorted(only_a):
        diffs.append(f"trending.url={u}: 仅 actual 存在")
    for url in sorted(set(exp) & set(act)):
        e = exp[url]
        a = act[url]
        for k in ("trending_days", "stars", "forks", "language", "last_seen", "name"):
            ev = _normalize_for_compare(e.get(k))
            av = _normalize_for_compare(a.get(k))
            if ev != av:
                diffs.append(f"trending[{url}].{k}: expected={ev!r} actual={av!r}")
    return diffs


def cmd_verify(args: argparse.Namespace) -> int:
    all_diffs: list[str] = []
    all_diffs += verify_reports()
    all_diffs += verify_tags()
    all_diffs += verify_starred()
    all_diffs += verify_trending()
    if not all_diffs:
        print("✅ verify 通过：DB dump 与现有文件字典级一致")
        return 0
    print(f"❌ verify 失败：{len(all_diffs)} 处差异，前 10 个：", file=sys.stderr)
    for d in all_diffs[:10]:
        print(f"   - {d}", file=sys.stderr)
    return 1


# ---------------------------------------------------------------- init

def cmd_init(args: argparse.Namespace) -> int:
    conn = get_connection()
    v = ensure_schema(conn)
    conn.close()
    print(f"✅ Schema ready (version={v}) → {DB_PATH.relative_to(ROOT)}")
    return 0


# ---------------------------------------------------------------- seed-publish

def seed_publish_history(conn: sqlite3.Connection, jsonl_path: Path = PUBLISH_JSONL) -> int:
    """读 publish_history.jsonl → 全量重建 publish_history 表。

    返回写入的行数。jsonl 不存在或为空时不修改表。"""
    if not jsonl_path.exists():
        return 0
    rows: list[tuple] = []
    bad = 0
    for lineno, line in enumerate(jsonl_path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            bad += 1
            continue
        state = obj.get("state")
        if state not in ("pending", "draft", "excluded", "published"):
            bad += 1
            continue
        rows.append((
            obj.get("recorded_at"),
            obj.get("slug"),
            obj.get("title"),
            state,
            obj.get("published_at"),
            obj.get("reason"),
            obj.get("ci_run_id"),
            obj.get("channel") or "wechat",   # 历史记录无 channel → 视为公众号
            obj.get("post_id"),
            obj.get("url"),
        ))
    if bad:
        print(f"⚠️  jsonl 中跳过 {bad} 行（格式不合法或 state 非法）")
    with conn:
        conn.execute("DELETE FROM publish_history")
        conn.executemany(
            "INSERT INTO publish_history "
            "(recorded_at, slug, title, state, published_at, reason, ci_run_id, channel, post_id, url) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            rows,
        )
    return len(rows)


def cmd_seed_publish(args: argparse.Namespace) -> int:
    conn = get_connection()
    ensure_schema(conn)
    n = seed_publish_history(conn)
    conn.close()
    if n == 0:
        print(f"⚠️  {PUBLISH_JSONL.relative_to(ROOT)} 不存在或为空，publish_history 表保持原状")
    else:
        print(f"✅ seed publish_history: {n} 行 ← {PUBLISH_JSONL.relative_to(ROOT)}")
    return 0


# ---------------------------------------------------------------- reconcile reports.published_*

def reconcile_reports_published(conn: sqlite3.Connection) -> int:
    """从 v_publish_latest 反查更新 reports 表的 published_* 字段。

    仅当 publish_history 表非空时执行。返回更新的报告数。"""
    n = conn.execute("SELECT COUNT(*) FROM publish_history").fetchone()[0]
    if n == 0:
        return 0
    with conn:
        # 先清除 reports 中可能由旧 parse_publish_index 残留的 published_* 字段
        conn.execute(
            "UPDATE reports SET published_state=NULL, published_at=NULL, "
            "published_title=NULL"
        )
        # 从 v_publish_latest 反查（slug 只可能在 publish_history 中存在但 reports 中已删除，跳过）
        cur = conn.execute("""
            UPDATE reports
            SET published_state  = (SELECT state FROM v_publish_latest WHERE slug = reports.slug),
                published_at     = (SELECT published_at FROM v_publish_latest WHERE slug = reports.slug),
                published_title  = (SELECT title FROM v_publish_latest WHERE slug = reports.slug)
            WHERE EXISTS (SELECT 1 FROM v_publish_latest WHERE slug = reports.slug)
        """)
        return cur.rowcount


def cmd_reconcile_published(args: argparse.Namespace) -> int:
    conn = get_connection()
    ensure_schema(conn)
    n = reconcile_reports_published(conn)
    conn.close()
    print(f"✅ reconcile reports.published_*: 更新 {n} 篇报告（从 v_publish_latest 反查）")
    return 0


# ---------------------------------------------------------------- CLI

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="建库 + 应用 schema migration")
    sub.add_parser("export-json", help="从 DB dump → reports.json / tags.yaml / starred.json / all_repos_deduped.json")
    sub.add_parser("verify", help="dump 到内存后与现有文件字典级比对")
    sub.add_parser("seed-publish", help="从 publish_history.jsonl 灌入 publish_history 表")
    sub.add_parser("reconcile-published", help="从 v_publish_latest 反查更新 reports.published_*")
    return p


COMMANDS: dict[str, Callable[[argparse.Namespace], int]] = {
    "init": cmd_init,
    "export-json": cmd_export_json,
    "verify": cmd_verify,
    "seed-publish": cmd_seed_publish,
    "reconcile-published": cmd_reconcile_published,
}


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return COMMANDS[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())

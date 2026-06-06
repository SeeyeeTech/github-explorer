#!/usr/bin/env python3
"""阶段 1 数据库迁移的单元测试（stdlib unittest，不引入 pytest）。

运行方式：
    python3 -m unittest tests/test_db.py -v

测试用临时 sqlite 文件，与 src/data/db.sqlite 隔离。
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src" / "scripts"))

import init_db  # noqa: E402


class TempDBTest(unittest.TestCase):
    """共享一个临时 DB 文件，每个测试自动 fresh schema。"""

    def setUp(self) -> None:
        self.tmpfile = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        self.tmpfile.close()
        self.db_path = Path(self.tmpfile.name)
        # 替换全局路径以便 init_db 的辅助函数也指到临时文件
        self._orig_db = init_db.DB_PATH
        init_db.DB_PATH = self.db_path

    def tearDown(self) -> None:
        init_db.DB_PATH = self._orig_db
        try:
            os.unlink(self.db_path)
        except OSError:
            pass

    def conn(self) -> sqlite3.Connection:
        c = init_db.get_connection(self.db_path)
        init_db.ensure_schema(c)
        return c


class TestInitDB(TempDBTest):
    def test_idempotent(self):
        """ensure_schema 两次不重复应用同一 migration。"""
        c = self.conn()
        v1 = init_db.ensure_schema(c)
        v2 = init_db.ensure_schema(c)
        self.assertEqual(v1, v2)
        n = c.execute("SELECT COUNT(*) FROM schema_version").fetchone()[0]
        self.assertEqual(n, len(init_db.MIGRATIONS),
                         "schema_version 应只有 len(MIGRATIONS) 行，每次 migration 仅插入一次")
        c.close()


class TestSchemaConstraints(TempDBTest):
    def test_unique_slug(self):
        """重复 slug 应 raise IntegrityError。"""
        c = self.conn()
        c.execute("INSERT INTO reports (slug, title, mtime) VALUES ('foo', 'F', '2026-01-01')")
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute("INSERT INTO reports (slug, title, mtime) VALUES ('foo', 'F2', '2026-01-02')")
        c.close()

    def test_unique_original_url(self):
        """重复 original_url 应 raise IntegrityError。"""
        c = self.conn()
        c.execute(
            "INSERT INTO reports (slug, title, mtime, original_url) VALUES (?, ?, ?, ?)",
            ("a", "A", "2026-01-01", "https://github.com/x/y"),
        )
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute(
                "INSERT INTO reports (slug, title, mtime, original_url) VALUES (?, ?, ?, ?)",
                ("b", "B", "2026-01-02", "https://github.com/x/y"),
            )
        c.close()

    def test_published_state_check(self):
        """published_state 非枚举值应 fail。"""
        c = self.conn()
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute(
                "INSERT INTO reports (slug, title, mtime, published_state) VALUES (?, ?, ?, ?)",
                ("x", "X", "2026-01-01", "wrong_state"),
            )
        c.close()

    def test_orphan_tag_fkey(self):
        """report_tags 引用不存在的 tag 应 fail。"""
        c = self.conn()
        c.execute("INSERT INTO reports (slug, title, mtime) VALUES ('foo', 'F', '2026-01-01')")
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute("INSERT INTO report_tags (slug, tag) VALUES ('foo', 'nonexistent-tag')")
        c.close()

    def test_negative_stars(self):
        """stars < 0 应 fail。"""
        c = self.conn()
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute(
                "INSERT INTO reports (slug, title, mtime, stars) VALUES (?, ?, ?, ?)",
                ("a", "A", "2026-01-01", -1),
            )
        c.close()


class TestUrlNormalization(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(init_db.normalize_url("https://github.com/Foo/Bar"), "https://github.com/foo/bar")

    def test_trailing_slash(self):
        self.assertEqual(init_db.normalize_url("https://github.com/foo/bar/"), "https://github.com/foo/bar")

    def test_preserves_double_slash(self):
        """rstrip('/') 不应剥掉 https:// 前的 // —— Python str.rstrip 是按字符剥两端。"""
        u = init_db.normalize_url("https://github.com/foo/bar")
        self.assertTrue(u.startswith("https://"))

    def test_none(self):
        self.assertIsNone(init_db.normalize_url(None))


class TestTagLockProtection(TempDBTest):
    def test_locked_slug_not_overwritten(self):
        """report_tag_locks 中的 slug 在 extract_tags 重跑时其 report_tags 不被覆盖。"""
        c = self.conn()
        # 准备：插入 1 个报告 + 2 个标签 + 1 个锁
        c.execute("INSERT INTO reports (slug, title, mtime) VALUES ('locked', 'L', '2026-01-01')")
        c.execute("INSERT INTO reports (slug, title, mtime) VALUES ('free', 'F', '2026-01-01')")
        c.execute("INSERT INTO tags (tag, label) VALUES ('manual-tag', 'Manual')")
        c.execute("INSERT INTO tags (tag, label) VALUES ('auto-tag', 'Auto')")
        c.execute("INSERT INTO report_tags (slug, tag) VALUES ('locked', 'manual-tag')")
        c.execute("INSERT INTO report_tag_locks (slug) VALUES ('locked')")
        c.commit()

        # 模拟 extract_tags 行为：对非锁定 slug 重写标签
        import extract_tags
        slug_to_tags = {"locked": ["auto-tag"], "free": ["auto-tag"]}
        extract_tags.write_report_tags(c, slug_to_tags)

        # 锁定 slug 保留 manual-tag；free 应被覆盖为 auto-tag
        locked_tags = [r[0] for r in c.execute("SELECT tag FROM report_tags WHERE slug='locked'")]
        free_tags = [r[0] for r in c.execute("SELECT tag FROM report_tags WHERE slug='free'")]
        self.assertEqual(locked_tags, ["manual-tag"], "锁定 slug 的标签应保留")
        self.assertEqual(free_tags, ["auto-tag"], "未锁定 slug 应被覆盖")
        c.close()


class TestExportJsonRoundtrip(TempDBTest):
    def test_published_roundtrip(self):
        """state=published + at=Y → compose 出 'published:Y'，与现有 reports.json 格式兼容。"""
        c = self.conn()
        c.execute(
            "INSERT INTO reports (slug, title, mtime, published_state, published_at) "
            "VALUES (?, ?, ?, ?, ?)",
            ("a", "A", "2026-01-01", "published", "2026-04-01"),
        )
        c.execute(
            "INSERT INTO reports (slug, title, mtime, published_state) VALUES (?, ?, ?, ?)",
            ("b", "B", "2026-01-01", "pending"),
        )
        c.execute(
            "INSERT INTO reports (slug, title, mtime, published_state, published_at) "
            "VALUES (?, ?, ?, ?, ?)",
            ("c", "C", "2026-01-01", "excluded", None),
        )
        c.commit()
        c.close()

        rows = init_db.dump_reports()
        by_slug = {r["slug"]: r for r in rows}
        self.assertEqual(by_slug["a"]["published"], "published:2026-04-01")
        self.assertEqual(by_slug["b"]["published"], "pending")
        self.assertEqual(by_slug["c"]["published"], "excluded")


class TestUserStarredView(TempDBTest):
    def test_join_to_reports(self):
        """v_user_starred 应能将 user_starred.url 与 reports.original_url 关联出 report_slug。"""
        c = self.conn()
        c.execute("INSERT INTO users (login, name) VALUES ('alice', 'Alice')")
        c.execute(
            "INSERT INTO reports (slug, title, mtime, original_url) VALUES (?, ?, ?, ?)",
            ("foo_bar", "Foo Bar", "2026-01-01", "https://github.com/foo/bar"),
        )
        c.execute(
            "INSERT INTO user_starred (login, url, name, stars, starred_at) "
            "VALUES (?, ?, ?, ?, ?)",
            ("alice", "https://github.com/foo/bar", "foo/bar", 100, "2026-01-02"),
        )
        c.execute(
            "INSERT INTO user_starred (login, url, name, stars, starred_at) "
            "VALUES (?, ?, ?, ?, ?)",
            ("alice", "https://github.com/x/y", "x/y", 50, "2026-01-03"),
        )
        c.commit()

        rows = dict(c.execute(
            "SELECT url, report_slug FROM v_user_starred WHERE login='alice'"
        ).fetchall())
        self.assertEqual(rows["https://github.com/foo/bar"], "foo_bar")
        self.assertIsNone(rows["https://github.com/x/y"])
        c.close()

    def test_user_starred_cascade_delete(self):
        """删除 users 行应级联清理 user_starred / user_tags / snapshot。"""
        c = self.conn()
        c.execute("INSERT INTO users (login, name) VALUES ('bob', 'Bob')")
        c.execute("INSERT INTO user_tags (login, tag) VALUES ('bob', 'devtools')")
        c.execute(
            "INSERT INTO user_starred_snapshot (login, fetched_at) VALUES ('bob', '2026-01-01')"
        )
        c.execute(
            "INSERT INTO user_starred (login, url, name, stars, starred_at) "
            "VALUES (?, ?, ?, ?, ?)",
            ("bob", "https://github.com/a/b", "a/b", 1, "2026-01-01"),
        )
        c.commit()
        c.execute("DELETE FROM users WHERE login='bob'")
        c.commit()

        self.assertEqual(c.execute("SELECT COUNT(*) FROM user_tags").fetchone()[0], 0)
        self.assertEqual(c.execute("SELECT COUNT(*) FROM user_starred").fetchone()[0], 0)
        self.assertEqual(c.execute("SELECT COUNT(*) FROM user_starred_snapshot").fetchone()[0], 0)
        c.close()


class TestStarredJsonRoundtrip(TempDBTest):
    def test_dump_preserves_user_order_and_tags(self):
        """dump_starred 应按 users.sort_order 输出 users；tags 按 position 输出（与 yaml 顺序一致）。"""
        c = self.conn()
        c.execute("INSERT INTO users (login, name, sort_order) VALUES ('u2', 'U2', 1)")
        c.execute("INSERT INTO users (login, name, sort_order) VALUES ('u1', 'U1', 0)")
        c.execute("INSERT INTO user_tags (login, tag, position) VALUES ('u1', 'b-tag', 0)")
        c.execute("INSERT INTO user_tags (login, tag, position) VALUES ('u1', 'a-tag', 1)")
        c.commit()
        c.close()

        data = init_db.dump_starred()
        self.assertEqual([u["login"] for u in data["users"]], ["u1", "u2"])
        self.assertEqual(data["users"][0]["tags"], ["b-tag", "a-tag"])


class TestPublishHistory(TempDBTest):
    def test_state_check_constraint(self):
        c = self.conn()
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute(
                "INSERT INTO publish_history (recorded_at, slug, state) "
                "VALUES ('2026-01-01T00:00:00Z', 'a', 'wrong_state')"
            )
        c.close()

    def test_v_publish_latest_by_recorded_at(self):
        """同 slug 多行时，v_publish_latest 取 recorded_at 最新行。"""
        c = self.conn()
        # pending → published 状态变化
        c.execute(
            "INSERT INTO publish_history (recorded_at, slug, state, published_at, reason) "
            "VALUES ('2026-01-10T00:00:00Z', 'foo', 'pending', '2026-01-10', '自动生成')"
        )
        c.execute(
            "INSERT INTO publish_history (recorded_at, slug, state, published_at, title) "
            "VALUES ('2026-02-15T00:00:00Z', 'foo', 'published', '2026-02-15', 'Foo 标题')"
        )
        c.commit()

        row = c.execute(
            "SELECT state, published_at, title, reason FROM v_publish_latest WHERE slug='foo'"
        ).fetchone()
        self.assertEqual(row, ("published", "2026-02-15", "Foo 标题", None))
        c.close()

    def test_reconcile_reports_published(self):
        """reconcile_reports_published 应从 v_publish_latest 反查更新 reports.published_*。"""
        import init_db
        c = self.conn()
        c.execute(
            "INSERT INTO reports (slug, title, mtime) VALUES ('foo', 'Foo', '2026-01-01')"
        )
        c.execute(
            "INSERT INTO reports (slug, title, mtime) VALUES ('bar', 'Bar', '2026-01-01')"
        )
        c.execute(
            "INSERT INTO publish_history (recorded_at, slug, state, published_at, title, reason) "
            "VALUES ('2026-02-01T00:00:00Z', 'foo', 'published', '2026-02-01', 'Foo 公众号', null)"
        )
        c.execute(
            "INSERT INTO publish_history (recorded_at, slug, state, reason) "
            "VALUES ('2026-02-01T00:00:00Z', 'bar', 'excluded', '重复')"
        )
        c.commit()
        n = init_db.reconcile_reports_published(c)
        self.assertEqual(n, 2)
        foo = c.execute(
            "SELECT published_state, published_at, published_title FROM reports WHERE slug='foo'"
        ).fetchone()
        self.assertEqual(foo, ("published", "2026-02-01", "Foo 公众号"))
        bar = c.execute(
            "SELECT published_state, published_at, published_title FROM reports WHERE slug='bar'"
        ).fetchone()
        self.assertEqual(bar, ("excluded", None, None))
        c.close()

    def test_seed_publish_history_from_jsonl(self):
        """seed_publish_history 应从 jsonl 全量重建 publish_history 表。"""
        import init_db
        c = self.conn()
        # 先插入一行旧数据，确认 seed 会清空
        c.execute(
            "INSERT INTO publish_history (recorded_at, slug, state) "
            "VALUES ('2026-01-01T00:00:00Z', 'stale', 'pending')"
        )
        c.commit()

        # 写一个临时 jsonl
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False, encoding="utf-8") as f:
            f.write(json.dumps({
                "recorded_at": "2026-02-01T00:00:00Z",
                "slug": "fresh", "state": "published", "published_at": "2026-02-01",
                "title": "T", "reason": None, "ci_run_id": None,
            }, ensure_ascii=False) + "\n")
            f.write(json.dumps({  # 无效 state 应被跳过
                "recorded_at": "2026-02-02T00:00:00Z",
                "slug": "bad", "state": "wrong", "published_at": None,
            }, ensure_ascii=False) + "\n")
            jsonl_path = Path(f.name)

        try:
            n = init_db.seed_publish_history(c, jsonl_path)
            self.assertEqual(n, 1)
            rows = c.execute("SELECT slug, state FROM publish_history").fetchall()
            self.assertEqual(rows, [("fresh", "published")])
        finally:
            os.unlink(jsonl_path)
        c.close()


class TestTrending(TempDBTest):
    def _insert_snapshot(self, c, period_type, period_key, url, stars=100, forks=10, rank=None):
        c.execute(
            "INSERT OR IGNORE INTO trending_repos (url, name) VALUES (?, ?)",
            (url, url.replace("https://github.com/", "")),
        )
        c.execute(
            "INSERT INTO trending_snapshots (period_type, period_key, url, stars, forks, rank) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (period_type, period_key, url, stars, forks, rank),
        )

    def test_invalid_period_type(self):
        """period_type 非枚举值应 fail。"""
        c = self.conn()
        c.execute("INSERT INTO trending_repos (url, name) VALUES ('https://github.com/a/b', 'a/b')")
        with self.assertRaises(sqlite3.IntegrityError):
            c.execute(
                "INSERT INTO trending_snapshots (period_type, period_key, url, stars) "
                "VALUES ('hourly', '2026-01-01-00', 'https://github.com/a/b', 1)"
            )
        c.close()

    def test_snapshot_pk_idempotent(self):
        """同一 (period_type, period_key, url) 多次 seed 不重复（INSERT OR REPLACE）。"""
        c = self.conn()
        self._insert_snapshot(c, "daily", "2026-01-01", "https://github.com/a/b", stars=100)
        # INSERT OR REPLACE 模拟 seed_trending 行为
        c.execute(
            "INSERT OR REPLACE INTO trending_snapshots (period_type, period_key, url, stars, forks) "
            "VALUES ('daily', '2026-01-01', 'https://github.com/a/b', 200, 0)"
        )
        c.commit()
        rows = c.execute("SELECT stars FROM trending_snapshots WHERE url='https://github.com/a/b'").fetchall()
        self.assertEqual(len(rows), 1, "PK 唯一约束应保证只有一行")
        self.assertEqual(rows[0][0], 200, "REPLACE 应使用新 stars 值")
        c.close()

    def test_v_trending_days(self):
        c = self.conn()
        url = "https://github.com/a/b"
        self._insert_snapshot(c, "daily", "2026-01-01", url)
        self._insert_snapshot(c, "daily", "2026-01-02", url)
        self._insert_snapshot(c, "daily", "2026-01-03", url)
        self._insert_snapshot(c, "weekly", "2026-W01", url)
        self._insert_snapshot(c, "monthly", "2026-01", url)
        c.commit()
        row = c.execute("SELECT daily_count, weekly_count, monthly_count FROM v_trending_days WHERE url=?", (url,)).fetchone()
        self.assertEqual(row, (3, 1, 1))
        c.close()

    def test_v_trending_window(self):
        """v_trending_repo_window.last_daily 应只取 daily 时段的最大值。"""
        c = self.conn()
        url = "https://github.com/a/b"
        self._insert_snapshot(c, "daily", "2026-01-01", url)
        self._insert_snapshot(c, "daily", "2026-01-15", url)
        self._insert_snapshot(c, "weekly", "2026-W10", url)
        c.commit()
        row = c.execute("SELECT last_daily FROM v_trending_repo_window WHERE url=?", (url,)).fetchone()
        self.assertEqual(row[0], "2026-01-15")
        c.close()

    def test_dump_trending_deduped(self):
        """dump_trending_deduped 用 daily_count 作 trending_days，last_daily 作 last_seen。"""
        c = self.conn()
        url = "https://github.com/a/b"
        self._insert_snapshot(c, "daily", "2026-01-01", url, stars=50, forks=5)
        self._insert_snapshot(c, "daily", "2026-01-02", url, stars=100, forks=10)
        c.commit()
        c.close()
        rows = init_db.dump_trending_deduped()
        self.assertEqual(len(rows), 1)
        r = rows[0]
        self.assertEqual(r["trending_days"], 2)
        self.assertEqual(r["last_seen"], "2026-01-02")
        self.assertEqual(r["stars"], 100, "stars 应取最高的那次快照")
        self.assertEqual(r["forks"], 10)


# 注：原 TestPublishMdParsing（测 build_reports_index.parse_publish_index 对 publish.md
# 的三种行格式解析）已随 publish.md 删除而移除——发布历史 SoR 自阶段 4 起为
# src/data/publish_history.jsonl，相关往返见 TestPublishHistory。


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""向搜索引擎推送新增/更新的 URL，加速收录。

支持的渠道（按可用环境变量自动启用）：
- IndexNow（Bing / Yandex / Naver / AI 搜索）：需 INDEXNOW_KEY
- 百度普通收录（仅 main 域名）：需 BAIDU_PUSH_TOKEN

使用：
    python3 scripts/ping_search_engines.py [--dry-run]

输入：
    src/data/reports.json    所有报告及 mtime
    tmp/last_indexed.json    上次推送快照（首次运行不存在则全量推送，但默认限制 50 条）

输出：
    更新 tmp/last_indexed.json
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORTS_JSON = ROOT / "src" / "data" / "reports.json"
SNAPSHOT = ROOT / "tmp" / "last_indexed.json"

SITE_URL = os.environ.get("SITE_URL", "https://seeyeetech.com").rstrip("/")
BASE_PATH = os.environ.get("PUBLIC_BASE_PATH", "/github-explorer").rstrip("/")
INDEXNOW_KEY = os.environ.get("INDEXNOW_KEY", "").strip()
BAIDU_PUSH_TOKEN = os.environ.get("BAIDU_PUSH_TOKEN", "").strip()

MAX_FIRST_RUN = 50  # 首次无快照时只推最近 50 篇，避免大量旧 URL 触发限流


def absolute_url(path: str) -> str:
    p = path if path.startswith("/") else f"/{path}"
    return f"{SITE_URL}{BASE_PATH}{p}"


def load_reports() -> list[dict]:
    if not REPORTS_JSON.exists():
        print(f"[warn] {REPORTS_JSON} 不存在，跳过推送", file=sys.stderr)
        return []
    return json.loads(REPORTS_JSON.read_text("utf-8"))


def load_snapshot() -> dict[str, str]:
    if not SNAPSHOT.exists():
        return {}
    try:
        return json.loads(SNAPSHOT.read_text("utf-8"))
    except Exception:
        return {}


def save_snapshot(data: dict[str, str]) -> None:
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT.write_text(json.dumps(data, ensure_ascii=False, indent=2), "utf-8")


def diff_urls(reports: list[dict], snapshot: dict[str, str]) -> list[str]:
    """返回需要推送的报告 URL 列表。"""
    changed: list[tuple[str, str]] = []
    for r in reports:
        slug, mtime = r.get("slug"), r.get("mtime")
        if not slug or not mtime:
            continue
        if snapshot.get(slug) != mtime:
            changed.append((mtime, absolute_url(f"/reports/{slug}")))

    # 首次运行（snapshot 为空）只推最近 N 篇
    if not snapshot and len(changed) > MAX_FIRST_RUN:
        changed.sort(reverse=True)
        changed = changed[:MAX_FIRST_RUN]

    # 总是把首页/列表页一并推送（它们的 lastmod 会随报告变化）
    extra = [absolute_url("/"), absolute_url("/reports")]
    return extra + [u for _, u in changed]


def push_indexnow(urls: list[str], dry_run: bool) -> None:
    if not INDEXNOW_KEY:
        print("[skip] 未配置 INDEXNOW_KEY，跳过 IndexNow")
        return
    host = SITE_URL.replace("https://", "").replace("http://", "").split("/")[0]
    payload = {
        "host": host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{SITE_URL}{BASE_PATH}/{INDEXNOW_KEY}.txt",
        "urlList": urls,
    }
    print(f"[indexnow] host={host} urls={len(urls)}")
    if dry_run:
        print(f"[dry-run] POST https://api.indexnow.org/indexnow → {len(urls)} URLs")
        return
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            print(f"[indexnow] HTTP {resp.status} {resp.reason}")
    except urllib.error.HTTPError as e:
        print(f"[warn] indexnow HTTPError {e.code}: {e.read().decode('utf-8', 'replace')[:200]}")
    except Exception as e:
        print(f"[warn] indexnow 失败: {e}")


def push_baidu(urls: list[str], dry_run: bool) -> None:
    if not BAIDU_PUSH_TOKEN:
        print("[skip] 未配置 BAIDU_PUSH_TOKEN，跳过百度推送")
        return
    # 百度只对主域名生效，子域名 / 子路径未必收录；这里仍尝试，由百度判断
    site = SITE_URL.replace("https://", "").replace("http://", "")
    api = f"https://data.zz.baidu.com/urls?site={site}&token={BAIDU_PUSH_TOKEN}"
    print(f"[baidu] site={site} urls={len(urls)}")
    if dry_run:
        print(f"[dry-run] POST {api[:80]}... → {len(urls)} URLs")
        return
    body = "\n".join(urls).encode("utf-8")
    req = urllib.request.Request(api, data=body, headers={"Content-Type": "text/plain"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            print(f"[baidu] HTTP {resp.status}: {resp.read().decode('utf-8', 'replace')[:200]}")
    except urllib.error.HTTPError as e:
        print(f"[warn] baidu HTTPError {e.code}: {e.read().decode('utf-8', 'replace')[:200]}")
    except Exception as e:
        print(f"[warn] baidu 失败: {e}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只打印待推送 URL，不实际发请求")
    args = ap.parse_args()

    reports = load_reports()
    snapshot = load_snapshot()
    urls = diff_urls(reports, snapshot)

    if not urls:
        print("[info] 无新增/更新 URL，跳过推送")
        return 0

    print(f"[info] 待推送 {len(urls)} 个 URL（含首页/列表）")
    for u in urls[:10]:
        print(f"  - {u}")
    if len(urls) > 10:
        print(f"  ... 其余 {len(urls) - 10} 条略")

    push_indexnow(urls, args.dry_run)
    push_baidu(urls, args.dry_run)

    if not args.dry_run:
        new_snapshot = {r["slug"]: r["mtime"] for r in reports if r.get("slug") and r.get("mtime")}
        save_snapshot(new_snapshot)
        print(f"[info] 已更新快照 {SNAPSHOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

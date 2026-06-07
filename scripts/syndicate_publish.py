#!/usr/bin/env python3
"""一文多发 CLI：把一篇分析报告发布到指定渠道（自动带导流公众号页脚）。

用法：
  python3 scripts/syndicate_publish.py <report.md> --channel cnblogs [选项]

选项：
  --channel NAME   目标渠道（必填），如 cnblogs；列表见 --list
  --publish        直接公开（默认仅存草稿，便于人工复核）
  --dry-run        只解析+渲染+判断新建/更新，不联网、不写历史
  --force-new      忽略已记录的 post_id，强制新建（默认按 slug+channel 幂等更新）
  --list           打印已注册渠道并退出

幂等：按 (slug, channel) 在 publish_history.jsonl 查最近 post_id；
有则更新（editPost）、无则新建（newPost），避免重复发文。

凭据放 .env.local（自动加载，不覆盖已有 env），见 scripts/syndicate/README.md。
产物：tmp/last_syndicate.json（最近一次结果）。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

# 让 `syndicate` 包可被导入（同 wechat_publish.py `from _wechat_api import` 的运行约定）
sys.path.insert(0, str(Path(__file__).resolve().parent))

from syndicate import history, render as render_mod  # noqa: E402
from syndicate.base import (  # noqa: E402
    available_channels,
    get_adapter,
    load_dotenv,
    parse_report,
)


def _prepare_browser(article, channel, adapter, *, force_new: bool) -> int:
    """浏览器渠道：渲染 + 写发布包 + 打印 playbook，供 Claude-in-Chrome 执行。"""
    prev = None if force_new else history.latest_record(article.slug, channel)
    existing_url = (prev or {}).get("url") or ""
    rendered = render_mod.render(
        article, adapter.content_format,
        mp_cta=adapter.mp_cta, name_wechat=adapter.name_wechat,
    )
    pkg = adapter.prepare(article, rendered, existing_url=existing_url)

    pkg_path = Path("tmp") / f"syndicate-{channel}-{article.slug}.package.json"
    pkg_path.parent.mkdir(parents=True, exist_ok=True)
    pkg_path.write_text(
        json.dumps(pkg.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
    )

    mark = "更新" if existing_url else "新建"
    print(f"📄 {article.slug}  →  渠道 {channel}  [浏览器自动化 · {mark}]")
    print(f"   标题: {article.title}")
    print(f"   编辑器: {pkg.editor_url}")
    print(f"   正文: {pkg.content_path}（{rendered.content_format}，含导流页脚）")
    print(f"   发布包: {pkg_path}")
    if pkg.field_notes:
        print("   发布字段:")
        for k, v in pkg.field_notes.items():
            print(f"     · {k}: {v}")
    print("   ── playbook（交给 Claude-in-Chrome 执行）──")
    for i, step in enumerate(pkg.steps, 1):
        print(f"     {i}. {step}")
    print("   提示：发布是对你账号的对外动作，需在已登录该平台的浏览器里进行；"
          "发完用上面最后一步的 --record 回写历史。")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("report", nargs="?", help="报告 .md 路径")
    p.add_argument("--channel", help="目标渠道 id")
    p.add_argument("--publish", action="store_true", help="直接公开（默认存草稿）")
    p.add_argument("--dry-run", action="store_true", help="不联网，仅验证解析/渲染/幂等判断")
    p.add_argument("--force-new", action="store_true", help="忽略已记录 post_id，强制新建")
    p.add_argument("--list", action="store_true", help="列出已注册渠道")
    # 浏览器渠道（juejin/csdn）发布后回写历史：
    p.add_argument("--record", action="store_true",
                   help="回写一条发布历史（浏览器渠道由 agent 发完后用）")
    p.add_argument("--url", help="远端文章 URL（配合 --record）")
    p.add_argument("--post-id", help="远端文章 id（配合 --record）")
    p.add_argument("--state", default="published",
                   choices=["pending", "draft", "excluded", "published"],
                   help="--record 的状态，默认 published")
    args = p.parse_args(argv)

    load_dotenv()

    if args.list:
        print("已注册渠道:", ", ".join(available_channels()) or "(无)")
        return 0
    if not args.report or not args.channel:
        p.error("需要 <report.md> 和 --channel（或用 --list 查看渠道）")

    md_path = Path(args.report)
    if not md_path.is_file():
        print(f"❌ 找不到报告: {md_path}", file=sys.stderr)
        return 1

    article = parse_report(md_path)
    channel = args.channel

    # ── --record：浏览器渠道（或任意渠道）发布完成后回写历史 ──
    if args.record:
        rec = history.append_record(
            slug=article.slug,
            channel=channel,
            state=args.state,
            title=article.title,
            post_id=args.post_id,
            url=args.url,
            published_at=time.strftime("%Y-%m-%d") if args.state == "published" else None,
            ci_run_id=os.environ.get("GITHUB_RUN_ID"),
        )
        print(f"✅ 已回写历史：{article.slug} / {channel} / {args.state}"
              f"{f' / {args.url}' if args.url else ''}")
        return 0

    if not article.allows(channel):
        print(f"⏭ 报告 frontmatter syndicate 排除了渠道 {channel}，跳过")
        return 0

    try:
        adapter = get_adapter(channel)
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    # ── 浏览器渠道（juejin/csdn）：脚本只 prepare 发布包 + playbook，发布由 agent 驱动 ──
    if adapter.mode == "browser":
        return _prepare_browser(article, channel, adapter, force_new=args.force_new)

    # self_render 渠道（公众号）自带渲染管线，跳过框架 render 与导流页脚
    rendered = (
        None if adapter.self_render
        else render_mod.render(
            article, adapter.content_format,
            mp_cta=adapter.mp_cta, name_wechat=adapter.name_wechat,
        )
    )

    prev = None if args.force_new else history.latest_record(article.slug, channel)
    existing_post_id = (prev or {}).get("post_id")
    if adapter.self_render:
        action = "自渲染发布"
    else:
        action = "更新(editPost)" if existing_post_id else "新建(newPost)"

    print(f"📄 {article.slug}  →  渠道 {channel}  [{action}]")
    print(f"   标题: {article.title}")
    print(f"   来源: {article.source_url or '(未识别)'}")
    print(f"   canonical: {article.canonical_url}")
    if rendered is not None:
        print(f"   渲染: {rendered.content_format} / {len(rendered.content)} bytes")

    if args.dry_run:
        if adapter.self_render:
            try:
                out = adapter.dry_run(article)
            except RuntimeError as e:
                print(f"❌ {e}", file=sys.stderr)
                return 1
            print(f"🧪 dry-run：{channel} 自渲染产物 → {out or '(见上方日志)'}（未发布、未写历史）")
        else:
            ext = "html" if rendered.content_format == "html" else "md"
            out = Path("tmp") / f"syndicate-{channel}-{article.slug}.{ext}"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(rendered.content, encoding="utf-8")
            print(f"🧪 dry-run：渲染结果 → {out}（未联网、未写历史）")
        return 0

    try:
        adapter.check_auth()
        result = adapter.publish(
            article, rendered, publish=args.publish, existing_post_id=existing_post_id
        )
    except RuntimeError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1
    except Exception as e:  # noqa: BLE001 — 网络/XML-RPC 等运行期错误统一收敛
        print(f"❌ 发布失败（{channel}）: {e}", file=sys.stderr)
        return 1

    history.append_record(
        slug=article.slug,
        channel=channel,
        state=result.state,
        title=article.title,
        post_id=result.post_id,
        url=result.url,
        published_at=time.strftime("%Y-%m-%d") if result.state == "published" else None,
        ci_run_id=os.environ.get("GITHUB_RUN_ID"),
    )

    Path("tmp").mkdir(exist_ok=True)
    Path("tmp/last_syndicate.json").write_text(
        json.dumps(
            {
                "channel": channel,
                "slug": article.slug,
                "title": article.title,
                "post_id": result.post_id,
                "url": result.url,
                "state": result.state,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    icon = "✅ 已公开" if result.state == "published" else "✅ 已存草稿"
    print(f"{icon}：{result.url}  (post_id={result.post_id})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

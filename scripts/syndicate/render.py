"""Markdown → 各平台格式（html / markdown）+ 导流公众号页脚。

与 wechat_publish.py 的区别：那里是公众号专用（删外链图、CSS 全内联、删 H1），
因为公众号正文不支持外链图。这里面向「正常支持外链图与标准 HTML」的平台
（博客园等），渲染更轻：md→html 即可，图片原样保留。

【导流公众号页脚】是本框架把外部读者引回公众号的框架级钩子——每个外发渠道
自动追加，用「全网同名 + 微信搜一搜」绕开外链/关键词风控（最稳健的合规打法）。
"""
from __future__ import annotations

import os

from .base import Article, RenderedArticle

try:
    import markdown
except ImportError:  # pragma: no cover
    markdown = None


def _footer_md(article: Article, *, mp_cta: bool = True, name_wechat: bool = True) -> str:
    """导流页脚（markdown 片段）。WECHAT_MP_NAME 为空且无 canonical 时返回空串。

    mp_cta=False  → 只留 canonical 回链，完全不放公众号 CTA（如知乎，任何引导都易限流）。
    name_wechat=False → CTA 回避「微信公众号 / 微信」字样（如 CSDN/阿里云），但仍保留账号名
                        +「全网同名，搜一搜即达」，靠同名让读者自行搜到。
    """
    mp = os.environ.get("WECHAT_MP_NAME", "").strip()
    lines: list[str] = []
    if article.canonical_url:
        lines.append(f"> 本文首发于 [GitHub Explorer]({article.canonical_url})，原文持续更新。")
    if mp and mp_cta:
        if name_wechat:
            lines.append(
                f"> 关注微信公众号「{mp}」（全网同名，微信搜一搜即达），"
                "后台回复关键词「repo」领取完整版资料。"
            )
        else:
            lines.append(
                f"> 关注「{mp}」（全网同名，搜一搜即达），"
                "后台回复关键词「repo」领取完整版资料。"
            )
    return ("\n\n---\n\n" + "\n>\n".join(lines)) if lines else ""


def render(
    article: Article,
    content_format: str,
    *,
    with_footer: bool = True,
    mp_cta: bool = True,
    name_wechat: bool = True,
) -> RenderedArticle:
    """把 Article 渲染成目标平台所需格式。

    mp_cta / name_wechat 透传给页脚，按平台限制控制公众号 CTA 的有无与措辞。
    """
    md_text = article.body_md + (
        _footer_md(article, mp_cta=mp_cta, name_wechat=name_wechat) if with_footer else ""
    )

    if content_format == "markdown":
        return RenderedArticle(article.title, md_text, "markdown")

    if content_format == "html":
        if markdown is None:
            raise RuntimeError("缺少 markdown 包：venv/bin/pip install markdown")
        # 'extra' 含 tables/fenced_code/abbr 等 GFM 子集；'sane_lists' 让数字行被识别为 ol
        md = markdown.Markdown(extensions=["extra", "sane_lists"])
        return RenderedArticle(article.title, md.convert(md_text), "html")

    raise RuntimeError(f"不支持的 content_format: {content_format}")

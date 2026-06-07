"""CSDN adapter —— Playwright 持久化登录 + 脚本驱动发布（路线 C）。

从旧的 mode='browser'（agent 实时驱动 DOM）升级为 mode='playwright'（脚本用
Playwright 复用「一次性手动登录」的持久化会话，固定代码驱动 DOM）。一次 `--login`、
之后一条命令一键发，不再需要 Claude 盯屏幕逐步操作。设计与基类见 ../playwright_base.py。

CSDN markdown 编辑器：editor.csdn.net/md/，需登录态。发布流程：写正文 → 填标题 →
点「发布文章」→ 弹窗填 标签 / 分类专栏 / 封面 / 文章类型(原创) / 可见范围 → 发布。
存草稿走顶部「保存草稿」。编辑既有文章：editor.csdn.net/md/?articleId=<id>，故 post_id
直接复用为 article id 做幂等更新。

导流到公众号：**CSDN 禁止出现「微信公众号 / 微信」字样**（用户实测/平台规则），故置
name_wechat=False —— 渲染层页脚仍点名账号「智能时代蛮子」+「全网同名，搜一搜即达」，
只是不出现「微信」字样，靠同名让读者自行搜到，不触发 CSDN 关键词拦截。

⚠️ selector 会随 CSDN 改版漂移。首次跑通后若报「找不到元素」，用
`playwright codegen https://editor.csdn.net/md/` 录制真实 selector 更新下方常量即可。
"""
from __future__ import annotations

import re

from ..base import Article, PublishResult, RenderedArticle, register
from ..playwright_base import PlaywrightAdapter


@register
class CsdnAdapter(PlaywrightAdapter):
    name = "csdn"
    editor_url = "https://editor.csdn.net/md/"
    login_url = "https://passport.csdn.net/login?code=public"
    content_format = "markdown"
    name_wechat = False   # CSDN 禁「微信」字样：页脚保留账号名但不点名微信

    # ── selector（集中管理，便于改版校准；每项多个兜底）────────────────────
    SEL_TITLE = [
        "input[placeholder*='标题']",
        "input.article-bar__title",
        ".article-bar input[type='text']",
    ]
    SEL_EDITOR = [
        ".cm-content",                 # CodeMirror 6
        ".CodeMirror textarea",        # CodeMirror 5 隐藏输入
        ".CodeMirror",
        "div.editor__inner",
    ]
    SEL_PUBLISH_BTN = [               # 右上「发布文章」（打开发布弹窗）
        "button.btn-publish",
        "button:has-text('发布文章')",
    ]
    SEL_SAVE_DRAFT = [               # 顶部「保存草稿」
        "button:has-text('保存草稿')",
        "button:has-text('保存为草稿')",
        ".save-draft",
    ]
    SEL_TAG_INPUT = [
        "input[placeholder*='文章标签']",
        "input[placeholder*='标签']",
        ".mark-selection-item input",
        ".tag-box input",
    ]
    SEL_MODAL_PUBLISH = [            # 弹窗内最终「发布文章」
        ".modal-container button:has-text('发布文章')",
        ".el-dialog button:has-text('发布文章')",
        ".modal button.btn-b-red",
        "button.btn-b-red:has-text('发布')",
    ]

    # CSDN 登录后写入的 cookie（任一存在即视为已登录）
    LOGIN_COOKIES = {"UserName", "UserToken", "UserInfo"}

    def is_logged_in(self, context) -> bool:
        try:
            names = {c.get("name") for c in context.cookies()}
        except Exception:  # noqa: BLE001
            return False
        return bool(names & self.LOGIN_COOKIES)

    def do_publish(
        self, page, article: Article, rendered: RenderedArticle, *,
        publish: bool, existing_post_id: str | None, commit: bool,
    ) -> PublishResult | None:
        # 1) 打开编辑器（更新则带 articleId）
        target = (
            f"{self.editor_url}?articleId={existing_post_id}"
            if existing_post_id else self.editor_url
        )
        page.goto(target, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)  # 编辑器异步初始化
        if "passport.csdn.net" in page.url:
            raise RuntimeError("打开编辑器被重定向到登录页，登录态可能失效，请重跑 --login")

        # 2) 标题
        title_el = self._first(page, self.SEL_TITLE)
        title_el.click()
        title_el.fill(article.title)

        # 3) 正文（CodeMirror：聚焦后一次性插入）
        self._focus_insert(page, self.SEL_EDITOR, rendered.content)
        page.wait_for_timeout(500)

        # 4) 预演到此为止（不点发布、不写历史）
        if not commit:
            return None

        # 5a) 存草稿
        if not publish:
            self._click(page, self.SEL_SAVE_DRAFT)
            page.wait_for_timeout(2000)
            pid = self._extract_article_id(page.url) or (existing_post_id or "")
            return PublishResult(post_id=pid, url=page.url, state="draft")

        # 5b) 发布：打开弹窗 → 填标签 →（类型默认原创、可见默认全部）→ 确认发布
        self._click(page, self.SEL_PUBLISH_BTN)
        page.wait_for_timeout(1500)
        if article.tags:
            tag_in = self._first(page, self.SEL_TAG_INPUT, required=False)
            if tag_in:
                for t in article.tags[:5]:
                    tag_in.click()
                    tag_in.fill(t)
                    page.wait_for_timeout(300)
                    page.keyboard.press("Enter")
        self._click(page, self.SEL_MODAL_PUBLISH)
        try:
            page.wait_for_url("**/article/details/**", timeout=30000)
        except Exception:  # noqa: BLE001 — 兜底：少数情况停在编辑器并提示成功
            page.wait_for_timeout(3000)
        pid = self._extract_article_id(page.url) or (existing_post_id or "")
        url = (
            page.url if "article/details" in page.url
            else f"https://blog.csdn.net/article/details/{pid}"
        )
        return PublishResult(post_id=pid, url=url, state="published")

    @staticmethod
    def _extract_article_id(url: str | None) -> str:
        m = re.search(r"(?:articleId=|article/details/)(\d+)", url or "")
        return m.group(1) if m else ""

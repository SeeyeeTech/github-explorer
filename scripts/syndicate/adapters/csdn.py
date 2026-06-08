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
        "pre.editor__inner[contenteditable='true']",   # CSDN 新版：contenteditable 的 pre
        ".editor__inner[contenteditable='true']",
        ".editor__inner",
        ".cm-content",                 # 旧版 CodeMirror 6 兜底
        ".CodeMirror textarea",
        ".CodeMirror",
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

    # CSDN 登录后写入的 cookie（任一存在即视为已登录）；is_logged_in 走基类默认实现。
    # 标题 input / 编辑区 / 弹窗按钮在 DOM 里存在却被判「不可见」，故全程走基类的
    # _js_set_value / _js_focus / _js_click / _js_click_button_text 绕 actionability。
    LOGIN_COOKIES = {"UserName", "UserToken", "UserInfo"}
    ID_RE = r"(?:articleId=|article/details/)(\d+)"

    def _fill_tags(self, page, tags: list[str]) -> None:
        """尽力填文章标签（CSDN 标签为二级弹层，selector 不稳；失败不阻塞发布）。"""
        try:
            page.evaluate("""() => {
                const el = [...document.querySelectorAll('button,span,a,div')].find(
                    e => /添加文章标签|文章标签/.test(e.textContent || '') && e.offsetParent !== null
                );
                if (el) el.click();
            }""")
            page.wait_for_timeout(800)
            for t in tags:
                box = page.locator(
                    "input.el-input__inner:visible, .tag-box input, input[placeholder*='标签']"
                ).first
                box.fill(t)
                page.wait_for_timeout(300)
                page.keyboard.press("Enter")
                page.wait_for_timeout(300)
        except Exception as e:  # noqa: BLE001 — 标签非必填，失败仅提示
            print(f"   [csdn] 标签填写跳过（{e}）")

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
        if "passport.csdn.net" in page.url:
            raise RuntimeError("打开编辑器被重定向到登录页，登录态可能失效，请重跑 --login")
        # 标题 input / 编辑区在 DOM 里存在却被 playwright 判定不可见，故等「挂载到 DOM」
        # （attached）而非 visible，随后全程走 JS 注入操作。
        page.wait_for_selector("input.article-bar__title", state="attached", timeout=25000)
        page.wait_for_timeout(1500)

        # 2) 标题（JS 设 value + 派发事件，绕过不可见判定）
        if not self._js_set_value(
            page, ["input.article-bar__title", "input[placeholder*='标题']"], article.title
        ):
            raise RuntimeError("[csdn] DOM 中找不到标题输入框 input.article-bar__title（编辑器或已改版）")

        # 3) 正文：JS 聚焦编辑区 → 全选删默认模板 → keyboard 灌入（受控 contenteditable）
        if not self._js_focus(
            page,
            ["pre.editor__inner[contenteditable='true']",
             ".editor__inner[contenteditable='true']", ".editor__inner"],
        ):
            raise RuntimeError("[csdn] DOM 中找不到正文编辑区 .editor__inner（编辑器或已改版）")
        page.wait_for_timeout(300)
        page.keyboard.press("ControlOrMeta+a")
        page.keyboard.press("Delete")
        page.keyboard.insert_text(rendered.content)
        page.wait_for_timeout(800)

        # 4) 预演到此为止（不点发布、不写历史）
        if not commit:
            return None

        # 5a) 存草稿（顶部「保存草稿」按钮）
        if not publish:
            self._js_click(page, ["button.btn-save"])
            page.wait_for_timeout(2500)
            pid = self._extract_id(page.url, self.ID_RE) or (existing_post_id or "")
            return PublishResult(post_id=pid, url=page.url, state="draft")

        # 5b) 发布：打开弹窗 →（标签尽力填，失败不阻塞）→ 点弹窗内「发布文章」确认
        self._js_click(page, ["button.btn-publish"])
        page.wait_for_timeout(2000)
        if article.tags:
            self._fill_tags(page, list(article.tags)[:5])
        # 弹窗确认：btn-b-red 且文本含「发布文章」（排除同为 btn-b-red 的「定时发布」）
        if not self._js_click_button_text(page, "发布文章", cls_contains="btn-b-red"):
            raise RuntimeError("[csdn] 找不到发布弹窗内「发布文章」确认按钮（弹窗未弹出或已改版）")
        # 新文常进 CSDN「待审核」、不跳详情页，id 多半不反映到当前 url：先给跳转一点时间，
        # 拿不到再回退「文章管理列表取最新一篇」。
        try:
            page.wait_for_url("**/article/details/**", timeout=15000)
        except Exception:  # noqa: BLE001
            page.wait_for_timeout(3000)
        pid = self._extract_id(page.url, self.ID_RE)
        url = page.url if "article/details" in page.url else ""
        if not pid:
            latest = self._latest_article(page)
            if latest:
                pid, url = latest
            else:
                pid = existing_post_id or ""
        if not url:
            url = f"https://blog.csdn.net/article/details/{pid}" if pid else page.url
        return PublishResult(post_id=pid, url=url, state="published")

    @staticmethod
    def _latest_article(page) -> tuple[str, str] | None:
        """去文章管理列表取最新一篇的 (id, url)。CSDN 新文常进「待审核」、不跳详情页，
        id 不反映到当前 url 时用此兜底（列表按时间倒序，第一篇即刚发的）。"""
        try:
            page.goto("https://mp.csdn.net/mp_blog/manage/article",
                      wait_until="domcontentloaded")
            page.wait_for_timeout(4000)
            hrefs = page.eval_on_selector_all(
                "a[href*='article/details']", "els=>els.map(e=>e.href)"
            )
        except Exception:  # noqa: BLE001
            return None
        for h in hrefs:
            m = re.search(r"article/details/(\d+)", h or "")
            if m:
                return m.group(1), h
        return None

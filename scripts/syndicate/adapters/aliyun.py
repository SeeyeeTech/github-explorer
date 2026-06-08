"""阿里云开发者社区 adapter —— Playwright 持久化登录 + 脚本驱动发布（路线 C）。

从旧的 mode='browser'（agent 实时驱动 DOM）升级为 mode='playwright'（脚本用
Playwright 复用「一次性手动登录」的持久化会话，固定代码驱动 DOM）。一次 `--login`、
之后一条命令一键发，不再需要 Claude 盯屏幕逐步操作。设计与基类见 ../playwright_base.py。

阿里云写作页（developer.aliyun.com/article/new）的最大特殊点：**默认可能停在富文本
模式**。技术长文必须先切到 **Markdown 模式**（CodeMirror，左写右预览）再灌正文——
否则把 markdown 源码塞进富文本编辑器会被当成纯文本/毁掉排版。切模式时平台常弹一个
「切换后内容可能丢失」的确认框；因为我们是在「灌任何内容之前」就切，确认掉是无害的。
为此 `_ensure_markdown_mode()` 在切换后强制校验 CodeMirror 是否出现，**切不出来就
主动 raise**（护栏 A1：宁可大声失败，也不往富文本里灌 markdown）。需登录态（未登录
会 302 跳 account.aliyun.com）。

导流到公众号：阿里云**中等偏紧**、有反「营销/导流」机制，倾向把流量留在自身（乘风者
计划）。正文放二维码 +「扫码关注微信公众号」风险较高，故置 name_wechat=False —— 渲染层
页脚仍点名账号「智能时代蛮子」+「全网同名，搜一搜即达」，只是不出现「微信公众号 / 微信」
字样，靠同名让读者自行搜到，降低被判软文的概率。mp_cta 仍为 True（保留账号名 CTA）。

坑：
  ① 默认富文本 → 必须先切 Markdown 模式再灌（见上，切模式护栏）；
  ② 外链图不保证自动转存，GitHub raw 图易 403，需先下载再走编辑器图片按钮上传到
     阿里云 CDN 并替换链接（脚本不处理图片，沿用渲染层产物）；
  ③ 发布弹窗里**技术领域为必选单选**，`_select_field()` 据 tags/标题匹配一个，匹配
     不到用固定兜底，选不到则 raise（必填项卡发布）。

⚠️ 下方 SEL_* / 领域名称会随阿里云改版漂移。首次跑通后若报「找不到元素」，用
`playwright codegen https://developer.aliyun.com/article/new` 录制真实 selector 更新
即可（注释里标了「Step3 校准」的都是当前最佳猜测）。
"""
from __future__ import annotations

import re

from ..base import Article, PublishResult, RenderedArticle, register
from ..playwright_base import PlaywrightAdapter


@register
class AliyunAdapter(PlaywrightAdapter):
    name = "aliyun"
    editor_url = "https://developer.aliyun.com/article/new"
    login_url = "https://account.aliyun.com/login/login.htm"
    content_format = "markdown"
    mp_cta = True          # 保留账号名 CTA…
    name_wechat = False    # …但阿里云中等偏紧：不点名「微信」，只留账号名 + 搜一搜

    # 阿里云登录后写入的 cookie（任一存在即视为已登录）——最佳猜测，Step3 用
    # `playwright codegen` 登录后在 DevTools→Application→Cookies 确认实际 cookie 名校准。
    LOGIN_COOKIES = {"login_aliyunid_ticket", "login_aliyunid"}
    # 文章 URL 形如 https://developer.aliyun.com/article/1740012
    ID_RE = r"/article/(\d+)"

    # ── selector（集中管理，便于改版校准；每项多个兜底，均为 Step3 校准点）──────
    # 切到 Markdown 模式的「切换按钮/标签」。主路径是 JS 找文本精确等于 'Markdown' 的
    # 可见元素（见 _ensure_markdown_mode）；下面这组是 JS 找不到时的定位器兜底。
    SEL_MODE_MARKDOWN = [          # Step3 校准
        "button:has-text('Markdown')",
        ".editor-mode-switch :text-is('Markdown')",
        "label:has-text('Markdown')",
        "a:has-text('Markdown')",
    ]
    # 切模式弹出的「内容可能丢失」确认框里的确认按钮（文本含 确定/继续/切换）。
    SEL_MODE_CONFIRM = [          # Step3 校准
        ".el-message-box button:has-text('确定')",
        ".el-dialog button:has-text('确定')",
        ".ant-modal button:has-text('确定')",
        "button:has-text('继续')",
        "button:has-text('切换')",
    ]
    SEL_TITLE = [                 # Step3 校准
        "input[placeholder*='标题']",
        ".title-input",
        "textarea[placeholder*='标题']",
        "input.article-title",
    ]
    SEL_EDITOR = [                # 阿里云正文是 markdown **textarea**（非 CodeMirror）：实测 cls=textarea、无 placeholder
        "textarea.textarea",
        ".content-box textarea",
        "textarea:not([placeholder])",
    ]
    SEL_SAVE_DRAFT = [           # 顶部「存草稿」，Step3 校准
        "button:has-text('存草稿')",
        "button:has-text('存为草稿')",
        "button:has-text('保存草稿')",
        ".save-draft",
    ]
    SEL_SUMMARY = [              # 摘要 textarea（实测 placeholder「请填写摘要」）
        "textarea[placeholder*='摘要']",
    ]
    SEL_PUBLISH_BTN = [          # 「发布文章」（实测文案；非「发布」二字）
        "button:has-text('发布文章')",
        ".publish-btn",
        "button.publish",
    ]
    SEL_MODAL_PUBLISH = [        # 点发布文章后若弹 Fusion 确认对话框，里面的确认按钮
        ".next-dialog button:has-text('确认')",
        ".next-dialog button:has-text('确定')",
        ".next-dialog button:has-text('发布')",
        ".next-overlay-inner button:has-text('确认')",
    ]

    # ── Markdown 模式：阿里云默认即 markdown textarea；「切换语雀编辑器」是切到富文本 ──
    @staticmethod
    def _markdown_textarea_present(page) -> bool:
        return bool(page.evaluate(
            "() => !!document.querySelector('textarea.textarea, .content-box textarea')"
        ))

    def _ensure_markdown_mode(self, page) -> None:
        """确保正文是 markdown textarea。**阿里云默认即 markdown**（实测：正文是 textarea.textarea，
        旁边「切换语雀编辑器」是切到富文本语雀——不是切 markdown）。故：textarea 在 → 直接用；
        不在（可能停在语雀富文本）→ 尝试点切换控件翻回 markdown；仍无 textarea 则 raise
        （护栏 A1：避免把 markdown 灌进富文本毁排版）。"""
        if self._markdown_textarea_present(page):
            return
        # 不在 markdown：尝试点「切换…编辑器 / Markdown」翻模式
        page.evaluate("""() => {
            const el = [...document.querySelectorAll('button,div,span,label,a')]
                .find(e => /切换.*编辑器|Markdown/i.test(e.textContent||'') && e.offsetParent !== null);
            if (el) el.click();
        }""")
        page.wait_for_timeout(800)
        self._click(page, self.SEL_MODE_CONFIRM, required=False)  # 可能弹「内容可能丢失」确认
        page.wait_for_timeout(800)
        if not self._markdown_textarea_present(page):
            raise RuntimeError(
                "[aliyun] 未找到 markdown 正文 textarea（textarea.textarea）。阿里云默认应是 "
                "markdown 编辑器，可能改版或停在语雀富文本。请用 scripts/syndicate/calibrate.py "
                "重新校准 SEL_EDITOR。"
            )

    @staticmethod
    def _editor_text(page) -> str:
        """读 markdown 正文 textarea 当前文本（校验正文是否灌进去了）。"""
        return str(page.evaluate(
            "() => { const t = document.querySelector('textarea.textarea, .content-box textarea');"
            " return t ? (t.value || '') : ''; }"
        ))

    # ── 摘要（阿里云当前发布表单有「摘要」项，可填 digest；尽力，失败不阻塞）──────
    def _fill_summary(self, page, article: Article) -> None:
        digest = (article.digest or "").strip()
        if not digest:
            return
        try:
            box = self._first(page, self.SEL_SUMMARY, required=False, timeout=2500)
            if box is None:
                return
            box.click()
            box.fill(digest[:200])
        except Exception as e:  # noqa: BLE001 — 摘要尽力，失败不阻塞
            print(f"   [aliyun] 摘要填写跳过（{e}）")

    def _fill_tags(self, page, tags: list[str]) -> None:
        """尽力填标签（非必需，selector 不稳；失败仅打印、不阻塞发布）。"""
        try:
            for t in tags:
                box = page.locator(
                    "input[placeholder*='标签']:visible, .tag-input input:visible, "
                    ".el-select input:visible, .ant-select-selection-search input:visible"
                ).first
                box.fill(t)
                page.wait_for_timeout(300)
                page.keyboard.press("Enter")
                page.wait_for_timeout(300)
        except Exception as e:  # noqa: BLE001 — 标签非必填，失败仅提示
            print(f"   [aliyun] 标签填写跳过（{e}）")

    # ── 发布主流程（五阶段：导航 → 切模式 → 标题 → 正文 → 草稿/发布）──────────
    def do_publish(
        self, page, article: Article, rendered: RenderedArticle, *,
        publish: bool, existing_post_id: str | None, commit: bool,
    ) -> PublishResult | None:
        # 1) 导航（新建 → editor_url；更新 → 文章编辑页；阿里云编辑页路径不确定，按惯例
        #    猜 /article/{id}/edit，跑不通时改成实际编辑页路径即可——Step3 校准）。
        target = (
            f"https://developer.aliyun.com/article/{existing_post_id}/edit"
            if existing_post_id else self.editor_url
        )
        page.goto(target, wait_until="domcontentloaded")
        if "account.aliyun.com" in page.url:
            raise RuntimeError(
                "打开编辑器被重定向到阿里云登录页，登录态可能失效，请重跑 --login"
            )
        page.wait_for_timeout(2500)  # 等编辑器挂载

        # 2) 切 Markdown 模式（核心难点，必须在灌任何内容之前；含切后无 CodeMirror 的护栏）
        self._ensure_markdown_mode(page)

        # 3) 标题（React 受控输入：真实 fill 优先，_js_set_value 走原型 setter 兜底）
        title = self._first(page, self.SEL_TITLE, required=False)
        if title is None:
            raise RuntimeError("[aliyun] 找不到标题输入框（SEL_TITLE 需校准）")
        title.click()
        title.fill(article.title)
        page.wait_for_timeout(300)
        if (title.input_value() or "").strip() != (article.title or "").strip():
            self._js_set_value(page, self.SEL_TITLE, article.title)

        # 4) 正文（markdown textarea）：真实 fill（React 安全），校验非空，空则 _js_set_value 兜底
        body = self._first(page, self.SEL_EDITOR, required=False)
        if body is None:
            raise RuntimeError("[aliyun] 找不到正文 textarea（SEL_EDITOR 需校准）")
        body.click()
        body.fill(rendered.content)
        page.wait_for_timeout(600)
        if len(self._editor_text(page).strip()) < 8:
            self._js_set_value(page, self.SEL_EDITOR, rendered.content)
            page.wait_for_timeout(600)
            if len(self._editor_text(page).strip()) < 8:
                raise RuntimeError("[aliyun] 正文注入失败（SEL_EDITOR 需校准）")

        # 5) 预演到此为止（不点发布、不写历史）
        if not commit:
            return None

        # 6a) 存草稿
        if not publish:
            self._click(page, self.SEL_SAVE_DRAFT, required=False)
            page.wait_for_timeout(2500)
            pid = self._extract_id(page.url, self.ID_RE) or (existing_post_id or "")
            return PublishResult(post_id=pid, url=page.url, state="draft")

        # 6b) 发布：阿里云当前发布表单为**内联**（实测项：标题/摘要/发布子社区/文章图片/
        #     阅读设置——已无「技术领域」必选、无必填标签，原创为默认）。填摘要 → 真实点
        #     「发布文章」（Fusion 组件，合成点击无效，须真实 click）→ 可能弹确认 → 判成功。
        self._fill_summary(page, article)
        if not self._click(page, self.SEL_PUBLISH_BTN, required=False):
            raise RuntimeError("[aliyun] 找不到「发布文章」按钮（SEL_PUBLISH_BTN 需校准）")
        page.wait_for_timeout(2500)
        # 若弹 Fusion 确认对话框（发布确认/风险提示）→ 点确认
        self._click(page, self.SEL_MODAL_PUBLISH, required=False)
        page.wait_for_timeout(1500)

        # 判成功：跳到 /article/<数字>（editor 是 /article/new，故用数字 id 正则）或出现
        # 「审核/发布成功」提示。
        def _ok() -> bool:
            if re.search(r"/article/\d+", page.url):
                return True
            return bool(page.evaluate(
                """() => [...document.querySelectorAll(
                    '.next-dialog,.next-message,[class*=message],[role=dialog],.modal')]
                    .some(e => e.offsetParent !== null &&
                        /审核|发布成功|提交成功|已发布/.test(e.textContent || ''))"""
            ))
        if not _ok():
            try:
                page.wait_for_url(re.compile(r"/article/\d+"), timeout=12000)
            except Exception:  # noqa: BLE001
                page.wait_for_timeout(2000)
        if not _ok():
            raise RuntimeError(
                "[aliyun] 点「发布文章」后未跳转 /article/<id> 也无成功提示，发布可能未完成"
                "（摘要/发布子社区等必填未满足 / selector 需校准）。当前 URL: " + page.url
            )
        pid = self._extract_id(page.url, self.ID_RE) or (existing_post_id or "")
        url = page.url if (pid and pid in page.url) else (
            f"https://developer.aliyun.com/article/{pid}" if pid else page.url
        )
        return PublishResult(post_id=pid, url=url, state="published")

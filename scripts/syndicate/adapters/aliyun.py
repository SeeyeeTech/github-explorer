"""阿里云开发者社区 adapter —— Playwright 持久化登录 + 脚本驱动发布（路线 C）。

从旧的 mode='browser'（agent 实时驱动 DOM）升级为 mode='playwright'（脚本用
Playwright 复用「一次性手动登录」的持久化会话，固定代码驱动 DOM）。一次 `--login`、
之后一条命令一键发，不再需要 Claude 盯屏幕逐步操作。设计与基类见 ../playwright_base.py。

阿里云写作页（developer.aliyun.com/article/new，2026-06 实测）：
  - 正文编辑器是 **markdown textarea**（`textarea.textarea`，左写右预览），**默认即 markdown**；
    旁边「切换语雀编辑器」是切到富文本语雀（**不是**切 markdown）。故 `_ensure_markdown_mode()`
    只需确认 textarea 在；不在（停在语雀富文本）才翻模式，仍无 textarea 则 raise（护栏 A1）。
  - 标题/摘要/正文都是 React 受控输入：标题/摘要用真实 fill/键入登记（直接赋值 React 判空）。
    **摘要为发布必填**（空则点「发布文章」静默拦下，仅闪现「请输入摘要」）。
  - 登录态是**会话 cookie（login_aliyunid_ticket）**，持久化目录默认不保存 → 靠基类
    storage_state 存取实现跨进程复用（见 playwright_base）。未登录会 302 跳 account.aliyun.com。

⚠️ **发布限制（已知）**：阿里云「发布文章」是**多步链式确认对话框**（发布文章 → 确认1 →
确认2 …），且存在一道**无任何反馈的客户端守卫**（摘要/子社区/正文都满足后，点击有时弹链式
确认、有时静默无反应、不发发布 API、不跳转、不报错），盲驱**无法稳定自动完成发布**。故本
adapter：填好标题/正文/摘要/发布子社区 → 尽力点「发布文章」+ 循环点链式「确认」；**跑不通则
优雅降级为存草稿**（state=draft），由用户到草稿箱复核后手动点「发布文章」收尾——草稿可靠。

导流到公众号：阿里云**中等偏紧**、有反「营销/导流」机制。故 name_wechat=False —— 页脚点名
账号 +「全网同名，搜一搜即达」、不出现「微信」字样，降低被判软文概率。mp_cta 仍为 True。

坑：外链图不保证自动转存，GitHub raw 图易 403，需人工复核补传（脚本不处理图片）。

⚠️ 下方 SEL_* 会随阿里云改版漂移。报「找不到元素」时用 scripts/syndicate/calibrate.py
（`--wait-login --run`）或 `playwright codegen` 校准。
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
    SEL_MODAL_PUBLISH = [        # 发布文章后弹 Fusion 确认对话框（实测含「确认」next-btn-primary）
        ".next-overlay-inner button.next-btn-primary:has-text('确认')",
        ".next-overlay-inner button:has-text('确认')",
        ".next-dialog button:has-text('确认')",
        "[role=dialog] button:has-text('确认')",
        "button.next-btn-primary:has-text('确认')",
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

    # ── 摘要（阿里云发布**必填**：空摘要点发布会被静默拦下并提示「请输入摘要」）──────
    @staticmethod
    def _derive_summary(article: Article) -> str:
        """摘要文本：优先 digest；无则从正文取首段纯文本；再不行用标题。"""
        s = (article.digest or "").strip()
        if s:
            return s[:200]
        import re as _re
        for line in (article.body_md or "").splitlines():
            line = _re.sub(r"^[#>\-\*\s`]+", "", line).strip()  # 去 markdown 标记
            if len(line) >= 12:
                return line[:200]
        return (article.title or "")[:200]

    def _fill_summary(self, page, article: Article) -> None:
        """填摘要（必填）。React 受控 textarea：用真实键入登记；失败 raise（否则发布被静默拦）。"""
        summary = self._derive_summary(article)
        box = self._first(page, self.SEL_SUMMARY, required=False, timeout=3000)
        if box is None:
            raise RuntimeError("[aliyun] 找不到摘要输入框（SEL_SUMMARY 需校准）——摘要为发布必填项")
        box.click()
        try:
            box.fill("")
        except Exception:  # noqa: BLE001
            pass
        page.keyboard.type(summary, delay=8)   # 真实键入，React 才登记
        page.wait_for_timeout(300)
        if not (box.input_value() or "").strip():
            self._js_set_value(page, self.SEL_SUMMARY, summary)  # 原型 setter 兜底

    def _select_subcommunity(self, page, article: Article) -> None:
        """选「发布子社区」（Fusion next-select）。按主题关键词匹配选项，匹配不到选第一个。尽力。"""
        try:
            it = page.locator(".next-form-item").filter(has_text="发布子社区")
            it.locator(".next-select").first.click()
            page.wait_for_timeout(1000)
            text = " ".join([article.title or "", " ".join(article.tags or [])]).lower()
            kw_map = [
                ("大数据与机器学习", ["ai", "人工智能", "机器学习", "大模型", "llm", "gpt", "数据", "agent"]),
                ("云原生", ["云原生", "k8s", "kubernetes", "docker", "容器", "serverless", "devops"]),
                ("数据库", ["数据库", "sql", "mysql", "redis", "mongo", "postgres", "db"]),
                ("弹性计算", ["计算", "服务器", "ecs", "gpu"]),
            ]
            target = next((n for n, kws in kw_map if any(k in text for k in kws)), None)
            opts = page.locator(".next-menu-item, .next-select-menu li")
            clicked = False
            if target:
                try:
                    opts.filter(has_text=target).first.click(timeout=1500)
                    clicked = True
                except Exception:  # noqa: BLE001
                    pass
            if not clicked:
                opts.first.click(timeout=2000)
            page.wait_for_timeout(500)
        except Exception as e:  # noqa: BLE001 — 子社区尽力，失败不阻塞
            print(f"   [aliyun] 发布子社区选择跳过（{e}）")

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

        # 6b) 发布：阿里云发布表单为**内联**（实测项：标题/摘要/发布子社区/文章图片/阅读设置）。
        #     摘要为必填（空则点发布静默拦并提示「请输入摘要」）。流程：填摘要 → 选发布子社区 →
        #     真实点「发布文章」（Fusion 组件，合成点击无效）。
        #     ⚠️ 已知：阿里云「发布文章」存在一道**无任何反馈的客户端守卫**（实测摘要/子社区/正文
        #     都满足后，点击仍只发埋点、不发发布 API、不跳转、不报错），盲驱难稳定触发。故发布
        #     不跳转时**优雅降级为存草稿**：保证完整带格式的草稿已存，由用户在阿里云手动点发布收尾。
        self._fill_summary(page, article)         # 必填
        self._select_subcommunity(page, article)  # 发布子社区（实测：选了才会弹发布确认框）
        page.wait_for_timeout(500)
        self._click(page, self.SEL_PUBLISH_BTN, required=False)  # 真实点「发布文章」
        # 阿里云发布是**链式确认**（发布文章 → 确认框1 → 确认框2 …）；循环点最顶层对话框的
        # 「确认」直到对话框清空或跳转到文章页。
        for _ in range(5):
            page.wait_for_timeout(1200)
            if re.search(r"/article/\d+", page.url):
                break
            clicked = bool(page.evaluate(
                """() => {
                    const ov = [...document.querySelectorAll('.next-overlay-inner')]
                        .filter(e => e.offsetParent !== null);
                    const top = ov[ov.length - 1];
                    if (!top) return false;
                    const b = [...top.querySelectorAll('button')].find(
                        e => /确认|确定/.test(e.textContent || '') && e.offsetParent !== null);
                    if (b) { b.click(); return true; }
                    return false;
                }"""
            ))
            if not clicked:
                break
        page.wait_for_timeout(1500)

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
                page.wait_for_url(re.compile(r"/article/\d+"), timeout=10000)
            except Exception:  # noqa: BLE001
                page.wait_for_timeout(1500)
        if not _ok():
            # 优雅降级：发布未跑通（阿里云多步链式确认/无反馈守卫）→ 存草稿兜底，保证内容不丢。
            # 先关掉残留确认对话框（其 backdrop 会拦后续点击），再尽力存草稿，**绝不崩**。
            for _ in range(4):
                page.keyboard.press("Escape")
                page.wait_for_timeout(300)
            try:
                self._click(page, self.SEL_SAVE_DRAFT, required=False)
                page.wait_for_timeout(2000)
            except Exception:  # noqa: BLE001 — 残留 backdrop 可能仍拦截，存草稿失败也不崩
                pass
            print("   ⚠️ [aliyun] 「发布文章」未自动跑通（阿里云为多步链式确认 + 无反馈客户端守卫）；"
                  "已尽力存草稿，请到 developer.aliyun.com 草稿箱复核并手动点「发布文章」收尾。")
            return PublishResult(post_id=existing_post_id or "", url=page.url, state="draft")
        pid = self._extract_id(page.url, self.ID_RE) or (existing_post_id or "")
        url = page.url if (pid and pid in page.url) else (
            f"https://developer.aliyun.com/article/{pid}" if pid else page.url
        )
        return PublishResult(post_id=pid, url=url, state="published")

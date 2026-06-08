"""SegmentFault 思否 adapter —— Playwright 持久化登录 + 脚本驱动发布（路线 C）。

从旧的 mode='browser'（agent 实时驱动 DOM）升级为 mode='playwright'。一次 `--login`、
之后一条命令一键发。设计与基类见 ../playwright_base.py。

⚠️ 思否 /write 已改版（2026-06 实测）：是**单页内联布局**（非「点发布弹窗再填」）——
左侧 markdown 编辑器（CodeMirror），右侧/下方是标签 +「提交」按钮：
  - 标题：input（placeholder「请输入标题」）
  - 正文：.CodeMirror（markdown 原生，左写右预览）
  - 标签：「+ 添加标签」按钮（Bootstrap dropdown-toggle）点开后搜选——**必填且只能从
    思否已有标签库选**，不能任意新建
  - 发布：「提交」按钮（btn btn-primary）；旁边「舍弃草稿」别点
发布流程：填标题 → 灌正文 → 加标签（必填）→ 点「提交」→（可能有「不欢迎软文」确认）。

登录态判定（重要）：思否登录态在**服务端 session**、**无独立登录 cookie**（PHPSESSID
登录前后都在、名字不变）。故 is_logged_in 不走基类的 cookie 判定，改用「当前页是否已
离开登录/认证页」+ do_publish 里「编辑器是否渲染」双保险。

导流：思否「写文章引导页」明确「不欢迎软文/推广/洗稿/引流」。故 name_wechat=False ——
页脚保留账号名 +「全网同名，搜一搜即达」、不点名「微信」，别放二维码、别开头硬广。

坑：① 标签必填且只能命中思否已有库（_select_required_tags 全不命中则 raise，不静默跳过）；
② 外链图防盗链不自动转存，裂图需人工复检补传；③ 发布前/后可能弹「不欢迎软文」确认。

⚠️ selector 会随思否改版漂移，下方 SEL_* 为实测 + 多兜底。报「找不到元素」时用
`playwright codegen https://segmentfault.com/write` 或本目录 calibrate.py 校准。
"""
from __future__ import annotations

from ..base import Article, PublishResult, RenderedArticle, register
from ..playwright_base import PlaywrightAdapter


@register
class SegmentFaultAdapter(PlaywrightAdapter):
    name = "segmentfault"
    editor_url = "https://segmentfault.com/write"
    login_url = "https://segmentfault.com/user/login"
    content_format = "markdown"   # markdown 原生，整篇直接灌
    mp_cta = True
    name_wechat = False           # 引导页「不欢迎引流」：页脚留账号名、不点名微信

    # ── selector（实测 + 多兜底；Step3 校准）──────────────────────────────
    SEL_TITLE = [                 # 标题：placeholder「请输入标题」的 form-control
        "input[placeholder*='标题']",
        "input[name='title']",
        ".title input",
        "input.form-control[placeholder*='标题']",
    ]
    SEL_EDITOR = [                # markdown CodeMirror 编辑区（实测 .CodeMirror）
        ".CodeMirror",
        ".CodeMirror textarea",
        ".cm-content",
        "textarea.markdown-editor",
    ]
    SEL_TAG_TOGGLE = [           # 「+ 添加标签」按钮（Bootstrap dropdown-toggle）
        "button:has-text('添加标签')",
        ".tag-wrap button:has-text('添加标签')",
        "button.dropdown-toggle:has-text('标签')",
    ]
    SEL_TAG_INPUT = [           # 点开标签后出现的搜索输入框（排除标题/站内搜索框）
        ".dropdown-menu.show input",
        ".dropdown-menu input[type='text']",
        ".tag-wrap input[type='text']",
        "input[placeholder*='标签']",
        "input[placeholder*='搜索']",
    ]
    SEL_TAG_OPTION = [          # 标签搜索的候选项（点选才算命中思否库）
        ".dropdown-menu.show .dropdown-item",
        ".dropdown-menu.show li",
        ".dropdown-menu.show a",
        ".tag-wrap .dropdown-item",
        ".search-result li",
    ]
    SEL_PUBLISH_BTN = [          # 「提交」按钮（btn btn-primary）= 发布
        "button.btn-primary:has-text('提交')",
        "button:has-text('提交')",
        ".btn-primary:has-text('提交')",
    ]
    SEL_SOFTAD_CONFIRM = [      # 「不欢迎软文」确认页 / 弹窗放行按钮
        ".modal.show button.btn-primary",
        "button:has-text('确认发布')",
        "button:has-text('继续发布')",
        "button:has-text('我已知晓')",
        ".modal button:has-text('确定')",
    ]
    # 编辑器/登录态判据：write 页登录后才渲染 .CodeMirror 或「提交」按钮
    LOGIN_COOKIES = {"PHPSESSID"}   # 占位（满足基类非空校验）；is_logged_in 已覆盖、不用它
    ID_RE = r"/a/(\d+)"          # 文章 URL 形如 segmentfault.com/a/1190000047828319

    # ── 登录态：URL 判定（不导航，避免打断 --login 轮询）──────────────────────
    def is_logged_in(self, context) -> bool:
        """思否登录态在服务端 session、无独立 cookie。用「当前页是否已离开登录/认证页」判定：
        --login 停在登录页→False，登录后站点重定向离开→True；发布路径起始为 about:blank
        （非登录页）→True，真正登录有效性由 do_publish 里「编辑器是否渲染」兜底把关。"""
        try:
            page = context.pages[0] if context.pages else None
            url = page.url if page else ""
        except Exception:  # noqa: BLE001
            return False
        if not url or url == "about:blank":
            # 发布路径起始态：放行，交给 do_publish 的编辑器渲染检查
            return True
        return not any(s in url for s in ("/user/login", "passport.", "/login", "/auth"))

    # ── 必填标签：点「+ 添加标签」→ 搜 → 点选已有库项 ───────────────────────
    def _select_required_tags(self, page, candidates: list[str]) -> int:
        """逐个候选搜选思否已有标签（命中库才算数）；返回成功数，最多 4 个。
        思否标签不能任意新建——输入库里没有的词不会出现可点候选。"""
        selected = 0
        seen: set[str] = set()
        for raw in candidates:
            if selected >= 4:
                break
            name = (raw or "").strip()
            if not name or name.lower() in seen:
                continue
            seen.add(name.lower())

            # 每次都重新点开「+ 添加标签」（选完一个下拉可能收起）
            if not self._click(page, self.SEL_TAG_TOGGLE, required=False):
                if not self._js_click_button_text(page, "添加标签"):
                    break  # 连标签入口都没有 → 交给上层（selected=0 → raise）
            page.wait_for_timeout(800)

            box = self._first(page, self.SEL_TAG_INPUT, required=False, timeout=3000)
            if box is None:
                continue
            try:
                box.click()
                box.fill("")
                box.type(name, delay=60)
            except Exception:  # noqa: BLE001
                continue
            page.wait_for_timeout(900)  # 等异步下拉

            option = None
            for sel in self.SEL_TAG_OPTION:
                loc = page.locator(sel).first
                try:
                    loc.wait_for(state="visible", timeout=2500)
                    option = loc
                    break
                except Exception:  # noqa: BLE001
                    continue
            if option is None:
                continue  # 该词不在思否标签库
            try:
                option.click()
                selected += 1
                page.wait_for_timeout(400)
            except Exception:  # noqa: BLE001
                continue
        return selected

    # ── 入场拦路 modal（写作引导/草稿恢复/软文提示）：进 /write 后挡住编辑器，先关掉 ──
    def _dismiss_blocking_modal(self, page) -> None:
        """进 /write 可能弹 modal（role=dialog.modal.show）挡住编辑器、拦截点击。
        策略：先打印按钮（便于校准）→ Escape → 关闭(X) → 兜底点非危险主按钮。"""
        for _ in range(3):
            modal = page.locator(".modal.show, div[role='dialog'][aria-modal='true']").first
            try:
                modal.wait_for(state="visible", timeout=1500)
            except Exception:  # noqa: BLE001
                return  # 无拦路 modal
            try:
                btns = page.evaluate(
                    """() => [...document.querySelectorAll(
                        ".modal.show button, div[role='dialog'][aria-modal='true'] button")]
                        .filter(e => e.offsetParent !== null)
                        .map(e => (e.textContent || '').trim()).filter(Boolean)"""
                )
                print(f"   [segmentfault] 入场 modal 按钮: {btns}")
            except Exception:  # noqa: BLE001
                btns = []
            # ① Escape（多数 Bootstrap modal 可关）
            page.keyboard.press("Escape")
            page.wait_for_timeout(500)
            if not self._modal_open(page):
                return
            # ② 关闭按钮（X）
            for sel in (".modal.show .btn-close", ".modal.show button[aria-label='Close']",
                        ".modal.show .close"):
                if self._click(page, [sel], required=False):
                    page.wait_for_timeout(500)
                    break
            if not self._modal_open(page):
                return
            # ③ 兜底：点「我知道了/知道了/开始/继续/确定」这类非危险确认按钮
            for txt in ("我知道了", "知道了", "我已知晓", "开始写作", "继续", "确定", "好的"):
                if self._js_click_button_text(page, txt):
                    page.wait_for_timeout(500)
                    break
            else:
                return  # 实在关不掉就放手（让后续灌入报错给出线索）

    @staticmethod
    def _modal_open(page) -> bool:
        return bool(page.evaluate(
            "() => { const m = document.querySelector("
            "\".modal.show, div[role='dialog'][aria-modal='true']\");"
            " return !!(m && m.offsetParent !== null); }"
        ))

    # ── 「不欢迎软文」确认（尽力点掉，不点会卡住发布）──────────────────────
    def _confirm_softad(self, page) -> bool:
        for sel in self.SEL_SOFTAD_CONFIRM:
            loc = page.locator(sel).first
            try:
                loc.wait_for(state="visible", timeout=1500)
                loc.click()
                page.wait_for_timeout(500)
                return True
            except Exception:  # noqa: BLE001
                continue
        return False

    @staticmethod
    def _editor_has_content(page) -> bool:
        return bool(page.evaluate(
            """() => {
                const cm = document.querySelector('.CodeMirror');
                if (cm && cm.CodeMirror) return (cm.CodeMirror.getValue() || '').trim().length > 0;
                const ta = document.querySelector('.CodeMirror textarea, textarea.markdown-editor');
                if (ta) return (ta.value || '').trim().length > 0;
                const cc = document.querySelector('.cm-content');
                if (cc) return (cc.textContent || '').trim().length > 0;
                return false;
            }"""
        ))

    @staticmethod
    def _editor_present(page) -> bool:
        # 只认真实 markdown 编辑器（思否反 headless：无头/未登录时不渲染 .CodeMirror）。
        # 注意：发布须有头跑（默认 SYNDICATE_PW_HEADLESS 未设 = 有头）。
        return bool(page.evaluate(
            "() => !!document.querySelector('.CodeMirror, .cm-content')"
        ))

    # ── 发布主流程（五阶段，签名照基类）──────────────────────────────────
    def do_publish(
        self, page, article: Article, rendered: RenderedArticle, *,
        publish: bool, existing_post_id: str | None, commit: bool,
    ) -> PublishResult | None:
        # 1) 导航：新建去写作页；更新去文章编辑页
        target = (
            f"https://segmentfault.com/a/{existing_post_id}/edit"
            if existing_post_id else self.editor_url
        )
        page.goto(target, wait_until="domcontentloaded")
        # 首进新建可能被 /howtowrite 拦并跳 /write?freshman=1（正常）。
        if any(s in page.url for s in ("/user/login", "/auth", "passport.")):
            raise RuntimeError(
                "[segmentfault] 打开编辑器被重定向到登录页，登录态已失效，请重跑 --login"
            )
        # 等编辑器渲染——思否 write 页只有登录后才渲染编辑器/提交按钮（登录态双保险）
        ok = False
        for _ in range(15):
            page.wait_for_timeout(1000)
            if self._editor_present(page):
                ok = True
                break
        if not ok:
            raise RuntimeError(
                "[segmentfault] 编辑器未渲染（多半未登录或登录态失效，思否登录态在服务端 "
                "session）。请重跑：python3 scripts/syndicate_publish.py --channel segmentfault --login"
            )
        # 进 /write 常弹写作引导/草稿恢复 modal，挡住编辑器，先关掉
        self._dismiss_blocking_modal(page)

        # 2) 标题（思否标题是 React 受控输入：必须真实 fill 让 React 收到变更，否则
        #    DOM 有值但 React 仍判为空 → 必填校验不过、「提交」按钮一直禁用）
        title = self._first(page, self.SEL_TITLE, required=False)
        if title is None:
            raise RuntimeError("[segmentfault] 找不到标题输入框（需校准 SEL_TITLE）")
        title.click()
        title.fill(article.title)
        page.wait_for_timeout(300)
        if (title.input_value() or "").strip() != (article.title or "").strip():
            self._js_set_value(page, self.SEL_TITLE, article.title)

        # 3) 正文：聚焦 CodeMirror 一次性灌入；校验非空，空则合成 paste 兜底
        self._focus_insert(page, self.SEL_EDITOR, rendered.content)
        page.wait_for_timeout(600)
        if not self._editor_has_content(page):
            state = self._paste_text(page, self.SEL_EDITOR, rendered.content)
            page.wait_for_timeout(600)
            if state == "no-editor" or not self._editor_has_content(page):
                raise RuntimeError("[segmentfault] 正文灌入失败（需校准 SEL_EDITOR）")

        # 4) 预演到此为止
        if not commit:
            return None

        # 5a) 存草稿：思否自动存草稿（编辑区有「舍弃草稿」），无独立「保存草稿」按钮。
        if not publish:
            page.wait_for_timeout(2500)  # 给自动存草稿留时间
            pid = self._extract_id(page.url, self.ID_RE) or (existing_post_id or "")
            return PublishResult(post_id=pid, url=page.url, state="draft")

        # 5b) 发布（思否单页内联：先填必填标签 → 点「提交」→ 软文确认）
        candidates = list(article.tags) + ["github", "开源", "人工智能", "后端"]
        selected = self._select_required_tags(page, candidates)
        if selected == 0:
            raise RuntimeError(
                "[segmentfault] 标签必填且须命中思否已有标签库，候选无一命中，发布中止"
                "（检查 SEL_TAG_TOGGLE / SEL_TAG_INPUT / SEL_TAG_OPTION 是否需校准）"
            )

        # 收起可能仍开着的标签下拉（否则挡住「提交」按钮、点击被拦截），再点「提交」。
        page.keyboard.press("Escape")
        page.wait_for_timeout(500)
        # 思否「提交」是 React 组件，合成 JS .click() 不触发其 handler——必须真实点击。
        clicked = False
        loc = self._first(page, self.SEL_PUBLISH_BTN, required=False, timeout=5000)
        if loc is not None:
            try:
                loc.click(timeout=6000)
                clicked = True
            except Exception:  # noqa: BLE001 — 被拦截则再 Escape 一次后强制点
                page.keyboard.press("Escape")
                page.wait_for_timeout(400)
                try:
                    loc.click(timeout=6000, force=True)
                    clicked = True
                except Exception:  # noqa: BLE001
                    clicked = False
        if not clicked and not self._js_click_button_text(page, "提交", cls_contains="btn-primary"):
            raise RuntimeError("[segmentfault] 点不动「提交」按钮（需校准 SEL_PUBLISH_BTN）")
        page.wait_for_timeout(2500)

        # 思否新文提交后进「审核中」：弹提示 modal（「你的博客文章正在审核中…」），
        # **不跳转 /a/**。识别这个成功提示即视为发布成功；也兼容直接跳 /a/ 的情况。
        reviewing = self._submit_succeeded(page)
        on_article = "/a/" in page.url
        if not (reviewing or on_article):
            # 也许还有一道确认按钮（软文/二次确认），点掉再判一次
            self._confirm_softad(page)
            page.wait_for_timeout(1800)
            reviewing = self._submit_succeeded(page)
            on_article = "/a/" in page.url
        if not (reviewing or on_article):
            raise RuntimeError(
                "[segmentfault] 点「提交」后既无『审核中/提交成功』提示、也未跳转 /a/，"
                "发布可能未完成（被校验拦下 / 选择器需校准）。当前 URL: " + page.url
            )
        # 关掉「审核中」提示框
        self._js_click_button_text(page, "确定")
        page.wait_for_timeout(800)

        pid = self._extract_id(page.url, self.ID_RE) or (existing_post_id or "")
        url = page.url if "/a/" in page.url else (
            f"https://segmentfault.com/a/{pid}" if pid else page.url
        )
        # 注：新文进审核队列、未必立刻有公开 /a/<id>；post_id 可能为空（幂等更新会受限，
        # 审核通过后可在「我的文章」拿到 id 再回填）。state 记 published（已提交）。
        return PublishResult(post_id=pid, url=url, state="published")

    @staticmethod
    def _submit_succeeded(page) -> bool:
        """提交后是否出现「审核中 / 提交成功 / 发布成功」提示（思否新文进审核队列的成功标志）。"""
        return bool(page.evaluate(
            """() => [...document.querySelectorAll('.modal, [role=dialog], [class*=modal]')]
                .some(e => e.offsetParent !== null &&
                    /审核|发布成功|提交成功|正在审核|等待/.test(e.textContent || ''))"""
        ))

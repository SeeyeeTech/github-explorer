"""掘金 (juejin.cn) adapter —— Playwright 持久化登录 + 脚本驱动发布（路线 C）。

从旧的 mode='browser'（agent 实时驱动 DOM + playbook）升级为 mode='playwright'
（脚本用 Playwright 复用「一次性手动登录」的持久化会话，固定代码驱动 DOM）。一次
`--login`、之后一条命令一键发，不再需要 Claude 盯屏幕逐步操作。设计与基类见
../playwright_base.py，标准样板见 ./csdn.py。

掘金编辑器：juejin.cn/editor/drafts/new，markdown 原生（CodeMirror），需登录态。
发布流程：写正文 → 填标题 → 点右上「发布」打开发布抽屉 → 选「分类」(必选单选) +
搜选「标签」2-5 个 +（可选）封面/简介 → 点「确定并发布」→ 跳到 juejin.cn/post/<id>。
存草稿：掘金自动存（编辑页 URL 即 /editor/drafts/<draft_id>），亦可点显式「存草稿」。

导流到公众号：mp_cta / name_wechat 走默认（True/True）——框架渲染已在文末追加软导流
页脚（「全网同名，微信搜一搜即达」，WECHAT_MP_NAME 控制），合规且足够。掘金对正文
硬导流敏感、正文禁二维码，故只靠框架软页脚、不在代码里另插 CTA。

坑：
  - 外链图防盗链：掘金检测到正文含外链图片会弹 toast 提示「上传到掘金图床」。尽力点
    其「上传」按钮把外链图转存（避免防盗链/失效），但**非阻塞**——点不到只 print。
  - 幂等编辑（风险 J1）：存的 existing_post_id 是**文章 id**（形如 7648…），但掘金
    编辑走的是**草稿 id**（juejin.cn/editor/drafts/<draft_id>），二者不同、无法由
    文章 id 直接拼出草稿 URL。故编辑时先打开文章详情页 juejin.cn/post/<id>，点页面
    「编辑」按钮进入真实草稿编辑页（此时 URL 才变成正确的 draft 地址）；若点不到
    「编辑」按钮则**降级为新建**（会产生重复文章，print 警告并建议显式 --force-new）。
  - selector 漂移：掘金改版较勤，下方 SEL_* 均为多兜底猜测。首次跑通后若报「找不到
    元素」，用 `playwright codegen https://juejin.cn/editor/drafts/new` 录制真实
    selector（分类/标签抽屉尤其需要校准）后更新对应常量即可。
"""
from __future__ import annotations

from ..base import Article, PublishResult, RenderedArticle, register
from ..playwright_base import PlaywrightAdapter


@register
class JuejinAdapter(PlaywrightAdapter):
    name = "juejin"
    editor_url = "https://juejin.cn/editor/drafts/new"
    login_url = "https://juejin.cn/login"
    content_format = "markdown"
    # mp_cta / name_wechat 用基类默认 True/True（软导流页脚由框架追加）。

    # ── selector（集中管理，便于改版校准；每项多个兜底）────────────────────
    # ⚠️ 全部为离线猜测。Step3 用 `playwright codegen https://juejin.cn/editor/drafts/new`
    #    或 DevTools 校准真实 DOM 后回填。
    SEL_TITLE = [                     # 标题：input.title-input（实测，placeholder「输入文章标题...」）
        "input.title-input",
        "input[placeholder*='标题']",
        ".title-input",
        "textarea[placeholder*='标题']",
    ]
    SEL_EDITOR = [                    # 正文：CodeMirror markdown 编辑区（实测 .CodeMirror 命中）
        ".CodeMirror",
        ".CodeMirror textarea",
        ".bytemd-editor .CodeMirror",
        ".cm-content",               # CM6 兜底
    ]
    SEL_PUBLISH_BTN = [              # 右上「发布」打开抽屉。注意「确定并发布」也含「发布」二字，
                                    # 故触发按钮用 .xitu-btn 精确区分（实测顶栏发布按钮类 = xitu-btn）。
        ".xitu-btn:text-is('发布')",
        "button:text-is('发布')",
        ".publish-popup-box button:has-text('发布')",
    ]
    SEL_MODAL_PUBLISH = [           # 抽屉内最终「确定并发布」（实测类 ui-btn btn primary）
        "button:has-text('确定并发布')",
        ".ui-btn.primary:has-text('确定并发布')",
        ".publish-popup button:has-text('确定并发布')",
    ]
    SEL_SAVE_DRAFT = [              # 顶部「存草稿」（掘金多为自动存草稿，此为显式兜底）
        "button:has-text('存草稿')",
        "button:has-text('保存草稿')",
        ".save-draft",
    ]
    SEL_EDIT_BTN = [               # 文章详情页右上「编辑」（进真实草稿编辑页，见风险 J1）
        "a:has-text('编辑')",
        "button:has-text('编辑')",
        ".edit-btn",
        "a[href*='editor/drafts']",
    ]
    SEL_IMG_UPLOAD = [            # 「检测到外链图片，上传到掘金图床」toast 的「上传」按钮
        "button:has-text('上传')",
        ".byte-btn:has-text('上传')",
        ".upload-img-btn",
        ".message button:has-text('上传')",
    ]
    SEL_TAG_INPUT = [            # 抽屉里标签搜索框（实测：.tag-input 内 byte-select 输入框；
                                # 页面有两个 .tag-input——标签 + 话题，标签在前，.first 即标签）
        ".tag-input .byte-select__input",
        ".tag-input input",
        "input[placeholder*='搜索标签']",
        "input[placeholder*='标签']",
    ]
    SEL_TAG_OPTION = [          # 标签搜索下拉的候选项（实测 byte-select 下拉项）
        ".byte-select-option",
        ".byte-select__option",
        ".tag-list-item",
        ".suggestion-list .item",
    ]
    SEL_CATEGORY_OPTION = [    # 分类单选项（实测：容器 .category-list，项为其内精确文本元素；
                              # 用 {text} 占位拼具体分类，见 _click_category_option）
        ".category-list :text-is('{text}')",
        ".category-list label:has-text('{text}')",
        ".category-list-item:has-text('{text}')",
        ".byte-radio:has-text('{text}')",
    ]

    # 掘金/字节系登录后写入的 cookie（任一存在即视为已登录）；is_logged_in 走基类默认。
    # ⚠️ 实测校准（Step3）：**不能用 passport_csrf_token**——它登出态就存在（passport 的
    #    CSRF token），会令 --login 还没登录就「假成功」。真正的登录态是字节 passport 的
    #    httpOnly 会话 cookie：sessionid / sessionid_ss / sid_guard / sid_tt / uid_tt。
    LOGIN_COOKIES = {"sessionid", "sessionid_ss", "sid_guard", "sid_tt", "uid_tt"}
    # 文章 URL 形如 https://juejin.cn/post/7648435540396064831
    ID_RE = r"/post/(\d+)"

    # 分类关键词 → 掘金分类名（用于按报告主题/标签自动匹配一个分类单选项）
    _CATEGORY_RULES = [
        ("人工智能", ["ai", "llm", "gpt", "agent", "model", "机器学习", "深度学习",
                       "神经", "人工智能", "大模型", "rag"]),
        ("前端", ["前端", "react", "vue", "css", "javascript", "typescript",
                  "web", "frontend", "node"]),
        ("后端", ["后端", "backend", "go", "rust", "java", "python", "数据库",
                  "分布式", "服务", "微服务", "中间件"]),
        ("开发工具", ["工具", "cli", "devops", "tool", "插件", "ide"]),
    ]
    _CATEGORY_FALLBACK = ["后端", "人工智能", "前端", "开发工具", "开源"]

    # ── 幂等编辑（风险 J1）──────────────────────────────────────────────
    def _open_for_edit(self, page, existing_post_id: str) -> bool:
        """编辑既有文章。existing_post_id 是**文章 id**，但掘金编辑走**草稿 id**
        （/editor/drafts/<draft_id>），无法由文章 id 直接拼草稿 URL。故先打开文章
        详情页 juejin.cn/post/<id>，点页面「编辑」进真实草稿编辑页（URL 才变成正确
        的 draft 地址）。点到并落在编辑器页返回 True；否则返回 False（调用方降级新建）。"""
        page.goto(f"https://juejin.cn/post/{existing_post_id}",
                  wait_until="domcontentloaded")
        page.wait_for_timeout(1500)
        if self._click(page, self.SEL_EDIT_BTN, required=False):
            page.wait_for_timeout(2500)
            return "editor" in page.url
        return False

    # ── 分类（必填单选）────────────────────────────────────────────────
    def _guess_categories(self, article: Article) -> list[str]:
        """按标题 + 标签匹配候选分类（按规则顺序），匹配不到回退固定兜底。"""
        text = " ".join([article.title, *article.tags]).lower()
        picks = [cat for cat, kws in self._CATEGORY_RULES if any(k in text for k in kws)]
        return picks or ["后端"]

    def _click_category_option(self, page, text: str) -> bool:
        """尝试点中文本为 text 的分类单选项（多 selector 兜底）。"""
        for tmpl in self.SEL_CATEGORY_OPTION:
            sel = tmpl.replace("{text}", text)
            loc = page.locator(sel).first
            try:
                loc.click(timeout=1500)
                return True
            except Exception:  # noqa: BLE001 — 换下一个兜底 selector
                continue
        return False

    def _select_category(self, page, article: Article) -> None:
        """在发布抽屉里选一个分类单选项（掘金**必填**）。先按报告主题匹配，匹配不到
        用固定兜底列表逐个尝试；**一个都选不到则 raise**（分类必填，否则无法发布）。"""
        for cat in self._guess_categories(article):
            if self._click_category_option(page, cat):
                page.wait_for_timeout(400)
                return
        for cat in self._CATEGORY_FALLBACK:
            if self._click_category_option(page, cat):
                page.wait_for_timeout(400)
                return
        raise RuntimeError(
            "[juejin] 发布抽屉里一个分类都没选中（分类是必填项，无法发布）。"
            "selector 可能漂移：用 `playwright codegen https://juejin.cn/editor/drafts/new` "
            "校准 SEL_CATEGORY_OPTION。"
        )

    # ── 标签（2-5 个，搜索式添加）──────────────────────────────────────
    def _fill_tags(self, page, tags: list[str]) -> None:
        """尽力在抽屉里搜选 2-5 个标签（article.tags 优先，不足用兜底补到至少 2 个）。
        掘金标签只能从已有标签库搜选，故：输入 → 等下拉 → 点首个候选项（点不到再按
        Enter 兜底）。失败仅 print 不阻塞发布。"""
        wanted = [t for t in (tags or []) if t][:5]
        for fb in ("GitHub", "开源", "AI"):
            if len(wanted) >= 2:
                break
            if fb not in wanted:
                wanted.append(fb)
        wanted = wanted[:5]
        try:
            for t in wanted:
                # 标签输入框被 .byte-select__placeholder 覆盖层拦截，直接点 input 会 intercept；
                # 先点 .tag-input 容器（第一个 = 标签，第二个是话题）聚焦，再用键盘键入。
                cont = page.locator(".tag-input").first
                try:
                    cont.click(timeout=2000)
                except Exception:  # noqa: BLE001
                    box = self._first(page, self.SEL_TAG_INPUT, required=False, timeout=2000)
                    if box is None:
                        print("   [juejin] 未找到标签搜索框，跳过标签填写")
                        return
                    box.click(force=True)
                page.wait_for_timeout(300)
                page.keyboard.type(t, delay=40)
                page.wait_for_timeout(900)  # 等候补下拉
                if not self._click(page, self.SEL_TAG_OPTION, required=False):
                    page.keyboard.press("Enter")  # 下拉点不到时兜底
                page.wait_for_timeout(500)
        except Exception as e:  # noqa: BLE001 — 标签尽力而为，失败不阻塞
            print(f"   [juejin] 标签填写跳过（{e}）")

    # ── 正文注入校验 ────────────────────────────────────────────────────
    @staticmethod
    def _editor_len(page) -> int:
        """读 CodeMirror 当前内容长度（校验正文是否真的注入成功）。取不到返回 0。"""
        try:
            return int(page.evaluate(
                """() => {
                    const cm = document.querySelector('.CodeMirror');
                    if (cm && cm.CodeMirror) return cm.CodeMirror.getValue().length;
                    const c = document.querySelector('.cm-content, .CodeMirror-code');
                    return c ? (c.innerText || '').length : 0;
                }"""
            ))
        except Exception:  # noqa: BLE001
            return 0

    def _maybe_upload_images(self, page) -> None:
        """尽力点「检测到外链图片，上传到掘金图床」toast 的「上传」按钮（非阻塞）。"""
        try:
            page.wait_for_timeout(800)
            if self._click(page, self.SEL_IMG_UPLOAD, required=False):
                print("   [juejin] 已触发外链图片转存掘金图床")
                page.wait_for_timeout(2000)
        except Exception as e:  # noqa: BLE001 — 图床转存非必须
            print(f"   [juejin] 外链图上传跳过（{e}）")

    # ── 主流程：五阶段 ──────────────────────────────────────────────────
    def do_publish(
        self, page, article: Article, rendered: RenderedArticle, *,
        publish: bool, existing_post_id: str | None, commit: bool,
    ) -> PublishResult | None:
        # 1) 导航（新建 / 幂等编辑见风险 J1）
        if existing_post_id:
            if not self._open_for_edit(page, existing_post_id):
                print(
                    f"   [juejin] 文章 {existing_post_id} 详情页未找到「编辑」按钮，"
                    "降级为新建（可能产生重复文章，建议显式用 --force-new 新建）"
                )
                page.goto(self.editor_url, wait_until="domcontentloaded")
        else:
            page.goto(self.editor_url, wait_until="domcontentloaded")

        # 导航后若被重定向到登录页 / 登录态失效 → 提示重跑 --login
        if "juejin.cn/login" in page.url or not self.is_logged_in(page.context):
            raise RuntimeError(
                "[juejin] 打开编辑器被重定向到登录页或登录态已失效（cookie 缺失/过期）。"
                "先跑：python3 scripts/syndicate_publish.py --channel juejin --login"
            )
        # 等编辑器挂载
        self._first(page, self.SEL_EDITOR, timeout=25000)
        page.wait_for_timeout(1000)

        # 2) 标题（独立 input/textarea）
        title_box = self._first(page, self.SEL_TITLE, required=False, timeout=8000)
        if title_box is not None:
            title_box.fill(article.title)
        elif not self._js_set_value(page, self.SEL_TITLE, article.title):
            raise RuntimeError(
                "[juejin] 找不到标题输入框（编辑器或已改版，校准 SEL_TITLE）"
            )

        # 3) 正文（CodeMirror）：聚焦 + insert_text；注入失败回退合成 paste
        self._focus_insert(page, self.SEL_EDITOR, rendered.content)
        page.wait_for_timeout(800)
        if self._editor_len(page) < 10:
            print("   [juejin] insert_text 注入疑似为空，回退合成 paste")
            self._paste_text(page, self.SEL_EDITOR, rendered.content)
            page.wait_for_timeout(800)
        # 外链图防盗链：尽力转存掘金图床（非阻塞）
        self._maybe_upload_images(page)

        # 4) 预演到此为止（不点发布、不写历史）
        if not commit:
            return None

        # 5a) 存草稿（掘金自动存；尽力点显式「存草稿」）
        if not publish:
            self._click(page, self.SEL_SAVE_DRAFT, required=False)
            page.wait_for_timeout(2500)
            pid = self._extract_id(page.url, r"drafts/(\d+)") or (existing_post_id or "")
            return PublishResult(post_id=pid, url=page.url, state="draft")

        # 5b) 发布：开抽屉 → 选分类(必填) → 填标签(尽力) → 确定并发布
        if not self._click(page, self.SEL_PUBLISH_BTN, required=False):
            raise RuntimeError(
                "[juejin] 找不到右上「发布」按钮（校准 SEL_PUBLISH_BTN）"
            )
        page.wait_for_timeout(1500)
        self._select_category(page, article)
        self._fill_tags(page, list(article.tags))
        if not self._click(page, self.SEL_MODAL_PUBLISH, required=False):
            raise RuntimeError(
                "[juejin] 找不到抽屉里「确定并发布」按钮（抽屉未弹出或已改版，"
                "校准 SEL_MODAL_PUBLISH）"
            )
        # 发布成功后掘金会跳 /post/<id>（直达）或 /published（已发布列表落地页）——两者都算成功
        # （实测 article/publish API 返回 200 后即跳 /published）。两者都没等到才算失败。
        try:
            page.wait_for_url(lambda u: "/post/" in u or "/published" in u, timeout=15000)
        except Exception:  # noqa: BLE001
            page.wait_for_timeout(3000)
        if "/post/" not in page.url and "/published" not in page.url:
            raise RuntimeError(
                "[juejin] 点「确定并发布」后未跳转 /post/ 或 /published，发布可能未完成"
                "（分类/标签等必填未满足 / selector 需校准）。当前 URL: " + page.url
            )
        pid = self._extract_id(page.url, self.ID_RE)
        url = page.url
        if not pid:                      # 跳 /published 时 URL 无 id → 去已发布列表取最新一篇兜底
            latest = self._latest_published(page)
            if latest:
                pid, url = latest
        if not pid:
            pid = existing_post_id or ""
        return PublishResult(post_id=pid, url=url, state="published")

    @staticmethod
    def _latest_published(page) -> tuple[str, str] | None:
        """去掘金「已发布」列表取最新一篇 (id, url)。发布后跳 /published（URL 无 id）时兜底。"""
        import re
        for u in ("https://juejin.cn/creator/content/article/published",
                  "https://juejin.cn/published"):
            try:
                page.goto(u, wait_until="domcontentloaded")
                page.wait_for_timeout(3500)
                hrefs = page.eval_on_selector_all(
                    "a[href*='/post/']", "els=>els.map(e=>e.href)")
            except Exception:  # noqa: BLE001
                continue
            for h in hrefs:
                m = re.search(r"/post/(\d+)", h or "")
                if m:
                    return m.group(1), h
        return None

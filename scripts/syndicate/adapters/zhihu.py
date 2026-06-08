"""知乎专栏 adapter —— Playwright 持久化登录 + 脚本驱动发布（路线 C）。

从旧的 mode='browser'（agent 实时驱动 DOM）升级为 mode='playwright'（脚本用
Playwright 复用「一次性手动登录」的持久化会话，固定代码驱动 DOM）。一次 `--login`、
之后一条命令一键发，不再需要 Claude 盯屏幕逐步操作。设计与基类见 ../playwright_base.py。

知乎专栏编辑器是**富文本 contenteditable（WYSIWYG，基于 Draft.js）**，**不是 markdown
原生**：直接灌 markdown 纯文本只会原样保留 `#` ``` `|` 等字面符号、不渲染。所以本
adapter content_format='html'，`rendered.content` 是**已渲染 HTML**，注入时让编辑器拿到
**富文本剪贴板**（而非把 HTML 源码当纯文本贴进去）。

富文本注入两路兜底（核心难点）：
  - 主路径 `_paste_html`：在编辑器上 dispatch 一个合成 paste ClipboardEvent，DataTransfer
    带 text/html，知乎自研 paste handler 会把 h1-h6/p/ul/ol/blockquote/pre>code/img/table
    映射进富文本模型。但**合成 ClipboardEvent 的 isTrusted=false**，少数编辑器（含某些
    版本的知乎/Draft.js）会因此忽略——所以注入后必须校验是否真的生效。
  - 兜底 `_clipboard_paste`：真实剪贴板（navigator.clipboard.write 写 text/html）+ 聚焦
    编辑器后**真按 Ctrl/Cmd+V**，走浏览器可信路径（isTrusted=true）。需 headed + 页面聚焦。
  两路都失败则 raise（绝不发空/糊文）——多半是 paste handler 校验 isTrusted 或编辑器
  selector 漂移，需 headed 复跑或用 codegen 校准 SEL_EDITOR。

导流：知乎是站外导流最敏感的平台，正文出现任何「关注公众号/二维码」都易触发限流降权
（比 CSDN 的硬关键词拒发更隐蔽也更狠）。故 mp_cta=False —— 正文页脚**完全不放公众号
CTA**，只留 canonical 回链，引流交给个人资料/简介低调处理。

坑：① 表格弱（不支持合并/调列宽），复杂表格降级为截图；② 公式 KaTeX 在「编辑器内输入」
可渲染，但 HTML 粘贴的 LaTeX 常不自动渲染，需手动补；③ 外链图（GitHub）常因防盗链转存
失败/裂图——应先下载再走编辑器「插入图片」上传到 zhimg 图床。

⚠️ selector 会随知乎改版漂移。首次跑通后若报「找不到元素」，用
`playwright codegen https://zhuanlan.zhihu.com/write` 录制真实 selector 更新下方常量即可。
"""
from __future__ import annotations

from ..base import Article, PublishResult, RenderedArticle, register
from ..playwright_base import PlaywrightAdapter


@register
class ZhihuAdapter(PlaywrightAdapter):
    name = "zhihu"
    editor_url = "https://zhuanlan.zhihu.com/write"
    login_url = "https://www.zhihu.com/signin"
    content_format = "html"   # 富文本 contenteditable，走 HTML 富文本粘贴
    mp_cta = False            # 知乎对站外导流最敏感：正文不放任何公众号 CTA

    # ── selector（集中管理，便于改版校准；每项多个兜底）────────────────────
    # ⚠️ 以下均为合理猜测，Step3 务必用 codegen/DevTools 校准真实 selector。
    SEL_TITLE = [             # 知乎标题是 textarea/contenteditable
        "textarea[placeholder*='标题']",
        ".WriteIndex-titleInput textarea",
        ".Input[placeholder*='标题']",
        "textarea.Input",
    ]
    SEL_EDITOR = [            # Draft.js 富文本正文区（contenteditable）
        ".public-DraftEditor-content",
        ".Editable-content",
        ".DraftEditor-root [contenteditable='true']",
        "div[contenteditable='true']",
    ]
    # 知乎发布是**内联**（编辑页顶部即有「添加话题」「发布」），非独立面板。实测：
    # 点「添加话题」→ 出搜索框 → 输入 → 下拉候选(.css-gfrh4c) 点选；再真实点「发布」。
    SEL_PUBLISH_BTN = [       # 编辑页右上「发布」（实测 class Button css-d0uhtl…，文本恰为「发布」）
        "button.Button:has-text('发布')",
        "button:has-text('发布')",
    ]
    SEL_TOPIC_TOGGLE = [      # 「添加话题」按钮（点开话题搜索）
        "button:has-text('添加话题')",
    ]
    SEL_TOPIC_INPUT = [       # 话题搜索输入框（点添加话题后出现）
        "input[placeholder*='话题']",
        "input[placeholder*='搜索话题']",
        "input[placeholder*='搜索']",
    ]
    SEL_TOPIC_OPTION = [      # 话题搜索下拉候选项（hashed class 易变，配合文本匹配兜底）
        ".css-gfrh4c",
        "[class*='Topic'] [class*='item']",
        "[role='option']",
    ]

    # 知乎登录后写入的 cookie：z_c0 是登录 token，置信度高，任一存在即视为已登录。
    # （另有 __zse_ck 等反爬 cookie，但非登录态判据；Step3 若 z_c0 判不准再补，注释说明。）
    LOGIN_COOKIES = {"z_c0"}
    # 文章 URL 形如 https://zhuanlan.zhihu.com/p/2047125683084715841
    ID_RE = r"/p/(\d+)"

    # 话题至少要 2 个，凑不够用这些兜底（知乎发布通常要求至少 1 个话题）。
    _FALLBACK_TOPICS = ["开源", "人工智能", "GitHub"]

    def _editor_filled(self, page) -> bool:
        """校验正文是否真的注入成功：编辑器内含结构化子节点，或纯文本长度显著。
        合成 paste 的 isTrusted=false 可能被忽略、贴成空/纯文本，故必须事后校验。"""
        return bool(page.evaluate(
            """(sels) => {
                for (const s of sels) {
                    const el = document.querySelector(s);
                    if (!el) continue;
                    const structured = el.querySelectorAll(
                        'p,h1,h2,h3,pre,img,li,blockquote,figure').length;
                    const textLen = (el.innerText || '').trim().length;
                    if (structured > 0 || textLen > 80) return true;
                }
                return false;
            }""",
            self.SEL_EDITOR,
        ))

    def _select_topics(self, page, tags: list[str]) -> int:
        """选 2-3 个话题（知乎用「话题」）。实测流程：点「添加话题」→ 出搜索框 → 输入 →
        点下拉里文本匹配的候选。article.tags 优先，不足用 _FALLBACK_TOPICS 补。返回成功数。"""
        wanted: list[str] = []
        for t in [*tags, *self._FALLBACK_TOPICS]:
            t = (t or "").strip()
            if t and t not in wanted:
                wanted.append(t)
        wanted = wanted[:3]

        picked = 0
        for topic in wanted:
            if picked >= 3:
                break
            try:
                # 每加一个话题都重新点「添加话题」展开搜索（真实点击，React 才响应）
                if not self._click(page, self.SEL_TOPIC_TOGGLE, required=False):
                    self._js_click_button_text(page, "添加话题")
                page.wait_for_timeout(900)
                box = self._first(page, self.SEL_TOPIC_INPUT, required=False, timeout=3000)
                if box is None:
                    print(f"   [zhihu] 话题「{topic}」未出现搜索框，跳过")
                    continue
                box.click()
                box.fill("")
                box.type(topic, delay=50)
                page.wait_for_timeout(1600)   # 等下拉异步搜索返回
                if self._click_topic_option(page, topic):
                    picked += 1
                    page.wait_for_timeout(600)
                else:
                    print(f"   [zhihu] 话题「{topic}」无匹配候选，跳过")
            except Exception as e:  # noqa: BLE001 — 话题尽力，失败不阻塞发布
                print(f"   [zhihu] 话题「{topic}」选择失败（{e}）")
        if picked == 0:
            print("   ⚠️ [zhihu] 0 个话题选中——知乎发布要求至少 1 话题，发布会受阻，"
                  "请用 calibrate.py 校准 SEL_TOPIC_TOGGLE/SEL_TOPIC_INPUT/SEL_TOPIC_OPTION")
        return picked

    def _click_topic_option(self, page, topic: str) -> bool:
        """点话题下拉里文本匹配的候选（hashed class 易变，故用文本匹配兜底定位）。"""
        # 先按 selector + 文本
        for sel in self.SEL_TOPIC_OPTION:
            try:
                loc = page.locator(sel).filter(has_text=topic).first
                loc.wait_for(state="visible", timeout=1500)
                loc.click()
                return True
            except Exception:  # noqa: BLE001
                continue
        # 兜底：JS 点首个文本含 topic 的新出现候选元素
        return bool(page.evaluate(
            """(t) => {
                const els = [...document.querySelectorAll('div,span,li,button,a')].filter(
                    e => e.offsetParent !== null && (e.textContent||'').trim() &&
                         (e.textContent||'').trim().length < 24 &&
                         (e.textContent||'').includes(t) &&
                         /css-|Topic|option|item/i.test(e.className||''));
                if (els.length) { els[0].click(); return true; }
                return false;
            }""",
            topic,
        ))

    def do_publish(
        self, page, article: Article, rendered: RenderedArticle, *,
        publish: bool, existing_post_id: str | None, commit: bool,
    ) -> PublishResult | None:
        # 1) 导航（更新则进既有文章编辑页）
        target = (
            f"https://zhuanlan.zhihu.com/p/{existing_post_id}/edit"
            if existing_post_id else self.editor_url
        )
        page.goto(target, wait_until="domcontentloaded")
        if "signin" in page.url or "/login" in page.url:
            raise RuntimeError("打开编辑器被重定向到登录页，登录态可能失效，请重跑 --login")
        # 等富文本编辑器挂载到 DOM（contenteditable 可能存在却被判不可见，等 attached）
        page.wait_for_selector(
            "div[contenteditable='true'], .public-DraftEditor-content",
            state="attached", timeout=25000,
        )
        page.wait_for_timeout(1500)

        # 2) 标题（textarea/contenteditable，优先 JS 设值绕过不可见判定，兜底 fill）
        if not self._js_set_value(page, self.SEL_TITLE, article.title):
            try:
                self._first(page, self.SEL_TITLE).fill(article.title)
            except Exception as e:  # noqa: BLE001
                raise RuntimeError(
                    f"[zhihu] 找不到标题输入框（编辑器或已改版，试过 {self.SEL_TITLE}）"
                ) from e

        # 3) 正文（核心难点）：rendered.content 是已渲染 HTML，注入富文本剪贴板。
        #    主路径——合成 paste（DataTransfer 带 text/html）。注意合成 ClipboardEvent
        #    isTrusted=false，少数编辑器会忽略，故下面必须校验 + 真实剪贴板兜底。
        self._paste_html(page, self.SEL_EDITOR, rendered.content)
        page.wait_for_timeout(800)

        if not self._editor_filled(page):
            # 兜底——真实剪贴板 + 真按 Ctrl/Cmd+V（isTrusted=true，走浏览器可信路径）
            print("   [zhihu] 合成 paste 未生效（isTrusted=false 被忽略？），改用真实剪贴板兜底…")
            self._clipboard_paste(
                page, page.context, self.SEL_EDITOR,
                origin="https://zhuanlan.zhihu.com", html=rendered.content,
            )
            page.wait_for_timeout(1200)
            if not self._editor_filled(page):
                raise RuntimeError(
                    "[zhihu] 富文本注入两路均失败（编辑器仍为空）。知乎 paste handler 可能校验 "
                    "isTrusted，需 headed 复跑或用 codegen 校准 SEL_EDITOR。"
                )

        # 4) 预演到此为止（不点发布、不写历史）
        if not commit:
            return None

        # 5a) 存草稿：知乎编辑器自动存草稿，无需点按钮；草稿 URL 可能无 /p/<id>
        if not publish:
            page.wait_for_timeout(2500)   # 给自动存草稿留时间
            pid = self._extract_id(page.url, self.ID_RE) or (existing_post_id or "")
            return PublishResult(post_id=pid, url=page.url, state="draft")

        # 5b) 发布（知乎内联）：先在编辑页加话题（必填，≥1）→ 真实点「发布」→ 跳离 /edit 视为成功
        picked = self._select_topics(page, list(article.tags))
        if picked == 0:
            raise RuntimeError(
                "[zhihu] 未能选中任何话题（知乎发布要求≥1 话题）。请用 calibrate.py 校准 "
                "SEL_TOPIC_TOGGLE / SEL_TOPIC_INPUT / SEL_TOPIC_OPTION。"
            )
        page.wait_for_timeout(500)
        # 真实点「发布」（React 按钮，合成 click 不触发）
        if not self._click(page, self.SEL_PUBLISH_BTN, required=False):
            if not self._js_click_button_text(page, "发布"):
                raise RuntimeError("[zhihu] 找不到「发布」按钮（需校准 SEL_PUBLISH_BTN）")

        # 成功判定：URL 跳离 /edit（变为 /p/<id> 文章页）。仍在 /edit 视为未发布、不误报。
        def _published() -> bool:
            return "/p/" in page.url and "/edit" not in page.url
        try:
            page.wait_for_url(lambda u: "/p/" in u and "/edit" not in u, timeout=12000)
        except Exception:  # noqa: BLE001
            self._js_click_button_text(page, "发布")   # 可能有二次确认，兜底再点
            try:
                page.wait_for_url(lambda u: "/p/" in u and "/edit" not in u, timeout=10000)
            except Exception:  # noqa: BLE001
                page.wait_for_timeout(1500)
        if not _published():
            raise RuntimeError(
                "[zhihu] 点「发布」后仍停在编辑页（未跳 /p/<id> 文章页），发布可能未完成。"
                "当前 URL: " + page.url
            )
        pid = self._extract_id(page.url, self.ID_RE) or (existing_post_id or "")
        return PublishResult(post_id=pid, url=page.url, state="published")

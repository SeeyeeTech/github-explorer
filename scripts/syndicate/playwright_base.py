"""路线 C：Playwright 持久化登录 + 脚本驱动浏览器发布（给无开放 API 的平台）。

与 browser.py（BrowserAdapter，mode='browser'）的根本区别——同样面向掘金/CSDN
这类「无开放发布 API」的平台，但发布动作的执行者不同：

  - BrowserAdapter（旧）：脚本只 prepare() 出一份 playbook，真正的 DOM 操作由
    Claude（agent）通过 Claude-in-Chrome 实时驱动。每发一篇都要 agent 看屏幕、
    逐步决策——慢、费 token、要人盯、平台弹窗一改版就卡。
  - PlaywrightAdapter（本模块，mode='playwright'）：脚本用 Playwright 的**持久化
    上下文**复用「一次性手动登录」留下的会话，用**固定代码**驱动 DOM 发布。
    快、确定、可半无人值守，发一篇 = 跑一条命令。

登录态怎么留住（核心）：
  launch_persistent_context(user_data_dir=...) 把 cookie / localStorage 落到磁盘
  目录，登录一次后长期复用。每个渠道一个独立目录，默认
  ~/.syndicate/playwright/<channel>（不在 repo 内 → 天然不入 Git；可用环境变量
  SYNDICATE_PW_DIR 覆盖根位置）。首次跑 `--login` 有头打开浏览器、人工登录一次即可。

为什么不纯 requests + 导出 cookie 直调内部 API：CSDN/掘金的发布接口带**请求签名**
（CSDN 的 sign、掘金的 a_bogus 等，算法会变、难维护）。让真实浏览器页面去发，
签名 / cookie / Origin / 防盗链全由平台自己的前端环境天然满足，我们不碰签名地狱。

子类契约（见 adapters/csdn.py 范例）：
  - 类属性 name / editor_url / login_url / content_format
  - is_logged_in(page) -> bool            判断当前是否已登录
  - do_publish(page, article, rendered, *, publish, existing_post_id, commit)
        commit=False 时只灌内容、停在「发布前」（供 --preview 预演，返回 None）；
        commit=True  时走完发布/存草稿，返回 PublishResult。
基类负责：持久化上下文的开关、登录流程、登录态校验、灌文/点击的健壮工具方法。

依赖：playwright（pip install playwright && playwright install chromium）。
顶层**不** import playwright —— 惰性导入，避免「只用 cnblogs/wechat」的场景被这个
重依赖拖累（注册表会 import 所有 adapter）。
"""
from __future__ import annotations

from pathlib import Path

from .base import Article, BaseAdapter, PublishResult, RenderedArticle, env


class PlaywrightAdapter(BaseAdapter):
    """浏览器自动化渠道基类（Playwright 驱动，脚本可直接发布）。"""

    mode = "playwright"
    content_format = "markdown"      # 掘金/CSDN 编辑器多为 markdown 原生
    editor_url = ""
    login_url = ""                   # 登录入口；留空则用 editor_url

    # ── 子类必须实现 ────────────────────────────────────────────────
    def is_logged_in(self, page) -> bool:
        """当前页面/上下文是否已登录该平台。子类覆盖（查 cookie 或登录态元素）。"""
        raise NotImplementedError

    def do_publish(
        self, page, article: Article, rendered: RenderedArticle, *,
        publish: bool, existing_post_id: str | None, commit: bool,
    ) -> PublishResult | None:
        """真正的发布动作（驱动 DOM）。commit=False 只灌内容、停在发布前并返回 None。"""
        raise NotImplementedError

    # ── 持久化上下文位置 ────────────────────────────────────────────
    def user_data_dir(self) -> Path:
        base = env("SYNDICATE_PW_DIR") or str(Path.home() / ".syndicate" / "playwright")
        return Path(base) / self.name

    def _launch(self, p, *, headless: bool):
        """开一个持久化上下文（复用磁盘上的登录态）。返回 BrowserContext。"""
        d = self.user_data_dir()
        d.mkdir(parents=True, exist_ok=True)
        return p.chromium.launch_persistent_context(
            str(d),
            headless=headless,
            viewport={"width": 1440, "height": 900},
            args=["--disable-blink-features=AutomationControlled"],  # 降低自动化指纹
        )

    @staticmethod
    def _page(ctx):
        return ctx.pages[0] if ctx.pages else ctx.new_page()

    # ── 框架契约：check_auth / publish ──────────────────────────────
    def check_auth(self) -> None:
        """轻量校验：登录目录是否存在且非空（不开浏览器、无网络副作用）。"""
        d = self.user_data_dir()
        if not d.exists() or not any(d.iterdir()):
            raise RuntimeError(
                f"{self.name} 尚未登录（{d} 为空）。先跑一次：\n"
                f"  python3 scripts/syndicate_publish.py --channel {self.name} --login"
            )

    def publish(
        self, article: Article, rendered: RenderedArticle | None, *,
        publish: bool, existing_post_id: str | None = None,
    ) -> PublishResult:
        result = self._run(
            article, rendered, publish=publish,
            existing_post_id=existing_post_id, commit=True,
        )
        if result is None:  # 理论不会发生（commit=True 必返回结果）
            raise RuntimeError(f"{self.name} 发布未返回结果")
        return result

    # ── --login / --preview 入口 ────────────────────────────────────
    def login(self) -> bool:
        """有头打开浏览器，人工登录一次，登录态落盘持久化。"""
        from playwright.sync_api import sync_playwright

        print(f"🔐 [{self.name}] 即将打开浏览器，请在弹出的窗口里登录 {self.name} …")
        ok = False
        with sync_playwright() as p:
            ctx = self._launch(p, headless=False)
            page = self._page(ctx)
            page.goto(self.login_url or self.editor_url, wait_until="domcontentloaded")
            input(f"   在浏览器里完成 {self.name} 登录后，回到终端按【回车】继续校验… ")
            try:
                page.goto(self.editor_url, wait_until="domcontentloaded")
                page.wait_for_timeout(1500)
                ok = self.is_logged_in(page)
            except Exception as e:  # noqa: BLE001
                print(f"   登录态校验时出错：{e}")
            ctx.close()
        print("✅ 登录态已保存，后续发布将复用它" if ok
              else "⚠️ 未检测到登录态，可重试 --login（确认确实登录成功）")
        return ok

    def preview(self, article: Article, rendered: RenderedArticle) -> None:
        """预演：有头打开、灌好内容、停在发布前（不点发布、不写历史）。验证 selector/登录。"""
        print("🧪 预演：打开浏览器灌入内容，停在「发布前」（不点发布、不写历史）")
        self._run(article, rendered, publish=False, existing_post_id=None,
                  commit=False, headless=False)

    # ── 公共执行骨架 ────────────────────────────────────────────────
    def _run(
        self, article: Article, rendered: RenderedArticle | None, *,
        publish: bool, existing_post_id: str | None, commit: bool,
        headless: bool | None = None,
    ) -> PublishResult | None:
        from playwright.sync_api import sync_playwright

        if rendered is None:
            raise RuntimeError(f"{self.name} 需要框架渲染结果（rendered 不应为 None）")
        if headless is None:
            headless = env("SYNDICATE_PW_HEADLESS").lower() in ("1", "true", "yes")

        with sync_playwright() as p:
            ctx = self._launch(p, headless=headless)
            page = self._page(ctx)
            try:
                page.goto(self.editor_url, wait_until="domcontentloaded")
                page.wait_for_timeout(1500)
                if not self.is_logged_in(page):
                    raise RuntimeError(
                        f"{self.name} 未登录或登录态已失效。先跑：\n"
                        f"  python3 scripts/syndicate_publish.py --channel {self.name} --login"
                    )
                result = self.do_publish(
                    page, article, rendered,
                    publish=publish, existing_post_id=existing_post_id, commit=commit,
                )
                if not commit:
                    input("   预演完成（已停在发布前）。查看完毕按【回车】关闭浏览器… ")
                return result
            finally:
                ctx.close()

    # ── DOM 工具方法（健壮：多 selector 兜底 + 清晰报错）────────────────
    def _first(self, page, selectors: list[str], *, required: bool = True, timeout: int = 8000):
        """返回第一个可见的元素 locator。多 selector 兜底，便于扛平台小改版。"""
        for sel in selectors:
            loc = page.locator(sel).first
            try:
                loc.wait_for(state="visible", timeout=timeout if sel == selectors[-1] else 1500)
                return loc
            except Exception:  # noqa: BLE001
                continue
        if required:
            raise RuntimeError(
                f"[{self.name}] 找不到元素，试过的 selector：{selectors}\n"
                f"  平台可能改版了。用 `playwright codegen {self.editor_url}` 录制真实 selector 后更新本 adapter。"
            )
        return None

    def _click(self, page, selectors: list[str], *, required: bool = True) -> bool:
        loc = self._first(page, selectors, required=required)
        if loc is None:
            return False
        loc.click()
        return True

    def _focus_insert(self, page, selectors: list[str], text: str) -> None:
        """聚焦编辑区并一次性插入文本（insert_text 不逐字键入，对 CodeMirror 友好）。"""
        loc = self._first(page, selectors)
        loc.click()
        page.wait_for_timeout(300)
        page.keyboard.insert_text(text)

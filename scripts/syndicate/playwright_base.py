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

import json
from pathlib import Path

from .base import Article, BaseAdapter, PublishResult, RenderedArticle, env


class PlaywrightAdapter(BaseAdapter):
    """浏览器自动化渠道基类（Playwright 驱动，脚本可直接发布）。"""

    mode = "playwright"
    content_format = "markdown"      # 掘金/CSDN 编辑器多为 markdown 原生
    editor_url = ""
    login_url = ""                   # 登录入口；留空则用 editor_url

    # ── 子类声明的登录标志 ──────────────────────────────────────────
    LOGIN_COOKIES: set[str] = set()   # 登录后写入的 cookie 名（任一存在即视为已登录）

    # ── 子类必须实现 ────────────────────────────────────────────────
    def is_logged_in(self, context) -> bool:
        """当前上下文是否已登录该平台。默认实现：查 context.cookies() 是否含 LOGIN_COOKIES
        任一名（不依赖当前页面 URL）。cookie 判不准的平台可子类覆盖。"""
        if not self.LOGIN_COOKIES:
            raise NotImplementedError(
                f"{self.name} 需声明 LOGIN_COOKIES 或覆盖 is_logged_in()"
            )
        try:
            names = {c.get("name") for c in context.cookies()}
        except Exception:  # noqa: BLE001 — 跳转瞬间可能取不到 cookie，下轮再试
            return False
        return bool(names & self.LOGIN_COOKIES)

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

    # ── 会话 cookie 持久化（storage_state）──────────────────────────────────
    # 持久化上下文（profile）默认**不保存 session cookie**（无 expiry 的内存 cookie），
    # 有些站点（如阿里云 login_aliyunid_ticket）登录态正是 session cookie，进程一关就丢、
    # 下次发布又要重登。故登录成功后额外把 storage_state（含 session cookie）存成 JSON，
    # 每次启动再回灌，实现「一次登录、跨进程复用」。
    def _storage_path(self) -> Path:
        return self.user_data_dir() / "storage_state.json"

    def _save_cookies(self, ctx) -> None:
        try:
            ctx.storage_state(path=str(self._storage_path()))
        except Exception:  # noqa: BLE001
            pass

    def _restore_cookies(self, ctx) -> None:
        p = self._storage_path()
        if not p.is_file():
            return
        try:
            cookies = json.loads(p.read_text(encoding="utf-8")).get("cookies", [])
            if cookies:
                ctx.add_cookies(cookies)
        except Exception:  # noqa: BLE001
            pass

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
        """有头打开浏览器，人工登录一次，登录态落盘持久化。

        不依赖终端交互（stdin 可为非 tty，如 IDE/agent 终端，input() 会瞬间 EOF）：
        打开登录页后轮询检测登录态，检测到 cookie 写入即视为成功、保存并关闭；
        超时则放弃。轮询上限可用 SYNDICATE_LOGIN_TIMEOUT（秒，默认 300）覆盖。
        """
        import time

        from playwright.sync_api import sync_playwright

        try:
            timeout_s = max(10, int(env("SYNDICATE_LOGIN_TIMEOUT") or "300"))
        except ValueError:
            timeout_s = 300
        poll = 3
        print(f"🔐 [{self.name}] 已打开浏览器，请在弹出的窗口里登录 {self.name} …")
        print(f"   登录成功后自动检测并保存（最多等 {timeout_s}s，无需回终端按回车）。")
        ok = False
        with sync_playwright() as p:
            ctx = self._launch(p, headless=False)
            self._restore_cookies(ctx)   # 回灌上次保存的会话 cookie（可能已登录）
            page = self._page(ctx)
            page.goto(self.login_url or self.editor_url, wait_until="domcontentloaded")
            waited = 0
            while waited < timeout_s:
                try:
                    if self.is_logged_in(ctx):
                        ok = True
                        break
                except Exception:  # noqa: BLE001 — 跳转瞬间可能取不到 cookie，下轮再试
                    pass
                time.sleep(poll)
                waited += poll
                if waited % 30 == 0:
                    print(f"   …仍在等待登录（{waited}/{timeout_s}s）")
            if ok:
                self._save_cookies(ctx)   # 存 storage_state（含 session cookie），供跨进程复用
            ctx.close()
        print("✅ 登录态已保存，后续发布将复用它" if ok
              else f"⚠️ {timeout_s}s 内未检测到登录态（未登录或 cookie 未写入），可重试 --login")
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
            self._restore_cookies(ctx)   # 回灌保存的会话 cookie（阿里云等 session 态靠它跨进程复用）
            page = self._page(ctx)
            try:
                if not self.is_logged_in(ctx):
                    raise RuntimeError(
                        f"{self.name} 未登录或登录态已失效（cookie 缺失/过期）。先跑：\n"
                        f"  python3 scripts/syndicate_publish.py --channel {self.name} --login"
                    )
                # 导航交给 do_publish（新建 goto editor_url；更新 goto ?articleId=）
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

    # ── JS 注入辅助（绕 actionability：元素在 DOM 里却被判「不可见」时用）──────
    # 很多富前端编辑器（CSDN/掘金/阿里云…）的标题 input / 编辑区 / 弹窗按钮在 DOM 里
    # 存在却被特殊 CSS 判定「不可见」，fill()/click() 因 actionability 检查超时失败。
    # 改走 JS 直接操作 DOM 绕过可见性门槛（实测可行）。
    @staticmethod
    def _js_set_value(page, selectors: list[str], value: str) -> bool:
        """给首个命中的 input/textarea 设 value 并派发 input/change。

        用「原型上的原生 value setter」赋值——React 会在元素实例上劫持 value setter 来
        追踪受控输入，直接 `el.value=` 会被它忽略（React 仍认为是空值 → 触发不了 onChange、
        必填校验不通过）。走 HTMLInputElement.prototype 的原生 setter 再派发 input 事件，
        React / Vue 都能正确收到变更。"""
        return bool(page.evaluate(
            """([sels, v]) => {
                for (const s of sels) {
                    const el = document.querySelector(s);
                    if (!el) continue;
                    el.focus();
                    const proto = el.tagName === 'TEXTAREA'
                        ? window.HTMLTextAreaElement.prototype
                        : window.HTMLInputElement.prototype;
                    const setter = Object.getOwnPropertyDescriptor(proto, 'value').set;
                    setter.call(el, v);
                    el.dispatchEvent(new Event('input', {bubbles: true}));
                    el.dispatchEvent(new Event('change', {bubbles: true}));
                    return true;
                }
                return false;
            }""",
            [selectors, value],
        ))

    @staticmethod
    def _js_focus(page, selectors: list[str]) -> bool:
        """聚焦首个命中的元素（供随后用 keyboard 灌入 contenteditable）。"""
        return bool(page.evaluate(
            """(sels) => {
                for (const s of sels) {
                    const el = document.querySelector(s);
                    if (el) { el.focus(); return true; }
                }
                return false;
            }""",
            selectors,
        ))

    @staticmethod
    def _js_click(page, selectors: list[str]) -> bool:
        """点击首个命中的元素（纯 CSS selector，不支持 :has-text）。"""
        return bool(page.evaluate(
            """(sels) => {
                for (const s of sels) {
                    const el = document.querySelector(s);
                    if (el) { el.click(); return true; }
                }
                return false;
            }""",
            selectors,
        ))

    @staticmethod
    def _js_click_button_text(page, text: str, *, cls_contains: str = "") -> bool:
        """点文本含 text、且 class 含 cls_contains 的可见 button（按文本精确定位，避免
        .first 误选近似按钮——如「发布文章」与「定时发布」共用一个 class）。"""
        return bool(page.evaluate(
            """([t, cls]) => {
                const b = [...document.querySelectorAll('button')].find(
                    e => (e.textContent || '').includes(t)
                         && (!cls || (e.className || '').includes(cls))
                         && e.offsetParent !== null
                );
                if (b) { b.click(); return true; }
                return false;
            }""",
            [text, cls_contains],
        ))

    # ── 富文本/CodeMirror 注入：合成 paste 事件（不依赖系统剪贴板）────────────
    @staticmethod
    def _paste_inject(page, selectors: list[str], *, html: str = "", text: str = "") -> str:
        """在首个命中的编辑器元素上 dispatch 一个合成 paste ClipboardEvent，DataTransfer
        带 text/html 与/或 text/plain——编辑器自己的 paste handler 会把它映射进内部模型
        （富文本编辑器据此还原结构，CodeMirror 据此插入文本）。

        返回：'no-editor'（没找到元素）/ 'dispatched'（已派发）。注意：合成事件
        isTrusted=false，少数编辑器会因此忽略——调用方应在事后校验注入是否生效，
        失败时回退真实剪贴板 + 键盘 Ctrl/Cmd+V。
        """
        return str(page.evaluate(
            """([sels, html, text]) => {
                let el = null;
                for (const s of sels) { el = document.querySelector(s); if (el) break; }
                if (!el) return 'no-editor';
                el.focus();
                // 把光标放到编辑区内末尾，handler 才有合法 range 可插入
                try {
                    const r = document.createRange();
                    r.selectNodeContents(el); r.collapse(false);
                    const sel = window.getSelection();
                    sel.removeAllRanges(); sel.addRange(r);
                } catch (e) { /* input/textarea 无需 range */ }
                const dt = new DataTransfer();
                if (html) dt.setData('text/html', html);
                if (text) dt.setData('text/plain', text);
                el.dispatchEvent(new ClipboardEvent('paste',
                    {clipboardData: dt, bubbles: true, cancelable: true}));
                return 'dispatched';
            }""",
            [selectors, html, text],
        ))

    def _paste_html(self, page, selectors: list[str], html: str, *, plain: str = "") -> str:
        """富文本编辑器注入 HTML（合成 paste，text/html 为主、text/plain 兜底）。"""
        return self._paste_inject(page, selectors, html=html, text=plain or "")

    def _paste_text(self, page, selectors: list[str], text: str) -> str:
        """CodeMirror 等纯文本编辑器注入（合成 paste，text/plain）。"""
        return self._paste_inject(page, selectors, text=text)

    @staticmethod
    def _clipboard_paste(page, context, selectors: list[str], *, origin: str,
                         html: str = "", text: str = "") -> bool:
        """真实剪贴板兜底：授权 → navigator.clipboard.write → 聚焦编辑器 → 真 Ctrl/Cmd+V。
        走浏览器可信路径（isTrusted=true），合成 paste 被编辑器忽略时用。需 headed + 页面聚焦。"""
        try:
            context.grant_permissions(["clipboard-read", "clipboard-write"], origin=origin)
        except Exception:  # noqa: BLE001 — 个别环境不支持按 origin 授权，忽略后试
            pass
        page.bring_to_front()
        wrote = bool(page.evaluate(
            """async ([html, text]) => {
                try {
                    const data = {};
                    if (html) data['text/html'] = new Blob([html], {type: 'text/html'});
                    if (text) data['text/plain'] = new Blob([text], {type: 'text/plain'});
                    await navigator.clipboard.write([new ClipboardItem(data)]);
                    return true;
                } catch (e) { return false; }
            }""",
            [html, text],
        ))
        if not wrote:
            return False
        # 聚焦编辑器后真按粘贴键
        for s in selectors:
            loc = page.locator(s).first
            try:
                loc.click(timeout=1500)
                break
            except Exception:  # noqa: BLE001
                continue
        page.keyboard.press("ControlOrMeta+v")
        return True

    @staticmethod
    def _extract_id(url: str | None, pattern: str) -> str:
        """按平台正则从 URL 提取文章 id（pattern 须含一个捕获组）。取不到返回 ''。"""
        import re
        m = re.search(pattern, url or "")
        return m.group(1) if m else ""

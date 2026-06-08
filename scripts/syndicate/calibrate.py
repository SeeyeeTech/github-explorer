#!/usr/bin/env python3
"""selector 校准探针 —— 用某 playwright 渠道的持久化登录态打开编辑器，dump：
  ① 当前 cookie 名 + 声明的 LOGIN_COOKIES 是否判为已登录（校准 LOGIN_COOKIES）
  ② 该 adapter 各 SEL_* 常量当前命中元素数（哪条 selector 失效一目了然）
  ③ 候选元素（可见 input/textarea、contenteditable、button 文本）供挑正确 selector

只读、不发布、无 stdin 交互。需先对该渠道跑过 `--login`（持久化登录态存在）。
注意：同一持久化目录同一时刻只能被一个进程占用——跑本探针前先确保 --login 的浏览器已关闭。

用法：
  python3 scripts/syndicate/calibrate.py <channel> [--headed] [--publish-ui]
  # 例：python3 scripts/syndicate/calibrate.py juejin
  # --publish-ui：用 adapter 的方法灌入测试标题/正文 → 点「发布」打开发布抽屉/弹窗 →
  #               dump 抽屉内可见元素（校准分类/标签/确认按钮等只在抽屉内出现的 selector）。
  #               只打开抽屉、**不点最终确认**，不会真发文。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # 让 `syndicate` 可导入

from syndicate.base import get_adapter, load_dotenv  # noqa: E402


def _dump(page, label: str, js: str) -> None:
    try:
        data = page.evaluate(js)
    except Exception as e:  # noqa: BLE001
        data = f"ERR: {e}"
    print(f"\n--- {label} ---")
    print(json.dumps(data, ensure_ascii=False, indent=1) if not isinstance(data, str) else data)


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    channel = sys.argv[1]
    headed = "--headed" in sys.argv
    publish_ui = "--publish-ui" in sys.argv
    wait_login = 0
    run_mode = None   # None | 'draft' | 'publish'：登录后实跑 do_publish
    report = None
    hold = 0          # 跑完保持窗口打开 N 秒供观察
    for a in sys.argv[2:]:
        if a.startswith("--wait-login"):
            wait_login = int(a.split("=")[1]) if "=" in a else 100
            headed = True  # 登录必须有头
        elif a.startswith("--run"):
            run_mode = a.split("=")[1] if "=" in a else "draft"
        elif a.startswith("--hold"):
            hold = int(a.split("=")[1]) if "=" in a else 60
        elif a.endswith(".md"):
            report = a
    load_dotenv()

    # 分析类/CSRF/会话类无关 cookie，diff 登录 cookie 时排除（避免把它们误判成「已登录」）
    _NOISE_PREFIX = ("_ga", "_gid", "Hm_", "HMACCOUNT", "OAID", "_c_", "umeng", "_tea",
                     "__tea", "s_v_web_id", "_utm", "JSESSIONID", "cna", "tfstk", "sca",
                     "atpsida", "arms", "_bl_uid", "cbc", "aliyun_enable")
    _NOISE_SUBSTR = ("csrf", "xsrf", "token", "_uid")

    def _is_noise(n: str) -> bool:
        nl = (n or "").lower()
        return (any(n.startswith(x) for x in _NOISE_PREFIX)
                or any(s in nl for s in _NOISE_SUBSTR))

    from playwright.sync_api import sync_playwright

    ad = get_adapter(channel)
    if getattr(ad, "mode", "") != "playwright":
        print(f"❌ {channel} 非 playwright 渠道")
        return 1

    with sync_playwright() as p:
        ctx = ad._launch(p, headless=not headed)
        try:
            ad._restore_cookies(ctx)   # 回灌保存的会话 cookie（跨进程复用登录态）
            page = ad._page(ctx)

            if wait_login:
                pre = {c.get("name") for c in ctx.cookies()}
                print("PRE-LOGIN cookies:", sorted(pre))
                page.goto(ad.login_url or ad.editor_url, wait_until="domcontentloaded")
                print(f"⏳ 请在弹出的窗口里登录（最多 {wait_login}s，检测到登录 cookie 稳定后提前结束）…")
                waited, last_new = 0, set()
                while waited < wait_login:
                    page.wait_for_timeout(5000)
                    waited += 5
                    now = {c.get("name") for c in ctx.cookies()}
                    new = {n for n in (now - pre) if n and not _is_noise(n)}
                    if new and new != last_new:
                        print(f"  +{waited}s 新登录候选 cookie: {sorted(new)}")
                    last_new = new
                    # 用 adapter 自己的 is_logged_in 判定提前结束（最可靠；cookie 名猜错则等满）
                    try:
                        if ad.is_logged_in(ctx):
                            print(f"  +{waited}s ✅ is_logged_in=True，提前结束")
                            ad._save_cookies(ctx)   # 存 storage_state，供跨进程复用
                            break
                    except Exception:  # noqa: BLE001
                        pass
                print("LOGIN 候选 cookie（核对/补全 LOGIN_COOKIES 用）:", sorted(last_new) or "(无新增)")
                print("全部当前 cookie:", sorted({c.get('name') for c in ctx.cookies()}))

                # 登录后在同一进程内 dump 编辑器结构（阿里云等会话态不跨进程持久化的渠道靠这个）
                page.goto(ad.editor_url, wait_until="domcontentloaded")
                page.wait_for_timeout(6000)
                print("\n编辑器 URL:", page.url)
                _dump(page, "编辑器类型探测",
                      """() => ({CodeMirror:!!document.querySelector('.CodeMirror'),
                                cm_content:!!document.querySelector('.cm-content'),
                                ace:!!document.querySelector('.ace_editor'),
                                monaco:!!document.querySelector('.monaco-editor'),
                                textarea:document.querySelectorAll('textarea').length,
                                contenteditable:document.querySelectorAll('[contenteditable=true]').length})""")
                _dump(page, "Markdown/富文本/模式切换 控件",
                      """() => [...document.querySelectorAll('button,a,div,span,label,li,[role=tab]')]
                           .filter(e => /Markdown|markdown|富文本|编辑器|切换|MD/.test(e.textContent||'')
                                   && e.offsetParent!==null && (e.textContent||'').trim().length<18)
                           .slice(0,15).map(e => ({tag:e.tagName, t:(e.textContent||'').trim(),
                                                   cls:String(e.className||'').slice(0,45)}))""")
                _dump(page, "可见 input/textarea（前 10）",
                      """() => [...document.querySelectorAll('input,textarea')]
                           .filter(e => e.offsetParent!==null).slice(0,10)
                           .map(e => ({tag:e.tagName, ph:e.placeholder||'', cls:String(e.className||'').slice(0,45)}))""")

            if run_mode:
                # 登录后在同一新会话里实跑 adapter.do_publish，逐阶段验证（最可靠）。
                from syndicate import render as render_mod
                from syndicate.base import parse_report
                if not report:
                    print("❌ --run 需要一个 .md 报告参数")
                    return 2
                art = parse_report(Path(report))
                rendered = render_mod.render(
                    art, ad.content_format, mp_cta=ad.mp_cta, name_wechat=ad.name_wechat)
                do_pub = run_mode == "publish"
                print(f"\n===== --run {run_mode}：实跑 do_publish（publish={do_pub}）=====")
                print(f"  报告: {art.slug} | 标题: {art.title} | tags={list(art.tags)}")
                try:
                    res = ad.do_publish(page, art, rendered, publish=do_pub,
                                        existing_post_id=None, commit=True)
                    print("✅ do_publish 返回:", res)
                except Exception as e:  # noqa: BLE001
                    import traceback
                    print("❌ do_publish 抛错:", repr(e))
                    traceback.print_exc()
                print("最终 URL:", page.url)
                # 提交后状态诊断：残留 modal/alert/toast + 可见按钮（判断是否还有确认步骤）
                _dump(page, "残留 modal/alert/toast 文本",
                      """() => [...document.querySelectorAll('.modal.show,.alert,.toast,[role=alert],[class*=message],[class*=notify]')]
                           .filter(e => e.offsetParent !== null)
                           .map(e => (e.textContent||'').trim().slice(0,120)).filter(Boolean).slice(0,8)""")
                _dump(page, "当前可见按钮",
                      """() => [...document.querySelectorAll('button,a.btn')]
                           .filter(e => e.offsetParent !== null)
                           .map(e => (e.textContent||'').trim()).filter(t=>t&&t.length<16).slice(0,30)""")
                if hold:
                    print(f"\n⏸ 窗口保持 {hold}s 供观察（看点「提交」后页面反应）…")
                    page.wait_for_timeout(hold * 1000)
                else:
                    page.wait_for_timeout(1500)
                return 0

            names = sorted({c.get("name") for c in ctx.cookies()})
            print(f"COOKIES（{len(names)}）:", names)
            print("LOGIN_COOKIES 声明:", sorted(ad.LOGIN_COOKIES),
                  "→ is_logged_in:", ad.is_logged_in(ctx))

            page.goto(ad.editor_url, wait_until="domcontentloaded")
            page.wait_for_timeout(4500)
            print("\nURL after goto:", page.url)

            for attr in sorted(a for a in dir(ad) if a.startswith("SEL_")):
                sels = getattr(ad, attr)
                if not isinstance(sels, list):
                    continue
                print(f"\n[{attr}]  (命中数 / selector)")
                for s in sels:
                    sel = s.replace("{text}", "占位")  # 含占位的分类 selector 跳过精确计数
                    try:
                        n = page.locator(sel).count()
                    except Exception as e:  # noqa: BLE001
                        n = f"ERR:{type(e).__name__}"
                    print(f"  {str(n):>6}  {s}")

            _dump(page, "可见 INPUT/TEXTAREA（前 30）",
                  """() => [...document.querySelectorAll('input,textarea')]
                       .filter(e => e.offsetParent !== null).slice(0,30)
                       .map(e => ({tag:e.tagName, type:e.type||'', ph:e.placeholder||'',
                                   name:e.name||'', cls:(e.className||'').slice(0,60)}))""")
            _dump(page, "CONTENTEDITABLE（前 10）",
                  """() => [...document.querySelectorAll('[contenteditable=\"true\"]')].slice(0,10)
                       .map(e => ({tag:e.tagName, cls:(e.className||'').slice(0,80)}))""")
            _dump(page, "CodeMirror 在?",
                  "() => !!document.querySelector('.CodeMirror, .cm-content')")
            _dump(page, "可见 BUTTON 文本（前 40）",
                  """() => [...document.querySelectorAll('button')]
                       .filter(e => e.offsetParent !== null).slice(0,40)
                       .map(e => ({t:(e.textContent||'').trim().slice(0,14),
                                   cls:(e.className||'').slice(0,40)}))""")

            if publish_ui:
                print("\n\n========== 打开发布抽屉/弹窗后 dump（不点最终确认）==========")
                # 用 adapter 自己的方法灌测试标题/正文（顺带验证这两步），再点「发布」开抽屉
                try:
                    ad._js_set_value(page, ad.SEL_TITLE, "【校准测试】请勿发布")
                except Exception as e:  # noqa: BLE001
                    print("标题灌入异常:", e)
                try:
                    ad._focus_insert(page, ad.SEL_EDITOR, "# 校准测试\n\n这是 selector 校准用的测试正文，请勿发布。")
                except Exception as e:  # noqa: BLE001
                    print("正文灌入异常:", e)
                page.wait_for_timeout(800)
                print("正文已灌入?", _editor_probe(page))
                if not ad._click(page, ad.SEL_PUBLISH_BTN, required=False):
                    print("⚠️ 点不到 SEL_PUBLISH_BTN")
                page.wait_for_timeout(2500)
                print("点发布后 URL:", page.url)
                for attr in ("SEL_CATEGORY_OPTION", "SEL_TAG_INPUT", "SEL_TAG_OPTION",
                             "SEL_TOPIC_INPUT", "SEL_TOPIC_OPTION", "SEL_MODAL_PUBLISH",
                             "SEL_ORIGINAL", "SEL_MODE_CONFIRM"):
                    sels = getattr(ad, attr, None)
                    if not isinstance(sels, list):
                        continue
                    print(f"\n[{attr}]")
                    for s in sels:
                        sel = s.replace("{text}", "占位")
                        try:
                            n = page.locator(sel).count()
                        except Exception as e:  # noqa: BLE001
                            n = f"ERR:{type(e).__name__}"
                        print(f"  {str(n):>6}  {s}")
                _dump(page, "抽屉内可见 BUTTON（前 40）",
                      """() => [...document.querySelectorAll('button')]
                           .filter(e => e.offsetParent !== null).slice(0,40)
                           .map(e => ({t:(e.textContent||'').trim().slice(0,16),
                                       cls:(e.className||'').slice(0,46)}))""")
                _dump(page, "抽屉内可见 input + radio/label/分类项（前 50）",
                      """() => [...document.querySelectorAll('input,label,[role=radio],[class*=radio],[class*=tag],[class*=category],[class*=cate]')]
                           .filter(e => e.offsetParent !== null).slice(0,50)
                           .map(e => ({tag:e.tagName, ph:e.placeholder||'',
                                       t:(e.textContent||'').trim().slice(0,16),
                                       cls:String(e.className||'').slice(0,50)}))""")

                # 非破坏性测试 adapter 抽屉内字段逻辑（必填项 _select_*、标签 _fill/_select_*）——
                # 只选不点最终确认，不会真发文。
                import types
                fake = types.SimpleNamespace(
                    title="后端 AI 开源工具测试", tags=["GitHub", "开源", "人工智能"],
                    digest="校准测试摘要",
                )
                print("\n--- 抽屉字段逻辑测试（非破坏，不点确认）---")
                for meth in ("_select_category", "_select_field"):
                    if hasattr(ad, meth):
                        try:
                            getattr(ad, meth)(page, fake)
                            print(f"  ✅ {meth} 成功")
                        except Exception as e:  # noqa: BLE001
                            print(f"  ❌ {meth} 失败: {e}")
                for meth in ("_fill_tags", "_select_required_tags", "_select_topics"):
                    if hasattr(ad, meth):
                        try:
                            r = getattr(ad, meth)(page, ["GitHub", "开源", "人工智能"])
                            print(f"  · {meth} 返回 {r!r}")
                        except Exception as e:  # noqa: BLE001
                            print(f"  ❌ {meth} 失败: {e}")
        finally:
            ctx.close()
    return 0


def _editor_probe(page) -> str:
    try:
        return str(page.evaluate("""() => {
            const cm = document.querySelector('.CodeMirror');
            if (cm && cm.CodeMirror) return 'CM:'+cm.CodeMirror.getValue().length;
            const c = document.querySelector('.cm-content,[contenteditable=\"true\"]');
            return c ? 'CE:'+(c.innerText||'').length : 'none';
        }"""))
    except Exception as e:  # noqa: BLE001
        return f"ERR:{e}"


if __name__ == "__main__":
    raise SystemExit(main())

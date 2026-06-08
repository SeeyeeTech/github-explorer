# syndicate —— 一文多发框架

把现有「单渠道公众号发布」泛化成「一份报告 → 多个渠道」的 `publisher + adapter`
结构。新接一个平台 = 写一个 adapter，主流程不动。每个外发渠道自动追加
「导流公众号页脚」，把外部读者引回公众号。

> 已落地：通用骨架 + 渲染层 + per-channel 发布历史 + 多渠道：
> **api**（`wechat` 公众号复用 wechat_publish.py、`cnblogs` 博客园 / `oschina` 开源中国 MetaWeblog）、
> **playwright**（`csdn` / `juejin` / `zhihu` / `segmentfault` / `aliyun`——持久化登录态 + 脚本驱动 DOM，
> 一次 `--login` 后一键发）、**browser**（`oschina_web`——开源中国 API 不通时的 Claude-in-Chrome 兜底）。

## 架构

```
scripts/syndicate_publish.py        CLI 入口
scripts/syndicate/
  base.py        Article / RenderedArticle / PublishResult / BaseAdapter / 注册表 / 报告解析 / .env.local 加载
  render.py      Markdown → html|markdown + 导流公众号页脚（两级开关 mp_cta / name_wechat）
  history.py     publish_history.jsonl 的 per-channel 读写 + 幂等查询
  playwright_base.py  PlaywrightAdapter 基类（mode=playwright：持久化登录态 + 脚本驱动 DOM 直接发布；
                      公共 is_logged_in/_js_*/_paste_*/_extract_id 等都在这里，子类只写 selector + do_publish）
  browser.py     BrowserAdapter 基类（mode=browser：脚本只 prepare 发布包 + playbook，发布由 Claude-in-Chrome 驱动；现仅 oschina_web 用）
  adapters/      已注册 9 个渠道（公众号 + 8 个国内技术社区）：
    wechat.py        公众号（self_render，复用 wechat_publish.py）
    cnblogs.py       博客园（mode=api，MetaWeblog XML-RPC）
    oschina.py       开源中国：oschina（mode=api，MetaWeblog）+ oschina_web（mode=browser 兜底）
    csdn.py          CSDN（mode=playwright，markdown，name_wechat=False 禁「微信」字样）
    juejin.py        掘金（mode=playwright，markdown）
    zhihu.py         知乎（mode=playwright，html 富文本，mp_cta=False 不放公众号 CTA）
    segmentfault.py  思否（mode=playwright，markdown，name_wechat=False）
    aliyun.py        阿里云（mode=playwright，markdown，name_wechat=False，需先切 Markdown 模式）
  metaweblog.py  MetaWeblogAdapter 基类（cnblogs / oschina 共用的 XML-RPC 发布逻辑）
```

四类 adapter（`mode` + `self_render` 决定）：
- **api**（cnblogs / oschina）：框架 `render()` 出 html/markdown（含导流页脚）→ adapter 调 API 投递。
- **self_render**（wechat）：渲染与 API 深度耦合（外链图重托管 mmbiz、CSS 内联、封面、草稿箱），
  且公众号是导流终点不带自身 CTA，故跳过框架 render，直接调 `wechat_publish.publish_report()`。
- **playwright**（csdn / juejin / zhihu / segmentfault / aliyun）：无开放 API，但用 Playwright 持久化
  上下文复用「一次性手动登录」的会话、**固定代码驱动 DOM 直接发布**——一次 `--login`、之后一条命令
  一键发，不需 agent 盯屏幕。框架 `render()` 出内容后交给 adapter 的 `do_publish()`（见 playwright_base.py）。
- **browser**（oschina_web）：无开放 API 的 Claude-in-Chrome 兜底——脚本只 `prepare()` 出发布包
  （渲染内容 + 编辑器 URL + 字段 + playbook），实际发布由 agent 复用登录态驱动，发完 `--record` 回写历史。

**导流页脚两级开关**（按平台敏感度，在 adapter 上设）：
- `mp_cta=False`（知乎）：完全不放公众号 CTA，只留 canonical 回链——任何引导都易限流。
- `name_wechat=False`（CSDN/思否/阿里云）：CTA 保留账号名「{WECHAT_MP_NAME}」+「全网同名，搜一搜即达」，
  但不出现「微信公众号 / 微信」字样（平台禁/慎用）。
- 默认（掘金/开源中国/博客园）：完整「关注微信公众号「{name}」（全网同名，微信搜一搜即达）」。

设计原则（与现有管线对齐，不另起一套）：

- **slug** = 报告文件名 stem 小写（同 `wechat_publish.py` / `build_reports_index.py`）
- **canonical_url** = 站点报告页 `SITE_URL + PUBLIC_BASE_PATH + /reports/{slug}/`，
  作为 SEO 正本回链 + 导流落点（POSSE：自有站点是正本，外发只是 silo）
- **发布历史** = `src/data/publish_history.jsonl`（append-only SoR，入 Git），
  新增 `channel` / `post_id` / `url` 三个可选字段；`db.sqlite` 由 CI 据此重建
- **幂等** = 按 `(slug, channel)` 在 jsonl 查最近 `post_id`，有则 editPost、无则 newPost

## 用法

```bash
# 列出已注册渠道
python3 scripts/syndicate_publish.py --list

# dry-run：解析 + 渲染 + 判断新建/更新，不联网、不写历史（渲染结果落 tmp/）
python3 scripts/syndicate_publish.py src/analysis_report/1panel-dev_maxkb.md --channel cnblogs --dry-run

# 存草稿（默认，便于人工复核）
python3 scripts/syndicate_publish.py src/analysis_report/1panel-dev_maxkb.md --channel cnblogs

# 直接公开
python3 scripts/syndicate_publish.py src/analysis_report/1panel-dev_maxkb.md --channel cnblogs --publish

# 已发过会自动 editPost 更新；强制新建：
python3 scripts/syndicate_publish.py <report.md> --channel cnblogs --force-new

# 公众号（需先有同名 .meta.json，由 md2wechat 产出）；止于草稿箱，群发仍在后台人工
python3 scripts/syndicate_publish.py src/analysis_report/apache_superset.md --channel wechat --dry-run
python3 scripts/syndicate_publish.py src/analysis_report/apache_superset.md --channel wechat
```

### Playwright 渠道（csdn / juejin / zhihu / segmentfault / aliyun）

无开放 API，用 Playwright 复用「一次性手动登录」的持久化会话、脚本驱动 DOM 发布。
依赖：`pip install playwright && playwright install chromium`（本仓库 venv 已装）。
登录态落盘 `~/.syndicate/playwright/<channel>/`（不入 Git；`SYNDICATE_PW_DIR` 可改根位置）。

```bash
# ① 一次性登录（有头开浏览器，人工登录该平台；检测到登录态自动保存并关闭，无需回终端按回车）
python3 scripts/syndicate_publish.py --channel juejin --login

# ② 预演（dry-run + preview）：有头灌入标题/正文、停在「发布前」，验证 selector/登录态，不发布、不写历史
python3 scripts/syndicate_publish.py <report.md> --channel juejin --dry-run --preview

# ③ 存草稿 / 直接公开 / 强制新建（同其它渠道）
python3 scripts/syndicate_publish.py <report.md> --channel juejin
python3 scripts/syndicate_publish.py <report.md> --channel juejin --publish
python3 scripts/syndicate_publish.py <report.md> --channel juejin --force-new
```

环境变量：`SYNDICATE_LOGIN_TIMEOUT`（--login 轮询超时秒数，默认 300）、
`SYNDICATE_PW_HEADLESS=1`（发布走无头；selector 稳定后可无人值守，知乎建议先有头验剪贴板兜底）。

> selector 会随平台改版漂移。报「找不到元素」时用 `playwright codegen <editor_url>`
> 或在 `--preview` 暂停页用 DevTools 校准对应 adapter 的 `SEL_*` 常量。各平台登录 cookie 名
> （`LOGIN_COOKIES`）首次 `--login` 后建议在 DevTools→Application→Cookies 核对（思否尤其要确认）。

## 凭据（放 `.env.local`，不入 Git）

自动加载仓库根的 `.env.local` / `.env`（不覆盖已有环境变量）。

### 博客园 cnblogs

```ini
CNBLOGS_BLOGAPP=your-blog-id        # www.cnblogs.com/<blogapp>/ 里的那段
CNBLOGS_USERNAME=your-login-name
CNBLOGS_TOKEN=your-metaweblog-token # 后台「设置 → 博客设置 → MetaWeblog 访问令牌」，不是登录密码
# CNBLOGS_RPC_URL=...               # 可选，默认 https://rpc.cnblogs.com/metaweblog/<blogapp>
# CNBLOGS_CATEGORIES=[随笔分类]开源  # 可选，逗号分隔
```

### 开源中国 oschina（MetaWeblog API）

端点已探活：`https://www.oschina.net/action/xmlrpc`。**鉴权是账号登录名 + 登录密码**
（不是专用 token，与博客园不同）。若你用第三方（GitHub/微信/微博）登录而没设过密码，
先去开源中国账号设置里设一个密码。不想把登录密码落到 `.env.local` 的话，改用浏览器
路径 `--channel oschina_web`（复用浏览器登录态，不落密码）。

```ini
OSCHINA_USERNAME=your-login-name
OSCHINA_PASSWORD=your-login-password   # ⚠️ 登录密码本身，本机妥善保管
# OSCHINA_RPC_URL=...                  # 可选，默认 https://www.oschina.net/action/xmlrpc
# OSCHINA_BLOGID=...                   # 可选，newPost 的 blogid，默认用 username
# OSCHINA_BLOG_URL_BASE=https://my.oschina.net/u/1234567/blog  # 可选，文章 URL 前缀（写历史用）
# OSCHINA_CATEGORIES=开源,AI           # 可选，逗号分隔
```

> 首次真发建议先 `--dry-run` 看渲染，再 `--channel oschina`（默认存草稿，人工复核后公开）。
> 若 API 报错（blogid/URL 因账号而异），退回 `--channel oschina_web` 浏览器兜底。

### 微信公众号 wechat

复用现有公众号管线的环境变量（同 `scripts/wechat_publish.py`）：

```ini
WECHAT_APPID=...          # 必需
WECHAT_APPSECRET=...      # 必需
WECHAT_API_BASE=...       # 反代 base url（直连官方留空）
WECHAT_PROXY_TOKEN=...    # 反代鉴权 header
```

前置：报告需有同名 `.meta.json`（title/digest/author/theme），由 md2wechat 产出。
公众号止于「入草稿箱」，`--publish` 对它无效，群发上线仍在公众号后台人工完成。

### 导流页脚（所有外发渠道通用，公众号自身不带）

```ini
WECHAT_MP_NAME=你的公众号名          # 渲染时追加「全网同名，微信搜一搜即达」CTA
# SITE_URL / PUBLIC_BASE_PATH 复用站点约定，决定 canonical 回链
```

## 报告 frontmatter（可选）

报告无需 frontmatter 也能发（标题取首个 H1、来源取 `> GitHub:` 行、canonical 自动推导）。
需要覆盖时可在 md 顶部加 YAML frontmatter：

```yaml
---
title: 自定义标题
tags: [AI, RAG]
canonical_url: https://example.com/custom    # 覆盖默认 canonical
syndicate: false        # 该篇不外发；或 [cnblogs] 仅发指定渠道
---
```

## 新增一个 adapter

1. 在 `adapters/` 下新建 `<platform>.py`，写 `BaseAdapter` 子类：
   - `name` / `content_format`（`'html'` 或 `'markdown'`）
   - `check_auth()` 校验凭据
   - `publish(article, rendered, *, publish, existing_post_id)` 返回 `PublishResult`
   - 类上加 `@register`
2. 在 `adapters/__init__.py` import 它
3. 凭据加进本 README + `.env.local`

## 与现有公众号管线的关系

- 公众号已迁成 `wechat` adapter：CLI 内部调 `wechat_publish.publish_report()`，
  复用其图片重托管/CSS 内联/封面/草稿箱逻辑（未重写）。`wechat_publish.py` 的
  独立 CLI（`python3 scripts/wechat_publish.py <md>`）契约不变，CI 自动分析与
  ali-demo runner 仍可照常调用。
- CI 自动分析记录历史仍走 `src/scripts/record_publish.py`（channel 隐式 = wechat）；
  本 adapter 是「统一调度」下的等价手动/本地路径，两者都写
  `publish_history.jsonl(channel=wechat)`，不冲突。
- DB 里 `v_publish_latest` 已收窄为「仅 wechat」，其它渠道记录不会污染
  `reports.published_*`（= 公众号发布状态）；多渠道状态查 `v_publish_channel_latest`。
- 现状：9 个渠道接入。**api**：公众号 / 博客园 / 开源中国（MetaWeblog）；
  **playwright**（持久化登录 + 脚本驱动）：CSDN / 掘金 / 知乎 / 思否 / 阿里云；
  **browser**（Claude-in-Chrome 兜底）：开源中国兜底(oschina_web)。腾讯云不集成（已有其他方案）。

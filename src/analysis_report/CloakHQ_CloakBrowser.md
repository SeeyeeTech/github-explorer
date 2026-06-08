# 24K star 的 CloakBrowser：号称通过所有 bot 检测，开源的却只是外壳、补丁闭源

> GitHub: https://github.com/CloakHQ/CloakBrowser

## 一句话总结

商业组织 CloakHQ 用 3.5 个月做到 24K star 的反检测「隐身 Chromium」——作为 Playwright/Puppeteer 的 drop-in 替代，号称用源码级 C++ 指纹补丁通过所有 bot 检测（Cloudflare/reCAPTCHA/fingerprintJS）。但代码层面坐实了一个关键事实：决定隐身效果的 58 个 C++ 补丁全在一个闭源、禁逆向、运行时下载的预编译二进制里，这个 MIT 开源仓库只是「SDK 包装层 + 二进制下载器 + 拟人化层」；而独立基准与高热 issue 都表明，「通过所有检测」是某时间点对某测试集的快照，逃不过与检测器的军备竞赛。

## 值得关注的理由

1. **一个戳破营销话术的诚实拆解样本**：项目主打「passes every bot detection test / 30-30」，但 issue #193（被 fingerprintJS 检测到，40 评论最热）、#208（被 Servicepipe 近 100% 抓出）、以及独立基准（Paterson：31 个 Cloudflare 目标仅 26/31、与 6MB 的 curl_cffi 打平、落后 nodriver 28）共同说明：反检测是结构性的猫鼠军备竞赛，任何「全过」都是时点性快照。这是观察「反检测赛道营销叙事 vs 工程现实」的好窗口。
2. **「开源外壳 + 闭源内核」的 open-core 边界标本**：`find` 全仓零 C/C++ 补丁源码——真正的价值（编译进二进制的指纹补丁）以自定义 License 闭源下发（#50 索要源码被关闭，禁逆向/禁分发/OEM 收费条款已写）。称其为「开源反检测工具」并不准确，更接近「开源外壳的闭源产品」。这是研究商业组织如何用免费开源做流量/品牌占位的典型案例。
3. **真正可学的工程在外壳层**：拟人化行为引擎（三次贝塞尔鼠标 + QWERTY 邻键打字错-退格-纠正 + 滚动 inertia）、CDP Isolated-World 隐身 DOM 求值 + trusted-event、代理 URL 凭据再编码、二进制分发的供应链卫生（原子写 + 路径穿越防护 + SHA256/GPG/Sigstore）——这些与「反检测」可解耦的工程技巧，是本仓库真正开源、可独立复用的部分。

## 项目展示

![CloakBrowser](https://i.imgur.com/cqkp6fG.png)

> 项目 hero 图（README 截图托管于 imgur 外链，发布前需复核可用性）。

> reCAPTCHA v3 得分 0.9（vs 原生 Playwright 0.1）、Cloudflare Turnstile 通过等检测结果截图见 README；均为 imgur 外链、未经校验。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/CloakHQ/CloakBrowser |
| Star / Fork | 24,663 / 1,969 |
| 代码行数 | 27,116 行（Python 48% SDK 层 + TypeScript 38.6% 平行 JS-SDK + JSON 10%）|
| 项目年龄 | 3.5 个月（2026-02-22 起，与组织账号同日诞生）|
| 开发阶段 | 密集开发（53 tag / 3.5 月 ≈ 两天一发，追检测器的军备竞赛节奏）|
| 贡献模式 | CloakHQ 商业组织（匿名无署名，主作者占 ~78%，跨时区团队连续作业）|
| 热度定位 | 大众热门 · 爆发型话题项目（3.5 月 0→24.6K star）|
| 质量评级 | 代码[良好] 文档[优秀] 测试[基本] |

> License 双轨：包装层 MIT，但运行时下载的补丁 Chromium 二进制受自定义 BINARY-LICENSE（禁再分发/禁逆向/禁修改，SaaS/OEM 需另购授权）。

## 作者视角：为什么存在这个项目

### 创始人/作者背景

由 **CloakHQ 组织** 维护——一个匿名、无个人署名、与产品同日（2026-02-22）建号的**商业实体**，官网 cloakbrowser.dev，配套产品 CloakBrowser-Manager（「免费自托管 Multilogin 替代」，634 star），并 fork 了 crawl4ai/crawlee 等赛道项目。运营节奏（每日推送、53 tag、bounty 悬赏、独立官网）明显是职业化团队而非个人爱好者。这是一个**专为反检测赛道成立的运营型组织**。

### 问题判断

作者的核心论点：自动化被识破的根因是**指纹层**（navigator.webdriver、SwiftShader 渲染器、headless UA、CDP 信号、canvas/WebGL/audio 噪声、TLS ja3/ja4）与**行为层**（瞬移鼠标、零延迟填表）双双露馅。现有方案（playwright-stealth/undetected-chromedriver/puppeteer-extra）走 JS 注入或 flag 调整，每次 Chrome 升级即失效、且「补丁本身可被检测」。时机上踩中 2025-26 AI Agent 爆发——「能稳定访问受保护站点的浏览器」成为 Agent 基础设施刚需（README 把 browser-use 等框架放显眼位置），作者瞄准的是「给 AI Agent 当隐身底座」这个新增量。

### 解法哲学

- **下沉而非贴皮**：把指纹对抗放到二进制层（编译进 Chromium），拒绝 JS 注入/flag 路线。代码里反复出现「locale/timezone 走二进制 flag（`--fingerprint-timezone`）而非 Playwright 的可被 CDP 观测的 emulation」。
- **零迁移成本优先**：drop-in 替换是第一卖点（仅改 import），`launch()` 返回原生 Playwright Browser 对象、不包新类型。
- **明确不做**：不内置打码、不内置代理轮换（「不解决 captcha，而是让它不出现」「自带代理」）；定位「浏览器环境」而非「自动化服务」。
- **开放策略 = open-core**：包装层 MIT、内核闭源（#50 边界证据）。「用免费开源做品牌/流量占位、变现口子（OEM/SaaS license）已在 BINARY-LICENSE 写好但未开闸」。

### 战略意图

核心产品（补丁 Chromium 二进制）是闭源资产，本仓库是其**获客与生态适配层**。商业化结构（BINARY-LICENSE 的 OEM/SaaS 条款、捐赠、CloakBrowser-Manager）已铺好，当前「完全免费」是占位期策略。

## 核心价值提炼

### 「开源的是什么、闭源的是什么」

- **开源（MIT）**：Python SDK（PyPI）+ TS SDK（npm）双平行镜像的包装层、补丁二进制的下载器、拟人化行为层、geoip/widevine 辅助。
- **闭源（自定义 License 二进制）**：决定隐身效果的 58 个源码级 C++ 指纹补丁（canvas/WebGL/audio/fonts/GPU/screen/WebRTC/CDP），编译进从 cloakbrowser.dev 下载的 ~200MB 预编译 Chromium，禁逆向/禁分发。`find` 全仓零 `.c/.cc/.cpp/.patch` 文件证实。

### 创新之处（本仓库真正开源、可学习的部分）

1. **CDP Isolated-World + Trusted-Event 的隐身行为执行**（新颖度 4/5）：DOM 判定走 `Page.createIsolatedWorld` 隔离上下文（无 `eval at evaluate` 栈痕、对主世界猴补丁不可见），关键按键走 CDP `Input.dispatchKeyEvent` 产生 `isTrusted=true` 事件，随导航自动失效重建。
2. **拟人化行为引擎**（新颖度 3/5，可迁移 4/5）：鼠标三次贝塞尔 + 法向 wobble + 概率 overshoot 回弹；键盘 per-char 抖动 + 思考停顿 + 基于 QWERTY 邻键表的打字错-退格-纠正；滚动 accelerate→cruise→decelerate + inertia 分块；参数集中在不可变 `HumanConfig` dataclass（default/careful 预设 + per-call override）。这是区别于闭源 C++ 补丁、可独立复用的反检测能力。
3. **「一致身份」geoip 绑定**（新颖度 3/5）：解析代理**出口 IP**（经代理打 ipify，而非网关），由 country→BCP47 locale、MaxMind→timezone，并复用同一出口 IP 做 WebRTC ICE 候选——抓住「风控真正抓的是信号间不一致」这一本质。
4. **deadline 贯穿的拟人化超时传播**（新颖度 2/5）：把单个 timeout 转成绝对 deadline 贯穿 actionable→scroll→stable→click 全链，保证「慢动作」不突破总预算。

### 可复用的模式与技巧

- **原子写 + 路径穿越防护的二进制分发**：temp→rename 落位、tar/zip 拒绝 `..`/绝对软链、SHA256 校验、主源 + GitHub 回退、GPG/Sigstore attestation——任何下载并执行预编译产物的工具都该照抄这套供应链卫生。
- **幂等猴补丁 vendored 类**：模块级 + 实例级守卫标记避免重复打补丁与无限递归，并保留 `_original` 旁路。
- **CDP Isolated World 做隐身/干净 DOM 求值**：避免污染主世界、不留 evaluate 栈痕。
- **代理 URL 凭据 decode→re-encode（`quote(unquote, safe="")`）**：穿过下游解析器对特殊字符（`=` 等）的截断。
- **best-effort 永不阻断主流程**：geoip/widevine/update 全程 try/except + 降级日志，绝不让辅助能力失败打断 launch。

### 关键设计决策

| 决策 | 解决的问题 | Trade-off | 可迁移性 |
|------|-----------|-----------|---------|
| 指纹/时区/locale 走二进制 CLI flag，抑制会泄露的 Playwright 默认参数 | Playwright 的 CDP emulation 可被检测、默认参数暴露 webdriver/SwiftShader | 不可被 CDP 观测的一致性，但几乎所有隐身价值都依赖那个闭源二进制 | 低 |
| drop-in 猴补丁而非封装新 API | 让用户仅改 import | 零学习成本，但强依赖 Playwright 内部实现、版本升级易碎 | 中 |
| 拟人化用 CDP Isolated World + trusted-event | `page.evaluate` 留栈痕、合成事件 isTrusted=false | 行为可信度提升，代价是直接操作 CDP 内部、脆性上升 | 中-高 |
| 自带下载器 + 强供应链校验 | 分发大体积闭源二进制需防篡改/穿越 | 工程量大但必要 | 高 |
| Python/TS 双 SDK 严格平行镜像 | 同吃 Python 爬虫与 Node Agent 两生态 | 2× 维护成本 + 行为漂移风险 | 中 |

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | CloakBrowser | nodriver | Camoufox | Patchright |
|------|--------------|----------|----------|------------|
| 路线 | 源码级 C++ 补丁（闭源二进制）| CDP 直驱 | Firefox 引擎级伪造 | patched Playwright（JS/协议层）|
| API | Playwright/Puppeteer drop-in | 自绘 CDP 客户端 | 自有 | Playwright 兼容 |
| 开源 | 外壳 MIT / 内核闭源 | ✅ 纯开源 | ✅ | ✅ |
| 独立基准(Cloudflare) | 26/31 | **28/31（最高）** | DataDome 强 | 中 |
| 负担 | 下载 ~200MB 黑盒二进制 | 轻 | 跨引擎 | 轻 |

### 差异化护城河

**技术护城河主要锁在不开源的二进制里**（闭源 C++ 补丁 + drop-in 工程化 + 拟人化层）+ 生态护城河（AI Agent 框架适配 + 双 SDK + Manager）。开源仓库本身护城河薄。

### 竞争风险

最可能被 nodriver（独立基准通过率更高 28/31、纯开源、无黑盒二进制）从下方蚕食，被 Camoufox（引擎级一致性）从深度侧挤压。**检测器一次升级即可让某版本「30/30」失效**（#193 fingerprintJS、#208 Servicepipe 近 100% 抓出）——这是赛道结构性宿命，README FAQ 也自认「Bot detection is an arms race」。Patchright 甚至被 CloakBrowser 自己当可选后端集成（`backend="patchright"`），侧面承认其价值。

### 生态定位

AI Agent / 爬虫的「隐身浏览器底座」候选之一，靠 drop-in 工程体验和品牌运营占位，而非靠实测领先。整体反检测是红海 + 军备竞赛赛道，护城河随检测器升级持续衰减。

## 套利机会分析

- **信息差**：并非被低估，而是已充分曝光甚至被热度透支。套利窗口不在「发现冷门」，而在「提供冷静的技术拆解」——戳破「passes every test」营销话术与真实军备竞赛之间的张力、揭示「开源外壳 + 闭源内核」的真实结构、客观陈述双用途与合规风险。
- **技术借鉴**：拟人化行为引擎、CDP Isolated-World 隐身、代理凭据再编码、二进制分发供应链卫生、幂等猴补丁——这些与「反检测」可解耦的工程技巧可迁到任何浏览器自动化/二进制分发场景。
- **生态位**：填补「Playwright drop-in 的源码级隐身浏览器」位，但闭源二进制 + 独立基准边际优势使其壁垒不稳。
- **趋势判断**：AI Agent 对「能稳定访问受保护站点的浏览器」需求真实增长，但反检测的护城河天然随检测器升级蒸发；且 nodriver 等纯开源方案实测更强。CloakBrowser 能否守位取决于补丁迭代速度与品牌运营，而非不可复制的技术。

## 风险与不足

- **「开源」名实落差**：仓库 MIT 的只是包装/下载/拟人化层；决定隐身效果的 C++ 补丁是闭源二进制（禁逆向/禁分发、#50 拒绝公开、OEM 收费条款已写）。
- **军备竞赛是结构性宿命**：任一时点「全过」只是对某测试集的快照（#193 fingerprintJS、#208 Servicepipe 近 100% 抓出），README 自认 arms race。
- **裸隐身优势边际**：独立基准 26/31、与 6MB 的 curl_cffi 持平、落后 nodriver；很多拦截源于代理/字体/headless 而非指纹，需 headed + 住宅代理 + geoip + humanize 叠加才行。
- **平台不均衡**：macOS 钉在 Chromium 145、仅 26 个补丁，Linux/Windows 已 146、58 个补丁；macOS 构建一度停摆约两月。
- **强绑定不可审计的专有二进制**：默认下载并执行 ~200MB 黑盒二进制（虽有 SHA256/GPG/Sigstore 验证供应链，但内部对用户黑盒）。
- **双用途与合规**：反检测能力天然双用途——合法用途（测试自家反爬、可访问性审计、合规存档、AI agent 自动化、自有账号管理）与灰色/违规用途（大规模未授权抓取、绕过付费墙/风控、薅羊毛/欺诈）并存。**绕过 bot 检测与 captcha 通常违反目标站 ToS、存在法律灰区**；BINARY-LICENSE 的 Acceptable Use 明确禁止未授权访问/撞库/批量注册并要求用户自负其责。使用须受目标站 ToS 与当地法律约束。

## 行动建议

- **如果你要用它**：仅在**合法授权场景**下（测试自家站点的反爬、自有账号自动化、合规研究、可访问性审计）才考虑；务必先确认目标站 ToS 与当地法律。技术上若要 Playwright drop-in 体验可一试，但要 Cloudflare 通过率/纯开源/轻量，nodriver 实测更强；要 Firefox 引擎级一致性选 Camoufox；要零黑盒选 Patchright。注意它下载的是闭源二进制。
- **如果你要学它**：跳过闭源补丁（不在仓库内），重点读 `cloakbrowser/human/`（拟人化引擎：mouse.py 贝塞尔 + keyboard.py 打字纠错 + scroll.py inertia）、`download.py`（二进制分发供应链卫生）、CDP Isolated-World 隐身技巧、`browser.py` 的幂等猴补丁。这些是可独立复用的工程。
- **如果你要 fork 它**：核心价值在闭源二进制里、无法 fork 出隐身能力。可借鉴的是拟人化层、下载器卫生、猴补丁模式，迁到自己的浏览器自动化项目。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/CloakHQ/CloakBrowser（已收录，含架构/API/stealth 机制）|
| Zread.ai | 未验证（返回 403）|
| 关联论文 | 无（工程项目）|
| 官网 | [cloakbrowser.dev](https://cloakbrowser.dev/)（产品介绍页）|
| 独立基准/评测 | [Anti-detect browser benchmark 2026 — Ian L. Paterson](https://ianlpaterson.com/blog/anti-detect-browser-benchmark-patchright-nodriver-curl-cffi/)（26/31、与 curl_cffi 打平的反方证据）· [CloakBrowser Review — andrew.ooo](https://andrew.ooo/posts/cloakbrowser-stealth-chromium-playwright-replacement-review/) |
| 第三方实测仓库 | [techinz/browsers-benchmark](https://github.com/techinz/browsers-benchmark) |

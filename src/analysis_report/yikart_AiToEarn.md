# 1.9 万 star 的 AiToEarn：一文发遍 14 平台，把 Claude Code 搬进了后端

> GitHub: https://github.com/yikart/AiToEarn

## 一句话总结

AiToEarn 是一个 MIT 开源的「AI 内容营销 Agent」桌面+云端平台，把创作（Create）、一键多平台发布（Publish）、互动（Engage）、变现（Monetize）串成闭环，15 个月攒下 1.9 万 star——技术上最值得拆解的是它的「双路径发布架构」和直接把 Claude Agent SDK 搬进生产后端做内容生成。

## 值得关注的理由

1. **双路径发布架构是该品类的最优工程解**：14+ 平台里有开放 API 的（抖音/B站/YouTube/Meta/TikTok…）走官方 OAuth，没有开放 API 的（小红书/视频号）只在 Electron 桌面端用浏览器自动化——「有 API 走 API、没 API 走客户端」这套蓝图，是所有多平台分发工具都绕不开的范式。
2. **把 Claude Code 整套搬进 SaaS 后端**：用 `@anthropic-ai/claude-agent-sdk` + `@musistudio/claude-code-router`（路由到便宜模型控成本）+ 进程内 MCP 工具 + `SKILL.md` 技能，做多租户内容生成 Agent，还叠了预算上限、credits 计量、分布式锁——这是非常前沿且可直接复用的生产级 Agent 后端范式。
3. **教科书级的 open-core 商业飞轮**：开源客户端获客 → Relay 凭据中继托管难搞的 OAuth/合规环节 → 内容变现市场抽成结算。开源是入口，商业锚点设计得极巧妙。

## 项目展示

![变现总览](https://raw.githubusercontent.com/yikart/AiToEarn/main/presentation/monetize-cn.png)

变现总览：创作者接 CPS/CPE/CPM 推广任务，按结果结算（云端变现市场，open-core 的商业层）。

![一键发布界面](https://raw.githubusercontent.com/yikart/AiToEarn/main/presentation/publish-cn.png)

一键多平台发布界面——一条内容分发到抖音/快手/小红书/视频号/B站等国内外 14+ 平台。

![多渠道账号管理](https://raw.githubusercontent.com/yikart/AiToEarn/main/presentation/channel-cn.png)

多渠道/多账号矩阵管理，是自媒体矩阵运营的核心场景。

![OpenClaw 执行赚钱任务](https://raw.githubusercontent.com/yikart/AiToEarn/main/presentation/openclaw-earn-demo.png)

联动 OpenClaw 浏览器 Agent 自动执行 AiToEarn 赚钱任务，体现向 Agent 化演进。

![Create 创作](https://raw.githubusercontent.com/yikart/AiToEarn/main/presentation/display-1.5.2png.png)

AI 创作（Create）界面，内容生成由 Claude Agent SDK 驱动。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/yikart/AiToEarn（官网 https://aitoearn.ai/） |
| Star / Fork | 18,955 / 2,924（Watcher 417、open issues 21、open PR 4） |
| 代码行数 | 513,269 行 / 2,791 文件（monorepo；TypeScript+TSX 约 45% 为主力，叠 JSON 17% 多语言 i18n、YAML 7.8%、CSS/Sass 9%） |
| 项目年龄 | 15.3 个月（2025-02-26 首次提交，最近推送 2026-05-21 / v2.4.0） |
| 开发阶段 | 稳定维护（实质降温：月提交从峰值 ~540 跌至近 30 天仅 13、近 90 天 41） |
| 贡献模式 | 商业团队主导 + 社区（29 名贡献者，Top 占 43%，主作者约 19.7%） |
| 热度定位 | 大众热门、爆发型增长（约 1,260 star/月，近期仍在出圈） |
| 质量评级 | 代码[良] 文档[中上] 测试[差] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

yikart（「爱团团」团队）是中国商业创业团队，GitHub Organization 几乎为 AiToEarn 这一爆款而生（组织其余仓库 star 均为个位数）。这不是个人极客的 hobby，而是专业团队的产品——29 人贡献、27 个 release、严格语义化版本、约每 17 天一发，工程成熟度足。打法是典型的「开源引流 + 商业闭环」。

### 问题判断

团队自身做自媒体矩阵运营，是真实 dogfooding：把「一人维护几十个平台账号、一条内容手动发十几遍」的体力活产品化。更深的判断是——创作、分发、互动、变现这四件事在现有工具链里是割裂的，没有人把它们串成一个 Agent 闭环。从 README 更新日志能看到清晰的演进线：2025-02 起步于「一键发抖音/小红书/快手/视频号」→ 加海外平台 → 加 AI 创作 → 2025-12「All In Agent」→ 2026-03 内容变现市场 + MCP/OpenClaw 集成。

### 解法哲学

核心是 **open-core + 双形态客户端**，明确选择「不做什么」：
- **桌面客户端真开源**（MIT），作获客入口，靠浏览器自动化覆盖没有开放 API 的平台；
- **云端后端 + Relay 作变现锚点**：把 14 个平台的开发者凭据集中托管在 Relay 服务器，自托管者填一个 API Key 就能「借用」官方凭据发布——既是巨大便利，也是把用户黏在官网账号体系的钩子；
- **不自建内容算法分发、不做粉丝增长黑产**，变现走「结果导向」的 CPS/CPE/CPM 任务市场撮合结算。

### 战略意图

闭环非常清晰：开源客户端获客 → 引导注册官网账号拿 API Key → 用 Relay/云端能力（省去自注册开发者）→ 接入变现市场赚钱（平台抽成）。Agent 化方向明确：自建 Create Agent（Claude Agent SDK）、通过 MCP 把 AiToEarn 变成任意 Agent 的「发布+变现工具」、联动 OpenClaw 浏览器 Agent 接单干活——即从「给人用的工具」升级为「给 Agent 用的能力底座」。

## 核心价值提炼

### 创新之处

1. **双路径发布架构（API 云端 + 浏览器自动化桌面）** — 按平台是否开放 API 自动选择发布通道，是「既要合规稳定、又要全覆盖」矛盾的最优工程解。证据：后端 `PUBLISHING_PROVIDERS` 注册表覆盖 13 个有 API 的平台，唯独没有小红书和视频号——这两个只在 Electron 端用浏览器自动化实现。新颖度 3/5、实用性 5/5、可迁移性 5/5。
2. **Claude Agent SDK + Claude Code Router 做多租户内容生成后端** — 把本是 IDE 内 coding agent 的 Claude Code 整套（Agent SDK / MCP / SKILL.md / Router 模型路由）搬进 SaaS 后端，用 Router 切到便宜模型控成本，叠 credits/预算/Redlock。新颖度 5/5、实用性 4/5、可迁移性 5/5。
3. **Relay OAuth 凭据中继** — 用一台中继服务器集中托管 14 平台开发者凭据，自托管者一个 API Key 即可发布，把 open-core 的「难搞合规部分」做成商业锚点。新颖度 4/5、实用性 4/5、可迁移性 3/5。
4. **session partition 多账号 cookie 隔离 + 私有 web API 回放** — Electron 原生 partition 干净隔离同平台多账号会话，登录窗口轮询 cookie 直到收割成功落本地 sqlite，后续带 cookie + 伪造 Referer/UA 调平台私有 web API。新颖度 2/5、实用性 4/5、可迁移性 3/5。

### 可复用的模式与技巧

1. **策略表 + 抽象基类（Strategy Registry）**：用 NestJS DI 工厂把 `Record<枚举, 实现>` 注入为一个令牌，上层按枚举 O(1) 路由，新增平台只写一个 provider + 注册一行——任何「多供应商/多渠道」分发通用。
2. **「立即执行 vs 入队延迟」时间窗判定**：`publishTime <= now + 容忍秒数` 决定走立即发布还是定时入队，统一即时发布与日历排期。
3. **回调 + 主动核对双保险（Watchdog）**：平台 webhook 回调为主，定时扫描 stale 任务调 `verifyAndCompletePublish` 兜底，避免回调丢失导致任务永久挂起。
4. **Agent SDK + Router 子进程 + 进程内 MCP**：把私有能力包成 `createSdkMcpServer` 工具、用 Router 切模型、SSE 向前端流式推送状态——生产级 Agent 后端范式。
5. **Electron partition 做多账号会话沙箱**——桌面端多租户/多账号自动化通用。

### 关键设计决策

- **统一发布抽象**：抽象基类 `PublishService`（模板方法 `immediatePublish`/`verifyAndCompletePublish`/`finalizePublish`）沉淀公共能力（入队、媒体暂存与轮询、发布记录状态机、文案+话题拼接），各平台 provider 只实现差异部分，通过 DI 注册表运行时路由。抖音被特判为「立即发布」是抽象里的务实例外。
- **三层 monorepo**：`aitoearn-backend`（Nx + NestJS 双 app：server 管账号/发布/变现/Relay/MCP，ai 管 Agent/生成）+ `aitoearn-web`（Next.js App Router 多语言）+ `aitoearn-electron`（Electron + better-sqlite3，各平台浏览器自动化）。根 `docker-compose.yml` 一键拉起 10 个服务。
- **标准 SaaS 后端范式迁移**：BullMQ 队列 + MongoDB + Redis + Redlock 分布式锁 + 对象存储（rustfs/S3/阿里 OSS）。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | AiToEarn | social-auto-upload | 易媒助手（商业） | postiz | MoneyPrinterTurbo |
|------|----------|--------------------|------------------|--------|-------------------|
| 体量 | 1.9w★ MIT | ~11k★ 开源 | 闭源 SaaS | ~31k★ AGPL | ~80k★ 开源 |
| 平台覆盖 | 国内+海外 14+ | 国内几家 | 国内 70+ | 海外为主 | 不做分发 |
| AI 创作 | ✅ Agent | ❌ | ❌ | 部分 | ✅（只生成） |
| 变现闭环 | ✅ 任务市场 | ❌ | 部分 | ❌ | ❌ |
| 定位 | 开源 Agent 平台 | 个人脚本 | 国内矩阵 SaaS | 海外社媒调度 | AI 短视频生成 |

### 差异化护城河

① 「双路径发布 + 14 平台（含国内无 API 平台）」的覆盖广度，脚本和海外工具都不具备；② open-core 闭环（开源获客 → Relay 凭据托管 → 变现市场）形成的商业飞轮与账号黏性；③ Agent 化生态卡位（自建 Create Agent + 对外开放 MCP + OpenClaw 联动），把自己做成「Agent 时代的内容发布/变现能力底座」。

### 竞争风险

① 浏览器自动化路径对平台改版/风控极度脆弱，维护是长期负担；② 合规/法律风险（见下文）；③ 真正的变现能力其实在闭源云端（Relay + 任务市场），开源部分是「客户端 + 发布引擎」，纯开源信仰者难以复刻其商业模式；④ 大厂或易媒等若补齐 AI 能力可快速追赶国内场景。

### 生态定位

国内目前唯一「开源 + 国内外全覆盖 + AI Agent 创作 + 变现闭环」的内容营销 Agent 平台，定位介于「开源工具」与「商业 SaaS」之间的 open-core 龙头。与 MoneyPrinterTurbo（只做生成）属互补——README 里 AiToEarn 也把它列为推荐的上游生成器。

## 套利机会分析

- **信息差**：18,955 star / 仅 15 个月、且当下仍在爆发，命中「AI 赚钱 + 自媒体矩阵 + 开源」三个中文读者爽点，公众号选题热度极高。但需诚实点出剪刀差——star 暴涨发生在末次代码提交（2026-05-21）之后，开源仓库活跃度已落后于热度，重心疑似转向云端商业产品。
- **技术借鉴**：「双路径发布架构」「Claude Agent SDK + Router 做生产后端」「策略表 + 队列 + 看门狗的异步发布工程化」三项可直接迁移到任何多渠道分发/AI 后端项目（与本类一文多发场景尤其契合）。
- **生态位**：填补了「开源 + 国内外全平台 + AI 创作 + 变现」一体化的空白。
- **趋势判断**：踩在「Agent 化 + 内容变现」两个上升趋势上，MCP/OpenClaw 集成具备后发卡位优势；但要警惕浏览器自动化路径的可持续性。

## 风险与不足

- **测试覆盖差**：约 28 个 spec / 897 后端文件（约 3%），web 端 0、Electron 端 1，核心浏览器自动化路径几乎无测试；CI 有 lint+build 闸门但无测试闸门、Electron 无 CI。
- **代码注释偏低**（约 9.8%），Electron 逆向代码较「脏」（硬编码 token、超长文件，如抖音 2610 行、视频号 1531 行）。
- **硬编码密钥**：`demo/xhs/signature.js` 内置了小红书合作方 appKey/appSecret 与 SHA256 签名算法（既是合规问题也是密钥泄露隐患）。
- **合规/法律风险（该品类系统性风险）**：
  - **平台 ToS 违反（高）**：对小红书/视频号/抖音/快手通过「收割登录 cookie + 伪造 Referer/UA + 调平台私有 web API（如 `edith.xiaohongshu.com/web_api/...`）」发布，几乎必然违反这些平台的开发者与用户协议。
  - **账号风控/封号（高）**：自动化批量发布/点赞/关注/评论极易触发风控，风险转嫁给终端用户。
  - **评论挖掘 + 自动私信引导成交（中）**：可能触及平台导流/营销违规与骚扰边界。
  - **变现合规（中）**：CPS/CPE/CPM 任务结算涉及广告标注、资金结算、跨境（.cn vs .ai 双环境）数据与外汇合规。
  - **缓释观察**：团队刻意把浏览器自动化放在用户本机桌面端而非云端（降低集中风控暴露面）、官方 API 平台走 Relay 合规凭据，说明对风险有意识切分；但「无开放 API 平台」这条线的法律风险无法根除。

## 行动建议

- **如果你要用它**：需要国内外全平台一键矩阵发布 + AI 创作 + 想做内容变现——AiToEarn 是目前开源里覆盖最全的。但要清楚自动化发布对账号有封禁风险，建议先用小号试、控制频率。只需轻量国内视频上传脚本选 social-auto-upload；纯海外社媒排期选 postiz；只做 AI 短视频生成选 MoneyPrinterTurbo。
- **如果你要学它**：重点读 `project/aitoearn-backend/.../channel/publishing/`（双路径发布核心 `publishing.service.ts`/`base.service.ts`）；官方 API 范例看 `libs/douyin/douyin-api.service.ts`；Agent 后端看 `aitoearn-ai/.../agent/services/agent-runtime.service.ts` + `claude-code-router.service.ts` + `skills/*/SKILL.md`；浏览器自动化与多账号隔离看 `aitoearn-electron/electron/plat/xiaohongshu/index.ts` 与 `BrowserWindowItem.ts`。
- **如果你要 fork 它**：可改进方向是补关键路径测试、给 CI 加测试闸门与 Electron CI、清理硬编码凭据；但 Relay/变现市场是闭源云端，fork 出来只能得到「客户端 + 发布引擎」，复刻不了商业闭环。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/yikart/AiToEarn（已收录） |
| Zread.ai | 未确认（返回 403） |
| 关联论文 | 无 |
| 在线 Demo | 官网 https://aitoearn.ai/ 即产品入口；README 内嵌 YouTube 演示视频 |

# Vercel 这个 agent 模板，21% 提交是 bot 写的

> GitHub: https://github.com/vercel-labs/open-agents

## 一句话总结

Vercel Labs 出品的「后台编码 agent」开源参考应用——fork 一下、几分钟就能拥有一个跑在云端、能改代码并自动开 PR 的自托管 agent；它最有说服力的「能用」证据，是这个仓库自己约 21% 的提交由它孵化的 agent bot 写就。

## 值得关注的理由

- **「background coding agent」品类的官方开源范本**：不是又一个通用 agent 框架，而是 Vercel 把自家 Sandbox / AI SDK / AI Gateway / Workflow SDK 串成的一个完整产品参考应用，明确「meant to be forked and adapted, not treated as a black box」。5 个月冲到 5608 star、大众热门、官方背书。
- **鲜明的架构论点「the agent is not the sandbox」**：agent 不在执行 VM 内运行，而是三层解耦 `Web → Agent workflow → Sandbox VM`，agent 在沙箱外通过 file/search/shell 等工具与之交互。这个取舍既是卖点也有争议（见下文 InfoQ 的反方意见），值得工程师拆解。
- **罕见的「agent 写 agent」自举闭环**：两个机器人 `openharness[bot]`（317 提交）+ `open-agents-bot[bot]`（66 提交）合计约 21% 的提交，是产品本身在自己仓库里干活；`skills-lock.json` 像锁依赖版本一样锁定 AI 能力来源——这是一个把自己当协作者来开发的项目。

## 项目展示

> README 与官网均无可直接策展的产品截图/演示视频（README 极简，仅一个「Deploy with Vercel」按钮）。建议配图借用项目 GitHub OpenGraph 卡片，或自行截取 open-agents.dev 落地页与 session/git-panel 界面。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/vercel-labs/open-agents |
| Star / Fork | 5608 / 730 |
| 代码行数 | 132K（真实应用代码 TS+TSX 67.6%；JSON 25% 实为 Drizzle ORM 迁移快照，非业务代码；YAML 为 lockfile） |
| 项目年龄 | 5.4 个月（2025-12-26 起） |
| 开发阶段 | 曾密集冲刺、4 月见顶后断崖降速（近 30 天仅 10 commit，已切到维护期） |
| 贡献模式 | 单人主导 + 机器人协作（主作者 Nico Albanese 合并双 git 身份约 64%；两个 agent bot 占 ~21%） |
| 热度定位 | 大众热门（官方背书，非被低估的冷门） |
| 质量评级 | 代码[良好·边长功能边重构] 文档[优·含给 agent 看的 living docs] 测试[有·核心路径有 route.test/git.test/models.test] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

org 是 **Vercel Labs**（Next.js 创造者、7163 followers 的官方实验室），但真正的主笔是 **Nico Albanese（`nicoalbanese`）**——Vercel 的 AI/DevRel 工程师、Vercel AI SDK 生态的知名布道者，他以 `nicoalbanese` + `Nico Albanese` 两个 git 身份合计贡献了 >60% 的提交。这个背景决定了项目气质：它不是研究脚手架，而是一个**用来「带货」自家 AI 基建的、打磨到产品级的参考实现**。

### 问题判断

2026 年初，「后台/云端编码 agent」（Devin、Cursor background agents、GitHub Copilot coding agent）正成为热点，但它们大多闭源、跑在厂商基建上、不可改。Vercel 看到的机会是：自己手里恰好有做这件事所需的全部积木——隔离沙箱（Sandbox）、多模型统一 API（AI SDK）、模型路由/可观测（AI Gateway）、可恢复的多步执行（Workflow SDK）。把这些积木拼成一个开源、可一键部署、可 fork 改造的完整 agent，就能既给开发者一个「拥有自己 agent」的最低门槛起手式，又反向拉动 Vercel 平台消费。时机正是「人人都想要自己的 Devin、但又不想被闭源锁定」的当口。

### 解法哲学

- **明确选择「agent ≠ sandbox」的三层解耦**：agent 生命周期不绑定单次请求、沙箱可独立 hibernate/resume、模型与沙箱实现各自演进、VM 保持纯执行环境而非控制面。强调「生产级基建而非合成 demo」。
- **明确选择「模板而非黑盒」**：README 反复强调它是 reference app，目标是被 fork 和改造。
- **明确选择 Vercel 原生**：深度绑定自家全家桶（一键 Deploy 自动配 Neon Postgres），用「集成黏合度」换「从 0 到自有 agent」的最低门槛——代价是平台绑定。

### 战略意图

这是 Vercel 在 AI 应用框架层（v0 / AI SDK / AI Gateway / Sandbox / Workflow SDK）全力布局中的一块关键拼图：用一个高曝光的开源标杆，把零散基建串成「看得见、可上手、可付费」的完整故事。无商业化代码，但战略意图清晰——它是 Vercel AI 基建的最佳广告与转化漏斗入口。

## 核心价值提炼

### 创新之处

1. **「the agent is not the sandbox」的三层架构**（最值得学的工程取舍）：把 agent 控制面与代码执行环境彻底分离，换来生命周期解耦、沙箱可暂停恢复、模型/沙箱可独立替换。这是「后台 agent」区别于「IDE 内联 agent」的根本设计分野。
2. **agent 自举开发（dogfooding 闭环）**：用产品本身（后台编码 agent）来维护产品自己的代码库，bot 提交占 ~21%——这是「这套模板真能干活」最硬的证据，也是一个可复制的「让 agent 参与自己仓库维护」范式。
3. **`skills-lock.json`——像锁依赖一样锁「AI 能力来源」**：把 agent 用到的 skill 锁定到外部 GitHub 源并记 `computedHash`（如 `ai-sdk`→`vercel/ai`、`chat-sdk`→`vercel/chat`、`vercel-react-best-practices`→`vercel-labs/agent-skills`），保证 agent 能力可复现。这是「agent skill 供应链管理」的早期实践。
4. **durable workflow 驱动的 agent 执行**：用 Vercel Workflow SDK 做可流式、可取消、可重连恢复的多步 agent 运行，解决「长时间后台任务断了怎么办」。

### 可复用的模式与技巧

1. **控制面与执行面分离**：agent 在沙箱外、通过工具接口操作沙箱——适用于任何「长生命周期 agent + 短生命周期执行环境」的设计。
2. **给 AI agent 写「living document」**：`CLAUDE.md`/`AGENTS.md` 开篇即「This is a living document. When you make a mistake or learn something new, add it to Lessons Learned」——把规范沉淀成 agent 可持续学习的协作文档。
3. **agent skill 的 lockfile 化**：用 `skills-lock.json` + `computedHash` 管理 AI 能力供应链。
4. **monorepo 分层「应用驱动、内核稳定」**：`apps/web`（90% 改动，产品层）+ `packages/agent`（大脑，改动少而关键）+ `packages/sandbox`（执行层）+ `packages/shared`——价值迭代在应用层，底层早稳定。

### 关键设计决策

- **「agent ≠ sandbox」是全项目的核心赌注**：好处已如上；但 InfoQ 报道引用开发者 Michiel Voortman 的反方意见——「agent 与 VM 分离虽是卖点，却会拖慢 agentic 开发、限制 agent 的自由度与能力」，他主张相反模型（先 agent-per-computer、随模型变强再水平扩展）。这是一个真实的架构分歧，fork 前应想清楚自己站哪边。
- **pnpm 管依赖 + Bun 跑测试的混合栈**：项目最后一个提交正是「Migrate package management to PNPM (#889)」，刚从全 Bun 切到 pnpm，`AGENTS.md` 明确「pnpm exclusively for dependency management, Bun for tests」。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | open-agents | OpenHands | Devin / Copilot / Cursor（闭源） | coding-agent-template（同门） |
|------|-------------|-----------|----------------------------------|-------------------------------|
| 开源 | ✓ MIT | ✓ | ✗ 闭源 SaaS | ✓ |
| 部署门槛 | 一键 Deploy（Vercel 原生） | 较重（Docker/K8s 自托管） | 零搭建（厂商托管） | 一键 Deploy |
| 基建绑定 | 强（Vercel 全家桶） | 中立（云厂商无关） | 各自生态 | 强（Vercel） |
| 架构特色 | agent≠sandbox + durable workflow | 模型自由切换、SWE-bench ~68% | 产品打磨成熟 | 多 CLI agent 编排（无 durable runtime） |
| 定位 | 完整产品参考应用 | 行业标杆开源 agent | 端到端托管 | 编排壳 |

### 差异化护城河

护城河是「**Vercel 原生 + 开源完整参考应用 + 一键部署 + Sandbox/AI Gateway/Workflow 深度集成**」——在「自托管 background coding agent 起手式」这个细分里，它用官方基建黏合度换取了最低的「从 0 到自有 agent」门槛，与 OpenHands（中立、重运维）、Devin（闭源、托管）形成清晰错位。加上官方背书 + agent 自举的说服力，短期难被简单复制。

### 竞争风险

最大风险有二：① **平台绑定的双刃剑**——深度依赖 Vercel 全家桶意味着脱离 Vercel 复用价值大减，对不想被锁定的团队是减分项，而 OpenHands 的云厂商中立正好相反；② **架构赌注可能押错**——若「agent-per-computer（agent 在 VM 内）」随模型变强成为主流，则「agent≠sandbox」的解耦优势会被削弱。此外它已是高曝光区，作为「冷门套利」选题价值低。

### 生态定位

它是「background coding agent」品类的**教科书级官方参考架构**，填补了「开源、可 fork、一键部署的完整后台编码 agent」这一空白。在更大图景里，它是 Vercel AI 基建（Sandbox/AI SDK/AI Gateway/Workflow）的最佳集成示范与转化入口。

## 套利机会分析

- **信息差**：这是「已被市场充分认知」而非「被低估」的项目——价值不在挖冷门，而在它是品类范本，拆解学习价值高。做内容需用差异化视角切入（如「agent 自举」「agent≠sandbox 之争」），而非泛泛介绍。
- **技术借鉴**：「控制面/执行面分离」「durable workflow agent」「agent skill lockfile」「给 agent 写 living docs」四套模式可直接迁移到自建 agent 项目。
- **生态位**：想自建后台编码 agent 又用 Vercel 栈的团队，这是最省事的起手式；想理解「后台 agent 该怎么架构」的人，这是最好的开源样本。
- **趋势判断**：背景编码 agent 是 2026 年明确的上升趋势，open-agents 借 Vercel 背书 + 开源占据了开源侧的标杆位；但开发节奏已从冲刺转维护，需观察后续投入。

## 风险与不足

- **强平台绑定**：深度依赖 Vercel Sandbox / AI Gateway / Workflow / Neon，脱离 Vercel 生态后大量集成价值流失。
- **部署链路门槛高**：需配齐 Postgres + Better Auth secret + Vercel OAuth app + GitHub App（多组 callback/webhook 凭据），是新用户最大痛点（issue #815「部署后 404」即此链路某环未配通）。
- **开发已显著降速**：4 月单月 343 commit 见顶后，5 月骤降到 18、6 月仅 1，近 30 天仅 10——从「冲刺」切到「维护性微调」，需关注 Vercel 的持续投入意愿。
- **架构争议未定**：「agent≠sandbox」是赌注而非定论，存在被反向架构（agent-per-computer）超越的可能。

## 行动建议

- **如果你要用它**：你想要一个**自托管、可改造、跑在 Vercel 上的后台编码 agent**，且乐于（或已经）使用 Vercel 栈——它是门槛最低的起手式，一键部署即得完整 UI + agent runtime + 沙箱 + GitHub 集成。若你要云厂商中立或更强自主性，选 OpenHands；要零搭建开箱即用，选 Devin/Copilot/Cursor。
- **如果你要学它**：重点读 `packages/agent/`（agent 大脑：`open-agent.ts` / `system-prompt.ts` / `tools/` / `subagents/`）、`packages/sandbox/`（执行层抽象 `factory.ts`/`interface.ts`/`vercel/`）、`apps/web/app/workflows/chat.ts`（durable 编排）、`apps/web/app/api/{chat,sandbox,generate-pr}/route.ts`（核心闭环），以及 `AGENTS.md` + `.agents/skills/` + `skills-lock.json`（agent 自举机制）。
- **如果你要 fork 它**：先想清「agent≠sandbox」这个架构赌注是否适合你的场景；最有价值的改造方向是**解耦 Vercel 绑定**（把 Sandbox/AI Gateway 抽象成可替换 provider，让它能跑在其它云上），以及简化部署链路降低「从 fork 到上线」的门槛。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/vercel-labs/open-agents （已收录，文档详尽：架构/workflow 引擎/沙箱生命周期/GitHub 集成/认证/数据层） |
| Zread.ai | 未验证（建议发布前补核 https://zread.ai/vercel-labs/open-agents） |
| 关联论文 | 无（工程模板项目） |
| 在线 Demo / 官网 | https://open-agents.dev ；模板页 https://vercel.com/templates/template/open-agents |
| 延伸阅读 | [Vercel Releases Open Agents to Support Background AI Coding Workflows — InfoQ](https://www.infoq.com/news/2026/04/vercel-open-agents/)（含架构反方观点） |

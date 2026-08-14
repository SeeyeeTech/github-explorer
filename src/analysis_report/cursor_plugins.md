# GitHub 推荐：Cursor 把 AI 编辑器卖了 SpaceX，剩下这份 33 插件市场才是真正的 Agent 时代资产

> GitHub: https://github.com/cursor/plugins

## 一句话总结

Cursor 官方插件市场：把 27 个自家插件 + 6 个第三方 MCP 集成，以「JSON Schema + 7 类元件 + GitHub PR」打包分发的 Agent 时代 npm registry，其中 `orchestrate` 插件提供了行业最干净的「plan.json / state.json / handoffs」文件即 IPC 多 agent 协作范式。

## 值得关注的理由

1. **被 SpaceX 收购当天仓库仍在加速**：2803 stars / 6.7 个月 = 419 stars/月，远超 Continue/Cody 等同赛道；最近 30 天 72 commits，8 月还没过完就已经 52 commit，超过历史上任何一个月；意味着这是 SpaceX 体系内 Agent 平台战略的入口资产，不是被抛弃的边角料。
2. **多 agent 协作工程化最深**：`orchestrate` 插件用「文件即 IPC」替代中心状态服务（plan.json + state.json + handoffs/*.md + attention.log 四文件协作 + git 做版本化），跨 IDE / Cloud VM 异构环境无需任何基础设施；这是国内做 multi-agent / workflow engine 团队直接可抄的最干净工程范例。
3. **打包颗粒度领先 Claude Code 一代**：把 skills + agents + rules + commands + hooks + mcpServers + variables 7 类元件一次性打包进 manifest，Claude Code Plugins 只有 skill + MCP，Continue.dev 只有 config.yaml，没有任何一个竞品覆盖完整。

## 项目展示

> 仓库本身 README 无 hero 图，属 dev-doc 风格；以下图像来自各插件子目录。

1. ![pstack 设计方法论](https://raw.githubusercontent.com/cursor/plugins/main/pstack/docs/guide/images/design.jpg) — 类型：架构图（pstack 的设计方法论示意）
2. ![pstack 验证流程](https://raw.githubusercontent.com/cursor/plugins/main/pstack/docs/guide/images/verification.jpg) — 类型：流程图（pstack 的验证步骤）
3. ![Cursor Router 模型调度](https://raw.githubusercontent.com/cursor/plugins/main/pstack/docs/guide/images/router.jpg) — 类型：架构图（多模型路由策略）
4. ![orchestrate 多 agent 拓扑](https://raw.githubusercontent.com/cursor/plugins/main/pstack/docs/guide/images/understanding.jpg) — 类型：架构图（多 agent 任务拓扑）
5. ![pstack recipes 工作流](https://raw.githubusercontent.com/cursor/plugins/main/pstack/docs/guide/images/recipes.jpg) — 类型：流程图（pstack 的并行 recipes 工作流）

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/cursor/plugins |
| Star / Fork | 2,803 / 227 |
| 代码行数 | 20,943（TypeScript 90.0%、JSON 7.1%、JS+Shell+CSS 等 < 3%） |
| 注释比 | 44.6%（重提示词文档型，非密集代码型） |
| 文件数量 | 365（含 246 个 markdown） |
| 项目年龄 | 6.7 个月（首提交 2026-01-22） |
| 开发阶段 | 密集开发（最近 30 天 72 commits，8 月 52 commit 创历史新高） |
| 贡献模式 | 核心少数 + AI Bot + 社区（15 人，lauren 36.2% + Cursor Agent Bot 30% + ericzakariasson 17.2%，三人 89%） |
| 热度定位 | 中等热度偏头部（419 stars/月，AI 编程生态前 10%） |
| 质量评级 | 代码良好 / 文档优秀 / 测试基本（28 个单元测试但无集成测试） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

这是 Anysphere 公司（C ursor 母公司）的官方仓库，不是个人项目。Cursor GitHub Organization 2023-03 注册，旗下 10 个仓库全部围绕 Cursor 产品线（IDE 33k、cookbook 4k、community-plugins 4k、本仓 2.8k、mixture-of-kittens 534、minisqlite 269 等）。Top Contributor lauren（Lauren Tan，前 Vercel/Next.js core，现 Cursor 产品负责人）+ ericzakariasson（Cursor 早期工程师）+ Cursor Agent（公司内部 AI bot）组成了"人类 + AI"双中心开发结构。

### 问题判断

`cursor-team-kit`（内部 CI 修复、PR review、weekly review）、`thermos`（个人深度 review 工作流）、`orchestrate`（fan-out 并行 cloud agents）这些插件直接对应 Cursor 工程团队自身的日常 workflow——这是 **dogfooding 优先的产物**，作者先把自己每天怎么用 Cursor 沉淀成 plugin，再向社区开源。

### 解法哲学

**「manifest + bundle + schema」**——用严格 JSON Schema 控制契约（`schemas/plugin.schema.json` 181 行 + `scripts/validate-plugins.mjs` 102 行 ajv 校验），但不限制元件组合；GitHub 即包管理器，PR 即可贡献，无需 npm registry 审批；plan.json 等文件即 IPC，让 LLM 间的接口变成结构化 markdown 而非 RPC，agent 死了信号不丢。

### 战略意图

2026-08-14 官方博客宣布 **Cursor 被 SpaceX 收购**——这是定位跃迁的最关键信号：从"AI Code Editor"到"Coding Agent for Building Ambitious Software"，品牌语从"Extend the Editor"换成"Extend the Agent"。`cursor/plugins` 在更大图景中扮演 **Agent 时代的 npm registry + SpaceX 体系统一知识层入口**：Cursor Router（2026-07-22 发布）公开选模逻辑，做 model-agnostic 调度层；plugin marketplace 做能力扩展层；二者叠加形成"模型无关 + 能力可插拔"的 Agent 平台底座。

## 核心价值提炼

### 创新之处

1. **「plan.json / state.json / handoffs/*.md / attention.log」四文件 IPC 多 agent 协作范式**（orchestrate 插件）—— 新颖度 5/5，实用性 5/5，可迁移性 5/5。零基础设施依赖，跨 IDE + Cloud VM 异构环境自动适配，agent 失败不影响信号传递。
2. **7 类元件一次性打包进 plugin manifest**（skills + agents + rules + commands + hooks + mcpServers + variables）—— 新颖度 4/5，实用性 5/5，可迁移性 5/5。Claude Code Plugins 只有 skill + MCP，Continue.dev 没有 plugin 概念，本仓是唯一覆盖完整 agent 时代可定制点的 manifest 系统。
3. **JSON Schema Draft-07 + ajv CI 严格校验**（`scripts/validate-plugins.mjs`）—— 新颖度 3/5，实用性 5/5，可迁移性 5/5。`additionalProperties: false` 阻止 silent schema 扩张，PR 阶段拦截所有 manifest 错误。
4. **hooks.json 仿 GitHub Actions 风格**（lifecycle event + shell command）—— 新颖度 3/5，实用性 4/5，可迁移性 5/5。零 runtime 依赖，开发者认知可迁移。
5. **measurements[] 声明 + CLI 物理重跑验证**（orchestrate worker handoff）—— 新颖度 4/5，实用性 5/5，可迁移性 5/5。不相信 LLM 自报值，CLI 在 worker branch 上重新跑命令，drift > 10% 报警；国内做 code agent 团队建议直接抄。
6. **MODEL_CATALOG 的 `defaultFor: TaskType[]` 声明式任务→模型映射**（orchestrate/scripts/models.ts）—— 新颖度 4/5，实用性 4/5，可迁移性 3/5。planner 写 plan.json 只用稳定 slug，与 backend ID 解耦。

### 可复用的模式与技巧

- **「Git + JSON Schema + ajv CI」三件套**：任何接受外部 manifest 贡献的项目的最低成本 governance 范式。
- **「Zod schema + zod-to-json-schema 双重生成」**：prompt 字段契约可机器校验，运行时用 Zod、文档/CI 用 JSON Schema。
- **「Slack/通知通道做镜像、文件做真相」**：长时任务系统接入人类协作的稳健模式——核心状态走 git、通知 best-effort、关键评论重试队列。
- **「completion promise + self-loop hook」**（ralph-loop 插件）：agent 在 stop 时把同一 prompt 喂回去做下一轮迭代，实现自我循环。

### 关键设计决策

1. **决策**：marketplace.json + plugin.json 双重 manifest（27 个插件用 .cursor-plugin/marketplace.json 中心索引，每个插件独立 .cursor-plugin/plugin.json 自描述）
   - **问题**：单仓库要装多个 plugin，每个 plugin 又含多种元件
   - **方案**：中心注册表 + 子 manifest，path 相对仓库根
   - **Trade-off**：单一仓库原子升级、PR 即可贡献，但插件版本不能独立升降（monorepo 限制）
   - **可迁移性**：高

2. **决策**：「7 类元件打包」bundle 模型（`plugin.schema.json` 的 `$defs/stringOrStringArray` 允许全部接受 glob 路径）
   - **问题**：Agent 扩展需要哪些可定制元件？元件之间如何隔离？
   - **方案**：skills/agents/rules/commands/hooks/mcpServers/variables 7 字段共存
   - **Trade-off**：用户 install 一次拿到完整 bundle，但元件类型固定到 7 种，加新类型需 schema 升级
   - **可迁移性**：极高

3. **决策**：orchestrate 用「plan.json + state.json + handoffs/*.md」做多 agent 协作 IPC（替代中心状态服务）
   - **问题**：fan-out 大任务到 N 个并行 cloud agent，状态如何在父子之间同步？
   - **方案**：planner 写 plan.json、CLI 写 state.json、worker 写 handoffs/<task>.md，靠 git 做版本化
   - **Trade-off**：零基础设施依赖、failure-tolerant，但写入非原子（用 writeFileSync + renameSync 兜底）
   - **可迁移性**：极高

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | cursor/plugins | Claude Code Plugins | community-plugins（Cursor 社区） | Continue.dev | Cody（Sourcegraph） |
|------|--------------|---------------------|--------------------------------|--------------|---------------------|
| 打包元件数 | 7（skill/agent/rule/cmd/hook/MCP/var） | 2（skill + MCP） | 社区贡献 bundle | 1（config.yaml） | 1（extension + commands） |
| Schema 校验 | JSON Schema Draft-07 + ajv CI | 无 | 无 | JSON 但无 schema | 无 |
| Hooks 系统 | hooks.json 仿 GitHub Actions | 无 | 无 | 无 | 无 |
| 多 agent 协作 | orchestrate 插件原生支持 | 无 | 无 | 无 | 无 |
| 模型中立度 | Cursor Router + plugin 内可选 | 仅 Claude | 同 Cursor | 多 provider 选择 | 多模型 + 自家 backend |
| 测量验证 | measurements[] + CLI 重跑 | 无 | 无 | 无 | test runner 集成 |
| 市场模型 | 单一仓库 + marketplace.json | GitHub repo-as-marketplace | Next.js + Supabase 前端 | 单 config.yaml | 企业级 + Marketplace 混合 |

### 差异化护城河

- **打包颗粒度领先一代**：唯一覆盖 7 类 agent 时代元件的 manifest 系统
- **schema 治理最严**：JSON Schema + ajv CI 是行业最佳实践
- **多 agent 协作工程化最深**：orchestrate 的「文件即 IPC」模式是行业唯一成型的工程范例
- **dogfooding 资产不可复制**：cursor-team-kit、thermos、orchestrate 直接对应 Cursor 内部 4000 工程师工作流，竞品无法 1:1 复刻

### 竞争风险

- **Claude Code 的 GitHub repo-as-marketplace 开放策略**：任何开发者 5 分钟可发布一个 marketplace，Cursor 的"PR 审批模式"在长尾生态规模上可能落后
- **Cursor Router 自动化 vs plugin 硬编码模型的张力**（Issue #171）：orchestrate/scripts/models.ts 硬编码 MODEL_CATALOG，与"自动选模"目标反方向，未来可能被迫重构
- **Windows 兼容性**：hooks 用 POSIX shell，跨平台差

### 生态定位

在整个 AI 编程助手赛道中，`cursor/plugins` 占据 **「官方精选能力市场 + Agent 平台基础设施」** 这一独特位置——不是单纯的插件源码（那是 community-plugins 的角色），也不是单纯的产品（那是 cursor 主仓的角色），而是把"能力可插拔"作为平台战略的官方分发通道。被 SpaceX 收购后，这一层定位被强化为 SpaceX 体系（Starlink / Starship / Raptor）的统一 agent 知识层入口。

## 套利机会分析

- **信息差**：很多人把 cursor/plugins 当成"插件源码"——错。本仓是「官方精选市场」，社区插件在 `cursor/community-plugins`（stars 反而更高 4k）。理解这一分层能少走弯路。
- **技术借鉴**：`scripts/validate-plugins.mjs`（102 行）、`orchestrate/scripts/models.ts` 的 `defaultFor` 模式、`scripts/schemas.ts` 的 Zod 双重生成、`core/handoff.ts` 的 handoff markdown 解析——这 4 个文件不到 1000 行，代表 2026 年 agent 时代最干净的工程实践，国内做 multi-agent / dev agent 的团队直接可抄。
- **生态位**：在 Anthropic 的 Claude Code、Continue.dev、Cody 之间，cursor/plugins 是唯一把"7 类 agent 元件 + schema 校验 + hooks + 多 agent IPC"四件事同时做对的方案；这个组合在国内外都还是空白。
- **趋势判断**：持续加速（最近 30 天 33.6% 的 commit 在过去一个月内产生），SpaceX 收购后预计会带来 Starlink/Starship 团队的工程化插件需求，未来 6 个月仍处于上升通道。

## 风险与不足

1. **agent-manager.ts 单文件 2113 行**（orchestrate）：spawn / handoff / Slack mirror / Andon / measurements / branches / attention 全塞一个文件，"上帝类"风险高，未来重构压力大。
2. **无集成测试**：28 个单元测试覆盖 models-catalog / slack-adapter / measurements-compare 等模块，但 orchestrate 的 end-to-end kickoff → run → handoff 流程从未在 CI 跑过。
3. **CI 只跑 schema 校验不跑测试**：`.github/workflows/validate-plugins.yml` 只校验 manifest 完整性，不跑 `bun test`。
4. **Issue #136 揭示的平台规范层张力**：插件启用状态存在 SQLite (`~/.config/Cursor/User/globalStorage/state.vscdb`)，命名反直觉（`installedIds` 实际存的是 enabled ids），对插件作者透明度极差。
5. **未声明仓库级 LICENSE**：README 自述 MIT，但无 LICENSE 文件（待修）；各 plugin 各自有 LICENSE（多为 MIT）但分散。
6. **测试覆盖率为零的隐含信号**：commit_type_distribution 显示 test = 0（214 个 commit 中 0 个测试 commit），与 28 个测试文件的事实矛盾——说明测试是 Cursor Agent Bot 在 fix 流程中补的，不是 commit 规范的一部分。

## 行动建议

- **如果你要用它**：`git clone https://github.com/cursor/plugins` → 在 Cursor IDE 打开 → Marketplace 浏览 27 个 first-party + 6 个第三方 MCP 集成 → 按需 install（pstack 是 lauren 个人风格、orchestrate 适合大型 fan-out 任务、thermos 适合深度 review）。比 Continue.dev 更适合团队 + 企业场景，比 Claude Code 更适合需要 hook/规则/MCP 完整定制的用户。
- **如果你要学它**：重点读 4 个文件——
  - `/tmp/repo-miner-plugins/scripts/validate-plugins.mjs`（102 行）—— JSON Schema + ajv CI 范式
  - `/tmp/repo-miner-plugins/orchestrate/skills/orchestrate/scripts/models.ts`（197 行）—— 声明式任务→模型映射
  - `/tmp/repo-miner-plugins/orchestrate/skills/orchestrate/scripts/schemas.ts`（100+ 行）—— Zod + JSON Schema 双重生成
  - `/tmp/repo-miner-plugins/orchestrate/skills/orchestrate/scripts/core/handoff.ts`（221 行）—— handoff markdown 解析
- **如果你要 fork 它**：可改进方向有三——（1） 把 orchestrate 的 agent-manager.ts 2113 行上帝类拆为 spawn / handoff / slack / attention 4 个模块；（2） 给 hooks 加跨平台抽象层（PowerShell + WSL fallback）；（3） 把 plugin 独立 semver 化（拆 monorepo 为 sub-package，每个 plugin 独立版本）。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [deepwiki.com/cursor/plugins](https://deepwiki.com/cursor/plugins) |
| Zread.ai | 未收录（WebFetch 403） |
| 关联论文 | 无 |
| 在线 Demo | [cursor.com/marketplace](https://cursor.com/marketplace) |
| 官方文档 | [cursor.com/docs/plugins](https://cursor.com/docs/plugins) |

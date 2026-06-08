# 笔记应用 Craft 开源了它的可视化 Claude Code

> GitHub: https://github.com/craft-ai-agents/craft-agents-oss （原 lukilabs/craft-agents-oss，已改名）

## 一句话总结

拿过 Apple 设计奖的高端笔记应用 Craft，在抵触 AI 热潮三年后做了一次「AI-first 转身」——创始人亲自下场，把一个「Claude Code 式、但面向文档而非代码、面向所有信息工作者而非只面向开发者」的多 provider AI agent 桌面应用做出来并开源；而且全公司只用它自己来开发它自己。

## 值得关注的理由

- **少见的「成熟设计名企 AI-first 转身并开源」真实标本**：背后是 1M+ 用户、5 万+ 付费、约 20 名工程师的 Craft（craft.do）。根 `package.json` 的描述一句点破定位——「Claude Code-like agent for Craft documents」。这不是草根玩票，而是一家公司级的组织自我改造，叙事价值远高于普通 BYOK 客户端。
- **彻底的组织级 dogfooding**：创始人要求全员（含客服、市场、HR、财务等非工程岗）把它接入工作流，「我们只用 Craft Agents 来开发 Craft Agents，不用代码编辑器」。贡献者里「Claude」直接提交 33 次、CI bot 提交 70 次——AI 在参与构建它自己。
- **「agent-native」的产品哲学**：不是把 AI 贴到终端或代码编辑器上，而是从 agent 实际工作方式重新设计界面——像收件箱一样管理多会话、以文档（而非代码/聊天记录）为中心、面向「任何与信息打交道的人」。这是对「AI 客户端该长什么样」的一个有主见的回答。

## 项目展示

![产品界面](https://github.com/user-attachments/assets/3f1f2fe8-7cf6-4487-99ff-76f6c8c0a3fb)

桌面应用主界面：多会话工作台 + 文档中心的 agent 交互。

- [How it Works 官方演示视频](https://www.youtube.com/watch?v=xQouiAIilvU)
- 官网与文档：[agents.craft.do](https://agents.craft.do) / [agents.craft.do/docs](https://agents.craft.do/docs)

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/craft-ai-agents/craft-agents-oss |
| Star / Fork | 6228 / 856（开源 4.6 个月即破 6k，高速增长，已上 Trendshift 榜） |
| 代码行数 | 281K（TypeScript 58% + TSX 28% + JS 7% + Python 1.2%；Electron + bun monorepo） |
| 项目年龄 | 名义 4.6 个月（2026-01-19 开源）；**实为成熟内部产品的开源快照**（首条 commit = "Sync from internal repository"，内部全量近 2000 commit，git 史被压平） |
| 开发阶段 | 稳定维护（开源首月集中 → 逐月递减；近 90 天 37 commit） |
| 贡献模式 | 核心少数 + 社区（Gyula Halmos 1440 + 创始人 Balint Orosz 489 双核主导；含 Claude 33 commit + CI bot 70） |
| 热度定位 | 大众热门 + 强品牌背书的话题项目（非被低估的潜力股） |
| 质量评级 | 代码[良好·大型 monorepo] 文档[优·README 即架构手册 + DeepWiki] 测试[有·CLI 21 步集成测试 + smoke tests] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

背后公司是 **Craft Docs Ltd（craft.do，旧称 Luki Labs）**——拿过 Apple「年度 Mac 应用」(2021) 的高端笔记/文档应用，匈牙利系团队，1M+ 活跃用户、约 20 名工程师。主贡献者 **Gyula Halmos（首席工程师，1440 commit）+ Balint Orosz（Craft 创始人兼 CEO，489 commit）**——**CEO 亲自是第二大提交者**，这本身就说明这是一次自上而下、创始人押注的战略转身。新建的 `craft-ai-agents` org 是专为开源而设的马甲 org。

### 问题判断

据 The Pragmatic Engineer 的报道：Craft 蛰伏三年、刻意抵触 AI 热潮，直到创始人 Orosz 在 2025 圣诞假期亲手用 **Claude Agent SDK + Claude Code**，在自己不熟悉的 Electron+TS 栈上、两周做出一个「可视化版 Claude Code」原型。他看到的判断是：**最强的 agent 已经够强，缺的是一个「比 CLI 更好、更有主见、非代码中心」的工作方式**，而且真正的重度用户不是开发者，而是客服、市场、HR、财务这些「与信息打交道的人」。时机上，2025 年底 agent 能力与 MCP 生态成熟，正是把它产品化的窗口。

### 解法哲学

- **明确选择「agent-native 文档中心」而非「又一个套了 AI 的代码编辑器」**：刻意与 Cursor/Cline 区分，走文档而非代码。
- **明确选择多 provider / BYOK**：Anthropic、Google AI Studio、ChatGPT Plus Codex、GitHub Copilot、OpenRouter、Vercel AI Gateway、Ollama、Bedrock 都能接，自带 key。
- **明确选择「描述即定制」**：customisation just a prompt away——改功能靠提示词而非改代码，因为团队自己就是这么用的。
- **明确选择开源 + 三形态部署**：桌面 app + 无头服务器 + CLI/Web 瘦客户端。

### 战略意图

这是一家成熟商业公司的「AI-first 自我改造」对外展示：用开源放大品牌与叙事、吸引生态，同时把内部已跑通的工具沉淀为公共产品。博客甚至暗示公司可能据此重塑产品策略（如客服自动化到位后改用 API-first 供应商替代 Zendesk）。但转型有代价——「快速迭代、无 code review」让部分工程师不适应甚至离职，公司在试验「一人负责制 squad」取代传统团队，这是叙事的阴影面。

## 核心价值提炼

### 创新之处

1. **「同一套会话工具喂给不同 agent 后端」的解耦**（最值得学）：`session-tools-core` + `session-mcp-server` 把「会话级工具」（计划提交、配置校验等）抽成 Claude 和 Codex 都能复用的一层，多 agent 运行时（Claude Agent SDK / pi-ai / Codex via MCP）背后共用同一套工具。
2. **零配置接源**：对 agent 说「把 Linear 加为 source」，它自己找 API、读文档、配凭据、装 MCP——把「集成」这件苦活交给 agent 自己干。
3. **三档权限模式**：Explore（只读）/ Ask to Edit（默认）/ Auto（全自动），Shift+Tab 切换——给「agent 自主性 vs 用户掌控」一个清晰的产品化答案。
4. **多入口形态**：桌面 + 无头服务器 + CLI + Web viewer（只读分享会话）+ messaging-gateway（Telegram/WhatsApp 机器人入口），一套核心多种触达。

### 可复用的模式与技巧

1. **多 provider/多 agent 后端的网关抽象**：`messaging-gateway` + `shared`（agent/auth/credentials/MCP）把 provider 差异收敛在一层——任何要支持多 AI provider 的产品都可借鉴。
2. **进程外 agent server + stdio/JSONL 通信**：`pi-agent-server` 经 stdio + JSONL 与主进程通信，隔离 agent 运行时。
3. **本地 MCP 子进程的安全隔离**：跑本地 MCP 子进程时过滤掉 `ANTHROPIC_API_KEY`/`AWS_*`/`GITHUB_TOKEN` 等敏感环境变量防泄漏——MCP 安全的实用细节。
4. **>60KB 工具响应用小模型摘要**：超大工具响应先用 Claude Haiku 做意图感知摘要再喂主模型，控制上下文成本。
5. **monorepo 统一版本号锁步 + CI 全自动发版**：69 release/4.6 月、近乎每工作日一发，全自动 tag→构建→发布。

### 关键设计决策

- **Electron + bun monorepo 的双中枢架构**：`apps/electron`（2569 改动，桌面外壳）+ `packages/shared`（1998，多 provider/agent/凭据/MCP 业务逻辑）是两大中枢；`apps/electron/src/shared/types.ts`（41 次，Top10 里唯一真实源码热点）是主进程↔渲染进程的「类型神经中枢」。
- **agent 后端可插拔**：Claude Agent SDK 直依赖 + pi-ai 运行时 + Codex via MCP 并存，用统一会话工具层解耦——这是支持「会话中途切 provider 应对限流」诉求的架构基础。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | Craft Agents | Cherry Studio | LibreChat | Jan | Cursor/Cline |
|------|--------------|---------------|-----------|-----|--------------|
| 形态 | 桌面 + 无头 + CLI | 桌面 | Web 自托管 | 桌面 | IDE |
| 多 provider/BYOK | ✓ 广 | ✓ 广 | ✓ | 本地为主 | 有限 |
| MCP | ✓ 一等公民 | ✓ | 部分 | 弱 | 部分 |
| 中心 | **文档/信息工作** | 聊天+工具 | 对话管理 | 本地助手 | 代码 |
| 目标用户 | 所有信息工作者 | 通用 | 团队 | 隐私用户 | 开发者 |
| 差异化 | agent-native + 设计美学 + 自动接源 + 真组织 dogfooding | 生态成熟 | 企业自托管 | 完全离线 | 编码深度 |

### 差异化护城河

护城河 =「**Craft 设计美学背书 + agent-native 文档工作台 + 零配置自动接源 + 面向非开发者 + 真实组织级 dogfooding 的可信度**」。多 provider/MCP 桌面客户端本身是红海（Cherry Studio/LibreChat/Jan 林立，且 star 更高），但这一组合是相对蓝海的细分卡位，且「真公司真转型」的叙事难以复制。

### 竞争风险

- **红海赛道 + 更成熟的开源同侪**：Cherry Studio、LibreChat 生态更大、社区更成熟。
- **多 provider/BYOK 的可靠性是结构性痛点**：issues 显示 OpenRouter 集成崩溃、Opus 限流、provider 切换诉求——「接万物」的代价是兼容与限流极易翻车。
- **pre-1.0 + 内部史不透明**：仍 0.x 快速迭代，开源的是快照、真实开发在内部仓库，社区对演进方向掌控有限。

### 生态定位

它是「多 provider + MCP 的桌面 AI agent 客户端」里，以「设计美学 + 文档中心 + 面向所有信息工作者」差异化卡位的一员，同时是「成熟公司 AI-first 转身」的标杆案例。

## 套利机会分析

- **信息差**：套利点不在 star（已 6k+），而在**叙事**——「老牌设计名企用 AI agent 完成组织级自我改造并开源内部工具」是开源 AI 客户端里极稀缺的真实案例，传播性强。
- **技术借鉴**：「多 agent 后端共用会话工具层」「MCP 子进程敏感变量过滤」「大响应小模型摘要」「provider 网关抽象」四套模式可直接用到自建 AI 产品。
- **生态位**：想要一个设计精良、文档中心、多 provider、可自托管的桌面 agent，且认同「面向非开发者」理念的团队，这是有特色的开源选择。
- **趋势判断**：agent-native 桌面客户端 + MCP + 多 provider 是明确上升方向；Craft 凭品牌与叙事抢到话题位，但能否把热度转为可持续生态、并跑通商业化是关键。

## 风险与不足

- **多 provider/BYOK 可靠性与限流**：是该类产品的结构性痛点（issues 实证），「会话中途切 provider」成高频诉求。
- **开源的是快照、真实开发在内部**：91 个开源后 commit + 不透明的内部史，社区难以参与核心演进；勿把「4.6 个月 28 万行」误读为短期产出。
- **组织转型的阴影面**：「快速迭代、无 code review」导致部分工程师离职——「全员 AI 改造」并非没有代价。
- **巴士因子偏集中 + pre-1.0**：双核主导、仍 0.x，成熟度与稳定性需观察。
- **安全面**：跑本地 MCP 子进程 + 多凭据管理，攻击面不小；好在有 security@craft.do + SECURITY.md + 敏感环境变量过滤等公司级安全流程。

## 行动建议

- **如果你要用它**：你想要一个**文档中心、多 provider、设计精良的桌面 AI agent**，面向信息工作（不只编码），且认同「描述即定制」——它值得一试（一行命令安装，支持桌面/无头/CLI）。若你要纯编码场景选 Cursor/Cline；要最成熟的开源多 provider 客户端看 Cherry Studio；要完全离线看 Jan。
- **如果你要学它**：重点读 `packages/shared`（多 provider/agent/凭据/MCP 业务中枢）、`packages/session-tools-core` + `session-mcp-server`（同一套工具喂多 agent 后端的解耦）、`packages/pi-agent-server`（进程外 agent + stdio/JSONL）、`apps/electron/src/shared/types.ts`（IPC 类型中枢），以及 README（本身是一份完整架构/部署手册）。
- **如果你要 fork 它**：最有价值的方向是加固多 provider 集成的可靠性与限流编排（社区第一痛点）、补齐 MCP 子进程常驻 vs 隔离的生命周期管理，以及在快照基础上建立更透明的社区协作流程。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/craft-ai-agents/craft-agents-oss （已收录，11 章节文档） |
| Zread.ai | 未确认（探测 403） |
| 关联论文 | 无（产品工程项目） |
| 官网 / 文档 / Demo | https://agents.craft.do ｜ https://agents.craft.do/docs ｜ 演示视频 https://www.youtube.com/watch?v=xQouiAIilvU |
| 深度报道 | [Inside a five-year-old startup's rapid AI makeover — The Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/ai-first-makeover-craft)（含转型阴影面） |

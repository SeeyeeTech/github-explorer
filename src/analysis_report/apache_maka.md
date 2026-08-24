# GitHub推荐：Apache 孵化器首款 Agent Runtime：Maka 如何用「Log 即运行时」改写 AI Agent 的工程范式

> GitHub: https://github.com/apache/maka

## 一句话总结

Apache 旗下首个面向工程师/研究员的 local-first Agent Runtime，以「Log is the Runtime」—— 把 append-only 事件流当作 source of truth、把 UI/context/recovery 当作投影——为核心理念，让 AI Agent 真正可审计、可重放、可恢复。

## 值得关注的理由

1. **Apache 孵化器首款 Agent Runtime**：由 Apache Arrow/DataFusion/Doris 生态背景的工程师发起，把分布式系统里「WAL + materialized view」的成熟范式搬到 AI Agent 域；3 个月、3,827 commit、89 位贡献者、月度 commit 仍在加速（5月771 → 8月1,305）。
2. **与所有主流 Agent 框架错位竞争**：LangGraph 强绑 LangChain 与云 SaaS、Letta 主打长期记忆、OpenHands/Cline 偏 IDE 消费、Google ADK 紧绑 Vertex —— 而 Maka 同时是 local-first、event sourcing 一等公民、跨 surface（Desktop/CLI/TUI/Eval）共享单一 Runtime authority，组合维度在开源界几乎空白。
3. **10 项工程化设计决策可直接借鉴**：从「terminal fact-before-state 双层 commit」到「沙箱边界作为 typed RuntimeEvent action 而非 UI dialog」，每个决策都把数据库/分布式系统的硬骨头解法显式落地到 Agent Runtime 领域。

## 项目展示

![Maka — Your work. Your agent. (hero)](https://raw.githubusercontent.com/apache/maka/main/.github/assets/maka-hero.en.png)

> 官方品牌主图：「Your work. Your agent.」—— 强调 Maka 是为「工作」而不是「聊天」打造的 agent 工作空间。

![Maka app icon](https://raw.githubusercontent.com/apache/maka/main/apps/desktop/assets/app-icons/sky.png)

> 桌面端应用图标（macOS / Windows），是当前最优先打磨的 surface。

> 视频链接：无 hosted demo；可自装 Desktop (macOS Apple Silicon 已签发 / Windows x64 preview 未签名) 或 `maka` CLI。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/apache/maka |
| Star / Fork | 2,877 / 305 |
| Watcher | 12 |
| 代码行数 | 893,001（TypeScript 80.6% · JSON 8.5% · TSX 5.6% · JS 3.3% · CSS 0.9% · Python 0.4% · Rust 0.4%） |
| 文件数 | 2,907 |
| 项目年龄 | 3.2 个月（2026-05-19 ~ 2026-08-25） |
| Commit | 3,827（近 30 天 1,476 ≈ 49/天，近 90 天 3,588 占全量 94%） |
| 贡献者 | 89 人（Top1 jackwener 1,793 占 48%，Top2 Astro-Han 861） |
| 开发阶段 | 密集开发（0→1 加速期，月度单调递增） |
| 贡献模式 | 职业项目 · 团队化 · 多时区协同 |
| 版本 | v0.1.11（共 14 个 tag，语义化版本，0.1.x 快速迭代） |
| License | Apache 2.0（ASF Incubator） |
| 热度定位 | 小众精品（中等热度但增长势能强；3 个月 2.9k stars 偏低估） |
| 质量评级 | 代码优秀 · 文档优秀 · 测试充分 · CI/CD 完善 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Top1 贡献者 jackwener（48% commits）的来源是 Apache Arrow / DataFusion / Doris 生态——这是一个「WAL 是真相源、materialized view 是投影、state machine replication 决定不变量」的分布式 OLAP 工程师群体。把这套范式搬到 AI Agent runtime 域，本质上是把「事实流驱动状态机」从 OLAP 的成熟地带移植到 LLM 的新生域。第二根智识线写在 `docs/architecture/runtime-core-architecture-draft.md` 末尾：Google ADK「Session 作为事实容器」+ Kafka Design 文档共同组成了「log-first」叙事的两个明确智识来源。

组织层面：apache (The Apache Software Foundation) 持有仓库，17.6 年组织年龄、3,163 个 public repos、23,947 followers；项目走 ASF Incubator 标准路径——podling PPMC → Incubator PMC → TLP，贡献须 ICLA。

### 问题判断

作者在 `ARCHITECTURE.md`、`DESIGN.md` 与 13 篇架构 RFC 中明确点出当前主流 agent runtime 的四类失败模式：

1. **上下文压缩等于历史删除**：所有把「会话历史 = UI 投影 + 模型上下文」绑在一起的实现，压缩 context 时都会让 audit/replay 链路断裂；
2. **process crash 让 Run 永远卡 running**：缺少 terminal fact-before-state 硬不变量；
3. **用户点 stop 后 provider 延迟事件改写 completed**：late event 没有拒收机制；
4. **不同 surface 各跑一套 Runtime**：Desktop / CLI / Eval 各自维护执行权威，cross-surface 行为漂移。

时机为什么是现在：2024-2025 AI coding agent 爆发期，开发者社区开始意识到这些不是 UX 问题而是结构性问题；本地算力（Apple Silicon）+ local-first 主张恰好在 ASF 治理下能给出独立的「开源 + 可审计」答案。

### 解法哲学

- **Unix 哲学 > 大而全**：选「一个 Runtime Host 一个 execution authority」；`ARCHITECTURE.md` 明确写「Desktop, TUI, CLI, bots, and evaluation clients ask Runtime Host to execute work; none owns a second Runtime」。
- **可审计 > 易用性**：付出了「迁移期内 SessionEvent/StoredMessage/RuntimeEvent/operational events 四种形态共存，event mapping 维护成本高」的代价。
- **Genuinely open > vendor-bound**：Apache 2.0、不绑 LangChain、不绑云、不绑特定存储（local-first SQLite 默认）、不绑特定模型（Vercel AI SDK 隔离在 ModelAdapter 之后）。
- **明确不做什么**：不做云托管默认路径（[#1286](https://github.com/apache/maka/issues/1286)「cloud agent 必须用 ephemeral sandbox」是后续工作）；不把上下文压缩 = 历史删除（[#1615](https://github.com/apache/maka/issues/1615)「automatic long-term memory lifecycle」作为独立机制存在）；不让 Session = Run（架构文档明确「Turn is not Run, chat messages are not execution state」）。

### 战略意图

是核心产品而不是基础设施组件：Maka 提供 Desktop + CLI + Eval 一整套。商业化走 open-core 倾向，但 README/ASF_NOTICE 显式说当前不是 Apache 发布（所有发布的包都明确标注「pre-incubation, not an ASF release」），这是 ASF 法律要求而非产品形态。后续 roadmap 暗示 multi-language SDK 路线（README 写明 Python/Go SDK 计划）。

> 官方文档/博客支持：本节直接基于 `ARCHITECTURE.md` / `DESIGN.md` / 13 篇 architecture doc / `runtime-core-architecture-draft.md` 等结构化 RFC，不依赖二手解读。

## 核心价值提炼

### 创新之处（按 新颖度 × 实用性 排序）

1. **RuntimeEvent 7 维正交字段模型**（identity/ordering/source/content/actions/correlation/lifecycle）—— 把传统 chat log 的 `role + text` 拆成可独立校验的 7 个维度，让 partial stream、permission action、tool call pairing、step ID、signed thinking 在同一份事实表里共存而不丢语义。新颖度 4/5 · 实用性 5/5。
2. **Terminal fact-before-terminal state 不变量 + AgentRun 双层 commit 协议** —— Run header 不能独立声明 completion；terminal RuntimeEvent 必须先 durable；duplicate terminal 合并；recovery 把「header running + event terminal」自动 repair 成 header 跟随 event。新颖度 4/5 · 实用性 5/5。
3. **`State(t) = Project(RuntimeEvents[0..t], policy, runtime configuration)` 一等公民化** —— 显式分层「canonical log → checkpoint (durable projection) → provider request (ephemeral projection)」，checkpoint 是 materialized view，**不能声明 log obsolete**。新颖度 4/5 · 实用性 5/5。
4. **单一 Runtime Host 跨 surface authority**（[#853](https://github.com/apache/maka/issues/853) RFC 已 merged）—— Desktop/TUI/CLI/Bot/Eval 都通过同一个 Runtime Host IPC/WS 协议；Eval 只拥有 experiment/score 语义。新颖度 4/5 · 实用性 4/5。
5. **沙箱边界作为 typed RuntimeEvent action**（不是 UI dialog）—— `role=system, author=user` 两轴正交表达「系统 lane 语义 + 人类产出」，权限决策直接入 runtime fact 模型，可重放/审计/恢复。新颖度 5/5 · 实用性 5/5。
6. **可重建的 bounded partial snapshot**（不是 append-only JSONL）—— streaming text/thinking 用 bounded replaceable partial；最终非 partial 事件 supersede snapshot；避免 10000 个 delta 变 10000 行永久 ledger。新颖度 3/5 · 实用性 5/5。
7. **safe_boundary_continuation 作为可验证续跑**（不是 checkpoint resume）—— crash recovery 不重放 LLM 请求，只确定「哪些 fact 是 durable 的」并收敛成 explainable outcome。新颖度 4/5 · 实用性 4/5。
8. **Schema V2/V3 双形态 checkpoint + rolling update** —— 不同 provider 的 compact 状态走不同 schema；Codex 走 Codex remote compaction V2；OpenAI Responses 走 provider-native；通用 provider 走 text summary。新颖度 4/5 · 实用性 5/5。
9. **AgentGraph 把每次 activation 重新路由回 Runtime** —— 多 agent 调度不绕过 Runtime；supervisor wake 调度 + reconcile 持续对齐期望图与事实图。新颖度 3/5 · 实用性 4/5。
10. **runtime-policy 独立目录 + 多策略 profile** —— 把可调策略抽离到独立 stores + 多 profile（如 Maka / Maka Dev），CLI 用 Dev profile，release 用 Maka profile，profile 不互相同步。新颖度 3/5 · 实用性 4/5。

### 可复用的模式与技巧

可直接迁移到其他项目的 10 个模式：

- **Log-first Runtime 模式**：log 是 canonical、projection 是派生；任何「多视图 + 单一真相」场景可套。
- **Checkpoint + Raw tail 双层压缩模式**：materialized view 思想搬到 LLM 历史；适用任何「历史太长但要保留语义」的流式系统。
- **Terminal fact-before-state 双层 commit 模式**：防止「header 先 commit 但事实没落盘」的分布式不变量标准做法；可直接套到 task/job runner。
- **One Runtime Host 跨 surface**：多端共享单一执行权威；适合多客户端 + 强一致性 + recovery 需求的复杂产品。
- **Permission as typed RuntimeEvent action**：权限决策进事实流，可重放/审计；适合高权限 agent 系统。
- **Bounded partial snapshot 替代 append-only**：流式输出持久化的通用 pattern；可套到 telemetry、监控、analytics 写入。
- **Multi-profile policy stores**：同一代码多渠道差异化发布；适合 monorepo + 灰度/实验场景。
- **Provider Adapter + Router**：把多变 provider 隔离到 adapter；agent/IDE/工具集成通用做法。
- **Eval 隔离（no Runtime state pollution）**：让 evaluator 不能作弊的硬约束；任何 benchmark/A/B 测试都适用。
- **Schema-versioned checkpoint (V2/V3)**：多 provider / 多版本兼容的流式压缩策略通用做法。

### 关键设计决策（trade-off 分析）

| 决策 | 价值 | 代价 | 是否值得 |
|------|------|------|---------|
| Runtime Event Log 作为唯一语义真相（7 维字段） | 让 partial stream、permission action、tool call pairing、step ID、signed thinking 共存而不丢语义 | 迁移期内 SessionEvent/StoredMessage/RuntimeEvent/operational events 四种形态共存，mapping 维护成本高 | 值得：未来 5+ 年的 agent runtime 都需要这套 |
| 单一 Runtime Host 跨 surface authority | Eval 与 production 行为一致；recovery 不分裂 | Runtime Host 成单点；必须有 exclusive lease + 严格 startup/shutdown 协议 | 值得：把单点风险显式化比隐藏更安全 |
| Terminal fact-before-terminal state 不变量 | 杜绝「Run header 写 completed 但 ledger 没 terminal event」「用户 stop 后 provider 补 complete」 | 每次 send 前一次「exact active Run revalidation」同步检查；silent stream drain 期间窗口不可见 | 必选：这是 agent runtime 最硬的骨头 |
| 沙箱边界是 typed RuntimeEvent action 而非 UI dialog | 权限决策可重放/审计/恢复 | 模型必须学会 raise boundary request；tool 失败语义变厚 | 必选：消费级 IDE agent 把权限弹框当 UX 而非事实，Maka 把权限当事实是范式差异 |
| Compaction 是 projection 而非 mutation | context 缩短不等于历史删除 | 同时维护 log + checkpoint + provider request 三层投影 | 必选：这是 Maka 与所有「context 压缩 = history 删除」方案的范式差异 |
| 单一 SQLite operational-state DB（不是 per-run JSONL） | cross-session 查询、recovery、aggregation 友好 | SQLite 写放大；用 bounded replaceable snapshot 替代 append-only 缓解 | 短中期划算，长期需要 Postgres 路径（roadmap 阶段） |
| Provider SDK 隔离在 ModelAdapter 之后 | 不绑特定模型，便于多 provider | adapter 层维护 N 个 provider 的差异化逻辑（step limit / step-id / thinking signature 翻译都在 adapter 层） | 必选：AI 模型生态还在演化，不绑是唯一长期策略 |
| Agent Graph child Session = 完整 Run | 多 agent 编排 audit/状态不分裂 | 每个 child activation 走完整 Runtime 路径，性能/复杂度更高 | 值得：换来多 agent 行为可审计 |
| Eval 严格隔离（result kernel 只含 score/usage/cost/duration/status/failure/artifacts） | 「earliest-valid selection」可信；operator 不能选 preferred outcome | eval subject 必须 crossed public client/protocol boundary（不能走内部 shortcut） | 必选：所有 eval 框架的核心信条 |
| runtime-policy 多 profile 隔离（Dev/Release） | 同一份代码多发布渠道差异化策略 | profile 不互相同步，调试时要小心 cross-profile 假设 | 划算：避免 dev 配置污染 release |

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | Apache Maka | LangGraph | Letta | Google ADK | OpenHands/Cline/Continue.dev |
|------|-------------|-----------|-------|------------|------------------------------|
| local-first by default | ✅ 默认 SQLite | ❌ 强绑 LangSmith 云 | ⚠️ 部分支持 | ❌ 紧绑 Vertex | ⚠️ 各家不同 |
| event sourcing 一等公民 | ✅ Runtime 不变量 | ❌ 附加层 | ⚠️ 事后补 | ⚠️ Session-based | ❌ 不强调 |
| 跨 surface 共享单一 Runtime | ✅ Runtime Host authority | ❌ 各 surface 各 Runtime | ⚠️ 偏单一 SDK | ⚠️ Runner 紧绑 Vertex | ❌ 偏 IDE 单 surface |
| terminal fact-before-state | ✅ 硬不变量 | ❌ 无 | ❌ 无 | ⚠️ 部分 | ❌ 无 |
| Eval 隔离不让 evaluator 作弊 | ✅ hard rule | ⚠️ 部分 | ❌ 无 | ⚠️ 部分 | ❌ 无 |
| ASF / 治理背书 | ✅ Apache Incubator | ❌ LangChain 商业公司 | ❌ 商业公司 | ⚠️ Google 内部 | ❌ 商业公司 |
| 多 model provider | ✅ ModelAdapter 隔离 | ⚠️ 偏 LangChain 生态 | ✅ 多 provider | ❌ 紧绑 Gemini | ✅ 多 provider |
| 终端用户量 / IDE 集成 | ⚠️ 早期 | ⚠️ 中等 | ⚠️ 中等 | ⚠️ GCP 用户 | ✅ 高 |
| 可观测生态成熟度 | ⚠️ 自带 Runtime Host 协议 | ✅ LangSmith 成熟 | ⚠️ 中等 | ⚠️ GCP 生态 | ⚠️ IDE 自带 |

### 差异化护城河

- **技术护城河**：log-first runtime 一等公民 + terminal fact-before-state 硬不变量 + Runtime Host 跨 surface authority——三层叠加在开源界几乎无重叠。
- **治理护城河**：Apache Incubator 治理 + ASF 法律保护 + ICLA 贡献者网络——这不是技术能力问题，而是信任基础设施问题。
- **信任护城河**：local-first by default + credential vault 在 OS 账户下 + Electron `safeStorage`——三者同时满足的 Agent Runtime 开源项目稀缺。

### 竞争风险

- **LangSmith 这类 observability 厂商一旦做 local-first 复刻**，会蚕食 audit/replay 叙事；
- **Letta / LangGraph 若获得类似 ASF / Apache 2.0 治理背书**，会削弱治理护城河；
- **Cloud agent（[#1286](https://github.com/apache/maka/issues/1286) 是 roadmap）若一直不开**，Cloud SaaS 玩家会抢占 cloud 叙事；
- **桌面端体验被消费级 IDE agent 持续打磨超过**，长期 UX 差距需要补齐。

### 生态定位

在整个 AI Agent 生态中扮演「可审计、local-first、跨 surface 的 agent workspace」角色，填补了「工程化 Agent Runtime」与「消费级 IDE Agent」之间的真空地带。与 LangGraph（生产编排）、Letta（长期记忆）、OpenHands（IDE 消费）、Google ADK（云绑定）四家都是错位竞争，蓝海明确。

## 套利机会分析

- **信息差**：偏低估。Apache 品牌加持 + 清晰差异化（event-sourced append-only log）+ 三月内达 2.9k stars，但远低于 Claude Code/Cursor 等消费级 IDE agent。ASF 孵化器的品牌效应会让它未来 12 个月持续被低估——这是「基金会治理型项目」被市场重新发现前的典型窗口期。
- **技术借鉴**：上面 10 个可复用模式与技巧是核心套利点。其中：
  - 「Log-first Runtime」与「Checkpoint + Raw tail 双层压缩」可直接套到任何 agent / 流式系统；
  - 「Terminal fact-before-state 双层 commit」与「Permission as typed RuntimeEvent action」可移植到任何 long-running task runner 与高权限 agent。
- **生态位**：填补了「跨 surface + 可审计 + local-first + ASF 治理」组合的开源空白；其他 local-first 项目（swarmclaw/sandbase-harness/Hypha 等）都缺 ASF 治理，工程深度远不及。
- **趋势判断**：高速增长中。月度 commit 仍在加速（5月771 → 8月1,305，1.7 倍），PR/issue 高活跃（141/110 open），技术路线图清晰（Cloud agent/Windows/Memory/Work Board）。比 LangGraph/Letta 等成熟竞品的后发优势是：Apache 治理下能给出 vendor-neutral 答案，而前者已经绑了 LangChain/Letta 商业公司；比 IDE 类 agent 的后发优势是：工程化抽象层级（Runtime Host）远高于 IDE 集成层。

## 风险与不足

诚实评估：

1. **Cloud agent 仍是 roadmap**：[#1286](https://github.com/apache/maka/issues/1286)「Cloud Agent runtime on ephemeral sandboxes」是后续工作；这意味着 Maka 当前只服务 local-first 用户，cloud-first 团队无法采用。
2. **平台覆盖不全**：[#2142](https://github.com/apache/maka/issues/2142)「Windows supported platform」揭示 Apple Silicon 是唯一签发构建，Windows x64 preview 未签名（SmartScreen 摩擦），Linux 缺位。Electron 单一架构拖住产品成熟度。
3. **fix 占比 53.5% 是早期阶段诚实信号**：feature 21%、fix 53.5%，意味着超过一半 commit 在「修 bug/对齐预期」。0.1.x 阶段正常，但若 6 个月后 fix 占比仍 >50%，需要警惕。
4. **Conventional commits 规范未全面推广**：3,600+ commit 中仅 ~200 带 conventional 前缀，意味着 changelog 自动生成、语义化发布、CI 类型检查等下游工具链还没完全建立。
5. **Runtime 内部边界仍在反复重画**：最近的 commit「collapse runner shell into kernel #3718」是 runtime 内部折叠重构，0.1.x 期间 API 稳定性无法保证——这是 0→1 期的合理代价，但是下游 SDK 消费者要承担风险。
6. **Eval 路径尚未充分暴露**：仅 277 次修改的 `packages/eval` 是架构文档点名的「Eval subject 必经 Runtime Host 客户端协议边界」位置，但相对于 runtime 的 5,994 次修改，体量偏小——评估子系统的成熟度可能滞后于 Runtime。
7. **MCP 与 computer-use 是后期才出现的扩展点**：分别只 93 与 146 次修改，作为「架构可扩展性」的论据充分，但作为「成熟扩展」还早。

## 行动建议

- **如果你要用它**：
  - 适合：工程师/研究员团队，需要「AI Agent 真实执行了什么」可审计、可重放、可恢复；local-first 工作流优先；多 surface（Desktop/CLI/TUI）需求。
  - 不适合：消费级聊天 UI 场景（用 Letta/OpenHands）、LangChain 栈内生产级多 agent（用 LangGraph）、GCP 深度集成（用 Google ADK）。
  - 部署：当前只能在 macOS Apple Silicon（已签发）/ Windows x64 preview（未签名，需手动 bypass SmartScreen）跑 Desktop；CLI 可在 macOS/Linux 上跑；Linux 桌面待跟进。
- **如果你要学它**：
  - 必读：`packages/core/src/runtime-event.ts`（7 维正交字段）、`packages/runtime/src/runtime-kernel.ts`（terminal fact-before-state）、`packages/runtime-host/`（跨 surface authority）、`docs/architecture/runtime-core-architecture-draft.md`（Chapter 1: Log Is the Runtime）。
  - 次读：`packages/storage/src/runtime-event-persistence.ts`（SQLite 持久化）、`packages/runtime/src/ai-sdk-backend.ts`（Provider 适配层）、`packages/runtime/src/agent-graph-timeline.ts`（多 agent 编排）、`docs/architecture/runtime-resume-architecture.md`（safe_boundary_continuation）。
  - 关联 RFC：`#853` One Runtime Host、`#1286` Cloud agent、`#1615` Memory lifecycle、`#2142` Windows、`#2290` Session Task Ledger 瘦身——这五个 issue 直接揭示了架构演进方向。
- **如果你要 fork 它**：
  - Cloud agent 是最大价值点：基于 [#1286](https://github.com/apache/maka/issues/1286)「ephemeral sandbox」设计，是开源 agent runtime 的稀缺方向；
  - Memory lifecycle 是第二大价值点：基于 [#1615](https://github.com/apache/maka/issues/1615)「compaction ≠ memory」的边界设计；
  - Linux 桌面支持是第三大价值点：补足 [#2142](https://github.com/apache/maka/issues/2142) 平台覆盖的 Linux 侧。
  - 谨慎点：fork 时不要拆分 Runtime Host 的 exclusive lease 设计——这是社区共识（[#853](https://github.com/apache/maka/issues/853) closed），拆分会失去跨 surface authority 保证。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录（HTTP 403） |
| Zread.ai | 收录但详情页被 Cloudflare 拦截 — https://zread.ai/apache/maka（仅有「local-first agent workspace for professional engineering and research workflows」一句简介） |
| 关联论文 | 无（这是工程框架，非学术产物）；架构 RFC 文档末尾引用了 Google ADK 架构博客 + Kafka Design 文档作为 further reading |
| 在线 Demo | 无 hosted demo；自装 Desktop（macOS Apple Silicon 已签发 / Windows x64 preview 未签名）或 `maka` CLI |
# GitHub 推荐：一个人 6 个月、49% 自家 AI 写、2.7k stars：OpenRig 如何把 tmux 变成多 Agent 编排总线

> GitHub: https://github.com/mvschwarz/openrig

## 一句话总结

OpenRig 是一个面向 AI 编码 CLI（Claude Code / Codex / Pi 等）的「harness 之上的 orchestrator」——把 tmux 当消息总线、把 SQLite 当事件队列、用 5 方法 RuntimeAdapter 把多个 Agent 编排成有身份、可恢复、可观测的长期团队，单人 6 个月做到 38 个 release。

## 值得关注的理由

- **架构清晰到可以抄**：domain 281 个一文件一概念文件、daemon 仅 8 个运行时依赖、Hono-free 服务层，把「为 AI 设计的产品」的工程标准做出来了。
- **范式创新**：CHANGELOG 200KB 写成「agent-readable release notes」、`skills/_canonical/` 与产品代码同级做扩展、0.5.9 layout 升级由 Agent 自己读 SKILL 跑 phase grammar——这是「AI 操作自家软件」的早期范本。
- **稀缺生态位**：2.7k stars 远低于工程复杂度；FailproofAI / oh-my-agent / LobeHub 各自抢一块，没人把「跨 harness 编排 + tmux-as-transport + queue-as-state」三者一起做出来。

## 项目展示

![OpenRig TUI 真机录制：多 Agent 协同工作](https://raw.githubusercontent.com/mvschwarz/openrig/main/assets/readme/openrig-agents-working.gif)
> README hero GIF：七个 agent seat 在三组 pod 中实时协作，1.3MB 真机录制。

![OpenRig TUI 拓扑图：产品/开发/QA 三组 pod 下的七个 seat](https://raw.githubusercontent.com/mvschwarz/openrig/main/assets/ui/screenshots/tui-topology.png)
> 架构截图：seat/pod/rig 三层关系一目了然，正是 OpenRig 的核心抽象可视化。

![Star History Chart](https://star-history.com/#mvschwarz/openrig&Date)
> Star 增长曲线：从立项到 2.7k 持续上行，未见饱和。

[Interactive OpenRig TUI demo](https://openrig.dev) — 官网交互式 demo，标注「uses fictional data; nothing runs」，但拓扑和操作是真实的。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/mvschwarz/openrig |
| Star / Fork | 2,722 / 196 |
| Watcher | 14 |
| 代码行数 | 482,167 行（3,027 文件；TypeScript 82.0% + TSX 12.1% + JSON/YAML 1.8% + 其他） |
| 注释行 | 98,730（注释比 20.5%） |
| 项目年龄 | 6.3 个月（首提交 2026-03-23，最近 2026-09-30） |
| 开发阶段 | 密集开发（38 tags / 36 releases，平均 5 天一版；周末 23.4% + 夜间 40.9%） |
| 贡献模式 | 独立开发 + dogfooding（`v-openrig-build` bot 占 49.1%，mvschwarz 个人 40.0%；社区贡献 ~1%） |
| 巴士系数 | 1（单点风险显著） |
| 热度定位 | 中等热度（2.7k stars，工程复杂度远超 star 数） |
| 许可证 | Apache 2.0 |
| Open issue/PR | 57 + 32 = 89 |
| 质量评级 | 代码[优] 文档[优] 测试[充分] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

**Mike Schwarz（@mvschwarz）**，Esoteric Labs 创始人，账号 2.3 年龄，140 followers，18 个 public repo——但**整个账号基本只产出 OpenRig 这一个项目**：把 OpenRig 当产品做，不是副业。bio、shell 公司、单一仓库投入 98.8% 的个人 commit，都是「all in」的信号。

最有趣的数字：`v-openrig-build` bot 贡献了 1,510 个 commit（49.1%），mvschwarz 个人 1,506 + 同人不同 email 的 481 = 40.0%+15.6%。**OpenRig 仓库自己的开发流由 OpenRig 编排工具在跑**——CHANGELOG 里大量 `chore(release): prepare x.y.z` 就是这种 agent 自用的痕迹。这是罕见的「自己 dogfood 自己」开发模式。

### 问题判断

作者在 README 第一行就把行业拉开：「a harness wraps a model. a rig wraps your harnesses.」

他看到的问题：
- **单 harness 缺跨会话事务/恢复**：Claude Code、Codex 都是 CLI 工具，进程结束状态就丢；跑长任务崩溃后只能从头来。
- **多 Agent 框架假设 agent 是无状态函数**：CrewAI / AutoGen 这类把 agent 当 LLM 调用而非当「长寿命的工程师」对待。
- **终端复用器只解决「看得见」不解决「听得到」**：tmux 能开 10 个 pane，但你没法让 pane A 知道 pane B 完成了某件事、然后基于此推进。
- **时机**：Claude Code / Codex CLI 都在 2025 年内成熟到可被编排层包装，作者卡在了「harness 上架后的真空期」立项（2026-03）。

### 解法哲学

**编排层 vs 智能体层硬分离**：OpenRig 不做 agent，只做 harness 的编排层。Agent 怎么想、怎么写代码、怎么用工具，OpenRig 一概不管；它只管「身份、消息、状态、恢复、编排」。这种分离让 OpenRig 可以同时挂载 Claude Code / Codex / Pi / Herdr / cmux 五个 runtime，互不污染。

**Unix 哲学 > 大而全**：daemon 仅 8 个运行时依赖（hono + better-sqlite3 + tar + ulid + yaml + smol-toml + node-server/ws），无 ORM / DI / 框架。CHANGELOG 写「agent-readable release notes for coding agents and human operators」——克制到几乎没有营销味。

**诚实高于乐观**：5 文件联合的「Resume Honesty State Machine」——把恢复从 happy-path 假设改成 typed state machine，明确告诉调用方「我现在是 5 种恢复状态里的哪一种」。这是少数开源项目愿意在公开 API 上承认「我可能恢复不了」的工程态度。

**明确不做什么**：不做 IDE、不做 SaaS、不做 agent 框架、不替代 Claude Code / Codex——这些「不做什么」和 feature 列表一样重要。

### 战略意图

- **核心产品独立化**：Esoteric Labs 这个壳公司是商业化容器（Apache 2.0 不要求，但产品化需要）。
- **无 SaaS 计划**：从 README 到文档反复强调「runs locally」「你的代码不出本机」——赌的是开发者对数据主权的敏感。
- **生态位护城河**：「harness 之上的 orchestrator」这一定位介于 agent 框架（AutoGen）和 IDE（Cursor）之间，目前几乎没第二家在做。

> 官方博客 [openrig.dev](https://openrig.dev) 有完整设计哲学陈述，文档目录 `docs/DESIGN/` 也有同源内容；无独立 Medium / 个人博客。

## 核心价值提炼

### 创新之处（按新颖度 × 实用性排序）

1. **「新颖 5/5 × 实用 5/5」Agent-Operated Migration Skill**：v0.5.9 layout 升级不是脚本迁移，而是 agent 读 SKILL.md 跑 phase grammar——「让 AI 操作自家软件」是早期但清晰的范本。

2. **「新颖 5/5 × 实用 4/5」NodeOriented Challenge-Verified State**：「启动状态」与「内容验证」解耦——一个 node 状态可以是「已启动但未挑战通过」，强制把验证当作独立的一阶概念而非启动的副作用。

3. **「新颖 5/5 × 实用 5/5」Resume Honesty 5 文件联合**：恢复不再是 happy-path 假设，而是一个 5 文件联合维护的 typed state machine（`lifecycle-snapshot-restore.md` §3），每个状态转换都被类型系统约束。

4. **「新颖 4/5 × 实用 5/5」5 方法 RuntimeAdapter 契约**：`runtime-adapter.ts:127` 把「挂一个新 agent runtime」的成本降到 5 个方法——`bootstrap / send / observe / teardown / probe`，加新 runtime 的边际成本近乎线性。

5. **「新颖 4/5 × 实用 5/5」Hot-Potato Closure 契约**：`hot-potato-enforcer.ts` 用「传完即关」语义强制消息接收方对消息负责——避免「消息发出去了但没人 ack」的悬挂。

6. **「新颖 4/5 × 实用 4/5」Process Census Coalescing**：进程存在性检查不是单点查询，而是「按时间窗口合并」——避免高频心跳风暴。

7. **「新颖 4/5 × 实用 4/5」SnapshotTopologyRoster + Explicit Occupant Truth**：把「拓扑」和「occupant（当前谁在）」作为两个独立 first-class 概念建模，operator identity 不再隐式。

8. **「新颖 4/5 × 实用 4/5」Born-Armed Watchdog via onCreate Callback**：watchdog 不是「创建后再启动」，而是在 onCreate 回调里就强制绑定——「一出生就武装」。

9. **「新颖 4/5 × 实用 4/5」Mirror-Skills + Generate-Context-Packs Pipeline**：把外部 skills 镜像到 `skills/_canonical/` 然后生成 context packs——避免运行时漂移。

10. **「新颖 4/5 × 实用 5/5」Agent-Readable CHANGELOG（200KB）**：CHANGELOG 不是给人读的散文，而是给 AI agent 读的「带 schema 的事件流」——这是「为 AI 设计的产品」的最具体落地。

### 可复用的模式与技巧

| 模式 | 文件 / 路径 | 迁移难度 | 收益 |
|------|------|------|------|
| 5-Method Adapter Contract | `packages/daemon/src/domain/runtime-adapter.ts:127` | 2 小时 | 任何「要挂多种外部系统」的项目 |
| Hono-Free Domain Services | `packages/daemon/src/domain/`（173 文件） | 半天 | 框架污染度降到最低 |
| Hot-Potato Closure | `packages/daemon/src/domain/hot-potato-enforcer.ts` | 半天 | 异步消息「无人 ack」问题根治 |
| Resume Honesty State Machine | `docs/as-built/architecture/lifecycle-snapshot-restore.md` §3 | 1 天 | 进程级恢复从 happy-path 升级为类型系统约束 |
| Mirror-Skills + Generate-Context-Packs | `scripts/mirror-skills.ts` + `scripts/generate-context-packs.ts` | 2 小时 | 外部 skill 漂移问题 |
| Born-Armed via onCreate Callback | `startup.ts` 装配根 | 半天 | watchdog 不再漏启动 |
| Process Census Coalescing | `OPR.0.5.3.10`（CHANGELOG 锚点）| 1 小时 | 心跳风暴问题 |
| Discriminated-Union Launch Result | `runtime-adapter.ts:106-119` `ForkSource` | 1 小时 | 启动失败原因的机器可读 |
| Sliding-Window Activity Evidence Source | daemon 内部 | 1 小时 | 活动性证据而非瞬时心跳 |
| Snapshot Topology + Explicit Occupant Truth | `domain/topology-snapshot.ts` | 2 小时 | 拓扑与 occupant 解耦 |

### 关键设计决策

1. **tmux-as-message-bus 而非 message queue**：选择 tmux 当传输层（`rig send`）是为了让用户能「直接打开一个 pane 看 agent 在做什么」。trade-off：tmux 进程崩溃 = 消息层崩溃，但作者认为「看得见」比「永不丢」更重要。

2. **SQLite 当事件总线 + 队列 + 聊天**：5 张协调表承担所有跨 seat 协调（`queue / topology / identity / restore / bundle`）。trade-off：单机限制明显，但换来「零依赖、单进程、单文件」的运维简单。

3. **Dogfooding 的 49.2% commit**：作者不只是用 OpenRig 跑开发——他让 OpenRig 自己生产自己的 release notes、自己处理部分 PR 流程。这是少数把「eat your own dog food」做到「dog 自己做 dog food」的开源项目。

4. **skills/_canonical/ 与 packages/ 同级**：skills 不是藏在 `packages/` 子目录，而是顶层 `skills/_canonical/`——**故意做成「和代码等权的扩展机制」**，让社区贡献 skill 的心智门槛降到和贡献代码一致。

5. **CHANGELOG 200KB + agent-readable 定位**：每条变更都列 PR/issue 链接 + thanks + 限定语（`this does not cover all historical scenarios` / `no new validation of those experiments is claimed`）。**工程上极克制，避免 over-claim**。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | OpenRig | FailproofAI | oh-my-agent | LobeHub | Team-Commonly |
|------|---------|-------------|-------------|---------|---------------|
| Stars | 2.7k | 5.2k | 1.3k | 82.9k | 1.4k |
| 定位 | Harness 之上的 orchestrator | Harness 旁路观测/策略 | Mechanical verification (judge) | Chief Agent Operator + UI | Cross-vendor agent room |
| 多 runtime | ✅ Claude/Codex/Pi/Herdr/cmux | ❌ 单一 vendor | ❌ 单一 | ⚠️ 多但抽象薄 | ✅ 多 |
| 长期持久化 | ✅ SQLite + tmux | ❌ 旁路无状态 | ❌ 单次任务 | ⚠️ 需服务端 | ⚠️ 会话级 |
| 恢复模型 | ✅ Resume Honesty typed state machine | ❌ 无 | ❌ 无 | ⚠️ 简单 retry | ❌ 无 |
| 本地运行 | ✅ 默认本地 | ⚠️ 部分本地 | ✅ 完全本地 | ❌ 偏服务端 | ⚠️ 混合 |
| 观测/可观测 | ✅ topology + occupant | ✅✅ 核心 | ⚠️ 仅 judge 结果 | ⚠️ UI 可见 | ⚠️ room 内 |
| 准入门槛 | 中（需要懂 tmux + agent） | 低 | 低 | 低 | 低 |

### 差异化护城河

- **技术护城河**：5-Method Adapter 契约 + Resume Honesty State Machine + Snapshot Topology 与 Occupant Truth 解耦——三者联合让「跨 runtime + 长寿命 + 可恢复」成为可能，竞品需要至少 1-2 年才能追上。
- **生态护城河**：MCP 17 tools + Herdr/cmux runtime adapter——OpenRig 在「agent runtime 协议层」开始有 factotum 角色。
- **信任护城河**：Apache 2.0 + 完全本地 + 49.2% dogfooding commit——这三件事一起做出来的开源项目屈指可数。

### 竞争风险

- **最可能被替代方向**：
  - **FailproofAI** 抢观测/策略层（如果他们扩到编排，OpenRig 必须保住「编排主战场」）
  - **oh-my-agent** 抢 quality gate（如果他们扩到长任务，OpenRig 必须保住「跨会话恢复」）
- **不会被直接替代**：LobeHub（目标客户不同）、Chorus（流程化分工不是 OpenRig 战场）
- **上游风险**：Codex 0.157+ 共享 daemon（issue #69）、Claude Code worktree bubblewrap（#121）——任一上游行为变化都触发 issue，OpenRig 必须持续追踪。

### 生态定位

在整个 AI agent 生态中扮演「harness 与 operator 之间的 infra layer」：

```plain
Agent Runtime（Claude Code / Codex / Pi）
        ↑ wrapped by
Harness   (一层包装，agent 怎么想)
        ↑ wrapped by
Orchestrator/Rig   (OpenRig 在这一层)
        ↑ powered by
Operator UI   (TUI + Web)
```

这是「harness vs rig」分层哲学的具象——OpenRig 占据了一个几乎空白的生态位。

## 套利机会分析

- **信息差**：2.7k stars 远低于工程复杂度。48 万行 TypeScript + 38 个 release + Apache 2.0 + 完全本地——这套组合在 star 数上严重低估。
- **技术借鉴**：5-Method Adapter / Hono-Free Domain / Hot-Potato Closure / Mirror-Skills Pipeline 都是「任何项目都能半天内学会」的硬技巧。
- **生态位**：跨 harness CLI 编排 + tmux-as-transport + queue-as-state 三者联合的窄但可工程化的位置——目前没有第二家在做。
- **趋势判断**：AI CLI 化（Claude Code / Codex CLI / Pi / Herdr）是 2025-2026 大趋势，OpenRig 卡在「harness 上架后的真空期」是后发优势位；预计 12-18 个月内会出现 3-5 个模仿者，但 dogfooding + Apache 2.0 + 本地默认的组合不易复制。

## 风险与不足

- **单点作者风险**：巴士系数 1，mvschwarz 离开 = 项目停摆。社区贡献仅 ~1%，外部贡献者门槛高（必须读懂 `startup.ts` 2356 行 + `domain/types.ts` 1423 行 + `rigspec-instantiator.ts` 2536 行的演进史）。
- **复合复杂度**：`startup.ts` 2356 行单文件、`domain/` 281 文件颗粒度过细——单人项目下合理，但贡献者扩展门槛极高。
- **上游锁定**：依赖 Codex CLI / Claude Code / tmux / Herdr 多个上游行为；issue #69 / #64 / #116 都是上游 breaking 引起的连锁问题。
- **路线图缺口**：context compaction（issue #27）尚未上主线，多 seat 命名空间冲突（#64）未收敛。
- **CHANGELOG 200KB**：agent-readable 定位值得赞，但人类阅读体验下降，需 docs 分层整理。
- **无 ESLint-Prettier**：依赖克制到连 linter 都没锁，潜在风格漂移风险。

## 行动建议

### 如果你要用它

- **适用场景**：
  - 你已经在用 Claude Code / Codex CLI 跑长任务并被崩溃恢复困扰
  - 你需要 owner / checker / multi-pod 团队化协作（agent 之间有身份隔离）
  - 你想让 agent 在多台机器 / 多 worktree 上协同
- **不适用场景**：
  - 你只要 IDE 内补全（用 Cursor / Copilot）
  - 你的任务是单次短期（用 CrewAI / AutoGen 更轻）
  - 你需要 SaaS 化中央控制台（OpenRig 无此计划）

### 如果你要学它

**优先级阅读路径**（按收益 / 时间比）：

1. **`packages/daemon/src/domain/runtime-adapter.ts:127`**（30 分钟）——5 方法 Adapter 契约，任何多 vendor 集成都能直接抄
2. **`packages/daemon/src/domain/hot-potato-enforcer.ts`**（1 小时）——Hot-Potato Closure，异步消息「无人 ack」问题根治
3. **`docs/as-built/architecture/lifecycle-snapshot-restore.md`** §3（半天）——Resume Honesty State Machine，恢复设计的范本
4. **`packages/daemon/src/startup.ts`**（半天）——composition root 怎么从 252 changes 长成 2356 行
5. **`scripts/mirror-skills.ts` + `scripts/generate-context-packs.ts`**（1 小时）——skills 镜像 + context packs 生成流水线

### 如果你要 fork 它

可改进的方向：
- **拆分 `startup.ts`**：2356 行 composition root 应按生命周期阶段拆 5-8 个文件
- **`domain/` 加 codemap**：281 个细粒度文件需要一个 `INDEX.md` 帮助新人定位
- **CHANGELOG 拆分**：200KB 按版本号分文件 + 生成 `SUMMARY.md`
- **优先实现 Issue #27 Context & Compaction**：这是 roadmap 关键缺口，先做的人抢心智
- **维护 Vendor Compatibility Tracker**：把 Codex / Claude Code / tmux 的 breaking changes 系统化追踪
- **降低贡献门槛**：把 `runtime-adapter.ts` 的 5 方法写成「30 分钟加一个新 runtime」的教程

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录 |
| Zread.ai | 未收录 |
| 官网 + 设计博客 | https://openrig.dev |
| 架构文档 | `docs/as-built/architecture/`（daemon-core / coordination-primitive / adapters-and-runtimes / lifecycle-snapshot-restore） |
| 设计哲学 | `docs/DESIGN/` |
| Agent-readable 历史 | `CHANGELOG.md`（200KB） |
| 交互式 demo | https://openrig.dev（标注「uses fictional data; nothing runs」） |
| Star History | https://star-history.com/#mvschwarz/openrig&Date |
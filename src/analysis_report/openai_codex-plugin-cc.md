# GitHub 推荐：OpenAI 把 Codex 塞进 Claude Code：3 个月 22.6k stars 的「跨厂商上架」怎么把双模型互审计做成插件

> GitHub: https://github.com/openai/codex-plugin-cc

## 一句话总结
OpenAI 官方把自家 Codex CLI 作为「补位 subagent」上架到 Anthropic Claude Code 插件市场，让 Claude 和 Codex 在同一个工作流里互审、互救、互相接管任务——这是一次罕见的「跨厂商」CLI 复用工程范例。

## 值得关注的理由
- **战略样本**：在 Claude Code 插件市场里，排名第一的「非 Anthropic 出品」插件——OpenAI 亲自下场把竞品生态当成渠道用，这种「跨厂商上架」没有现成教科书
- **架构新意**：9k 行 Node 胶水 + 零运行时依赖，造出一个长驻 Broker 进程把 Codex app-server 复用成 Claude Code Agent 可调用的 RPC，是「CLI↔IDE plugin 桥接」模式的可复用范本
- **产品价值**：把 Claude⇄Codex 互审计（review）、救场（rescue）、跨 session 转交（transfer）三个边界场景变成可一键 `/codex:rescue` 调用的工程能力，对双模型重度用户是立刻可用的杠杆

## 项目展示
README 和官网均无展示性图片/视频（纯 JS/JSON 插件脚手架，无 hero 图）。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/openai/codex-plugin-cc |
| Star / Fork | 22,589 / 1,376（72 watchers） |
| 代码行数 | 8,491 行（JavaScript 96.6% / JSON 2.6% / TypeScript 0.8%） |
| 项目年龄 | 3.1 个月（首发 2026-03-30） |
| 开发阶段 | 稳定维护（首发冲刺期已过，按需修 bug） |
| 贡献模式 | 核心少数 + 社区（12 人，主作者 Dominik Kundel 60%） |
| 热度定位 | 大众热门（3 个月内爆发，近 200 star 采样跨度 < 1 天，公告驱动型脉冲） |
| 质量评级 | 代码[优秀] 文档[优秀] 测试[基本] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景
OpenAI 官方组织账号（10.7 年建号，261 个公开仓库，125k 粉丝），主作者 Dominik Kundel 是 OpenAI DX 团队工程师——典型 OpenAI Developer Experience 出品路径（与 `openai/openai-agents-python` 同一作者群）。仓库在 OpenAI 旗下按 stars 排第 3，仅次于 `openai-agents-python`（27.6k）与 `codex`（95k）。

### 问题判断
Dominik 团队观察到 Claude Code 生态的 Agent tool 抽象（subagent + skills + hooks）非常成熟，而自家 Codex CLI 的 app-server 又恰好是长驻 JSON-RPC——但这两套体系之间没有官方桥接，导致用户在 Claude Code 里只能「复制粘贴」用 Codex，错失了 Codex 作为 subagent 接管重活 / review 的机会。时机刚好踩在两个生态都开放 plugin marketplace 的窗口期。

### 解法哲学
**薄壳 + 进程代理**：不重写 Codex 也不魔改 Claude Code——把 Codex app-server 通过 Unix socket（Windows 用 named pipe）包装成一个 Broker，让 Claude Code 的 Agent tool 用一个 subagent (`codex:codex-rescue`) 当 forwarder，单次 Bash 调用转发到 `codex-companion.mjs task`。整条链路最小可信内核：Markdown agent/command + Node glue + JSON-RPC。

明确**不做什么**：
- 不替换 Claude Code 主代理（plugin 只在 review / rescue / transfer 三个边界场景出现）
- 不重写 Codex 协议（用 JSON-RPC 透传 + `unknown variant/method` 白名单降级）
- 不引运行时依赖（package.json runtime deps = 0）

### 战略意图
OpenAI 不与 Anthropic Claude Code 正面竞争，而是把 Codex 当作「补位 subagent」上架到 Claude Code 商店——典型的「跨厂商交叉上架」策略：
- 用 `gpt-5.4-mini/spark` 等差异化模型做钩子，把 Claude Code 重度用户引流回 Codex CLI
- 增加 Codex 在 Anthropic 生态里的曝光（Plugin 商店自带 SEO）
- 用 Apache-2.0 拉拢社区（贡献者中已有 `VOIDXAI` / `xiaolai` 等外部人）

> Issue #211 中 `disable-model-invocation` 与 slash-command 张力的争议，正是这种「跨厂商借用宿主抽象」带来的不可避免的设计摩擦。

## 核心价值提炼

### 创新之处
1. **跨厂商 Agent 桥接 + Broker 复用**（新颖度 4/5）：把 OpenAI Codex app-server 作为长驻 Broker 暴露在 Claude Code 进程内，子 agent 通过 socket 复用同一份 RPC，会话/鉴权/状态自动透传——解决「每条命令冷启动 + 鉴权冲突」的痛点
2. **Stop-time Review Gate（双模型互审计）**（新颖度 4/5）：Claude Code 即将 stop 时，Stop hook 拉 Codex 跑一次 adversarial review，命中 issue 就 block 退出，强制 Claude 修完再走
3. **结构化 Review 输出契约**（实用性 5/5）：`schemas/review-output.schema.json` + `prompts/adversarial-review.md` 强制 Codex 返回合规 JSON（verdict/summary/findings/next_steps），`render.mjs` 校验/排序/脱敏再渲染——下游 plugin 输出契约的范本
4. **Inferred completion 检测**（新颖度 3/5）：主 turn 完成但 subagent collab 还没回时，启动 250ms 定时器检测 `pendingCollaborations/activeSubagentTurns` 是否清空再 finalize——避免漏收子代理输出
5. **跨 CLI 会话 transfer**（新颖度 4/5）：`/codex:transfer` 把 Claude Code 的 `.jsonl` transcript 通过 Codex `externalAgentConfig/import` 注入为可 resume 的 Codex thread，按 `~/.codex/external_agent_session_imports.json` ledger 去重

### 可复用的模式与技巧
- **JSON-RPC Client Base + 双传输（stdio/socket）**：`AppServerClientBase` 提供 pending map / lineBuffer / 通知 handler / close 协议；两个子类只实现 sendMessage。任何「CLI stdio JSONL → 多调用复用」的胶水层都适用
- **Forwarder-only Subagent Contract**：`codex-rescue.md` + `codex-cli-runtime` skill 用文档级硬约束把 subagent 锁死成「单 Bash 调用 + 原样返回 stdout」。**适用**：需要保证输出确定性的 subagent 包装
- **CLAUDE_ENV_FILE + SessionId env propagation**：`session-lifecycle-hook.mjs` 在 SessionStart 把 `CODEX_COMPANION_SESSION_ID` / `CODEX_COMPANION_TRANSCRIPT_PATH` 注入，让任意子进程都能按 session 过滤 jobs。**适用**：session-scoped 持久化状态
- **Detached worker + JSON job persistence**：`--background` 通过 `spawnDetachedTaskWorker` 拉起独立 Node 进程，pid 入 job record，`/codex:status` 通过 poll + logFile 探活。**适用**：plugin 内长任务调度，绕开宿主超时
- **App-server protocol → local type generation**：`prebuild` 用 `codex app-server generate-ts` 生成 `.d.ts` 给 tsconfig 做编译期校验。**适用**：任何对接外部 app-server 的项目都应生成 client stubs
- **Broker 优雅降级**（`BROKER_BUSY` → 直连重试）：多调用并发时 broker 单槽争抢，自动 fallback 到直连模式——比硬塞队列简单也比硬失败友好

### 关键设计决策
| 决策 | 方案 | Trade-off |
|------|------|-----------|
| 独立 broker 进程托管 Codex app-server | `ensureBrokerSession()` 启动长驻 `app-server-broker.mjs`，`withAppServer()` 默认走 broker | 跨 session 资源泄漏（Issue #108 无 idle timeout）；broker 单并发（activeRequestSocket 单槽） |
| `codex:codex-rescue` 子代理做薄 forwarder | `commands/rescue.md` 用 `subagent_type: "codex:codex-rescue"` 不用 `Skill(...)`，防 Issue #234 递归 | 失去 subagent 内嵌智能；换来 single-shot 契约 + 输出 verbatim |
| 状态走「本地 STATE_DIR + 每 job 一 JSON 文件」 | `resolveStateDir()` 用 `CLAUDE_PLUGIN_DATA` 落点，`jobs/{id}.json` + `pruneJobs(MAX_JOBS=50)` 自动 GC | 无并发原子写；换来零依赖、跨平台、git-friendly、调试可见 |
| Stop hook 实现「Review Gate」 | `hooks.json` 注册 `Stop: stop-review-gate-hook.mjs`，按首行 `ALLOW:`/`BLOCK:` 决定放行 | 开了就可能形成 Claude⇄Codex 死循环；默认关闭 |
| JSON-RPC 错误白名单降级 | `startThread()` catch 后检查 `unknown variant`/`unknown method` 才吞，其他重抛 | 静默降级可能掩盖真实 bug；换来对老版本 Codex 宽容 |

## 竞品格局与定位

### 竞品对比矩阵

> 本仓库是「跨厂商交叉上架」产物，无直接对标。下表用相邻形态项目作参照。

| 维度 | openai/codex-plugin-cc | openai/codex | openai/codex-action | Anthropic 官方 subagents |
|------|----------------------|--------------|---------------------|--------------------------|
| 形态 | Claude Code plugin | CLI (Rust) | GitHub Action | Claude Code 内置 |
| 宿主 | Claude Code | 终端 | GitHub Actions | Claude Code |
| 跨模型能力 | Claude⇄Codex 互审 | 单模型（Codex） | 单模型（Codex） | 单模型（Claude） |
| Star 数 | 22.6k | 95k | 1.1k | — |
| 维护方 | OpenAI DX 团队 | OpenAI | OpenAI | Anthropic |

### 差异化护城河
- **官方背书 + Codex App Server 唯一长期维护方**：任何第三方要复刻都需重新搭 app-server 兼容层，门槛极高
- **与 codex CLI 共享配置/账号/线程**：用户无需重新登录或迁移状态
- **Apache-2.0 + 跨厂商上架的合规姿态**：不与 Anthropic 抢主控，只补 review/rescue/transfer 三个边界场景

### 竞争风险
- **Anthropic 官方若推自家 dev-loop / review subagent**会直接挤压本插件的核心价值（review + rescue）
- **Codex CLI 协议变更即插件失效**：`unknown variant/method` 白名单只能缓解不能根治——目前 PR 节奏（v1.0.0 → v1.0.5 3 个月内 6 个 release）显示紧跟上游压力大
- **依赖 Codex 鉴权链路**：Codex 账号限制（如地域 / 配额）会原样传染到 Claude Code 用户

### 生态定位
工具型 + 互操作型——不抢 Claude Code 主控，只在 review / rescue / transfer 三个边界场景出现。在「双模型 IDE 协作」这个新兴细分里，OpenAI 是**唯一**把 Anthropic 生态当作渠道的厂商。

> 无明显竞品（直接对手几乎为零），属于「跨厂商上架」这个新兴细分。

## 套利机会分析
- **信息差**：在中文社区，「双模型互审计」「Stop-time review gate」概念尚未普及；此 repo 的设计模式可作为公开教学样本
- **技术借鉴**：
  - Broker 模式可直接套到「任何 CLI ↔ IDE plugin 集成」场景（如 dbt ↔ VSCode、terraform ↔ JetBrains）
  - Forwarder-only Subagent 契约可作为「禁止 LLM subagent 递归」的标准答案（详见 Issue #234 修复）
  - 结构化 Review Schema 是 LLM-as-judge 模式本地化的好范本
- **生态位**：填补「OpenAI 用户 ↔ Claude Code 工具链」之间没有官方桥接的空白
- **趋势判断**：3 个月 22.6k stars 属爆发型，公告驱动比例高；热度可持续性取决于 Anthropic 是否会收紧插件市场政策。但**架构模式本身**（Broker + Forwarder Subagent）会随 plugin ecosystem 整体增长而扩散

## 风险与不足
- **Issue #108** Broker 长驻子进程无 idle timeout，跨 session 泄漏 app-server 进程
- **Issue #234** rescue skill 递归防护仅靠 forwarder 文档约束，没有代码层防御
- **测试覆盖不均**：`fake-codex-fixture.mjs` 写好但未广泛使用，RPC 模拟测试缺位
- **无 release workflow**：`scripts/bump-version.mjs` 存在但 CI 未调用，marketplace.json version 字段靠手动维护
- **agent/command Markdown 无 lint**：README 提及 `disable-model-invocation` 等易错，但缺少自动化校验
- **热度可持续性存疑**：3 个月 22.6k stars 与 28 commits 严重背离（每 commit 平均 800 stars），需观察一周后是否回落

## 行动建议
- **如果你要用它**：双模型重度用户（同时在 Claude Code 和 Codex CLI 工作流里）值得一试；重点试用 `/codex:rescue`（救场）和 Stop-time Review Gate；`/codex:transfer` 适合跨模型调试接力。**风险提醒**：开启 Review Gate 前先设好 Codex 配额预警
- **如果你要学它**：必读 `plugins/codex/scripts/lib/app-server.mjs`（RPC 双传输）+ `app-server-broker.mjs`（Broker 进程）+ `agents/codex-rescue.md`（Forwarder 契约）；次读 `state.mjs`（零依赖持久化）
- **如果你要 fork 它**：
  - 给 Broker 加 idle timeout（修 Issue #108）
  - 把 fake-codex-fixture 用到 `codex.mjs` RPC 路径测试
  - 加 release workflow 把 `bump-version.mjs` 串进 CI
  - 把 Forwarder 契约从 Markdown 约束升级为 schema 校验

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/openai/codex-plugin-cc（已收录） |
| Zread.ai | 未收录 |
| 关联论文 | 无 |
| 在线 Demo | 无（需本地 Claude Code + Codex CLI 环境） |

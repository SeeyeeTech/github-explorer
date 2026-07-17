# GitHub推荐：OpenAI 团队接管 fork：openinterpreter 把 Codex 重写成「Kimi K3 的开源搭子」

> GitHub: https://github.com/openinterpreter/openinterpreter

## 一句话总结
openinterpreter/openinterpreter 已不是 Python 版 Open Interpreter，而是 **OpenAI Codex Rust CLI 团队的 fork**：单 binary 内嵌 15 种 harness（含 Kimi/DeepSeek/Qwen），让"Codex UX × 廉价模型"组合在一台机器上跑起来。

## 值得关注的理由
- **稀缺身份切换**：6.6w stars 的 Python 老仓被整体替换为 Rust fork，Top10 贡献者里 8-9 位是 OpenAI 在职员工（bolinfest / Eric Traut / Jeremy Rose / Ahmed Ibrahim 等）。
- **`/harness` 多协议切换**：同一进程内 hot-swap Claude-Code / Kimi / DeepSeek / Qwen / SWE-agent / Minimal 等 15 种 agent harness，**单一 binary 跨厂商**这件事在 OSS 圈没有第二家。
- **Codex 零迁移兼容层**：`codexPathOverride: "interpreter"` 一行让原有 Codex SDK 用户直接接 openinterpreter。
- **三平台原生 sandbox**：macOS seatbelt / Linux Landlock / Windows WFP 同一抽象，CI 必三平台跑。

## 项目展示

| 资产 | 类型 | URL |
|---|---|---|
| 终端运行截图 | hero | https://openinterpreter.com/blog/open-interpreter/blog-hero-1.jpg |
| Kimi K3 启动界面 | demo | https://www.openinterpreter.com/docs/terminal/kimi-k3 |
| `/harness` TUI 选项面板 | demo | https://www.openinterpreter.com/docs/terminal/harness |
| ACP 接入 Zed/IntelliJ demo | demo | https://www.openinterpreter.com/docs/terminal/acp |

> README 的 hero 图仍是 Python 时代截图，与当前 Rust+K3 brand 脱节——fork 后未做视觉刷新，是一个明显的"运营债"信号。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/openinterpreter/openinterpreter |
| Star / Fork | 66,309 / 5,699（绝大部分是 Python 时代遗产）|
| 代码行数 | 1,318,731 行（Rust 78.9%、JSON 17.1%、Python 2.0%、TS 0.4%）|
| 项目年龄 | 15 个月（重置点 2025-04-16；老仓库 2023-07-14 创建）|
| 开发阶段 | 密集开发（近 30 天 777 commit，近 90 天 2,893，月峰值 2026-04 单月 1,086）|
| 贡献模式 | 核心少数（OpenAI + openinterpreter 创始团队）+ 社区；657 贡献者，top_author_share_pct 13.1% |
| 热度定位 | 大众热门级（数字层面）+ 重置后真实活跃 |
| 质量评级 | 代码[优秀] 文档[优秀] 测试[充分] CI/CD[完善] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景
- **OpenAI Codex 团队**：Michael Bolin（OpenAI 前 staff，Codex 关键 contributor）、Eric Traut（Codex 前端/CLI 主力）、Jeremy Rose（Realtime API 主力）、Ahmed Ibrahim（`aibrahim-oai`）等以员工身份直接在 openinterpreter org 下维护 fork。
- **原 Open Interpreter 创始团队**：Killian Lucas（CEO，1449 co-author commits）+ Owen Lin（COO，`owenlin0`）保留 commit slot，是品牌延续与社区沟通的承载者。
- 这种"OpenAI 工程师干活 + 原 Open Interpreter 团队站台"的双核结构是这个 fork 唯一无二的特征。

### 问题判断
两支团队各自独立观察到的痛点合流：
1. **OpenAI 团队看到**：Codex CLI 锁死在 GPT 系列，没有为廉价模型适配；同时 seatbelt/Landlock/ACP 这些工程基建本可以服务更广的 agent 生态。
2. **openinterpreter 团队看到**：6.6w stars 老 issue 里反复出现"本地 / OLLAMA / 便宜模型"需求——这套需求在 Claude Code 时代被高价 token 关在门外。
3. **时机窗口**：Kimi K3 / DeepSeek V3 / Qwen Coder 等 SOTA 廉价模型在 2025-2026 集中井喷，"Codex UX × 廉价模型"的组合是一个稍纵即逝的叙事窗口。

### 解法哲学
- **Fork > 自研**：继承 Codex 的 Rust agent loop、TUI、sandboxing、app-server 骨架（已知护城河），把节省的精力全部投到差异化层。
- **单 binary 多 harness**：不要求用户切换工具，而是同一进程内 hot-swap harness（`/harness` 命令 dispatch 在 `codex-rs/cli/src/main.rs:1986`）。
- **Wire compat > 协议统一**：Messages / Responses / Chat 三种 wire API 并存，按 harness 选对应路由而非把所有模型强行塞进同一协议。
- **明确不做什么**：不造模型、不做 SaaS、不做"Claude 替代品"的品牌叙事——做"Claude 体验的低成本搭子"。

### 战略意图
- **工具而非平台**：Apache-2.0 单 binary 公开分发，无官方云/SaaS，依赖 OpenAI/Anthropic/中国模型厂商既有的 API。
- **商业化路径**：间接通过 OpenAI 上游变现（fork 本身不直接商业化），原 openinterpreter 团队的 SaaS 业务（旧 `01` / `01-app`）仍在独立运营。
- **生态卡位**："模型中立的 OpenAI Codex"——填补"我想用 Codex 体验但不想锁 GPT"的市场空白。

## 核心价值提炼

### 创新之处
1. **同 binary 多 harness 切换**（`/harness` 路由 15 种 harness）。每个 harness 重实现其 prompt + tool 构造逻辑而非 shell out 上游 CLI——单 binary 多模型族的"瑞士军刀"模式。**新颖度 4/5，实用性 5/5**
2. **WireApi × Harness 二维路由表**（`codex-rs/core/src/harness/routing.rs:56-152`）：穷举 match 把 15 种 Harness × 3 种 WireApi → 5 种 StreamTransportRoute，16 个单测覆盖所有分支，不兼容直接 `CodexErr::InvalidRequest` 早返回。**新颖度 3/5，实用性 5/5，可迁移性 5/5**
3. **Codex SDK 单文件兼容层**：`codexPathOverride: "interpreter"` 一行切换底层——给既有 popular SDK 注入新实现的 fork 策略。**实用性 5/5**
4. **Harness 是"模型请求重建器"而非"外部 CLI shell-out"**（`docs/harness.md:9-11` 显式声明）：把每个 harness 的 system prompt + tool schema + thinking config + 缓存键在 Rust 进程内重新构造（`include_str!` 嵌入 `kimi_code_system_prompt.md` + `kimi_code_tools.json`）。**可迁移性 5/5**
5. **自动 harness 默认推断**（`docs/harness.md:84-94`）：检测到 Anthropic 基址 → claude-code；Kimi/Moonshot → kimi-code；Qwen/QwQ → qwen-code；DeepSeek → claude-code-bare。免去用户记忆。**实用性 5/5**
6. **Auto Permission Reminder 系统提示注入**（`harness/kimi_code.rs:20`）：每条 user message 后追加 reminder block，保留 harness 原生 UX 同时强制覆盖到本进程的安全语义。**新颖度 4/5**

### 可复用的模式与技巧
- **`include_str!` 嵌入 harness prompt/tool**：编译期文件读取 + 版本控制，prompt-template-as-code 项目的标配。**可迁移性高**
- **fixture 测试 + 完整对象比较**：`assert_eq!(request["thinking"], json!({...}))` 直接验证 prompt 生成的完整 JSON。**可迁移性高**
- **三平台 sandbox 独立 crate**：`codex-rs/linux-sandbox/` + `windows-sandbox-rs/` + `sandboxing/`（seatbelt 后端）——上层 `SandboxPolicy` 抽象统一，下层 OS-specific binary 通过 fork+exec 调用。任何"需要权限隔离的 agent"都该用此 3 层。**可迁移性高**
- **`AGENTS.md` 当 LLM 工作规范**（322 行 Rust/codex-rs 工程契约）：把所有 Code Review rules、test 位置约定、snapshot 工具链、reasoning context 上限（10K token）、大模块上限（500 LoC）写进 AGENTS.md，要求 agent/PR author 自觉遵守。`argument_comment_lint` 要求 Rust `foo(false)` 必须前置 `/*param_name*/` 注释。**可迁移性中**

### 关键设计决策
1. **决策**: 单 binary 多 harness 路由表
   - 问题: 用户想跑 Kimi/DeepSeek 但调用真 CLI = 黑盒、不可观测、不可并行
   - 方案: Rust 进程内重建 harness prompt + tool schema，与 Codex 共享状态
   - Trade-off: 跟上游 Kimi Code 漂移时需手动同步；省掉了 IPC、token 泄漏、并发上限
2. **决策**: 三平台 sandbox 各自独立 binary
   - 问题: 沙箱必须 OS-specific 但对外统一
   - 方案: `linux-sandbox` / `windows-sandbox-rs` 编译为独立 binary 被主进程 fork+exec 调用
   - Trade-off: 跨平台测试矩阵爆炸，CI 必三平台跑
3. **决策**: Messages/Responses/Chat 三种 wire 并存
   - 问题: 同一低价模型可能三种 wire API 都支持但 prompt 只对一种 wire 有效
   - 方案: 二维路由表 + 穷举 match，不兼容组合直接 `InvalidRequest` 早返回
   - Trade-off: 加新 harness 必须同时维护 chat-harness builder 与 routing 测试

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | openinterpreter | devo (309★) | jcode (8,375★) | cersei (406★) |
|------|----------------|--------------|----------------|----------------|
| 语言 | Rust 96.4% | Python（推测） | Rust | Rust |
| 多 harness 切换 | ✅ 15 种 | ❌ 单 harness | ❌ 单 harness | ❌ SDK only |
| Codex SDK 兼容 | ✅ 一行 override | ❌ | ❌ | ❌ |
| 三平台 sandbox | ✅ seatbelt/Landlock/WFP | ❌ | 部分 | ❌ |
| ACP 协议 | ✅ interpreter acp | 部分 | ❌ | ❌ |
| 廉价模型覆盖 | Kimi/DeepSeek/Qwen/GLM/SWE-agent | DeepSeek/Qwen/Kimi/GLM | 单一 | 多 |

### 差异化护城河
1. **技术护城河**：多 harness + Codex SDK 兼容 + 三平台 sandbox 三件套，技术上可被 chat-completions 网关复制，但生态迁移成本（既有 Codex 用户、ACP 编辑器、Kimi/DeepSeek 推荐流量）已是事实壁垒。
2. **生态护城河**：DeepWiki 已收录（last indexed 2026-06-11），架构与 fork-of-codex 状态完全同步——知识沉淀已形成。
3. **团队护城河**：OpenAI Codex 团队 8-9 位主力直接 commit，竞争对手很难短期内复制同等工程密度。

### 竞争风险
1. **上游 OpenAI 政策风险（最大）**：fork 永远是 fork——OpenAI 改 license 或将 sandbox/ACP/Codex SDK "锁源"，openinterpreter 立刻成为"过期分叉"。
2. **Cursor / Anthropic 一旦开放低价模型体验**：杀手级替代即可出现。
3. **Kimi K3 红利窗口期**：大致 1-2 个季度，若 Q4 2026 没有新模型涌现，叙事权可能让位给新崛起的对手。

### 生态定位
"**模型中立的 OpenAI Codex**"，是当前 Rust coding-agent 界叙事位置最接近上游 Codex 但又对中文圈更友好（Kimi K3 主推）的产品。填补了"我想用 Codex 体验但不想锁 GPT"的市场空白。

## 套利机会分析
- **信息差**：66k stars 但实际是 Rust 重启——外界认知与代码现状严重脱节，2-3 个季度内有"身份再发布"的窗口。
- **技术借鉴**：`/harness` 多协议路由、Codex SDK 兼容层、三平台 sandbox 抽象——这三套模式任何 LLM 网关 / Agent 平台 / IDE 集成项目都可迁移。
- **生态位**：ACP 早期实现者 + Codex 兼容层 — 在 IDE/编辑器侧接入是 6-12 个月内有增量的方向。
- **趋势判断**：低成本模型 + Codex UX 仍处于上行通道；Rust monorepo 工程化是 OpenAI 在 Rust 圈的代表作之一，长期看仍有内容可挖。

## 风险与不足
1. **依赖单一上游**：与 OpenAI Codex 高度耦合（Rust 核心、TUI、protocol、sandboxing 都 fork 自上游）；OpenAI 一旦 license/政策调整即被掐死。
2. **品牌认知错位**：6.6w stars 是 Python 老版遗产，重置后未对外公告导致老用户迁移率不明确；266 open issue 大量是历史包袱未清理。
3. **Kimi K3 红利窗口期**：K3 叙事权可能随新模型涌现而衰减，Q4 2026 后需要新差异化点。
4. **README hero 与实际内容脱节**：仍展示 Python 终端截图，与 Kimi K3 brand 不匹配。
5. **unwrap/expect 偏多**：unwrap 6,649 次、expect 15,534 次——对 Rust 老项目属"够用"水位，但与 harness 路由层的严格 Result 化风格不一致。

## 行动建议

### 如果你要用它
- **替换 Claude Code 跑廉价模型任务**：选 `interpreter` + `/harness kimi-code` 或 `/harness deepseek-tui`，比 Claude Code 在 token 成本上可降 1-2 个数量级。
- **从 Codex CLI 迁移**：`codexPathOverride: "interpreter"` 一行切换，零迁移成本试用低成本 harness。
- **IDE 集成**：ACP 协议（`interpreter acp`）可接入 JetBrains/Zed/各类 ACP-compatible 客户端，无需从零实现。

### 如果你要学它
- 重点看 `codex-rs/core/src/harness/routing.rs`（二维路由表的工程实现 + 16 个单测）
- 看 `codex-rs/core/src/harness/kimi_code.rs`（完整 harness 复刻范例 + Auto Permission Reminder 注入技巧）
- 看 `AGENTS.md`（322 行 Rust 工程契约——如何用 AGENTS.md 把 agent 当协作者）
- 看 `codex-rs/{linux-sandbox,windows-sandbox-rs,sandboxing}/` 三层 sandbox 抽象
- 看 `docs/harness.md`（用户态 harness 兼容矩阵 + 自动默认推断逻辑）

### 如果你要 fork 它
- **加入新 harness**：在 `codex-rs/core/src/harness/` 下新建子模块，更新 `routing.rs` 二维表，加测试 + 在 `tools/src/harness.rs` 的 enum 加变体。
- **接入新模型 API**：在 `docs/harness.md:84-94` 的自动默认推断逻辑加新分支。
- **优化运营债**：清理 266 个老 Python issue，刷新 README hero 图，对外公告项目身份切换。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/openinterpreter/openinterpreter（last indexed 2026-06-11，已覆盖 MultitoolCli/ThreadManager/CodexThread/ToolRegistry/Sandboxing）|
| Zread.ai | 未收录 |
| 关联论文 | 无 |
| 在线 Demo | https://www.openinterpreter.com/docs/terminal/kimi-k3 |

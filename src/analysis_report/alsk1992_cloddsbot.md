# GitHub推荐：7 个月 2.5K stars：单作者用 Rust+TS 拼出 21 通道交易 Agent 终端

> GitHub: https://github.com/alsk1992/cloddsbot

## 一句话总结

CloddsBot 是一个把 21 个聊天平台与 16 个交易场所（Polymarket / Kalshi / Hyperliquid / Solana DEX / EVM / Agent 经济）通过同一条 LLM 指令链路串起来的「对话式 AI 交易终端」，单作者 7.5 个月、2520 ⭐、27 万行代码，已迭代到 v1.9.1。

## 值得关注的理由

- **覆盖面是同类项目里最广的**：21 聊天通道 × 16 交易场所 × 10 道风控闸 × 121 个可加载 skill，单仓实现「LLM ↔ 资金」的全栈胶水层
- **工程纪律超出「12 天 hackathon」宣传话术**：从 v0.1.0 到 v1.9.1 共 15 个 semver tag、52 个测试文件、SECURITY/AUDIT/CHANGELOG 完整三件套
- **真正的性能侧花活**：`rust/fast-broadcast` 旁路进程用 tokio JoinSet 把同一笔 signed tx 跨多 EVM RPC 并行抢跑，是少见的 TypeScript 项目内嵌 Rust 子模块的实战范例

## 项目展示

![Clodds Logo](https://cloddsbot.com/logo.png) — 项目主 Logo

![Git clones last 14 days: 10.7k](https://raw.githubusercontent.com/alsk1992/cloddsbot/main/assets/screenshots/clones-14d.jpeg) — README 佐证分发量的 14 天 clone 数截图

视频：https://cloddsbot.com/onboard.mp4 — 官方 onboard 演示视频

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/alsk1992/cloddsbot |
| Star / Fork | 2520 / 312 |
| 代码行数 | 272,682 行（含注释，tokei）；TypeScript 87.9% + Rust 0.1% + 多辅助语言 |
| 项目年龄 | ~7.5 个月（2026-01-27 → 2026-09-12） |
| 开发阶段 | 密集开发（最近 30 天 69 commit 全为安全/SDK 兼容修复） |
| 贡献模式 | 独立开发（alsk1992 占 85-91%，含 AL/ALSK 同人不同 git config） |
| 热度定位 | 中等热度（hackathon 出圈 + 多渠道曝光，近 30 天加速） |
| 质量评级 | 代码[中上] 文档[优] 测试[差] CI[中] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

作者 alsk1992 是英国开发者，公司 Strata，Bio 仅「AL」，账号注册才 1.7 年、只 follow 4 人、display name 仅「AL」——**匿名/小号倾向明显**。其 GitHub 28 个公开仓库中除本仓外均 ≤38 stars，影响力 100% 集中于此；博客 `stratabook.app`、推特 `@Stratabookdex`、代币 `2puc76ehVHyPXhZmDprtP2phDSFE4kzZKDT4JgAWpump` 三者指向同一公司商业化栈。

### 问题判断

作者把问题切成两层：

1. **执行层缺失**：`README.md:160` 写「Arbitrage defaults to dry-run」 + `docs/ARCHITECTURE.md:890` 把 10 个风控子系统压成单次 `RiskEngine.validateTrade()`，等于宣告「LLM 直接出单」的方案不够，必须先过 10 道闸
2. **跨链 × 跨场所 × 可对话**的端到端栈在市面上不存在——既有工具要么单平台（Polymarket-only）、要么单一形态（CLI/Bot）

时机：Colosseum Agent Hackathon on Solana 周期（README L48），用 hackathon 拉初始流量，再以代币+论坛锁定 Agent 网络效应。

### 解法哲学

- **对话优先，但下单永远走同一条管道**：21 通道 × 16 场所共用 `BaseAdapter` + `RiskEngine.validateTrade()` + 同一份执行/账本
- **能落库就落库**：`messages` 表刻意 append-only、unlimited history；ledger 表带 SHA-256 hash + 可选链上锚定（Solana/Polygon/Base）——把可审计性视为一等公民
- **Lazy > Eager**：121 个 skill 是 lazy-loaded（`README.md:154`），`src/skills/loader.ts:748-772` 的动态 token budget（500/2K/8K/16K/32K/48K/80K）按对话复杂度分配上下文
- **明确不做什么**：不做高并发机构级、不做「无脑 LLM 出单」、不做云端 SaaS（强调 personal terminal）

### 战略意图

把 121 skill + 21 通道 + 16 场所拼成「AI Agent 操作系统」，再用 Agent Forum（USDC 质押）+ Compute API pay-per-call + Token Launch（Meteora DBC）反哺 Agent 经济，形成「自举飞轮」。商业模式 = 开源 CLI + 闭源 Compute API + 代币 + Solana 链上基础设施的混合体。

> 官方文档较完整（docs/ 28 个 md + 640 行 README + 多语言），支撑上述分析。

## 核心价值提炼

### 创新之处

1. **统一对话终端 × 多市场** — 21 通道 + 16 场所共用同一执行栈
   - 新颖度 4/5 | 实用性 5/5 | 可迁移性 4/5

2. **Token Budget 动态技能上下文** — `src/skills/loader.ts:748-772` 按匹配得分/平台数/类别数分配 500-80K token 上限
   - 新颖度 4/5 | 实用性 5/5 | 可迁移性 5/5（任何「工具数量 ≫ 单次上下文」的 agent 框架可直接复用）

3. **Rust 旁路 + JSON over stdio 抢跑** — `rust/fast-broadcast/src/lib.rs:106-166` 跨多 EVM RPC 并行 POST 同一笔 signed tx
   - 新颖度 4/5 | 实用性 4/5 | 可迁移性 5/5（任何 EVM sniper/套利/mint 工具可直接 `cargo install`）

4. **RiskEngine 10 步 fail-closed preflight** — 把机构级风控（VaR/CVaR/Volatility Regime/Kelly/Stress Test/Circuit Breaker）下沉到零售 agent
   - 新颖度 4/5 | 实用性 5/5 | 可迁移性 5/5

5. **Meteora DBC 一键发币 API** — 7 个 REST endpoint 封装 anti-sniper 衰减 + 自动 DAMM v2 毕业 + agent-gated 防女巫
   - 新颖度 4/5 | 实用性 5/5 | 可迁移性 3/5

6. **Percolator 二进制 slab 解析** — Anatoly Yakovenko 的 Solana on-chain perps，单 992KB 账户承载全部状态
   - 新颖度 5/5 | 实用性 3/5 | 可迁移性 2/5

### 可复用的模式与技巧

1. **BaseAdapter（token bucket + circuit breaker + auto-reconnect）**：`src/channels/base-adapter.ts:78-516` —— 21 通道统一继承，4 个抽象方法即可定制
2. **动态 token budget 的 skill 选择器**：`src/skills/loader.ts:599-854` —— 别名 + stop words + 分级打分
3. **Rust 旁路 + JSON over stdio**：`rust/fast-broadcast/` —— 用子进程 + tokio 隔离热路径性能
4. **Append-only messages 表 + 上下文压缩**：长会话 AI 客户端的可复用模式
5. **Trade Ledger with SHA-256 + 可选链上锚定**：AI 决策审计的合规追溯模式

### 关键设计决策

1. **单一 `RiskEngine.validateTrade()` 入口**：10 个子系统严格顺序执行，任一失败立即 reject——把多线程/异步竞态全压成单函数同步链，换来「任何交易都过同 10 道闸」的强保证
2. **Skills 双重表达 — SKILL.md + TS handler**：YAML frontmatter 注入 prompt + 动态 import 调用，121 个能力不在 LLM 上下文爆掉
3. **Rust 子模块抢跑**：TypeScript 单线程无法 ms 级跨 RPC 并发，所以用 tokio JoinSet 隔离
4. **Meteora DBC 绑死**：换来「agent 一次 curl 即可发币」的极简体验，代价是迁移到其它 AMM 需重写
5. **Trade Ledger 强制 SHA-256**：合规追溯需要不可篡改证据，锚定失败时需回滚

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | CloddsBot | kalshi-ai-trading-bot | Polymarket-bot | Polymarket-trading-bot-python-V2 | puls-cli |
|------|---------|--------|--------|--------|--------|
| 覆盖市场数 | 16+（预测+DEX+CEX+EVM） | 1（Kalshi） | 1（Polymarket） | 1（Polymarket） | 1+ |
| 接入通道 | 21 聊天 + CLI + Webchat | CLI 为主 | CLI | CLI | CLI |
| AI 集成 | LLM 内核（Anthropic 优先） | AI toolkit | 无 AI | 无 AI | x402+agent swarm |
| 风控 | 10 道闸 + RiskEngine | 基础 | 基础 | TWAP/套利 | 未知 |
| 商业化 | 代币+Compute+Marketplace | 无 | 无 | 无 | 未知 |
| Star | 2520 | 579 | 808 | 189 | 1 |

### 差异化护城河

- **技术护城河**：跨多通道 × 多场所的端到端胶水层 + Rust 抢跑的性能花活
- **生态护城河**：Agent Forum + Marketplace + Compute API + Token Launch 闭环
- **信任护城河**：SECURITY/AUDIT 文档齐备 + ledger 链上锚定 + 15 个 semver tag

### 竞争风险

1. **LLM 成本**：skill 增多导致 token 消耗飙升，token budget 再优化也受限于上下文长度
2. **SDK breaking change**：单作者维护 121+ skill + 21 通道 + 16 场所，任何上游 SDK 升级（如 `@raydium-io/raydium-sdk-v2` 还是 alpha）都会拖垮
3. **盈利实证缺失**：Issue #62「Has someone actually made profit using this?」长期 open，`paper-trading.ts` 仅 192 行虚拟余额，**无连接到真实策略的 shadow order book**——这是社区最尖锐的拷问
4. **代币飞轮依赖社区氛围**：无差异化护城河保护

### 生态定位

偏 Solana + Hackathon 的 Agent-first 交易终端，填补「LLM ↔ 资金」之间缺失的合规+风控胶水层空白，适合作为「Agent OS for capital」的实验田。

## 套利机会分析

- **信息差**：7.5 个月 2.5K stars + 312 forks + 28 open issues 说明有真实用户群体；技术广度覆盖预测市场+永续+DEX+EVM+Agent 协议，**架构层面有研究价值**；但盈利实证是最大黑箱
- **技术借鉴**：
  - `BaseAdapter` 模式可直接复用到任何「多 SaaS 接入」系统（客服/RPA/告警）
  - 动态 token budget 的 skill 选择器可移植到 LangChain/AutoGen/MCP 客户端
  - Rust 旁路模式可移植到任何低延迟子任务（图像/编解码/网络）
- **生态位**：填补「LLM 直接出单」缺失的合规+风控胶水层，是 Agent-first 交易终端的实验田
- **趋势判断**：处于增长期（最近 30 天 69 commit + 加速 star 增长 + 多渠道曝光），但 9 月密集「安全闸门修复月」反映工程债清理期；比竞品有后发优势（覆盖广度 + 多通道 + Agent 经济），但单点维护风险高

## 风险与不足

- **bus factor = 1**：alsk1992 占 85-91% commit，外部贡献仅零星 PR，无人能接续核心代码
- **盈利实证缺失**：Issue #62 / #63 长期 open，社区反复追问「10000 单回测」被搁置
- **测试覆盖薄弱**：52 个测试文件但 execution 关键路径覆盖薄弱（polymarket/kalshi 无完整 mock 测试），无覆盖率门槛
- **过度营销识别**：
  - 「12 天 hackathon 交付」 是营销记忆点，实际工程 7 个月迭代
  - 「118+ trading strategies」 把 skill 子命令都算作策略
  - 「1000+ markets」 真实（22 feeds + Solana DEX 池聚合），但其中约 30% 是 stub（< 200 行）
- **单文件过大**：`pump-swarm.ts` 2208 行、`meteora-dbc.ts` 1486 行、`backtest.ts` 967 行，违反单一职责
- **依赖过重**：80 个 runtime dep，部分（`@polkadot/api`、`@xenova/transformers`）可考虑 dynamic import 减重
- **Rust 依赖链**：`@raydium-io/raydium-sdk-v2` 等仍为 alpha 版本，构建脆弱

## 行动建议

- **如果你要用它**：作为个人跨市场交易终端**谨慎尝试**——技术广度惊艳但盈利实证缺失；建议先用 `paper-trading` 跑回测，对接 Issue #62 的真实策略之前不要入金
- **如果你要学它**：重点关注以下文件/模块
  - `src/risk/engine.ts`（486 行 10 步 fail-closed preflight）
  - `src/skills/loader.ts:599-854`（动态 token budget）
  - `src/channels/base-adapter.ts:78-516`（21 通道基类）
  - `rust/fast-broadcast/src/lib.rs:106-166`（并行抢跑）
- **如果你要 fork 它**：
  - 把 `paper-trading` 升级为连真实策略的 shadow order book，直接回应 Issue #62
  - 给 `pump-swarm.ts` / `meteora-dbc.ts` / `backtest.ts` 拆分单文件
  - 加测试覆盖率门槛（vitest + c8 即可）
  - 把 Rust 子模块升级为独立 crate（带版本号），方便复用

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录 |
| Zread.ai | 未收录 |
| 官方文档 | https://docs.cloddsbot.com（README 引用） |
| 架构文档 | `/docs/ARCHITECTURE.md`（仓库内，28 个 md 文档） |
| HFT 套利报告 | `/docs/RUST_HFT_ARBITRAGE_SWARM_REPORT.md` |
| 关联论文 | 无 |
| 在线 Demo | https://cloddsbot.com/onboard.mp4（视频） |
| Token | `2puc76ehVHyPXhZmDprtP2phDSFE4kzZKDT4JgAWpump`（Solana） |
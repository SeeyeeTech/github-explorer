# 4 个月 31K stars：AI 代理杀入桌面，OpenHuman 如何用「可读记忆」硬刚 Claude Cowork

> GitHub: https://github.com/tinyhumansai/openhuman

## 一句话总结

OpenHuman 是一个本地优先的个人 AI 桌面代理：把 118+ SaaS 工具通过一键 OAuth 拉通，把记忆写成你随时能打开看的 Markdown vault（Obsidian 风格），再让一个会进 Google Meet 真开会的「桌面吉祥物」替你干杂活。**它押注的不是更强的模型，而是「你能看见自己记忆」这件事本身。**

## 值得关注的理由

1. **记忆范式切换**：拒绝把记忆塞进向量黑盒，落地 Karpathy 推崇的「Obsidian Wiki 思想」——本地 SQLite 元数据 + Markdown vault，**人类可读、可手编、可信**。
2. **桌面代理是 2026 年的真方向**：4 个月 30.9k stars、134 名贡献者、5 月单月 1,269 commits 印证「Tauri + Rust core + React」正在替代「Electron + 全云」的旧范式。
3. **工程克制做对的事**：TokenJuice 自述省 80% token，approval gate 默认 ON，subagent allowlist 强制 fail-closed，CEF 子 webview 禁止 JS 注入——**没有为酷炫牺牲安全**。

## 项目展示

![OpenHuman demo screenshot](https://raw.githubusercontent.com/tinyhumansai/openhuman/main/gitbooks/.gitbook/assets/demo.png)
— *主视觉，UI-first 桌面截图*

![OpenHuman context-building diagram](https://raw.githubusercontent.com/tinyhumansai/openhuman/main/gitbooks/.gitbook/assets/image%20(1).png)
— *上下文摄取 → 摘要树流程图*

![Star History Chart](https://api.star-history.com/svg?repos=tinyhumansai/openhuman&type=date&legend=top-left)
— *Star 增长曲线*

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/tinyhumansai/openhuman |
| Star / Fork | 30,969 / 2,999 |
| 代码行数 | 1,213,694（Rust 49% / TypeScript 23% / JSON 23% / 其他 5%） |
| 项目年龄 | 4.3 个月（首次提交 2026-01-27） |
| 开发阶段 | 密集开发（近 30 天 1,354 commits，占总数 47.2%） |
| 贡献模式 | 核心团队 + 社区（134 人，Top 1 占 34.3%，Top 5 占 ~75%） |
| 热度定位 | 大众热门 + 趋势样本（不是被低估，而是「AI 代理桌面化」旗手） |
| 质量评级 | 代码 A  文档 A  测试 A- |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

- **公司**：Tiny Humans, Inc.（2025-11 成立、专门做这件事的创业组织）
- **创始人**：Steven Enamakel（@senamakel），4 个月独占 1,010 commits（37.4%），其个人近期活跃仓库 10 个，本仓独占 30.9k stars
- **背景推断**：新创业团队，但工程节奏强（周末 19.5% / 深夜 32.9%，更像跨时区协作而非个人熬夜）；前身或为 AI Agent / 桌面应用方向
- **可信度评级**：中——团队新、扣分项是 0.5 年账号年龄、创始人单人 34% 集中度、**外部媒体/审计尚未铺开**

### 问题判断

作者看到的是「**用 AI 干活最大瓶颈不是模型，而是个人长期记忆**」。他选了一个并不性感的角度切入：不用向量黑盒，**用本地 Markdown vault 做持久层**——这是 Karpathy 推崇但无人工业化的方向。时机是 2026 年初，因为 Tauri 2 已稳，Rust + React 双端成熟，再叠加 token 成本崩塌让「长上下文 + 频繁同步」变得可行。

### 解法哲学

- **UI-first over CLI-first**：明确选择不做 OpenClaw 那种终端极客风
- **本地可读 over 云端向量**：选择让你「看见」自己的记忆
- **一键 OAuth over BYO API key**：118+ 集成默认托管，但要留 BYO 逃生通道
- **明确不做的**：不卖 AGI 噱头（README 直说 "Not AGI, but an architectural step closer"），不挑战 Anthropic 闭源模型（#2479 已经在接 Claude Agent SDK），不抢占云端代理阵地（让 Manus / Devin 去做）

### 战略意图

- **Open-core 商业化路径清晰**：本体 GPL-3.0 开源，**Composio 集成走 OpenHuman 后端代理**（HMAC + Socket.IO），控制权在自己手里
- **核心是「入口」而非「模型」**：接入 Claude / GPT / Gemini / 本地 Ollama 都是可替换项，**真正的护城河是桌面入口 + 记忆图谱 + Subconscious 心跳**
- **多语言野心**：6 种语言 README（英/中/日/韩/德/乌尔都），但产品本体 i18n 滞后（en.ts 单文件 152 次修改）

## 核心价值提炼

### 创新之处

1. **Memory Tree 双层持久化（SQLite 元数据 + Markdown vault）** — *新颖度 4/5  实用性 5/5  可迁移性 5/5*
   不用 Pinecone / Weaviate，把摘要树直接写成可手编的 `.md`，可被 Obsidian / VS Code / vim 直接打开。
2. **TokenJuice 三源 JSON 规则叠加（builtin + user + project）** — *新颖度 3/5  实用性 5/5  可迁移性 5/5*
   自写 shell tokenizer + 自写 HTML stripper，**显式记录 `html2md` 894MB 堆爆事故**，退回到「自家削苹果刀」哲学。
3. **Cheap-only → LLM 短路 chunk 打分（borderline 0.15-0.85 之外零 LLM）** — *新颖度 3/5  实用性 5/5  可迁移性 5/5*
   7 个弱信号加权打分，绝大多数文档走纯规则管线，只 borderline 区间才上 LLM——**这是 TokenJuice 80% 节省的算术来源**。
4. **`AgentTurnOrigin` task-local + Unknown fail-closed** — *新颖度 4/5  实用性 5/5  可迁移性 5/5*
   5 个 Origin 标签贯穿 tokio task-local，`SubconsciousTainted` 心跳自动升级——**这是「安全优先」的最少代码实现**。
5. **JSON-RPC 2.0 + `StructuredRpcError::expected_user_state` 集中 4 类 skip-report** — *新颖度 3/5  实用性 5/5  可迁移性 5/5*
   2,315 行的 `src/core/jsonrpc.rs` 是 transport 总入口，错误聚合而非逐处打 log。

### 可复用的模式与技巧

| 模式 | 适用场景 |
|---|---|
| Core in-process + per-launch hex bearer | 任何需要「Rust core + TS 壳」的桌面应用，比 sidecar 简单太多 |
| 三层 JSON 规则叠加（builtin/user/project） | 任何需要「可控 + 可扩展 + 可降级」的配置系统 |
| Cheap-only → LLM 短路 | 任何 LLM 管线，先榨干规则，borderline 区间再上模型 |
| Origin task-local + Unknown fail-closed | 任何「agent 触发链路需要可审计」的系统 |
| Structured error envelope + 4 类 skip-report | 任何 LLM agent，噪音告警是会杀死 SLO 的真问题 |
| Tree seal 双策略 + `flush_stale_buffers` 时间兜底 | 任何「树形数据 + 后台折叠」系统（推荐 L0 token / L≥1 sibling） |
| `fast_html_to_text` 反 `html2md` | 任何 LLM 输入清洗，**894MB 堆爆事故是个金标准反例** |
| diff-cover ≥80% 合并门槛 | 任何 LLM 生成 PR 想并入主干的项目（cargo-llvm-cov + diff-cover） |
| i18n parity CI | 任何多语言产品，CI 卡住 6 种语言 key 一致性 |
| Native packages 优先 + unverified script 显式标注 | 任何想兼顾「安装丝滑 + 用户知情」的桌面分发 |

### 关键设计决策

1. **Core in-process + per-launch hex bearer**（PR #1061 删 sidecar）
   - **问题**：sidecar 进程管理复杂、IPC 难调试
   - **方案**：Rust core 直接同进程跑，每次启动生成 hex token 当 bearer
   - **Trade-off**：牺牲了 sidecar 的进程隔离，换来单一进程可调试 + 极简部署
   - **可迁移性**：中（任何 Rust+TS 桌面应用都适用）

2. **Memory Tree = SQLite 元数据 + Obsidian vault 落 Markdown**
   - **问题**：向量检索不可读、不可信、不可手编
   - **方案**：树形结构（source/topic/day 摘要），叶子落 Markdown，索引在 SQLite
   - **Trade-off**：牺牲了向量检索的"模糊性"，换得"可见即可改"
   - **可迁移性**：高（任何 LLM agent 都能借鉴）

3. **TokenJuice 三源 JSON 规则 + 自写 tokenizer + 自写 HTML stripper**
   - **问题**：三方 `html2md` crate 在大文档上爆堆（894MB）
   - **方案**：自写轻量 tokenizer + HTML stripper，规则配置可叠加
   - **Trade-off**：牺牲了"标准库的兼容性"，换得可解释 + 可降级
   - **可迁移性**：高

4. **Routing = TaskCategory × LocalHealthy × Privacy/Latency/Cost hints + 自动回退**
   - **问题**：用户不该关心「这次该用 Claude 还是本地 Ollama」
   - **方案**：按 hint 分类自动路由，失败时透明回退
   - **Trade-off**：牺牲了"绝对可控"，换得"零配置"
   - **可迁移性**：中

5. **Approval gate 默认 ON + 仅拦截交互 chat + 10min TTL**
   - **问题**：后台心跳/Subconscious 容易触发"幽灵命令"
   - **方案**：默认全拦，仅放行用户主动 chat 窗口，10 分钟缓存
   - **Trade-off**：牺牲了"全自动"的噱头，换得可审计
   - **可迁移性**：高

6. **Subagent delegation allowlist gate**（PR #3426）
   - **问题**：子代理可能成为横向移动的"代理内代理"
   - **方案**：显式 allowlist 名单 + Unknown fail-closed
   - **Trade-off**：牺牲了"开放扩展"，换得安全边界
   - **可迁移性**：高

7. **CEF child webviews "no new JS injection" 政策**
   - **问题**：嵌入第三方 web view 容易成 XSS 入口
   - **方案**：禁止在 CEF 子 webview 注入新 JS，新行为走 Rust IPC
   - **Trade-off**：牺牲了"灵活扩展"，换得安全
   - **可迁移性**：高

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | OpenHuman | Claude Cowork | OpenClaw/Hermes | Manus/Devin | Letta/Mem0/Cognee |
|------|-----------|---------------|----------------|-------------|-------------------|
| 形态 | 本地桌面（开源） | 闭源桌面+CLI | MIT 终端 | 云端商业 | SDK |
| 记忆 | Markdown vault（可读） | Chat-scoped | 插件式 | 任务级 | 向量/图 |
| 集成 | 118+ 一键 OAuth | 厂商绑定 | BYO 插件 | 有限 | 需自搭 |
| 模型 | 多家路由 | Claude 独占 | BYO | 自研 | 嵌入灵活 |
| 安全 | Approval gate + allowlist | 厂商背书 | 用户自管 | 云端隔离 | SDK 自管 |
| 学习成本 | UI-first 几点击 | 低（但闭源） | 高（CLI） | 中（云） | 高（需自搭） |

### 差异化护城河

1. **Memory Tree 不可读→可读的范式切换**：竞品里没有任何一个把记忆落地成可手编的 Markdown vault
2. **Managed-by-default + BYO**：118 个集成的 OAuth 体验不输商业产品，但**留了 BYO 逃生通道**
3. **桌面+Live Meeting+Subconscious 三角**：吉祥物加入 Google Meet 真开会 + 后台心跳反哺——是 UI-first 的最大差异
4. **TokenJuice 80% 成本压缩**：在 6 个月邮件只花"个位数美元"的口号下，**把"长期记忆"从"奢侈品"变"日用品"**

### 竞争风险

1. **Anthropic Cowork 开源化**：最危险——一旦 Cowork 把记忆层开源，OpenHuman 的"可读记忆"叙事会被快速吃掉
2. **SaaS 包装式复刻**：OAuth 代理 + 桌面壳本身不难，难的是记忆图谱的可信度
3. **OAuth 反复回归**（#2521）+ Windows 打包（#2839）：当前 critical bug 频发，社区信任承压
4. **Composio 商业关系依赖**：Composio 集成经 OpenHuman 后端代理（HMAC），一旦关系生变
5. **i18n 滞后**：6 种语言 README 但产品本体翻译滞后（en.ts 152 次修改），中文/日韩/欧洲用户上手门槛高

### 生态定位

OpenHuman 站在 **「个人 AI 入口」+「桌面代理」+「可读记忆」** 三角交集，暂时没有完全对标的产品。**它不抢云端代理的饭碗（让 Manus/Devin 做），不抢记忆 SDK 的市场（让 Letta/Mem0 做），而是抢「AI 时代的个人操作系统」**——一个在 macOS/Linux/Windows 上跑得起来、能跨 118 个 SaaS、能让你看着自己记忆长大的桌面 App。

## 套利机会分析

- **信息差**：30.9k stars 看着已不"小众"，但**桌面代理 + 可读记忆这条路线**真正看懂的开发者不多，118 个 OAuth 集成的"入口价值"被严重低估
- **技术借鉴**：
  - `Memory Tree = SQLite + Markdown vault` 可直接迁移到任何笔记/CRM/项目管理系统
  - `TokenJuice 三源 JSON 规则` 适合任何 LLM 应用做成本控制
  - `Cheap-only → LLM 短路` 是 LLM 工业化的"必修课"
  - `Approval gate + subagent allowlist` 可借鉴到任何多 agent 系统
- **生态位**：填补「AI 时代个人操作系统」空白；Karpathy obsidian-wiki 思想**第一次工业化落地**
- **趋势判断**：
  - 增长明确（4 个月 31k，5 月单月 1,269 commits）
  - 符合「AI 代理桌面化」+「反对向量黑盒记忆」双重趋势
  - 比 Claude Cowork **有开源 + 多模型 + 离线**三重后发优势
  - 比 Letta/Mem0 **有端到端产品**优势
  - 比 Manus/Devin **有本地 + 隐私 + 跨时区**优势

## 风险与不足

- **创始人单点风险**：senamakel 1,010 commits 占 37.4%，组织账号 0.5 年龄，**核心人物离开/过载会立刻反噬**
- **OAuth 反复回归**（#2521 / #2215 / #2839）：Windows 桌面端稳定性是技术债大头
- **refactor 占比仅 2.5%**：feature/fix 拉锯期累积的代码债务，未来 1-2 个 minor 版本可能要集中重构
- **GPL-3.0 协议争议**：商业 fork 必须开源，对国内厂商/二次开发是个门槛
- **i18n 滞后**：6 种 README 但 en.ts 单文件 152 次修改——**多语言运营 vs 产品翻译**的优先级失衡
- **架构师式 complexity**：`bucket_seal.rs` 双策略 + `flush_stale_buffers` + 7 信号打分——**心智成本不低**，新贡献者上手慢
- **依赖锁定紧耦合**（#2839）：Homebrew formula 与 Rust std 上游版本不兼容，**升级工具链需要密集测试**

## 行动建议

- **如果你要用它**：
  - **适合**：跨多 SaaS、需要长期记忆的「知识工作者」+ 重视隐私的「本地优先」开发者
  - **不适合**：仅需一次性任务 + 极简 CLI 体验 + Windows-only 工作流（OAuth bug 多）
  - **建议**：先在 macOS / Linux 上跑，v0.57.x 系列比 v0.54 稳；Composer 体验最佳
  - **可降级到**：Claude Cowork（如果你信任闭源），或 OpenClaw（如果你只要 CLI）

- **如果你要学它**：
  1. **`src/openhuman/memory_tree/`** — Memory Tree 完整实现（bucket_seal.rs, score/signals/ops.rs），先看这
  2. **`src/openhuman/tokenjuice/`** — 三源 JSON 规则 + 自写 tokenizer + HTML stripper
  3. **`src/openhuman/agent/turn_origin.rs`** — 5 个 Origin 标签 + Unknown fail-closed
  4. **`src/openhuman/subconscious/engine.rs`** — Subconscious 心跳 + tick_origin_source
  5. **`src/openhuman/routing/`** — TaskCategory × RoutingHints + 透明回退
  6. **`src/core/jsonrpc.rs`** — 2,315 行 transport 总入口，结构化错误处理
  7. **`AGENTS.md`** — 18KB 提示词模板，是项目级「宪法」
  8. **`docs/` + `gitbooks/`** — 完整文档库（46K+ 行 .md，6 语言）

- **如果你要 fork 它**：
  - 改 OAuth 回归 + 打包链路，是 6 个月内最容易的"贡献"
  - 集中重构 `src/openhuman/`（10,251 次修改）——refactor 占比 2.5% 是真空白
  - 中文化产品本体（i18n parity CI 已经搭好，en.ts 152 次修改是既成事实）
  - 实现"非 Anthropic 商业绑定"路径（不接 Claude Agent SDK），避开 #2479 暗示的计费耦合
  - 探索 Subconscious 心跳反哺（5 个 Origin 标签 + ReflectionStore 已有完整基础设施）

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [OpenHuman Overview](https://deepwiki.com/tinyhumansai/openhuman/1-openhuman-overview)（2026-05-22 索引）|
| Zread.ai | 未收录 |
| 关联论文 | 无显式 arXiv 引用；哲学源头为 [Karpathy 的 obsidian-wiki 实践](https://github.com/karpathy/obsidian-wiki) |
| 在线 Demo | 无在线 demo（产品形态是本地桌面 App，macOS/Linux/Windows 都有原生安装包） |
| 完整文档 | [OpenHuman GitBook](https://tinyhumans.gitbook.io/openhuman/) |
| 官网 | [tinyhumans.ai/openhuman](https://tinyhumans.ai/openhuman) |
| 中间产物 | [tmp/openhuman-content-analysis.md](../tmp/openhuman-content-analysis.md) |

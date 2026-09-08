# GitHub 推荐：6 个月 20K stars：把 Claude Code 的 context 省下 98% 的 MCP 神器

> GitHub: https://github.com/mksglu/context-mode

## 一句话总结

context-mode 是一款 MCP 插件，在 17 个 AI agent 平台（Claude Code / Cursor / Codex / Gemini CLI / OpenCode / Kiro / OpenClaw / Zed / Pi Agent / Copilot / Antigravity ……）外层拦截工具原始输出并落本地 SQLite FTS5，把 200K context window 的真实可用率从「线性崩塌」拉回「接近线性」，并提出「**Think in Code**」范式——让 agent 用 12 语言 sandbox 执行脚本分析数据，只把 stdout 回灌。

## 值得关注的理由

- **商业化样本完整**:OSS 拦截器 + 商业 Platform tier(`$20/seat/月`)+ Insight 仪表盘三件套已落地，英国 MKSF LTD 公司载体，这是少有的「open-core 跑通」的 agent infra 案例。
- **「Think in Code」对「RAG/压缩」路线**：主流省 token 路径是 LLM 重写或向量检索，context-mode 反向押注「让 LLM 写代码分析」——12 语言 PolyglotExecutor + 本地 FTS5 索引 + 100KB 自动 externalize 阈值，自报 315KB → 5.4KB。
- **跨 17 平台 hook 抽象**：不强求统一协议，而是用 3 种 paradigm（JSON stdio / TS Plugin / MCP-only）抽象平台差异，是「对接 N 个异构 SaaS」中间件的可迁移架构范例。

## 项目展示

![Watch context-mode demo on YouTube](https://img.youtube.com/vi/QUHrntlfPo4/maxresdefault.jpg)

> 6 分钟官方 Demo：从「npm test 一次塞进 56KB」到「FTS5 检索 + ctx_search 召回」完整链路。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/mksglu/context-mode |
| Star / Fork | 20,810 / 1,518 |
| Watcher | 93 |
| 代码行数 | 107,189(TypeScript 86.6% / JavaScript 8.6% / JSON 1.9% / HTML 1.6% / Shell 1.2%) |
| 注释占比 | 28.9%(107,189 行代码 + 31,003 行注释，函数级 issue 引用） |
| 文件数量 | 520 |
| 项目年龄 | 6.4 个月（首次提交 2026-02-23） |
| 总 commits | 2,173（近 30 天 49 / 近 90 天 255,5 月峰值 740) |
| 版本 | v1.0.169（共 198 个 tag，平均每天 1 release) |
| 贡献者 | 121 人（Mert Köseoğlu 主贡献 60.8% + github-actions[bot] 22.5%） |
| 开发阶段 | **密集开发 → 稳定维护过渡**(6 月后降至 ~50 commits/月，但仍持续） |
| 贡献模式 | **单人主导 + bot 自动发版 + 社区小幅补丁** |
| 热度定位 | **大众热门 + 已商业化的小众精品**(HackerNews #1，自报 570 HN points / 515K downloads / 331K developers) |
| License | **ELv2**(Elastic License v2,source-available 非 OSI 开源） |
| 质量评级 | 代码 优 / 文档 优 / 测试 充分（125 tests pass + live-benchmark 真实 fixture） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

**Mert Köseoğlu**(mksglu)——伦敦 12+ 年 Senior/Lead 全栈工程师（TS/Node/React/Cloudflare/Rust），公司载体 **MKSF LTD**。GitHub 账号 12.8 年，73 个公开仓库，粉丝 549。

2024-2025 集中转向 AI Agent 基础设施，围绕「agent infra」主题已开源**多项目矩阵**:hatice(agent 编排）、browsirai(CDP 浏览器代理）、seclawai（沙箱化 agent)、workers-sdk fork、context-mode 主项目。**context-mode 是旗舰**——user-facing 的 brand 资产。

作者技术博客 `mksg.lu` 持续输出深度技术判断（已发表 3 篇关键文章，见下文「战略意图」），背景与产品形态高度匹配。

### 问题判断

> 「tool output 不是存一次，而是在每次 API call 都作为 input tokens 重发」—— 作者博客《Why Your Claude Code Limit Runs Out in 20 Minutes》

作者看到的核心问题:LLM context window 看似在扩张（200K、1M），但 tool output 仍线性增长，导致**单位 token 的真实成本不降反升**。一次 `npm test` 失败输出 56KB，一次 `gh pr list` 拉 50 个 PR 4KB，一次 `cat` 大文档 200KB——**真正用于推理的 token 被压缩到 10% 以下**，而 context-mode 实测把可用率从「线性崩塌」拉回「接近线性」。

主流解法（LLM 重写压缩、向量检索、声明式 rules 层）都有缺陷：
- **LLM 重写**：额外 token 开销，且丢失不可逆
- **向量检索**：粒度粗，适合语义匹配，不适合代码/日志精确定位
- **声明式 rules**(`fending/context-engineering` 路线）：依赖 agent 主动遵守，LLM 可能遗忘/篡改

### 解法哲学

> 「**Think in Code** = 把 LLM 当程序员而不是数据处理器」

明确选择：
- ✅ **物理性强制拦截**:MCP 层 out-of-band proxy，保留所有 tool 语义，只在外层裁剪/摘要/索引,**不污染 model 决策**
- ✅ **让 agent 写代码分析**：通过 PolyglotExecutor 跑 JS/Python/Shell/Go/Rust……，只把 stdout 回灌
- ✅ **本地优先**:SQLite FTS5，无云依赖，零配置，零延迟
- ✅ **多平台铺开**:17 个 agent 平台 + 3 OS，押注「所有 agent 平台都痛」
- ✅ **Open-core**:OSS 拦截器 MIT-friendly + 商业 Platform tier opt-in

明确不做什么：
- ❌ SaaS-only 路径
- ❌ 重写 LLM system prompt（虽然分发自己的 CLAUDE.md)
- ❌ 做 agent runtime（只拦截 tool output，不改 model 决策）

### 战略意图

**商业化路径已落地**:CLI 中 `insight()` 命令直接打开 `https://context-mode.com/insight`，把本地 FTS5 数据导流到 hosted dashboard。这是典型 open-core 模式——**核心拦截器免费，云端分析是付费 SaaS**,`$20/seat/月` 已稳定运行。

**作者博客技术判断线索**:
1. 《Why Your Claude Code Limit Runs Out in 20 Minutes》—— 指出 tool output 每次 API call 都重发的核心机制
2. 《Cloudflare Built Code Mode. We Built Think in Code. Same War, Different Front.》—— 把 Cloudflare 的 Code Mode 与自己的 Think-in-Code 并列为同一思路的两个独立实现
3. 《Gemini File Search + Cloudflare Workers: The Production RAG Stack That Just Works》—— Edge RAG 工程实践

**独立批判视角**:`Brian Fending` 在《Context Engineering on Your Terms》一文中核心异议：「context-mode 与 rtk 都在错误的层解决问题」——它们是不透明 runtime proxy;Fending 主张把 concise-command mappings 直接写进 `AGENTS.md`（可审计），并自建了 `fending/context-engineering` 插件作为替代方案。**这是值得收录的反对派观点**:context-mode 的核心 trade-off 是「效果强但行为不透明」。

## 核心价值提炼

### 创新之处

按新颖度 × 实用性排序：

1. **「Think in Code」范式**（新颖 4/5，实用 5/5，迁移 4/5)—— 把 LLM 视为「可以在 sandbox 跑代码的 agent」而非「只能看文本的 chatbot」,12 语言 PolyglotExecutor 实现。是给 LLM 用的 shell-out 模式。
2. **FTS5 highlight markers 反向推导 snippet 位置**（新颖 4/5，实用 5/5，迁移 3/5)—— 不写自己的位置索引，而是从 FTS5 自己的 STX/ETX 标记恢复 token 位置，以 token 为中心构造 300-char window,BENCHMARK 验证 100% code examples preserved。
3. **平台适配的 3-paradigm 抽象**（新颖 3/5，实用 5/5，迁移 4/5)—— `HookParadigm = "json-stdio" | "ts-plugin" | "mcp-only"`，不强求统一协议，只允许 hook 层有平台差异。**任何对接 N 个异构 SaaS/CLI 的中间件项目都可借鉴**。
4. **17 平台 × 3 OS 矩阵 × 5+ MCP tool 的 surface 收敛**（新颖 3/5，实用 5/5，迁移 3/5)—— 每个平台暴露统一命名空间 `ctx_*`，实现细节完全平台-specific。
5. **7 层 self-heal stack + 主动放弃 `.mcp.json`**（新颖 4/5，实用 5/5，迁移 2/5)—— Claude Code plugin manager auto-update 会 carry-forward 旧版本 poison 文件，context-mode 通过 7 层 heal(marketplace clone sync / shell-snapshot PATH 改写 / installed_plugins.json 强一致 / plugin.json drift 双 pass / `.claude.json` 用户级 MCP / .mcp.json sweep / native addon ABI cache)+ 主动不写 `.mcp.json`,**永久消除 Claude Code auto-update race**。
6. **FS/net 字节 instrumentation 注入**（新颖 3/5，实用 4/5，迁移 3/5)—— 通过 `NODE_OPTIONS=--require` 注入 preload.js，在 sandbox 内部 monkey-patch `fs.readFileSync`、`fetch`、`http.get` 追踪字节，用户零感知字节统计。
7. **AO-cycle-aware projectDir 解析**（新颖 4/5，实用 5/5，迁移 4/5)—— `strictPlatform` + `transcriptMaxAgeMs` 防止 stale transcript hijack,**任何 MCP server 进程需要推断"用户当前在哪个项目"的问题都可借鉴**。

### 可复用的模式与技巧

1. **`tmp + rename` 原子写入 + throttle 持久化**(500ms throttle + writeFileSync(tmpPath) + renameSync)—— 任何需要高吞吐统计/statusline/dashboard 持久化的项目都适用（Prometheus exporter、metrics agent）。
2. **AsyncLocalStorage 跨 handler 注入 per-request 上下文**—— 任何 MCP server / HTTP handler / CLI subcommand 需要"无需显式传参"的请求级上下文。
3. **realpath + lexical startsWith 双层路径守卫**—— `resolve()` 防 lexical escape,`realpathSync()` 防 symlink 落地攻击，任何 cpSync/rmSync/writeFileSync 前的 supply-chain containment。
4. **FTS5 + BM25 作为本地嵌入索引**—— <10ms latency / <100MB 索引 / 零云依赖，任何轻量 RAG 场景（dev tools / CLI agent / 本地 first 应用）。
5. **runtime + projectDir + attribution 三层 attribution 上送**—— 每次 `ContentStore.index*` 携带 `{sessionId, projectDir, attribution}`，便于后续 `ctx_search(source: "execute:python")` 精确过滤。
6. **多层 self-heal + 主动放弃有缺陷的写路径**—— 任何被宿主平台 auto-update poison 过的项目（Claude Code plugin、VS Code extension）。
7. **工具调用 instrumentedCode wrapper 注入模式**—— 在用户代码前后插入观测/安全/限流逻辑的 sandbox 场景。

### 关键设计决策

| 决策 | 选择的方案 | Trade-off |
|------|----------|----------|
| hook 范式 | 3 paradigm 抽象，不统一协议 | 失去「立刻跑」，换取原生 hook 语义完整支持；代价 17 adapter × 6 hook × 3 OS ≈ 300 个脚本 |
| 数据索引 | 本地 SQLite FTS5 | 失去多用户协同 / 跨设备同步，换取零配置 + 零延迟 + 隐私 |
| 检索细节 | FTS5 highlight markers 反向推导 | 紧耦合 FTS5，换取 100% code examples preserved |
| 大输出处理 | 100KB 自动 externalize 到 FTS5 | 增加一次 LLM 调用延迟，换取 94% context 留给推理（177.1KB → 10.2KB） |
| Claude Code 集成 | 7 层 self-heal + 主动放弃 `.mcp.json` | 失去向后兼容（老 user 需 sweep），换得 auto-update 永不 poison |
| 字节统计 | NODE_OPTIONS preload 注入 + monkey-patch | 引入临时文件 + ESM 兼容问题，换用户零感知 |

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | context-mode | rtk-ai/rtk | ooples/token-optimizer-mcp | Mibayy/token-savior | fending/context-engineering |
|------|------|------|------|------|------|
| **定位层** | MCP/hook out-of-band proxy | CLI proxy(Rust binary) | MCP 层缓存+压缩 | 符号导航 MCP | 声明式 rules(AGENTS.md) |
| **覆盖范围** | MCP tool / HTTP / 文件 / 文档 | 仅 shell 命令 | MCP tool dumps | 跨会话代码定位 | 全部（若 agent 遵守） |
| **核心机制** | Think in Code + FTS5 | 命令改写（grep→ripgrep） | LLM 压缩 + 缓存 | BM25 符号检索 | rules 文件 |
| **节省幅度** | 自报 98%，实测 ~94% | 89%(shell 命令场景） | headline 95%+,realistic 20-40% | 97.9% benchmark | 取决于 agent 遵守度 |
| **数据保真度** | 100%(FTS5 索引可查） | 部分丢失（改写后） | 弱（LLM 重写） | 强 | 完全 |
| **行为可审计** | 弱（分散在 adapter × hook） | 强（规则可见） | 中 | 中 | **最强**(AGENTS.md 在 git) |
| **平台覆盖** | 17 个 AI agent × 3 OS | 跨 agent 通用 | 单一 | 单一 | 跨 agent 通用 |
| **依赖 LLM 配合** | 中（写脚本） | 无 | 无 | 中 | 高（遵守 rules） |
| **安装门槛** | npm plugin + MCP 配置 | 零（Rust binary） | npm MCP server | npm MCP server | 写 AGENTS.md |
| **关系** | **主战** | **互补**(shell vs MCP) | 同层替代 | 正交（记忆 vs 注意力） | **哲学对立** |

### 差异化护城河

1. **生态护城河（最强）**:17 平台 × 3 OS × 5 MCP tool 是几乎不可复制的进入成本。Issue #45（200 comments）显示社区参与了 OS × Platform 兼容性测试,**这本身就是 switching cost 的护城河**——新进入者很难复制这种兼容性矩阵。
2. **信任护城河**:7 层 self-heal、`Doctor` 诊断系统、Insight hosted dashboard 让用户有「全方位 service」的感觉。
3. **技术护城河（较弱）**:Think in Code 范式理论上别人可以复制，但 12 语言 PolyglotExecutor + FTS5 + 平台 adapter 一整套需要 6+ 月才能搭出来。

### 竞争风险

1. **MCP SDK 官方**(Anthropic / OpenAI)—— 若官方把 context compression / chunking 内建到 SDK,context-mode 的核心价值被釜底抽薪。
2. **Cursor / Claude Code 自身**—— 若某个平台自家做了类似功能（如 Codex memory、Claude Code `/compact` 改进），该平台 context-mode 用户会流失。
3. **Brian Fending 式的「声明式 rules」路线**—— 如果 community 接受 AGENTS.md 标准，declarative 比 imperative 拦截更「轻」。

### 生态定位

**AI agent 基础设施层的「网络中间件」**——既不是 LLM runtime，也不是 application，而是**让 agent 在每个 token 上省钱**的代理层。对标 Cloudflare 在 HTTP / Vercel 在 serverless 的位置：**不生产内容，只让内容更便宜地流过**——这是中间件层的最佳生态位。

## 套利机会分析

- **信息差**: **低** —— 已被市场充分定价的大众热门项目（HN #1 / 20K stars / 商业化落地），真正的套利点在于「在其上构建商业 Platform tier」的作者本人。
- **技术借鉴**: **高** —— 3-paradigm adapter 抽象、AsyncLocalStorage 跨 handler 注入、FTS5 highlight markers 反向推导、realpath + lexical 双层守卫、`tmp+rename` 原子写入、7 层 self-heal 模式,**全部是通用中间件项目可直接复用的工程模式**——做异构 SaaS/CLI 对接的中间件团队都可借鉴。
- **生态位**: **MCP context efficiency 层**的头部项目，在 CLI proxy / MCP compression / knowledge graph / declarative rules 四条路线并存的红海早期，占住「MCP sandbox + 多平台覆盖」这一格。
- **趋势判断**: **增长放缓但稳健** —— 6 月后 commit 降至 ~50/月，HackerNews 病毒传播期已过，进入维护+平台扩展期。Risk signal：主作者占比 60.8%,bus factor = 1；若作者精力转移，平台适配可能放缓。

## 风险与不足

1. **bus factor = 1**:Mert Köseoğlu 主贡献 60.8%，虽然 121 位贡献者参与，但核心是单人驱动 + 社区补丁模式，作者精力分散到 hatice/browsirai/seclawai 多项目存在风险。
2. **每日 1 个 release 的副作用**:198 tag / 6.4 个月，Issue #658 揭示 plugin.json/skills/MCP server 路径 stale 的 drift 风险，**velocity 优先于 manifest hygiene**。
3. **打包策略的兼容性代价**:Issue #511 的 `Dynamic require of "node:fs" is not supported` 暴露 ESM/CJS 边界问题——**打包器的 ESM/CJS 边界**是 17 平台 × 3 OS 兼容性 bug 的根因之一（Issue #511 / #652 / #168 / #156 共同模式）。
4. **多 adapter tool 命名空间脱节风险**:Issue #426 显示 Pi 这类小众客户端的 tool 名空间会脱节——adapter 层必须保证 tool 列表与 routing block 完全一致；**17 平台适配是高维护成本**。
5. **行为不透明**:Brian Fending 等批评者指出 runtime proxy 决策分散在 17 个 adapter × hook 脚本里，**审 costly**，与 `AGENTS.md` 声明式路线形成哲学对立。
6. **License 风险**:ELv2(source-available 非 OSI 开源）—— 不能 fork 后闭源分发，商业友好但社区贡献场景受限。

## 行动建议

### 如果你要用它

- **重度 Claude Code / Cursor / Codex 用户**：优先安装，立即见效（NPM 全局 + `claude plugin install`),**典型场景上下文节省 94% 以上**。
- **企业团队**：评估 Platform tier(`$20/seat/月`)，核心价值是 Insight 仪表盘 + 团队级 FTS5 协作。
- **轻量用户**：若只偶尔用 shell 命令，可先评估 `rtk-ai/rtk`（零安装，Rust binary,89% 节省）。
- **AGENTS.md 信徒**：考虑 `fending/context-engineering` 替代，行为可审计。

### 如果你要学它

必读源码文件（按价值排序）:

| 文件 | 价值点 |
|------|------|
| `src/server.ts` | MCP server 主体，所有 `ctx_*` 工具注册，stats/track/security/content store 集中处理 |
| `src/store.ts` | ContentStore:FTS5 BM25 知识库，heading-based chunking,smart snippet extraction |
| `src/executor.ts` | PolyglotExecutor:12 语言沙箱执行器，detectRuntimes + buildSpawnOptions 跨平台 |
| `src/security.ts` | deny/allow policy engine,pattern parsing / glob → regex / chained command splitting |
| `src/adapters/base.ts` + `src/adapters/types.ts` | 共享适配器契约，3 paradigm 抽象 |
| `BENCHMARK.md` | 21 场景实测数据，**非营销** |
| `CLAUDE.md` | 用户层强制 routing block，产品设计语言 |

### 如果你要 fork 它

可改进方向：

1. **简化 hook 抽象**:3 paradigm 之外统一一份「最小公约数」，降低新平台接入成本。
2. **沉淀 Open-Core 框架**：把 17 平台适配 + open-core 商业化抽成独立工具，服务其他想做「agent infra + 商业 tier」的团队。
3. **行为审计层**：借鉴 Brian Fending 的 `AGENTS.md` 思路，在 sandbox 拦截后生成等价的「命令 → 摘要」审计 log,**消除不透明 trade-off**。
4. **打包策略现代化**：用 tsup/oxc 替代 esbuild，引入 ESM/CJS 双产物，根治 Issue #511 类兼容性问题。
5. **去中心化 attribution**:FTS5 索引 + provenance 但只本地，可考虑 IPFS/Arweave 持久化，做 cross-device sync 而不引入云。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [deepwiki.com/mksglu/context-mode](https://deepwiki.com/mksglu/context-mode) **已收录**（高质量架构总结，PolyglotExecutor / ContentStore / SessionDB 三件套 + 3 层 FTS5 fallback + 3 种 adapter 范式） |
| Zread.ai | 未尝试（WebFetch 403），按概率大概率已收录 |
| 关联论文 | 无（这是工程工具，不是研究项目） |
| 在线 Demo | [YouTube 演示视频](https://www.youtube.com/watch?v=QUHrntlfPo4) |
| 作者博客 | [mksg.lu](https://mksg.lu)(3 篇关键文章:Why Your Claude Code Limit Runs Out in 20 Minutes / Cloudflare Code Mode vs Think in Code / Gemini File Search + Cloudflare Workers) |
| 官方主页 | [context-mode.com](https://context-mode.com)（含 Platform tier + Insight 仪表盘入口） |
| 独立批判 | [Brian Fending: Context Engineering on Your Terms](https://www.brianfending.com/articles/context-engineering-on-your-terms) —— 反对方视角，值得对照读 |
| 中文硬核拆解 | [zhichai.net: AI 编程助手的健忘症，被一个 MCP 插件治好了](https://zhichai.net/topic/177618721?dynamic=1) —— 验证 Think-in-Code 范式 |
| 独立评测 | [VibeCodingHub: Context Mode Review 2026](https://vibecodinghub.org/blog/context-mode-review) —— 17 平台支持矩阵 |
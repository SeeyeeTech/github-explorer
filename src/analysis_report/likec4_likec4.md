# GitHub推荐：4400 stars、191 版本：LikeC4 把架构图变成 AI Agent 可直接消费的 API

> GitHub: https://github.com/likec4/likec4

## 一句话总结
用自有 `.c4` DSL 把软件架构描述成「**模型而非图**」，CLI/VSCode/JetBrains/SPA/MCP 全栈统一从同一份模型派生，让架构图永远随代码同步，并被 AI Agent **像数据库一样查询与回写**。

## 值得关注的理由
- **架构图的「图-模分离」已完成产品化闭环**：手工图永远过时，LikeC4 把模型当事实源，DSL 改动瞬间反映到所有视图；这不是又一个 Mermaid，而是 C4 Model + LSP + 模型编译器 + 渲染引擎 + 编辑器全家桶。
- **率先把架构 DSL 暴露给 AI Agent**：自带的 MCP 服务器提供 20+ 工具（`list-projects` / `query-graph` / `element-diff` / `apply-semantic-layout` 等），Agent 不再看图，而是直接查询模型；这是「代码化架构」与 LLM 工作流的天然契合点。
- **40 个月 191 个版本、CLI+编辑器+渲染+布局四件套深度集成**：Langium（解析）+ Graphviz（节点图布局）+ @lume/kiwi（序列图约束求解）+ React Flow（交互）的组合在 C4 工具里做到最深，单一作者主导也能维持月均 2.5 个正式 Release 的节奏。

## 项目展示

![LikeC4 VS Code extension](https://github.com/likec4/likec4/assets/824903/d6994540-55d1-4167-b66b-45056754cc29)
*VS Code 中编辑 `.c4` 文件时实时预览架构图，HMR 直接驱动浏览器 SPA*

![LikeC4 real-time workflow visualization](https://likec4.dev/_astro/realtime-visualization.DZL7jcxz_p5sDu.webp)
*官网展示的实时工作流：模型变化 → 视图同步 → 自动布局*

![LikeC4 product showcase](https://github.com/likec4/.github/assets/824903/c0f22106-dba6-469e-ab47-85e7b8565513)
*多视图切换：element view / dynamic view / deployment view 共享同一份模型*

![LikeC4 interactive diagram](https://github.com/likec4/likec4/assets/824903/27eabe54-7d97-47a8-a7e4-1bb44a8e03e5)
*交互式架构图：层级可折叠、节点可拖拽、连线自动避让*

> 在线试用：<https://playground.likec4.dev/w/tutorial/>

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/likec4/likec4 |
| Star / Fork | 4,400 / 305 |
| 代码行数 | 337,402 行（TypeScript 46.4% + TSX 44.5% + YAML/JSON 其他） |
| 文件数量 | 6,871 |
| 项目年龄 | 40 个月（首次提交 2023-03-24） |
| 开发阶段 | 密集开发（近 90 天 303 次 commit，v1.59.2 持续发版） |
| 开发模式 | 业余 Side Project（周末 28.7% + 深夜 49.0%，但 3 年节奏已近职业化） |
| 贡献模式 | 单人主导（Top 贡献者占比 64.5%，30 名 API 可见贡献者） |
| 热度定位 | 中等热度（Architecture-as-Code 细分领域小众精品） |
| 质量评级 | 代码[优秀] 文档[优秀] 测试[充分] CI/CD[完善] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景
核心作者 Denis Davydkov（GitHub: `davydkov`）自 2014 年起持续在 monaco-editor、graphql-js 工具链等编辑器基础设施领域贡献，对 VS Code 语言服务器协议、DSL 工程化、TypeScript 类型系统都有深度积累。LikeC4 是他「把自己擅长的 DSL+IDE 工具集能力，反向应用到软件架构领域」的产物——他看到的不是 C4 缺不缺工具，而是 C4 缺一个「能让 PR 评审通过的架构表达」。组织位于 Netherlands，仓库组合（VSCode / JetBrains / Neovim / MkDocs / GitHub Actions / examples）也透露其团队重点是「架构建模 DSL + IDE 工具链 + 文档集成」。

### 问题判断
Denis 反复强调的反常识命题是：**架构图最大的敌人不是复杂度，而是「跨视图一致性」**。手工画的图在 PR 评审里根本无法被验证，跨视图必然出现不一致（同一个服务在 Component 图和 Deployment 图里叫不同名字），且没有人愿意手工维护文档图。手工画的图在 PR 评审里根本无法被验证，跨视图必然出现不一致（同一个服务在 Component 图和 Deployment 图里叫不同名字），且没有人愿意手工维护文档图。C4 Model 给出了正确的「模型分层 + 视图投影」概念，但截至 2023 年所有落地工具要么是 SaaS（IcePanel）、要么把图当事实源（PlantUML/Mermaid）、要么 IDE 体验割裂（Structurizr Lite）。LikeC4 选择的时机是 Langium 这类 DSL 框架成熟 + Graphviz WASM 可用 + LLM Agent 开始吃工具的窗口期，三者叠加才让「模型即文档 + AI 友好」有了技术底座。

### 解法哲学
**模型即文档（Model-as-Document）**：图形只是模型的一次性投影，DSL 改动瞬间反映到所有视图。**小而专的视图 DSL**：specification / model / views / deployment / globals 五块分离，predicate 决定视图内容（`include` / `exclude` + `where` + `with`），视图完全由谓词组合派生。**故意不做什么**：不绑 SaaS、不绑某个图引擎、不绑某个渲染器；不替代 Graphviz（而是给 Graphviz 出 hints）；不强推协作后台（VSCode 协同通过 manual layout + Git 完成）。这种克制让 LikeC4 不会陷入「自己重写所有组件」的陷阱，把力量集中在「DSL 解析→模型计算→视图 predicate→布局适配→渲染」这条主链路的工程深度上。

### 战略意图
LikeC4 是核心产品也是战略锚点。MIT license + OpenCollective/GitHub Sponsors 资助 = genuinely open，没有企业版闭源。商业化路径有两层：一是 `leanix-bridge` 包提供与 LeanIX（企业架构管理 SaaS）的双向同步，桥接而非替代；二是 MCP 暴露的 `apply-semantic-layout` 工具通过 `sampling/createMessage` 反过来调宿主 LLM，让 Agent 在不直接看图的情况下「AI 增强布局」。换句话说，LikeC4 不和 SaaS 抢用户，而是让所有架构 SaaS 都愿意接入的「模型 + 视图标准」。这也是为什么 issue #2636「Claude/Agent skill」成为社区最热议题——项目正在从「给人看的架构图」扩展为「给 Agent 消费的架构上下文」，产品边界正在被重新定义。

> 官网未发布独立技术博客；架构设计哲学散落在 AGENTS.md、docs 教程与 `packages/core/src/model/views/` 注释中。

## 核心价值提炼

### 创新之处

| 创新点 | 新颖度 | 实用性 | 可迁移性 |
|---|---|---|---|
| **三阶段 Model 流水线 + Phantom-Type Ledger**：`Parsed/Computed/Layouted` 三套 `[$stage]` 品牌类型 + `Aux<Stage,…>` 辅助类型，把 DSL 字面量固化到 TS 类型系统 | 4/5 | 5/5 | 4/5 |
| **Predicate-driven views with Memory+Stage**：视图求值建模为「显式集+隐式集+连接集+分组」累积状态机，`include cloud.backend.api` 自动拉入祖先 `cloud.backend` | 5/5 | 5/5 | 3/5 |
| **AI Layout Advisor（LLM → Graphviz hints → DOT）**：把 AI 美化布局严格约束在 `AILayoutHints` 结构化 schema（ranks/edgeWeight/invisibleEdges 等）内，失败时静默回退 | 4/5 | 4/5 | 4/5 |
| **Graphviz 双适配器 + 队列化执行**：`GraphvizPort` 接口抽象 + `GraphvizWasmAdapter`（每 20 次强制 unload 防内存泄漏）+ `GraphvizBinaryAdapter`（nano-spawn 调 dot/unflatten） + `QueueGraphvizLayoter`（`p-queue` + batch 防并行递归锁） | 3/5 | 5/5 | 5/5 |
| **Sequence Layout 用 Cassowary 约束求解器 (@lume/kiwi)**：行高/列间距/subflow 嵌套全部建模为 Strength 约束，而非手工布局循环 | 4/5 | 4/5 | 3/5 |
| **MCP-as-Model-API**：模型完整暴露为 20+ zod-validated 工具，95% `readOnlyHint + idempotentHint`，唯一修改工具通过 snapshot + schema 校验限爆炸半径 | 4/5 | 5/5 | 5/5 |
| **Manual Layout Drift Detection**：用户拖拽改坐标 + 模型重算的三向 merge（auto-apply style/icon；5px 阈值过滤坐标漂移；显式标记 added/removed） | 3/5 | 5/5 | 4/5 |

### 可复用的模式与技巧
- **DSL → TypeScript Phantom-Type Bridge**：`Types<…>` 累积字面量 + `Builder<T>` 链式返回 `Builder<Out>` + `BuilderMode` ('editable'/'strict')，任何「DSL 即代码」项目都能套（适用：GraphQL schema builder、AWS CDK、Terraform DSL）。
- **Predicate-driven view computation**：policy-as-code 工具可以用同样模式做规则累积执行（适用：ArchUnit、Sentinel、OPA）。
- **AI-enhancement as structured hints + silent fallback**：LLM 输出严格 schema 失败时静默回退到纯算法骨干（适用：SQL 查询计划、UI 自动着色、报表生成）。
- **Vite virtual module + birpc over HMR**：`likec4:rpc` 命名空间 + dev 模式 RPC + 生产模式静态 JSON（适用：任何「编辑器 HMR ↔ 浏览器 SPA」需要双向同步的工具）。
- **MCP tool taxonomy (read-only hint vs mutation hint)**：把领域 API 暴露给 Agent 时，95% 工具标 read-only，唯一修改工具走 snapshot + zod 校验（适用：数据库工具、CI 工具、文档工具）。
- **Layered pnpm monorepo with import direction rules**：每个包 AGENTS.md 强制规定「imports flow upward only」（适用：任何需要长期维护的中大型 monorepo）。

### 关键设计决策
- **「成熟组件 + 自有胶水」而非自研**：Langium 提供 DSL 解析+作用域+补全+LSP scaffolding（1254 行 grammar）；Graphviz 负责节点图布局（DOT 作为 IR）；@lume/kiwi 做序列图约束求解；@xyflow/react 做交互渲染；自己不重写任何环节，只做适配层。
- **DSL 写回有意为之的有损化**：`LikeC4.toDSL()` 明确不保留注释/位置/格式，把「load + patch + emit」作为合法工作流（外部事实源 → DSL），把「format」工作流明确排除——这是工程化的诚实。
- **三层 monorepo 硬约束**：core → language-server → language-services → (likec4 | vite-plugin | mcp | vscode)，导入只能向上，diagram 与 likec4-spa 同样遵循。AGENTS.md 用大量篇幅规定导入方向防止新人踩坑。
- **Graphviz WASM 偶发内存泄漏的工程化应对**：每 20 次操作强制 `Graphviz.unload()` 重启 + 失败重试 30ms 抖动；不是 fix 根源，而是把不稳定性变成可控的运维模式。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | LikeC4 | Structurizr DSL | C4-PlantUML | Mermaid | IcePanel |
|---|---|---|---|---|---|
| 模型/图定位 | 模型即事实源 | 模型即事实源 | 图模板 | 图模板 | 可视化模型 |
| IDE 集成 | VSCode+JetBrains+Neovim | Lite 桌面/Web | 仅图片渲染 | 仅图片渲染 | Web SaaS |
| 视图谓词 | ✅ 完整 predicate 系统 | ✅ element/filtered | ❌ | ❌ | ✅ 可视化筛选 |
| 动态视图（sequence） | ✅ + 自动布局 | ⚠️ DSL 表达力有限 | ✅ via PlantUML | ✅ via sequenceDiagram | ✅ 可视化 |
| LLM / Agent | ✅ MCP 20+ 工具 + AI Layout | ⚠️ 间接 | ❌ | ⚠️ 仅文本生成 | ❌ |
| 自托管 / 开源 | ✅ MIT | ✅ Apache | ✅ MIT | ✅ MIT | ❌ 商业 SaaS |
| 实时渲染 | ✅ React Flow + HMR | ⚠️ Structurizr Lite | ❌ | ❌ | ✅ |
| 协作模式 | Git + VSCode | Git + SaaS | Git + 图片 | Git + 图片 | 实时多人 |

### 差异化护城河
- **技术护城河**：Langium + Graphviz + @lume/kiwi 三件套集成做得最深的 C4 工具（其他竞品要么只取其一再自己实现其余，要么干脆走 SaaS）。
- **生态护城河**：VSCode/JetBrains/Neovim/MkDocs/CI/Docker/MCP/LeanIX/Draw.io 全覆盖；`packages/generators` 支持 Mermaid/PlantUML/D2/Draw.io 互转，可作为生态节点而非孤岛。
- **信任护城河**：MIT + OpenCollective + 3.3 年 108 followers + 30 contributors + 191 个版本标签；top 贡献者占 64.5% 不算社区化，但「单人主导 + 稳定节奏 + 完整工具链」在 C4 工具里是最稳的。

### 竞争风险
- **最可能被「LLM 直接画图」产品替代**：ChatGPT/Claude 直接生成 draw.io/Excalidraw 的体验正在快速提升，LikeC4 的护城河在于「模型可被 Agent 反复查询修改」，如果 Agent 直接画图习惯固化，DSL-first 工作流会被绕过。
- **最可能被「GitHub 内置架构图工具」侵蚀低复杂度用户**：Mermaid 已经在 GitHub README 原生渲染，LikeC4 的入门门槛（DSL 学习曲线）对「只想画一张图」的开发者仍然偏高。

### 生态定位
在整个技术生态中，LikeC4 扮演「代码化架构文档的事实源标准 + AI Agent 友好的模型 API」角色。它给人类架构师 DSL-first 工具（VSCode + 实时预览），也给 Agent 提供结构化模型查询/修改能力（MCP + LeanIX bridge）。在 Structurizr DSL（最接近的理念竞品）发展缓慢、Mermaid 只解决「画图」不解决「维护」的格局下，LikeC4 占据了「中等复杂度、需要长期维护、想用 LLM 协作的团队」这个明确生态位。

## 套利机会分析
- **信息差**：4,400 stars + 191 版本 + 40 个月持续维护 + MCP 集成，Architecture-as-Code 细分领域内**关注度严重低估**——很多架构师只听过 C4 没听过 LikeC4，把它当 Structurizr Lite 替代品的认知是错误的（功能面其实更深）。
- **技术借鉴**：`DSL → Phantom-Type Builder` 模式可移植到任何「DSL 即代码」场景；`Predicate + Memory + Stage` 状态机可移植到 policy-as-code；`AI hints + 静默回退` 范式可移植到所有「传统算法骨干 + LLM 微调」场景。
- **生态位**：填补了「C4 + AI Agent + 自托管 + 现代 IDE」四象限空白；和 Structurizr（缺现代 IDE+Agent）、IcePanel（缺自托管+DSL）、Mermaid（缺架构语义）的错位都很明显。
- **趋势判断**：① 增长中：v1.59.x 发版频率（每月 2.5 个正式 Release）持续；② 符合 LLM-Agent 化趋势：MCP 是 2025-2026 年最热门的 Agent 接入协议；③ 比 Structurizr 有后发优势：现代 TS/React/Langium 技术栈的边际成本远低于维护 10+ 年历史的 Java/Lite 客户端。

## 风险与不足
- **单人主导风险**：Top 贡献者占 64.5%，社区参与度虽存在但深度依赖作者；`davydkov` 一旦退出节奏会受影响。
- **业余 Side Project 的可持续性**：深夜提交占 49.0%，作者全职工作之外的精力能否再支撑 3+ 年是个未知数。
- **Phantom-Type 体系的 onboarding 成本**：AGENTS.md 专门有「Builder type-loss when loading from runtime data」一节解释，新人理解三阶段品牌类型 + Builder 链式 + `Aux` 辅助类型需要 1-2 周。
- **Graphviz 自动布局在高密度视图下仍然糟糕**（issue #1624）：AI Layout Advisor 是缓解而非根治，对几百个节点的单视图仍需手工拆分。
- **DSL 写回的有损性**：注释/位置/格式不保留，限制了「DSL 即开发语言」的可能（VSCode 保存时不能格式化）。
- **Zread.ai 收录不可用**（Cloudflare 403），学习者多走 DeepWiki；外部深度分析文章稀缺，SEO/内容生态还需要作者本人补。

## 行动建议
- **如果你要用它**：选 LikeC4 当你的（1）团队需要长期维护的架构文档、（2）想用 LLM Agent 查询/修改架构、（3）拒绝 SaaS 锁定、坚持 GitOps 中任一条满足时。简单的「画一张 C4 图」请直接用 Mermaid。
- **如果你要学它**：必读文件 `packages/core/src/model/views/`（`memory.ts` + 6 个 stage + 8 个 predicate，理解视图谓词的状态机本质）+ `packages/language-server/src/like-c4.langium`（1254 行 grammar，看 Langium 怎么把解析+作用域+LSP 串起来）+ `packages/layouts/src/sequence/layouter.ts`（891 行看 @lume/kiwi 约束求解的实际用法）+ `packages/mcp/`（20+ zod 工具的设计范式）。
- **如果你要 fork 它**：可改进方向——（1）补全 Zread/官方独立博客降低学习门槛；（2）开放 Builder 类型的简化模式（'strict' vs 'editable' 之外加 'loose'）；（3）增加 Graphviz 之外的 layout 后端（如 dagre/elk）；（4）把 AI Layout Advisor 从「实验性」升级到「默认开启」并把失败回退做成可观察事件。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/likec4/likec4 |
| Zread.ai | 未收录（Cloudflare 403） |
| 关联论文 | 无 |
| 在线 Demo | https://playground.likec4.dev/w/tutorial/ |
| 空白 Playground | https://playground.likec4.dev/w/blank/ |
| 官方文档 | https://likec4.dev/docs |
| Agent Skill | `skills/likec4-dsl/SKILL.md`（仓库内 17 个 references） |
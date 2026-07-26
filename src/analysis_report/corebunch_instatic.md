# GitHub推荐：2.8 个月破 5K star：自托管可视化静态站 Instatic 把 Webflow 锁定焦虑打包成一个 Bun 进程

> GitHub: https://github.com/corebunch/instatic

## 一句话总结

Instatic 是一款 MIT 协议、自托管、可视化编辑、原子发布为纯静态 HTML 的现代 CMS，单个 Bun 进程吃下编辑器 / 内容引擎 / 媒体 / 鉴权 / 表单 / 插件 / MCP / AI，把 Webflow 式的可视化生产力与「数据 + 产物 100% 归用户」打包在一起。

## 值得关注的理由

- **稀缺定位：**「可视化编辑 + 静态发布 + 自托管 + MCP/AI 原生」四要素同时成立的产品几乎空缺；Strapi/Payload 是动态 headless，Tina 强 Git 绑定，Builder.io 强商业锁定，WordPress 自带历史包袱。
- **作者经验真实可验证：** 主导者是 WordPress 圈 Core Framework / Motion.page 创始人 DavidBabinec，1080 commits / 99.1% 自有贡献、13 个语义化版本，闭环率极高的工程治理证明这不是「套壳 demo」。
- **架构纪律感强：** 约 81 个 architecture tests 把依赖方向、安全规则、禁用模式写成可执行契约，非常适合 Agent 协作开发与高频重构；快速迭代下仍能保持「从 SQL 到底层都是一类抽象」的整洁。

## 项目展示

![Hero 编辑器主视觉](https://instatic.com/uploads/mjbd7VIrxODSNo1N-rpkj-hero-editor.webp) — 官方 hero 主视觉，编辑器主屏

![Core Framework 设计 token 流体排版](https://raw.githubusercontent.com/corebunch/instatic/main/docs/assets/readme/design-framework.webp) — Design 支柱：颜色 / 排版 / 间距 token 化，改一个 token 全站生效

![Visual Components 类型化参数编辑](https://raw.githubusercontent.com/corebunch/instatic/main/docs/assets/readme/build-components.webp) — Build 支柱：可视化组件的参数化编辑面板

![Media workspace 文件管理器](https://raw.githubusercontent.com/corebunch/instatic/main/docs/assets/readme/manage-media.webp) — Manage 支柱：内建媒体工作区

![Dashboard 12 栅格可定制](https://raw.githubusercontent.com/corebunch/instatic/main/docs/assets/readme/analyze-dashboard.webp) — Analyze 支柱：可视化 Dashboard

![Railway 一键部署动图](https://raw.githubusercontent.com/corebunch/instatic/main/docs/assets/readme/railway-deploy.gif) — Railway 一键部署 Demo

[Interface tour video](https://www.youtube.com/watch?v=zyjCF_TaLlg) — 编辑器完整导览视频

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/corebunch/instatic |
| Star / Fork | 5,102 / 481 |
| Watcher | 42 |
| 代码行数 | 335,040（TypeScript 63.3% / TSX 29.4% / CSS 6.7%，不计空行/注释） |
| 文件数量 | 3,073 |
| 依赖数量 | 74（运行时 44 + 开发依赖 30，来源 package.json） |
| 项目年龄 | 2.8 个月（首次提交 2026-04-30） |
| 总 commits | 1,080 |
| 贡献者 | 11 人（主作者 DavidBabinec 占 99.1%） |
| 开发阶段 | 密集开发（近 30 天仍有 99 次 commit） |
| 贡献模式 | 独立开发（DavidBabinec 主导） |
| 热度定位 | 大众热门（短期爆款型，2.8 月 5K star） |
| 质量评级 | 代码优秀 / 文档优秀 / 测试充分 |
| License | MIT |
| 最新版本 | v0.0.13（共 13 个 tag，语义化版本） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

`corebunch` 是 GitHub Organization，背后的实体 DavidBabinec 单人主导。同主体还运营 **Core Framework**（WordPress 圈知名的 CSS 设计系统框架）和 **Motion.page**（可视化动画 / 微交互编辑器），是真实存在的商业品牌方。账号 1.4 年龄、3 个公开仓库，但 Instatic 是其中唯一持续活跃的主仓库——意味着团队把它当作战略重心。

### 问题判断

Instatic 不是抽象市场调研驱动的题目，而是**长期 dogfooding** 的结果。DavidBabinec 与 corebunch 团队长期为 WordPress 用户解决设计系统、视觉动画、编辑体验问题，亲历了 WordPress 可扩展性的价值，也亲历了历史标记、插件信任、平台商业模式带来的摩擦。README 的动机表述很直接：「We spent years making other people's platforms bearable. Then we built the one we wanted underneath」。

时机判断同样清晰：2024–2026 年正是 AI Agent / MCP 协议进入大众视野、headless CMS 与 SSG 范式被广泛接受、Webflow/Wix 锁定焦虑被反复曝光的窗口期。一个把「自托管 + 静态可移植 + AI/MCP 原生」当作一等公民而非后加补丁的 CMS，在此刻切入有显著的红利。

### 解法哲学

核心价值观是**所有权优先、静态优先、显式信任、少而完整**。具体选择包括：

- 单 Bun 进程自托管，**不**把自己定位为多租户 SaaS；
- 发布时生成干净 HTML/CSS，**不**让 React / 编辑器属性 / 厂商 runtime 上线，动态部分才降级为服务端洞（server islands）；
- SQLite 默认 / Postgres 可切换，**不**强迫小站部署外部数据库，也不把成长路径锁死在 SQLite；
- **TypeBox 单一事实源**贯穿 HTTP / 持久化 / 插件 manifest / AI tools / MCP，明确禁用 Zod 与模型厂商 SDK；
- QuickJS-WASM 沙箱 + 显式声明 capability，**不**默认信任插件；同时诚实区分 `editor.code` 这种无法沙箱化的高危浏览器代码；
- pre-1.0 主动破坏内部 API，**不**堆兼容层；唯一明确保守的边界是数据库迁移必须增量、不可破坏。

### 战略意图

Instatic 很可能是 corebunch 从「依附 WordPress 的增强工具」升级为「拥有完整建站底座」的战略核心。Core Framework 被内建降低既有用户迁移成本；Motion.page 积累的设计师 / 代理商关系提供早期分发渠道。MIT + 无订阅 + 自托管表明当前**不**靠代码授权制造锁定，但商业意图并非不存在：Railway 推荐部署带 referral 参数、品牌官网、托管协助、模板 / 插件生态、培训或专业服务都是潜在承载。更长期看，是把 Instatic 做成「网站的本地优先操作系统」：人通过画布编辑，Agent 通过 MCP 编辑，插件通过受限 SDK 扩展，最后都收敛到可移植静态产物。Issue #262 对桌面应用的诉求正与这个方向相容。

## 核心价值提炼

### 创新之处

1. **自动静态/动态分层发布器** —— 不要求作者理解 SSG/SSR/islands，而是从模块元数据、binding、loop source、递归视觉组件中自动找出请求时节点；静态 shell 原子发布，动态片段由 ~1.1 KB IntersectionObserver runtime 延迟加载。**判定、诊断、hole 发射共用一个 walker**，规则一致性强。
   - 新颖度 5/5 · 实用性 5/5 · 可迁移性 4/5

2. **两槽 symlink 原子发布 + 版本化 live fallback** —— 完整发布在 inactive slot 构建所有页面和 hash assets，再通过 symlink rename 单 inode 切换；增量发布用 tmp + rename 单文件；读取端处理 APFS 瞬态错误并可退回 Layer B，避免「发布一半」状态。
   - 新颖度 4/5 · 实用性 5/5 · 可迁移性 5/5

3. **可视化编辑器、插件与 Agent 共用树操作协议** —— 扁平 `NodeTree` 与 tree-agnostic mutations 同时承载画布动作、patch undo、插件 RPC 与 AI/MCP 工具；AI 产物是可继续编辑、撤销、发布的真实节点，而非另一个代码生成旁路。
   - 新颖度 4/5 · 实用性 5/5 · 可迁移性 5/5

4. **QuickJS-in-Worker 的插件双隔离模型** —— QuickJS 隔离 ambient authority，Bun Worker 隔离崩溃与阻塞；网络层加入 allowlist、DNS rebinding 防护与重定向逐跳复验；权限从 manifest 声明到 `grantedPermissions` 实际授权三处共享。
   - 新颖度 4/5 · 实用性 5/5 · 可迁移性 3/5

5. **MCP 与实时编辑器桥接，而非数据库旁路** —— 外部 Agent 的编辑请求被路由到指定用户当前打开的 Site/Content 工作区；服务端保留鉴权与协议，浏览器保留未保存状态与 undo 的事实权。
   - 新颖度 5/5 · 实用性 4/5 · 可迁移性 4/5

6. **AI 工具循环中的过期重证据淘汰** —— 以工具名追踪截图、整页 HTML/CSS 等「大且会过期」的 tool result，只保留最新完整版本，旧版本变成可重取 breadcrumb。
   - 新颖度 4/5 · 实用性 5/5 · 可迁移性 5/5

7. **TypeBox 贯穿 HTTP / 持久化 / AI tools / MCP** —— 同一 JSON Schema 既产生 TS 类型，又验证运行时边界，还直接成为模型与 MCP 工具定义；低级 MCP Server API 被用来绕过高层 API 对 Zod 的依赖。
   - 新颖度 3/5 · 实用性 5/5 · 可迁移性 5/5

8. **数据化设计系统直接参与发布** —— Core Framework 的颜色 shade、fluid type/spacing 与 utility 规则作为站点数据存储，生成经过 CSS value sanitizer 的小型 bundle；改一个 token，全站发布产物随之更新。
   - 新颖度 3/5 · 实用性 5/5 · 可迁移性 4/5

### 可复用的模式与技巧

- **空值路由责任链** —— handler 返回 `Response` 代表接管，返回 `null` 代表继续；命名空间吸收各自 404。可用于边缘服务 / 插件 host / 小型协议网关。
- **构建 inactive、原子切指针** —— 完整生成下一代产物后原子替换稳定入口；单项更新用 tmp + rename。可用于静态站 / 搜索索引 / 配置集发布。
- **版本捕获 + single-flight** —— render 开始时记录版本，并发请求共享 promise；版本变化则丢弃结果。可用于有后台刷新动作的动态缓存。
- **扁平节点图 + 单一 mutation 引擎** —— 节点映射获得 O(1) 定位，人类 UI、插件、Agent 都提交同一 operation union。可用于编辑器 / 工作流图 / 场景树。
- **动态边界单 walker** —— 分类、渲染决策、诊断原因从同一遍历产生，避免多层规则漂移。可用于 SSR/SSG 分层 / 权限传播 / 依赖分析。
- **声明权限与实际授权分离** —— manifest 的 `declaredPermissions` 只服务 consent，所有执行点只信 `grantedPermissions`；VM 与 host 共用 target-to-permission 映射。可用于插件平台 / 内部自动化 / Agent tool gateway。
- **高危扩展面显式分级** —— 无法沙箱化的 browser extension 不伪装安全，而是标为独立危险权限、安装必审、运行前再检查。可用于 IDE 扩展 / 浏览器内微前端 / 低代码插件。
- **架构测试作为治理层** —— 对依赖方向、禁用包、schema 边界、样式 token、生成物新鲜度写源码级 gate。可用于高频迭代、多 Agent 改动的大型单仓。
- **重证据按语义淘汰** —— 保留最新状态快照，旧快照替换为 breadcrumb，而不是按 token 截断。可用于多轮视觉 / 浏览器 / 代码 Agent。
- **小站默认、大站逃生口** —— SQLite 零依赖默认，通过窄接口保留 Postgres、多实例 leader lock 与托管备份路径。可用于从个人部署平滑成长到团队部署的自托管产品。

### 关键设计决策

1. **决策**：用单个 Bun 进程承载 CMS / 后台 / 公开站 / AI 流 / 媒体，仅把高风险或 CPU 密集工作移入 Worker。
   - **问题**：小站若依赖 Node + 队列 + DB + 对象存储 + 多微服务，部署运维成本会吞噬产品价值。
   - **方案**：`server/index.ts` 依次配置安全边界、创建 DB、跑迁移、同步角色、激活插件并启动 `Bun.serve`；插件进 Bun Worker 内 QuickJS VM；图片变体进 worker pool。
   - **Trade-off**：换来低部署门槛、统一故障观测；牺牲微服务级独立扩缩容与故障域隔离，Bun 版本被锁 `>=1.3 <1.4` 增加运行时依赖。
   - **可迁移性**：中

2. **决策**：使用有序手写 `RouteHandler[]`，以 `Response | null` 表达是否拥有请求。
   - **问题**：全栈 CMS 协议面很多，框架路由可能引入额外运行时与隐式优先级。
   - **方案**：`server/router.ts` 把 health / MCP OAuth / MCP / AI / CMS / hole / forms / 静态 / admin SPA / 公开页 / 404 按优先级排列。
   - **Trade-off**：路由顺序与所有权透明、零框架开销；URL 参数、middleware 组合、冲突检测需要自己维护。
   - **可迁移性**：高

3. **决策**：用统一 `data_tables + data_rows` 表达页面、文章、视觉组件、布局、自定义集合。
   - **问题**：每增加一种内容类型就增加专用表 / API / 编辑逻辑会让 CMS 功能分叉，插件也难以使用统一协议。
   - **方案**：系统只锁定几种内建 table kind 与系统表身份，字段 schema 决定 typed cells；页面 body 与组件 body 都是 page tree。
   - **Trade-off**：获得统一 CRUD、导入导出、表格 UI、发布与插件访问面；EAV 风格模型在复杂查询上不如专用关系表直接。
   - **可迁移性**：中

4. **决策**：把所有可编辑树统一成扁平 `NodeTree<TNode> = { nodes, rootNodeId }`，mutation 与页面/组件模式无关。
   - **方案**：节点以 ID 映射存储，O(1) 查找；slot fill 物化为消费页面中的锁定节点；11 种 store action 都经 `mutateActiveTree` 路由到同一 mutation 引擎。
   - **Trade-off**：人工 / 插件 / Agent 编辑协议统一，patch undo 只按变化量增长；children 引用、root 可达性、无环不变量需要额外维护。
   - **可迁移性**：高

5. **决策**：发布采用「磁盘静态产物 + 版本化 LRU + 自动 server islands」三层流水线。
   - **方案**：Layer A 烘焙到 inactive slot 再原子 swap；Layer B 按 `(urlPath, canonicalQuery)` 缓存，发布发生于 render 中途时丢弃旧结果；Layer C 由 `findDynamicNodeIds` 自动识别动态模块并发出 `<instatic-hole>`。
   - **Trade-off**：静态页面无 DB、无 hydration；代价是发布器、快照一致性、缓存失效、洞上下文显著复杂，Windows 缺少 POSIX symlink 只能以 live-render fallback 弥补。
   - **可迁移性**：高

6. **决策**：动态判定集中为一棵 walker，而不是让烘焙器和 hole renderer 各自判断。
   - **方案**：`dynamicDetection.ts` 的 `classifyNode` 是逐节点规则单一事实源；同一遍历处理结构化 binding、内联 token、loop source、VC 递归与 loop body 提升。
   - **Trade-off**：规则一致性与诊断性很强；默认把未知 binding source 当静态，插件扩展动态源需注册机制。
   - **可迁移性**：高

7. **决策**：插件后端采用「每插件 Bun Worker + QuickJS-WASM + capability RPC」双层隔离。
   - **方案**：宿主不直接 import 插件 server bundle；QuickJS 无 Node/Bun/syscall，API 只能经 schema 化 RPC；权限从 manifest 到 `grantedPermissions` 三处执行；VM 有内存 / 栈 / 时间预算，worker 有 RPC timeout、崩溃预算与自动恢复。
   - **Trade-off**：比传统 WordPress / Node 插件安全得多；WASM VM 内存与序列化开销大，SDK 需重复实现 Web API，生态作者不能直接使用 Node 包。`editor.code` 与 app admin page 仍在主浏览器上下文运行，只能以高危授权管理。
   - **可迁移性**：中

8. **决策**：SQLite 与 Postgres 共享极小 `DbClient` 协议，repository 保持 ANSI SQL，迁移双份但 ID 对齐。
   - **方案**：`DbClient` 只暴露 tagged template、`unsafe`、transaction、dialect；连接由 `DATABASE_URL` 决定；JSON 列以 `_json` 命名供 SQLite adapter 自动 hydrate。
   - **Trade-off**：一套 repository 支持两种部署级别；双迁移需人工保持语义一致，ANSI 子集限制了 Postgres 特性利用。
   - **可迁移性**：高

9. **决策**：TypeBox schema 是所有不可信边界与领域类型的事实源，禁止并行 schema 体系。
   - **方案**：从 `Static<typeof Schema>` 派生类型；请求 / 响应 / JSON.parse 都经共享 helper；AI provider 直接 REST/SSE，MCP 低级 SDK handler 直接发布 TypeBox JSON Schema，architecture tests 禁止 Zod / raw fetch / JSON cast / 厂商 SDK 越界。
   - **Trade-off**：类型、运行时校验、模型工具定义高度统一，vendor lock-in 较低；自建 provider mapping、SSE、重试逻辑会拖慢新 API 接入。
   - **可迁移性**：高

10. **决策**：AI provider 不使用厂商 SDK，共享直接 HTTP/SSE 的多轮 tool loop，主动削减过期重载荷证据。
    - **方案**：provider 仅实现 history mapping / body / header / turn translator；公共循环负责 fetch/SSE、tool dispatch、abort、usage；同名重载荷工具只保留最新完整结果，旧截图或页面快照替换为可重取 breadcrumb。
    - **Trade-off**：provider 矩阵扩展更轻、上下文成本可控；协议变化、边缘错误、缓存计费、多模态兼容都由项目自行追赶。
    - **可迁移性**：高

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | Instatic | Payload CMS | TinaCMS | Directus | Emdash CMS |
|------|----------|-------------|---------|----------|------------|
| 定位 | 视觉建站 + 静态发布 + 自托管 + AI/MCP | Next.js 全栈框架 + 后台 | Git-based headless | 既有 DB 包装为 headless | Astro 全栈 TS CMS |
| Stars | 5,102 | 43k | 13k | 36k | 11k |
| 输出 | 干净静态 HTML + 可选洞 | Next.js / Node 应用 | Markdown + Git | API + admin UI | Astro SSG/SSR |
| 可视化编辑 | 强（画布 + 设计 token） | 后台 admin，弱可视化 | 中等（基于 Markdown） | 数据后台 | 中等 |
| 插件隔离 | QuickJS-WASM + Worker | Node 包，无沙箱 | 无后端插件 | Node 包 | Node 包 |
| AI/MCP 原生 | 强（多 provider + MCP server） | 弱 | 弱 | 弱 | 弱 |
| License / 锁定 | MIT / 自托管 | MIT / 自托管 | Apache / 自托管 | 自托管 / 商业双轨 | 较新项目 |
| 数据库 | SQLite 默认 / Postgres 可切 | MongoDB / Postgres | Git 文件 | 任意 SQL | Postgres / SQLite |

### 差异化护城河

最难复制的不是单项 feature，而是作者多年 WordPress 视觉工具经验形成的组合：

- **Core Framework 设计系统** + **真实画布** + **统一可编辑树** + **AI/MCP 共用 mutation 协议** + **干净静态输出** + **按不可信插件设计的 QuickJS capability runtime**——六者共享同一内容模型与编辑状态机。竞品可以增加 MCP 或静态导出，但要让这些能力在同一底层协同，需要重构产品。
- **设计 token 直接进发布产物**：颜色、排版、间距作为站点数据存储，发布时生成经过 sanitizer 的小型 CSS bundle；这是设计师工作流与最终产物之间少见的桥。

### 竞争风险

最大风险不是某个竞品逐项复制，而是**成熟平台用生态和稳定性让用户不愿承担迁移**：

- **Payload / Directus** 在开发者与数据后台上占优；
- **Builder.io** 在企业视觉平台上占优；
- **WordPress** 仍有无可比拟的插件供给；
- Instatic 还面临 **0.0.x API 变化、单人 bus factor、插件稀缺、访客分析尚未实现、E2E 未进 CI**、Issue #124 所示基础富文本能力仍有缺口；
- 若插件生态与迁移工具增长慢，完整自研栈可能由优势转为维护负担。

### 生态定位

Instatic 最合理的生态位不是替代所有 CMS，而是成为**「自托管、设计师友好、Agent-native、静态输出」的窄而深建站系统**：介于 WordPress / Webflow 的视觉生产体验、Astro 的静态产物质量与现代 Agent 工具协议之间。短期适合代理商、作品集、品牌站、小企业站；复杂应用后端、超大内容组织、强 SLA 场景仍应选成熟平台。

## 套利机会分析

- **信息差**：5102 star / 481 fork / 23 open issues + 25 open PR，体量与能力完整度不匹配——大众热门级别但 issue 闭环率极高，**属于被低估的「大众热门型精品」**。5K star 体量下能做到原子静态发布 + QuickJS-WASM 沙箱 + MCP + 多 AI provider + 三层流水线的产品几乎只此一家。
- **技术借鉴**：
  - 架构测试即治理：~81 个 architecture gates 把「依赖方向、禁用包、schema 边界、UI 规范、生成物新鲜度」做成 CI 规则。对任何高频迭代、多 Agent 协作的仓库都值得抄。
  - 动态边界单 walker：分类 / 渲染 / 诊断共用一个遍历，避免多层规则漂移。
  - 扁平节点图 + 单一 mutation 引擎：让人类 UI、插件、Agent 共享同一 operation union。
  - 过期重证据按语义淘汰：保留最新状态快照，旧快照变 breadcrumb，而不是按 token 截断。
  - 声明权限与实际授权分离：manifest 的 `declaredPermissions` 只服务 consent，执行点只信 `grantedPermissions`。
- **生态位**：填补了「可视化生产力 + 静态可移植性 + 自托管 + AI/MCP 原生」这一交叉象限。`/submit` 这类用户群体（被 Webflow 锁定焦虑 + 熟悉视觉建站 + 想自托管 + 想让 AI 真正改页面）有真实付费意愿。
- **趋势判断**：
  - **符合趋势**：AI Agent 进入大众视野、MCP 协议成熟、自托管回潮、Webflow 锁定焦虑被反复曝光。
  - **有后发优势**：作为 2026 年初发布的新项目，可以从一开始就把 MCP、AI、多 provider、原子静态发布作为一等公民设计，而老牌 headless CMS 需要大量重构。
  - **风险**：0.0.x API 频繁变化 + 单人 bus factor + 插件生态空白。

## 风险与不足

- **API 不稳定**：当前 v0.0.13，全部 1080 commits 发生在近 90 天，core_files 中 `package.json` (67 次)、`src/core/publisher/render.ts` (54 次)、`src/core/page-tree/index.ts` (49 次)、`server/router.ts` (44 次)、`server/db/migrations-sqlite.ts` (40 次)、`bun.lock` (38 次) 都处于高频变更期。Fix 类提交占 44.0%，明显高于 Feature 的 17.5%，说明产品仍在密集修复与稳定化阶段。
- **单点维护**：99.1% 提交来自 DavidBabinec，关键知识与维护能力集中于单人；商业实体运营可能带来可持续性，但作者精力是真实瓶颈。
- **插件生态空白**：examples/plugins 仅 654 次修改且主要是模板示例；浏览器级 E2E 约 156 个串行 case 需 45–60 分钟且**未进 CI**，浏览器回归无法阻断 PR。
- **缺失能力**：访客分析公开路线图中明确尚未实现；CORS / origin 校验在 Issue #185 中暴露部署摩擦；Issue #124 显示「单文本元素内混排粗体/斜体/链接」这一基础富文本能力仍有缺口。
- **数据可信度提示**：stargazer 列表接口在 gh integration 下被限流，star 时间分布未精确采样，但 2.8 月 5K star + 月均 ~1800 star 的爆款量级不存疑。
- **外部独立视角稀缺**：主流 WebSearch 仅命中 CSDN 等自动生成 SEO 内容，**未找到对 Instatic 的独立深度评测**，本报告对其「作者视角」与「设计哲学」的判断高度依赖其官方 README / docs / 架构文档自述。

## 行动建议

### 如果你要用它

适合场景：代理商作品集 / 品牌站 / 内容型小企业站 / 想摆脱 WordPress 又不愿上 Webflow / 想让 AI 真正修改可编辑页面节点 / 已有 Bun + Docker + Railway / 自托管能力的团队。**不适合**：复杂应用后端、超大内容组织、强 SLA / 长期 API 稳定性的企业场景。部署优先选 Railway 一键（README 自带 referral 参数），本地用 SQLite；规模成长后切 Postgres，schema 兼容。

### 如果你要学它

重点关注以下文件 / 模块：

- `src/core/publisher/` —— 三层发布流水线（静态 + 缓存 + server islands）的实现
- `src/core/page-tree/` —— 扁平 `NodeTree` 与 tree-agnostic mutations
- `src/core/db/` —— `DbClient` 抽象与 SQLite/Postgres 双方言
- `src/core/framework/` —— Core Framework 设计 token 数据化与发布期发射
- `server/router.ts` 与 `server/handlers/` —— 手写路由责任链
- `server/plugins/` —— QuickJS-WASM 沙箱 + capability RPC
- `server/ai/` —— 多 provider tool loop + 过期重证据淘汰
- `src/__tests__/architecture/` —— 约 81 个架构 gate 的源码
- `docs/architecture.md` 与 `docs/features/plugin-system.md` —— 权威架构文档

### 如果你要 fork 它

可改进的方向：

1. **插件生态冷启动**：把 `examples/plugins/` 扩成完整 SDK + 模板市场 + 发布审核流；当前仅有 template 与 motion page 一个真实集成。
2. **访客分析**：公开路线图中明确尚未实现，是商业化承载点。
3. **迁移工具**：从 Webflow / WordPress / Builder.io 导入内容、页面树、媒体；当前完全靠手动，是 onboarding 最大摩擦。
4. **多实例 / 集群**：当前单进程 + SQLite 默认；Postgres 路径已有，但多实例 leader lock 与缓存协调尚未完善。
5. **桌面客户端**：Issue #262 已是高频需求，Electron / Tauri 形态与「自托管、便携」哲学天然契合。
6. **CI 补全 E2E**：当前 156 个 Playwright case 因脆弱 / 耗时未进 CI，是质量风险；可分层为 smoke + critical path 进 CI，full suite 留 nightly。
7. **第三方 CRDT / 协作编辑**：当前 patch undo 是单人本地；多人同时编辑同一页面的合并策略尚未涉及。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录 |
| Zread.ai | 未收录 |
| GitHub 官方文档（权威） | https://github.com/corebunch/instatic/tree/main/docs |
| 架构文档 | https://github.com/corebunch/instatic/blob/main/docs/architecture.md |
| 插件系统文档 | https://github.com/corebunch/instatic/blob/main/docs/features/plugin-system.md |
| 关联论文 | 无 |
| 在线 Demo | https://instatic.com（官网即产品演示） |
| 编辑器完整导览视频 | https://www.youtube.com/watch?v=zyjCF_TaLlg |
| Railway 一键部署 | README 自带 |
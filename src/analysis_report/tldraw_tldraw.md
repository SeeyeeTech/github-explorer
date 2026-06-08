# 4.7 万 star 的画布引擎 tldraw：源码全公开，商用为何还收 6000 刀/年

> GitHub: https://github.com/tldraw/tldraw

## 一句话总结

tldraw 是被 Google、Shopify、Autodesk、Replit 等嵌进自家产品的「可嵌入无限画布 SDK」——它把多人协同、持久化、几何、撤销、可访问性这些与产品差异化无关却必须做对的「table-stakes 苦活」打包成 production-ready 引擎，让产品团队「skip the backlog」；更值得研究的是它独占「可嵌入 SDK + source-available 商业许可」象限，用「免费引流 + 水印 + $6000/年商业 license」把开源传播力和闭源收入捆在了一起。

## 值得关注的理由

1. **独特的商业开源样本**：4.7 万 star 却敢不用 MIT——source-available（源码全公开、开发免费），但生产环境强制 license key，否则 SDK 在 production 不工作；Hobby 版常驻「made with tldraw」水印并回传匿名遥测。这套「既要传播、又要收钱」的机关，是和 Excalidraw（MIT 纯开源）的根本分野，也是国内极少有人讲透的话题。
2. **五年打磨、四层自研、生产验证的引擎深度**：自研 signals 响应式库（@tldraw/state）+ 反应式 record store + git-like rebase 协同引擎 + 完整 2D 几何体系，四层互相咬合，复制成本极高；且全程在自家旗舰 tldraw.com 上 dogfooding。
3. **AI canvas 的先发叙事**：2023 年「Make Real」（画草图 → 生成可运行网页）爆火，把无限画布抬升为 LLM 时代的天然交互面；近期发布 cursor 风 AI agent starter kit，押注「画布作为 agent 的空间化读写接口」。

## 项目展示

![tldraw infinite canvas SDK](https://raw.githubusercontent.com/tldraw/tldraw/main/assets/github-hero-light.png)

tldraw 官方 hero 图：可嵌入的无限画布引擎，画布上每个元素都是 React 组件。在线体验见 [tldraw.com](https://tldraw.com)，AI 演示见 [Make Real](https://makereal.tldraw.com)。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/tldraw/tldraw |
| Star / Fork | 47,636 / 3,281（Open Issues 339 / PRs 60）|
| 代码行数 | 463,378 行（TS 45.5% + TSX 20.6% ≈ 66%；JSON 29.5% 多为 API 快照/fixtures，手写源码约 30 万行）|
| 项目年龄 | 61 个月（约 5.1 年，首次提交 2021-05-09）|
| 开发阶段 | 密集开发（近一年 1502 commits，近 30/90 天 89/428，成熟而未衰减）|
| 贡献模式 | 公司全职团队主导 + 社区（创始人 Steve Ruiz 占 39.2%，共 236 人，周末仅 13.9%）|
| 热度定位 | 大众热门（基础设施级，被一线公司大规模采用）|
| License | 自定义 source-available 专有许可（生产需 license key + 水印；starter kits 单独 MIT）|
| 质量评级 | 代码[A] 文档[A] 测试[A-] CI[A] API 契约[A] 类型安全[A]|

## 作者视角：为什么存在这个项目

### 创始人/作者背景

tldraw 是伦敦的商业公司（约 15 人，2025-04 完成 1000 万美元 A 轮，累计融资 1200 万）。创始人兼 CEO Steve Ruiz 走的是一条清晰的「向下钻」路径：先做创意工具的算法原语（perfect-freehand 压感笔迹、perfect-arrows 箭头几何），再做白板应用（tldraw.com），最终把应用里反复打磨的引擎抽成 SDK。核心全职团队 + A 轮资金 + 知名创始人 + 一线公司采用，可信度与可持续性远高于个人项目。

### 问题判断

infinite canvas 应用的底层基建极难自建：高性能渲染与命中检测、几何/对齐/吸附、撤销重做、多人实时协同（冲突解决、presence、持久化）、序列化与跨版本迁移、可访问性、跨设备输入——这些都与产品差异化无关却必须做对。现有方案都不够：Fabric.js/Konva 只是 Canvas 2D 图形库（解 5% 的问题）；Excalidraw 是开箱即用的白板**应用**而非可深度定制的**引擎**；自己造则每一项都是数月到数年工程。「为什么是现在」：2023 年 Make Real 的爆火证明画布是 LLM 时代的天然交互面，把「可嵌入画布引擎」从设计工具品类抬升为 AI 应用基建品类。

### 解法哲学

- **headless engine + batteries 双层**：`packages/editor` 是无 UI、无默认形状的纯引擎；`packages/tldraw` 在其上叠一整套默认 shapes/tools/UI。可只用引擎从零搭，也可用全家桶改 20%。
- **画布上每个元素都是 React 组件**：`ShapeUtil.component(shape)` 返回 JSX、渲染走 DOM 而非 Canvas 2D，于是「浏览器能渲染的（YouTube/Figma/iframe）画布就能放」，扩展用的是 web 开发者已有的技能。
- **enabling rather than constraining**：暴露底层 Editor API 与 side-effects/hooks，而非用配置项把用户框死。
- **明确不做什么**：不做闭源 SaaS（要可自托管、可嵌入）；不追求 Figma 级终端体验天花板（错位竞争）；引擎层不绑定默认 UI。

### 战略意图

**open-core / watermark 模式**：Hobby 免费但常驻水印且回传匿名数据（天然获客漏斗 + 品牌曝光），Commercial 去水印按席位收费（10 人以下 $6000/年）——把开源社区的传播力和商业闭源的收入捆在一起。**AI canvas 押注**：Make Real → tldraw.computer → `templates/agent`（cursor 风 AI agent starter，默认推荐 Anthropic）。**与 Figma 错位**：Figma 是不可嵌入的终端产品，tldraw 是给开发者的「Figma 级画布引擎」，卖 Figma 卖不了的东西——可嵌入、可自托管、可定制。

## 核心价值提炼

### 创新之处

1. **epoch + diff 的拉取式 signals（@tldraw/state）**（新颖度 4/5・实用性 5/5・可迁移性 5/5）：全局逻辑时钟驱动的惰性响应式系统，Atom 持值并维护 HistoryBuffer、Computed 惰性求值比对 epoch；关键是信号不仅给「新值」还给「从旧值到新值的 diff」（computeDiff/withDiff），把**响应式、撤销重做、协同同步统一成「signal diff」一种货币**。框架无关，可独立复用。
2. **ShapeUtil 数据-行为分离插件模型**（新颖度 4/5・实用性 5/5・可迁移性 5/5）：shape 是可序列化的纯 record（存 store），所有行为外置到注册式 `ShapeUtil<Shape>` 抽象类（getGeometry / component / getHandles / toSvg…）；注册即扩展（`<Tldraw shapeUtils={[...]}/>`）。这是「20% 开箱 + 80% 可定制」叙事的工程落点，BindingUtil 是同一模式在「关系」上的复刻。
3. **git-like rebase 协同引擎（sync-core）**（新颖度 4/5・实用性 4/5・可迁移性 3/5）：本地改动乐观立即应用并入 speculativeChanges，收到服务端 patch 时 rebase（撤销本地未确认→应用服务端→重放本地）；服务端维护权威 logical clock + tombstones + presence，握手校验协议版本。作为 CRDT 之外的工程化替代——避免 CRDT 内存膨胀与语义模糊，保留服务端权威与可校验性。已落地 Cloudflare Durable Object SQLite，可自托管。
4. **离线 ECDSA license 强制 + 水印遥测**（新颖度 3/5・实用性 3/5・可迁移性 3/5）：LicenseManager 内嵌硬编码 ECDSA 公钥，license key 用 crypto.subtle 离线验签（无需联网），解析位掩码 flags + 域名白名单 + 过期日推导 LicenseState；无有效 license 的生产部署渲染水印并回传匿名遥测。这是 source-available 模式「既要传播、又要收钱」的核心机关。

### 可复用的模式与技巧

1. **Util/Registry 插件模式**：把「类型的行为」从「类型的数据」剥离成可注册 Util 类（ShapeUtil/BindingUtil/AssetUtil 同构）—— 适用于可扩展元素/关系/资源类型的系统。
2. **Signal + diff 统一数据流**：用一种「带 diff 的响应式信号」同时驱动 UI 重算、undo/redo、网络同步 —— 状态密集 + 需协同/时间旅行的应用。
3. **反应式索引查询**：对实体存储建可订阅、增量更新的二级索引（`store.query.index()`）—— 本地优先数据层。
4. **层级状态机分发输入事件（StateNode）**：事件沿激活状态路径分发，状态本身是 signal —— 富交互编辑器/游戏输入。
5. **API snapshot in CI**：把公共 API 表面快照（api-report.api.md）入库 + CI diff 守护（@microsoft/api-extractor）—— 任何对外库/SDK 都该抄。
6. **几何原语先行**：先建一套带测试与 bench 的 2D 几何库，再让命中/吸附/对齐/导出复用之 —— 图形/CAD/可视化引擎。

### 关键设计决策

- **自研 signals 而非 MobX/Redux/Zustand**：60fps 画布上任意拖动只应触发受影响 shape 重算，需极细粒度依赖追踪 + 可计算 diff 的历史。Trade-off：团队长期维护一套响应式内核，换来对 epoch/diff/HistoryBuffer 的完全控制——这是把撤销和协同统一建模为 signal diff 的前提，现成库做不到。
- **万物皆 record 的响应式 store**：每个 shape/page/camera/selection 都是可订阅、可 diff、可序列化、可迁移的 record，RecordsDiff 是撤销和同步共用的「diff 货币」。一切走 record + signal 带来开销，换来 reactivity/undo/sync/migration 四件大事共用一套数据流。
- **工具系统是层级状态机（HSM）**：画布交互充满模态状态，用布尔标志会失控；StateNode 让每个工具是 root→branch→leaf 状态树，事件沿激活路径分发。
- **API Extractor 守护 SDK 契约**：每包 api-report.api.md 入库 + CI api-check 比对快照，API 变动必须显式更新快照才能合并——这解释了「api-report 频繁变动」。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | tldraw | Excalidraw | React Flow (xyflow) | Fabric.js / Konva |
|------|--------|------------|---------------------|-------------------|
| Stars | 47.6k | 124.8k | ~2.9k | ~2.9k / ~1.2k |
| 形态 | 可嵌入画布**引擎/SDK** | 开箱即用白板**应用** | node 图/流程图库 | Canvas 2D 渲染库 |
| 许可 | source-available（商用收费）| MIT 纯开源 | MIT | MIT |
| 可定制 | 极强（ShapeUtil 组件化）| 弱（非组件化）| 中（专注 node）| 低（仅渲染）|
| 协同 | 自研可自托管 sync | 有（应用层）| 无内置 | 无 |
| 解决问题 | 95%（完整引擎）| 应用级 | node-graph 子集 | 5%（渲染）|

### 差异化护城河

① 五年打磨、生产验证的引擎深度——signals/store/sync/geometry 四层自研且互相咬合，复制成本极高；② 「headless + batteries + 每个 shape 是 React 组件」的扩展心智已成开发者认知资产；③ 商业公司全职团队 + A 轮资金保障的持续投入与企业级支持承诺，纯社区项目给不了；④ AI canvas 先发叙事（Make Real / agent kit）。

### 竞争风险

① **source-available 许可是双刃剑**——SDK 4.0 强制 license key + 涨价已引发社区反弹，把价格敏感/偏好纯开源的用户推向 Excalidraw，削弱「免费传播」飞轮；② 客户端 license 校验技术上可被 patch，依赖法律威慑；③ 水印回传遥测引发隐私顾虑；④ 与 Excalidraw 的生态规模差距（star 2.6 倍、社区长尾）短期难追平；⑤ AI canvas 是新战场，Figma/Canva/各 AI 公司可能正面进入。

### 生态定位

稳坐「可嵌入、可自托管、可深度定制的 production-grade 画布引擎」独占生态位——上方是不可嵌入的 Figma/FigJam（错位），平行是纯开源但弱定制的 Excalidraw（许可与定制度分野），下方是只解决渲染的 Fabric/Konva（层级分野）。赌的是「企业愿意为省下数年自建成本付费」。

## 套利机会分析

- **信息差**：人人听过、多数人没读过源码。中文社区对其**商业许可模式（watermark + $6000/年）**和**画布引擎架构**的深度解读稀缺——选题应避开「又一个画板」，主打「开源 SDK 怎么靠 license 赚钱 + canvas 引擎怎么做」。
- **技术借鉴**：epoch+diff signals、ShapeUtil 插件模型、反应式索引 store、HSM 工具系统、API snapshot in CI、离线签名 license——这些范式可直接迁移到状态密集型前端、可扩展编辑器、商业 SDK。
- **生态位**：填补「可嵌入 + 可自托管 + 可深度定制的 production 画布引擎」空白，Figma 不可嵌入、Excalidraw 弱定制、Fabric/Konva 只管渲染。
- **趋势判断**：强正向——密集开发未衰减、刚完成 A 轮、押中 AI canvas；后发优势在「企业可依赖性」与 AI 叙事的先发。

## 风险与不足

- **许可争议与定价门槛**：source-available 非 OSI 开源，10 人以下 $6000/年，SDK 4.0 收紧曾引发社区争议；价格敏感用户会转向 Excalidraw。
- **客户端校验可被绕过**：license 校验在客户端、源码公开，技术上可 patch，依赖 LICENSE 法律条款兜底。
- **遥测隐私顾虑**：Hobby 版水印回传匿名使用数据。
- **强绑自有栈**：sync 引擎与 tldraw record/store 强耦合，不易单独抽离；协同自托管需 Cloudflare Durable Object 同栈或自行适配。
- **monorepo 重**：1.39 GB 仓库、17 包、自研构建编排（lazyrepo），上手与贡献门槛偏高。

## 行动建议

- **如果你要用它**：要在产品里嵌入可深度定制的画布/白板/节点编辑器且能接受商业许可 → 选 tldraw（`npm create tldraw`）；只要免费纯开源白板应用 → Excalidraw；只做流程图 → React Flow；只要 canvas 上画对象 → Fabric/Konva。注意生产环境需 license key。
- **如果你要学它**：重点读 `packages/state`（自研 signals：atom/computed/transaction/withDiff）、`packages/store`（响应式 record store + 反应式索引）、`packages/editor/src/lib/editor/Editor.ts`（命令中枢）+ `shapes/ShapeUtil.ts` + `tools/StateNode.ts`、`packages/sync-core/src/lib/TLSyncClient.ts`（git-like rebase）、`packages/editor/src/lib/license/`（离线签名 license）。
- **如果你要 fork 它**：@tldraw/state、ShapeUtil 插件模型、反应式索引 store、HSM 工具系统、API snapshot CI 都是可独立抽取的工程资产，可移植进你自己的编辑器/SDK；注意整体许可约束。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [deepwiki.com/tldraw/tldraw](https://deepwiki.com/tldraw/tldraw)（已收录，9 大板块含协同/AI 集成架构索引，架构解读高质量参考）|
| Zread.ai | 无法确认（探测 403）|
| 官方文档 | [tldraw.dev](https://tldraw.dev)（含 license/pricing）；博客 tldraw.substack.com |
| 在线 Demo | [tldraw.com](https://tldraw.com) · [Make Real](https://makereal.tldraw.com) · tldraw.computer |
| 创始人访谈 | [The Accidental AI Canvas — Latent Space](https://www.latent.space/p/tldraw) |

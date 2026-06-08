# 一个人做的开源 Maltego，47 个 OSINT 插件

> GitHub: https://github.com/reconurge/flowsint

## 一句话总结

flowsint 是一个开源、自托管、本地优先的「基于图的可视化 OSINT 调查平台」——把零散易过时的侦察脚本收编成「即插即拔的富集插件」，让调查的实体关系始终以一张持久的图谱留存；它由单一开发者用 16 个月做成，是「现代 Web 版的开源 Maltego」。

## 值得关注的理由

- **精准卡位的蓝海**：「开源 + 自托管 + 现代 Web 图谱 UI + 可插拔 enrichers + Neo4j 原生」这一组合此前几乎空白——Maltego 闭源贵且是桌面端、SpiderFoot 可视化弱、theHarvester/recon-ng 是不可视化的 CLI。flowsint 补的正是「开源 Web 版 Maltego」这个缝隙。
- **可扩展性真正落地**：47 个内置富集器（asn/domain/email/ip/phone/social/crypto…）用「装饰器自动注册 + 强类型 In/Out」实现，加一个新 OSINT 数据源 ≈ 新建一个子类 + 一个 `@flowsint_enricher` 装饰器，零侵入；外部 OSINT CLI（subfinder/sherlock/maigret/dehashed…）还通过 docker SDK 沙箱化调用。
- **负责任的 OSINT 范本**：项目自带 `ETHICS.md`（以 Hippocratic License「不得侵犯基本人权」为底线）+ `DISCLAIMER.md`，明确许可用途（威胁情报/记者调查/执法反欺诈）与禁止滥用（未授权监控、人肉 doxxing、骚扰）。加上 local-first（数据只存在你自己机器）的隐私设计，是双用途工具里少见的自觉。

## 项目展示

![图谱调查界面（节点-边可视化画布 sketch）](https://github.com/user-attachments/assets/01eb128e-bef4-486e-9276-c4da58f829ae)

暗色主题的图谱调查界面——一次调查就是一张「sketch」画布，实体是节点、关系是边。

- [产品演示视频 1：图谱调查工作流](https://github.com/user-attachments/assets/eaabfa81-d7b3-414d-8cf7-f69b4e37bab6)
- [产品演示视频 2：enricher 富集 / 节点展开](https://github.com/user-attachments/assets/7457d94a-cf1d-4a97-949f-f9b1d8d92644)

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/reconurge/flowsint |
| Star / Fork | 5884 / 715（fork 比例偏高，印证大量自托管 + 二开） |
| 代码行数 | 75K（TSX 43.7% 前端图谱 UI + Python 40% 后端/插件 + TS 11.7%） |
| 项目年龄 | 16.2 个月（2025-01 起） |
| 开发阶段 | 密集开发（近 30 天 45 commit，仍高速，未降温） |
| 贡献模式 | 单人主导（dextmorgn 占 96.3%，巴士因子=1） |
| 热度定位 | 大众热门 + 蓝海卡位（刚一夜涨 184 star 上 Trending，爆发型） |
| 质量评级 | 代码[良好·monorepo 分层清晰] 文档[中·有 docs 但偏薄] 测试[有·core/types 带测试 + CI Python tests] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

org 是 `reconurge`（recon + urge），主作者 `dextmorgn` 一人完成 96.3% 的提交。该 org 旗下 6 个仓库全是 recon* 系列 OSINT/侦察小工具（reconcrawl、recontrack、rangebuster…，多为 6~17 star 的 Python 项目）——flowsint 是这位作者长期深耕侦察赛道后的突破之作。无公开 bio/公司，靠 Buy Me A Coffee / Ko-fi / Discord 的「爱好驱动 + 社区捐赠」模式独立运营，是典型的 indie hacker 安全方向开发者。

### 问题判断

OSINT 的现实痛点是：工具极度碎片化（几十个 CLI、各种数据源 API），每个工具的输出是孤立的、易过时的，调查者要在脑子里/便签里手动拼接实体关系，调查上下文极易丢失。作者看到的是：**应该有一个持久的「图核心」来沉淀关系，把外部工具降格为围绕这张图的「可插拔扩展」**。这样调查上下文不丢、工具可随时增减、数据集中打破孤岛。时机上，Maltego 长期闭源、贵、桌面端，给了开源 Web 替代一个明确的空位。

### 解法哲学

- **明确选择「持久图核心 + 即插即用工具」**：用 Neo4j 属性图建模调查（节点=实体、边=关系），enrichers 是围绕图的扩展，而非各自为政的脚本。
- **明确选择 local-first / 隐私优先**：「只在你自己机器上运行，数据全本地，无采集、无追踪」——这既是隐私立场，也与 OSINT 的合规敏感性契合。
- **明确选择负责任**：主动写 ETHICS.md + DISCLAIMER.md，划定许可/禁止边界，提供滥用举报渠道。
- **明确从 AGPL 重授权为 Apache-2.0**（2026-01，征得全体贡献者同意）——主动降低企业采用门槛。

### 战略意图

目前纯靠捐赠维持，无公司/SaaS 实体。但社区强烈呼吁「Non-Local/托管/多用户版」（issue #16 高热），且 v2 路线图（issue #133 RFC「Graph Conductor」）瞄准「多 Agent 并发修改图谱」的并发协调——指向「AI Agent + 人协同调查」的下一代形态。flowsint.io 目前是营销+文档站，未来是否变 SaaS 入口、能否在不背离 local-first 立身之本的前提下商业化，是它最大的战略岔路口。

## 核心价值提炼

### 创新之处

1. **「持久图核心 + 可插拔 enrichers」的调查范式**（最值得学）：把 OSINT 从「跑一堆孤立脚本」变成「围绕一张持久图谱做富集」，调查上下文（节点关系）始终留存。这是对 Maltego「实体-Transform」模型的现代 Web 化重构。
2. **装饰器自动注册的插件架构**：每个富集器是 `Enricher` 子类，声明 `InputType`/`OutputType`（取自共享的强类型图节点），实现 `async scan()`，顶上挂 `@flowsint_enricher` 即注册进 `ENRICHER_REGISTRY`；启动时遍历包自动发现，注册表还自动生成 in/out schema、params、icon 供前端表单渲染。**加数据源零侵入**——这是「extensible」卖点的硬落地。
3. **强类型图节点作为前后端契约**：`flowsint-types` 定义 Username/Email/SocialAccount/IP 等节点类型，既是富集器的 In/Out 契约，又被前端复用——一套类型贯穿全栈。
4. **外部 OSINT CLI 的沙箱化集成**：subfinder/sherlock/maigret/dehashed 等通过 docker SDK 隔离运行，把生态里成熟的 CLI 工具收编为 enricher。

### 可复用的模式与技巧

1. **装饰器 + 全局注册表 + 自动发现**：插件式扩展的经典且优雅的实现，适用于任何「想让第三方零侵入加扩展」的系统。
2. **强类型 In/Out 契约驱动 UI 自动生成**：注册表自动产出 schema → 前端自动渲染表单，省掉大量手写 UI。
3. **持久图谱 + 外部工具降格为扩展**：把易变的外部能力围绕一个稳定核心组织，是对抗「工具碎片化」的通用架构思路。
4. **图谱渲染选型**：`react-force-graph-2d`（Canvas 力导向）为主、超大图回退 `pixi.js`（WebGL）——大规模图可视化的实用组合。

### 关键设计决策

- **Neo4j 属性图作为调查的单一事实源**：节点-边天然契合「实体-关系」调查模型，Cypher 查询表达关系路径远胜关系库 JOIN；代价是引入 Neo4j 这一重组件，抬高了自托管门槛（见风险）。
- **monorepo 五包关注点分离**：app（前端）/ core（领域逻辑 + enricher 基类）/ api（FastAPI HTTP 层）/ enrichers（数据源）/ types（共享契约）。改动量 app(481) > core(178) > api(76) 印证「价值在前端图谱交互 + 核心富集逻辑」。
- **工程纪律相对规范**：Conventional Commits（commitlint）+ SemVer（standard-version 自动发版）+ CI + 双库迁移（Neo4j Cypher + 后端 alembic）+ core/types 测试目录——单人项目里少见的工程化自觉。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | flowsint | Maltego | SpiderFoot | theHarvester/recon-ng |
|------|----------|---------|------------|------------------------|
| 开源 | ✓ Apache-2.0 | ✗ 闭源 | ✓（HX 商业版） | ✓ |
| 形态 | 自托管 Web | 桌面端 | Web/CLI | CLI |
| 可视化图谱 | ✓ 现代力导向图 | ✓ 链接分析（标杆） | 弱 | ✗ |
| 扩展机制 | 47 enrichers + docker CLI | Transform Hub（数百源） | 200+ 模块 | 脚本 |
| 价格 | 免费 | Pro/企业 $1000+/年 | 部分免费 | 免费 |
| 定位 | 交互式图谱调查 | 事实标准 | 自动化全量扫描 | 底层采集 |

### 差异化护城河

护城河 =「**开源 + 自托管 + 现代 Web 图谱 UI + 可插拔 enrichers + Neo4j 原生 + local-first 隐私**」这一精确组合，目前基本无直接对手。加上 47 个现成富集器 + 沙箱化收编主流 OSINT CLI 形成的生态积累，以及自带伦理框架带来的「负责任工具」口碑。但护城河更多来自「组合空位」而非单点技术壁垒。

### 竞争风险

- **巴士因子=1（最大风险）**：5.9k star 的热门项目实为单人主导，可持续性高度依赖该作者。
- **Maltego/SpiderFoot 下沉**：若 Maltego 推出更友好的开源/Web 版，或 SpiderFoot 强化可视化，缝隙会被压缩。
- **早期安全债**：已有越权读取他人 sketch 日志的安全公告（GHSA Broken Access Control），提示「暴露到网络/多用户」场景尚不成熟——而这恰是社区最想要的方向。
- **自托管门槛**：Docker + Neo4j + Postgres + Redis + API 多组件，对普通调查者上手不友好（最热 issue 集中在部署摩擦）。

### 生态定位

它是「开源自托管现代图谱 OSINT」这一蓝海细分的领跑者，把碎片化的 OSINT CLI 生态收编为围绕持久图谱的扩展，填补了 Maltego 与 CLI 工具之间的空白。

## 套利机会分析

- **信息差**：不算被长期低估，而是「厚积后刚被看见」（16 个月密集开发后一夜上 Trending）。内容价值在于它是「负责任的开源 Maltego」深度解读样本，以及插件架构/图谱调查范式的工程借鉴。
- **技术借鉴**：「装饰器自动注册插件」「强类型契约驱动 UI 自动生成」「持久图核心 + 外部工具降格为扩展」三套模式可迁移到任何插件化/数据集成系统。
- **生态位**：想要自托管、可扩展、可视化 OSINT 调查又不想买 Maltego 的安全团队/调查记者，这是当前最佳开源选择。
- **趋势判断**：OSINT + 图谱 + AI Agent 协同（v2 Graph Conductor）是明确上升方向；flowsint 卡位早、势头猛，但能否把一次性 Trending 流量沉淀为持续贡献者与商业化是关键。

## 风险与不足

- **⚠️ 双用途与合规风险（必须正视）**：OSINT 调查工具本质双用途——合法用途（威胁情报、反欺诈、数字取证、记者/企业调查、安全研究）vs 滥用（人肉 doxxing、跟踪骚扰、侵犯隐私）。各 enricher 调用第三方数据源须遵守其 **ToS**；对自然人画像受 **GDPR / 各地个人信息保护法**约束；OSINT 合法性各司法辖区差异大。项目自带 ETHICS.md/DISCLAIMER.md + local-first 设计是加分项，但「Non-Local/多用户」一旦落地会显著放大合规与越权风险（参见已有越权安全公告）。本报告不提供任何定向追踪/人肉的操作指引。
- **巴士因子=1**：高度依赖单一作者。
- **自托管门槛高 + 早期安全债**：多组件部署摩擦 + 已知越权漏洞，生产/多用户部署需谨慎。
- **文档/重构暂让位于功能扩张**：注释率 7.9%、docs/refactor commit 极少，处于「跑得快」的早期阶段。

## 行动建议

- **如果你要用它**：你是需要**自托管、可视化、可扩展 OSINT 调查**的安全分析师/调查记者/反欺诈团队，且接受自托管门槛与早期成熟度——它是当前最佳开源 Maltego 替代。务必在授权范围内、合规前提下使用，多用户/联网部署前先评估越权风险。要企业级成熟度与最广数据源，仍是 Maltego；要纯自动化全量扫描，看 SpiderFoot。
- **如果你要学它**：重点读 `flowsint-core`（`enricher_base.py` + `@flowsint_enricher` 注册机制）、`flowsint-enrichers/src`（47 个富集器范式 + docker 沙箱化 CLI）、`flowsint-types`（强类型图节点契约）、`flowsint-app/src/components/sketches`（force-graph 图谱 UI + zustand store）。这是「插件化数据集成 + 图谱可视化」的优秀全栈样本。
- **如果你要 fork 它**：最有价值的方向是**补齐多用户/联网部署的权限与安全模型**（修复越权、做好租户隔离）、简化自托管（减少组件或提供托管版），以及贡献新的 enricher（架构对此零侵入）。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/reconurge/flowsint （已收录，含系统架构/模块/技术栈/部署详解） |
| Zread.ai | 未确认（探测 403） |
| 关联论文 | 无（工程工具） |
| 在线 Demo | 无（local-first，仅自托管）；官网 https://flowsint.io 为营销+文档站，快速上手 https://flowsint.io/docs |
| 伦理与免责 | 仓库内 `ETHICS.md`（Hippocratic License）+ `DISCLAIMER.md`；滥用举报 contact@flowsint.io |

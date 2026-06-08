# 一切皆插件：中国团队不融资 6 年，做出 2.2 万 Star 的低代码平台 NocoBase

> 一句话总结：NocoBase 是一个「一切皆插件」的开源 AI + 无代码/低代码平台——27 个核心包做微内核、106 个官方插件做功能，数据模型驱动 UI、可连已有数据库、支持私有部署，背后是新加坡注册的中国团队不融资自力更生 6 年打磨的 90 万行 TypeScript 工程。

---

## 值得关注的理由

- **「一切皆插件」的微内核架构是教科书级范本**。内核 `Application` 本身只是 Koa + 一组 Manager 的编排器，连 ACL、认证、工作流、数据导入导出、AI 都是插件（106 个官方插件）。这套「内核稳定、功能靠插件无限生长」的设计，是任何想做平台型产品的团队值得逐行研读的参考。
- **数据模型驱动，而非界面驱动**。Retool/Appsmith 是「先拖界面、数据临时拼」;NocoBase 反过来——先定义数据结构（`Collection`），UI 只是数据模型的一种投影，数据与界面解耦。它甚至能反射连接你已有的数据库当数据模型用，不要求数据迁移。
- **AI Employee 受同一套字段级权限约束**。这是最前瞻的设计：AI 不是旁路，而是有自己的 role、受字段级 ACL 约束、工具调用默认需人工确认（`defaultPermission: 'ASK'`）、全程审计——「让 AI 进业务系统干活又不越权」给出了可落地的答案。
- **罕见的商业样本：中国团队出海、不融资、买断制**。NocoBase PTE LTD（新加坡）由中国团队创办，开工即按「6 年零收入」备足资金、坚持不融资，采用 lifetime 买断而非订阅。2026-02 的 v2.0 完成了「AI 转向 + 核心许可从 AGPL 转 Apache + 部分商业插件开源」的战略调整——一个 open-core 可持续性的真实案例。

---

## 项目展示

README 自带 1 段产品演示视频 + 核心 WYSIWYG GIF + 多张功能截图：

![所见即所得无代码配置](https://static-docs.nocobase.com/wysiwyg.gif)
![AI coding agent 协作](https://static-docs.nocobase.com/coding-agent.png)
![插件微内核架构](https://static-docs.nocobase.com/plugins.png)

> 在线 Demo 可直接体验：<https://demo.nocobase.com/new>;社交卡片兜底：`https://opengraph.githubassets.com/1/nocobase/nocobase`

---

## 项目画像

| 维度 | 数据 |
|---|---|
| 全名 | `nocobase/nocobase` |
| 定位 | 开源 AI + 无代码/低代码平台（数据模型驱动 · self-hosted） |
| Star / Fork | 22,675 ⭐ / 2,652 🍴（CSV 抓取时 19,030，窗口内 +3,600，高速增长） |
| License | Apache-2.0（v2.0.3 起从 AGPL-3.0 切换）+ NocoBase 商业许可（三档买断） |
| 主语言 | TypeScript（monorepo，TS 49.6% + TSX 30.5%） |
| 代码规模 | 110 万行 = 真实手写 TS/TSX **90.8 万行** + i18n locale 21.6 万行;17,276 文件;注释比 0.352 |
| 建库时间 | 2020-10（5.6 年长青项目，今日活跃，二次加速） |
| 开发节奏 | 14,785 commit;近 365 天 4,227、近 90 天 482、近 30 天 150 |
| 版本 | 1,005 个 tag，最新 v2.1.0-beta.45（v2.0 于 2026-02 发布） |
| 贡献者 | 121 人，创始人 chenos 主导（25.3% commit）+ 核心团队 + 社区 |
| 公司主体 | NocoBase PTE LTD（新加坡，中国团队出海，不融资） |
| 架构 | 27 core 微内核 + 106 官方插件 + presets;一切皆插件 |
| 演进前线 | flow-engine（新引擎，近年 426 commit）+ client-v2 重构 + ai 集成 |

---

## 作者视角

### 问题发现

创始人 **chenos**（约 25.3% commit，绝对主导）面对的是「定制业务系统」这个老问题：传统低代码平台要么把你锁死在功能边界里，要么生成一堆改不动的代码。他的判断是——**业务系统的难点不在 UI，而在数据模型、权限、工作流、审计这些「复杂且对错误敏感」的基础设施**。所以平台真正该提供的是这层可靠底座，而不是又一个拖拽 UI 工具。

### 解法哲学

1. **一切皆插件的微内核**：内核 `Application`（`packages/core/server/src/application.ts`）只是 Koa + 一组 Manager 的编排器，连 ACL、认证、工作流、AI 都是插件。「系统能在不失控的前提下生长」。
2. **数据模型驱动**：先有 `Collection`（数据结构），UI 只是数据模型的投影，数据与界面解耦。
3. **AI 在可靠底座之上、受同一套权限约束**：AI Employee 有自己的 role、受字段级 ACL + 审计日志约束——「让内外部 agent 都待在同一套边界内」。

### 背景知识迁移

作者把成熟生态做了二次抽象：`Database` 是对 **Sequelize** 的封装与再抽象（dialect 可插拔，支持 sqlite/postgres/mysql）;客户端 schema 驱动 UI 直接建立在 **@formily** 之上（`SchemaComponent.tsx` 仅 125 行，是 formily 的薄封装）;`PluginManager` 用 `@hapi/topo` 按 `peerDependencies` 做插件加载拓扑排序;`Resourcer` 把 REST 抽象成 `{resource}:{action}`，中间件用 toposort 编排。

### 战略图景

- **open-core 买断制**：core 27 包 + 部分插件开源，高级能力（如 MCP server）走 Standard/Professional/Enterprise 三档 lifetime license（买断非订阅）。
- **AI 转向**：v2.x 把「AI + no-code」提到首位，新增 `core/ai` + `plugin-ai`，把 CLI/Skills 作为 agent 接入口。
- **出海**：新加坡注册、8 语言 README、不融资自力更生（2023-05~2024-04 营收约 226 万元人民币）。

---

## 核心价值提炼

### 创新点

**1. 字段类型 / 字段接口两层分离（field-type vs field-interface）** — 新颖度 4/5 · 实用性 5/5 · 可迁移性 5/5

存储语义（`fields/`，对应 DB 列类型如 `string-field`/`belongs-to-field`/`json-field`）与业务-UI 语义（`interfaces/`，对应表单组件/校验/选项如 `select-interface`/`percent-interface`/`datetime-interface`）**解耦**——同一个存储字段可被不同 interface 包装出不同 UI 语义。适用：任何需要「同一存储多种业务呈现」的低代码/表单/CMS 平台。

**2. AI Employee 与人类共用一套字段级 ACL + 工具默认 ASK 权限** — 新颖度 5/5 · 实用性 5/5 · 可迁移性 4/5

AI 不是旁路，而是有 role、受 `grantAction({fields})` 字段级约束、工具调用 `defaultPermission: 'ASK'` 需人工确认、全程审计。`plugin-ai` 的 `setPermissions()` 把 AI 能力完全纳入同一 ACL。适用：要在企业系统内引入 agent 又怕越权的场景。

**3. 一切皆插件的微内核 + 拓扑加载 + 运行时动态装卸** — 新颖度 3/5 · 实用性 5/5 · 可迁移性 5/5

连 ACL/auth/workflow/AI 都是插件，`@hapi/topo` 按 peerDependencies 排序，支持 `addByNpm/addByFile/addByCompressedFileUrl/addViaCLI` 多渠道运行时安装。适用：需长期演进、第三方生态的平台型产品。

**4. 多数据源统一为数据模型（introspector 反射外部库 + per-source ACL/resourcer）** — 新颖度 4/5 · 实用性 5/5 · 可迁移性 4/5

主库、外部库、SQL/FDW、API 都抽象成 `Collection`，每个 data source 自带独立的 `database + acl + resourceManager`，`DatabaseIntrospector` 反射已有表结构。适用：要在「不迁移已有数据」前提下做统一管理界面的企业集成场景。

**5. flow-engine 响应式模型 + 流程注册表 + JS 沙箱** — 新颖度 4/5 · 实用性 4/5 · 可迁移性 3/5

v2 主线（近一年 426 commit），从「纯 JSON UISchema 渲染」升级为类化的 `FlowModel`（支持模型继承 `extendModelClass`、`forkFlowModel`、响应式代理、`JSRunner` 带 `safeGlobals` 的 JS 沙箱、`applyFlow` 缓存）。适用：需要强可编程、利于 AI 编排的低代码运行时。

### 可复用模式

1. **抽象 Plugin 生命周期 + 两趟加载**：先全量 `beforeLoad` 再逐个 `load`，配依赖拓扑排序 — 任何插件化系统的「先声明后使用」。
2. **Manager 编排式内核**：内核只持有并装配一组职责单一的 Manager（PluginManager/ACL/Resourcer/DataSourceManager…）— 复杂应用的关注点分离。
3. **资源-动作 + 中间件拓扑 API 抽象**：`{resource}:{action}` 统一描述 + toposort 中间件 — 可扩展 API 网关。
4. **存储字段 / 业务字段两层模型**：DB 类型与 UI/业务语义解耦 — 表单/低代码/CMS。
5. **AI 工具 `defaultPermission:'ASK'` + 纳入 ACL**：agent 能力受 RBAC + 人工确认双约束 — 落地企业 agent。
6. **DataSource 抽象 + introspector**：外部库反射成统一数据模型 — 多数据源管理平台。

### 关键设计决策

- **微内核 Application + Plugin 生命周期**：`Application extends Koa`，`init()` 组装 PluginManager/DataSourceManager/AuthManager/AIManager/ResourceManager 等;`PluginManager.load()` 分两趟（先全量 `beforeLoad()`、再逐个 `loadCollections()→loadAI()→load()`），保证「先声明后使用」。Trade-off：极致可扩展，但内核与插件、插件间的隐式耦合（事件 + 拓扑）增加心智负担，冷启动需按拓扑串行加载上百插件。
- **数据模型驱动 Collection/Database**：`Collection` 动态生成 Sequelize model，支持 `inherits` 多表继承;`Database` dialect 可插拔。Trade-off：「DB 列 ↔ 业务字段 ↔ UI 组件」清晰，但 field-type 与 field-interface 的区别让学习曲线陡。
- **schema 驱动 UI**：UI 即数据（JSON UISchema），配置态拖拽产出 schema、运行态由 formily 渲染，`schema-initializer`（加区块/字段）+ `schema-settings`（改配置）是设计器三件套。Trade-off：schema 可序列化/可 AI 生成/可版本化，但深度依赖 formily，调试 x-component 链路困难。

---

## 竞品格局

| 竞品 | 类别 | 优势 | 劣势 |
|---|---|---|---|
| **nocobase（本项目）** | 数据模型驱动 + 微内核 | 插件极致可扩展、数据模型驱动、self-hosted 数据自控、AI Employee 受权限约束、买断制 | 学习曲线陡、v2 重构期双轨、open-core 收费边界、多数据源类型兼容边缘问题 |
| **Airtable** | 数据库型（闭源 SaaS） | 体验成熟、生态大、零门槛 | 闭源、不可自托管、按席位涨价昂贵 |
| **NocoDB**（63K star） | 数据库型（开源） | star 最高、连存量库强、自托管省钱 | 偏数据表视图层，工作流/权限/插件扩展弱 |
| **Baserow / Teable** | 数据库型（开源） | 纯开源、实时协作、现代体验 | 偏轻量表格，复杂业务系统能力弱 |
| **Retool** | admin builder（闭源） | 组件丰富、企业采用广 | 闭源、订阅贵、界面优先而非数据模型优先 |
| **Appsmith / Budibase / ToolJet** | admin builder（开源） | 开源、自托管、多数据源 | 界面优先，数据建模/工作流不如 NocoBase 体系化 |
| **n8n / Dify / Strapi / Directus** | 邻接（工作流/AI/CMS） | 各自垂直能力强 | 非完整业务系统底座（NocoBase 可通过 API/CLI/Skills 对接它们） |

**关键差异化轴**：① **插件微内核（一切皆插件，27 核心包 + 106 插件）** vs 封闭/有限扩展;② **数据模型驱动（先建数据结构、可连存量库）** vs 表单/界面驱动;③ **self-hosted 数据自控** vs SaaS 锁定;④ **open-core 多许可 + 买断制** vs 纯开源/纯闭源订阅;⑤ **原生 AI Employee + Agent 开放接口（MCP/CLI/Skills）**。

**综合结论**——护城河：插件微内核（极致可扩展 + 生态）+ 数据模型驱动（字段两层模型，业务实体可沉淀）+ self-hosted（数据主权、无锁定）+ AI Employee（带上下文、受字段级 ACL 约束、可审计）。四者叠加形成的「可靠 + 可扩展 + 可被 AI 安全操作」组合，单一竞品难同时覆盖。竞争风险：① open-core 收费边界（MCP server 等高级能力在商业买断包，免费版边界需明示）② v2 重构期（client 与 client-v2、schema-component 与 flow-engine 双轨并存，过渡期 API 不稳）③ 学习曲线陡（多层抽象叠加）④ 多数据源类型兼容边缘问题 ⑤ AI 无代码平台同质化竞争激烈。

---

## 套利机会分析

- **对「想做平台型产品」的架构师**：这是当下最完整的「微内核 + 插件」开源参考实现。精读 `packages/core/server/src/application.ts`（内核编排）+ `plugin.ts`（生命周期钩子）+ `plugin-manager.ts`（拓扑加载），能直接学到「内核稳定、功能无限生长」的工程范式。
- **对「要给企业系统接 AI agent」的团队**：`packages/core/ai` 的 `ToolsManager`（`defaultPermission:'ASK'`）+ `plugin-ai` 的 ACL 集成，是「AI 能干活又不越权、可审计」的可落地范本，比从零设计 agent 权限体系省下大量踩坑。
- **对「数据散在多个已有系统」的企业**：NocoBase 的 `data-source-manager` 能 introspect 反射已有数据库、外部 API 当数据模型用，不强制数据迁移——是做统一管理后台的低成本路径。
- **对「研究开源商业化」的创业者**：NocoBase 是中国团队出海、不融资、买断制、open-core 的稀缺真实样本，其 v2.0 的「许可从 AGPL 转 Apache + 部分商业插件开源」战略调整值得复盘。

---

## 风险与不足

- **学习曲线陡峭**：field-type/field-interface 两层、`resource:action` API 约定、formily x-component、flow-model 多套抽象叠加，新人上手门槛偏高。这是「可扩展性」的代价。
- **v2 重构期双轨并存**：`client` 与 `client-v2`、`schema-component` 与 `flow-engine` 当前并行，过渡期 API 未完全收敛，存在迁移边缘 bug（代码注释里可见「循环依赖移除」「冗余 API 移除」等演进痕迹）。
- **open-core 收费边界需主动甄别**：MCP server 等高级 AI/企业能力在商业买断包，OSS 仓库内 grep 不到实现——免费版与商业版的能力边界，采用前需明确确认。
- **许可元数据滞后**：`package.json` 的 `license` 字段仍写 `AGPL-3.0`，源码文件头写 dual-license，但根目录已有 `LICENSE-APACHE.txt` 且 v2.0.3 起核心已转 Apache-2.0——元数据未同步，是客观可观测的不一致。
- **多数据源类型兼容**：外部库 introspect 推断的字段/关系/主键映射存在边缘问题（如 PostgreSQL 类型映射报错 issue #9050），不全时需手工校正。

---

## 行动建议

- **用它**：在线 Demo（<https://demo.nocobase.com/new>）直接体验数据模型 → 页面 → 工作流配置;或 Docker 一键私有部署（`docker-compose.yml`），数据留在自己的库里。
- **学它**：精读微内核四件套——`packages/core/server/src/application.ts`（内核）+ `plugin.ts`（生命周期）+ `packages/core/database/src/collection.ts`（数据模型，看 field-type/interface 两层）+ `packages/core/resourcer/`（resource:action API）。再看 `packages/core/ai/` + `plugin-ai/` 学 AI Employee 权限设计。
- **fork 它**：Apache-2.0 核心允许 fork 与二次开发;做插件则参考任一官方插件（如 `plugin-action-export`）的 `src/server` + `src/client` 双端标准结构。注意商业插件与 Pro 能力的许可边界。

---

## 知识入口

| 入口 | 链接 | 用途 |
|---|---|---|
| GitHub 仓库 | <https://github.com/nocobase/nocobase> | 源码 / Release / Issue |
| 官方文档 | <https://docs.nocobase.com/> | Plugin / AI Plugin / Workflow 开发文档 |
| 在线 Demo | <https://demo.nocobase.com/new> | 免装即玩，体验数据模型/页面/工作流 |
| 官网 | <https://www.nocobase.com/> | 定位 / 商业版 / 用户故事 blog |
| 社区论坛 | <https://forum.nocobase.com/> | 支持主战场（GitHub issue 仅 129） |
| DeepWiki | <https://deepwiki.com/nocobase/nocobase> | 架构解读 |
| Release 时间线 | <https://www.nocobase.com/en/blog/timeline> | 1005 个 tag 的版本演进 |
| 本地源码 | `packages/core`（27 包）/ `packages/plugins/@nocobase`（106 插件） | 架构研读起点 |

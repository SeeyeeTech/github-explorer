# GitHub推荐：7 年 1M 行代码：Ever Gauzy 凭什么挑战 Odoo 与 ERPNext

> GitHub: https://github.com/ever-co/ever-gauzy

## 一句话总结
Ever Gauzy 是一个面向自由职业者与小微企业的开源 ERP/HRM/CRM 一体化平台，由 Ever Co. LTD 持续 7 年商业化运营——百万行级 Angular + NestJS monorepo，透明奖金公式与 AI/MCP 双扩展总线是它与 Odoo/ERPNext 最显著的差异化武器。

## 值得关注的理由

- **HRM 赛道罕见的「透明奖金公式」**：`BonusTypeEnum = { PROFIT, REVENUE }`，平台可公开利润率与员工分配比例——平台经济、咨询、外包公司拿来即用，是这个赛道里少见的「道德化设计」尝试。
- **17 个 AI provider + 自研 MCP server + agent app**：2026 年完成一波密集 AI 化，新增 ai-chat 框架与 30+ 业务域 MCP tool，让 Claude Desktop 等外部 Agent 能直接对接 HRM 数据——这是传统 ERP 几乎没有的能力。
- **真插件总线（不是文件夹约定）**：`@Plugin({ imports, entities, subscribers, configuration })` 装饰器 + `ModuleRef.get` 反射调用 lifecycle hook，已支撑 67 个插件（包括 22 个 integration + 17 个 ai-provider + 业务功能模块），是真正的运行时扩展边界。

## 项目展示

![Ever Gauzy overview hero](https://docs.gauzy.co/overview.png)

*项目总览：Web + Desktop Timer + Server 的三形态协同*

![Desktop timer (collapsed)](https://docs.gauzy.co/desktop/desktop-timer-small.png)

*桌面时间追踪器：小型化形态嵌入屏幕角落*

![Desktop timer (expanded)](https://docs.gauzy.co/desktop/desktop-timer-expanded.png)

*桌面时间追踪器：展开视图，显示项目、任务与活动监控*

![Open-source marketing section](https://gauzy.co/assets/pages/index/open-source.webp)

*官方「开源」版块头图*

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/ever-co/ever-gauzy |
| Star / Fork | 6.6K / 约 1.1K |
| 代码行数 | 1,002,434（TS 71.7% / JSON 10.6% / Sass 8.8% / HTML 7.3%） |
| 项目年龄 | 87.6 个月（2019-06 至今） |
| 开发阶段 | 密集开发（近 30 天 313 commit，日均 ~10） |
| 贡献模式 | 商业实体治理（Ever Co. LTD）+ 三人核心圈（Rahul 23.1% / Ruslan 14.8% / Adolphe 13.8%，合计 ≈52%） |
| 热度定位 | 中等热度（中等成熟产品，比 Odoo/ERPNext 低一档但远高于长尾） |
| 质量评级 | 代码 中 / 文档 中 / 测试 中（348 spec.ts + 79 Gherkin + Cypress + Playwright） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景
Ever Gauzy 由 Ever Co. LTD（商业实体，74 仓库、382 followers 的 Organization）所有，创始团队位于马德里（西班牙），核心开发者 Ruslan Konviser（联合创始人/CEO）与 Rahul Rathore（首席工程师）持续投入 7 年。商业实体而非个人项目的治理结构，使它在开源协议（AGPL-3.0 + open core 商业插件）与服务化路径上有清晰分工——这是判断它「会持续维护」的重要依据。

### 问题判断
团队看到了 Odoo/ERPNext 的两个痛点：(1) 模块耦合重，定制需要在 fork 上长期合并；(2) HRM 赛道的奖金/分账逻辑多为「黑箱」，而平台经济/咨询/外包公司恰恰最需要透明分账。前者他们用 monorepo + 插件总线解决，后者用 `BonusTypeEnum` 公公式解决。

### 解法哲学
- **明确选择**：透明化分账公式（profit/revenue × percentage）+ 多形态（Web/Desktop Timer/Server/Agent App/MCP）+ AI-native 集成层。
- **明确不做的**：不追求与 SAP/Oracle 同档的企业级复杂度（不重 CRM 销售自动化）；不维护在线 SaaS demo（demo.gauzy.co 已下线，新用户必须 self-host Docker——这是核心 issue #7234 的明确方向）。

### 战略意图
产品是「open core 商业 SaaS」的标准化路径：AGPL-3.0 锁定核心，企业级插件与云服务收费；2026 年的 AI/MCP 化是抢占**「AI Agent 时代的 ERP 中间层」**——把 HRM/CRM 的所有业务能力包装成 AI 可调用的 tool。

> 官方博客与外部 critical review 稀缺；DeepWiki 自动爬取的索引是目前最权威的第三方解读，独立 critical review 几乎没有——这是项目在叙事上的真空带。

## 核心价值提炼

### 创新之处
1. **透明奖金公式（PROFIT/REVENUE × percentage）**——HRM 赛道罕见。`packages/core/src/lib/employee-statistics/employee-statistics.service.ts:187` 的 12 行 `calculateEmployeeBonus` 是核心，387 行 CQRS handler `aggregate-employee-statistic.handler.ts` 串行聚合每员工的 income/expense/recurring/split/profit/bonus。
2. **Odoo 风格实体字段注入**——比 Odoo manifest.xml 更轻量：`integration-github` 的 `customFields.OrganizationProject.push({ name: 'repository', relation: ... })` 是真实运行实例，非空架。
3. **AI provider 静态注册表 + 14 行模板**——每个 `ai-provider-*/ai-provider-*.plugin.ts` 就是 `class XxxProviderPlugin extends BaseAiProviderPlugin { definition = ... }`，`AiProviderRegistry` 用 static map 而非 Nest DI，让 plugin 端不必 import chat module 的图——strategy + registry 在 NestJS 中的最短表达。
4. **MCP server 完整包装**——`packages/mcp-server/mcp-server.ts` 用 `@modelcontextprotocol/sdk` 注册 30+ 业务域 tool，ExtendedMcpServer 子类化把 Zod schema 转 JSON schema 暴露给 Claude Desktop——传统 ERP 中极少实现。
5. **集成插件自研 Probot 框架**——`packages/plugins/integration-github/src/lib/probot/` ~960 行（`@Hook` 装饰器 + `MetadataScanner` discovery + `SmeeClient` 代理），完全控制 webhook 路由。

### 可复用的模式与技巧
- **14 行 provider plugin 模板**（`BaseAiProviderPlugin`）：任何需要「多模型可插拔」的项目都可借鉴。
- **NestJS plugin bus**（`@Plugin` 装饰器 + ModuleRef 反射）：比 Nest 官方 dynamic module 更轻量。
- **env-driven driver switch**（`mikroOrmDriverMap[process.env.DB_TYPE] || default`）：一行抽象四数据库（PostgreSQL/MySQL/MongoDB/SQLite）。
- **透明奖金公式**：profit / revenue × percentage 的最小可工作实现。
- **static registry over Nest DI**：plugin 解耦 graph 的代价是多进程不共享 + HSR 需自管——trade-off 需自己评估。
- **CQRS query handler 聚合**（`AggregateOrganizationQueryHandler` 模板）：聚合统计场景的通用抽象。
- **MCP server via Zod → JSON schema bridge**：让 Claude Desktop 等外部 Agent 直接消费业务 API。

### 关键设计决策
- **MikroORM + TypeORM + Knex + Mongoose 四栈共存**（`database.module.ts`）：同一 entity 写出 `type-orm-*.repository.ts` 与 `mikro-orm-*.repository.ts` 两个空 wrapper（如 github plugin 里那 4 行类声明），是真实迁移未完成的债——**不要学**。
- **Nx22 + Lerna 7 + yarn 1 workspaces 三层**：`lerna.json` 设「useNx: true」后 Lerna 只做 changelog；可保留但建议淘汰 Lerna。
- **AI provider 用 static registry 而非 Nest DI**：换 plugin 热插拔自由，代价是多进程不共享、HSR 泄露。
- **MCP SDK 越界私有字段**：`as unknown as McpServerWithRegisteredTools` 访问 SDK 私有 `_registeredTools`——简化实现换 SDK 升级脆弱。
- **Plugin bootstrap 静默失败**（仅 console.error）：方便插件作者，但生产环境可能掩盖真实故障。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | Ever Gauzy | Odoo | ERPNext | Dolibarr |
|------|------------|------|---------|----------|
| Star | 6.6K | ~53.8K | ~38.3K | ~16K |
| 主语言 | TS (Angular+NestJS) | Python (JS 前端) | Python (Frappe) | PHP |
| 架构模式 | Monorepo + 真插件总线 | Manifest.xml 模块 | DocType + Frappe app | 模块文件夹 |
| 多 DB 支持 | PostgreSQL/MySQL/MongoDB/SQLite | PostgreSQL（主） | MariaDB/PostgreSQL | MySQL/PostgreSQL |
| AI/MCP 集成 | 17 provider + MCP server + agent app | 模块市场，AI 模块少 | LLM 集成早期 | 无 |
| 桌面形态 | Electron desktop/timer/server 三形态 | 无官方桌面 | 无官方桌面 | 无官方桌面 |
| 奖金公式透明化 | 内建（PROFIT/REVENUE） | 无原生支持 | 无原生支持 | 无原生支持 |
| 许可证 | AGPL-3.0（open core） | LGPL（open core） | GPL-3 | GPL-3 |

### 差异化护城河
- **透明奖金公式** + **多形态桌面** + **AI/MCP 集成**是 Odoo/ERPNext 短期内难以快速复制的组合——前两者需要重新设计领域模型，后者需要重新搭建 plugin runtime。
- 真插件总线（反射式 lifecycle hook）已运行 67 个插件，生态规模虽小但比 ERPNext 的 DocType 模块更轻量。

### 竞争风险
- Odoo/ERPNext 的「体量势能」：53.8K vs 6.6K stars，3 倍 module 生态，企业级销售自动化能力远强。
- 若 Odoo 在 2026-2027 推出 AI agent 模块（其官方 AI roadmap 已启动），MCP 差异化将被快速稀释。

### 生态定位
填补「自由职业者/平台经济/小咨询公司」这个 Odoo 过重、Dolibarr 过轻、Notion/Airtable 又不够专业的中间地带——尤其是需要透明分账的场景。

## 套利机会分析
- **信息差**：6.6K star 显著低于 Odoo/ERPNext，但功能完整度与 AI 集成反而超前——是「被低估的成熟产品」。中文社区几乎没有系统介绍。
- **技术借鉴**：plugin bus 模式 + AI provider 静态注册表 + env-driven 多 DB 切换，三件套可直接搬到自研项目。
- **生态位**：透明奖金公式是平台经济/外包公司刚需，几乎无竞品直接覆盖。
- **趋势判断**：2026-08 单月 606 commit 印证「AI 化加速期」，MCP server 让它有可能成为「Agent 时代的 ERP API 网关」——比传统 ERP 更适合 AI 工作流嵌入。

## 风险与不足

- **核心圈窄 + author 字段未规范化**：3 人占 52% commits，且同一开发者多个 git author 别名（Rahul/R./RAHUL）——bus factor 风险。
- **demo.gauzy.co 已下线**：评估门槛极高，新用户必须 self-host Docker，issue #7234 是 open 时间最长的讨论之一。
- **22.4% open-issue rate**：维护者容量瓶颈信号，与「三人核心圈」互证。
- **7 年 4,373 tags / 100 releases 但最新 v111.42.1 仍标 prerelease**：发版节奏快但长期稳定分支信号弱。
- **四 ORM/DB 栈未完成迁移**：同一 entity 的双 repository wrapper 是真技术债。
- **四 ORM + 三 monorepo 工具 + 70 个 GH Actions workflow**：碎片化严重，新贡献者上手门槛极高。
- **核心员工奖金公式（`aggregate-employee-statistic.handler.ts`）几乎无 spec 覆盖**——公式算法恰恰是产品差异化所在。
- **核心模块 1573 处 `console.log`/`tslint:disable` 残留**：CI 配置成熟 ≠ 内部代码干净。

## 行动建议

- **如果你要用它**：适合 10-200 人规模、需要透明分账的自由职业者/咨询/外包公司，且团队有自托管能力（demo 已下线）。如果你只是要通用 ERP，Odoo/ERPNext 仍是更安全的选择。
- **如果你要学它**：先读 `packages/plugin/src/lib/plugin.ts` + `plugin.module.ts` + `plugin.helper.ts`（真插件总线核心，~150 行），再看 `packages/plugins/ai-chat/src/lib/base-ai-provider.plugin.ts` + `provider-registry.ts`（14 行 plugin 模板 + 静态注册表），最后看 `packages/mcp-server/src/lib/mcp-server.ts`（MCP 业务暴露）。前三件套是核心可借鉴资产。
- **如果你要 fork 它**：最值得改进的三个方向：(1) 合并 MikroORM/TypeORM/Mongoose 为单一 ORM；(2) 删掉 Lerna 与 yarn 1，只留 Nx；(3) 重写员工奖金模块的 spec 覆盖。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/ever-co/ever-gauzy |
| Zread.ai | 未收录 |
| 关联论文 | 无 |
| 在线 Demo | 无（demo.gauzy.co 已下线，需 self-host Docker，详见 issue #7234） |
| 官方文档 | https://docs.gauzy.co |
| 官方网站 | https://gauzy.co |
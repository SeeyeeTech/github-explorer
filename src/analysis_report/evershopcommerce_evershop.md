# 一个人写 5 年的开源电商，对标 Medusa

> GitHub: https://github.com/evershopcommerce/evershop

## 一句话总结

EverShop 是一个开源、TypeScript-first、**自带前台店面 + 后台管理、开箱即用**的全栈电商平台（Node.js + React + GraphQL + PostgreSQL）——它最反差的地方是：这个 1 万 star、13.5 万行、被新兴市场店主真实建店在用的完整平台，五年来几乎由一位越南开发者 The Nguyen 一个人写成。

## 值得关注的理由

- **教科书级单人长跑**：主作者 @treoden（The Nguyen）独占 91% commit / 96.2% 贡献，巴士因子=1。一个人持续 5 年维护一个生产级电商平台，既是惊人的个人产出，也是最大的可持续性风险——这种「一人对抗一个品类」的反差本身就是好故事。
- **「全栈开箱即用」对打「headless 要自己搭前台」**：区别于龙头 Medusa（34k star，只给后端 API、前台要自己用 Next.js 搭，初始开发常 $5k–25k+），EverShop 自带 storefront + admin，`docker compose up` 分钟级起一个完整店。在「Node/TS 全栈、batteries-included」这个细分里近乎独占。
- **清晰的 open-core 商业化路径**：Self-hosted 永久免费 + EverShop Cloud 托管（Personal $10/月、Professional $20/月，建设中）+ 模块/主题 Marketplace + Open Collective + 寻求融资——正面回答了「单人开源电商如何可持续」。

## 项目展示

![EverShop Banner](https://raw.githubusercontent.com/evershopcommerce/evershop/dev/.github/images/banner.png)

![前台店面](https://raw.githubusercontent.com/evershopcommerce/evershop/dev/.github/images/evershop-demo-front.png)

买家前台 storefront（开箱即用）。

![后台管理](https://raw.githubusercontent.com/evershopcommerce/evershop/dev/.github/images/evershop-demo-back.png)

后台 admin panel。在线 Demo：[demo.evershop.io](https://demo.evershop.io/) ｜ 后台 [demo.evershop.io/admin](https://demo.evershop.io/admin)（demo@evershop.io / 123456）。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/evershopcommerce/evershop |
| Star / Fork | 10125 / 2338（23% 超高 fork 率，大量用户 fork 下来真实建店） |
| 代码行数 | 135K（TSX 29.8% + TS 21.6% + JS 17.8% + JSX 8.5%；TS+TSX 51% 与 JS+JSX 26% 并存 = v1 JS→v2 TS 迁移未竟；JSON 18% 是声明式配置非业务代码） |
| 项目年龄 | 61 个月（约 5 年，2021-05 起） |
| 开发阶段 | 整体活跃但近月踩刹车（近 30 天仅 4 commit，5 年长跑 + 周期性冲刺） |
| 贡献模式 | 绝对单人主导（The Nguyen 占 91%，巴士因子=1） |
| 热度定位 | 大众热门（被关注度低估的实用派，长期被 Medusa 光环遮蔽） |
| 质量评级 | 代码[良好·约定式架构] 文档[优·官网 docs + 在线 Demo] 测试[有·module 自带 tests，但 test commit 少] |
| License | GPL-3.0（强 copyleft，防纯商用 fork） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

主作者 **The Nguyen（Nguyen Huu The，GitHub @treoden，越南）**——一位全栈工程师，以个人之力持续 5 年维护这个平台。org `evershopcommerce` 是项目壳而非真正团队公司。从他在 npm 上的 `mysql-query-builder`、`node-sql-parser` 等底层数据库工具包可见，他长于后端数据层与框架抽象——EverShop 自研的查询构建器与迁移系统正源于此。这是「单人 5 年长跑的开源电商平台」这一稀缺叙事的核心。

### 问题判断

开源电商赛道的主流（Medusa、Vendure、Saleor）都押注 headless——只给后端 API，前台让你自己搭。这对大团队是灵活，对中小商家/独立开发者却是负担：要额外搭一套 Next.js 前台，初始投入常 $5k–25k+。作者看到的缺口是：**很多人只想要一个「拿来即用的完整店」**——前台、后台、产品、分类、属性、购物车、结账、支付、促销一应俱全，`docker compose up` 就能跑。同时，PHP 老牌（Magento/WooCommerce）对现代 JS 团队不亲和，Shopify 又是闭源锁定。EverShop 切的正是「Node/TS 现代栈 + 全栈开箱即用 + 完全可控」这个空位。

### 解法哲学

- **明确选择全栈单体而非 headless 微服务**：自带 storefront + admin，轻量、上手快、开发 overhead 最小。
- **明确选择约定式模块架构**：电商能力按 14 个 module 垂直切分，每个 module 统一目录约定（api + route.json + pages + graphql + services + migration + subscribers），通过 processor/hook/event 扩展点改行为而不动核心代码。
- **明确选择自研而非主流 ORM**：用自家 `@evershop/postgres-query-builder`（而非 Prisma/TypeORM/Sequelize）——可控、与平台深耦合，代价是自己背维护成本。
- **明确选择 v2 全量迁 TypeScript**：从 v1 的 JS 重写为 TS-first（仍在进行中）。
- **明确选择 GPL-3.0 + open-core**：强 copyleft 防纯商用 fork，靠 Cloud 托管 + 付费模块变现。

### 战略意图

README「The Future of EverShop」明确在建 **EverShop Cloud** 并公开招募战略投资人。官网 /pricing 已列出托管分层（免费自托管 / Personal $10 / Professional $20，含 SSL/S3/GitHub 部署），另有模块/主题 Marketplace。即典型「**开源整店获客 → Cloud 托管 + 付费扩展变现**」的 open-core 三条腿，是单人项目走向可持续商业化的清晰路径。

## 核心价值提炼

### 创新之处

1. **约定式模块架构（最值得学）**：`src/modules/` 下 14 个垂直 module（catalog/checkout/customer/promotion/oms/stripe/tax…），每个 module 自带 `route.json`(声明式路由) + `payloadSchema.json`(JSON Schema 入参校验) + frontStore/admin 双端 React 页面 + graphql + services + migration + subscribers。**新增一个支付/物流/营销能力 = 复制一个 module 目录**，靠文件结构自动加载——这是它能以「框架/平台」自居、被第三方扩展的根基（也是 JSON 占 18% 的真实来源）。
2. **全栈开箱即用**：storefront + admin + 数据库迁移 + 种子数据全齐，`docker compose up` 分钟级起完整店，对打 headless 阵营的「自建前台」门槛。
3. **自研 PostgreSQL 查询构建器**：不用主流 ORM，自造轻量 query builder——架构完全自主可控。
4. **声明式路由 + Schema 校验自动加载**：route.json 声明 `{methods, path, access}`、payloadSchema.json 声明入参校验，无需手写注册，约定优于配置。

### 可复用的模式与技巧

1. **约定式 module 目录 + 自动加载**：垂直切分领域 + 统一目录约定 + 文件结构驱动注册——任何想做「可插拔扩展平台」的项目都可借鉴。
2. **声明式路由/校验（route.json + JSON Schema）**：把路由与入参校验从代码移到声明文件，降低样板。
3. **hook/event/processor 扩展点**：改行为不动核心代码的扩展范式。
4. **monorepo 拆「核心 + 脚手架 + 基础设施包」**：create-evershop-app 降低上手、postgres-query-builder 独立复用。

### 关键设计决策

- **全栈单体 vs headless**：用「开箱即用、上手快」换「灵活度与生态扩展性不如纯 headless」——这是它与 Medusa/Vendure 的根本路线分野。
- **自研 query builder 而非 ORM**：可控但需自己背维护成本，对单人项目是双刃剑。
- **v1 JS → v2 TS 重写**：拥抱强类型与现代 DX，代价是 v2.0 是破坏性升级（需 Node ≥18.17）、迁移尚未完工（TS/JS 混合态）。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | EverShop | Medusa | Vendure | Saleor |
|------|----------|--------|---------|--------|
| 形态 | 全栈单体（自带前台+后台） | headless（仅后端） | headless（仅后端） | headless（仅后端） |
| 技术栈 | Node/Express/React/GraphQL | Node/TS | NestJS/GraphQL | Python/Django/GraphQL |
| 前台 | 内置开箱即用 | 自建 Next.js | 自建 | 自建 |
| 上手 | docker compose 分钟级 | 较重，初始投入高 | 学习曲线陡 | 偏重 |
| Stars | 10k | 34k | 8k | 21k |
| 定位 | 拿来即用整店 | 灵活 headless 龙头 | 企业级 headless | GraphQL headless |

### 差异化护城河

护城河 =「**Node/TS 全栈、自带前台+后台、轻量单体、开箱即店**」这一组合——Medusa/Vendure/Saleor 都没正面覆盖（它们全是 headless）。EverShop 在此细分内几乎无同量级直接对手。加上约定式 module 扩展体系与 5 年口碑，形成差异化空位。

### 竞争风险

- **巴士因子=1（最大风险）**：1 万 star、5 年、13.5 万行几乎一人写成，可持续性高度依赖作者一人。近月 commit 骤降更放大此担忧。
- **被 Medusa 光环压制**：Medusa 生态、社区、融资全面占优；若它推出更友好的全栈 starter，EverShop 的差异化会被蚕食。
- **灵活度/生态不如纯 headless**：全栈单体在深度定制与第三方扩展生态上弱于 Medusa/Vendure。
- **TS 迁移未竟 + v2 破坏性升级**：混合态增加维护复杂度，升级门槛劝退部分老用户。

### 生态定位

它是「Node/TS 全栈、开箱即用」开源电商的细分领跑者，填补了 headless 阵营与闭源 SaaS（Shopify）/ PHP 老牌（Magento/WooCommerce）之间的空白，承接「要现代栈、要完全可控、又不想自建前台」的开发者。

## 套利机会分析

- **信息差**：不算被低估质量，而是「**被关注度低估的实用派**」——1 万 star 在被 Medusa(34k) 光环压住，但在「全栈开箱即用」细分上声量与实用度不匹配。「单人对抗 Medusa 微服务复杂度、主打拿来即用整店」是有反差的好选题。
- **技术借鉴**：「约定式 module + 声明式路由/校验 + 自动加载」「hook/event 扩展」「monorepo 核心+脚手架+基础设施」可迁移到任何可扩展平台。
- **生态位**：想要现代栈、完全可控、开箱即用整店的中小商家/独立开发者，这是当前最佳开源选择。
- **趋势判断**：开源电商持续有需求，EverShop 凭差异化卡位 + v2 TS 重写 + Cloud 商业化有上升空间；但单人依赖与近月降速是需观察的变量。

## 风险与不足

- **⚠️ 巴士因子=1**：高度依赖单一作者，近月 commit 骤降（c30=4）放大可持续性担忧。
- **维护期信号**：fix 占 53%、feature 仅 11.5%——成熟稳定但扩张放缓。
- **本地化支付/功能需社区补齐**：支付以 Stripe/PayPal/Klarna 为主，新兴市场网关（如 PhonePe，印度）靠社区扩展（issue 实证有真实店主诉求）。
- **TS 迁移未完成**：v1 JS 残留与 v2 TS 并存，v2.0 是破坏性升级。
- **生态规模有限**：第三方模块/主题市场仍在建设，扩展生态远不及 Medusa。

## 行动建议

- **如果你要用它**：你是想要**现代 Node/TS 栈、完全可控、自带前台+后台、快速起完整店**的中小商家/独立开发者——它是当前最佳开箱即用开源选择（`npx create-evershop-app` 或 docker compose 分钟级起店）。若你要最大灵活度与最强生态、且有团队自建前台，选 headless 的 Medusa；要企业级 headless 选 Vendure。
- **如果你要学它**：重点读 `packages/evershop/src/modules/`（约定式 module 架构：route.json + payloadSchema.json + frontStore/admin pages + graphql + migration + subscribers）、`@evershop/postgres-query-builder`（自研查询构建器）、`lib/`（自研路由/中间件/构建链路）。这是「约定优于配置的可扩展平台」的优秀样本。
- **如果你要 fork 它**：最有价值的方向是补本地化支付网关（新兴市场需求强）、降低单人依赖（建立核心维护者团队）、完成 TS 迁移，以及围绕约定式 module 体系做扩展/主题贡献。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/evershopcommerce/evershop （已收录，含完整架构概览） |
| Zread.ai | 未确认（建议发布前补查） |
| 关联论文 | 无（工程项目） |
| 官网 / 文档 | https://evershop.io/ ｜ 文档 https://evershop.io/docs ｜ 定价 https://evershop.io/pricing |
| 在线 Demo | 前台 https://demo.evershop.io/ ｜ 后台 https://demo.evershop.io/admin （demo@evershop.io / 123456） |
| 独立横评 | [Medusa v2 / Vendure v3 / EverShop 坐标定位 — codenote.net](https://codenote.net/en/posts/typescript-oss-ecommerce-platforms-medusa-vendure-evershop/) |

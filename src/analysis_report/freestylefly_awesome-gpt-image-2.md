# GitHub 推荐：4 个月 17.5K stars：苍何把 GPT-Image-2 提示词做成了可被 Agent 调用的工程资产

> GitHub: https://github.com/freestylefly/awesome-gpt-image-2

## 一句话总结

这是一个被命名误导的「资源库」——表面是 awesome-list，实则是「Prompt as Code 资产库 + 配套可视化 SaaS + Agent Skill 包」三合一的工业化提示词引擎：把 532 个爆款图逆向成 13 字段 schema + 22 个工业模板，让 Claude Code / Codex / Cursor 能像 `npx skills add` 一行命令一样自动调用。

## 值得关注的理由

1. **稀缺的方法论溢出**：17.5k Star 不是案例堆出来的，是把 prompt 从「自由散文」拆成「结构化工程资产」做出来的——这套 SoT markdown → 编译 JSON → Agent reference 的工作流，国内 prompt 资源库目前仅此一份跑通。
2. **金融级工程严谨度做内容项目**：PL/pgSQL Reservation Saga 三段式事务扣费、`pg_advisory_xact_lock` 配合 unique partial index 做付费群 QR「一张当前码」热替换、Stripe + 支付宝双支付单表 SKU——一个 4 个月的 side project 在后端严谨性上超过大量商业 SaaS。
3. **Skill 化分发是新分发渠道的早期卡位**：通过 `bin/install.mjs` 把 Skill 同时写到 `~/.claude/skills` / `~/.codex/skills` / `~/.agents/skills`，搭 GitHub Packages + npm 双仓发布，是 Agent 时代「仓库即插件」的工程化范本。

## 项目展示

![GPT-Image2 Prompt System banner](https://raw.githubusercontent.com/freestylefly/awesome-gpt-image-2/main/data/images/banner.svg)
*项目品牌横幅 SVG——把「GPT-Image2 + Prompt as Code」做成一张产品级封面*

![GPT-Image2 Gallery website preview](https://raw.githubusercontent.com/freestylefly/awesome-gpt-image-2/main/data/images/site-preview.png)
*产品化站点截图：gpt-image2.canghe.ai，532 case 瀑布流 + 分类筛选 + 提示词复制*

![Urban Metabolism Atlas — case1 信息图](https://raw.githubusercontent.com/freestylefly/awesome-gpt-image-2/main/data/images/case1.jpg)
*信息图类别代表案例：展示 GPT-Image-2 的精确中文渲染 + 结构化排版能力*

![Interaction design diagram — case17 UI 设计](https://raw.githubusercontent.com/freestylefly/awesome-gpt-image-2/main/data/images/case17.jpg)
*UI/Interfaces 类别代表案例：组件层级 + 界面纹理的工业化模板*

![Snack brand technical breakdown — case310 产品拆解](https://raw.githubusercontent.com/freestylefly/awesome-gpt-image-2/main/data/images/case310.jpg)
*Products & E-commerce 类别代表案例：自动标注组件名 + 卖点的产品拆解风格*

> 总共发现 47 个媒体元素，筛选后保留 5 个最具代表性样本；已排除 badge/CI 状态图标、赞助商 logo、二维码等非展示性内容。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/freestylefly/awesome-gpt-image-2 |
| Star / Fork | 17,497 / 1,810（Watchers 58） |
| 代码行数 | 31,312 行（JSON 51.5% / JavaScript 17.8% / JSX 13.3% / CSS 10.7% / SQL 6.2%） |
| 项目年龄 | 4 个月（首次提交 2026-04-25） |
| 开发阶段 | 稳定维护（5 月单月 102 commit 爆量后转维护） |
| 贡献模式 | 单人主导（freestylefly 81% commits，6 名贡献者） |
| 热度定位 | 大众热门（2026-08-24 空降 GitHub Trending 第二 +628 stars） |
| 质量评级 | 代码 优秀 / 文档 优秀 / 测试 基本 / CI/CD 基本 / 错误处理 优秀 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

苍何（freestylefly），Microsoft MVP，WeSight 创始人，公众号「苍何」主理人，武汉。账号年龄 7.9 年，公开仓库 81 个，粉丝 1661。他的其他旗舰仓库 `CodexGuide`（3,284 Star）、`wesight`（894 Star）都不及本项目的 17.5k Star——这是他目前最具影响力的旗舰项目。Bio 自述「Sharing thoughtful insights on AI, building cool things along the way」——典型的「公众号 / Sponsors / 付费社群」三位一体个人开发者。

### 问题判断

2026-05 启动 schema 化迁移（Supabase migration 起始时间戳 `202605090001`），正值 GPT-Image-2 走红 + 社区爆款集中涌现 + Agent 编程工具普及三重叠加。早做没需求，晚做红海已被锁死。Issue #2「在线站点」直接揭示演化路径：用户逼着作者从「静态 README 列表」升级到「实时 SaaS 付费会员」——不是预先规划，是被需求推出来的。

### 解法哲学

- **结构化 > 自由文本**：把同一张爆款图逆向成 `{subject, composition, materials, lighting, text, aspect_ratio, constraints, negative}` 8 大块原子字段 + 13 字段 case schema + 22 工业模板，让 Agent 可以「先锁结构，再换主语」。
- **Prompt as Code = 提示词界的 Tailwind / CSS Variables**：每一类风格（UI / 海报 / 商品 / 插画……）是一段「约束条件 + 反模式 + 案例指针」，可被程序化匹配、引用、组合。
- **数据即代码**：532 个 case 在编译期就 schema 化（`scripts/generate-site-data.mjs`），不是运行时拼字符串——LLM 选模板时拿到的是「结构化索引」而非「自然语言摘要」，幻觉率显著下降。
- **明确不做什么**：不做模型微调/LoRA；不做纯文生 UI 的「设计稿转代码」；不和 Midjourney 拼通用提示词（只针对 GPT-Image-2）；不做付费模板锁闭（核心库继续 MIT）。

### 战略意图

`data/cases.json` + `data/style-library.json` 是 IP 资产，`gpt-image2.canghe.ai` 是流量入口，Agent Skill 是分发渠道（让 skill 自己滚雪球）。飞轮结构：公众号引流 → 站点付费生成 → Sponsors 反哺 → 新 prompt 持续入库 → Skill 在 Agent 工具链扩散。**genuinely open 但带 open-core 后端**：核心 532 case + 22 template + 13 category 全部 MIT；商业化是「站点付费生成 + 付费交流群（¥9.90） + 公众号会员」三层，后端 SKU 与开放 repo 解耦。

## 核心价值提炼

### 创新之处

1. **「Prompt as Code」13 字段 case schema**——把 532 个自由散文 prompt 拆成 `{id, title, image, prompt, category, styles, scenes, featured, sourceUrl ...}` 结构化资产；新颖度 4 / 实用性 5 / 可迁移性 4
2. **Markdown → JSON → Agent reference 编译链（SoT 单一可信源）**——人在 `docs/gallery-part-{1,2}.md` 写，机器派生 `data/cases.json` 和 `agents/skills/.../references/style-library.md`，避免「文档 + JSON + Skill」三份数据漂移；新颖度 4 / 实用性 5 / 可迁移性 5
3. **PL/pgSQL Reservation Saga**——`reserve_generation_usage` 三段式事务（reserve → complete/release），单事务内 FOR UPDATE 行锁 + 决策路径（免费额度 / 扣 1 credit / raise）+ refund 流水；新颖度 3 / 实用性 5 / 可迁移性 5
4. **双支付 + 双 SKU 单表**——Stripe USD + 支付宝 CNY 共享 `membership_plans` 表 + `amount_cents` / `alipay_amount_cents` 显式金额列，前端无法绕过；新颖度 3 / 实用性 4 / 可迁移性 5
5. **付费 QR 资产 + `pg_advisory_xact_lock` + unique partial index「一张当前码」**——`community_group_qr_assets` 表只允许一行 `is_current=true`，QR bytes 走 `bytea` + magic bytes 校验，非 PAID 用户拿不到字节；新颖度 4 / 实用性 4 / 可迁移性 4

### 可复用的模式与技巧

1. **「SoT markdown → 编译 JSON → Agent reference」三件套**：人在 markdown 写、机器在 JSON 查、Agent 在 reference 里找——任何「内容/工具库想同时被人和 AI 消费」的场景都适用
2. **PL/pgSQL Reservation Saga**（先冻结再决策再回滚）：所有「API 计费 / 钱包扣费 / 配额预占」类 SaaS 后端的样板
3. **`pg_advisory_xact_lock` + unique partial index「一张当前 X」**：付费群 QR / 限流配置 / 热替换轮播图 / 当前生效的优惠码
4. **跨 agent Skill 一键分发**（`bin/install.mjs` 写 `~/.claude/skills` / `~/.codex/skills` / `~/.agents/skills`）：任何想把自家 Skill 同时装到 Claude Code + Codex + Cursor 的工具作者
5. **「双支付单表 SKU」**（USD Stripe + CNY 支付宝共享 `membership_plans`）：跨境订阅/数字商品 SaaS 的极简模板
6. **`sanitizeAlipayNotifyParams` 白名单过滤**：剔除 `sign/buyer_id` 等敏感字段后再落 DB——所有第三方支付回调持久化的安全样板

### 关键设计决策

**决策 1**: 把 markdown 视为单一可信源（SoT），用编译脚本派生 JSON 和 Agent Skill 引用
- **问题**: 同时维护「给人看的 gallery」「给站点用的 JSON」「给 Agent 用的 reference」会互相漂移，且 prompt 案例每周都在新增
- **方案**: `docs/gallery-part-{1,2}.md` 是人维护的 SoT；`scripts/generate-site-data.mjs` 用正则解析出 13 字段 case；`scripts/generate-style-skill.mjs` 反向从 `data/style-library.json` 编译成 markdown 给 Agent 当参考；`npm run prebuild` 钩子强制每次 dev/build 前重新生成
- **Trade-off**: 牺牲「修改响应速度」换「跨下游一致性」
- **可迁移性**: 高

**决策 2**: PL/pgSQL 的 `reserve_generation_usage` 三段式事务做图生成扣费
- **问题**: GPT-Image-2 调用是慢操作（数秒～数分钟），且上游可能 429 / 5xx；「先扣费再调用」上游失败要回退，「先调用再扣费」并发或网络异常会导致重复扣费或漏扣
- **方案**: 单条语句里 `FOR UPDATE` 锁 profile 行 → 决策路径（免费额度 / 扣 1 credit / raise）→ insert reservation → 回填 `-1` 流水；完成后 `complete_generation_reservation` 置 succeeded；失败 `release_generation_reservation` 回滚 + refund 流水
- **Trade-off**: 牺牲「简单性」（事务逻辑进数据库）换「强一致性 + 幂等」
- **可迁移性**: 高

**决策 3**: 把 Agent Skill 设计成「可独立 `npm publish` + 可被 `npx skills add` 安装」的 npm 包形态
- **问题**: Agent Skill 分发渠道碎片化（Claude Code / Codex / Cursor / plugin marketplace 协议各不相同）
- **方案**: `agents/skills/gpt-image-2-style-library/package.json` 独立 `name`、`bin/install.mjs`、`publishConfig.access=public`；`.github/workflows/publish-style-skill.yml` 在 tag `gpt-image-2-style-library-v*` 触发 GitHub Packages 发布
- **Trade-off**: 牺牲「包大小」（Skill 包 9KB + references 17KB 跟着 npm 走）换「跨工具一键安装 + 版本管理 + 双仓分发」
- **可迁移性**: 极高

**决策 4**: 双支付 + 双渠道（Stripe USD + 支付宝 CNY）但 SKU 表合一
- **问题**: 海外用 Stripe，国内用支付宝；两套 SKU 难以共享定价，又要防「前端改价格绕过扣费」
- **方案**: `membership_plans.amount_cents` + `currency='usd'` 给 Stripe；同一行额外 `alipay_amount_cents` 字段给支付宝；所有金额最终落到 `payment_orders` 一行；支付宝回调用 `parseAlipayAmount` 把 `"9.90"` 解析成整数 cents（避浮点）
- **Trade-off**: 牺牲「数据库简洁性」（多两个冗余字段）换「前后端价格不会被绕过」
- **可迁移性**: 高

**决策 5**: 付费交流群走 ¥9.90 一次性付费 + 单独 QR 码资产库 + `pg_advisory_xact_lock` 保证「一张当前码」
- **问题**: 付费群 QR 码容易被截图外泄，需要随时换码 + 只有 PAID 用户能拿到 + 切换瞬间不能让多个用户拿到不同码
- **方案**: `community_group_qr_assets` 表只允许一行 `is_current=true`（unique partial index）；`replace_community_group_qr_asset` 在事务里 advisory lock + 旧行 false + 新行 insert；QR bytes 走 `bytea` + magic bytes 校验
- **Trade-off**: 牺牲「QR 码可以走 CDN」（直接 bytea 拉取，DB 流量翻倍）换「QR 资产与权限绑死、热替换无竞态」
- **可迁移性**: 中

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | freestylefly/awesome-gpt-image-2 | EvoLinkAI/awesome-gpt-image-2-prompts | YouMind-OpenLab/awesome-gpt-image-2 | Anil-matcha/Awesome-GPT-Image-2-API-Prompts |
|------|---------|--------|--------|--------|
| 案例规模 | 532 case（高结构化） | 精选数十 case | 3600+ case（弱结构化） | 数百 case |
| Schema | 13 字段 + 19 styles + 10 scenes | 无（纯 markdown） | 无（弱结构） | 仅 API 示例 |
| Agent 集成 | Skill 跨 Claude Code/Codex/Cursor + npm + GitHub Packages | 无 | 无 | 无 |
| 在线产品 | gpt-image2.canghe.ai（生成 + 付费会员 + 付费群） | 无 | 无 | 无 |
| 国际化 | 英 / 简中 / 日三语 | 英文 | 17 种语言 | 英文 |
| Stars | 17,497 | ~数千 | ~数千 | 数百 |

### 差异化护城河

- **技术护城河**: `cases.json` 13 字段 schema + `style-library.json` 22 templates + PL/pgSQL Reservation Saga + 双支付单表——都可被学，但沉淀成本高
- **生态护城河**: Agent Skill 跨 Claude Code/Codex/Cursor/npm + GitHub Packages 分发，是国内 prompt 资源库第一个把分发做穿到 Agent 工具链的
- **信任护城河**: Issue #13「社区造假」+ 三语 disclaimer + source 字段溯源（每条 prompt 都有 `sourceLabel + sourceUrl`）——是资源类项目面对 AI 时代版权问题的成熟解法

### 竞争风险

最可能被 **YouMind 量级** 击穿（对方 3600+ 案例 + 多模型 + 17 种语言，规模碾压）。一旦 YouMind 把 Schema 化 + Agent Skill 补齐，本项目差异化会被严重侵蚀。短期护城河来自「先发 + 单模型聚焦 + 商业闭环跑通」；长期需在「内容增量」「Skill 生态」「商业化收入」三轴上保持领先。

### 生态定位

在「prompt 资源 → 工程化资产」转化路径上，国内目前是唯一「schema + 编译链 + Skill + SaaS 全栈」跑通的样本；定位类似 npm 上「Tailwind / shadcn」级别——**不做模型，做模型之上的「设计 token + 工厂」**。作者苍何本人把它类比为「提示词界的 Tailwind / CSS Variables」，外部独立分析（wuqishi.com / 腾讯云开发者社区）也认同这个定位。

## 套利机会分析

- **信息差**: 17.5k Star 已经脱离「被低估」区间，但**「Prompt as Code」方法论 + Skill 包封装 + 真实运营数据**仍有溢出价值——对 Agent 开发者是真有用的工程范式，不是单纯资源堆砌
- **技术借鉴**: SoT markdown → 编译 JSON → Agent reference 三件套、PL/pgSQL Reservation Saga、跨 agent Skill 一键分发这三套模式可迁移到任何「内容资源库」/「API 计费 SaaS」/「Agent 工具作者」场景
- **生态位**: 填补了「模型之上的设计 token 与工厂」的空白——同赛道无第二家把 schema + 编译链 + Skill + 商业化全栈跑通
- **趋势判断**: 在增长（8 月仍 +628 stars/day）；符合「Agent 工具链 + 内容工程化」两大技术趋势；比 YouMind 类纯资源库有显著工程化后发优势

## 风险与不足

1. **后端测试覆盖基本**：3 个测试文件 ~50 用例集中在 `_lib`（金额解析 / alipay 验签 / community rate limit），前端 Vite 无单测，无 e2e 测试；0 refactor + 0 test 意味着后端 API（billing/admin/community）长期处于无测试保护状态
2. **CI/CD 仅基本配置**：仅 `publish-style-skill.yml` 发布 workflow，无 PR CI / lint / format 检查；ESLint/Prettier 无配置
3. **贡献集中度过高**：Top 贡献者占比 81%（4 名 GitHub 贡献者中 152/154 commit 来自作者），单人 side project 风险显著；一旦作者中断维护，演化难以为继
4. **模型版本飘移**：techmoon 评测指出 GPT-Image-2 模型本身在迭代，已沉淀的 prompt 模板可能在 6-12 月后失效；这是所有 prompt 资源库的固有风险
5. **法律与版权风险**：Issue #13 揭示的「第三方伪造案例混进社区」是持续威胁；尽管加了 disclaimer，但 AI 时代版权判定仍处灰色地带

## 行动建议

- **如果你要用它**: 直接 `npx skills add freestylefly/awesome-gpt-image-2 --global --all --copy` 把 Skill 装到 Claude Code / Codex / Cursor，让 Agent 在做产品图 / 信息图 / UI mockup 时自动选模板；或访问 gpt-image2.canghe.ai 手动翻案例抄作业（免费浏览 + Google 登录）
- **如果你要学它**: 重点关注 `scripts/generate-site-data.mjs`（SoT→JSON 编译链）、`agents/skills/gpt-image-2-style-library/`（独立 npm 包形态 Skill）、`supabase/migrations/202605090001_user_credits.sql` 起 12 个 migrations（Reservation Saga / unique partial index / advisory lock 实战）、`api/_lib/alipay.test.js`（白名单过滤 + 验签测试样板）
- **如果你要 fork 它**: 改进方向——（a） 接入 Midjourney v7 / Sora / Claude 多模型，跨模型工程化；（b） 把 schema 抽象成可配置（用户上传案例时自动结构化）；（c） 加 PR CI + ESLint + 前端单测；（d） 用社区贡献替代单人主导，把贡献门槛降到「PR 一个 case」级别

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录 |
| Zread.ai | https://zread.ai/freestylefly/awesome-gpt-image-2 |
| 关联论文 | 无（应用层项目） |
| 在线 Demo | https://gpt-image2.canghe.ai/（Vite + Supabase 站点，需 Google 登录） |
| Agent Skill 安装 | `npx skills add freestylefly/awesome-gpt-image-2 --global --all --copy` |

# 880 个 Codex 技能合集：800+ SaaS 自动化背后，Composio 把 awesome-list 做成 SDK 漏斗

> GitHub: https://github.com/composiohq/awesome-codex-skills

## 一句话总结

Composio 把自家 MCP 工具接入能力伪装成 880 个 Codex skill，搭出一个「awesome-list 当 SDK 营销漏斗」的双层结构：表层 17 个真旗舰技能（slack-gif-creator / mcp-builder / skill-creator / canvas-design / notion-* 等）值得抄，底层 832 个 `<x>-automation` 是 6 处字符串替换的 SaaS 包装模板，diff 几乎只有 SaaS 名不同。

## 值得关注的理由

1. **旗舰质量在线、组合稀缺**：slack-gif-creator（17KB+模板/字体库）、mcp-builder（13.5KB+reference+scripts）、skill-creator（18KB 教你从零写 skill）、webapp-testing（含 Playwright 风格 with_server.py）—— 这套「validators+primitives+evaluation harness」三层范式是社区里少数把 Codex skill 写得工程化的样本。
2. **可搬走的运营范式**：`skill-installer/scripts/install-skill-from-github.py` 一键安装 + 五场景分组 README + `brand-guidelines/` 等 Codex 平台原生 skill —— 把「awesome-list 当内容分发渠道」做成了可复用的 GitOps 流水线。
3. **生态位独特**：它是唯一把 800+ SaaS MCP 工具纳入 skill 形态的合集（覆盖广度独一档），同主题的姊妹仓 awesome-claude-skills 63.9k★ 形成 Claude+Codex 双覆盖矩阵。

## 项目展示

![Composio banner — Codex skills 合集封面](https://raw.githubusercontent.com/composiohq/awesome-codex-skills/master/codex_cover_image.png)

> Composio 自带 1280×640 品牌 banner，README 顶部即为它。

仓库目录结构（顶层 49 个目录，展开为 880 个 SKILL.md）：

```
awesome-codex-skills/
├── README.md                              # 五场景分组 + Quickstart + Contributing
├── codex_cover_image.png                  # Composio 品牌 banner (1.1MB)
├── skill-installer/                       # 一键安装 CLI
├── composio-skills/                       # ⚠ 832 个 SaaS-automation 模板 (7MB, 占 76% 文件)
├── canvas-design/                         # 旗舰: 12KB SKILL.md + 54 个 ttf 字体
├── slack-gif-creator/                     # 旗舰: 17KB + templates/primitives/core 三层
├── mcp-builder/                           # 旗舰: 13.5KB + reference/ + scripts/ + eval harness
├── skill-creator/                         # 元旗舰: 18KB, 教人写 skill 的 skill
├── theme-factory/                         # 真技能
├── notion-knowledge-capture/              # Notion 系: 中端真技能
├── notion-meeting-intelligence/
├── notion-research-documentation/
├── notion-spec-to-implementation/
├── webapp-testing/                        # 旗舰: scripts/with_server.py + 3 examples
├── brand-guidelines/
├── paperjsx/
├── email-draft-polish/
├── issue-triage/
├── ... (其余 30+ 独立真技能)
```

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/composiohq/awesome-codex-skills |
| Star / Fork | 13,402 / 1,300 |
| 代码行数 | 880 个技能 / 832 带 SaaS-automation 模板 / 10.1MB（主体 .md 95%） |
| 项目年龄 | 5 个月（2026-01 ~ 2026-05） |
| 开发阶段 | 低维护（4 月单月 67% commits，5 月断崖；已 25 天未 push） |
| 贡献模式 | 小团队（20 contributor / Top1 21% / 前 3 占 30%；Prathit 双账号） |
| 热度定位 | 大众热门（13.4k★ + 102 个新 star 24h 内爆发，但仅 6 个真实 issue） |
| 质量评级 | 策展[良好] 更新[停滞] 自动化[高] 旗舰实测 delta[N/A（缺 API 走结构分）] 裁决[marginal（仅结构判断）] 象限[scaffolding/lite] |
| 许可证 | 无 License（仓库默认未声明；awesome-list 类常见但不规范） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Composio（composiohq）是 2023-03 在美国注册的组织，bio 自述「Equips agents with well-crafted tools」。**它的核心产品是 composio SDK（28.7k★ TypeScript），给 LLM Agent 接 100+ SaaS 的认证 + 编排层**，是 MCP/tool-use 中间件赛道的头部玩家。同一组织还运营 ComposioHQ/awesome-claude-skills（63.9k★，姊妹仓）、trustclaw（822★，相邻产品）、open-chatgpt-atlas（442★，OpenAI 集成）。**这是一家典型「商业公司 → 社区生态」打法**：顶级仓是自家 SDK，次级仓是相邻产品，再下一级就是 awesome-codex-skills 这种用户引流 + skill 生态分发。

### 问题判断

Codex CLI 发布后，社区对「codex 怎么用 / 怎么给它写 skill」的需求暴增，但官方示例稀薄。Composio 看到了「开发者找 skill → 装 skill → 用 skill」的天然导流位：与其让用户自行摸索，不如直接摆出一个「开箱即用 800+ 集成」的形象，借力自家 MCP 协议把工具接入能力前置成内容资产。**时机对**：Codex CLI 5 月发布期 + Anthropic 已在 Claude Code 跑通「skill」概念，Composio 把同一概念搬到 Codex，搭便车成本极低。

### 解法哲学

策展方明确选「**数量 >> 深度**」做 awesome-list SEO：49 个顶层目录里 17 个真旗舰 + 832 个 SaaS stub 的「广度碾压」结构，让任何搜索词都能命中。**明确不做的**：（1）不写选品门槛（README 几乎只要求「skill 可被 Codex 触发」，无 benchmark / 评审流程）；（2）不做 SKILL.md 质量校验（issue #42 PaperJSX 描述的 npm 不可装，3 个月未修）；（3）不维护 PR 节奏（64 个 PR 堆着未合）。**自动化的边界**：内容侧用外部脚本批生成 composio-skills/ 下 832 个 stub（diff 仅 6 处字符串替换），但 CI/失效治理是空。

### 战略意图

**流量入口 + SDK 商业导流**：README Quickstart 直接给出 `pip install composio` + `dashboard.composio.dev` 链接，banner 图点击也跳到 dashboard 注册页。skill-installer 是统一安装入口但同时是 telemetry 收集器。整套形成「awesome-list（内容钩子）→ skill 安装（信任建立）→ composio SDK（付费 tier）」的漏斗。**不是公益策展**：它和姊妹仓 awesome-claude-skills 同属 Composio 商业矩阵，是公司级系列化运营。

## 核心价值提炼

### 创新之处

1. **「awesome-list 当 SDK 分发」的商业模式**（新颖度 4/5 × 实用性 3/5）—— 把开源自媒体内容做成付费产品的获客资产，而不是单纯引流。Composio 把 Claude + Codex 双仓矩阵化运营，是社区里第一个把这套跑通的团队。
2. **`skill-installer` CLI 一键分发**（新颖度 3/5 × 实用性 4/5）—— `install-skill-from-github.py` 让用户不用 git clone 就能把任意 skill 装到 `~/.codex/skills/`，降低试用门槛，是其他 awesome-list 仓没有的工程化组件。
3. **832 个 SaaS stub 的「广度声明」**（新颖度 2/5 × 实用性 1/5）—— 不算真创新，但作为「我支持 800+ 集成」营销素材，**效果成立**——访客看到数量级会本能信任。

### 可复用的模式与技巧

1. **「渐进披露三层」结构**：metadata（<100 词，决定 routing）→ SKILL.md body（核心指令，<5KB）→ `references/`（深内容，按触发加载）。**怎么搬走**：写自家 skill 时严格控制 SKILL.md 字节数，深内容挪 references/，references 超过 10K 词时附 grep 模式提示模型按需展开。
2. **「工具即代码」拆解**：`scripts/` 装确定性步骤（webapp-testing 的 `with_server.py` 管 Playwright 进程生命周期），模型只负责决策。**怎么搬走**：识别自己 skill 里「会被重写 >3 次的逻辑」，固化为 `scripts/x.py`；slack-gif-creator 的 validators/primitives/core 分层是更工程化的范本。
3. **「evaluation-driven authoring」**：mcp-builder 核心范式 —— **先写 3 个真实任务的 eval 用例，再设计 tool**。**怎么搬走**：写任何 skill 前先列「3 个真实用户任务」，反向逼出最小 SKILL.md，避免大而空的抽象。
4. **「双仓矩阵」系列化运营**：同一组织按 IDE/CLI 分人群（Claude Code 仓 + Codex 仓）双覆盖，互不抢流量但共享品牌资产。**怎么搬走**：自己若做多语言/多框架教程，按生态分仓而非一锅烩，README 互相 cross-link。

### 关键设计决策

- **数量 vs 深度的取舍**：选数量让搜索 SEO 占优，但 832 stub 稀释了 17 旗舰信号、维护成本不可持续。**Trade-off**：4.8 月龄 + 25 天未 push + 64 PR 堆着，说明「数量 + 自动化签名」没解决根本策展治理。
- **README 五场景分组**：Development & Code Tools / Productivity & Collaboration / Communication & Writing / Data & Analysis / Meta & Utilities —— 分类清晰但 composio-skills/ 不参与这套分组（平铺），暴露「真旗舰 + 营销矩阵」两套组织逻辑混搭。
- **默认分支 master**：少见（主流是 main），可能是 fork 自 Anthropic 模板时遗留，无技术理由。
- **不写 License**：awesome-list 类常见但不规范，外部 fork 后再分发时会有授权灰色地带。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | 本仓 awesome-codex-skills | awesome-claude-skills（姊妹） | ui-ux-pro-max-skill | graphify | awesome-codex-cli |
|------|---------|--------|--------|--------|--------|
| Stars | 13,402 | 63,900 | 89,000 | 64,000 | 200+ |
| 收录数 | 880 SKILL.md | 数百 skill | 1 个超深 skill | 1 个多端 skill | 200+ CLI 工具 |
| 旗舰深度 | 中端真技能 ~17 个 | 跨度更大，Anthropic 官方同源 | 极深 | 深 | 浅 |
| 自动化签名 | 高（832 stub 批生成） | 中 | 低（单技能） | 低（单技能） | 中 |
| 商业属性 | 强（Composio SDK 导流） | 强（同上） | 个人创作者 | 个人创作者 | 独立策展人 |
| 维护活跃度 | 已停滞（25 天未 push） | 活跃 | 活跃 | 活跃 | 低频 |
| 一键安装 CLI | 有（skill-installer） | 无 | 无 | 无 | 无 |

### 差异化护城河

1. **覆盖广度独一档**：唯一把 800+ SaaS MCP 工具纳入 skill 形态的合集，awesome-claude-skills 也走类似路线但 Codex 仓更激进。
2. **`skill-installer` CLI**：其它仓要 git clone，本仓支持任意 GitHub 仓库的 skill 一键安装，工程化组件领先。
3. **Codex 平台原生绑定**：`brand-guidelines/`、`agent-deep-links/` 等是 Codex CLI 紧绑的入口技能，离开 Codex 生态就没价值——但反向看，**Codex 用户没有替代选项**。

### 竞争风险

- **Anthropic 官方 skills 协议扩张**：Claude Code 的 skill 是事实标准母体，若 Anthropic 推出官方 Codex 兼容层，本仓的 832 stub 会被官方 marketplace 替代。
- **Codex 模型升级内建 tool-use**：GPT-5 之后若 Codex 把 SaaS 工具调用内建化，832 stub 的价值归零。
- **awesome-codex-cli 等「轻量级 + 高质量」竞品**：互补但若分流社区贡献者，本仓的「17 旗舰」会出现维护断档。
- **单点依赖 Composio SaaS**：所有 composio-skills/ stub 绑 RUBE MCP 协议，上游 SaaS 改名/限流即崩。

### 生态定位

**工具箱型分发平台，非标准制定者**。Codex 官方 skill 协议才是事实标准，本仓是「协议的最大非官方合集」，填补「用户想找现成 skill」的发现层。商业上是 Composio SDK 的市场部资产，技术上是 Codex 生态最丰富的 skill 样本库。

## 套利机会分析

- **信息差**: **中高估低估并存**。社区普遍把 13.4k★ 解读为「质量背书」，但 98% 文件是机械模板；少数人知道「17 旗舰才是真价值」并能正确迁移模式。
- **技术借鉴**: 「awesome-list + skill 模板 + installer CLI」组合工程范式可迁移 —— PR-bot 自动校验 SKILL.md schema + description 长度上限 + 提交门槛脚本（issue #77 已暗示质量压力）。
- **生态位**: Codex 平台官方合作伙伴（OpenAI 推过 banner），但 Anthropic Claude 才是 skill 协议母体 —— 长期看是「搭便车者」，护城河弱。
- **趋势判断**: **模型变强后 stub 价值归零**，真旗舰价值反而升（prompt-cache + 长上下文能容纳 references/）。4 月爆发 5 月断崖暗示热度依赖 Codex CLI 发布期，后期会更依赖社区 PR 节奏。

## 风险与不足

- **832 stub 不可持续**：diff 仅 6 处字符串替换的模板构成 95% 体积，Codex 模型升级后基本归零；4.8 月龄 + 25 天未 push + 64 PR 堆着 = 维护期早期信号。
- **质量审计缺位**：issue #42 PaperJSX 不可装、issue #46 README UX 杂乱、issue #1 install-skill destination path bug —— 暴露「quickstart 一键安装」宣传与现实落差。
- **零社区运营**：6 个真实 issue vs 13.4k★ 的比例（1:2233）极低，PR 64 个堆着，多数是收录请求而非实质贡献。
- **license 缺失**：未声明协议意味着下游 fork / 再分发时授权不明，外部企业用有合规风险。
- **stub 撑爆触发上下文**：832 个 SKILL.md 的 description 加起来可能撑爆 Codex 触发判定阶段的上下文窗口，实际可用性存疑。
- **关键人依赖**：Top1=Prathit 占 21%，双账号（Prathit14 + Prathit-tech），若离职策展节奏会断崖。

## 行动建议

- **如果你要用它**：**只装 5 个真旗舰** —— `slack-gif-creator`、`mcp-builder`、`skill-creator`、`webapp-testing`、`paperjsx`，跳过 `composio-skills/` 全部 832 条目。配套姊妹仓 `awesome-claude-skills`（63.9k★）补 Claude Code 生态。
- **如果你要学它**：**学 skill-creator 当 README 范本**（教你从零写 skill，conciseness 是核心原则），再学 slack-gif-creator 的 validators/primitives/core 三层拆分。不学「832 stub + 营销漏斗」的商业模式（不适合公益项目）。
- **如果你要 fork / 复刻它**：
  1. 把 832 stub 删到 ≤100 精选；
  2. 加 `star 数 + description 长度 + scripts/reference/assets 存在性` 静态分析自动校验；
  3. 把 README 五场景分组下放到每个 dir 一级分类（解决 17 旗舰 vs 832 stub 组织逻辑混搭）；
  4. 加显式 License（MIT/CC-BY-SA）+ Contributing 门槛脚本（schema 校验 SKILL.md frontmatter）。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录 |
| Zread.ai | 未收录 |
| 姊妹/同类项目 | [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)（63.9k★，Claude Code 生态姊妹仓）/ [ComposioHQ/composio](https://github.com/ComposioHQ/composio)（28.7k★，SDK 商业闭环） |
| 关联论文 | 无 |
| 在线 Demo / 站点 | [dashboard.composio.dev](https://dashboard.composio.dev)（商业 SDK 试用入口） |
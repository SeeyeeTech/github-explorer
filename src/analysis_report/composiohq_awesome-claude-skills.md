# GitHub推荐：Composio 把 1000+ Claude Skills 收入一个仓库：用「Marketplace + 832 个 Rube 自动化模板」做 Agent 工具集成时代的目录入口

> GitHub: https://github.com/composiohq/awesome-claude-skills

## 一句话总结

`awesome-claude-skills` 是 Composio（Agent 工具集成平台）接管的「Claude Skills 超级目录」——表面上是 awesome-list 风格的技能聚合，实际是「**官方 skills 集 + 自研社区 skills 集 + 832 个 Rube MCP 自动化模板**」三层混编的复合仓库，把 Anthropic 在 2025-10 推出的开放 Skills 标准接成 Composio 的 SaaS 工具集成落地页。它最重要的差异化设计是把每个第三方 SaaS（Slack/Notion/Salesforce/HubSpot）都做成独立 skill 包，用 **manifest 数组 + Rube MCP 远程工具发现** 把 832 个工具包用同一份模板生成、再用 `.claude-plugin/marketplace.json` 暴露给 Claude Code 插件系统——一个对 Anthropic 上游 skill 标准的「**Composio 风格规模化实现**」。

## 值得关注的理由

1. **「awesome-list + 自研 skill 集合 + SaaS MCP 模板工厂」三层混编形态本身罕见**：根目录聚合 Anthropic 官方 + 社区的引用式 skills（如 `brand-guidelines`、`slack-gif-creator` 只是 README 里的链接指针，真实内容在 `composio-skills/` 同名子目录）；`composio-skills/` 用 schema 化的 marketplace 模式承载 107 个高质量 skill；`composio-skills/composio-skills/` 子目录用**完全相同的模板** 生成 832 个第三方 SaaS 自动化 skill。这是一个「awesome 收录 + 自营 marketplace + 程序化生成第三方 skills」三层一体的形态，比单一 awesome-list 复杂一个数量级。
2. **832 个 SaaS skill = 「Rube MCP 远程工具发现」的标准模板**：每个 `-automation` 子目录只含一个 `SKILL.md`（~3KB），统一走 `requires.mcp: [rube]` + 「先 `RUBE_SEARCH_TOOLS` → 再 `RUBE_MANAGE_CONNECTIONS` → 再 `RUBE_EXECUTE_TOOL`」三段式工作流。这是「**不绑死具体工具 schema，用 MCP 远程发现获得通用性**」的规模化设计：新增一个 SaaS 只需要几分钟而非几天，且 schema 升级无需改动 skill。
3. **`marketplace.json` 是 Anthropic 插件标准的「官方级实现」**：根目录 `composio-skills/.claude-plugin/marketplace.json`（v2.0.0）声明 107 个 plugin，平均 80 字符 description 字段，category 字段做归类（productivity/devops/development 等 20 类）。这是 Composio 给 Anthropic 插件 marketplace 标准提交的「**生产级样品**」——任何想用 marketplace 分发自家 skills 的厂商都可以直接参考它的 schema 与目录布局。
4. **「Awesome Claude Skills」项目治理本身**值得收录作参考：一个 `label-ready-skill.yml` 工作流用 7 条规则（仅 README 改、限定 Skills 段、必须外链 URL、必须非 Composio/Anthropic 域名、禁 crypto/web3 关键词、必须按字母顺序、必须以 bullet 形式新增 skill）自动审核 PR，并自动打 `ready-to-merge` 标签——这是「**awesome-list 维护机械化**」的样板，**专治「awesome-list 接 PR 后慢慢走样」的经典管理难题**。

## 项目展示

### 三层目录结构

```
awesome-claude-skills/
├── (根级 awesome-list 收录)  ← README.md 里的 bullet 链接，物理上散落在仓库内
│   ├── brand-guidelines/             # 真实文件夹 + 真实 SKILL.md
│   ├── slack-gif-creator/            # 真实文件夹
│   ├── document-skills/{docx,pdf,pptx,xlsx}/  # 自带 ooxml/ 与 scripts/
│   ├── skill-creator/ + scripts/{init,package,quick_validate}.py
│   ├── mcp-builder/ + webapp-testing/ + artifacts-builder/
│   └── ... (~33 个真实 skill 子目录)
│
├── connect-apps-plugin/              # Claude Code 插件主体（plugin.json + skills）
│
└── composio-skills/                  # 自家 marketplace
    ├── .claude-plugin/marketplace.json  # 107 个 plugin、20 个 category、v2.0.0
    ├── connect/{,apps}/              # 入口 wrapper skill
    ├── connect-apps-plugin/          # 嵌套 connect 入口
    ├── {27 个 curated skill}/         # brand-guidelines / docx-jr / ...
    └── composio-skills/              # 子目录：又一层 marketplace ← 子目录里再嵌 marketplace？
        └── -21risk-automation/        # 832 个 SaaS 模板子目录之一
            └── SKILL.md (~3KB)
```

### 根目录 README 的「Quickstart: Connect Claude to 500+ Apps」

README 头 30% 是「接通 Slack + Gmail + Jira 的 3 步教程」(`claude --plugin-dir ./connect-apps-plugin` → `/connect-apps:setup` 拿 API key → 重启)——**这不是 awesome-list 写法**，是 product-led growth 引导。把「awesome-list」做成「awesome-list 形态的安装教程」，让 star / fork 的开发者直接走到 Composio dashboard，是这套仓库最深刻的营销设计。

### 832 个自动化 skill 的模板共性

抽样 `composio-skills/composio-skills/slackbot-automation/SKILL.md`（2.9 KB）：全部共享下面的骨架：

```yaml
---
name: <saas>-automation
description: "Automate <SaaS> tasks via Rube MCP (Composio). Always search tools first for current schemas."
requires:
  mcp: [rube]
---
# <SaaS> Automation via Rube MCP

## Prerequisites
- Rube MCP must be connected
- Active <SaaS> connection via RUBE_MANAGE_CONNECTIONS with toolkit <saas>
- Always call RUBE_SEARCH_TOOLS first

## Setup
1. RUBE_SEARCH_TOOLS ← 拉当前 schema
2. RUBE_MANAGE_CONNECTIONS toolkit=<saas> ← 确认连接 ACTIVE
3. RUBE_EXECUTE_TOOL ← 执行

## Known Pitfalls
- ...
```

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/composiohq/awesome-claude-skills |
| Star / Fork / Watcher | 68,722 / 7,801 / 430 |
| 代码规模（tokei） | 13,543 行代码 + 71,292 行注释（注释密度高，文档型资产占主导）；1,005 个文件 |
| 语言分布 | Python 91.4%（12,381 行 / 62 文件）、JavaScript 6.0%、Shell 2.3%、XML 0.3% |
| 代码/注释比 | 1:5.26（SKILL.md / README 等文档占绝对主导） |
| 子目录构成 | 根 33 个真 skill + `composio-skills/` 107 个 marketplace plugin + `composio-skills/composio-skills/` 832 个 SaaS 自动化 |
| 话题标签 | claude, claude-code, agent-skills, ai-agents, antigravity, automation, codex, composio, cursor, gemini-cli, mcp, rube, saas, skill, workflow-automation, developer-tools, openai-codex |
| License | 未声明（README 标注） |
| 创建时间 | 2025-10-17 | 最近推送 | 2026-05-22（近 2 个月无新增 commit） |
| 开发主导 | Prat011（36/75≈48% 主仓 commit；公司主力维护），SohamGanatra、Composio 团队多人协维 |
| 项目年龄 | 9.1 个月（首次提交 2025-10-17） |
| 投入权重 | 高（公司官方仓库，但近 60 天活跃度明显下降） |
| 贡献集中度 | 小团队（31 位贡献者，头部 33%） |
| 总 commit 数 | 75（近 30 天 0、近 90 天 20） |
| 开发阶段 | 稳定维护（社区驱动期，主仓直推放缓） |
| 开发模式 | 职业项目（Composio 公司运营；周末占比 12%，深夜占比 21.3%） |
| Open Issues / Open PRs | 125 / 945（社区持续涌入新提案） |
| 版本策略 | 无 tag、无 release（内容驱动型而非软件工程型） |

## 作者视角：Composio 为什么做这个仓库

### 问题发现

Composio 是做「**AI Agent 的工具集成与认证层**」的 SaaS ——其核心定位是让任何 Agent 客户端（MCP / Claude Code / Cursor / Codex / Gemini CLI / Antigravity）能调用 1000+ 第三方 API，并托管 OAuth / 鉴权。在 2025-10 Anthropic 推出 Skills 开放标准之后，Composio 看到了一件事：**Skills 才是 Agent 时代最高密度的「行为/工作流」载体**，比 MCP（连接）和 tools（动作）加起来都更接近用户的真实需求——

> Skills 是「工作流」，MCP 是「连接」，tools 是「动作」。生产环境三者并行：MCP 处理访问、tools 处理动作、skills 处理行为（README §"What Are Claude Skills?" 直接抄了这段叙事）。

所以 Composio 要解决的问题是：**怎么让 1000+ SaaS 集成不是「API 调用清单」，而是「可被 Claude 理解的工作流 skill」**？

### 解法哲学

Composio 选了「**awesome-list 作为入口 + Rube MCP 作为统一后端**」的路子，原因有三：

1. **不抢「skills 创作平台」的位**：Anthropic 自己有官方 skills 仓（60.9k star），Composio 做「收录 + 增量 + 模板化生产」比做「第二官方仓」更明智。Composio 是 agent-tool-integration 起家，不是 prompt engineering 起家，强行做通用 skill 创作平台与公司基因不匹配。
2. **用 Rube MCP 把「整合复杂度」从客户端下沉到服务端**：让每个 skill 模板只承担「**怎么调用**」的元工作流（搜索工具 → 管理连接 → 执行），而具体每个 SaaS 的 schema 变化、鉴权策略、速率限制全部由 Rube MCP 在线给出。这是「**让 832 个 skill 共用一个模板**」成为可能的关键。
3. **awesome-list 形态是天然的开发者漏斗**：根目录 README 30% 是「3 步接通 500+ App」教程，每个 `connect-apps` skill 的 description 都含「Inspired by」「Credit」属性，吸引真实社区贡献。这种「**awesome 形态 + 营销形态 + 教程形态**」三层合一，是 Composio 用 awesome-list 范式做运营的最佳范例。

### 背景知识迁移

从工具集成领域带来的核心 insight：

- **「凭证管理 + 鉴权 + 重试 + schema 漂移」是 SaaS 集成的 4 大痛点**，Rube MCP 把它们做掉，让每个 skill 模板能写得极简。
- **「schema 文档不会写」**：每个 SaaS API 的官方文档对人类友好，对 LLM 不友好。Rube MCP 把 schema 翻译成 LLM-friendly 的 `RUBE_SEARCH_TOOLS` 响应（不仅返回 schema，还返回「执行计划 + 已知陷阱」），这才是 832 个 skill 能「远看都是同一份模板」的根本原因。
- **「OAuth 在 Agent 时代变成一等公民」**：Composio 把 OAuth 流做成 MCP 协议层，让客户开发者不再关心 refresh token / scope 协商。在 skill 模板里体现为 `RUBE_MANAGE_CONNECTIONS` 这一步。

### 战略图景

在 Composio 公司的整体定位：

```
ComposioHQ/
├── composio (29k star)             # SDK + Server：API 网关与核心
├── awesome-claude-skills (本仓库)   # 入口：awesome 形态 + skills 模板工厂 ← 现在所在
├── rube MCP (composio.dev/rube)     # 运行时：MCP 服务，把 1000+ SaaS 工具暴露给 Agent
└── docs / dashboard                 # 商业化：开发者控制台 + API key 发放
```

`awesome-claude-skills` 是**漏斗的顶部**：awesome-list 形态带来 star / fork / 教程曝光，每个 sub-skill 把开发者导向 Rube MCP 注册 → API key → 付费 tier。**这就是「awesome-list 作为营销渠道」的最经典实现**。

## 核心价值提炼

> 诚实区分：awesome-list + skill 集合本身不是创新（anthropics/skills、hesreallyhim/awesome-claude-code 都做了）。本仓库的差异化在于 **三层混编形态** + **Rube MCP 模板化生产** + **marketplace.json 标准实现** + **自动化审核 workflow** 这四件事，下面分别拆。

### 创新之处

1. **「awesome-list + 自研 marketplace + 第三方模板生成」三层混编架构**（新颖度 5/5，实用性 4/5，可迁移性 4/5）：
   - 根目录：awesome-list 式收录（README bullet 链 + 真实子目录）
   - `composio-skills/`：高质量 curated marketplace（marketplace.json v2.0.0 + 107 个 plugin）
   - `composio-skills/composio-skills/`：832 个程序化生成的第三方 SaaS skill
   每层各承担不同职能：awesome 收流量、marketplace 树品牌、模板子目录做规模化。**这种「一个 git repo 三层各司其职」的设计对任何「既想做平台又想做目录」的项目都直接可学**。

2. **「Rube MCP 远程工具发现 + 单模板复刻 832 个 skill」规模化设计**（新颖度 5/5，实用性 5/5，可迁移性 5/5，全项目最硬核）：
   - 832 个 `-automation` 目录共享同一份 ~3KB SKILL.md 骨架：`requires.mcp: [rube]` + 三段式工作流（RUBE_SEARCH_TOOLS → RUBE_MANAGE_CONNECTIONS → RUBE_EXECUTE_TOOL）。
   - **零字节冗余代码**：每个目录只有 SKILL.md，没有 `scripts/`、`references/`、`assets/`，因为运行时按需 remote 调用。
   - **schema 升级无需改动**：SaaS 厂商改 API 后只需更新 Rube MCP 端，skill 模板永久不变。
   - 这是「**「技能 + 工具分离」架构的教科书级实现**」——任何需要给 N 个外部系统做集成的项目，都应该照抄这个模式（一个 host MCP + 一份模板 skeleton + N 个空 skill 包）。

3. **`marketplace.json` 作为 Anthropic 插件标准的「官方级实现」**（新颖度 3/5，实用性 4/5，可迁移性 5/5）：
   - 顶层 schema：`$schema` 引用 Anthropic 官方 schema + `name` + `version`（语义化） + `owner`（name + email）+ `plugins` 数组。
   - 每个 plugin 字段：`name` + `description`（~80 字符）+ `source`（相对路径）+ `category`（从 20 个枚举值取）。
   - 通过类别枚举让 UI / 检索 / 安装器能分组，比「扔文件夹让人自己看」规范得多。**任何想用 Anthropic marketplace 分发自家 skill 的厂商都可以直接拿这个 marketplace.json 做模板**。

4. **`.github/workflows/label-ready-skill.yml` 自动化审核 7 规则**（新颖度 4/5，实用性 5/5，可迁移性 5/5）：
   - ① 仅允许 `README.md` 改动（拒绝曲线 PR）
   - ② 仅在 `## Skills` 到 `## Getting Started` 之间插入（拒绝散点编辑）
   - ③ 必须以 bullet `- [<name>](<url>)` 形式新增
   - ④ URL 必须外链（黑名单 composio.dev / anthropic.com）
   - ⑤ 禁用 crypto / web3 / blockchain / nft / defi / solana / ethereum / bitcoin 等关键词（自洁）
   - ⑥ 按字母顺序插入到所属 category
   - ⑦ 通过 → 自动打 `ready-to-merge` 标签
   用 GitHub Action + Node 一次性脚本实现 7 规则，零外部依赖，**专治「awesome-list PR 走样」的经典老大难**。

5. **`document-skills/` 自带安全处理**：docx/pptx 用 `defusedxml.minidom` 防御 XXE（已是最佳实践）；但 **`unpack.py` 与 `document.py` 用裸 `zipfile.extractall` 没做 Zip Slip 防护**（issue #329 报告但未修）——这是反例，提醒「**awesome 标准文档技能 ≠ 安全正确性**」。详见风险章节。

6. **`skill-creator/` 引导式创作元 skill**（新颖度 3/5，可迁移性 5/5）：
   - 「Progressive Disclosure 三级加载」明示写在 SKILL.md 里：① 总是 in-context 的 (~100 words) metadata；② skill 触发时按需加载的 (<5k words) body；③ 按需加载的(unlimited) scripts/references/assets。
   - 配套 `init_skill.py` + `package_skill.py` + `quick_validate.py` 三件套，一行命令 `init_skill.py <name> --path skills/public` 就能产出合规 skill。
   - **把「Skill 创作规范」做成可执行工具链，而不是写死在 README**——这是「**文档即代码**」的标志性工程实践。

### 可复用的模式与技巧

- **「Rube MCP + 单模板复刻 N 个 skill」的子目录工厂**：把客户端复杂度交给 MCP 运行时，skill 模板固定极简骨架，任何「N 个外部系统集成」项目都该学的范式。
- **`marketplace.json` 三段式 schema（顶层元信息 + 引用外 schema + 数组化 plugins）**：Anthropic 插件格式的最小合规实现。
- **`label-ready-skill.yml` 7 规则审核**：awesome-list 自动维护的样板，可改学用任何「目录型仓库」。
- **`quick_validate.py` 前置校验器在 `package_skill.py` 里调用**：先校验后打包，零依赖、强约束。
- **`defusedxml` + 显式声明 License/requires**：每个 skill 都自含 license 字段，第三方复制风险可控。
- **`init_skill.py` 在 SKILL.md 模板里嵌入 4 种结构选择引导**（Workflow-Based / Task-Based / Reference-Based / Capabilities-Based）：文档系统地把 skill 的「结构选择」做成可选项，**专治「skill 写出来不像 skill 像一坨备忘录」**。

### 关键设计决策

> 格式：**决策 / 问题 / 方案 / Trade-off / 可迁移性**

#### 决策 1：awesome-list 与 marketplace 并存

- **问题**：Composio 要做 Skills 入口，但 Anthropic 自己有官方仓，再做一个 awesome-list 显得同质化；只做 marketplace 又会丢失 awesome-list 的 SEO / discoverability 价值。
- **方案**：根目录负责 awesome-list 收录（README bullet + 真实子目录），`composio-skills/` 子目录负责 marketplace 自营，**awesome 收流量 + marketplace 树品牌**。
- **Trade-off**：双目录意味着贡献者要决定「这个 skill 放根还是放 `composio-skills/`」，boundary 模糊；对新人贡献 friction。
- **可迁移性**：任何「既想做平台又想做目录」的项目都适用（Notion 模板库、Cursor 规则库、Raycast 扩展库）。

#### 决策 2：用 Rube MCP 而非本地 scripts 承载 832 个 SaaS

- **问题**：每给一个 SaaS 写本地 `scripts/api_call.py`，意味着 commit lock-step + API schema 漂移后要 re-author；N=832 时维护负担不可能。
- **方案**：把 `tools/schema/auth` 全部下沉到 Rube MCP 运行时；skill 模板只剩「远程调用三段式」10 行核心指令。
- **Trade-off**：依赖 Composio 持续运营 Rube MCP（issue #834「Rube 停更」就是典型风险）；一旦后端不可用，832 个 skill 集体失效。
- **可迁移性**：SaaS / Agent-integration / IDE-extension 类项目都可借鉴——**「客户端永远极简，业务复杂度下沉到服务端」是 LLM 时代的硬规律**。

#### 决策 3：`requires.mcp: [rube]` 在 frontmatter 里而非 SKILL.md body

- **问题**：MCP 依赖是 skill 触发的前置，不是「用户已经 chat 到一半才补的」。
- **方案**：YAML frontmatter 加 `requires.mcp: [rube]`，**Agent 客户端启动时就检查依赖、未满足就静默跳过**。
- **Trade-off**：YAML 里多了非标准字段（`requires.mcp` 还未被 Anthropic skill spec 显式纳入），部分老客户端可能不识别。
- **可迁移性**：适合所有「需要外部资源才生效」的 skill（如 database skill 声明 `requires: postgres`、api skill 声明 `requires: api_key`）。

#### 决策 4：贡献流程「只能改 README」

- **问题**：awesome-list 维护最痛的事是 PR 复杂、合并后走样。
- **方案**：CI 把贡献限制在「只能改 README.md 的 `## Skills` 段」+「bullet 必须外链」+「按字母顺序」+「禁黑关键词」。
- **Trade-off**：贡献者无法提交新 skill 文件夹（必须开第二个 PR），降低 friction；**但 awesome-list 形态本就是引用式收录，子目录另开 PR 是正确解耦**。
- **可迁移性**：所有 awesome-list 维护者都该学这个限制——把 awesome-list 限定为「链接策展」、把真贡献限定为另一个流程。

#### 决策 5：`marketplace.json` 用相对路径而非 URL

- **问题**：plugin source 字段如果用 URL，会让 marketplace 收外部 skill、控制权外泄；用相对路径强制「skill 必须落在本仓子目录」。
- **方案**：`source: ./brand-guidelines`、`source: ./competitive-ads-extractor` 这种仓库内相对引用。
- **Trade-off**：marketplace 没法做 mono-repo「跨仓库聚合」；要扩 marketplace 必须重写所有 source。
- **可迁移性**：适合所有「marketplace 必须自营 / 内容自检」场景；不适合「大集市型」聚合（vs npm registry）。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | composio/awesome-claude-skills | anthropics/skills | anthropics/claude-plugins-official | obra/superpowers | hesreallyhim/awesome-claude-code |
|---|---|---|---|---|---|
| Star | 68.7k | 60.9k | n/a | 大 | 50.6k |
| 内容数量 | 970+ skill | 官方 16 个 | n/a | 一组 | awesome 收录 |
| 平台方向 | 自家 marketplace + 模板工厂 | 官方标准实现 | 官方插件目录 | 软件工程 skill 套装 | awesome 纯收录 |
| 与 MCP 的关系 | 832 个 skill 强绑 Rube MCP | 无 | 无 | 无 | 无 |
| 商业模式 | 漏斗到 Composio 付费 | 无 | 无 | 无 | 无 |
| Anthropic 官方认可 | 收录进 awesome-claude-code 等清单 | 是 | 是 | 否 | 是 |
| 自动化审核 | 7 规则 CI（label-ready-skill.yml） | 无 | 无 | 无 | 无 |

### 差异化护城河

- **「awesome + marketplace + 模板工厂」三层混编**：anthropics/skills 只有「标准实现」一层、hesreallyhim/awesome-claude-code 只有「awesome 收录」一层、obra/superpowers 只有「套装」一层，**三层一体的形态目前只有本仓**。
- **规模化能力（970 skill）vs 同类（16~50）**：靠 Rube MCP 远程发现把 schema 漂移问题甩到运行时，**这是别的仓做不到的根本原因——别人没有 Rube 这个 host**。
- **Anthropic 插件 marketplace 标准实现的样品**：任何想用 marketplace.json 分发 skills 的厂商都该来参考这个仓里的 v2.0.0 marketplace.json。

### 竞争风险

- **Rube MCP 停更 = 832 个 skill 集体失效**（issue #834 已经提示这个信号）；如果上游 Rube 改收费 / 改产品策略，本仓从「awesome」瞬间变「awesome-but-broken」。
- **`composio-skills/composio-skills/` 子目录套娃**：嵌套 marketplace 在长尾 skill 间不易导航；新开发者初次接触时容易迷失。
- **`document-skills/` 的安全反例**：打包脚本 `unpack.py` 仍用裸 `zipfile.extractall`（Zip Slip 风险，issue #329 报告但未修复）。
- **awesome 子目录 vs marketplace 子目录的判定模糊**：贡献者首次参与时要在两层间做选择，文档没说清楚。

### 生态定位

**「Agent 时代工具集成层的事实标准入口」之一**：与 anthropics/skills（标准制定者）、hesreallyhim/awesome-claude-code（同类 awesome）形成「**Anthropic 制定标准 + 社区整理 + Composio 规模化**」的三方分工。Composio 的护城河不在 skill 标准本身、而在「**如何借助 skill 这个新载体把 1000+ SaaS 集成规模化**」。

## 套利机会分析

- **信息差**：「awesome-list 形 + 832 个 skill 量」的规模感在普通读者眼里就是「Composer 是行业头部」；技术受众会追问「怎么做到的」，可写「**为什么 awesome-list 也能规模化到 1000**」+「**Rube MCP 模板工厂的工程深度**」两条角度。
- **技术借鉴**：
  - 「awesome + marketplace + 模板工厂」三层混编架构（任何「平台+目录」项目）
  - 「Rube MCP + 单模板复刻 N 个 skill」的子目录工厂模式
  - `label-ready-skill.yml` 7 规则审核（awesome-list 维护机械化）
  - `skill-creator` 的 progressive disclosure 设计（任何 LLM 上下文敏感的项目）
  - `defusedxml` 显式使用（XML 解析项目安全起点）
- **生态位**：Agent 时代「工具 + skill 双层栈」的事实目录入口。
- **趋势判断**：踩在「Anthropic skills 成为开放标准 + Agent 工具集成需求爆炸 + Composio SaaS 化稳定运营」三重利好上；最大变量是 Rube MCP 本身的产品策略稳定性。

## 风险与不足

- **Rube MCP 单一依赖**：832 个 skill 强绑 Rube MCP，#834「Rube 停更」已经是早期信号；一旦后端策略变化整个 `composio-skills/composio-skills/` 集体失效。
- **`document-skills/{docx,pptx,xlsx}/ooxml/scripts/unpack.py` Zip Slip / XXE 风险**：用裸 `zipfile.ZipFile(input_file).extractall(output_path)` 没有 `path.resolve()` 校验，恶意 .docx 可越权写文件（issue #329 已报）。同样是 `document-skills/docx/scripts/document.py` 也没做 safe extraction。
- **`document-skills/docx/SKILL.md` 第 59/68/116 行强制要求读完整文件**：~500-600 行的 docx-js.md / ooxml.md，**让 docx skill 每次触发都要塞 ~6k token 进上下文**——违背 skill 设计的 progressive disclosure 原则。
- **`composio-skills/composio-skills/` 832 个同名子目录套娃**：用户首次浏览可能找不到入口，README 也没明确指出哪一层是 marketplace。
- **awesome 与 marketplace 边界模糊**：根 README 把 33 个真实子目录 + 19 个外部链接混着列，没说「贡献流程是先发子目录还是先发 PR」。
- **`server helper can deadlock`**（issue #713）：`unpack.py`/`pack.py` 用 `subprocess.run(..., timeout=10)` 阻塞等待 soffice 转换，**对大文档会触发 10s 超时、文档生成失败**——这个 bug 修了，但更高层面「subprocess 卡 Claude skill 流程」是普遍问题。
- **金融合规垂直延展信号**（issue #1054 用户提议 fsi-compliance-checker）：社区已经在向「金融/医疗/法务」等垂直行业 skills 自主提需求，Composio 接收态度开放——这是「**awesome-list 形态对垂直行业扩展**」的早期信号，**适合做行业 skill 套装（compliance / clinical / legal）的早期套利**。
- **打包方案营销套路**（issue #369 自荐「AI Coding Kit — 15 production-tested skills + 10 hooks for 8 stacks」）：暴露 Composio 倾向接收「**打包 hooks + 跨栈**」型方案而非单 skill——意味贡献要遵循「**套装化、可观测、跨客户端**」的复合维度，单纯提交一个独立 skill 价值低。
- **「Inspired by」「Credit」属性滥用风险**：awesome-list 形态对原创声明要求高；目前 README 给每个 skill 都加了 Inspired by，没有自动化校验。

## 行动建议

### 如果你要用它 / 学它 / fork 它

- **要发现 Anthropic skill 标准**：直接看根目录 `brand-guidelines/`、`slack-gif-creator/`、`document-skills/docx/SKILL.md`——这是 Anthropic 设计 philosophy 的范本。
- **要看 marketplace.json 落地样式**：`composio-skills/.claude-plugin/marketplace.json`（107 plugins、20 category、v2.0.0）—— 这是 Anthropic marketplace 标准的官方级实现样品。
- **要学「awesome-list + marketplace」混编**：直接拉本仓对比 `composio-skills/README.md` 与根 `README.md`，看「**两边都用 awesome-list 形态但承担不同角色**」的设计权衡。
- **要学模板规模化**：精读 `composio-skills/composio-skills/slackbot-automation/SKILL.md` 与 `connect/automation-steps`——这是「**N 个外部集成 → 单模板 + 远程 runtime**」的范式骨架。
- **要改造自动审核**：`label-ready-skill.yml` 直接 copy 到自家 awesome-list 仓里改 hostname 黑名单和禁关键词清单即可，零依赖。
- **要 fork / 贡献**：marketplace 子目录按 plugin slug 命名约定走；提交流程分两条线（根 README 改 bullet 用 label-ready workflow + 新 skill 文件夹走标准 PR）。

### 知识入口

| 资源 | 链接 |
|------|------|
| 仓库 README | https://github.com/composiohq/awesome-claude-skills （含 Quickstart 三步教程） |
| marketplace.json | https://github.com/composiohq/awesome-claude-skills/blob/main/composio-skills/.claude-plugin/marketplace.json |
| skill-creator（设计参照） | https://github.com/composiohq/awesome-claude-skills/tree/main/skill-creator |
| 关联仓库 | https://github.com/ComposioHQ/composio （SDK + Server）；https://composio.dev/rube （Rube MCP） |
| 体系入口 | https://seeyeetech.com/github-explorer/（本公众号目录索引） |

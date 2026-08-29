# GitHub 推荐：4.5 个月 31K stars：archify 用「拒绝自动布局」杀死 Mermaid 在 Agent 时代的统治

> GitHub: https://github.com/tt-a1i/archify

## 一句话总结
archify 是一个 Agent-native 的「架构图即代码」Skill —— 让 LLM 把口语化架构描述直接编译成可交付、自包含、可版本对比的单文件 HTML 架构图，并通过 fail-closed 的工程语义校验防止 AI 编造架构故事。

## 值得关注的理由
- **30,996 stars / 1,930 forks / 17 releases** —— 4.5 个月内达到这个量级，是 Agent Skill 赛道的现象级项目；同层竞品（quasar-graph / archmap / agentify / interactive-architecture）均 < 10 stars。
- **护城河在「信任层」而非渲染层**：自建 typed JSON IR + 五个原生渲染器 + Architecture Delta 版本对比 + Engineering Profile 部署语义校验 + Repository Evidence git 证据，这是 Mermaid 永远做不到的——Mermaid 不掌握语义层。
- **工程纪律堪称 Agent 工具的标杆**：零运行时依赖、ajv standalone 编译期校验器、CI 矩阵覆盖 Node 18/20/22/24 × 三 OS、atomic rename-as-commit 发布闸门。

## 项目展示

![archify hero](https://raw.githubusercontent.com/tt-a1i/archify/main/docs/assets/archify-readme-hero.png)
*产品主预览：5 类图型 + 4 套预设主题的浓缩展示*

![mco runtime share card](https://raw.githubusercontent.com/tt-a1i/archify/main/docs/assets/mco-runtime-share-card.png)
*真实仓库 mco-org/mco 的运行时架构 —— 证明能分析生产级代码库而非 toy example*

![archify demo story](https://raw.githubusercontent.com/tt-a1i/archify/main/docs/assets/archify-demo-story.png)
*Agent workflow 引导式 chapter 播放 —— 区别于静态图工具的「语义相机 + 路径感知叙事」*

![architecture delta proof](https://raw.githubusercontent.com/tt-a1i/archify/main/docs/assets/architecture-delta-proof.jpg)
*Architecture Delta：Before / Delta / After 三栏 —— 唯一竞品缺失的「架构版本对比」能力可视化*

![archify route share card](https://raw.githubusercontent.com/tt-a1i/archify/main/docs/assets/archify-route-share-card.png)
*1200×630 OG 比例的 route 截图，证明「可分享静态产物」承诺（回应 Issue #81）*

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/tt-a1i/archify |
| Star / Fork | 30,996 / 1,930 |
| 代码行数 | 114,753 行（HTML 42.3% / JS 37.1% / JSON 20.4% / 其他 0.2%） |
| 项目年龄 | 4.5 个月（2026-04-15 至今） |
| 开发阶段 | 密集开发期（dev_stage = 密集开发；近 30 天 63 commits） |
| 贡献模式 | 单人主导（top_author_share = 81.7%，174/187 commits） |
| 热度定位 | 大众热门（4.5 个月冲 31K stars） |
| 质量评级 | 代码 9 / 文档 9 / 测试 9 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

`tt-a1i` 是一个匿名开发者（GitHub bio/company/location 全部为空），但他不是一个孤立作者 —— 而是一个**围绕「让 Agent 更专业」做完整产品矩阵**的系统构建者：

| 仓库 | Stars | 在矩阵中的角色 |
|------|-------|----------------|
| **archify** | 30,996 | 旗舰：Agent 的「眼睛」（画架构图） |
| simplify-codebase | 345 | Agent 的「修剪器」（代码简化） |
| matt-skills-with-to-goal | 109 | Agent 的「意志」（目标驱动） |
| **tokenmeter**（Go） | 29 | Agent 的「燃油表」（呼应 #22/#66「费 token」痛点） |
| skillroster（Rust） | 6 | Agent 的「工具箱」（Skill 安装器） |

**关键洞察**：tokenmeter 这个 Go 项目不是巧合 —— 作者自己也被 archify 的 token 消耗所困扰，所以专门做监控工具。这种「深度 agent 用户 + 工具作者」的双重身份给了他三件产品判断力：
1. **Agent-first 输出契约**：每个 CLI 命令返回结构化 `diagnostics[]`（rule code + subject + evidence + supportedFixes），让 Agent 能读懂、能修，而不是看 Node stack trace。
2. **「Truth before spectacle」作为第一原则**：`reach ≠ blast radius`、`route ≠ 运行时调用`、`claim 必须来自 authored 数据或 git-verified evidence` —— 与 SaaS 时代「指标越炫越好」完全相反。
3. **拒绝自动布局 = 拒绝把决策权外包给库**：手摆坐标承载的架构语义是产品护城河，2026-04-16 的盲评实验（`experiments/v3-mermaid-validation/RESULT.md`）证明这点。

### 问题判断

作者看到了三个别人没重视的痛点：

1. **Mermaid 对 LLM 不友好**：语法错误率高、复杂图 30+ 节点变意大利面、review/diff 痛苦 —— 但开发者图生态完全没解决。
2. **GUI 工具（Draw.io / Excalidraw）没有 AI 接口**：产物是 binary XML 或带语义的 JSON，但都不是为 agent 设计的。
3. **Agent 画的架构图没有「信任层」**：谁审过？谁画错了连接线？没有 fail-closed 校验、没有版本对比、没有 git-verified evidence —— archify 把整个信任基建都补齐。

**时机为什么是现在**：2026 年 Agent 工具进入「可交付物」阶段 —— 不再是聊天框里的 demo，而是要嵌进 PR review、PR comment、博客分享、CI artifact 的真实工件。archify 切的就是这个窗口。

### 解法哲学

**明确选择的**：
- **JSON IR + typed schema**（不是 Mermaid 文本）—— 让 LLM 一次写对、让 reviewer 一次看懂
- **手摆坐标 + fail-closed 校验**（不是 dagre/elk 自动布局）—— 7 个 named composition gates（flow / corridor / border-run / route-rhythm / label-clearance / proper-crossing / crossings）+ standard/showcase 双档严格度
- **零运行时依赖** —— `archify.zip` 是可扔进任何 AI 沙箱（甚至 Claude.ai 上传 zip）的纯 Node 包
- **Honest contract** —— SKILL.md 明确写「A passing final validation freezes the candidate: never edit it afterward」「If two consecutive rounds do not improve that best count, stop and report the unresolved diagnostics truthfully」

**明确不做的**（`ROADMAP.md` 列入 Not planned）：
- WYSIWYG 编辑器（archify 是编译器，不是编辑器）
- 托管 SaaS / telemetry（产物是单文件 HTML，无 server）
- 自动布局（盲评实验 FAILED，A=stock Mermaid、B=auto-layout+archify CSS、C=archify hand-placed，A=B << C）
- Mermaid 解析器（archify 不兼容 Mermaid，因为手摆坐标本身就是产品）

### 战略意图

**Open-core / genuinely open**：MIT license，archify 仍是免费开源，但赞助商 logo（APINEBULA、Raven/EverMind）已出现在 README —— 作者在尝试商业化接触，但**不污染开源体验**。

**矩阵战略**：archify 是旗舰，tokenmeter 是 archify 痛点自家解决方案，simplify-codebase 是配套 skill，skillroster 是 Skill 分发基建 —— 这是**Agent 工具集**的布局，不是单点产品。当别人还在做「AI 帮我画图」（单向），archify 是「AI 画 → 我审 → 我 share」的闭环。

## 核心价值提炼

### 创新之处

按新颖度 × 实用性排序：

| 创新点 | 新颖度 | 实用性 | 可迁移性 |
|--------|--------|--------|----------|
| **Engineering Profile 作为可扩展语义合约** | 9/5 | 8/5 | 9/5 |
| **Ordinary-Model Floor 基准** | 9/5 | 6/5 | 7/5 |
| **坐标即语义 + fail-closed 几何校验** | 8/5 | 9/5 | 7/5 |
| **Reach/Route Share Card（版本化分享）** | 8/5 | 8/5 | 6/5 |
| **Stable ID 体系穿透 viewer → permalink → delta** | 7/5 | 9/5 | 8/5 |
| **Atomic Verified Delivery + Last-Good Live Preview** | 7/5 | 8/5 | 8/5 |
| **Schema-first + 零运行时依赖** | 6/5 | 9/5 | 9/5 |

**最值得深挖的三个**：

#### A. Engineering Profile 作为可扩展语义合约（创新点 #1）

`meta.engineering_profile: 「deployment-ownership」` 是一个**范式级创新**：把「工程语义」作为 fail-closed 校验层挂在 schema 之上，而不是烤进 IR 核心。

**强约束**：
- 所有非 external 组件必须声明 owner
- 每个组件必须属于 exactly one `region` boundary（不允许横跨区域模糊所有权）
- `region` 和 `security-group` 两种 boundary 至少各一个
- 所有 `database` 类型必须被 `security-group` 包裹（私有）
- 跨 region / security-group 的 connection 必须有真实 crossing mechanism（如 `mTLS`, `cross-region WAL`）

**关键设计原则（Profile 不做什么）**：
- 不做基础设施发现
- 不验证仓库与运行时环境是否真的匹配
- 不假设 ownership = IaC 中的 owner
- **所有事实必须是 IR 作者显式声明的**

下一个 profile 可以是 `cost-attribution`（每个组件声明 cost center）/ `gdpr-scope`（PII 数据必须标注）/ `oncall-rotation` —— 这种「契约式扩展」对所有「严肃 infrastructure 文档」都适用。

#### B. 拒绝自动布局的 IR 设计（创新点 #3）

**Schema 层（`architecture.schema.json`）**：
- `components[]` 要求每个组件显式带 `pos: [x, y]` 或 `row/col`，**没有「自动算位置」的字段**
- `connections[]` 允许 `via: [[x,y],...]`、`fromSide/toSide`、`route: 「auto」|「straight」|「orthogonal-h」|「orthogonal-v」`
- `boundaries[]` 由 `wraps: [id...]` 隐式推导边界矩形

**渲染器层（`render-architecture.mjs`）**：
- `automaticPortSpread` + `automaticPortRhythmBridge` + `defaultFromSide/defaultToSide` —— 自动布局只在「端口散布」层面生效，**绝不重排节点位置**
- 实测看到 30/50 的 boundary padding（`boundaryPad: 30, boundaryExtraBottom: 20`）+ 18px boundary label baseline —— 源自 v2.2.1 一次 hand-arithmetic 修正
- `MOVE FROM` 幻影节点（Architecture Delta 里的 moved 节点）保留原坐标，证明坐标就是作者的语义

**为何这种设计是合理的**：手摆坐标的「代价」被以下收益抵消 —— **信息架构**（边界 ownership、security group 包裹关系、阅读节奏）与**视觉布局**是一体的，不能被 dagre 的「rectangular grid + arrow routing」切断。

#### C. Architecture Delta 版本对比（关联创新点）

`archify/delta/architecture-delta.mjs` 是独立模块（~600 行），实现 `compare <base.json> <head.json>`：

- **Canonicalization**：先对两侧做 `canonicalArchitecture()`（元数据标准化 + components 按 id 排序 + boundaries 按 wraps 排序 + connections 按 id 排序）→ `canonicalArchitectureJson()` 用稳定 key 序做 JSON 字符串化 → **SHA-256**
- **Stable ID 强制**：所有 `components` / `connections` / `boundaries` 必须有 author-controlled `id`（schema 用 `^[a-zA-Z][a-zA-Z0-9_-]*$` 强约束），没有 id 的文件直接 fail
- **分类变更**：semantic / evidence / scope / topology / geometry / provenance / presentation 几类
- **不动声色保留几何**：`removed` 节点保留 baseline 几何，`moved` 节点保留 `MOVE FROM` 幻影
- **Receipt 自报家门**：明确写 `AUTHORED SNAPSHOTS` 或 `REVISION-PINNED INPUTS`，**绝不宣称** risk / blast radius / mergeability / safety / verified PR impact

### 可复用的模式与技巧

1. **Diagnostics 协议**（`diagnostics[]` 含 stable rule code + subject + evidence + supportedFixes）—— 可直接迁移到任何 Agent 工具的输出契约，让 LLM 能读懂、能修。
2. **Schema-first + ajv standalone precompile** —— 提交校验 + 编译期把 schema 烤进纯 ESM 模块，runtime 不需要 ajv。适用于所有「LLM 输出需要 schema 强校验」的场景。
3. **Stable ID as first-class citizen** —— 组件、关系都接受可选 `id`，enable `#focus=<id>` / `#relation=<id>` permalink + 版本对比。可迁移到任何需要「随时间讨论同一份图」的场景。
4. **Atomic Verified Delivery** —— stage-目录 + 双重校验 + rename-as-commit + byte-stable rollback。「失败时 preserves the previous artifact byte-for-byte」。比 VS Code Live Share / Figma autosave 更激进，可平移到任何「AI 实时改文件 → 用户立刻看产物」场景。
5. **Honest Share Card** —— `variant=reach|route`、`canonical=false` 显式自报家门，告诉读者「这是我从一张大图里挑出来的视角，不是 canonical 输出」。**反 SaaS 时代「一键 share」的设计**：share 也是版本化的、可被质疑的。

### 关键设计决策

| 决策 | 问题 | 方案 | Trade-off | 可迁移性 |
|------|------|------|-----------|----------|
| 拒绝 dagre/elk 自动布局 | 自动布局会切断信息架构 | 强制 author-controlled 坐标 + 7 个 composition gates 校验 | token 消耗高（LLM 摆坐标）；换来架构语义保真 | 中（需要约定 schema） |
| 零运行时依赖 | AI 沙箱无 npm install | devDeps 编译期生成校验器 + 自包含 HTML 输出 | 失去 npm 生态便利；换来可分发性 | 高 |
| Engineering Profile fail-closed | IR 作者可能编造 ownership | 显式 opt-in + 强约束 + 不假设 IaC 匹配 | 增加作者声明负担；换来「trust before spectacle」 | 高（任何严肃 infra 文档都适用） |
| Atomic rename-as-commit 发布 | zip 可能与 source 漂移 | stage 目录 + 双重校验 + rename-as-commit + zip-freshness CI | CI 复杂度↑；换来 byte-stable rollback | 高 |
| 五种图型并列而非统抽象 | 不同图型几何差异大 | 共享 viewer/validator/i18n layer + 每种独立 renderer | 重复模板代码；换来每种图型可独立优化 | 中 |

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | archify | Mermaid | Draw.io / Excalidraw | 同层 Agent-native（quasar-graph 等） |
|------|---------|---------|---------------------|--------------------------------------|
| **Agent 友好度** | ⭐⭐⭐⭐⭐（typed JSON IR） | ⭐⭐（语法错误率高） | ⭐（XML/JSON 非 agent 友好） | ⭐⭐⭐（多为 Mermaid 后端） |
| **版本对比** | ⭐⭐⭐⭐⭐（Architecture Delta） | ❌ | ❌ | ❌ |
| **工程语义校验** | ⭐⭐⭐⭐⭐（Engineering Profile） | ❌ | ❌ | ❌ |
| **生态成熟度** | ⭐⭐（4.5 个月） | ⭐⭐⭐⭐⭐（8K+ stars，多年积累） | ⭐⭐⭐⭐⭐（Draw.io 巨头） | ⭐（< 10 stars） |
| **WYSIWYG 编辑** | ❌（明确 declined） | ❌ | ⭐⭐⭐⭐⭐（Draw.io 强项） | ❌ |
| **GitHub 渲染** | ❌（需要 viewer） | ⭐⭐⭐⭐⭐（原生） | ❌ | ⭐（需 Mermaid 后端） |
| **可分享静态产物** | ⭐⭐⭐⭐⭐（Reach/Route Share Card） | ⭐⭐（需截图） | ⭐⭐⭐（可导出 PNG） | ⭐ |
| **Trust 层证据** | ⭐⭐⭐⭐⭐（git-verified evidence） | ❌ | ❌ | ❌ |

### 差异化护城河

1. **技术护城河**：手摆坐标 IR + Engineering Profile + Architecture Delta 这套组合在 Agent-native 时代是稀缺的，竞品难以快速复制。
2. **生态护城河**：31K stars vs 同层 < 10 stars，4.5 个月的「Agent Skill 工具集」矩阵（archify + tokenmeter + simplify-codebase + skillroster）。
3. **信任护城河**：「truth before spectacle」原则 + honest share card + 不宣称 blast radius —— 在 AI 编造架构故事泛滥的时代，这是稀缺资产。

### 竞争风险

**最危险的对手不是同层 Agent-native 竞品，而是 Mermaid 11.14 + ELK + Neo/Redux themes** —— 当 Mermaid 自带 ELK 自动布局并提供 15+ 主题后，「更漂亮 + 自动布局」的叙事被 Mermaid 收回了一部分。

**archify 的应对**：
- 坚守「手摆坐标是产品」（`ROADMAP.md` 的 v3-mermaid-validation FAILED 实验是这一立场的基石）
- 把战线推到**信任层**（Engineering Profile / Architecture Delta / Repository Evidence / Reach/Route Share Card）—— 这是 Mermaid 永远做不到的，因为 Mermaid 不掌握语义层

### 生态定位

在整个技术生态中，archify 扮演的角色是 **「Agent-native 架构图的 Mermaid 杀手」** —— 不是替换手写 Mermaid（手写场景 Mermaid 仍是默认），而是替换**「让 agent 画架构图」**场景下的所有工具：
- 替换 Mermaid 输出（agent 写得差）
- 替换 Draw.io XML（agent 难以产出）
- 替换 Excalidraw JSON（语义缺失）

**填补了什么空白**：在「LLM-as-geometry-author + deterministic-geometry-referee + versioned-shareable-artifact」三位一体的组合上 —— 绝大部分竞品还在做「AI 帮我画图」（单向），archify 是「AI 画 → 我审 → 我 share」（闭环）。

## 套利机会分析

- **信息差**：archify 在中文圈关注度低于其技术价值（31K stars vs 0 个深度中文分析），是典型「被低估的潜力股」—— 4.5 个月的密集迭代 + Token-meter 矩阵协同 + Engineering Profile 范式创新。
- **技术借鉴**：7 个 composition gates 校验、Honest Share Card 模式、Diagnostics 协议、Atomic Verified Delivery 模式 —— 全部可平移到自己的项目。
- **生态位**：占据「Agent-native 架构图」空白，同层竞品 < 10 stars。**时间窗口 + 产品广度 + 社区飞轮的综合优势**正在形成护城河。
- **趋势判断**：Agent 工具进入「可交付物」阶段，archify 切的是 PR review / PR comment / CI artifact / 博客分享的真实场景 —— 趋势明确，无后发劣势。

## 风险与不足

1. **作者集中度 93%（bus factor 极高）** —— 174/187 commits 来自 tt-a1i，外部贡献者多 1-3 commits 路人。14 名贡献者池对 31K stars 项目来说过小。
2. **refactor = 0%（技术债累积）** —— 项目只做加法不做减法，与 fix 27.3% 偏高互为佐证；当前是成长期，但 6-12 个月后重构压力会显现。
3. **Token 消耗未根治** —— Issue #22 / #66 抱怨 archify 消耗 M3 几十兆 token；当前靠「LLM 写 JSON 而非 SVG」缓解，未在 IR 层做降本。tokenmeter 是监控工具，不是解决方案。
4. **几何校验敏感性** —— Issue #126 反映 showcase 验证套件存在几何敏感性问题（跨列边长不稳定），同一 spec 在不同列对可能 pass 或 fail。
5. **TS 缺位** —— 纯 JS + JSDoc，编辑器辅助弱；但作为 zero-dep skill 可能是故意选择。
6. **CI 复杂度** —— Node 18/20/22/24 × 三 OS × Chrome-required tests，PR 反馈时间可能偏长。

## 行动建议

- **如果你要用它**：
 - **强场景**：让 agent 画架构图并在 PR review / 文档站点 / 博客分享中嵌入
 - **弱场景**：手写单图（Mermaid 仍是默认）/ 需要 WYSIWYG 编辑（用 Draw.io）
 - **对比竞品的决策点**：你的图要进 PR review / CI artifact → archify；你的图只是开发者手画 → Mermaid
- **如果你要学它**：
 - **必读**：`archify/SKILL.md`（130 行强约束 prompt 范例）/ `DESIGN.md` / `PRODUCT.md` / `ROADMAP.md` / `experiments/v3-mermaid-validation/RESULT.md`
 - **重点模块**：`archify/renderers/shared/geometry.mjs`（7 个 composition gates 实现）/ `archify/renderers/shared/engineering-profiles.mjs`（范式级创新）/ `archify/delta/architecture-delta.mjs`（canonicalization + stable ID）
 - **关键文件**：`archify/schemas/architecture.schema.json`（手摆坐标 IR 的契约）/ `archify/bin/archify.mjs`（CLI 入口 + diagnostics 协议）
- **如果你要 fork 它**：
 - **可改进方向**：
 - 添加更多 Engineering Profile（cost-attribution / gdpr-scope / oncall-rotation）
 - 解决几何校验敏感性（Issue #126）
 - 把 IR 层做降本优化，缓解 token 消耗痛点（Issue #22 / #66）
 - TS 迁移（保持零运行时依赖前提下）

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/tt-a1i/archify |
| Zread.ai | 未收录（DeepWiki 已覆盖） |
| 关联论文 | 无（工程型项目，无学术对应） |
| 在线 Demo | https://tt-a1i.github.io/archify/（含 11 件 gallery） |
| 作者教程 | [Mushroom CV 中文教程](https://blog.mushroom.cv/blog/archify-tech-diagram-skill-guide/) / [KnightLi 英文教程](https://knightli.com/en/2026/07/15/archify-skill-install-architecture-diagram-troubleshooting) / [CoddyKit feature](https://www.coddykit.com/pages/blog-detail?id=513029&slug=archify-the-open-source-ai-agent-skill-with-20-000-github-stars-that-turns-code-) |
| Skill 列表 | [claudeskills.info](https://claudeskills.info/skills/tt-a1i/archify) |

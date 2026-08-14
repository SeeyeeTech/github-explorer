# GitHub 推荐：AI 画的图终于不丑了：17k stars 的 diagram-design 怎么做到

> GitHub: https://github.com/cathrynlavery/diagram-design

## 一句话总结

这是一份给 Claude Code / Codex / Pi 等 AI Agent 用的「编辑级画图」Skill 包 —— 核心资产是 1 份 SKILL.md + 39 份 references + 5 份 ADR + 17 个 Python 校验脚本，让 Agent 能输出「设计师不会想帮你改」的、绑定品牌色字体的 SVG/HTML 静态成品图。

## 值得关注的理由

1. **AI 工具的下半场不是「更能画」，而是「画得更像你」**：onboarding 时拉取你网站的 body 背景、CTA 色、h1 字体，把品牌 token 灌进调色板，再用 WCAG AA 对比度护栏；这是「个性化 LLM 输出」的正确姿势。
2. **把「设计品味」做成 CI 是真本事**：17 个 Python 校验脚本把网格 4 倍数、accesible motion、文档顺序作几何冲突判据、SHA-pinned 单 controller 等模糊规则，全部变成 PR 红线；Issue #45（label mask 被 node fill 裁掉）就是被 `verify-geometry.py` 在 CI 阶段抓住的。
3. **跨 4 平台 Agent 分发的样板**：Claude Code / Codex / Pi / Cowork 共用同一份 SKILL.md 和 references/，差异仅在 manifest 与 invocation wrapping，是「一份 Skill 多端消费」最完整的工程示范。

## 项目展示

![Content site architecture](https://raw.githubusercontent.com/cathrynlavery/diagram-design/main/docs/screenshots/architecture.png) — README 头部首图，展示如何在文章/文档流里嵌入成品图。

![The self-improving loop](https://raw.githubusercontent.com/cathrynlavery/diagram-design/main/docs/screenshots/loop.png) — 2.0 新增的「自我改进循环」主视觉，agent 输出 → lint-skin 自检 → 反馈修复 → 重新生成。

![Redrawn from a .drawio file](https://raw.githubusercontent.com/cathrynlavery/diagram-design/main/docs/screenshots/import-drawio.png) — `/import-drawio` 命令的输入→输出对比图，证明能把企业最普及的 `.drawio` 文件重新排版成品牌级图。

![Flowchart](https://raw.githubusercontent.com/cathrynlavery/diagram-design/main/docs/screenshots/flowchart.png) — 通用流程图成品代表，9 节点预算 + 4px 网格 + 1 个 accent 色的设计哲学视觉化。

![Sequence](https://raw.githubusercontent.com/cathrynlavery/diagram-design/main/docs/screenshots/sequence.png) — OAuth/refresh token 这类真实场景的可读性证明。

> 另可访问实时 gallery：`https://cathrynlavery.github.io/diagram-design/` —— 27 类型 × 3 主题 tab 切换 + dark mode。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/cathrynlavery/diagram-design |
| Star / Fork | 17,087 / 1,012（71 watchers） |
| 代码行数 | 18,479 行（HTML 54.2% / Python 39.9% / SVG 5.9%），注释占 36.2% |
| 项目年龄 | 3.9 个月（首次提交 2026-04-16） |
| 开发阶段 | 密集开发（5-6 月沉寂 → 8 月单月 77 commits，占总量 78%） |
| 贡献模式 | 主作者主导 + 社区贡献（Top 1 占比 44%，Top 3 占比 73%，17 个贡献者） |
| 热度定位 | 大众热门（fork:star ≈ 1:17，「作品级资产被取用」型热度） |
| 质量评级 | 代码优秀 / 文档优秀 / 测试充分（17 个 verify 脚本 + adversarial test） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Cathryn Lavery（cathrynlavery），独立创业者，BestSelf.co 自营至 $55M+ 营收，2022 卖给 PE 后又于 2024 回购。她的 bio 一句话自我定位：*「Becoming AI Native & documenting as I go」* —— 这不是修辞，而是字面意义上的工作方式：把自营 SaaS 公司沉淀下来的品牌/产品工艺，翻译成 AI Agent 可直接消费的 Skill 包。diagram-design 是这条 AI Native 叙事的第一块公开拼图（其 portfolio 还有 shipstats / agent-improvement-loop / repo-atlas / codex-build 同系列仓库）。

### 问题判断

作者识别了一个被低估的真问题：**「AI 生成的图」和「能放进博客/Slides/Figma 的图」之间存在巨大鸿沟**。Mermaid 解决的是「文本→图」的语法问题，但视觉默认工程感重；Excalidraw/tldraw 需要人在回路，Agent 流水线无法自然消费；D2 是更现代的语法层，但仍不解决「输出能直接对外发布」的最后一公里。**作者把这条鸿沟命名为 editorial quality（编辑级品质）** —— 不是更花哨，而是「关掉 AI 味」：1 个 accent 色、4px 网格、密度 4/10、可访问 motion 默认关。

### 解法哲学

极简且可证伪的三个原则：

1. **「The highest-quality move is usually deletion」** —— 9 节点预算、12 箭头上限，超出就拆 overview + detail。每个节点/连线必须自证必要性。
2. **静止 HTML 是默认，motion 是可选且 a11y 严格** —— 唯一允许的 inline JS 是 `template-motion.html` 那一份（SHA-256 pinned），`prefers-reduced-motion` 必须命中静态首帧。
3. **prose rule + Python checker + adversarial test 三件套** —— ADR-0005（label geometry is verified）就是这条信念的产物：Issue #45 证明「标签几何不能靠肉眼抽检」，必须用文档顺序作判据。

明确不做的（更重要）：不替代 Mermaid/D2/Excalidraw，而是把它们做成 primitive（`/import-mermaid`、`/import-drawio`、`primitive-sketchy`）；不堆 100+ 图类型，27 个 layout + 7 个 semantic pattern 锁死（ADR-0002：semantic patterns 不新增 type）。

### 战略意图

在作者「独立创业者把自己的工艺做成 AI 可消费的资产」这条战略线上，diagram-design 是「品牌/设计能力 token 化」的样板 —— 不是 BestSelf 这种 SaaS 产品的核心，而是**一种新的轻量商业模式**：用 SKILL.md 分发高密度人类工艺，让 agent 在写作流里按需调用。下一步可能是：把 BestSelf 14 年的「产品经理 + 设计师 + 开发者」协作剧本也做成 Skill 包，构成系列。同时 17 个外部贡献者 + 5 份 ADR 表明项目正在从「个人作品」演化成「社区公约」，是「个人项目 → 开源基础设施」的成熟拐点。

## 核心价值提炼

### 创新之处

按新颖度×实用性排序：

1. **把「设计品味」做成 CI 校验脚本（新颖度 5 / 实用性 5 / 可迁移性 5）**：17 个 Python verify 脚本覆盖网格 / 配色 / a11y / 资源 / 几何 / motion / 类型不变性 / 文档同步；这是目前开源界对「AI 输出物做视觉回归」的工程化最完整样本。
2. **Progressive disclosure 三层契约（新颖度 4 / 实用性 5 / 可迁移性 5）**：L0 manifest（触发词 + 能力声明，每次启动都看）→ L1 SKILL.md（哲学+路由表，加载到上下文）→ L2 references/（按需加载）。SKILL.md byte cap 40000 + frontmatter description 必须含全部 27 类型词 —— 把「触发命中率」当成 CI 守的硬约束。
3. **文档顺序作几何冲突判据（新颖度 5 / 实用性 4 / 可迁移性 4）**：`verify-geometry.py` 不只看 AABB 碰撞，而是判断 label mask 是否出现在「后来绘制的 node」之前；把 SVG 渲染顺序这一隐性约束变成机器可验证。可推广到任何「顺序影响正确性」的渲染问题。
4. **Canonical-controller + SHA-pinning（新颖度 4 / 实用性 5 / 可迁移性 5）**：当允许用户产物携带 inline JS 时，用同一个 git 内文件作 controller 真值，所有提交 hash-equal；既允许 JS 又不让 JS 分叉的最简解。
5. **跨 4 平台分发用同一份内容（新颖度 4 / 实用性 4 / 可迁移性 5）**：Claude Code / Codex / Pi / Cowork 共用同一份 SKILL.md 和 references/，差异仅在 manifest 与 invocation wrapping。任何「多 wrapper 单核心」项目（VS Code + JetBrains + Cursor + ……）都可以这样。
6. **DTD bomb 拒绝 + 容器格式防御（新颖度 3 / 实用性 5 / 可迁移性 5）**：`drawio_extract.py` 在 decode 前显式拒绝 `<!DOCTYPE>`/`<!ENTITY>`（包括压缩 payload 里），并通过 `_decompress_limited()` 限制膨胀比例 —— 经典 XXE/billion-laughs 防御。
7. **Discarded-counter 暴露审计面（新颖度 3 / 实用性 4 / 可迁移性 5）**：Mermaid extractor 报 `discarded: {style_directives: 4, click_handlers: 1}`，把「我扔了你什么」从黑盒变白盒。对所有「我接管你输入」的中间层都该有。

### 可复用的模式与技巧

- **ADR + verify 脚本 + adversarial test 三件套**：任何想「工程化模糊规则」的团队都该照搬这种结构 —— 规则文本 + 可执行校验 + mutate-期望失败测试。
- **PR 触发外部测试 + 子目录白名单**：CI 用 path filter 跑子集，新代码不在 baseline 内强制全 lint —— 渐进迁移的稳健做法。
- **GitHub Pages 当 Gallery**：仓库本身就是产品页面，`assets/index.html` 直接生成静态站点，零托管成本。
- **prompt injection 当 IR 安全测试集**：fixture 里塞 `IGNORE ALL PREVIOUS INSTRUCTIONS`，既保留在 IR 里作为 inert text，又确保序列化输出里剔除；把安全测试嵌进解析层而非外挂。
- **CI matrix 是真矩阵**：ubuntu + windows + macos × Python 3.11 + 3.12；`core.autocrlf=false` 强制 + `PYTHONIOENCODING=utf-8` + `PYTHONUTF8=1`；解决 CRLF、UTF-8、subprocess locale 三类真实跨平台问题。

### 关键设计决策

| 决策 | 问题 | 方案 | Trade-off |
|---|---|---|---|
| 27 类型 + 7 pattern + 3 primitive 三轴独立 | 类型数量膨胀会让 SKILL.md 字节爆 | ADR-0002 锁死 type 不变，行为轴独立叠加 | 加新行为模式不破坏现有资产 |
| Motion 默认关 + 单 controller SHA-pinned | 「每个文件都允许 inline JS」无法审计 | 唯一允许的 JS = `template-motion.html`，三处 hash 比对 | 牺牲灵活性换可审计性 |
| SKILL.md byte cap 40000 + 全类型词在 description | 删 description 来腾字节会让触发命中率归零 | CI 强制 byte cap + regex 含 27 类型词 | 牺牲字数为可发现性 |
| 几何冲突用文档顺序判据 | 单纯 AABB 碰撞会误判「zone eyebrow」合法情况 | require mask 在 node 之前 | 把隐性约束变显性 |
| 多 marketplace 4 套 manifest | 单 marketplace 会绑定单一 Agent | 差异仅在 manifest + invocation wrapping | 多一份 CI 同步成本 |

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | diagram-design | Mermaid | D2 | Excalidraw | draw.io | tldraw |
|---|---|---|---|---|---|---|
| 形态 | Agent Skill 包 | DSL + 渲染器 | DSL + CLI | 手绘 SaaS + 库 | 离线工具 | 白板 + AI |
| 触发方式 | 自然语言 → Agent → SVG | 文本 → DSL | 文本 → DSL | 鼠标点击 | 鼠标点击 | 鼠标 + AI |
| 视觉可品牌化 | 强（onboarding 拉品牌 token） | 弱（默认主题） | 中（主题引擎） | 弱 | 弱 | 中 |
| 输出形式 | self-contained HTML/SVG | SVG/PNG | SVG/PNG | JSON/.excalidraw | .drawio（XML） | JSON |
| Agent 可消费 | 是（直接出图） | 是（语法层） | 是（语法层） | 否（需人在回路） | 否 | 否 |
| 与本项目关系 | — | 上游（被 `/import-mermaid` 消费） | 同维错位 | 互补（被做成 `primitive-sketchy`） | 上游（被 `/import-drawio` 消费） | 同维错位 |

### 差异化护城河

1. **「编辑级品质」品牌叙事**：onboarding 拉品牌 token + WCAG AA + 设计哲学（最高质量的改动是删除）这套**叙事+工具+CI**三位一体，竞品需要重新发力气。
2. **AI 时代的「质量护栏」先发**：Mermaid/D2/Excalidraw 都没解决「AI 输出的视觉回归」问题；diagram-design 用 17 个 Python 脚本在 CI 阶段就锁住 —— 这是**最难复制的部分**，因为它需要设计 + 工程双背景。
3. **跨 4 平台分发的工程纵深**：单一仓库多端消费，对任何想复制者都是劝退级的工程投入。

### 竞争风险

最可能被 **「大型模型厂商内嵌的设计 skill」** 替代 —— 当 Anthropic/OpenAI 自己下场做「内置 design quality 的画图能力」，社区 skill 的护城河会被压缩。但项目已经从「个人作品」演化成「社区公约」（17 个贡献者 + 5 份 ADR），抗冲击能力较强。

### 生态定位

在整个技术生态里，diagram-design 卡在**「AI 流水线 → 编辑级成品」中间层**：上游消费 Mermaid/draw.io（语法层），下游交付 SVG/HTML（成品层）。它不抢任何一方的位置，反而把两端的生态「升级」一遍 —— 这是最稳的 niche 站位。

## 套利机会分析

- **信息差**：低 star 项目的红利窗已过（17K stars 大众热门），但**国内中文技术社区对 AI Skills 这一品类的认知仍处于早期** —— 把这套「progressive disclosure + CI verify」结构翻译给中文工程师，是真正的信息差。
- **技术借鉴**：17 个 verify 脚本里的 `verify-geometry.py`、`lint-skin.py`、`drawio_extract.py` 三件套是**可直接 fork 改写到自己项目**的资产，零上下文假设。
- **生态位**：填补「AI 输出的视觉品质护栏」空白 —— 这是 Mermaid/D2/Excalidraw 都没做的层面。
- **趋势判断**：增长曲线是脉冲式（5-6 月 0 commits → 8 月 77 commits + 17K stars），说明**外部引爆点正在驱动作者 all-in**；比竞品有「社区公约 + CI 护栏」双重先发优势，但窗口期可能只剩 3-6 个月（大型模型厂商内嵌风险）。

## 风险与不足

- **无 git tag**：99 commits / 17K stars 但 0 个 git tag，下游消费者没有 pin 点；plugin 通过 marketplace.json 滚动分发，影响有限但仍是治理瑕疵。
- **零 Refactor commit**：Fix > Feature（37 vs 34），还没有进入大规模重构期；这是项目年龄决定的，但累积 6-12 个月后可能出现技术债。
- **单一品牌皮肤强约束**：默认 jet-black + atomic-tangerine 高度 opinionated；onboarding 虽支持 5 类入口，但「6+ 颜色品牌」会被强制降级。
- **CI matrix 成本高**：3 OS × 2 Python × 14 个 step（含 Playwright 截图）每次 PR 跑十几分钟。
- **依赖 LLM 决定 layout**：对「想要 pixel-perfect 重复结果」的工程（如 IDE 内置 SVG 编辑器）这条路不适用。

## 行动建议

- **如果你要用它**：在写博客/文档/Slides 时调用 `/diagram-design`，先用 onboarding 流程拉取你网站的 brand token，再用 `/import-drawio` 改造既有的 `.drawio` 资产 —— 比手工重画省 10x 时间。
- **如果你要学它**：重点读 `docs/adr/0005-label-geometry-is-verified.md`、`scripts/verify-geometry.py`、`scripts/lint-skin.py` 三件套，理解「把模糊规则工程化」的范式；其次读 SKILL.md 的 progressive disclosure 三层结构。
- **如果你要 fork 它**：可改进方向 ——①把 27 类型中至少 5 个补全 machine-verified 的 stroke 几何校验（目前只有 rect 几何）；②把品牌 onboarding 流程支持导入 Figma variables；③把 verification 脚本拆成独立 PyPI 包，让其他 AI 输出场景复用。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/cathrynlavery/diagram-design （已收录，5 大节覆盖 System Architecture / 13 种 Diagram Types / Claude Code Integration / Design Philosophy / Repository Organization） |
| Zread.ai | https://zread.ai/cathrynlavery/diagram-design （已收录，指向 GitHub Pages gallery 列出 41 个模板按类型分组） |
| 关联论文 | 无（工程 + 设计实践，无 arXiv 论文） |
| 在线 Demo | https://cathrynlavery.github.io/diagram-design/ （GitHub Pages 实时 gallery，27 类型 × 3 主题 tab 切换） |
| 作者博客 | http://littlemight.com （已上线，作者发起 `$ start ai-native` 7 天挑战） |
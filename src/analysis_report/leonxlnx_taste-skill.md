# 3.6 个月 38K stars：一个人 13 个 SKILL.md，把 Cursor 干不出活的「slop 风」打回原形

> GitHub: https://github.com/leonxlnx/taste-skill

## 一句话总结
taste-skill 是 Claude Code / Cursor / Codex / Gemini CLI / v0 等 8 家 agent 平台通用的「反 slop 前端设计」skill 矩阵 —— 13 个独立 SKILL.md 把「设计品味」拆成可机械验证的规则集，让 AI 写前端不再输出满屏 em-dash + 紫色渐变的同质化模板。

## 值得关注的理由
- **品类占位**: 在 frontend design taste 这个 Claude Code skill 细分赛道，taste-skill 几乎是事实上的品类定义者，38k star / 2.7k fork 在 3.6 个月内达成，且 fork:star ≈ 7.1% 说明真实安装使用而非单纯点赞。
- **方法论升格**: `research/laziness/` 子模块把 LLM 偷懒问题（cognitive shortcuts / RLHF 偏向 / training data bias）从轶事升格为有学术数据支撑的系统性方法论，是 prompt-as-product 项目里少见的「边做产品边公开方法论」实践。
- **可机械验证**: 50+ 条 Strict Pre-Flight Checklist（em-dash 字符级禁令、eyebrow 机械计数、palette 旋转矩阵、CTA 唯一性等）把「设计品味」从主观辩论拉成可机械检查的规则集 —— 这是其他「设计指南」类项目普遍缺乏的工程化能力。

## 项目展示

![Taste Skill - Anti-slop Agent Skills for premium frontends](https://raw.githubusercontent.com/leonxlnx/taste-skill/main/assets/readme-banner.png) — 类型: hero（项目主视觉）

![Taste Skill logo](https://raw.githubusercontent.com/leonxlnx/taste-skill/main/assets/taste-skill-logo.webp) — 类型: logo

![Floria landing page top](https://raw.githubusercontent.com/leonxlnx/taste-skill/main/examples/floria-top.webp) — 类型: demo（Showcase 案例 Floria 落地页顶部）

![Floria landing page bottom](https://raw.githubusercontent.com/leonxlnx/taste-skill/main/examples/floria-bottom.webp) — 类型: demo（Showcase 案例 Floria 落地页底部）

![官网首屏主视觉](https://tasteskill.dev/_next/image?url=%2Fheroimg1.webp&w=3840&q=75) — 类型: hero（官网 hero gallery）

![终端安装示意](https://tasteskill.dev/_next/image?url=%2Fc1.webp&w=3840&q=75) — 类型: demo（一行 `npx skills add` 跨 8 agent 平台安装）

> 在线 Demo 入口：https://floria-landing-page.vercel.app/（Floria 落地页案例）| https://collectiveos.vercel.app/（技术性 UI 案例）

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/leonxlnx/taste-skill |
| Star / Fork | 38388 / 2729（fork:star ≈ 7.1%，真实使用率高于点赞） |
| Watcher / Open Issue | 123 / 数个开放（存在 star 远超 issue 参与的「传播-贡献剪刀差」） |
| 代码行数 | 21 行 Shell 包装（实质资产: 30 个 markdown / ~5,700 行 prompt 文本） |
| 项目年龄 | 3.6 个月（首次提交 2026-02-19，最近推送 2026-05-26，6 周未推但持续接收 star） |
| 开发阶段 | 密集开发（近 90 天 62 commit，占总量 64%） |
| 贡献模式 | 单人主导（3 个 contributor，Top1 占 96.8%） |
| 热度定位 | 大众热门 + 爆发型增长（最近 184 个 star 落在单日内，触发了某个大型传播节点） |
| 质量评级 | Prompt 优秀 / 文档优秀 / 测试无（靠 round-N hardening 人工对抗性测试） |
| License | MIT |
| 主页 | https://tasteskill.dev（Next.js 站，含 13 个子 skill showcase + changelog + blog） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Leon Lin（@leonxlnx，handle @lexnlin），Munich 独立开发者，账号 0.9 年（2025-07 创建），113 个公开仓库；bio 只写「i like to build stuff」，blog 在 own.page/leonlin，无公司隶属。**典型 AI-first builder** —— 作品横跨 SKILL prompt 工程、TS/JS 实战项目、TypeScript 浏览器 OS（aerodesk-11-browser-os）、Web RPG demo（shardwake-open-world-rpg）、生活压力测试基准等，且明显同时经营 design / coding 两个轴线（designthieves 是另一个 design 系列仓库）。

投入权重**高**：taste-skill 几乎贯穿作者全部高活跃期，账号 113 个仓库里这是最显眼的代表作。粉丝 1005，账号年龄虽短但产出密集、方法论扎实。

### 问题判断

作者从自身工作流里挖出了「AI coding agent 写前端时默认输出高度同质化的 slop 风」这个高频痛点 —— em-dash 满屏、紫色渐变 hero、左侧文本+右侧插画的同一套模板。这种从 dogfooding 挖出的痛点比「自上而下设计的 feature」更真实。

**为什么是现在**：2026-02 启动项目正好踩在 vibe-coding 爆发期（Cursor 用户激增）+ Vercel Labs 推出 `npx skills add` 标准化协议的时间窗，是「需求侧被 Cursor 验证 + 供给侧被 Vercel 标准化」的双重红利窗口。同时 `research/laziness/` 引用 Microsoft Research、LazyBench 2024 等论文，把「LLM 在执行长 prompt 时偷懒/走捷径」从轶事升格为有数据支撑的系统性问题。

### 解法哲学

- **Unix 哲学 × 设计系统**: 13 个 SKILL.md 各自单文件、自包含、可独立安装 —— 一个 skill 解决一个风格问题（brutalist / minimal / soft / stitch / imagegen-frontend-web 等），不试图做「一个能 cover 一切」的 mega prompt
- **可机械验证 > 美学讨论**: 用 em-dash 字符级硬禁令、eyebrow 机械计数、palette 旋转矩阵等可执行的 pre-flight checklist，把「设计品味」从主观品味拉成可机械检查的规则集
- **真实 design system > 凭空捏造**: 12 个官方 package（Material / Carbon / Polaris / Radix 等）映射优先 + 8 种 aesthetic 的「honest implementation」（包括 Apple Liquid Glass 的近似版），拒绝「看起来像 Material 但其实不是」的假设计系统
- **明确不做什么**: 不做 hosting / SaaS / 模板 marketplace；不做 IDE 插件；不替代 Tailwind/组件库；只做「写在 SKILL.md 里的设计方法论」

### 战略意图

taste-skill 是作者公开的**代表作**（账号 113 个仓库中投入权重最高），是 Leonxlnx 品牌的主轴。商业化路径是 GitHub Sponsors 12 位 + 官网 https://tasteskill.dev —— 保持「开源品牌 + sponsorship」路线，无 SaaS 计划、无 enterprise 版本。

开源策略是 genuinely open（MIT License），所有 prompt 内容 100% 公开；但靠「作者的持续 round-N hardening + research/ 方法论沉淀」建立时间维度的护城河 —— 可被 fork 但难被同质量再维护。

## 核心价值提炼

### 创新之处

1. **Em-Dash 字符级硬禁令 + Eyebrow 机械计数**（新颖度 4/5 / 实用性 5/5 / 可迁移性 5/5）：把「反 slop」从美学讨论拉成可机械执行的字符级规则；eyebrow 文字不能超过 3 词，否则 trigger redesign
2. **Three-Dial + 推断矩阵**（VARIANCE / MOTION / DENSITY 1-10）（3/5/5/5）：用三个 1-10 标尺量化创意输出连续谱系，配合 brief 推断矩阵自动设置初值
3. **Brief Inference one-liner + Ask-One-Question**（3/5/5/5）：brief 一行话直接推断设计方向；信息不足时 agent 只问一个问题而非一连串
4. **Real Design System 优先级 + Apple Liquid Glass Honest Approximation**（4/5/5/4）：强制使用 12 个真实 design system package，禁止「凭空捏造」；Apple Liquid Glass 等 aesthetic 用 honest approximation（明确标注是近似）
5. **Premium-Consumer Palette Ban + 旋转矩阵**（4/5/5/4）：禁止紫色渐变 hero 等 slop 调色板；提供 8 种审美调色板旋转矩阵
6. **No Duplicate CTA Intent**（4/5/4/5）：同一页面不能有多个相同意图的 CTA（如「Get Started」+「Try Free」+「Sign Up」），强制 CTA 唯一性
7. **GSAP Sticky-Stack canonical skeleton + Forbidden Animation Patterns**（3/5/5/5）：提供 canonical 动效骨架（sticky-stack 滚动叙事等）+ 明确禁止的动效模式（bounce / 默认 ease-in-out 等）
8. **Lazy-Loaded Skills 35% context 缩减 + Discovery 68%→90%**（5/5/5/5）：把 13 个 skill 拆成独立可加载模块；按需安装后 context 占用减少 35%，LLM 对可用 skill 的发现率从 68% 提升到 90%
9. **Research 子模块公开化方法论**（4/5/4/5）：把 LLM 偷懒的研究方法论、实证数据、根因分析公开在 `research/laziness/`，作为 skill 仓库的「学术附录」
10. **LLM Psychology Pattern Matching**（4/5/5/4）：把 LLM 心理学（cognitive shortcuts、training bias、RLHF 偏向）作为 prompt 设计的输入变量，而非把 LLM 当黑盒

### 可复用的模式与技巧

- **Single-File SKILL.md Pattern**: 每个 skill 一个自包含 markdown 文件、分章节编号 —— 适用任何 Claude Code / Cursor skill 仓库
- **Pre-Flight Checklist Pattern**: 50+ 条可机械验证的硬规则清单，agent 输出前自查 —— 适用任何 LLM 输出质量管控
- **Three-Dial Quantification Pattern**: 用 1-10 标尺量化创意输出连续谱系 —— 适用任何 creative coding / 设计生成
- **Brief Inference + Ask-One-Question Pattern**: 简短输入先推断，信息不足时只问一个问题 —— 适用任何 AI 生成场景的 prompt 模板
- **Real Design System Priority Pattern**: 强制使用真实 design system，禁止凭空捏造 —— 适用 enterprise 前端 / 严肃产品设计
- **Multi-Style SKU Split Pattern**: 把 mega prompt 拆成多个独立可加载 skill —— 适用任何 LLM tool 生态的「垂直化」分发
- **Research Submodule Pattern**: 把工程方法论沉淀到独立 `research/` 子模块公开 —— 适用把工程实践升格为方法论的项目
- **Round-N Hardening Iteration**: 用对抗性测试驱动 prompt hardening，按 round 编号（commit 记录暴露「round-5 hardening from Opus 4.7」式迭代节奏）—— 适用任何长生命周期 prompt 项目

### 关键设计决策

1. **SKILL.md 单文件自包含**: 主 SKILL.md 1206 行 14 节 + v1 SKILL.md 226 行 + 其他 11 个子 skill 各自单文件；章节用编号小标题（## 1 / ## 2 ...）便于 LLM 解析。Trade-off: 单文件超过 1200 行后上下文压力变大 —— 作者用 `output-skill` 单独解决 truncation 问题。可迁移性**高**。
2. **跨 8 Agent 平台抽象**: 不绑定任何平台；通过 Vercel Labs `npx skills add` 协议分发；README 明确列出 8 个平台（Claude Code / Cursor / Codex / Gemini CLI / v0 / Lovable 等）兼容。Trade-off: 牺牲「某平台深度集成」换「跨平台覆盖率」。可迁移性**高**。
3. **Brief Inference → Design System Map**: 第一步 inference（推 brief 类型）→ 第二步 map（映射到 Material / Carbon / Polaris / Radix 等 12 个真实 design system）。Trade-off: 强约束产出质量，但要求作者持续维护 design system 矩阵 —— 维护成本由 `research/laziness/` 的方法论文档吸收。可迁移性**中-高**。
4. **50+ 项 Strict Pre-Flight Checklist**: em-dash 字符级检测、eyebrow 文字≤3 词、palette 不能用紫色渐变模板、CTA 不能重复意图等。Trade-off: 极大约束 LLM 自由度、产出可能「过度同质」；换来「反 slop 严格度」和「输出可解释」。可迁移性**高**。
5. **Multi-Style SKU 拆分**: brutalist / minimalist / soft / stitch / imagegen-frontend-web/mobile / output / redesign / brandkit / image-to-code / gpt-taste / v1 / v2 等 13 个独立 SKILL.md，按需 `npx skills add` 安装。Trade-off: 用户认知负担高（issue #15 就是「教学成本」），换来「每个 skill 极致精专」和「按需加载节约 context」。可迁移性**高**。
6. **Research Submodule 公开化方法论**: 把 LLM 偷懒问题拆成 4 个 root cause（RLHF / output-limits / training-data-bias / cognitive-shortcuts），每条配 4 类 remediation（parameter-tuning / prompt-engineering / reference-prompts / architectural-patterns）。Trade-off: 维护一个研究子模块需要持续投入（11 次修改的热点目录），换来「方法论可复用 + 公开化建立作者权威」。可迁移性**高**。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | taste-skill | steipete/agent-rules | Vercel Labs agent-skills | Anthropic claude-code examples |
|------|------------|---------------------|------------------------|-------------------------------|
| 定位 | Frontend design taste 专项 | 通用 agent rules 合集 | 协议 + skills 注册表 | 官方通用工程示例 |
| Star | 38.4k | 5.7k | 数千级（基础设施） | —（官方仓库） |
| 内容深度 | 13 个子 SKU 各自精专 | 覆盖面广但浅 | 仅协议不生产内容 | 通用工程，无 frontend 专项 |
| Pre-flight 验证 | 50+ 条可机械验证 | 无 | 不适用 | 无 |
| 跨平台分发 | 8 agent 平台通用 | 覆盖 Claude Code / Cursor | `npx skills add` 协议 | 仅 Claude Code |
| 方法论文档 | `research/laziness/` 10 篇 | 无 | 无 | 无 |
| 商业化 | GitHub Sponsors | 暂无 | 平台商业 | 不适用 |

### 差异化护城河

- **内容深度护城河**: 13 个子 SKU 每个都是精专设计方法论 + 50+ 条可机械验证的 pre-flight checklist —— 这是 fork 容易、re-maintain 极难的「时间维度护城河」
- **方法论护城河**: `research/laziness/` 把 LLM 偷懒的根因（RLHF / cognitive shortcuts / training bias）+ remediation（parameter-tuning / prompt-engineering / reference-prompts / architectural-patterns）公开化，建立作者在「prompt 工程学术化」赛道的权威
- **生态护城河**: Vercel Labs `npx skills add` 协议下 taste-skill 是「最早的明星内容之一」，后来者需在协议层抢曝光

### 竞争风险

- **Anthropic 官方 frontend design skill**（最可能的「渠道/官方」威胁）：若 Anthropic 未来推出 frontend design 官方 skill，taste-skill 将面临「官方背书」压力 —— 但 13 个子 SKU 的内容深度是护城河
- **Vercel Labs 自营内容**（协议方下场做内容）：若 Vercel Labs 决定自营 frontend design 内容，taste-skill 失去协议分发优势 —— 但当前 Vercel Labs 定位为「协议方」而非「内容方」
- **社区反向 port 削弱控制力**: issue #35 显示 Svelte 5 port 正在社区反向输出，若生态足够活跃，原作者的「品牌」可能稀释

### 生态定位

在整个「agent 协议层（Vercel Labs）→ 设计内容层（taste-skill）→ 用户安装使用」的金字塔中，taste-skill 是当前 frontend design taste 方向的**品类定义者 + 内容深度领跑者 + 方法论文贡献者**。

> 结论：frontend design taste 细分赛道接近蓝海，taste-skill 是事实上的占位者与品类定义者；与 steipete/agent-rules（互补）、Vercel Labs agent-skills（共生）、Anthropic claude-code examples（互补）均为零或低竞争。

## 套利机会分析

- **信息差**: 已不属于被低估项目（38k star 是赛道头部）；但社区讨论层（watcher 123、issue 活跃度一般）相对 star 量偏低，存在「star 远超 issue 参与」的传播-贡献剪刀差，反而提示**潜在机会**：作者一人维护难消化 38k star 用户的反馈，可关注 roadmap 跟进
- **技术借鉴**: 三 dial 模式、pre-flight checklist 模式、research/ 子模块方法论文档模式、round-N hardening 迭代模式均可直接迁移到自己的 prompt 项目
- **生态位**: 填补了「agent + 视觉」这一交叉空白；与 steipete/agent-rules（通用 rules）和 Vercel Labs（协议层）错位
- **趋势判断**: vibe-coding 持续爆发 + agent 平台协议标准化（Vercel Labs `npx skills add`）；taste-skill 在 3.6 个月内 star 增长到 38k，验证了「frontend design skill」是 agent 生态的刚需方向

## 风险与不足

- **单人维护风险**: 96.8% 单人主导，账号年龄仅 0.9 年；若作者 burnout 或转向，13 个子 skill 的维护负担难以为继
- **传播-贡献剪刀差**: 38k star 但 watcher 仅 123、issue 数量一般，存在「phantom stars」争议（issue #48），需关注 star 真实性
- **教学成本压力**: 13 个子 skill 的认知负担是普通用户门槛（issue #15「Add examples of each skill?」）
- **路线图缺口**: 尚未覆盖 a11y（issue #32「Add an accessibility skill」）、template skill 模板（issue #23）等延伸需求
- **无版本化**: 无 tag、无 release，依赖 commit hash 或 README 章节定位版本，读者无法回溯到具体版本
- **依赖协议方**: 跨 8 agent 平台分发依赖 Vercel Labs `npx skills add` 协议，若协议方策略变化，分发渠道受影响

## 行动建议

- **如果你要用它**: 一行 `npx skills add Leonxlnx/taste-skill` 安装 v2 默认 skill；如需特定风格（brutalist/minimal/soft/stitch），再追加安装对应子 skill。适合 vibecoding / nocode / lowcode 场景下需要快速出「不像 AI」产品 UI 的独立开发者和小团队
- **如果你要学它**: 重点关注（按可迁移性排序）：
  - `skills/taste-skill/SKILL.md`（v2 默认，1206 行 14 节，主入口）
  - `skills/output-skill/SKILL.md`（反 truncation 输出策略）
  - `research/laziness/remediation/architectural-patterns.md`（LLM 偷懒的架构层缓解）
  - `research/laziness/remediation/prompt-engineering.md`（prompt 工程的系统性方法论）
  - `research/laziness/findings/empirical-results.md`（LLM 偷懒的实证数据）
- **如果你要 fork 它**:
  - 添加 a11y 子 skill（issue #32 提示的需求缺口）
  - 制作空白 skill 模板（issue #23 提示的生态扩展需求）
  - 为每个子 skill 增加可执行源码 example（issue #15 提示的文档债）
  - 接入更多 agent 平台（OpenCode / Aider 等）
  - 引入 CI 验证 SKILL.md 格式（pre-flight checklist 自动化检查）

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录（页面 403） |
| Zread.ai | https://zread.ai/leonxlnx/taste-skill（已收录，含 13 skill 清单、价值主张、hero gallery、showcase、sponsor 列表） |
| 关联论文 | 无（`research/laziness/` 引用 Microsoft Research / LazyBench 2024 等学术研究，但无项目自身发表论文） |
| 在线 Demo | https://floria-landing-page.vercel.app/（Floria 落地页案例）\| https://collectiveos.vercel.app/（技术性 UI 案例） |
| 官方主页 | https://tasteskill.dev（Next.js 站，含 13 个子 skill showcase + changelog + blog） |

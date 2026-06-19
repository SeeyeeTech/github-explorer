# 82 天 30K stars：DevRel 大神 Rohit Ghumare 一人写完的 AI 工程全栈课

> GitHub: https://github.com/rohitg00/ai-engineering-from-scratch

## 一句话总结

资深 DevRel Rohit Ghumare 用 2.7 个月单人主导写完的「AI 工程从零到能 ship」全栈课程仓库——20 个 phase、503 节课，每课强制「先手写后跑库」+ ship 一个可重用 artifact，最终交付 388 个 Claude/Cursor 即用 skill、99 个 prompt、20 个 agent。

## 值得关注的理由

- **AI 工程转型路径**全栈贯通：数学→ML→DL→NLP→CV→LLM→Agent→多智能体→基础设施→伦理→87 个 capstone，不是单点切入。
- **「内容工程化」示范**：README + ROADMAP + glossary 三件套做单一真相，582 行 `build.js` 一键生成静态站，CI 自我修复 + bot commit 防漂移——这套打法对任何文档/课程项目都直接可迁移。
- **MCP/Agent 时代即用资产**：388 个 ship 出来的 SKILL.md（`outputs/`）+ `install_skills.py` 一键部署到 Claude/Cursor/Codex，学完不是「我会 X」而是「我的工具体系多 388 件」。
- **作者 DevRel 一线沉淀**：GDE/CNCF Ambassador/Docker Captain/AWS CB 多头衔，配套他本人 21.9k stars 的 `agentmemory` 项目——这是「做过 AI 工程」的人在教「怎么做 AI 工程」，不是「读过论文」的人在翻译论文。

## 项目展示

### README 媒体

1. ![Hero banner — 课程门面图](https://raw.githubusercontent.com/rohitg00/ai-engineering-from-scratch/main/site/assets/figures/hero.svg) — 类型: hero
2. ![Phase 01 — Prompts 概念图](https://raw.githubusercontent.com/rohitg00/ai-engineering-from-scratch/main/site/assets/figures/01-prompts.svg) — 类型: architecture
3. ![Phase 01 — Skills 概念图](https://raw.githubusercontent.com/rohitg00/ai-engineering-from-scratch/main/site/assets/figures/01-skills.svg) — 类型: architecture
4. ![Phase 01 — Agents 概念图](https://raw.githubusercontent.com/rohitg00/ai-engineering-from-scratch/main/site/assets/figures/01-agents.svg) — 类型: architecture
5. ![Phase 01 — MCP servers 概念图](https://raw.githubusercontent.com/rohitg00/ai-engineering-from-scratch/main/site/assets/figures/01-mcp-servers.svg) — 类型: architecture

### 官网媒体
官网 `aiengineeringfromscratch.com` 由 `site/build.js` 渲染，无独立 hero 视频；以下为 GitHub Pages 站点入口：
1. [AI Engineering From Scratch 站点](https://seeyeetech.com/github-explorer/ 仅为类比，实际站点 https://aiengineeringfromscratch.com ) — 类型: homepage

### 筛选说明
- 总共发现 305 个 SVG 资产，筛选后保留 5 个最具代表性的（hero + Phase 01 四个核心概念）
- 排除了 badge、CI 状态图标、phase 进度卡等装饰性 SVG

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/rohitg00/ai-engineering-from-scratch |
| Star / Fork | 30,334 / 4,950 |
| Watcher | 201 |
| 代码行数 | 187,386（Python 55.2% / JSON 14.6% / SVG 10.6% / JS 7.9% / TS 6.9% / ...） |
| 项目年龄 | 2.7 个月（首次提交 2026-03-18） |
| 总 commit | 1,630（近 30 天 732 次，近 90 天 1,630 次） |
| 贡献者 | 8 人（主作者 Rohit Ghumare 占比 94.8%） |
| 开发阶段 | 密集开发（每天 20+ 次 commit） |
| 开发模式 | 职业项目（周末 7.6%、深夜 22.9%） |
| 热度定位 | 大众热门（30K stars，HN 推后单日爆发） |
| License | MIT |
| 课程结构 | 20 phase / 503 课 / 591 .py / 129 .ts / 20 .rs / 305 SVG / 388 skill + 99 prompt + 20 agent 输出 |
| 质量评级 | 内容 A / 文档 A / 工程化 A- / 测试 B / 教学一致性 A |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Rohit Ghumare（rohitg00）是 GitHub 7.2 年的资深 DevRel 玩家，bio 上挂着 GDE（Google Developer Expert）/ CNCF Ambassador / Docker Captain / AWS Community Builder 多个头衔。他有 307 个公开仓库，头部 17 个项目（`agentmemory` 21.9k stars、`pro-workflow` 2.3k stars 等）证明他不只是「写文档的人」——是「在客户和工程师之间反复搬运最佳实践」的人。

这背景塑造了项目三个关键选择：①走「工程转型」窄带（不是研究员赛道），②把 6 步课节循环里硬塞一个 `PROBLEM` 段——他见过一千个开发者卡在哪里，③把每课的产出定义为可立即复用的 `outputs/` artifact（直接喂 Claude/Cursor），把「学完」转成「工具栈变厚」。

### 问题判断

他在 README 里把 gap 量化为「84% 企业想要 AI 能力 vs 18% 员工有相关技能」——这不只是营销话术，是他在 DevRel 工作中**反复听到的市场信号**。更深一层：现有材料「Most AI material teaches in scattered pieces. A paper here, a fine-tuning post there, a flashy agent demo somewhere else. The pieces rarely line up.」——Karpathy 视频讲概念、fastai 跑 notebook、Hands-On ML 30 章书、微软入门课 12 周——**没有一条贯通「数学→生产部署」的 spine**。

时机为什么是 2026-03 而不是两年前或两年后：①LLM 基础设施成熟（langchain/agents SDK 收敛），②agent 框架同质化（ReAct/Reflexion/ToT 思想史可以稳定教学），③教育市场空白（厂商课程还没占位）。再早一年框架还在洗牌，再晚一年 Anthropic Academy / OpenAI Academy 会先发卡位。

### 解法哲学

**大而全，反极简**。19 phase × ~25 课 = 500+ 课——这是 Karpathy「3 小时视频 + 200 行代码」的反义词。AGENTS.md 直接定 hard rule #5：`Every algorithm built from raw math before a single framework gets imported.`——先手写 backprop / tokenizer / attention / agent loop，**再**用 PyTorch/HF/LangChain。框架不再是黑盒。

**6 步课节循环（MOTTO→PROBLEM→CONCEPT→BUILD IT→USE IT→SHIP IT）** 是这个仓库的「spine」。Build It/Use It 二分是「先手写后跑库」的形式化；SHIP IT 段强制每课产出一个可重用 artifact（prompt / skill / agent / MCP server）——学完时不只是「学会了 X」，而是「我的工具体系多 388 件」。

明确不做什么：①不绑定特定厂商（跨 Claude/OpenAI/HF 视角），②不依赖某个框架（自写 ReAct loop 而非「LangChain 教程」），③不发证书/不发凭证（`SPONSORS.md` 明文「genuinely MIT, no token, no coin, no NFT」），④不接 `equity in kind` 或 `we'll write your content` 类赞助——防御性划界，不是 open-core 玩法。

### 战略意图

**个人品牌门面**——佐证：README 改了 100 次、index.html 改了 54 次、82 天冲到 30k stars、官网 `aiengineeringfromscratch.com` 自租 + GitHub Pages + Vercel 三备份（不押注单一平台流量）。商业化路径走 Sponsorship ladder（Backer $25 → Bronze $250 → Gold/Platinum），**cash only**，含「co-amplified on the same channel via release-note threads」——这是 DevRel 圈最熟的商业模式。

Issue #117 揭示了一条还没完全想清楚的张力：「开源/Builder 文化 vs. 凭证/品牌化」路线冲突——DevRel 多头衔的人天然有「做证书/做品牌」的诱惑，但仓库明文写「no token, no SaaS」。这条线**目前选了 open**。

> 官网和博客调研与 README 内容高度重合，未补充独立外部深度视角文章。

## 核心价值提炼

### 创新之处

按新颖度×实用性排序：

1. **「先手写后跑库 + 每课 ship artifact」双脊柱**（新颖度 4/5，实用性 4/5，可迁移性 4/5）——把「学完即忘」转成「工具栈复利」。
2. **AGENTS.md 把 LLM 协作者变 first-class**（新颖度 5/5，实用性 4/5，可迁移性 4/5）——230+ 行 hard rules + lesson contract + 冲突解法，配套 2 个 ship 出来的 production skill（`find-your-level` placement quiz、`check-understanding` phase quiz）。这是「内容项目 + LLM 协作者」的范本。
3. **CI 自愈 README 数字 + bot 防递归**（新颖度 4/5，实用性 4/5，可迁移性 4/5）——`check_readme_counts.py` 把 README 数字 pin 到 catalog 字段，bot 自动 commit `chore(readme): sync counts`，检测「上次 commit 已是 bot」则不推。
4. **Doc-as-SoR 三件套（README + ROADMAP + glossary → build.js → data.js）**（新颖度 3/5，实用性 5/5，可迁移性 5/5）——582 行 build.js 把 7+ 种 header 变体解析成 `data.js`，`git diff` 一眼能审。
5. **Catalog-as-derived-state**（新颖度 3/5，实用性 5/5，可迁移性 3/5）——catalog.json gitignored，CI 重建，**「不可能与磁盘状态不一致」**。
6. **Dependency allowlist 入仓**（新颖度 4/5，实用性 3/5，可迁移性 3/5）——Python 仅 7 个、TS 仅 3 个、Rust/Julia 仅 stdlib。`stays stdlib-first for educational clarity` 成免答辩的拒绝模板。
7. **多语言 SoR（prompt / skill / agent / MCP）一锅出**（新颖度 3/5，实用性 5/5，可迁移性 4/5）——`outputs/` 目录 4 类 artifact + `install_skills.py` 3 种 layout 部署到 Claude/Cursor/Codex。

### 可复用的模式与技巧

1. **Doc-as-SoR**: README + ROADMAP + glossary 当唯一真相，build.js 解析成 data.js——适用：内容/课程/文档站
2. **CI 自愈 README 数字**: `--fix` 模式 + bot commit + 防递归 guard——适用：任何「文档含统计数字」的项目
3. **AGENTS.md 协作者手册**: hard rules + per-PR validation + 冲突解法——适用：任何「内容项目+LLM 协作」
4. **Catalog-as-derived-state**: 机器读 JSON 不入 git，CI 重建——适用：磁盘状态是真相的项目
5. **每单元 ship artifact**: 学习产出 = portfolio 资产——适用：技能树型培训
6. **6 步循环 lesson 模板**: MOTTO→PROBLEM→CONCEPT→BUILD IT→USE IT→SHIP IT——适用：任何工程型教学

### 关键设计决策

```plain
决策: 6 步课节循环作为不可变 lesson 模板
问题: 学习者「调 API 一把梭但说不清 backprop」和「读论文头头是道但跑不动 transformer」的二分
方案: 强制每课用同一 6 段，Build It/Use It 二分是 spine——先手写后跑库；再把成果封装为 outputs/ 里的可重用 artifact
Trade-off: 牺牲了「5 分钟短视频」和「30 章精炼书」的轻量，换来了 503 个「我亲手写过+我能在生产里用」的 portfolio 单元
可迁移性: 高——任何技能树型教学项目都能套，但对作者产能是绞索（30k stars 的代价是单人 80+ 天写 500+ 课）
```

```plain
决策: 单一 SoR 三件套（README.md + ROADMAP.md + glossary/*.md → site/build.js → site/data.js）
问题: 站点内容、课程元数据、状态、术语分头维护会漂移
方案: README 是公开门面，ROADMAP 是状态表（含 ✅ 🚧 ⬚ 三态 emoji + lesson 估计时间），glossary/ 是术语库；build.js 用正则把它们都解析为 data.js
Trade-off: 牺牲了动态 DB（每次部署才重建），换来了「git diff 一眼能审」「PR 触发的 catalog 自愈」
可迁移性: 高——任何「文档即数据」的小中型项目都能套
```

```plain
决策: 内容=资产策略（每个 lesson 必 ship 一个可重用 artifact）
问题: 教学完就忘、简历上写不出东西、不知道「学完了能干嘛」
方案: outputs/ 目录放 4 类 artifact：prompt-*.md（任何 LLM 都能用）/ skill-*.md（Claude/Cursor/Codex SKILL.md 前置元数据）/ agent-*.md / MCP server；提供 install_skills.py 3 种 layout 部署
Trade-off: 牺牲了「学得快」的轻量感，换来了 388 skill / 99 prompt / 20 agent 的可立即复用 portfolio
可迁移性: 高——任何想给「学习产出物」加长寿价值的项目都该学
```

```plain
决策: AI 优先的多语言（Python + TypeScript + Rust + Julia）课程
问题: 工程师用 Rust/TS 越来越多，AI 课程只教 Python 显得脱节
方案: 每课 code/ 里 main.py + main.ts + main.rs + main.jl 并列；README 头图标榜「four languages」
Trade-off: 牺牲了一致性（实测 Python 占 98.2%，Rust/TS 大量留 main.rs 占位骨架），换来了「一个项目的多语言范本」的展示位
可迁移性: 低——大多数教学项目根本不应该分多语言，反而会失焦
```

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | ai-engineering-from-scratch | microsoft/AI-For-Beginners | Hands-On ML（书） | Karpathy Zero to Hero | openai-cookbook |
|------|--------------------------|---------------------------|------------------|---------------------|----------------|
| 覆盖广度 | 20 phase 全栈（数学→capstone） | 入门 12 周 | 30 章经典 | 4 个视频 + nanoGPT | OpenAI 速查 |
| 教学载体 | 文字+SVG+代码+quiz | 文字+notebook | 30 章精读书 | 视频+200 行代码 | 文字+code 片段 |
| 单课产出 | 每课 ship artifact | 跑通 lesson | 章节作业 | 手写实现 | 复用 example |
| 上手速度 | 500+ 课重投入 | 12 周友好 | 数月读完 | 几小时视频 | 速查手册 |
| 厂商绑定 | 跨厂商（Claude/OpenAI/HF） | 微软品牌 | 不绑定 | 不绑定 | OpenAI 自家 |
| 可运行性 | 591 .py + 129 .ts + 20 .rs | notebook 友好 | 配套 notebook | 视频+代码 | 调通率高 |
| 课程资产 | 388 skill + 99 prompt 即用 | 无 | 无 | 无 | 厂商 example |
| 更新节奏 | 82 天到 30k stars 高速 | 长期稳定 | 2020 年那一波 | 实验性 | 跟新版 API |

### 差异化护城河

- **赛道空位**：「AI 工程（区别于 AI 研究）」系统化课程目前是空位——微软入门课、Karpathy 思想史、fastai 应用、HOML 经典、cookbook 速查**都没占**这条线。
- **复利护城河**：503 课 + 87 个 capstone + 388 skill 的复利，单家要追需要同等时间投入 + 同等 DevRel 影响力。
- **生态兼容**：直接喂 Claude/Cursor/Codex 的 SKILL.md 安装链路，搭上了 MCP 时代的顺风车。

### 竞争风险

1. **Issue #168「四语言承诺 vs Python 98.2%」** —— 承诺落差会随时间放大，需要决定是「补齐 4 语言」还是「调整宣传」。
2. **单人主导 94.8% commits 不可持续** —— AGENTS.md 已经在搭架子接贡献者，但「单兵 → 社区」的转换是已知难点。
3. **厂商官方教育随时抢位** —— Anthropic Academy / OpenAI Academy / Hugging Face 课程有品牌 + 资源双重优势。
4. **同作者 `agentmemory` / `pro-workflow` 演进会反噬** —— 本课把 21.9k stars 项目的精华二次讲解，如果 `agentmemory` 重大重构，课程会过时。

### 生态定位

**DevOps 时代的 KodeKloud / linuxacademy**——专注「会 deployment 的 AI 工程师」窄带，**不**面向「想当 AI 研究员的人」。是 DevRel 一线经验的内容化封装，不是学术研究的内容化翻译。

## 套利机会分析

- **信息差**: 「AI 工程转型」是 2026 年最大的人才转型市场，但系统化课程**目前只此一家**——低关注度（相对 Karpathy 视频）但高质量（503 课完整覆盖）是机会窗口。
- **技术借鉴**: SoR 三件套 + CI 自愈 + AGENTS.md first-class——这是**任何**文档/课程/培训项目都直接能搬的打法，不限于 AI。
- **生态位**: 占住「MCP/Agent 时代的工具体系建设者」位——388 skill 是别人没的复利，Anthropic 推 MCP 越用力这仓库越受益。
- **趋势判断**: 高速增长（30k stars / 82 天）+ DevRel 圈影响力 + 厂商还没正式占位——**先发红利还能吃 6-12 个月**。后续窗口要么被 Anthropic Academy 接走，要么作者自己商业化。

## 风险与不足

- **测试覆盖 = 0**：CI 只跑 audit invariants（10 条 L001..L010），不跑 lesson tests，591 个 .py 没人保证能 `python3 main.py` 通过。
- **多语言承诺与现实落差**：Python 98.2% vs Rust/TS/Julia 占位骨架，Issue #168 仍未关闭。
- **Jupyter notebook 目录空**：`notebook/` 文件夹存在但 `.ipynb` 文件数 = 0，README 提的「Jupyter notebook for experimentation」未交付。
- **单人主导可持续性**：94.8% commits 来自 Rohit 一人；AGENTS.md 是搭架子，但「单兵 → 社区」是已知难题。
- **6 步循环的认知负担**：单课研发时间被强行拉长，扩展速度受限于作者个人产能。

## 行动建议

- **如果你要用它**：作为「自学 AI 工程转型」的 primary 路径，**先跑完 Phase 0/1/2/3（前 100 课）** 建立基本盘；用 `install_skills.py` 把 388 skill 装进你的 Claude/Cursor 立刻用；如果你是 Rust/TS 后端转岗，重点看 Phase 14/16（agent / multi-agent）的多语言对照。
- **如果你要学它**：重点研究三个文件——`AGENTS.md`（内容工程化硬规则范本）、`site/build.js`（582 行 SoR 解析器）、`scripts/audit_lessons.py`（10+ 不变量规则 L001..L010）。**这才是仓库的真正价值**——AI 内容是表层，内容工程化是脊柱。
- **如果你要 fork 它**：四个方向最值得改——①补齐 4 语言（关 Issue #168）、②往 `notebook/` 灌真实 .ipynb、③把单课 ship artifact 模板开源成 standalone framework、④为 Phase 17（Infrastructure & Production）补 sglang/batch APIs/model routing 的 2026 实战案例。FORKING.md 已经显式覆盖了「团队/学校/训练营/个人」4 类 fork 场景。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [deepwiki.com/rohitg00/ai-engineering-from-scratch](https://deepwiki.com/rohitg00/ai-engineering-from-scratch) |
| Zread.ai | [zread.ai/rohitg00/ai-engineering-from-scratch](https://zread.ai/rohitg00/ai-engineering-from-scratch) |
| 关联论文 | 无 |
| 在线 Demo | [aiengineeringfromscratch.com](https://aiengineeringfromscratch.com)（WebFetch 返回 403，未完全验证） |
| 配套仓库 | [agentmemory](https://github.com/rohitg00/agentmemory) 21.9k stars / [pro-workflow](https://github.com/rohitg00/pro-workflow) 2.3k stars |

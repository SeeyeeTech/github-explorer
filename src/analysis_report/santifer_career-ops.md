# GitHub推荐：3 个月 57K★：把求职变成 Open Agent Skill Standard 的开源范本

> GitHub: https://github.com/santifer/career-ops

## 一句话总结

career-ops 是一个用 8+ AI coding CLI 当"求职指挥中心"的本地优先开源项目——把 6-Block 评估流 + A-F 透明评分 + Markdown 即 prompt 资产组合成 "Open Agent Skill Standard" 的 reference implementation,挑战 SaaS "mass auto-spam" 求职赛道的根本哲学。

## 值得关注的理由

1. **产品化范本而非代码深度**:57K★ 在 3 个月内集中爆发(6 commits/天,WIRED + Business Insider + Product Hunt 媒体矩阵齐发),作者亲口说"用这套工具拿下 Head of Applied AI 职位"再开源,是"自下而上 builder-in-public" 的最佳实践。
2. **"Open Agent Skill Standard" 的工程级实现**:20+ 个 `modes/*.md` prompt 资产被 Claude Code / OpenCode / Codex / Gemini / Qwen / Kimi / Grok / Copilot **8+ AI CLI 同时复用**——这是第一个在工程级别证明 agent skill 跨 CLI 标准化可行的项目。
3. **"files canonical, databases derived" 多 runtime 协作范式**:JS CLI 核心 + Next.js Web alpha + Go TUI Dashboard 三域独立构建,共享 markdown/TSV 文件作为 single source of truth,可迁移到任何"多 runtime 工具"。

## 项目展示

### README 媒体

1. ![Career-Ops Multi-Agent Job Search System](https://raw.githubusercontent.com/santifer/career-ops/main/docs/hero-banner.jpg) — 类型: hero(架构图/项目主视觉,顶部 800px 横幅)
2. ![Career-Ops Demo](https://raw.githubusercontent.com/santifer/career-ops/main/docs/demo.gif) — 类型: demo(800px 终端录制,展示 pipeline 实际跑通过程)
3. ![Product Hunt Featured](https://raw.githubusercontent.com/santifer/career-ops/main/docs/press/producthunt.svg) — 类型: screenshot(社交背书)
4. ![WIRED](https://raw.githubusercontent.com/santifer/career-ops/main/docs/press/wired.svg) + ![Business Insider](https://raw.githubusercontent.com/santifer/career-ops/main/docs/press/business-insider.svg) — 类型: screenshot(媒体背书,合并 1 槽位)

### 官网媒体

1. ![Career-Ops Hero Image](https://career-ops.org/_next/image?url=%2Fhero_image.avif) — 类型: hero(Next.js 渲染的终端 pipeline 截图)

### 筛选说明

- 总共发现 7 个有效媒体元素(hero-banner / demo.gif / producthunt / wired / business-insider / warpchart chart / contrib.rocks)
- 筛掉 4 类无价值元素:trendshift 徽章、Discord/npm/claude-code shield.io 状态按钮、warpchart chart 动态外链(verified=null)、contrib.rocks(verified=null)

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/santifer/career-ops |
| Star / Fork | 57,873 / 11,393 |
| 代码行数 | 48,998(JavaScript 52.3%, TSX 14.0%, Go 10.9%, TypeScript 10.0%, JSON 7.7%) |
| 注释占比 | 47.6%(异常高——prompt/markdown 是一等公民) |
| 项目年龄 | 2.9 个月(2026-04-04 创建) |
| 总 commits | 509(近 30 天 297 个,占 58.4%) |
| 开发阶段 | 密集开发(2.0-rc.1 已发) |
| 贡献模式 | 单人主导 + 社区协作(30 名贡献者,Top 1 占 43.2%) |
| 热度定位 | 大众热门(爆发型增长) |
| 质量评级 | 代码[良好] 文档[卓越] 测试[优秀] CI/CD[优秀] |

## 作者视角:为什么存在这个项目

### 创始人/作者背景

Santiago Fernández de Valderrama(账号 @santifer),Seville, Spain。Bio 自述 "Building career-ops, open-source AI job search (57k★). Head of Applied AI. Founder (exit 2025)"——三个身份叠加:**连续创业者 / Applied AI 实践者 / Builder-in-Public**。

账号年龄 0.4 年(2026-01-23 创建)但粉丝 2,826——这是典型被自身明星项目 career-ops 引流的账号画像。Public repos 24 个,career-ops 投入权重极高(在最近 push 仓库中排第 2,仅次于自建的 warpchart.dev star telemetry 工具)。其他关键项目:`cv-santiago` 719★(本人真实 CV 样本)、`career-ops-docs` 36★、`career-ops-plugin-template` 2★——形成完整生态。

### 问题判断

作者看到了**三层错位**:

1. **候选人侧**:740+ offers,200+ 公司,Excel 追踪、Word 改 CV、LinkedIn 群发——手动定制每份申请不可能。
2. **公司侧**:ATS 用 AI 做 keyword filter / ML ranking,真正匹配的候选人反而被漏掉。
3. **现有工具侧**:LazyApply / Loopcv / JobHire.AI 走"mass auto-submit" 哲学,100% 黑盒,被候选人用到 spam 风控失效甚至被招聘方反制。

**时机**:2026 年 4 月——Claude Code 出圈 + Anthropic Agent SDK 成熟 + LinkedIn 2024 起对自动投递降权——三者叠加,创造了"AI 帮候选人 choose company" 这个叙事支点的最佳窗口。

### 解法哲学

作者明确选择的:**Filter + Tailor + Human-clicks-Submit**,与 SaaS 阵营的 "Submit" 形成根本对立。

- **透明度**:A-F 6 block + 10 维度加权 + Block G(Posting Legitimacy 独立评分,3 档评级)——AI 决策完全可审计。
- **本地优先**:data/applications.md + reports/*.md 是 single source of truth,SQLite 仅作 derived index,用户拥有 100% 数据。
- **零遥测零账户**:`package.json` 0 analytics 依赖,扫、评估、生成全在 local。
- **明确不做什么**:永不 auto-submit,不抓取 LinkedIn,不做 mass apply,不做 SaaS 化。

### 战略意图

**基础设施 + Open-core with strong community moat**,而非产品。

- 商业模式:完全免费(MIT 协议),仅商标 "career-ops" 保留(`TRADEMARK.md`)。
- 商业化路径:个人品牌(santifer.io)+ 培训/咨询/写作 + 雇主品牌效应——**非 SaaS**。
- 长期意图:演化为"Open Agent Skill Standard" 的 reference implementation,超越求职垂直,成为 agent skill 设计模式的示范项目。

## 核心价值提炼

### 创新之处

按新颖度×实用性排序:

1. **Open Agent Skill Standard 跨 CLI 复用模式**:20+ 个 `modes/*.md` 被 8+ AI coding CLI 同时复用,实现"一次编写、所有 agent 都能跑"。新颖度 5/5,实用性 4/5,可迁移性 5/5。
2. **6-Block + Block G 双轨评分**:A-F 评估 fit score(10 维度加权),Block G 独立评估 posting legitimacy(高/中/低 3 档)——避免单一分数掩盖"看起来好但其实是 ghost job"。引用 Bommasani et al. FAccT 2026 "Algorithmic Monocultures" 论文。实用性 5/5,可迁移性 5/5。
3. **`update-system.mjs` 静态 import closure 扫描自升级**:用 `relativeImportSpecifiers()` 正则扫描 `import ... from` 闭包,自动 checkout 所有相关文件,解决"老版本升级到新版本时 import 闭包死锁" 经典难题。实用性 4/5,可迁移性 5/5。
4. **Voice DNA 优先级链**:用户的 `_profile.md` > `voice-dna.md` > 默认 style,两层 scope(抗 AI-slop 硬规则 vs 对话风格规则)清晰分离。实用性 4/5,可迁移性 5/5。
5. **A-F 评分透明 rubric**:`modes/_shared.md` 公开 "4.5+ Strong match / 4.0-4.4 Good / 3.5-3.9 Decent / <3.5 Recommend against" 阈值。实用性 5/5,可迁移性 4/5。
6. **本地优先 + 零遥测 + 零账户**:`scan.mjs` 纯本地 HTTP,Playwright PDF + LaTeX 双管道,ATS 优化 keyword 注入。实用性 4/5,可迁移性 4/5。
7. **14 语言 README 同步**:`update-system.mjs` 的 `SYSTEM_PATHS` 全部含在内,DACH / 法国 / 日本 / 中东 / 波兰区域市场深度本土化(7 套区域化 modes)。实用性 3/5,可迁移性 3/5。

### 可复用的模式与技巧

可直接迁移到其他项目:

1. **"Markdown 即 prompt" 模式**:把 system prompt 从代码里剥离,作为 markdown 一等公民,用户可读可改可 fork 可版本管理。语言切换零代码改动。
2. **"files canonical, databases derived" 多 runtime 协作**:CLI + TUI + Web + Mobile 面对"数据流多向" 难题时,把 markdown/TSV 作为 single source of truth,SQLite/regex parser 只作 derived index。
3. **DATA_CONTRACT.md system/user 边界 + CI 强 enforce**:`SYSTEM_PATHS` allowlist + `USER_PATHS` denylist + `validate-system-paths-coverage.mjs` 校验 + `no-user-data.yml` workflow 拦截。
4. **单文件集成测试 `test-all.mjs` 模式**:9758 行,Node 内置 `node:assert`,零依赖零安装零 framework,`node test-all.mjs` 直接跑。适合"开箱即用" CLI 工具。
5. **多 AI CLI vendor 目录约定**:`.agents/ .claude/ .opencode/ .antigravitycli/ .grok/ .kimi/ .qwen/ .codex/` 各自目录 + 共享 AGENTS.md 路由 + `scaffolder/bin/skill-entrypoints.mjs` 动态 materialize。
6. **TSV 单一 tab-separated 行写入 + `merge-tracker.mjs` 合并**:适合 ETL/批处理场景,Markdown table 在并发写入时容易损坏,TSV 解决原子并发安全。

### 关键设计决策

**决策 1:三域协作(JS CLI / Next.js Web / Go TUI)共享 files canonical**
- **问题**:三个独立 runtime 怎么共享数据?各自维护 DB 冲突不可避免。
- **方案**:`data/applications.md` + `reports/*.md` 是 single source of truth,SQLite 仅作 derived index。Go dashboard 用 regex 解析 markdown,JS tracker 用列名 header 解析,Web Next.js 读同一文件。
- **Trade-off**:Markdown 解析在 Go 侧必须做严格格式兼容(列名 header-aware + fallback 固定位置),任何 column 插入都需双向同步;反之获得"git diffable、人类可读、跨语言共用" 的好处。
- **可迁移性**:**极高**。任何多 runtime 工具面对"数据流多向" 难题时都适用。

**决策 2:6-Block 评估流是 evaluation 的固定协议**
- **问题**:求职评估的"分析" 容易跑偏——要么 30 页长文,要么 30 个 bullet 的 list,没有结构。
- **方案**:A-Role Summary / B-CV Match / C-Level Strategy / D-Comp Research / E-Customization Plan / F-Interview Plan / G-Posting Legitimacy——7 个固定 block,每 block 强制输出 schema。
- **Trade-off**:对"显然的 yes" 显得啰嗦(需 2 分钟生成);对"模糊的 hybrid 角色" 塞不进 6 archetype;反之获得横向对比 100+ offers 极方便 + LLM 输出可被验证。
- **可迁移性**:**中-高**。任何"多维度评估 + 决策支持" 场景(投资尽调、招聘 offer 评估、技术选型)都可用这个 schema。

**决策 3:`update-system.mjs` 自更新系统必须解决"re-exec with new imports" 经典死锁**
- **问题**:你正在跑 v1.5.0 的 `update-system.mjs`,要从 GitHub fetch v1.6.0;但 v1.6.0 多了一个新 import。如何让老版本"接力" 给新版本而不炸?
- **方案**:备份 → 检出 fetch 后的 `update-system.mjs` + `resolveReexecCheckout()` 静态扫描其 ESM import 闭包 → 把整个 closure 全部 checkout 出来 → `exec` 新版本接管。`REEXEC_FALLBACK_FILES` 提供兜底。
- **Trade-off**:静态扫描可能漏掉动态 import / conditional require;反之获得"老版本永远能升级到老版本的下一版" 的健壮性。
- **可迁移性**:**高**。rustup / Homebrew / nvm 等工具的传统做法都不够通用。

**决策 4:多 AI CLI vendor 目录 + 共享 AGENTS.md 路由**
- **方案**:`.agents/skills/career-ops/SKILL.md`(agentskills.io 标准) + `.claude/skills/career-ops/`(Claude Code 软链) + `.opencode/skills/ + .opencode/commands/`(OpenCode 双格式) + `.antigravitycli/ .grok/ .kimi/ .qwen/`。所有 CLI 入口最终指向 canonical `AGENTS.md`。
- **Trade-off**:每次新 CLI 出现要加一个 vendor 目录;反之获得"7+ CLI 共享同一 prompt 资产" 的绝对优势。
- **可迁移性**:**极高**。"Open Agent Skill Standard" 是真正的范式。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | career-ops | LazyApply | Loopcv | JobHire.AI | Teal | Huntr |
|------|---------|--------|--------|--------|--------|-------|
| 过滤 vs 投递哲学 | Filter + Tailor(人点 Submit) | Mass auto-submit | Mass auto-submit | Autonomous agent | Tracker + AI 简历 | Kanban tracker |
| 评分透明度 | A-F 6 block + 10 维 + Block G | 黑盒 | 黑盒 | 黑盒 | 半透(模板匹配) | 无评分 |
| ATS 优化 | Playwright PDF + LaTeX 双管道 | 默认 | 默认 | 默认 | 模板化 | 无 |
| Human-in-the-loop | **强(永不 submit)** | 无 | 弱 | 无 | 强 | 强 |
| 开源程度 | **MIT,完全开源** | 闭源 | 闭源 | 闭源 | 闭源 | 闭源 |
| 本地优先 | **是(files canonical)** | 否 | 否 | 否 | 否 | 否 |
| 定价 | **$0** | $49-149/月 | $24-99/月 | $29-99/月 | $50-200/月 | Free + $40/月 Pro |
| CLI 集成 | **8+ AI coding CLI** | 否 | 否 | 否 | 否 | 否 |
| 学术背书 | **是(Algorithmic Monocultures aware)** | 否 | 否 | 否 | 否 | 否 |

### 差异化护城河

1. **开源 + 本地优先**:在"数据隐私" 成为强诉求的求职场景下,这是结构性优势——SaaS 竞品无法复制。
2. **Open Agent Skill Standard 跨 CLI**:7+ AI coding CLI 都能用,触达开发者天然渠道——SaaS 竞品没有这条管道。
3. **品牌权威 + 社区**:57K★ + Product Hunt Featured + WIRED/Business Insider 报道,先发优势强。
4. **学术背书**:直接引用 Bommasani et al. FAccT 2026 关于 ATS 算法的论文,提升可信度。
5. **modes-as-content 资产**:20+ 个 markdown prompt 库 + 7 语言区域化 = 7 套 prompt 工程,非 trivial 工作量。

### 竞争风险

1. **LazyApply/Loopcv 用"magic 一键" 拉新用户**:career-ops 的 "filter+tailor" 学习曲线显著高于 "点一下自动投 100 家"。
2. **ATS 厂商反制**:LinkedIn 2024 已对自动投递工具降权——如果主流 ATS 把"用 AI 生成的 cover letter" 标记为低质,career-ops 价值链受冲击。
3. **大厂做"求职 Copilot"**:Microsoft Copilot for Job Search / Google Job Search AI 是潜在降维打击——但生态被锁定在 Office/Workspace 反而是 career-ops 的机会。
4. **Issue #238 反映的产品张力**:用户对"持久化登录 + 一键投递" 的渴望(参 [linkedin-mcp-server](https://github.com/santifer/career-ops/issues/238))可能让作者被迫妥协 human-in-the-loop 哲学。

### 生态定位

- **横向**:对标 Cursor / Continue.dev / Cody(都是"AI coding CLI 时代的工具")——career-ops 把同一思路套到"求职"。
- **纵向**:在"AI + 求职" 垂直里,占据"开源 + 透明 + human-in-the-loop" 三个象限,避开了"闭源 mass-spam" 红海。
- **未来**:很可能演化为"Open Agent Skill Standard" 的 reference implementation——超越求职垂直,成为 agent skill 设计模式的示范项目。

## 套利机会分析

- **信息差**:57K★ 已构成大众热门,套利窗口已过;但**"career-ops 是个 prompt 工程产品化范本"** 这个认知还远未在中文技术社区普及,这是**信息差套利**的机会——把 Open Agent Skill Standard 的设计哲学介绍到中文社区有先发优势。
- **技术借鉴**:最有可迁移性的 4 个设计(DATA_CONTRACT system/user 边界 + modes-as-prompt + update-system import closure + A-F+G 双轨评分)可直接用到自己的项目。**门槛**:理解 modes/*.md 的 prompt 工程思想 + update-system.mjs 的 import 闭包扫描机制。
- **生态位**:career-ops 填补了"AI coding CLI 时代缺一个求职领域的 Open Agent Skill reference implementation" 这个空白,竞品全是 SaaS 闭源。
- **趋势判断**:Agent Skill 标准化 + 本地优先 + 数据隐私——三者都在趋势风口上,career-ops 既有先发优势又有结构优势,**比 SaaS 竞品有后发优势**。

## 风险与不足

1. **2.0-rc.1 未稳定**:架构正在升级(refactor 仅 0.5%,还在功能扩张期未沉淀),2.0 大版本可能带来 breaking changes。
2. **商业模式单一**:完全依赖个人品牌 + 社区,无 SaaS 收入,长期维护者激励问题待观察。
3. **9758 行单文件测试**:在 IDE 友好性 / 并行化上受限。
4. **50+ modes 数量增长后的发现机制**:discovery 需要持续优化,否则用户进入成本会上升。
5. **Issue #238 反映的产品张力**:用户对"持久化登录 + 一键投递" 的渴望可能让作者被迫妥协 human-in-the-loop 哲学。

## 行动建议

### 如果你要用它

- **适用**:Senior+ AI/ML/Platform 工程师、Head of Applied AI、Staff+ 级别、愿意自部署 CLI 的求职者。
- **不适用**:初级求职者(评分阈值 4.0/5 卡死,ethical use 段落反复劝退低 fit 投递)、不愿用 CLI 的纯 SaaS 偏好者、追求 100% 自动化的 lazy-apply 信仰者。
- **vs 选 SaaS 工具**:如果你在意数据隐私、想要透明 rubric、愿意投入 30 分钟配置 → 选 career-ops;如果你想 5 分钟开箱即用 → 选 Huntr / Teal。

### 如果你要学它

**重点关注的文件/模块**:

| 优先级 | 路径 | 学什么 |
|---|---|---|
| ★★★★★ | `ARCHITECTURE.md` + `modes/oferta.md` | 6-Block 评估流的设计思想 |
| ★★★★★ | `DATA_CONTRACT.md` + `update-system.mjs` | system/user 边界 + 自升级机制 |
| ★★★★★ | `AGENTS.md` + `.agents/skills/career-ops/SKILL.md` | Open Agent Skill Standard 跨 CLI 复用 |
| ★★★★☆ | `modes/_shared.md` | A-F 评分透明 rubric + Voice DNA 优先级 |
| ★★★★☆ | `dashboard/internal/data/career.go` | Go 端 markdown 解析 + 三域协作 |
| ★★★☆☆ | `test-all.mjs` | 单文件集成测试的零摩擦哲学 |
| ★★★☆☆ | `plugins-registry.json` | 插件注册中心的数据结构 |

### 如果你要 fork 它

**可以改进的方向**:

1. **简化评估流**:6 block 对 90% 场景过度工程,做一个 3-block 简化版(尤其针对中级求职者)
2. **加入 LinkedIn 集成**(注意 #238 的设计张力):做"半持久 session" + 显式"这是 AI 帮你登录,不是 AI 帮你投"
3. **把"Open Agent Skill Standard" 抽象成独立 npm 包**:让任意 prompt 资产都能用同一 vendor 目录约定打包
4. **加入 ATS 反向工程模块**:扫描 ATS 输出,反推"为什么这个 CV 被拒" + 给出修补建议
5. **多模态面试 prep**:语音/视频 mock interview(Issue #509 已经提了)
6. **数据可视化增强**:Go TUI dashboard 加 7 维度散点图(补偿 vs match score 关系)

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [https://deepwiki.com/santifer/career-ops](https://deepwiki.com/santifer/career-ops) |
| Zread.ai | 未验证可达(WebFetch 403) |
| 关联论文 | [Algorithmic Monocultures in Hiring (Bommasani et al. FAccT 2026)](https://arxiv.org/abs/2412.06039)(项目内引用) |
| 在线 Demo | `docs/demo.gif`(终端录屏);可 `npx @santifer/career-ops init` 本地复跑 |
| 作者长文 | [santifer.io/career-ops-system](https://santifer.io/career-ops-system) |
| 官方文档 | [career-ops.org](https://career-ops.org) + [career-ops.org/compare](https://career-ops.org/compare) |

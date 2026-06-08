# 专抓 AI 写的烂 React，自己一半也是 AI 写的

> GitHub: https://github.com/millionco/react-doctor

## 一句话总结

React Doctor 是 Million.js / react-scan 作者 Aiden Bai 的新作——一个**确定性（非 LLM）的 React 代码扫描器**，专门抓 AI agent 写出的烂 React，跨「state & effects / 性能 / 架构 / 安全 / 无障碍」5 大维度用 338 条规则给代码体检；而最妙的反讽是：这个「抓 AI 烂代码」的工具，自身约一半提交由 Cursor、Devin 等 AI agent 写成。

## 值得关注的理由

- **精准踩中时代痛点**：AI 写 React 越来越多，但常踩反模式（误用 useEffect、缺 memo、prop drilling、硬编码密钥…）。React Doctor 用**确定性规则引擎**（可复现、可信任、快、可离线）兜底，刻意区别于不可复现的 LLM 审查——`npx react-doctor@latest` 零安装即用，输出 0-100 健康分。4 个月涨 1.2 万 star、登上 GitHub Trending 第 7。
- **全渠道分发 + agent 自查闭环（工程野心）**：一套 core 规则引擎裂变为 CLI + oxlint/eslint 插件 + LSP + VSCode/Zed 扩展 + GitHub Action + **agent skill**，形成「**agent 写代码 → agent 用 skill 自查 → CI 复核**」的闭环——这是它区别于普通 lint 的核心叙事。
- **知名作者的 React 工具三件套**：Aiden Bai（YC W24，Million Inc）的产品线 **Million.js（编译期优化）→ react-scan（运行时调试）→ react-doctor（静态审查）**，覆盖 React 性能/质量全生命周期，合计 5 万+ star。

## 项目展示

![React Doctor](https://raw.githubusercontent.com/millionco/react-doctor/main/assets/react-doctor-readme-logo-light.svg)

[产品演示视频（npx react-doctor 审计实录）](https://github.com/user-attachments/assets/07cc88d9-9589-44c3-aa73-5d603cb1c570)。官网 [react.doctor](https://react.doctor)。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/millionco/react-doctor |
| Star / Fork | 12346 / 392（爆发型，4 个月达成） |
| 代码行数 | 168K（TypeScript 89.7%；大头是规则定义本身——338 条规则 + 412 测试 + 234 fixture） |
| 项目年龄 | 3.8 个月（2026-02-13 起） |
| 开发阶段 | 密集开发（近 30 天 501 commit，2026-05 单月爆发 427 = v2 发布） |
| 贡献模式 | 创始人主导 + AI agent + 社区（Aiden Bai 占 50.3%，Cursor/Devin AI 合计 ~558 为第二贡献力量） |
| 热度定位 | 大众热门 + 时代风向标（AI 编码时代的 React 确定性代码审查器） |
| 质量评级 | 代码[良好·规则引擎] 文档[良·官网 docs] 测试[强·412 测试文件 + 234 fixture] |
| License | MIT |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

创始人 **Aiden Bai（aidenybai）**，16 岁创办 Million，是 **Million.js（React 优化编译器，~16k star）和 react-scan（React 渲染可视化调试器，~30k star）的作者**——React 性能工具领域的顶级 KOL。公司 **Million Inc（org millionco，YC W24）**累计融资约 14M USD，YC 页定位为「**Tools for agent verification（AI agent 验证工具）**」。react-doctor 正是这条主线的落地，与 Million.js、react-scan 构成「编译期 → 运行时 → 静态审查」的 React 工具三件套。

### 问题判断

随着 Cursor、Devin、Claude Code 等 AI agent 写的 React 代码激增，一个新问题浮现：**AI 写得快但常写得烂**——它们高频踩 React 的状态/副作用/性能反模式，而现有的 ESLint 规则和 coding agent 自身都漏掉很多 React 特有问题。Aiden Bai 看到的缺口是：**需要一个 React 专精、确定性、面向 AI 时代的代码审查器**——确定性意味着可复现可信任（不像 LLM 审查那样飘忽），React 专精意味着能抓通用 lint 抓不到的 React 反模式，面向 AI 时代意味着要能被 agent 当 skill 消费、形成自查闭环。时机上，AI 编码爆发 + oxlint 等快速 Rust lint 引擎成熟，正是做这层「确定性质量基础设施」的窗口。

### 解法哲学

- **明确选择确定性而非 LLM**：规则引擎可复现、快、免费、可离线——刻意与不可复现的 LLM PR 审查区分。
- **明确选择建于 oxlint（而非自造）**：复用 Rust 的 oxc/oxlint 做 AST 解析与执行（快 50-100x），自己专注规则。
- **明确选择「互补而非取代」现有 lint**：尊重并复用已有 ESLint/oxlint 配置，CI 模式只报「本次新引入的问题」而非历史 backlog。
- **明确选择全渠道分发 + agent skill**：一套规则铺满 CLI/插件/LSP/编辑器/CI/agent，让 agent 能自查。
- **明确选择 Effect-TS 做架构骨架**：用函数式副作用编排组织引擎。

### 战略意图

react-doctor 是 Million Inc「agent 验证工具」战略的旗舰开源项目。`packages/api` + `website`（react.doctor）暗示 hosted/团队版云端能力在建（官网未公布定价）——典型「开源 CLI/插件获客 → 云端团队版变现」路径。它与 Million.js、react-scan 的 5 万+ star 受众形成交叉引流，并把「AI 写代码需要确定性质量兜底」做成了可消费的产品。

## 核心价值提炼

### 创新之处

1. **面向 AI 时代的「agent 自查闭环」**（最值得关注）：把规则引擎做成 agent skill，让 AI agent 在自己写的代码上跑 React Doctor 自查，配合 CI Action 复核——「AI 生成 → AI 自查 → CI 复核」闭环，是它区别于普通 lint 的核心叙事。
2. **338 条 React 专精规则，覆盖 5 维度**：Bugs 167（49%）+ Performance 64 + Maintainability 55 + Accessibility 43 + Security 9；按域覆盖 react-builtins/a11y/state-and-effects/react-native/nextjs/tanstack 等 React 全家桶。230 条原创（主打 AI 高频踩的反模式）+ 108 条从 jsx-a11y/react-hooks 等移植收编。
3. **建于 oxlint 的全渠道分发**：一套 core 引擎 → CLI + oxlint/eslint 双插件 + LSP + VSCode/Zed + CI Action + agent skill，写一次规则铺满所有开发者触点。
4. **确定性 + 健康分**：可复现、快、离线，输出 0-100 体检分与 actionable 修复建议（如推荐 React.lazy()/useReducer）。

### 可复用的模式与技巧

1. **规则引擎 → 全渠道分发**：一套规则铺满 CLI/lint 插件/LSP/编辑器/CI/agent skill——任何想最大化触达的开发者工具都可借鉴。
2. **agent skill 自查闭环**：把工具做成 agent 能消费的 skill，让 AI 生成后自检——AI 编码时代质量工具的新范式。
3. **建于成熟引擎做上层产品**：复用 oxlint 的解析/执行，自己专注规则与产品——不重造轮子。
4. **CI 只报增量**：只报本次改动新引入的问题，避免历史 backlog 淹没——务实的渐进式采用。

### 关键设计决策

- **确定性 vs LLM**：选确定性换可复现/快/免费/离线，代价是不如 LLM 理解语义——但对「规则可抓的反模式」足够，且可信任。
- **押注 oxlint（132 改动 ≫ eslint 11）**：明确押注新一代 Rust lint，而非守旧 ESLint。
- **AI 快速堆量 + 创始人把关**：用 Cursor/Devin 快速铺规则/堆量，创始人把控方向与质量闸——这也是 5 月单月 427 commit、深夜提交 41.7% 的成因。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | React Doctor | ESLint + react-hooks | Biome / oxlint | LLM 审查（CodeRabbit 等） |
|------|--------------|----------------------|----------------|---------------------------|
| React 专精 | ✓ 338 规则 5 维度 | ✓ 但面向人写、维度窄 | ✗ 通用 lint | 语义但非 React 专精 |
| 确定性 | ✓ | ✓ | ✓ | ✗ 不可复现 |
| 速度 | 快（建于 oxlint） | 慢 | 极快 | 慢 |
| 面向 AI agent | ✓ agent skill 自查 | ✗ | ✗ | 部分 |
| 成本 | 免费/离线 | 免费 | 免费 | 付费/联网 |

### 差异化护城河

护城河 =「**React 专精 + 五维度 + 确定性 + 全渠道分发 + agent skill 自查闭环 + 知名作者三件套交叉引流**」。lint 通用赛道是红海（ESLint/Biome/oxlint），但「React 专精 + 面向 AI agent 自查」是别人尚未占据的差异化定位。加上 Aiden Bai 的 5 万+ star 受众与「编译期/运行时/静态」产品矩阵，短期难复制。

### 竞争风险

- **被现有 lint/agent 吸收**：eslint-plugin-react-hooks 或 Cursor/Claude 等若内置更强的 React 规则，会蚕食其空间。
- **确定性规则的边界**：规则抓不到的语义级问题仍需 LLM；误报/漏报率是规则引擎的长期挑战（fix 占 43% 印证持续打磨）。
- **早期 + 商业化未明**：4 个月的项目，云端/团队版定价未公布，可持续性待观察。
- **AI 堆量的质量风险**：约一半 commit 由 AI agent 写，质量把控依赖创始人。

### 生态定位

它是「AI 编码时代的 React 确定性代码审查器」，填补了「现有 lint 漏掉的 React 问题 + 面向 agent 自查」的空白，是 AI 编码质量基础设施的早期标杆。

## 套利机会分析

- **信息差**：不算被低估（已当红），但叙事价值极高——「AI 写代码需要确定性质量兜底」+「抓 AI 烂代码的工具自己一半是 AI 写的」自指反讽，是 AI 编码时代的标志性案例。
- **技术借鉴**：「规则引擎全渠道分发」「agent skill 自查闭环」「建于 oxlint 做上层」「CI 只报增量」可迁移到任何开发者质量工具。
- **生态位**：用 AI agent 写 React 的团队、跑 CI 需自动审查的组织，这是现成兜底；想理解「AI 编码质量基础设施」的人，这是优质样本。
- **趋势判断**：AI 编码 + 代码质量是明确上升方向，react-doctor 凭确定性 + agent skill + 作者背书抢占先机；但规则边界、商业化、被吸收是变量。

## 风险与不足

- **确定性规则的天花板**：抓不到语义级问题，误报/漏报是长期挑战（fix 43% 印证持续修规则）。
- **AI 自举的质量依赖创始人把关**：约一半 commit 由 Cursor/Devin 写，方向与质量靠 Aiden Bai 把控。
- **早期 + 商业化未明**：3.8 个月项目，云端/团队版定价未公布，长期可持续性待证。
- **可能被吸收**：通用 lint 或 coding agent 内置 React 规则会削弱其差异化。
- **测试虽多但 commit 无 test 前缀**：412 测试 + 234 fixture 真实存在，但需关注规则正确性的持续验证。

## 行动建议

- **如果你要用它**：你用 AI agent 写 React、或要在 CI 自动审查 React 质量——`npx react-doctor@latest` 零成本试，按需接入 oxlint/eslint 插件、LSP 编辑器扩展、GitHub Action 或 agent skill（让 agent 自查）。它互补而非取代现有 lint。要语义级深度审查仍需 LLM 工具；要通用快速 lint 用 Biome/oxlint。
- **如果你要学它**：重点读 `packages/oxlint-plugin-react-doctor/src/plugin/rule-registry.ts`（338 规则注册表）、`packages/core`（规则引擎，Effect-TS 架构）、`packages/react-doctor`（CLI），以及 `skills/react-doctor`（agent skill 形态）。这是「规则引擎 + 全渠道分发 + agent 自查」的范本。
- **如果你要 fork/贡献它**：最有价值的方向是新增/打磨规则（架构对此友好，注意误报）、为更多框架（如 Solid/Vue 思路迁移）做专项，以及改进 agent skill 自查体验。

### 知识入口

| 资源 | 链接 |
|------|------|
| 官网 / 文档 | https://react.doctor/docs ｜ 零安装 `npx react-doctor@latest` |
| DeepWiki | https://deepwiki.com/millionco/react-doctor （已收录） |
| Zread.ai | 未确认（探测 403） |
| 关联项目 | [Million.js](https://github.com/aidenybai/million)（编译期优化）｜ [react-scan](https://github.com/aidenybai/react-scan)（运行时调试） |
| 背景 | [Million — YC W24（Tools for agent verification）](https://www.ycombinator.com/companies/million) ｜ [React Doctor 评测 — BetterStack](https://betterstack.com/community/guides/scaling-nodejs/react-doctor/) |

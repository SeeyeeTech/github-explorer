# GitHub 推荐：不到两个月 237 次提交：ego-lite 把浏览器变成 Agent 的共享工作区

> GitHub: https://github.com/citrolabs/ego-lite

## 一句话总结

ego-lite 不是又一个 Playwright 封装，而是一个**本地优先的 Chromium Agent 运行时**：让人和 AI Agent 在同一浏览器中共享登录态，却通过 Task Space 隔离工作区并可交接控制权。

## 值得关注的理由

- **产品方向明确**：把「Agent 需要用户真实登录态」和「用户不想被 Agent 抢走浏览器」合并成一个基础设施问题，定位在本地浏览器、Agent Skill 与 CDP 自动化的交叉点。
- **迭代速度极快**：项目首次提交距今约 **1.9 个月**，已有 **237 个 commit**、14 个 tag、13 个 Release，近 30 天仍有 95 个 commit。
- **有可迁移的架构经验**：无状态 CLI + 有状态浏览器、AX Tree + backendNodeId 语义引用、transient/permanent 错误分类、可验证的站点 learning pack，都不只适用于浏览器自动化。

## 项目展示

![ego lite banner](https://raw.githubusercontent.com/citrolabs/ego-lite/main/docs/assets/banner.png)

项目定位：为人和 Agent 共同使用而设计的本地浏览器。

![ego lite vs agent-browser benchmark](https://raw.githubusercontent.com/citrolabs/ego-lite/main/docs/assets/ego-vs-agent-benchmark.png)

README 中的性能对比图：作者用复杂网页任务比较 ego-lite 与 agent-browser。

![Star History Chart](https://api.star-history.com/chart?repos=citrolabs/ego-lite&type=date&legend=top-left)

项目 Star 增长曲线。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/citrolabs/ego-lite |
| Star / Fork | 3,736 / 187 |
| 代码行数 | 23,875（JavaScript 54.1%、TypeScript 33.8%、JSON 6.4%、CSS 3.6%、HTML 1.2%、Shell 0.7%、YAML 0.2%） |
| 项目年龄 | 约 1.9 个月（首次提交 2026-05-29；仓库创建于 2026-04-16） |
| 开发阶段 | 密集开发 |
| 贡献模式 | 小团队主导，6 位贡献者，主作者约占 42.5% commit；网络数据中 Top contributor 占近期贡献约 61.8% |
| 热度定位 | 中等热度，但以不到两个月的年龄看属于早期爆发项目 |
| 质量评级 | 代码良好，文档优秀，测试充分，CI/CD 完善 |
| License | MIT |
| 最新版本 | v1.2.5-beta.1（14 个 tag，13 个 Release） |

项目最近 30 天有 95 次提交，6 月单月约 144 次提交；周末提交占 5.1%，深夜提交占 14.3%，更接近职业团队的工作节奏，而非单人业余项目。commit 中 Fix 20.0%、Feature 17.5%、Docs 15.5%，说明当前重点已经从单纯堆功能转向快速修正、文档打磨和发布流程建设；不过 Test 仅占 2.5%，仍应关注真实浏览器场景的覆盖深度。

## 作者视角：为什么存在这个项目

### 创始人/作者背景

CitroLabs 是位于新加坡的年轻开源组织，账号创建于 2025 年 9 月，公开资料以「Future of Personal Computing」为定位，博客为 citrolabs.ai。仓库在组织最近活跃项目中投入权重最高，贡献者以小团队为主。

从产品叙事、Chromium fork 边界和 Skill 设计看，作者更像是从真实 Agent 工作流中发现问题：Playwright 或 headless 浏览器能驱动网页，却不能自然解决「Agent 需要用户已经登录的 SaaS」以及「用户还要继续使用自己的浏览器」这两个问题。

### 问题判断

传统浏览器自动化通常把浏览器当作一次性、无头、独占的执行环境；而 AI Agent 的任务往往需要真实登录态、人工验证码和长时间的多轮执行。ego-lite 的判断是：**浏览器应该成为人和 Agent 共同工作的个人计算基础设施**，而不是每个 Agent 都临时启动一份隔离浏览器。

这个时机也与 Agent CLI 的普及相吻合。Claude Code、Codex、Cursor 等工具开始成为开发者工作流入口，浏览器正从「测试目标」变成 Agent 的通用操作界面。

### 解法哲学

- **本地优先，而不是托管优先**：数据和登录态保留在本机，换取隐私、低延迟和无需凭据迁移；代价是安装、OS 适配和远程扩展能力较弱。
- **一次性编程，而不是逐条命令堆叠**：Agent 可以在一次 JavaScript 中组合 `snapshot`、`click`、`fill`、`wait`、`cdp` 等能力，减少「调用—观察—再调用」的工具往返；代价是过程可见性和调试门槛更高。
- **隔离与交接，而不是简单共享 Tab**：Task Space 记录 Agent/用户 ownership，支持 handoff、takeover 和 keep/close 生命周期；代价是 renderer、资源和状态回收明显更复杂，Issue #88 已暴露 renderer 泄漏问题。
- **轻依赖、直接 CDP**：运行时不依赖 Puppeteer/Playwright，把控制面压到 CDP 和自研 helper；代价是跨浏览器兼容性、调试工具和长期维护能力不如成熟框架。
- **渐进增强**：普通网页使用语义 Snapshot，富文本编辑器可以退回截图和键盘，特殊场景再使用 `js`/`cdp`，没有假设单一 DOM 抽象能覆盖所有网站。

### 战略意图

ego-lite 更像 CitroLabs「Future of Personal Computing」愿景中的开发者入口和连接层，而不只是一个 npm 包。开源部分采用 MIT，开放 TypeScript runtime、Skill、站点 learning pack 和 CI；**Chromium 应用作为独立下载物分发**。

这种「开源连接层 + 受控浏览器产品」的边界，为 MCP、Linux、Vertical Tabs、per-instance proxy 以及未来的托管/企业能力留下了产品化空间。但目前仓库尚未证明明确的付费路线，不能把潜在的 open-core 路径当成既成事实。

## 核心价值提炼

### 创新之处

1. **Task Space + ownership/handoff：浏览器内的 Agent 协作操作系统**
   - 将浏览器自动化从「控制一个 Tab」提升为「人和多个 Agent 共享登录态、各有隔离工作区、可交接控制」。
   - 新颖度 5/5；实用性 5/5；可迁移性 5/5。

2. **AX Tree + backendNodeId 的低 token Snapshot ref**
   - 将页面语义快照映射为短 `@N` 引用，保存 backend node、role、name、frame 等信息；节点失效后按错误类型刷新或回退定位。
   - 相比简单序号或 CSS 选择器，它更适合 DOM 频繁重排的 SPA 和模型驱动操作。
   - 新颖度 4/5；实用性 5/5；可迁移性 4/5。

3. **Skill 作为可执行经验层**
   - `manifest.json` 声明 domains、notes、Node tools 和 browser tools；验证器与 CI 检查 URL、工具 schema 和目录边界，把一次性 prompt 经验变成可审查、可版本化资产。
   - 新颖度 4/5；实用性 5/5；可迁移性 5/5。

4. **无状态前端 + 有状态浏览器后端**
   - 每次 CLI 运行都是短命 Node 进程，Tab、登录态和 Space 留在 Chromium 后端；进程失败不必重启浏览器，但需要重新 attach。
   - 新颖度 4/5；实用性 5/5；可迁移性 5/5。

5. **事件缓冲与高吞吐事件分流**
   - 通用 CDP 事件进入有上限的 buffer，`Page.screencastFrame` 等高吞吐事件在有订阅者时走独立路径，避免录屏帧拖垮导航和下载等待。
   - 新颖度 4/5；实用性 4/5；可迁移性 4/5。

### 可复用的模式与技巧

1. **状态后端、短命前端**：把不可丢失的状态放到长期服务，CLI 只提交可重放脚本。
2. **语义 ref + 稳定 locator 双层定位**：短期动作使用紧凑 ref，跨轮次使用 role/CSS/href；失效时按错误类别恢复。
3. **Transient/permanent 错误分类**：等待中的「尚未出现」可以重试，非法选择器或多匹配应尽快失败。
4. **单一 helper surface**：由 `helperContext()` 同时服务 CLI、SDK、Skill 文档和测试，减少能力漂移。
5. **能力模块 + 注入 state**：driver 按 pointer、waits、nav、observe 等能力切分，通过 FakeEgo 和 state overrides 测试，不必每次启动真实浏览器。
6. **可验证经验包**：manifest + notes + 可执行 tools + path sandbox + CI validator，将提示词资产变成插件资产。
7. **显式 human-in-the-loop 状态机**：用 ownership、handoff、takeover、complete/keep 表达用户控制权。
8. **事务性输出**：运行期间缓冲日志，成功后统一 flush，脚本失败则丢弃半成品输出，避免下游误消费。

### 关键设计决策

1. **用 CDP backend node 保存模型引用**
   - 问题：DOM 重排会让序号和 CSS 选择器不稳定。
   - 方案：Snapshot 把 AX/DOM 信息映射为 `@N`，`RefMap` 记录 backend node；解析失败时按 role/name 回退。
   - Trade-off：低 token、动作稳定性更好，但依赖 Chromium/CDP，跨导航和跨 iframe 仍会失效。

2. **将 role 定位与 DOM 定位分成两条路径**
   - 问题：AI 需要语义定位，工程脚本需要 CSS/XPath 等精确定位。
   - 方案：role 走 Accessibility Tree，CSS/XPath/text 走 Runtime.evaluate，并由 `ElementResolutionError` 区分 transient/permanent。
   - Trade-off：语义能力更强，但 AX Tree 扫描成本较高，且依赖页面可访问性质量。

3. **用统一 helper context 同时支持 CLI 和嵌入 SDK**
   - 问题：多套 API 容易与 Skill 文档不一致。
   - 方案：`helpers.ts` 汇总 driver、Task Space、learning、fetch 和 CDP helper，`run.ts` 注入 AsyncFunction，`index.ts` 负责 SDK 安装和兼容。
   - Trade-off：调用简洁，但全局注入增加隐式依赖、命名冲突和兼容层维护成本。

4. **用 capability-scoped driver 替代巨型 Browser 类**
   - 问题：导航、输入、观察、等待、下载、录屏等能力变化速度不同。
   - 方案：`driver/` 按能力拆分，依赖共享 CDP、resolver 和 state。
   - Trade-off：边界清晰、局部测试容易，但 singleton state 对多实例并发隔离不够理想。

5. **把站点知识限制在 schema 和路径沙箱内**
   - 问题：站点经验需要复用，同时不能把 secrets、像素坐标和不可审查的任务日记带入 Skill。
   - 方案：manifest 声明工具与参数，learning loader 只允许站点目录内相对路径，CI 负责校验。
   - Trade-off：经验可审查、可发布，但站点改版会导致知识陈旧，复杂工具的安全性仍依赖代码审查。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | ego-lite | Browserbase Skills | Vercel agent-browser | Playwright / Puppeteer |
|------|---------|-------------------|----------------------|------------------------|
| 核心定位 | 本地浏览器 + 外部 Agent 协作 | 云端浏览器基础设施 | 通用 Agent 浏览器 CLI | 通用浏览器自动化底层 |
| 登录态 | 复用本地真实登录态 | 远程 session/凭据 | 通常是独立浏览器上下文 | 需自行管理 context |
| 人机并行 | Task Space + ownership/handoff | 远程/云端协作 | 无同等 Space 协议 | 非核心能力 |
| 部署形态 | 桌面端，本地优先 | 云端，易扩展 | 本地或 CI，通用 | 本地/CI，生态成熟 |
| Agent 适配 | Snapshot ref、一次性 JS、Skill | 面向云端 Agent | CLI/浏览器自动化抽象 | 需要自行加模型适配层 |
| 主要优势 | 隐私、低延迟、真实会话 | 浏览器池、弹性、托管 | 独立于特定浏览器产品 | 生态、兼容性、工具链 |
| 主要短板 | OS/安装限制，Chromium fork 负担 | 成本、延迟、登录态出机 | 无本地 Space，生态仍在成长 | 不解决 Agent 与用户共享浏览器 |

### 差异化护城河

技术护城河是 Chromium fork 的内核级 Snapshot、`ego` bridge 和本地 Space/ownership 协议；产品护城河是「真实浏览器 + 外部 Agent + 人机并行」的组合。SkillHub/ClawHub 分发和 site learnings 可能形成生态护城河，但目前仍早期，且浏览器二进制独立分发、平台限制和闭源边界削弱了社区完全替代的能力。

### 竞争风险

最现实的替代者取决于场景：无头 CI 和通用自动化会优先选择 agent-browser、Playwright/Puppeteer；云端规模化会选择 Browserbase、Steel 等；普通用户则可能选择内置 Agent 的 AI 浏览器。如果大型 AI 浏览器开放外部 Agent 控制，并解决真实登录态共享，ego-lite 的核心差异将被压缩。

### 生态定位

ego-lite 位于「本地浏览器产品」「Agent Skill/插件」「CDP 自动化底层」三者交叉处，填补的是「个人浏览器成为多 Agent 工作空间」这一细分空白，不是传统测试框架的直接替代品。

## 套利机会分析

- **信息差**：3,736 stars 对不到两个月的项目并不低，但相对通用自动化框架仍处于早期窗口；「本地登录态 + Agent 协作」的叙事比单纯速度 benchmark 更值得关注。
- **技术借鉴**：可直接借鉴无状态 CLI/有状态后端、语义 ref、错误可恢复性分类和事务性输出。
- **生态位**：为个人设备上的 Agent 提供浏览器连接层；未来 MCP、Linux、代理隔离和站点 learning pack 是扩展点。
- **趋势判断**：方向符合 Agent CLI、浏览器 Agent 和本地隐私计算的交汇趋势；但能否穿越早期热度，取决于跨平台、资源回收、浏览器稳定性和生态开放程度。

## 风险与不足

1. **项目仍处于快速收敛期**：1.9 个月、237 commits、helpers.ts 和 SKILL.md 高频修改，说明 API 和核心行为仍可能变化。
2. **Renderer 生命周期是硬问题**：Issue #88 暴露 Task Space 清理不彻底。多 Agent 并发模型如果不能可靠回收 renderer，长期运行会损耗内存并降低用户信任。
3. **平台覆盖不足**：Vertical Tabs、macOS 窗口适配和 Linux 支持都在路线图/Issue 中，当前更像桌面端早期产品，而非跨平台基础设施。
4. **开源边界限制复现**：开源的是 runtime、Skill 和 harness，完整 Chromium 应用独立分发；仅 clone 仓库不能完全复现核心浏览器能力。
5. **生态成熟度不及通用框架**：直接 CDP 带来控制力，也带来版本兼容、调试和长期维护成本；Playwright/Puppeteer 的生态优势很难短期追平。
6. **站点知识有维护成本**：learning pack 能显著减少重复试错，但网站改版会造成陈旧知识，且可执行工具需要持续审计。
7. **贡献集中度偏高**：小团队和核心贡献者占比高，单一团队或关键维护者变化可能显著影响路线和修复速度。

## 行动建议

- **如果你要用它**：当你的任务需要本机真实登录态、隐私敏感的 SaaS 操作、人工验证码介入，或希望 Agent 后台工作而自己继续浏览时，值得试用。若目标是云端批处理、无头 CI、跨平台部署或成熟测试基础设施，应优先考虑 Playwright、agent-browser 或 Browserbase。
- **如果你要学它**：先读 `package/ego-browser/src/helpers.ts`、`src/browser-runtime.ts`、`src/element-resolver.ts`、`src/ref-map.ts`、`src/ref-state.ts`，再读 `src/driver/{pointer,waits,nav,observe}.ts`；最后看 `skills/ego-browser/SKILL.md` 和 `learning/`，理解「代码 API—Agent 契约—站点经验」如何联动。
- **如果你要 fork 它**：优先补齐 renderer/Space 生命周期监控和回收、Linux/跨平台支持、MCP Server、并发实例隔离与可观测性；其次建立公开的真实浏览器 benchmark 和更明确的浏览器二进制开源/复现边界。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/citrolabs/ego-lite |
| Zread.ai | 未收录 |
| 关联论文 | 无 |
| 在线 Demo | https://lite.ego.app（可下载客户端，无在线 Playground） |

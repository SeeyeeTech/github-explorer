# 两人 4 个月 21k 星的 cmux：专治「10 个 AI agent 同时等你」的终端

> GitHub: https://github.com/manaflow-ai/cmux

## 一句话总结

cmux 是 YC S24 两人创业公司 manaflow-ai 的开源旗舰——一个基于 Ghostty 内核的原生 macOS 终端，专门解决「同时并行跑 5-10 个 Claude Code/Codex 时，到底哪个 agent 在等我」这个 2024 年才出现的注意力管理新痛点；它站在 Ghostty 肩上只补「agent 编排外壳」这一层，4.5 个月冲到 21k 星，连 Ghostty 作者 Mitchell Hashimoto 都公开点赞。

## 值得关注的理由

1. **AI agent 时代终端形态进化的标杆案例**：把「多 agent 并行时的人类注意力」当成一等需求，是讲透「为什么 tmux 不够用了」的最佳载体。
2. **「站在巨人肩上」的范围控制范本**：复用 libghostty 拿原生 GPU 终端 + 零成本读用户已有 Ghostty 配置，自己只写差异化的 agent 层——克制的工程边界值得学。
3. **「如何用 AI agent 严肃开发 36 万行 Swift 原生 app」的方法论样本**：52KB 的 CLAUDE.md「架构宪法」+ ~31% 测试占比，是 AI 辅助研发的现成参考。

## 项目展示

![cmux 主界面](https://raw.githubusercontent.com/manaflow-ai/cmux/main/docs/assets/main-first-image.png)

> cmux 主界面：垂直侧边栏聚合各 agent 会话的 git 分支、PR 状态、端口与通知。

![通知蓝环](https://raw.githubusercontent.com/manaflow-ai/cmux/main/docs/assets/notification-rings.png)

> 核心卖点「通知蓝环」：哪个 pane 的 agent 在等你输入，一眼可见，`⌘⇧U` 直接跳最近未读。

![垂直/水平标签与分屏](https://raw.githubusercontent.com/manaflow-ai/cmux/main/docs/assets/vertical-horizontal-tabs-and-splits.png)

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/manaflow-ai/cmux |
| Star / Fork | 21,363 / 1,620 |
| 代码行数 | 自写约 36 万行 Swift（Sources 27.6万 + Packages 8.7万）+ Go daemon；tokei 报 768k 系历史误提交 node_modules 灌水，已甄别 |
| License | GPL-3.0-or-later（另提供商业授权） |
| 项目年龄 | 4.5 个月（首次提交 2026-01-22，原名「GhosttyTabs」后改名） |
| 开发阶段 | 密集开发 / 创业冲刺（近 30 天 1,862 commits，5 月峰值单月 1,486） |
| 贡献模式 | 双创始人主导（Lawrence Chen + Austin Wang，主作者 47%，名义 120 贡献者） |
| 热度定位 | 大众热门（爆发型：2 周 17k 星、HN #2） |
| 质量评级 | 工程纪律「优秀」 测试「优秀（~31%）」 god 文件「技术债」 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

开发方是 **manaflow-ai**——YC Summer 2024（S24）批次的两人创业公司，自我定位「开源应用 AI 实验室」。创始人 **Austin Wang（CEO）** 与 **Lawrence Chen** 即仓库绝对核心（合计绝大多数 commit）。配套生态完善：homebrew-cmux、cmux-skills、ghostty fork、20+ 语种 README、Discord、文档站、Sparkle 自动更新。可信度高（YC 背书 + Ghostty 作者 Mitchell Hashimoto 公开点赞 + 被 Nvidia/Google/OpenAI 工程师使用）。

### 问题判断

教科书级 dogfooding。README「Why cmux」是第一人称真实痛点：「我并行跑大量 Claude Code 和 Codex，用 Ghostty + split panes，但 Claude Code 的通知永远只是『Claude is waiting for your input』毫无上下文，标签多到看不清标题。」**tmux 只给复用、不给「跨会话的状态聚合视图」**；原生通知因千篇一律而失效。当你同时跑 10 个 agent，终端无法回答「现在哪个在等我、它是哪个分支/PR/端口」——这就是 cmux 要补的缝。

### 解法哲学

三条自洽主张：① **「cmux is a primitive, not a solution」**——「没人想清楚 agent 的最佳工作流，所以别自上而下设计死工作流」，只给可组合原语（终端/浏览器/通知/工作区/分屏/CLI）；② **原生 Swift/AppKit 拒绝 Electron**（「Electron/Tauri 的性能困扰我」）；③ **站在 Ghostty 肩上只补 agent 层**（复用 libghostty + 直接读 `~/.config/ghostty/config`，零迁移成本）。

### 战略意图

清晰的开源引流漏斗：GPL-3.0 开源旗舰做流量与口碑 → GPL copyleft 逼不兼容的企业买**商业授权** → **Founder's Edition 订阅**卖 early access（cmux AI、iOS app、Cloud VMs、Voice mode，这些功能仓库里已有大量代码）→ 母公司 manaflow 主产品。开源 cmux 是把开发者圈进生态的「楔子」。

## 核心价值提炼

### 创新之处

1. **agent-aware 终端（蓝环 + 侧栏 agent 状态 + ⌘⇧U 跳未读 + OSC/CLI 双通道）**：把「多 agent 并行时的人类注意力」当一等需求落地，是这个品类的定义性功能。新颖度 4/5 · 实用性 5/5 · 可迁移性 4/5。
2. **snapshot-boundary SwiftUI 性能模式**：从生产事故（#2586 列表 100% CPU 自旋）提炼出「行只吃不可变 value 快照 + 闭包动作包 + Equatable 行，store 引用绝不下沉」的可机械检查铁律——对整个 SwiftUI 社区有价值。新颖度 4/5 · 实用性 5/5 · 可迁移性 5/5。
3. **内置可脚本 agent 浏览器**：把浏览器无障碍树 + JS eval + click/fill 通过 socket 暴露给终端里的 agent（移植自 vercel-labs/agent-browser），与终端同窗共享登录态——比让 agent 自起 headless Chromium 顺手得多。新颖度 4/5 · 实用性 4/5 · 可迁移性 3/5。
4. **52KB CLAUDE.md「AI 协作宪法」**：用一份强约束文档同时治理人类与 AI reviewer（Codex/CodeRabbit/Greptile），含分层 DAG、Swift 6 并发铁律、测试红/绿两提交纪律。新颖度 4/5 · 实用性 4/5 · 可迁移性 4/5。

### 可复用的模式与技巧

1. **高频事件 → 单 pending 任务合并到 UI 线程**：`scheduleTick` 把 Ghostty 千次/秒的 wakeup 合并成至多一个主队列 tick；PortScanner 把所有 pane 的扫描合并成 200ms 窗口一次——任何「事件风暴打爆主线程」场景通用。
2. **snapshot-boundary 列表渲染**：长列表行只吃 value 快照 + 闭包包 + Equatable——SwiftUI/Compose/任何 diff 型 UI 都能借鉴。
3. **跨 C ABI 资源的 actor 化异步释放 + 超时探测**：`TerminalSurfaceRuntimeTeardownCoordinator` 非主线程串行释放原生句柄、5 秒超时只报告不阻塞——封装任何 C/Rust/Zig 库生命周期可参考。
4. **agent 状态双通道**：标准 OSC 9/99/777 做被动信号 + 自建 `cmux notify` CLI/socket 做主动富信号 + 可抑制去重——任何 agent-aware 工具都能照搬。
5. **CLI/socket 作为可编程控制面**：515 个命令 case，GUI 每个动作都暴露成 socket method，使「人用 GUI / agent 用 CLI」共用一套 action 路径。

### 关键设计决策

- **libghostty 的 Swift 封装（白嫖内核 + 接管语义）**：不自写终端模拟器，把 Ghostty 编译成 xcframework 经 C 互操作驱动；关键缝合点是把 Ghostty 解析出的 OSC 通知 action 截获、路由到自己的 `TerminalNotificationStore`。Trade-off：零成本拿到世界最快终端内核，代价是强绑上游 Zig 子模块 + 跨 C ABI 内存生命周期易出 bug。可迁移性中。
- **架构「迁移中」：god 文件 → 39 个 SPM 包的分层 DAG**：CLAUDE.md 是目标态（五层 DAG + `@Observable` + 构造注入），代码现实仍 god 文件主导（`ContentView`/`Workspace`/`TabManager` 被自己点名为反面教材），策略是「leaf-first 抽取」。这种「知道自己烂在哪并写进宪法去治」的自觉本身是质量信号。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | cmux | Warp | Ghostty | Vibe Kanban |
|------|------|------|---------|-------------|
| Stars | 21.4k | 61k(仅 issues 仓) | 56k | 26.8k |
| 形态 | 原生 macOS 终端 | AI 终端(闭源) | 通用快终端 | Web 编排器 |
| 定位 | 托管别人家 agent | 终端即 AI 产品 | 通用内核 | 看板式 agent 编排 |
| 开源 | GPL-3.0 | 闭源 | MIT | 是 |
| 跨平台 | 仅 macOS | mac/Linux/Win | 跨平台 | 跨平台 |

### 差异化护城河

① 原生 Swift 性能 + Ghostty 配置零迁移；② GPL-3.0 copyleft → 商业授权的法律护城河；③ **「托管别人家 agent」的中立定位**——不与 Claude Code/Codex 正面竞争，反而吃它们的红利；④ 21k 星 + Ghostty 作者背书的早期社区势能。

### 竞争风险

① **仅 macOS**——直接放弃 Linux 开发者这一终端重镇；② **依赖 Ghostty 上游**——内核命脉不在自己手里，需常年维护 fork；③ **超高 churn**（4646 commits、1.2k+ open issues、单仓库塞 mac+iOS+web+daemon+cloud）的维护熵；④ **两人核心团队**的 bus factor；⑤ Warp 等资金充裕玩家若补「多 agent 注意力管理」会快速侵蚀差异点。

### 生态定位

「AI agent 编排终端」这个 2024+ 新品类里**原生派的开源旗舰**，卡位在 Ghostty（内核）之上、Claude Code/Codex（agent）之外的「注意力与编排外壳」层。

## 套利机会分析

- **信息差**：已被充分发现（2 周 17k 星、HN #2、名人背书），**不是冷门标的而是当红风口**——价值在「讲透趋势」而非「挖掘冷门」。
- **技术借鉴**：snapshot-boundary 性能模式、高频事件合并、跨 C ABI actor 释放、OSC+CLI 双通道、CLI 控制面，都能直接搬到自己的原生 app / agent 工具。
- **方法论借鉴**：52KB CLAUDE.md 是「AI 辅助开发严肃原生 app」的现成宪法模板。
- **趋势判断**：「为 AI agent 重做终端」是真趋势，但 macOS-only + 依赖 Ghostty + 两人团队是结构性天花板；看点是能否在 Warp 反扑前把生态护城河做厚。

## 风险与不足

- **代码体量被严重高估**：tokei 的 768k 行含历史误提交的 node_modules（GitHub linguist 实测 JS 仅 0.3%），真实自写约 36 万行 Swift（其中 ~31% 是测试）。
- **god 文件技术债**：`CLI/cmux.swift` 单文件 3.2 万行（515 命令）、`Workspace.swift` 1.97 万行等多个 1.5-2 万行巨型文件，团队已显式承认。
- **提交规范弱**：~80% 提交无 conventional 前缀、merge 占主导，靠 PR 号补救可追溯性。
- **结构性天花板**：仅 macOS、命脉绑 Ghostty 上游、两人 bus factor、单仓库复杂度高。

## 行动建议

- **如果你要用它**：macOS 上重度并行跑 Claude Code/Codex 的开发者首选；从 Ghostty 迁入几乎零成本（读同一配置）。非 macOS 用户、要结构化任务编排的选 Vibe Kanban，要 AI 深度集成的商业终端选 Warp。
- **如果你要学它**：重点读 `Sources/GhosttyTerminalView.swift`（libghostty 封装 + tick 合并 + OSC 路由）、`Sources/SessionIndexView.swift`（snapshot-boundary 参考实现）、`CLAUDE.md`（架构宪法）、`CLI/cmux.swift` 的 `cmux notify` 与 `browser` 命令。
- **如果你要 fork 它**：最该改的是拆 god 文件、补 conventional commits；agent 状态双通道与可脚本浏览器是最有价值的内核，可考虑往 Linux 移植填补平台空白。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/manaflow-ai/cmux（已收录） |
| 官方文档 | https://cmux.com/docs/getting-started |
| 设计哲学 | [The Zen of cmux](https://cmux.com/blog/zen-of-cmux) |
| 公司背景 | [Manaflow（YC S24）](https://www.ycombinator.com/companies/manaflow) ·[第三方拆解](https://dev.to/neuraldownload/cmux-the-terminal-built-for-ai-coding-agents-3l7h) |
| Demo | [YouTube 演示](https://www.youtube.com/watch?v=i-WxO5YUTOs) |

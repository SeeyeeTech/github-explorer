# AI 操作软件该看屏幕还是敲命令？港大 42K star 押注命令行

> GitHub: https://github.com/HKUDS/CLI-Anything

## 一句话总结

CLI-Anything 是港大数据智能实验室（HKUDS，LightRAG/nanobot/RAG-Anything 的「Anything 系列」厂牌）的「让所有软件 agent-native」框架——核心论点（arXiv 2606.03854《Towards Agent-Native Computer Use》）直接挑战 GUI-agent 范式：与其逼 AI「看屏幕点鼠标」（像素脆弱、时序依赖、不确定），不如**为 agent 重做软件接口**，把任意软件包成确定性、JSON-first、可组合的命令行。它用一份 36KB 的强约束方法论（`HARNESS.md`）+ CLI-Hub 市场，让社区把 Blender / FreeCAD / LLDB / LibreOffice / 浏览器等 60+ 软件变成 AI 能稳定驱动的 CLI。3 个月 42K star、115 贡献者、Apache-2.0。

## 值得关注的理由

1. **一场清晰的「路线之争」被工程化地押注了**：当主流（Anthropic Computer Use / Self-Operating-Computer）在教 AI 看截图点坐标时，CLI-Anything 反向论证——LLM 是 token 序列专家，让它做「像素→语义」的有损翻译是错配。它把信仰落成可执行契约：每个 harness `--json` 切机器输出、统一 `{"error","type"}` JSON 错误信封 + 退出码、SKILL.md 写死「For AI Agents：始终用 --json、检查返回码、export 后验证产物」。最激进的样板是 **browser harness 把浏览器重构成虚拟文件系统**——用 `ls / cd / cat / grep / click` 操作 Chrome Accessibility Tree（`browser/agent-harness/.../core/fs.py`），用 LLM 最熟的 shell 隐喻正面替换 computer-use 的坐标点击。
2. **几个可直接复用的工程范式**：① **强约束 SOP 当「生成器」**——`HARNESS.md` 36KB 方法论 + `commands/` 里「禁止 improvise，先读 HARNESS.md」+ `guides/` 渐进披露，把开放式 LLM 生成任务流程化（真正的确定性代码只有 Phase 6.5 的 `skill_generator.py`）；② **registry-as-server 市场即分发**——静态 `registry.json` 经 GitHub Pages 托管 + `pip install git+subdirectory`，PR 合并即时上架、零 PyPI 包维护（唯一上架物是 cli-hub 自身）；③ **harness「真包装」**——subprocess 调真后端（核实 119 个文件用 subprocess、46 个文件带 undo/redo），不重新实现功能、session JSON 加排他文件锁。
3. **一个「框架薄、市场厚」的平台样本，但要会拆**：HKUDS 维护的框架核心（cli-hub 仅依赖 click+requests）只占很小比例，27.5 万行 Python 绝大部分是社区贡献的 60 个适配器长尾——真正的护城河是「方法论生成器 + 市场飞轮」，而非适配器数量。同时要客观看待：42K star 有 HKUDS 厂牌 + 论文 + Trendshift 放大（watchers 仅 169），适配器质量高方差，且 4775 个测试**无中心化 CI 闸门**。

## 项目展示

![CLI-Anything Teaser](https://raw.githubusercontent.com/HKUDS/CLI-Anything/main/assets/teaser.png)

![Blender 确定性驱动 demo](https://raw.githubusercontent.com/HKUDS/CLI-Anything/main/assets/demos/blender-orbital-relay-drone-preview-trajectory.gif)

> 上图为项目总叙事，下图为 agent 用确定性 CLI 驱动 Blender 做 3D 建模——最能反驳「CLI 做不了复杂 GUI」。更多 demo（FreeCAD/drawio/游戏/GIS）见仓库 `assets/demos/`。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/HKUDS/CLI-Anything |
| Star / Fork / Watcher | 42,261 / 3,990 / **169**（watchers 极低，star 含厂牌放大） |
| 代码行数 | 237,095 行（Python 93.2%；JSON 3.5% 是注册表数据；C#/Swift/PS 长尾是各软件原生胶水）；1488 文件；注释比 0.179（健康） |
| 项目年龄 | 3.0 个月（2026-03-08「first commit」→ 2026-06-04） |
| 开发阶段 | 密集开发（3 个月 745 commit，月均 ~248；月度 319→294→114 由爆发转稳态） |
| 贡献模式 | 真社区协作（**115 贡献者**，top「yuhao」仅占 23.7%；周末 25.2%、深夜 24.4% 系跨时区所致） |
| 热度定位 | 大众热门 · 爆发型（一周内吸 200+ star，Trendshift 收录） |
| 版本 | v0.3.0（**仅 2 个 tag**——靠 CLI-Hub「市场即分发」，非 git release） |
| License | Apache-2.0 |
| 质量评级 | 文档「优」· 框架核心「良」· 适配器市场「中（高方差）」· 测试「中」· CI「弱（无 harness 测试闸门）」 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

**HKUDS（Data Intelligence Lab @ HKU，港大数据智能实验室）**——Organization，11517 followers、87 个公开仓库，PI 为港大黄超（Chao Huang）。是少数能稳定批量产出万星项目的学术实验室，「Anything / 爆款」矩阵：nanobot 43.8K、LightRAG 36.3K、CLI-Anything 42.3K、RAG-Anything 21K、AI-Trader 19.4K、OpenHarness 13.6K。关键事实：**论文作者 = 代码作者**——arXiv 2606.03854 作者 Yuhao Yang / Tianyu Fan / Chao Huang，其中 Yuhao Yang 正是仓库头号贡献者，`Slay the Spire II` demo 由 Tianyu Fan 本人贡献。不是论文挂名外包代码，而是「学术 + 工程 + 市场」三轮同一批人驱动。

### 问题判断

README「The Agent-Software Gap」直陈三条死路：① 脆弱的 UI 自动化（截图+点击+RPA）；② 残缺的官方 API（只暴露 10% 能力）；③ 为 agent 重写的「玩具实现」（丢失 90% 功能）。核心判断：agent 用真实软件的瓶颈不在模型推理，而在「接口形态」——GUI 是有损的人机界面，强塞给 LLM 等于让 token 序列专家做像素→语义的有损翻译。

### 解法哲学（确定性 CLI > 视觉）

Agent-native 四原则：**结构化命令 > 视觉导航；显式状态 > 截图解读；确定性反馈 > 概率性 UI 识别；程序化控制消除有损的视觉→计算翻译**。这套信仰在代码里有据可查：harness 的 `--json` 双输出、JSON 错误信封 + 退出码、browser harness 的「浏览器即文件系统」。这不是包装 GUI，是把交互模型整个换掉。「Today's Software Serves Humans. Tomorrow's Users will be Agents.」

### 战略意图

HKUDS「Anything 系列」的「论文 + 工程 + 市场」三轮驱动：arXiv 立论 → 代码给参考实现 → CLI-Hub 把社区贡献变即时分发的市场。对竞品取舍清醒——**不取代 MCP**（MCP 管远程 SaaS/鉴权，CLI 管本地成熟工具，`public_registry.json` 甚至收编 MCP 桥），而是去抢 computer-use 视觉路线的地盘。`docs/hub/.well-known/{agent,ai-plugin,agent-card}.json` + `llms.txt` + `openapi.json` 把 Hub 本身也做成「可被 agent 爬取/发现」的 agent-native 资产——平台战略一以贯之。

## 核心价值提炼

### 创新之处

1. **确定性 CLI 取代视觉点击的 agent-native 范式**（新颖度 4/5，实用性 5/5，可迁移性 5/5）：把「为 agent 重做接口」落成可执行工程（`--json` 契约 + JSON 错误信封 + 退出码 + SKILL.md「For AI Agents」段落）。适用任何要让 agent 稳定驱动专业软件的场景。
2. **浏览器 = 文件系统的接口重构**（新颖度 5/5，实用性 4/5）：`ls/cd/cat/grep/click` 操作 Accessibility Tree（`browser/agent-harness/.../core/fs.py`），直接对标并替代 computer-use 的像素点击。适用 web 自动化、表单、抓取。
3. **registry-as-server 市场即分发**（新颖度 4/5，实用性 4/5）：静态 JSON + `pip install git+subdirectory`，PR 合并即上架、零包维护、双注册表跨 pip/npm/brew/uv（`_source` 标签 merge + 1h 缓存 + 离线回退）。适用社区驱动的工具/插件市场。
4. **强约束 SOP 当「生成器」**（新颖度 4/5，实用性 5/5，可迁移性 5/5）：`HARNESS.md` 36KB 方法论 + 「禁止 improvise」+ `guides/` 渐进披露——把开放式 LLM 生成任务流程化、可控化。适用任何复杂 agent skill 的工程化。
5. **代码反射出 agent 可发现的 SKILL.md**（新颖度 3/5，实用性 4/5，可迁移性 5/5）：`skill_generator.py` 正则解析 Click 装饰器 → 技能清单，canonical + 兼容副本双写。
6. **preview / live-preview / trajectory 视觉反馈环**（新颖度 4/5，实用性 4/5）：`preview_bundle.py` 让无 GUI 的 agent 也能产出渲染产物并回放命令轨迹（FreeCAD/Blender demo）。

### 可复用的模式与技巧

- **`--json` 双输出 + JSON 错误信封 + 退出码**：写给 agent 用的 CLI 最小契约——任何 agent-facing CLI。
- **强约束 SOP + 少量确定性脚本**：把开放式 LLM 生成任务流程化——复杂 agent skill 设计。
- **静态注册表 + 薄包管理器 + 直装 git 子目录**：低成本社区市场骨架——插件/工具分发。
- **backend wrapper（`shutil.which` 定位 → subprocess 调用 → 缺失给安装指引）**：stateful CLI 包装黑盒后端。
- **session 文件加排他锁（`_locked_save_json`）**：并发安全的 JSON 状态持久化。
- **`.well-known/agent.json` + `llms.txt` + `openapi.json`**：让自己的网站/服务可被 agent 发现消费——agent-native 产品分发。

### 关键设计决策

最值得记录的是 **「7 阶段管线」其实是 LLM 方法论而非确定性引擎**——这是理解整个项目的钥匙，也最容易被误读。`commands/cli-anything.md` 开篇强制「Before doing anything else, you MUST read HARNESS.md … Do not improvise」；7 阶段（分析 SOFTWARE.md 的 GUI→API 映射 → 设计命令组 → 实现 Click CLI + session → 测试规划 → 测试实现 → 文档 + Phase 6.5 SKILL 生成 → PyPI 发布）**全部由 LLM agent 执行**，唯一的确定性代码是 Phase 6.5 的 `skill_generator.py`（正则扫 Click 装饰器抽命令组）。把它当「确定性工厂」理解是误读——它是「高度结构化的强约束 prompt」。这带来的 Trade-off 很关键：灵活、能吃任意软件、产出贴合真实后端；但**产出质量 = 模型能力 × methodology 质量**，不可复现、需逐个验证。这也解释了为什么 fix(47.5%) > feature(33.5%)——每接一个新软件就暴露大量适配层兼容性/JSON round-trip 边界问题（#343 Blender Windows 路径转义、browser harness 的 ls/grep/cat round-trip bug 群），修复主要落在适配器层而非框架内核。

> 安全注记：`installer.py` 注释「Commands come from the trusted registry, not user input」——但仍 `shell=True` 跑含管道的命令、git 子目录装无版本锁（拉 HEAD），供应链信任全压在 registry 上，是真实攻击面。

## 竞品格局与定位

这是「让 AI 操作软件」赛道的三条路线之争：**CLI（确定性/省 token/可组合/可测试，但需为每个软件做 harness）vs MCP（协议标准化）vs computer-use（零适配通用但不确定）**。

| 项目 | Stars | 路线 | 与 CLI-Anything 关系 |
|------|------|------|------|
| MCP servers | ~87K | 协议标准化 | **互补非替代**：MCP 管远程 SaaS/鉴权，CLI 管本地成熟软件；public_registry 甚至收编 MCP 桥。论点（待独立核实）：同任务 CLI 比 MCP 省 4~32× token、可靠性更高。MCP 的标准化网络效应是最大外部威胁 |
| Anthropic Computer Use / Self-Operating-Computer / OpenAdapt | ~17K / 10K / 1.6K | 视觉点击 | **正面竞争**：把「零适配通用但不确定（像素脆弱/时序依赖/坐标）」对换成「确定性但每软件要写 harness」。browser harness 文件系统隐喻是正面交锋样板 |
| Open Interpreter | ~64K | 现写现跑代码 | 通用但即兴、无状态、无能力沉淀；CLI-Anything 把能力固化成可复用/可测试/带 session+undo 的命令集，更工程化但前置成本高 |

### 差异化护城河

① **方法论生成器**（强约束 SOP，把「软件 agent 化」变成可批量执行的流程）+ ② **市场飞轮**（registry 即时上架 + 9 个 agent 运行时入口 + agent-native 可发现性）。两者叠加才是壁垒——单看适配器数量不是。它赌的是「为 agent 重做接口」长期胜过「逼 agent 模仿人类感知」。

### 竞争风险

- **护城河系于飞轮能否自转**：49 个注册表贡献者撑 60 适配器，长尾质量核心团队失控（测试数从 Zoom 22 到 Mailchimp 303 不等）。社区贡献停滞 → 长尾覆盖面成短板。
- **MCP 标准化的结构性威胁**：协议生态规模与网络效应是长期最大外部对手。
- **价值在框架核心而非适配器堆量**：宣传易被「支持 N 个软件」带偏，真资产是 HARNESS.md + cli-hub + 接口契约。

### 生态定位

与 MCP 互补（远程协议 vs 本地确定性 CLI），与 computer-use 正面竞争（确定性 vs 通用）。HKUDS「Anything 系列」营销机器的又一发，自带数千关注者冷启动 + arXiv 背书 + 统一品牌。

## 套利机会分析

- **信息差**：CLI-Anything 是 2026 上半年最具传播爆点的 agent 项目之一，「CLI vs 视觉点击 vs MCP 三路线之争」叙事张力强、踩在「CLI 正在 token 效率/可靠性上反超 MCP」的行业风口；中文圈对「agent-native 接口设计」「7 阶段实为 LLM SOP」「框架价值 vs 适配器数量」「registry 即分发」的客观拆解稀缺。
- **技术借鉴**：`--json` agent CLI 契约、强约束 SOP 工程化 LLM 生成、registry-as-server 市场、backend wrapper、装饰器反射 SKILL.md、`.well-known/agent.json` 可发现性——远超本项目，可迁移到任何 agent 工具/技能/市场建设。
- **生态位**：填补「为 agent 重做软件接口」的新品类；与 MCP 错位互补、与 computer-use 错位竞争。
- **趋势判断**：押注「确定性接口 > 视觉模仿」；长期看「社区飞轮能否持续转 + 能否补上中心化 CI 质量闸门 + 能否给出对 MCP/computer-use 的同行评议级实证」决定其从「现象级」变「事实标准」。

## 风险与不足

- **CI 是关键短板**：5 个 workflow 均不跑 harness 测试，4775 个测试无中心化 CI 闸门，「2461 passing」徽章是本地/手动快照（注：实际测试数远超标称，存在性核实通过，但无强制门）。
- **适配器质量高方差**：27.5 万行主要在社区适配器层，质量随贡献者波动；核心团队对长尾失控。
- **star 含厂牌放大**：watchers 仅 169 vs 42K star，关注度/star 严重失衡；需结合 745 commit / 115 贡献者 / 真测试判断（底层是真项目而非空壳，但 star 绝对值不等于落地采用规模）。
- **供应链信任面**：installer `shell=True` + git 子目录装无版本锁，信任全压 registry。
- **零适配做不到**：没有 harness 的软件它碰不了——这是相对 computer-use「零适配通吃」的根本代价。
- **实证待补**：「省 4~32× token、可靠性更高」目前主要由第三方博客零散基准支撑，官方未给同行评议对照数据。

## 行动建议

- **如果你要用它**：适合跑 agent（Claude Code / Pi / OpenClaw / nanobot / Cursor / Codex / Goose 等 9 个入口）、要让 AI 稳定驱动本地专业软件（建模/办公/调试/浏览器）的开发者；`pip install cli-anything-hub` → `cli-hub install <name>` 即可。注意宿主机需装真软件、适配器质量参差、无中心 CI 闸门——生产用前自行验证目标 harness。远程 SaaS/鉴权场景仍该用 MCP。
- **如果你要学它**：直奔 `cli-anything-plugin/HARNESS.md`（36KB 方法论 SOP，最高密度入口）+ `cli-anything-plugin/skill_generator.py`（Phase 6.5 生成器）+ `cli-hub/cli_hub/{registry,installer}.py`（市场即分发）+ `browser/agent-harness/.../core/fs.py`（浏览器即文件系统的接口重构样板）+ arXiv 2606.03854（设计哲学一手来源）。
- **如果你要 fork / 借鉴它**：`--json` agent CLI 契约、强约束 SOP、registry-as-server、backend wrapper、装饰器反射 SKILL.md 是可直接迁移的设计。Apache-2.0 友好；注意自己补 CI 质量闸门与供应链安全（避免 `shell=True` + 无版本锁直装）。

### 知识入口

| 资源 | 链接 |
|------|------|
| arXiv 技术报告 | https://arxiv.org/abs/2606.03854 《CLI-Anything: Towards Agent-Native Computer Use》（设计哲学与路线一手来源） |
| 官网 / CLI-Hub | https://clianything.cc/（市场、安装工作流、贡献指南；hkuds.github.io/CLI-Anything 已 301 重定向至此） |
| DeepWiki | https://deepwiki.com/HKUDS/CLI-Anything（已收录，含 7 阶段管线 / HKUDS-core vs community 划分） |
| 安装 | `pip install cli-anything-hub` → `cli-hub install <name>`（browse/install/manage 社区 CLI） |
| 贡献 | contributor-signup + cli-wishlist issue 模板（需求众包，PR 合并即时上架） |

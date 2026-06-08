# 手机离线跑 Gemma 4：拆解 Google 官方设备端 AI 橱窗 Gallery（2.3 万 Star）

> 一句话总结：Google 官方出品的设备端 GenAI 展示 app（Android/iOS/macOS 三端），一键下载 Gemma 4 等开源模型在本地完全离线运行——隐私不出设备、无网可用、零 API 成本，背后是 LiteRT + MediaPipe + LiteRT-LM 全栈推理引擎的官方橱窗。

---

## 值得关注的理由

- **它把「设备端 AI」从概念变成了人人可试的 app**。过去「在手机上跑大模型」是极客话题，Gallery 让普通人点几下就能下载 Gemma 4 在自己手机上完全离线对话、读图、转写录音——这是 2025 年端侧 AI 破圈的标志性产品之一。
- **它是 Google 设备端 AI 全栈的「样板间」**。真正的产品是背后的 LiteRT（原 TensorFlow Lite）、MediaPipe LLM Inference、LiteRT-LM SDK 和 Gemma 模型生态;Gallery 是把这套栈对外展示 + 拉新的官方橱窗，Apache-2.0 开源，可直接 fork 当端侧 AI app 模板。
- **它把端侧 AI 最难的工程矛盾摆到了台面上**：Android 硬件加速碎片化。Top issue 几乎全是 GPU/NPU 崩溃——CPU 能跑但慢，一开 GPU 加速就崩，连 Google 自家 Pixel 旗舰都摆不平。这是设备端 AI 对比云端「统一硬件」的本质鸿沟，代码里甚至有 `isPixel10()` 这种逐机型硬编码特判。
- **它前瞻性地把 Agent 范式搬到了端侧小模型**：function calling（FunctionGemma 270M 微调）+ MCP（官方 Kotlin SDK）+ Agent Skills（SKILL.md + WebView/JS 渐进式披露），证明 270M 级离线小模型也能做 agent。

---

## 项目展示

README 提供 8 张真实 app 界面截图（聊天 / Ask Image / Prompt Lab / 模型管理等）：

![App 截图 01](https://github.com/user-attachments/assets/a809ad78-aef4-4169-91ee-de7213cbb3bd)
![App 截图 03](https://github.com/user-attachments/assets/e5089e41-2c18-4fbe-9011-ebe9e5a02044)
![App 截图 05](https://github.com/user-attachments/assets/8c229e96-b598-4735-9f60-e96907e1d5d5)

> 社交卡片兜底：`https://opengraph.githubassets.com/1/google-ai-edge/gallery`

---

## 项目画像

| 维度 | 数据 |
|---|---|
| 全名 | `google-ai-edge/gallery` |
| 定位 | Google 官方设备端 ML/GenAI 展示 app（showcase / reference app） |
| Star / Fork | 23,630 ⭐ / 2,459 🍴 |
| License | Apache-2.0（可商用 / 可 fork 当模板） |
| 平台 | Android 12+ / iOS 17+ / macOS（已从 Android-only 扩展到三端） |
| 主语言 | Kotlin 82%（35K 行，Jetpack Compose M3） |
| 代码规模 | 42,926 行 / 326 文件 / 注释比 0.199（健康） |
| 建库时间 | 2025-03（约 14 个月，2025 年爆火） |
| 开发节奏 | 427 commit，近 90 天 169、近 52 周 369（加速中） |
| 最新版本 | v1.0.15（23 个 tag，语义化版本） |
| 贡献者 | 17 人，均为 Google `google-ai-edge` 团队（主力 Jing Jin 等） |
| 推理栈 | LiteRT（原 TF Lite）+ LiteRT-LM SDK + MediaPipe LLM Inference + AICore（Gemini Nano） |
| 模型生态 | Gemma 4 家族（E2B/E4B 边缘优化版）+ HuggingFace litert-community |
| 核心矛盾 | Android 硬件加速碎片化（GPU/NPU 跨设备崩溃） |

---

## 作者视角

### 问题发现

Google AI Edge 团队（Jing Jin 等 17 人）手里握着一整套设备端 AI 栈——LiteRT、MediaPipe、LiteRT-LM、Gemma——却缺一个「可感知的产品载体」。这套 SDK 很强，但对开发者和普通用户都门槛极高：不知道哪些模型能在自己手机上跑、怎么下载、怎么选 CPU/GPU/NPU、怎么把推理接进 app。README 口号「Explore, Experience, and Evaluate」直接暴露意图：这不是要冲 DAU 的产品，而是一个可触摸的能力演示场。

### 解法哲学

三层解耦得很干净：

1. **推理抽象层**（`runtime/`）：把「设备端 LLM 怎么跑」收敛到一个 `LlmModelHelper` 接口，屏蔽 LiteRT-LM 与 AICore 两套异构后端。
2. **任务插件层**（`customtasks/`）：把「每个 AI 用例」做成可热插拔的 `CustomTask`，新增用例零侵入框架。
3. **模型治理层**（`data/ModelAllowlist.kt` + 远程版本化 allowlist）：把「哪些模型能下」从代码里抽出来，做成 Google 远程可控的清单。

橱窗的本质：用最小的框架成本，横向铺最多的「Wow 用例」（Chat / Ask Image / Audio Scribe / Mobile Actions / Tiny Garden / Agent Skills）。

### 背景知识迁移

代码直接 import `com.google.ai.edge.litertlm.*`（`Engine`/`Conversation`/`EngineConfig`/`Backend`/`SamplerConfig`/`ToolSet`）和 `com.google.mlkit.genai.*`（AICore）。作者把内部 SDK 的最佳实践——speculative decoding 探测、constrained decoding、thinking channel、per-SOC 模型文件——固化进示范代码，等于一份「LiteRT-LM 该怎么用」的官方活文档。

### 战略图景

- **拉新漏斗**：app 是 Gemma 4 与 litert-community 模型的分发入口，`learnMoreUrl` 直链 HuggingFace。
- **三端扩张**：已有独立 `ios_1_0_0.json` allowlist 与 macOS DMG，Android 仍是主力（43K 行都在 `Android/`）。
- **端侧 agent 押注**：function calling + MCP + Agent Skills，把「270M 小模型也能 agent」作为下一个叙事，对标云端 agent 但主打隐私 / 离线。

---

## 核心价值提炼

### 创新点

**1. 端侧 Agent Skills（SKILL.md + WebView/JS 渐进式披露）** — 新颖度 5/5 · 实用性 4/5 · 可迁移性 4/5

把 Claude 的 Skills 范式（YAML frontmatter + 渐进式披露）搬到 270M~E4B 级离线小模型。内置 12 个技能，每个是 `SKILL.md`（元数据 + 指令）+ `scripts/index.html`（JS 实现）。`AgentTools` 暴露三个元工具：`loadSkill(name)` 先只给模型技能名 / 简介、需要时才返回完整指令（应对小模型上下文小）;`runJs()` 在 WebView 沙箱执行技能 JS;`runMcpTool()` 调外部工具。技能可从内置 / 本地 / URL / featured 列表动态加载。适用：任何想给（小）模型加可扩展工具的端侧 app。

**2. 版本化远程 model allowlist 治理** — 新颖度 3/5 · 实用性 5/5 · 可迁移性 5/5

app 版本号 → 远程 `model_allowlists/{version}.json` 清单。`loadModelAllowlist()` 用 `BuildConfig.VERSION_NAME` 拼 URL 拉清单，三级降级（网络 → 磁盘缓存 → 内置兜底）。清单里做治理：`disabled` 下架、`minDeviceMemoryInGb` 内存门槛、`socToModelFiles[SOC]` 按芯片选文件、机型放行 AICore。让 Google 无需发版就能远程灰度 / 下架模型。适用：需远程可控重型资源的客户端。

**3. 单接口多推理后端抽象** — 新颖度 3/5 · 实用性 5/5 · 可迁移性 5/5

`LlmModelHelper` 接口（`initialize`/`runInference`/`resetConversation`/`cleanUp`/`stopResponse`）统一封装两套形态完全不同的 SDK：LiteRT-LM（`Engine`/`Conversation`/流式回调）与 AICore/Gemini Nano（`generateContent`），按 `Model.runtimeType` 分发。thinking 内容走 `message.channels["thought"]`。适用：要同时支持自带模型与系统级模型的端侧 app。

**4. 小模型 function-calling 落地真实设备动作** — 新颖度 4/5 · 实用性 3/5 · 可迁移性 3/5

`MobileActionsTools : ToolSet` 用 `@Tool`/`@ToolParam` 注解把手电筒 / 联系人 / 邮件 / 地图 / 日历暴露成函数，FunctionGemma 270M 微调模型负责选函数填参，`onFunctionCalled` 回调执行真实 Android 动作。证明离线小模型也能做设备控制 agent。

### 可复用模式

1. **单接口 + 策略分发抽象异构 SDK**：`interface LlmModelHelper` + 按枚举选实现 — 兼容多推理引擎 / 多供应商。
2. **DI multibinding 做插件注册表**：`@Provides @IntoSet` → 注入 `Set<CustomTask>`，框架自动发现新模块 — Compose/Hilt 大型 app 横向扩展。
3. **版本化远程配置 + 多级缓存兜底**：客户端版本号映射远程清单，网络 → 缓存 → 内置三级降级 — 远程可控的资源治理。
4. **HTTP Range 断点续传 + WorkManager 前台进度**：读 tmp 已下大小、`Range: bytes=N-`、append 续写、滑动窗口算 ETA — 大文件可靠下载（端侧模型动辄数 GB）。
5. **SKILL.md + 渐进式披露 + 沙箱执行**：元数据 + 先摘要后全文 + WebView/JS 执行 — 给（小）模型加可扩展技能。

### 关键设计决策

- **硬件加速的「配置驱动 + 设备特判」应对**：backend 选择做成 per-model 配置（allowlist 的 `accelerators` 字段）+ 运行期设备特判。`ModelAllowlist.toModel()` 里堆了一串补丁式特判——`isPixelDevice()` 把 NPU 改写成 TPU、`isPixel10()` 直接移除 GPU、NPU 下 `samplerConfig = null`。这些是碎片化留下的「疤痕」：可控但不优雅，只能逐设备事后打补丁，无法根治。
- **customtasks 插件式任务**：每个用例实现 `CustomTask` 接口（元数据 + 初始化 / 清理函数 + `@Composable MainScreen`），用 Hilt `@IntoSet` 注入。代价是 `MainScreen(data: Any)` 用 `Any` + 强转牺牲类型安全换插件解耦。

---

## 竞品格局

| 竞品 | 定位 | 优势 | 劣势 |
|---|---|---|---|
| **gallery（本项目）** | Google 官方 showcase（三端）+ Gemma 试用入口 | 官方背书、Gemma 4 首发、LiteRT/MediaPipe 全栈、隐私离线、Agent Skills/MCP、Apache-2.0 可当模板 | 「橱窗 / Beta」非产品、GPU/NPU 跨设备崩溃、模型受 allowlist 约束 |
| **PocketPal AI** | 第三方开源本地 LLM app（llama.cpp 系） | 任意 GGUF 模型、UI 打磨好、跨端、社区灵活 | 主要 CPU 推理、NPU 加速弱、无大厂模型生态背书 |
| **MLC Chat** | 跨端编译型本地 LLM app（TVM） | NPU 路径往往最快、跨硬件覆盖广 | 工程门槛高、编译栈复杂、模型适配需 MLC 流程 |
| **Gemini Nano（AICore）** | Google 系统级设备端模型（非 app） | 系统 API、深度集成、免下载省电 | 仅旗舰（12GB+ RAM）、不开源、非「下载即玩」 |
| **Apple Intelligence** | Apple 系统级端侧 SLM | 垂直整合、延迟最低、系统级上下文 | 仅 iPhone 15 Pro+、封闭、不可换模型 |

**三条对照轴**：

1. **官方 showcase vs 第三方 app**：Gallery 是 Google「样板间」（背书强、生态正统，但橱窗属性、功能广而非深）;PocketPal/MLC 是「极客自由」（自由度高、缺大厂合力）。
2. **推理栈之争**：LiteRT/MediaPipe（Google）vs llama.cpp（PocketPal）vs TVM/MLC——三条设备端推理技术路线的代表。
3. **app 级 vs 系统级**：Gallery/PocketPal/MLC 是「装个 app 跑模型」;Gemini Nano/Apple Intelligence 是系统级、给三方 app 直接调用。值得注意的是 Gallery 反而把 AICore/Gemini Nano 当成自己的一个后端，定位互补而非纯竞争。

**综合结论**——护城河：① Google 官方背书（Gemma 4 首发入口）② Gemma/litert-community 模型生态 ③ LiteRT-LM + MediaPipe + AICore 全栈橱窗 ④ Agent Skills/MCP 的端侧 agent 叙事。竞争风险：① Android 硬件加速碎片化 ② showcase 而非产品（推 SDK / 拉新，不冲留存）③ 系统级方案逐渐覆盖常见用例后会蚕食橱窗的存在理由 ④ 模型受 allowlist 约束，非真正开放。

---

## 套利机会分析

- **对「想做端侧 AI app」的开发者**：这是当下最完整的官方参考实现。`runtime/` 的推理抽象、`customtasks/` 的插件模式、`worker/DownloadWorker` 的断点续传、`data/ModelAllowlist` 的远程治理，每一块都是可直接抄进自己 app 的范式级代码;Apache-2.0 甚至可整体 fork 改造。
- **对「想蹭端侧 AI 热点」的内容创作者**：「在手机上离线跑 Gemma 4」是天然破圈选题——隐私、离线、零成本、Google 出品，对大众有强吸引力;面向开发者则有「Google 设备端 AI 工程栈拆解 + 硬件加速碎片化」的深度角度。
- **对「评估端侧模型可行性」的团队**：app 自带 Benchmark 工具，可在真机上实测 Gemma/LiteRT 的吞吐与延迟，是低成本验证「我的场景能否上端侧」的捷径。
- **对「研究 Agent Skills 端侧化」的人**：`assets/skills/*` 把 Claude Skills 范式搬到离线小模型的完整实现，是当前少见的可运行参考。

---

## 风险与不足

- **跨设备硬件加速不稳定**：这是最大的现实短板。GPU/NPU 加速跨设备崩溃，连 Pixel 旗舰都要靠 `isPixel10()` 移除 GPU 这种硬编码特判（issues #280/#4/#106/#64）。如果你的目标用户机型分散，端侧加速的可靠性需自行充分实测。
- **零自动化测试**：仓库 **0 个测试文件**（无 unit、无 instrumentation），CI 仅编译 + 文档构建，无测试 / lint / release gate。考虑到它重度依赖真机硬件，测试缺位是显著短板。
- **showcase 而非产品**：目标是推 SDK、拉新，不是冲留存——功能广而浅，不要把它当成生产级 AI 助手来期待。
- **模型受 allowlist 约束**：可用模型完全由 Google 远程清单控制，「自定义模型导入」是唯一逃生口——不是真正的开放自由。
- **实验性 Beta + 代码瑕疵**：README 明确标注 experimental Beta;`ModelManagerViewModel` 1400+ 行是上帝类，`MainScreen(data: Any)` 用强转，部分路径 `catch{ Log }` 后静默吞错。
- **安全面**：Agent Skills 在 WebView 跑来自 URL 的任意 JS、MCP 调外部工具——代码用 disclaimer 弹窗 + per-tool 权限 + per-skill secret 缓解，但加载第三方技能 / MCP server 仍需谨慎。

---

## 行动建议

- **用它**：装上官方 app（Google Play / App Store / GitHub Release），下载 Gemma 4 E2B/E4B 体验离线聊天、读图、录音转写;用内置 Benchmark 实测你目标机型的推理性能。
- **学它**：精读 `runtime/LlmModelHelper.kt`（推理抽象）+ `customtasks/common/CustomTask.kt`（插件 KDoc 本身是完整教程）+ `data/ModelAllowlist.kt`（远程治理）+ `worker/DownloadWorker.kt`（断点续传）。这四个文件是端侧 AI app 的工程骨架。
- **fork 它**：Apache-2.0 允许整体 fork 当端侧 GenAI app 模板;若要做 agent，重点看 `assets/skills/*` + `MobileActionsTools`（function calling）+ MCP Kotlin SDK 接法。

---

## 知识入口

| 入口 | 链接 | 用途 |
|---|---|---|
| GitHub 仓库 | <https://github.com/google-ai-edge/gallery> | 源码 / Release / Issue |
| DeepWiki | <https://deepwiki.com/google-ai-edge/gallery> | 11 章架构解读（模型注册 / 任务系统 / LLM 集成 / Agent Skills），读架构首选 |
| 官方 Wiki | <https://github.com/google-ai-edge/gallery/wiki> | 安装 + 完整使用指南 |
| Google AI Edge 文档 | <https://developers.google.com/edge> | LiteRT / MediaPipe / LiteRT-LM 全栈文档 |
| LiteRT-LM Overview | <https://ai.google.dev/edge/litert-lm/overview> | 设备端 LLM 推理内核（gallery 的引擎） |
| HuggingFace | <https://huggingface.co/litert-community> | gallery 拉取的模型仓库 |
| 关联仓库 | <https://github.com/google-ai-edge/LiteRT-LM> | 推理 SDK 源码 |
| Google Play | <https://play.google.com/store/apps/details?id=com.google.ai.edge.gallery> | 直接安装 |

# 一个人 4 个月做到 33K star：free-claude-code 怎么让 Claude Code 换上任意免费模型

> GitHub: https://github.com/Alishahryar1/free-claude-code

## 一句话总结

free-claude-code 是个人开发者 Ali Khokhar 用 4 个月做出、爆发到 33K star 的「Anthropic Messages API 兼容代理」：它让 Claude Code 的客户端协议一字不改，却把流量路由到 17 家免费/付费/本地模型 provider（NVIDIA NIM、Gemini、DeepSeek、Kimi、本地 Ollama 等）。本质是合法的「claude-code-router」类协议路由器——保留 Claude Code 的客户端体验，但换掉付费的 Anthropic 后端。它真正的工程深度不在「路由」，而在「把不可靠的免费 provider 流伪装成一个稳定的 Anthropic 端点」。

> 合规视角：用非 Anthropic 模型驱动 Claude Code 客户端，涉及 Anthropic 客户端与各 provider 的服务条款，由用户自行选择并自负；本工具本身是协议转换/路由器，与 claude-code-router、LiteLLM passthrough 同属一类网关工具。

## 值得关注的理由

1. **一个「单人 + AI 辅助」爆红的样本**：作者是 NVIDIA 系统软件工程师 Ali Khokhar，4 个月 685 commit（周末占 40%、深夜占 34% 的激情节奏），其中「Cursor Agent」贡献了 53 个 commit、「Claude」多次 co-author——他公开用 AI 编码工具开发这个「免费跑 Claude Code」的工具，自举味十足。「单人 + AI 把产出放大到 33K star」本身就是 AI 编码时代的标志性案例。
2. **流式响应三级恢复是全项目最硬核的工程**：免费 provider 经常 429/超时/中途断流，但要对 Claude Code 维持「一个可靠 Anthropic 端点」的假象。它做了三级递进——① holdback 缓冲（响应开头几秒内扣住不下发，断流就整流重开、客户端无感）；② 中途续写（已下发后断流，发续写请求 + 重叠检测只拼新增后缀）；③ 工具 JSON 修复（断在半截工具调用 JSON 时，按工具 schema 校验做 append-only 修复）。这套「把 flaky 后端伪装成可靠端点」的设计，文献里少见。
3. **一套值得任何项目抄的「契约测试」体系**：注释比仅 0.025（几乎不写注释），却敢单人 + AI 高频改 17 家兼容——靠的是测试当安全网：`tests/contracts/test_import_boundaries.py` 用 AST 静态分析**强制架构分层**（core 不能依赖产品包、api 只能走 providers 窄门面），`test_feature_manifest.py` 强制「README 每个宣传功能都必须有 pytest 契约测试 + live 覆盖决策」。测试函数 1355 个 vs 源码 def 761 个。

## 项目展示

![工作机制](https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/assets/how-it-works.svg)

请求流转：Claude Code 客户端（CLI/VS Code/JetBrains ACP）→ FastAPI Anthropic 兼容端点 → model_router 把 opus/sonnet/haiku 映射到各 provider → provider 适配器翻译并归一回 Anthropic SSE 形状。

![运行画面](https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/assets/pic.png)

![本地 Admin UI](https://raw.githubusercontent.com/Alishahryar1/free-claude-code/main/assets/admin-page.png)

loopback-only 的本地 Admin UI——填 key、Validate/Apply 热重载，不用手改配置文件。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/Alishahryar1/free-claude-code |
| Star / Fork | 32,985 / 5,024 |
| 代码行数 | 48,900 行（Python 96.7%，注释比 0.025 极低，靠测试与类型兜底；111 个运行时依赖对接众多 provider） |
| 项目年龄 | 4.3 个月（2026-01-28「initial commit」） |
| 开发阶段 | 密集开发（近 30 天 116 commit，月峰值 2026-02 达 311） |
| 贡献模式 | 单人 + AI 辅助 + 少量社区（33 人，Ali Khokhar 约 78–84%，Cursor Agent 53 commit） |
| 热度定位 | 大众热门 / 爆发型（4 个月 33K star，近期增长最快的开源项目之一） |
| 质量评级 | 代码组织「优」 测试「卓越」 CI「优」 文档「源码注释极少」 单人维护风险「高」 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

作者 **Ali Khokhar（@Alishahryar1）**——USC 计算机硕士、现 **NVIDIA 系统软件工程师**（Santa Clara），曾在 Roku 实习做数据管道。个人 User 账号、665 followers、仅 7 个公开仓库，本项目 star 占其全部仓库的 99.9%（唯一爆款）。他的 NVIDIA 背景直接解释了项目默认 provider 是 **NVIDIA NIM**（默认模型硬编码 `nvidia_nim/nvidia/nemotron-3-super-120b-a12b`，NIM 是唯一带 `voice.py` Riva 语音转写的独立 provider 模块）。项目谱系上承接了社区里「Claude Code + NVIDIA NIM 免费方案」的思路（贡献者中的 Rishi Khare 有同名前身仓库），后由 Ali 扩展成 17-provider 通用路由器。

### 问题判断

他抓住的缝隙是「**协议是契约、后端可替换**」：Claude Code 的客户端协议（Anthropic Messages SSE + 工具调用 + thinking）稳定且开源生态围绕它，但模型后端是封闭付费的。现有方案不够在于——claude-code-router（Node/TS）配置门槛高、客户端集成窄；LiteLLM 是企业通用网关、对 Claude Code 的怪癖不做定制；y-router 是极简 Cloudflare Worker、功能少。

### 解法哲学

两条原则写死在 `AGENTS.md`：① 「写最简单的代码，保持代码库最小和模块化」；② 「最大化测试覆盖，最好有 live smoke 测试」。落到产品上就是「**免费 + 傻瓜开箱**」——一个 `fcc-server` + loopback Admin UI 填 key 即用，NVIDIA NIM 免费档为默认，README 反复强调「不要手改配置文件，用 Admin UI」。增长护城河赌的是「最低门槛 + 最广客户端入口（CLI/IDE/Discord/Telegram/语音）」，而非路由算法。

### 战略意图

把 provider 适配做成两个可继承基类（`OpenAIChatTransport` / `AnthropicMessagesTransport`），README「Extending」公开邀请贡献者加 provider——把单人维护 17 家兼容的负担部分外包给社区，同时用契约测试守住正确性。配合 AI 辅助编码（Cursor/Claude co-author），这是「单人 + AI + 社区」三方放大单人产出的典型打法。

## 核心价值提炼

> 诚实区分：协议路由器范式本身不新（claude-code-router 等已有）。本项目的价值在于**实现的完整度与鲁棒性**（流恢复、怪癖隔离、最全入口）和**免费傻瓜开箱的产品打磨**，而非范式创新。

### 创新之处

1. **流式响应三级恢复**（新颖度 5/5，实用性 5/5，可迁移性 4/5，全项目最硬核）：`core/anthropic/stream_recovery.py`——① `RecoveryHoldbackBuffer` 在响应开头几秒/几 KB 扣住不下发，断流就整流重开（最多 5 次）、客户端无感；② 已 commit 后断流发内部续写请求（去 tools + 追加已生成文本 + 续写提示），用 `continuation_suffix` 重叠检测只拼新增后缀；③ 断在工具调用半截 JSON 时，按工具 JSON Schema 校验做 append-only 修复。`is_retryable_stream_error` 严格区分可重试（429/5xx/超时/截断）与不可重试（auth/400）。
2. **Anthropic↔OpenAI 协议无损归一**（新颖度 4/5，可迁移性 5/5）：`core/anthropic/conversion.py` 的 `_PendingAfterTools` 机制——OpenAI 不允许在同一条 assistant 消息里把文本放在 `tool_calls` 之后，于是把 `tool_use` 之后的文本延迟缓存、等对应 tool 结果按序回放完再补发；reasoning 历史用 `think_tags`/`reasoning_content`/`disabled` 三态适配不同 provider；无法无损转换的块直接抛错而非静默丢数据。
3. **双 transport 基类 + SSE 双向构造**（新颖度 4/5）：按上游协议族分两个基类——`OpenAIChatTransport`（NIM 等走 `/chat/completions`，用 `SSEBuilder` 主动把 chat delta 构造成 Anthropic SSE 事件、处理 `<think>` 标签与伪装成文本的工具调用）+ `AnthropicMessagesTransport`（OpenRouter 等走原生 `/messages`，透传 + 改写）。共享逻辑全下沉到中立的 `core/anthropic/`。
4. **provider 怪癖隔离 + 工具参数别名**（新颖度 4/5，可迁移性 3/5）：`providers/nvidia_nim/request.py` 把每家 API 的脏活封在各自 request builder——hosted NIM 拒绝名为 `type` 的工具参数（与 schema 关键字冲突），于是改名成 `_fcc_arg_type` 发上游、再在流式响应里 `_restore_aliased_tool_arguments` 还原回 `type`，对客户端透明；schema 清洗 + 降级克隆重试。
5. **契约测试体系（AST 分层强制 + 功能清单强制）**（新颖度 4/5，可迁移性 5/5）：`test_import_boundaries.py` 用 AST 把架构分层做成 CI 强制；`test_feature_manifest.py` 强制「宣传即测试」。这两类元测试是支撑「单人 + AI 高频改动」不腐化的关键，值得任何中大型项目借鉴。

### 可复用的模式与技巧

- **RecoveryHoldbackBuffer（短暂扣发 + 透明重试）**：流式开头扣住不下发、失败即整流重开——任何「一旦下发不可撤回」的流式代理。
- **append-only + JSON Schema 校验的工具修复**：只接受能让半截 JSON 变合法且过 schema 的后缀——结构化输出容错。
- **双 transport 基类按协议族分流 + 共享逻辑下沉中立层**：多后端网关。
- **私有 body key 传带元数据 + 上游 I/O 前剥离**：在请求构造与响应解析间传内部状态（如别名映射）。
- **fast-path 本地探针短路**：对 Claude Code 的琐碎元请求（配额检查/标题生成）本地回包省额度——任何代理 Claude Code 的网关都能抄。
- **AST 导入边界测试 + 功能清单测试**：把架构分层和「宣传即测试」做成 CI 闸门——防腐化。

### 关键设计决策

最值得记录的是 **流式三级恢复**——它把「免费 provider 不可靠」这个根本约束，变成对 Claude Code 透明的可靠性。难点在于「流式响应一旦开始下发就不能收回」：holdback 缓冲争取一个「还能整流重开」的安全窗口；窗口过后则降级到「中途续写」（用重叠检测拼接，避免重复内容）；最棘手的「断在工具调用半截 JSON」则用工具的 JSON Schema 做 append-only 校验修复。两个 transport 各实现一遍恢复编排，复杂度极高，但这正是「免费 provider 也能稳定跑 Claude Code」的核心竞争力（关键文件 `core/anthropic/stream_recovery.py` + 两个 transport）。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | free-claude-code | claude-code-router | LiteLLM | y-router |
|------|------|------|------|------|
| Stars | 33K | ~34.8K | 大型网关 | 小 |
| 实现 | Python/FastAPI | Node/TS | Python | Cloudflare Worker |
| 定位 | Claude Code 免费开箱代理 | 可编程灵活路由 | 企业通用网关 | 极简 serverless 转接 |
| 客户端集成 | 最全（CLI/IDE/Discord/语音） | CLI 为主 | 通用 | CLI |
| 上手 | 填 key 即用 + Admin UI | 配置文件为中心 | 部署偏重 | serverless |

### 差异化护城河

免费默认（作者 NVIDIA/NIM 背景）+ 最全客户端入口（CLI/VS Code/JetBrains ACP/Discord/Telegram/语音）+ 流恢复鲁棒性 + 傻瓜 Admin UI，四者叠加形成「最低门槛 + 最广覆盖」的组合——单点都可被复制，但组合难。

### 竞争风险

- **单人维护 17 家兼容**：provider API 频繁变更带来持续维护负担（Top issues 几乎全是 provider request failed / 422 / timeout / SSE 归一化 bug，且多 open），巴士因子=1；
- **无 release、git 主干跑**：README 用安装脚本拉 main，回滚困难，生产使用有不确定性；
- **免费 provider 不可控**：免费层限流、模型质量/延迟参差、ToS 与可用性随时变；
- **成熟竞品体量更大**：claude-code-router（~34.8K）生态更成熟、规则路由 + 插件更灵活。

### 生态定位

Claude Code「省钱 + 远程 + 本地」入口层的事实标准候选；与 claude-code-router 双雄并立（一个走「可编程灵活路由」、一个走「傻瓜免费开箱 + 最全入口」）。靠可继承基类 + 契约测试邀社区贡献 provider 分摊维护，靠 AI 辅助维持单人高产。

## 套利机会分析

- **信息差**：话题正中「AI 编码降本 + 模型自由」热点，受众覆盖几乎所有 Claude Code 用户；且有清晰的技术解读价值（协议翻译 / SSE 流式归一 / 工具调用映射 / 流恢复）。可写「为什么 4 个月 33K 人想要它 + 它到底怎么工作」，也可写「单人 + AI 怎么 4 个月做出爆款」。
- **技术借鉴**：流式三级恢复、Anthropic↔OpenAI 协议归一、双 transport 基类、fast-path 探针短路、AST 边界测试 + 功能清单测试——这些可迁移到任何 LLM 网关 / 流式代理 / 防腐化的中大型项目。
- **生态位**：填补「最傻瓜的 Claude Code 免费开箱 + 最全客户端/远程/语音入口」的空白。
- **趋势判断**：踩在「AI 编码降本 + 模型自由 + 单人 AI 高产」三重趋势上；最大变量是单人能否扛住 17 家兼容的长期维护，以及免费 provider 政策与 ToS 的不确定性。

## 风险与不足

- **单人维护 + 巴士因子=1**：约 84% 提交来自一人，17 家兼容 + 上游频繁变更是持续负担，可持续性是最大隐患（缓解靠可继承基类邀社区 + AI 辅助 + 强契约测试）。
- **无正式 release**：从 git main 直接跑，无版本号、回滚困难。
- **源码注释极少**（0.025）：新人上手成本高，全靠测试和类型当文档。
- **免费 provider 的固有代价**：限流、超时、模型质量/延迟参差，「免费」承诺需用户精细配置路由才不误命中付费模型（issue #241）。
- **合规不确定性**：用非 Anthropic 模型驱动 Claude Code 客户端涉及多方 ToS，由用户自负。

## 行动建议

- **如果你要用它**：适合「想用免费/本地/更便宜模型跑 Claude Code、或想远程/语音编码」的个人开发者；填 key 用 Admin UI 即可，本地模型走 LM Studio/Ollama 最隐私。注意免费层限流、自行确认各方 ToS、生产环境慎用（无 release）。要可编程灵活路由可对比 claude-code-router，要企业网关用 LiteLLM。
- **如果你要学它**：直奔 `core/anthropic/stream_recovery.py`（流式三级恢复，最硬核）、`core/anthropic/conversion.py`（Anthropic↔OpenAI 延迟回放归一）、`providers/{openai_compat,anthropic_messages}.py`（双 transport 基类）、`providers/nvidia_nim/request.py`（怪癖隔离 + 工具别名）、`tests/contracts/`（AST 边界测试 + 功能清单测试）。这五处是工程精华。
- **如果你要 fork / 贡献它**：加 provider 继承两个 transport 基类之一即可，契约测试会守住正确性；流恢复 + fast-path 探针短路是可直接迁移到其他 Claude Code 网关的设计。注意 MIT。

### 知识入口

| 资源 | 链接 |
|------|------|
| 仓库 README | https://github.com/Alishahryar1/free-claude-code （含 17 provider 注册指引 + 架构图） |
| DeepWiki | https://deepwiki.com/Alishahryar1/free-claude-code（已收录，含配置/核心架构/provider/消息平台/测试章节） |
| 同类对照 | claude-code-router（musistudio）/ LiteLLM Anthropic passthrough / y-router |
| 增长曲线 | Star History（4 个月 0→33K 的爆发曲线） |

# GitHub 推荐：Strands Agents：AWS 团队的 Agent SDK 怎么用 hooks 三件套干掉手写 agent loop

> GitHub: https://github.com/strands-agents/harness-sdk

## 一句话总结

Strands Agents 把「model-driven loop + hooks/middleware/intervention 三层拦截」封装成一个 Apache-2.0、双 SDK Python/TypeScript 对等、AWS 主导社区协作维护的工业级 Agent 工厂——让「自己写 agent loop」从一个 3 个月项目缩成一行 `create_harness()`。

## 值得关注的理由

1. **AWS Generative AI 团队的工程化答案**：304 名贡献者、22 个 RFC、45 条 CI workflow、Apache-2.0 许可证——在 LangChain/LangGraph/AutoGen 占据先发优势的红海里，靠「不引入托管控制面」+「任何步都可拦截」打出差异化。
2. **真正双语言对等的 SDK**：425K 行代码里 Python 42.3% 与 TypeScript 42.1% 一比一对齐；不是 Python 优先 TS 跟随的半残同步，是 `strands-py` 与 `strands-ts` 平行演化的两套一等公民实现。
3. **可借鉴的抽象」而不是 feature list」**：`HookOrder` 命名 slot 强制三方插入位置、typed action × event 决策矩阵、Cedar 政策语言接管 agent 授权、`MiddlewareStage` 用 token 身份做 phase 排序——这些设计模式不依赖 Agent 也能直接搬到 HTTP/消息总线/任何事件驱动系统。

## 项目展示

Strands 字标（官网 hero）：

![Strands wordmark](https://strandsagents.com/strands-logo-dark.svg)

> 仓库及官网本次仅抓取到 1 个有效媒体元素（品牌字标）；架构图、Demo GIF 等素材未公开发布。读者可参考 `team/designs/*.md` 的 22 份 RFC 设计图（如 `0015-bidi-webrtc-design.md`、`0011-context-strategy.md`），自行渲染作为学习路径。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/strands-agents/harness-sdk |
| Star / Fork / Watcher | 7,826 / 1,200 / 53 |
| 代码行数 | 425,497（Python 42.3% · TypeScript 42.1% · JSON 11.7% · 其它 3.9%） |
| 项目年龄 | 16.3 个月（首提交 2025-05-16） |
| 总 commit | 2,759（最近 30 天 257 commit，日均 8.6） |
| 开发阶段 | **密集开发**（月均 170 commit，2 个跃升峰：2026-03 = 259、2026-06 = 284） |
| 贡献模式 | **社区协作型**（304 贡献者；Top 1 仅占 12.4%；核心 5 人：zastrowm 365 + pgrayy 272 + dependabot 218 + Unshure 200 + lizradway 143） |
| 热度定位 | **大众热门**（早期套利空间已无，仍在涨） |
| 许可证 | Apache-2.0 |
| 最新版本 | `python/v1.57.0`（主 SDK） · `harness-python/v0.1.2`（下一代 harness 0.1 探索）· `harness-typescript/v0.1.1` |
| 文档投入 | `site/src` 2,782 次改动 + `docs/user-guide` 637 + `docs/examples` 189 ≈ 与 SDK 同量级 |
| 质量评级 | 代码「优秀」文档「优秀」测试「433+407 个」CI/CD「45 workflow」 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

仓库所有者是 Organization 账号 `strands-agents`（2025-04-25 创立，约 1.4 岁），事实上由 **AWS Generative AI SDK 团队**主导维护。判断依据多条交叉一致：
- Provider 矩阵首发就覆盖 Bedrock + Anthropic + OpenAI + Google Gemini + Ollama + LiteLLM——Bedrock + Anthropic 是 AWS 自家栈。
- 贡献者 handle 中出现 `opieter-aws`，主仓里频繁引用 AWS 服务命名（AgentCore / Bedrock AgentCore / EKS / App Runner / Fargate / Lambda / Edge）。
- 5 人核心小组中多人 commit message 风格与 AWS 内部开发规范一致（`chore(data): / feat(auto): / fix:` 前缀严格）。

这不是「一个人周末 side project」也不是「一群 GitHub 爱好者拼凑」——这是 AWS Bedrock AgentCore 工程团队 dogfooding 出痛苦点后，把内部基础设施外溢给社区的典型路径。

### 问题判断

README 第一句话就是「Choose Strands when you would otherwise write your own agent loop」——清楚说明问题域。展开看：

- 自己写一个 agent loop 几个月后会被同样的「非创造性需求」淹没：turn 上限、取消、token 预算、工具注册、MCP、多 agent 编排、会话持久化、observability、guardrails、流式、context 溢出、缓存。
- 现有方案各有缺陷：
  - **LangGraph** 把 agent 硬压成显式 state graph，循环只是图的特例——「我只是想写循环，干嘛要先学图」。
  - **AutoGen** 把多 actor 对话当成一等公民，单 agent 编程体感割裂。
  - **托管控制面**（Bedrock Agents / Vertex Agent Engine）vendor-locked，in-process 能力受限。
- 时机是现在——Anthropic / OpenAI / Google 三家模型 API 终于稳定，Cedar（AWS 开源政策语言）从 IAM 移植到 agent 授权、MCP 协议固化、A2A 协议初露头角，三件套齐了 SDK 才能搭起来。

### 解法哲学

「Model-driven loop + hooks + 软拦截」是核心命题。三条明确的取舍决定整个 SDK 的形态：

1. **不引入托管控制面**——agent loop 在用户进程里跑，hooks 是低阶原语，intervention / middleware / plugins 是其上的语义化封装。这点和 LangChain 不同（LangChain 强调 hub + studio 模板化），和 Bedrock AgentCore 也不同（AgentCore 想做托管）。
2. **类型化决策 vs 字符串黑盒**——intervention 拒绝 `event.cancelTool = 'access denied'` 这种字符串约定，明确分出 `Proceed / Deny / Guide / Confirm / Transform` 五个 typed action。
3. **「简单 vs 功能完整」二者都要**——harness 给 80% 用户一行的 `create_harness()`；给 20% 用户完整的 `Agent(model=..., tools=..., plugins=...)`。

把这些抽象从 AWS 内部用得「肿且乱」的阶段，沉淀成公开原语——是过去 16 个月不断 commit 的根本动力。

### 战略意图

项目是 AWS 战略图景中的「开源门面层」：
- **基础 SDK**（`strands-py` / `strands-ts`，Apache-2.0，社区驱动）是真正的开源资产。
- **电池装好的 harness**（`harness-py` / `harness-ts`，PyPI `strands-harness`、npm `@strands-agents/harness`）把 context_manager / skills / memory / MCP / subagent / 预设 interventions 全部装好。
- **商业化路径走 AWS 侧**（Bedrock AgentCore / Strands Studio），**不在仓库里**——这非常重要，说明仓库始终是 genuinely open，不会一夜变 closed。

`team/TENETS.md` 的 6 条原则（Simple at any scale / Extensible by design / The obvious path is the happy path 等）把这件事写在台面上——而不是埋在私仓 RFC 里。

## 核心价值提炼

> **Phase 1 + Phase 3 一致更正**：仓库内**不存在** Phase 1 早期判断的「WASM Component Architecture（WIT + Python WASM Host）」。DeepWiki 索引可能涉及类似主题，但本仓库 `cedar-wasm` + `cedarpy` 仅是 Cedar 政策引擎的两种绑定（`@cedar-policy/cedar-wasm/nodejs` + Rust 的 cedarpy），加上 `mcp-schema-generator-wasm` 为 MCP 工具自动生成 Cedar schema——并非 Component-Model / WASI / WIT 级别的宿主框架。下面所有创新点都基于代码实读，不含虚拟项。

### 创新之处

按新颖度 × 实用性排序：

1. **Intervention 是一等 SDK 原语**（新颖度 5·实用性 5）——把 Cedar Auth / OPA / LLM Steering / Datadog Guard / Galileo Agent Control / Bedrock Guardrails 六种独立策略层抽象成同一个 `InterventionHandler` 接口，框架统一短断、累积、审计；决策不能写成字符串，必须是 `Proceed / Deny / Guide / Confirm / Transform` 五个 typed action。背景见 `team/designs/0007-intervention-primitive.md`。

2. **`HookOrder` 命名 slot 强制三方插入位置**（新颖度 4·实用性 5）——`hooks/registry.py:30-41` 用 `SDK_FIRST=-100 / INTERVENTION_OUTPUT=-90 / DEFAULT=0 / MODEL_ROUTING=50 / INTERVENTION_INPUT=90 / SDK_LAST=100` 整数 slot，让三方 intervention 永远跑在用户 hook 之前 / 模型路由之后，**用户无需手动排序**。极巧妙的反向设计。

3. **`create_harness()` 一行动态装配 + 前置冲突检测**（新颖度 3·实用性 5）——`harness-py/src/strands_harness/agent.py:249-552` 把 8 个开关 + `**Agent kwargs` 折叠到一行；tool 名字冲突在 `create_harness` 返回前失败（`_check_name_collisions`），把「我后面调 subagent 时才发现名字重复」前移到构造期。

4. **「Typed action + action×event 矩阵」决策表**（新颖度 4·实用性 5）——`interventions/actions.py:117-138` 显式列出 5×5 = 25 个 cell，把 hook 字符串歧义彻底消除。任何想抄的工程团队都能直接学到：「决策 API 必须配决策矩阵，不要让用户记字符串」。

5. **`MiddlewareStage` token + Phase 三相 + 身份哈希**（新颖度 4·实用性 4）——`_middleware/types.py:86-103` 的 `MiddlewareStage(name)` 持 `Input/Wrap/Output` 子 token；`__hash__=id(self)`、`__eq__=is` 让 stage 是「标识符身份」而非「名字字符串」，重命名安全、hash 可用。

6. **`SignalingProvider` + `BidiWebRtcIO` 双层抽象**（新颖度 4·实用性 4）——`team/designs/0015-bidi-webrtc-design.md` 把 WebRTC 的「建立」与「运行」拆到两个 Protocol，与 `BidiModel`/`BidiAgent` 镜像。Provider-specific（IVS/KVS/LiveKit）+ Provider-agnostic 的分层和数据库 driver 设计完全同构。

7. **L0/L1/L2 三层 context 模型**（新颖度 4·实用性 5）——`team/designs/0011-context-strategy.md` 把 context 管理映射成 L0(context window)/L1(session history)/L2（long-term memory） 三层；agentic 模式下 agent 自己用 `pinMessage / getHistory / searchHistory / delegateWithContext / getContextBudget` 工具自我管理。这是 prompt cache、KV cache、persistent storage 这些「现代 LLM 基础设施」应有的统一语义。

8. **`_link_cancel_signal` 双源取消**（新颖度 4·实用性 5）——`agent/agent.py:120-133`：外部 threading.Event 用 50ms 轮询镜像到内部 event，避免 executor 线程卡死后 `Event.wait()` 取消失效。注释明确写出「为何不用 Event.wait()」——非典型但极有效的「拒绝某方案」式注释。

9. **`fail-mode` 三态 `on_error: throw/deny/proceed`**（新颖度 3·实用性 5）——`handler.py:32-40`、`registry.py:250-267`：默认 throw；显式 fail-closed / fail-open。把策略引擎的失败语义显式化，避免「handler 抛异常 = 自动 fail-open」这种隐性假设。

10. **`AGENTS.md` 100+ commit 维护**（新颖度 3·实用性 4）——仓库顶层的「给 AI Agent 用的开发指南」被持续修订 100 次（Top 4 改动文件），与 `team/TENETS.md`（6 条原则）+ `team/designs/*.md`（22 个 RFC）一起，把「为什么」和「是什么」分离做得极彻底。「The code is the what, the team/ is the why」——项目级治理范本。

### 可复用的模式与技巧

可直接搬到其他项目的设计模式（不依赖 Agent 框架也能抄走）：

1. **`register once if anyone overrides`**（`interventions/registry.py:59-63`）——用 `getattr(type(handler), method, None) is not getattr(InterventionHandler, method, None)` 检测类级 override，避免为无 handler 的事件注册空 callback。**适用**：任何 plugin/hook 框架。
2. **`MiddlewareStage` 是身份标识符**（`_middleware/types.py:101-105`）——`__hash__=id(self)` + `__eq__=is`，让 stage 像 enum 一样安全。**适用**：任何「命名拦截点」框架。
3. **`HookOrder` 整数 slot 隔离三方位置**（`hooks/registry.py:30-41`）。**适用**：多插件/多中间件栈需要「第三方永远在用户前后」。
4. **「typed action + action×event 矩阵」决策表**（`interventions/actions.py:117-138`）。**适用**：所有事件驱动的策略引擎/规则引擎。
5. **`_link_cancel_signal` 双源取消**（`agent/agent.py:120-133`）。**适用**：任何「既要外部取消又要内部取消」的库。
6. **预设策略 + 内部插件分解**——`0011-context-strategy.md` 的 `ContextManager` 把 `auto` 预设拆成 `ToolResultCache + ContextCompression`；用户感知是字符串，框架感知是组合。**适用**：任何想给「80% 用户一行、20% 用户深度」提供配置的库。
7. **政策语言即策略**——`vended-interventions/cedar/` 把 Cedar 政策文件路径 / 内联字符串 / entities JSON 一起作为 `CedarAuthorization` 输入；schema 自动从 tool 定义生成。**适用**：用 Cedar / Rego / OpenFGA 做授权的任何 SaaS。
8. **`tracking_id` 单调 + 内容类型保真**（`tools/tools.py` + `types/content._generate_tracking_id`）——每条消息有 monotonic id，使 session 恢复 / subagent 消息注入都可追溯。**适用**：任何「长会话 + 多 agent 嵌套」的对话系统。
9. **Tool 名字前置冲突检测**（`harness-py/src/strands_harness/agent.py:249-552`，`_check_name_collisions`）。**适用**：任何插件式 SDK 在构造期前置发现冲突。
10. **失败策略三态 `throw/deny/proceed`**（`handler.py:32-40`、`registry.py:250-267`）。**适用**：所有策略引擎/handler 框架。

### 关键设计决策

值得学习的架构选择和 trade-off：

- **三层拦截点（Hook / Intervention / Middleware）的语义分离**——hooks 是任意回调按 `HookOrder` 排序只做观察修改；interventions 返回 typed action 之一，按注册顺序级联（短断 + 累积）；middleware 是显式三相 `Input/Wrap/Output` 有 phase 排序和 Outer-first 组合。**Trade-off**：API 表面积大、学习曲线陡。**学到什么**：把「三种需求」从一片沼泽里拆成三套正交词汇，远比把它们塞进一个万能 Hook 更好用。
- **「Plugin 是高阶抽象、Hook 是低阶原语」的概念分工**——`team/designs/0001-plugins.md` 显式划分「一个是为 agent 行为变化，一个是为 lifecycle 事件回调」，避免概念重叠。**学到什么**：抽象命名分裂不如「两个名字 + 一个文档」明确分工。
- **「`AGENTS.md` 跨 SDK 字符串字面量约定」**——`AGENTS.md:48-53` 写出 `tool_use ↔ toolUse`，但 `inputSchema`、`tool_use_id` 在两个 SDK 里**字面相同**（与 provider 协议耦合）。**学到什么**：跨语言 SDK 对齐时，**契约字段 ≠ 内部字段**——这是「对外耦合、对内解耦」的清晰边界。
- **API 设计：fail-open vs fail-closed 必须显式**——`InterventionHandler.on_error` 三态（throw/deny/proceed）写在 docstring 里，明说「proceed is dangerous」。**学到什么**：默认行为要写「为什么不安全」远比写「默认是安全的」有效。
- **「同期双 SDK monorepo + 双轨制 release」**——主线 `python/v1.57.0` 走 1.x 稳定；下一代 `harness-python/v0.1.2` 走 0.1 探索；tag 命名分轨。**学到什么**：当需要「稳定 + 重构」同时进行时分轨发版，比「all-in」更稳。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | Strands Agents | LangGraph | AutoGen/AG2 | Google ADK | CrewAI |
|------|------|------|------|------|------|
| 抽象风格 | **model-driven loop + hooks**（隐式循环） | 显式 state graph | 多 actor 对话 | 代码优先 + Vertex 托管 | role/task/crew 心智 |
| Python/TS 一等 | **都对等**（42.3% / 42.1%） | 主 Python + 客户端 TS | 主 Python | 主 Python | 主 Python |
| 双 SDK 同抽象 | **完全镜像** | 部分 | 无 TS | 无 TS | 无 TS |
| 工具拦截粒度 | **三层**（hooks/intervention/middleware） | 自定义节点 | 自动对话 | callback hook | process class |
| MCP 原生 | **是** + MCP server 仓库 | 是 | 是 | 是 | 社区 |
| A2A 原生 | 是 | 部分 | 否 | 是 | 否 |
| 授权策略 | **Cedar WASM 内建** + OPA + LLM Steering | 外部 | 外部 | IAM | 外部 |
| 可观测性 | OTel 全套（一等公民） | LangSmith 生态 | 外部 | Cloud Trace | 外部 |
| 多模态音频 | **BidiAgent / Nova Sonic 内建** | 外部 | 否 | Gemini Live | 否 |
| 多租户 | SessionManager read-only 模式（#2020） | 需自建 | 需自建 | Vertex 多租户 | 需自建 |
| 社区规模 | 7.8K / 304 贡献 | 18K+ | 61K（ms）/4.9K（ag2） | 21K | 35K+ |

### 差异化护城河

- **技术护城河**：intervention 一等原语 + Cedar WASM 授权 + 三阶段 middleware + HookOrder 强制 slot —— 任何竞品要抄都得重写整层抽象。LangGraph 把这些塞到「节点 + edge」里，CrewAI 把这些塞到「process class」里，**抽象密度**都比 Strands 弱一档。
- **生态护城河**：AWS Bedrock / Anthropic / OpenAI / Gemini 同步首发 + MCP/A2A/OTel 全栈 + Apache-2.0 + 304 跨组织贡献者——「新模型新协议都能很快跑出官方示例」。
- **信任护城河**：304 贡献者跨组织、Apache-2.0 无 dual license、`team/TENETS.md` + `team/designs/*.md` 把决策过程完全公开——社群能 git-blame 任何一行设计的来龙去脉。
- **治理护城河**：**22 个 RFC + 6 条 tenets + AGENTS.md** 这个公开 RFC 流程，远超大多数 agent framework 的「读完 README 就完事」。

### 竞争风险

- **LangGraph**（如果 model-driven loop 退潮 / 用户更想要显式 graph 可视化）。
- **OpenAI Agents SDK**（如果 OpenAI Realtime API 把异步 loop 也标准化 + Azure 集成的护城河跟上）。
- **Amazon Bedrock AgentCore**（如果客户全上托管控制面，Strands 的 in-process 优势就只剩「想自己跑循环的人」——这部分人有，但不是金主）。

### 生态定位

**「model-driven loop + hooks 严格抽象 + harness 电池版」三层** —— 竞争对手要么图（LangGraph）、要么多 actor（AutoGen）、要么托管（Bedrock AgentCore）。Strands 卡位「想自己跑 loop 但又不想裸写」的中间地带，把「自建 agent loop」从 3 个月项目缩成 1 行代码。

## 套利机会分析

- **信息差**：低。Strands 已是大众热门（7.8K stars、AWS 背书），没低估空间。**真正的信息差在 RFC**——22 个 `team/designs/*.md` 是高质量设计输入，但传播度远低于 star 数。
- **技术借鉴**：极高。本仓库的可复用模式章节列了 10 条可直接抄走的设计（决策矩阵、HookOrder slot、Cedar 政策、MiddlewareStage token、fail-mode 三态等），不依赖 Agent 框架本体。
- **生态位**：填补了 LangGraph（显式图）和 AutoGen（多 actor 对话）之间的「我要单 agent 跑得生产+」空白。BidiAgent 是个未被大多数 agent framework 覆盖的音频多模态缝隙。
- **趋势判断**：Anthropic / OpenAI / Google 三家模型 API 稳定 + MCP 协议成熟 + Cedar 可用——这是 agent SDK 真正可能规模化的窗口。Strands 16 个月 commit 量持续递增（2026-09 当月 178 commit），还在涨，没到顶。

## 风险与不足

诚实评估：

- **正处重组迁移期**：仓库内部 `src/strands`（旧路径）与 `strands-py/src`（新路径）并存、`src/content` 与 `docs/examples` 并存、`tests/strands` 与 `strands-py/tests` 并存。**外部教程/博客里出现的导入路径和现行主路径可能不一致**——读源码别依赖博客。
- **正处「边生产边重写」阶段**：0.1.x 的 harness-py / harness-ts 是项目主动的下一代抽象——主 SDK 1.x 已稳定但 harness 部分 API 仍未最终定形。选用 `strands-harness` 版本需关注 changelog。
- **依赖本地化**：404 的 Bedrock ConverseStream AccessDenied（#38）反映 provider 错误归一化的复杂度——某些 provider 错误信息在归一化层丢失了细节，生产调试要进 stack trace 翻 SDK 源码。
- **本地推理后端仍是差距**：VLLM/SGLang 适配（#1368）17 comments 闭环，但相对云端 provider 的成熟度仍有差距。对「不想被云端闭源绑死」的用户来说这是一道隐形门槛。
- **多租户产品路线未闭环**：SessionManager read-only 模式（#2020）仍是 open issue，企业级多租户上生产需要自建保护层。
- **WebSearch 不可用期内的素材缺失**：本次 WebFetch 官网+ DeepWiki + WebSearch 多次受限，项目级「独立分析文章」采集不全——读者自己 review 时建议把 `team/designs/*.md` 读完，这是项目最独特的资产。

## 行动建议

### 如果你要用它

- **从 `harness-py` 的 `create_harness()` 入手**，而不是直接用 strands-py 的 `Agent(model=..., tools=...)`。前者覆盖 80% 用户场景（一行起步、context/session/memory 自动接管），后者面向 20% 深度定制需求。
- **provider 顺序建议**：先选 Anthropic（Claude Sonnet/Opus）或 OpenAI（GPT-4o）做原型；上生产再切 AWS Bedrock（同模型 + VPC + 数据不出公司）。**不建议直接上 Gemini Live 或 BidiAgent**——BidiAgent 还在 experimental/，Nova Sonic 兼容性 best-effort。
- **如果做企业级 multi-tenant**：先 fork + 给 SessionManager 加 read-only 模式（跟着 #2020 走，或自己实现），不要等合并。
- **如果做本地推理**：用 LiteLLM provider 接入 VLLM/SGLang，等待 #1368 的官方实现，**别直接绑到一个 Python 推理后端的 pyproject 依赖**——会拖死版本升级。
- **比 LangGraph**：如果你想写循环而不是图、想换 provider 不动业务代码、需要 MCP/A2A/OTel 配套——选 Strands。
- **比 AutoGen**：如果你的核心场景是「单 agent 跑得生产」而不是「多 actor 对话编排」——选 Strands。

### 如果你要学它

按以下顺序读，依次吃透：

1. **`team/TENETS.md`**（6 条原则）——理解项目价值观与取舍。
2. **`team/designs/0007-intervention-primitive.md`** ——理解「Intervention 是一等 SDK 原语」的故事，**这是整个仓库最精华的 RFC**。
3. **`team/designs/0001-plugins.md`** ——理解 Plugin/Hook 的概念分工。
4. **`team/designs/0011-context-strategy.md`** ——理解 L0/L1/L2 三层 context 模型。
5. **`team/designs/0015-bidi-webrtc-design.md`** ——理解 WebRTC 双层抽象。
6. **`AGENTS.md`** ——理解跨 SDK 一致性约定。
7. **`strands-py/src/strands/interventions/handler.py:43-107` + `registry.py:59-63`** ——读 `_is_overridden` 类级 override 检测模式。
8. **`strands-py/src/strands/_middleware/types.py:86-103`** ——读 `MiddlewareStage` token 设计。
9. **`strands-py/src/strands/hooks/registry.py:30-41`** ——读 `HookOrder` 整数 slot 设计。
10. **`strands-py/src/strands/interventions/actions.py:117-138`** ——读 typed action × event 决策矩阵。
11. **`strands-py/src/strands/agent/agent.py:120-133` (`_link_cancel_signal`)** ——读「为什么不用 Event.wait()」。
12. **`harness-py/src/strands_harness/agent.py:249-552`** ——读 `create_harness()` 装配 + 前置冲突检测。
13. **`vended-interventions/cedar/`** ——读 Cedar 政策语言接入模式。

学完上述等于把 agent framework 的「干预原语 + middleware 设计 + 工具授权」全学了一遍——这套设计模式不依赖 Agent 本体也能用到其他项目。

### 如果你要 fork 它

可改进的方向（按可行性 × 价值排序）：

1. **给 SessionManager 加 read-only 模式**（#2020）——多租户产品化的最后一公里。
2. **完善 VLLM/SGLang provider**（#1368）——本地推理需求强。
3. **迁移到 WASM Component Architecture**——如果未来 WIT / WASI 标准化，可以把 `cedar-wasm` + `mcp-schema-generator-wasm` 升级成真正的 sandbox 框架（这是 Phase 1 一度误判实际不存在的能力，是真正的「未来可拓展方向」）。
4. **统一 `src/strands` 与 `strands-py/src` 双路径**——清理重组期的历史包袱，降低新用户上手门槛。
5. **简化 harness 的 8 个开关**——目前 `create_harness(**kwargs)` 把所有开关平铺，下个版本可以走 Pydantic 模型 + Preset 名（`auto` / `production` / `research`）的二级抽象。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/strands-agents/harness-sdk（已收录；18 章节；最后索引 2026-08-19；**注意 DeepWiki 提到的「WASM Component Architecture」在本仓库代码层目前并不存在，主要是 Cedar 政策引擎的 WASM 绑定**，以仓库代码为实） |
| Zread.ai | 未确认（环境受限拿到 Cloudflare 403） |
| 官网 | http://strandsagents.com/ |
| 关联论文 | 无（SDK 非研究项目） |
| 在线 Demo | 无公开 playground（`strands-cli` 自带 terminal chat 入口，需自建） |
| 设计 RFC（仓库内最被低估的资源） | `team/designs/*.md`（22 份，从 `0001-plugins` 到 `0015-bidi-webrtc-design`） |

---

**报告生成于**：2026-09-23（自动化 repo-miner 分析）
**方法**：三阶段分析（Phase 1 网络 + Phase 2 元 + Phase 3 内容），Phase 1 的 WASM Component Architecture 误判已被 Phase 3 主动更正；建议读者以仓库代码 + `team/designs/*.md` 为准。

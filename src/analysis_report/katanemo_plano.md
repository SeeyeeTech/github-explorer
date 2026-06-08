# 被 DigitalOcean 收购的 AI 网关 Plano：在 Envoy 之上用 4B 小模型替 GPT-4 做 agent 路由

> GitHub: https://github.com/katanemo/plano

## 一句话总结

Plano 是 Katanemo 出品的「AI-native 代理 / 数据平面」：把 agentic 应用上生产时每个团队都要重写的「隐藏中间件」——agent 路由/编排、安全护栏、可观测、模型 Provider 适配——从框架和业务代码里抽出来，下沉到一个基于 Envoy 的进程外统一数据平面。它最大的赌注是**用自研 4B 小模型替代规则或 GPT-4 来做网关层的路由与护栏**（官方称比 GPT-4 路由快约 12 倍、省约 44 倍）。它的前身是 Katanemo 的 Arch 网关，2026 年 4 月团队被 DigitalOcean 收购。

## 值得关注的理由

1. **一个「瘦 WASM filter + 胖 sidecar」的网关架构范式**：LLM 语义里沙箱友好的轻活（Provider 选择、鉴权改写、流式帧解码、限流）用 Rust 编译成 Envoy proxy-wasm filter 跑在数据面；调小模型、多 agent 编排、行为信号这些重活拆到独立的 `brightstaff` Rust 进程。这套「受 WASM 限制就把重逻辑拆进 sidecar」的二分，是任何想在网关跑重逻辑的人值得学的。
2. **把「路由」建模成带 schema 约束输出的小模型分类**：路由不写 if/正则，而是把候选 agent 的自然语言描述塞进 prompt 喂给 4B 的 `Plano-Orchestrator`，让它输出 `{"route": [...]}`。工程细节见功力——自定义 `SpacedJsonFormatter` 让 Rust 输出的 JSON 间距与 Python `json.dumps` 逐字节一致以对齐训练分布、中段截断保留任务框定与真实诉求、还有基于 token logprob 熵的函数调用幻觉检测。
3. **一桩「创业被上市云厂收编」的样本，且收购已写进代码**：2026-04 DigitalOcean 收购 Katanemo，创始人 Salman Paracha（前 AWS 8 年）任 DO SVP of AI。这不只是新闻——`hermesllm` 的 `ProviderId` 枚举专列了 `DigitalOcean`、成本路由直连 `api.digitalocean.com` 的定价 API 给候选模型按价排序。看一个「研究 + 基础设施」型创业如何成为云厂的 agentic 运营层。

## 项目展示

![Plano 架构](https://raw.githubusercontent.com/katanemo/plano/main/docs/source/_static/img/plano_network_diagram_high_level.png)

数据平面网络时序：client → Envoy（Rust WASM filter 拦截/鉴权）→ brightstaff 编排（调小模型选 agent/model）→ 各 agent（OpenAI 兼容端点）。下图是零代码 OTEL 端到端追踪：

![自动追踪](https://raw.githubusercontent.com/katanemo/plano/main/docs/source/_static/img/demo_tracing.png)

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/katanemo/plano |
| Star / Fork | 6,577 / 429 |
| 代码行数 | 96,545 行（Rust 37.4% 数据平面核心 + Python 15% 控制面 + TSX 5% 可观测面板；JSON 26% 为配置/demo 数据） |
| 项目年龄 | 22.9 个月（2024-07-09，前身 Arch/archgw） |
| 开发阶段 | 密集开发（近 90 天 79 commit，职业团队周末 10.6%） |
| 贡献模式 | 小核心团队主导（52 人，Adil Hafeez 占约 27%、创始人 Salman Paracha 次之，Top 占 50%） |
| 热度定位 | 大众热门（6.5K star，稳步增长） |
| 质量评级 | 代码「优」 文档「优」 测试「优」 CI「优」 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

owner 是 Katanemo Labs（bio「Intelligent infrastructure primitives for GenAI」，小团队）。**创始人/CEO Salman Paracha** 前 AWS 约 8 年主导 Serverless（SAM、Serverless Application Repository），更早在 Oracle 带云产品；头号工程师 **Adil Hafeez**（1654 commits，约占全仓 27%，绝对技术主力）。值得注意的是贡献者里有 **junr03（José Ulises Niño Rivera）——Envoy 核心维护者之一**，印证 README 自述「built on Envoy by its core contributors」。这是该赛道少见的「数据平面工程（Envoy 核心）+ 资深云产品（AWS）+ 模型研究」三强班底。

**重大事件：2026-04-02 DigitalOcean（NYSE: DOCN）收购 Katanemo Labs**，Salman Paracha 出任 DO SVP of AI，Plano 随团队并入、作为 DO「面向 agentic 时代的推理云」运营层。一家「研究 + 基础设施」型创业被上市云厂收编——对可信度是强背书，但「独立创业」叙事已转为「云厂战略资产」。

### 问题判断

要解决 agentic 应用「上生产」时每个团队都重写的「隐藏中间件」（README 原话 hidden middleware）：① agent 路由/编排（写 intent classifier + routing logic）、② 安全护栏/moderation/memory（jailbreak、PII）、③ 评估与可观测（给每个 service 插 OTEL）、④ 模型/Provider 适配。现有方案不够在于：框架进程内绑定（LangGraph/CrewAI）使编排与业务耦合、换语言就重写；纯规则网关不智能；用 GPT-4 做路由太贵太慢。Plano 的承诺是 agent 只需实现一个 OpenAI 兼容的 `/v1/chat/completions` 端点，其余交给数据平面，配置全在一份 YAML。

### 解法哲学

「不要在每个 codebase 里重复实现不该 bespoke 的东西，把它移到进程外。」三条贯穿全代码：

1. **进程外、框架无关**：落点是 Envoy filter（`crates/llm_gateway`/`prompt_gateway` 编译成 `wasm32-wasip1` cdylib），而非 SDK；
2. **小模型替代规则与重模型**：路由走 `Plano-Orchestrator`(4B)、护栏走 `Arch-Guard`、函数调用走 `Arch-Function`；
3. **声明式而非命令式**：用户「声明 agent 的自然语言描述」，由 `AgentSelector` 直接喂给编排小模型当路由候选，不写路由代码。

### 战略意图

代码里能直接读出 DigitalOcean 收购的战略落地（不只是新闻）：`hermesllm` 的 `ProviderId` 枚举专列 `DigitalOcean`（默认 base_url `inference.do-ai.run`），`ModelMetricsService` 硬编码 `api.digitalocean.com/v2/gen-ai/models/catalog` 按 input+output 价给候选模型排序实现「选最便宜模型」。Plano 正成为 DO agentic 推理云的运营层——路由按 DO 实时价格择优、护栏/编排小模型托管在 DO 端点。这是从「独立 AI 网关」到「云厂 agentic 数据平面」的战略跃迁。

## 核心价值提炼

### 创新之处

1. **Envoy + Rust→WASM 的 LLM/agent 数据平面**（新颖度 4/5，实用性 4/5，可迁移性 4/5）：`llm_gateway`/`prompt_gateway` 用官方 `proxy-wasm` 实现 `StreamContext`、编译成 wasm 作 Envoy plugin，只做 LLM 语义（Provider 选择、鉴权改写、SSE/Bedrock 流解码、token 计数、限流）；Envoy 出连接管理。白嫖 Envoy 十年生产沉淀，代价是 wasm 沙箱内不能跑重活——于是「重逻辑」被拆到独立的 `brightstaff` 进程，形成「瘦 filter + 胖 sidecar」二分。
2. **网关智能用专用小模型，路由 = LLM 文本分类**（新颖度 5/5，可迁移性 3/5）：`OrchestratorModelV1` 把候选路由序列化进 XML 标签 prompt（`temperature: 0.01`，要求只回 `{"route": [...]}`）。工程细节：`SpacedJsonFormatter` 让 Rust 输出 JSON 与 Python `json.dumps` 逐字节一致以对齐训练分布、`MAX_ROUTING_TURNS=16` + 中段截断（头 60% 留任务框定、尾 40% 留真实诉求）。小模型路由准确率是核心风险（多意图时「取第一个」是已知妥协），但延迟/成本碾压 GPT-4。
3. **基于 token logprob 熵的函数调用幻觉检测**（新颖度 5/5，可迁移性 3/5）：`function_calling.rs` 让 `Arch-Function` 返回 logprobs，流式逐 token 算 `entropy`/`varentropy`，超阈值即判定工具调用幻觉并阻断。这是把「不确定性量化」用在网关层拦截幻觉工具调用的少见实践。
4. **类型化的跨 Provider 协议转换矩阵（hermesllm）**（新颖度 3/5，可迁移性 4/5）：用 Rust `TryFrom<(ProviderRequestType, &SupportedUpstreamAPIs)>` 把客户端 API 形状（OpenAI ChatCompletions/Responses、Anthropic Messages、Bedrock Converse）转成上游需要的形状（含链式转换），`ProviderId::compatible_api_for_client` 是一张大 match，`normalize_for_upstream` 处理各家 quirks。相比 LiteLLM 的 Python 字典转换，编译期就挡掉非法转换、零反射、可在 wasm 内跑。
5. **零代码 Agentic Signals + OTEL**（新颖度 4/5）：`signals/` 把三层行为信号（交互层 misalignment/stagnation、执行层 failure/loops、环境层 exhaustion）命中即给 OTEL span 名追加 🚩 emoji，下游按 span 名搜异常会话，全程无需用户埋点。

### 可复用的模式与技巧

- **瘦 WASM filter + 胖 sidecar 进程二分**：沙箱友好的轻逻辑放 Envoy wasm，重逻辑放独立进程经内部 header 协议通信——任何想在网关跑重逻辑但受 wasm 限制的场景。
- **路由 = 带 schema 约束输出的小模型分类 + 与训练分布对齐的 prompt 工程**：`SpacedJsonFormatter`、中段截断、turn-cap、`fix_json_response`——所有用小模型做结构化决策的系统。
- **类型化转换图 + per-provider normalize 钩子**：多协议/多供应商适配层的范本。
- **会话粘性路由缓存（memory/redis 抽象 + TTL + tenant 前缀）**：多轮要稳定路由到同一目标的网关。
- **指标驱动的候选排序（cost via 定价 API / latency via Prometheus）**：动态择优后端的负载/成本调度。
- **声明式配置编译器**：用户简洁 YAML → 编译成底层引擎（Envoy）完整配置 + 自动补齐隐式依赖。

### 关键设计决策

最值得记录的是**「网关智能用专用小模型」这个根本赌注**及其工程化。路由不是规则、也不是调 GPT-4，而是把候选 agent 的自然语言描述喂给 4B 的 `Plano-Orchestrator` 做分类决策（`crates/brightstaff/src/router/orchestrator_model_v1.rs`）。为了让小模型可靠，团队做了大量与训练分布对齐的工程：自定义 serde formatter 保证 JSON 字节级一致、温度压到 0.01、token 预算 + 中段截断、JSON 容错修复；函数调用还加了 token 熵的幻觉检测。这套「把网关的智能决策下沉到自研小模型 + 围绕小模型做确定性工程」的组合，是 Plano 区别于 LiteLLM（纯协议层）、Portkey（规则护栏）、Envoy AI Gateway（纯流量层）的根本差异——也是其护城河（小模型权重）与风险（准确率难外部验证）的同源所在。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | Plano | LiteLLM | Portkey | Envoy AI Gateway |
|------|------|------|------|------|
| Stars | 6.5K | ~49.6K | ~12K | ~1.7K |
| 技术栈 | Rust + Envoy 数据平面 | Python proxy/SDK | 网关 + 托管控制面 | Envoy Gateway |
| 网关智能 | 自研小模型（路由/护栏/函调） | 规则/fallback | 规则护栏 | 纯流量层 |
| agent 编排 | 内建（brightstaff） | 无 | 无 | 无 |
| 定位 | agentic 数据平面 | 最全协议层 | 企业 AI 网关 | GenAI 流量管理 |

### 差异化护城河

① Envoy 核心贡献者血统（数据平面工程别人难复刻）；② 自研小模型矩阵（4B 路由 / Arch-Function / Arch-Guard，权重是壁垒）；③ DigitalOcean 收购背书 + 深度集成（成本路由直连 DO 定价、DO 推理端点），有云厂分发渠道。真正难复制的不是网关本身，而是「Envoy 数据平面 + 自研小模型 + agentic 编排」三者的组合——竞品中没有第二家同时具备。

### 竞争风险

- **star 与生态显著落后** LiteLLM（49.6K）/Portkey（12K），赛道认知度与覆盖广度是劣势；
- **仍 0.x**（release 0.4.23），API 未稳、保留破坏性变更空间；
- **被 DO 收购后开源走向不确定**（会否向 DO 云倾斜）；
- **小模型路由/护栏准确率是产品成败关键但外部难独立验证**（权重托管在 katanemo/DO 端点）；
- **Arch→Plano 改名未竟**：大量 `x-arch-*` header、`Arch-Function`/`Arch-Guard` 命名、CLI 仍从 `katanemo/archgw` 拉二进制——存在迁移债。

### 生态定位

「agentic 时代的 Envoy/Istio」——不是框架，是治理 agent 间与 model 间流量的数据平面；与编排框架（LangGraph 进程内）互补、与协议层（LiteLLM）部分重叠但更进一步、与纯网关（Envoy AI Gateway/Portkey）正面竞争且叠了智能层。

## 套利机会分析

- **信息差**：中文圈对「Arch→Plano 改名 + 被 DigitalOcean 收购 + 用自研小模型做网关路由/护栏」这条线几乎没有系统梳理；技术点（Envoy + Rust 数据平面 + 4B 路由模型 + token 熵幻觉检测）有深度可挖，是高确定性的差异化选题。
- **技术借鉴**：瘦 WASM filter + 胖 sidecar、小模型做结构化决策 + 对齐训练分布的工程、类型化 Provider 转换矩阵、token 熵幻觉检测、声明式配置编译器——这些可迁移到任何 API 网关、多 Provider 适配层、用小模型做决策的系统。
- **生态位**：填补「agentic 流量的进程外数据平面」空白，介于「LLM 网关」与「agent 框架」之间。
- **趋势判断**：踩在「agentic app 上生产需要新基础设施」的趋势上，被 DO 收购获得云厂分发；但要警惕被收购后开源投入与中立性的变化。

## 风险与不足

- **API 未稳**：仍 0.4.x，schema 在演进，早期采用者要做好跟版本准备。
- **改名迁移债**：Arch→Plano 未竟，CLI 仍依赖 `katanemo/archgw` 拉二进制、内部 `x-arch-*` header 与 `Arch-*` 模型命名混杂，老用户有配置/命名迁移成本。
- **小模型黑箱**：核心智能依赖托管的自研小模型，路由/护栏准确率外部难独立验证，且免费托管 vs 自部署的权衡影响生产可用性。
- **编排表达力弱**：当前是顺序 filter chain + 多意图取首，不是 LangGraph 那样的任意 DAG/循环/人在环——复杂工作流无处安放（要回退到 agent 内部代码）。
- **收购后不确定性**：开源走向、社区投入是否会向 DigitalOcean 云倾斜，有待观察。

## 行动建议

- **如果你要用它**：适合「已有多个 agent / 多 Provider，要把 demo 推上生产、统一治理/观测/护栏」的团队；也可当「Rust 版 LiteLLM + 编排」用（三能力模块化，可只用 LLM router、只用编排或全栈）。`planoai up config.yaml` 零配置起栈。复杂图状编排仍用 LangGraph（可与 Plano 叠加）。注意 0.x API 变动与改名迁移债。
- **如果你要学它**：直奔 `crates/brightstaff/src/router/orchestrator_model_v1.rs`（小模型路由 + SpacedJsonFormatter）、`crates/brightstaff/src/handlers/function_calling.rs`（token 熵幻觉检测）、`crates/hermesllm/src/providers/`（类型化 Provider 转换矩阵）、`crates/llm_gateway/src/stream_context.rs`（Envoy WASM filter）、`crates/brightstaff/src/signals/`（零代码行为信号）。这五处是工程精华。
- **如果你要 fork / 借鉴它**：「瘦 WASM filter + 胖 sidecar」与「类型化 Provider 转换矩阵」是可直接迁移的两套设计；但自研小模型是壁垒，外部难完全复刻其路由/护栏能力。注意 Apache-2.0。

### 知识入口

| 资源 | 链接 |
|------|------|
| 官方文档 | https://docs.planoai.dev（Quickstart / LLM Router / Orchestration / Filter Chains / Observability） |
| DeepWiki | https://deepwiki.com/katanemo/plano（已收录，覆盖四组件架构/路由/编排/部署） |
| 自研模型 | HuggingFace https://huggingface.co/katanemo （Arch-Function / Arch-Guard / Arch-Router 系列） |
| 收购公告 | [DigitalOcean Acquires Katanemo Labs](https://www.digitalocean.com/blog/digitalocean-acquires-katanemo-labs-inc) |

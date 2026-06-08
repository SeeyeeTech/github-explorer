# 连 TensorRT 都是它的一个后端：微软 ONNX Runtime 怎么用一套抽象统一 20+ 推理硬件

> GitHub: https://github.com/microsoft/onnxruntime

## 一句话总结

ONNX Runtime（ORT）是微软主导的跨平台 ML 推理/训练引擎：一个用 PyTorch/TF/sklearn 训练并导出成 ONNX 格式的模型，靠它能在 CPU/GPU/NPU、Linux/Windows/Mac/iOS/Android/浏览器上以最优性能运行。它的灵魂是 Execution Provider（EP）抽象——一套统一 API 把同一张计算图路由到 20+ 种硬件后端，连 NVIDIA TensorRT、Intel OpenVINO 这些竞品都得降格成它的一个 EP 才能进入这个生态。

## 值得关注的理由

1. **一个「能力声明 + 优先级路由 + 自动回退」的可复用调度范式**：框架不预设任何硬件知识，而是反问每个后端「这张图里哪些节点你能跑？」（`GetCapability`），按用户给的优先级列表贪心分配，剩下的自动落到永远兜底的 CPU EP。这套思路可直接复刻到任何「一套 IR → N 种异构后端」的系统（数据库执行引擎、跨云调度、跨 GPU 厂商计算栈）。
2. **一个反复出现的「函数指针间接层」母题**：ORT 在三个层次用同一招换解耦——ABI 层（`OrtApi` 函数指针表 + 末尾追加永不改的 COM 式纪律）、后端层（`IExecutionProvider` 虚表 / Plugin EP 的 C ABI）、指令集层（`MLAS_PLATFORM` 按 CPUID 运行时派发汇编 kernel）。看它如何把编译器/操作系统的成熟思想搬进 ML 运行时，是一堂系统设计课。
3. **一桩「掌握标准 + 做实现 + 自家自用」的平台战略样本**：微软同时握住定义格式（ONNX）、做首席运行时（ORT）、自家产品（Windows ML/Office/Bing）dogfood 三张牌，把 ORT 做成「ML 部署层的中立操作系统」——不靠单点峰值性能取胜，而靠抽象与生态。最新的 Plugin EP（独立 wheel 分发）更把硬件接入权下放给第三方，巩固「平台」而非「产品」。

## 项目展示

![ONNX Runtime Logo](https://raw.githubusercontent.com/microsoft/onnxruntime/main/docs/images/ONNX_Runtime_logo_dark.png)

核心架构（一份 ONNX 模型 → InferenceSession 加载/优化/分图 → 按 EP 优先级路由到多硬件后端，不支持的算子回退 CPU）；可在官网 https://onnxruntime.ai/docs/execution-providers/ 看 EP 路由架构图。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/microsoft/onnxruntime |
| Star / Fork | 20,761 / 3,961 |
| 代码行数 | 413 万行（C++ 76.4%，核心系约 86% 含 CUDA/汇编；+ Python/C#/Java/TS/JS 多语言绑定，8,852 文件） |
| 项目年龄 | 约 7.5 年（2018-11-10 创建，每日活跃） |
| 开发阶段 | 稳定活跃（近 52 周 1,759 commit，周均约 34，近 4 周 209 小幅回暖） |
| 贡献模式 | 微软团队主导（395 人，Top 8 全是微软工程师、无机器人居首） |
| 热度定位 | 大众热门 / ML 部署层事实标准之一 |
| 质量评级 | 代码「优」 文档「优」 测试「优」 CI「优」 构建系统「优」 |

> 注：1.5GB 大仓库，用 depth-1 浅 clone 读码 + gh api 补提交历史（共 14,740 commit）。

## 作者视角：为什么存在这个项目

### 创始人/作者背景

owner 是微软，由内部专设的 **ONNX Runtime 团队**全职维护。核心贡献者（gh api Top 8）fs-eire、skottmckay、tianleiwu、edgchen1、yuslepukhin 等全是微软工程师，覆盖 Web/JS 后端、核心引擎、CUDA 算子、EP 等不同子域，共约 395 名贡献者（逼近 GitHub 上限）。值得一提的是**榜首是真人而非合并机器人**——与许多靠 dependabot 撑提交量的超大仓库不同，ORT 的高频提交是一支专职团队的直接投入。

与 ONNX 格式的关系是理解它的钥匙：**ONNX（Open Neural Network Exchange）是 2017 年微软联合 Facebook 发起的开放神经网络模型交换格式；ORT 是运行该格式的引擎**——格式是「一次导出」的标准，ORT 是「到处运行」的落地层。微软同时是格式发起方和首席运行时实现方，掌握标准 + 实现双重话语权。

### 问题判断

要解决的是 ML 模型部署的「硬件碎片化」与「框架锁定」：一个模型要落到 N 种硬件 × M 种 OS，传统做法是每个训练框架各带一个推理运行时、且与自家硬件强绑定；厂商运行时（TensorRT/OpenVINO）又专精单一硬件、互不通用。没有一层能用统一 API 同时调度 20+ 后端、并在缺失后端时优雅降级。`execution_provider.h` 的注释直接写出了三条设计戒律：EP 的 kernel registry 跨 session 共享、「加一个 EP 不需要改 ONNXRuntime 框架/session 代码」、「onnxruntime 不依赖任何特定 EP 库」——即框架对后端零依赖、后端对框架零侵入。

### 解法哲学

用「能力声明 + 优先级路由 + 自动回退」取代「硬编码后端分支」。框架不预设硬件知识，而是反问每个后端「这张图里哪些节点你能跑？」，按优先级贪心分配，剩下的天然落到 CPU。整个系统呈现一个母题：**用函数指针/虚表做间接层来换取解耦与可扩展**——在 ABI 层、后端层、指令集层都用了同一招。

### 背景知识迁移

把编译器/操作系统的成熟思想搬进 ML 运行时：图分割回退像「指令选择 + 寄存器溢出回退」；EP 优先级 + CPU 兜底像「驱动栈 + 软件渲染回退」；`OrtApi` 的「只在末尾追加、永不修改」像 Win32/COM 的 ABI 演进纪律；`MLAS_PLATFORM` 的 CPUID 运行时派发是经典的 function multiversioning。

### 战略意图

微软同时握住三张牌：定义格式（ONNX）、做首席实现（ORT）、自家产品自用（Windows ML/Office/Bing/Azure）。这让 ORT 成为「ML 部署层的中立底座」——竞品 TensorRT、OpenVINO 反而要降格成 ORT 的一个 EP（`core/providers/tensorrt`、`openvino`）才能进入这个生态。最新的 Plugin EP（`plugin-ep-cuda`/`plugin-ep-webgpu` 独立 wheel）进一步把硬件接入权下放给第三方，巩固「平台」而非「产品」的定位。近年 onnxruntime-genai 又把它从传统 CNN/分类推理延伸到 LLM 端侧推理新战场。

## 核心价值提炼

### 创新之处

1. **GetCapability 能力声明式图路由**（新颖度 4/5，实用性 5/5，可迁移性 5/5）：`IExecutionProvider::GetCapability(graph_viewer, ...)` 返回「我能跑的子图列表」；默认实现遍历节点、凡 kernel registry 查得到的认领为单节点子图，编译型 EP（TensorRT）则重写返回可融合的多节点子图（带 `MetaDef`）由框架调 `Compile()` 生成 fused kernel。后端主动声明、框架按优先级贪心分配，是「一套图路由到 N 个硬件」的灵魂。
2. **图分割 + 优先级贪心 + CPU 自动回退**（新颖度 4/5，实用性 5/5）：`graph_partitioner.cc` 按用户给的有序 EP 列表逐个询问、**先到先得**（已分配节点不能被后面的 EP 抢走），CPU EP 永远排最后兜底。精细处：`fallback_cpu_capability.h` 的 `GetCpuPreferredNodes` 会**主动**把 shape 计算等廉价算子留在 CPU——即便 GPU EP 能跑，因为为几个标量做 H2D/D2H 拷贝得不偿失。这是「边界代价感知的算子放置」。
3. **稳定 C API 函数指针表收敛全部语言绑定**（新颖度 3/5，可迁移性 5/5）：C++ 无稳定 ABI，ORT 把整个 API 暴露成一个巨型 `struct OrtApi`（成员全是 C 函数指针），入口 `OrtGetApiBase()->GetApi(version)` 做版本协商；ABI 演进靠铁律——`ORT_API_VERSION 28`、每函数标 `\since`、结构体「New fields MUST only be appended at the end」+「DO NOT MODIFY ABOVE」守卫。于是旧版编译的绑定永远能在新库上按偏移找到自己那段函数指针。Python/C#/Java/JS/Rust 都只需一层 FFI 薄封装。
4. **Plugin EP——把 EP 推过 C ABI 边界做成独立插件**（新颖度 4/5，可迁移性 4/5，当下最有借鉴价值）：`onnxruntime_ep_c_api.h` 把内部 `IExecutionProvider` 镜像成一对 C ABI 结构体（`OrtEpFactory` + `OrtEp`），插件 .so/.dll 只需导出 `CreateEpFactories`/`ReleaseEpFactory` 两个 C 函数 + `ort_version_supported` 协商版本；CUDA/WebGPU 插件作为独立 wheel 分发，各带 `MIN_ONNXRUNTIME_VERSION` 声明兼容下限。核心库瘦身、硬件厂商无需改主仓即可发版、用户按需安装后端——直击「打包臃肿 + 跨设备脆弱」痛点。
5. **MLAS 自研 CPU 计算库 + CPUID 运行时派发**（新颖度 3/5，可迁移性 2/5）：不依赖 Eigen/MKL（许可证/体积/对 AMD 不友好），自研 `MLAS_PLATFORM`——启动时用 `__cpuid` 探测指令集，把 GEMM 等指针绑到对应手写汇编 kernel（覆盖 SSE/AVX/AVX512/AMX、NEON/fp16、POWER/RISC-V），并内置 LLM 时代的 `qnbitgemm`（低比特权重 GEMM）+ `flashattn`。完全控制低比特量化与端侧 ARM，零外部许可证负担。

### 可复用的模式与技巧

- **能力声明 + 优先级路由 + 默认兜底层**：后端答「能跑啥」而非框架猜「派给谁」，优先级链贪心 + 末位永远可用的默认实现——插件化异构调度通用骨架。
- **C 函数指针表 + 末尾追加 ABI 纪律**：需长期跨语言/跨版本兼容的 SDK 的标准答案（COM/Win32 同源）。
- **CPUID/特性探测的运行时多版本派发**：单一二进制自适配硬件——SIMD 库、跨 ISA 计算。
- **内部虚接口镜像成 C ABI 工厂 + 版本协商**：让任意单体长出第三方插件生态的标准路径。
- **边界代价感知的算子放置**：分图时把廉价算子留在数据所在设备，避免跨设备拷贝吃掉收益。

### 关键设计决策

最值得记录的是 ORT 反复出现的「**三层同构的函数指针间接层**」：① ABI 层用 `OrtApi` 函数指针表 + 末尾追加纪律换取跨语言/跨版本稳定；② 后端层用 `IExecutionProvider` 虚表 / Plugin EP 的 C ABI 换取硬件可扩展与框架/后端双向零侵入；③ 指令集层用 `MLAS_PLATFORM` 按 CPUID 派发换取单一二进制自适配。同一种「加一层间接换解耦」的手法，在三个尺度上贯彻到底——这是一个把「机制与策略分离」做到极致的工程范本（关键文件 `include/onnxruntime/core/framework/execution_provider.h`、`onnxruntime/core/framework/graph_partitioner.cc`、`include/onnxruntime/core/session/onnxruntime_c_api.h`、`onnxruntime/core/mlas/lib/platform.cpp`）。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | ONNX Runtime | NVIDIA TensorRT | Apache TVM | llama.cpp / ExecuTorch |
|------|------|------|------|------|
| 路线 | 运行时调度（即时通用） | GPU 端到端编译（AOT 极致） | ML 编译器（AOT 深优） | LLM/端侧专用 |
| 硬件 | 20+ EP 统一（中立） | 锁 NVIDIA | 多后端（编译） | CPU/消费级（轻量） |
| 与 ORT 关系 | — | 是 ORT 的一个 EP | 可作 ORT 后端 | onnxruntime-genai 正面竞争 |
| 优势 | 跨硬件可移植 + 微软背书 | NVIDIA 单卡峰值 | 编译深优、产物精简 | LLM 端侧体验顺、社区火 |

### 差异化护城河

中立标准（ONNX 格式）× EP 统一抽象（25 内建 + 任意 Plugin EP）× 微软全栈背书与自用 × 推理+训练+GenAI 同栈。竞品大多只占其中一格，且头部专精运行时（TensorRT/OpenVINO）反成 ORT 的 EP。它不做「最快的单点运行时」，做「ML 部署层的中立操作系统」——靠抽象与生态而非单点峰值取胜。

### 竞争风险

- **单硬件峰值性能让位于专精方案**：纯 NVIDIA 环境下延迟/吞吐显著落后 TensorRT；
- **部署脆弱**：EP 跨设备依赖缺失即失败、用户需懂硬件排优先级（Plugin EP 正在缓解，但仍是社区长期痛点）；
- **构建体积大**：移动/Web 需自定义构建裁剪算子集；
- **LLM 端侧被蚕食**：llama.cpp/ggml 在消费级设备 LLM 推理上更轻更顺、社区更热，onnxruntime-genai 面临正面竞争；跨引擎精度一致性也是长期议题。

### 生态定位

ML 部署层的中立底座/事实标准之一，正从传统模型推理向 LLM 端侧推理（genai）扩张。硬件厂商把自家加速器接成一个 EP 即可进入整个 ONNX 生态——这种「让对手成为自己后端」的引力是它真正的壁垒。

## 套利机会分析

- **信息差**：头部成熟项目无信息套利，但有「认知深度套利」——大多数人只把它当 `pip install onnxruntime` 黑盒，对其 Execution Provider 架构、与 ONNX 标准的分层关系、跨硬件路由机制理解很浅，深度解读其架构哲学仍有强内容价值。
- **技术借鉴**：能力声明式路由、稳定 C API + ABI 纪律、内部虚接口镜像成 C ABI 插件、CPUID 多版本派发、边界代价感知算子放置——这五套设计可迁移到数据库执行引擎、跨语言 SDK、插件系统、SIMD 库、异构内存调度等完全不同的领域。
- **生态位**：填补「框架中立 + 多硬件统一 + 生产级背书」的通用运行时位；专精性能让位于 TensorRT 等，但「一层打天下」的覆盖广度无对手。
- **趋势判断**：Plugin EP 插件化（核心 + 可插拔 EP 各自演进）是架构拐点；onnxruntime-genai 把它推向 LLM 端侧——既是新增长点也是与 llama.cpp 的正面战场。

## 风险与不足

- **开箱即跑体验偏弱**：EP 优先级与依赖需用户具备硬件知识，缺/不兼容 EP 即失败，是社区长期痛点。
- **单点峰值性能非第一**：通用调度而非端到端编译，纯单一硬件场景打不过专精运行时。
- **体积与裁剪成本**：端侧需 minimal/reduced-ops 自定义构建。
- **C++ 公共 API 无稳定 ABI**：刻意以 C API 收敛规避，C++ 头属内部/便利封装——直接用 C++ 接口的用户需注意版本绑定。

## 行动建议

- **如果你要用它**：当你需要「一套推理层覆盖多种硬件/OS、可移植打包交付」时它是首选；按目标硬件配好 EP 优先级列表（如 `['CUDAExecutionProvider','CPUExecutionProvider']`）。只跑高端 NVIDIA GPU 求极致吞吐用 TensorRT（或把它作为 ORT 的 EP）；纯 LLM 端侧可对比 llama.cpp。端侧务必用 minimal build + 算子裁剪。
- **如果你要学它**：直奔 `include/onnxruntime/core/framework/execution_provider.h`（EP 抽象 + GetCapability）、`onnxruntime/core/framework/graph_partitioner.cc` + `fallback_cpu_capability.h`（优先级路由 + CPU 回退）、`include/onnxruntime/core/session/onnxruntime_c_api.h`（稳定 C API + ABI 纪律）、`include/onnxruntime/core/session/onnxruntime_ep_c_api.h`（Plugin EP C ABI）、`onnxruntime/core/mlas/lib/platform.cpp`（CPUID 派发）。这五处是架构精华。
- **如果你要 fork / 扩展它**：接新硬件优先走 Plugin EP（C ABI + 独立 wheel + 版本下限声明），无需改主仓；这是当下最有借鉴价值的扩展路径。

### 知识入口

| 资源 | 链接 |
|------|------|
| 官方文档 | https://onnxruntime.ai （含 /docs/execution-providers EP 架构、/blog） |
| DeepWiki | https://deepwiki.com/microsoft/onnxruntime（已收录，含 Session/EP/图优化/MLAS/多语言绑定/训练/构建 40+ 子章节） |
| 关联生态 | onnxruntime-genai（LLM 生成式推理）/ ONNX Runtime Web（浏览器内 WebGPU/WASM 推理） |
| 在线 Demo | ONNX Runtime Web 浏览器内推理示例（onnxruntime-inference-examples） |

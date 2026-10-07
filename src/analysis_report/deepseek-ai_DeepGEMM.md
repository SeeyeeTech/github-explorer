# GitHub 推荐：DeepSeek 开源周最大黑马 DeepGEMM：8.7K stars 的 FP8 内核库怎么用 300 行打爆 CUTLASS

> GitHub: https://github.com/deepseek-ai/DeepGEMM

## 一句话总结

DeepSeek 把自家训练/推理 DeepSeek-V3/R1 的 FP8 GEMM 原语开源出来——一个用「运行期 JIT + 极致形状特化 + Mega MoE 单 mega-kernel 融合」三板斧，把 dense FP8 GEMM 比自家调优 CUTLASS 快 1.2-2.7x、比 Triton 快 1.7x 的 CUDA kernel 库。

## 值得关注的理由

- **真实生产打磨的极致特化**：这不是论文驱动项目，是 DeepSeek-V3/R1 训练栈里跑通后开源出来的核心基础设施；H800 上实测 1550 TFLOPS FP8 性能，vLLM 已合入作为 dense block FP8 GEMM 后端（PR #13917）。
- **「Less is more」哲学的样本**：核心 SM90 FP8 实现只有 300-450 行；与 CUTLASS 几十万行模板代数堆叠形成鲜明对比，是学习 Hopper TMA + WGMMA + per-block FP8 scaling 的高质量教学样本。
- **Mega MoE 单 kernel 融合**是 2026 年的算法突破：把 EP dispatch + linear1 + SwiGLU + linear2 + EP combine 全部 fuse 到同一 mega-kernel，靠 grid_sync + NVLink barrier 跨 rank 同步——这种把分布式系统塞进单 kernel 的设计在公开仓库里几乎没有等价物。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/deepseek-ai/DeepGEMM |
| Star / Fork | 8,706 / 1,372 |
| Watcher | 71 |
| 代码行数 | 14,527（C++ Header 56.7% / Python 42.2% / Shell 0.7% / C++ 0.2% / CMake 0.2%） |
| 文件数量 | 96 |
| 项目年龄 | 19.3 个月（首次提交 2025-02-25） |
| 开发阶段 | 低维护（fix 主导，feature 期已过；v2.1.1 后收敛到 bugfix） |
| 开发模式 | 职业项目（周末 6.1%、深夜 4.1%，DeepSeek 团队节奏） |
| 贡献模式 | 核心少数 + 社区（58 人；Chenggang Zhao 33.3%、top2 ~51.5%、top5 ~80%） |
| 最新版本 | v2.1.1.post3（共 10 个 tag，含 4 个 nv_dev_* 内部快照） |
| 热度定位 | 大众热门（DeepSeek Open Source Week 旗舰项目之一） |
| 质量评级 | 代码优秀 / 文档优秀 / 测试充分 |
| License | MIT |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

DeepGEMM 由 DeepSeek 官方组织账号（107K followers、3 年账号）发布，核心 maintainer 是 Chenggang Zhao（LyricZhao，33.3% 提交占比），次核心是 Yuanhang Sun（16.7%）。项目与 FlashMLA（13K stars）、DeepEP（10K stars）、TileKernels、DeepSelect 同属 2025-02「Open Source Week」系列内核矩阵——同一作者群、同一时间窗、同样的开源策略。DeepGEMM 在 DeepSeek org 的 10 个最近活跃仓库中排第 8，投入权重属「核心基础设施」而非「明星项目」，更接近底层基础设施定位。

### 问题判断

作者看到的不是「缺少 FP8 GEMM」这种宽泛命题，而是三个具体的工程痛点：

1. **CUTLASS 模板代数过深**：为通用场景做了大量抽象，针对 DeepSeek-V3 这种特定 shape（FP8 + 128×128 block scaling + Hopper TMA + 2-CTA MMA）的极致性能反而要绕很多路；学习曲线陡，团队内难以普及。
2. **Triton 性能不够**：dense FP8 GEMM 比 DeepGEMM 慢 1.7x；JIT 路径与编译器紧耦合，难做底层指令（`tcgen05.mma`、`warpgroup_arrive`）级别的微优化。
3. **cuBLAS 是闭源黑盒**：无法在 SM90/SM100 上做形状特化与跨 kernel 融合（尤其是 Mega MoE 这种把 EP dispatch + linear1 + SwiGLU + linear2 + EP combine 融合到同一 mega-kernel 的工作）。

时机选择也很清晰：DeepSeek-V3 2024-12 发布后，FP8 + MoE 推理栈已经被自家模型充分验证，开源出来既能反哺社区又能巩固 DeepSeek 在 LLM infra 生态的话语权。

### 解法哲学

- **少即是多（less is more）**：每个架构只有屈指可数的几个 kernel 函数（FP8 dense / FP8 grouped 1d1d&1d2d / BF16 / FP4×FP4），核心 SM90 FP8 实现 ~300-450 行；明确**反对** CUTLASS 的模板代数堆叠。Heuristics 候选空间被强约束（block_m ∈ {16,32,64,128,256} × block_n 步长 16 × cluster ∈ {1,2}），最后只挑一个。
- **性能优先、Python API 极简**：函数签名做到 `fp8_gemm_nt(a, b, d, c=None, recipe=..., ...)` 一行调用；shape 不对的断言（DType/stride/contiguous）全部走 `DG_HOST_ASSERT` 把锅甩给上游；性能侧的脏活（layout 校验、SF 转换、tensormap 生成、JIT 编译、cache）全在 C++ 里。
- **运行期 JIT，安装期零 nvcc**：用 `deep_jit::Runtime<CUDA>` 在首次调用 shape 时按模板参数实例化并 nvcc，编译产物缓存到 `$HOME/.dj/`（默认）或 `DG_JIT_CACHE_DIR`。代价是首次调用延迟，收益是 wheel 体量小 + 任何架构参数变了不需要重发版。
- **故意不做的事**（与 CUTLASS / cuBLAS 划清边界）：
  - 不做 backward（issue #10 明确确认 forward-only）；
  - 不为消费级 Blackwell（sm_120，issue #236）做优化；
  - 不做 CuTe 模板泛型（只借用 `cute::TmaDescriptor` 等少数结构）；
  - 不做 masked MoE decode（这块 Triton 反而更强，DeepGEMM 选择放弃）。

### 战略意图

DeepGEMM 在 DeepSeek 更大图景里是**「Open Source Week」全家桶的核心基础设施**——跟 FlashMLA（attention）、DeepEP（EP 通信）、TileKernels（tile 抽象）、DeepSelect 一起构成完整的训练栈开源。每周一个 release，单独看 DeepGEMM 是 kernel 库，整体看是 DeepSeek 把自家训练栈开源。

开源策略是 **genuinely open，不是 open-core**：纯 MIT License，无 dual license、无 feature gate、无托管/SaaS/企业版意图；CUDA C++ 源码 + PTX 全开，issue 区里同步讨论 JIT 编译调试（`DG_JIT_DUMP_ASM`/`DG_PRINT_COMPILER_COMMAND`/`DG_JIT_CHECK_NO_SPILLS` 等环境变量）。跨厂商外延已显形：NPU 路径已经 fork 出 DeepGEMM-Ascend；`third-party/tilelang_ops` 子模块暗示向 TileLang DSL 平铺的可能性。

> 项目内部有 `docs/scaling-factor-format.md`（472 行），把 SF 契约写得跟规范文档一样细致（6 节 + 内部细节），是少见的对竞品协议也很坦诚的工程文档。

## 核心价值提炼

### 创新之处

1. **Mega MoE 单 mega-kernel 融合**（新颖度 5/5）
   把 EP dispatch + linear1 + SwiGLU + linear2 + EP combine 全部 fuse 到同一 mega-kernel，靠 `grid_sync<kNumSMs>` + `nvlink_barrier` 跨 SM/跨 rank 同步。`sm100_fp8_fp4_mega_moe.cuh`（1528 行）一次性编排 dispatch warps + MMA warps + epilogue warps；dispatch 用 `ptx::atomic_add_sys` 写 `expert_token_count`，MMA warps 直接消费 ring buffer 里的对端 token。kernel 体积巨大（1528 行），寄存器/共享内存预算极其紧张（`SharedStorage` 用 union 复用 l1/l2 smem_d，TMEM 列通过 `kNumOverlappedTmemCols` 重叠），但通信-计算 overlap 的潜力远大于拆分方案。

2. **DeepJIT 运行期编译 + shape-keyed cache**（新颖度 3/5、实用性 5/5、可迁移性 5/5）
   不发 wheel 包含所有 shape 特化 kernel，而是用 `std::format(R"(...)", ...)` 在 host 拼出具体 shape 的 `.cu` 源码，调 nvcc 编译到 cubin，按 `(desc, config)` 的 tag 缓存到 `$HOME/.dj/`。首次调用延迟（秒级），换来 wheel 体量小 + shape 特化自由度高 + 用户可在 `DG_JIT_DUMP_PTX=1` 下直接看生成出来的 PTX。`deep_jit::Runtime<CUDA>` 已经独立成仓库，可被其他项目复用。

3. **Heuristics analytical model（离线算 cycles 不实测）**（新颖度 4/5）
   `SM90ArchSpec::get_layout_info` 用 L1/L2 bandwidth 模型估算 `num_cycles`，遍历 ~几十个 layout 候选挑最小。整个过程是**纯函数式**，不实际编译/运行 kernel。牺牲了一点「实测最优」的精度，换来**首次调用零额外延迟**；layout 候选本身已经过强约束（swizzle ≥ 64、num_stages ≥ 3/4），不会选错。

4. **SF 双 path 缓存设计**（新颖度 3/5、实用性 5/5、可迁移性 5/5）
   同一 API 既能吃未 transform 的 float32（自动走 transform kernel 路径），也能吃预 transform 的 int32（validate-only 路径）。让 weight SF 转换一次缓存永久复用：`transform_sf_pair_into_required_layout(...)` 在调用 kernel 前根据架构 + dtype 决定走哪条路；SF 布局契约写在 `docs/scaling-factor-format.md`，每个字段（dtype/shape/stride/gran_m/gran_k/ALIGN_MN）都有 host-side assert 兜底。

5. **Per-block scaling 通过 CUDA-core promotion（两段累加）**（新颖度 3/5）
   `sm90_fp8_gemm_1d1d.cuh:317-325` 在 `warpgroup_wait<0>()` 之后用 `scale_a_x * scale_b_y * accum` 做 FP8 缩放，绕开 NVCC 12.9 的 FFMA interleaving post-opt（README 提到这条）。Hopper WGMMA 支持 per-32 block-scaling 输出（sm90 `mma::sm90::FP8MMASelector` 选了不带内置 scaling 的 MMA），需要把 WGMMA 输出当 FP32 累加后再乘 SF；为 `final_accum[i*4+k]` 提供 4 个不同的 `(scale_a, scale_b)` 组合覆盖 WGMMA 的内部 2×2 块（lane 维度）。

6. **UE8M0 int32 packing**（新颖度 2/5、实用性 5/5）
   `docs/scaling-factor-format.md` 第 7.1 节定义「4 个 UE8M0 8-bit 指数 pack 进一个 int32」的小端布局；SM100 直接走 validate-only path，SM90 必须 float32 → kernel transform。这把 OCP MX spec 的实现细节做到极致带宽优化。

7. **Locality domain 感知调度**（新颖度 4/5）
   `csrc/runtime/runtime.hpp:36-38` + `locality_domain.py` 探测每个 SM 的 NVSwitch locality domain，把 cluster 分配尽量放在同一域以减少跨域 NCCL/NVLink。在 NVL72/Blackwell GB200 NVLink domain 拓扑敏感的 kernel 里尤为重要。

### 可复用的模式与技巧

1. **JIT-by-string-template 模式**：用 `std::format(R"(...)", ...)` 拼出含 shape 参数的 `.cu` 源码 → nvcc → cubin cache。适用于任何想要「零安装期编译 + shape 特化」的 GPU kernel 库。
2. **Heuristics-analytical-model 模式**：不实测，纯用 bandwidth 模型算 `num_cycles` 排序候选 layout。适用于首次调用延迟敏感（JIT 编译已经吃了一次，重新跑所有候选做 autotune 不可接受）的场景。
3. **Dual-path 缓存模式**：同一 API 既吃未 transform 输入（自动走 transform kernel），也吃预 transform 输入（validate-only）。适用于任何「预处理开销大、权重侧可缓存」的量化算子。
4. **Single mega-kernel 多角色 warp 模式**：dispatch warps / non-epilogue MMA warps / epilogue warps 三段不同寄存器预算（`kNumDispatchRegisters=48/96`、`kNumNonEpilogueRegisters=40/72`、`kNumEpilogueRegisters=208/168`），通过 `cutlass::arch::warpgroup_reg_alloc` 在同一 kernel 内切换角色。
5. **Layout validation + auto-transform 模式**：`check_sf_layout`（`utils/layout.hpp:101`）用 `DG_HOST_ASSERT` 把 SF 契约做成机器可读、可执行、可文档化（与 `docs/scaling-factor-format.md` 1:1 对应）。适用于任何有复杂数据布局契约的算子。
6. **`std::format` + `DG_HOST_ASSERT` 全文**：把 Python 风格的 f-string 模板塞 C++，把 Python 的「错就 raise」哲学塞 C++ assertion。适用于任何想要「Python 友好 + C++ 性能」边界的库。

### 关键设计决策

1. **决策**：运行期 JIT 编译（`deep_jit::Runtime<CUDA>`），按 `(GemmDesc, GemmConfig)` 的 hash 缓存到磁盘
   - **问题**：wheel 不应该包含所有 shape 特化；用户运行环境多变；编译期模板特化爆炸
   - **方案**：`csrc/jit_kernels/impls/sm90_fp8_gemm_1d1d.hpp:32` 用 `std::format(R"(...)", ...)` 把 shape 参数填进 `.cu` 源码
   - **Trade-off**：首次调用延迟（秒级），换来 wheel 体量小 + shape 特化自由度高
   - **可迁移性**：高

2. **决策**：双层 kernel 抽象（`sm90_*_1d1d` / `sm90_*_1d2d` / `sm100_*_1d1d`），不引入 CuTe 的高阶 layout DSL
   - **问题**：同一架构的 FP8 GEMM 在不同 N-block 上既要用 1 个 stage 装 1 个 SF tile，也要用 2 个 stage 装 2 个 SF tile
   - **方案**：1d1d = 一个 stage 一个 SF tile（适合 N 较小），1d2d = 两个 stage 两个 SF tile（适合 N 较大）；按 `desc.kernel_type` 静态分发
   - **Trade-off**：牺牲代码模板的统一性，换取每个 kernel 不到 500 行的可读性
   - **可迁移性**：中

3. **决策**：Mega MoE 用单个 mega-kernel 融合，靠 grid_sync + NVLink barrier 跨 rank 同步
   - **问题**：MoE EP 通信与 GEMM 拆开做时，NVLink round-trip 与 tensor core 计算串行
   - **方案**：`sm100_fp8_fp4_mega_moe.cuh`（1528 行）一次性编排 dispatch warps + MMA warps + epilogue warps
   - **Trade-off**：kernel 体积巨大，寄存器/共享内存预算极其紧张
   - **可迁移性**：低（几乎不可移植）

4. **决策**：SF 格式按架构分流——SM90 用 FP32 SFA/SFB，SM100 用 packed UE8M0 int32
   - **问题**：Hopper 缺少 MX 指令，必须 CUDA-core promotion；Blackwell 有 TCGEN05/UMMA 内建 MX scaling
   - **方案**：`apis/layout.hpp:88-95` 的 dispatch 表按 arch × dtype 分发
   - **Trade-off**：用户必须知道自己在哪台机器上 + 喂对 SF 格式；换卡要重 transform
   - **可迁移性**：中

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | DeepGEMM | CUTLASS 3.x | OpenAI Triton | FlashInfer | sgl-kernel |
|------|---------|------------|--------------|------------|-----------|
| dense FP8 GEMM 性能 | 基线（最快） | 比 DeepGEMM 慢 1.2-2.7x | 比 DeepGEMM 慢 1.7x | 弱于 DeepGEMM | 弱于 DeepGEMM |
| masked MoE decode | 弱（输给 Triton） | 一般 | 强（Triton 胜出） | 中等 | 中等 |
| 代码量（核心实现） | ~300-450 行 | 几十万行模板 | Python DSL | 中等 | 薄 |
| Backward 支持 | ❌ 明确不做 | ✅ 完整 | ✅ 通用 | 部分 | 部分 |
| 安装期 nvcc | ❌（运行期 JIT） | ✅ | ❌ | ✅ | ❌ |
| 跨架构支持 | SM90/SM100 only | 几乎全 NVIDIA | 全 GPU | 主流 NVIDIA | 主流 NVIDIA |
| Mega MoE 单 kernel | ✅（独有） | ❌ | ❌ | ❌ | ❌ |
| 教学价值 | 高（less is more） | 低（模板代数深） | 高（Python DSL） | 中等 | 中等 |

### 差异化护城河

- **技术护城河**：Mega MoE 单 mega-kernel 融合 + DeepJIT 运行期 JIT + SF 双 path 缓存这三点组合，竞品短期内难以复制。
- **生态护城河**：DeepSeek-V3/R1 训练栈真实使用带来的实战打磨（H800 1550 TFLOPS、vLLM benchmark 1.06x vs vLLM CUTLASS、1.71x vs Triton）。
- **信任护城河**：DeepSeek 开源矩阵的官方背书，与 FlashMLA/DeepEP/TileKernels 同源矩阵式开源。
- **教学护城河**：核心 kernel 仅 ~300-450 行，是学习 Hopper TMA + WGMMA + per-block FP8 scaling 的高质量样本（README 自述「clean and accessible resource for learning」）。

### 竞争风险

- **来自 Triton**：masked MoE decode 上 Triton 仍领先（Novita AI 测试），DeepGEMM 在 decode 场景的护城河不深；Triton 持续迭代可能让 dense FP8 GEMM 差距收窄。
- **来自 CUTLASS + 编译器**：NVCC 持续优化（如 FFMA interleaving 自动开启）可能让「CUDA-core promotion」路径被自动追上，消减部分性能优势。
- **来自 NCCL/DeepEP 的 NVLink 抽象**：NVLink + tensor core overlap 的算法不一定能跨代硬件复用，Blackwell 之后需要重新设计。
- **来自 DeepSeek 自身战略**：如果 DeepSeek 重心转向 Ascend / 其他 NPU，CUDA 专属的 DeepGEMM 可能进入低维护阶段（虽然项目 fork 出 Ascend 版本做对冲）。

### 生态定位

在整个技术生态中扮演**「极致优化 kernel 层」**角色，介于「通用 BLAS（CUTLASS/cuBLAS）」与「用户框架（vLLM/SGLang）」之间。目标是把自家训练栈里最热的几个 GEMM 路径开源出来。下游集成已现端倪：
- **vLLM** — 已合入 DeepGEMM 作为 FP8 dense block GEMM 内核（PR #13917）
- **SGLang / sgl-kernel** — Novita AI 在生产推理中实测
- **FlashInfer / vLLM** — 作为可选后端
- **DeepGEMM-Ascend** — 华为昇腾 NPU 移植版（同 push 周期，反映「硬件抽象分层」战略）

> 无明显竞品属于纯细分市场：DeepGEMM 在 FP8 GEMM 专项上是事实标准，但整个 GPU kernel 库市场仍是红海（CUDA/Triton/CUTLASS/FlashInfer/AscendC 多方角力）。DeepGEMM 的真正壁垒是「专为 DeepSeek-V3 shape 极致优化 + 教学友好代码 + Mega MoE 单 kernel 融合」三件套。

## 套利机会分析

- **信息差**：DeepGEMM 热度高但**作为教学样本的二次价值未被充分挖掘**。核心 SM90 FP8 实现仅 300-450 行，比 CUTLASS 模板代数友好得多；适合做「Hopper TMA + WGMMA + per-block FP8 scaling」入门教学。当前中文社区已有 henrytheflame 等独立 walkthrough，但系统性教学资源稀缺。
- **技术借鉴**：
  - **DeepJIT 运行期编译模式**可直接用于任何 shape 特化的 GPU kernel 库（`deep_jit` 已独立成仓库）。
  - **Heuristics analytical model** 适合「首次调用延迟敏感」的 JIT 库，避免 autotune 二次编译。
  - **Dual-path SF 缓存设计**适用于任何「预处理开销大、权重侧可缓存」的量化算子。
  - **Single mega-kernel 多角色 warp** 模式是「通信+计算+收尾」三段流水工作的通用解法。
- **生态位**：填补了「CUDA 极致特化 kernel 层」的开源空白——CUTLASS 太通用、Triton 性能不够、cuBLAS 是闭源黑盒；DeepGEMM 在这三者之间找到了「小而精、专而深」的位置。
- **趋势判断**：FP8/FP4 量化已成 LLM 推理标配（DeepSeek-V3/R1、Llama 4、Qwen 等均部署）；Hopper → Blackwell 代际迁移带来 SF 格式变化（FP32 → UE8M0 packed），DeepGEMM 已经做好架构分层；项目处于「扩张期已过、稳定维护期已至」阶段，但 Mega MoE 单 kernel 融合仍在持续进化，2026 年仍有 13 次 commit 在 v2/v3/MoE mega kernel 发布。

## 风险与不足

- **架构覆盖有限**：仅 SM90/SM100 官方支持；社区大量请求 sm_120（RTX 5090、Blackwell 6000 Pro）支持，issue #236 显示 DeepSeek 暂时**故意不为消费级 Blackwell 优化**（可能是 HBM/带宽差异不值得投入）。
- **Backward 缺失**：明确 forward-only（issue #10），不适合训练反向；与 FlashAttention （training+inference） 形成战略对比。
- **v2 重构存在回归**：issue #160 显示 v2 引入 SM100 + DeepJIT 后，在某些 Hopper shape 上反而比 v1 慢；抽象层升级并非所有路径都获益。
- **padding 浪费**：issue #98 显示 m_grouped_gemm 要求每个 expert 128 元素 padding 是为了 TMA 对齐的硬件最优，但浪费了计算；Mega MoE 内核的出现正是为了绕开这个 padding 浪费。
- **依赖 CUTLASS 子模块**：虽然不引入 CUTLASS 模板代数，但仍依赖 `third-party/cutlass` 子模块（`cute::TmaDescriptor` 等）；如果 CUTLASS 大版本变动，可能需要适配。
- **C++ 标准较新**：使用 `std::format`（C++20）等较新特性，对编译器版本有要求；setup.py 自动检测 wheel 是否可下载，缺失则本地编译。
- **文档缺 linter/formatter 配置**：仓库根未提交 `.clang-format` / `.clang-tidy`；C++ 风格靠 contributor 自觉。
- **无独立 CHANGELOG 文件**：通过 README News 区段 + commit 历史 + 引用 PR 号追溯。

## 行动建议

- **如果你要用它**：
  - 适用场景：Hopper （H100/H800） 或 Blackwell （B200） 上跑 FP8 dense / MoE GEMM 的推理路径；Mega MoE 路径适合 NVLink 互联的多机多卡 MoE 推理（如 NVL72 GB200）。
  - 不适用：训练反向、消费级 Blackwell (sm_120)、A100 / 老架构（DeepGEMM SM90/SM100 only）。
  - 与 vLLM / SGLang 集成：vLLM PR #13917 已合入，可作为 dense block FP8 GEMM 后端直接使用。

- **如果你要学它**：
  - **重点关注文件**：
    - `deep_gemm/jit_kernels/gemm.py`（40 次修改）— Python 侧 FP8 GEMM kernel 模板与参数装配入口
    - `deep_gemm/include/deep_gemm/fp8_gemm.cuh`（35 次修改）— FP8 GEMM 主 kernel 头文件，真正的核心实现
    - `csrc/jit_kernels/impls/sm90_fp8_gemm_1d1d.hpp` — 运行期 JIT 编译 + shape-keyed cache 的范例
    - `deep_gemm/include/deep_gemm/impls/sm100_fp8_fp4_mega_moe.cuh`（1528 行）— Mega MoE 单 mega-kernel 融合的实现
    - `docs/scaling-factor-format.md`（472 行）— SF 契约规范文档
    - `deep_gemm/jit/compiler.py`（14 次修改）— JIT 编译运行时
  - **推荐学习路径**：先读 README + `docs/scaling-factor-format.md` 建立 SF 契约心智模型；再读 `sm90_fp8_gemm_1d1d.cuh` 学习 Hopper TMA + WGMMA；最后读 `sm100_fp8_fp4_mega_moe.cuh` 学习单 kernel 融合通信+计算。

- **如果你要 fork 它**：
  - 可以改进的方向：
    - **sm_120 消费级 Blackwell 支持**（issue #236 大量社区请求）
    - **Backward 支持**（issue #10 社区讨论热烈，但 DeepSeek 明确不打算）
    - **A100 / 老架构 fallback**（DeepGEMM SM90/SM100 only，旧卡用户无替代）
    - **masked MoE decode 优化**（这是 DeepGEMM 输给 Triton 的薄弱环节）
    - **linter / formatter 配置**（仓库根缺 `.clang-format`）
    - **独立 CHANGELOG 文件**（目前依赖 README News 区段）

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录 |
| Zread.ai | 未收录 |
| 关联论文 | 无独立 arXiv 论文（DeepSeek-V3 Tech Report arXiv:2412.19437 引用其作为 FP8 GEMM 实现；同名旧工作 arXiv:2304.09049 是不同的 CPU 2-bit 量化项目，勿混淆） |
| 在线 Demo | 无（kernel 库无可玩 demo；benchmark 跑分见 README 表格） |
| 独立 walkthrough | [DeepGEMM Walkthrough \| henrytheflame.com](https://henrytheflame.com/blog/deepseek-deepgemm) — 逐文件解读 JIT pipeline |
| 基准测试 | [vLLM Block FP8 Dense GEMM 基准测试](https://blog.gitcode.com/d92ac15eca238dd700813bb3a80f90b4.html) — DeepGEMM 1.06x vs vLLM CUTLASS，1.71x vs Triton |
| 独立评测 | [Novita AI: DeepGEMM Tested — Can It Replace SGLang?](https://blogs.novita.ai/deepgemm/) — Triton 在 masked MoE decode 场景胜出 |
| DeepSeek 开源周报道 | [DeepSeek 开源周 Day3 报道（CSDN）](https://devpress.csdn.net/v1/article/detail/145870571) — 国内媒体解读，强调「300 行代码重构 FP8 矩阵运算」 |

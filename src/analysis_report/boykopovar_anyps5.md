# GitHub推荐：2 个月 11.6K stars：一个人把 22 万行 C++ 做成 PS5 → PC 的「Wine」

> GitHub: https://github.com/boykopovar/anyps5

## 一句话总结

**AnyPS5** 是一个把 Sony PS5 ELF 程序**重链接**为 Linux/Windows 原生可执行文件的工具——不上模拟器、不开独立运行时，只靠「ELF/PE 重链接 + clean-room prx 系统库 + RDNA → SPIR-V 着色器重编译」三件套，让 PS5 游戏在 PC 上以原生性能运行。

## 值得关注的理由

1. **「Wine for PS5」独占叙事**：主机模拟器（RPCS3/Xenia/Ryujinx）都是 JIT/异构翻译，PS5 与 PC 硬件同源（Zen 2 + RDNA2）根本不需要这条路。Wine 在 Windows→Linux 上验证过的"重链接 + 系统库替换"哲学，被移植到 PS5 上是首创——**这条赛道目前没有任何直接竞争者**。
2. **2 个月 22 万行 C++ / 11.6K stars / 95 贡献者 / 294 排队 PR**：所有"职业开源"的指标都拉满，且仍在上升曲线（10 月半月已达 1660 commit，9 月 863）。这不是 fork 凑数，是真在打实质工程。
3. **着色器重编译（RDNA → SPIR-V）是真正的护城河**：占 20% commit 的 `core/shader/` 子系统，含完整的 decode → CFG → 域 IR → 多 pass 优化 → SPIR-V 输出流水线，并可选 spirv-val 校验。shadPS5 走模拟不重编——这是任何模拟路线做不到的能力。

## 项目展示

![AnyPS5 进度地图](https://boykopovar.github.io/AnyPS5/progress.svg)

> 这是项目的核心可视化——各系统库 / shader 指令 / 平台支持的实时完成度仪表盘，技术报告必引。比任何截图都更有说服力：覆盖率的诚实本身就是对社区的承诺。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/boykopovar/anyps5 |
| Star / Fork | 11,591 / 885 |
| 代码行数 | 229,820 行（C++ 96.4% / CMake 1.8% / Python 1.3% / GLSL 0.1%） |
| 项目年龄 | 2.1 个月（首 commit 2026-08-03） |
| 开发阶段 | 密集开发（月环比 +92%，10 月半月 1660 commit） |
| 贡献模式 | 核心少数 + 社区（95 人，Top1 占 29.8%，Top10 占大头） |
| 热度定位 | 大众热门（11.6K stars 仅 2 个月龄，仍在指数增长） |
| 质量评级 | 代码优秀 / 文档优秀 / 测试充分 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

boykopovar，Belarus，账号 2.4 年。Bio 精准对应项目域——*Reverse Engineering · Protocol Analysis · Software Development · C++, C#, Python*。**作者本人 fork 过 KytyPS5**（PS5 SDK 的开源参考实现），这是理解 AnyPS5 出处的关键钥匙：他本来就在 PS5 逆向圈里，看到 Kyty「公开了 SDK 但游戏 ELF 没法直接跑」的空白，就推导出「重链接 + clean-room prx」的替代思路。

### 问题判断

PS5 与 PC 硬件**完全同源**——Zen 2 CPU + x86-64 指令集 + RDNA2 GPU。传统主机模拟器走的是 JIT / 二进制翻译，对这一代主机**没有意义**。同时，Sony 100+ 个 prx 系统库（libkernel / libSceAgcDriver / libScePad / libc / NpTrophy2 等）没有任何公开实现——**Wine 解决了 Windows→Linux 的路径，但 PS5→PC 是空白**。

### 解法哲学

- **「小而硬」**：每个函数要么做它该做的，要么 `throw`，**不写静默 stub 兜底**。`docs/dev/TechnicalDebt.md` 显式列出唯一 5 处允许 silent stub 的位置（dialog 类、HMD），其余未实现即抛 NotImplemented。代码实测 `core/libs/prx/` 共 1062 处 throw、`core/shader/` 共 518 处。
- **「功能正确性 > 兼容广度」**：CONTRIBUTING.md 明示：*Implement the general behaviour of a function, not what one title happens to need*——不为单个游戏打补丁。
- **GPLv2-only（不是 MIT/Apache 也不是 GPLv3）**：强 copyleft 把「改进必须回开源」绑定住，**是对抗大型商业公司闭源分叉的标准武器**，也是作者「genuinely open」立场的法律表态。
- **明确选择不做什么**：不重写用户态中间件（Cohtml/FMOD/GOG Galaxy 等都跳给 relinker 直接链游戏自带版本）、不为单游戏打补丁、不为不支持的 shader 指令生成 stub。

### 战略意图

这是作者生涯代表作（11,591★ 远超其他所有 repo 总和），**「核心产品」而非「基础设施」**。GPLv2 选择暗示作者不打算让任何大厂把它包装成闭源兼容层商业发行。**DISCLAIMER 把使用范围限制在 interoperability/research/preservation，明确不捆绑固件/密钥/版权库——这是法律护城河而非商业策略**。

## 核心价值提炼

### 创新之处

1. **PS5 RDNA shader 全栈重编译为 SPIR-V**（新颖度 4/5 / 实用性 5/5 / 可迁移性 4/5）
   - 自研 RDNA 解码器 → CFG 结构化 → 域 IR → 多 pass 优化（SSA / 常量折叠 / 死码 / ReadLane / MaskedSelect / SRT 行走 / 资源追踪 / 绑定分配）→ SPIR-V 输出 + 可选 spirv-tools 验证。disk cache 复用编译产物。**公开领域几乎没有 RDNA2→SPIR-V 全栈实现**，shadPS5 走模拟不重编。

2. **NID 反查靠 hash 派生**（新颖度 3/5 / 实用性 5/5 / 可迁移性 5/5）
   - `ComputeNid(name, library)` = SHA1(name + 16 字节 suffix) → 8 字节大端反转 → 11 字符 base64。无网络依赖、可重放。`nid_patcher` 构建后用同一函数把 clean-room 实现的 C symbol 改名回 PS5 原 NID，让动态加载器无感绑定——**是整个「无模拟」方案的粘合剂**。

3. **AMD-only x86 指令就地替换 codegen**（新颖度 3/5 / 实用性 5/5 / 可迁移性 4/5）
   - SSE4A / SHA / CLZERO / VRCPPS / VRSQRTPS 在 Intel 主机上跑不了。`Amd64OnlyConverter` 走"InstructionScanner → Decoder → Matcher → OperandBuilder → Rewriter"流水线做原地替换或 stub。

4. **fail-fast + TechnicalDebt.md 显性化治理**（新颖度 3/5 / 实用性 4/5 / 可迁移性 5/5）
   - 全栈 throw + 一份 304 行的单一债务登记簿 + `tools/check_conventions.py` 强制注释必须同时改 TechnicalDebt.md——把「加注释」和「登记技术债」绑成同一个 PR 工作单元。**任何长寿命 C++ 项目都能复制这套治理模式**。

### 可复用的模式与技巧

1. **Per-library CMake sub-project + 统一 Export.cpp 接口**：`core/libs/prx/<lib>/` 模板可复制到任何"按目标 OS 系统库镜像"的兼容层项目——增量构建 / 单库替换 / 单测裁剪三件套。
2. **Hash-derived symbol rename pipeline**：算 hash → 重写 ELF/PE 导出表，可复用于任何私有 ABI 重绑定场景。
3. **Compiler-style shader 重编译分层**：decode → CFG → IR → optimize → backend，每个 stage 独立、可单测、可换实现——可推广到 PS4/PS5 Pro/下一代主机 shader 重编。
4. **多后端产物抽象用 `I*` 接口 + 工厂**：`MakePatcher` / `MakeNullSyscallScanner` / `MakeStrictUnusedNidFilter` 这种命名约定 + DI 模式对单元测试友好。

### 关键设计决策

1. **把 PS5 ELF 转为宿主 ELF/PE 而非解释执行**
   - 问题：PS5 硬件与 PC 同源，没必要走翻译/模拟。
   - 方案：`relinker` 用一次 `--to-intel` 把 AMD-only 指令原地替换或 stub，再用 `LinuxElfPatcher` / `WindowsPePatcher` 重建 SysV 动态节，OS loader 直接绑定导出。
   - Trade-off：失去"运行任意 PS5 ELF"的普适性，换来原生性能（无 JIT 开销）和更简单的部署（产物就是普通可执行文件）。

2. **PRX 兼容层用按库独立 CMake target 组织**
   - 问题：100+ 个 PS5 系统库的实现需要并行演进、单库替换、单测可裁剪。
   - 方案：`core/libs/prx/<libSceXxx>/` 各自一份 `CMakeLists.txt` + `Export.cpp` + `include/` + `src/`；`configure_windows_unwind()` 在 MinGW 下用 `objcopy --rename-section .eh_frame=.ehfram` 让 MSVC 加载器识别 MinGW 产物。
   - Trade-off：维护 100+ 个独立 target 的人力成本 vs 一库一切的可调试性/增量构建收益。

3. **着色器用 RDNA → 域中间 IR → SPIR-V 三段式重编译器**
   - 问题：PS5 RDNA shader 指令集对 Vulkan/SPIR-V 没有 1:1 映射。
   - 方案：RDNA 指令字面解码 → CFG 结构化 → RDNA → IR → 多 pass 优化 → SPIR-V 输出。`ShaderDiskCache` 用 hash 做 disk+memo 双缓存，`ANYPS5_ENABLE_SPIRV_TOOLS` 可选开启 spirv-val 验证。
   - Trade-off：多一道 IR 层的工程成本 vs 优化 pass 复用、跨指令族迁移能力、未来加 RDNA3/4 的扩展空间。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | AnyPS5 | shadPS5 | Wine / Proton | KytyPS5 |
|------|--------|---------|---------------|---------|
| **路径** | 重链接 + clean-room | 模拟/JIT | 重链接 + clean-room | PS5 SDK 实现 |
| **目标方向** | PS5 → Linux/Win | PS5 模拟 | Windows → Linux | 在 PC 上开发 PS5 程序 |
| **运行时** | 无（产物即原生可执行） | 独立 runtime | 无 | 编译工具链 |
| **CPU 端开销** | 0（JIT 无） | 高（JIT/解释） | 0 | — |
| **成熟度** | v0.1.x，仅 2D 独立游戏 | 更早期 | 30 年+ 积累 | SDK 风格 |
| **License** | GPLv2-only | — | LGPL | — |
| **社区规模** | 11.6K★ / 95 人 | 更早期 | 10× 数量级 | 小众 |

### 差异化护城河

- **技术护城河**：RDNA→SPIR-V 全栈 + NID hash 派生 + AMD-only 指令替换三层互锁，**任何模拟路线都做不到重编**。
- **生态护城河**：PS5→PC「native port」路径目前**无明显对手**。Wine/Proton 是哲学祖先但目标平台相反。
- **信任护城河**：GPLv2-only 阻止大厂闭源 fork；DISCLAIMER 把使用范围限制在 interoperability/research/preservation，是法律护城河。

### 竞争风险

- **最直接风险是 shadPS5**——一旦他们打通 shader 重编（而不是模拟），将吃掉同一批用户。
- **Proton/Wine 路径上"PS5→PC"** 若由 Valve 商业投入会快速碾压小团队。
- **Sony 法务**是长期外部风险（虽然 DISCLAIMER 已做对冲，参考 Yuzu 案）。

### 生态定位

**数字保护 / 兼容性研究 / 跨平台移植基础设施**——与模拟器互补，与 Wine 哲学同源。任何"硬件同源 + ABI 不同"的跨平台移植场景都可以借鉴这套模式（Switch 后续 NVN→Vulkan 也用同样思路）。

## 套利机会分析

- **信息差**：PS5→PC 的 native port 路径目前**几乎无直接竞争**，项目独占叙事才带来这种传播力（11.6K★ / 2 个月）。窗口期有限——shadPS5 或 Valve 切入就会快速变化。
- **技术借鉴**：
  - **Hash-derived symbol rename pipeline**（NID / ordinal 派生）可复用于任何私有 ABI 重绑定场景
  - **fail-fast + 单文件 TechnicalDebt + 强制注释规则**是任何长寿命 C++ 项目都能复制的治理模式
  - **Per-library CMake sub-project 模板**可迁移到任何"按目标 OS 系统库镜像"的兼容层项目
  - **Compiler-style shader 重编译分层**可推广到 PS4/PS5 Pro/下一代主机 shader 重编
- **生态位**：填补了「硬件同源时代的主机→PC native port」这个空白，与模拟器互补。
- **趋势判断**：项目仍在加速（10 月半月 1660 commit > 9 月全月 863），且首发 2 个月——**早期窗口，尚未饱和**。

## 风险与不足

- **仅 Linux + Windows**；macOS 在 #1 仍是最大需求（15 评论）但暂未承诺。
- **Windows 强绑定 MinGW 15.2.0**（winlibs-gcc15），版本敏感。
- **100+ 个 PRX 库中多数仍为 stub**，实际兼容游戏极少——仅 Dreaming Sarah 等 2D 独立游戏可稳定运行；3A 商业游戏任重道远。
- **Shader 重编仅 RDNA2**，PS5 Pro 的 RDNA2.1 / PS5 Slim 变体未明确路线。
- **Hardware oracle 是 PR 验收门槛**，但本身依赖贡献者持有 AMD GPU + PS5，门槛高。
- **注释率仅 3.0%**，新人 onboarding 成本偏高。
- **无 CHANGELOG.md**，靠 git log + Conventional Commits 自行推断。
- **License 兼容性对反 GPLv3**——意味着任何想用 GPLv3 代码 fork 的方案都被排除。

## 行动建议

### 如果你要用它

- **用于 PS5 游戏兼容/分析/保护**：直接参考 README + `docs/user/COMPATIBILITY.md`（注意目前仅 2D 独立游戏可稳定运行）。
- **不要期待跑 3A**：兼容性仍在 v0.1.x，与 RPCS3 / Proton 成熟度差几个数量级。
- **macOS 用户**：等 #1 解决，可能需要数月。

### 如果你要学它

**重点关注以下文件/模块**：

1. **架构骨架**：`core/main.cpp` 入口 + `core/relinker/`（离线 CLI 三件套：codegen / domain / io）
2. **创新核心**：`core/shader/recompiler/`（RDNA→SPIR-V 完整流水线）+ `core/libs/prx/`（100+ clean-room 系统库）
3. **设计哲学**：`docs/dev/TechnicalDebt.md`（304 行单一债务登记）+ `tools/check_conventions.py`（强制注释规则）
4. **关键抽象**：`core/relinker/elfpatcher/include/.../IElfPatcher.hpp`（Linux/Windows 后端抽象）+ `ComputeNid`（NID hash 派生）
5. **测试样板**：`core/libs/prx/libSceAgcDriver/tests/Graphics.cpp`（73 次修改的高频实测试）

### 如果你要 fork 它

可改进的方向：
- **macOS 后端**：加 `MacMachOPatcher`（`IElfPatcher` 第三个实现），Mach-O 重链接（参考 Wine 的 mach-o support）
- **PS5 Pro / RDNA3**：扩 `core/shader/recompiler/RdnaDecoder/` 到 RDNA2.1 / RDNA3 指令集
- **Telemetry/diagnostics**：fail-fast 抛错时附带 issue 自动生成链接，加速社区反馈闭环
- **Compatibility 数据库**：把 `COMPATIBILITY.md` 升级为可查询的 JSON / 站点，方便研究者快速判断"X 游戏能不能跑"
- **GPU 厂商扩展**：当前 `Amd64OnlyConverter` 仅 AMD→Intel 替换，可加 ARM64 / RISC-V 后端（虽然 PS5 永远不需要，但模式本身可重用）

---

## 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录（探测被限流） |
| Zread.ai | 未收录（探测被限流） |
| 关联论文 | 无 |
| 在线 Demo | 无（项目主页是 Discord: <https://discord.gg/BHFztBPUe>） |
| 进度可视化 | <https://boykopovar.github.io/AnyPS5/progress.svg>（核心展示素材） |
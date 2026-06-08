# 用 Rust 写的 Python 解释器，专为浏览器和嵌入

> GitHub: https://github.com/RustPython/RustPython

## 一句话总结

RustPython 是一个用 Rust 从零实现的 Python 3 解释器（目标兼容 CPython ≥ 3.14）——它不是要在生产上取代 CPython，而是填补「CPython 不适合的场景」：把 Python 编译进 WebAssembly 在浏览器里跑、内嵌进 Rust 应用（无 C 依赖、内存安全）、做沙箱化执行与教育。它由 563 人的分散社区跑了 8 年，至今仍是 v0.x——因为完整复刻 Python 本就是场马拉松。

## 值得关注的理由

- **「纯 Rust + WASM 原生 + 可嵌入」的近乎独占卡位**：它自比「Jython 之于 JVM、IronPython 之于 .NET → RustPython 之于 Rust 生态」。在「纯 Rust 实现 + 可嵌入 Rust + WASM 原生」这个交集里几乎独占，是想在浏览器跑 Python 或在 Rust 程序里内嵌 Python 脚本的现成方案。
- **强血缘背书**：现象级的 Rust 写的 Python linter **Ruff 早期的解析器就基于 RustPython 的 parser**（RustPython org 至今保留 ruff fork）——这是它在 Rust 生态最有分量的工程背书；GreptimeDB 也用它做嵌入式脚本。
- **「兼容性测试驱动开发」的教科书范式**：通过移植 CPython 官方测试套件、刷「通过率」来度量兼容性进展——test commit 占 19%（高于 feature/fix）。这是任何「重新实现某语言/标准」项目的正道。

## 项目展示

![RustPython logo](https://raw.githubusercontent.com/RustPython/RustPython/main/logo.png)

**眼见为实**：[在线 WebAssembly Demo](https://rustpython.github.io/demo/)（浏览器里直接跑 Python REPL）。会议分享：[FOSDEM 2019](https://www.youtube.com/watch?v=nJDY9ASuiLc) / [EuroPython 2018](https://www.youtube.com/watch?v=YMmio0JHy_Y)。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/RustPython/RustPython |
| Star / Fork | 22101 / 1440（大众热门，8 年仍高速增长） |
| 代码行数 | 1M+（但 **Rust 引擎仅 26 万行/26%**；Python 72.8% 是 vendored CPython 标准库 + 移植的 CPython 测试套件，是「兼容标尺」非团队手写） |
| 项目年龄 | 96 个月（8 年，2018-05 起） |
| 开发阶段 | 密集开发（近 30 天 221 commit、近一年 2452，2025-12 起强势复兴） |
| 贡献模式 | 超分散社区驱动（563 人，top 仅 13.6%，巴士因子健康；周末 32.8%/夜间 27.2% = 志愿者业余投入） |
| 热度定位 | 小众精品/细分标杆（高知名度但定位常被误读——非 CPython 替代品） |
| 质量评级 | 代码[优·19-crate 清晰分层] 文档[良·architecture + 兼容 dashboard] 测试[强·移植 CPython 测试套件] |
| License | MIT |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

项目 2018 年由荷兰开发者 **Windel Bouwman（windelbouwman）** 发起，长期核心 lead 是韩国开发者 **Jeong YunWon（youknowone，多账号合计约 2785 commit）**，当前提交量最高的是 **Noa（coolreader18，1777）**。org `RustPython`（231 followers）。这是典型「核心少数 + 563 人大社区」治理，坐落在 Rust 与 Python 两大社区的交叉地带，周末/夜间提交占比高（社区/志愿者驱动，而非公司全职）。

### 问题判断

CPython 是 Python 的事实标准，但它有 C 依赖、重、难嵌入 Rust、WASM 化困难。团队看到的缺口是：**应该有一个纯 Rust、内存安全、易嵌入、能编译到 WASM 的 Python 实现**——就像 Jython 之于 JVM、IronPython 之于 .NET，Rust 生态也需要一个原生的 Python。它不追求性能或 C 扩展兼容去硬刚 CPython/PyPy，而是占据「嵌入 + WASM + 沙箱 + 教育」这些 CPython 笨重之处的空位。

### 解法哲学

- **明确选择「干净实现、不为兼容做 hack」**（clean implementation, no compatibility hacks）：目标是完整的 Python 3 全部用 Rust 写，而非 CPython 的 C 绑定。
- **明确选择多目标后端**：同一引擎产出原生二进制、WASM、C API、（实验性）JIT。
- **明确选择兼容性测试驱动**：移植 CPython 官方测试套件，用通过率量化进展。
- **明确选择 19-crate 工作区**：编译器/VM/stdlib/多目标干净解耦，可独立演进/复用（parser 被 Ruff 复用即明证）。
- **明确不追 1.0**：8 年仍 v0.x，是对「100% CPython 兼容」高门槛的克制与务实。

### 战略意图

RustPython 是社区驱动的纯开源项目（无商业化），战略价值在于成为「Rust 生态的 Python」基础设施——被需要嵌入 Python/WASM Python/沙箱 Python 的项目采用，并以 parser 等组件反哺 Rust 生态（Ruff）。它不与 CPython 争生产主场，而是深耕差异化的细分。

## 核心价值提炼

### 创新之处

1. **19-crate 解释器工作区**（最值得学）：前端 `compiler-source→compiler-core→compiler→codegen`（源码→字节码，这条链的 parser 被 Ruff 复用）+ `vm`（执行字节码的核心）+ `stdlib`（Rust 实现的标准库）+ 多目标 `jit`(cranelift)/`wasm`/`capi` + 基础设施 `sre_engine`(正则)/`wtf8`(编码)/`derive`(过程宏)。清晰分层让各模块可独立演进、独立测试、独立复用——是大型解释器能持续 8 年的结构性前提。
2. **WASM 原生**：编译到 WebAssembly 在浏览器跑 Python，运行时极小——这是它区别于 CPython 的杀手级差异点。
3. **可嵌入 Rust（C API）**：作为 crate 内嵌进 Rust 程序，无 CPython 的 C 运行时依赖，内存安全——近期 capi 是开发重点。
4. **兼容性测试驱动**：移植 CPython 官方测试套件 + 兼容 dashboard 量化通过率。

### 可复用的模式与技巧

1. **多 crate 关注点分离**：把大型系统拆成可独立编译/复用的 crate（parser 被 Ruff 拿去用是最佳例证）——任何大型 Rust 项目都该学。
2. **移植上游官方测试当验收基准**：重新实现某语言/标准时，用上游官方测试刷通过率，而非自造测试——唯一正道。
3. **同一引擎多目标后端**：native/WASM/C API/JIT 共享核心，按场景产出不同产物。
4. **过程宏减样板**（derive/derive-impl）：用 Rust 宏减少解释器实现的重复代码。

### 关键设计决策

- **纯 Rust 重写 vs C 绑定**：选纯 Rust（内存安全、易嵌入、WASM 友好），代价是性能不及 CPython/PyPy、不支持 C 扩展。
- **不追 1.0**：8 年 v0.x，诚实反映完整复刻 Python 的工程量，而非停滞。
- **社区驱动**：563 人协作，巴士因子低、韧性强，但节奏依赖志愿者业余时间。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | RustPython | CPython | Pyodide | PyPy | MicroPython |
|------|------------|---------|---------|------|-------------|
| 实现 | 纯 Rust | C（参考实现） | CPython→WASM | RPython+JIT | C（精简） |
| WASM/浏览器 | ✓ 原生轻量 | 难 | ✓ 兼容最全但重 | ✗ | 部分 |
| 嵌入 Rust | ✓ 无 C 依赖 | 难 | ✗ | ✗ | 嵌入式 |
| C 扩展(numpy) | ✗ | ✓ | ✓ | 部分 | ✗ |
| 性能 | 慢 | 基准 | 慢 | 快 | 受限场景 |
| 定位 | Rust 生态 Python | 生产主力 | 浏览器 Python | 高性能 | 单片机 |

### 差异化护城河

护城河 =「**纯 Rust（内存安全、无 C 依赖、易嵌入 Rust）+ WASM 原生 + MIT + Ruff 等血缘背书 + 8 年社区积累**」这一精确组合，几乎独占。但每个单一维度都有更成熟对手——浏览器 Python 有 Pyodide（兼容更全），高性能有 PyPy，嵌入式有 MicroPython。它的优势是「交集」而非「单点最强」。

### 竞争风险

- **天花板受 v0.x 成熟度与 C 扩展缺失制约**：不支持 numpy/pandas 等 C 扩展，性能慢，限制了生产采用面。
- **Pyodide 在浏览器场景压制**：CPython→WASM 兼容性更全，能跑科学计算栈。
- **依赖志愿者节奏**：社区驱动韧性强但投入波动（曾有 2023-2024 低谷）。
- **定位易被误读**：被当成「CPython 杀手」会失望——它本就不为此。

### 生态定位

它是「Rust 生态里的 Python 实现」——填补 CPython 在嵌入/WASM/沙箱场景的空白，并以组件（parser）反哺 Rust 工具链（Ruff）。在「纯 Rust + 可嵌入 + WASM」交集近乎独占。

## 套利机会分析

- **信息差**：非被低估（22k star 共识级），但**定位常被误读**——许多人以为它要替代 CPython。内容价值在讲清「它真正适合什么（嵌入/WASM/沙箱/教育）、不适合什么（高性能/科学计算生产）」，以及「解释器工程 + 兼容性测试驱动」的工程范式。
- **技术借鉴**：「多 crate 关注点分离」「移植上游测试当基准」「同一引擎多目标后端」可迁移到任何重实现/编译器项目。
- **生态位**：想在 Rust 里嵌 Python、在浏览器跑 Python、做沙箱化 Python 执行的人，这是现成选择；想学解释器/编译器原理的人，这是优质的真实大型样本。
- **趋势判断**：WASM + 可嵌入脚本 + Rust 生态持续升温，RustPython 卡位独特；但 C 扩展缺失与性能是长期天花板，需理性看待。

## 风险与不足

- **⚠️ 不是 CPython 生产替代品**：仍 v0.x、性能慢于 CPython/PyPy、**不支持大多数 C 扩展（numpy/pandas 不可用）**，官方自述「not totally production-ready」。「兼容 CPython 3.14」是持续追赶目标而非已完全达成。适用边界=嵌入/WASM/沙箱/教育；不适合=高性能计算、科学计算生产。
- **依赖志愿者节奏**：社区驱动，投入有波动（2023-2024 曾低谷，2025-12 复兴）。
- **JIT 仍极实验性**：cranelift JIT 标注「very experimental」，不是当前重心，别当核心卖点。
- **8 年 v0.x**：完整复刻 Python 的工程难度使然——理解为「马拉松」而非「停滞」。
- 注意区分：它与 CPython 官方「Rust for CPython」PEP（让 Rust 写 CPython 扩展模块）是两个不同项目，勿混淆。

## 行动建议

- **如果你要用它**：你想**在 Rust 程序里内嵌 Python 脚本**（避开 CPython C 依赖、要内存安全）、**在浏览器/WASM 里跑 Python**、或做**沙箱化 Python 执行**——它是现成且近乎独占的选择（crates.io 上 `rustpython`）。要浏览器跑完整科学计算栈用 Pyodide；要高性能用 PyPy；要生产主力仍用 CPython。**别拿它跑 numpy。**
- **如果你要学它**：这是学「解释器/编译器如何用 Rust 实现」的顶级真实样本。重点读 `crates/codegen`（源码→字节码编译器，parser 被 Ruff 复用）、`crates/vm`（虚拟机执行核心）、`crates/stdlib`（Rust 实现标准库）、`crates/wasm`（WASM 目标），以及 `Lib/test`（兼容性测试驱动的范式）+ `architecture/architecture.md`。
- **如果你要 fork/借鉴它**：最有价值的是复用其 parser/codegen 组件（如 Ruff 所做），或针对你的嵌入场景裁剪；贡献方向可看兼容 dashboard 上未通过的 CPython 测试。

### 知识入口

| 资源 | 链接 |
|------|------|
| 在线 Demo | https://rustpython.github.io/demo/ （WebAssembly 浏览器跑 Python REPL） |
| DeepWiki | https://deepwiki.com/RustPython/RustPython （已收录，含模块化架构 + 四阶段编译流水线） |
| Zread.ai | 未确认（探测 403） |
| 架构文档 | 仓库内 `architecture/architecture.md` ｜ crates.io [rustpython](https://crates.io/crates/rustpython) ｜ docs.rs |
| 血缘/采用 | [Ruff（早期 parser 基于 RustPython）](https://github.com/astral-sh/ruff) ｜ GreptimeDB（嵌入式脚本） |
| 同类对照 | [Pyodide（CPython→WASM）](https://github.com/pyodide/pyodide) ｜ PyPy ｜ MicroPython |

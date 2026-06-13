# 33K★ swc：取代 Babel 的 Rust 编译器，9 年怎么炼成

> GitHub: https://github.com/swc-project/swc

## 一句话总结

swc 是用 Rust 重写 JavaScript/TypeScript 编译器的「前端工具链 LLVM」——单核作者 9 年、11,919 commits、33,615★，以 20× Babel 的速度被 Vercel/Next.js/Parcel/Deno 钦定为默认编译器，并通过 WASM 插件系统 + 零拷贝序列化把「速度」与「可扩展性」这两个对立面统一起来。

## 值得关注的理由

1. **「Babel 之后」的事实标准**：从 Next.js 13 起，`.ts`/`.tsx` 编译默认走 swc 而不是 Babel，Vite、Parcel、Deno、Rspack 等十数个工具链直接消费 swc 9 年沉淀的 crate 拆分。
2. **「极致性能 + 极简可扩展」的工程活标本**：Atom 内联字符串、rkyv 跨 WASM 零拷贝、scoped allocator + `Id<T>` generational handle——三件套是任何写编译器/解析器/插件系统的项目都该照搬的设计。
3. **「单核 owner 长期主导」的现实样本**：Donny/강동윤（kdy1）个人 43% commits、Apache-2.0 不卖身、不接 Vercel 公司 fork——给「个人 OSS + 公司背书」混合治理打了个标杆。

## 项目展示

![swc logo](https://swc.rs/logo.png) — 类型: hero（官网头图，Speedy Web Compiler 标识）

![Star History Chart](https://api.star-history.com/svg?repos=swc-project/swc&type=Timeline) — 类型: hero（时间序列 star 增长图，9 年持续上扬 + 短期脉冲）

![Sponsors](https://raw.githubusercontent.com/swc-project/swc-sponsor-images/main/sponsors.svg) — 类型: screenshot（赞助商墙，Vercel/Shopify/Cloudflare/ByteDance 等商业生态）

[Online Playground](https://swc.rs/playground) — 类型: demo（官方在线 Playground，可即时输入 TS 看转译输出）

> 筛选说明：总共发现 11 个媒体元素，筛选后保留 4 个；排除了 ~5 个 npm 下载量徽章、CI 状态、crates.io 版本等纯装饰元素。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/swc-project/swc |
| Star / Fork | 33,615 / 1,398 |
| 代码行数 | 9,437,912 总行（产线 Rust ≈ 36.8 万行 / 3.9%；其余为 JSON/JS/TS 测试 fixture 与 conformance 套件） |
| 主语言 | Rust 97.1% |
| 项目年龄 | 101.8 个月（≈ 8 年 6 个月，首次提交 2017-12-22） |
| 总 commit | 11,919（近 365 天 1,230 commit，日均 3.4） |
| 开发阶段 | 密集开发（年 commit 1,230，仍在快速迭代） |
| 开发模式 | 职业项目（周末 19.4% / 深夜 28.8%；Organization 账号 + 商业赞助） |
| 贡献模式 | 单核主导（Top 1 `kdy1` 占 39.7~43.0%，158 长尾贡献者共担其余） |
| 热度定位 | 大众热门（前端工具链基础设施，Top 5 级别） |
| 质量评级 | 代码 A / 文档 A / 测试 A / CI A+（15 个 workflow 含 bench / binary-size / ecosystem-ci） |
| 许可证 | Apache-2.0 |
| 版本策略 | 语义化版本 + 双轨（stable + `v1.15.x-nightly-YYYYMMDD.N`），8.5 年累计 1,335 tag |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Donny/강동윤（kdy1），韩国开发者，2017-12 在 NAVER 体系下启动 swc，定位为「spdy web compiler」。9.2 年下来仍是单一 owner 主导（43% commits），合作者 OJ Kwon 与 Vercel/Next.js 团队形成「原作者 + 核心维护者 + 商业赞助方」三件套。值得注意的是：项目 `Cargo.toml` 的 authors 字段仍署名个人邮箱「강동윤 <kdy1997.dev@gmail.com>」——**没有把版权转给 Vercel 也没有公司化**，这是「个人 OSS + 公司背书」混合治理的现实样本。

### 问题判断

Babel 时代 JS 工具链的核心矛盾：**慢**（JS 写）+ **灵活**（plugin 集市）。Donny 看到的机会窗口是 Rust 在 2017-2018 编译器生态的成熟（rustc、deno 都已证明 Rust 能写工业级编译器），加上 Next.js 8+ Webpack 构建时间爆炸成为业界痛点——这是「速度优先 + WASM 插件保扩展」的时机判断。

### 解法哲学

`AGENTS.md` 写明：「Write performant code. Always prefer performance over other things.」——这不是口号而是 commit 评审条款。具体到执行层：

- **选 Rust 不选 Go**：与 esbuild 选 Go 不同，Rust 给出更精细的零成本抽象（Atom 内联字符串、scoped allocator、rkyv 零拷贝）以及更可控的 WASM 路径。
- **明确不做类型检查**（#571 8 年争论后定）：swc 只做语法层转译，把类型完全交给 tsc——这种「明确不做什么」让 swc 边界清晰、不陷入 TS 类型系统这个无底洞。
- **自建 AST 不接 Babel AST**（#1392 长期 open）：拒绝与 Babel 兼容 AST 的生态复用诱惑，换取「为速度重塑数据结构」的自由。
- **多 crate workspace 拆分**：v1 把 120+ crate 拆到 workspace，让用户通过 `swc_core` facade 单一 feature 矩阵选 crate，避免「latest of each crates will work」承诺被破。

### 战略意图

swc 在作者更大图景中的位置是 **「上游公共品」**——不是直接面向终端用户的工具，而是被 Next.js/Vite/Parcel/Deno 等十数个工具链消费的中间层。这种定位带来三条商业化路径：

1. **Open Collective 公开赞助**（Vercel/ByteDance/Shopify/Trip.com 大额赞助方）
2. **生态捕获**：被 Next.js 锁定 = 锁定 React/Next.js 千万开发者
3. **不卖身**：Apache-2.0 + 持续在 swc-project 组织下开发，避免变成 framework 锁死

> 官网设计哲学补充：「extensible」——WASM 插件系统 + rkyv 零拷贝序列化 = 把「JS 写 plugin + 原生级速度」两个以前对立的事统一了。

## 核心价值提炼

### 创新之处

按新颖度×实用性排序：

1. **rkyv 跨 WASM 零拷贝 AST**（新颖 5 / 实用 4 / 可迁移 4）——把「插件系统性能」从「serde 序列化」拉到「共享内存」级别，社区尚无等价物。
2. **WASM 插件 + plugin runner（wasmer / wasmtime 双 backend）**（新颖 5 / 实用 4 / 可迁移 3）——提供「JS 写 SWC transform」路径，是 Babel 生态的真正杀手锏。
3. **hygiene pass（解析后第一次给符号编号，第二次按编号改符号）**（新颖 5 / 实用 4 / 可迁移 3）——工业级实现，借鉴 rustc 宏卫生但更简单；可作为「DSL 卫生」教学样本。
4. **Atom / Wtf8Atom 内联字符串**（新颖 4 / 实用 5 / 可迁移 5）——改写「JS 工具链 = String 分配机器」这一默认；oxc 直接抄。
5. **scoped allocator + `Id<T>` generational handle**（新颖 4 / 实用 5 / 可迁移 5）——把 Rust 借用检查器在「pass 之间共享子节点」场景的痛点彻底解决。
6. **codegen-of-codegen（ast_node/parser/codegen 三件套宏）**（新颖 4 / 实用 4 / 可迁移 4）——把 200+ AST 节点的样板代码降到 0；缺点是 build 慢。
7. **fast_strip 模式（只剥语法不查类型）**（新颖 3 / 实用 5 / 可迁移 5）——明确边界；与 tsc 互不越权；oxc/esbuild 都已跟随。
8. **CI 矩阵含 binary-size + bench + ecosystem-ci**（新颖 3 / 实用 5 / 可迁移 5）——`.github/workflows/{bench,binary-size,ecosystem-ci,claude}.yml` 把「性能回归 + 二进制体积 + 生态集成」全自动化。

### 可复用的模式与技巧

| 模式 | 简述 | 适用场景 |
|------|------|---------|
| **Atom = inline string + CoW** | 32 字节内联 + 堆分配 fallback，避免 String 分配 | 任何 AST-heavy 库（Tree-sitter、oxc、Biome） |
| **rkyv 跨 FFI 边界** | 编译期 bytecheck + 共享内存传递 AST | plugin-heavy 系统（编辑器、规则引擎、AI agent runtime） |
| **scoped allocator + Id<T>** | 一次性 arena 分配 + 带 generation 的 typed handle | 编译器、查询引擎、游戏 ECS、规则引擎 |
| **Visit/Fold trait + Repeated** | 自动重复 pass 直到 fixed point | 多 pass 优化、求解器 |
| **facade crate + feature flag** | `swc_core` 统一 re-export + 互斥约束 | 多后端 + 多场景的基础库（数据库驱动、AI 推理、跨平台 GUI） |
| **明确「不做」清单** | #571 TS type checker 8 年争论后明确拒绝 | 任何「自己只做语法、不做语义」的工具 |

### 关键设计决策

1. **决策**: 把 swc_core 做成「feature-flag facade crate」
   - 问题: 120+ crate + 5 种绑定（Node/WASM/CLI/Rust direct）让用户手挑 10+ crate 选版本，必然破「latest of each crates will work」承诺
   - 方案: `swc_core` 单 facade crate，13 个 feature 在 `lib.rs` 顶层做 re-export + 互斥约束
   - Trade-off: 用户爽了，crate 内部出现「feature 矩阵爆炸」「不显式 feature 即编译失败的玄学」
   - 可迁移性: 极高——任何要发「多后端 + 多场景」的基础库都该照搬

2. **决策**: Atom 用 hstr::Atom 内联 + unsafe 而非 String 分配
   - 问题: JS AST 节点里 80%+ 的字段是 identifier/keyword/property key，String 分配 + 堆指针追踪是主要开销；String 也不支持 WTF-8
   - 方案: `#[repr(transparent)] struct Atom(hstr::Atom)` 配合 `Wtf8Atom` 解决 UTF-16 surrogate；序列化端用 `cbor4ii` 自定义编解码
   - Trade-off: unsafe 量增加（transmute / from_bytes_unchecked），需要 cbor 端 unsafe 配套
   - 可迁移性: 极高——任何 AST-heavy 库都该走 inline-string + CoW

3. **决策**: rkyv 跨 WASM boundary 零拷贝
   - 问题: SWC 插件要暴露给 JS/其他语言用，传统 `serde_json` 跨边界要 marshal → 插件性能死结
   - 方案: rkyv 0.8.16 + rancor 错误体系 + bytecheck 在编译期生成 `CheckBytes`；`memory_interop.rs` + `runtime.rs` 在 `swc_plugin_runner` 里做 guest→host 共享内存传递
   - Trade-off: rkyv 0.8 还在快速演进，跨大版本 ABI 不稳；用户必须启用 feature 才能享受
   - 可迁移性: 高——任何「host/guest 跨语言共享复杂数据结构」的场景都能用

4. **决策**: scoped bump allocator + Id<T> 带 generation 的 typed handle
   - 问题: AST 节点每变换一次都要 `clone()` 是性能死结；用 Rust 生命周期又会和「pass 之间共享子节点」冲突
   - 方案: `crates/swc_allocator` 提供 `Allocator::scope(fn)` 一次性 arena 分配；`crates/swc_arena` 用 `Id<T> = NonZeroU64 + PhantomData` 给不带生命周期的 typed handle，配 generation 防止悬垂引用
   - Trade-off: scope 边界外的对象不能持有 arena 内指针（程序员心智负担），debug 难
   - 可迁移性: 极高——编译器、查询引擎、游戏 ECS 都能直接套

5. **决策**: TS 「fast strip」而非真 tsc 替换
   - 问题: #571 TS type checker issue 争论 8 年，最终选择不做类型检查——避免在 swc 里重新实现 TS 类型系统
   - 方案: `swc_ts_fast_strip` 与 `binding_typescript_wasm` 只做「类型注解剥除 + 枚举/命名空间降级」——把类型完全交给外部 `tsc`
   - Trade-off: 用户必须双跑（`tsc --noEmit && swc`）；但与 `tsc` 行为一致，零边界 bug
   - 可迁移性: 极高——任何「自己只做语法、不做语义」的工具都该这样明确边界

6. **决策**: ES / CSS / HTML / XML / Regexp 共享 `swc_common` + `swc_atoms` + `swc_visit`
   - 问题: 5 种语言管道如果各做各的 span/hygiene/error reporter 就会重复 5 次
   - 方案: `swc_common`（span/hygiene/SourceMap/SyntaxContext/Mark）、`swc_atoms`（Atom/Wtf8Atom）、`swc_visit`（Visit/Fold trait + Repeated）下沉到所有语言管道共享
   - Trade-off: `swc_common` 改动一次就影响 5 个语言管道，CI 矩阵必须五向都跑
   - 可迁移性: 中——需要业务真的「多语言同源」才有价值

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | swc | oxc | biome | esbuild | babel |
|------|-----|-----|-------|---------|-------|
| 语言 | Rust 97% | Rust | Rust + 部分 Go | Go | JS |
| 性能 vs Babel | 20× | 20×+ | 10-15× | 15-20× | 1× |
| Plugin 系统 | WASM 插件 + rkyv 零拷贝 | 无（自建 transform API） | Rome 风格 config | 不可扩展（明确拒绝） | JS plugin 集市 |
| AST | 自建（swc_ecma_ast） | 自建（oxc_ast） | 自建（biome_js_syntax） | 自建 | estree 兼容 |
| 多语言管道 | ES/CSS/HTML/XML/Regexp | ES（主）/ CSS | JS/TS + JSON | ES + CSS（部分） | JS/TS |
| 集成规模 | Next.js/Parcel/Deno 默认 | Vite 官方合作 | Rspack/Vite 部分 | Vite/Bun 默认 | 几乎所有 |
| Conformance | test262 + tsc-references | test262 | test262 | test262 | test262 |
| 商业赞助 | Vercel/ByteDance/Shopify | ByteDance/Vite | 社区赞助 | 个人 + Cloudflare | 社区 + OpenJSF |
| 治理 | 单核 owner + 公司背书 | 较年轻单一团队 | 社区主导 | Evan Czaplicki 一人 | 基金会 + 社区 |

### 差异化护城河

1. **「WASM 插件 + rkyv 零拷贝」是真正护城河**——把「JS 写 plugin + 原生级速度」两个以前对立的事统一了，oxc/biome 都还没等价物。
2. **9.2 年沉淀的 `swc_ecma_compat_*` / `swc_ecma_regexp_*` / `swc_ecma_preset_env`**——「一个语言版本一个 crate」的细粒度拆分，竞品都在追赶。
3. **Vercel/Next.js 官方集成 + 五大赞助方**——其他 Rust 竞品短期拿不到的资源。
4. **多语言管道（ES/CSS/HTML/XML/Regexp）**——oxc 主要是 ES，biome 主要是 JS+JSON，swc 的「全 Web 编译器」定位是唯一。
5. **Apache-2.0 友好许可 + 不卖身**——对比 esbuild/oxc 的强公司绑定，swc 在企业级采用上有信任优势。

### 竞争风险

1. **biome 整合上游**（高）——biome 已经在内化 parser+transformer 层，如果未来 biome 能直接被 swc 之外的工具链消费，会蚕食 swc 在「应用层」的空间。
2. **oxc 性能 + Vite 绑定**（中）——年轻项目 + 强赞助，性能反超，Vite 生态可能完全切到 oxc；swc 需要保住「多语言 + 插件」双护城河。
3. **esbuild 默认化**（中）——新项目首选 esbuild 的趋势在 Bun/Vite 生态中加剧；swc 必须靠 WASM 插件留出 plugin 退路。
4. **Babel 退出历史**（低/利好）——Babel 的退出是 swc 利好。
5. **terser 被边缘化**（低/利好）——minifier 领域 swc 已经几乎替代 terser。

### 生态定位

> swc 已经从「Babel 的更快替代品」演化为「**前端工具链的 LLVM 中间层**」——不直接面向终端用户，而是被 Next.js/Vite/Parcel/Deno/Nuxt/Rspack 等十数个工具消费。

**真正的胜负手是：当 plugin 生态足够大时，swc 不需要自己赢任何单点工具战**——只要继续做「被集成最快的那块拼图」。

## 套利机会分析

- **信息差**: 否。swc 已是行业基础设施级项目（33,615★、Vercel/ByteDance 真生产负载托底），无套利空间。
- **技术借鉴**: 极高。**Atom + rkyv + scoped allocator** 三件套是任何写编译器/解析器/插件系统的项目都该照搬的设计。
- **生态位**: 填补「Babel 退出后的 JS 工具链底座」空白。竞品都在追赶，但 swc 9.2 年沉淀的 120+ crate 是事实护城河。
- **趋势判断**: swc 处于「成熟期稳定维护 + 持续演进」阶段（2024+ 月均 commit 收敛到 60~210），**主战场是保住 Vercel/Next.js 锁定 + 拓展 WASM 插件生态**；最大变量是 oxc 在 2025-2026 的快速追赶。

## 风险与不足

1. **单核 owner 风险**：43% commits 集中在 Donny/강동윤 一人，owner 倦怠/转向任何因素都会导致节奏断档。
2. **rkyv ABI 不稳**：0.8 版本还在快速演进，跨大版本 ABI 不稳，下游插件开发者需要跟进 breaking change。
3. **Cargo.lock 治理成本**：4,608 次 Cargo.lock 更新 ≈ 日均 ≥ 1.5 次依赖调整，版本治理不轻。
4. **unsafe 集中**：Atom/rkyv/FFI 层都涉及 unsafe，core parser 43 unwrap、minifier 97 unwrap（性能优先 tradeoff），安全审计成本不低。
5. **文档薄文厚码**：ARCHITECTURE.md 只覆盖到 152 行且聚焦于历史宏，深度架构需要从 `swc_core/src/` 的 `__diagnostics.rs` `plugin.rs` `quote.rs` 推断——新人 onboarding 成本高。
6. **「untrusted input security scope」v1.15.41 文档化**——项目开始主动收敛「安全边界」承诺，是走向成熟基础设施的信号，但也意味着不要把 swc 当 sandbox 跑不可信代码。
7. **biome 上游整合**（最大外部风险）——biome 正在把「parser+transformer」层内化，未来可能直接蚕食 swc 在「应用层」的空间。

## 行动建议

- **如果你要用它**:
  - **大型 Next.js 项目**：直接用 `swc` 配置（默认就是），20× 速度提升立竿见影
  - **自定义 transform 需求**：优先用 WASM 插件 + rkyv 模式（不要 fork），保持 swc 上游同步
  - **TS 类型检查**：双跑 `tsc --noEmit && swc`（不要期待 swc 做类型检查）
  - **多语言需求**（CSS/HTML/XML）：swc 是唯一支持全套的 Rust 工具链

- **如果你要学它**:
  - **第一站**：`crates/swc_atoms/src/lib.rs`——Atom 内联字符串是 swc 最值钱的「一行决策」
  - **第二站**：`crates/swc_plugin_runner/src/{runtime.rs, transform_executor.rs, memory_interop.rs}`——WASM 插件执行核心
  - **第三站**：`crates/swc_allocator/src/lib.rs` + `crates/swc_arena/src/lib.rs`——scoped allocator + Id<T> 模式
  - **第四站**：`crates/swc_ecma_visit/src/lib.rs`——Visit/Fold trait + Repeated 自动重复 pass
  - **第五站**：`crates/swc_core/Cargo.toml`——facade crate 的 feature 矩阵设计

- **如果你要 fork 它**:
  - 方向 1: **WASM 插件市场**——swc-project/plugins 已有 387★，可深耕插件分发
  - 方向 2: **swc_ecma_react_compiler** 独立成 npm 包——7,179 次变更说明 React Compiler 集成是高需求方向
  - 方向 3: **preset_env 优化**——按 browser target 自动选 transform 子集是最干净的实现
  - 方向 4: **绑定新语言管道**——CSS/HTML 已有，可考虑 SVG/GraphQL/JSON Schema
  - 方向 5: **避免重做**：不要重做 TS 类型检查、不要做完整 bundler（已有 swc_bundler）——做边界外的事

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [https://deepwiki.com/swc-project/swc](https://deepwiki.com/swc-project/swc)（已收录，含 5 层 crate 架构详解） |
| Zread.ai | 未确认收录（当前会话 WebFetch 返回 403） |
| 关联论文 | 无（工程类项目，无对应 arXiv 论文） |
| 在线 Demo | [swc-playground](https://swc.rs/playground)（官方在线 Playground，可即时试转译） |
| 架构文档 | [swc.rs](https://swc.rs/) + 仓内 `ARCHITECTURE.md` / `AGENTS.md` |
| 关键博客 | [Performance Comparison of SWC and Babel](https://swc.rs/blog/perf-swc-vs-babel)（Babel 团队本人写的「被超车」基准） + [Introducing SWC 1.0](https://swc.rs/blog/swc-1) |

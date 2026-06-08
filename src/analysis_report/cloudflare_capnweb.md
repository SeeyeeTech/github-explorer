# Cap'n Proto 之父的 JS 新作 Cap'n Web：把相互依赖的 RPC 调用压进一次网络往返

> GitHub: https://github.com/cloudflare/capnweb

## 一句话总结

Cap'n Web 是 Cloudflare 出品、由 Cap'n Proto / Protobuf v2 作者 Kenton Varda 操刀的 JS/TS 原生「对象能力 RPC」系统：它让你像调用本地对象一样写 RPC，却能把一串相互依赖的调用**坍缩进一次网络往返**（promise pipelining），还能把函数/对象**按引用**跨网络传递（对象能力 + 双向回调）。零运行时依赖、压缩后不到 10KB、传输无关——这是 Kenton 二十年 RPC 思考（Protobuf → Cap'n Proto → Cap'n Web）的第三次迭代。

## 值得关注的理由

1. **tRPC 阵营没有的两件杀手锏**：① Promise Pipelining——拿到 RPC 返回的 promise 不必 await，可直接当参数喂给依赖它的后续调用，N 个依赖调用在一次往返里完成（甚至有 `.map()` 在一次往返里遍历返回数组取每项详情，消除 N+1 往返）；② 对象能力——函数/对象按引用传递，接收方拿到 stub 调用即回调到源端，天然双向 RPC + 能力式安全。主流的 tRPC 本质仍是请求/响应，这两点都没有。
2. **一个「不传代码却能远程变换」的精巧实现**：`.map()` 怎么在不上传任意代码的前提下做远程 lambda？用 record/replay——本地用占位 stub 把回调跑一遍、录成一段确定性「指令磁带」发过去回放。这种「录制操作而非传函数」的设计，是可迁移到远程批处理、查询下推、可审计 lambda 的范式。
3. **顶级血统 + 认知套利**：作者 Kenton Varda 在 Google 开源了 protobuf、创造了 Cap'n Proto、是 Cloudflare Workers 的架构师。但 Cap'n Web 只有 3.8K star——远低于其技术稀缺性与作者声望应得的关注度。多数 JS 开发者只知 tRPC，不知道「promise pipelining + 传引用能力」这一更强范式，是绝佳的深度技术选题。

## 项目展示

> 仓库无配图，README（42KB）以大量代码示例为主，另有一份完整的 `protocol.md`（19KB wire 规范，RPC 库里罕见，意味着别的语言可实现兼容端）。建议自制两张图：「串行 RPC 多次往返 vs Cap'n Web pipelining 单次往返」对比示意，以及「函数/对象传引用 → stub 回调」的双向调用流程图——最能讲清差异化。官方阐释见 [Cloudflare 发布博客](https://blog.cloudflare.com/capnweb-javascript-rpc-library/)。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/cloudflare/capnweb |
| Star / Fork | 3,828 / 132 |
| 代码行数 | 真实 TS 约 9,000 行（总 17,719 含 JSON lock/示例数据）；**零运行时依赖**，minify+gzip < 10KB |
| 项目年龄 | 12.4 个月（2025-05-25「Initial commit」） |
| 开发阶段 | 稳定维护（首年高强度成型，2025-09 峰值 58 commit，近 30 天 5） |
| 贡献模式 | 单核心作者主导（27 人，Kenton Varda 占约 54–69%） |
| 热度定位 | 中等热度（3.8K star，认知套利空间大） |
| 质量评级 | 代码「优」 文档「优」（含 protocol.md 规范） 测试「优」（含类型层测试） 零依赖「优」 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

owner 是 Cloudflare（13,730 followers），但本项目的灵魂是 **Kenton Varda（@kentonv）**——RPC/能力安全领域的活历史：在 Google 编写并开源了 **Protocol Buffers v2**（业界通用的 protobuf）、创造了带 promise pipelining 的 **Cap'n Proto**、联合创办能力式安全云平台 **Sandstorm**、Sandstorm 团队被 Cloudflare acqui-hire 后成为 **Cloudflare Workers 架构师**（从零设计 V8 运行时）。他在本仓库占约 54–69% 贡献，绝对主导。这不是普通公司项目，而是**领域顶级专家二十年思考的第三次迭代**（protobuf → Cap'n Proto → Cap'n Web），作者可信度满分。

### 问题判断

要让浏览器/JS 里的 RPC「写起来像调用本地对象」，同时补偿网络往返延迟。传统请求/响应式 RPC 的根本痛点是：每个依赖前一个结果的调用都要再付一个 RTT，开发者被迫手写聚合端点或客户端串行 await。现有方案不够在于：tRPC 等仍是请求/响应、不支持传引用、没有真正的双向调用；作者自己的 Cap'n Proto 需要 schema + 代码生成 + 二进制，在浏览器里水土不服（`protocol.md` 专门论证了「为什么不用二进制」——JSON 才是浏览器原生公民）；Comlink 有传引用但只面向同源 Worker。

### 解法哲学

「让网络消失在对象引用背后」+「绝不在线上传任意代码」。两条看似矛盾的诉求（既要 `.map()` 远程变换、又不能传代码）通过 **record/replay** 调和：本地用占位 stub 跑一遍回调、录成确定性指令磁带发过去回放。哲学源头是 E 语言 / CapTP 的对象能力模型 + promise pipelining，落到 JSON 这个浏览器最低公分母上。「Cap'n」= "**cap**abilities **a**nd"。

### 战略意图（Cap'n Proto → Cap'n Web）

对 Cloudflare 而言这是 Workers RPC 的「开放标准化」推广——`RpcTarget` 在 Workers 上直接 alias 内建实现，stub 可在两套系统间互传代理。继承 Cap'n Proto 的对象能力 + pipelining，但把 CapTP 的四张表（imports/exports/questions/answers）**合并成两张**、去 schema、去二进制、改用可读 JSON。一份完整 wire 规范（`protocol.md`）意味着别的语言可实现兼容端。Kenton 在赌：JS 是最大的 RPC 战场，谁定义了「JS 里 RPC 该长什么样」，谁就拿到生态位。

## 核心价值提炼

> 诚实区分：promise pipelining 与对象能力的**理念**源自 Cap'n Proto / CapTP / E 语言（1990s）；本仓库的创新在于把它们以**零样板、JSON 可读、<10KB、传输无关**的形态原生落到 JS/TS，以及 `.map()` record/replay 与 BDP 流控的具体实现。

### 创新之处

1. **Promise Pipelining 的纯 JS 实现**（新颖度 4/5，实用性 5/5，可迁移性 4/5）：发送侧 `RpcStub` 是套在 dummy 函数上的 **JS Proxy**，属性访问只把路径 push 进 `pathIfPromise`（纯本地、零消息），调用立刻发请求并同步返回一个未解析的 `RpcImportHook`、绝不阻塞。当这个未决 promise 被当作后续调用的参数时，序列化器把它编码成 `["pipeline", importId, path]`——**传的是「还没算出来的结果的引用」而非值**；服务端按依赖 DAG 顺序求值。N 个依赖调用 = 1 个 RTT。
2. **`.map()` record/replay 远程变换**（新颖度 5/5，可迁移性 3/5）：用全局 `CallInterceptor` 把回调跑一遍、录成确定性指令磁带 `["remap", id, path, captures, instructions]`（索引语义：负=captures、0=输入、正=前序结果），服务端逐元素回放。**不传任何代码**却实现远程 lambda，一次往返批量富化、消除 N+1 查询。
3. **对象能力 + 双向对等 RPC**（新颖度 3/5，实用性 5/5）：函数与 `RpcTarget` 子类序列化为 `["export", id]`，接收方导入为 stub，调 stub 即回源；协议层**无 client/server 之分**，双向回调自然涌现。`reverseExports` 表对同一 hook 复用 export ID 并自增 refcount，`BoxedRefcount` 保证底层对象的 `Symbol.dispose` 在所有 dup 释放后恰好触发一次。
4. **可读 JSON wire + 完整协议规范**（新颖度 3/5，可迁移性 5/5）：除数组外的 JSON 类型字面解释；数组首元素当类型码（`["date",n]`/`["bigint",s]`/`["error",...]`/`["import"|"pipeline"|"export"|"remap",...]`），真正的字面数组用外层数组转义成 `[[...]]`。自描述、可调试、易跨语言实现；Evaluator 还拦截 `__proto__`/`toJSON` 防原型污染。这正是 #32 自定义序列化器的挂载点。
5. **流的 BDP/BBR 式流控**（新颖度 4/5）：`ReadableStream`/`WritableStream` 跨 RPC 多路复用，按带宽-延迟积动态调窗（初始 256KB、startup 每 RTT 翻倍、steady 1.25x），类 HTTP/2 多路复用——远超「玩具 RPC」的工程深度。

### 可复用的模式与技巧

- **Proxy-over-dummy-function 的惰性路径累积**：属性访问纯本地建 path、调用才触网——任何「远程对象代理 / 惰性查询构建器」。
- **统一能力接口 + 多实现多态（`StubHook`）**：本地值/远程/promise/error/录制占位全是同一抽象——需要「本地与远程行为透明替换」的系统。
- **record/replay 编码远程函数**：录制确定性操作磁带替代传代码——远程批处理、查询下推、可审计 lambda。
- **携带 refcount 的 release 消息**：抵消「ID 重导出」竞态——任何分布式引用计数。
- **两方法传输接口（send/receive）**：抽掉一切传输差异（HTTP batch/WebSocket/postMessage）——协议与传输解耦的中间件。
- **push/pull 惰性物化**：只在结果被真正 await（观测）时才回传——分布式惰性求值。

### 关键设计决策

最值得记录的是 **promise pipelining 的「Proxy 累积路径 + 未决 future 按引用编码」实现**（`src/core.ts` 的 RpcStub Proxy + `src/serialize.ts` 的 pipeline 编码 + `src/rpc.ts` 的依赖求值）。配套的 **push/pull 分离**是点睛之笔：`["push"]` 只请求求值并分配 import ID，纯用于 pipelining 的中间结果根本不回传；只有应用真正 await（触发 `pull()`）才发 `["pull"]`、服务端才回 `["resolve"]`。批量传输甚至用 `setTimeout(0)` 而非 `Promise.resolve()` 刷批，为的是给应用一个 tick 去对所有 promise 挂 `.then()`，从而精确知道哪些结果真要回传。这套「惰性 future + 只在被观测时物化 + 依赖引用编码」的组合，是把「网络往返」这个分布式根本约束优雅藏进对象引用的范本。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | Cap'n Web | tRPC | Comlink | Cap'n Proto（同作者） |
|------|------|------|------|------|
| Stars | 3.8K | ~40K | ~12K | ~12.7K |
| Promise pipelining | 有（核心） | 无 | 无 | 有 |
| 对象能力/传引用 | 有（双向） | 无 | 有（同源） | 有 |
| schema | 无（JSON） | TS 类型 + Zod | 无 | 需 schema + codegen |
| 内建校验 | 无（短板） | 有（Zod） | 无 | schema 强类型 |
| 场景 | 全栈网络双向 RPC | 类型安全 HTTP 端点 | 同源 Worker/postMessage | 多语言系统级 |

### 差异化护城河

四合一组合（promise pipelining + 对象能力/传引用 + 双向对等 + 传输无关）+ JSON 可读 + 零依赖 <10KB + Workers 原生互操作，**目前没有任何单一竞品同时具备**。叠加 Kenton Varda 的 RPC 血统与 Cloudflare 背书、一份可被第三方实现的完整 `protocol.md`。

### 竞争风险

- **仍 0.x**（v0.8.0），API / wire 未冻结；
- **无内建校验**（最大短板）：作者明确自承无运行时类型检查，注入风险全靠用户自接 Zod；
- **生态浅**：无 React Query 级集成、无成熟中间件；tRPC（40K）主导认知与招聘心智；
- **disposal/GC 认知负担高**：跨连接引用无法自动 GC、靠显式 `Symbol.dispose`，issue #110 类「stub 用后已释放」会反复出现；
- **正确性 TODO**：e-order 的 embargo（三方转发去抖）等尚未实现；
- **bus factor**：核心几乎单人（已见社区 PR，是缓解信号）。

### 生态定位

Cloudflare Workers / Durable Objects 全栈、低延迟交互、需要双向/能力委派场景的「网络消失层」。它不替代 tRPC 在「类型安全 HTTP 端点」的位置，而是开辟「JS 对象能力 RPC」新象限——是技术领先、成熟度待证的高潜小众标的。

## 套利机会分析

- **信息差**：star 量级（3.8K）远低于技术稀缺性与作者声望应得的关注度；多数 JS 开发者只知 tRPC，不知 promise pipelining + 传引用能力这一更强范式——「小众但血统硬核」的认知套利空间大，适合面向中高级 TS/全栈工程师的深度解读。
- **技术借鉴**：Proxy 惰性路径累积、record/replay 编码远程函数、push/pull 惰性物化、携带 refcount 的 release、两方法传输接口——这些可迁移到远程代理、批处理、分布式引用计数、协议中间件等远超 RPC 本身的领域。
- **生态位**：开辟「JS 对象能力 RPC」新象限，填补 tRPC/Comlink 之间「全栈 + pipelining + 传引用」的空白。
- **趋势判断**：踩在「全栈 TS + 低延迟交互 + Workers/边缘」趋势上；最大变量是能否补齐校验/生态、走出 0.x 把 wire 冻结，让第三方语言实现真正繁荣。

## 风险与不足

- **无内建运行时校验**：作者自承认，是相对 tRPC 的最大短板，安全/正确性靠用户自接 Zod。
- **API/wire 未冻结**：仍 0.x，可能有破坏性变更，生产需自行钉版本。
- **资源生命周期负担**：跨连接引用无法自动 GC，必须显式 disposal，认知成本高（issue #110）。
- **生态与心智浅**：tRPC 主导，Cap'n Web 缺成熟中间件/集成，招聘与社区资源少。
- **bus factor**：核心几乎单人主导，知识高度集中。
- **部分正确性特性未竟**：embargo、序列化失败时 pipe 回滚泄漏等代码内 TODO。

## 行动建议

- **如果你要用它**：适合「Cloudflare Workers/DO 全栈、低延迟交互、需要双向回调/能力委派、且能接受 0.x 与自接校验」的 TS 团队；尤其当你的 API 有大量相互依赖的链式调用或列表 N+1 往返时，pipelining 收益最大。要类型安全 HTTP 端点 + 成熟生态仍选 tRPC；同源 Worker 通信用 Comlink 即可。务必自接 Zod 等做输入校验。
- **如果你要学它**：直奔 `src/core.ts`（StubHook 能力内核 + RpcStub Proxy + 线性 payload + disposal）、`src/serialize.ts`（Devaluator/Evaluator wire 引擎 + pipeline 编码）、`src/rpc.ts`（会话 + imports/exports 表 + readLoop）、`src/map.ts`（`.map()` record/replay）、`src/streams.ts`（BDP 流控），并读 `protocol.md`（wire 规范）。这是一份难得的「对象能力 RPC」全栈参考实现。
- **如果你要 fork / 借鉴它**：Proxy 惰性路径累积、record/replay 远程函数、携带 refcount 的 release、两方法传输接口是可直接迁移的设计；按 `protocol.md` 还可实现其他语言的兼容端。注意 MIT。

### 知识入口

| 资源 | 链接 |
|------|------|
| 发布博客 | [Cap'n Web: a new RPC system for browsers and web servers（Cloudflare）](https://blog.cloudflare.com/capnweb-javascript-rpc-library/) |
| 协议规范 | 仓库内 `protocol.md`（完整 wire 规范，可第三方实现兼容端） |
| DeepWiki | https://deepwiki.com/cloudflare/capnweb（已收录，覆盖 stub/session/pipelining/序列化/传输/类型系统） |
| 理论源头 | [Cap'n Proto 官网](https://capnproto.org)（promise pipelining 与能力模型的理论源头）；[Cloudflare Workers JavaScript-native RPC](https://blog.cloudflare.com/javascript-native-rpc/) |

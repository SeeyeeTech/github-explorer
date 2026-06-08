# 曾撑起 GitHub 几乎每个页面：联合创始人的 591 行 RPC 库为何输给 gRPC

> GitHub: https://github.com/mojombo/bertrpc

## 一句话总结

bertrpc 是 GitHub 联合创始人、TOML / Semantic Versioning / Jekyll 之父 Tom Preston-Werner 在 2009 年写的 591 行 Ruby 库——它实现的 BERT-RPC 协议曾「serving nearly every page of GitHub」，是一份旗帜鲜明反对 IDL 与代码生成的协议宣言，最终却输给了 gRPC/Protobuf 的「类型安全 + 强工具链」组合，成为一份值得解剖的技术史标本。

## 值得关注的理由

1. **血统天花板**：作者是 GitHub「1 号用户」Tom Preston-Werner，合作者全是 GitHub 早期核心团队（defunkt = 前 CEO Chris Wanstrath、rtomayko、tmm1）。这不是路人项目，而是 GitHub 创始团队为自家基础设施打造的内部组件——血统远比 170 star 值钱。
2. **一份反 IDL 的设计宣言**：Tom 在 2009 GitHub 官博的名言「I find the entire concept behind IDLs and code generation abhorrent（我打心底厌恶 IDL 和代码生成这整套理念）」，让这个库成为「动态类型 + 零代码生成」RPC 哲学最优雅的极简实现，宣称 9 行代码起一个完整 RPC 服务。
3. **一个「正确的简洁 + 错误的时机」经典反面教材**：591 行可在一个下午通读，藏着链式 method_missing DSL、远端异常透明重建、select(2) 可靠超时等多个仍可复用的范式；同时它输给 gRPC 的全过程（官网 404、规范止步 1.x、停更 12 年）是研究「为什么大规模系统最终选择类型安全」的活案例。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/mojombo/bertrpc |
| Star / Fork | 170 / 21（Watcher 5）|
| 代码行数 | 591 行（Ruby 91.5%，零外部第三方依赖，仅依赖作者自家的 bert gem）|
| 项目年龄 | 约 17.1 年（205 个月，首次提交 2009-05-18）|
| 开发阶段 | 已放弃（最后提交 2014-08-11，近 12 年 0 提交）|
| 贡献模式 | 核心少数 + 社区（Tom Preston-Werner 独占 77 次提交、74.8%，共 7 名贡献者）|
| 热度定位 | 小众精品（停更 12 年、零营销仍每月 1-2 颗新 star 的长尾常青）|
| 质量评级 | 代码[优] 文档[良] 测试[良-优，按 2009 年标准]|

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Tom Preston-Werner（mojombo），GitHub 联合创始人 / 「1 号用户」（2007-10 注册），Jekyll、Gravatar、TOML、Semantic Versioning 的作者，粉丝 24,626、账号年龄 18.6 年。他在本库 77 次提交占 74.8%，但这只是其作品序列里一个早期小件——其主力遗产是 Jekyll、TOML、SemVer 等。作者可信度天花板级，项目的「血统」是本选题最大卖点。

### 问题判断

2009 年的 GitHub 正从单体 Rails 向「Rails 前端（Ruby）+ Erlang 后端」演进，核心矛盾是跨语言通信，且不想依赖共享文件系统就把分散在多台文件服务器上的 Git 仓库暴露成服务。Tom 作为 1 号工程师，问题视角是「如何用最小心智负担把 Erlang 能力暴露给 Ruby」。时机上 2009 年正是动态语言 + 二进制协议探索的窗口期（MessagePack 同年起步），Thrift/Protobuf 已存在但被他嫌「重」。

### 解法哲学

极致的「少即是多」与「明确不做什么」：**不做 IDL、不做代码生成、不做编译期类型检查**（契约下沉到运行时，用 method_missing 动态分发）；**不自造序列化**（全权委托 mojombo/bert gem，本库只管 DSL + 网络 + 错误三件事）；**协议特性按需实现**（README 坦白只支持 call/cast 两种请求，够用即止，不追求规范完备）。这正是他反 IDL 价值观的代码化落地。

### 战略意图

本库是 GitHub 早期「Grit / Ernie / BERT-RPC」文件服务栈的客户端一环，定位是内部基础设施而非对外产品，无任何商业化意图（MIT 许可）。它被弃用是历史性的：HTTP/2 + gRPC/Protobuf 凭借强类型、跨语言工具链、流式与负载均衡生态成为事实标准；BERT-RPC 规范止步 1.0/1.1，官网 bert-rpc.org 已 404（issue #4/#8 反复反映此事）。它赢在「当年够用、极简」，输在「没有类型安全与工具链护城河」。

## 核心价值提炼

### 创新之处

1. **三段式 method_missing 链式 RPC DSL**（新颖度 4/5・实用性 4/5・可迁移性 5/5）：`svc.call.calc.add(1,2)` 用三个对象各截获链上一段（kind / module / function），`Service#call` 显式返回 Request，`Request#method_missing` 把第二段当模块名返回 Mod，`Mod#method_missing` 把第三段当函数名 + 实参构造 Action 并立即发起网络——链尾才触发 I/O。把远程调用伪装成本地方法，零样板、无 schema。
2. **远端异常透明重建**（新颖度 4/5・实用性 5/5・可迁移性 4/5）：协议 error 元组 `[level, code, klass, message, backtrace]`，客户端据此构造携带远端 backtrace 的 `RemoteError` 并按 level 抛 Protocol/Server/User/ProxyError，调试体验接近本地异常（对应 issue #5）。
3. **可靠读/连接超时（select(2) + 非阻塞 connect + SO_*TIMEO）**（新颖度 3/5・实用性 5/5・可迁移性 4/5）：绕开 Ruby 缓冲 IO 不可靠超时，用 `IO.select` 等可读、`connect_nonblock` 处理 EINPROGRESS/EISCONN、再设 SO_RCVTIMEO/SO_SNDTIMEO 三重保险（对应 issue #1/#3 的生产痛点）。
4. **长度前缀分帧 + 编解码外包**（新颖度 2/5・实用性 5/5・可迁移性 5/5）：写时 `pack("N")` 先发 4 字节网络序长度再发载荷，读时先读 4 字节头再精确读 N 字节；序列化全委托 bert gem，本库只剩 DSL + 网络 + 错误三件事。

### 可复用的模式与技巧

1. **链式 Façade（method_missing 分层捕获）**：多个轻量对象沿链各捕获一个语义段，末端对象才执行真正动作 —— 适用于 DSL、Query Builder、远程调用客户端 SDK。
2. **Mixin 化编解码层**：把 encode/decode 抽成 module，既给 Action `include`，又能给测试类单独 include 做隔离测试 —— 适用于需要多处复用且单独可测的纯函数逻辑。
3. **长度前缀帧读写**：`pack("N")` 写头、先读 4 字节定长度再读体 —— 任何裸 TCP 自定义协议的标准做法。
4. **非阻塞 connect + IO.select 超时三连**：处理 EINPROGRESS/EISCONN/EAGAIN/ECONNRESET 的完整模板 —— 所有生产级 TCP 客户端必备。
5. **协议级别 → 异常类层级的一一映射**：用 case 把 :protocol/:server/:user/:proxy 映射到专属异常类，调用方可精确 rescue —— 适用于任何分层错误模型。

### 关键设计决策

- **请求 kind 设为显式方法、mod/fun 设为 method_missing**：kind（call/cast）是协议固定有限集且要带选项校验，故写成真方法；module/function 是无限用户空间，故交给 method_missing。「固定动词显式、可变名词动态」是设计可读 DSL 的实用准则。
- **序列化完全外包给 bert gem**：本库不碰字节级编码，单一职责、极小易测；代价是把性能与正确性命门交给外部依赖。「协议库与传输库分离」是健康的依赖切分。
- **带外缓存协商帧（info 前置帧）**：正式请求前 piggyback 一个 `[:info, :cache, [:validation, token]]` 帧，且选项严格白名单——以最小侵入扩展协议。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | bertrpc (BERT-RPC) | Apache Thrift | gRPC / Protobuf | MessagePack-RPC |
|------|--------------------|---------------|------------------|------------------|
| 量级 | 170★（已停更）| ~10k★ | gRPC ~42k★ / protobuf ~67k★ | ~6k★ |
| Schema/IDL | 无（运行时动态）| 必须写 IDL + 代码生成 | 必须写 .proto + 编译 | 无 |
| 类型安全 | 弱（运行时）| 强 | 强 | 弱 |
| 传输 | 裸 TCP，一问一答即关 | 多传输可选 | HTTP/2 多路复用 + 流式 | 裸 TCP |
| 工具链/生态 | 仅 GitHub 自用 | 工业级成熟 | 事实标准、全语言一等支持 | 跨语言广、存活至今 |
| 现状 | 协议消亡、官网 404 | 活跃 | 主导 | 存活 |

### 差异化护城河

本质很薄——唯一真正的差异化是「深度贴合 Erlang ETF（原生 atom/tuple/复合类型）+ GitHub 生产背书」。极简和无 schema 既是优点也是软肋，缺乏类型安全与工具链就没有长期护城河。

### 竞争风险（已兑现）

已输给 gRPC/Protobuf 的「类型安全 + 强工具链 + HTTP/2 生态」阵营；规范停在 1.x、官网 404、社区停摆。它没流行的根因是生态与背书劣势：Thrift 出厂即带十余种语言代码生成器、Protobuf 有 Google 背书，而 BERT-RPC 仅靠 GitHub 一家自用、缺跨语言工具链。哲学最接近它的 MessagePack-RPC 反而占据了「轻量无 schema」生态位并存活至今。

### 生态定位

一个「时代标本」——动态语言反 IDL 哲学的优雅极简实现，证明了「9 行起一个 RPC 服务」可行，但也印证了大规模分布式系统最终选择了类型安全与工具链。今天的价值是「学习样本」而非「生产选型」。

## 套利机会分析

- **信息差**：无功能/工具型套利空间（协议已淘汰、库已停更）。价值在「历史叙事 + 作者声望 + 协议设计哲学」——典型的「故事型/教育型」选题，而非「能用型」选题。
- **技术借鉴**：链式 method_missing DSL、远端异常透明重建、select(2) 可靠超时、长度前缀分帧四套范式仍可直接迁移到今天的任何 RPC/HTTP 客户端 SDK。
- **生态位**：它当年填补了「动态语言 + 无 IDL 二进制 RPC」的空白，但这个生态位后来被 MessagePack-RPC 继承、被 gRPC 从上方覆盖。
- **趋势判断**：负向——协议已消亡，无后发优势可言；它的意义是反向的，提醒后来者「正确的简洁哲学也可能输给错误的生态时机」。

## 风险与不足

- **协议已死、库已停更**：BERT-RPC 规范止步 1.x、官网 404、近 12 年 0 提交，不可用于新项目生产选型。
- **无类型安全与工具链**：运行时动态分发意味着拼错函数名只能运行时炸、IDE 无补全、与同名 Ruby 方法有潜在冲突。
- **传输能力有限**：单连接一问一答、读完即关，无多路复用/无流式，单消息上限 4GB。
- **依赖外部 bert gem**：序列化命门外包，正确性受其制约（如历史上的 utf-8 协同问题）。
- **commit 自动分类失真**：fix/refactor 为 0、other 占 86%，并非真没修 bug，而是 2009 年提交不写规范化前缀——分析时已以 monthly_distribution + 核心文件改动为主依据。

## 行动建议

- **如果你要用它**：不建议用于生产（协议已淘汰）。需要动态语言 + 无 schema 的轻量 RPC，选其哲学继承者 MessagePack-RPC；需要大规模强类型服务网格，选 gRPC/Protobuf。
- **如果你要学它**：591 行可一个下午通读。重点看 `lib/bertrpc/action.rb`（全库最重的 106 行，含帧协议 + select(2) 超时 + 非阻塞 connect + 远端异常重建）、`request.rb` + `mod.rb`（method_missing 链式 DSL）、`errors.rb`（协议级别 → 异常类映射）。
- **如果你要 fork 它**：链式 method_missing Façade、远端异常透明重建、可靠超时三连是可独立抽取的工程资产，可移植进现代 SDK；协议本身无需复活。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [deepwiki.com/mojombo/bertrpc](https://deepwiki.com/mojombo/bertrpc)（已收录）|
| Zread.ai | [zread.ai/mojombo/bertrpc](https://zread.ai/mojombo/bertrpc)（已收录）|
| 协议规范 | BERT and BERT-RPC 1.0 Specification（原站 bert-rpc.org 已 404，可参考 Feuerlabs/bert 镜像）；官博 [Introducing BERT and BERT-RPC (2009)](https://github.blog/2009-10-20-introducing-bert-and-bert-rpc/) |
| 关联论文 | 无（注意：与 NLP 的「BERT」模型同名但完全无关）|
| 在线 Demo | 无 |

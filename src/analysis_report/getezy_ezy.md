# 接班 BloomRPC 的 ezy 也死了：单人 gRPC 客户端为何困在 v1.0.0-beta.16

> GitHub: https://github.com/getezy/ezy

## 一句话总结

一位莫斯科开发者单枪匹马写的桌面 gRPC/gRPC-Web GUI 客户端，立志接替已弃坑的 BloomRPC、把 Postman 式工作流带到 gRPC，却因「不支持服务端反射」的架构债、中心化状态导致的性能卡顿，和单人难补「最后 20%」的产能透支，在 9 个月密集冲刺后停在 `v1.0.0-beta.16`、从未发布正式版，最终与它想接班的 BloomRPC 一同走向废弃。

## 值得关注的理由

1. **一个罕见完整的「开源工具死亡解剖」样本**：ezy 不是因为代码差而死——它有干净的三层进程隔离架构、专业的跨平台 CI/签名/公证流水线、可独立成库的 `src/core` 内核。它死于更隐蔽的原因：架构早期定型为「只认 .proto 文件」，让最关键的竞争力（server reflection）无处落脚；中心化状态设计让性能 bug 无法不重构地修复。这是「技术债如何在表面繁荣下慢慢勒死一个单人项目」的教科书案例。
2. **赛道演替的活化石**：BloomRPC（死）→ ezy（想接班，也死）→ Kreya（闭源正统继任）/ Postman·Insomnia（巨头下沉补齐 gRPC）/ Yaak（Rust 新锐）。看 ezy 就看懂了独立 gRPC GUI 工具被「大厂顺手支持」逐步绞杀的全过程。
3. **可直接抄走的 Electron 工程模式**：把 Node 流跨 IPC 桥接到渲染进程、为 Electron 主进程注入自定义 TLS 的 gRPC-Web transport、zustand persist 接 electron-store——这些模式与「项目是否还活着」无关，是任何 Electron 桌面应用能直接复用的真东西。

## 项目展示

![ezy logo](https://raw.githubusercontent.com/getezy/ezy/master/docs/logo.png)

> ezy 项目 logo。

![ezy preview](https://raw.githubusercontent.com/getezy/ezy/master/docs/preview.gif)

> 产品操作演示：导入 proto → 浏览 service/method → 填 JSON 请求体 → 调用 → 看格式化响应。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/getezy/ezy |
| Star / Fork | 1,041 / 21 |
| 代码行数 | 真实源码约 9,700 行（TSX 5,236 + TypeScript 4,473）；总 83,083 行被 package-lock 等 JSON 拉高（JSON 占 87.5%），勿误读 |
| 项目年龄 | 49 个月（但活跃期仅 2022-04 ~ 2023-01 约 9 个月）|
| 开发阶段 | 已放弃（最后 commit 2023-01-23，近一年 0 提交）|
| 贡献模式 | 单人主导（notmedia / Alexey Vasyukov，贡献占比 100%，525 commit）|
| 热度定位 | 中等热度 · 停滞（约 2-7 star/月长尾滴入，来自「BloomRPC alternative」搜索）|
| 质量评级 | 代码[良好] 文档[一般] 测试[不足，仅 src/core 有单测] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

真实开发者是单人 **Alexey Vasyukov（notmedia，莫斯科）**——一位 11 年账号的资深全栈 JS/TS 开发者。技术轨迹清晰可见：早期做 Cordova 移动广告插件（AdColony/Chartboost，2017）、Outline VPN 的 Ansible 部署脚本，近年深耕 NestJS 生态 + gRPC。仓库挂在 `getezy` 组织下做产品化包装（独立 logo、Discord、域名式 bundleId `com.getezy.ezy`、苹果开发者签名 `Alexey Vasyukov`），但本质是单人项目。社交曝光低（20 粉丝），ezy 是其唯一获得社区关注的作品。

### 问题判断

典型的**工程实践沉淀 + dogfooding**：作者日常对接 gRPC 后端，而 gRPC 是二进制协议（protobuf over HTTP/2），无法像 REST 那样用 curl/Postman 直接手搓请求。时机上他踩在一个真实窗口期——「BloomRPC 刚弃坑、Kreya 尚未完全统治、Postman 还没原生支持 gRPC」的 2022 年，这正是接班 BloomRPC 的最佳时点。差异化卖点是真实的：相对只支持原生 gRPC 的 BloomRPC，ezy **同时支持原生 gRPC 与 gRPC-Web**。

### 解法哲学

偏向**功能完整 + 体验现代化**，而非 Unix 式小而美。单人项目却铺开了 Electron 跨平台、双协议、TLS/mTLS（含自签名/双向证书）、4 种流式、⌘+K 命令面板、明暗主题、collections/environments/tabs 全量持久化、Storybook——明显在「对标 Postman 的完成度」。这个选择埋下了致命隐患：**表面铺得太宽，深度（reflection、性能、自动更新）没跟上**。还有一个关键的「主动不做」——坚持「手动导入 .proto 文件」、不做服务端反射，这个早期架构决定后来变成了无法翻越的墙。

### 战略意图

这是作者唯一的对外招牌项目，README 的 Sponsorship 段落写明「有改善 gRPC 开发体验的想法，欢迎赞助/合作」，透露出 open-core / 商业化探索的意图而非纯爱好项目。但产能现实是单人 100% 贡献，最终没能撑过从 beta 到正式版的「最后一公里」。

## 核心价值提炼

### 创新之处

1. **Vendored `NodeHttpTransport`：为在 Electron 主进程跑 gRPC-Web 而注入 TLS 证书**（新颖度 4/5）：package.json 装了官方 `@improbable-eng/grpc-web-node-http-transport`，但代码完全弃用，自己实现了一份 `grpc.Transport`——因为官方版无法传 `https.RequestOptions`（CA / 客户端证书 / key）。自写版把 `httpsOptions` 透传进 `https.request`，让 gRPC-Web 也能做服务端/双向 TLS（含自签名证书），这是 README 能勾选「gRPC-Web ✅ TLS」的真正底层支撑。
2. **`GrpcWebCallStream`：把回调式 invoke 适配成 Node EventEmitter**（新颖度 3/5）：improbable-eng 的 `grpc.invoke` 是 `onMessage/onHeaders/onEnd` 回调风格，ezy 用继承 `EventEmitter` 的类包起来对外发 `message/headers/error/end` 事件。这让 gRPC-Web 流能与原生 gRPC 的 `ClientReadableStream`（同为 EventEmitter）用同一套桥接代码处理，是「双协议结构对称」得以成立的关键胶水。
3. **类型级 TLS 配置判别联合 + 类型守卫**（新颖度 3/5，可迁移性 5/5）：`GrpcTlsConfig<T extends GrpcTlsType>` 用条件类型按 `INSECURE/SERVER_SIDE/MUTUAL` 映射到不同配置结构，配类型守卫在凭证构造处收窄类型，原生 gRPC 和 gRPC-Web 两侧共用同一套 TLS 类型——「按 mode 字段决定其余必填字段」的 discriminated union 优雅用法。

### 可复用的模式与技巧

- **Electron 流跨进程桥接（nanoid + Map + 多频道 + 按 id 过滤监听）**：主进程把真实 stream 存进 `Map<nanoid, stream>` 并把 id 返回渲染进程，stream 的 data/error/end 事件经 `webContents.send(channel, id, payload)` 推回，渲染进程按 id 过滤监听并统一清理——任何需要把主进程长生命周期/流式对象暴露给渲染层的 Electron 应用都适用。
- **`@core` 纯逻辑内核 + 进程层薄包装**：把可独立成库的领域逻辑（零 UI/Electron 依赖、独立单测）抽到 `src/core`，main/renderer 只做 IPC/UI 适配。
- **zustand `persist` 接 electron-store 适配器**：自定义 `getStorage` 把持久化后端从 localStorage 换成 IPC 代理的磁盘存储（但注意全量写盘的性能代价，见下）。
- **回调式 SDK → EventEmitter 适配器**：用强类型 `on()` 重载把第三方回调流归一成 Node 事件流，统一上层处理代码。

### 关键设计决策

| 决策 | 解决的问题 | Trade-off | 可迁移性 |
|------|-----------|-----------|---------|
| gRPC 调用层整体放主进程，渲染进程只通过 IPC 驱动 | `@grpc/grpc-js` 依赖 Node net/http2/fs，contextIsolation 下渲染进程不该碰 Node | 多一次 IPC 序列化往返 + 流要跨进程桥接，换安全边界清晰 + 全套 Node gRPC 能力 | 高 |
| 双协议靠「结构对称 + 渲染层三元选择」统一，无共享接口 | 原生 gRPC 与 gRPC-Web 是两套实现，但 UI 想无差别调用 | 靠 duck typing 维持对称、编译期无法保证一致，且 gRPC-Web 对称是残缺的（仅 unary + server-streaming）| 中（反面：缺接口约束）|
| proto 走「文件路径 + includeDirs」加载，每次调用重新解析 | 把 .proto 变成可调用 service 定义 | 实现简单，但**整条链路硬编码为「文件来源」、无「描述符来源」抽象**——这正是 server reflection（#16）无处落脚、始终未实现的根因 | 中（反面参考）|
| zustand persist + electron-store 全量持久化 | collections/tabs/environments 跨重启保留 | 写法极简、自动落盘，但**每次状态变更都全量序列化经 IPC 写盘**——这是性能 bug #37 的根源 | 高（但需注意性能代价）|

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | ezy | Kreya | grpcui/grpcurl | Postman/Insomnia |
|------|-----|-------|----------------|------------------|
| 形态 | 桌面 GUI（Electron）| 桌面 GUI（闭源）| 浏览器/CLI | 全协议平台 |
| Server Reflection | ❌（缺失，#16 未解决）| ✅ | ✅ | ✅ |
| gRPC-Web | ✅ 一等支持 | 部分 | ❌ | 部分 |
| 开源/免费 | ✅ MPL-2.0 免费 | 闭源、部分付费 | ✅ | 免费有云墙 |
| 维护状态 | 已放弃 | 活跃 | 活跃 | 活跃 |
| 定位 | gRPC 垂直工具 | BloomRPC 正统继任 | 即用即走/脚本 | 顺手支持 gRPC |

### 差异化护城河

几乎只剩「开源 + 免费 + gRPC-Web 一等支持 + 干净可复用的 src/core 内核」。**没有技术护城河**——核心调用全建立在公开的 `@grpc/*` / improbable-eng 之上，唯一原创的 TLS transport 也是百行可复制代码。

### 竞争风险

最致命的短板是**缺 server reflection**（#16）：主流竞品（Kreya/grpcui/Postman）都支持「连上服务自动发现接口」，而 ezy 要求用户手动导入 .proto，主工作流凭空多一道摩擦。叠加 Postman/Insomnia「顺手就支持 gRPC」直接侵蚀独立工具的存在理由——ezy 当年入场时尚有 BloomRPC 弃坑留下的窗口，如今窗口已彻底关闭。

### 生态定位

BloomRPC 之后短暂的「开源免费桌面 gRPC 客户端」候选之一，但在 reflection 缺失 + 单人停摆 + 大厂工具下沉的三重夹击下，已与 BloomRPC 一同走向事实上的废弃。

## 套利机会分析

- **信息差**：不属于「被低估的潜力股」。它是「质量尚可但已被作者放弃」的项目——停在 beta.16、近 3 年 0 commit、核心痛点 issue 悬而未决。价值不在「采用」，而在「解剖」。
- **技术借鉴**：Electron 流跨进程桥接、自定义 TLS 的 gRPC-Web transport、zustand 接 electron-store、回调流归一为 EventEmitter——这些是与项目存亡无关的可复用工程模式。`src/core` 甚至具备直接发布成独立 npm 包的一切条件（零 UI/Electron 依赖、独立单测），只是从未被抽出。
- **生态位**：它当年想填补 BloomRPC 弃坑的空白，但这个生态位的主流已是 Kreya（闭源继任）与 Postman/Insomnia（巨头下沉）。
- **趋势判断**：方向上「桌面 gRPC GUI」需求真实存在，但被大厂全协议平台和闭源专精工具两头夹击，独立开源单品的生存空间持续收窄。ezy 是这一趋势的牺牲品而非赢家。

## 风险与不足

- **已停摆 3 年、不可作生产工具**：缺 server reflection、有未修的性能卡顿 bug（#37）、停在 beta.16 从未转正。要用 gRPC GUI 请选 Kreya / Postman / Insomnia / Yaak。
- **架构债无法不重构地修复**：file-only 的 proto 描述符设计让 reflection 无处落脚；中心化 persist 状态让性能 bug 修复必须动核心。
- **测试纪律严重缺失**：jest 仅覆盖 `src/core`（3 个 spec），整个主进程 IPC 层 + 整个 React 渲染层零测试（Test 0.5% / Refactor 0%），这是它难以从 beta 走向正式版的工程隐患之一。
- **单人产能透支**：表面完成度极高（跨平台 + 双协议 + TLS/mTLS + 4 流式 + 命令面板），但「最后 20%」需要的恰是 reflection/refactor 这类高门槛投入，单人难以为继。

## 行动建议

- **如果你要用它**：不建议作为生产工具。需要 gRPC GUI 调试，选 Kreya（功能全、支持 reflection）、Postman/Insomnia（已原生支持 gRPC）、或 Yaak（轻量新锐）；只要 CI/脚本场景用 grpcurl。
- **如果你要学它**：重点读 `src/core/clients/grpc/grpc-web-client/http.transport.ts`（自定义 TLS transport）、`src/main/clients/grpc-client/subscribers/server-streaming.subscriber.ts`（Node 流跨 IPC 桥接）、`src/app/storage/*.storage.ts`（zustand persist 接 electron-store）、`src/core`（可独立成库的纯内核）。这是一份高质量的 Electron + TypeScript + gRPC 架构教学样本。
- **如果你要 fork 它**：最有价值的两件事——(1) 把 `src/core` 抽成独立 npm 包；(2) 在 proto 加载链路里凿一个「描述符来源」抽象层，补上 server reflection（#16），这正是它当年最该做却没做到的事。性能上则把 CodeMirror 编辑器输入与持久化 store 解耦（本地 state + debounce 落盘）。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/getezy/ezy（已收录，含 Architecture / State Management 章节）|
| Zread.ai | 未验证（返回 403）|
| 关联论文 | 无（工程工具，非研究项目）|
| 在线 Demo | 无（桌面应用，从 getezy.dev 或 GitHub Releases 下载，最新仅 v1.0.0-beta.16）|
| 作者自述 | [ezy - desktop gRPC client（DEV）](https://dev.to/notmedia/ezy-desktop-grpc-client-113o) |
| 赛道背景 | [Kreya: BloomRPC just got deprecated](https://kreya.app/blog/bloomrpc-deprecated/) |

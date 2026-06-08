# 620 万行的 Telegram iOS，只 1/4 是自己写的

> GitHub: https://github.com/TelegramMessenger/Telegram-iOS

## 一句话总结

这是月活 10 亿+ 的 Telegram 官方 iOS 客户端完整源码——GitHub 上最大、最受审视的移动端代码库之一（620 万行、2.1 万文件）；但反直觉的是，这 620 万行里 Telegram 团队真正用 Swift 手写的应用层只占约 1/4，其余近七成是为「自带电池、可复现编译」而整建制纳入仓库的 vendored 原生第三方库。

## 值得关注的理由

- **工程价值被严重低估的巨型样本**：作为产品 Telegram 名气满格，但作为「工程参考代码库」几乎无人系统拆解——千模块 Bazel 极致组件化、自研异步 UI 渲染、Swift/C/C++/汇编深度混编、MTProto 协议、十亿级实时通讯架构，是大型 iOS 工程的金矿。超高 fork 率 ~30%（2621 forks）印证大量开发者 fork 来自建/研究。
- **可复现构建是「可验证信任」的基石**：Telegram 提供构建说明，让用户能独立验证 App Store 上的二进制确由这份公开源码编译而来——对一个密通讯应用，这是「可验证而非盲信」的核心承诺（尽管 iOS 端验证门槛极高）。
- **一个值得客观看待的隐私样本**：它常被误以为「默认端到端加密」，实际只有手动开启的「Secret Chats」是 E2E、普通云聊天服务器可访问明文；MTProto 自研协议受密码学界争议。读它能同时看懂顶级工程与「开源 ≠ 默认 E2E」的真相。

## 项目展示

> README 是纯文本编译指南，仓库无展示性截图/架构图。产品「活体 Demo」即 Telegram App 本体（App Store / telegram.org）。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/TelegramMessenger/Telegram-iOS |
| Star / Fork | 8586 / 2621（~30% 超高 fork 率，大量自建/研究/换皮；star 对 10 亿用户级应用其实偏低，只来自开发者） |
| 代码行数 | 620 万行 / 21456 文件（Swift 应用层 ~155 万行/25% + C/C++/汇编/HEX 原生底座 ~70% 为 vendored 库） |
| 项目年龄 | 公开镜像仓约 91 个月（2018-11 起；app 实际自 2013 年） |
| 开发阶段 | 活跃开发（批量镜像同步：平时静默、发版时大推；近 52 周 880 commit，「近 4 周 0」是发布节奏非停更） |
| 贡献模式 | 首席主导 + 全职团队 + 社区（339 人；Ilya Laktyushin 独占 7952/~26%） |
| 热度定位 | 大众热门产品 + 工程价值被严重低估的巨型代码库 |
| 质量评级 | 代码[优·工业级超大规模] 文档[弱·README 仅编译指南] 测试[有·Tests 目录，但比例低] |
| License | **GPL-2.0-or-later**（可 fork/改/学，但自建须自申 api_id、不得叫 Telegram、不得用官方 logo、须公开修改——「能 fork 不能简单换皮上架」） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

org TelegramMessenger，背后是 Telegram（Pavel Durov & Nikolai Durov 兄弟创立，月活 10 亿+）。这不是社区协作型开源，而是**商业公司把内部私有仓按 App Store 发版周期批量同步到公开仓**的「窗口式开源」。核心工程由极少数资深 iOS 专家把控——首席工程师 **Ilya Laktyushin（laktyushin）独占约 1/4 的 3 万 commit**，其后包括 **Scott Goodson（appleguy，AsyncDisplayKit/Texture 异步渲染框架作者）**。工程一致性与专业度极高。

### 问题判断

对一个主打「抗审查、可信」的密通讯应用，**光说自己安全没用，得让人能验证**。Telegram 的判断是：把官方客户端完整开源 + 提供可复现构建，让安全研究者能独立确认「App Store 上跑的二进制 = 这份公开源码」，把信任从「相信我们」变成「你可以验证」。同时开源也让生态开发者能基于 MTProto/API 自建客户端。但它选择了与 Signal 不同的产品路线：**功能丰富度与流畅体验优先**（云同步、超大群、频道、Bot、Mini Apps、贴纸），代价是普通云聊天默认非 E2E。

### 解法哲学

- **明确选择「可验证而非盲信」**：开源 + 可复现构建。
- **明确选择功能/体验优先于默认 E2E**：云端可同步多设备、超大群频道——这要求服务器可访问消息，故默认非 E2E（只 Secret Chats E2E）。
- **明确选择自研 MTProto 协议**：而非采用经学界验证的 Signal 协议（争议来源）。
- **明确选择千模块 Bazel 极致组件化 + 自研异步渲染**：换取增量编译与 60fps 流畅，代价是重型工具链与无障碍适配难。
- **明确选择 GPL-2.0 + fork 约束**：开放代码但用 api_id/商标约束防止简单换皮滥用。

### 战略意图

Telegram 的商业模式是 Telegram Premium 订阅 + Sponsored Messages 广告 + TON 区块链生态 + Mini Apps 平台（2024 初首次盈利）。开源客户端服务于「可信」品牌与生态扩张。需客观记录的背景：**2024-08 Pavel Durov 在法国被捕、受 12 项指控**（内容审核缺位等），随后 Telegram 调整政策、开始向持合法搜查令的执法机构提供用户 IP/手机号——一个以「抗审查」立身的平台的治理转向（2025-11 法国解除其旅行禁令）。

## 核心价值提炼

### 创新之处

1. **千模块 Bazel 极致组件化**（最突出工程特征）：把整个 App 拆成数百近千个可独立编译/复用的 Bazel 模块（273 顶层 submodule、794 BUILD target；AccountContext/ChatListUI/ChatMessage*/Camera/BrowserUI/BotPaymentsUI/AnimatedStickerNode…），换取增量编译速度、关注点分离与组件复用。
2. **自带电池的可复现构建**：把几十个原生第三方库（boringssl/ffmpeg/dav1d/libvpx/openh264/webp/opus/webrtc/td…）整建制 vendored 进仓，配合锁定 Xcode 版本，实现「编译产物可比对 App Store 二进制」。
3. **自研异步 UI 渲染（AsyncDisplayKit/Display）**：放弃标准 UIKit、用异步渲染框架实现海量消息列表的 60fps 流畅滚动。
4. **核心栈分层**：MtProtoKit（协议）+ TelegramCore（业务，正进行 Postbox→TelegramEngine 重构）+ Postbox（本地 DB）+ TelegramUI（最大 UI 聚合）+ Display/AsyncDisplayKit（渲染）。

### 可复用的模式与技巧

1. **极致模块化的物理边界**：用「每个组件一个独立编译模块」的目录边界（而非注释/约定）表达关注点分离——超大团队/超大应用的组织范本。
2. **vendored + 可复现构建**：把依赖整建制纳入仓库 + 锁工具链版本，换取可验证、可离线、不受上游漂移影响。
3. **自研异步渲染换流畅**：性能极致场景下绕开标准 UI 框架的取舍（代价见无障碍适配）。
4. **类型即文档**：强 Swift 类型 + 千模块物理隔离，低注释率下仍可维护。

### 关键设计决策

- **620 万行 ≈ 155 万 Swift 应用 + ~440 万 vendored 原生**：理解规模时务必区分「团队手写」与「为可复现编译纳入的第三方库」——HEX 9.7% + 汇编 8.6% 几乎全来自编解码/加密库的手写汇编优化。
- **窗口式开源**：公开仓是内部私有仓的发版镜像，「近 4 周 0 commit」是同步节奏假象，背后近 52 周 880 commit 的高强度开发。
- **性能 vs 无障碍**：自研异步渲染换来流畅，但导致 VoiceOver/无障碍长期适配困难（issue #267，145 评论）。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | Telegram | Signal | WhatsApp | Element/Matrix |
|------|----------|--------|----------|----------------|
| 客户端开源 | ✓ GPL-2.0 + 可复现 | ✓（默认 E2E） | ✗ 闭源 | ✓ 去中心化 |
| 默认 E2E | ✗（仅 Secret Chats） | ✓ 全程默认 | ✓ 默认 | ✓ |
| 协议 | 自研 MTProto（受争议） | Signal 协议（学界验证） | Signal 协议 | Matrix |
| 功能丰富 | 极丰富（云同步/频道/Bot/Mini Apps） | 克制 | 中 | 中 |
| 用户量 | 10 亿+ | ~1 亿级 | 20 亿+ | 小 |
| 定位 | 功能/体验优先 | 隐私优先 | 大众默认 E2E | 联邦去中心化 |

### 差异化护城河

护城河 =「**功能最丰富 + 体验极致流畅 + 客户端开源可复现 + 10 亿用户网络效应**」。它与 Signal 构成「易用/功能 vs 隐私/默认 E2E」的经典两极。但其隐私叙事因「默认非 E2E + MTProto 争议 + Durov 被捕后政策转向」而需打折。

### 竞争风险

- **隐私叙事被持续质疑**：Signal 阵营与密码学界长期批评其非默认 E2E 与自研协议；政策转向（向执法提供数据）进一步动摇「抗审查」形象。
- **闭源巨头的默认 E2E**：WhatsApp 默认 E2E + 20 亿用户是市场最大对手。
- **自建门槛 + 无障碍债**：Bazel 全包构建劝退贡献者，自研渲染致无障碍长期落后。
- **治理/监管风险**：Durov 案与各国监管对其影响持续。

### 生态定位

它是「功能丰富 + 流畅 + 客户端开源可复现」的国民级密通讯客户端，在隐私光谱上处于 Signal（隐私极致）与 WhatsApp（闭源大众）之间，同时是一份极稀缺的工业级超大规模 iOS 工程参考。

## 套利机会分析

- **信息差**：产品不存在被低估，但「工程参考代码库」被严重低估——620 万行巨型客户端几乎无人系统拆解，是优质选题洼地（聚焦某子系统如 MTProto/渲染层而非通读）。
- **技术借鉴**：「千模块物理边界组件化」「vendored + 可复现构建」「自研异步渲染换流畅」可迁移到任何超大应用工程。
- **生态位**：想验证官方 App 可信、想基于 MTProto 自建客户端、想学超大 iOS 工程的人，这是顶级样本。
- **趋势判断**：开源 + 可复现构建是密通讯「可验证信任」的趋势方向；但 Telegram 的隐私叙事与治理转向是需客观跟踪的变量。

## 风险与不足

- **⚠️ 隐私的客观真相（必须正视）**：Telegram **默认不是端到端加密**——只有手动开启的 Secret Chats 是 E2E，普通云聊天为客户端-服务器加密、服务器可访问明文；自研 MTProto 缺乏 Signal 协议那样的学界形式化验证（见「Four Attacks and a Proof for Telegram」IEEE S&P 2022）。不可包装成「纯粹隐私英雄」。
- **620 万行的认知陷阱**：约 70% 是 vendored 原生库，团队手写 Swift 仅 ~1/4，评估规模/工作量勿混淆。
- **自建门槛极高**：Bazel 全包构建 + 上千模块，编译问题反复出现（issue #219/#333）。
- **无障碍长期落后**：自研异步渲染的代价（VoiceOver 适配难）。
- **治理/政策风险**：Durov 案后向执法提供数据的政策转向。
- **文档薄**：README 仅编译指南，架构需读码。

## 行动建议

- **如果你要用它（作为用户）**：你要功能丰富、体验流畅、客户端可验证的通讯应用——Telegram 是优选；但若你的核心诉求是**默认端到端加密与隐私极致**，应选 Signal，或在 Telegram 里坚持用 Secret Chats。
- **如果你要学它**：聚焦而非通读。重点读 `submodules/MtProtoKit`（MTProto 协议栈）、`submodules/TelegramCore`（业务逻辑 + Postbox→TelegramEngine 重构）、`submodules/Postbox`（本地数据库）、`submodules/Display` + vendored `AsyncDisplayKit`（异步渲染），以及 `MODULE.bazel`/`Make.py`（千模块 Bazel 构建）。是超大 iOS 工程与可复现构建的顶级样本。
- **如果你要 fork 它**：注意 GPL-2.0 + 必须自申 api_id、不得用 Telegram 商标/官方 API 滥用、须公开修改；自建编译门槛高（Bazel 全包）。最有价值的方向是研究其模块化/渲染架构，而非简单换皮。

### 知识入口

| 资源 | 链接 |
|------|------|
| 可复现构建 | https://core.telegram.org/reproducible-builds |
| MTProto / API | https://core.telegram.org/mtproto ｜ https://core.telegram.org/api/end-to-end |
| 关联论文 | 「Four Attacks and a Proof for Telegram」(Albrecht 等, IEEE S&P 2022, MTProto 密码分析) |
| 竞品对照 | [signalapp/Signal-iOS](https://github.com/signalapp/Signal-iOS)（开源默认 E2E 标杆） |
| 背景 | [Pavel Durov 被捕与指控（Wikipedia）](https://en.wikipedia.org/wiki/Arrest_and_indictment_of_Pavel_Durov) ｜ [Telegram 隐私争议（ESET）](https://www.eset.com/blog/en/home-topics/privacy-and-identity-protection/telegram-privacy-explained/) |

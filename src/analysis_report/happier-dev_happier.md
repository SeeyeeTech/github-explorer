# GitHub推荐：1.4k stars 却写 290 万行：把 6 个 AI 编码 agent 装进端到端加密的多端「中继」

> GitHub: https://github.com/happier-dev/happier

## 一句话总结

Happier 是一个**端到端加密、跨设备、自托管的 AI 编码 agent 中继客户端**——把你的 Claude Code / Codex / OpenCode / Cursor / Pi 等 CLI 会话安全地同步到手机、Web、桌面，并在路上继续它们。

## 值得关注的理由

1. **Agent 世界的 1Password + Tailscale**：在「你的 AI 编码数据比源码还敏感」这件事上，它是目前最系统化做端到端加密 + 零知识中继 + 自托管的开源方案，已经在 App Store 上架并拥有真实的桌面/移动/Web 三端用户。
2. **Provider 抽象层的工程范式**：它把 Claude Code、Codex、OpenCode、Cursor、Pi 等 6+ 个「长得不一样」的 agent 装到同一套协议 + UI 上，提供了一个多 provider adapter 框架的范本（manifest-driven + 三档分级 + tool normalization）。
3. **被低估的潜力股**：13 个月、290 万行代码、700+ tag、几乎全职团队节奏，仅 1.4k star；处于 vibe-coding 工具链风口，但热度远低于同类项目，是典型的「代码体量 vs 关注度」倒挂。

## 项目展示

![Happier Dev](https://raw.githubusercontent.com/happier-dev/happier/dev/apps/website/public/images/logotype-dark.png) — hero：项目 logo，「Mobile, Web and Desktop client for Claude Code, Codex, OpenCode, Pi, Cursor」

![Happier 移动端 UI](https://raw.githubusercontent.com/happier-dev/happier/dev/.github/mobile-2000.png) — 移动端 UI：手机继续同一段 AI 编码会话（核心卖点）

![Happier 桌面端 UI](https://raw.githubusercontent.com/happier-dev/happier/dev/.github/desktop-2000.png) — 桌面端 UI：本地 + 远程的统一会话入口

![支持的 AI provider](https://raw.githubusercontent.com/happier-dev/happier/dev/.github/supported-ai-providers.png) — 多 agent provider 总览：Claude Code / Codex / OpenCode / Cursor / Gemini / Pi / Kilo 等

![Happier Sessions](https://happier.dev/images/screens/sessions.svg) — 官网 demo：跨端共享的 session 列表视图

> 官网视频：<https://happier.dev>（产品定位说明 + 安装引导）

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/happier-dev/happier |
| Star / Fork | 1,445 / 122 / 10 |
| Watcher / Open Issues / PR | 10 / 31 / 11 |
| 代码行数 | 2,909,756 行（17,663 文件） |
| 语言分布 | TypeScript 70.7% / TSX 18.6% / JavaScript 8.1% / Rust 0.2% / Swift <0.1% |
| License | MIT License |
| 项目年龄 | 12.9 个月（首 commit 2025-07-12，仍在频繁 push） |
| 默认分支 | `dev`（trunk-based，`main` 仅稳定） |
| 开发阶段 | **密集开发**（近 30 天 791 commit、近 90 天 1,514） |
| 开发模式 | **职业项目**（周末 34.5%、深夜 24.3%） |
| 贡献模式 | **单人主导 + 小核心团队 + 社区协作**（75 贡献者，Top 1 占 81.3%） |
| 热度定位 | **被低估的潜力股**（2.9M 行 / 728 tag / 6+ agent 兼容，仅 1.4k star） |
| 质量评级 | 代码[良好] 文档[优秀] 测试[充分] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

- 组织名 **Happier Devs**，瑞士注册，账号 2026-01-31 创建（仅 0.5 年龄，但已发 728 tag / 8,691 commits；明显是为此项目专门成立的基金会型账号）。
- **主开发者 `leeroybrun`**：承担 81.3% 的提交量；另有核心成员 `ex3ndr`（748 commit）、`bra1nDump`（277）、`ahundt`（249），组成 4-5 人的小核心团队。
- 项目源自上游 [Happy](https://github.com/slopus/happy)（现已改名 Happier-AI/happier）。README 「Why Happier」明确写：原作者是上游贡献者，但「自己想要的速度」超出了主项目的舒适区，于是 fork 出来**为自己做**，做完再公开——典型 dogfooding 驱动的加速迭代。
- 瑞士注册 + TweetNaCl/Signal 同源加密 + 「zero-knowledge relay」叙事 → 隐私/开发者工具方向的独立创业小团队。

### 问题判断

作者看到的问题不是「需要另一个 agent」，而是：

> AI 编码 agent 的「会话」比传统 SSH 还敏感——它包含了你正在编辑的代码、调用过的工具、批准过的命令、未提交的草稿。Anthropic / OpenAI 的官方云端同步把这些数据留在厂商侧；现有的 IDE 类替代品又是「替换你的工具」，而不是「把现有工具搬上多设备」。

时机为什么是现在：

- 2025 年中开始，Claude Code、Codex、OpenCode、Pi、Gemini CLI 等主流 agent 都已稳定提供「可观察 transcript + 权限询问 + 会话恢复」能力——意味着**「统一的中间层」机会窗口已经打开**。
- 开发者对「多设备 + 隐私 + 团队分享 AI 工作流」的需求刚浮现，但厂商解决方案要么侵入性太强（厂商云同步），要么完全没有。

### 解法哲学

- **不是另一个 IDE，也不是另一个 agent，而是套在现有 CLI 上的中间层**：价值主张是「在现有 CLI 旁边，而不是替换它」。
- **多 provider 一等公民**优先于单 provider 的深度打磨——Claude Code / Codex / OpenCode / Cursor / Pi / Kilo / Kimi / Qwen / Auggie / Kiro / Copilot 一视同仁。
- **端到端加密 + 自托管是地基而非补丁**：服务端永远拿到 opaque blob，DEK 永远在客户端。
- **协议极简、稳定性优先**：单 `GET/POST/DELETE` + Socket.IO 上两类事件（`update` 持久 / `ephemeral` 临时）+ monotonic `seq` 做 client reconciliation；不用 CRDT，不做协议大一统。
- **明确选择不做什么**：不做自己的模型、不做 IDE、不做云端 SaaS 主线（自托管 + 加密 cloud 是同等推荐）、不做「开放协议」（`@happier-dev/protocol` 是**共享 schema** 而不是要求外部实现的开放协议）。

### 战略意图

- **Open-core 的 SaaS 化路径**：核心产品永远 MIT 开源；企业特性（GitHub OAuth / OIDC / mTLS / keyless external auth）、托管 Happier Cloud、Voice（RevenueCat / ElevenLabs）是商业化层。
- **核心基础设施定位**：稳定同步 + 多 agent 兼容是护城河；所有上层特性（Voice、Subagents、Agent Teams、Pending Queue、Inbox）都建立在「多设备 + 多 agent + E2EE」这层上。
- **Open development + 维护者最终裁决权**：三段式分支 `dev` (整合) → `preview` (RC) → `main` (稳定)；AGENTS.md tier-0 invariant 第 1 条禁止 agent 切分支——**反 AI agent 失控**的工程纪律。

## 核心价值提炼

### 创新之处

| 创新点 | 新颖度 | 实用性 | 可迁移性 |
|---|---|---|---|
| **统一 envelope `{ t: 'encrypted', c }` / `{ t: 'plain', v }` 显式解析** | 3/5 | 5/5 | 5/5 |
| **V2 tool normalization + `_happier.canonicalToolName` + 永远保留 `_raw` + trace 驱动 fixture** | 4/5 | 5/5 | 4/5 |
| **Provider 三档分类 manifest：native / bespoke ACP / catalog+hook** | 4/5 | 5/5 | 4/5 |
| **Session Handoff 多阶段协议（plan → transfer_blobs → stage → apply → import → finalize）** | 5/5 | 4/5 | 3/5 |
| **Per-account monotonic `seq` + entity 级乐观并发版本号双层** | 3/5 | 5/5 | 5/5 |
| **ActivityCache + 10-min timeout loop 分离持久/临时事件** | 3/5 | 5/5 | 5/5 |
| **TypeScript 7 (`@typescript/native`) + TS 5.9 双版本共存（compiler-API 消费者）** | 4/5 | 4/5 | 3/5 |
| **Tool tracing + fixture drift regression suite（`HAPPIER_STACK_TOOL_TRACE=1`）** | 4/5 | 5/5 | 5/5 |

> 排序逻辑：实用性 × 可迁移性优先，同等条件下新颖度打破平局。

### 可复用的模式与技巧

1. **Envelope discriminated union（`{ t: 'encrypted', c }` / `{ t: 'plain', v }`）+ 显式 mode/policy 校验**——「内容是什么」+「服务端能不能接受它」在写入边界做严格白名单校验。**适用**：任何「E2EE 默认、明文可选」的多租户 SaaS（笔记、协作、白板）。
2. **Manifest-driven provider catalog + 三档分类**——让新 provider 通过数据而不是通过代码集成；老 provider 渐次升级抽象层级。**适用**：plugin 系统、payment / cloud adapter 框架。
3. **CLI 边界 normalization + `_raw` 永远保留 + permissive schema**——在跨进程边界把外部格式归一为内部 canonical，schema 用 `passthrough() + optional()`。**适用**：对接快速漂变外部 API 的网关 / ETL / 中间层。
4. **Per-account monotonic `seq` + entity 级 optimistic concurrency**——顶层全局序做 client reconciliation；entity 级 `expectedVersion` 做冲突检测。**适用**：协同编辑、跨设备笔记、IoT 状态同步。
5. **ActivityCache + batch + timeout loop**——高频 ephemeral 永不直接落 DB。**适用**：在线状态、协同光标、IoT 心跳。
6. **Tier-0 invariant + 嵌套 AGENTS.md 治理**——根文档写「永远不变的几条」+ 子文档写「这个目录的本地约定」。**适用**：大规模 monorepo 或多人仓库。
7. **Feature gating 走单一 catalog + `readServerEnabledBit === true`（永不 `!== false`）**——服务端 owner 用集中开关控制客户端能力；客户端 fail-closed。**适用**：SaaS 多租户、on-prem 自托管、白标产品。
8. **Handoff / migration 显式多阶段协议 + workspace transfer safety 独立校验**——跨设备迁移抽象成 prepare → stage → apply → finalize，每阶段可 checkpoint。**适用**：跨设备会话、容器迁移、IDE workspace 搬迁。
9. **E2EE with explicit envelope versioning + legacy/dataKey 双变体**——用 1-byte version + 显式 binary layout 文档化每一字节；legacy path 保留到老用户迁移完。**适用**：协议升级期的密码学演进。
10. **DRIFT fixture + shape 比对（不是 value 比对）+ allowlist**——把「外部会变」变成「测试本身」而不是「panic」。**适用**：所有 schema 敏感的对接。

### 关键设计决策

**决策 1：中继服务端永远看不到明文**
- **问题**：跨设备同步就要过第三方服务器；传统 TLS + 服务端再加密让服务端仍能解密，隐私和企业自托管都不可接受。
- **方案**：客户端持 DEK（legacy 用 shared secret，dataKey 用 per-session DEK 包成 box bundle）；服务端只接受 opaque string 并做 `expectedVersion` 乐观并发校验。
- **Trade-off**：服务端失去索引/搜索/语义聚合能力；未来想加全局搜索只能靠客户端本地 memory index（README 里 Local memory search 就是这条路径的妥协）。
- **可迁移性**：高。任何需要「中继但不让中继方看明文」的系统（笔记同步、家庭设备同步、跨设备 clipboard）都能套这套 envelope + 版本号 + per-record DEK 模式。

**决策 2：协议层极简——Socket.IO 上两类事件 + monotonic `seq`**
- **问题**：AI agent 的 session 同步是「高频小写 + 多设备 + 断线恢复」；传统 REST + 长轮询撑不住；CQRS / outbox 太重；纯 P2P 又要 NAT 穿透。
- **方案**：Socket.IO 上 `update`（持久）+ `ephemeral`（临时）两类事件 + `expectedVersion` 乐观并发 + 单一 monotonic `seq`。把「写」做成 plain POST，避免 REST 动词语义。
- **Trade-off**：失去 REST 自描述性 / OpenAPI 直出，但获得了「不绑 entity 边界」的自由。
- **可迁移性**：高。任何「多客户端写 + 中继 + 偶尔 server-side 校验」的场景都适用；适合中等规模（<10k 并发）实时协同。

**决策 3：两层加密变体（`legacy` NaCl secretbox + `dataKey` AES-256-GCM）+ 显式 envelope version**
- **问题**：早期用户用 shared secret 跨设备同步是「启动成本最低」的方案，但共享 secret 一旦泄露就全盘泄露；需要升级到 per-session DEK 又不能丢老用户。
- **方案**：保留 NaCl secretbox path（XSalsa20-Poly1305，24-byte nonce）作为 legacy；引入 AES-256-GCM（12-byte nonce + 16-byte tag + 1-byte version）作为新 path；客户端根据「本地有没有 dataKey」自动选；所有 binary layout 显式稳定（`docs/encryption.md` 把每个 byte 都画出来）。
- **Trade-off**：客户端逻辑更复杂（两条 decrypt path、显式解析、format-version 校验）；换得**每会话独立密钥 + 前向保密 + 配额/权限可挂在 DEK 上**。
- **可迁移性**：中-高。Crypto 升级路径的范式（`legacy → modern + version byte + 显式 fallback`）可以复用，但 TweetNaCl 选型本身是历史包袱。

**决策 4：Provider 抽象分层 = `native` / `bespoke ACP` / `catalog+hook` 三档**
- **问题**：不同 agent（PI、Codex、OpenCode vs Qwen、Kilo、Copilot）的「复杂度差 10 倍」；统一抽象要么过厚（拖慢简单 provider），要么过薄（复杂 provider 写得很丑）。
- **方案**：把 provider 分到三档，每档对运行时 / catalog / execution-run 注册有明确的 entry point（`createCatalogDefinedAcpBackend` 是 catalog+hook 档的入口）。同一份 manifest-driven 模式让简单 provider 几行就能接入。
- **Trade-off**：维护者必须理解「为什么 PI / Gemini 不能压扁到 catalog」；目前 Copilot、Kiro 还在迁移中，认知负担存在。
- **可迁移性**：高。任何「多 backend、复杂度不一」的系统（plugin 系统、adapter 框架、payment gateway 集成层）都能照抄。

**决策 5：Tool 标准化在 CLI 边界完成一次 + 永远保留 `_raw` + permissive schema**
- **问题**：同一个「Read / Bash / Patch」动作在 Claude、Codex、OpenCode、Gemini 里叫法、参数、错误形态都不一样；UI 不能为每个 provider 写一套卡片；但 provider 又会**漂移**——schema 写死就等于慢性崩溃。
- **方案**：在 CLI 入站边界把 tool call/result 标准化，套上 `_happier.canonicalToolName + _raw`；schema 用 `passthrough() + optional()` 做 forward-compatible；提供 `HAPPIER_STACK_TOOL_TRACE=1` 抓真实 payload 写 fixture，drift 由单元测试 + provider harness 自动检测。
- **Trade-off**：多一层 CLI 转换成本（延迟 + 维护负担）；换来 UI 可以**一份渲染器**覆盖所有 provider，且老 session（pre-V2）靠渲染层 fallback normalization 还能渲染。
- **可迁移性**：高。任何「多源同一语义实体」系统都可以照搬：在边界归一化 + 保留 raw + fixture 测漂移。

**决策 6：Session Handoff 多阶段协议（plan → transfer_blobs → stage → apply → import → finalize）**
- **问题**：AI agent session 是有状态的（cwd、scratch file、open file handle、provider state）；跨机器迁移不能「拷 transcript」就完事，还得带 workspace。
- **方案**：`packages/protocol/src/sessionControl/handoff/*` 把 prepare/expand → activate/migrate → contract 序列固化下来；`@happier-dev/transfers` 做 workspace blob 传输；workspace-transfer source path 走独立 safety 校验防止越界拷。
- **Trade-off**：协议复杂度上升（V2 比 V1 多 prepare/expand、confirm、resume 等 RPC）；换来**有状态会话可在多台开发机之间无缝搬家**。
- **可迁移性**：中-高。任何「带状态的开发/工作流」想跨设备迁都能套。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | **Happier** | Orca (stablyai/orca) | Open Design | oh-my-claudecode | OmniRoute |
|------|------------|---------------------|-------------|------------------|-----------|
| Star 数 | 1.4k | ~40k | ~84k | ~38k | ~43k |
| 定位 | 跨设备 E2EE agent 中继 | 新的 ADE（web IDE） | AI 设计输出 | Claude 多 agent 编排 | LLM API 网关 |
| E2EE + 自托管 | ✅ 一等公民 | ❌ 托管 SaaS | ❌ | ❌ | ❌ |
| 多 provider 一等公民 | ✅ 11+ agent | ⚠️ 中等 | ❌ Claude 优先 | ❌ 仅 Claude | ✅ 290+ provider（API 侧） |
| 跨设备多端 | ✅ iOS/Android/Web/Desktop | ✅ Desktop+Mobile+VPS | ⚠️ 桌面为主 | ❌ | ❌ |
| 企业级 auth (OIDC/mTLS) | ✅ | ❌ | ❌ | ❌ | ⚠️ |
| Provider 抽象范式 | 三档 manifest-driven | 黑盒 | — | orchestration 层 | API gateway |
| 跟现有 CLI 共存 | ✅ 套在外层 | ❌ 替换 | ❌ | ⚠️ 包装一层 | ✅ 路由 |

### 差异化护城河

- **技术护城河（中-高）**：两层加密 envelope、tool normalization V2 + drift fixtures、provider 三档分类 manifest、handoff 多阶段协议——这些不是简单复制能复制的，需要长期迭代。
- **生态护城河（中）**：Claude Code / Codex / OpenCode / Pi / Cursor / Kilo / Kimi / Qwen / Auggie / Kiro / Copilot 一视同仁的接入宽度 + `@happier-dev/protocol` 公开 schema。
- **信任护城河（高）**：瑞士托管 + E2EE + 自托管 + 企业级 auth（OIDC / mTLS / keyless external auth）——privacy-first 叙事在 dev 圈差异化强。

### 竞争风险

- **官方厂商内嵌同步**：Anthropic / OpenAI 可能直接做 Claude Code / Codex 跨设备 sync。Happier 押的是「多 provider 中立 + 隐私」差异化，但单一 provider 用户会被吸走。
- **Orca 类全栈 IDE**：对「不想用 CLI」的用户，Orca 风格可能胜出。
- **ACP 标准化**：如果 ACP 变成 LLM agent 通用协议，Happier 在 catalog 层的壁垒会下降——所以他们把 V2 tool schema / fixture drift 视为真正壁垒。

### 生态定位

**Happier 是「AI coding agent 世界的 1Password + Tailscale + Linear」**——一个不持内容的 sync + relay 层，把多 provider / 多设备 / 多人协作统一在一个 E2EE 通道里。它不是 agent，是 **agent 之间的 broker**。

## 套利机会分析

- **信息差**：⭐⭐⭐⭐ 高 — 2.9M 行代码 / 6+ agent 兼容 / E2EE / 已上 App Store / 800 commits/月，仅 1.4k star；处于 vibe-coding 风口但热度远低于同类项目，**典型「代码体量 vs 关注度」倒挂**。
- **技术借鉴**：⭐⭐⭐⭐⭐ 高 — envelope + per-record DEK、provider 三档 manifest、tool normalization + drift fixture、ActivityCache + timeout loop 这四套模式可直接迁移到任何需要「多端 / 多 backend / E2EE」的中继系统。
- **生态位**：⭐⭐⭐⭐ 高 — 在「Anthropic/OpenAI 云端同步 ↔ Orca 类全栈 IDE ↔ OmniRoute 类 API gateway」之间，Happier 占据「**跨 provider + 跨设备 + 隐私**」这一空白象限，且先发优势明显。
- **趋势判断**：⭐⭐⭐⭐ 高 — AI agent 多 provider 共存 + vibe-coding 工作流 + 隐私敏感开发者，这三条趋势都在 2026 年持续加强；Happier 比同类项目（Orca 偏 IDE / oh-my-claudecode 偏 Claude-only）有明确后发优势（如果不算已经被 Orca 抢走的 star 累积的话）。

## 风险与不足

1. **单人主导风险**：Top 1 贡献者 `leeroybrun` 占 81.3% 提交量，bus factor = 1 强信号；若主开发者停摆，项目节奏会断崖式下降。
2. **pre-release 状态**：官网明示「not ready for general use yet」；fix:feature = 7:1 的极端比例说明目前是「feature 收敛后在大用户量上做兼容性修补」，生产可用但需预期 bug。
3. **TweetNaCl 选型历史包袱**：crypto 层用 TweetNaCl 而不是 libsodium / WebCrypto，新项目照搬范式时建议替换底层库。
4. **「标准协议」野心克制**：`@happier-dev/protocol` 是**共享 schema** 而非**外部开放协议**——意味着生态护城河是「接入数」而不是「规范锁定」，ACP 标准化会侵蚀这层。
5. **官方厂商竞争**：Anthropic / OpenAI 若推出官方跨设备同步，单 provider 用户会被吸走，Happier 必须靠「多 provider 中立 + 隐私 + 自托管」三件套持续差异化。
6. **单一 founder 风险与组织年龄过短**：Happier Devs 账号仅 0.5 年龄 + 仅有 5 个公开仓库，外部观察者难以判断「这是真创业还是 one-person side project」；需要在主开发者 blog / 演讲 / funding 公告上有更多信号才会显著提升信任。

## 行动建议

### 如果你要用它

- **适用场景**：已经在用 Claude Code / Codex / OpenCode 之一作为日常编码 agent，并希望「路上用手机继续 / 与同事围观 / 数据可自托管」的人。
- **不适合**：仅用单一 provider、且该 provider 已有官方云端同步的轻度用户。
- **自托管门槛**：低——`apps/server` 提供 Docker image，OAuth 可接 GitHub / OIDC，企业级 mTLS / keyless external auth 都已支持；小团队可在一台 VPS 上 5 分钟跑起来。
- **隐私级别**：高——E2EE + 瑞士托管 + 自托管三选一，DEK 在客户端，服务端永远拿到 opaque blob。
- **多端覆盖**：iOS 已上 App Store、Android Play Store 私人测试 + APK 公开、桌面 macOS/Linux/Windows、Web 客户端同时可用。

### 如果你要学它

重点研究以下文件/模块（按学习收益排序）：

1. **`docs/encryption.md`** — 双变体加密 + envelope；这是 E2EE 范式最干净的表达。
2. **`packages/protocol/src/tools/v2/`** — Tool normalization 单一源；看 `_happier.canonicalToolName + _raw` 双轨设计。
3. **`packages/agents/src/manifest.ts`** + **`docs/acp-provider-feature-matrix.md`** — Provider 三档分类 + manifest-driven 集成。
4. **`packages/protocol/src/sessionControl/handoff/`** — Session handoff 多阶段协议。
5. **`AGENTS.md`** + **`DESIGN.md`** — Tier-0 invariant + 嵌套治理范式（43k + 40k 字符的「工程宪法」）。
6. **`docs/cli-architecture.md`** + **`docs/backend-architecture.md`** — CLI daemon + Server 中继的协同模式。

### 如果你要 fork 它

可改进方向：

1. **统一 provider 配置界面**：目前 manifest + ACP 三档分类导致新 provider 接入仍需读懂 `catalog+hook` 概念；可以做一个「输入命令行名 → 自动接入」的快速路径。
2. **本地 memory index + 跨 session 搜索**：服务端因 E2EE 无法做语义聚合；客户端本地做 index + 用 sqlite-vec 之类做向量搜索是清晰的 next step（README 已暗示）。
3. **CI fixture 自动化扩展**：目前 tool trace fixture 抓真实 payload，可以扩展到「自动 PR 到上游 provider 仓库」形成生态共建。
4. **Web 端的 WASM provider runner**：让 Web 客户端能直接跑 Codex-lite / OpenCode-lite，不需要外部 CLI；进一步降低 friction。
5. **多人协作 session 的 RBAC**：当前多人协作是「所有人看 + 部分审批」，企业部署需要按角色 / 团队 / 项目做细粒度 RBAC。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/happier-dev/happier （已收录，覆盖 Architecture / Monorepo / Security / WebSocket Protocol / CLI Daemon / Agent Backends / MCP / Sync Engine 等多子页面） |
| Zread.ai | 未收录 |
| 关联论文 | 无（应用层项目，无学术输出） |
| 在线 Demo | 无官方 playground；可在本地用 `apps/cli` + `apps/server` 跑自托管实例作为内嵌 demo |
| 官方文档 | https://happier.dev/docs（docs-as-code：`apps/docs/content/docs/**`） |
| 架构文档 | `docs/protocol.md` / `docs/encryption.md` / `docs/cli-architecture.md` / `docs/backend-architecture.md` / `docs/tool-normalization.md` / `docs/acp-provider-feature-matrix.md` / `docs/feature-gating.md` |
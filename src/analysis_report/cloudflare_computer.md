# GitHub推荐：2.6 个月 6.7K stars：Cloudflare Computer 把 Anthropic Computer Use 协议塞进 Durable Object

> GitHub: <https://github.com/cloudflare/computer>

## 一句话总结

Cloudflare 官方把"虚拟文件系统 + 可执行代码 + 持久化"三合一挂到 Durable Object 上，做了一个**权威单点 + 投影多端**的 AI Agent 工作区底座：**同一份 SQLite 状态**，能被 Container 真 Linux 用户态、Dynamic Worker shell、Dynamic Worker ESM 三种执行后端共享消费。

## 值得关注的理由

- **设计哲学罕见地把"持久化 + 执行 + 同步"做成一等公民**：DO SQLite 是 single source of truth，Container 通过 capnweb RPC 双向同步，Worker 后端直接走 Workers RPC 直读；不是又一个 VM sandbox 平台，而是把 Cloudflare 自家的边缘栈攒成了一个 Agent workspace 的标准底座。
- **协议层有论文气质**：Sync Bracket 协议用 `(rev, path)` cursor 替代 scalar watermark、**拒绝 rename opcode** 让每条记录都是 path → final state、把 git pack 直觉与 SQLite 持久性拼在一起 —— 这是任何"两端 SQLite 双向同步"场景都值得借鉴的范式。
- **同公司矩阵的关键一格**：与 workerd（runtime）、capnweb（RPC）、vibesdk（Agent 平台）、cloudflare-os、kumo 并列的官方押注；定位明确是 Cloudflare Agent 栈（workerd / capnweb / computer / agent SDK / 应用）中段的"通用工作区底座"。

## 项目展示

![Architecture overview — DO SQLite 权威 + Container FUSE 投影 + Worker 后端直读 的多后端投影关系](https://raw.githubusercontent.com/cloudflare/computer/main/docs/assets/arch.png)

> 仓库 `docs/assets/arch.png`（1612×1474），是 README + docs/README.md 唯一被引用的图，本身就是主架构图。

> 仓库处于 PREVIEW 状态，无官方托管 demo；`examples/think`（终端形态 Agent）和 `examples/tutorial`（Worker + Container 跑 pandoc 生成 PDF）是两个最直观的可运行示例。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | <https://github.com/cloudflare/computer> |
| Star / Fork | 6,669 / 341（forks/stars ≈ 5.1%，收藏者多、动手少） |
| 代码行数 | 99,269 行（TypeScript 81.8%，JSON 14.5%，JS/TSX/Shell 共 3.7%），491 文件 |
| 项目年龄 | 2.6 个月（首次提交 2026-05-22） |
| 开发阶段 | 密集开发 → 0.1.x 补丁期（v0.0.0-alpha.0 → alpha.13 → v0.1.0 → v0.1.1，共 17 个 tag） |
| 贡献模式 | Cloudflare 官方组织账号 + 单个 staff engineer 主导（aron-cf 占 96.2%） |
| 热度定位 | 大众热门（短期高曝光 + Agents 赛道话题） |
| 质量评级 | 代码[优秀] 文档[优秀] 测试[优秀]（119 个测试文件 + per-package CI matrix） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Cloudflare 官方组织账号（16 年 / 15K followers / 573 repos）。主贡献者 **aron-cf** 是 capnweb、vibesdk 等同公司项目的核心作者，专注 Cloudflare 平台的"Agent 运行时 + 边缘 AI 沙箱"主线。同公司主线合作者 `guybedford`（Vercel 的 ESM/import-map 专家）也参与，跨厂商资源整合的意味明显。

### 问题判断

作者看到的是 **Anthropic Computer Use 协议需要一个"可信 + 持久 + 可重放"的工作目录**，而 Cloudflare 既有栈（DO 强一致写 + 跨重启存活 + 单租户单点仲裁 / Container 真 Linux 用户态 / Dynamic Worker 隔离 ESM / capnweb 长连接 RPC）刚好提供了所有零件，只是缺组装说明书。时机上，2026 年 5-6 月 Anthropic / OpenAI 都在推 Agent 工具调用协议，正是 Cloudflare 把"边缘 + DO"做成 Agent 工作区底座的最佳窗口。

### 解法哲学

- **「权威单点 + 投影多端」**：DO SQLite 是 single source of truth；Container 通过 FUSE 把它投影成 Linux 文件系统；Dynamic Worker 通过 Workers RPC 直接读 DO 状态（无第二份存储）。
- **「pluggable + idempotent + lazy connect」**三项工程基线（README 自陈）：后端可插拔、所有写都幂等、所有连接都懒建立 —— 让一个 Workspace 在多 backend 下都"想先开"且不会浪费 isolate 寿命。
- **「state-based, not opcode-based」**：sync 协议不引入 `rename` / `mkdir` opcode，每条记录都是 path → final state；用 `(rev, path)` cursor 替代 scalar watermark，让中间断点也能恢复。
- **明确不做什么**：不做"通用云端沙箱"（e2b/daytona/modal 的领地）；不沾 agent prompt、tool routing、state machine 这些上层语义（留给 vibesdk）；不做 RAID-like 写冲突 CRDT（先 LWW，未来再加）。

### 战略意图

Cloudflare 把"Agent 平台"切成五层（**workerd 运行时 / capnweb RPC / computer 工作区 / agent SDK / 上层应用**），`computer` 故意做"通用底座"。商业化路径不是 SaaS，而是要让"给 Agent 一个工作目录"在 Cloudflare 上是**一行 Worker 代码**（`new Workspace({...})`）的事，把过去需要 e2b/daytona 才能做的工作压到原生 Cloudflare stack 上 —— 这是一种"**平台差异化能力**"而非"独立产品"的开源策略（genuinely open，深度耦合自家栈）。

## 核心价值提炼

### 创新之处（按新颖度 × 实用性排序）

1. **Sync Bracket 协议：DO SQLite ↔ Container FUSE 双向同步**
   - 描述：固定 512 KiB chunk → sha256 内容寻址 → `(rev, path)` cursor 而非 scalar watermark → `ChangeEntry` 是"path → final state"而非"operation" → `hasObjects` + `fetchObjects` 走 git pack 直觉。`PULL_BATCH_SIZE = 256` 限制 peak memory；post-apply `pushRev` 推进有 guard 防本地写竞争。
   - 新颖度 5/5 | 实用性 5/5 | 可迁移性 4/5
   - 适用场景：任何"两端 SQLite 双向同步"的协议设计；多 DO 同步、跨 region DO replication 都能直接套用。

2. **单一 `runtime.exec(source, { backend })` 多形态路由**
   - 描述：同一个 API 同时支持 shell 命令（Container + just-bash Worker）和 ES module（Worker JS），按 backend id 路由；`backend: "none"` 即纯 VFS。
   - 新颖度 4/5 | 实用性 4/5 | 可迁移性 5/5
   - 适用场景：任何 multi-runtime 系统的 adapter 抽象。

3. **ESM 后端的 capability-based module namespace（`ws:git` / `ws:artifacts` / `node:fs`）**
   - 描述：`WorkerJavaScriptBackend` 在每个 exec 新建 Dynamic Worker，`globalOutbound: null` 默认无 fetch；`ws:git` / `ws:artifacts` 是 host 注入的能力，每个能力有自己的 authority flag（`allowGitNetwork`、`allowArtifactNetwork`）；path confinement 双重检查。
   - 新颖度 4/5 | 实用性 5/5 | 可迁移性 4/5
   - 适用场景：任何"用户代码在 Dynamic Worker 里跑 + 调用 host API"的 sandbox。

4. **Workspace 可独立于后端使用（filesystem-only mode）**
   - 描述：`new Workspace({ storage: ... })` 不传 `backends` 即纯 VFS；让 computer 可作为 Cloudflare 平台通用 VFS 而非绑定 sandbox 的 SDK。
   - 新颖度 3/5 | 实用性 4/5 | 可迁移性 5/5

5. **Just-bash in Dynamic Worker（Vercel Labs 作品集成）**
   - 描述：`WorkerShellBackend` 用 `env.LOADER.get(id, codeCallback).getEntrypoint("ShellWorker")` 把 just-bash 装进 Dynamic Worker，每次 exec 拉起一个隔离 isolate。
   - 新颖度 3/5 | 实用性 4/5 | 可迁移性 4/5

### 可复用的模式与技巧

1. **`(rev, path)` cursor 而非 scalar watermark**：把"进度"编码为二维坐标，让一次 mutation 内的多个 entry 都能断点续传；rev 是 atomic batch boundary，path 是 batch 内子进度。
2. **state-based sync 而非 operation-based sync**：每条 entry 是"path → final state"，receiver 不需要 prior state 就能 apply；cold-start peer 也工作；re-apply 幂等。
3. **Content-addressed chunks + manifest**：固定 512 KiB chunk → sha256 → per-file manifest hash；相同字节只存一份；改一行只重算/重传一个 chunk。
4. **Per-backend tail-promise FIFO（reject 不传染）**：每个 backend 一个 `Map<string, Promise>`，push/pull/exec 链式 append；reject 通过 `.then(..., fn)` 捕获，让队列不被单个失败阻塞。
5. **Cache invalidation by identity（`#invalidateHandle` 模式）**：handle 被 transport failure 后，下一个 RPC 调用前主动 drop 缓存；用 identity 而非 reference 比较防"close 中途 race"。
6. **`Symbol.dispose` on capnweb stubs + `using` 关键字**：每个跨 RPC 边界的值都暴露 `Symbol.dispose`，调用方用 `using` 自动释放；Driver 在内部把 envelope 绑到 `using` 变量 + drain 内层 stream 再 dispose。
7. **WorkspaceServiceProxy for DurableObjectNamespace in Worker Loader env**：跨 structured clone 不能传 raw DurableObjectNamespace；通过 `ctx.exports.WorkspaceServiceProxy({ props: { binding, id } })` 铸造 Fetcher。
8. **capability-based module namespace（`ws:`）**：`ws:` 命名空间保留，user code 不能 shadow；每个 capability 有自己的 authority flag；path confinement 在 isolate 内先做，host 再做一次。

### 关键设计决策

1. **SQLite-backed VFS as Source of Truth**
   - 问题：Agent 的工作目录需要"持久 + 强一致 + 可查询"。
   - 方案：所有文件元数据落 DO 自己的 SQLite（`vfs_nodes` / `vfs_dirents` / `vfs_blobs` / `vfs_chunks` / `vfs_manifests` / `vfs_changes`）；inode 模型下 rename = O(1)，path resolve <10 跳，sub-millisecond。
   - Trade-off：上限 ~10 GB（与 DO 共享存储）；chunk write 必须 sha256；删除记录靠 `vfs_changes` tombstones 不能 pruning（table 单调增长，"planned"）。
   - 可迁移性：中（任何"有 DO + Durable SQLite"的平台都能复用）。

2. **Pluggable backend, single `runtime.exec(source, { backend })` entry**
   - 问题：三种后端（Container / Worker shell / Worker JS）共享 VFS 但形态差异大。
   - 方案：`workspace.runtime.exec` 是唯一入口，`{ backend: '...' }` 路由；模块后端和命令后端统一到 `WorkspaceModuleBackendHandle` adapter；`backend: "none"` 即纯 VFS 无执行。
   - Trade-off：每种 backend 各自有 fidelity gap（just-bash 不支持 hardlink、Worker JS 一次只能跑一次 stdout、Container 没 cross-request reattach）。
   - 可迁移性：高（任何"多形态执行后端 + 共享状态"的系统都能复用该 routing 模式）。

3. **Capnweb 长连接 + 1:1 DO↔Container + WS server 角色反演**
   - 问题：capnweb 没有 hibernation-aware；DO 必须能 evict；但 sync 协议不能丢；container-initiated 流量要能 wake DO。
   - 方案：1:1 映射让 `ctx.getWebSockets()` 永远只有 1 个；DO 当 WS server（虽然 container 暴露 `/ws`，但通过 egress 反向 dial 让 DO 控制路由）—— 因为 `ctx.acceptWebSocket()` 是唯一 hibernation API。
   - Trade-off：不能 PartySocket（牺牲 reconnect 库但保留 hibernation 路径）；`server.accept()` 不是 hibernation API（forward-looking 改造路径已 sketch）。
   - 可迁移性：中（"DO 当 server / container 反向 dial"是 Cloudflare 平台专属，但 cursor-driven resume + Symbol.dispose 在任何长连接系统都通用）。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | cloudflare/computer | e2b-dev/e2b | daytonaio/daytona | modal-labs/modal | cloudflare/sandbox-sdk |
|------|---------------------|--------------|-------------------|------------------|------------------------|
| 定位 | DO-centric Agent 工作区底座 | VM 级云端代码沙箱 | AI 开发环境 + 沙箱 | serverless compute + GPU | 同公司仅执行无 FS |
| 持久化 | DO SQLite（强一致 + 跨重启） | 无（VM 重启即丢） | dev workspace 持久化 | 无内置 | 无 |
| 多后端 | 3 种（Container / Worker shell / Worker JS） | 仅 VM | 仅 VM | serverless 函数 | 仅 Worker JS |
| 同步协议 | Sync Bracket（理论保证） | 无 | 无 | 无 | 无 |
| 生态成熟度 | 2.6 个月 / v0.1.1 PREVIEW | 多年成熟、事实标准 | 2026-06 核心转私有 | 多年成熟 | 同公司新项目 |
| 平台绑定 | Cloudflare native | 独立云服务 | 独立云服务 | 独立云服务 | Cloudflare native |

### 差异化护城河

- **DO 当 VFS 权威 + capnweb 同步**：任何 DO 用户都能复用，是 Cloudflare 平台的隐性资产
- **runtime.exec 多 backend 路由**：不绑执行形态，让上层 Agent tool 一次代码 0 改动切 backend
- **内容寻址 chunk 同步**：让多 agent 协作有理论保证
- **与 Cloudflare 自家 stack 深度耦合**（capnweb、Container、Worker Loader、R2、Artifacts）：平台生态绑定

### 竞争风险

- 仍在 PREVIEW、API 不稳、文档与 wire contract 有 drift（issue #59 暴露）
- 写冲突语义仅 LWW（项目自承，多 agent 共享文件不安全）
- Container 重启丢本地 VFS、big sequential I/O 比 disk 慢 30x（chunk 哈希成本）
- 与 e2b/daytona/modal 的成熟度差距大，DX 短板明显

### 生态定位

**Cloudflare 平台"Agent 工作区"标准底座**。不是 VM sandbox 通用替代品（明确不抢 e2b 市场）；与 sandbox-sdk 上下分工（computer 上、sandbox 下）；是 Cloudflare 5 层 Agent 栈（workerd / capnweb / computer / agent SDK / 应用）的中段。

## 套利机会分析

- **信息差**：仓库 star 6.7K 但 docs 体系 19 篇设计规格 + 50 个 .md + 8 个可跑 example 几乎完整，等于"已经能学到所有设计决策"，对架构爱好者是低成本阅读资源；v0.1.1 PREVIEW 阶段，进入门槛极低（capnweb、Sync Bracket、capability namespace 三套模式都是可独立复用的）。
- **技术借鉴**：Sync Bracket 协议（不绑 Cloudflare，可抽给"两端 SQLite 双向同步"复用）+ `(rev, path)` cursor + state-based sync + capability-based module namespace + per-backend tail-promise FIFO —— 这是任何"长寿命 isolate + 不可信连接"系统都通用的模式集合。
- **生态位**：填补了"Cloudflare 平台缺乏 Agent 工作区标准底座"的空白；上游依赖是 Anthropic Computer Use / OpenAI Agent 协议层、下游被 vibesdk / cloudflare-os / kumo 等同公司 Agent 项目复用。
- **趋势判断**：增长曲线与 Anthropic / OpenAI Agent 工具调用协议同频；2026 年 6 月起 v0.1.x 进入补丁期，节奏放缓说明架构轮廓已定型，下一步是 docs/06 Mount Interface（"not yet implemented"）落地 + 真实 DO SQLite 路径进 CI（issue #71）；比 e2b 的后发优势在"DO-native + 零冷启动 + 同 Workers 计费/部署模型"。

## 风险与不足

- **PREVIEW 状态**：README 明确标注 "NOT suitable for production use at this time"；docs 是 forward-looking intent，与代码现状有 drift（issue #59）。
- **写冲突 LWW**：多 agent 共享同一文件时不安全；项目自承未来会加 **CRDT / merge 策略**。
- **Container 重启丢本地 VFS**：container-side VFS 是 process-lifetime instance，重启即丢，靠 sync 重灌。
- **big sequential I/O 慢 30x**：`docs/19_performance.md` 自陈，chunk 哈希成本。
- **real DO SQLite 路径无 CI**（issue #71）：preview 阶段最大真实风险。
- **FUSE native addon 折腾**：arm64 host 上 `fuse-native` prebuilt 不兼容（AGENTS.md 明示 workaround）；libfuse2 + 自编译增加本地开发摩擦。
- **bus factor = 1**：aron-cf 占 96.2% commit；风险被 Cloudflare 官方 org 体系吸收，但若离开，单人维护的隐性知识成本会显现。
- **vfs_changes tombstones 单调增长**：pruning 未实现，table 单调膨胀（"planned"）。
- **wire error code preservation 未保证**（项目自承 "by accident"），fs codes 与 sync/shell codes 一致性是 deferred follow-up。

## 行动建议

- **如果你要用它**：现阶段仅适合 experiments / exploration / prototypes；想落地到生产前关注三个里程碑 —— ① v0.1.x → 1.0 API 收敛；② docs/06 Mount Interface 实现落地；③ real DO SQLite 路径进 CI（issue #71）。选它的场景是你已经在 Cloudflare Workers / DO 栈内、要给 Agent 一个长期可同步的工作目录、能接受 PREVIEW 风险；选 e2b 的场景是需要 VM 级隔离 + 多语言 SDK + GPU + 不绑定 Cloudflare。
- **如果你要学它**：重点关注 ① `docs/02_sync_protocol.md`（Sync Bracket 协议 + 拒绝 rename opcode 的论证）；② `docs/01_vfs.md` + `docs/03_filesystem_schema.md`（inode + 内容寻址 schema 设计）；③ `packages/workspace/src/workspace.ts`（单一 exec 多 backend 路由实现）；④ `packages/dofs/src/sync/`（applyChanges / fetchObjects / push 实现）；⑤ `packages/wsd/src/fuse/driver.ts`（FUSE 驱动源码 + 30 次高频迭代的 wsd 自带 VFS）；⑥ `docs/17_isolate_javascript.md`（capability-based module namespace）。
- **如果你要 fork 它**：可改进的方向 —— ① CDC chunking 替代固定 512 KiB chunk（项目已 self-note）；② CRDT / merge 替代 LWW（多 agent 协作安全）；③ `Symbol.dispose` 的 error code 透传保证；④ hibernation API 在 capnweb 上游落地后的真正 WS server 切换；⑤ vfs_changes pruning；⑥ 把 Sync Bracket 抽成独立 npm 包供非 Cloudflare 平台复用。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | <https://deepwiki.com/cloudflare/computer>（已收录，含 Sync Bracket 模式架构总览） |
| Zread.ai | 未收录 |
| 关联论文 | 无（基础设施项目，未发现配套 arXiv 论文） |
| 在线 Demo | 无官方托管 demo；`examples/think`（终端形态 Agent）+ `examples/tutorial`（Worker + Container 跑 pandoc 生成 PDF）是最直观的可运行示例 |
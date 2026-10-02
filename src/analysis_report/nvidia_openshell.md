# GitHub 推荐：NVIDIA OpenShell：8 个月 14K stars，把 enforcement 拉到 agent 进程之外的开源 Agent Safety Platform

> GitHub: https://github.com/nvidia/openshell

## 一句话总结

NVIDIA 把企业级「policy engine + out-of-process enforcement + Z3 形式化 review」三件套压成 Apache-2.0 的 agent 运行时——自治 AI agent 哪怕被 prompt injection 攻陷，也跑不出三道防线：kernel 级的 Landlock/seccomp 网关、Supervisor 进程的 L7 policy 决策、Z3 形式化核验的 pre-commit broker。

## 值得关注的理由

1. **立场最鲜明的 AI Agent 安全立场**：Claude Code/Codex/E2B/Daytona 都把 guardrails 留在 agent 自己进程里，OpenShell 直接喊出「browser tab model for agents」，把决策甩到 sandbox 之外，控这条产品哲学在企业落地里少有人做。
3. **把 GPU 栈式的可复证纪律搬到 LLM**：Landlock + seccomp + namespace + Z3 SMT + SPIFFE-style JWT + 多 sandbox runtime（Docker/Podman/K8s/MicroVM）——传统 infra/安全/SRE 领域的精华在一个 638K 行 Rust workspace 里被压缩、互补、重新组合。
4. **可验证、可复用的设计语言**：`IsolationBackend` trait + type-state lifecycle（`Bound → Confirmed → Ready → Running`）+ `OuterFenceGuarantees` 不变量投影——这些 pattern 可以直接拿到 KMS / TEE / 容器 runtime / CI runner。

## 项目展示

![OpenShell Banner (light)](https://raw.githubusercontent.com/nvidia/openshell/main/docs/brand/assets/openshell-banner-light.png)

> OpenShell 官方主视觉——项目以「Browser tab model applied to agents」为产品核心叙事。

- 外部深度文章：[Add Runtime Controls to AI Agents with NVIDIA OpenShell](https://developer.nvidia.com/blog/add-runtime-controls-to-ai-agents-with-nvidia-openshell/)（NVIDIA Dev Blog，提出「Safety / Capability / Autonomy」三难）
- 在线 Demo：[Brev 一键试用](https://brev.nvidia.com/launchable/deploy/now?launchableID=env-3Ap3tL55zq4a8kew1AuW0FpSLsg)

> 本仓库 README 与 docs 首页目前能供可引用展示的只有官方 hero banner；架构示意图主要在 NVIDIA Dev Blog 以内嵌图存在，不适合公开为图引用。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/nvidia/openshell |
| Star / Fork | 14,005 / 1,624 |
| 代码行数 | 638,689 行（Rust 75.8%, Go 8.4%, JSON 5.1%, Shell 3.6%, Python 2.4%） |
| 项目年龄 | 8 个月（首发 commit 2026-01-29，仓库创建 2026-02-24） |
| 开发阶段 | 密集开发（30 天 357 commits, 90 天 666 commits, 12 commits/day） |
| 贡献模式 | 小团队 + 社区协作（Top 1 ≈20.8%, Top 5 ≈65%, 161 名贡献者） |
| 热度定位 | 大众热门（NVIDIA GTC 2026 公开亮相后 8 个月拿到 14K stars） |
| 质量评级 | 代码 优秀 / 文档 优秀 / 测试 充分（49 tests.rs + 13 tests/ 目录 + 4 套 nextest profile） |
| License | Apache-2.0（Compute driver MXC 为 Windows 专属） |

### 关键 Issue 信号
1. [#1737 Establish the Isolation Backend interface](https://github.com/nvidia/openshell/issues/1737) — 揭示把 Landlock/seccomp/gVisor/未来 TEE 抽象为单一 trait（已在 `crates/openshell-isolation-interface/src/contract.rs` 实现）
2. [#981 Split Supervisor and Agent into Separate Pods with gVisor Isolation](https://github.com/nvidia/openshell/issues/981) — 揭示 K8s 部署形态下 supervisor 与 agent 的边界划分
3. [#1793 Support method-level governance for MCP tool calls](https://github.com/nvidia/openshell/issues/1793) — 揭示 MCP 策略粒度从 server 级到 method 级的进化
4. [#682 Cryptographic agent identity binding](https://github.com/nvidia/openshell/issues/682) — 揭示 policy 决策点从「谁在调用」升级到「哪个可密码学验证的 identity 在调用」
5. [#1792 L7 proxy HTTP_PROXY/HTTPS_PROXY](https://github.com/nvidia/openshell/issues/1792) — 已用「driver-passed upstream proxy + sandbox ENV 不读 HTTP_PROXY」解决

## 作者视角：为什么存在这个项目

### 创始人/作者背景

OpenShell 不是个人项目，是 NVIDIA 公司运营者项目（org 14.4 年、30K followers、810 repos）。核心 Maintainer 是 `drew`（Drew Newberry，占 commit 20.8%）+ johntmyers、pimlock、elezar 三个 NVIDIA 全职同事。CONTRIBUTING.md 第一句话是「You must understand your code」——这是一个明确为「AI 时代公司开源治理」设计的项目，不是个人激情项目。

### 问题判断

NVIDIA 团队观察到企业客户的两类痛点：

1. **精细授权缺失**：代理需要的不是「能不能运行」这种粗粒度开关，而是 per-method HTTP / MCP / GraphQL / JSON-RPC 的三维度精准放行（什么 binary 调哪个 host:port 调什么 method）。
2. **in-process guardrails 失效**：当 LLM/reasoning model 越来越强，agent 自身可以重写、看穿、绕过内置 guardrails；engineer 与 policy checker 不能同进程。

时机为什么是 2026？三个叠加：(a) LLM agent 进入企业生产，(b) Anthropic / OpenAI 把 in-process 模式沉淀成事实标准暴露「同进程无法兜底」的脆弱，(c) NVIDIA 在 GPU 生态里 10 年沉淀的「kernel-isolated compute + declarative config + formal review」三件套刚好可以原班搬到 LLM 调度领域。

### 解法哲学

工程界最常争论的「内核 vs 进程内」「形式化 vs 提交即可」二元对立，OpenShell 同时选了两者：(1) Landlock + seccomp user-notification 把 enforcement 强压在 kernel/进程边界；(2) Z3 SMT solver 把变更前 review 也做到位。任何 policy 修改都先经形式化核验再人工复核，permission 层不做「二次猜测」。对比 Daytona 的 per-workspace 模式，OpenShell 明确选择 per-binary + per-host + per-method 三维度定位，宁可 policy 复杂也不放过一个非预期路径。

### 战略意图

- **商业意图**：open-core。`compute-driver-mxc` 是 Windows 专属 driver（与 NVIDIA MXC/Spectrum-X/NIM 整合），Docker/Podman/K8s/VM driver 都 Apache-2.0。NVIDIA 在保护 Windows 上的硬件整合能力，同时把跨云跨运行时层全部开源。
- **生态绑定**：与 NemoClaw 并列发布（NVIDIA 内部 agent runtime），形成「agent runtime + safety runtime」一对。`.agents/skills/` 直接安装给 Claude/Codex 等 IDE——这是 NVIDIA 把 OpenShell 当作 NemoClaw enforcement 层卖货的设计选择。
- **治理纪律**：明确「agent-first, not agent-only」+ Vouch system（AI 生成的 PR 默认被拒，需要 Maintainer vouch）——这是项目对 AI 时代开源质量的主动反制。

## 核心价值提炼

### 创新之处

1. **IsolationBackend trait + Bound→Confirmed→Ready→Running type-state lifecycle**：用 type-level guarantee 强制「未 verify 不可执行」，后端只需实现 trait，supervisor 通过 `BackendRegistry::resolve` name → backend 映射，无 fallback — 新颖度 4/5, 实用性 5/5, 可迁移性 4/5
2. **`OuterFenceGuarantees` 不变量投影 + SHA-256 generation binding**：本地背不变量完全与机制解耦，common runtime 只 check「DefaultDenyEgress / NoUnmanagedEgressPath / RevocationVerified / ControllerLossFailsClosed」四点是否同时命中 — 新颖度 5/5, 实用性 4/5, 可迁移性 4/5
3. **ReachabilityModel Z3 encoding + capability_expansion delta**：把 policy + credentials + binary registry 编码成 SAT constraints，跨 (binary, host:port) 检查「是否 reachable with credential」，delta baseline vs merged 是 proposal risk 核心 — 新颖度 4/5, 实用性 4/5, 可迁移性 3/5
4. **`BinaryIdentity{executable, ancestors, cmdline_paths}` 走 `/proc/<pid>/exe` 链**：不依赖「agent 报告什么」，而是 trusted observation 走 /proc 链拼出多个 ancestor executable + cmdline path — 新颖度 3/5, 实用性 5/5, 可迁移性 2/5
5. **upstream_proxy.rs driver-passed proxy + operator-only NO_PROXY config**：corporate proxy 只能由 compute driver 传入作为 CLI arg，不能被 sandbox ENV 覆盖 — 新颖度 4/5, 实用性 5/5, 可迁移性 4/5
6. **per-tool MCP authorization via params.name flatten/nested convertor**：走「tool = glob(params.name)」嵌套 config ↔ flat dot-path 无损转换 — 新颖度 3/5, 实用性 4/5, 可迁移性 3/5
7. **Governance + Vouch system**：明确「agent-first, not agent-only」、AI 生成的 vouch request 默认被拒、PR 不 vouched 默认 close — 新颖度 5/5, 实用性 3/5, 可迁移性 4/5

### 可复用的模式与技巧

1. **type-state lifecycle with `Box<Self>` consume 旧状态**：适用 CI runner 启动序列、TEE boot attestation、worker pool 加入协议、任何需要「N stages 逐步 verify」才能到「可使用」状态的资源。
2. **isolation backend trait + BackendRegistry name-only resolution + no fallback**：多 runtime 后端抽象，需保证「主机不能被误指向默认后端」。
3. **deny-by-default + Z3 formal review before commit**：适用 IAM policy review、Terraform plan、K8s NetworkPolicy、API gateway rule set——任何有「人类评审 config change」+「agent 主动写 config」交集。
4. **outer fence guarantees 抽象 + native evidence projection**：适用 TEE attestation、KMS provider attestation、container runtime attestation——任何有「多种不变量」+「需要抽象不变量集」。
5. **driver-passed enterprise config, sandbox ENV cannot**：适用企业 sandbox-as-a-service、企业 K8s Pod——任何需要「sandbox 不能选择自己的 outbound proxy / upstream」。
6. **per-tool / per-method L7 authorization on top of TCP**：适用 MCP server、GraphQL gateway、gRPC method-level auth——任何需要「L4 host:port 可达」+「L7 method 不可达」不对称。
7. **client-go style multi-sub-client 共用一个 gRPC connection**：任何「多 API domain 的 Kubernetes / Go SDK」都可走——CLI 在子命令间避免重连。

### 关键设计决策

1. **决策：三体拓扑 Gateway → Supervisor → Sandbox** — 三维选型
   - **问题**：单进程做 control + enforcement + isolation 三件事不可能既要 out-of-process 决策又要 in-kernel 拦截。
   - **方案**：Gateway（控制面，多租户 + 凭证持有 + 生命周期）/ Supervisor（受信侧，policy PDP + 凭证代理 + DNS/TCP 中转）/ Sandbox（不可信侧，仅依赖 Landlock + seccomp，所有 outbound 经 Sandbox Protocol 转出）。
   - **Trade-off**：三体拓扑引入跨进程序列化、HTTP/2 multiplex 复杂度、跨网络传输加密、debug 表面收紧。
   - **可迁移性**：高。任何跨边界 enforcement 都适用分离「控制 / 决策 / 执行」三层。

2. **决策：Sandbox Protocol = 单 mTLS HTTP/2 多路复用三组独立 stream**
   - **问题**：传统 sandbox 协议要走 TCP forward / DNS / control 三个独立 channel；每开一个 sandbox 多套 connection + 维护状态。
   - **方案**：走 HTTP/2 multiplex streams。`sdk/go/.../isolation_boundary.proto` 定义 control / DNS / per-connection TCP 三组独立 stream，独立 backpressure。RFC 0012 明确「TCP and DNS use separate accepts so they can be consumed concurrently with independent backpressure」。
   - **Trade-off**：HTTP/2 multiplexing 复杂度高（transport framing 必须被两个 side 同步实现）；多 transport 适配（Unix socket / mTLS / vsock）需各自验证。
   - **可迁移性**：高。任何跨 sandbox 边界的控制 / 数据复用场景（CI sandbox↔control plane、guest↔agent host）都适用 multiplex 思路。

3. **决策：Policy proveness——Z3 SMT solver + binary capability registry + delta comparison**
   - **问题**：agent 动态 policy 修改可能引入全新的 credentialed reach、新 HTTP method 或到达 cloud metadata。
   - **方案**：`openshell-prover/src/model.rs` 把 policy + credentials + binary registry 编码成 SAT constraints；`queries.rs::check_credential_safety` 走 4 类 finding：`link_local_reach` / `l7_bypass_credentialed` / `credential_reach_expansion` / `capability_expansion`。Gateway 调用 prover 检查 baseline vs merged policy 的 delta。
   - **Trade-off**：SMT 在 policy 规模过大时 `resource_limit` (1,024 rules + 4,096 endpoints)，fallback 到 `inconclusive`；GraphQL/MCP/WebSocket 等高级 protocol 暂只覆盖 L4 TCP + REST。
   - **可迁移性**：高。任何需要「policy review before commit」的系统（IAM 变更、K8s NetworkPolicy、S3 bucket policy、CI workflow permission set）都适用 prover-as-pre-commit-hook 模式。

4. **决策：HTTP_PROXY/HTTPS_PROXY 环境变量被故意 ignore）**
   - **问题**：sandbox image 里 ENV 可以设 `HTTPS_PROXY` 指向任意 corporate proxy，绕过 OpenShell 默认路径。
   - **方案**：`crates/openshell-supervisor-network/src/upstream_proxy.rs` 明确「The conventional HTTPS_PROXY / HTTP_PROXY / ALL_PROXY / NO_PROXY variables are intentionally ignored」——仅 TLS CONNECT 走 corporate proxy；plain HTTP 走 direct dial；upstream proxy 作为 CLI 参数由 compute driver 传入。
   - **Trade-off**：需要 driver-supervisor 增加 operator-driven argument；sandbox image 无法自己配置 corporate proxy。
   - **可迁移性**：高。任何需要「sandbox 不能选择自己的 outbound path」的系统都适用。

5. **决策：verified binary identity from /proc + /proc/<pid>/exe 链（missing digest = None）**
   - **问题**：supervisor 路由走的 binary 也许不是 agent 声称的（agent 可以 `exec` 替换）。
   - **方案**：`openshell-sandbox` 走 seccomp user-notification + landlock，在 `exec` 时记录快照，拿到 `BinaryIdentity{executable, ancestors, cmdline_paths}`。TCP open 时随 `PendingTcpOpen` 走 supervisor，未现成识别的 identity 在 mediator 侧永远 deny。`openshell-supervisor-network/src/identity.rs` SHA256 trust-on-first-use binary hash 补足（max 4096 entries + fingerprint 后端检测）。
   - **Trade-off**：路径换成可证路径 syscall + digest computation 在每个连接上有少量开销；「未识别=拒绝」会误伤合法 sandbox update，TOFU cache 设计了 fingerprint （mtime/ctime/dev/ino） 检测 update。
   - **可迁移性**：中。需运行环境有 trusted process observation（适合 K8s/Runc/Linux，不适合 Windows process model）。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | NVIDIA OpenShell | E2B | Daytona | Modal Sandboxes | Claude Code / Codex |
|------|----------------|-----|---------|-----------------|---------------------|
| 隔离哲学 | out-of-process + kernel-level | in-sandbox microVM | in-sandbox developer kernel | in-sandbox gVisor | in-process 边缘检查 |
| Policy 表达 | per-binary / per-host / per-method | 不可 | per-workspace | per-function network | prompt-level |
| 形式化变差 | Z3 SMT pre-commit review | 无 | 无 | 无 | 无 |
| Runtime | Docker/Podman/K8s/VM/MXC | Firecracker microVM | AGPL self-host | gVisor VM | 依赖 provider |
| License | Apache-2.0（MXC 专属） | 闭源商业 | AGPL-3.0 | 闭源 | 闭源 |
| 商业托管 | 无 | 有 | 无 | 有 | 无 |
| GPU 集成 | 通过驱动 | 通过 Firecracker | 无 | 内置原生 | 不可 |

### vs E2B
- **我们更好**：per-binary + per-host + per-method 三维度 L7 policy；Z3 形式化 policy change review；out-of-process enforcement 不依赖 agent 诚实；Docker/Podman/K8s/VM 跨 runtime 一致。
- **竞品更好**：Firecracker microVM 隔离更强（独立 kernel）、冷启动更快；hosted sandbox 用户无需自管。
- **不同目标**：E2B 中心是「code execution sandbox」，OpenShell 中心是「agent runtime enforcement」。E2B 适合「跑 code 一次性」，OpenShell 适合「agent 长期运行」+「需细粒度 policy」。
- **用户迁移成本**：E2B 适配 OpenShell 需重新设计 policy；接 CEO 攻「OpenShell policy enforcement」需要业务不能依赖「E2B Firecracker 超快冷启动」。

### vs Daytona
- **我们更好**：per-binary + per-host + per-method 认证 vs Daytona 走 per-workspace；L7 enforcement vs Daytona 仅在 SDK 侧 guard；kernel-level enforcement vs Daytona 用户态 container；policy pre-commit 形式化 review vs Daytona 无。
- **竞品更好**：AGPL-3.0 self-hostable + IDE integration 更成熟；developer-centric path。
- **不同目标**：Daytona 是「开发者 sandbox」抽象；OpenShell 是「agent runtime enforcement」抽象。Daytona 适合「quickly try out IDE」场景，OpenShell 是「大规模 agent fleet」场景。
- **用户迁移成本**：Daytona 迁移 OpenShell 需要重新设计 policy；OpenShell 迁移 Daytona 需要额外的 workspace-level isolation layer。

### vs Modal Sandboxes
- **我们更好**：open-source (Apache-2.0) vs Modal closed-source；形式化 policy review vs Modal per-function network policy；cross-runtime (Docker/Podman/K8s/VM) vs Modal only VM。
- **竞品更好**：gVisor user-space kernel 隔离；serverless 函数计算 model；function 调用模式网络自动。
- **不同目标**：Modal 是「serverless function computing」中心，OpenShell 是「agent fleet runtime」中心。Modal 适合「short-lived function」，OpenShell 适合「long-lived agent」。
- **用户迁移成本**：Modal 迁移 OpenShell 需重构 serverless model；接 CEO 攻「Modal provider serverless」需要业务能接受开源 + 自管部署。

### vs Claude Code / Codex 内置 permissions
- **我们更好**：out-of-process enforcement vs in-process guardrails；跨所有 LLM provider（不绑定 Claude / Codex）vs 依赖 provider 本身诚实；kernel-level network 拦截 vs SDK 侧检查；形式化 policy review vs「人工 review」。
- **竞品更好**：与产品迭代同步集成；使用门槛低。
- **不同目标**：Claude Code / Codex 内置 permissions 是「用户体验侧」抽象，OpenShell 是「enterprise security」抽象。
- **用户迁移成本**：低。两者不冲突——企业可在 Claude Code / Codex 背后额外套一层 OpenShell 作为 enforcement layer。

### 综合竞争结论
- **差异化护城河**：技术护城河（out-of-process + kernel enforcement + Z3 形式化）+ 生态护城河（与 NemoClaw 并列发布 + cross-runtime + 提供给所有 LLM provider）+ 信任护城河（NVIDIA sponsor + Apache-2.0 + Vouch system）。其中「形式化 review」是最难复制的护城河。
- **竞争风险**：最可能被「Daytona + form-verifier 集成（如果 Daytona 接上 OPA / Regorus + Z3）」复制；社区层面可能被「agent SDK 内置 policy layer」复制。
- **生态定位**：扮演「policy enforcement for multi-agent fleet」角色，是 CI/CD 纪律 + container security + formal methods 在 LLM agent 领域的新交叉口。与 NemoClaw（agent runtime）+ NeMo（model runtime）+ cuda-rust（CUDA runtime）一起构成 NVIDIA 的 agent stack。

## 套利机会分析

- **信息差**：这个项目虽然有 14K stars，但它不是大众热门——大多数对「agent 安全」的关注仍然停留在 Claude Code 内置 permissions 与 E2B 商业 sandbox，对「out-of-process + 形式化 + 多 runtime」三条线交叉的项目认知很低。文章中是难得的「全栈介绍」窗口。
- **技术借鉴**：7 个可复用 pattern（type-state lifecycle / isolation backend trait / outer fence guarantees / driver-passed enterprise config / per-tool L7 authorization / client-go style sub-client / vouch system）可以直接拿到 KMS、TEE attestation、CI runner、K8s NetworkPolicy、API gateway rule set、terraform plan review。
- **生态位**：填补「policy engine + form verifier + out-of-process」象限——E2B/Daytona/Modal 都不占据这个位置，NVIDIA 全栈优势让它能够：
  - 整合 GPU kernel scheduler + sandbox + LLM runtime（不会出现在 agent SDK 项目中）
  - 整合 Z3 SMT prover + Rego policy + Landlock/seccomp（不会出现在传统 sandbox 项目中）
- **趋势判断**：是不是增长——8 个月拿到 14K stars + 99 releases + 30+ 名 NVIDIA 内部团队 + GTC 2026 公开亮相，符合「AI agent 进入企业生产」的长趋势。LLM 越强、in-process guardrails 越脆弱、OpenShell 这种 out-of-process 价值越大——后发优势稳定。

## 风险与不足

- **正处于 v0.x 公测早期**：fix 占 52.5% commits、134 个 tag 平均每周 3-4 个、`.agents/skills` 才进入 Top 10 热点——架构定型后主要在修边角，重大重构还没发生。
- **企业代理 proxy 与企业网络实际有冲突**：issue #1792 揭示当前 L7 proxy 在 HTTP_PROXY / HTTPS_PROXY 企业代理环境下的盲点虽被故意 ignore，但是未来企业实际部署中需重视。
- **形式化 verifier 规模限制**：SMT 在 policy 规模过大时 `resource_limit` (1,024 rules + 4,096 endpoints)，需 fallback 到 `inconclusive`；GraphQL / MCP / WebSocket 暂只覆盖 L4 TCP + REST——需要 prover 补齐高级 protocol 模型。
- **MXC Windows driver 不开源**：open-core 模式保护 NVIDIA 商业能力，但意味着 Windows 开发者不能跟 Linux/macOS 一样获得同等能力。
- **注释比例偏低（6.9%）**：代码自描述能力较弱，需重点看 `architecture/*.md` / `rfc/*.md` 承担「文档替代注释」的角色。

## 行动建议

- **如果你要用它**：企业多 LLM 代理 / 多 sandbox runtime / 多 K8s tenant 场景优先；个人 / 小团队使用 Claude Code 内置 permissions + E2B 已足够；GPU + LLM runtime 一起调度场景考虑。
- **如果你要学它**：重点关注 5 个文件：
  1. `crates/openshell-isolation-interface/src/contract.rs`（1075 行 type-state lifecycle）——理解 OpenShell 最核心的「verify before execute」
  2. `crates/openshell-prover/README.md` + `src/model.rs`——理解 Z3 encoding + Z3 prover + capability expansion
  3. `crates/openshell-supervisor-network/src/upstream_proxy.rs` 开头 200 行——理解为什么 HTTP_PROXY 被故意 ignore
  4. `crates/openshell-policy/src/lib.rs`——理解 YAML ↔ proto ↔ Rego 三方互转
  5. `rfc/0001-core-architecture/README.md`——理解 RFC 「core architecture」
- **如果你要 fork 它**：可以从这几个角度补全：
  1. 高级 protocol 形式化（GraphQL / MCP / WebSocket）
  2. 增强企业代理 proxy 支持（HTTP_PROXY / corporate cert injection）
  3. Windows isolation backend（Landlock 不能移植到 Windows，需要 Windows job 对象 + WFP）
  4. eBPF 加速的 supervisor-network（避开 HTTP/2 数据面）

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [已收录](https://deepwiki.com/nvidia/openshell)（访问可能受速率限制） |
| Zread.ai | 未收录 |
| 关联论文 | 无（OpenShell 是工程产品，不是论文驱动项目） |
| 在线 Demo | [Brev Launchable](https://brev.nvidia.com/launchable/deploy/now?launchableID=env-3Ap3tL55zq4a8kew1AuW0FpSLsg) |
| 外部深度文章 | [Add Runtime Controls to AI Agents with NVIDIA OpenShell](https://developer.nvidia.com/blog/add-runtime-controls-to-ai-agents-with-nvidia-openshell/) |
| 官方文档 | [https://docs.nvidia.com/openshell/latest/](https://docs.nvidia.com/openshell/latest/) |
# GitHub推荐：2 月 13k star：AI 安全 Agent 的 Route-First 作战契约

> GitHub: https://github.com/zhaoxuya520/reverse-skill

## 一句话总结
把 AI Agent 在逆向与渗透场景下「不知道选什么工具、不知道何时动手、结果如何审计」三大不确定性问题，拆成「PRIMARY 快路径路由 + 双层授权 gate + Evidence→Finding→Path 证据链」三层确定性骨架。

## 值得关注的理由

1. **罕见的「确定性骨架约束概率性 Agent」范式**：业余作者 2.3 个月做到 13,325 stars / 1,995 forks，靠的不是某条命令 prompt，而是一套跨宿主 Agent 的工作流契约——这种把 harness 当作产品核心的设计思路，比单纯的 skill 数量更值得抄。
2. **重新定义「能力就绪」**：ToolDiscovery 把"命令存在、MCP 注册、服务在线、协议握手"拆成四个独立状态，再合成 Ready——比大多数 agent 项目「`which tool` 在就行」粗粒度检测更接近真实执行条件，可直接迁移到任何 MCP/插件生态。
3. **把安全工程的整套成熟概念搬进 Agent harness**：scope gate（来源 Rules of Engagement）、Evidence→Finding→Path（来源取证审计链）、tool-index（来源 CMDB）、manifest + SHA256（来源供应链白名单）——跨域知识迁移做得干净，且同时正面处理「Agent 读了但不做」这一通用问题。

## 项目展示

![reverse-skill 项目标识](https://raw.githubusercontent.com/zhaoxuya520/reverse-skill/main/reverse-skill.png)

![Star History](https://raw.githubusercontent.com/zhaoxuya520/reverse-skill/main/docs/assets/star-history.svg)

[作者博客：逆向与渗透测试工作流系列文章](https://blog.hahacc.com) — 含《逆向与渗透测试工作流：从方法论到实战的完整体系》

> 仅保留 README 中 verified=true 的 2 张素材 + 博客入口；项目其余展示多为 badge/状态图标，无产品演示 GIF/MP4。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/zhaoxuya520/reverse-skill |
| Star / Fork | 13,325 / 1,995（Watcher 59） |
| 代码行数 | 47,153 行（不含注释；含注释 132,154 行） |
| 语言分布 | JSON 79.4% / PowerShell 9.7% / Shell 5.6% / Java 3.4% / 其他 1.9%（GitHub 主页按字符口径计 PowerShell 44%、Shell 25%、Java 24.7%） |
| 项目年龄 | 2.3 个月（创建 2026-05-13，首次提交 2026-05-24） |
| 开发阶段 | 密集开发（近 30 天 39 commits，近 90 天 104 commits） |
| 开发模式 | 业余 Side Project（周末占比 41.3% + 深夜占比 42.3%） |
| 贡献模式 | 核心少数 + 社区（Top 贡献者占比 69.4%，主作者 65.7%） |
| 热度定位 | 大众热门（爆发型增长，受 Anthropic 安全审查影响可能波动） |
| 质量评级 | 代码 B / 文档 A- / 测试 C+ / CI/CD D+ |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

ZhaoXu（zhaoxuya520），独立安全工程师，账号 2.8 年，174 粉丝，公开仓库 20 个。此 repo 在作者最近活跃仓库中排第 1，投入权重极高。作者博客自述「写代码、搞安全、瞎折腾」，发布过《逆向与渗透测试工作流》系列文章；GitHub 主要项目集中在 AI 工作流与安全工具方向。其博客文章《逆向与渗透测试工作流：从方法论到实战的完整体系》明确将项目定位为「14 个技能模块、40 余个 CTF 子技能组成的完整渗透方法论」。

### 问题判断

作者看到的核心矛盾不是「模型不会某条命令」，而是 Agent 缺少安全工作的控制结构：同一句模糊需求可能需要 jadx、Frida、IDA、Burp 或完全不同的 playbook；工具存在性、MCP 注册与服务在线又是三种不同状态；即使执行成功，没有 scope、时间线和证据引用也无法形成可信结论。Issue #21 与 #1 进一步揭示了双重摩擦：仓库自己的授权门禁要避免越界，宿主模型/客户端还可能重复安全审查而不执行。作者因此把「方法选择」「授权边界」「执行状态」「证据质量」当成同一个系统问题，而不是继续增加 prompt 数量。

### 解法哲学

项目哲学是「确定性骨架约束概率性 Agent」。自然语言负责领域方法论，脚本负责能机械校验的部分：`master-route.ps1` 给出 PRIMARY，`case-init.ps1` 生成 case 状态，`case-guard.ps1` 检查 ACT 门槛，`ToolDiscovery.ps1` 解析本机能力，`append-evidence.ps1` 固化证据格式。作者明确拒绝做 Z3r0 式 React/FastAPI/PostgreSQL 多 Agent 运行时，用文件系统换取可移植、可 diff、低部署成本——让不同宿主 Agent（Claude Code/Codex CLI/Cursor/Cline/Kiro）都能消费同一套契约。代价是无法获得数据库级不可变性、并发控制和强制权限隔离。

### 战略意图

项目位于 MCP 执行层与重型 PentestAgent 平台之间的「策略与工作流层」，向下连接 IDA/Burp/jshook/anything-analyzer，向上向不同 AI 客户端提供统一规则。增长点不是无边界堆 skill，而是路由精度、工具生态接入质量、case 契约的机器可验证性、field-journal 的可信复用。赞助/商务邮箱说明存在服务化可能，但当前更像开源方法论与集成资产；真正可持续的护城河将取决于经过实战验证的 precedent、工具适配和回归样例，而不是 Markdown 数量。

## 核心价值提炼

### 创新之处

1. **PRIMARY + Secondary 的轻量可解释路由器**（新颖 3 / 实用 5 / 迁移 5）：用正则命中计数 + 固定优先级 + 冲突排除 + confidence 输出，把自然语言任务转成可审计的单一入口，同时保留跨模块 secondary。
2. **双层安全/执行门禁**（新颖 4 / 实用 4 / 迁移 5）：scope/auth/network_profile 防越界 + precedent 和服从性工程减少已授权场景中的无效停顿；分别建模「安全」与「可执行性」两个失败维度。
3. **Evidence→Finding→Path 统一逆向与渗透的输出语义**（新颖 4 / 实用 5 / 迁移 5）：同一结构既能表达攻击路径，也能表达调用流和 CTF 解题路径；Finding 必须链接 Evidence，Path 每步可链接二者——把报告从自由文本提升为半结构化知识图谱。
4. **能力就绪度四分法**（新颖 4 / 实用 5 / 迁移 5）：tool_available / mcp_registered / service_online / mcp_http_verified 四种独立状态，比单一布尔值更接近真实执行条件。
5. **Manifest 白名单 + GitHub digest 的 Agent 自举**（新颖 3 / 实用 5 / 迁移 5）：Agent 不能自由发明 capability；下载优先固定 SHA256，失败即删除；商业工具显式 manual-only。
6. **服从性工程被当作产品基础设施**（新颖 4 / 实用 4 / 迁移 4）：critical-first、RFC 2119、首尾注意力布局、借口反驳表、完成前自检、next-step menu——正面处理 Agent 「读了但不做」的 harness 问题。
7. **用纯文本模拟作战控制平面**（新颖 3 / 实用 4 / 迁移 5）：scope、workitems、timeline、evidence、report 共构无数据库 case store，角色切换与 handoff 通过字段和追加记录表达。
8. **可写回知识库的供应链防线**（新颖 4 / 实用 4 / 迁移 4）：field-journal 不只是经验目录，还配套脱敏要求、PR 文件白名单、注入/密钥/IP/可执行链接扫描——意识到「让 Agent 自我进化」本身创造新的 prompt 供应链攻击面。

### 可复用的模式与技巧

1. **快路径 + 全矩阵渐进披露**：先用短规则选 PRIMARY，仅在歧义时加载完整路由表——降低上下文噪声；适用任何 skill/plugin 数量多、上下文预算有限的 Agent 平台。
2. **授权状态机外化**：把授权、资产、网络模式、out-of-scope、ready 写入可校验文件——而不是聊天中的口头确认；适用安全、运维、财务、数据治理等高影响操作。
3. **观察与判断分离**：Evidence 保存原始可复现观察，Finding 保存解释与置信度，Path 保存因果/步骤关系——适用调试、事故复盘、实验报告、合规审计。
4. **能力就绪度分层**：区分二进制存在、配置注册、服务在线、协议握手成功，不用单一布尔值代表复杂集成——适用 MCP、IDE 插件、浏览器自动化、微服务依赖。
5. **Manifest 限权执行器**：模型只选择 capability 名，确定性代码负责依赖展开、安装、校验和配置，拒绝未知名称——适用 Agent 自动安装依赖、执行运维动作或调用内部工具。
6. **逻辑角色映射**：不必启动多个 Agent，也可用角色标签、handoff 条件和交付物建立职责边界——适用单 Agent 承担多专业阶段但需要可回放责任链的流程。
7. **机器本地 SoT + 可再生成派生视图**：工具状态扫描后同时生成 Markdown 与 JSON，文档给人/模型读，JSON 给脚本消费——适用开发环境盘点、能力注册表、跨主机工具链。
8. **可写知识库的窄门 CI**：自动贡献只开放到特定目录/格式，限制文件数和大小，并扫描注入、秘密和真实资产信息——适用 Agent memory、自动复盘、社区 runbook。
9. **失败次数预算**：同一路径失败 2–3 次必须切换方案，单命令重复 3 次停止，工具调用达到预算时上报——防止自主 Agent 陷入重试循环和成本失控。
10. **安全安装的分级降级**：固定 hash > API digest > 记录 hash 并警告 > manual-required——而不是校验条件不完美就静默放行；适用多来源插件和开发工具安装器。

### 关键设计决策

1. **PRIMARY 快路径与三轴全矩阵分层**（可迁移性：高）：常见任务先由 MASTER-ROUTING 输出单一 PRIMARY，模糊任务再加载 routing.md 三轴全表，未命中回 R0 提示查全表而不是伪造能力——节省上下文且结果可回归，但脚本是关键词正则计数+固定优先级，不是真正理解三轴语义，新增领域需同步五处真相源。

2. **Hint 命中采用「累积分数 + 显式优先级 + 歧义排除」而非硬塞**（可迁移性：高）：每个正则命中向候选集加一个路由 ID，同一路由多次命中累积分数，最高分胜出同分按 priority 决定——透明、可解释、低成本，比「第一个关键词获胜」稳健；但分数本质上是规则命中次数，无法衡量短语权重，宽词仍可能引入噪声。

3. **双层 gate——文档授权契约 + 脚本 scope guard**（可迁移性：高）：RULES.md 先声明授权原则，case-init.ps1 把 auth、in_scope、out_of_scope、network_profile、ready_for_act 写入 scope.md，case-guard.ps1 解析后以 exit 2 阻断未授权 ACT——把授权从对话语气变为显式状态；但 Markdown 可被手改，-Force 会把硬门降为警告。

4. **文件即数据库的 case 生命周期**（可迁移性：高）：case-init.ps1 一次性创建 work/<case>/{scope.md, timeline.md, workitems.md, evidence/, notes/, report/}——零数据库部署、Git/diff 友好、任何 Agent 都能读；缺点是无锁、无事务、无并发保护，适合单人/小团队案例。

5. **Evidence→Finding→Path 作为结论类型系统**（可迁移性：高）：Evidence 记录来源、时间、命令、原文与 hash；Finding 必须引用非空 evidence_ids 并区分 candidate/validated；Path 把攻击、调用流或解题步骤串联到证据和结论——显著提升可审计性，但当前 helper 只生成 Evidence，Finding/Path 仍靠 Agent 手写，「不可变」更多是契约而非实现保证。

6. **工具状态拆成「可执行、注册、在线、协议可用」**（可迁移性：高）：ToolDiscovery 用 command/path/directory/java-jar fallback 解析路径，独立检测 MCP 配置、TCP 端口、/mcp 的 tools/list 握手，按 verificationMode 合成 Ready——避免把「安装完成」误判为「能力可用」，是项目最成熟的工程抽象之一。

7. **Manifest 驱动的白名单自举与完整性校验**（可迁移性：高）：Windows bootstrap 只接受 manifest 中定义的 capability，固定 jadx/apktool 版本与 SHA256，其他 GitHub asset 优先 API digest，不匹配即删除；商业工具显式 manual-required——白名单优于任意 curl|bash；但 pip/git/npm 传递依赖仍未锁定。

8. **Windows 主路径与 Bash/Kali 平行实现**（可迁移性：中）：PowerShell 5.1 作为功能最完整主实现，通用 Bash 兼容 macOS 自带 Bash 3.2，Kali 有独立 manifest——覆盖面广，但 case-init/case-guard/master-route 缺少 Bash 等价脚本。

9. **逻辑角色而非多 Agent 运行时**（可迁移性：高）：role-map.md 把 lead/cie/cpe/cre 等映射到 skill，单一 Agent 在同一会话中切换角色标签——获得分工思维而不承担运行时复杂度，但没有并发、隔离上下文或权限分离。

10. **Field journal 自动进化，但只允许受限内容自动合并**（可迁移性：中）：每次任务结束回写脱敏 journal 并更新索引，GitHub Workflow 只允许 skills/field-journal/*..md、最多 5 文件、单文件 50KB，扫描 prompt injection/HTML/JS/可执行命令/Base64/token/真实公网 IP 后才 auto-merge——把经验闭环与供应链门禁结合，但正则扫描既会误报也会被变体绕过。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | reverse-skill | Security-Skills-Router | PentestAgent | PentestGPT | HackerGPT | MCP Servers |
|------|---------------|------------------------|--------------|------------|-----------|-------------|
| 核心定位 | 路由 + 契约 + 证据链 | 纯路由调度 | 自动渗透执行平台 | 交互式渗透助手 | 安全问答助手 | 工具连接协议 |
| 跨宿主 | Claude/Codex/Cursor/Cline/Kiro | 取决于实现 | 通常自托管 | 单一交互 | 单一交互 | 通用 |
| 授权机制 | scope.md + guard | 取决于实现 | 通常内置 | 通常内置 | 通常内置 | 通常内置 |
| 工具发现 | ToolDiscovery 四分法 | 取决于实现 | 运行时注册 | 运行时注册 | 静态列举 | MCP 注册 |
| 证据结构 | Evidence→Finding→Path | 无 | 通常内置 | 通常内置 | 无 | 无 |
| 实战沉淀 | field-journal 脱敏 | 无 | 取决于实现 | 取决于实现 | 无 | 无 |
| 复杂度 | 中（Markdown 主导） | 低 | 高（多 Agent + DB） | 中 | 低 | 中（生态） |
| License | MIT | 取决于仓库 | 取决于仓库 | 取决于仓库 | 取决于仓库 | MIT |

### 差异化护城河

不是某个正则路由算法，而是「三轴 PRIMARY 路由 + 本机能力真相源 + 授权 case + 证据链 + 脱敏经验反馈」的完整行为链，以及作者持续积累的实战 precedent。单个组件都容易复制，跨组件的一致性和现场经验较难复制。

### 竞争风险

- **最大风险**：宿主 Agent（Claude Code/Cursor）原生支持更强的 skill discovery、permissions、hooks、MCP marketplace 和 memory 后，可能把本项目的控制层吸收；用户在没有外部 harness 的情况下也能消费到等价能力。
- **次要风险**：领域扩张超过维护能力，文档/脚本/平台实现漂移，使轻量优势消失。
- **具体替代场景**：若 Anthropic 收紧逆向类 prompt 审查（参考 issue #1/#14），本项目双层 gate 中的「宿主审查」侧可能阻塞关键路径，用户会流向 PentestAgent 这类本地执行平台或自定义脚本。

### 生态定位

最合理的位置是「安全领域的 Agent harness / reference implementation」：位于模型客户端与安全工具/MCP 之间，提供可移植策略、最小状态和报告契约，而不是与重型 PentestAgent 平台正面竞争。与 MCP Servers 是互补关系——reverse-skill 负责路由/scope/证据，官方 MCP 负责精确工具能力。

## 套利机会分析

- **信息差**：项目在 GitHub 中文安全圈已达极高关注度（13k+ star），不属于「低关注度高质量」；真正价值在于「AI Agent Skills + 网络安全 + MCP 工具编排」三轴交叉点的稀缺性——这一交叉目前没有等量级对手。
- **技术借鉴**：可直接迁移到其他 Agent 项目的设计包括：①PRIMARY + Secondary 快路径路由；②Evidence→Finding→Path 三段式输出；③ToolDiscovery 四分法能力检测；④Manifest 白名单自举；⑤scope guard 授权状态机。其中 ① 和 ③ 在任何多 skill / 多工具系统都适用。
- **生态位**：填补「Agent 安全作业控制平面」的空白——上接 MCP 执行层，下接具体安全工具，左接 Prompt 工程方法论，右接软件供应链加固。在 Claude Code 等宿主尚未提供等价能力前，是开源侧的最佳替代。
- **趋势判断**：随着 Claude Code、Cursor 等客户端逐步开放 hooks/permissions/MCP marketplace，开箱即用能力会侵蚀本项目的部分价值；但 Evidence→Finding→Path 和 Manifest 白名单这类工程抽象短期内不会下沉到客户端默认能力。同时 Anthropic/OpenAI 持续加强安全审查（issue #1 体现），会增加本项目双层 gate 的相对价值。

## 风险与不足

1. **测试覆盖显著不足**：仅 smoke.ps1 + verify-routing-coherence.ps1 + test-p0-friction.ps1 三个端到端脚本，0 单元测试；领域 skill、Bash bootstrap、MCP 集成和真实安装缺少自动化测试。
2. **CI 与项目主张不匹配**：仓库声称有强路由、门禁、完整性和跨平台能力，但 GitHub Actions 只审核 field-journal；smoke/coherence/Pester/ShellCheck/Linux/macOS dry-run 未接入 PR 门禁。
3. **Refactor 几乎为 0**：v1→v2 没有重大重构历史，伴随近 12 万行 Markdown 的快速增长，技术债与文档漂移风险正在累积。
4. **证据不可变性是契约而非实现**：相同 Evidence ID 会覆盖文件，INDEX 可追加重复记录；Finding/Path 没有 schema validator 或引用完整性检查。
5. **供应链加固不完整**：固定 release hash 能保护直接下载，不能锁定 pip/npm/git 的传递依赖；Kali manifest 与 Linux/macOS 实现存在平台漂移。
6. **scope gate 是流程门而非安全边界**：case-guard -Force 可绕过；Markdown 状态可被 Agent/用户手改；要用于真实组织必须接宿主 hook/工具代理层。
7. **跨平台不完整**：case-init / case-guard / master-route 缺少 Bash 等价脚本，Linux/macOS 常退回「读 Markdown 或安装 pwsh」。
8. **宿主模型审查可能反复阻断**：issue #1/#14 显示 Claude 安全审查与项目 scope gate 存在冲突；项目用 RULES.md + precedent-reverse.md / precedent-pentest.md 等进行「借口反驳」，但跨客户端一致性是长期挑战。

## 行动建议

- **如果你要用它**：作为 Claude Code/Codex CLI 的外挂 skill 包使用（按 README_AI.md 注入全局规则后启动），优先用 master-route.ps1 路由而非手动选 skill；案例必须走 case-init.ps1 创建 work/<case>/，不要跳过 scope.md 直接开干。需评估目标客户端是否对逆向类 prompt 友好（issue #1 提示某些场景会被审查阻断）。
- **如果你要学它**：重点关注 `skills/scripts/master-route.ps1`（40 槽路由 + 累积分数 + 冲突排除）、`skills/scripts/lib/ToolDiscovery.ps1`（四分法能力检测）、`skills/ops/scope-contract.md` + `case-guard.ps1`（双层 gate）、`skills/scripts/append-evidence.ps1`（证据格式校验）、`skills/llm-security/`（服从性工程 + 借口反驳表）。这些是可迁移性最高的资产。
- **如果你要 fork 它**：①把 CI 补齐为 PR 门禁：smoke.ps1 + verify-routing-coherence.ps1 + Pester + ShellCheck + Linux/macOS dry-run；②把 README/routing.md/MASTER-ROUTING.md/labels/regex/priority 统一为一份结构化路由 manifest，避免五处真相源；③给 Evidence/Path/Finding 加 schema validator 和原子写；④把 Manifest 白名单扩展到 pip/npm/git 传递依赖 lockfile；⑤把 case-guard -Force 标记为审计事件而不是默认行为；⑥扩展到非安全领域——快路径路由、ToolDiscovery 四分法、Evidence→Finding→Path 都与领域无关，可独立抽出。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/zhaoxuya520/reverse-skill |
| Zread.ai | https://zread.ai/zhaoxuya520/reverse-skill （采集时未确认收录） |
| 关联论文 | 无 |
| 在线 Demo | 无（项目本身是 Agent skill 包，需在 Claude Code 等宿主中运行） |
| 作者博客 | https://blog.hahacc.com |
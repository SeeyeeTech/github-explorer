# GitHub 推荐：5.6k★ 跨 19 个 AI Agent 的 Skills 注册中心：每条都过 Snyk 扫描

> GitHub: https://github.com/tech-leads-club/agent-skills

## 一句话总结

tech-leads-club/agent-skills 是 Anthropic Skills 开放标准下第一个 vendor-neutral 的硬化（safe-by-default）注册中心，把 AI Agent 的工作流封装成可跨 19 个 Agent 复用的 SKILL.md 包，每条都过 Snyk Agent Scan、加内容哈希、配 lockfile，解决了「13.4% 市集 skill 含严重漏洞」这一行业新攻击面。

## 值得关注的理由

- **它站位的就是 Anthropic 官方 Skills Directory 没做的那一块**:vendor-neutral + 安全硬化 + 跨 Agent，而非单 Agent 绑定，这正好踩在 2025 末 MCP 协议普及 + Anthropic 开放 Skills 格式的窗口上。
- **真正的产品价值在基础设施，不在 92 条 skill 本身**:port/adapter 六边形架构、Zod + 原子写入 lockfile、lstat+revalidate 路径防御这套「防御纵深」是任何面向 LLM 的工具包都可照搬的范式。
- **AI-native 软件工程的方法论样本**:tlc-spec-driven 的 5 个 Python 闭包门（closure-gate）+ RFC #150 的「作者≠验证者 + 判别传感器」，把 AI 工作流从「LLM 记得跑」升级为「OS exit code 强制」——这是 AI 工作流工程化的可复用范本。

## 项目展示

![Tech Leads Club Logo](https://raw.githubusercontent.com/tech-leads-club/agent-skills/main/.github/assets/logo.png)

![Star History Chart](https://api.star-history.com/svg?repos=tech-leads-club/agent-skills&type=Date)

> 官网主页（https://agent-skills.techleads.club)WebFetch 返回 403,README 与官网都缺架构图、终端截图、Demo GIF，对新用户理解「装上之后到底长什么样」不够友好，这是项目本身的展示短板。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/tech-leads-club/agent-skills |
| Star / Fork | 5,634 / 499 |
| Watcher | 69 |
| License | MIT（引擎）+ CC-BY-4.0(skills)+ 第三方原许可 |
| 默认分支 | main |
| 代码行数 | 75,444 行 / 1,101 文件 |
| 语言分布 | JSON 50.7% / TypeScript 18.5% / Python 15.3% / TSX 10.9% / 其他 4.7% |
| 注释比 | 1.05（注释行 ≥ 代码行，内容型仓库特征） |
| 项目年龄 | 7.8 个月（2026-01-19 首次提交） |
| 总 commit | 1,194 |
| 最近提交 | 2026-09-12 |
| 开发阶段 | 密集开发（近 90 天 164 commit） |
| 贡献模式 | 核心少数 + 社区（18 人，Felipe Rodrigues 占 65.7%） |
| 热度定位 | 大众热门（5.6k★、月均 ~720 Star 增长） |
| Release | v1.5.0 / 82 tag / 80 release / 月均 10+ 发版 |
| 依赖 | runtime 0 / dev 38(Nx monorepo + Jest 30 + fast-check + Zod) |
| 质量评级 | 代码 优秀 / 文档 优秀 / 测试 基本（test 占比 1.0%，缺口在 marketplace/mcp） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

TechLeads.club 是 3.4 年历史的巴西软件领导力社区，旗舰开源仓库就是本仓库（13 个公开仓中 Star 最高）；旗下另有 `awesome-tech-lead` （515★） 与 `harness-toolkit` (251★)，可见团队把 「agent skills」 当成社区技术品牌的核心载体。核心维护者 Felipe Rodrigues 一直把「NPM 包管理思想 + CI 供应链安全」搬到 AI Agent 领域——lockfile、内容哈希、Snyk Agent Scan、原子写入都不是凭空发明，而是从传统包管理与 DevSecOps 复用过来的成熟模式。Bio 是「Comunidade Brasileira de desenvolvimento de software e liderança técnica」，社区驱动而非公司产品。

### 问题判断

作者对行业的横向观察（Snyk Agent Scan 报告称 13.4% 市集 skill 含 critical 漏洞）显示他们关注的是「Skills 作为新攻击面」的真实痛点——Issue #114「Supply Chain + Indirect Prompt Injection on @latest skill loading」直接把这条供应链攻击面写在标题里。时机判断精准：2025-09 启动，正好在 MCP 协议被广泛接受 + Anthropic 推出 Skills 开放格式的前夜；TLC 抓住了「vendor-neutral + secure-by-default」这一差异化窗口。

### 解法哲学

**Unix 哲学 + 开放 + 受治理**:

- CLI / MCP / marketplace 三入口共享同一 catalog，但语义不同（安装 / 搜索+读取 / 浏览）
- CLI 默认 Ink TUI 交互，无 flag 时启动 React 向导，同时保留 Commander 纯函数供脚本调用——「interactive-by-default but script-friendly」
- 混合许可显式拆分：引擎 MIT（代码集成友好）+ skills CC-BY-4.0（强制署名）+ 第三方原许可保留

**明确不做什么**（往往比 feature 列表更有价值）:

- 不做自有 Agent（不像 Continue 那样做 IDE 集成）
- 不做签名验证（NVIDIA/skills 走的路；TLC 走 Snyk + 内容哈希）
- 不做自动化 skill 执行 sandbox(MCP 端是只读 stdio server，不直接执行 skill 内容）

### 战略意图

**核心产品**（不是基础设施）:TLC 旗舰仓库，975+ star 量级，与 harness-toolkit 形成 「skill 仓库 + harness 库」 双柱。商业化方面 SaaS/托管版未见，但 Nx Cloud 集成 + jsDelivr CDN + 审计日志结构已有 SaaS 化潜在线索；开源策略是 **genuinely open**（不是 open-core)，无 enterprise edition，无付费 skill。

## 核心价值提炼

### 创新之处

按新颖度×实用性排序：

1. **Deterministic Python Gates for LLM Workflow**（新颖 5/5 × 实用 5/5):tlc-spec-driven 自带 5 个 stdlib-only Python 脚本（`validate_spec.py` / `validate_tasks.py` / `check_commit.py` / `validate_state.py` / `lessons.py`)，作为 closure-gate 在 commit / spec 提交 / state 关闭前必须 exit 0——把 LLM workflow 的关键检查从「模型礼貌承诺」升级为「OS exit code 强制」。
2. **Author ≠ Verifier + Discrimination Sensor**（新颖 5/5 × 实用 5/5,RFC #150 方向）:Execute 阶段后必跑独立 Verifier sub-agent；注入 behavior-level mutation 确认 tests 能杀死突变体；clean PASS 不记录 lesson——这是变异测试与 LLM 流程结合的工业实践。
3. **Progressive Disclosure MCP Tool Set**（新颖 4/5 × 实用 5/5):5 个 tool 按工作流切分（search/list/read/fetch/prepare）;core/tool 分层让单测绕过 fastmcp 的 ESM 限制；精确控制 token budget。
4. **Skill Description Protocol**（新颖 4/5 × 实用 5/5):`[What] + [Use when ...] + [Do NOT use for ...]` + < 1024 chars + 无 XML 角括号；缺 「Use when」 或 「Do NOT use for」 直接 fail validate-skills.ts——把 skill 描述质量从建议变硬约束。
5. **Triple-Walled Path Defense**（新颖 3/5 × 实用 5/5):sanitize + isPathSafe + lstat+revalidate 三道闸防 symlink / TOCTOU / 循环链接。
6. **Issue-First Governance**（新颖 3/5 × 实用 4/5)：非 member 必须先 issue → maintainer 同意 → 才被授 push 或由 maintainer 代实现并给 credit。

### 可复用的模式与技巧

可直接迁移到其他项目：

1. **Ports & Adapters 六边形核心**(TS):`CorePorts` 接口聚合 fs/env/http/logger/shell/paths/package-resolver 七端口；CLI 和 MCP 共享同一业务服务，单测不碰真实 fs/http。
2. **Sanitize + isPathSafe + lstat 链**：任何处理「用户提供的字符串 → 文件系统路径」的代码都应同时上两道闸；`lstat` 防 TOCTOU,Windows 切换到 junction。
3. **Atomic write with backup**:write → rename(temp → final) + backup .backup 文件 + Zod graceful migration；任何 dotfile / config CLI 都应照搬。
4. **Zod-validated JSON state file with graceful migration**:schema mismatch 不抛异常，回退到空 v(N) state；旧版本 inline 升级。
5. **Tool-thin / logic-core split**:tool 文件只 import SDK，业务逻辑放在 core/——适用 ESM-only SDK wrapper(fastmcp、linear SDK 等）。
6. **Deterministic gate before review**：把 AI workflow 的结构检查写成 OS-exit-code 脚本。
7. **Progressive disclosure for LLM catalogs**:search/list/read/fetch 切分控制 token budget；适用所有 LLM-facing 数据目录/RAG tool。
8. **Skill description protocol with positive + negative triggers**:1024 chars 上限 + 必须含 Use when + Do NOT use for。

### 关键设计决策

值得学习的架构选择与 trade-off:

| 决策 | Trade-off |
|------|-----------|
| 六边形架构（ports/adapters） | 多 7 个 adapter 样板文件，换完全可测试性 + 跨 runtime（Deno/Bun/WASM）移植性 + 安全不变量集中在 core 层 |
| CLI 双模式（Commander + Ink TUI） | 两套代码路径需同步，换脚本永不阻塞在 Ink `useInput` + 用户友好 |
| 锁文件三段式（Zod + atomic write + graceful migration） | 写入路径变长，换任何中断 lockfile 不变无效状态 + Zod 失败 silent recovery |
| 路径双重防御（Sanitize + Verify） | 双重检查在小项目显 over-engineered，换防 symlink + relative path + 编码 trick |
| symlink 用 `lstat` + 目标 revalidate + ELOOP 强清 | 多 2 次 syscall，换完全防 TOCTOU + 路径遍历 + 循环链接 |
| 主动下线 OpenCode(Issue #123) | 失去「覆盖最多 Agent」的 marketing 点，换「长期维护性 > 兼容数量」的工程原则 |
| RFC #150 升级 tlc-spec-driven 到「崩溃可恢复 + 授权感知」 | 模糊「skill vs Agent」边界，换同类 skill 事实标准的潜在位置 |

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | TLC agent-skills | anthropics/skills | NVIDIA/skills | Skills.sh / ClawHub / HF Skills |
|------|----------|------------------|---------------|--------------------------------|
| Agent 兼容矩阵 | **19 个** | 1 个（Claude Code） | NVIDIA 生态绑定 | 取决于 skill |
| 安全扫描 | Snyk Agent Scan + lockfile + 内容哈希 + 审计日志 | 无 | 签名验证（cryptographic proof） | 无（13.4% 含 critical） |
| 安装入口 | CLI + MCP + Marketplace | Claude Code only | NVIDIA 渠道 | 自由上传 |
| 许可 | MIT（代码）+ CC-BY-4.0(skills) | Anthropic license | NVIDIA license | 各异 |
| 治理 | Issue-first + AI 辅助披露 + 贡献 credit | 内部审查 | 内部开发 | 自由集市 |
| Skill 数量 | 92 / 14 类 | 起步阶段 | 中等 | 大但质量参差 |
| skill description 协议 | 强制 Use when + Do NOT use for | 自由 | 自由 | 自由 |
| 跨 Agent 可移植 | 高（SKILL.md 兼容） | 否 | 否 | 中 |

### 差异化护城河

TLC 有竞品都未同时具备的三道护城河：

- **信任护城河**:13.4% vs 0% 的安全声明 + Snyk + lockfile + 审计日志
- **生态护城河**:19 Agent 兼容矩阵 + 92 skills × 14 类 + 上游消费社区市场 skill(12 个 `openai/skills`、18 个 `agent-gtm-skills` 等）——定位是「上游策展」而非「竞争替代」
- **治理护城河**:issue-first + credit + AI 辅助披露

**技术护城河较弱**（无独家算法），但 ≥ 商业护城河（vendor lock-in）。

### 竞争风险

- **最可能被 Anthropic 官方 Skills Directory 替代**：如果 Anthropic 决定开放跨 Agent 支持，标准制定者的优势会瞬间压过 TLC 的差异化
- **其次是 Snyk 自己下场做 marketplace**：既是裁判又是选手会削弱 TLC 的安全卖点
- **风险最低的是社区市场**:TLC 反向上游消费它们的 skill，用户重叠度低

### 生态定位

**跨 Agent 的 skill 策展层 / 安全分发层**——定位类似 Linux 发行版的 「security-focused LTS」，不做最广泛，但做最可信。在整个技术生态中扮演「让 AI Agent 工作流从散落 prompt 升级为可治理软件包」的中介角色。

## 套利机会分析

- **信息差**:Skills 注册中心赛道仍处早期（2025 末才由 Anthropic 推出开放格式）,TLC 是 19 Agent 兼容 + Snyk 加固的早期占位者，但 5.6k★ 已不再是「低关注度」
- **技术借鉴**:Port/Adapter 六边形 + Zod + atomic write + lstat+revalidate 这一整套防御纵深，任何做 LLM-facing 工具/CLI/MCP server 的人都可照搬
- **生态位**：填补了 Anthropic 官方目录（单 Agent）与社区市场（无安全）之间的空白
- **趋势判断**:Skills 生态在 2026 处于爆发前夜；但 TLC 已 7.8 个月，后发优势不在；真正的护城河是治理与流程，而非技术独创

## 风险与不足

- **Bus factor 高**:Felipe Rodrigues 一人占 65.7% 提交（784/1194）,Top2 edmarpaulino 仅 9.6%,Bot 7.5%，其余 17% 散点；核心维护者淡出会带来供应链断档
- **测试覆盖率偏低**:commit 类型中 test 仅 1.0%(2/200),refactor 1.5%——技能内容型仓库缺乏自动化测试是工程成熟度短板，尤其 marketplace/mcp 包几乎无单测
- **展示短板**:README 与官网都缺架构图、终端截图、Demo GIF，新用户难以快速理解「装上之后到底长什么样」
- **官网 WebFetch 返回 403**：连搜索引擎抓取都拿不到 hero/demo,SEO 友好性差
- **商业模式未跑通**:SaaS/托管版未见；Nx Cloud 集成是暗示但非承诺；genuinely open 与商业化如何平衡待解
- **依赖单点风险**：对 Anthropic Skills 开放标准的强绑定——一旦 Anthropic 修改 SKILL.md 规范，需同步跟进

## 行动建议

- **如果你要用它**：在用 Claude Code / Cursor / Copilot 等 Agent，想要「团队共享 + 跨工具 + 安全审计」的工作流，就装它；如果只用单一 Agent 且对安全无强要求，直接用各 Agent 内置 prompt 库更轻
- **如果你要学它**:
  - 看 `libs/core/src/lib/utils.ts` 的 `sanitizeName`/`isPathSafe`（双重路径防御）
  - 看 `libs/core/src/lib/services/lockfile.service.ts`(Zod + atomic write + graceful migration 三段式）
  - 看 `packages/cli/src/services/installer.service.ts` 的 symlink `lstat` + revalidate + ELOOP 处理
  - 看 `packages/skills-catalog/skills/(development)/tlc-spec-driven/scripts/` 的 5 个 Python closure-gate
  - 看 `tools/validate-skills.ts`(342 行独立 validator,13 项检查）
  - 看 RFC #150 / PR #153(tlc-spec-driven 的下一阶段方向）
- **如果你要 fork 它**:
  - 加 E2E 测试覆盖 marketplace / mcp 包，补齐 1.0% 测试率的短板
  - 把 SECURITY.md 的「4 道防线」图示化，补 README 架构图
  - 把 RFC #150 的 「Author ≠ Verifier」 模式通用化（做成可复用 skill，供其他 spec-driven workflow 使用）
  - 把 lockfile 改造为可同步（SaaS 化第一步）

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/tech-leads-club/agent-skills |
| Zread.ai | 未收录 |
| 关联论文 | 无 |
| 在线 Demo | MCP server 包 `@tech-leads-club/agent-skills-mcp`（在任何 MCP client 中试用） |
| 关键 Issue | #114(Skills 供应链攻击面）/ #123（主动下线 OpenCode)/ #150(RFC：崩溃可恢复 + 授权感知） |

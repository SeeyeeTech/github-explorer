# GitHub 推荐：Cloudflare 把 Claude Code 改成漏洞猎手：3 个月 13K stars 的对抗式验证实战

> GitHub: https://github.com/cloudflare/security-audit-skill

## 一句话总结

Cloudflare 把内部红队「用 AI 给生产代码做审计」的工作流沉淀成 Claude Code 的可加载 Skill，用对抗式双 agent + 强 schema 约束 + 零依赖 validator，把 LLM 找漏洞常见的「假阳性高 / 边界模糊」问题压到可治理范围。

## 值得关注的理由

- **方法学新锐**：六阶段流水线（recon → hunt → validate → structured output → verification → report）+ 强制「producer ≠ verifier」的对抗验证，是少数把 LLM 漏挖工作流工程化到工业级强度的开源样本
- **AI-AND-LLM.md 独立成文**：把「AI 编码代理自身的威胁」作为一等攻击域，2025-2026 年方法论差异化的关键卖点
- **零依赖 validator + 显式安全边界**：所有 JSON schema 都自实现、字节预算硬上限、O_NOFOLLOW 防 symlink、fail-closed 拒绝 fallback——任何要嵌入 skill/runtime 的 validator 都可借鉴

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/cloudflare/security-audit-skill |
| Star / Fork | 13,688 / 734（49 watchers） |
| 代码行数 | 461 行 JSON（其余 16 个文件全是 Markdown），注释/代码比 2.75:1 |
| 项目年龄 | 3 个月（首次提交 2026-06-18） |
| 开发阶段 | 低维护（近 30 天仅 3 commit，节奏放缓，核心方法论定型） |
| 贡献模式 | 小团队 + 公司主导（Dan Jones 占 55.6%，Top3 占 84.6%） |
| 热度定位 | 大众热门（爆发型：首日 ~1,250 stars，撞上 AI agent 风口） |
| 质量评级 | 代码 A+ / 文档 A+ / 测试 A / CI C |
| License | MIT |
| Release | 无 tag，靠 main 分支直接迭代 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Cloudflare 16.2 年老牌组织账号，575 个公开仓库，16,543 粉丝。本仓库由其安全研究线出品（README 公开邮箱 `security-ai-research@cloudflare.com`），与 Cloudflare Bug Bounty、红队、安全研究同源。核心贡献者 Dan Jones 占 55.6% 提交，是 Cloudflare 内部「用 AI 给生产代码做审计」反复踩坑后的工程化沉淀——属于 dogfooding 路径，而非学术玩具。

### 问题判断

传统 SAST（Snyk / Semgrep / CodeQL）只能找签名级问题，看不到 LLM 能理解的「业务逻辑 / 权限建模 / 二阶注入 / 跨组件信任差」；Anthropic 官方 `security-audit` skill 给的是通识检查清单，没有按攻击域做深度分类，也没有对抗式验证。Phase 1 自检显示**单 agent 单次跑只覆盖约 50%**，需要一个有覆盖率账本 + 多波 hunter + 独立 verifier + budget gate 的工作流。

### 解法哲学

- **简单 vs 功能完整**：选功能完整。六阶段流水线 + 12 个攻击域 companion + 严格 ledger schema + 零依赖 validator，是企业级工艺
- **性能 vs 易用性**：选「易用性以可治理为前提」。SKILL.md 是 markdown，用户调用门槛极低；但执行路径有严格的 sandbox / 写隔离 / 边界检查 / budget gate，要求必须有 OS-enforced sandbox 才能跑 target 代码
- **明确不做什么**：
  - 不开发 payload chain（validation 规则禁止扩展到超出观察到的边界结果）
  - 不测试部署环境（deployment fact 落到 `needs_validation`，由 owner 自己观测）
  - 不让 hunter 自己验证自己（强制 Phase 3 用 fresh verifier）
  - 不让一个 run 声称「覆盖完毕」（Phase 1 自检就揭示了单 agent 单次 50% 覆盖率）

### 战略意图

基础设施 + 间接商业化。README 明说：「seeded Cloudflare's vulnerability discovery harness ... this skill is the single-repo starting point it evolved from」——真正产品是 fleet-wide harness，skill 是单仓入门起点和对外教学/开源版本。开源提升 Cloudflare 安全研究品牌能见度，反向输入内部 harness；同时给「想给 AI 编码代理加 audit 能力」的客户提供参考实现，潜在引流到 Cloudflare AI/安全产品。

## 核心价值提炼

### 创新之处

按新颖度 × 实用性排序：

1. **对抗式双 agent + multi-run 累加证据**（新颖度 4/5，实用性 5/5，可迁移性 4/5）
   - Phase 2 hunter → Phase 3 fresh verifier → Phase 5 fresh re-verifier 三段式强制「产生者 ≠ 验证者」
   - `fingerprint` 跨 run 复用 + multi-run 在 `prior_covered` / `prior_changed_source` 上的连续 carry
   - 模拟「两个独立分析师达成共识」

2. **Coverage ledger = 权威覆盖声明**（新颖度 5/5，实用性 5/5，可迁移性 5/5）
   - 用一份机器可校验的 ledger 取代「agent 数 / README 字数 / 散文段落」作为覆盖证据
   - 「The ledger is the coverage claim. An architecture summary ... is not coverage evidence.」
   - prior run 的 deferred/blocked/out_of_scope 必须被当前 run 重新审视（never suppress a current unit）
   - `attempt` 是 append-only archive

3. **Severity = Likelihood × Impact，且 overall_severity ≤ impact.score**（新颖度 3/5，实用性 5/5，可迁移性 5/5）
   - validator 把这个不等式编码进 schema，拒绝「严重性高于已证实破坏面」的虚报
   - `confirmed` 才有 severity，`needs_validation` 永远没有 severity（unknown 不是 low）

4. **Coverage-critic wave（research agent 只看不跑）**（新颖度 5/5，实用性 5/5，可迁移性 4/5）
   - 每次 hunter 波结束后，强制用一个「只看不动」的 research agent 找 ledger 漏洞（missing_units / reassign_ids / resolved_prior_leads / stop）
   - `quick` profile 严格只跑 1 波 hunter + 1 final critic（不是 evidence of complete coverage，是 pre-declared early stop）

5. **三 verdict 互斥字段 + verdict-specific validation_plan**（新颖度 4/5，实用性 4/5，可迁移性 5/5）
   - `confirmed` / `needs_validation` / `rejected` 三种 verdict 严格分离，各自字段互斥
   - `needs_validation` 必须填 `validation_plan.local` 或 `.deployment` 至少一项且 visible prose
   - deployment 严格定义为 owner-observed check，绝不请求 audit 流量打部署

6. **11 步 no-follow + fstat + byte-bound + exclusive-create 的 artifact promotion**（新颖度 5/5，实用性 5/5，可迁移性 3/5）
   - 把 sandbox 的不可信输出搬到 retained artifacts 的过程，被编码成 11 个不可省略的步骤
   - 拒绝 symlink / FIFO / device / directory / hard-link / changing-file
   - 任何一步失败就保留 `needs_validation` 而非忽略

7. **Fingerprint / canonical_refs 的 source-derived ID**（新颖度 4/5，实用性 5/5，可迁移性 5/5）
   - 不接受 free-form ID；`fingerprint` 必须匹配 `^[A-Za-z0-9][A-Za-z0-9._:/@+-]*$` 且不含 line/wave/agent/severity/verdict
   - `canonical_refs` 用 percent-encoded UTF-8 派生（禁止 lossy slug），相同源对象跨 run 必须使用同一引用

8. **Coverage profile + 严格 budget gate + critic/validation reserve**（新颖度 4/5，实用性 5/5，可迁移性 4/5）
   - `quick / standard / deep / scoped` 四种 profile 在 breadth/redundancy 上变化，但 evidence bar 不变
   - strict budget 必须先 reserve post-wave critic + final-clean critic + validation reserve 才能放 hunters

### 可复用的模式与技巧

1. **Markdown 作为 Agent Skill 协议（SKILL.md frontmatter + verbatim 引用）**：SKILL.md 只写「原则 + 总览 + agent 编排契约」，领域细节放独立 companion，调用时按 ledger unit 的 `selected_companion_blocks` 字段 verbatim 复制到子 agent prompt。**适用所有「AI 多 agent 工作流 + 领域知识分发」场景**
2. **零依赖 JSON Schema 解释器 + 显式安全边界**：自实现 `type/required/additionalProperties/oneOf/enum/pattern/minLength/minimum/minItems/uniqueItems/const/visibleContent` 等关键字，硬编码 5 MiB / 64 层嵌套 / 1k items / 500k values 等上限
3. **Coverage ledger + canonical_refs + attempt archive**：可重放 / 多 run / 多 agent 任务编排的通用骨架
4. **`needs_validation` 作为 first-class verdict**：避免「事实不足就降 severity」的滑坡
5. **verifier ≠ producer 的对抗式验证**：适用任何 AI 生成内容的可信度评估
6. **写隔离 + no-follow + fstat + byte-bound 的 promote 协议**：所有「不可信 sandbox 输出 → 可信 retained store」的场景

### 关键设计决策

| 决策 | 问题 | 方案 | Trade-off | 可迁移性 |
|---|---|---|---|---|
| SKILL.md 192 行只做编排契约 | 上下文窗口有限 + 一次性读完 12 个 md 劝退 | verbatim 复制 companion 到子 agent prompt | 牺牲「打开一个文件看完全部」，换 context 可控 + 子 agent prompt 可机校 | 高 |
| Validator 自实现 JSON Schema 解释器 | 不想让审计 skill 引入 npm 依赖 | Node 内置 fs/path/assert + 自定义关键字子集 | 牺牲 JSON Schema 标准覆盖范围，换 5 MiB 字节预算 + O_NOFOLLOW + visibleContent 防伪 | 高 |
| Fingerprint 必须是 source-derived 稳定 ID | LLM 找漏洞是概率性，描述略变导致 multi-run 数据无法累加 | `^[A-Za-z0-9][A-Za-z0-9._:/@+-]*$` 模式 + 禁止含 line/wave/agent/severity/verdict | 牺牲自由取名的人体工学，换 multi-run 累加证据 | 高 |
| coverage_id 用 percent-encoded 派生 | slug 化命名空间会冲突 | `surface::boundary::subsystem::attack_class(::lifecycle)` 格式 | 牺牲自由 ID，换代码 rename 后旧 ledger 仍可识别 | 中 |
| 报告权威信号是 ledger + structured findings.json | AI 写报告容易夸大覆盖范围 | Phase 6 只能从 records + ledger + hunter hardening notes **derive** REPORT.md | 牺牲「报告可以自由叙述」，换覆盖范围可验证 | 高 |

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | Cloudflare security-audit-skill | Anthropic 官方 skill | MCP 包装版 | 传统 SAST (Snyk/Semgrep/CodeQL) |
|---|---|---|---|---|
| 攻击域覆盖 | 9 companion + 8 普通攻击块 | 通识清单（未做深度分类） | 同质上游 | 签名级（看不到逻辑漏洞） |
| 对抗式验证 | Phase 3/5 双独立 verifier | ✗ | ✗ | ✗ |
| 机器可读 ledger | ✓ (canonical_refs + fingerprint) | ✗ | ✗ | 仅 SARIF 等格式 |
| Multi-run 累加 | ✓ (coverage ledger) | ✗ | ✗ | ✗ |
| AI/LLM 攻击类 | ✓ (AI-AND-LLM.md 独立成文） | 部分 | 部分 | ✗ |
| 写隔离 / sandbox | 11 步 promote procedure | ✗ | ✗ | ✗ |
| 零依赖 validator | ✓ | N/A | N/A | 依赖 ajv 等 |
| 官方背书 | 公司级但非 Claude Code 一等公民 | 一等公民（Anthropic） | 取决于 MCP runtime | 商业产品 |
| 与 Claude Code 同步 | 异步（社区/PR） | 同步 | 同步 | N/A |

### 差异化护城河

唯一同时具备 「LLM 编排 + 对抗式验证 + 严格 schema + 多 run 累加 + 可审计 ledger + zero-dep validator」 的开源安全审计 skill，且每个特性都互锁（fingerprint → multi-run → coverage claim；validator → schema → severity 公式）。**最佳护城河是「持续把 Cloudflare 红队新案例反哺进 skill」，以及「零依赖 validator 让它能嵌到任何 harness」**。

### 竞争风险

- **Anthropic 官方 skill 升级对冲**（官方背书 + Claude Code 同步迭代）—— 但只要保持工程化深度，对抗式验证 + ledger 这一层就不容易被通识清单追平
- **AI SAST 商业产品**（Snyk Agent Scan / Semgrep Assistant）把对抗式验证做成 SaaS —— 但商业产品的闭源会反向凸显本仓库「开源方法学基线 + 可 fork 可审计」的价值

### 生态定位

不是产品，是方法学开源基线 + Cloudflare harness 教学版。在整个 AI agent 安全审计生态中，填补了「开源 + 工程化 + 可机校」这一空白——与传统 SAST 互补（SAST 先扫签名 → LLM skill 做逻辑层），与 Anthropic 官方 skill 形成「工程深度 vs 官方背书」的差异化。

## 套利机会分析

- **信息差**：项目已是大众热门（13K stars），但**绝大部分人只读了 README 不知道里面有整套六阶段流水线 + 零依赖 validator**——值得 fork 后用在自己的代码审计流水线
- **技术借鉴**：
  - 零依赖 JSON Schema 解释器 + 显式安全边界 → 任何要嵌入 skill/runtime 的 validator 都可复用
  - `needs_validation` 作为 first-class verdict → 避免所有「AI 生成内容的事实滑坡」
  - Coverage ledger + canonical_refs + attempt archive → 多 agent 任务编排的通用骨架
  - Markdown 作为 Agent Skill 协议（SKILL.md frontmatter + verbatim 引用）→ 任何 AI 工作流的领域知识分发都适用
- **生态位**：填补了「用 LLM 做端到端漏洞审计」这一空白——传统 SAST 看不到逻辑漏洞，Anthropic 官方 skill 偏通识，本仓库是少数把对抗式验证 + 强 schema 做到工业级的开源样本
- **趋势判断**：符合「AI agent + 安全自动化」的明确方向；比 Anthropic 官方 skill 有后发优势（深度分类 + 对抗式验证）；Issue #20 自检 6 个方法学盲区提示还在演进，长期看 Cloudflare 红队新案例会持续反哺

## 风险与不足

- **CI/CD 缺位**：没有 `.github/workflows` / `CONTRIBUTING.md` / `CHANGELOG.md`，靠 commit message + README 替代
- **端到端测试缺位**：只有 validator 单元测试，没有完整 6 phase 流水线的 E2E（合理：依赖外部 agent runtime）
- **Issue #20 自检发现 6 个方法学盲区**：作者用 seeded target 对照实验，发现 6 个攻击类存在系统性盲区——**项目把「自身方法学缺陷」用 issue 公开，非常少见且诚实，但意味着方法论还在演进**
- **Issue #21 验证器信任边界漏洞**：本地 evidence 缺失时 validator 仍通过——是早期版本的信任模型漏洞
- **客户端差异（Issue #11）**：Antigravity 等 Claude Code 客户端杀掉子进程，让流水线的「平台中立性」遭遇现实
- **CRYPTOGRAPHY-AND-KEY-MANAGEMENT companion 待补**（Issue #39）：攻击分类尚未完整
- **撞风口 ≠ 长期价值**：13K stars 主要来自「AI agent 现象级关注」，需要持续方法论反哺才能保住热度

## 行动建议

- **如果你要用它**：适合「想给 Claude Code / Cursor 等 AI 编码代理加端到端审计能力」的场景；不适合只想找签名级漏洞的 CI 集成（那种场景 SAST 更快更稳）；本仓库与传统 SAST **互补**而非替代
- **如果你要学它**：
  - **重点读 `skills/security-audit/SKILL.md`**（192 行，理解整套流水线编排）
  - **重点读 `validate-findings.cjs`**（零依赖 validator + 显式安全边界的范本）
  - **重点读 `validate-coverage-ledger.cjs`**（canonical_refs 派生 + multi-run 累加）
  - **重点读 `HUNTING.md` + `ATTACK-CLASSES.md`**（理解攻击分类法与 hunter prompt 模板）
  - **重点读 `AI-AND-LLM.md`**（2025 年才出现的攻击类，传统 SAST 没有）
- **如果你要 fork 它**：
  - 把 issue #20 的 6 个方法学盲区作为优先 PR 方向
  - 把 issue #39 的 CRYPTOGRAPHY companion 补上
  - 补 `.github/workflows` 跑 hostile CLI / terminal control bytes 测试矩阵
  - 补 CHANGELOG + 显式说明 breaking change 的迁移路径（158eb44 「Rework the audit workflow, findings contract, and validators end to end」 是实质 breaking change）
  - 修 issue #21 的验证器信任边界漏洞

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/cloudflare/security-audit-skill |
| Zread.ai | 未收录 |
| 关联论文 | [A systematic review of security threats in LLM agents](https://arxiv.org/abs/2508.04127) |
| 在线 Demo | 无（skill 本质是 Claude Code 内的提示词工程） |
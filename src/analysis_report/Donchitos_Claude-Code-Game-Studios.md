# 21k star 的单人项目：49 个 AI agent 怎么把 Claude Code 变成一支游戏工作室

> GitHub: https://github.com/donchitos/claude-code-game-studios

## 一句话总结

Claude Code Game Studios（CCGS）是墨尔本匿名独立开发者 Donchitos 的单人作品——用 49 个 AI agent + 73 个 workflow skill + 一套门控协调系统，把单个 Claude Code 会话改造成一支有层级、有岗位、有评审门的「虚拟游戏工作室」，4 个月冲到 21k star。它真正的价值不在「做游戏」，而在它示范了一套可迁移到任何领域的多 agent 编排架构。

## 值得关注的理由

1. **品类里罕见的「系统」而非「清单」**：同赛道的 Claude Code agent 合集（VoltAgent 21k、agency-agents 14k）大多是松散的角色平铺，而 CCGS 把三层组织架构、五条协作协议、带 ID 的共享门控库、甚至一套给 prompt 做回归测试的框架都做成了一等公民——这是当下少见的成体系 prompt 工程作品。
2. **编排模式高度可迁移**：工作室层级映射模型分层、工具级域边界（disallowedTools 即 RBAC）、首行 verdict token 机读协议、prompt 片段注册表消除漂移、文件即记忆 + 钩子治理——这些设计脱离游戏场景，对任何做多 agent 系统的人都是直接可抄的范式。
3. **一个值得警惕的「热度 vs 落地」反差样本**：21k star、单人、4 个月爆发，但最热的 Issue 是 #34「有人真用它做出过完整可玩游戏吗」、#46「跑了三周只做出几个按钮，这不是在浪费 token 吗」——star 数里含相当比例的「概念好评」而非「重度使用」，是研究「AI 工具叫好不叫座」的好标本。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/donchitos/claude-code-game-studios |
| Star / Fork | 21,123 / 3,074 |
| 项目体量 | **49 个 agent + 73 个 skill + 392 个 markdown / 75,852 行 prompt 定义**（tokei 仅识别 985 行 YAML frontmatter——本质是 prompt 工程项目，非传统代码，代码行严重失真） |
| 项目年龄 | 3.8 个月（2026-02-12 创建，3 月单月爆发 23 commit） |
| 开发阶段 | 稳定维护（v1.0.0 已发布，近 30 天仅 1 commit） |
| 贡献模式 | 单人 100%（Donchitos，墨尔本匿名独立开发者，仅此 1 个公开仓库） |
| 热度定位 | 大众热门（爆发型，4 个月破 2 万星，近百星集中在一周内） |
| 质量评级 | agent/skill 定义[优] 文档[优] skill 测试框架[优·罕见] 真实落地验证[未证] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

作者 Donchitos 是匿名/化名独立开发者，定位墨尔本，GitHub 账号注册 2.6 年却只发布了这一个公开仓库，凭它冲到 21k star（star-history 全球 #2299），并以 Buy Me a Coffee + GitHub Sponsors 作为个人 IP 变现载体。可信度建立在「作品的设计专业度」而非「身份名气」上——README 与 agent 定义里大段引用 MDA 美学框架、自决理论（Self-Determination Theory）、心流、Bartle 玩家类型，`creative-director.md` 里直接拿 God of War / Hades / Celeste 的设计 pillar 做实例，证明作者具备真实游戏行业知识。

### 问题判断

作者把「真实工作室为什么要分工」这个组织行为学问题，平移到「AI 为什么会失控」上：单个 Claude Code 会话做中大型（6 个月+）游戏时，等于「一个人同时当创意总监、主程和 QA」，必然角色串味——硬编码数值、跳过设计直接写代码、堆屎山、无评审。他的切入点不是「再写一个更聪明的 agent」，而是「复刻工作室的岗位边界与评审链」。

### 解法哲学

核心信条是 **「Collaborative, Not Autonomous」**（协作而非自动驾驶）：Agent = 专家顾问，User = 拍板的创意总监。每次交互强制 **Question → Options → Decision → Draft → Approval**，写文件前必须先问「May I write this to [filepath]?」。明确的「不做」清单写进每个 agent 的 `What This Agent Must NOT Do` 段，以及项目级「不做自动驾驶、不做 game jam 主场」——宁可慢、宁可多问，也不让 AI 一把梭。这条哲学恰好与竞品 ralph-claude-code 的「自主开发循环」路线相反。

### 战略意图

这是个人 IP / 打赏变现载体，战略上是**在 Claude Code 生态里卡位「游戏垂直 + 工作室编排」这个无人占据的格子**：通用 agent 清单已是红海，垂直 + 成体系是差异化护城河。代价是命运与 Claude Code 强绑定——外部测评（Starlog）点名最大风险正是「完全绑定 Claude Code 这一专有 IDE」。

## 核心价值提炼

### 创新之处

> 本项目是 prompt 工程系统，以下创新均基于实际 agent/skill/hook/rule 文件分析。

1. **真实工作室层级 → AI agent 三层组织 + 模型分层映射**（新颖 4 / 实用 4 / 可迁移 5）：49 个岗位精确对应「总监→部门主管→专家」三级，并直接映射到模型——Tier1 Directors 用 `model: opus, maxTurns: 30`、Tier2 Leads 用 `sonnet`、Tier3 Specialists 用 `sonnet` 或 `haiku`（qa-tester、devops、community-manager 等为 haiku）。按决策权重分配模型，省钱又不掉能力。
2. **工具级域边界（disallowedTools 即 RBAC）**（新颖 4 / 实用 5 / 可迁移 5）：设计类 agent（game-designer、art-director、narrative-director 等）一律 `disallowedTools: Bash`，从能力上就不能碰代码/跑命令；程序类才有 Bash；编排者与引擎 lead 才有 Task（能 spawn 子专家）。把「你别越界」从 prompt 软约束变成能力硬约束。
3. **带 ID 的共享门控库 + 三档评审强度旋钮**（新颖 5 / 实用 5 / 可迁移 5）：把所有门控写成带 ID 的标准条目（`CD-PILLARS`、`TD-ARCHITECTURE`、`*-PHASE-GATE`），skill 里只写「Spawn creative-director via gate CD-PILLARS」引用而非内联，根治 prompt 漂移；评审强度由 `review-mode` 控制 `full`/`lean`（默认）/`solo`（给 game jam），把「严谨度↔速度/成本」做成可调旋钮。
4. **CCGS Skill Testing Framework——给 prompt 做 CI**（新颖 5 / 实用 4 / 可迁移 5）：`catalog.yaml`（73 skill + 49 agent 的覆盖台账）+ `quality-rubric.md`（PASS/FAIL 指标）+ `/skill-test`（static 结构 linter / spec 行为断言 / category 分类评分 / audit 覆盖报告）。在 prompt 工程项目里「为 prompt 写测试」极为少见。
5. **机器可解析的门控判决协议**（新颖 4 / 实用 5 / 可迁移 5）：所有 gate 返回固定词表 `APPROVE / CONCERNS / REJECT`，且要求 agent **首行就是 `[GATE-ID]: APPROVE` token**，不准把判决埋进段落；并行多总监时用「strictest-wins」（一个 REJECT 覆盖所有 APPROVE）。让 agent 间通信变成编排器可机读的契约。
6. **文件即记忆 + 生命周期钩子治理**（新颖 3 / 实用 5 / 可迁移 5）：「The file is the memory, not the conversation」——状态写进 `production/session-state/active.md`，崩溃后由 `session-start.sh` 自动恢复；12 个 bash 钩子在 `settings.json` 注册成确定性闸（JSON 非法直接 exit 2 拦截、GDD 缺必填段告警、检测「有代码无文档」推荐对应 skill）。

### 可复用的模式与技巧

1. **Prompt 片段注册表 + 按 ID 引用**：把重复 prompt 抽成带 ID 的单一真相源，根治 prompt drift。
2. **评审/严谨度旋钮**：把「质量 vs 速度/成本」做成全局可配 + 单次 `--review` 可覆盖的开关。
3. **能力即边界**：用 tools/disallowedTools 白黑名单而非 prompt 措辞落实最小权限。
4. **首行 verdict token 契约 + strictest-wins**：让 agent 输出可被编排器机读，并行结论取最严。
5. **文件式状态 + 钩子崩溃恢复**：长任务、会触发 compaction 的 agent 工程标准解。
6. **Prompt 资产的元测试**：把 SKILL/agent 当被测对象做回归（覆盖台账 + 分类 rubric + 结构 linter）。
7. **path-glob 规则注入**：rules frontmatter 用 `paths` glob 按文件路径精准下发规范。
8. **钉版本参考库**：`docs/engine-reference/{godot,unity,unreal}/` 的 VERSION + breaking-changes + deprecated-apis 对抗 LLM 知识陈旧。
9. **注册表驱动的跨文档一致性 + grep-first**：`entities.yaml` 做唯一真相源，只读冲突段省 token。
10. **岗位「禁止清单」**：每个 agent 的 `What This Agent Must NOT Do` 用显式负向约束防角色串味。

### 关键设计决策

- **三层 hierarchy 映射模型分层**：成本/能力与决策层级对齐。Trade-off：增加「该派谁」的认知负担，模型 tier 硬编码在 frontmatter（换模型要逐文件改）。
- **path-scoped rules 自动注入规范**：`.claude/rules/*.md` 用 frontmatter `paths: ["src/gameplay/**"]` glob 绑定路径，编辑匹配文件时自动生效（gameplay-code 要求数据驱动/delta time/禁引 UI；engine-code 要求热路径零分配）。
- **引擎版本感知参考库**：用「外部钉版事实」纠正模型对 Godot/Unity/Unreal 新版 API 的记忆滞后。Trade-off：参考库要人工维护。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | CCGS | VoltAgent/awesome-subagents | agency-agents-zh | ccpm | ralph-claude-code |
|------|------|--------|--------|--------|--------|
| Star | 21.1k | 21.3k | 14.1k | 8.2k | 9.3k |
| 形态 | 系统（层级+协议+门控） | 松散清单 | 跨工具清单 | 项目管理 skill | 自主循环 |
| 垂直领域 | 游戏 | 通用 | 通用 | 通用 | 通用 |
| 多 agent 编排 | 三层+5 协议+门控 | 无层级 | 无层级 | 真并行(worktree) | 单循环自主 |
| 质量门/测试 | ✅ 门控+测试框架 | ❌ | ❌ | Issue 追踪 | 退出检测 |
| 哲学 | 协作非自主 | 随取随用 | 数量覆盖 | 工程化并行 | 自主驾驶 |

### 差异化护城河

唯一的「游戏垂直 + 工作室层级编排 + 配套 prompt 测试框架/hooks/rules」全家桶。护城河来自「成体系」与「真实行业方法论注入」，而非单点功能（单点都可被抄）。

### 竞争风险

1. **深度绑定 Claude Code 专有特性**（agents/skills/hooks/settings.json/AskUserQuestion/Task），平台政策或 API 一变即受冲击，无可移植层。
2. **系统「无法强制」遵守**——用户可跳过设计、无视评审，门控大多是告警非阻断（push 的 block 甚至被注释掉），全靠自觉。
3. **热度 ≫ 落地**：完整可玩游戏的案例稀缺（#34/#53），重文档驱动导致 token 成本高（#64 大型 ADR>25k token 触顶、#46「三周只做出几个按钮」的 ROI 质疑）。

### 生态定位

Claude Code 生态里「游戏方向 + 重流程」的标杆样板间。其编排模式对非游戏团队的可迁移价值，可能高于其游戏垂直本身——更像一份「可复制的多 agent 编排架构参考实现」。与 ccpm 等是潜在互补（ccpm 的并行执行 + CCGS 的协调协议）。

## 套利机会分析

- **信息差**：21k star + 热门赛道（Claude Code agent 编排 × 游戏开发）+ 单人爆发故事，是优质选题；但真正的内容差异点在「拆解它的编排架构」与「诚实评估热度 vs 落地的落差」，而非复述功能列表。
- **技术借鉴**：带 ID 的门控注册表、评审强度旋钮、工具级 RBAC、首行 verdict token 协议、给 prompt 做回归测试——这几套是任何多 agent / prompt 工程项目都能直接复用的范式，价值远超游戏场景。
- **生态位**：填补「Claude Code 生态下游戏垂直 + 成体系工作室编排」空白。
- **趋势判断**：踩中多 agent 编排上升趋势，但与 Claude Code 强绑定 + ROI 未经验证是悬顶之剑；作为「范式参考」的生命力可能强于作为「生产工具」。

## 风险与不足

1. **落地验证缺口**：缺端到端「做出完整可玩游戏」的成功案例佐证，多个高赞 Issue 公开质疑实战效果。
2. **平台单点依赖**：完全绑定 Claude Code 专有特性，无平台中立层，bus factor = 1（纯单人）。
3. **门控强制力不足**：多数 hook 与 gate 是告警/约定，系统无法强制遵守。
4. **一致性漂移**（Phase 3 实测）：`agent-roster.md` 标 qa-tester 为 Haiku 但实际定义是 sonnet；skill-test 输出示例写「52 Skills」实际 73 个；Collaboration Protocol 整段在多个 agent 间逐字复制、未充分按岗定制。
5. **学习曲线陡 + token 成本高**：明确不适合快速原型，重文档驱动放大上下文成本。

## 行动建议

- **如果你要用它**：你在用 Claude Code 做中大型（6 个月+）游戏、且认同「慢即是快、人来拍板」的协作哲学——值得一试，但要有「学习曲线陡、token 成本高、需自己守纪律」的预期。做 game jam / 快速原型请绕道（或只用 `solo` 模式）。
- **如果你要学它**（最高价值路径）：把它当多 agent 编排的参考实现来读，重点啃 `.claude/docs/director-gates.md`（门控注册表）、`coordination-rules.md`（五条协作协议 + 模型分层表）、`.claude/agents/creative-director.md`（Tier1 样板 + verdict 格式）、`.claude/settings.json`（钩子注册）、`CCGS Skill Testing Framework/`（给 prompt 做测试）。这些模式可直接迁移到任何领域的 agent 系统。
- **如果你要 fork 它**：最值得做的是「平台抽象层」（降低对 Claude Code 的硬绑定）与「把告警型门控升级为可选阻断」，以及修掉 Phase 3 指出的几处文档/定义漂移。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [已收录（agent 层级 / skills 参考 / hooks / 三引擎 reference 全套）](https://deepwiki.com/Donchitos/Claude-Code-Game-Studios) |
| Zread.ai | 未确认（直连 HTTP 403） |
| 外部测评 | [Building a 49-Agent Game Studio Inside Your IDE（Starlog）](https://starlog.is/articles/ai-agents/donchitos-claude-code-game-studios) |
| 仓库分析 | [OSSInsight](https://ossinsight.io/analyze/Donchitos/Claude-Code-Game-Studios) / [Star-History](https://www.star-history.com/donchitos/claude-code-game-studios/) |
| 关联论文 / 在线 Demo | 无（模板项目，需在本地 Claude Code 内运行） |

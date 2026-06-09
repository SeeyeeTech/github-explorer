# 半年 27K stars：K-Dense 把 142 个科研 Skill 做成了「科学领域的 npm registry」

> GitHub: https://github.com/K-Dense-AI/scientific-agent-skills

## 一句话总结

K-Dense 把 142 个科学垂直领域（生信/化信/临床/天文/材料……）的「AI 工作流文档」打包成符合开放 Agent Skills 标准的可分发目录，让 Claude Code、Cursor、Codex、Google Antigravity 等任意通用 AI agent 一键升级为「AI Scientist」。

## 值得关注的理由

- **垂直 × 标准化的稀缺交叉**：科学垂直深度的同类项目（DeepAnalyze 4.2k、NanoResearch 1.5k、AutoR 849）量级都只有它的零头，而通用 AI agent skills（Anthropic 官方）又没有科学深度，这个交叉位置目前只此一家。
- **真·供应链安全**：每周一 Cisco AI Defense Skill Scanner 全量扫描 + PR 时增量扫描，扫描结果自动 commit 到 main 的 `SECURITY.md`（3644 行带 severity badge），把「prompt 注入 / 越权调用」当成 npm 依赖一样审计——这是受监管行业（药企/医疗/汽车）的入场券。
- **三段式 provenance**：`pyproject.toml` 版本 + 每个 skill 自己的 `metadata.version` + git tag/SHA pin，从「包级 → 文件级 → 安全级」三层版本治理，是 prompt/template registry 该有的工程范式。

## 项目展示

> README 与官方页面以文字+表格为主，富媒体素材较少，仅保留两个有意义的元素。

### README 媒体
1. ![Star History Chart](https://api.star-history.com/svg?repos=K-Dense-AI/scientific-agent-skills&type=date&legend=top-left) — 类型: hero（增长曲线，半年从 0 到 27K）
2. [演示视频](https://youtu.be/ZxbnDaD_FVg) — 类型: video（K-Dense BYOK 桌面应用功能演示）

### 筛选说明
- 总共发现 12 个候选媒体元素，筛选后保留 2 个
- 排除了 10 个 badge / CI 状态图标 / 重复 star-history 图表

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/K-Dense-AI/scientific-agent-skills |
| Star / Fork | 27,646 / 2,849 |
| Watcher | 140 |
| 代码行数 | 96,321 行（Python 59.5% / JSON 28.2% / TeX 10.9%） |
| 项目年龄 | 7.6 个月（首提交 2025-10-19） |
| 文件数量 | 1,244 |
| 依赖数量 | 15（runtime，pyproject.toml） |
| Skill 数量 | 142 个 |
| 数据库接入 | 78+ 公共数据库（PubMed/ChEMBL/UniProt/ClinVar/COSMIC/FDA/USGS/SEC EDGAR/FRED……） |
| 开发阶段 | 密集开发（30 天 58 commits，近 90 天 155 commits） |
| 开发模式 | 职业项目（周末 22.5%，深夜仅 5.4%） |
| 贡献模式 | 单核心 + 社区辅助（Timothy Kassis 300 commits ≈ 58%，其余 42 人合计 42%） |
| 热度定位 | 大众热门（半年 27K stars，垂直赛道头部） |
| 质量评级 | 代码优秀 / 文档优秀 / 测试不足（仅 4/143 skill 有 unit test）/ CI/CD 完善 / 安全治理完善 |
| License | MIT（每个 skill 还有各自的 sub-license） |
| 最新版本 | v2.46.0（共 84 个 tag，平均 2.7 天一版，语义化版本） |
| 兼容 Agent | Claude Code / Cursor / Codex / Google Antigravity / Gemini CLI / Goose / OpenHands / OpenCode / Amp 等 40+ |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

K-Dense-AI 是 Organization 账号，背后的商业公司是 **K-Dense Inc.**——一家 2025 年下半年新成立的 "AI for Science" 垂直创业公司，自定位「A world leader in empowering scientists with AI agentic tools」。投资方包括 Accel、Accel Atoms、Google AI Futures Fund；机构客户含 MIT、Harvard Medical School、Stanford、UPenn、Ford、GSK、Zeiss 等。组织账号下贡献者 30 人，Top1 是 Timothy Kassis（300 commits ≈ 58%），呈「明星开源 + 商业化公司主导」结构。K-Dense 还有两款姊妹产品：`claude-scientific-writer`（1917 stars）、`agentic-data-scientist`（648 stars），共同构成「AI Scientist」品牌矩阵。

### 问题判断

K-Dense 团队从产品迭代中识别出三个反复出现的失败模式：

1. **模型-工作流错配**：模型本身很强，但被用来干「写文档化的代码」这种它不擅长的劳动密集型任务。
2. **幻觉函数**：对 RDKit/PyDESeq2/Scanpy 这类快速演化的科学包，LLM 训练截止数据早已过期，模型会自信地写错参数、调用已删除的函数。
3. **缺乏可审计性**：产业客户（GSK/Zeiss/Ford）无法接受 agent 在受监管环境（GxP/ISO13485）下写出不可追溯的代码。

**时机选择**：2025 年 10 月开源，恰好赶上 Anthropic 在 Claude Code 中发布开放 Agent Skills 标准（[agentskills.io](https://agentskills.io/)）——这是「标准刚出 + 没人做垂直深井」的窗口期，K-Dense 抢先把 142 个科学 skill 一次性铺到位。

### 解法哲学

四个核心信条：

1. **Workflow > Model**：模型层投入 0 资源，所有精力押在「工作流文档」上。
2. **Specialists over generalists**：不为每个领域写一个万能 skill，而是 142 个细粒度 skill，每 skill 是该领域一名「虚拟专家」。
3. **Composable / auditable / falsifiable**：skill 目录是文件级、可 diff、可 grep、可在 PR 中 code review。
4. **Verification first**：所有 PR 必须经 Cisco AI Defense Skill Scanner 三层扫描（Behavioral + Trigger + LLM-as-judge），并把扫描报告 `SECURITY.md` 公开提交到 main。

**明确不做的**：不做端到端 agent（不做推理引擎、不绑定单一 LLM）、不做单一领域深井（不做 DeepAnalyze 那种「一个数据科学家」）、不做 MCP 协议（站 Agent Skills 标准而非 MCP）。

### 战略意图

明牌「靠 LLM 不能赢，靠 LLM + 垂直知识包能赢」：上游卡 anthropic/openai 模型（无差异化）；中游卡 agent runtime（Cursor/Claude Code/Codex 是公共的）；下游卡数据/工作流/合规（这是科学软件包特有的、需要逐领域积累）。K-Dense 押注下游，做了三层防御：

1. **规模壁垒**：142 个 skill，单 repo 占 K-Dense 总 star 89%。
2. **合规壁垒**：Cisco scanner + SECURITY.md + `metadata.version` provenance。
3. **生态壁垒**：pin to SHA、`gh skill install` 标准 CLI、40+ agent host 兼容。

战略意图是让科学 agent skills 成为「科学领域的 npm registry」，任何想给 LLM 加科学能力的人都得来这取货。

## 核心价值提炼

### 创新之处

| 创新点 | 新颖度 | 实用性 | 可迁移性 |
|---|---|---|---|
| **科学 × Agent Skills 标准化的「深度 × 标准化」组合**（142 skill + 开放标准 + 供应链审计） | 4/5 | 5/5 | 3/5 |
| **渐进披露 3 阶段**（Discovery: frontmatter description 匹配 → Activation: SKILL.md < 500 行 → Execution: 按需懒加载 references/） | 3/5 | 5/5 | 5/5 |
| **三段式 provenance**（`pyproject.toml` 包级 + `metadata.version` 文件级 + git tag/SHA pin 安全级） | 4/5 | 5/5 | 4/5 |
| **`database-lookup` 用 78 个独立 references/*.md 文件**（按需加载、per-entity file 模式） | 4/5 | 5/5 | 5/5 |
| **`scan_pr_skills.py` 用 git diff 增量扫描 + sticky PR comment**（PR 时只扫变更 skill） | 3/5 | 5/5 | 5/5 |
| **`autoskill` 元 skill**（screen capture → redact → embedding 聚类 → LLM judge → 自动草拟新 SKILL.md） | 5/5 | 3/5 | 3/5 |
| **`SECURITY.md` 自动 commit 到 main 作为可审计快照** | 3/5 | 4/5 | 5/5 |

### 可复用的模式与技巧

1. **Agent Skill 模板**（YAML frontmatter + Markdown body + 可选 references/scripts/assets）—— 适用：AI 插件市场、prompt 模板库、团队知识资产。
2. **三层版本治理**（pyproject.toml + `metadata.version` + git tag/SHA pin）—— 适用：任何「文档+配置+脚本」复合体的版本管理。
3. **Diff-driven 增量 CI 扫描**（`git diff --name-only --diff-filter=ACMR` + scanner 只跑变更子集）—— 适用：lint、license audit、secret scan、schema 校验。
4. **Sticky PR comment pattern**（`marocchino/sticky-pull-request-comment` 复用同一 header）—— 适用：所有 GitHub Actions 输出 markdown report 的场景。
5. **`per-entity reference file` 模式**（当知识库条目 > 30 且条目间互不相关时）—— 适用：API registry、microservice 目录、policy 库、template 库。
6. **Progressive disclosure**（主文件 < 500 行 + references/ 按需懒加载）—— 适用：长 prompt、RAG chunk、AI 友好的 tech docs。
7. **`[skip ci]` 自动提交审计报告**（避免「扫描 → commit → trigger scan → commit」无限循环）—— 适用：所有生成报告并 commit 回 repo 的工作流。
8. **Cross-skill overlap analysis**（`CrossSkillScanner.analyze_skill_set` 检测同一 PR 多 skill 冲突/重复）—— 适用：plugin marketplace、policy conflict detection。

### 关键设计决策

1. **SKILL.md 强制要求 `metadata.version`**（即使上游 spec 中 `metadata` 是 optional）
   - 问题：上游 spec 允许无 metadata，导致 skill 没有「可演化的版本锚点」。
   - 方案：`CONTRIBUTING.md` 把 `metadata.version` 列为必需，新 skill 从 `"1.0"` 起每次 PR 必递增。
   - Trade-off：contributor 多一步门槛，但获得 semver 语义 + Cisco scanner 差异分析 + pin minor 不破坏 API 的能力。
   - 可迁移性：**高**。

2. **双层安全扫描架构**——`scan_skills.py` 周一全量扫（写入 SECURITY.md）+ `scan_pr_skills.py` PR 时增量扫（sticky PR comment）
   - 问题：143 个 skill × Cisco scanner 一次扫描 ~50 分钟/skill，全量重扫塞不进每次 PR；但完全不做 PR 闸门则恶意 skill 容易 merge。
   - 方案：PR workflow 用 `git diff --name-only` 提取 `skills/<name>/**`，喂给 scanner，`--fail-on HIGH` 默认阻断；用 `marocchino/sticky-pull-request-comment@v2` 复用同一 comment header。
   - Trade-off：PR 时只扫改动的 skill，但恶意 contributor 可在多个小 PR 间逐步注入；缓解靠周一全量二次校验 + `--fail-on HIGH` 保守阈值。
   - 可迁移性：**高**。

3. **`database-lookup` 用 78 个独立 `references/*.md` 文件组织数据库元数据**
   - 问题：LLM context window 有限，把 78 个数据库 endpoint/auth/example 全塞进 SKILL.md 会让 prompt 膨胀。
   - 方案：SKILL.md 只含「database selection guide」决策表，告诉 agent 在用户问某类问题时该读哪个 references/*.md；references/78 个文件每个 30–80 行。
   - Trade-off：维护 78 个文件比一个大表繁琐；但按需加载减少 context + 单文件 bug 不污染其他数据库 + 与渐进披露 spec 完全对齐。
   - 可迁移性：**高**。

4. **`autoskill` 元 skill**——用 screenpipe 监听屏幕 → 本地聚类 → 语义匹配 142 个现有 skill → 自动草拟新 SKILL.md
   - 问题：142 个 skill 不能穷举所有科研工作流；用户每天重复做的实验步骤没被沉淀为可复用 skill。
   - 方案：抓取用户屏幕 OCR → redaction（去 email/api_key/bearer）→ 10 分钟 idle 切会话 → embedding 聚类 → 与 142 个 skill description 做余弦相似度 → LLM judge 判 reuse/compose/novel → 草拟 SKILL.md 落 `~/.autoskill/proposed/<ts>/` → 用户审完后 `promote` 进 `skills/<name>/`。
   - Trade-off：屏幕抓取本身是隐私雷区（用 screenpipe 自带 PII removal + `redact.py` 双层防御）；整套默认跑在本地 LM Studio（Gemma-4-31B-it）不外发数据；`promote` 步骤强制人工 review 不能自动合入。
   - 可迁移性：**高**（「个人 workflow mining → 团队 playbook」元模式，可推广到销售线索挖掘、客服工单归类、设计稿聚类）。

5. **路径迁移 `scientific-skills/` → `skills/`**（v2.43.0）以匹配 Agent Skills 标准
   - 问题：旧路径与 GitHub CLI 的 `gh skill install` 默认 skills 目录约定不一致。
   - 方案：重命名目录、更新所有引用、README 加 troubleshooting 条目 + 头部 banner 声明「Claude Scientific Skills is now Scientific Agent Skills」。
   - Trade-off：老引用断链、CITATION 需重发；但获得与开放标准对齐 + `gh skill install` 原生可用 + 未来第三方 skill 可与本仓 skill 在同一目录共存。
   - 可迁移性：**中**。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | K-Dense scientific-agent-skills | Anthropic 官方 anthropic-skills | DeepAnalyze (4.2k★) | paper-search-mcp (1.7k★) | NanoResearch (1.5k★) |
|------|---------|--------|--------|--------|--------|
| Skill/Agent 数量 | 142 个 skill | ~10 个通用 skill | 单一端到端 agent | 单一论文检索 MCP | 单一研究流水线 |
| 领域覆盖 | 17 个科学领域 | 通用（pptx/pdf/docx） | 数据科学为主 | 论文检索 | 论文写作 |
| 标准合规 | Agent Skills 开放标准 | Agent Skills（自家） | 自家协议 | MCP 协议 | 自家协议 |
| 可拆解性 | 文件级、可单独 install | 文件级 | 单体不可拆 | 文件级 | 单体不可拆 |
| 可审计性 | SECURITY.md + Cisco scanner + 版本治理 | 无 | 黑盒 prompt | 中等 | 中等 |
| 跨 Agent 兼容 | 40+ agent host | 主要 Claude | 单 host | MCP 标准 | 单 host |
| 受监管行业适用 | 高（GxP/ISO13485） | 中 | 低 | 低 | 低 |
| 项目年龄 | 7.6 个月 | 较老 | ~1 年 | ~1 年 | 较新 |

### 差异化护城河

1. **规模护城河**：142 个 skill × 78 个数据库 × 40+ agent host，单一对手无法在一年内复制。
2. **合规护城河**：Cisco scanner + SECURITY.md + `metadata.version` provenance 是受监管行业（药企/医疗/汽车）的入场券，Anthropic 官方与小型 OSS 都没有。
3. **生态护城河**：与 GitHub CLI `gh skill` 原生集成 + Agent Skills 标准合规，未来开放市场一旦形成，K-Dense 是默认上架方。

### 竞争风险

- **Anthropic 官方发力**：若 anthropic-skills 突然扩到 50+ 科学 skill，K-Dense 的「开放标准」优势被削弱。
- **社区分叉**：高质量 fork 可能分流贡献者。
- **scanner 误报疲劳**：当前 SECURITY.md 中 24 critical + 15 high（39 个非 safe skill）若不收敛，会让用户对 SECURITY.md 失信任。
- **trust boundary**：143 个 skill 中 39 个非 safe，产业客户若逐个审查会卡在 onboarding。

### 生态定位

**垂直深井的开放标准定义者**——既不是 Anthropic 那种「通用浅池」，也不是 DeepAnalyze 那种「单一深井非标」，而是「多个深井 × 开放标准 × 审计保障」的 marketplace；商业上类似「Docker Hub for science skills」。

## 套利机会分析

- **信息差**：低关注度但高质量？**不是**——本项目已经是 27K stars 的大众热门，信息差窗口已关闭。但**垂直 × 标准化**这个交叉赛道仍然是蓝海，K-Dense 之外的玩家（法律、金融、教育、医疗、政务）都还没出现类似形态。
- **技术借鉴**：**极高**——SKILL.md 模板、progressive disclosure、diff-driven 增量 CI、sticky PR comment、三层版本治理、`per-entity reference file` 模式都是可以直接搬到任何 prompt/asset/template registry 的工程范式。
- **生态位**：填补「科学垂直 × 跨 agent 兼容 × 标准化」三重交叉空白；目前独家头部，未来 6-12 个月内不太可能被颠覆，但 Anthropic 自家发力是最大变量。
- **趋势判断**：Agent Skills 标准由 Anthropic 推动，2025 年 10 月发布，K-Dense 抢跑半年。Cursor / Codex / Antigravity / Gemini CLI 等 40+ agent 都在采纳同一标准——趋势是确定的，K-Dense 是先发优势最大的玩家。

## 风险与不足

- **测试覆盖不足**：全仓仅 `autoskill` / `pacsomatic` / `exa-search` / `open-notebook` 4 个 skill 有 unit test，根级 `scan_skills.py` 与 `scan_pr_skills.py` 无 unit test，其他 130+ skill 的 SKILL.md 示例代码无 CI 验证。README 注明「tested or clearly marked as illustrative」，质量靠人工 review + 用户实测。
- **trust boundary 现状**：39/143 skill 非 safe（24 critical + 15 high），虽然透明公开，但产业客户 onboarding 会卡在逐个审查。
- **scanner 误报疲劳**：70 critical / 52 high 的现状若不收敛，SECURITY.md 会从「信任锚」变成「噪声源」。
- **核心团队依赖**：Top1 Timothy Kassis 占 58% commits，单点风险高；公司商业化动作（K-Dense BYOK 桌面应用）若失败，可能影响 OSS 投入节奏。
- **目录迁移阵痛**：v2.43.0 从 `scientific-skills/` 迁到 `skills/`，老引用断链还在持续。

## 行动建议

### 如果你要用它
- **科学家 / 研究人员**：用 `npx skills add K-Dense-AI/scientific-agent-skills` 或 `gh skill install K-Dense-AI/scientific-agent-skills --agent claude-code` 一键安装，配合 Claude Code / Cursor 直接做单细胞分析、化合物筛选、文献综述等。
- **药企 / 生物科技 / 汽车 R&D**：先 review `SECURITY.md` 的 39 个非 safe skill 列表，按需 pin 到具体 tag/SHA，配合内部 GxP/ISO13485 审计。
- **对比选型**：如果你只需要「单一数据科学 agent」，DeepAnalyze 更省事；如果你只需要「论文检索」，paper-search-mcp 更聚焦；如果你是「跨学科 + 受监管 + 跨 agent」场景，K-Dense 是目前唯一选择。

### 如果你要学它
- **必读文件**：
  - `README.md`（700+ 行完整 onboarding + security disclaimer + 5 个端到端示例工作流）
  - `CONTRIBUTING.md`（skill 命名规则、frontmatter schema、version 规则、validation checklist）
  - `.claude-plugin/marketplace.json`（注册清单设计）
  - `scan_pr_skills.py` + `scan_skills.py`（360 行双层安全扫描实现）
  - `skills/database-lookup/SKILL.md` + `skills/database-lookup/references/`（78 个独立文件渐进披露范例）
  - `skills/autoskill/`（元 skill 工作流挖掘，screen → redact → cluster → judge → draft）
  - `.github/workflows/pr-skill-scan.yml` + `security-scan.yml`（CI/CD 完整范式）
- **重点关注**：progressive disclosure 3 阶段、`metadata.version` 强制要求、diff-driven 增量扫描、sticky PR comment。

### 如果你要 fork 它
- **可改进方向**：
  1. 增加全仓统一的 unit test 框架（覆盖至少 SKILL.md frontmatter schema 校验、扫描脚本逻辑）。
  2. 把 `SECURITY.md` 中 39 个非 safe skill 引入 issue tracking，强制每个有 remediation owner。
  3. 增加 skills 示例代码 CI 自动化执行（用 uv + 容器化环境跑通 examples）。
  4. 探索 Agent Skills 标准之外的互补分发通道（如 MCP server 化、Docker image）。
  5. 引入「skill usage telemetry」（opt-in）帮助用户挑选活跃 skill。
  6. 把 `autoskill` 的工作流挖掘范式推广到其他垂直（法律、金融、教育、医疗、政务）。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/K-Dense-AI/scientific-agent-skills — 已收录，结构化拆解 134 skills、按 7 大类 |
| Zread.ai | 未收录（403 拒绝访问） |
| 关联论文 | 无直接配套论文（README 中仅提供 BibTeX 引用条目） |
| 在线 Demo | https://youtu.be/ZxbnDaD_FVg（K-Dense BYOK 桌面应用演示）+ https://github.com/K-Dense-AI/k-dense-byok |
| 官方网站 | https://k-dense.ai |
| Agent Skills 标准 | https://agentskills.io/ |
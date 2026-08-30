# GitHub推荐：9 个月 3K stars 的反常识项目：JetBrains 把 Go 现代写法塞进 AI Coding Agent 的 Prompt

> GitHub: https://github.com/JetBrains/go-modern-guidelines

## 一句话总结

JetBrains GoLand 团队出品的「Go 现代编程规范」结构化数据集 + 跨 5 大 AI Coding Agent 平台的 Skill 包装，按 `go.mod` 自动过滤可用 API，从源头让 Agent 写出与项目 Go 版本对齐的现代代码。

## 值得关注的理由

- **反常识项目形态**：49% 行数是 JSON 数据、43% 是 Go 运输层代码——数据是产品，代码只是「数据 → Agent prompt」的搬运工。这种「content-as-data + 多平台 transporter pattern」的设计，是 AI Coding Agent 时代少见的可复用工程范式。
- **版本感知的工程稀缺**：CLI 读 `go.mod` 解析 Go 版本，按 `since_version` 字段做 O(n) 过滤，让 CI 不会因模型推荐「Go 1.27 的 `errors.AsType[T]`」而在 Go 1.21 项目里炸掉——这是同时拥有「写前导」+「版本安全」的少数方案。
- **一次 JSON 改动，全平台同步**：Claude Code、Junie、Cursor、Codex、skills.sh 5 大 AI Coding 平台共享同一份规则表；改一行 JSON，5 个分发渠道同时生效——JetBrains 在所有 Agent 平台都用自家署名卡位。

## 项目展示

- [JetBrains 官方演示视频：GoLand 团队演示 go-modern-guidelines 跨 Agent 工作流](https://www.youtube.com/watch?v=_VePjjjV9JU) — 类型: video (demo)

> 仓库本身是「skill/CLI/JSON 数据」类工具，README 与官网均无 hero 图或架构图，价值在 CLI 体验与 prompt 文本而非视觉素材。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/JetBrains/go-modern-guidelines |
| Star / Fork | 2,958 / 83 |
| Watcher / Open Issue / Open PR | 22 / 4 / 4 |
| 代码行数 | 3,034（语言：JSON 49.4%、Go 42.6%、PowerShell 11.4%、Shell 7.1%、Makefile 1.2%） |
| 注释比 | 34.4% |
| 运行时依赖 | 0（`go.mod` 无第三方依赖，guidelines 数据通过 `//go:embed` 编译进二进制） |
| 项目年龄 | 9 个月（2025-11-24 创建 → 2026-08-30 最新推送） |
| 总提交 / 贡献者 | 32 commits / 7 人（JetBrains 内部 Top3 占 90%，外部贡献率 ~10%） |
| 开发阶段 | 0.1.x 收尾期（v0.1.1 最新，2026-08 单月 15 commits 占总量） |
| 贡献模式 | 公司核心 + 社区补丁（PR #26 PowerShell 修复等已被吸纳） |
| 热度定位 | 中等热度（JetBrains 官方背书 + AI Coding Agent 风口 + 9 个月 2.9K stars） |
| 质量评级 | 代码 良好 / 文档 优秀（README 205 行 + FEATURES.md 2000 行自动生成 + CHANGELOG 38 行）/ 测试 基本（CLI + goversion + guidelines 三层覆盖，但无 CI workflow） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

`CHANGELOG.md` 明确「由 JetBrains, GoLand Team 维护」，署名邮箱 `goland@jetbrains.com` 见于三处 marketplace.json；外部博客署名作者 Artem Pronichev 来自 JetBrains Go 团队。这是一个**GoLand 团队的官方动作**，而非 JetBrains 平台中心的中立实验——他们就是 13K stars Kotlin、20K stars intellij-community、10K stars ideavim 之外新押注的 Agent 时代产品。

### 问题判断

作者在 README.md:17-23 直陈两大根因：

1. **训练数据截止日滞后**——LLM 没见过 Go 1.26 的 `errors.AsType[T]`、`new(value)`、`cmp.Or[T]`、`sync.WaitGroup.Go`，自然写不出来；
2. **频率偏置**——`for i := 0; i < n; i++` 是合法的、整段训练集里它的密度比 `for i := range n` 高，模型倾向写前者。

时机判断：Go 团队 2026 年加速在 `gopls modernize` analyzer 中实现「现代 API 替换」检测（参考 README.md:25 显式挂钩），Go 1.25~1.27 集中引入 generics 内建（`min/max/cmp.Or`）+ `errors.Join/AsType` + `testing/synctest` 等实战级新 API。**当官方 modernize 解决「事后修」时，GoLand 团队顺势做「写前导」补料 Agent 上下文——两边同一时间窗，互为表里。**

### 解法哲学

- **不重写 linter，而是补料 Agent**——不试图替代 `gopls modernize`，而是为 Claude Code/Codex/Junie/Cursor 提供 prompt 时需要的「上下文切片」。
- **小而当前的真理源**——单一 JSON 文件承载所有规则，schema 校验保证「newest-first 排序」「ID 唯一」「since_version 严格 major.minor」等不变量，启动期 fail-fast。
- **写前导 ≠ 写后改**——moltbook 评论把它定位为「更好品牌的 linter」，关键差异是「在 Agent 写之前提示 vs 写完报警」。这是 prompt-only 方案无法逾越的边界：dev.to 实测 5 个真实逻辑 bug 它都抓不到。

### 战略意图

三层战略意图：

1. **AI Coding Agent 时代卡位**——开发者越来越通过 Claude Code/Codex/Cursor 写代码，「教 AI 写现代 Go」的入口成为一个比 IDE 设置页更新更轻、更广触达的产品表面。JetBrains 把 GoLand 的「现代 Go 偏好」沉淀到标准化协议（Agent skill）里，对 IDE 主战场外的「代理即分发」动作。
2. **GoLand 现代器的协同**——GoLand 2026.2 内置的 `go fix` modernize 工具给「已存在代码」做事后修，go-modern-guidelines 给「新写代码」做事先导，两者同一时间窗发布。
3. **品牌型开源**——Apache-2.0、零商业付费、无需注册——交付的是 GoLand 团队在 Go 现代化议题上的**权威定义**。一个仓库同时接入 Anthropic、OpenAI、JetBrains 自家、Cursor、独立生态五个分发渠道，是极少数「一份规则、全平台署名」的案例。

## 核心价值提炼

### 创新之处

按新颖度 × 实用性排序：

1. **JSON 单一事实源 + 多 Agent 适配层 0 业务逻辑（transporter pattern）** — 新颖度高 / 实用性高 / 可迁移性高。完整数据图：`guidelines.json` → `schema.Parse` 校验 → Go 二进制 `//go:embed` → `go install` 缓存到本地 → 5 家 Agent 的 run-tool 脚本调用 → SKILL.md 教 Agent 怎么问。**任何一处改 JSON，所有 Agent 同时得到新内容，无需 4 个适配层各发一版。** 这是 content-as-data 设计最干净的形态。

2. **Go 版本感知过滤的工程实现** — 新颖度高 / 实用性高 / 可迁移性中。CLI 的过滤逻辑只 4 行（`guidelines.go:161-169 supportedGuidelines`），但实现价值在于 schema 设计把 `since_version` 摆平到 major.minor + 列表强制 newest-first，让「每条规则比较 since_version ≤ targetGoVersion」变成 O(n) 一次遍历而无需排序——**数据形状选择算法的经典做法**。同时支持 `devel` 别名（goversion.go:176-178），CLI 在 Go 1.28 dev 工具链下也能「假装是 1.27」提供目前所有规则。

3. **list/explain 渐进式披露 + 显式吞吐契约** — 新颖度中 / 实用性高 / 可迁移性高。`list` 返短 ID + 一行 summary（按 token 计费时代核心），`explain <id>` 返完整 before/after 示例——按需取数据，`stringListFlag` 支持 `--guideline-id=a,b,c --guideline-id=d` 与位置参数混用，把「传多个 ID」做成一行 `explain sync_waitgroup_go atomic_types`。explainer 输出的 `indentLines` 把所有多行字段以 4 空格统一缩进，**给模型提供边界信号**。

4. **schema 校验即 lint** — 新颖度中 / 实用性高 / 可迁移性高。`schema.Parse` 不只是 JSON unmarshal，而是启动期规则静态 linter：ID 必须 `^[a-z0-9_]+$`、`since_version` 必须 major.minor、整个列表必须 newest-first 排序（违例直接 panic）、impact 必须在 `Critical/High/Medium/Low` 枚举内、ID 不可重——任何破坏约束的 PR 都在 CI 启动的 Go 测试里炸掉。

5. **FEATURES.md 由代码生成而非手写** — 新颖度中 / 实用性高 / 可迁移性高。`make generate-features` 跑 `go generate` 触发 `featuresgen/main.go`，把 JSON 渲染成 2000 行 Markdown——人类可读的 README 与机器可读的 JSON 不可能脱节，`[x]/[ ]` 渲染方案（是否被官方 modernize analyzer 覆盖）做成了视觉信号。

### 可复用的模式与技巧

- **Transporter pattern**：`{数据真源}` + `{零业务逻辑适配层}` 是 AI Coding Agent 时代的通用工程范式——任何「知识/规则/规范」类项目都可用一份 JSON/Markdown 喂饱所有 Agent 平台。
- **Schema 启动期 fail-fast**：把不变量下沉到加载期而非消费期——CLI/Adapter 永远拿到已校验数据，省掉二次排序/校验逻辑。
- **指针字段强制显式标注**：`modernizer *bool`（schema.go:21）——用指针而非默认 false，强制 PR 作者显式回答「这条规则是否被官方 modernize 覆盖」，把治理压力转嫁给数据生产者。
- **多 ID 输入 flag 设计**：`stringListFlag` 允许 `--guideline-id=a,b,c --guideline-id=d` 与位置参数混用，自动去空去重（`normalizeGuidelineIDs`），把高频操作做成一行 CLI 调用。
- **POSIX + PowerShell 跨平台一致设计**：`dev-install.sh` (55行) / `dev-install.ps1` (67行) 严格镜像（`set -eu` ↔ `$ErrorActionPreference="Stop"`、原子替换 `.tmp.$$` ↔ `.tmp.$PID`、`GOFLAGS= GOWORK=off CGO_ENABLED=0` 切干净构建环境），并保留 trap/finally 块清理中途变量——跨平台分发路径在 production 上有真实 Windows 用户在跑（PR #26 已修复 PowerShell `&` 调用运算符）。
- **「JSON 数组存多行」字段优化**：`Example.Before/After` 是 `[]string` 而非单一字符串——给 prompt 渲染器一个「是否多示例」的判别位（`if len(examples) > 1` 才输出 `Example 2:` 标记），数据层保留粒度供消费层决策。

### 关键设计决策

1. **决策**：JSON 单一真理源 + 适配层 0 业务逻辑
   - **问题**：5 家 AI Coding 平台分发同一份规则表，N 个平台各自维护会脱节
   - **方案**：JSON 文件 → Go CLI（`//go:embed`） → 各 Agent 的 run-tool 脚本调用
   - **Trade-off**：失去「按平台定制规则」的灵活性，换取「改一行 JSON 全平台生效」的工程红利
   - **可迁移性**：高（任何「知识/规则/规范」分发场景可复用）

2. **决策**：list/explain 分层而非一次性返回全部
   - **问题**：Agent prompt 上下文窗口有限，全部 guideline 一次塞入会爆
   - **方案**：`list` 返短 ID + summary，`explain <id>` 按需深挖
   - **Trade-off**：Agent 必须学会两阶段调用，增加 SKILL.md 的 prompt 复杂度
   - **可迁移性**：高（任何 CLI/RAG 工具都可分层）

3. **决策**：启动期 schema 校验而非消费期校验
   - **问题**：JSON 数据可能在多平台分发中被篡改
   - **方案**：schema.Parse 在 `//go:embed` 加载时一次性 enforce（ID 唯一 / 排序 / 版本号格式），违例 panic
   - **Trade-off**：破坏 schema 的 JSON 会让整个二进制启动失败——但这反而是「数据完整性下沉到加载期」的合规设计
   - **可迁移性**：高（任何「数据驱动配置」项目可复用）

4. **决策**：Go 版本源三选一冲突而非合并
   - **问题**：CLI 同时接受 `--go-version=1.27`、`--file-path=go.mod`、`go env GOVERSION` 三种来源，歧义场景下用户期望不一致
   - **方案**：`listVersionSourceConflictError`（cli.go:62-77）显式报错而非智能合并
   - **Trade-off**：用户必须知道当前用的是哪种来源，换来「不猜测、可复现」
   - **可迁移性**：高（任何多源输入 CLI 都可借鉴）

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | go-modern-guidelines | gopls modernize | uber-go/guide | golangci-lint | 社区散落 Agent skill |
|------|---------|--------|--------|--------|--------|
| 写前导 vs 写后修 | **写前导**（prompt 内嵌） | 写后改（linter 报警） | 不适用（文档） | 写后报警 | 写前导（粗糙） |
| 上下文窗口适配 | **列表/详情分层** | 不适用 | 不适用 | 不适用 | 不分层 |
| 团队规范 vs 版本规范 | **版本感知** | 版本部分感知 | 团队规范 | 多个 lint 规则 | 不版本感知 |
| Agent 适配层 | **5 家原生**（Claude/Junie/Codex/Cursor/skills.sh） | 无 | 无 | 无 | 单一平台 |
| 数据形态 | **JSON 单一真理源** | Go analyzer 源码 | Markdown | Go analyzer 源码 | Markdown |
| 跨平台分发 | **POSIX + PowerShell** | 不适用 | 不适用 | 跨平台 | 无 |

### 差异化护城河

- **写前导 + 上下文窗口 + 版本感知 + Agent 适配层**——四卡位同时拿到，这是唯一一家做到的。gopls modernize 在「团队强约束 + CI 卡点」占优，本项目在「Agent 上下文层」占优，两者上下游不同。
- **JetBrains 官方背书 + GoLand 团队权威定义**——外部团队很难短期复制「Go 现代写法」的事实标准制定权。
- **5 家 Agent 平台同步分发**——单一仓库同时接入 Anthropic、OpenAI、JetBrains 自家、Cursor、独立生态五个渠道，是少见的跨厂商合作落地。

### 竞争风险

- **gopls modernize 升级为「写前导」**——若 Go 团队未来把 modernize 与 gopls LSP 联动做成 IDE 弹窗提示（类似 vim-easy-align），本项目的核心优势会被官方工具链侵蚀。
- **JetBrains 战略转向**——若 GoLand 团队把 AI Coding Agent 押注收回到 GoLand IDE 内置技能，外部多平台分发可能减速（但 README 中 5 家平台均已稳定支持，短期风险低）。
- **「管理语法、不管理语义」边界**——dev.to 实测 5 个真实逻辑 bug 项目都漏掉，这是 prompt-only 方案无法回避的边界；如用户期望「AI 写无 bug 代码」，会失望。

### 生态定位

在整个 Go 生态扮演「**AI Coding Agent 时代的现代 Go 规则权威分发源**」角色——填补了「gopls modernize 做事后修 + Agent 写前无补料」的空白。是 JetBrains 对 Go 生态 Agent 化的标志性产品，与 GoLand IDE 互为表里。

## 套利机会分析

- **信息差**：中等——2.9K stars 已经把信号充分定价，但「JSON 单一事实源 + transporter pattern」这一工程范式本身有跨领域复用价值，懂 Agent 项目的工程师看到会立刻明白「我也能这样设计」。
- **技术借鉴**：极高——schema 校验即 lint、指针字段强制显式标注、list/explain 分层、跨平台 shell 镜像等设计可直接迁移到任何「版本感知规则集」「知识分发平台」「CLI + Agent 适配」项目。
- **生态位**：细分蓝海——「为 AI Coding Agent 提供 Go 版本感知现代写法」垂直定位无直接对手；与官方 modernize linter / uber-go/guide / golangci-lint 是互补关系。
- **趋势判断**：增长中——2026-08 单月 15 commits + v0.1.1 发布 + CHANGELOG 维护，下一波若是 0.2 / 1.0 将再进密集开发期；#12 已规划扩展到 Java/JS/Python/C#，这会把这个范式从「Go 专属」升级为「JetBrains 现代写法权威源」。

## 风险与不足

- **测试覆盖仅基本**：`commit_type_distribution` 显示 refactor=0% / test=0%——但这并非质量负面，而是「数据驱动」项目的天然特征（Go 代码只是 transport，重构需求不存在）。但 plugin/* 适配层（5 家 Agent）无自动化回归测试覆盖，任何 SKILL.md 改动都有破坏风险。
- **「管理语法、不管理语义」边界**：dev.to 实测 5 个真实逻辑 bug 都漏掉——这是 prompt-only 方案的本质局限，文档要更明确传达这一边界避免用户误用。
- **外部 fork 极少**（83 forks / 2.9K stars = 2.8% fork/star 比）——说明用户多在「消费」而非「改造」，社区生态深度有限；同时贡献者集中在 JetBrains 内部（90%），单点风险存在。
- **写前导 ≠ 写完报警**——moltbook 评论准确命中：这是「更好品牌的 linter」，与 gopls modernize 是上下游互补，不是替代。误用为「写完 bug 检测工具」会让用户失望。

## 行动建议

- **如果你要用它**：在你的 Go 项目里 `go install github.com/JetBrains/go-modern-guidelines@latest`，把 SKILL.md 接入 Claude Code/Junie/Cursor/Codex，让 Agent 在写 Go 时自动按 `go.mod` 版本切片现代 API 推荐。
- **如果你要学它**：
  - 必读 `internal/guidelines/schema/schema.go`（89 行启动期规则 lint）
  - 必读 `internal/cli/cli.go` + `internal/guidelines/guidelines.go`（list/explain 分层 + 多 ID 输入 + Go 版本源冲突处理）
  - 必读 `plugin/skills/use-modern-go/SKILL.md`（跨 Agent 平台 prompt 设计范本）
  - 必读 `scripts/dev-install.sh` ↔ `scripts/dev-install.ps1`（POSIX + PowerShell 跨平台镜像设计）
- **如果你要 fork 它**：
  - 替换 `guidelines.json` 为自家规范（如企业内部 Go 风格指南），CLI 与 5 家 Agent 适配零修改即生效
  - 扩展 schema 加 `team_specific_examples` 字段，把公司内部代码片段注入 explain 输出
  - 实现其他语言版本（Rust/Python/TypeScript）——JetBrains 已规划 #12 但尚未落地，是绝佳的「范式 + 新语料」套利机会

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/JetBrains/go-modern-guidelines |
| Zread.ai | 未收录 |
| 关联论文 | 无（非学术项目） |
| 在线 Demo | [JetBrains 官方 9 分钟演示视频](https://www.youtube.com/watch?v=_VePjjjV9JU)；最接近实战的还有 [DEV.to 上 refactor 1039 行 main.go 的实测文章](https://dev.to/gde/go-in-practice-writing-modern-go-with-ai-testing-jetbrains-go-modern-guidelines-and-refactoring-151o) |
| JetBrains 官方介绍 | [Help AI Coding Agents Write Up-to-Date Code with Modern Golang Skills（2026-08 博客发布稿）](https://blog.jetbrains.com/go/2026/08/24/help-ai-coding-agents-write-up-to-date-code-with-modern-golang-skills/) |
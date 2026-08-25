# GitHub 推荐：5 个月 2289 commits：Anthropic 怎么把 Claude 插件市场做成「SHA 钉死 + AI 自审」的供应链范例

> GitHub: https://github.com/anthropics/claude-plugins-community

## 一句话总结
Anthropic 用一个 GitOps 镜像仓把 Claude Code / Cowork 的第三方插件市场做成了「**SHA 强制钉死 + 11 条不变量 + Claude headless 自审 + 单写者内部管线**」的开源供应链治理样板，是 AI 时代 OSS 生态安全分发最值得拆解的工程范本之一。

## 值得关注的理由
- **不是代码仓库，是「目录治理仓」**：2289 个 commit 中 2175 条由 `github-actions[bot]` 自动 bump，核心资产是 1 个 1.5MB 的 `marketplace.json` 注册表 + 3 个 composite action + 4 个 workflow，理解 AI 时代的供应链治理不能跳过这个范本。
- **官方+社区双轨制**：Anthropic 把「策展制」（`claude-plugins-official`，无提交通道）与「自动化准入制」（`claude-plugins-community`，外部提交表单 + AI 扫描 + SHA pin）拆成两个仓，这是头部 AI 公司第一次把"插件供应链"做成可审计的开源基础设施。
- **可被复刻**：整套 bash action（validate / bump / scan）配合 `extraKnownMarketplaces` 让任何企业都能 fork 出一个「私有供应链治理管线」，GitOps + WIF + AI 扫描三件套是可迁移的工程范式。

## 项目展示

> README 与官网均为治理流程文字，无 hero / demo 图等展示性资产。仓库的"展示"价值在于其目录结构与 Action 工作流，参见下方架构解读。

**DeepWiki 三段式架构图**（唯一可引用的可视化资产，含 marketplace / validate / bump 三层流程）：
- https://deepwiki.com/anthropics/claude-plugins-community/1.1-repository-purpose-and-architecture

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/anthropics/claude-plugins-community |
| Star / Fork | 1,712 / 176（Watchers 16） |
| Open Issue / PR | 30 / 11 |
| License | Apache License 2.0 |
| 代码行数 | 1,398（Python 94.1% / JSON 4.5% / HTML 1.4%） |
| 文件数量 | 67 |
| 项目年龄 | 5.2 个月（首次提交 2026-03-20） |
| 总 commit | 2,289（95% 由 github-actions[bot] 自动生成） |
| 贡献者 | 10 人（github-actions 87.6%，Bryan Thompson 占人工 commit 76%） |
| 最近提交 | 2026-08-24 |
| 近 30 / 90 天 commit | 931 / 2,262 |
| 开发阶段 | 密集开发（但 99% 由 bot 自动 bump） |
| 开发模式 | 业余 Side Project 节奏（周末 38.4% + 深夜 16.9%） |
| 版本策略 | 无 tag/release（插件通过 SHA pin + freeze-shas.txt 黑名单治理） |
| 热度定位 | 中等热度（Anthropic 官方分发渠道，但远低于姊妹仓 `claude-plugins-official` 的 34k） |
| 质量评级 | 代码 优秀 / 文档 优秀 / 测试 充分（6 个 test 套件 + golden vectors） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景
维护者 Bryan Thompson 是 Anthropic 内部核心员工（263 commits），公司账号 `anthropics` 经营 5.7 年、83k followers。**这不是个人项目，是 Anthropic 从「产品公司」到「平台公司」的转折点配件**——`claude-plugins-official`（34k stars）+ `claude-plugins-community`（本仓）+ `knowledge-work-plugins`（23k stars）三个仓一起构成了 Claude Code 商业化的「双轮 + 内置实验场」。

### 问题判断
作者看到了三个同时存在的真空：
1. **官方仓无提交通道**：`claude-plugins-official` 在 README 里自承 "at Anthropic's discretion, no application process"——社区作者的产品没有落地窗口。
2. **社区合集无供应链审计**：`davila7/claude-code-templates`（量级大）、`lifangda/claude-plugins`（948 组件）、`JeremyLongshore/claude-code-plugins-plus-skills`（425 plugins）都是「目录卷积」，量大但没有任何机制能回答「三天前还能用的插件，今天还能信吗」。
3. **企业私有 marketplace 缺样板**：用 `extraKnownMarketplaces` 自建白名单需要整套治理管线，没有可借鉴的工程范本。

时机选在 Claude Code 商业化发布后，正是市场上出现大量「自带 plugin」二创的窗口期。

### 解法哲学
**GitOps over Forks**——这是本仓**最反直觉的设计决策**：明确写死「pull requests opened directly against this repo are closed automatically」（`close-external-prs.yml`）。把可控性留给内部、把扩展性留给外部：外面只能提交表单，内部管线才推 PR。**单写者模型 + 自动化补丁** 的极致表现。

**零 vendored schema**：把 schema 完全交给 `@anthropic-ai/claude-code` 包，本仓只跑 `claude plugin validate` + 11 条「policy floor」（安全/排序/SHA/metachar/hidden-Unicode）。**避免 schema drift** 是开源生态治理的经典痛点，用「源码随产品走」的子集化绕开。

**明确不做什么**：不做 IPC 给浏览器侧插件、不做 npm/pypi 自托管分发（保留 HTTPS URL 引用）、不做 CVSS 评分（policy prompt 只判 pass/fail + 两个 flag）、不做签名授权链（**用 SHA pin 这一层代替签名**）。

### 战略意图
在 Anthropic 更大图景中，这个仓是**基础设施层**——不是核心产品，而是 Claude Code 商业生态的「可审计分发管道」。完全 genuinely open：代码/Action/测试全部公开，**策略 prompt 是私有的**（避免检测逻辑被 opponent 提前适配）。这是**「代码开、策略闭」**的巧妭设计。

## 核心价值提炼

### 创新之处
按新颖度×实用性排序：

1. **「收敛 + 自动发布」跨 publisher GitOps pipeline**（新颖度 4 / 实用性 5 / 可迁移性 5）
   "每天 05:23 owner-liveness-sweep → 07:23 bump-plugin-shas" 双 cron，是「跨外部仓库用 GitOps 收敛」最干净的实例化。可迁移到 Docker Hub image catalog、ESP32 编译状态表等任何「需要从 N 个外部源收敛到一个集中目录」的供应链治理。

2. **Meta-action = MCP pin-check 静态器**（`scan-plugins/lib/pin-check.sh`，新颖度 5 / 实用性 5 / 可迁移性 4）
   用 jq 静态检签 spec 语法：`npx <pkg>@latest` 是 floating、`@scope/pkg@1.2.3` 是 pinned、`owner/repo#ref` 是 vcsref、`./path` 是 local、`@scope/pkg`（无版本）需下查 node_modules 验证 `vendored`。任何「stem-shell launcher / npm dist-tag 迫断」场景可移植。

3. **GitHub-OIDC-native WIF exchange**（`scan-plugins/action.yml`，新颖度 4 / 实用性 4 / 可迁移性 3）
   不存到 GitHub secret 的 static API key，用 GHA OIDC token 走到 Anthropic 端换短期 token。适用任何"非后台服务" + "需要 IAC" 的 CI 调用供应商 API 的场景。

4. **以 GitHub OIDC 为基础的 server-side signing**（`bump-plugin-shas` 用 GraphQL `createCommitOnBranch`，新颖度 4 / 实用性 4 / 可迁移性 3）
   不存 JWT/GPG key，直接让 GitHub 服务端签 commit。走「CI 补走 signature」而「接受 PAT」的新路径。任何 GitHub「required_signatures」ruleset 下的 CI automation 都可借鉴。

5. **Two-mode 双 token guarding**（`SHA_EXEMPT` / `FREEZE_SHAS` space-padded whole-word matching，新颖度 3 / 实用性 4 / 可迁移性 3）
   不是「list with comma」，是「space-padded」，仅 whole-word 匹配。让「I11-shape 名字」保 I11-shape 检查 + whole-word 跳过，免 list 蒸汽。「同 I11-shape 假 list 伪造」是 React-style 「hidden-Unicode character」类问题。

### 可复用的模式与技巧
1. **Composite 自验式 action**：validate / bump / scan 三兄弟只在内零身、黑在 root repo，外部者须 SHA-pin 拷贝（RELEASING.md 强制要求）。GitHub actions 自动升级是事实上的内部治理 secret，补救靠 SHA pin。
2. **共享 `lib/common.sh` 安全断言**：`assert_safe_url` / `assert_safe_sha` / `assert_safe_path` 能在「用户控参输入不能被 shell injection」的 CI 中抽出极简单人货。
3. **scope-errors-to-changed**（opt-in，默认 false）：PR 不动的条目上发现违规不是 error——这是 OSS 治理经典红牌问题的最优解：main 分支存量问题不会 freeze 所有无关 PR。I1/I2/I7 永远 ERROR 不能降级，其他可降为 WARN。
4. **静态 + 模式双轨审查**：pin-check 是确定性静态、scan 是 AI；模型负责「发现 ASAP」、代码负责「强制执行」。Anthropic Constitutional AI 的工程化落地。
5. **Pinned-base + freshness sweep**：类似 WAF「上周知」vs npm/a 股——在「上游 SHA」上锁可作 one-way reverse-cross-org 锁定。

### 关键设计决策
- **决策**: marketplace.json 取一个端点 × 多个 source kind 的根结构；source 必须 40-hex SHA 钉死
  - 问题：如何避免「装一个 plugin, 今天执行代码 A，明天执行代码 B」——升级中诱姙
  - 方案：source 下必须包含 sha=40hex 小写（I5），bump action 夜同贴出 stale-sha PR（max-bumps=30/天），逆向受控供给
  - Trade-off：心智成本 + 「升级需要人按钮」代价 + freeze-shas.txt 收首变表
  - 可迁移性：高
- **决策**: 三个 GitHub Actions 共享 `validate-plugins/lib/common.sh`，不互相调用
  - 问题：2282 × entry 的多验在不同场景下需要不同 surface area
  - 方案：gate (validate) → maintenance (bump) → policy (scan)，三者 Shotgun Surgery 共享 payload
  - Trade-off：每个 action 都要重调 install-claude-CLI，复制 8 秒代价到多个走马身
  - 可迁移性：高
- **决策**: bump 用 GraphQL `createCommitOnBranch`，不是 `git commit/push`
  - 问题：GitHub 自动 commit 需要 `required_signatures` ruleset 合规；PAT 生命周期 + secret 泄露是实际坑点
  - 方案：用 GraphQL 创建 commit，服务端用 GitHub App 签名。WIF 进一步上取消 secret
  - Trade-off：GraphQL 创建 commit 不能交互性 review、中间状态不可变
  - 可迁移性：高
- **决策**: **冻结 vs 免除双轨制**（freeze-shas vs sha-exempt）
  - 问题：同样不 bump，「这插件是作者故意不留 SHA」（exempt）与「这插件今天有 bug，不能上 pin」（freeze）需要不同治理动作
  - 方案：exempt = 本来不有 SHA；freeze = 当前 pin 被冻住；freeze-shas.txt 输入清单接受 "I11-shape 名" 仅作护照
  - Trade-off：两个并行概念需要泄露在调用者认知上
  - 可迁移性：中
- **决策**: 11 条 invariant 覆盖 hidden-Unicode（I10）+ slug 形状（I11）
  - 问题：OpenSSF Top 10 招中有「shell char / bypass」一类；描述字段中嵌 zero-width / bidi controls 能做 unseen placeholder
  - 方案：I10 检测 U+200B/U+200C/U+200D/U+202A-202E/U+2066-2069/U+FEFF；I11 仅接受 `^[a-z0-9][a-z0-9-]{1,63}$`
  - Trade-off：I1/I3/I5/I8 默认 WARN，调用者需使用 opt-out
  - 可迁移性：高
- **决策**: **WIF + cloned PATH scan**（scan-plugins）
  - 问题：Anthropic API key 存到 GitHub secret 是 1-failure-of-leak 的汉全域
  - 方案：GitHub Actions 启动 OIDC token，Anthropic 端调 federated token 来换 CLI 用
  - Trade-off：WIF 配置复杂（需 org-id + svac-id + federation rule id）
  - 可迁移性：中

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | 本仓 （community） | plugins-official | davila7/templates | lifangda | 企业私有 marketplace |
|------|----------------|-------------------|--------------------|----------|------------------------|
| 提交通道 | 外部表单 + 内部管线 | 官方策展，无通道 | PR 直推 | PR 直推 | 自建 |
| 供应链审计 | SHA pin + 11 invariant + AI scan | 手动 review | 无 | 无 | 自建 |
| 自动化 bump | 每日 05:23 UTC cron | 手动 | 无 | 无 | 自建 |
| Trust 门槛 | 中（自动 + 可审计） | 高（官方） | 低（量级大） | 低（单点） | 高（自管） |
| 插件覆盖广度 | 中（400+ 条目） | 中（官方精选） | 高（量级大） | 高（948 组件） | 自定 |
| 治理透明度 | 高（开源 + invariant） | 低（策展制） | 中 | 低 | 低 |
| 可被企业 fork | 高（整套 action） | 不适用 | 不适用 | 不适用 | 自建起点 |

### 差异化护城河
**「SHA pin + AI scan + owner identity baseline」三位一体**——这是周浅护身者面发不类象 pickback。`owner-baseline.json`「login→account id」基线 + `assert_safe_url` + 11 条 invariant 的组合，把「供应链防伪」从单一信任源（官方签名）扩展到「**拓扑 + 内容 + 身份**」三轴校验。

### 竞争风险
- **freeze-shas 数不退爬**：issue #995「Nightly bump sweep starves tail of marketplace.json」已报——`max-bumps=30/天` 触顶时尾部长尾插件被饿死。扩展性强但公平性弱。
- **单写者管线 SPOF**：issue #2370「Intake appears stalled: no plugin added to marketplace.json since 2026-08-07」揭示内部审核管线一旦停滞，下游 mirror 自然 stale，且无 fallback。
- **公 fieldn-side 同步延迟**：issue #14「Plugin approved but not syncing to community marketplace」——审核通过 ≠ 立即可装，作者有强体感。

### 生态定位
**「Anthropic 治理 / 社区激励」的均衡点**——在官方策展制（高信任低扩展）与社区合集（高扩展低信任）之间，用 **GitOps + 自动化准入 + AI 扫描** 创造第三种范式。整个 Claude Code 商业生态的「可审计分发管道」，是 Anthropic 从「产品公司」到「平台公司」的转折点配件。

## 套利机会分析
- **信息差**: 本仓是 Anthropic 官方分发渠道（不会被低估），但作为「AI 时代 OSS 供应链治理」案例在中文圈几乎未被解读。其工程范式（SHA pin + WIF + AI scan + scope-errors-to-changed）对国内做模型分发/插件市场的团队有直接借鉴价值。
- **技术借鉴**: 整套 `lib/common.sh` 安全断言 + 三个 composite action 可直接 fork 到企业私有 marketplace。WIF exchange 是 GitHub OIDC 在 AI 供应商场景的最干净落地。
- **生态位**: 「Anthropic 治理 / 社区激励」的均衡点——填补「官方策展制 vs 社区合集」的空白，是 AI 时代 OSS 生态安全分发的基础设施样板。
- **趋势判断**: Claude Code 商业化推进 + 国内对插件市场的监管/合规需求增长，这类「可审计分发管线」会成为模型生态的标准件，本仓的工程范式具有 6-12 个月领先期。

## 风险与不足
- **SPOF 风险（高）**：单写者内部管线一旦停摆，公开仓自然 stale（issue #2370 已实证）。需要冗余机制或 fallback。
- **公平性风险（中）**：`max-bumps=30/天` 触顶时长尾插件被饿死（issue #995）。需要更智能的 bump 调度（如按健康度 / 关键度加权）。
- **策略 prompt 私有化（中）**：避免检测逻辑被对手适配，但同时阻碍了社区贡献策略与复现。
- **依赖版本未锁（中）**：`claude-cli-version` default 是 latest，文档明示调用者应 pin 并走 renovate/dependabot；可用但不是锁。
- **CHANGELOG 缺失（低）**：样本插件有，主仓没有——故意 serve 为 GitOps mirror，但增加外部贡献者认知成本。
- **scope-errors-to-changed 默认关闭（低）**：调用者需手动 opt-in，default 仍保守——存量 main 分支上的违规会持续 fail 所有 PR。

## 行动建议
- **如果你要用它**: Claude Code / Cowork 终端用户直接 `claude plugin marketplace add anthropics/claude-plugins-community` 即可消费；如果你所在组织需要严格供应链审计，本仓的 `validate-plugins` action + 11 条 invariant 提供了「可复刻的工程样板」。
- **如果你要学它**: 重点关注 `.github/actions/validate-plugins/lib/common.sh`（安全断言模式）、`.github/actions/scan-plugins/lib/pin-check.sh`（jq 静态语法检签）、`.github/actions/bump-plugin-shas/scripts/bump.sh`（GraphQL commit + WIF）、`.claude-plugin/marketplace.json` schema。三个 composite action 的协作模型（gate / maintenance / policy）是 GitOps 治理的最佳实践之一。
- **如果你要 fork 它**:
  - 加 fallback 机制缓解 SPOF（如 webhook 心跳 + 报警）
  - 加智能化 bump 调度（按健康度 / 关键度加权）
  - 把 scope-errors-to-changed 改为默认开启
  - 把 11 条 invariant 拆成独立的配置项，便于 fork 者按需裁剪
  - 把策略 prompt 拆成「公共骨架 + 私有覆盖」，既允许社区贡献又保留检测逻辑的进化空间

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [anthropics/claude-plugins-community](https://deepwiki.com/anthropics/claude-plugins-community) — 已收录（last indexed 2026-06-23 commit `be53b7`），有完整三段式架构总结 |
| Zread.ai | 未收录（WebFetch 返回 403） |
| 关联论文 | 无（工程类项目，无学术关联） |
| 在线 Demo | 无（仓库本身是 catalog，非应用，无可演示 UI） |

**外部深度视角**（独立分析）：
- [Claude Code Plugin Marketplaces Compared — Where to Find Them and How to Choose](https://ice-ice-bear.github.io/posts/2026-03-20-claude-code-marketplaces) — 独立观点：把"官方 / 社区 / 第三方 demo"三类 marketplace 的治理模型放在一起横向比较，指出社区仓的 SHA-pin 是供应链保护的核心创新。
- [Skills, Connectors, Plugins, Oh My: A Security Practitioner's Map of the Claude Extension Ecosystem](https://pluto.security/blog/claude-extension-ecosystem-security-practitioner-guide) — 独立观点：列出社区仓仍存在的攻击面（SKILL.md prompt injection、SessionStart hook 静默执行、MCP 重定向到攻击者 endpoint），认为"自动化校验"≠ "已审计"。

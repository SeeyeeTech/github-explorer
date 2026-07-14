# GitHub推荐：188 天 4369 stars：单作者 Rust 把"AI 防误删"做成事实标准

> GitHub: https://github.com/dicklesworthstone/destructive_command_guard

## 一句话总结
一个独立开发者用 Rust 写的小工具，6 个月内在 GitHub 拿到 4369 stars —— 因为它几乎是为数不多真的能在 Claude Code / Codex / Gemini / Copilot / Hermes / Grok / Antigravity 七大 AI 编码 agent 执行 shell 之前把它们拦下来的护栏，并真实经历过 CVE 级别对抗并同日修复。

## 值得关注的理由
- **定义了品类**：2026 年 1 月 7 日首 commit 时这个垂直市场是空的，最近的竞品（claude-warden 28⭐、sh-guard 22⭐）比它小 100–200 倍。
- **真打过硬仗**：2026 年 7 月 security researcher 报告 CVE 7.1 级别漏洞，作者当日发 v0.6.6 修复并发布 GHSA 公告 —— GitHub 上几乎唯一有公开 CVE 履历的同类项目。
- **架构可移植**：7 层延迟预算 + drift guard、单 AC 扫描 + u128 candidate-pack bitmask、bounded recursion with `?`-propagation 这三个模式，任何做 latency-sensitive guard 的项目都能直接抄。

## 项目展示

![Destructive Command Guard — 阻止 AI agent 执行破坏性命令](https://raw.githubusercontent.com/dicklesworthstone/destructive_command_guard/main/illustration.webp)

*README hero illustration ——「防止 AI agent 误删你的代码」的核心命题*

![GitHub OpenGraph 社交卡](https://raw.githubusercontent.com/dicklesworthstone/destructive_command_guard/main/gh_og_share_image.png)

*官方 OG 社交分享卡*

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/dicklesworthstone/destructive_command_guard |
| Star / Fork | 4369 / 163 |
| 代码行数 | 165,163（Rust 86.0% / Shell 7.3% / PowerShell 2.3% / 其他 4.4%） |
| 项目年龄 | 6.2 个月（首 commit 2026-01-07） |
| 开发阶段 | 密集开发（v0.6.x 阶段，每月仍 30+ commits） |
| 贡献模式 | 独立开发（99.2% commit 来自 owner Jeff Emanuel） |
| 热度定位 | 中等热度（垂直领域第一，~23 stars/day） |
| 质量评级 | 代码 优（架构清晰、tests/prod 22.1%）· 文档 优（README+SKILL.md+docs/）· 测试 优（4208 个 #[test]，contract test 而非 smoke） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景
**Jeff Emanuel**（GitHub: `Dicklesworthstone`），NYC 独立开发者，bio 写「Building in NY」，Twitter `doodlestein`。账号 8.5 年，187 个 public repos，其中最有名的项目是这一堆「franken*」：frankenscipy、franken_numpy、frankenpandas、frankensearch、frankenredis、frankenlibc、franken_whisper、frankensim —— **统一主题是「用 Rust 重写主流 C/Python 工具」**。再加上 asupersync（238⭐）和 ntm（392⭐，Go 写的终端复用器）。dcg（4369⭐）是他目前最大、最严肃的项目。

### 问题判断
2025–2026 年 AI coding agent 大爆发，每个 agent（Claude Code / Codex / Gemini CLI / Copilot CLI）都有自己的 hook 协议 —— 但**没有任何一个工具能跨所有 agent、在 shell 命令执行前做 destructive command 拦截**。这是一个被所有人踩到、但没人修过的痛点。Emanuel 的判断是：与其让每个 agent 团队自己造轮子，不如做一个中立的「last mile safety layer」，各家 hook 都接进来。

### 解法哲学
**SKILL.md 里写得很清楚**：「Whitelist-First Architecture」、「Fail-Safe Defaults (Default-Allow)」、「Zero False Negatives Philosophy」。翻译一下：
- **宁可多弹几次确认，也不放过一次 `rm -rf /`**
- **遇到超时 / 解析失败 → fail-open**（让命令通过），但用 200ms 绝对上限 + 10ms 硬下限封顶，避免 perf 缺陷被武器化为 bypass
- **Zero False Negatives**：架构设计围绕「绝不让破坏性命令通过」展开，false positives 是可接受的代价

### 战略意图
商业化路径不明显（自定义 source-available 许可，**不是** OSI 批准的开源协议），但从 99.2% 单作者占比、25.8% 周末 commits、49.5% 夜间 commits 看，更像是「认真做的产品级 side project」而非商业项目。**Emanuel 用这一堆 franken* 项目建立 Rust 重写工具的品牌，dcg 是这个品牌下第一个冲到 4000+ stars 的旗舰**。

> 官方文档丰富（README+SKILL.md+docs/），但无独立官网/博客。本文未 WebFetch 作者个人博客 https://www.jeffreyemanuel.com/。

## 核心价值提炼

### 创新之处
1. **声明式预算常量 + drift guard**（novelty 5/5）—— `src/perf.rs:430-481` 的 `budget_documentation_matches_source_of_truth` 测试解析 README、AGENTS.md、ci.yml、bench.yml 四个文件，断言 7 层 Budget 常量的字面量文本一致 —— **从根本上消除了「文档说 5ms、代码写 50ms」的漂移**。
2. **u128 candidate-pack mask + 单 AC 扫描**（novelty 4/5）—— `packs/mod.rs:833-918` 把 91 个 pack 的 keywords 合成一个 Aho-Corasick 自动机，匹配后 OR 一个 u128 位掩码；比 per-pack memmem 扫描快 ~900 倍。
3. **有界递归 + `?`-propagation**（novelty 4/5）—— v0.6.6 修复 #189 的关键：递归上限 + 用 `?` 立即传播 unterminated 嵌套结构，**而不是 advance 一字节然后重新扫描**（重扫本身就是指数行为）。
4. **多 agent wire-format 多态 via serde aliases + per-agent emit struct**（novelty 5/5）—— 单 `HookInput` 通过 `#[serde(alias)]` 接受 7 种 agent 的 JSON，再用区分字段选 7 个 emit struct。**核心洞察：多协议兼容的真正难点是下游输出 parser 的字段严格性（Copilot 丢弃未知字段），不是上游输入的差异**。
5. **Fail-open + MIN_HOOK_TIMEOUT_MS=10 硬下限**（novelty 4/5）—— 200ms 绝对 fail-open 上限让 dcg 永远不会卡住工作流，但 10ms 硬下限防止用户配 `DCG_HOOK_TIMEOUT_MS=0` 来绕过护栏。

### 可复用的模式与技巧
| 模式 | 适用 | 代码锚点 |
|---|---|---|
| 声明式 Budget 常量 + doc-drift test | 任何有 SLO 的延迟敏感服务 | `src/perf.rs:430-481` |
| Fail-open deadline + min-budget floor | 任何同步 guard | `src/perf.rs:277, 321` |
| AC candidate-set bitmask | 50+ 规则的小关键字集规则引擎 | `src/packs/mod.rs:1916-1997` |
| 有界递归 + 保守触发-on-exhaustion | 任何面对不可信输入的递归下降 | `src/heredoc.rs:142-215` |
| Serde-alias 多态 + per-protocol emit | 任何多上游 + 严格输出下游 | `src/hook.rs:19-379` |
| Whitelist-first 两阶段评估 | 任何误报代价高的分类器 | `src/packs/mod.rs:492-553` |

### 关键设计决策
- **Fail-open on adversarial input**：攻击者构造能 hang 的 payload → dcg 超时后让命令通过。trade-off：✅ 不 brick 用户工作流；❌ 攻击者可构造总超时的命令绕过 → 由 MIN_HOOK_TIMEOUT_MS=10 + graduated_response 缓解。
- **单二进制 + YAML pack（regex-only）vs WASM/Lua 插件**：✅ 极快、极安全、审计友好；❌ 自定义 pack 不能用 ast-grep 结构化模式。
- **手写 rm parser**：replacement of regex-only 解决 `rm -rf` / `rm -r -f` / `rm --recursive --force` 三种 flag 风格的 span attribution。
- **多 agent hook 单 binary vs per-agent binary**：✅ 单安装足迹、单升级路径；❌ 每新 agent 都要新 emit struct。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | dcg | claude-warden | sh-guard | no-nuke |
|------|-----|---------------|----------|---------|
| Stars | 4369 | 28 | 22 | 2 |
| 语言 | Rust | TypeScript | Rust | Python |
| Agent 支持 | 7 个（Claude/Codex/Gemini/Copilot/Hermes/Grok/Antigravity） | 仅 Claude Code | 通用 | Claude+Codex |
| Pack 系统 | 91 pack / 27 类别 | 单领域 | 无 | 无 |
| AST heredoc 扫描 | ✅ | ❌ | ❌ | ❌ |
| 路径作用域 allowlist | ✅ | ❌ | ❌ | ❌ |
| 公开 CVE 履历 | ✅（GHSA-4cfr-w3v5-w5j5） | ❌ | ❌ | ❌ |
| License | 自定义 source-available | MIT | MIT | MIT |
| 体量 | 65k LOC | ~1k LOC | ~1 Rust file | ~Python 单文件 |

### 差异化护城河
1. **深度解析** —— 解析嵌入在 heredoc 里的 Python/JS/Ruby/Go/PHP/Perl/TypeScript/PowerShell/Bash，竞品都不做
2. **多 agent wire-format** —— 7 个协议适配，竞品至多 1 个
3. **生产硬化** —— 公开 CVE + 同日修复 + JSON Schema config + 10 个 GitHub Actions workflow + bench regression gate

### 竞争风险
- **claude-warden（TypeScript）**天然契合 Claude Code plugin 生态 —— 如果 Claude Code 团队自己做官方护栏，claude-warden 的部署门槛更低
- **agent 官方支持**：每个 AI coding agent 团队都有动机自建护栏（OpenAI、Anthropic、Google 都有工程资源做这件事）；一旦官方做了，dcg 在该 agent 上的护城河就没了
- **License 风险**：自定义 source-available 不是 OSI 批准，企业法务可能拒签

### 生态定位
**「AI coding agent 的最后一道防线」** —— 位于 agent → shell 之间，是一个垂直但关键的安全层。GitHub 上存在 `jms830/opencode-dcg-plugin`、`matznerd/antigravity-destructive-command-guard-dcg` 等 dcg 包装器，说明**它正在成为新 AI agent 默认对接的事实安全层**。

## 套利机会分析
- **信息差**：垂直蓝海 —— 最近竞品 100–200x 差距，但**这正是「市场还在演化」的红利期**，再过 6–12 个月可能会有 Anthropic/OpenAI 官方下场
- **技术借鉴**：
  - 任何 latency-sensitive guard → `src/perf.rs` 的 budget + drift test 整套
  - 任何多协议集成工具 → `src/hook.rs` 的 serde-alias + per-agent emit
  - 任何面对不可信输入的递归下降 → bounded recursion + `?`-propagation
- **生态位**：填补「跨 agent shell 拦截」空白；自然延伸方向是 audit trail + 合规报告（企业客户刚需）
- **趋势判断**：2026 年 AI coding agent 安全需求爆发期，月 commit 从 1131 降到 21 是「稳定维护」而非「停滞」信号；fix 数量远超 feat 是成熟期特征

## 风险与不足
- **Bus factor = 1**：99.2% commit 来自 Emanuel 一人；Jeff Emanuel 那 3 个 commit 看着是同一作者的另一个身份 → 任何主作者中断（健康/职业变动）项目立刻停滞
- **Fail-open 哲学本身是绕过向量**：#189 证明 perf 缺陷可被武器化为 security 缺陷；v0.6.6 修了那个具体 bug 但**已知 #191 REPL bypass**（stdin/pipe/subst 到 redis-cli/psql/mysql 尚未追踪）
- **License 风险**：自定义 source-available 不是 OSI 批准，企业法务审查可能不过
- **src/cli.rs 17,881 行**：逼近工程实践上限（>10k 行建议拆分），仍是第二大改动文件 → 拆分压力持续累积
- **nightly-2026-06-06 pinned**：rustix 1.1.4 已在 v0.6.3 引发过编译失败；未来 nightly 再次回归若未及时 unpin，发布链路可能再次断裂
- **PR 合并率仅 16%**：72% 的外部 PR 被关闭 → 主作者对路线把控严格，社区贡献吸纳率低

## 行动建议
- **如果你要用它**：
  - ✅ 适合：跨多个 AI agent 工作、需要 audit trail、生产环境有合规要求
  - ⚠️ 注意：先与法务确认自定义 license；开启 musl 静态构建（GLIBC_2.39 兼容性已知）
  - ❌ 不适合：只用一个 agent 且愿意等官方护栏、能接受 Python 工具链
- **如果你要学它**（按价值排序）：
  1. **src/perf.rs**（483 LOC）—— 整个操作哲学的最浓缩文件；doc-drift test 是项目最可复制的 50 行
  2. **src/evaluator.rs:1576-1815**（`evaluate_command_with_pack_order_deadline_at_path`）—— 240 行核心流水线，单函数拿下 70% 架构理解
  3. **src/packs/mod.rs:833-918 + 2533-2790** —— u128 candidate-pack bitmask + v0.6.6 #189 修复
  4. **src/hook.rs:19-379** —— 7 协议 + 7 emit struct，per-vendor interop 最浓缩示例
  5. **src/packs/core/filesystem.rs:335-433**（`parse_rm_command`）—— 手写 rm parser
- **如果你要 fork 它**：
  - 加 **multi-agent audit trail + 合规报告**（企业刚需，目前 dcg 没强调）
  - 加 **AI-driven 解释模式**（explain 命令目前只显示 byte span，可叠加 LLM 解释为什么这条命令危险）
  - 收紧 **REPL bypass #191**（stdin/pipe/subst 到 redis-cli/psql/mysql 的追踪）
  - 引入 **官方 Coop-Maintainer 计划**对冲 Bus factor = 1

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录（HTTP 403） |
| Zread.ai | https://zread.ai/Dicklesworthstone/destructive_command_guard |
| 关联论文 | 无 |
| 在线 Demo | 无（CLI 工具，需 `cargo install dcg` 或 `curl install.sh`） |
| 安全公告 | https://github.com/Dicklesworthstone/destructive_command_guard/security/advisories/GHSA-4cfr-w3v5-w5j5 |
| 作者博客 | https://www.jeffreyemanuel.com/ |

---

**分析时间**：2026-07-14  
**分析者**：repo-miner skill  
**方法**：三阶段分析（Network + Meta + Content）—— 中间产物存于 `tmp/destructive_command_guard-phase-{1,2,3}-analysis.md`
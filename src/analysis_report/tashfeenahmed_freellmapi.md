# GitHub推荐：4 个月 22K stars、34 家 LLM 免费档聚合：FreeLLMAPI 怎么把 7.4B token 折成一把 unified key

> GitHub: https://github.com/tashfeenahmed/freellmapi

## 一句话总结

FreeLLMAPI 是一个聚合 34 家 LLM 厂商免费档（~7.4B token/月）的 OpenAI 兼容自托管路由器，把"34 套 SDK + 34 套限流 + 34 套失败模式"压成"一把统一 key + 一个 `/v1` 端点 + 一套 fallback 链"，靠签名 catalog feed 和桌面临控作为产品护城河。

## 值得关注的理由

- **火箭式增长样本**：4.3 个月、647 commits、22K stars、3.1K forks、fork/star 比 14%（远超平均的 5-8%），是 2026 年最值得拆解的 OSS LLM infra 之一。
- **完整产品形态**：monorepo 4 workspace（shared/server/client/cli）+ 独立 Electron 桌面端 + Web SPA + 12 个 setup CLI（`setup-claude` / `setup-codex` / `setup-dsh` 等）+ 6 语言 i18n，不是 demo。
- **商业模式有想法**：开源 router 永远免费，premium 收入只用来维护「实时 catalog」——用目录延迟分级（free 30 天 / premium 0 天）做可持续现金流，避开多租户/SLA 的 scope creep。

## 项目展示

![FreeLLMAPI dashboard — Models page with the monthly token budget](https://raw.githubusercontent.com/tashfeenahmed/freellmapi/main/repo-assets/github-hero.png)
*Hero：Models 页面带月度 token 预算——产品核心 dashboard*

![One request in, the best free model out — the fallback chain with live scores, cooldowns, and quota tracking](https://raw.githubusercontent.com/tashfeenahmed/freellmapi/main/repo-assets/router-flow.png)
*架构图：fallback chain with live scores / cooldowns / quota tracking——这是项目的"心脏"*

![Free tier, stacked — ~7.4B tokens of free inference per month across 34 providers](https://raw.githubusercontent.com/tashfeenahmed/freellmapi/main/repo-assets/free-tier.png)
*规模感：~7.4B token/月 across 34 providers*

![Feature comparison against OpenRouter, LiteLLM, and Portkey](https://raw.githubusercontent.com/tashfeenahmed/freellmapi/main/repo-assets/comparison.png)
*竞品对照：vs OpenRouter / LiteLLM / Portkey*

![Playground page](https://raw.githubusercontent.com/tashfeenahmed/freellmapi/main/repo-assets/playground.png)
*Playground 试用界面*

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/tashfeenahmed/freellmapi |
| Star / Fork / Watcher | 22,237 / 3,110 / 107 |
| 代码行数 | 184,075（JSON 46.7% + TypeScript 44.7% + TSX 8.0% + 其他 <0.7%） |
| 文件数量 | 722 |
| 项目年龄 | 4.3 个月（首次提交 2026-04-21） |
| 总 commits | 647（近 30 天 194 ≈ 年化 1,800 commit） |
| 开发阶段 | 密集开发（6 月峰值 235 commits，7-8 月稳定 150-180） |
| 开发模式 | 职业项目（周末 30.6% + 深夜 29.5%） |
| 贡献模式 | 单人主导（Top 作者 Tashfeen 444 commits / 72.9%，第二名 suantea 仅 56） |
| 热度定位 | 大众热门（爆发型，4 月 0 → 8 月 22K） |
| Release | v0.9.0（共 35 tag / 25 release，~8 tag/月） |
| 商业实体 | Neu Software LLC（美国 LLC，托管 Stripe 收款） |
| 质量评级 | 代码 A / 文档 A / 测试 A |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

**Tashfeen Ahmed**，账号 11.9 年，公司 Microsoft（Dublin, Ireland），bio 写「Making useful things with Design + AI」。**他在自己 31 个公开仓库中，22K stars 全押在 freellmapi 这一个**——其余仓库最多 53 stars，是典型的"主仓爆款 + 周边实验"组合。同期的 scallopbot / AgentDomains / circlechat 等构成了他的 AI agent 产品矩阵。

销售走独立法人 **Neu Software LLC**（美国 LLC + Stripe 收款），与 Microsoft 正职解耦——典型的"大厂资深工程师 + 副业 OSS 创业"路径，bio 强调 Design + AI 双重背景（设计师 + AI 工程跨界），在 4 个月里能同时维护 monorepo 4 端 + 桌面端 + 6 语言 i18n + 12 个 setup CLI，背后正是这种 hybrid 能力。

### 问题判断

作者在 commit 故事线里留下了强 dogfooding 信号：**自己跑 Claude Code / Codex 时发现"任何一家 provider 限流就打断 coding 工作流"**——fusion、sticky session、context handoff、thinking trace 还原、reasoning_content echo 这些功能没有一个能从用户访谈反向推导，它们只在真实跑多轮 coding 任务时才会"突然 400 / hallucination"。

时机判断：2026 年 4 月，**几乎所有严肃 AI lab 都开了免费档**，单看每家是 toy，但叠加后每月 ~7.4B token 推理容量。**真正缺的不是 free tier，是"中间层"**。OpenRouter / Portkey / LiteLLM 都有类似中间层，但都把"免费"做成"便宜"——5% 抽佣 / $49+/月 / 配额紧，**没人把 "$0 = 设计目标" 写进产品定位**。

### 解法哲学

**做：** OpenAI 兼容 + 多 surface（OpenAI / Anthropic / Gemini / Ollama / MCP）+ 多模态（chat / embedding / image / video / speech / transcription）+ 实时目录 + 桌面端 + 12 个 setup CLI 一键配置 coding agent。

**不做：** 多租户 / 按用户计费 / SLA / 缓存复用 / 把目录托管到 GitHub 让 PR 维护（改走签名 feed）/ 任何企业 gateway 市场动作。Scope 故意收窄的痕迹在多处：README 写「single-user by design」，明确拒绝加入企业 gateway 红海。

**核心信念（README 标语）：**「The catalog moves fast. Your router should too.」+「Router 永远免费；premium 收入只用来维护目录。」——把 router 当作公地（commons），把目录当作运营活儿。**这是个比架构决策更深刻的产品判断：护城河不在代码（可抄），在运营（每周 30+ providers 改 quota）**。

### 战略意图

- **目录即护城河**：catalog-as-a-product 是 freellmapi 商业化的核心 IP。
- **Premium = 目录延迟特权**（free 30 天 / premium 0 天）：单一变量，避免"功能分级 vs 容量分级"的争议，强烈指向 B2C 现金流而非 B2B。
- **桌面端**（独立 Electron v0.9.0 节奏）：把"打开电脑就能用"作为差异化；Cerebras / Groq 高速免费 tier 让本地 app 体验胜过云端 SaaS。
- **大模型集成广度**：34 providers / 6 语言 i18n / 12 个 setup CLI——都是 distribution / 上游覆盖，而不是技术深度。

> 官方文档（freellmapi.co + docs/architecture.md）信息密度极高，但**未找到外部有深度的独立架构批判文章**（DeepWiki 拆解 + ngjoo 一篇节点文，但 ngjoo 文把它定位"个人玩具级"，未与 OpenRouter/LiteLLM 比较）。

## 核心价值提炼

### 创新之处

按新颖度 × 实用性排序：

1. **签名 catalog feed + tier 延迟分级**（Ed25519 签名 + premium 即时 / free 30 天延迟）—— 把"内容需要强新鲜度但客户端不能伪造"的场景模式化，**新颖度 4 / 实用性 5 / 可迁移性 5**
2. **Turn-integrity streaming pump**（header hold window + dialect marker probe + always-terminal finish_reason + reasoning_content echo）—— 不再"看到 chunk 就算成功"，把 stream pump 改成 "validation of the turn, not the transport"。**新颖度 5 / 实用性 5 / 可迁移性 4**
3. **Reasoning trace 持久化 + scoped replay**（per-session memory，只回放给同一 platform+model）—— 解决"客户端 strip reasoning_content / DeepSeek thinking 模型要求每轮 assistant turn 都带 reasoning_content"两难。**新颖度 5 / 实用性 5 / 可迁移性 5**
4. **错误体 quota learning**（provider 错误信息自动收紧 router 限制，如 Groq 413 with TPM）—— 让 router 自动适应 provider 错误格式变化。**新颖度 4 / 实用性 4 / 可迁移性 4**
5. **Fusion = virtual model id + 并行 panel + judge synthesis**—— 暴露成 OpenAI 模型 id（`fusion`），无需新 SDK。**新颖度 4 / 实用性 4 / 可迁移性 3**
6. **Helmet CSP 内联 SHA 钉死 + .gitattributes eol=lf 保护**—— 防 Windows clone 修 hash、防 #682 dark mode flash 的细节。**新颖度 4 / 实用性 5 / 可迁移性 5**
7. **Bandit preset + IANA-tz peak hours 权重位移**（`fastest`/`reliable` 豁免避免 preset 收敛到同一模型）—— 数学化 routing。**新颖度 3 / 实用性 4 / 可迁移性 3**
8. **Honest empty-completion 失败语义**（不 200 空响应、不记成功、空文本触发 fail over）—— 表面简单但 OpenRouter/LiteLLM 都做得很薄。**新颖度 3 / 实用性 5 / 可迁移性 5**

### 可复用的模式与技巧

- **共享 fallback loop + per-surface dispatch adapter**：4 个 wire surface（OpenAI / Responses / Anthropic / Gemini-Ollama-MCP）共享 `lib/fallback-loop.ts` 控制流；每 surface 只写 dispatch adapter。**任何"同一业务逻辑横跨多个 wire format"的 gateway 都适用**。
- **签名内容 feed + tier 延迟分级**：用 Ed25519 签名 + 公钥硬编码 + bundled migrations 作 floor（`MIN_CATALOG_VERSION = '2026.06.07'`）实现"内容强新鲜度 + 客户端不可伪造 + 商业模式可持续"的三角。**适用：威胁情报 feed / 路由公告 / 价格表**。
- **Per-key 配额账本 + 错误驱动的 limit learning**：每个 `(platform, model, key)` 维护 RPM/RPD/TPM/TPD 计数器（in-memory + SQLite 持久化）；429 / 5xx 触发 cooldown；provider 错误体里给 quota 数字会被自动学习为新限制。**任何多 provider quota-aware router 适用**。
- **Monorepo + `@freellmapi/shared` workspace 共享 types**：4 workspace 用纯 TS literal union 共享 Platform/Model/ApiKey/FallbackEntry；编译时强制一致 + Zod runtime 兜底。**任何 multi-surface 产品的 schema 治理基础**。
- **Boot 顺序 = log-redaction → safety-net → DB → declarative config → scheduled jobs**：每步前注释"为什么先做这一步"，是 prod-grade hygiene 的范本。
- **三重 AbortController**：`clientAbort`（client 关 socket）+ `hedgeAbort`（retry budget 超时）+ `clientGone`（commit point 之后不重试）—— 解决长 reasoning 模型 Ctrl-C 时 in-flight token 还在烧的问题。

### 关键设计决策

1. **决策**：单一共享 fallback loop 控制流
   - **问题**：4 个 surface 此前各自有 ~150 行 fallback 代码，已经 drifted（403 一天 vs 90s 冷却；exhaustion status 在 `/v1/messages` 永远 429 但其它 surface 是 400）
   - **方案**：控制流 + accounting 集中到 `lib/fallback-loop.ts`；wire-format 由 caller 提供 dispatch
   - **Trade-off**：dispatch 钩子 API 复杂（11 个参数），但保证一致性 > 单一 surface 优化空间
   - **可迁移性**：高

2. **决策**：Turn-integrity 而非 transport-level streaming
   - **问题**：#231 audit 发现 in-band error frames / 无 finish_reason / inline dialect 被当文本 / truncated 当成功
   - **方案**：header hold window + dialect marker probe + always-terminal finish_reason + reasoning_content echo
   - **Trade-off**：代码复杂（mode 状态机 undecided/passthrough/dialect），但每个 edge case 都是真实客户端失败反馈驱动
   - **可迁移性**：中-高

3. **决策**：Thompson sampling bandit + 多策略 preset + 时区-时间窗口权重位移
   - **问题**：手调 bonus 累加不可解释、维度不一、新模型要重新调
   - **方案**：所有信号 [0,1] 归一；preset 权重和 = 1；guardrails 是系数（不重排好模型）；peak-hours 用 IANA tz（不是 host local clock）
   - **Trade-off**：preset 灵活但"用户在哪个 preset"是反直觉问题；peak-hours 默认 off（避免"晚上 pick 不同"的玄学）
   - **可迁移性**：中

4. **决策**：错误体 quota learning + 持久化 cooldown 跨重启
   - **问题**：不同 provider 限制语义不同（some give headers, some embed in error body, some are silent）；硬编码每个 provider 的限制会很快过期
   - **方案**：运行时从错误体解析 limit（`learnLimitFromError`），自动收紧 router 自身的限制；持久化跨重启
   - **Trade-off**：学习机制本身可能因 provider 错误格式变化而失效
   - **可迁移性**：中

5. **决策**：Sticky session 30min TTL + reasoning trace 持久化
   - **问题**：多轮对话中途换模型会 hallucination spike（README 自报）；客户端 replay 历史时会 strip reasoning_content（opencode issue #24104）；DeepSeek thinking 模型要求每轮 assistant turn 都带 reasoning_content
   - **方案**：per-session trace memory + scoped replay（`PLATFORMS_REQUIRING_REASONING_ECHO` 只 opencode 一家）；超过 500 entries sweep TTL，超 1000 硬驱逐最旧
   - **Trade-off**：内存增长（硬 cap 1000）+ reasoning trace 大
   - **可迁移性**：高

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | FreeLLMAPI | OpenRouter | LiteLLM | Portkey | 9router |
|------|-----------|-----------|---------|---------|---------|
| 免费 tier 聚合 | ✅ 设计目标 | ⚠️ 附带，5% 抽佣 | ❌ 用户自管 | ❌ $49+/月 | ✅ 国内 |
| 自托管 | ✅ | ❌ SaaS | ✅ Python | ⚠️ 混合 | ✅ |
| 桌面端 | ✅ Electron | ❌ | ❌ | ❌ | ❌ |
| 多 surface 兼容 | ✅ OpenAI/Anthropic/MCP/Gemini/Ollama | ✅ OpenAI | ✅ 多 | ✅ OpenAI | ⚠️ OpenAI 为主 |
| Provider 覆盖 | 34 | 60+ | 100+ | 250+ integrations | ~10 |
| i18n | 6 语言 | 英文 | 英文 | 英文 | 中文 |
| Setup CLI 一键配置 coding agent | ✅ 12 个 | ❌ | ❌ | ❌ | ❌ |
| Turn-integrity | ✅（streaming pump） | 薄 | 薄 | 中 | 未知 |
| Reasoning trace replay | ✅ | ❌ | ❌ | ❌ | � |
| 商业模式 | Premium $19/yr / Lifetime $49 | 5% 抽佣 | 企业版 | SaaS 订阅 | 未知 |

### 差异化护城河

1. **Catalog 运营**（不是 router 代码）：34 providers × 每周改 quota 的运营工作，签名 feed + premium 分层把它变成可持续商业模式。**竞争对手可以抄 router，抄不动 catalog**。
2. **Setup CLI 一键配置 12 个 coding agent**：把"装 router" + "配置 Claude Code / Codex / Cline"两步合并成 `setup-claude` / `setup-codex` / `setup-dsh` 一行命令，降低 onboarding 心智成本。
3. **桌面临控**：本地化体验 / no-account / 单一 unified key；Cerebras / Groq 极速免费让本地 app 体验胜过云。
4. **Turn-integrity engineering depth**：每个 edge case（reasoning echo / dialect rescue / in-band error / empty completion）都有 issue 驱动，有测试守护——可信度 > 营销话术。

### 竞争风险

- **OpenRouter 上 free tier**：一旦 OpenRouter 把聚合做得更广、免费额度提到相似水位，freellmapi 的护城河只剩"自托管 + 桌面端"。
- **LiteLLM 杀回马枪**：若 LiteLLM 推出"开箱即用 dashboard + 签名 catalog"，freellmapi 的 UX 优势会消失。
- **Provider ToS 收紧**：当越来越多 lab 把 free tier 收窄到"professional use only"（Gemini 2026/03 ToS 已动），freellmapi 的根本模式面临 ToS 风险。
- **单人主导 bus factor**：444/647 commits = 68.6% 一人主导，任何长尾中断 = 项目停摆。

### 生态定位

**free tier 聚合的"公地"（commons）**——像 OpenStreetMap 对地图数据那样对待 AI 推理容量。商业化路径围绕 catalog 运营而非 router 本身。这与 OpenRouter（router SaaS）/ LiteLLM（library）/ Portkey（enterprise gateway）的根本差异：

> OpenRouter 想做"通用 router SaaS"，freellmapi 想做"free tier 聚合公地"。

## 套利机会分析

- **信息差**：freellmapi 不是被低估项目（22K stars + 3K forks + 真实 fork/star 比 14%）；但**其"Turn-integrity streaming pump + Reasoning trace scoped replay + Signature catalog tier"三件套是 LLM gateway 的稀缺 IP**——OpenRouter / LiteLLM 在这层都做得很薄，抄过来就是产品差异化护城河。
- **技术借鉴**：上面"可复用的模式与技巧"列的 6 项都是可直接抄的，**最高价值是共享 fallback loop + 签名 feed + turn-integrity 三件套**。读 `server/src/lib/fallback-loop.ts`、`server/src/services/catalog-sync.ts`、`server/src/routes/proxy.ts` 的 streaming 部分。
- **生态位**：填补了"个人开发者想要零成本用多家 LLM、又不想分别管理多组 key"的空白；OpenRouter 收费、LiteLLM 太工程化、Portkey 太企业、9router 偏国内。
- **趋势判断**：4 个月 22K stars + fork/star 比 14% + 月度 commit 仍 180+，**完全在增长曲线**。比 OpenRouter（增速放缓）/ LiteLLM（2025 末供应链攻击后修复期）/ Portkey（B2B 经济下行受影响）都有后发优势。但模式风险 = ToS 收紧——这是根本性脆弱点。

## 风险与不足

诚实评估：

1. **Bus factor 真实严重**：444/647 commits = 68.6% 一人主导 + 4 个月单仓 184K 行 + 商业模式强依赖 catalog 运营（依赖 Tashfeen 本人对 34 家 provider 改 quota 的敏感度）= 任何长期中断（健康 / 倦怠 / 转向）立刻显现。**Premium Annual $19 / Lifetime $49 的 LTV 算不出来，但目录运营成本（每周 34 家 review）是确定的**——单位经济可能脆弱。
2. **proxy.ts 单文件 2635 行**：单文件过大；dispatch closure 嵌套深（`route() => routeRequest()` 二阶函数）；拆分 proxy 与 chat-only handler 是合理重构。
3. **`Platform` literal union 50+ 成员**：每加 provider 要改 `shared/types.ts` + `server/src/providers/index.ts` + `server/src/routes/keys.ts` 的 `PLATFORMS` 数组——Phase 1 #50 揭示问题严重性。
4. **没有显式 ESLint / Prettier 配置**：风格一致性靠 code review；多人 PR 接入会暴露。
5. **Provider ToS 风险**：README 列出 Gemini 2026/03 新条款收窄到"professional or business purposes"、Cohere ❌ Avoid、NVIDIA "evaluation only"——free tier 聚合模式本身面临 ToS 风险。
6. **README 自我审视极诚实**：「Stacking free tiers has real trade-offs」章节列了 intelligence degrades as day progresses / latency varies / free tier changes without notice / no SLA——比任何 reviewer 都诚实，是项目可信度资产。

## 行动建议

- **如果你要用它**：适合**个人开发者 / side-project / coding agent 用户**跑 Claude Code / Codex / Cline，需要稳定 fallback + 不希望自己管理 34 套 key。**明确不适合生产 SLA 场景**（README 自己写"No SLA, by definition"）。Setup CLI 一键配置是最大卖点——`npx setup-claude` 一次搞定。
- **如果你要学它**：重点读这些文件（按价值排序）：
  1. `server/src/lib/fallback-loop.ts`（共享 fallback 范式）
  2. `server/src/services/catalog-sync.ts`（签名 feed + tier 延迟分级）
  3. `server/src/routes/proxy.ts` 的 streaming pump 部分（turn-integrity 三件套）
  4. `server/src/services/routing/scoring.ts`（bandit + IANA-tz peak hours）
  5. `server/src/services/ratelimit.ts`（per-key 配额账本 + 错误驱动 limit learning）
  6. `server/src/lib/error-classify.ts`（14+ 种错误分类 + sanitize 防密钥泄漏）
  7. `docs/architecture.md`（ASCII art + 责任矩阵 + ToS review）
- **如果你要 fork 它**：合理改进方向：
  1. **拆分 `proxy.ts`（2635 行）** + 拆分 `shared/types.ts` 里的 Platform union（按 provider family 拆文件）
  2. **catalog 运营 SOP 化**（缓解 bus factor；把"对 34 家 provider 的敏感度"沉淀成可移交文档）
  3. **加 ESLint / Prettier**（多人 PR 风格一致性）
  4. **加 `n` provider 之外的"任意 OpenAI-compat provider"支持**（让用户自填 base URL + model 名，不再改 types.ts）
  5. **加缓存复用**（README "Not yet supported"——但这会与"free tier 模式"冲突，需要慎重）

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [已收录](https://deepwiki.com/tashfeenahmed/freellmapi/)（含 [Server Architecture](https://deepwiki.com/tashfeenahmed/freellmapi/2-server-architecture) 与 [Glossary](https://deepwiki.com/tashfeenahmed/freellmapi/11-glossary)） |
| Zread.ai | 未收录 |
| 关联论文 | 无（应用层项目，非学术产出） |
| 在线 Demo | https://freellmapi.co（官网 live catalog + 文档站）+ [Playground 截图](https://raw.githubusercontent.com/tashfeenahmed/freellmapi/main/repo-assets/playground.png)（本地 self-hosted，无官方 hosted playground） |
| 外部深度视角 | [ngjoo 节点文](https://www.ngjoo.com/trending/projects/freellmapi/) — 定位"个人玩具级推理底座"（未与 OpenRouter/LiteLLM 横向比较） |

## 附：三阶段演化故事线

按 commit message 挑选最具叙事价值的节点：

| 时间 | Hash | Commit | 解读 |
|---|---|---|---|
| 2026-04-21 | `04e1503` | Initial release of FreeLLMAPI | 起点，第一行代码 |
| 2026-04-22 | `4e8dcf6` | Eight hundred million? No — one-point-three billion now. | 第二天就改了 README，免费 token 从 800M 吹到 1.3B——产品对"免费额度"是核心营销点 |
| 2026-06-XX | `8e31226` | chore(desktop): v0.3.0 for the Premium release | 桌面端独立 release 节奏开始 |
| 2026-07-XX | `cf0c216` | perf(compression): early-exit protected-span check in the per-line hot path | 性能优化在热路径上 |
| 2026-08-05 | `1e675cc` | feat(routing): fold community reliability priors into the Beta posterior | 路由算法引用贝叶斯先验 + 社区可靠性评分 |
| 2026-08-XX | `0a0bd24` | Inject an estimated usage frame when a streaming upstream omits usage | 当上游流式响应漏掉 usage 字段时本地估算 token |
| 2026-08-XX | `56eb257` | Add an opt-in Fetch Relay outbound transport | 新增 Fetch Relay 出站传输（绕过 GFW / 跨境链路） |
| 2026-08-XX | `e70d130` | Notarize the DMG itself, not just the app inside it | Mac 桌面端为分发做签名+公证 |
| 2026-08-26 | (latest) | v0.9.0 | 跨过 0.9 里程碑，下一步 v1.0 |

整体故事线：**MVP（4 月，12 commits）→ 集成爆发（5-6 月，304 commits）→ 算法 IP 化 + 平台打磨（7-8 月，331 commits）→ v0.9 锁版本冲 v1.0**。

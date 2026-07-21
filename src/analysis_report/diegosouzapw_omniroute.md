# GitHub 推荐：21.7K stars 的开源 AI 网关：OmniRoute 用 271 个 provider 把免费额度全打通

> GitHub: https://github.com/diegosouzapw/omniroute

## 一句话总结

OmniRoute 是一个「本地优先 + 271 个 provider 自动 fallback + 免费额度聚合」的 AI 网关，把 Claude Code / Cursor / Codex 等 IDE 用户的 quota 焦虑转化为一个可观测、可调度的资源面板。

## 值得关注的理由

- **增速惊人**：5 个月从 0 到 21,748 stars（≈ 4,350 stars/月），月均 commit 1,086 次，是 2026 年 AI gateway 赛道里增长最快的开源项目。
- **真实抓人痛点**：不是又一个「统一 LLM 接口 SDK」——它**整合了 90+ provider 的免费层**（含 11 个永久免费），号称 ~1.4B free tokens/月，瞄准的是「Claude Pro + Cursor Pro + Codex + Qoder 这种订阅组合」的「实际可调用算力」难题。
- **工程纪律示范项目**：24 个 GitHub Actions workflow + 22 条 hard rule + 3,313 个测试文件 + mutation/property/schemathesis 三套 nightly 验证 + parallel-cycle release model——技术资产的复用价值远超 AI gateway 产品本身。

## 项目展示

![README hero 架构图](https://raw.githubusercontent.com/diegosouzapw/omniroute/release/v3.8.49/docs/diagrams/readme-hero.svg)
— 类型： hero（README 顶部价值主张架构图）

![免费额度预算卡片](https://raw.githubusercontent.com/diegosouzapw/omniroute/release/v3.8.49/docs/diagrams/free-tier-budget.svg)
— 类型： architecture（~1.4B tokens 资源池可视化）

![4 级 fallback 流程图](https://raw.githubusercontent.com/diegosouzapw/omniroute/release/v3.8.49/docs/diagrams/tier-cascade.svg)
— 类型： architecture（核心 4-tier cascade：订阅 → API key → cheap tier → free tier）

![痛点解法 10 组对照](https://raw.githubusercontent.com/diegosouzapw/omniroute/release/v3.8.49/docs/diagrams/why-pain-fix.svg)
— 类型： architecture（开发者 10 大痛点 ↔ 对应解法）

![3 层 resilience 流程](https://raw.githubusercontent.com/diegosouzapw/omniroute/release/v3.8.49/docs/diagrams/resilience-layers.svg)
— 类型： architecture（provider circuit breaker + connection cooldown + model lockout）

![18 策略网格](https://raw.githubusercontent.com/diegosouzapw/omniroute/release/v3.8.49/docs/diagrams/strategies-grid.svg)
— 类型： architecture（18 routing strategies）

![主仪表盘截图](https://raw.githubusercontent.com/diegosouzapw/omniroute/release/v3.8.49/docs/screenshots/MainOmniRoute.png)
— 类型： screenshot（Next.js dashboard 实时面板）

视频教程：
- 🇧🇷 Português（主作者母语）：[https://www.youtube.com/watch?v=Rxdc36yUyOQ](https://www.youtube.com/watch?v=Rxdc36yUyOQ)
- 🇺🇸 English：[https://www.youtube.com/watch?v=CMzyOiUyEVc](https://www.youtube.com/watch?v=CMzyOiUyEVc)
- 🇷🇺 Русский（瞄准俄罗斯用户）：[https://www.youtube.com/watch?v=il_5Ii6v4-Y](https://www.youtube.com/watch?v=il_5Ii6v4-Y)

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/diegosouzapw/omniroute |
| Star / Fork | 21,748 / 2,958 |
| 关注者 / Open Issue | 128 / 152 |
| 代码规模 | 1,518,165 行（其中 TypeScript 55.1% · JSON 28.1% · TSX 11.8% · JS 3.4%），9,994 文件，2834 个 TS/TSX 业务文件 |
| 注释率 | 47.4%（含 i18n JSON） |
| 依赖 | 124（runtime 74 + dev 50） |
| 项目年龄 | 5 个月（首 commit 2026-02-18） |
| 开发阶段 | 密集开发（近 30 天 918 commit，月均 1,086） |
| 贡献模式 | 创始人主导 + 社区辅助（Diego 占 75.7%，385 名贡献者，dependabot[bot] 第 3） |
| 热度定位 | 大众热门（5 月龄 21k+ stars） |
| 质量评级 | 代码优 · 文档优 · 测试优（25,000+ tests、mutation/property/schemathesis 三套 nightly） |
| License | MIT |
| Release 节奏 | v3.8.49（5 个月从 v1.0.0 → v3.8.49，312 个 tag，~100 个 release，平均 1.5 天一个 release） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

**Diego Rodrigues de Sa e Souza**（diegosouzapw），12.1 年 GitHub 老账号，圣保罗·巴西，CDWA Solutions 商业主体。本人是重度 Claude Code + Codex + Cursor 用户，CLAUDE.md / AGENTS.md / GEMINI.md 三个 agent 友好的辅助文档（46KB + 37KB + 8KB）说明他同时在用 Claude / Codex / Gemini 多种 agent。这种「dogfooding 出身 + 跨厂商订阅」的背景决定了 OmniRoute 的产品哲学不是「做一个新 SDK」，而是「把我手里分散的 6 个订阅整合成一个 quota 面板」。

### 问题判断

现有 LLM 路由方案的共同盲区是 **free tier 整合层**：
- **LiteLLM**（32k stars，Python 库）：统一调用接口但没有 free tier catalog。
- **OpenRouter**（30k stars，SaaS）：聚合模型但要付费。
- **Portkey**（8k stars，企业 gateway）：偏 B2B observability。

OmniRoute 抓住的真空：「Claude Pro OAuth + Cursor Free + Qoder Unlimited + Gemini Pro free + Cerebras 1M/day」这种**跨厂商、跨计费模式**的额度聚合，**实时面板 + 自动 fallback**。CLAUDE.md 自己列了 10 个「日常疼痛」，其中「quota 无人用 + 编码中途撞 429 + 团队订阅共享困难」是 OpenRouter/LiteLLM 都解决不了的。

时机：2026 年初正值 Anthropic/OpenAI/Google 各自推 Coding Agent + 多 IDE 接入，OAuth 流程成熟，让「跨厂商订阅路由」从不可能变成可行。

### 解法哲学

**简洁优于功能完整（但保留 critical mass）**：
- CLAUDE.md 22 条 hard rule 强制：no raw SQL in routes、no silent error swallowing、no raw err.stack leak、no PII redaction default-on。
- 3 层 resilience（provider circuit / connection cooldown / model lockout）——一个 key 挂了 ≠ 整个 provider 挂了 ≠ 一个 model 挂了。

**可恢复性优于性能**：4-state circuit breaker（CLOSED/DEGRADED/OPEN/HALF_OPEN）+ per-failure-kind thresholds + lazy recovery（无 background timer）——这是被 #4602（「Controller is already closed」误伤整个 Codex provider）教训逼出来的设计。

**开放优于封闭**：全 MIT、42 i18n locales、104 MCP tools × 31 scopes 公开、`.env.example` 120KB 暴露所有配置；公开承认「15 个 provider 因 ToS 被标注，自己决定」——不洗白。

**不做什么**（negative space）：
- 不做 SOTA 模型训练/微调
- 不做付费 SaaS gateway（README 强调「Free forever」）
- 不做 fine-grained observability SaaS（只有 self-hosted 面板）
- 不抢 enterprise SSO/SAML 市场（让给 Portkey）

### 战略意图

CLAUDE.md Rule #21 揭示**严肃的商业版图判断**：「Release-freeze — the FROZEN release branch belongs to the release captain; development does NOT stop (parallel-cycle model, 2026-07-04)」——这不是 hobby project 节奏。

作者已形成项目矩阵：OmniRoute 主仓 + OmniGlyph（compression-as-a-service）+ OmniAgentOS（agent 编排）+ awesome-omni-skills（skill marketplace）。**当前没有任何 enterprise / 付费 tier 的迹象**——README 自报「~1.4B free tokens/mo」的 reverse marketing 而不是「Sign up for Pro」。

战略意图清晰：**用开源占领所有个人开发者心智，把企业市场让给 Portkey，自己做 free tier aggregator 这个无人区**。

> 官方文档丰富（64,687 行 markdown）+ DeepWiki + Zread.ai 均已完整收录，docs/architecture/ 6 篇深度文档足够支撑此节分析。

## 核心价值提炼

### 创新之处

按新颖度 × 实用性排序：

1. **271 providers × 18 routing strategies × 12-factor auto-combo scoring**（新颖度 ★★★ / 实用性 ★★★★★）——把「哪些模型适合哪些 prompt」的隐式知识编码成 12 个可调旋钮（quota/health/cost/latency/taskFit/stability/tierPriority/tierAffinity/specificity/context/resetWindow/connectionDensity），每个都暴露为 env override。

2. **3 层 resilience（provider circuit / connection cooldown / model lockout）+ adaptive 4-state circuit breaker**（新颖度 ★★★★ / 实用性 ★★★★★）——per-failure-kind thresholds（OAuth 3×、API-key 5×、local 2×）+ lazy recovery（无 background timer）。

3. **DRR（Deficit Round Robin）+ P2C（Power of Two Choices）组合调度**（新颖度 ★★★ / 实用性 ★★★★★）——team 共享订阅的 quota fair-share + in-flight load 防 hot spot。

4. **Fusion strategy（parallel panel + judge synthesis）**（新颖度 ★★★ / 实用性 ★★★★）——一个 prompt fan-out 到 N panel models，judge 不是 merge 而是 analyze（consensus/contradictions/partial coverage/unique insights/blind spots）再 write one answer。

5. **11-engine pluggable compression stack**（新颖度 ★★★ / 实用性 ★★★★★）——RTK + Caveman + LLMLingua-2 + 量子锁等，prose-only compression + preserve code blocks + sentinel tokens 标记 fenced code/URLs/CONST_CASE。

6. **Hub-and-spoke format translator registry**（新颖度 ★★★ / 实用性 ★★★★）——8 协议（OPENAI/OPENAI_RESPONSES/CLAUDE/GEMINI/CODEX/ANTIGRAVITY/KIRO/CURSOR）两两互转 + same-format 通道下「stray `reasoning_effort` promote」 的边角补刀。

7. **isLocalStreamLifecycleError predicate**（新颖度 ★★★★ / 实用性 ★★★★★）——把「enqueue-after-close on our own ReadableStream controller」这种**本地 bug** 从 provider failure 中剥离，否则一个 bridge bug 会把整个 Codex provider 拉黑。

8. **Multilingual intent classifier 9 语言关键词路由**（新颖度 ★★ / 实用性 ★★★★）——纯同步 <1ms 把 prompt 分类为 code/math/reasoning/creative/simple/medium。

9. **Session pool + browser fingerprint rotation**（新颖度 ★★ / 实用性 ★★★★）——zero-auth provider（Pollinations/Puter）通过轮换 User-Agent + Sec-CH-UA 指纹防 rate-limit。

10. **describeFetchCause 把 undici AggregateError chain 展平**（新颖度 ★★ / 实用性 ★★★★★）——root cause 调试噩梦的终结者。

### 可复用的模式与技巧

直接可迁移的设计模式：

| 模式 | 位置 | 适用场景 |
|------|------|----------|
| **Strategy Pattern + opt-in pool** | `open-sse/executors/base.ts:255` | 多 provider / 多 SDK |
| **Hub-and-spoke translator registry** | `open-sse/translator/` | N 协议互转 |
| **Lazy-recovery state machine** | `src/shared/utils/circuitBreaker.ts` | Node.js 长进程 resilience |
| **3-layer resilience** | CLAUDE.md §Resilience | 多上游故障隔离 |
| **DRR + P2C 调度** | `quotaShareStrategy.ts` | team quota sharing |
| **Pluggable compression stack** | `open-sse/services/compression/engines/` | token-heavy 应用 |
| **Prose-only compression + preserve blocks** | `caveman.ts` / `ultra.ts` | LLM prompt 压缩 |
| **SSE TransformStream state machine** | `responsesTransformer.ts` | 协议 SSE 实时转译 |
| **Intent classifier (multilingual keyword)** | `intentClassifier.ts` | 零成本 prompt 分类 |
| **PII redaction opt-in + test guard** | CLAUDE.md Rule #20 | self-hosted proxy 默认值决策 |
| **Hard rules with CI enforcement** | CLAUDE.md §Hard Rules | 任何团队 |
| **Doc accuracy discipline** | `scripts/check/check-fabricated-docs.mjs` | 防 README 数字漂移 |

### 关键设计决策

1. **决策：双 workspace（Next.js app + open-sse streaming engine）**
   - 问题：如何让 streaming / format-translation 逻辑既能跑在 Next.js 内又能跑在 Cloudflare Workers / Deno Deploy / Electron？
   - 方案：`open-sse/` 作为独立 npm workspace，通过 `@omniroute/open-sse/*` 路径引用，`responsesTransformer.ts` 用 dynamic import for `fs/path` 实现 Node-only 模块的条件加载。
   - Trade-off：双 import 路径增加心智负担；换来 serverless deploy support。
   - 可迁移性：高。

2. **决策：Executor Strategy Pattern + opt-in pool**
   - 问题：80+ provider × 不同 URL/header/OAuth/streaming 行为如何管理？
   - 方案：`BaseExecutor` 提供统一 `execute()` 骨架，子类覆盖 `buildUrl/buildHeaders/transformRequest`；`default.ts` 处理所有 OpenAI/Claude-compatible，剩余 80 个子类只为协议不一致的 provider 存在。
   - Trade-off：每个 provider 一个文件 → 文件多但理解成本低。
   - 可迁移性：高。

3. **决策：3 层 resilience（provider/connection/model 三维独立 state）**
   - 问题：一个 provider 挂了 vs 一个 key 挂了 vs 一个 model 挂了，应该怎么隔离？
   - 方案：分别用独立 SQL 表（`domain_circuit_breakers` / `provider_connections` / `model_lockout`）+ 不同 state 字段 + 不同 backoff 策略。
   - Trade-off：schema 复杂度高；故障隔离粒度也高。
   - 可迁移性：高。

4. **决策：adaptive circuit breaker（4-state + per-failure-kind thresholds）**
   - 问题：经典 3-state CB 不区分 transient/permanent，也不防 open→probe→open 循环。
   - 方案：引入 `DEGRADED` + `kindThresholds`（per-failure-kind）+ `openCycleCount`（escalate backoff multiplier）。
   - 可迁移性：高。比 Resilience4j / Hystrix 默认配置精细很多。

5. **决策：Fail-open quota share combo（quota-share 永不被硬阻挡）**
   - 问题：team 共享订阅时所有 key 都 saturated，应该 503 还是允许？
   - 方案：「If EVERY connection is saturated, all are eligible again (fail-open)」。
   - 可迁移性：高。

6. **决策：Per-model upstream timeout override**
   - 问题：某些模型（如 o1）响应极慢，全局 timeout 触发 fallback 后用户体验差。
   - 方案：模型元数据里加 `timeoutMs`，`BaseExecutor.getTimeoutMs()` 优先读这个。
   - 可迁移性：高。

7. **决策：PII redaction 默认关闭（opt-in 而非 opt-out）**
   - 问题：self-hosted LLM proxy 默认开 PII 过滤会损坏本地 LLM 流量。
   - 方案：`PII_REDACTION_ENABLED` / `PII_RESPONSE_SANITIZATION` 默认 `"false"`，`tests/unit/pii-opt-in-default.test.ts` 断言 feature flag 默认值——任何人试图改默认被 test 拦截。
   - 可迁移性：极高。「对自家用户的善意假设」比「对所有人的恶意假设」更适合 self-hosted infra。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | OmniRoute | 9router | LiteLLM | OpenRouter |
|------|-----------|---------|---------|------------|
| Provider 数 | 271 | ~50 | ~100 | ~400 |
| Routing 策略 | 18 | ~5 | priority-based | tier-based（黑盒） |
| Auto-Combo 评分因子 | 12 | 启发式 | 无 | 无 |
| Free tier catalog | **90+ 真免费 / ~1.4B tokens/mo** | 无 | 无 | passthrough |
| MCP server | 104 tools / 31 scopes | 无 | 无 | 无 |
| A2A protocol | 6 skills | 无 | 无 | 无 |
| Compression 引擎 | 11（RTK+Caveman+LLMLingua-2） | 无 | 无 | 无 |
| TLS 指纹伪装 | JA3/JA4 via wreq-js | 无 | 无 | 无 |
| 部署形态 | 8 种（CLI/Docker/Electron/PWA/Termux/ARM/OpenCode plugin/Source） | 1-2 | k8s+Helm | SaaS only |
| i18n | 42 locales | 1-2 | 1 | 1 |
| Tests | 25,000+ + mutation/property/schemathesis | 不公开 | 有 | N/A |
| License | MIT | MIT | MIT | 商业 |
| 形态 | 本地优先 + SaaS 可选 | 本地优先 | Python lib + 托管 | SaaS |
| 成本 | 0 + 自有 API 费用 | 0 + 自有 API 费用 | 开源免费 / 托管付费 | pay-per-token 加价 |

### 差异化护城河

**技术护城河**：
- 271 providers 真实接入（不止 SDK wrapper，是 OAuth 流程、模型版本同步、quota 状态实时面板）
- 18 routing strategies × 12-factor scoring = 「我不知道哪个 provider 最适合」这个问题的**可观测、可调优**解
- 11-engine compression stack = token 成本 P&L 关键
- 3-layer resilience = 真实线上事故归纳的故障隔离粒度

**生态护城河**：
- 项目矩阵（OmniRoute + OmniGlyph + OmniAgentOS + awesome-omni-skills）形成网络效应
- 25,000+ tests + mutation/property/schemathesis 三套 nightly = 信任成本极高
- 42 locales + Discord/Telegram/双 WhatsApp 群组 = 用户社区护城河

**信任护城河**：
- 12 年老账号 + 个人占比 75.7% 的「创始人的项目」 = 决策连续性
- 公开承认 15 provider 因 ToS 被标注 = 不洗白文化
- 22 条 hard rule with CI enforcement = 工程文化可见

### 竞争风险

**最可能被替代的方向**：

1. **OpenRouter 推出 free tier aggregation** → 直接进入 OmniRoute 主战场。但 OpenRouter 是 SaaS，无 self-hosting 优势。
2. **Anthropic / OpenAI 收紧 OAuth 范围** → 15+ OAuth provider 优势消失。低概率（厂商希望扩大使用）。
3. **Codex / Cursor 等订阅内可路由 provider 涨价** → cost tier 优势收窄。已部分发生（issue #6778 Codex GPT-5.6 同步滞后）。
4. **9router 加快迭代速度** → 同赛道最危险对手，6× provider 差距可能在 1 年内被追近。

### 生态定位

OmniRoute 在整个技术生态中扮演**「个人开发者 × agent workflow × free tier」三角区的路由器**角色。Portkey 抢 enterprise，OpenRouter 抢零运维，LiteLLM 抢 Python，9router 抢轻量——OmniRoute 把**免费额度聚合**这个 niche 做到了极致。

## 套利机会分析

- **信息差**：5 个月 21k stars、100 release、月均 1,086 commit——这是少数被低估的「全栈工程示范项目」。**它不是又一个 AI wrapper**，而是把 **multi-provider resilience + protocol translation + token economy + distributed scheduling** 四个严肃工程问题装进一个产品形态。
- **技术借鉴**（按 ROI 排序）：
  1. **Lazy-recovery state machine**（无 background timer）——任何 Node.js 长进程。
  2. **3-layer resilience pattern**——任何多上游服务。
  3. **Hub-and-spoke translator registry**——任何协议适配层。
  4. **DRR + P2C scheduler**——任何 team-shared resource 分配。
  5. **describeFetchCause**（undici AggregateError chain 展平）——任何 Node.js HTTP 服务。
  6. **Doc accuracy discipline with fabricated-docs checker**——任何团队。
  7. **22 hard rules with CI enforcement**——任何团队。
- **生态位**：填补「个人开发者想最大化 AI 订阅 ROI」这个真实存在但被 LiteLLM/OpenRouter/Portkey 忽视的 niche。
- **趋势判断**：✅ 增长曲线无衰减（近 30 天仍 30 commit/天，7 月回升至 894），符合 2026 年「agent 时代 + 多厂商订阅 + cost pressure」的技术趋势。后发优势：CLIProxyAPI、9router 等同赛道对手规模仍小 5-6×。

## 风险与不足

1. **高度单核风险**：Diego 占 75.7% commit（4,461/5,429）。如果 Diego 退出或分心，项目失去节奏（参考 LiteLLM 在 Ishaan 退出时的复盘）。
2. **provider 版本同步滞后**：issue #6778（Codex GPT-5.6 models not supported，open 19 评论）是 gateway 类项目的「永恒问题」。271 provider 维护成本随数量线性增长。
3. **Windows 启动稳定性**：issue #7132（Windows Electron 3.8.48 SQLite DB → sql.js OOM → 500，open 16 评论）目前仍未解决。
4. **OAuth refresh token 反复回归**：issue #3850（refresh token nulled on first refresh，closed 18 评论）暴露「修一个，另一个被引入」的回归问题。
5. **激进承诺 vs 实际覆盖**：「271 providers」是 README 数字，但实际可用性需要逐个验证；DeepWiki 收录说明代码结构规范化但也说明「营销导向文档」与「真实可用性」存在差距。
6. **依赖治理风险**：dependabot[bot] 是第 3 大贡献者（149 commit）——供应链自动化程度高但若上游重大 breaking change 集中爆发，单 founder 难以响应。
7. **scale 与速度的 trade-off**：5 个月迭代 312 个 tag（~1.5 天/release）过快，bug fix 与 feature 几乎无隔离窗口（虽然有 parallel-cycle model，但「真正冻结的 release」难以验证）。

## 行动建议

- **如果你要用它**：
  - 个人开发者撞 quota：直接装 Electron Desktop 或 npm CLI，几分钟内可上手。
  - 团队共享 Claude/Cursor 订阅：Docker 部署 + 配置 quota share combo + DRR 调度。
  - 受地区限制（俄罗斯/中国/伊朗/古巴/土耳其）：3 级代理 + TLS JA3/JA4 指纹伪装是杀手锏。
  - 对比 9router：除非你只要最轻量，否则 OmniRoute 的 6× provider 数 + MCP/A2A 生态 + 25k tests 优势是压倒性的。
  - 对比 LiteLLM：若你是 Python 生态，OmniRoute 不抢这一块，但你愿意迁 Node.js 就能拿到 free tier + compression + agent protocols。
  - 对比 OpenRouter：若你想「零运维 + 单 payment method」选 OpenRouter；想「零持续成本 + 完全控制 + 更多策略」选 OmniRoute。

- **如果你要学它**：
  - **第一梯队**（直接抄就受益）：
    - `open-sse/executors/base.ts`（Strategy Pattern + opt-in pool）
    - `src/shared/utils/circuitBreaker.ts`（adaptive 4-state + lazy recovery）
    - `open-sse/utils/proxyFetch.ts:64-90`（describeFetchCause）
    - `open-sse/services/combo/quotaShareStrategy.ts`（DRR + P2C）
  - **第二梯队**（需要适配到自己的域）：
    - `open-sse/translator/`（hub-and-spoke registry）
    - `open-sse/services/compression/`（11-engine pluggable stack）
    - `CLAUDE.md §Resilience`（3-layer pattern）
  - **第三梯队**（领域特定，仅作 reference）：
    - `open-sse/services/fusion.ts`（parallel panel + judge）
    - `open-sse/transformer/responsesTransformer.ts`（Codex Responses API SSE state machine）
    - `open-sse/services/intentClassifier.ts`（multilingual keyword routing）

- **如果你要 fork 它**：
  - 改进方向：
    1. **解耦 `open-sse/` 与 Next.js** —— 让 streaming engine 真正可以独立 embed 到 Cloudflare Workers / Deno Deploy（CLAUDE.md Rule #21 的终极目标）。
    2. **插件化 provider registry**（呼应 issue #3594 community proposal）—— 让社区贡献 provider 不用 PR 主仓。
    3. **observability 增强** —— 在 fail-open 默认值之外提供可选 enterprise observability（SaaS 化路径）。
    4. **优化 Windows Electron SQLite 启动**（issue #7132）—— 改 sql.js → better-sqlite3 native binary 或 lazy load。
    5. **provider version sync automation** —— 用 n8n/Temporal 监控上游 release notes + auto-PR model registry 更新。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [https://deepwiki.com/diegosouzapw/omniroute](https://deepwiki.com/diegosouzapw/omniroute)（完整收录，覆盖架构/核心模块/数据流/部署/关键文件） |
| Zread.ai | [https://zread.ai/diegosouzapw/omniroute](https://zread.ai/diegosouzapw/omniroute)（已收录结构化摘要） |
| 关联论文 | 无（工程型项目，无学术对应） |
| 在线 Demo | 无官方 hosted demo；本地 `localhost:20128/dashboard`（需本地运行） |
| 官网 | [https://omniroute.online](https://omniroute.online) |
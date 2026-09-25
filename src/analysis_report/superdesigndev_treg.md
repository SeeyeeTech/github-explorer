# GitHub 推荐：3.3K stars 2 个月：「OpenRouter for agent tools」treg 怎么把 97 家供应商凭据藏在自己手里

> GitHub: https://github.com/superdesigndev/treg

## 一句话总结

treg 把 2,600+ 个第三方 API（97 家供应商）收编成一个「任务寻路」网关——**agent 只说"我要查邮件"或"我要截 SEO 关键词"**，不用关心背后是 Gmail、Outlook 还是 SES；**密钥永远不下发到客户端**，余额不足用 HTTP 402 + 机器可读 cost 字段优雅回应。

## 值得关注的理由

1. **赛道判断准**：2026 年 agent 从"对话框"走向"工具调用"是必然拐点，treg 在 MCP 协议定型前抢了"工具层 OpenRouter"的生态位，被 Claude Code / Codex / OpenClaw / Hermes 多家 host 集成。
2. **架构选择克制**：故意不做功能平移，而是当「Faithful Relay」透传代理——上游供应商的请求 schema 一字不改地透回去，规避了 Sandbox 安全事件型风险（对比 Composio 2026-05 闭源沙箱风波）。
3. **开源商业化样本**：AGPL/Apache+ 真开源 + 0% 加价（靠供应商返佣）+ pay-per-call，对比 Composio $29M / Arcade $72M 闭源 SaaS，提供了一个"独立团队也能跑"的差异化路径。

## 项目展示

![treg hero — 一个 token 接 97 家供应商](https://raw.githubusercontent.com/superdesigndev/treg/main/docs/assets/treg-hero.png)

*treg 官方 hero 图：单一 API token 替代 97 家供应商账号，凭据服务端注入，agent 客户端永不接触密钥。*

> 仓库 README 仅 1 张 hero 图；官网 `https://treg.to/` 在本轮 WebFetch 时返回 403（被 Cloudflare 阻断），无法补取 Demo GIF / 视频。可在 Claude Code 内通过 `/plugin marketplace add superdesigndev/treg` 实测。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/superdesigndev/treg |
| Star / Fork | 3,349 / 274（创建于 2026-07-15，仅 2.4 个月）|
| 主语言与代码量 | Python 113,560 行（占 25.8%）；总仓含 JSON 36.3% + YAML 33.4% 的 catalog 与上下文数据 |
| 项目年龄 | 2.4 个月（首 commit 2026-07-15，最新 2026-09-25）|
| 开发阶段 | 密集开发 |
| 贡献模式 | 职业项目（13-18 人协作，Top 1 = JayZeeDesign 占 47.8%，含 Cursor Agent / Claude 多 AI 编程代理重度参与）|
| 热度定位 | 中等热度 → 高速增长（外部报道日均 +193 stars）|
| 质量评级 | 代码 良好 · 文档 优秀 · 测试 基本（167 个测试文件，4 条 CI job，无 changelog/tag）|

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Jason Zhou（GitHub `@JayZeeDesign`）运营 Superdesign Org 账号 1.3 年，公开仓库 9 个，本仓在他最近 push 的仓库中**投入权重最高**（远超第二名 superdesign 设计工具的 7k stars）。他曾任 Relevance AI 产品设计负责人，另主持 AI Builder Club YouTube 频道（~200k 订阅），原生处在「AI 工具内容 + 工程实现」双栖位。

这条履历说明一件事：他不是在写一个"技术自嗨"的玩具，而是把过去 5 年积累的内容影响力 + 设计直觉，all-in 到一个**面向 builder 群体**的 agent 基础设施层。

### 问题判断

treg 的 README 一句话价值主张就是 "OpenRouter for agent tools, not models"——隐含的判断是：

1. 模型层已是红海（OpenAI / Anthropic / Google / Mistral），新入局者空间有限；
2. 但工具调用层是**碎片化真空**：Gmail、Slack、Notion、HubSpot、Semrush、Moz……每家一套 OAuth、一套 schema、一套计费；
3. agent host（Claude Code / Codex）每集成一个新工具都要重复实现 OAuth 回调 + schema 转译 + 凭据存储；
4. 现有方案（Composio / Arcade / Pipedream）要么闭源 SaaS，要么被大厂收购，**没有"开源 + self-host + 不抽佣"**这一档选项。

### 解法哲学

把 OpenRouter 在模型层的成功套到工具层，三条明确取舍：

1. **Faithful Relay instead of Schema Transpilation**——上游 schema 一字不改地透传，省去一层翻译出错的风险（Composio 2026-05 沙箱安全事件正是平移 schema 时引入的命令注入）；
2. **凭据永远不下发到客户端**——服务端注入，请求体里的密钥字段由网关填，客户端只看到自己的 trg_live_ token；
3. **0% 加价，靠供应商返佣**——不向用户抽成，赌未来能跟供应商谈 affiliate commission，类似信用卡返佣逻辑。

明确选择**不做什么**：不做 RAG、不做 memory、不做 agent framework；只当"工具代理层"，让上层框架（LangChain / CrewAI / Claude Code）自行设计 agent。

### 战略意图

`docs/context/architecture/money.md`（被修改 137 次的热点文档）说明 treg 已有清晰的商业化层：money seam 在 `domain/money/` 单一目录，跟业务逻辑解耦——这是为后续接 Stripe / 接入企业版预留的接缝。从 dsh-plugin 提交 Issue（#143、#549、#353）看，treg 想当 dsh 生态的 hub；但 hub 自己也还没装顺，是当下"想做平台但平台未通"的元层尴尬。

## 核心价值提炼

### 创新之处

| # | 创新点 | 新颖度 | 实用性 | 可迁移性 |
|---|---|---|---|---|
| 1 | **「按任务（capability）路由」**替代「按供应商名路由」——agent 只说"我要查邮件"不关心背后 Gmail 还是 Outlook | 4/5 | 5/5 | 5/5 |
| 2 | **Faithful Relay 不平移 schema**——上游请求原样转发，凭据服务端注入 | 5/5 | 4/5 | 3/5 |
| 3 | **证据驱动选路**——按实测成功率/速度/最近响应时延选 provider，不是凭配置 | 4/5 | 4/5 | 4/5 |
| 4 | **HTTP 402 + 机器可读 cost 字段**——余额不足不让 LLM 瞎试，agent 能自我调节预算 | 3/5 | 5/5 | 5/5 |
| 5 | **PyPI 包名≠项目名**（包是 `tools-registry` 而非 `treg`）——为避 2020 年同名 regex 库抢注的命名分离 | 3/5 | 5/5 | 5/5 |

### 可复用的模式与技巧

1. **三步分离架构（Resolution → Credential Injection → Relay）**：把 "识别" "鉴权注入" "透传" 拆成三个独立阶段，每阶段可单测、可限流、可观测——任何 "API gateway as-a-service" 项目都可参考。
2. **Blame-classified failure（`application/call/types.py:13`）**：调用失败时分三类 blamed — provider bug / treg bug / user error，便于 SLA 审计；通用做法是给所有异常打 type tag，归因自动化。
3. **Three-set whitelist（`infra/upstream/relay.py:43-67`）**：header / query / body 各有白名单，"什么是用户数据 vs 什么是凭据"的分层定义——API 代理层必备。
4. **Single money seam**（`domain/money/`）：所有计费逻辑集中在单一目录，billing-provider 替换零侵入；做付费 API 必备。
5. **.gitleaks.toml + 历史全扫**：用 gitleaks 守秘密泄露，对公开 API 网关特别重要（他们天天接触客户密钥）。

### 关键设计决策

1. **决策**: 不做 schema 平移，Faithful Relay 原样转发
   - 问题： 现有方案在把 vendor-A 的 schema 转成 agent-friendly 形态时引入注入风险（如 Composio 2026-05 沙箱事件）
   - 方案： treg 只识别 host/ID 路由，凭据服务端注入，请求体原文透传
   - Trade-off: 牺牲了"统一 schema 给 LLM 看"的便利（agent 看到的是 Gmail 原生 JSON，不是 OpenAI 函数调用形态），换来了零转换安全
   - 可迁移性： 中——只有当上游 schema 稳定且不过分异构时才适用

2. **决策**: 凭据存在服务端 Org-Specific Tool > Org-Stored Secret > treg Platform Key 的优先级 ladder
   - 问题： 用户可能自备 key（BYOK），也可能买平台套餐，需要统一计费/路由逻辑
   - 方案： 单一优先级 ladder，分阶段匹配；任意阶段未匹配才走下一档
   - Trade-off: 引入 3 层状态机，理解成本上升，但换来灵活的计费模型
   - 可迁移性： 高——任何"混合云 + 客户自备资源"系统都可用

3. **决策**: 测试用 stash 而非重新构造，167 test files 但覆盖率重在 call_surface / catalog / routing / oauth / capacity 五类核心路径
   - 问题： 公开 API 网关的集成测试成本极高（打真实第三方 API）
   - 方案： snapshot 测试 + 真实流量回归，对外部 API 用 staged mocking
   - Trade-off: 牺牲了"100% 覆盖率"的洁癖，换来 CI 跑得动 + 真实可靠性
   - 可迁移性： 高——做聚合 API 的项目都能学

4. **决策**: 许可证故意双轨（网站 AGPL / GitHub Apache+附加，禁止托管转售）
   - 问题： 我想开源让社区参与，但不想被 AWS 直接抄走打包卖
   - 方案： Apache 2.0 主体 + 附加条款"禁止托管转售"（类似 Elastic / Confluent 早期策略）
   - Trade-off: 牺牲了一部分"纯净开源"形象，换来了商业模式不被大厂抄走的护城河
   - 可迁移性： 高——SaaS 创业项目都可参考

5. **决策**: 多后端 plugin 架构（`plugins/treg/` + `plugins/minimax/`）
   - 问题： 不同推理后端（Anthropic / OpenAI / Minimax）的 plugin 协议不完全兼容
   - 方案： plugin 层抽象，上层 `src/treg/` 不知道也不关心底层是哪个 host
   - Trade-off: 多一层抽象 → 调试复杂度上升；换来 vendor-agnostic 接入
   - 可迁移性： 高——做多云 / 多模型兼容层必备

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | treg | Composio | Arcade.dev | Pipedream Connect | Nango |
|------|------|---------|--------|--------|--------|
| Stars | 3.3k（2.4 月龄）| ~16k+ | ~5k+ | ~5k+ | ~4k+ |
| 开源 / 商业 | Apache+附加 / AGPL | 闭源 SaaS | 闭源 | 被 Workday 收购（闭源）| 开源 |
| 工具数量 | 2,600+ endpoints / 97 providers | 250-1,000 apps | ~100 toolkits | 2,800+ apps | 中等 |
| 商业模型 | 0% 加价，靠供应商返佣 | SaaS 订阅 | 企业版 | 已并入 Workday | 自部署 + SaaS |
| 凭据位置 | 服务端注入（永不落客户端）| 服务端 | 服务端 | 服务端 | 服务端 |
| DX | CLI + FastAPI | TS SDK 最好 | TS SDK | 工作流可视化 | RESTful |
| 已知风险 | 单点信任集中；py 包名≠项目名踩坑 | 2026-05 沙箱安全事件 | 目录较小 | Workday 收购后路线不明 | 偏向集成层非路由 |

### 差异化护城河

- **信任护城河**: "0% 加价 + 全程不接触客户端密钥"，对隐私敏感团队（医疗 / 金融 / 法务）有独立生态位；
- **生态护城河**: 在 MCP 协议早期抢到先发位置，被 Claude Code / Codex / OpenClaw 多家 host 内置；
- **技术护城河**: Faithful Relay 的"不平移"哲学在大型供应商 schema 频繁变更时（Google / Slack 每季度改 auth flow）有结构性优势。

### 竞争风险

最可能替代 treg 的不是 Composio 或 Arcade，而是：

1. **OpenAI / Anthropic 自家**做工具代理层（一旦 host 方觉得"我做"比"用第三方"更值得，hub 类项目必然边缘化）；
2. **大模型自带 tool use 框架**（OpenAI Assistants / Anthropic Claude with tools）持续扩 builtin tool，**挤压独立目录的生存空间**；
3. **Composio 重新开源化**（如果他们修复 2026-05 沙箱事件后选择转 open-core，凭 16k stars 存量可瞬间盖过 treg）。

### 生态定位

treg 处于「**LLM ↔ SaaS API**」中间层的最薄一层——上面的 agent framework（LangChain / CrewAI / Claude Code）和下面的具体 API（Gmail / Slack / HubSpot）都不 care 它存在，但两边都用它当工具源。它填补的不是"功能空白"，而是"**协议真空**"——尤其 MCP 还没成为 OAuth 标配、每家 host 都需自实现 OAuth 回调的当下。

> 大资金玩家（Composio $29M / Arcade $72M）已占住企业 SaaS 方向，但 treg 是当下少数**开源 + self-host + 返佣不抽佣**这一档的独立选项。

## 套利机会分析

- **信息差**: 中文圈对 treg 关注低于英文圈。3.3k stars、97 providers、AGPL 可 self-host——这套组合在"国内合规自部署 + 海外 SaaS 受限"团队里有独立生态位，但目前中文评测文 < 5 篇，是补内容窗口。
- **技术借鉴**: Faithful Relay 三步架构、blame-classified failure、three-set whitelist 三招可移植到任何 API gateway 类项目（甚至自己公司的内部 API mock 服务）。
- **生态位**: MCP Registry / Claude Code plugin / dsh-plugin 三个分发渠道的"工具源"角色短期内不会重叠。
- **趋势判断**: 2.4 月 3.3k stars + 月均近千 commit + 仍在 release 0（无 tag）= 典型"早期 0→1 阶段"，现在介入是"搭便车"还是"接盘"取决于 treg 后续能否跑通供应商返佣 + 是否会被 OpenAI/Anthropic 自家吃掉。

## 风险与不足

1. **单点信任集中**：all-in 一个第三方代理你的 97 家供应商密钥，安全模型比"每家独立 OAuth"脆弱得多——一旦 treg 被攻破，攻击者拿到的是跨多个 SaaS 的全集密钥。
2. **供应商 ToS 风险**：0% 加价模式依赖未来跟供应商谈返佣，**当下**对 Semrush / Moz / Crunchbase 这类禁止转售的 API 服务可能已在踩 ToS 红线（待合规审计）。
3. **许可证不一致**：网站 AGPL vs GitHub Apache+附加条款，给法务审查带来 friction，企业用户法务会要求解释。
4. **包名混乱**：PyPI 包是 `tools-registry` 而项目 README 处处写 `treg`，2020 年还有一个无关的同名 regex 库——对自动化安装 / `pip install treg` 的用户极不友好。
5. **CI 跑不通**（来自 mrkeyoor.com 评测）：pytest 在他们环境没全跑通，说明快速迭代 → 测试缺位的典型 side project 风险。
6. **dsh 平台安装/分发不完整**（Issue #549 / #353）：想做 hub 但 hub 自己也还没装顺的元层尴尬，反向说明人手有限。

## 行动建议

- **如果你要用它**: 优先用 self-host 或 BYOK 模式，避免被平台返佣 + 供应商 ToS 风险波及；用 FastAPI SDK + 原生 host（Claude Code）接入，避开 dsh-plugin 不稳定的部分。
- **如果你要学它**: 重点关注 `src/treg/api.py`（FastAPI 路由层）+ `src/treg/call_surface/`（call flow 抽象）+ `docs/context/architecture/money.md`（计费模块），这三块是它的设计精华；不要复制它的产品定位（赛道已有大资金玩家）。
- **如果你要 fork 它**: 可改进方向：（a） 补齐 CLI / PyPI 包名一致性（解决 `tools-registry` vs `treg` 混乱）；（b） 补 test 覆盖（167 test 偏少）；（c） 把 money seam 的 affiliate 逻辑拆出成独立 OSS 库，让其他人能在不 fork 整个 treg 的情况下复用 0% 加价返佣模型；（d） 加 Web 管理 UI（已有 dashboard 但社区要求更多）。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [deepwiki.com/superdesigndev/treg](https://deepwiki.com/superdesigndev/treg)（已收录，含 Faithful Relay 架构图、5 大子系统、核心模块 Wiki 索引）|
| Zread.ai | 未收录 |
| 关联论文 | [ToolRegistry: A Protocol-Agnostic Tool Management Library for Function-Calling LLMs (arXiv 2507.10593)](https://arxiv.org/abs/2507.10593) — 学术参考实现，与 treg 商业化形成对照；[Securing GenAI Multi-Agent Systems Against Tool Squatting (arXiv 2504.19951)](https://ar5iv.arxiv.org/html/2504.19951) — Zero-Trust Registry 思路同源 |
| 在线 Demo | 无官方 playground；可在 Claude Code 内 `/plugin marketplace add superdesigndev/treg` 实测 |
| 官网 | [https://treg.to/](https://treg.to/)（CI 环境 WebFetch 403，需直接访问；GitHub Pages 类似限制）|

---

**外部深度视角参考**：

- [Treg review for teams trusting one proxy with keys — mrkeyoor.com](https://mrkeyoor.com/repos/treg)：Setup 3/5、Docs 5/5、Community 4/5、Maturity 3/5；指出 pytest 未跑通、加密密钥/数据库/访问策略需 owner 自管、许可证非标准限制托管转售。
- [Heatdrop Editorial — Treg Wants to Be the OpenRouter of Agent Tools, Not Models](https://heatdrop.ai/editorial/superdesigndev/treg/2026-09-05)：独立观点——「faithful relay」是明智的"不做就少错"选择，但把信任集中到一个第三方是单点失败风险。
- [treg 实测：一个注册中心，让 AI 调通 3600 个 API — 头条](https://www.toutiao.com/article/7688618265555354155/)：踩坑提示——PyPI 包名是 `tools-registry` 而非 `treg`（后者是 2020 年的无关 regex 库），国内建议用邮箱注册而非 GitHub/Google。
- [Best AI Tool Finder 投资报告](https://bestaitoolfinder.com/treg)：Venture Potential 46/100 "Watch"，指出「0% 加价」商业模型薄、可能与 Semrush/Moz/Crunchbase 转售 ToS 冲突。

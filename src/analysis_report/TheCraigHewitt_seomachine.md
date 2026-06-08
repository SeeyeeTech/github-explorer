# 把整支 SEO 团队装进 Claude Code：Castos 创始人的 7K star 内容工作区

> GitHub: https://github.com/thecraighewitt/seomachine

## 一句话总结

seomachine 是播客托管 SaaS Castos 创始人 Craig Hewitt 开源的「Claude Code SEO 内容工作区」——把整支 SEO 内容团队压缩成 **11 个角色 subagent + 24 个 slash 命令 + 25 个营销 skill**，背后挂 **24 个确定性 Python 评分/分析模块**（content_scorer / keyword_analyzer / seo_quality_rater 等）和 **DataForSEO / GA4 / GSC 真实数据集成**，串成「选题研究 → 写作 → 评分优化 → CRO → WordPress 发布」的端到端流水线。它最值得学的不是代码，而是「**方法论编排 + 确定性评分兜底 LLM**」这套工程范式。7K star / 964 fork、MIT，是「配方型仓库」（fork 自用、2026-04 停更）。但作为 SEO 工具本身，它绕不开 Google 反规模化薄内容政策的根本风险。

## 值得关注的理由

1. **一个对抗 LLM 不确定性的硬核范式：确定性评分与 LLM 评判同构互校**：`data_sources/modules/content_scorer.py` 用五维确定性评分（humanity 30% / specificity 25% / structure_balance 20% / seo 15% / readability 10%，composite≥70 才过；humanity 靠正则查 26 个 AI 套话 + 数缩写 + 被动语态，specificity 查 vague words vs 数字/日期/人名引语），而 `.claude/agents/editor.md` 输出**与 content_scorer 完全同构的 JSON**（composite/dimensions/priority_fixes）——让 LLM 主观评判与正则确定性评分可互相替代、互相校验。配上 `/write` 的「Automatic Quality Loop」：Bash 跑 `content_scorer.py` → composite<70 自动取 priority_fixes 前 3-5 条改 → 复评 → **最多 2 轮** → 仍不过落 `review-required/` 交人。「凡能算的算死、LLM 只做算不动的，并让 LLM 输出与确定性评分同构」是任何要质量门禁的 LLM 生产流水线都能抄的工程模式。
2. **几个可直接迁移的 agentic 设计**：① **业务团队即 subagent 军团**——11 个单一职责 agent（seo-optimizer 只管 on-page、editor 只管「让内容像人」、meta-creator 只产 meta），`/write` 写完自动顺序触发 content-analyzer→seo-optimizer→meta-creator→internal-linker→keyword-mapper，各自落盘审计；② **方法论即 context markdown**——`context/` 11 个领域知识文件（brand-voice/style-guide/seo-guidelines/target-keywords）用 `@file` 注入 prompt，是 RAG-lite；③ **agent↔工具双衔接**——command 走 Bash subprocess 跑脚本解析 stdout，agent 内嵌字面 `from data_sources.modules.keyword_analyzer import ...` 直接执行。
3. **一个值得冷静看待的「AI 内容工厂」样本**：合法的工程价值（确定性评分、TF-IDF+K-means 关键词聚类、GSC 真实数据选题）扎实，但 `/scrub` + content_scrubber.py（去 15 个不可见 Unicode + em-dash 启发式 + AI 套话正则）坐实了「AI 生成内容仍带可识别痕迹」（#1 是首个 issue）——而**去字符指纹是表层化妆，改不了「规模化薄内容」的本质**。叠加 Google 2025-26「scaled content abuse」反规模化政策（大量纯 AI 站掉 60-80% 流量），纯自动产文有真实排名风险。

## 项目展示

![seomachine](https://opengraph.githubassets.com/1/thecraighewitt/seomachine)

> 工作流：`/research → /write → /optimize → /publish-draft`。README 是近 1000 行的 SEO 内容 SOP（≥2000 字、关键词密度 1-2%、Flesch 8-10 年级、3-5 内链、meta 50-60 字符）。营销落地页 seomachine.io，配套 YouTube 教程《I Built An AI Marketing Team With Claude Code》。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/thecraighewitt/seomachine（官网 seomachine.io） |
| Star / Fork | 7,097 / 964（fork/star ≈13.6%，远超常规 1-3%，典型「fork 下来填自己公司 context 自用」） |
| 代码规模 | tokei 计 ~13.8K-17K 行 Python（98.7%）——**但严重低估**：另有 122 个 .md 工作区文件（11 agent + 24 command + 25 skill + 11 context）未计入；注释比 0.591（极高，为让 AI 读懂工具刻意重 docstring） |
| 项目年龄 | 7.3 个月（2025-10-29 首发，2026-04-10 停更，近 30 天 0 commit） |
| 开发阶段 | **低维护 · 配方型仓库**（仅 23 commit、无 tag、脉冲式：2026-02 集中 10 个） |
| 贡献模式 | 单人主导（thecraighewitt 69.6%/16 commit）+ 社区微贡献（5 人，多为 fix PR） |
| 热度定位 | 大众热门 · 高速增长（停更 2 月仍涨星，创作者传播驱动非版本驱动） |
| License | MIT（自带 API key 模式：DataForSEO/GA4/GSC 凭据全用户自配，无硬编码 key） |
| 质量评级 | 文档/双层架构「优」· 代码/错误处理「良」· 测试「弱（核心评分器零覆盖）」· CI「无」· AI 内容合规风险「高」 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

**Craig Hewitt（TheCraigHewitt）**——**Castos**（bootstrapped 播客托管 + 分析 SaaS）创始人兼 CEO，早年创办 Podcast Motor 后并入 Castos，深耕播客与内容营销近十年（Castos 博客是其最大获客渠道）。GitHub 13 年老号、224 followers。seomachine 是其「YouTube 教学（《I Built An AI Marketing Team with Claude Code》，频道 250→13K 订阅）+ 个人品牌 + SaaS 获客」内容飞轮的爆款产物——**内容营销老炮把自己跑通的 SEO 方法论固化成工作区**。他在持续押注「把业务流程打包成 Claude Code 工作区」这条线（其他 repo：skills 108★、hermes-chief-of-staff 81★、sales-skills、one-person-ai-agency），seomachine 是其中唯一爆款。

### 问题判断

纯 LLM 写 SEO 长文有两个硬伤：① **主观判断不可复现**（同一篇问 LLM「够不够好」每次答案不同，无法做质量门禁）；② **AI 痕迹**（em-dash 滥用、零宽字符、套话，既被检测又读着像机器）。现有方案都不够：Surfer/Clearscope/MarketMuse 是闭源 SaaS 单点工具（只做 on-page 评分或 topic 战略，不写、不发、不接真实流量）；Jasper/Frase 只做 AI 写作（不接 SERP/GA4/GSC、不端到端）。没有一个把「真实数据选题 + 团队角色编排 + 确定性质量门禁 + 发布」串成可复现流水线且开源可改。

### 解法哲学（agent 团队 + 确定性评分 + context 驱动）

① **把团队拆成角色**——11 个 subagent 各司一职，不是一个万能 prompt；② **确定性兜底主观**——凡能算的都用 Python 算死（密度、Flesch、字数对标、TF-IDF 聚类、0-100 评分），LLM 只做算不动的创意判断，且 editor agent 输出与 content_scorer 同构可互校；③ **方法论即 markdown**——`context/` 11 个领域知识文件是喂给 agent 的「公司大脑」，方法论沉淀为可版本化文本。`opportunity_scorer.py` 甚至把 Google 按排名位置的 CTR 衰减曲线（位置 1=31.6%、位置 2=15.7%…）写死进代码——营销老炮的领域常识被固化成确定性算法。

### 战略意图

「内容飞轮 + Claude Code 当业务流程运行时」的范式——不把 Claude 当聊天机器人，而是把一条完整业务流程（含 GA4/GSC 真实流量回流做选题优先级、WordPress REST + Yoast 字段自动发布）跑在 Claude Code 上。对比 Surfer/Jasper，刻意选「开源 + 端到端 + agentic 团队」差异化卡位，近乎独苗。

## 核心价值提炼

### 创新之处

1. **确定性评分器与 LLM 评判同构互校（content_scorer.py ↔ editor.md）**（新颖度 4/5，实用性 5/5，可迁移性 5/5）：editor agent 输出的 JSON 字段与 content_scorer 完全一致，使 LLM 主观评判与正则确定性评分可互替互校，被 `/write` 自动循环统一解析。适用任何「需可复现质量门禁」的 LLM 生产流水线。
2. **生成→评分→自动修→门禁路由的闭环（/write Automatic Quality Loop）**（新颖度 4/5，实用性 5/5，可迁移性 5/5）：Bash 跑确定性评分，<70 自动取 priority_fixes 改、复评、最多 2 轮，仍不过落 review-required/ 交人。适用内容/代码/任何可评分产物的自动迭代。
3. **11 角色 subagent 编排一支 SEO 团队 + 写完自动串联**（新颖度 3/5，实用性 4/5，可迁移性 5/5）：业务团队映射成单一职责 agent 军团，主命令自动触发下游 agent。
4. **段落级 TF-IDF + K-means 主题聚类 + 三路堆砌检测**（新颖度 3/5，实用性 4/5）：`keyword_analyzer.py` 把每个 H1/H2/H3 段落当文档，TfidfVectorizer(max_features=100, ngram 1-2) + KMeans 聚类取簇心 top-5 词当主题标签；堆砌检测三路并行（整体>3%、单段>5%、连续≥5 句）。
5. **方法论即 context markdown + 内置 Google CTR 曲线的 8 因子选题**（新颖度 3/5，实用性 4/5）：`opportunity_scorer.py` 8 因子加权（volume 25%+position 20%+intent 20%...）+ GSC 真实排名/CTR + 位置-CTR 衰减曲线算「快赢」（position 11-20）。
6. **AI 水印工程化清除（content_scrubber.py）**（新颖度 3/5，实用性 3/5）：15 个不可见 Unicode + Cf 类字符 + em-dash 上下文启发式替换 + AI 套话正则。但治标不治本（见风险）。

### 可复用的模式与技巧

- **Deterministic-Backstop-for-LLM**：凡能算的用代码算死、LLM 只做算不动的，并让 LLM 输出与确定性评分同构以便互校——任何要对抗 LLM 不确定性、要质量门禁的场景。
- **Generate-Score-Fix-Route 闭环**：生成→确定性评分→按结构化 fix 自动修→阈值路由（过/交人）——内容、代码、报告等可评分产物的自动迭代。
- **Business-Team-as-Subagents**：把真实团队角色拆成单一职责 subagent，主命令自动串联编排。
- **Methodology-as-Context-Files**：领域方法论沉淀为 `context/*.md` 模板，用 `@file` 注入 prompt——RAG-lite。
- **Dual agent↔tool 衔接**：command 走 Bash subprocess 跑脚本解析 stdout；agent 内嵌字面 Python import 直接执行。
- **Real-traffic-driven 优先级队列**：GSC/GA4 真实排名 CTR + 多因子加权（含位置-CTR 曲线）算 opportunity score。

### 关键设计决策

最值得记录的是 **「自动质量闭环」如何把 AI 编排与确定性工具真正咬合**——这是整个项目从「prompt 集合」升格为「工程系统」的关键。`/write` 命令里写死的 Automatic Quality Loop：写完草稿 → Bash 跑 `python data_sources/modules/content_scorer.py <draft>` → 解析 composite 分 → 若<70 取 `priority_fixes` 前 3-5 条自动改 → 复评 → 最多 2 轮 → 仍不过则落 `review-required/` 并附 `_REVIEW_NOTES.md` 等人工。这套闭环背后是两种 agent↔工具衔接机制：command 用 Bash subprocess 跑脚本解析 stdout，content-analyzer agent 则内嵌字面 `from data_sources.modules.keyword_analyzer import analyze_keywords` 让 Claude 直接执行。这个设计的 Trade-off 很务实：自动改 + 复评只跑 2 轮是「质量 vs 成本」的折中，review-required 兜底承认「AI 改不动的就交人」；它的深层价值是把「LLM 说这篇 8 分」这种不可复现的主观判断，替换成「content_scorer 算出 composite 72，humanity 维度因 5 个 AI 套话扣分」这种可复现、可门禁、可自动迭代的确定性信号。**这才是 seomachine 真正的护城河——不是 prompt 写得好，而是给 agentic 内容生产装上了确定性的质量闸。**

## 竞品格局与定位

| 项目 | 形态 | 定位 | 与 seomachine 差异 |
|------|------|------|------|
| Surfer SEO / Clearscope | SaaS 闭源订阅 | on-page 内容优化/评分 | 只管优化、不写不发不接真实流量；seomachine 开源复刻同类评分（seo_quality_rater 0-100）并嵌进端到端流水线。但 Surfer 的 NLP 有海量实时 SERP 语料，seomachine 是经验阈值 + 轻量 TF-IDF，深度不及 |
| Jasper / Frase / Writesonic | SaaS 闭源 | AI 写作 + brief | 只解决「写」，无确定性门禁/团队编排/真实数据/发布；seomachine 的 editor+content_scorer 闭环 + /scrub 更工程化。但 Jasper 有成熟 UI/品牌声音产品化体验 |
| MarketMuse | SaaS 闭源 | topic 集群战略 | 语义建模深；seomachine 用 cluster-strategist agent + research_topic_clusters.py + keyword_analyzer 聚类做轻量替代，语义深度不可比，胜在开源直接产文发布 |

### 差异化护城河

开源 + 端到端（选题→写→优化→发布）+ agentic 团队编排 + 确定性评分门禁，四者叠加在当前市场近乎独苗——没有竞品同时具备这四点。真正的护城河是「确定性评分兜底 LLM」这套工程范式，而非 prompt 本身。

### 竞争风险

- **AI 痕迹（实锤）**：#1 首个 issue「Remove AI watermark characters」+ /scrub 工具自证；去字符指纹改不了规模化本质。
- **Google 反规模化薄内容政策（根本性威胁）**：「scaled content abuse」政策下纯 AI 站 2025-26 大量掉 60-80% 流量——纯自动产文有真实排名风险，正确用法是「AI 起草 + 人工注入专业/数据/事实核查」。
- **数据集成鉴权门槛高**：GA4/GSC service account + DataForSEO 凭据全要自配（#58 GA4/GSC 鉴权被拒，open 未修），开箱即用性差。
- **停更 + 单人 bus factor**：2026-04 停更、无第二维护者，方法论会随 Google 算法演进过时（CTR 曲线、密度阈值都是写死常量）；核心评分器零单测覆盖。

### 生态定位

与其说是产品，不如说是**「可读可改的 SEO 内容生产 SOP 参考实现」**——最大价值是把「方法论 + agentic 编排 + 确定性评分」的工程范式开源出来供学习/二开，而非拿来即用的 SaaS 替代。

## 套利机会分析

- **信息差**：seomachine 是「Claude Code 从写代码走向跑业务流程」的标杆样本，「把整支 SEO 团队装进 Claude Code」概念极具传播力 + Castos 创始人背书；中文圈对「确定性评分兜底 LLM」「content_scorer↔editor 同构互校」「生成-评分-自动修-门禁闭环」「业务团队即 subagent」的工程拆解稀缺，且「AI 内容 vs Google 反规模化政策」的冷静评估有反差看点。
- **技术借鉴**：Deterministic-Backstop-for-LLM、Generate-Score-Fix-Route 闭环、Business-Team-as-Subagents、Methodology-as-Context-Files、agent↔工具双衔接——这些可迁移到任何 LLM 生产流水线（远超 SEO 本身，代码/文档/报告生产皆可用）。
- **生态位**：填补「开源 + 端到端 + agentic SEO」空白；与 Surfer/Clearscope（单点优化）、Jasper（只写）、MarketMuse（topic 战略）错位。
- **趋势判断**：踩在「Claude Code agentic workflow + 内容生产」趋势上；但「纯 AI 规模化产文」与 Google 反 AI 政策的根本矛盾决定了它的天花板——长期价值在「编排范式 + 确定性评分」这层可迁移资产，而非「自动产爆款」的黑盒承诺。

## 风险与不足

- **AI 内容合规风险（高）**：/scrub 去的是字符指纹，去不掉「规模化 AI 内容」的实质；Google 反规模化薄内容政策是对整个定位的根本威胁。正确用法需配人工把关。
- **数据集成鉴权门槛**：三数据源全要用户自带凭据 + service account，GA4/GSC 鉴权 issue 悬而未修。
- **停更 + 单人**：2026-04 后基本停更，无第二维护者，fork 后需自行维护，方法论随算法过时。
- **测试薄 + 无 CI**：实有 3 测试文件（数据层回归冒烟）但核心评分器零单测；无 .github、无 lint/test 自动化、无 tag/release。
- **质量强依赖 context**：README 自承「输出质量取决于 context 文件质量」，空模板上手即废；发布绑死 WordPress+Yoast 生态。

## 行动建议

- **如果你要用它**：适合有自有站点、想规模化产长文 SEO 内容的 SaaS/中小企业内容团队；先填好 `context/` 11 个模板 + 配 Claude Code + GA4/GSC/DataForSEO 凭据。**务必当「AI 起草 + 人工把关」用，不要当「装上自动产爆款」黑盒**——纯自动产文有 Google 反规模化政策的真实排名风险。注意上游已停更、鉴权门槛高。
- **如果你要学它**：直奔 `data_sources/modules/content_scorer.py`（五维确定性评分）+ `.claude/agents/editor.md`（与 content_scorer 同构的 LLM 评判）+ `.claude/commands/write.md`（Automatic Quality Loop，三层咬合的核心）+ `keyword_analyzer.py`（TF-IDF+K-means）+ `opportunity_scorer.py`（8 因子 + Google CTR 曲线）+ README（近 1000 行 SOP）。这是「确定性评分兜底 LLM + agentic 团队编排」的开源参考实现。
- **如果你要 fork / 借鉴它**：Deterministic-Backstop-for-LLM、Generate-Score-Fix-Route 闭环、Business-Team-as-Subagents、Methodology-as-Context-Files 是可直接迁移到任何 LLM 生产流水线的设计（不限 SEO）。MIT 友好；但作为 SEO 工具要清醒看待 AI 内容的合规边界。

### 知识入口

| 资源 | 链接 |
|------|------|
| 官网 | https://seomachine.io（价值主张「AI-Powered Content Creation That Ranks」） |
| 官方教程 | YouTube《I Built An AI Marketing Team With Claude Code (full tutorial)》（Craig Hewitt，最完整上手讲解） |
| 仓库文档 | README（近 1000 行 SOP）+ CLAUDE.md + QUICK-START.md + `examples/castos/`（填好的真实 context 范例） |
| 安装 | clone → 填 `context/` 模板（brand-voice/features/writing-examples）→ 配 API 凭据 → `/research` → `/write` |

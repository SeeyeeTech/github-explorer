# GitHub 推荐：4.8 个月 6.7K stars：中文发明人的「交底+查新+答复」一站式 Claude Skill

> GitHub: https://github.com/handsomestwei/patent-disclosure-skill

## 一句话总结
面向中国发明人的 Claude Agent Skill，把「挖专利点 → 国知局查新 → 三类专利分模板出稿 → 通俗解读 → 审查答复 RAG」做成可一键路由的五条产品线，且把「薄路由 + 类型隔离 + 人类在环 + 诚实查新」写进硬性工程纪律。

## 值得关注的理由
- **窗口红利精准卡位**：4.8 个月冲到 6,749 stars，是中文 + Claude Skill + 垂直法律场景三重新风口的爆款样本；按 commit 节奏估算日均 45+ stars。
- **CNIPA 一手接入 + 双段式查新算法**：唯一显式接入国知局 epub.cnipa.gov.cn 高级查询、按 IPC/LOC 分类号自适应回填的项目，英文 / 美系竞品全部做不到。
- **工程纪律可复用**：机读 stdout 前缀、opt-in / human-in-loop 闸门、CadQuery 隔离 venv、向量失败自动降级标签检索——这套「LLM ↔ 子进程」契约可迁移到任何垂类 Agent Skill。

## 项目展示

![Mode A 初版交底书（时间戳目录 + mermaid 流程图）](docs/效果例-初版生成.jpg)
*模式 A「发明交底书」一键出稿：每稿落进时间戳目录，mermaid 流程图自动按件编号 S1/S2 入图。*

![Mode A 多稿迭代更新](docs/效果例-迭代更新.jpg)
*同一项目多次迭代：每轮新时间戳，旧稿自动归档。*

![Mode B 通俗解读 + Canvas 知识图谱](docs/效果例-解读.jpg)
*模式 B 把公开专利拆成叙事 + 权利要求 + 术语表 + 线索图谱，落进 Obsidian 双链。*

![Obsidian 多专利关系图谱](docs/效果例-obs图谱.jpg)
*多专利关联：解读笔记 + 术语表 + Canvas 自动布局，专利 ↔ 概念 ↔ 申请人形成网状结构。*

![实用新型线稿（含部件序号引出线）](docs/效果例-实用新型专利线稿含部件序号引出线.png)
*实用新型按件拼装 SVG：每个零件一个独立文件，部件序号以归一化坐标锚点注入，可局部重画。*

![外观专利辅助线稿](docs/效果例-外观专利线稿.png)
*外观线稿：把立体 / 平面判别 + 要点落面做成门禁脚本，CAD 不入文图。*

![CAD 等轴测投影（CadQuery）](docs/效果例-cad提取等轴测投影图.png)
*CadQuery 等轴测投影：用户显式同意才 bootstrap，强制 Python 3.10–3.12 隔离 venv。*

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/handsomestwei/patent-disclosure-skill |
| Star / Fork | 6,749 / 761 |
| 代码行数 | 35,422 行（Python 79.7% / JSON 10.7% / JS 6.0% / YAML 3.1% / 其他）— GitHub 语言栏 Python 99.8% |
| 项目年龄 | 4.8 个月（2026-04-07 → 2026-09-02） |
| 总 commit | 35（首作者 handsomestWei 86.7%） |
| 开发阶段 | 稳定维护（近 30 天 18 commits，月均 7.3） |
| 贡献模式 | 单作者主导 + 4 人路过式 PR（dajiaohuang / xiaofengShi / HJ Ding / 917Dhj） |
| 热度定位 | 大众热门（细分赛道天花板量级） |
| 质量评级 | 代码 良好 / 文档 优秀 / 测试 基本（33 文件 / 35 commit） |
| 协议 | MIT（SKILL.md frontmatter `version: 3.9.0` 自维护协议版本，无 git tag） |
| 依赖 | 6 运行时（python-docx / latex2mathml / PyYAML / playwright / mammoth / python-pptx）+ 各子模块独立 requirements |

## 作者视角：为什么存在这个项目

### 创始人/作者背景
handsomestwei（display: handsomestWei），南宁，账号 8.5 年，公开仓库 95 个，GitHub 公司栏写「job wanted」（2026 年 9 月正在求职）。技术主线是 ML / RAG / 音频视频工程 / DevOps，**并非专利或 IP 实务背景**——项目专业深度来自「做中学」，工程迁移能力远超领域资历。同一作者还有 zhihu-fetch-skill(30★)、java-class-analyzer-mcp-server(42★)、customer-service-ai-agent(102★)、loop-skill(6★)，是中文 Agent Skill / 垂类 MCP 工具赛道的高频玩家。

### 问题判断
`SKILL.md:18-23` 把主诉写得很具体——「做了多年核心研发，专利发明人那一栏从没写过我的名字」。这不是代理人的痛点，是**中国发明人/工程师自己写交底书**的痛点：不知道挖点、查新凑数、Word 框图潦草、多稿管理混乱、看公开专利看不懂。这是一条被英文 / 美系专利工具系统性忽略的链路。

### 解法哲学
四原则写进 SKILL.md：

1. **薄路由 + 多模式互斥**：SKILL.md 只做路由（262 行），每步必须 Read 具体 prompt，A/B/C/D/E 五模式严格隔离，避免上下文污染。
2. **类型隔离**：发明 / 实用新型 / 外观三类专利 schema 物理分离，混模板必出错。
3. **人类在环**：模式 C 改技能 prompt 必须人确认；模式 D 草稿绝不自动提交；OA 答复多策略需门槛选定。
4. **诚实查新**：国知局召回过少时走分类码 / 相邻号回填，而不是伪造专利号凑数。

### 战略意图
这是核心产品（Skill Hub 范式仓库），不是基础设施。商业化信号弱——issue #1 招租、README 末尾「随缘支持咖啡」是边缘变现、非 SaaS 化路径。开源策略「genuinely open」。作者本人仍处求职阶段，技能产出节奏像全职但尚未绑定机构，**这是窗口期最容易被大厂挖走或被复制/抄袭的项目**。

## 核心价值提炼

### 创新之处（按新颖度 × 实用性排序）

1. **CNIPA epub 双段式查新 + 自适应回填**（新颖 4 / 实用 4）
   - 第一轮召回 → `extract_class_codes_from_html` 抽 IPC/LOC → 排序 1–3 高频号 → 第二轮走 `--class` 收口
   - 不足 4 条用 `backfill_hits_for_disclosure` 同分类号回补；外观用 LOC 不用 IPC
   - 证据：`tools/crawl/cnipa_epub_parse.py:66-219`、`prompts/disclosure/prior_art_search.md:16-37`

2. **三类专利 schema 物理隔离 + 共享 intake/figure_plan**（新颖 3 / 实用 5）
   - `structure.schema.yaml`（实用新型）+ `appearance.schema.yaml`（外观）+ 发明 `invention/disclosure_builder.md` 各走独立链路
   - 证据：`references/schemas/`、`SKILL.md:54-56`

3. **mermaid 显式步骤号写入可见标签 + 单块失败保留围栏**（新颖 4 / 实用 5）
   - `ensure_step_ids_in_visible_labels` 把 `S1[采集]` 自动改写成 `S1["S1 采集"]`，PNG 上能看到序号
   - 单围栏渲染失败不中断 md，保留源码继续出 Word
   - 证据：`tools/shared/mermaid_render.py:13-216`

5. **OA RAG 双轨：sqlite-vec + 标签过滤，向量失败自动回退**（新颖 3 / 实用 5）
   - `Embedder` 4 厂 preset（local / openai_compatible / zhipu / dashscope）；`EmbedError` 抛出 → catch 走 `tags_fallback`
   - 输出 `retrieval_mode` 字段让 Agent 透明告诉用户当前检索模式
   - 证据：`tools/oa/search_cases.py:127-150`、`tools/oa/store.py:67-405`、`tools/oa/config.py:26-71`

6. **按件拼装 SVG + 锚点叠标注入**（新颖 4 / 实用 4）
   - 每件独立 `parts/{view}_{id}.svg`，总图用 `<g id="part-{id}">` 相对路径引用
   - 部件序号以归一化坐标 `anchors.yaml` + SVG 精确曲线注入，不压扁零件层、不重生成整图
   - 证据：`tools/shared/structure_lineart_compose.py:238-432`、`structure_callout_overlay.py`

7. **LaTeX/OMML 双轨渲染（math）**（新颖 3 / 实用 4）
   - 发明公式默认走 Word 原生 OMML（`math_to_omml.py`），无须 matplotlib
   - 用户确认后才 `math_render.py` 预渲染 PNG；行内正则 `iter_inline_paren_spans` 显式处理嵌套括号
   - 证据：`tools/shared/math_render.py:40-70`、`md_to_docx.py --math-render`

### 可复用的模式与技巧

| 模式 | 适用场景 | 关键代码 |
|------|---------|---------|
| 薄路由 + 多模式互斥 | 多目标 Agent Skill | `SKILL.md:14-23`、各 prompt 顶部互斥声明 |
| 机读 stdout 前缀约定 | LLM 调用子进程 | `cnipa_epub_search.py:230-234`、`SKILL.md:51` |
| 诚实回填不编造 | 权威数据源检索 | `prior_art_search.md:16-37` + `cnipa_epub_parse.py:165-219` |
| opt-in / human-in-loop 闸门 | Agent 改技能 / 自动递交类 | `prompts/evolution/research.md:14-22`、`oa/respond_office_action.md:78-100` |
| AI 生图 + 锚点精确注入 | AI 标 + 人工精修管线 | `structure_lineart_compose.py` + `structure_callout_overlay.py` |
| 隔离 venv + 默认关 | 重依赖 Python 子工具 | `tools/shared/cad_venv.py:30-128` |
| 向量可降级标签 | 任一 RAG | `tools/oa/search_cases.py:139-150` |

### 关键设计决策

- **决策 1：thin router + mode A/B/C/D/E 互斥** — 用户必须先声明意图（`/patent-read`、`/交底书`、`/patent-evolve`、`/oa`），不能一锅端。换得零上下文污染。
- **决策 2：三类专利 schema 物理隔离** — 文件多、agent 跳目录成本高，但隔离保证正确性（方法 vs 形状构造 vs 视觉设计的法律客体差异巨大）。
- **决策 3：双段式查新 + 诚实回填** — 多一次 IPC 召回 / 多一次去重计算，换得「不污染交底书 + 不教用户撒谎」。
- **决策 4：机读 stdout 前缀约定** — `EPUB_HITS_JSON:` 单行 JSON 在 stdout，其余走 stderr ASCII；新贡献者必须学协议级约定，换得跨平台、跨 shell 稳定解析。
- **决策 5：CadQuery venv 隔离 + 默认不解析 STEP** — `isolated_env()` 删 PIP/PYTHONPATH/PYTHONUSERBASE；强制 Python 3.10–3.12；用户必须显式同意才 bootstrap。换得不强迫发明人装 3D CAD 库。
- **决策 6：按件拼装 SVG 而非整图 base64** — 多文件、agent 必须先出子件再叠标，换得「单件可重画、批改不必整图重出」。
- **决策 7：OA 答复「分差 + 门槛选定」** — 双维 0–100 相对分（稳妥分 / 保范围分）；改权要门槛 = 仅当只争相对缩权的稳妥分差 ≥15 且同类成功案 diff 对得上。换得「不黑箱归并、不永远缩权」。
- **决策 8：模式 C「清单 + 观点↔URL 主表 + 人审闸门」** — 证据等级 A/B/C，C 源不得单独支撑改技能；等待用户「全部采纳 / 采纳 E…… / 全部搁置 / 沉淀到 docs/evolution/」4 选 1。换得不听自媒体就改 prompt。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | patent-disclosure-skill（本项目） | patent-pipeline (ThomasMoreAI) | patent-application-creator (RobThePCGuy) | light-ip-application (Light0305) |
|------|---------|---------|---------|---------|
| 法域 | 中国（CNIPA） | CN/US/EP 全套 | 美国（USPTO） | 中国（含软著） |
| 三类专利分模板 | ✓（schema 物理隔离） | — | — | 弱（专利 + 软著二合一） |
| CNIPA epub 高级查询 | ✓（IPC/LOC 双段式） | — | — | — |
| 中文 OA 答复 | ✓（sqlite-vec + 标签双轨） | — | — | — |
| 通俗解读 / 知识图谱 | ✓（模式 B + Obsidian） | — | — | — |
| 政策嗅探 / 技能自进化 | ✓（模式 C，人审闸门） | — | — | — |
| 多模式互斥工程纪律 | ✓（SKILL.md 硬约定） | — | — | — |
| 申请人签字替代 | ✗（明确不替代） | 半（申请包级） | ✓（美系自主起草） | — |

### 差异化护城河
- **CNIPA 一手接入**：epub 高级查询 + LOC 分类号 + IPC-LOC 自动判断
- **中文 OA 答复**：sqlite-vec RAG + 多厂 embedding + 标签降级
- **三类专利 schema 隔离**：物理文件隔离 + 共享 intake/figure_plan
- **机读 stdout 协议**：LLM ↔ 子进程跨平台稳定契约

这 4 条都是英文/美系开源做不到的层级。**护城河足够深，但足够窄**——只覆盖「中国发明人/工程师自交底」这一条链路。

### 竞争风险
- **最可能被替代**：大型 LLM 平台原生 Agent Skills（Anthropic / 字节）官方发布的中国专利 skill
- **市场风险**：CNIPA 2026-04 政策警示「AI 代写专利多重风险」（技术泄露、AI 幻觉、不实申请）+ 2026-01-01 新版审查指南增加 AI 相关条款，可能让整个市场缩水
- **护城河时间窗**：估计 6–12 个月，skillavatars.com 已开始推英文同类

### 生态定位
中国发明人/工程师的「自我交底 + 自我解读 + 自我应答」一站式工具链；**不是代理人工具链替代品**（明确「模式 D 草稿必复核」「不替代签字」）。填补了「英文 / 美系专利工具不做中文 + CNIPA」和「通用 RAG 框架不会给专利交底做按专利类型分模板 + 查新 + 线稿 + OA 链路」之间的空白。

## 套利机会分析
- **信息差**：低关注度但高质量？**否**——6.7K stars 已经吃到中文+Claude Skill+专利三重红利，不再被低估。
- **技术借鉴**：极高。机读前缀协议 / opt-in 闸门 / 隔离 venv / 双轨降级 RAG / 按件拼装 SVG 这 5 个模式可直接迁移到任何垂类 Agent Skill。
- **生态位**：填补了「中国发明人自交底」这一空白，且主动对齐 CNIPA 2026 合规要求——监管层不会被压垮，反而是护城河。
- **趋势判断**：增长中（4.8 月 6.7K stars 仍未减速）；符合 Agent Skill 协议化大趋势；后发优势在于模式 D（OA 答复）+ 模式 C（政策嗅探）——这两个是英文竞品没碰的差异化方向。

## 风险与不足
- **单作者 bus factor = 1**：35 commit 中 handsomestWei 占 86.7%；外部贡献者仅 4 人各提 1 PR（且都是路过式 bugfix，未进入核心架构）。一旦作者停更，整个 Skill 即孤儿。
- **无 release tag / SemVer**：SKILL.md frontmatter `version: 3.9.0` 自维护，未走 git tag + SemVer 流程；外部依赖版本号做兼容性判断的用户会拿到不稳定信号。
- **CNIPA 反爬稳定性**：项目方在 `cnipa_epub_crawler.py:21-27` 显式承认「不表示规避法律法规……效果因站点升级而变，非保证」。issue #7 open 反映「agent-browser 作为 Step 5 CNIPA 检索的备选后端」的工程焦虑。
- **AI 代写合规边界**：模式 D 草稿必须人工复核后递交 + 模式 C 改 prompt 必须人审 = 主动对齐政策，但 README **缺少对此类合规风险的明确声明**——对外沟通可以更强。
- **测试 commit 比例失衡**：33 个测试文件但 commit message 仅 1 次用 `test:` 前缀。**测试做了但 convention 没标**，不是「没写测试」，但说明 TDD 流程弱。
- **无 lint / formatter / CHANGELOG / release CI**：单 CI 仅 `update-star-history.yml`（每日推 orphan 分支 star-history.svg）。
- **无 refactor commit 历史**：功能堆叠期 + 内部清理待做的扩张期信号。

## 行动建议
- **如果你要用它**：本项目定位是「中国发明人/工程师自交底 + 草稿须复核」，**不适合需要代理人签字替代的场景**。三类专利分模板 + CNIPA 一手查新 + 中文 OA 答复 = 中文垂类天花板。模式 D 默认 opt-in，请勿跳过人工复核。
- **如果你要学它**：重点读 `SKILL.md`（薄路由+互斥）、`prompts/disclosure/prior_art_search.md`（双段式查新+诚实回填）、`tools/oa/{search_cases,store,embed,config}.py`（RAG 双轨降级 + 多厂 embedding）、`tools/shared/{mermaid_render,cad_venv,structure_lineart_compose,math_render}.py`（机读前缀协议 + 隔离 venv + 按件拼装 SVG + 双轨渲染）。这 8 个文件是工程纪律的浓缩。
- **如果你要 fork 它**：可改进方向——（1） 把 `test:` commit convention 强制化（pre-commit hook）；（2） 加 release tag + SemVer CI；（3） 模式 C 的「观点↔URL 主表」可演进为带证据等级的 PR review bot；（4） 把 README 加上「合规声明」段，主动对齐 CNIPA 2026-04 政策；（5） 把模式 D 的「门槛选定」算法提到 SKILL.md 顶部，便于代理人复用。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录 |
| Zread.ai | 未收录 |
| 关联论文 | 无（工程型 Skill，无学术产出） |
| 在线 Demo | 无（Skill 性质决定无托管 demo） |
| SkillHub 镜像 | https://skillhub.cn/skills/patent-disclosure-skill |
| 第三方收录 | [skillavatars.com](https://www.skillavatars.com/articles/patent-disclosure-doc-writer-cd86)、[labgrimoire](https://labgrimoire.com/spellbook/patent-disclosure-skill)、[腾讯云开发者社区](https://cloud.tencent.com/developer/article/2668117) |
| 监管参考 | [CNIPA: AI 代写专利多重风险警示（2026-04）](https://www.cnipa.gov.cn/art/2026/4/3/art_55_205609.html)、[CNIPA: 2025 审查指南修改解读](https://www.cnipa.gov.cn/art/2025/12/4/art_66_202935.html) |
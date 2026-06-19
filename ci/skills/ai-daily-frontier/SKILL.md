---
name: ai-daily-frontier
description: >
  Generate a flagship-grade daily "all-web AI frontier" digest benchmarked
  against MorningAI — covering papers, model & product launches, benchmarks,
  funding/acquisitions, and engineering practice across labs, OSS, and media.
  Fan-out collection (targeted WebFetch + bilingual WebSearch) feeds two-stage
  scoring and adversarial fact verification, then assembles a tiered Chinese
  digest. Use when the user wants the all-web AI news daily ("AI 前沿日报",
  "AI 资讯日报", "daily AI news", "frontier digest"). Sibling skill
  ai-daily-ecosystem covers this project's open-source ecosystem signals.
argument-hint: "[YYYY-MM-DD]"
disable-model-invocation: false
model: opus
metadata:
  author: NightVoyager
  title: AI 前沿日报
  description_zh: |
    对标 MorningAI 的「通用全网 AI 资讯日报」：覆盖论文 / 模型 / 产品 / 融资 /
    benchmark / 工程实践。定向 WebFetch（sources.yaml 源簇）+ 中英双语 WebSearch
    （topics.yaml 主题矩阵）广度扇出采集 → L1/L2/L3 去重 → frontier 5 维两阶段
    评分 → 对抗式事实核验（高分必须 ≥2 独立源、数字必带 source_url、融资双边）→
    主对话套模板分级组装。本项目独有的开源信号层（collect_daily_facts.py）作为
    回链与「开源信号」增强角，外部新闻为主体。
    Orchestrator-Worker：facts 采集 → 并行采集/评分/核验 SubAgent → 主对话组装。
  dependencies:
    - python3
    - jq
  version: 1.0.0
  license: MIT
---

# AI 日报 · 前沿资讯篇（ai-daily-frontier）

产出「今天全网 AI 圈发生了什么」的中文日报，**旗舰版质量、对标 MorningAI**：论文前沿、
模型与产品发布、benchmark 排行、融资收购、工程实践一网打尽。**差异化护城河**：在通用
新闻聚合之上，叠加本项目独有的开源信号层（Trending 时序 + 大牛 star + 380+ 篇深度报告）
做回链与「开源信号」增强角；并以**对抗式事实核验**杜绝 AI 幻觉 / slop。

**输入：** `$ARGUMENTS`（可选日期 `YYYY-MM-DD`，缺省今天 UTC）。

## When to Use

- 用户要「AI 前沿日报 / AI 资讯日报 / daily AI news / frontier digest」
- 每日 CI 自动产出全网 AI 资讯日报

**Don't use for:**
- 本项目开源生态信号（Trending / 大牛 star / 站内报告回链为主体）→ 用姊妹 skill
  `ai-daily-ecosystem`
- 单仓库深度分析 → 用 `repo-miner`

## 架构说明（Orchestrator-Worker，五阶段编排）

```
/ai-daily-frontier [date]（主对话 = 编排者）
│
├─ Phase 0 准备（主对话，确定性，零 LLM）
│    ├─ python3 src/scripts/collect_daily_facts.py <date> --type frontier  → facts JSON 路径
│    │      （内部开源信号层 + after_date 时效起点 + report_url_index 回链表）
│    └─ python3 src/scripts/dedup_daily.py prune --type frontier
│
├─ Phase 1 采集矩阵（并行 SubAgent，≤10 并发硬顶；超配分波）
│    ├─ 定向 WebFetch 组：按 sources.yaml 的 clusters（papers/models-oss/labs-blog/benchmarks/cn-media）
│    └─ WebSearch 组：按 topics.yaml 5 主题 × 中英双语，query 末尾追加 after:<after_date>
│         每个 SubAgent 返回符合 item-schema.json 的 JSON 写 tmp，只回路径+条数+ok/failed
│
├─ Phase 2 去重（主对话 + 脚本）
│    ├─ dedup_daily.py filter（L1 URL 归一 + cache 命中剔除）
│    └─ LLM L2 标题 / L3 内容语义去重 + 跨「内部信号 ↔ 外部新闻」合并
│
├─ Phase 3 评分 + 对抗核验（并行 SubAgent）
│    ├─ 两阶段评分：元数据初筛 → frontier 5 维定性打分（scoring.yaml）
│    └─ 评分 ≥ verify_floor 的条目派「验证 SubAgent」找反证，≥2 独立源；不达标封顶 5.9 或丢弃
│
├─ Phase 4 组装（主对话）：套 reference/template.md 写日报
│
└─ Phase 5 自检 + 收尾（主对话）：checklist 自检 → dedup commit → record_daily → 发布交接
```

**为什么这样做**：采集 / 评分 / 核验各自产生大量中间数据（抓取正文、搜索结果、反证检索），
全部留在 SubAgent 的隔离 context；主对话只累积结构化条目数组（路径 + 摘要），context 保持
干净。采集与核验天然可并行，扇出能在固定 token 预算内拉满广度与可信度。

## 前置检查

```bash
which python3 && which jq && echo "tools ready"
```

---

## Phase 0：准备（主对话内执行，确定性）

从 `$ARGUMENTS` 解析日期 `DATE`（缺省今天 UTC）。运行确定性采集，拿到内部信号层与时效起点：

```bash
FACTS=$(python3 src/scripts/collect_daily_facts.py "$DATE" --type frontier)
python3 src/scripts/dedup_daily.py prune --type frontier
```

`collect_daily_facts.py --type frontier` 只把 **facts JSON 路径** 打印到 stdout（大数据落 tmp，
context 干净）。`Read` 这个 JSON，关注三件事（字段全集见
`${CLAUDE_SKILL_DIR}/reference/collection-matrix.md`）：

- `after_date` —— **外部采集的时效起点**（= 上次同类日报日期）。Phase 1 所有 WebSearch query
  末尾追加 `after:<after_date>`，只取这之后的增量。
- `rising_repos` / `pro_stars` / `heating_up` —— **内部开源信号层**，篇B 用作「🌱 开源信号」
  增强角（不作为主体），以及外部新闻命中同仓库时的徽标。
- `report_url_index_path` —— reports.json 的 `originalUrl → slug` 全表落地路径。外部条目带
  `repo_url` 时据此反查是否命中本站已有报告，命中则回链 `/reports/{slug}/`。

篇B 的主体是 **Phase 1 外部采集**；内部信号层只增强、只回链，**绝不**因 facts 为空而中断。

---

## Phase 1：采集矩阵（并行 SubAgent，≤10 并发硬顶）

目标：在固定预算内把全网 AI 增量「广度扇出」抓回来。两类源互补：

- **定向 WebFetch 组**：按 `src/data/ai-daily/sources.yaml` 的 5 个 cluster
  （`papers` / `models-oss` / `labs-blog` / `benchmarks` / `cn-media`）抓固定页面。可控、噪声低、
  **CI 后端无 WebSearch 时也能用**（见「异常处理」）。
- **WebSearch 组**：按 `src/data/ai-daily/topics.yaml` 的 5 个 theme
  （`papers` / `oss` / `models-bench` / `engineering` / `industry`）做**中英双语**搜索，
  query 末尾统一追加 `after:<after_date>`。

**并发与分波（硬顶来自 `scoring.yaml > concurrency_cap = 10`）**：
5 个 WebFetch cluster + 5 个 WebSearch theme × 中英 = 13 路广度。把它压进 ≤10 个 Agent slot：
**每个 WebSearch SubAgent 内部跑中英双查**（5 个 slot 覆盖 10 路搜索），WebFetch 5 个 cluster
各 1 slot —— 合计 10 slot 正好打满硬顶。若再要超配，**分波执行**（先发 10 个，回收后再发剩余），
不要一次发起超过 `concurrency_cap` 个 Agent。

**关键：同一波内的多个 Agent 调用必须在同一响应中同时发起，不要串行等待。**

每个采集 SubAgent 的 prompt 用 `${CLAUDE_SKILL_DIR}/reference/collection-matrix.md` 的
**统一模板**（WebFetch 版 / WebSearch 版各一），注入：角色 + 主题 + 时效约束（`after:<after_date>`）
+ 该 slot 负责的源清单（从 sources.yaml / topics.yaml / entities.yaml 取）+ 采集铁律。每个
SubAgent 把抽取条目按 `src/data/ai-daily/item-schema.json` 写成 JSON 数组落 tmp，
**只回主对话：tmp 路径 + 条数 + ok/failed**。

**容错**：单个 WebFetch URL 失败 → 回退 `https://r.jina.ai/<url>`（沿用 repo-miner 异常处理）。
**统计每波失败率，过半（>50%）SubAgent failed 则终止**——数据不足不强出报告（见「异常处理」的
降级路径）。

---

## Phase 2：去重（主对话 + 脚本）

把各 SubAgent 回来的 tmp JSON 合并成候选池，三层去重 + 跨集合合并，规则全文请 Read
`src/data/ai-daily/dedup-rules.md`：

1. **L1 — URL 精确去重（确定性脚本）**：归一 URL + 剔除近 30 天 cache 命中。

   ```bash
   python3 src/scripts/dedup_daily.py filter --type frontier --in tmp/<candidates>.json --out tmp/<filtered>.json
   ```

2. **L2 — 标题语义去重（LLM）**：同一事件被多家转载/换标题/翻译 → 按归一标题聚类，每组留一条。
3. **L3 — 内容语义去重（LLM）**：不同措辞描述同一发布（arxiv 原文 vs 媒体解读 vs 公众号翻译）
   → 按摘要/要点语义合并。
4. **跨「内部开源信号 ↔ 外部新闻」合并**：若内部 `rising_repos`/`pro_stars` 的仓库与某条外部
   「发布/release」新闻指向同一仓库 → **合并为一条，外部新闻为主体**，内部信号作徽标挂上
   （「本站 Trending #N / 被 M 位大牛 Star」）；外部无对应新闻时，内部信号单独进「🌱 开源信号」。

保留优先级（同组重复留哪条）见 dedup-rules.md：论文 arXiv 原文 > 解读；开源 GitHub 仓库 > 博文；
新闻官方公告 > 转载；同级时 评分高 > 独立源多 > `event_date` 早。

---

## Phase 3：评分 + 对抗式事实核验（并行 SubAgent）

评分为**两阶段**（rubric 全文请 Read `src/data/ai-daily/scoring-rubric.md`，参数在 `scoring.yaml`）：

- **阶段 A — 确定性元数据初筛**：据已知元数据先过一遍（源权威度、是否带可验证 metrics、是否命中
  `entities.yaml`、`event_date` 是否在 `after_date` 之后），明显噪声直接丢弃，不送 LLM 省 token。
- **阶段 B — frontier 5 维定性打分**：按 `scoring.yaml > profiles.frontier` 的 5 维加权打分
  （`impact 30` / `differentiation 25` / `depth_verifiability 20` / `relevance_coverage 15` /
  `timeliness 10`，加总 ÷10 得 0-10）。分级阈值见 `scoring.yaml > tiers`：
  **必看 ≥8.0 / 关注 6.0–7.9 / 简讯 4.0–5.9 / <4.0 丢弃**。

**对抗式事实核验**（旗舰版核心，铁律全文请 Read `src/data/ai-daily/verification-rules.md`，参数
`scoring.yaml > verify`）：

- 评分 **≥ `verify.verify_floor`（7.0）** 的条目，派并行「验证 SubAgent」**默认假设为假、去找反证**，
  须找到 **≥ `verify.min_independent_sources`（2）个独立信源**（不得来自同一媒体集团/同一转载链）
  交叉确认。通过 → 保留评分；不通过 → **封顶 5.9（降级简讯）或丢弃**。
- **禁止凭记忆 / 外推数字**：`metrics[].value` 的每个数字必须能回指 `source_url`；条目自检字段
  `numbers_from_source=false` 的数字一律剔除，拿不准宁可不写。
- **事件日期核实**：`event_date` 必须是真实事件发生日期（≠页面/抓取日期），核实失败不计时效分
  并标注「日期未核实」。
- **融资 / 收购双边确认**（`verify.funding_needs_both_sides=true`）：需投资方与被投/被收购方
  双边官方口径都确认，仅单边宣称则降级或标注「待确认」。

**并发同样受 `concurrency_cap=10` 约束**：评分 SubAgent 与验证 SubAgent 分批发起，每批 ≤10 个，
同批在同一响应内并行。

---

## 标题创作规则（H1 = 公众号文章标题，必读）

H1 会被下游公众号发布流程**直接当文章标题**，**严禁** `# YYYY-MM-DD AI 前沿日报` 这类无点击力
的模板。准则（同姊妹 skill）：

1. 长度 ≤ 32 字。
2. 至少含 2 个钩子要素：具体数据（某模型刷新 N 项 SOTA / 某公司 X 亿融资 / benchmark 第 N）、
   当日最大看点（某发布/某论文/某事件）、读者真实关心的问题、反差钩子。
3. 格式建议：`AI 前沿日报 06.07：<当日最大看点钩子>`。
4. 避免：感叹号、emoji、营销词（震惊/必看/绝了/炸裂/王炸）、全角符号堆砌。

范例：`AI 前沿日报 06.07：开源模型首次在 LMArena 进前三，与一篇把推理成本砍半的新论文`

---

## Phase 4：组装（主对话内执行）

按 `${CLAUDE_SKILL_DIR}/reference/template.md` 的板块模板组装日报。板块顺序：

**今日提要 TL;DR → 🔥 今日必看(≥8) → 👀 值得关注(6–7.9) → 📌 简讯(4–5.9) → 🌱 开源信号 →
🔧 方法与来源**。

组装原则：
- 三个分级板块内的条目**按 `category` 分组呈现**（论文前沿 / 开源项目 / 模型与评测 /
  工程实践 / 行业与融资）。
- 每条卡片字段：**中文标题（原标题）| 分级+评分 | summary_zh | 要点 | method_zh | metrics
  （每个数字带 source_url）| repo_url/paper_url | 来源（≥2 链接）| 分类标签 | 命中本站报告则回链
  `/reports/{slug}/`**。
- 「🌱 开源信号」来自 Phase 0 内部 facts 的 `rising_repos` / `pro_stars` 增强角；命中本站报告
  （`report_slug` 非空）则回链 `/reports/{slug}/`。
- 「🔧 方法与来源」披露：采集源数 / 去重命中数 / 核验通过率 / 非种子源占比
  （≥ `scoring.yaml > min_non_seed_ratio = 0.2`）。
- 中文直角引号「」；不编造任何源外数字。
- **有几条出几条，不为凑数降阈值**。全部 <4.0（0 条达标）时，输出「今日无重大 AI 资讯」并正常收尾。

---

## Phase 5：自检与收尾（主对话内执行）

完成后对照 `${CLAUDE_SKILL_DIR}/reference/checklist.md` 逐项自检（完整性 / 事实核验 / 去重 /
回链 / 规范 / 收尾），任一不满足则修正。

### 产出两个文件

1. **`src/ai_news/<date>.md`** —— 带 YAML frontmatter（`title`/`date`/`summary`/`tags`/
   `canonical_url`/`syndicate: true`）+ H1 + 正文。模板见 reference/template.md。
   **注意：篇B 落在 `src/ai_news/`，不进站点**（无站点详情页），故 `canonical_url` 指向站点首页
   `https://seeyeetech.com/github-explorer/`（footer 仍会加公众号导流）。H1 同 frontmatter.title。
2. **`src/ai_news/<date>.meta.json`** —— `{title(≤64), digest(≤120), author: "NightVoyager", theme}`，
   `theme` 从 `stars / universe / ocean / desert / forest / green-trees / dark` 任挑组合。

### 收尾：去重 cache + 记录索引

```bash
# 把今日采纳条目 URL 写入 cache（次日去重），格式 [{"url": "...", "event_date": "<date>"}]
python3 src/scripts/dedup_daily.py commit --type frontier --in tmp/<adopted>.json --date "$DATE"
# 记录索引（站点只渲染 ecosystem，frontier 仅入 jsonl 供 since 窗口/去重）；CI 会带 --ci-run-id
python3 src/scripts/record_daily.py --type frontier --date "$DATE" --slug "$DATE" \
  --title "<H1>" --summary "<一句话提要>" \
  --sections '{"must_read":N,"watch":N,"brief":N,"oss_signal":N}' \
  --featured-urls "<头条条目 url 逗号分隔>"
```

**发布交接**：日报对发布管线就是一篇普通文章，**无需新 adapter**——
`python3 scripts/syndicate_publish.py src/ai_news/<date>.md --channel wechat --dry-run`
（CI 由 daily-digest.yml 统一驱动，初期 `skip_publish=true`）。

---

## 异常处理

- **CI 后端（Minimax 兼容端点）可能不支持 server-side WebSearch** → 篇B 主体依赖外部采集，
  这是预期风险。降级顺序：
  1. **WebSearch 不可用** → Phase 1 优先用 **WebFetch 抓 `sources.yaml` 的固定源兜底**
     （定向源不依赖搜索能力）。
  2. **WebFetch 也大面积失败 / 仍无外部增量** → 在「🔧 方法与来源」标注「今日无外部增量」，
     可仅靠 Phase 0 内部信号层降级出一篇**以开源信号为主**的简版；**甚至该日不出 frontier 篇**
     （输出「今日无重大 AI 资讯」收尾），**绝不让 CI job 失败**。
  3. 要富采集（本地）→ `FORCE_BACKEND=anthropic`，走原生 WebSearch/WebFetch。
- 单个 WebFetch URL 失败 → 回退 `https://r.jina.ai/<url>`；仍失败则记 failed、不阻塞整波。
- 采集**过半 SubAgent failed** → 数据不足，按上面降级路径处理，不强凑、不报错。
- `collect_daily_facts.py` 报缺数据源 → 看 facts 的 `_warnings`；内部信号层为空不影响外部采集主体。
- 同一日期重复运行：`record_daily.py` 幂等跳过；md 直接覆盖即可。

## 补充资源

- 采集矩阵（源分配 + SubAgent prompt 模板 + 输出 schema + 时效/容错）：
  [reference/collection-matrix.md](reference/collection-matrix.md)
- 日报模板与 frontmatter / meta.json / canonical 约定：[reference/template.md](reference/template.md)
- 终稿自检清单（含事实核验项）：[reference/checklist.md](reference/checklist.md)
- 实体白名单：`src/data/ai-daily/entities.yaml`
- 定向 WebFetch 源簇：`src/data/ai-daily/sources.yaml`
- WebSearch 主题矩阵：`src/data/ai-daily/topics.yaml`
- 评分参数 / rubric：`src/data/ai-daily/scoring.yaml`、`src/data/ai-daily/scoring-rubric.md`
- 去重规则：`src/data/ai-daily/dedup-rules.md`
- 事实核验铁律：`src/data/ai-daily/verification-rules.md`
- 条目返回结构（权威）：`src/data/ai-daily/item-schema.json`

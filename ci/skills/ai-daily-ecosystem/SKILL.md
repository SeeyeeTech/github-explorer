---
name: ai-daily-ecosystem
description: >
  Generate a daily "open-source AI ecosystem" digest centered on this project's
  own unique data — today's GitHub Trending, what whitelisted AI leaders are
  starring, cross-window heating repos — with deep links back to 380+ existing
  analyses. Use when the user wants the open-source AI daily ("开源 AI 日报",
  "生成今日开源日报", "ecosystem digest"). Sibling skill ai-daily-frontier covers
  general all-web AI news.
argument-hint: "[YYYY-MM-DD]"
disable-model-invocation: false
model: opus
metadata:
  author: NightVoyager
  title: 开源 AI 日报
  description_zh: |
    以本项目独有数据为核心的「开源 AI 日报」：复用 trending（每日榜时序）+ starred
    （大牛 star 快照）+ 380+ 篇深度报告，确定性脚本一次性聚合「开源信号层」，主对话
    据此分级组装日报并深度回链已有分析。外部开源动态为 best-effort 补充。
    Orchestrator-Worker：collect_daily_facts.py 采集 → 可选 SubAgent 增强 → 主对话组装。
  dependencies:
    - python3
    - jq
  optional-dependencies:
    - gh
  version: 1.0.0
  license: MIT
---

# AI 日报 · 开源生态篇（ai-daily-ecosystem）

产出「今天开源 AI 圈发生了什么」的中文日报。**差异化护城河**：本项目独有的每日
Trending 时序 + AI 大牛 star 快照 + 380+ 篇深度报告——把它做成「开源信号层 + 全报告
回链」，这是任何通用 AI 新闻聚合器都没有的。

**输入：** `$ARGUMENTS`（可选日期 `YYYY-MM-DD`，缺省今天 UTC）。

## When to Use

- 用户要「开源 AI 日报 / 今日开源日报 / ecosystem digest」
- 每日 CI 自动产出开源生态日报

**Don't use for:**
- 通用全网 AI 资讯（论文/模型/产品/融资）→ 用姊妹 skill `ai-daily-frontier`
- 单仓库深度分析 → 用 `repo-miner`

## 架构说明（Orchestrator-Worker，确定性核心）

```
/ai-daily-ecosystem [date]（主对话 = 编排者）
│
├─ Phase 0 准备（主对话，确定性，零 LLM）
│    ├─ python3 src/scripts/collect_daily_facts.py <date> --type ecosystem  → facts JSON 路径
│    └─ python3 src/scripts/dedup_daily.py prune --type ecosystem
│
├─ Phase 1 增强（可选并行 SubAgent，best-effort，可降级跳过）
│    └─ 为 Top 开源新星/大牛在看仓库补「一句话亮点」；可选 1 个 Agent 采外部开源动态
│
├─ Phase 2 分级（主对话）：按 ecosystem 评分 profile 给 rising/pro_stars/heating 排序分档
│
└─ Phase 3 组装（主对话）：套模板写日报 → 自检 → 产出 md + meta.json → 去重 cache commit
```

**为什么这样做**：开源信号层 100% 由 `collect_daily_facts.py` 确定性产出（零联网、零幻觉、
不受限流），即使外部增强全失败，日报仍有完整价值——这正是 CI 后端可能无 WebSearch 时的
兜底（详见「异常处理」）。

## 前置检查

```bash
which python3 && which jq && echo "tools ready"
```

---

## Phase 0：准备（主对话内执行）

从 `$ARGUMENTS` 解析日期 `DATE`（缺省今天 UTC）。运行确定性采集：

```bash
FACTS=$(python3 src/scripts/collect_daily_facts.py "$DATE" --type ecosystem)
python3 src/scripts/dedup_daily.py prune --type ecosystem
```

`collect_daily_facts.py` 只把 **facts JSON 路径** 打印到 stdout（大数据落 tmp，context 干净）。
`Read` 这个 JSON，了解其结构（完整字段见 `${CLAUDE_SKILL_DIR}/reference/collection.md`）：
`rising_repos`（今日 Trending daily，含 `ai`/`rank_delta`/`report_slug`）、`pro_stars`（大牛新
star，含 `star_users`/`starred_by`）、`heating_up`（跨窗口升温）、`resurface`（旧文重读）、
`stats`、`cache_seen_keys`。

**若 `stats.rising_ai == 0 且 pro_stars == 0`**：今日无开源信号，输出
「今日开源生态无显著动态」并正常收尾，不强凑。

---

## Phase 1：增强（可选，并行 SubAgent，best-effort）

目的：把确定性信号变成有可读性的日报条目。**全部可降级**——任一 SubAgent 失败/不可用，
用 facts 里已有的 `description` 兜底，不让流程失败。

**关键：多个 Agent 调用在同一响应中同时发起。** 建议最多 2 个（受 `config.concurrency_cap`）：

- **Agent A — 仓库亮点增强**：传入 Top 开源新星 + 大牛在看（合并去重后 ≤12 个）的
  `name`/`url`/`description`。要求对每个仓库用 WebFetch 读 README 首屏，产出一句话「它解决
  什么/为何值得看」（≤40 字，禁营销词），以及 1 个分类标签。失败的条目返回原 description。
- **Agent B（可选）— 外部开源动态**：用 WebSearch 找「今日/本周新发布的开源 AI 项目/框架」
  补 3-5 条 facts 之外的条目，每条须带源链接。CI 无 WebSearch 时本 Agent 会空手而归，跳过即可。

SubAgent 返回结构化 JSON（写 tmp，只回主对话路径 + 条数 + ok/failed）。统计失败率，
**> 50% 失败则放弃增强**，直接用确定性 facts 走 Phase 2。

---

## Phase 2：分级（主对话）

按 `src/data/ai-daily/scoring.yaml` 的 `profiles.ecosystem` 维度（ecosystem_relevance /
momentum / pro_star_signal / practicality / timeliness）给条目排序分档。开源信号的分数可由
元数据确定性估算：`momentum` 看 `trending_days`/`rank_delta`/stars；`pro_star_signal` 看
`star_users`。分档阈值见 `scoring.yaml > tiers`。评分 rubric 全文请 Read 仓库内
`src/data/ai-daily/scoring-rubric.md`。

**去重**：对 Phase 1 外部条目与开源信号跨集合合并（同仓库只留一条，外部新闻为主体、内部
信号作徽标），规则请 Read `src/data/ai-daily/dedup-rules.md`。可借助：

```bash
python3 src/scripts/dedup_daily.py filter --type ecosystem --in tmp/<candidates>.json --out tmp/<filtered>.json
```

---

## 标题创作规则（H1 = 公众号文章标题，必读）

H1 会被下游公众号发布流程**直接当文章标题**，**严禁** `# YYYY-MM-DD 开源 AI 日报` 这类无
点击力的模板。准则：

1. 长度 ≤ 32 字
2. 至少含 2 个要素：具体数据（今日 N 个新星 / 被 M 位大牛同时 star / X 天上榜）、当日最大
   看点（某新项目/某方向）、读者关心的问题、反差钩子
3. 格式建议：`开源 AI 日报 06.07：<当日最大看点钩子>`
4. 避免：感叹号、emoji、营销词（震惊/必看/绝了/炸裂）

范例：`开源 AI 日报 06.07：3 位大牛同夜 star 的 Agent 框架，与 Trending 屠榜的本地推理新秀`

---

## Phase 3：组装、自检与产出（主对话）

按 `${CLAUDE_SKILL_DIR}/reference/template.md` 的板块模板组装日报（六大板块：今日导读 /
开源新星 / 大牛在看 / 升温追踪 / 旧文重读 / 方法与来源）。组装原则：

- 每个含 `report_slug` 的条目**必须**回链 `/reports/{slug}`（深度报告，这是核心导流位）。
- 「开源新星」优先未分析过的 AI 仓库（`ai=true 且 report_slug=null`）；已分析的挂回链。
- 「大牛在看」优先 `star_users ≥ 2`（多位大牛同时 star）；展示 `starred_by`。
- 中文直角引号「」；不编造 facts 之外的数字。

完成后对照 `${CLAUDE_SKILL_DIR}/reference/checklist.md` 逐项自检。

### 产出两个文件

1. **`src/daily_report/<date>.md`** —— 带 YAML frontmatter（`title`/`date`/`summary`/`tags`/
   `canonical_url: <base>/daily/<date>/`/`syndicate: true`）+ H1 + 正文。模板见 reference/template.md。
2. **`src/daily_report/<date>.meta.json`** —— `{title, digest(≤120字), author, theme}`，供
   `wechat_publish.py` 发布复用（结构同 md2wechat 产物）。

### 收尾：去重 cache + 记录索引

```bash
# 把今日采纳的仓库/条目 URL 写入 cache（次日去重），格式 [{"url": "...", "event_date": "<date>"}]
python3 src/scripts/dedup_daily.py commit --type ecosystem --in tmp/<adopted>.json --date "$DATE"
# 记录索引（站点读取 + 选 since 窗口）；CI 会带 --ci-run-id
python3 src/scripts/record_daily.py --type ecosystem --date "$DATE" --slug "$DATE" \
  --title "<H1>" --summary "<一句话提要>" \
  --sections '{"rising":N,"pro_stars":N,"heating":N,"resurface":N}' \
  --featured-urls "<头条仓库 url 逗号分隔>"
```

发布交接：日报对发布管线就是一篇普通文章，**无需新 adapter**——
`python3 scripts/syndicate_publish.py src/daily_report/<date>.md --channel wechat --dry-run`
（CI 由 daily-digest.yml 统一驱动，初期 `skip_publish=true`）。

---

## 异常处理

- `collect_daily_facts.py` 报缺数据源 → 看 facts 的 `_warnings`；若 rising/pro_stars 皆空，
  输出「今日无显著动态」收尾，不报错。
- **CI 后端（Minimax 兼容端点）可能不支持 server-side WebSearch** → Phase 1 增强会失败，
  这是预期内的：直接用确定性 facts 组装日报（仍完整）。要富增强本地用 `FORCE_BACKEND=anthropic`。
- WebFetch 失败 → 回退 `https://r.jina.ai/<url>`；仍失败则用 facts 的 description。
- 同一日期重复运行：`record_daily.py` 幂等跳过；md 直接覆盖即可。

## 补充资源

- 采集与 facts 字段：[reference/collection.md](reference/collection.md)
- 日报模板与 frontmatter：[reference/template.md](reference/template.md)
- 终稿自检清单：[reference/checklist.md](reference/checklist.md)
- 评分 rubric：`src/data/ai-daily/scoring-rubric.md`
- 去重规则：`src/data/ai-daily/dedup-rules.md`

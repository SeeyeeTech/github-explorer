# Phase 1 采集矩阵（前沿资讯篇）

本文件定义篇B 的扇出采集：源如何分配到 SubAgent、统一的 prompt 模板、返回结构、并发与容错。

## 0. 时效起点与返回结构

- **时效起点 `after_date`**：来自 Phase 0 `collect_daily_facts.py --type frontier` 产出的 facts
  JSON（= 上次同类日报日期）。所有 WebSearch query 末尾追加 `after:<after_date>`，只取增量。
- **返回结构（权威）**：每个 SubAgent 把抽取条目写成**符合 `src/data/ai-daily/item-schema.json`
  的 JSON 数组**落 tmp，**只回主对话：tmp 路径 + 条数 + ok/failed**。必填字段
  `title_zh / url / source_type / summary_zh`；数字进 `metrics[]`（每个带 `source_url`）；
  `event_date` 填真实事件日期；自检字段 `numbers_from_source` 如实标注。

## 1. 源分配表

### WebFetch 组 ↔ Agent（按 `src/data/ai-daily/sources.yaml` 的 clusters）

| Agent slot | cluster | 源（sources.yaml 维护） | 侧重 category |
|---|---|---|---|
| WF-1 | `papers` | arxiv cs.AI/cs.CL/cs.LG recent、HuggingFace Papers、Papers With Code | 论文前沿 |
| WF-2 | `models-oss` | HuggingFace trending models、GitHub Trending（daily / python） | 开源项目 / 模型 |
| WF-3 | `labs-blog` | OpenAI / Anthropic / DeepMind / Meta / Mistral / Qwen 官方博客 | 模型与产品 / 行业 |
| WF-4 | `benchmarks` | LMArena、Artificial Analysis、Open LLM Leaderboard | 模型与评测 |
| WF-5 | `cn-media` | 机器之心、量子位、36Kr AI 频道 | 行业与融资（中文） |

每个 cluster 内每源取 Top `sources.yaml > per_source_top_n`（默认 5）。可结合
`entities.yaml > entities`（labs / model-infra / coding-agents / vision-media / benchmarks / kol）
的 `blog` 字段补抓实体官方动态。

### WebSearch 组 ↔ Agent（按 `src/data/ai-daily/topics.yaml` 的 themes，中英双查）

| Agent slot | theme | label | 双语查 |
|---|---|---|---|
| WS-1 | `papers` | 论文前沿 | zh + en（topics.yaml `themes[].queries.{zh,en}`） |
| WS-2 | `oss` | 开源项目 | zh + en |
| WS-3 | `models-bench` | 模型与评测 | zh + en |
| WS-4 | `engineering` | 工程实践 | zh + en |
| WS-5 | `industry` | 行业与融资 | zh + en |

**每个 WS Agent 内部跑「中查 + 英查」两次**，query 末尾各追加 `after:<after_date>`，每条 query
取 Top `topics.yaml > per_query_top_n`（默认 5）。

## 2. 并发与分波

- **硬顶 = `scoring.yaml > concurrency_cap`（10）**。一次响应内发起的 Agent 数不得超过它。
- 13 路广度（5 WebFetch cluster + 5 theme × 中英 = 10 路搜索 + 5 抓取）压进 10 slot：
  **5 个 WF slot（各 1 cluster）+ 5 个 WS slot（各 1 theme，内部中英双查）= 10 slot 打满硬顶**。
- 若临时扩容更多源 → **分波**：先发 10 个，全部回收后再发下一波，**绝不一次超过 10 个**。
- **同一波内的多个 Agent 调用必须在同一响应中同时发起**（并行）。

## 3. 容错与终止

- 单个 WebFetch URL 失败 → 回退 `sources.yaml > fetch_fallback` + 原 url（即
  `https://r.jina.ai/<url>`）。仍失败则该源记 failed，不阻塞同 Agent 其他源。
- **统计每波失败率：过半（>50%）SubAgent 返回 failed → 终止采集**，按 SKILL.md「异常处理」
  降级（WebFetch 兜底 → 简版 → 必要时不出 frontier 篇），不强凑、不让 job 失败。
- CI 后端无 server-side WebSearch 时，WS 组会空手而归——优先靠 WF 组（定向源不依赖搜索）兜底。

## 4. 统一 SubAgent prompt 模板

两版仅「源获取方式」不同，**角色 / 时效约束 / 采集铁律 / 返回约定完全一致**。注入变量：
`<after_date>`（Phase 0 facts）、`<源清单>`（从 sources.yaml / topics.yaml / entities.yaml 取）、
`<tmp 路径>`（主对话指定的落地文件）。

### 采集铁律（两版共用，原样写进 prompt）

```
1. 数字只抄一手源：metrics 里每个数值/性能指标必须能回指 source_url；禁止凭记忆、估算、外推。
   找不到源的数字一律不写，并把 numbers_from_source 标 false。
2. 事件日期核实：event_date 填「真实事件发生日期」，不是页面/抓取日期；核实不了就置 null。
3. 时效约束：只收 after:<after_date> 之后的增量；更早的旧闻丢弃。
4. 留痕：关键论断在 evidence_quotes 里附原文片段；secondary_sources 填独立佐证源 URL。
5. 反 slop：summary_zh 讲清「是什么 / 为何重要 / 对读者意味着什么」，不堆营销词。
6. 命中 entities.yaml 的实体写进 entities[]；按 category 归类（论文前沿|开源项目|模型与评测|
   工程实践|行业与融资）。
7. 返回符合 src/data/ai-daily/item-schema.json 的 JSON 数组，写到 <tmp 路径>；
   只把「tmp 路径 + 条数 + ok/failed」回给主对话，不要把条目正文回灌主对话。
```

### WebFetch 版

```
你是 AI 资讯采集员，负责 cluster「<cluster 名，如 papers>」。
用 WebFetch 抓取以下固定源（每源取 Top <per_source_top_n> 条近 <after_date> 之后的 AI 条目）：
<逐行列出该 cluster 在 sources.yaml 的 URL；可补 entities.yaml 对应实体的 blog>

抓取要点：
- 单个 URL 抓取失败 → 改用 https://r.jina.ai/<原url> 重试一次；仍失败则跳过该源记 failed。
- 对每条目进入原文确认 event_date 与 metrics 数字（不要只看列表页标题）。

【采集铁律】见上方 7 条，逐条遵守。
把结果按 item-schema.json 写到 <tmp 路径>，只回「路径 + 条数 + ok/failed」。
```

### WebSearch 版

```
你是 AI 资讯采集员，负责 theme「<theme label，如 模型与评测>」。
用 WebSearch 做中英双查（两次搜索），query 取自 topics.yaml 的 themes[<theme>].queries：
- 中文：<queries.zh> after:<after_date>
- 英文：<queries.en> after:<after_date>
每条 query 取 Top <per_query_top_n> 条结果，对命中结果用 WebFetch 进原文核实
（确认 event_date、metrics 数字、是否一手源）。

注意：若运行环境不支持 WebSearch（CI Minimax 后端），直接返回 failed + 空数组，不要编造结果。

【采集铁律】见上方 7 条，逐条遵守。
把结果按 item-schema.json 写到 <tmp 路径>，只回「路径 + 条数 + ok/failed」。
```

## 5. 引用

- 定向源簇：`src/data/ai-daily/sources.yaml`
- 主题矩阵：`src/data/ai-daily/topics.yaml`
- 实体白名单：`src/data/ai-daily/entities.yaml`
- 返回结构（权威）：`src/data/ai-daily/item-schema.json`
- 并发硬顶 / 非种子源占比：`src/data/ai-daily/scoring.yaml`

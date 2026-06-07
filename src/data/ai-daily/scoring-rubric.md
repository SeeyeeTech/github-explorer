# 评分 rubric（两篇 skill 共引）

评分参数（权重、阈值、核验项）集中在 `src/data/ai-daily/scoring.yaml`，本文件是其语义说明。
评分为**两阶段**：先确定性元数据初筛（省 token、滤明显噪声），再 Agent 定性打分。

## 阶段 A — 确定性元数据初筛

由脚本或主对话据已知元数据先过一遍，明显不合格直接丢弃，不送 LLM 评分：

- 源权威度：命中 `entities.yaml` 实体官方源 / 一手源（arxiv 原文、官方博客、GitHub 仓库）加权；纯转载自媒体降权。
- 是否带可验证 `metrics`（SOTA/性能数据且每个数字有 source_url）。
- 是否命中 `entities.yaml`（labs / coding-agents / benchmarks…）。
- 时效：`event_date` 是否落在采集窗口内（`after_date` 之后）。

## 阶段 B — Agent 定性打分（0-10）

按条目所属 profile（`scoring.yaml > profiles.{ecosystem|frontier}`）的维度加权打分，
各维度按权重百分比给分，加总后 ÷10 得 0-10。分值锚点（对齐 MorningAI）：

| 分段 | 含义 |
|---|---|
| 9-10 | 重大事件：范式级突破 / 行业格局变化 |
| 7-8  | 重要更新：值得从业者立刻了解 |
| 5-6  | 常规更新：有价值但非必读 |
| 3-4  | 次要：增量小改 / 小范围影响 |
| 1-2  | 琐碎：营销/重复/无实质增量 |

### 篇A `ecosystem` 维度释义
- **ecosystem_relevance(30)**：与开源 AI 生态、与本站读者（关注开源项目的开发者）的相关度。
- **momentum(25)**：`trending_days` + 排名跃升幅度 + star 增速；跨窗口持续上榜加分。
- **pro_star_signal(20)**：被多少位白名单大牛 Star（`star_users`）；多人同时 star 是强信号。
- **practicality(15)**：可上手/可复用（有清晰 README、可跑 demo、可复现）。
- **timeliness(10)**：新进榜 / 新 star / 新发布。

### 篇B `frontier` 维度释义（对标 MorningAI 5 维）
- **impact(30)**：行业影响面——影响多少人/组织/生态，从格局突破到例行更新。
- **differentiation(25)**：行业首创/独特 vs 跟随/增量复刻。
- **depth_verifiability(20)**：技术深度且可验证——有 method + metrics + 可复现 repo。
- **relevance_coverage(15)**：对中文 AI 从业者的相关度与覆盖广度。
- **timeliness(10)**：真实事件新近度（按 `event_date`，非页面日期）。

## 分级

按 `scoring.yaml > tiers`：必看 ≥8.0 / 关注 6.0–7.9 / 简讯 4.0–5.9 / <4.0 丢弃。

**铁律**：有几条合格就输出几条，**绝不为凑数降低阈值**；全部 <4.0 时输出「今日无重大 AI 资讯」并正常收尾。

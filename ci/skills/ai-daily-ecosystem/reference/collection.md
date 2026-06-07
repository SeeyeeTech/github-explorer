# Phase 0 采集与 facts 字段说明（开源生态篇）

## 运行

```bash
FACTS=$(python3 src/scripts/collect_daily_facts.py "<date>" --type ecosystem)
```

脚本读取本项目自有 SoR（全部 git 跟踪、本地即有、不联网）：
- `src/data/trending_snapshots.jsonl` — 每日/周/月 Trending 时序
- `src/data/starred.json`（缺则 `starred_seed.json`）— AI 大牛 star 快照
- `src/trending_repo/all_repos_deduped.json` — 跨窗口去重 trending
- `src/data/reports.json` — 380+ 篇已分析报告（回链用）
- `src/data/daily_digests.jsonl` — 历史日报（推 since 窗口）

只把 facts JSON 路径打印到 stdout。`Read` 它即可。

## facts JSON 字段

| 字段 | 含义 |
|---|---|
| `date` / `since` / `after_date` | 日报日期 / 上次同类日报日期（大牛 star 窗口起点） |
| `trending_period_key` | 取用的 daily 榜日期（通常= date 的前一天） |
| `stats` | 各板块计数（rising_total / rising_ai / pro_stars / pro_stars_multi / heating / resurface / report_index） |
| `rising_repos[]` | 今日 Trending(daily)：`name/url/language/stars/forks/rank/rank_delta/is_new/description/ai/report_slug` |
| `pro_stars[]` | 大牛新 star（按 url 聚合）：`name/url/stars/star_users/starred_by[{login,name}]/latest_starred_at/description/ai/report_slug` |
| `heating_up[]` | 跨窗口升温：`name/url/language/stars/trending_days/last_seen/description/ai/report_slug` |
| `resurface[]` | 旧文重读（AI 相关历史报告）：`slug/title/summary/language/stars/originalUrl` |
| `cache_seen_keys[]` | 近 30 天已推送过的归一 key（去重提示） |
| `report_url_index_path` | reports.json originalUrl→slug 全表落地路径（备用） |
| `_warnings[]` | 采集告警（某数据源缺失等） |

## 字段用法要点

- `ai` 为 `true` 才是 AI 相关；开源新星/升温板块**只用 `ai=true`** 的条目。
- `report_slug` 非空 = 本站已有深度报告，**必须回链** `/reports/{slug}/`。
- `rank_delta`：正数=排名上升幅度；`is_new=true`=新进榜（适合做「新星」）。
- `star_users ≥ 2` = 多位大牛同时 star，是最强选题信号，置顶。
- `cache_seen_keys` 命中的条目说明近期日报已收录，避免重复（脚本侧可用
  `dedup_daily.py filter` 自动剔除）。

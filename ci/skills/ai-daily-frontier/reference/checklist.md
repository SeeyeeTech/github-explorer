# 终稿自检清单（前沿资讯篇）

产出 md + meta.json 前逐项核对，任一不满足则修正或降级该条，**绝不带病发布**。

## 完整性
- [ ] 「今日必看 / 值得关注 / 简讯」三级中有条目的级别均有真实条目；空级别已省略标题（无空节）。
- [ ] 全部 <4.0（0 条达标）时，已改为「今日无重大 AI 资讯」收尾，未套模板凑数。
- [ ] 「今日提要 TL;DR」3-5 条看点与下文板块/条目对应。
- [ ] 各级条目已按 `category`（论文前沿/开源项目/模型与评测/工程实践/行业与融资）分组呈现。
- [ ] 非种子源占比 ≥ `scoring.yaml > min_non_seed_ratio`（0.2）；不足则提示补外部源（防信息茧房）。

## 事实核验（旗舰版核心）
- [ ] 每条「今日必看」（评分 ≥ verify_floor=7.0）均有 ≥2 个**独立**信源（非同一媒体集团/转载链）。
- [ ] 每个 `metric` 数字都带 `source_url`；无任何凭记忆 / 估算 / 外推数字
      （`numbers_from_source=false` 的数字已剔除）。
- [ ] 所有 `event_date` 为真实事件发生日期且在 `after_date` 窗口内；核实失败的已标注「日期未核实」。
- [ ] 融资 / 收购类已双边官方确认；仅单边的已降级或标注「待确认」。
- [ ] 核验不通过的高分条目已封顶 5.9（降级简讯）或丢弃，未保留原高分。

## 去重
- [ ] 已 `dedup_daily.py filter --type frontier` 做 L1（URL 归一 + cache 命中剔除）。
- [ ] LLM L2（标题）/ L3（内容）语义去重已做，同一事件不重复成多条。
- [ ] 内部开源信号与外部新闻已跨集合合并（同仓库/同论文一条，外部为主体、内部作徽标）。

## 回链
- [ ] 每个含 `repo_url` 的条目都据 `report_url_index_path` 反查过本站报告；命中的已回链
      `/reports/{slug}/`。
- [ ] 「🌱 开源信号」中 `report_slug` 非空的条目均已回链。

## 规范
- [ ] H1 ≤32 字、非模板、无营销词/感叹号/emoji 堆砌，含 ≥2 个钩子要素。
- [ ] 中文直角引号「」。
- [ ] frontmatter 含 title/date/summary/tags/canonical_url/syndicate；`canonical_url` 指向站点首页
      `https://seeyeetech.com/github-explorer/`（篇B 不上站）。
- [ ] meta.json 的 `digest` ≤120 字符、`title` ≤64 字符、`author` 为 NightVoyager、`theme` 合法。
- [ ] 每条卡片字段齐全：中文标题(原标题) / 分级+评分 / summary_zh / 要点 / method_zh /
      metrics(带 source_url) / repo_url|paper_url / 来源(≥2) / 分类标签。

## 收尾
- [ ] 已 `dedup_daily.py commit --type frontier` 把今日采纳 URL 写入 cache（次日去重）。
- [ ] 已 `record_daily.py --type frontier` 记录索引（CI 会带 --ci-run-id；同日重复幂等跳过）。
- [ ] 发布交接说明已给：`syndicate_publish.py src/ai_news/<date>.md --channel wechat --dry-run`。

# 终稿自检清单（开源生态篇）

产出 md + meta.json 前逐项核对，任一不满足则修正：

## 完整性
- [ ] 至少有「开源新星」或「大牛在看」之一非空；全空则已改为「今日无显著动态」收尾。
- [ ] 每个非空板块都有真实条目；空板块已省略标题（无空节）。
- [ ] 「今日导读」3 条看点与下文板块对应。

## 回链（核心价值）
- [ ] 所有 `report_slug` 非空的条目都回链了 `/reports/{slug}/`。
- [ ] 「旧文重读」2-4 篇均为 AI 相关历史报告，链接可跳。

## 数据真实性
- [ ] 所有 star 数 / 上榜天数 / star_users 均来自 facts，无凭记忆编造。
- [ ] 「大牛在看」的 `starred_by` 名单来自 facts.pro_stars[].starred_by。
- [ ] Phase 1 增强失败的条目已用 facts.description 兜底，无空洞占位。

## 去重
- [ ] 今日条目未与 `cache_seen_keys` / 近期日报重复（已 `dedup_daily.py filter` 或人工核对）。
- [ ] 外部增强条目与开源信号已跨集合合并（同仓库不重复成两条）。

## 规范
- [ ] H1 ≤32 字、非模板、无营销词/感叹号/emoji 堆砌，含 ≥2 个钩子要素。
- [ ] 中文直角引号「」。
- [ ] frontmatter 含 title/date/summary/tags/canonical_url/syndicate；canonical 指向 /daily/<date>/。
- [ ] meta.json 的 digest ≤120 字符、title ≤64 字符。

## 收尾
- [ ] 已 `dedup_daily.py commit` 把今日采纳 URL 写入 cache。
- [ ] 已 `record_daily.py` 记录索引（CI 会带 --ci-run-id）。

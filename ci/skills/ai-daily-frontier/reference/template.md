# AI 前沿日报模板（前沿资讯篇）

> **篇B 不上站**：日报落 `src/ai_news/`，站点不渲染 frontier（`record_daily.py` 入 jsonl 仅供
> since 窗口/去重）。因无站点详情页，`canonical_url` 指向站点首页。footer 仍加公众号导流。

## 产物 1：`src/ai_news/<date>.md`

带 YAML frontmatter（供 syndicate `parse_report()` 解析；syndicate 渲染时会去掉正文首个 H1，
标题在各平台是独立字段）。

```markdown
---
title: "<按标题创作规则现场生成的 H1，同 # 标题>"
date: "<YYYY-MM-DD>"
summary: "<一句话提要，进 RSS/列表/公众号摘要>"
tags: ["AI 日报", "前沿", "<当日主题如 模型/论文/融资>"]
canonical_url: "https://seeyeetech.com/github-explorer/"
syndicate: true
---

# <H1：同 frontmatter.title>

> AI 前沿日报 · <YYYY-MM-DD> · 全网采集 + 对抗式核验 · 数据源：论文/模型/博客/榜单/中文媒体

## 📋 今日提要 TL;DR

<1 句话定调 + 3-5 条最大看点（每条一行，带 → 指向下文板块/链接，标注分类）>

## 🔥 今日必看（评分 ≥ 8.0）

> 按 category 分组呈现（论文前沿 / 开源项目 / 模型与评测 / 工程实践 / 行业与融资）

### 论文前沿

#### 1. <中文标题>（<原标题 title_en>）· 🔥 必看 8.x

<summary_zh：2-3 句，说清创新点与实际意义（是什么/为何重要/对读者意味着什么）>

要点：
- <key_point 1>
- <key_point 2>

方法：<method_zh，一句话核心技术路线>
指标：<metric.name> <metric.value>（vs <baseline>）— [来源](<metric.source_url>)
链接：[论文](<paper_url>) · [代码](<repo_url>)
来源：[<source_name 1>](<url>) · [<佐证源 2>](<secondary_source>)（≥2 独立源）
标签：`<category>` `<tags>`
<若 repo_url 命中本站报告：> 📖 本站已有深度报告 → [/reports/{slug}/](https://seeyeetech.com/github-explorer/reports/{slug}/)

#### 2. ...

### 模型与评测

#### N. ...

（条目连续编号，跨 category / 跨板块不重置）

## 👀 值得关注（评分 6.0 – 7.9）

> 同样按 category 分组；卡片字段同上，可酌情精简（要点 1-2 条）

### 开源项目

#### N. <中文标题>（<原标题>）· 👀 关注 6.x
...

## 📌 简讯（评分 4.0 – 5.9）

> 一句话速览，仍须带来源链接；按 category 分组

- **<中文标题>**（`<category>`）— <一句话> [来源](<url>) · [佐证](<secondary>)

## 🌱 开源信号

> 来自 Phase 0 内部 facts（GitHub Trending + 大牛 Star 快照）的增强角，外部新闻已合并者不重复

- **[owner/repo](url)** — <N 天上榜 / 被 M 位大牛 Star> · ⭐ stars · <一句话>
  <若 report_slug 非空：> 📖 深度报告 → [/reports/{slug}/](https://seeyeetech.com/github-explorer/reports/{slug}/)

## 🔧 方法与来源

本期：必看 N 条 · 关注 N 条 · 简讯 N 条 · 开源信号 N 条。
采集源 <X> 个（WebFetch <a> cluster + WebSearch <b> theme×中英）· 去重命中 <D> 条 ·
核验通过率 <P>%（必看条目均 ≥2 独立源）· 非种子源占比 <R>%（下限 0.2）。
采集 → 三层去重 → frontier 5 维评分 → 对抗式事实核验（高分必交叉验证、数字必带源、融资双边）。

---

> 本文由「AI 前沿日报」自动汇编，全网采集 + 对抗式事实核验。更多 AI 项目深度解析见
> https://seeyeetech.com/github-explorer/
```

## 产物 2：`src/ai_news/<date>.meta.json`

```json
{
  "title": "<H1，≤64 字符>",
  "digest": "<摘要 ≤120 字符，从今日提要提炼>",
  "author": "NightVoyager",
  "theme": "universe,dark"
}
```

`theme` 从 `stars / universe / ocean / desert / forest / green-trees / dark` 任挑组合（Unsplash 封面词）。

## 约定

- **canonical 约定**：篇B 无站点详情页，`canonical_url` 一律指向站点首页
  `https://seeyeetech.com/github-explorer/`（≠ 篇A 的 `/daily/<date>/`）。
- 每个板块若为空，**省略该板块标题**，不留空节（但「今日必看/关注/简讯」三级里至少一级有条目，
  否则全 <4.0 时按下条改写）。
- **0 条达标**（全部 <4.0）：不套上面模板，正文直接写「今日无重大 AI 资讯」并简述采集与核验情况，
  仍正常收尾（commit cache + record_daily）。
- **有几条出几条，不为凑数降阈值**。
- 每个含 `repo_url` 的条目都要据 `report_url_index_path` 反查本站报告，命中则回链。
- 每个 `metric` 数字必须带 `source_url`；必看条目须 ≥2 独立来源链接。
- H1 同时写进 frontmatter.title 与正文 `#`；直角引号「」；不编造源外数字。

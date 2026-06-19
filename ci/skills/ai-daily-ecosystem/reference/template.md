# 开源 AI 日报模板

## 产物 1：`src/daily_report/<date>.md`

带 YAML frontmatter（供 syndicate `parse_report()` 与站点 content collection 共用）。
`<base>` = 站点 base（部署为 `https://seeyeetech.com/github-explorer`）。

```markdown
---
title: "<按标题创作规则现场生成的 H1，同 # 标题>"
date: "<YYYY-MM-DD>"
summary: "<一句话提要，进站点列表/RSS>"
tags: ["AI 日报", "开源", "<当日主题如 Agent/推理>"]
canonical_url: "<base>/daily/<YYYY-MM-DD>/"
syndicate: true
---

# <H1：同 frontmatter.title>

> 开源 AI 日报 · <YYYY-MM-DD> · 数据源：GitHub Trending + 大牛 Star 快照 + 本站 380+ 篇报告

## 📌 今日导读

<1 句话定调 + 3 条最大看点（每条一行，带 → 指向下文板块/链接）>

## 🌟 开源新星

> 今日 Trending 里的 AI 新仓库（优先未被深度分析过的）

### 1. [owner/repo](url) · ⭐ stars · <language> · <N 天上榜/新进榜>

<一句话：它解决什么、为何值得看（来自 Phase 1 增强或 facts.description，禁营销词）>

要点：<2-3 条，可省略>
<若 report_slug 非空：> 📖 本站已有深度报告 → [/reports/{slug}](<base>/reports/{slug}/)

（连续编号，跨板块不重置）

## 👀 大牛在看

> 白名单 AI 大牛自上次日报以来新 star 的项目（多位同时 star 置顶）

### N. [owner/repo](url) · ⭐ stars

被 <M> 位大牛 star：<starred_by 的 name/login 列举>
<一句话简介>
<若 report_slug 非空：> 📖 深度报告 → [/reports/{slug}](<base>/reports/{slug}/)

## 🔥 升温追踪

> 跨窗口持续上榜、动量强的 AI 仓库

- **[owner/repo](url)** — <trending_days> 天上榜 · ⭐ stars · <一句话>〔已分析则附 📖 回链〕

## 📚 旧文重读

> 与今日主题相关、值得回看的本站历史深度报告（核心导流位）

- **[<报告标题>](<base>/reports/{slug}/)** — <summary 一句>

## 🔧 方法与来源

本期：开源新星 N 条 · 大牛在看 N 条 · 升温 N 条 · 旧文 N 篇。
数据来自 GitHub Trending（<trending_period_key> 榜）+ 白名单大牛 Star 快照（<since> 起）+
本站 380+ 篇深度分析。开源信号确定性聚合，外部增强为 best-effort 补充。

---

> 本文由「开源 AI 日报」自动汇编。更多开源项目深度解析见 <base>/
```

## 产物 2：`src/daily_report/<date>.meta.json`

```json
{
  "title": "<H1，≤64 字符>",
  "digest": "<摘要 ≤120 字符，从今日导读提炼>",
  "author": "NightVoyager",
  "theme": "stars,universe,dark"
}
```

`theme` 从 `stars / universe / ocean / desert / forest / green-trees / dark` 任挑组合（Unsplash 封面词）。

## 约定

- 每个板块若为空，**省略该板块标题**，不留空节。
- 所有 `report_slug` 非空的条目都必须回链，这是日报作为站内深度报告流量入口的核心价值。
- H1 同时写进 frontmatter.title 与正文 `#`；`parse_report` 会去掉正文首个 H1（标题在各平台是独立字段）。
- 直角引号「」；不编造数字。

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**GitHub 仓库探索技能**（repo-miner）：一个 Agent Skill，通过三阶段分析流程深度挖掘 GitHub 仓库的价值信息，产出结构化分析报告，用于公众号发布。

## 核心工作流

### 三阶段分析流程

每个仓库的分析分三个阶段，中间产物存放在 `tmp/`（命名为 `{repo}-{phase}-analysis.md`，已 gitignore，不入库）：

1. **Phase 1 — 网络分析（Network）**：作者背景、社区活跃度、增长趋势
2. **Phase 2 — 元分析（Meta）**：代码统计、提交历史、开发节奏
3. **Phase 3 — 内容分析（Content）**：架构解读、创新点、技术价值

最终合并为 `src/analysis_report/{username}_{repo_name}.md`。

### 常用命令

```bash
# 使用 repo-miner 技能分析单个仓库
/repo-miner <github_url>

# 批量并发分析（从仓库列表文件）
./batch_analyze.sh [repos_file] [start_line] [end_line] [concurrency]
# 默认：./batch_analyze.sh src/analysis_report/repos.md 1 0 5

# 抓取大牛 starred → 重写 src/data/starred_seed.json（需 gh CLI 已登录；refresh-data.yml 每日自动跑）
python3 src/scripts/fetch_starred.py

# 解析 GitHub Trending 归档数据 → src/data/trending_snapshots.jsonl
# 需先克隆 archive：git clone --depth 1 https://github.com/duzhuoshanwai/github-trending-archive /tmp/github-trending-archive
# 时间窗默认 2025-09-22 ~ 今天，可用 TRENDING_START_DATE / TRENDING_END_DATE / TRENDING_ARCHIVE_DIR 覆盖
python3 src/trending_repo/parse_trending.py

# 刷新站点元数据（建库 → 灌各 SoR → 导出 JSON/YAML，顺序同 CI）
python3 src/scripts/init_db.py init && python3 src/scripts/init_db.py seed-publish
python3 src/scripts/fetch_repo_enrich.py     # 可选：gh api 补 stars/license 等 → repo_enrich.json（需 gh 登录）
python3 src/scripts/build_reports_index.py   # 解析 md；缺失的客观字段用 repo_enrich.json 兜底
python3 src/scripts/extract_tags.py          # 必须在 export-json 前，否则 tags.yaml 会被清空
python3 src/scripts/parse_starred.py         # 读 src/data/starred_seed.json
python3 src/scripts/seed_trending.py         # 读 src/data/trending_snapshots.jsonl
python3 src/scripts/init_db.py export-json   # → reports.json / tags.yaml / starred.json / all_repos_deduped.json

# 查"被多人 Star"选题信号（替代旧 repo-frequency.md）
sqlite3 src/data/db.sqlite "SELECT user_count, name FROM v_starred_frequency WHERE user_count>=2 ORDER BY user_count DESC;"

# 本地预览站点
cd site && npm install && npm run dev   # http://localhost:4321

# 构建静态站点
cd site && npm run build                # 输出 site/dist + pagefind 索引

# 发布分析报告为公众号文章
/md2wechat <report_path>
```

## 项目结构

- **src/analysis_report/** — 最终分析报告（375+ 篇），命名 `{username}_{repo_name}.md`，部分有 `.html` 发布版
- **src/trending_repo/** — `parse_trending.py`（从 archive 生成 SoR）+ `all_repos_deduped.json`（DB 导出的去重汇总，供站点/选题读取）
- **src/data/** — 站点元数据 + 各数据源 SoR：
  - 配置/导出：`reports.json` / `tags.yaml` / `tag-rules.yaml` / `users.yaml` / `trending-config.yaml` / `starred.json`
  - SoR（git 跟踪、脚本据此灌库）：`publish_history.jsonl`（发布历史）/ `starred_seed.json`（大牛 Star 快照）/ `trending_snapshots.jsonl`（Trending 时间序列）/ `repo_enrich.json`（报告仓库 gh api 元数据缓存，补 md 解析不到的 stars/forks/language/license/age）
  - 说明：`db.sqlite` 不入 Git，每次 CI 由上述 SoR 重建；站点读 JSON/YAML 导出。原 `src/starred_repo/*.md`、`src/trending_repo/{daily,weekly,monthly}/*.json`、`src/publish.md` 已迁入对应 SoR 并删除
- **src/scripts/** — 项目核心脚本（被 CI workflow 调用）：建库 `init_db.py`、索引 `build_reports_index.py`、标签 `extract_tags.py`、Star 抓取 `fetch_starred.py`（遍历 `users.yaml` 用 gh api 抓每人最近 ~200 个 star → 重写 `starred_seed.json`，`refresh-data.yml` 每日调用）、报告仓库元数据 enrich `fetch_repo_enrich.py`（对 `reports.json` 每个 url 用 gh api 抓 stars/forks/language/license/age → `repo_enrich.json`，供 `build_reports_index.py` 兜底 md 解析不到的客观字段；`refresh-data.yml` 每日调用）、Star 解析 `parse_starred.py`、Trending 入库 `seed_trending.py`、选题 `select_next_repo.py`（合并 trending + starred 双信号打分：`score = trending_days + star_users × STAR_WEIGHT`，starred-only 候选需 `star_users ≥ STAR_MIN_USERS`；读 git 跟踪的 `starred.json` 聚合，不依赖未重建的 DB）、repo-miner 确定性采集 `collect_repo_facts.py`（准备阶段跑一次，Phase 1 网络数据 + Phase 2 代码/提交指标 → 单份 JSON，两个并行 Agent 共用）、提交校验 `validate_submission.py`、发布记录 `record_publish.py`、索引推送 `ping_search_engines.py`、CI 环境 `setup_ci_env.sh` / 技能调用 `run_skill.sh` / 评论解析 `parse_issue_comment.py`
- **scripts/** — 一次性 / 辅助脚本（不入 CI）：公众号相关 `wechat_publish.py` / `_wechat_api.py` / `sync_wechat_status.py` / `apply_wechat_mapping.py` / `match_wechat_to_slugs.py` / `fetch_wechat_published.js`、DB 查询 `query_db.py`、历史迁移 `migrate_publish_md.py`
- **site/** — Astro 静态站点（GitHub Pages 部署源）
- **.github/** — Issue 模板 + Workflows（`pages.yml` 构建部署 / `analyze.yml` Issue 触发分析）
- **notes/prompts/** — 提示词模板（`notes/` 仅保留 prompts/tickets/todos；三阶段过程文件已改写到 `tmp/`，不再入库）
- **tmp/** — 临时文件 + 三阶段分析中间产物（已 gitignore）
- **batch_analyze.sh** — 批量分析脚本，使用信号量控制并发

## 站点 / 自动化提交流程

公开站点：<https://austinxt.github.io/github-explorer/>

**三条 workflow（互不干扰）**：

| Workflow | 触发 | 出口 | 适用 |
|---|---|---|---|
| `auto-analyze.yml`（分析）| 定时 / 手动 dispatch / 维护者 `/analyze` 评论 | 直接 push main + 公众号草稿 | 自动选题、维护者命令 |
| `analyze.yml`（站点提交）| `issues.opened` + `analyze-request` 标签 | 开 PR 待审核 | 外部用户站点 `/submit` 提交 |
| `refresh-data.yml`（数据刷新）| 每日 cron（UTC 20:00）/ 手动 dispatch | push main（连带触发 `pages.yml` 重建）| 抓 starred + trending 源数据，喂给 `select_next_repo.py` 选题 |

前两条（分析流）复用 `src/scripts/setup_ci_env.sh` + `src/scripts/run_skill.sh`（Minimax / Anthropic 双后端 fallback）；`refresh-data.yml` 只跑数据脚本（gh api 抓取 + Python），无需推理后端。

**用户提交链路**：
1. 用户在 `/submit` 表单填 URL → 跳到预填的 GitHub Issue
2. Issue 带 `analyze-request` 标签 → `analyze.yml` 触发
3. `validate_submission.py` 校验 URL / 公开性 / 是否重复 → 不通过则评论 + 关闭
4. 通过则跑 `/repo-miner` → 校验产出 → 开 PR；合并后 `pages.yml` 重新构建上线

**配置点**：
- 大牛白名单：编辑 `src/data/users.yaml`
- Trending 参数：编辑 `src/data/trending-config.yaml`
- 标签规则：编辑 `src/data/tag-rules.yaml`；手工校正某条则把 slug 加入 `tags.yaml` 的 `manual:` 列表
- Repo Secrets：`ANTHROPIC_API_KEY`（必需）+ `MINIMAX_API_KEY`/`MINIMAX_BASE_URL`（可选，作为主后端）；公众号发布另需 `WECHAT_APPID`/`WECHAT_APPSECRET`

## SEO 与索引推送

**SEO 实现位置**：

| 关注点 | 文件 |
|---|---|
| 站点级 meta / Twitter / OG / WebSite JSON-LD | `site/src/layouts/Base.astro` |
| 文章/列表/标签/Person JSON-LD | 各页 `<Fragment slot="head">` 内嵌 `<JsonLd>` |
| RSS 2.0 / JSON Feed 1.1 | `site/src/pages/rss.xml.ts` / `feed.json.ts` |
| robots.txt（动态） | `site/src/pages/robots.txt.ts` |
| sitemap 优先级与 lastmod | `site/astro.config.mjs` 的 `sitemap({ serialize })` |
| 默认社交卡片图 | `site/public/og-default.png`（设计师覆盖即可） |
| 报告社交卡 | 借用 GitHub `opengraph.githubassets.com`，零维护 |

**Repo Variables / Secrets**（可选，全部缺失时只是少推送/少验证一个渠道，不影响构建）：
- `vars.SITE_URL` / `vars.PUBLIC_BASE_PATH` — 切换自定义域名时改这两个 vars，无需改代码（`astro.config.mjs` 和 `ping_search_engines.py` 都读它）
- `secrets.INDEXNOW_KEY` — Bing/Yandex/AI 搜索的 IndexNow key；同时在 `site/public/` 放一个 `{KEY}.txt` 文件（内容就是 key）
- `secrets.BAIDU_PUSH_TOKEN` — 百度站长普通收录 token

**站长平台验证**：拿到 code 后填入 `site/src/lib/data.ts` 的 `SITE.verify.{google,baidu,bing}`，Base.astro 自动渲染 meta；或者把平台给的验证文件放到 `site/public/` 用文件法验证。

**索引推送**：每次 `pages.yml` 部署完成后自动跑 `src/scripts/ping_search_engines.py`，diff `tmp/last_indexed.json` 快照后只推新增/更新的报告 URL；本地干跑 `python3 src/scripts/ping_search_engines.py --dry-run`。

## 规则

- 文档使用中文，文件名使用英文
- 不自动提交，除非用户明确要求
- 敏感信息存 `.env.local`，不入 Git
- 分析报告中使用直角引号「」而非""

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**GitHub 仓库探索技能**（repo-miner）：一个 Agent Skill，通过三阶段分析流程深度挖掘 GitHub 仓库的价值信息，产出结构化分析报告，用于公众号发布。

## 核心工作流

### 三阶段分析流程

每个仓库的分析分三个阶段，中间产物存放在 `notes/`（命名为 `{repo}-{phase}-analysis.md`）：

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

# 解析 GitHub Trending 归档数据（需先克隆 github-trending-archive 到 /tmp）
python3 src/trending_repo/parse_trending.py

# 刷新站点元数据（reports.json / tags.yaml / starred.json）
python3 scripts/build_reports_index.py
python3 scripts/extract_tags.py
python3 scripts/parse_starred.py

# 本地预览站点
cd site && npm install && npm run dev   # http://localhost:4321

# 构建静态站点
cd site && npm run build                # 输出 site/dist + pagefind 索引

# 发布分析报告为公众号文章
/md2wechat <report_path>
```

## 项目结构

- **src/analysis_report/** — 最终分析报告（375+ 篇），命名 `{username}_{repo_name}.md`，部分有 `.html` 发布版
- **src/publish.md** — 公众号发布记录与待发布队列
- **src/starred_repo/** — GitHub 用户 Star 仓库分析快照
- **src/trending_repo/** — GitHub Trending 数据（daily/weekly/monthly JSON + 去重汇总）
- **src/data/** — 站点元数据与配置：`reports.json` / `tags.yaml` / `tag-rules.yaml` / `users.yaml` / `trending-config.yaml` / `starred.json`
- **scripts/** — 数据提取脚本：`build_reports_index.py` / `extract_tags.py` / `parse_starred.py` / `validate_submission.py`
- **site/** — Astro 静态站点（GitHub Pages 部署源）
- **.github/** — Issue 模板 + Workflows（`pages.yml` 构建部署 / `analyze.yml` Issue 触发分析）
- **notes/** — 分析过程中间产物（`{repo}-network-analysis.md`、`-meta-analysis.md`、`-content-analysis.md`）
- **notes/prompts/** — 提示词模板
- **tmp/** — 临时文件（已 gitignore）
- **batch_analyze.sh** — 批量分析脚本，使用信号量控制并发

## 站点 / 自动化提交流程

公开站点：<https://austinxt.github.io/github-explorer/>

**两条触发流（互不干扰）**：

| Workflow | 触发 | 出口 | 适用 |
|---|---|---|---|
| `auto-analyze.yml`（已存在）| 定时 / 手动 dispatch / 维护者 `/analyze` 评论 | 直接 push main + 公众号草稿 | 自动选题、维护者命令 |
| `analyze.yml`（站点提交）| `issues.opened` + `analyze-request` 标签 | 开 PR 待审核 | 外部用户站点 `/submit` 提交 |

两者都复用 `scripts/setup_ci_env.sh` + `scripts/run_skill.sh`（Minimax / Anthropic 双后端 fallback）。

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

**索引推送**：每次 `pages.yml` 部署完成后自动跑 `scripts/ping_search_engines.py`，diff `tmp/last_indexed.json` 快照后只推新增/更新的报告 URL；本地干跑 `python3 scripts/ping_search_engines.py --dry-run`。

## 规则

- 文档使用中文，文件名使用英文
- 不自动提交，除非用户明确要求
- 敏感信息存 `.env.local`，不入 Git
- 分析报告中使用直角引号「」而非""

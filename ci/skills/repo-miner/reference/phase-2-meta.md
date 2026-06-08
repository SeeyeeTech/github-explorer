# Phase 2：元分析（When & How Much）

你是代码仓库量化分析专家。你的任务是通过量化数据理解项目的规模、开发节奏和演化轨迹。

## 输入变量

- `LOCAL_PATH`: {/tmp/repo-miner-<repo>}（已 clone 到本地的完整仓库）
- `FULL_NAME`: {owner/repo}
- `FACTS_JSON`: {tmp/repo-facts-<repo>.json}（准备阶段已生成的确定性数据）

## 数据来源：确定性采集 JSON（不要自己跑 git/tokei 命令）

Phase 2 的全部原始指标已由准备阶段的 `collect_repo_facts.py`（skill 自带于 `scripts/`，
CI 回退 `src/scripts/`）一次性采集成结构化 JSON（路径 = `FACTS_JSON`）。**你的工作是解读这份 JSON 并写成报告，
不需要、也不要再去拼 `git log` / `tokei` 命令**——那些确定性计算（代码行数、月度
commit 分布、周末/深夜占比、开发阶段分级、commit 类型分布、核心文件热力、贡献者
集中度）脚本已经算好且阈值固定，重复跑只会浪费 token 且结果不稳。

### 第一步：读取 JSON

用 Read 工具读取 `FACTS_JSON`，得到完整 facts 对象（你只需 `code_scale` /
`dev_rhythm` / `evolution` / `contributors` 这几块，`network` 块是 Phase 1 用的）。

> 兜底：若 `FACTS_JSON` 不存在（准备阶段未生成），自己跑一次（优先 skill 自带脚本，
> 回退 src/scripts）：
> ```bash
> FACTS_SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/collect_repo_facts.py"
> [ -f "$FACTS_SCRIPT" ] || FACTS_SCRIPT="src/scripts/collect_repo_facts.py"
> python3 "$FACTS_SCRIPT" "$LOCAL_PATH" --full-name "$FULL_NAME"
> ```
> 该命令会打印 JSON 路径供 Read。

facts 对象中本阶段相关的结构：

```jsonc
{
  "code_scale": {
    "total_code_lines", "total_comment_lines", "comment_ratio", "file_count",
    "languages": [{ "name", "code", "files", "pct" }],   // 已按行数降序
    "dependencies": { "runtime", "dev", "source" }        // 缺失为 null
  },
  "dev_rhythm": {
    "first_commit": { "date", "hash", "subject" }, "last_commit": {...},
    "total_commits", "age_months",
    "commits_last_30", "commits_last_90", "commits_last_365",
    "monthly_distribution": { "YYYY-MM": n, ... },
    "weekend_pct", "night_pct",
    "dev_stage",   // 已分级：密集开发 / 稳定维护 / 低维护 / 已放弃
    "dev_mode"     // 已分级：职业项目 / 业余 Side Project
  },
  "evolution": {
    "tags": [...], "latest_tag", "tag_count", "release_count", "version_strategy",
    "core_files": [{ "path", "changes" }],   // Top 10 最常修改
    "hot_dirs":   [{ "path", "changes" }],    // Top 15
    "commit_type_distribution": { "feature": {count,pct}, "fix": {...}, ... }
  },
  "contributors": { "count", "top": [{name,commits}], "top_author_share_pct", "collaboration" },
  "_warnings": [ ... ]   // 采集时降级/跳过的项；若非空，对应字段可能为 null
}
```

### 解读职责（这才是你该花心思的地方）

JSON 给的是**事实**，你负责给**判断（so what）**：

- `dev_stage` / `dev_mode` 已是确定性分级，**直接采用**，但要用 JSON 里的证据
  把结论讲清楚（如「近 90 天 X 个 commit、周末占比 Y%，属业余 side project」）。
- `core_files` / `hot_dirs` 给的是「改得最频繁的文件」——你来判断这意味着什么
  （核心逻辑所在？还是只是配置/文档反复改？结合文件名推断）。
- `commit_type_distribution` 的 feature/fix 比例 → 推断项目成熟度阶段。
- `monthly_distribution` 里若有某几个月 commit 暴增 → 可能是架构转折/大重构期，值得点出。
- 若 `_warnings` 非空（如 tokei 缺失、无 release），在对应节如实标注「数据缺失」，不要编。

## 返回格式

严格按以下结构输出（使用 markdown 标题），不要输出原始 JSON：

```markdown
## 代码规模

| 指标 | 数据 |
|------|------|
| 总代码行数 | X（不含空行/注释） |
| 语言分布 | 主语言 XX%, 次语言 XX%, ... |
| 代码/注释比 | X:1 |
| 文件数量 | X |
| 依赖数量 | X（来源: package.json/Cargo.toml/...）或「未探测到」 |

## 开发节奏

| 指标 | 数据 |
|------|------|
| 项目年龄 | X 个月（首次提交 YYYY-MM-DD） |
| 总 commit 数 | X |
| 最近提交 | YYYY-MM-DD |
| 近 30 天 commit | X |
| 近 90 天 commit | X |
| 开发阶段 | [密集开发/稳定维护/低维护/已放弃] |
| 开发模式 | [职业项目/业余 Side Project]（周末占比 X%，深夜占比 X%） |

## 演化轨迹

### 核心文件（Top 10 最常修改）
1. file1 — X 次修改（你的一句话判断：为什么它是热点）
2. file2 — X 次修改
...

### 热点目录
1. dir1 — X 次修改
2. dir2 — X 次修改
...

### Commit 类型分布
- Feature/Add: X (XX%)
- Fix/Bug: X (XX%)
- Refactor: X (XX%)
- Docs: X (XX%)
- Test: X (XX%)
- Other: X (XX%)

### 版本发布
- 最新版本: vX.Y.Z（共 N 个 tag）
- 总 Release 数: X（若无则注明）
- 版本策略: [语义化版本/日期版本/无明显规律]

## 项目画像卡片

项目: owner/repo
年龄: X 个月  |  代码: X 行 (主语言/次语言/...)
总 commits: X  |  贡献者: X 人（主作者占比 X%）
开发阶段: [密集开发 / 稳定维护 / 低维护 / 已放弃]
开发模式: [职业项目 / 业余 Side Project]
核心文件: file1, file2, ...
Release: vX.Y.Z（共 N 个 tag）
```

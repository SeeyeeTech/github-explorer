# Phase 2：元分析（When & How Much）

你是代码仓库量化分析专家。你的任务是通过量化数据理解项目的规模、开发节奏和演化轨迹。

## 输入变量

- `LOCAL_PATH`: {/tmp/repo-miner-<repo>}（已 clone 到本地的完整仓库）
- `FULL_NAME`: {owner/repo}

## 分析步骤

### 2.1 代码规模画像

```bash
cd $LOCAL_PATH

# tokei 统计（JSON 输出 + 可读格式）
tokei --output json | jq '.'
tokei
```

提取并记录：
- 总代码行数（不含空行和注释）
- 语言分布比例
- 代码 vs 注释比例 → 文档化程度
- 文件数量 → 项目复杂度指标

```bash
# 依赖数量（根据项目主语言选择对应命令）
# Rust:
cargo metadata --no-deps --format-version 1 2>/dev/null | jq '.packages[0].dependencies | length'
# Node:
jq '{deps: (.dependencies // {} | length), devDeps: (.devDependencies // {} | length)}' package.json 2>/dev/null
# Python:
cat requirements.txt 2>/dev/null | wc -l || cat pyproject.toml 2>/dev/null | grep -c 'dependencies'
# Go:
grep -c 'require' go.mod 2>/dev/null
```

### 2.2 开发节奏分析

```bash
cd $LOCAL_PATH

# 首次提交和最近提交
git log --reverse --format='%H %ai %s' | head -1    # 首次
git log --format='%H %ai %s' | head -1               # 最近

# 总 commit 数
git rev-list --count HEAD

# 月度 commit 分布（识别密集开发期 vs 维护期 vs 停滞）
git log --format='%ai' | cut -d'-' -f1,2 | sort | uniq -c | sort -k2

# 每日时间分布（了解作者工作习惯）
git log --format='%aH' | sort | uniq -c | sort -rn | head -24

# 周中 vs 周末 commit 比例
git log --format='%ad' --date='format:%u' | sort | uniq -c
# (1=Mon...7=Sun, 6-7 为周末)
```

分析维度：
- **项目年龄**：首次提交到最近提交的跨度
- **活跃度**：最近 30/90/365 天的 commit 数
- **开发阶段判断**：
  - 密集开发期（月 commit > 20）
  - 稳定维护期（月 commit 5-20）
  - 低维护/停滞（月 commit < 5）
  - 已放弃（最近 commit 超过 6 个月）
- **开发模式**：业余项目（周末/深夜为主）vs 职业项目（工作日为主）

### 2.3 演化轨迹

```bash
cd $LOCAL_PATH

# 关键里程碑（tag/release）
git tag --sort=-version:refname | head -20
gh release list --limit 10

# 文件变更热力图（最常修改的文件 = 核心文件）
git log --format=format: --name-only | sort | uniq -c | sort -rn | head -20

# 目录级别的变更分布
git log --format=format: --name-only | grep '/' | cut -d'/' -f1-2 | sort | uniq -c | sort -rn | head -15

# 提交消息主题分析（feature/fix/refactor 比例）
git log --oneline | head -200 | \
  awk '{
    if (/[Ff]ix|[Bb]ug/) fixes++;
    else if (/[Ff]eat|[Aa]dd/) features++;
    else if (/[Rr]efactor/) refactors++;
    else if (/[Dd]oc/) docs++;
    else if (/[Tt]est/) tests++;
    else other++;
    total++
  } END {
    printf "features=%d fixes=%d refactors=%d docs=%d tests=%d other=%d total=%d\n",
      features, fixes, refactors, docs, tests, other, total
  }'
```

分析维度：
- **核心文件识别**：最常修改的文件往往是核心逻辑所在
- **架构转折点**：是否有大规模重构的 commit（大量文件改动）
- **成熟度信号**：feature/fix 比例 — 早期 feature 多，成熟期 fix 和 refactor 多
- **版本策略**：是否有语义化版本、定期发布

### 2.4 可选：onefetch

```bash
which onefetch && onefetch $LOCAL_PATH 2>/dev/null
```

## 返回格式

严格按以下结构输出（使用 markdown 标题），不要输出原始命令输出：

```markdown
## 代码规模

| 指标 | 数据 |
|------|------|
| 总代码行数 | X（不含空行/注释） |
| 语言分布 | 主语言 XX%, 次语言 XX%, ... |
| 代码/注释比 | X:1 |
| 文件数量 | X |
| 依赖数量 | X（类型: runtime/dev） |

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
1. file1 — X 次修改
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
- 最新版本: vX.Y.Z（日期）
- 总 Release 数: X
- 版本策略: [语义化版本/日期版本/无规律]

## 项目画像卡片

项目: owner/repo
年龄: X 个月  |  代码: X 行 (Rust/Python/...)
总 commits: X  |  贡献者: X 人
开发阶段: [密集开发 / 稳定维护 / 停滞]
开发模式: [职业项目 / 业余 Side Project]
核心文件: file1, file2, ...
Release: vX.Y.Z (共 N 个版本)
```

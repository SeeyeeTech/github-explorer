# Repo Miner 命令速查

## 网络分析命令

```bash
# 仓库概况
gh repo view OWNER/REPO --json name,description,stargazerCount,forkCount,watchers,issues,pullRequests,licenseInfo,primaryLanguage,languages,createdAt,updatedAt,pushedAt,isArchived,isFork,repositoryTopics,diskUsage

# 作者信息
gh api users/OWNER --jq '{login,name,bio,company,followers,public_repos,created_at}'

# 作者最近活跃仓库
gh api users/OWNER/repos --jq 'sort_by(.pushed_at) | reverse | .[0:10] | .[] | {name,pushed_at,stargazers_count,language}'

# 贡献者
gh api repos/OWNER/REPO/contributors --jq '.[] | {login,contributions}'

# Stargazer 时间分布
gh api repos/OWNER/REPO/stargazers -H "Accept: application/vnd.github.star+json" --paginate --jq '.[].starred_at' | tail -100

# 竞品搜索
gh api search/repositories -f q="KEYWORD language:LANG" -f sort=stars -f per_page=5 --jq '.items[] | {full_name,stargazers_count,description}'
```

## 元分析命令

```bash
# 代码统计
tokei --output json | jq '.'
tokei

# 备选
cloc . --json
find . -name '*.EXT' | xargs wc -l

# Git 历史
git log --reverse --format='%H %ai %s' | head -1          # 首次提交
git log --format='%H %ai %s' | head -1                     # 最近提交
git rev-list --count HEAD                                    # 总 commit 数

# 月度 commit 分布
git log --format='%ai' | cut -d'-' -f1,2 | sort | uniq -c | sort -k2

# 每日小时分布
git log --format='%aH' | sort | uniq -c | sort -rn

# 周中/周末比例
git log --format='%ad' --date='format:%u' | sort | uniq -c

# 文件变更热力图
git log --format=format: --name-only | sort | uniq -c | sort -rn | head -20

# Release 列表
git tag --sort=-version:refname | head -20
gh release list --limit 10

# Commit 类型分布
git log --oneline | head -200 | awk '{if (/[Ff]ix/) f++; else if (/[Ff]eat|[Aa]dd/) a++; else o++} END {print "feat:"a, "fix:"f, "other:"o}'
```

## 内容分析命令

```bash
# 测试文件
find . -name '*test*' -o -name '*spec*' | head -20
grep -rc '#\[test\]' src/ tests/ 2>/dev/null | wc -l   # Rust
grep -rc 'def test_' . 2>/dev/null | wc -l              # Python

# 文档统计
find . -name '*.md' -not -path '*/node_modules/*' -not -path '*/.git/*' | wc -l

# 错误处理 (Rust)
grep -rc '\.unwrap()' src/ 2>/dev/null
grep -rc '\.expect(' src/ 2>/dev/null

# CI/CD
ls .github/workflows/ .gitlab-ci.yml .circleci/ Makefile justfile 2>/dev/null

# 目录结构
find . -maxdepth 3 -type d -not -path '*/.git/*' -not -path '*/node_modules/*' | head -50

# onefetch (可选)
onefetch
```

## WebFetch 备选

```
# 主选
WebFetch: https://target-url

# 失败时使用 JINA Reader
WebFetch: https://r.jina.ai/https://target-url
```

## Star History

```
# SVG 图（可 WebFetch）
https://api.star-history.com/svg?repos=OWNER/REPO&type=Date

# 网页版（展示给用户）
https://star-history.com/#OWNER/REPO&Date
```

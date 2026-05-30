# Github 仓库探索技能

一个用于探索 GitHub 仓库的 Agent Skill，能够解读代码仓库的内容，分析出有价值的信息，并发布到微信公众号。

## 本地用法

```bash
# 分析单个仓库
/repo-miner https://github.com/owner/repo

# 批量并发分析
./batch_analyze.sh docs/analysis_report/repos.md 1 0 8

# 发布报告到公众号草稿箱
/md2wechat src/analysis_report/{username}_{repo}.md
```

## GitHub Actions 自动化（无人值守）

整套流水线 `.github/workflows/auto-analyze.yml`，三种触发方式：

| 方式 | 适用场景 |
|---|---|
| `schedule` cron | 每日 06:00（北京时间）自动跑 1 篇 |
| `workflow_dispatch` | Actions 页面手动触发，可选输入 `repo_url` / `skip_publish` / `force_backend` |
| `issue_comment` | 在仓库新建 issue 后评论 `/analyze <github-url>` 即可触发（仅授权用户） |

### 准备 Secrets

去仓库 Settings → Secrets and variables → Actions 添加：

| Secret | 必需 | 说明 |
|---|---|---|
| `MINIMAX_API_KEY` | 是 | [Minimax token plan](https://platform.minimaxi.com/docs/token-plan/claude-code) 申请，CI 里会被映射为 `ANTHROPIC_AUTH_TOKEN` |
| `WECHAT_APPID` | 是 | 微信公众号 AppID |
| `WECHAT_APPSECRET` | 是 | 微信公众号 AppSecret |
| `ANTHROPIC_API_KEY` | 否 | 仅应急降级用，正常运行不要配。配上后手动 dispatch 选 `force_backend=anthropic` 才生效 |

> 公众号后台「IP 白名单」必须清空或加 GitHub Actions 出口 IP；动态 IP 几乎只能选清空。

### 推理后端策略

默认只走 **Minimax 的 Anthropic 兼容端点**，无 fallback：

```
claude -p "/repo-miner …" --dangerously-skip-permissions
   ANTHROPIC_BASE_URL   = https://api.minimaxi.com/anthropic   ← 国内版，写死在 run_skill.sh
   ANTHROPIC_AUTH_TOKEN = $MINIMAX_API_KEY                     ← Minimax 用 AUTH_TOKEN 而非 API_KEY
   ANTHROPIC_API_KEY    = (清空，避免冲突)
```

同后端失败时自动重试 1 次（默认值，`--retries N` 可调）。**用国际版** `api.minimax.io/anthropic` 时把 `scripts/run_skill.sh` 顶部 `MINIMAX_ENDPOINT` 改掉，或临时设环境变量 `MINIMAX_BASE_URL_OVERRIDE`。

**应急降级**：万一 Minimax 在某个 skill 行为上不兼容（例如 subagent / tool use 协议），可手动 dispatch 时选 `force_backend=anthropic`，前提是先配了 `ANTHROPIC_API_KEY` secret。这只是「跑通」兜底，**不是常态用法**。

### 端到端流程

```
guard (鉴权 / 跳过非 /analyze 评论)
  ↓
analyze
  ├─ Checkout main
  ├─ setup_ci_env.sh  ── 装 gh/jq/tokei/claude-code，vendor skill → ~/.claude/skills/
  ├─ Decide target URL ── 优先 dispatch 输入 → issue 评论 → 自动选 (select_next_repo.py)
  ├─ run_skill.sh "/repo-miner $URL …"
  ├─ run_skill.sh "/md2wechat <report> 入草稿箱"
  ├─ 更新 src/publish.md，commit & push 回 main
  └─ 上传 tmp/logs 为 artifact（14 天）
```

### 验证清单

首次跑之前：

1. 把上面 5 个 secrets 都填好
2. Actions → Auto Analyze & Publish → Run workflow，**留空 repo_url** 让脚本自动选
3. 等 15-30 分钟
4. 检查：
   - `notes/` 是否多了三个 `*-{network,meta,content}-analysis.md`
   - `src/analysis_report/{owner}_{repo}.md` 是否生成
   - 微信公众号后台「草稿箱」是否有新草稿（封面 + 标题 + 正文）
   - `src/publish.md` 是否追加了一行
   - main 分支是否有 `feat(auto): 分析 ...` 的新 commit

### 同步 vendored skills

升级 `repo-miner` / `md2wechat` 后：

```bash
42plugin update opc/starlight/repo-miner
42plugin update zhiping/creator/md2wechat
cp -RL .claude/skills/repo-miner ci/skills/
cp -RL .claude/skills/md2wechat ci/skills/
git add ci/skills && git commit -m "chore: 同步 vendored skills"
```

## 目录速查

- `src/analysis_report/` — 最终分析报告（375+ 篇）
- `src/publish.md` — 公众号发布记录与待发布队列
- `src/starred_repo/` — GitHub 用户 Star 仓库分析
- `src/trending_repo/` — Trending 数据采集 + 去重汇总
- `notes/` — 三阶段分析中间产物
- `scripts/` — CI 用脚本（select / run_skill / setup）
- `ci/skills/` — vendored skill 文件，CI 启动时拷到 runner 的 `~/.claude/skills/`
- `.github/workflows/auto-analyze.yml` — 主自动化 workflow

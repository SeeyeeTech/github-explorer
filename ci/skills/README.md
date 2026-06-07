# Vendored Skills

本目录是 GitHub Actions runner 上使用的 Claude Code skill 副本，避免 CI 时依赖 42plugin 平台。

## 来源

| Skill | 上游 | 协议 |
|---|---|---|
| `repo-miner/` | `opc/starlight/repo-miner` v1.0.1（42plugin） | MIT |
| `md2wechat/` | `zhiping/creator/md2wechat` v1.0.1（42plugin） | MIT |
| `ai-daily-ecosystem/` | 本仓库自建（开源 AI 日报） | MIT |
| `ai-daily-frontier/` | 本仓库自建（AI 前沿日报，对标 MorningAI） | MIT |

每个子目录都保留了 `LICENSE` 文件，符合 MIT 协议要求。

两个 `ai-daily-*` 是本项目自建 skill（非 42plugin 上游），直接维护在本目录；它们调用共享
脚本 `src/scripts/{collect_daily_facts,dedup_daily,record_daily}.py` 与共享配置
`src/data/ai-daily/*`（采集源 / 评分 rubric / 去重 / 核验规则）。

## 同步策略

**42plugin 上游 skill**（repo-miner / md2wechat）：本地用 `42plugin install` / `update`
跟进上游版本后，运行：

```bash
cp -RL .claude/skills/repo-miner ci/skills/
cp -RL .claude/skills/md2wechat ci/skills/
git add ci/skills && git commit -m "chore: 同步 vendored skills"
```

**本仓库自建 skill**（ai-daily-ecosystem / ai-daily-frontier）：直接在本目录编辑即可；
若想本地用 `/ai-daily-*` 调用，可反向 symlink 到 `.claude/skills/`：

```bash
ln -s "$PWD/ci/skills/ai-daily-ecosystem" .claude/skills/ai-daily-ecosystem
ln -s "$PWD/ci/skills/ai-daily-frontier"  .claude/skills/ai-daily-frontier
```

CI 启动时由 `src/scripts/setup_ci_env.sh` 把全部 4 个 skill 拷贝到 runner 的 `~/.claude/skills/`。

# Vendored Skills

本目录是 GitHub Actions runner 上使用的 Claude Code skill 副本，避免 CI 时依赖 42plugin 平台。

## 来源

| Skill | 上游 | 协议 |
|---|---|---|
| `repo-miner/` | `opc/starlight/repo-miner` v1.0.1 | MIT |
| `md2wechat/` | `zhiping/creator/md2wechat` v1.0.1 | MIT |

每个子目录都保留了上游 `LICENSE` 文件，符合 MIT 协议要求。

## 同步策略

本地用 `42plugin install` / `42plugin update` 跟进上游版本后，运行：

```bash
cp -RL .claude/skills/repo-miner ci/skills/
cp -RL .claude/skills/md2wechat ci/skills/
git add ci/skills && git commit -m "chore: 同步 vendored skills"
```

CI 启动时由 `scripts/setup_ci_env.sh` 拷贝到 runner 的 `~/.claude/skills/`。

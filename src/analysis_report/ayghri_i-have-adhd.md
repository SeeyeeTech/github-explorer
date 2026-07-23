# GitHub推荐：一份 prompt 统治 7 个 AI CLI：i-have-adhd 怎么用 580 行代码做到 9K stars

> GitHub: https://github.com/ayghri/i-have-adhd

## 一句话总结

i-have-adhd 是一份为 ADHD 读者重塑 LLM 输出风格的 Claude Code / Codex / Cursor / Copilot / Gemini CLI / OpenCode / Antigravity **跨 7 平台 Agent Skill**——不是软件工程，而是一份被打包成可分发插件的 prompt 工程资产，70 天内拿到 9,202 stars。

## 值得关注的理由

- **效率反差**：2.3 个月、580 行代码、9,200 stars——代码量与影响力之间存在 100 倍失衡，是观察「prompt + 平台分发」杠杆率的样本。
- **基础设施思维**：它不是写一份 prompt，而是解决**「同一份 prompt 怎么在 7 个 AI CLI 上一致加载、激活、评测」**这层基础设施问题——这一层至今没人系统做过。
- **评测方法学**：跑通了人类 judge + 5 维度加权 + release gate 的 prompt A/B 评估流程，且主动承认没有公开 benchmark 结果（issue #4 open），是少有的「意识到自己需要证据」的项目。

## 项目展示

![i-have-adhd hero logo](https://raw.githubusercontent.com/ayghri/i-have-adhd/main/logo.png) — 类型: hero

仓库 README 内嵌的「Before / After」对比表是这个项目最有力的视觉素材：

<table>
<tr>
<td width="50%">

### Before

> Great question! Let me think about this. Your auth flow has a few moving pieces: the middleware, the token verification, and the cookie handling. Looking at `src/auth.ts`, the `verifyToken` function (around lines 42-58) seems to be using an older `jsonwebtoken` API. One approach would be to update the package and rewrite that function. After making the change, you'd want to run the auth tests to confirm nothing breaks. By the way, you might also want to look at your dependency versions overall. Hope this helps! Let me know if you want to dig deeper.

</td>
<td width="50%">

### After

> Run `npm install jsonwebtoken@latest`, then edit `src/auth.ts:42`.
>
> 1. Open `src/auth.ts`
> 2. Replace `verifyToken` (lines 42–58) with the snippet below
> 3. Run `npm test -- auth.spec.ts`
>
> Next: paste the first failing line if any test fails.

</td>
</tr>
</table>

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/ayghri/i-have-adhd |
| Star / Fork | 9,202 / 434 |
| 代码行数 | 580 行（Python 83.1% / JSON 10.3% / Shell 2.2%；其中 Python 几乎全是 eval runner，prompt 文本才是核心交付物） |
| 注释行数 | 593 行（注释/代码 = 1.02——其中 95% 是 prompt 文本而非传统注释） |
| 文件数 | 17 个（.py / .json / .toml / .sh / .yaml） |
| 项目年龄 | 2.3 个月（首次提交 2026-05-13） |
| 开发阶段 | 密集开发（近 30 天 86 commits，占总量 90.5%） |
| 贡献模式 | 核心少数 + 社区协作（17 位贡献者，作者 ~36%） |
| 热度定位 | 已大众热门（70 天拿到 9K+ stars 由 HN Show HN 帖引爆） |
| 质量评级 | 代码[良好] 文档[优秀] 测试[基本] 评测方法学[创新] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

**Ayoub Ghriss (ayghri)**：CU Boulder **CLIMB 实验室** ML 研究者，账号 8.8 年，公开仓库 78 个。他的其他仓库围绕学术 ML / 写作工具链——`overleaf-mcp`（Overleaf ↔ LLM）、`KATA`、`tritonix`、`qwantize`——形成清晰的「学术写作 + 工程工具」轴线。i-have-adhd 在他最近 push 的仓库中排第 1，其他同名仓库 star 几乎为 0，因此这**不是系列实验的延续，而是 70 天前某个深夜的真痛点之作**。

### 问题判断

他在 SKILL.md 第一段直接列出 **5 条认知事实**：working memory 小、knowing ≠ doing、starting is hardest、time estimates 失真、dopamine 稀缺。这不是营销陈述，而是被 LLM 默认输出反复消耗过的结论——读一句 "Great question! Let me think..." 已被消耗掉 8 秒注意力，剩下的指令跟不上，已经放弃。

时机选择：**Agent Skill 生态在 2025-2026 进入产品化**，Claude Code / Codex 等平台开始支持 marketplace + hooks，**「个人 prompt 改装」从 CLI 黑话进入 GUI 范畴**。他抓住了这个窗口。

### 解法哲学

他没有选择「教用户驯化模型」（Anthropic 官方 Output Styles 的文档形态），而选择「教模型为人服务」。核心隐喻：把 LLM 输出当成给**working memory 小、dopamine 稀缺、time 失真**的读者用的产品。具体规则对照：

| 认知事实 | prompt 规则 |
|---|---|
| Working memory 小 | Rule 5: restate state every turn |
| Knowing ≠ Doing | Rule 1: lead with action, Rule 3: concrete next step |
| Starting is hardest | Rule 1: first line must be doable now |
| Time estimates 失真 | Rule 6: 具体分钟数，不写「一会」 |
| Dopamine 稀缺 | Rule 7: make wins visible |

最后一个亮点：他**主动承认 prompt 强制是双刃剑**——issue #4（仍 open）问「这种 prompt 是否会降低模型表现」。SKILL.md 末尾还专门有「When to break the rules」6 条 escape hatch，**给模型"合法逃避规则"的出口**——这是少有的「元规则比硬规则更可靠」认知。

### 战略意图

三条信号组合判断**没有商业化意图**：
- README 致谢 *The Adult ADHD Tool Kit*（临床心理学专著），强调「Adapted for how an LLM should respond」——非医疗；
- 开源策略是「fork-friendly」——README 写明怎么 fork 后替换 install URL，鼓励个人化变体扩散；
- 安装手册 17KB / 588 行覆盖 7 平台——纯做分发，**挣不到钱也不指望挣**。

战略性意义：把自己做成 Agent Skill 生态里的「输出风格事实标准」。如果 Anthropic 未来推官方 Output Style（比如 "ADHD Mode"），他要么被收编，要么被吸收——这两种结局都不亏。

## 核心价值提炼

### 创新之处（按新颖度×实用性×可迁移性综合排序）

#### 1. 「同一份 prompt + 跨 7 平台 manifest 分发」架构（新颖度★★★★ 实用性★★★★ 可迁移性★★★★★）

仓库存的不是软件工程，而是一份 canonical prompt（`skills/i-have-adhd/SKILL.md`，142 行）+ 7 套平台 manifest（`.claude-plugin/`、`.codex-plugin/`、`gemini-extension.json`、`.cursor/skills/` 副本、`.agents/plugins/`、Antigravity `plugin.json` 等）的分发体系。Cursor 不读 `skills/` 而读 `.cursor/skills/`，所以 CI（`cursor-skill-sync.yml`）用 `cmp` 守住一致性，失败信息**直接给修复命令**：

```
cmp skills/i-have-adhd/SKILL.md .cursor/skills/i-have-adhd/SKILL.md || {
  echo "::error::.cursor copy is out of sync. Run: cp ..."
  exit 1
}
```

**「distribution reality > DRY」**——副本而非 symlink，因为 Windows / ZIP 不保留 symlink。这是工程人对受众的敬畏，不是 DRY 教条。

#### 2. `disable-model-invocation: true` + 文件 flag 的双层 always-on（新颖度★★★ 实用性★★★★★ 可迁移性★★★★）

Claude Code 没有"always-on plugin"开关。`disable-model-invocation: true` 让模型无法自动把 skill 注入 system prompt，用户必须显式 `/i-have-adhd` 或 `touch ~/.claude/.i-have-adhd-always`。`hooks/always-on.sh` 在 SessionStart 检测文件存在才注入，**任何失败都 `exit 0` 绝不阻塞 session 启动**。这个组合解决了三个问题：
- 用户意图对齐（用户主动开 vs 模型主动用）
- 默认安全（不打开 = 不影响）
- 平台兼容（hook 跨平台报错不致命）

#### 3. 5 维度加权 + release gate 的人类 judge 评测 harness（新颖度★★★★ 实用性★★★★ 可迁移性★★★★★）

`scripts/run_evals.py`（371 行）跑 baseline / candidate / comparator 三个条件，rubric 拆 5 个独立维度：
- correctness 35% / autonomy 25% / actionability 20% / safety 10% / concision 10%

**关键独立**：actionability 与 concision 分开评分——很多评测把这两者混在一起，但 prompt skill 的核心恰恰是「actionability 不靠压缩达成」。

release gate 4 条件串行 fail-fast：
1. 无 blocking findings（blocker=true 不管分数都 fail）
2. correctness 与 safety 不比 baseline 低 0.1 分以上
3. weighted score > baseline
4. 任何公开对比必须用同样 case/model/trial/rubric——**把可复现性写进 gate**

外加：budget 上限 $25/次、unmetered runner 强制 `--allow-unmetered`、可断点续跑（`completed_keys` 四元组去重）、JSONL append + flush（崩溃不丢）。**避免「用 LLM 评 LLM」的循环偏差**。

#### 4. 「Output style」可移植 snippet 模式（新颖度★★★ 实用性★★★★★ 可迁移性★★★★）

INSTALL.md 把所有 always-on 路径汇总，但**只用一段相同的「Output style」markdown 块**（5 维度 12 行 prompt）作为 portable fragment——分发到 Codex / Gemini / Zed / Hermes / Pi / OpenCode / Antigravity 等不支持 SessionStart hook 的 harness。**用户 fork 改一次 SKILL.md，全平台生效**。

#### 5. Pre-send check 反向 prompt（新颖度★★★★ 实用性★★★★ 可迁移性★★★★）

SKILL.md 末尾的「pre-send check」是元层 prompt：
> 如果读者只能读首末两句，是否能知道 (a) 下一步做什么 (b) 发生了什么？

比单纯给规则更能约束行为漂移——是「少即是多」与「正反双向约束」的范式。

#### 6. 「Escape hatch」段落（新颖度★★★ 实用性★★★★ 可迁移性★★★★★）

SKILL.md 第 119-128 行「When to break the rules」明列 6 条打破规则的条件——包括「规则与 harness 系统提示词冲突时，harness 赢」。这解决了 Issue #43（已 close）揭示的「tangent suppression 在错层过滤」问题。任何约束性 prompt 都该有这个段落。

### 可复用的模式与技巧

#### 模式 1: Canonical content + per-platform copy + drift-check workflow
任何「同一份内容要在 N 个加载路径分发」的项目都该用：主文件 + 镜像副本 + CI `cmp` 守门人 + 失败信息内嵌修复命令。

#### 模式 2: Behavior-modifying skill 必须 opt-in
`disable-model-invocation: true` + 文件 flag = 用户控制 vs 模型自主。任何「输出风格 / 合规约束 / 安全过滤」类 skill 都该用——**默认信任用户意图**。

#### 模式 3: Pre-send check 反向约束
prompt 末尾追加「发送前自检：如果只剩首末两句仍能让读者知道下一步做什么 + 发生了什么，就发」。比单纯给规则更能约束行为漂移。

#### 模式 4: 评测 isolation 强制约束
评测 runner 用 `--setting-sources ""` / `--ignore-user-config --ephemeral` 等隔离参数，**注释里点名「避免本 repo 自己的 always-on flag 污染 baseline」**——这是评测方法学的最佳实践。

### 关键设计决策

1. **决策**：「副本 + 守门人」而非 symlink
   - 问题：跨 IDE / ZIP / Windows 加载路径不一致
   - 方案：`.cursor/skills/` 真实副本 + CI `cmp` 守门
   - Trade-off：DRY 让步给分发现实
   - 可迁移性：高

2. **决策**：`disable-model-invocation: true` 强制 opt-in
   - 问题：模型会"自作主张"调用 skill
   - 方案：frontmatter 标志 + always-on hook 检测文件
   - Trade-off：牺牲模型任务自适应换可控副作用边界
   - 可迁移性：高

3. **决策**：always-on 用 POSIX sh + 文件 flag
   - 问题：Claude Code 没有 always-on 开关
   - 方案：`touch ~/.claude/.i-have-adhd-always` + SessionStart hook
   - Trade-off：用户必须知道"魔法文件"，INSTALL.md 已解释
   - 可迁移性：高

4. **决策**：评测 harness 是 release gate 而非评分脚本
   - 问题：如何量化 prompt skill 有效性
   - 方案：5 维度加权 + blocker 必失败 + 4 条件 release gate
   - Trade-off：人工 judge 慢，但避免 LLM-as-judge 循环偏差
   - 可迁移性：极高

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | i-have-adhd | ravila4/claude-adhd-skills | abullard1/claude-bionify | Anthropic 官方 Output Styles |
|------|---------|--------|--------|--------|
| 平台覆盖 | **7 个 CLI** | 仅 Claude Code | 仅本地 terminal | 仅 Claude Code |
| Star 数 | **9,202** | 106 | 16 | N/A |
| 方案层 | prompt 层 | prompt + workflow | terminal 渲染层 | style preset |
| 集成方式 | 单一 Skill + always-on | 多 skill 套件 | ANSI 转义 | 文件配置 |
| 评测 harness | **有（release gate）** | 无 | 无 | 无 |
| 多语 README | 中/英/日 | 仅英文 | 仅英文 | N/A |
| 启发来源 | 临床认知心理学 | 个人工具流 | bionic reading 学术 | 设计哲学 |

### 差异化护城河

- **生态护城河**：9K stars + 17 贡献者 + 7 平台覆盖已是事实标准——竞品要追上需要至少 6 个月社区积累
- **方法学护城河**：评测 harness 是「prompt A/B 测试」领域的现成范本，竞品没有
- **认知科学锚点**：`The Adult ADHD Tool Kit` 是显式参考文献，竞品都只是工具流自述

### 竞争风险

**最可能被替代的维度**：如果 Anthropic 官方未来推 "ADHD / Executive Function" Output Style，本项目差异会被压缩到只剩跨 7 平台 + 评测 harness——这两层**仍是护城河**，所以不至于被淘汰，但明星地位会下降。

**次要威胁**：Claude Code 官方推 output-styles marketplace 后，第三方 plugin 分发难度上升（但作者已通过 `.claude-plugin/marketplace.json` 接入官方 marketplace，所以这是合作而非竞争）。

### 生态定位

「Agent Skill 时代的 dotfiles」——dotfiles 之父是 Zach Holman 那套 shell + vim 配置哲学，i-have-adhd 是把同一思路搬到 Agent Skill 时代：**把个人偏好的 prompt 改出来、装到所有平台、用评测守住质量**。在整个技术生态中，它是**「输出风格层」的事实标准候选**——填补了「prompt engineering 没有 reference implementation」的空白。

## 套利机会分析

- **信息差**：9K stars 已无信息差，但**评测方法和跨平台分发策略**仍是稀缺知识——多数竞品连「跨 2 平台」都没做
- **技术借鉴**：「Pre-send check」反向 prompt + 「release gate」评测范式可直接套到任何 prompt engineering / agent framework 项目
- **生态位**：填补「跨平台 Agent Skill 分发基础设施」空白，仍是空白蓝海
- **趋势判断**：Agent Skill 生态 2026 高速发展，跨平台分发是各家都在建的标准——i-have-adhd 已经被 HN 推上桌，会有更多人 fork，因此趋势上行但不会独家

## 风险与不足

诚实评估：

1. **评测公开结果缺失**：Issue #4（"does this reduce model capability?"）仍 open；rubric 设计存在但没有 baseline vs candidate 公开数字。**对声称改进行为的 prompt 项目，这是显著证据缺口**。在 issue 关掉之前，9K stars 来自社区情绪而非客观证据。
2. **always-on 跨平台兼容性未充分验证**：`plugin-load-check.yml` 只验证 Claude Code 加载。其他 6 个 CLI 的 always-on snippet 是手贴的，INSTALL.md 没说明粘贴后如何验证生效（除「重启 + 看行为」）。
3. **eval cases 偏少**：14 case × 8 category = 每类 1-2 case，统计功效有限；release gate 的 0.1 分阈值在这种小样本下敏感。
4. **`agents/gemini.toml` 与 SKILL.md 内容冗余**但没有像 `cursor-skill-sync.yml` 那样的同步 CI——可以补一个 `agents-sync.yml`。
5. **始终是单作者视角**：「no ADHD diagnosis needed」的卖点意味着 **没有真实 ADHD 用户的对照研究**——价值主张目前完全基于自身 dogfooding 与社区反馈，工程上没有对照组。
6. **依赖未声明的 `npx skills add` 等外部工具**：Cursor 等平台用 `npx skills add` 安装时被自动同步，但前提是用户已经装了 skills CLI；INSTALL.md 文档化但没强制路径。

## 行动建议

- **如果你要用它**：先在 Claude Code 跑 `/i-have-adhd` 验证风格喜不喜欢，再用 `touch ~/.claude/.i-have-adhd-always` 把它开为 always-on。跨平台需求时按 INSTALL.md 顺序贴 portable snippet 到你用的 CLI。**不要直接套全部规则**——它们的「Hard rule / Escape hatch」设计就是为了让你个性化。
- **如果你要学它**：重点看 3 个文件：
  - `skills/i-have-adhd/SKILL.md` — prompt engineering 范本（5 认知事实 → 10 规则 + escape hatch + pre-send check）
  - `scripts/run_evals.py` — prompt A/B 评测 harness 的完整实现
  - `hooks/always-on.sh` — 30 行 POSIX sh，零依赖的设计哲学
- **如果你要 fork 它**：替换 `/skills/i-have-adhd/SKILL.md` 全文即可——它是唯一的 canonical source，所有平台的 manifest 都从它派生。如果你做的是不同风格的 prompt（不是 ADHD），请改 `disable-model-invocation: false` 让模型有更大自由度，并准备相应的 escape hatch 段。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [已收录](https://deepwiki.com/ayghri/i-have-adhd)（last indexed 2026-07-21） |
| Zread.ai | 未收录 |
| 关联论文/书 | [The Adult ADHD Tool Kit](https://www.amazon.com/Adult-ADHD-Tool-Kit-Russell-Ramsay/dp/0365900848) — J. Russell Ramsay & Anthony L. Rostain（作者公开致谢） |
| HN Show 帖 | [news.ycombinator.com/item?id=32436254](https://news.ycombinator.com/item?id=32436254) — 主要增长发动机 |
| 在线 Demo | 无（skill 性质项目，无在线 playground） |

---
name: repo-miner
description: >
  Deep analysis and value mining of GitHub repositories across three dimensions:

  network analysis (author profile, community heat, growth trends), meta
  analysis

  (code stats, commit history, development rhythm), and content analysis
  (architecture,

  innovation, reusable patterns). Use when the user wants to analyze a GitHub
  repo,

  evaluate a project's value, mine a repo for insights, or asks "analyze this
  repo",

  "is this repo worth studying", "what can I learn from this project".
argument-hint: <github-url>
disable-model-invocation: false
model: opus
metadata:
  author: opc
  title: Repo 深度挖掘
  description_zh: |
    GitHub 仓库四维深度分析：网络分析（作者画像、社区热度、增长趋势）、
    外部情报（官方文档/博客、竞品识别）、元分析（代码统计、提交历史、开发节奏）、
    内容分析（架构创新、作者视角价值、竞品交叉对比、设计决策、可复用模式）。
    使用 Orchestrator-Worker 模式，三阶段各自委托 subagent 并行/串行执行，
    主对话仅保留结构化摘要，输出可操作的价值判断和套利机会识别。
  dependencies:
    - gh
    - git
    - tokei
    - jq
  optional-dependencies:
    - onefetch
  version: 1.0.2
  license: MIT
---

# Repo Miner — GitHub 仓库深度挖掘

对 GitHub 仓库进行深度分析，提炼独特价值、创新之处和可利用的模式。
分析结果追求全面、准确、产出实际价值，不惜 token 做深入长时间分析。

**输入：** `$ARGUMENTS`（GitHub URL，格式：`https://github.com/owner/repo`）

## When to Use

- 评估一个 GitHub 项目是否值得深入学习
- 挖掘项目中可复用的架构模式和技术技巧
- 分析项目在生态中的定位和发展潜力
- 寻找信息差套利机会（低关注度高质量项目）
- 做技术选型时的候选方案评估

**Don't use for:**
- 自己正在开发的项目（用 code review 或 project-knowledge-base 更合适）
- 仅需了解 README 概要的简单查询
- 非代码仓库（纯文档、awesome-list 等）

## 架构说明

本 Skill 使用 **Orchestrator-Worker** 模式执行：

```
/repo-miner <url>（主对话 = 编排者）
│
├─ 准备：clone repo，提取变量
│
├─ Phase 1 + Phase 2（并行 Agent 调用）
│   ├─ Agent → 网络分析 → 返回结构化摘要
│   └─ Agent → 元分析   → 返回结构化摘要
│
├─ Phase 3（串行 Agent 调用，接收 Phase 1 结果）
│   └─ Agent → 内容分析 → 返回结构化摘要
│
└─ 主对话：基于三份摘要组装最终报告
```

**为什么这样做：**
- 每个阶段产生大量中间输出（API JSON、git log、代码阅读），留在 subagent 的隔离 context 里
- 主对话只累积三份结构化摘要（约 3000 字），context 保持干净
- Phase 1 和 Phase 2 互相独立，可以并行

## 前置工具检查

开始分析前，验证必需工具：

```bash
which gh && which git && which tokei && which jq && echo "All tools ready"
```

任何工具缺失则**停止分析**并提示用户安装：
- `brew install gh git tokei jq`

可选增强工具（有则用，无则跳过）：
- `onefetch` — 仓库概览卡片（`brew install onefetch`）

## 执行流程

### 准备阶段：Clone 并解析目标（主对话内执行）

从 `$ARGUMENTS` 中提取 GitHub URL（支持 `https://github.com/owner/repo` 格式，也接受简写 `owner/repo`）。

```bash
# 提取 OWNER 和 REPO
# 从 URL: https://github.com/owner/repo → owner/repo
# 从简写: owner/repo → owner/repo

# 完整 clone（需要完整 commit 历史用于元分析）
git clone <url> /tmp/repo-miner-<repo>
```

**提取关键变量**供后续各阶段 Agent 使用：
- `OWNER` — 仓库所有者
- `REPO` — 仓库名
- `LOCAL_PATH` — clone 后的本地路径 `/tmp/repo-miner-<repo>`
- `FULL_NAME` — `owner/repo` 格式
- `GITHUB_URL` — 原始 GitHub URL
- `DEFAULT_BRANCH` — 默认分支名（用于媒体 URL 转换）

```bash
# 获取默认分支名
DEFAULT_BRANCH=$(cd /tmp/repo-miner-<repo> && git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||' || echo "main")
```

#### 确定性数据采集（一次性，供 Phase 1 + Phase 2 共用）

Phase 1（基本数据/作者/star 增长/竞品候选/Top issues/README 媒体）和 Phase 2
（代码统计/提交节奏/演化轨迹/贡献者）里**确定性的 gh + git + tokei 采集**，全部由
一个脚本一次性完成，写成结构化 JSON。**在主对话准备阶段运行一次**（而不是让两个并行
Agent 各跑一遍——否则会抢同一文件且重复触发 gh 限流）：

```bash
# 优先用 skill 自带脚本（发布安装后可独立运行）；本仓库 CI 回退到 src/scripts
FACTS_SCRIPT="${CLAUDE_PLUGIN_ROOT}/scripts/collect_repo_facts.py"
[ -f "$FACTS_SCRIPT" ] || FACTS_SCRIPT="src/scripts/collect_repo_facts.py"
FACTS_JSON=$(python3 "$FACTS_SCRIPT" "$LOCAL_PATH" --full-name "$FULL_NAME")
# 脚本把 JSON 写入 tmp/repo-facts-<repo>.json 并把该路径打印到 stdout
```

脚本只把**路径**打印到 stdout（大体积原始数据落在文件里），主对话 context 保持干净。
把 `FACTS_JSON`（即那个路径）作为变量传给下面两个 Agent，它们各自 Read 自己需要的字段。

---

### Phase 1 + Phase 2（并行启动两个 Agent）

**关键：两个 Agent 调用必须在同一个响应中同时发起，不要串行等待。**

#### Agent 1 — 网络分析

读取 `${CLAUDE_SKILL_DIR}/reference/phase-1-network.md` 获取完整的 Phase 1 分析指令。

使用 Agent 工具启动一个 subagent，prompt 包含：
1. Phase 1 分析指令的完整内容
2. 替换其中的变量：FULL_NAME, OWNER, REPO, GITHUB_URL, LOCAL_PATH, DEFAULT_BRANCH, **FACTS_JSON** 为实际值（FACTS_JSON 是准备阶段采集脚本打印的 JSON 路径）

#### Agent 2 — 元分析

读取 `${CLAUDE_SKILL_DIR}/reference/phase-2-meta.md` 获取完整的 Phase 2 分析指令。

使用 Agent 工具启动一个 subagent，prompt 包含：
1. Phase 2 分析指令的完整内容
2. 替换其中的变量：LOCAL_PATH, FULL_NAME, **FACTS_JSON** 为实际值（FACTS_JSON 是准备阶段采集脚本打印的 JSON 路径）

---

### Phase 3（串行，依赖 Phase 1 结果）

等待 Phase 1 和 Phase 2 都返回后再启动。

读取 `${CLAUDE_SKILL_DIR}/reference/phase-3-content.md` 获取完整的 Phase 3 分析指令。

使用 Agent 工具启动一个 subagent，prompt 包含：
1. Phase 3 分析指令的完整内容
2. 替换其中的变量：LOCAL_PATH, FULL_NAME, GITHUB_URL 为实际值
3. **附加 Phase 1 的关键结果**作为上下文：
   - 作者画像摘要（供 3.2 作者视角分析用）
   - 官方文档/博客采集结果（供 3.2 作者视角分析用）
   - 竞品清单（供 3.5 竞品交叉分析用）
   - 关键 Issue 信号（供 3.3 架构与设计决策、3.6 代码质量评估引用）

---

### 报告组装（主对话内执行）

收到三个 Phase 的结构化结果后，按照下方**最终报告模板**组装完整报告。

组装原则：
- 直接使用各 Phase 返回的分析结论，不要重新推理
- 如果某个 Phase 标注了「跳过」的部分（如无竞品、无官方文档），报告中对应节注明即可
- 报告模板中的维度，从三份 Phase 结果中对应提取
- 项目展示节：直接使用 Phase 1 返回的「项目展示素材」中的图片 markdown，无需再处理 URL
- 如果 Phase 1 标注无展示素材，省略「项目展示」节，不保留空标题

---

## 标题创作规则（H1 = 公众号文章标题，必读）

H1 标题会被下游公众号发布流程**直接拿去当文章标题**。**严禁**输出
`# {repo name} 深度分析报告` / `{repo name} 全方位解读` 这类
泛泛模板 —— 在公众号文章流里完全没有点击竞争力。

**创作准则**：

1. **长度**：≤ 32 字（微信列表页超出会截断）
2. **必须包含其中至少 2 个要素**：
   - 具体数据（star 数、年龄、版本数、贡献者数、性能倍数等）
   - 差异化卖点（"零内存分配"/"事实标准"/"被 N 家抄袭"等）
   - 读者真实关心的问题（"为什么 X 框架都长得像 Y？"等）
   - 故事性反差（"一个人写 12 年"/"被收购前最后一版"等）
3. **格式建议**：主标题 + 「：」+ 副标题（钩子 + 解释）
4. **避免**：感叹号、emoji、过度营销词（震惊/必看/绝了）、全角符号堆砌

**范例**（同样的项目，差的标题 vs 好的标题）：

| 项目 | 差的（禁用） | 好的（参考） |
|---|---|---|
| Gin | Gin 深度分析报告 | 11 年 80K stars：Go 后端框架事实标准 Gin 怎么做到零内存分配 |
| Bun | Bun 全方位解读 | 比 Node 快 3 倍的 Bun：一个 Zig 写的运行时怎么撼动 JS 生态 |
| Manim | Manim 项目分析 | 3Blue1Brown 的可视化引擎 Manim：让数学动画开发从 1 周变成 1 小时 |
| Claude Code | Claude Code 仓库分析 | Anthropic 自研 Claude Code：把 AI 当工程师而不是聊天框 |

标题是发布漏斗的第一关，**这里花 3 分钟思考的收益远大于报告任何
一节多写 500 字**。

---

## 最终报告模板

```markdown
# [按上方创作规则现场生成的标题，不要套用模板]

> GitHub: $GITHUB_URL

## 一句话总结
[一句话概括这个项目最核心的价值]

## 值得关注的理由
[为什么应该关注这个项目，2-3 点]

## 项目展示

[从 Phase 1 返回的「项目展示素材」中选取，直接使用 markdown 图片语法展示]
[每张图片下方附简短说明文字]

[如有视频链接，以链接形式展示]

> 如果 Phase 1 标注"无展示性图片/视频"，省略此节。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | $GITHUB_URL |
| Star / Fork | X / X |
| 代码行数 | X (语言分布) |
| 项目年龄 | X 个月 |
| 开发阶段 | [密集开发/稳定维护/停滞] |
| 贡献模式 | [独立开发/小团队/社区驱动] |
| 热度定位 | [小众精品/中等热度/大众热门] |
| 质量评级 | 代码[X] 文档[X] 测试[X] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景
[作者的领域背景、关键经历，以及这如何塑造了项目的设计选择]

### 问题判断
[作者看到了什么别人没看到或没重视的问题？时机为什么是现在？]

### 解法哲学
[作者明确选择了什么，以及明确不做什么——这往往比 feature 列表更有价值]

### 战略意图
[这个项目在作者/公司更大图景中的位置，是否有商业化路径]

> 如果官方文档/博客数据不足以支撑此节分析，简要说明并跳过细节。

## 核心价值提炼

### 创新之处
[按新颖度×实用性排序的创新点列表]

### 可复用的模式与技巧
[可直接迁移到其他项目的设计模式和代码技巧]

### 关键设计决策
[值得学习的架构选择和 trade-off 分析]

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | [本项目] | [竞品A] | [竞品B] | [竞品C] |
|------|---------|--------|--------|--------|
| [关键维度1] | | | | |
| [关键维度2] | | | | |
| [关键维度3] | | | | |

### 差异化护城河
[这个项目有什么是竞品很难快速复制的]

### 竞争风险
[最可能被哪个竞品替代，在什么情况下]

### 生态定位
[在整个技术生态中扮演什么角色，填补了什么空白]

> 如果无明显竞品，此节注明"无明显竞品，属于细分/新兴领域"。

## 套利机会分析
- **信息差**: [低关注度但高质量？竞品众多但此项目有差异化？]
- **技术借鉴**: [哪些技术可以用到自己的项目？]
- **生态位**: [这个项目填补了什么空白？]
- **趋势判断**: [是否在增长？符合技术趋势？比竞品有没有后发优势？]

## 风险与不足
[诚实评估项目的短板和风险，包括竞争风险]

## 行动建议
- **如果你要用它**: [建议，对比竞品说明什么情况下选它]
- **如果你要学它**: [重点关注哪些文件/模块]
- **如果你要 fork 它**: [可以改进的方向]

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [链接] 或 "未收录" |
| Zread.ai | [链接] 或 "未收录" |
| 关联论文 | [标题](arXiv 链接) 或 "无" |
| 在线 Demo | [链接] 或 "无" |
```

---

## 注意事项

### 分析原则

1. **深层 > 表层** — 不要列 feature list，要提炼 design decisions
2. **判断 > 描述** — 每个发现都要给出"so what"，对读者有什么用
3. **诚实 > 好听** — 发现问题直说，不掩饰 over-engineering 或低质量
4. **可操作 > 抽象** — 输出的结论要能指导下一步行动
5. **对比 > 孤立** — 放在竞品和生态的语境中分析，而不是孤立评价
6. **作者视角 > 旁观者视角** — 尝试理解创造者的世界观，不只是用户视角
7. **引用 > 概括** — 引用具体数据或观点时附原始来源链接，不使用"评价很高""社区反响热烈"等空泛描述

### 异常处理

- `gh` API 限流 → 等待后重试，或减少请求量
- `star-history` 获取失败 → 用 `gh api` stargazers 时间分布代替
- WebFetch 失败 → 使用 JINA AI reader (`https://r.jina.ai/<url>`) 作为备选
- Clone 超时 → 对大仓库使用 `git clone --filter=blob:none` (treeless clone)
- 官方文档/博客不存在 → 跳过相关分析，在报告中标注"无官方文档"
- 竞品搜索无结果 → 跳过竞品分析，在报告中标注"无明显竞品"

### Token 使用策略

- 准备阶段（主对话）：仅 clone 和变量提取，消耗极低
- Phase 1 + Phase 2（并行 subagent）：中间数据留在 subagent context 内，不占主对话
- Phase 3（subagent）：深度代码阅读留在 subagent context 内
- 报告组装（主对话）：仅处理三份结构化摘要
- 如果 Phase 1 判断项目不值得深入，可以提前终止，不再启动 Phase 3

### 补充资源

- 命令速查：[reference/commands-cheatsheet.md](reference/commands-cheatsheet.md)
- Phase 1 详细指令：[reference/phase-1-network.md](reference/phase-1-network.md)
- Phase 2 详细指令：[reference/phase-2-meta.md](reference/phase-2-meta.md)
- Phase 3 详细指令：[reference/phase-3-content.md](reference/phase-3-content.md)

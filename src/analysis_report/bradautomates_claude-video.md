# GitHub 推荐：一个人 2.5 个月写 6036 stars：/watch 如何让 Claude「真看」YouTube 视频

> GitHub: https://github.com/bradautomates/claude-video

## 一句话总结

`/watch` 是一个 Claude Code 斜杠命令 skill，把 YouTube / Loom / 本地视频变成 Claude 多模态可读的「帧 + 对齐 transcript」流——一个人 2.5 个月、11 个 commit、7 个 Python 脚本就做出 6036 stars 的爆款。

## 值得关注的理由

- **prompt-as-product 的样本**：SKILL.md 的修改频次和核心 Python 文件几乎持平（4 次 vs 3 次），整个仓库的 product = 1 个 markdown prompt + 7 个 stdlib Python 脚本，这是 agentic 时代特有的产品形态
- **零依赖视频 RAG 管线**：16×16 灰度 mean-abs-diff 帧去重 + 三种采样策略 + 25MB chunked Whisper，**整套 dedup 算法不依赖 OpenCV/Pillow**，纯 ffmpeg + stdlib
- **跨 50+ agent host 单 SKILL.md 分发**：`SKILL_DIR` 解析从 Read 返回路径而非 env var，规避 `${CLAUDE_SKILL_DIR}` 在 Codex/Cursor/Copilot 上的不兼容
- **真实蓝海**：Anthropic Skills 生态内「video input」细分赛道**目前为空白**，最近似竞品 tapestry-skills 仅提供 transcript

## 项目展示

![Star History Chart](https://api.star-history.com/chart?repos=bradautomates/claude-video&type=date&legend=top-left)

*2.5 个月内 0 → 6036 stars 的爆发曲线，独占性可见一斑*

[README Demo 链接（Rick Astley 经典示例）](https://youtu.be/dQw4w9WgXcQ)

> README 实际嵌入的展示素材以占位符 URL 为主（`<viral-video>` / `<long-thing>`），可用的只有 star-history 图 + 1 个 demo 链接。架构图、dedup 算法可视化均无。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/bradautomates/claude-video |
| Star / Fork / Watcher | 6036 / 721 / 36 |
| 代码行数 | 2,777 行（Python 94.7% / Shell 4.7%）+ 519 行注释 |
| 项目年龄 | 2.5 个月（首发 2026-04-24，最近 push 2026-07-01） |
| 提交数 | 11 个 commit（5 个 release tag） |
| 贡献者 | 1 人（bradautomates 100%，bus factor = 1） |
| 开发阶段 | 低维护（最近 9 天真空，bugfix 收尾） |
| 开发模式 | 职业项目（深夜占比 36.4%，周末 27.3%） |
| 开放 PR | 32 个（远超 11 commits，OSS 协作未跑通） |
| 热度定位 | 大众热门（2.5 月爆发型增长） |
| License | MIT |
| 质量评级 | 代码优秀 / 文档优秀 / 测试充分 / CI 仅 release |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

**Bradley Bonanno**（bradautomates），澳大利亚独立开发者 + 小型工作室主理人，1.7 年 GitHub 账号（2024-10 注册），粉丝 237。主业 **Solaris Automation**（solarisautomation.io）做「端到端 AI 系统」的咨询交付，目标客户：律所 / SaaS / 特许经营等中型企业，固定价 2-6 周项目。副业是 YouTube 频道 **@bradbonanno** 讲 AI 应用。

**双重身份收敛**：作者既是 AI 自动化顾问（客户给 bug screen recording 是日常）又是内容创作者（拆解他人视频找 hook 是日常工作流），两条职业路径共同收敛到「我能不能让 Claude 直接看视频」。

### 问题判断

现有 LLM agent 没有视频输入通道：给定 YouTube URL，agent 只能从标题猜测，或者依赖 transcript 文本（**而字幕丢失 90% 视觉信息**——屏幕录制、PPT、UI bug 视频、hook 分析全部失灵）。Anthropic Skills 生态截至 v0.2.0 没有任何 video skill；通用 `yt-dlp + whisper` 手搓 pipeline 又缺 auto-fps / 场景感知采样 / 帧去重，把 30 分钟视频均匀抽 80 帧等于 token 浪费在「连续相同的幻灯片」上。

**时机判断**：Anthropic Skills 协议刚成熟（SKILL.md frontmatter + `npx skills add` 通用安装器），仓库 0.1.0 时间线（2026-04-24）跟 Skills 生态标准化几乎同步——是**生态窗口期下的快速占位**。

### 解法哲学

- **极简 / 纯 stdlib**：全部 Python 脚本不依赖 requests/groq/openai SDK，连 multipart/form-data 都是手搓的。SKILL.md 自带「no pip install needed」宣传点
- **Unix 哲学组合现成工具**：yt-dlp（下载）+ ffmpeg（抽帧）+ Whisper（转写）+ Claude Read（多模态读取），不自研任何一层
- **prompt-as-product**：SKILL.md 是 product spec，不是文档——它包含完整 Step 0→5 操作流，告诉模型什么时候用 `AskUserQuestion`、什么时候写 `.env`、什么时候 fallback 到 `--no-whisper`、exit code 2/3/4 各意味着什么
- **细节里的「不做什么」**：不做 video understanding 模型（外包给 Claude）、不做结果缓存（trade-off 绝对隐私 vs 重复视频成本）、不做多视频批处理、不做账号/登录支持

### 战略意图

`skills/watch/SKILL.md` / `.claude-plugin/plugin.json` / `.codex-plugin/plugin.json` / README 全部署名 Bradley Bonanno + Solaris Automation + YouTube @bradbonanno——**funnel 设计：skill → 频道订阅 → 顾问咨询**。没有 SaaS/托管版/企业版；商业模型是「内容 + 服务」，不是「工具订阅」。

> 无独立项目主页（homepage_url 为 null），无博客或文档站；README + CHANGELOG + SKILL.md 自含完整文档。

## 核心价值提炼

### 创新之处（按新颖度×实用性排序）

1. **prompt-as-product 范式**：SKILL.md 改频 = 核心代码改频（4 次 vs 3 次），整个 repo 的 product = 1 个 markdown prompt。这是 agentic 时代特有的产品形态，教科书还没写
2. **「detect all candidates → even-sample cap」范式**：0.2.0 修复长视频尾巴 bug 来源（CHANGELOG 显式记录「previous early-exit was faster but kept only the first cuts and dropped the tail of long videos」）——跟 ffmpeg `-frames:v` 行为的反直觉很值得写下来
3. **16×16 灰度 + last-kept 比对 + even-sample 选 first+last 三段式去重管线**：纯 stdlib，无 OpenCV/Pillow/numpy，让 ffmpeg 做 decode + downscale，Python 只做 byte comparison（[frames.py:415-460](../analysis_report/_ref)）
4. **「first run 鼓励 / 后续静默」双 state preflight**：exit code 0/2/3/4 协议 + `SETUP_COMPLETE` 标记，keyless 用户算 ready 不阻断（[setup.py:259-291]）
5. **transcript 容许 partial failure + 跨 chunk timestamp stitching**：分布式系统的常识用在 ASR 分片上，25MB cap 自动 chunk，任一段失败不丢整段（[whisper.py:371-400]）

### 可复用的模式与技巧

1. **「Read 完 SKILL.md 你就知道文件路径 → `SKILL_DIR` 是该路径」的跨 host 分发 pattern**：规避 `${CLAUDE_SKILL_DIR}` 在 Codex/Cursor/Copilot 上的不兼容，单 SKILL.md 在 50+ host 跑通（[SKILL.md:18-37]）
2. **「silent-on-success / actionable-on-failure」preflight**：所有被 LLM tool loop 调用的 CLI 都该这么设计——`os.Exit(0)` 静默 + 3-4 个非零码各对应一种 remediation
3. **「keyless user 算 ready」的 `SETUP_COMPLETE` 标记**：适用于任何「key 是 nice-to-have 不是 must-have」的工具（VCS 装 GitHub CLI 但允许只 SSH；Linter 装 Slack webhook 但允许 print-only）
4. **Cloudflare WAF 规避 UA 硬编码**：`whisper.py:250` 注释直说「Groq sits behind Cloudflare — the default `Python-urllib/3.x` UA trips WAF rule 1010 (403) before auth even runs」
5. **`<viral-video>` README 占位符模式**：README 自带占位符替换 demo，比一次性 demo URL 更可移植
6. **`-skip_frame nokey` keyframe-only 模式**：FFmpeg 老手才知道的「40× 加速帧抽取」技巧，注释直说 「near-instant tier」
7. **`-ss before -i` fast seek vs `-ss after -i` 精确 seek**：区分得清楚是视频处理圈的标准素养

### 关键设计决策

- **帧去重用「last-kept frame 对比」而不是「相邻 frame 对比」**：A,A,B,B,A 序列会保留 A0,B2,A4 三个关键状态（而不是 A0 后所有都被合并成 A），正好覆盖「回到原状态也算 distinct moment」的场景（[frames.py:479-507]）
- **三种采样策略 + 单一样后处理管线**：「detect all → dedup → even-sample」是所有 engine 共享的尾段，唯一区别是 detect 阶段用 keyframe 还是 scene filter。cap 永远作用在 dedup 之后，保证「花预算在 distinct 帧上」（[frames.py:510-682]）
- **path 解析完全 harness-agnostic**：把 `SKILL_DIR` 解析的责任推给模型（它 Read 完 SKILL.md 必然知道文件路径），不依赖任何 env var
- **transcript 双 provider fallback + auto-chunking**：Groq 优先（cheaper, faster），OpenAI 备选；`--whisper openai` 强制；25MB cap 留 1MB 边界；plan_chunks 按 duration 均匀分；最后一段吸收 rounding remainder

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | claude-video (`/watch`) | tapestry-skills | 手搓 yt-dlp + whisper | browser-use/video-use |
|------|---------|--------|--------|--------|
| 视觉帧采样 | ✅ 三策略 + dedup | ❌ 仅 transcript | ❌ 需手写 | ✅ 多模态帧分析 |
| transcript | ✅ 双 provider + auto-chunk | ✅ 自研 ASR | ⚠️ 需自接 Whisper | ❌ |
| 跨 agent host | ✅ 50+ host 单 SKILL.md | ⚠️ Claude Code 为主 | ⚠️ CLI 单独跑 | ⚠️ |
| 零依赖 | ✅ 纯 stdlib | ✅ | ❌ 取决于 ASR 选型 | ❌ |
| 方向 | 消费/理解视频 | 消费（仅文字） | 消费 | 生产（编辑） |
| 社区热度 | 6036 / 721 | 低 | — | 中 |

### 差异化护城河

- **跨 host 分发 + 三档 detail 模式 + dedup 算法** = 「唯一在 Claude 生态里把 video 当一等公民输入」的 skill
- **生态护城河强**：已 commit 到 Anthropic + Codex + Agents 三套 manifest；上 50 个 host 不是 50 份 fork，是一份代码 + 一份 manifest
- **技术护城河中**：ffmpeg/yt-dlp/whisper 都是公开工具，任何人能复刻，但 dedup 算法 + 跨 host 分发 + prompt-as-product 是组合护城河
- **信任护城河弱**：单作者 100% commits，bus factor = 1

### 竞争风险

- **Anthropic 官方 native video input**（如果 Claude 多模态扩展到 video）→ 整个 wrapper 层会塌，single point of failure，发生时间不可控
- **YouTube 改 API / 收费墙** → yt-dlp 维护成本上升
- **Whisper API 涨费** → Groq 仍是 niche provider，可能被 enterprise 用户嫌弃
- **32 个未 review PR（#47 Windows / #31 multi-provider fork / #56 v2）**——都在排队，都没人 review，是社区不健康的明显信号
- **Windows 兼容性**：issue #47 还在 open，README 自身标注 Windows 需要 `python`（非 `python3`）—— winget / path 分隔符 / cp1252 console 都有遗留

### 生态定位

**「video → Claude multimodal input」的 thin wrapper**，类似 Anthropic 官方 Skills 里的 PDF/文档处理类——是工具型 skill 而非产品。围绕这个 skill 作者构建的是**内容 + 顾问**生意，不是 skill 本身。

> 真正的「观看/理解」竞品只有 tapestry-skills（功能更弱，仅 transcript），其他均为「生产」方向——本项目在「AI 消费视频」细分赛道近乎蓝海。

## 套利机会分析

- **信息差**：
  - Anthropic Skills 生态的「video input」空白是**结构性先发**机会，等 Anthropic 自己做 native video 之前 6-12 个月窗口期
  - 「16×16 灰度 mean-abs-diff dedup 在零依赖约束下是 trade-off 甜区」——大多数 video-RAG 项目用 OpenCV 算 pHash/SSIM/CLIP embedding
  - 「SKILL.md 是 product spec 不是 docs」是 agentic 时代的产品形态——市场上 99% 的「Claude skill」还是把 SKILL.md 当 README 写
- **技术借鉴**：
  - `detect all → dedup → even-sample` 三段式直接拿来做自己的产品（screen-recording bug tracker / 监控视频摘要 / 长访谈 RAG）
  - 「`SKILL_DIR` 解析自 Read 返回的路径」比自己做跨 host skill 时直接抄
  - 「first run 鼓励 / 后续静默」双 state preflight 用户体验差异巨大
- **生态位**：
  - 横向扩展：同作者可做 `/listen`（audio 摘要）、`/read-paper`（PDF → Claude）、`/screenshot-watch`（desktop 录屏 watch）——同 SKILL.md 范式 + ffmpeg 复用，单 skill 2 个月交付
  - 纵向加深：video 上加更多 mode（podcast-only ASR / keyframe contact sheet / caption quality scoring）
  - 企业版：收「custom domain 视频 host + 内部 watch skill」的钱（类似 NotebookLM enterprise 模式）
- **趋势判断**：
  - Anthropic Skills 协议标准化 + 50+ agent host 兼容是大方向，早占位 = 早拿品牌
  - Video → multimodal input 需求会爆发（Gemini video / GPT-4o video / Qwen2-VL video 都是新方向）
  - 「单作者 + 跨 host 分发 + 内容驱动商业化」是个人 AI 工具的标准路径：1 个独立开发者 + 1 个 SKILL.md + 1 个 YouTube 频道 + 1 个顾问业务
  - 多模态 RAG 框架会侵蚀 thin wrapper 空间；保持竞争力 = 持续在 dedup 算法 / auto-fps / token 优化上微调领先

## 风险与不足

1. **bus factor = 1**：100% commits 单作者，如果 Brad 弃坑无 collaborator 能接手
2. **32 个 open PR（远超 11 commits）**：维护者 review 速度远低于社区贡献速度 → OSS 协作未跑通 → 重要 issue 都堵在队列里
3. **Windows 兼容性**：#47 还在 open，README 标注 Windows 需要 `python` 非 `python3`
4. **依赖声明缺失**：无 `pyproject.toml` / `requirements.txt`，全部依赖靠运行时 + 文档；新用户首次跑 `python3 setup.py` 才知道要 brew install ffmpeg，第一次体验不丝滑
5. **SKILL.md 是 single point of failure**：改坏一个 prompt 可能让所有 50+ host 的 `/watch` 同时坏；没 PR 流程，全是直推 main
6. **没有 lint 规范**：no ruff / black / mypy；新 contributor 加的 error path 不会被任何 CI 拦截
7. **项目太新**：0.2.0 距首次 release 只 2.5 个月，无 production 长期使用数据；「100 帧 + balanced 默认」是经验值，不是 benchmark
8. **Anthropic native video 是 single point of failure**：发生时整个 wrapper 层价值归零

## 行动建议

### 如果你要用它

- 给 Claude Code / Codex / Cursor 等 agent host 装一次，`/watch <url> [question]` 直接用
- keyless 用户先用 `--no-whisper` 跳过 transcript（只有帧采样 + Read），后续按提示加 Groq key
- 长视频（>30 分钟）先用 `--start / --end` 聚焦到目标段落，避免 100 帧 cap 触发 sparse scan warning
- 三档 detail：`efficient`（默认，适合普通短视频）/ `balanced`（默认 vs. 详细对比的中间档）/ `token-burner`（>20 帧上限）
- **对比竞品选它的情况**：你需要「agent 直接看视频并推理」，而不是「只要 transcript 文本」——后者选 tapestry-skills 更轻

### 如果你要学它

重点关注这些文件，按「产品形态 → 核心算法 → 工程哲学」顺序读：

| 文件 | 学什么 |
|------|-------|
| `skills/watch/SKILL.md`（388 行） | prompt-as-product 范式完整样本——exit code 协议 / AskUserQuestion 用法 / 跨 host 路径解析 / `SKILL_DIR` 模式 |
| `skills/watch/scripts/frames.py`（756 行） | dedup 算法核心：16×16 灰度 mean-abs-diff + last-kept 对比 + detect all → dedup → even-sample 三段式 |
| `skills/watch/scripts/whisper.py`（480 行） | 纯 stdlib multipart + 4 次指数退避 retry + Cloudflare UA 硬编码 + auto-chunking + 容许 partial failure |
| `skills/watch/scripts/setup.py`（364 行） | 「first run 鼓励 / 后续静默」双 state preflight + `SETUP_COMPLETE` 标记 + exit code 协议 |
| `tests/`（10 个 pytest 文件） | ffmpeg-synthesized clips 离线跑、0 network、字节级断言——如何为 IO-heavy 模块写测试 |
| `hooks/scripts/check-setup.sh` | SessionStart hook 一次性 preflight，避免每个 `/watch` 都跑 setup 检查 |
| `AGENTS.md` | 「product is the slash-command-invoked skill, not a CLI」哲学声明 |

### 如果你要 fork 它

- **Windows 兼容性**：#47 排队中没人做，是最直接的贡献窗口
- **multi-provider transcript**：#31 pheistman/claude-watch fork 已有原型，集成进主线是 v2 信号
- **`/watch v2` 路线图**：#56 作者自发预告 0 comments，是抢答窗口
- **结构化输出**：`--json` flag （#25） 让 machine-readable 输出，是 RAG 索引化的前置
- **加 lint / CI 跑测试**：当前零 lint 配置 + 无 test CI，新 contributor 加的代码没有任何 CI 拦截

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [已收录](https://deepwiki.com/bradautomates/claude-video)（2026-05-04 indexed） |
| Zread.ai | 未确认收录（403 拒绝） |
| 关联论文 | 无（应用层 skill，无学术论文） |
| 在线 Demo | 无独立 playground；需在 Claude Code/Codex/claude.ai 等 50+ host 内安装使用 |
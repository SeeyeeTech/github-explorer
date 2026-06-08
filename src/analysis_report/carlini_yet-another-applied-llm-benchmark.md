# 为什么该写自己的 LLM benchmark：Carlini 用 100 道真题反刷榜

> GitHub: https://github.com/carlini/yet-another-applied-llm-benchmark

## 一句话总结

顶级 AI 安全研究者 Nicholas Carlini 把「我过去一年真实问过 LLM 的问题」攒成约 100 道可自动判分的测试，用一套优雅的 `>>` 管道 DSL 串起「出题→模型执行→Docker 真跑代码→断言/视觉模型判分」，回答的不是「哪个模型更强」，而是「这个模型对我到底有没有用」——它真正的产品是一套人人可复制的「反刷榜私有 benchmark」方法论。

## 值得关注的理由

1. **顶级研究者的方法论范本**：作者是对抗样本 Carlini-Wagner 攻击、LLM 训练数据记忆化提取的提出者，常年公开批判「benchmark 被污染/被刷榜」。这个项目是其立场的代码化身，思想密度远超其 6000 行的代码量。
2. **一份值得读源码学设计的极简实现**：框架核心只有约 2400 行 Python，却包含一个被 Simon Willison 专门盛赞「优雅」的内嵌 DSL，和一套教科书级的「不可信代码沙箱执行」骨架。
3. **可直接迁移的工程范式**：`>>` 运算符重载 DSL、生成器回溯校验、一次性容器沙箱、test-as-code 题库——每一个都能搬到自己的评测/抽取/agent 系统里。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/carlini/yet-another-applied-llm-benchmark |
| Star / Fork | 1,058 / 80 |
| 代码行数 | 6,369（Python 99%；框架仅 ~2,447 行，117 道题占文件主体） |
| License | GPL-3.0 |
| 项目年龄 | 29.7 个月（首次提交 2023-12，已停更于 2025-04） |
| 开发阶段 | 已放弃 / 停更（近 365 天 0 commit） |
| 贡献模式 | 个人主导（Carlini 占 73.7%，14 名贡献者多为零星补 provider 适配） |
| 热度定位 | 中等热度（影响力远超代码量与 star 数） |
| 质量评级 | 代码「中」 文档「中-高」 测试「无框架自测」 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Nicholas Carlini（GitHub bio 只有一句「I break things」），ML 安全/对抗样本领域权威——Carlini-Wagner 攻击、LLM 训练数据记忆化与提取攻击的提出者，长期 Google Brain→DeepMind，2025 年转入 Anthropic。粉丝 2277、42 个公开仓库，本项目是其 star 最高的代表作。其它仓库（`pycallcc`、`intel-4004-in-4004-bytes-of-c` 等）都是「小而精的实验性 hack」，风格高度一致。作者权威性极高，立场由学术声誉直接背书。

### 问题判断

他要回答的不是「哪个模型更强」，而是极度个人化的「这个模型对我（一个真实用 LLM 写代码的人）有没有用」。在他看来现有方案都不够：学术 benchmark 是「homework 范式」（few-shot 刷标准题型，与日常脱节）；公开榜单天然会被对抗性优化和训练集污染（这是安全研究者的本能判断）；花式 prompt engineering（「给你十万小费/深呼吸一步步想」）扭曲了真实信号。他的主张直白——「我就想打字提问、直接拿到对的答案」。

### 解法哲学

四条写进 README 的硬约束就是他的评测世界观：① 必须**机械可验证**（哪怕这排除了大量真实用例）；② 必须**跑得快**；③ **构造期不许拿 LLM 调题**（否则就是过拟合到模型）；④ **passing 才有意义，failing 不说明什么**——一种刻意的非对称设计：宁可漏报也不误报能力。并且明确「这不是学术工具、不做 leaderboard、不要拿去写论文比模型」。

### 战略意图

表面是个人工具，实质是**思想布道的代码化身**。它的影响力（被 Simon Willison、Latent Space 反复引用）远超它作为一份 100 题测试集的价值——因为它给出的是一套人人可复制的「私有 benchmark」方法论，对冲公开榜单失效。这与作者长年的公开立场完全一致；代价（覆盖偏闭源 API、停更后仍被当参考榜）他主动接受，因为他要传的是「自己测自己在乎的事」这个观念。

## 核心价值提炼

### 创新之处

1. **`>>` 内嵌数据流 DSL（Python magic method 做管道）**：用 `__rshift__`/`__rrshift__` 把「and then」管道编码进语法，`a >> b` 编译成 `ThenNode`，一行表达式即一道题。新颖度 5/5 · 实用性 5/5 · 可迁移性 4/5。
2. **生成器回溯求值（「存在一条通过路径即判过」）**：每个节点的 `__call__` 是生成器，`yield` 多个候选输出，`ThenNode` 做笛卡尔积遍历——把 LLM 输出歧义（多代码块、判分抖动）当搜索空间穷举，从根上压低 false negative，呼应「failing 不该因为我的疏忽」。新颖度 4/5 · 实用性 4/5 · 可迁移性 4/5。
3. **多层判分混用：精确断言 + 真执行 + LLM-as-judge + 视觉模型判分**：「画美国国旗→跑 C→让视觉模型认这是什么旗→断言含 USA」一条线把生成-执行-跨模态验证串起来，信条是「verification is usually easier than generation」。新颖度 4/5 · 实用性 5/5 · 可迁移性 4/5。
4. **Docker 真执行判分（而非只判文本）**：代码真的编译、真的跑、真的取回 stdout 再判，是与几乎所有同类 benchmark 的本质区别。新颖度 3/5 · 实用性 5/5 · 可迁移性 5/5。

### 可复用的模式与技巧

1. **运算符重载内嵌 DSL（`__rshift__` 管道）**：把领域流程写成接近自然语言的 Python 表达式——适合评测框架、ETL、查询构造等可组合步骤。
2. **生成器回溯校验**：节点 yield 多候选、上游笛卡尔积、「任一通过即过」——适合判定本身带不确定性、想消化抽取/解析歧义的校验流水线。
3. **一次性容器沙箱原语**：内存 tar 注入文件 + `exec_run` + `signal.alarm(20)` 硬超时 + 后台线程异步销毁 + docker/podman 双后端——任何要执行不可信/LLM 生成代码的系统的标准骨架。
4. **薄 adapter + 统一缓存/重试包装的多模型抽象**：每厂商一个 15–62 行 `make_request`，外层统一加 pickle 缓存（重复跑近乎免费）、3 次重试、超时——横评多 LLM 的工具通用（路由建议用注册表而非字符串匹配）。
5. **test-as-code 插件目录**：一文件一用例 + 模块级 `DESCRIPTION`/`TAGS` + importlib 反射收集——可插拔规则/题库/插件体系的轻量范式。
6. **把「危险开关」编码进命名**：放弃沙箱的开关被命名为 `I_HAVE_BLIND_FAITH_IN_LLMS_AND_AM_OKAY_WITH_THEM_BRICKING_MY_MACHINE...`，用 API 命名传递威胁模型，让误用变得刺眼。

### 关键设计决策

- **DSL + 回溯求值**：问题是要让多步、可分支的评测流程加题成本低到几行，同时消化 LLM 输出的多种解读；方案是 magic method 管道 + 生成器笛卡尔积「宽进严判」。Trade-off：可读性极高、加题极易，但 magic method 有认知门槛、类型靠约定不透明。可迁移性高。
- **沙箱真执行**：必须真跑 LLM 生成的代码但不能把宿主机交给模型；方案是 Docker/podman 双后端 + tar 注入 + SIGALRM 超时 + 异步销毁，甚至支持 PTY 交互式会话（让模型像 agent 一样多轮操作 sqlite）。Trade-off：拿到真实执行 + 隔离 + 可复现，代价是依赖容器、CI 不友好。可迁移性高。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | 本项目 | openai/evals | lm-evaluation-harness | Chatbot Arena |
|------|--------|--------------|------------------------|----------------|
| Stars | 1,058 | ~18.6k | ~12.9k | ~39.5k |
| 范式 | 个人真实用例 + 真执行 | YAML + LLM-as-judge | 学术 few-shot 标准题 | 众包人类盲评 |
| 评分 | 自动（断言/执行/视觉） | LLM 评审 | 标准化打分 | 人工投票 |
| 可复现 | 到 git commit | 中 | 高 | 低（众包） |
| 立场 | 反刷榜、拒绝 leaderboard | 中立框架 | 学术标准 | 正是被批判对象 |

### 差异化护城河

「个人真实用例 + 可自动评分 + 顶级研究者反刷榜背书」三位一体；技术上 `>>` DSL + 真执行 + 多层判分的组合优雅度业内罕见。真正壁垒是**方法论与立场**（人人可复制一套私有反 gaming benchmark）而非代码本身——这反而难被超越，因为它不争同一条赛道。

### 竞争风险

已停更，新模型（o1/DeepSeek）社区只能干等（issue #22/#28 开着没人接）；覆盖偏闭源 API、对开源模型不友好（#16）；100 题样本小、统计意义弱（作者自己也承认）；无 CI、无 release，作为「能跑的工具」上手有门槛；社区想要 leaderboard 被哲学性拒绝（#10），存在持续张力。

### 生态定位

不是要取代任何框架的「另一个 benchmark」，而是一个**反 benchmark 的 benchmark**——示范作用 > 工具作用。它在生态里的位置是「思想样板 + DSL 设计参考实现」，而非长期维护的评测基础设施。

## 套利机会分析

- **信息差**：代码维度无套利（已放弃、依赖旧模型 API），但**内容/选题套利价值高**——「为什么你该写自己的 benchmark」是 LLM 评测领域被广泛认同却少有人系统讲透的反共识洞见，由顶级研究者背书，传播力强。
- **技术借鉴**：`>>` DSL + 生成器回溯、Docker 沙箱判分骨架、test-as-code 反射加载，可直接迁移到自己的 agent 评测 / 在线判题 / 数据校验系统。
- **生态位**：填补「个人真实任务 + 反刷榜方法论」的空白，与拼规模的学术框架正交。
- **趋势判断**：模型选型从「看公开榜」转向「测自己在乎的任务」是明确趋势，这个项目是该趋势最早、最有思想的样板。

## 风险与不足

- **研究型一次性代码**：字符串匹配路由（`'gpt' in name` 易误命中）、裸 `except: pass/continue` 遍布、podman 路径 `time.sleep` 时序 hack、类型靠约定不透明、`main.py` 末尾 `raise "Unreachable"`（字符串 raise）。
- **无框架自测、无 CI、无 release、无 tag**：坏题在 importlib 加载时静默跳过，无回归防护；使用者只能按 commit/日期对齐，无法锁定稳定版本。
- **已停更 + 题库过时**：题目停在 2025-04 之前的模型能力假设上，部分可能已被新模型刷穿、区分度下降；内置参考 leaderboard 不含后来的模型。
- **样本与覆盖局限**：100 题统计意义弱，且偏闭源 API。

## 行动建议

- **如果你要用它**：当「方法论范本 / 自建评测脚手架」用，价值高；当「现成排行榜」用，已过时——别照搬它的分数，要 fork 出来换上你自己在乎的真实任务。
- **如果你要学它**：重点读 `evaluator.py`（877 行，DSL 全部节点 + 回溯求值引擎，项目心脏）和 `docker_controller.py`（269 行，沙箱执行 + PTY 交互）。学的是评测设计思路与沙箱判分工程。
- **如果你要 fork 它**：把字符串 if-elif 路由换成注册表/映射、给框架本身补单元测试、把宽泛 `except` 收窄为结构化错误，再换上覆盖新模型与开源模型的题库。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/carlini/yet-another-applied-llm-benchmark（已收录） |
| Zread.ai | 探测返回 403，未能确认收录 |
| 作者原文 | [My benchmark for large language models](https://nicholas.carlini.com/writing/2024/my-benchmark-for-large-language-models.html) |
| 深度访谈 | [Latent Space: Why you should write your own LLM benchmarks](https://www.latent.space/p/carlini) ·[Simon Willison 评介](https://simonwillison.net/2024/Nov/6/yet-another-applied-llm-benchmark/) |
| 在线 Demo | 无（无托管 leaderboard） |

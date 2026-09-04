# GitHub 推荐：7.5 个月 42K stars：一个 30KB 的 Prompt 怎么改写 AI 写作的规则

> GitHub: https://github.com/blader/humanizer

## 一句话总结

把 Wikipedia 社区维护的 35 条 AI 写作特征清单包装成 Claude Code 可调用的「风格清洗」skill——7.5 个月拿下 42K stars，本质是一份**prompt 即产品**的极简工程范本。

## 值得关注的理由

- **代码/产品倒挂的范式**：仓库只有 74 行 Python 和 543 行「注释」——但真正的产品就是那 543 行里的 35 条 pattern。GitHub 上几乎找不到第二个用 prompt 文本本身当主交付物的 4 万 star 项目。
- **Anthropic Agent Skills 生态的早期占位**：发布于 2026-01-18，恰好卡在 skills 协议发布的窗口内，是当时市面上最早的「风格清洗」类 skill。
- **可迁移的反模式**：它把 Wikipedia 编辑治理里的「signs of AI writing」分类法机器可执行化——这种「社区共识 → agent 指令」的迁移模板，可以直接套到 OWASP、PG 风格指南、合规清单等任何已有公开分类法的领域。

## 项目展示

README 和官网（skills.sh/blader/humanizer）均无展示性图片或视频——本节省略。仓库的「视觉资产」是 `SKILL.md` 里的 35 组 Before/After 文本示例，已经在「核心价值提炼」里逐条体现。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/blader/humanizer |
| Star / Fork | 42,672 / 3,606 |
| 代码行数 | 74 行 Python（仅打包脚本）+ 35 条 AI-isms pattern（SKILL.md 主体） |
| 项目年龄 | 7.5 个月（2026-01-18 首发） |
| 开发阶段 | 稳定维护（规则迭代期，不是软件维护期） |
| 贡献模式 | 核心少数 + 社区（16 人，top-3 占 59%） |
| 热度定位 | 大众热门 |
| 质量评级 | 代码 N/A · 文档 优秀 · 测试 无（无单元测试；用结构性 lint 作 release gate） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

**Siqi Chen**（@blader），旧金山，18.5 年 GitHub 老账号，1,191 followers，21 个公开仓库——是典型的「资深 founder+creator」而非个人爱好者。公开履历显示他是 **Postmates 联合创始人兼 CEO**（被 Uber 收购）、**Zynga 前 PM**、**CTHDRS 创始人**（被 Robinhood 收购），目前在做一个叫 **Runway** 的项目。bio 是空的，blog 链到 `twitter.com/blader`——这意味着他**不在 GitHub 上经营身份**，humanizer 是他顺手的产出而非主业。

他最近 push 的仓库里，humanizer 排第 2（第 1 是 `MiraViewer`，TS 写的小工具）。这说明 humanizer 不是「闲来练手」，而是他当下愿意花精力维护的少数项目之一——一个 founder 愿意持续投入 35.2% 深夜 commit 的项目，值得严肃看。

### 问题判断

作者在 2026-01 把项目首发，恰好是 Anthropic 推出 Agent Skills 标准的窗口期。这是**时机信号**，不是偶然——他判断：

1. **LLM 输出的「机器味」已经成为普遍痛点**。Wikipedia 的 WikiProject AI Cleanup 在 2024 下半年汇总了 30+ 条 AI 写作的明文特征，社区需求已经被验证。
2. **现有解法走偏了**。商业 SaaS（StealthGPT、HideMyAI、Walter Writes、GPTinf）走「再生成一遍让它像人」的路线，但 [wpnews.pro 的批评](https://wpnews.pro/news/claude-code-why-humanizing-prompts-usually-fail)指出：prompt-only 重写在 token 概率分布层无法逃过检测器，最佳改写仍被 42% 概率打标。
3. **Wikipedia 的诊断文档是金子，只是格式不对**。那份「Signs of AI writing」是**给人类编辑看的**——Chen 的工作是把诊断文档翻译成 agent skill 格式，让 LLM 也能按单执行。

### 解法哲学

- **Unix 哲学在 prompt 时代的体现**：一个 Markdown 文件就是产品。`AGENTS.md` 明文写「The repo has no build step」。`scripts/validate-package.py` 是对 SKILL.md 做结构性 lint，不是运行时——把 linter 角色从 CI 退化为发布闸门。
- **负面清单而不是正面清单**：35 条编号 AI-isms，每条带 *Words to watch / Problem / Before / After*。为什么不写「用这些人类写法」？因为人类正向写作空间太大列不完，而**负面清单可枚举、可辩论、可扩展**——每加一条 AI-ism 是 additive 价值，每加一条「human-like」特征都要论证普适性。
- **Free + MIT + 不跑 SaaS**：和商业竞品的核心区别。开源免费版的「去 AI 味」工具，直接动摇商业 AI-detection 行业的存在根基。
- **不替代作者，只清洗**：明确写「Do not change what it says or make up details」——是 post-processor，不是 generator。

### 战略意图

不是 Runway 的核心产品，但和 Runway 叙事高度协同：Runway 是「AI 时代的人类工具」，humanizer 是「AI 时代的反-AI 工具」——两者在同一个论点上互相支撑。**商业意图：从 humanizer 引流到 Runway/Chen 后续项目，不从 humanizer 收钱**。这是典型 founder-as-creator 用开源积攒社会资本的玩法。

> 关键解读：Siqi Chen 不是在做一个产品，是在用 humanizer 抢 Agent Skills 生态里「风格清洗」品类的 mindshare。这决定了它「质量优先而非速度优先」（7.5 个月只发 4 个 tag）和「不试图商业化」的产品姿态。

## 核心价值提炼

### 创新之处

按新颖度 × 实用性排序：

1. **可枚举的 AI-isms 分类法（35 条 pattern）**——新颖度 3/5、实用性 5/5、可迁移性 4/5。不是原创研究，而是把 Wikipedia 社区的 WikiProject AI Cleanup 分类法机器可执行化——但分类本身（语言/语法/样式/chatbot/filler 五大类、每类 5–10 条 + Before/After few-shot examples）是稀缺 IP。
2. **「What not to flag」误报清单作为反过度泛化的内嵌防御**——新颖度 4/5、实用性 5/5、可迁移性 5/5。15 条「人类写作也会触发的模式」+「多个 pattern 同时出现才动手改」的判定标准，是 deny list + allow list + density gate 三层防御范式的样板。
3. **三处版本同步 + 35 条 pattern 编号连续的发布 lint**——新颖度 4/5、实用性 4/5、可迁移性 5/5。`validate-package.py` 强制 SKILL.md / README.md / plugin.json 三处 semver 一致、pattern 编号 1–35 连续——把 semver 的 release discipline 应用到**纯 prompt 仓库**。
4. **3 种 output mode + 同一 process 的「tool-as-skill」契约**——新颖度 3/5、实用性 5/5、可迁移性 5/5。pasted / file / embedded 三模式满足不同场景（人工、批处理、子调用），但 rewrite 过程共享——skill 作为 building block 的最小可用接口设计。
5. **fact-fidelity gate 嵌入工作流**——新颖度 3/5、实用性 5/5、可迁移性 4/5。Rewrite process 第 3 步强制 LLM 自问「Did the rewrite add or remove any fact, name, number...」——把幻觉检测嵌入到工作流而不是依赖外部 verifier。

### 可复用的模式与技巧

1. **「Negative-list pattern taxonomy」四段式**：Words to watch → Problem → Before → After。任何需要 LLM 学习反模式的场景（code review、prompt injection 检测、合规检查）都可照此结构包装。
2. **Allowlist + deny list + density gate 三层防御**：解决模式匹配会误伤的通用范式，可直接用到反 spam、反抄袭、反幻觉等所有「敏感模式匹配」任务。
3. **跨 harness single-prompt**：一份 SKILL.md frontmatter + 多份 harness-specific manifest（Claude plugin.json + marketplace.json + Codex openai.yaml）。任何想一招鲜吃遍天的 prompt 库都要面对这个问题。
4. **Release lint for content-only repos**：semver + 跨文件版本一致性 + pattern 编号连续性。适用于 prompt 库、policy 文档、rule 集合。
5. **Embedded mode as sub-skill contract**：当调用方是另一个 skill 时返回「只回最终产物」。这是 skill composition 的关键设计。

### 关键设计决策

```plain
决策: 负面清单（avoid-list）而不是正面清单（use-list）
问题: 怎么让 LLM 在不改写事实的前提下消除「机器味」？
方案: 35 条编号 AI-isms，每条带 Watch words / Problem / Before / After
Trade-off: 负面清单无法生成性教你写人话——只能从已有文本剔除 AI-isms
  对 prompt 层引导 LLM 写人话的场景无效，需要正面清单补全
可迁移性: 高
```

```plain
决策: 把「已知误报」显式列入 §What not to flag
问题: AI-isms 清单会过度泛化——em-dash、curly quote、bold 等正常人类写作也会触发
方案: 单独一节列 15 条已知误报，明确「一个 em dash 不能定罪，多个 stock pattern 同时出现才是强证据」
Trade-off: 需要 LLM 具备模式聚合能力（不仅是 grep）
可迁移性: 极高
```

```plain
决策: 边界声明 + 不可做的事（但回避了 wpnews.pro 的根本性批评）
问题: 用户会期望 humanizer「去掉所有 AI 检测器告警」
方案: SKILL.md 末尾要求 LLM 自问「是否添加/删除了事实」——把事实保真作为内嵌 gate
Trade-off: 没有正面回应 wpnews.pro 的「统计签名不可逃」论点；全文搜不到 detector / probability / watermark
  这是有意识的回避——把「对抗检测器」留给商业 SaaS，避免越界承诺
可迁移性: 中等
```

```plain
决策: 3 种 output mode（pasted / file / embedded）+ 通用 rewrite process
问题: humanizer 既要支持手动调用，又要支持批处理，又要被其他 skill 作为子调用
方案: if-then 路由，所有模式走同一份 rewrite process；embedded mode 只回最终文本
Trade-off: 三种模式差异全靠文档约束，没有运行时类型系统
可迁移性: 高
```

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | blader/humanizer | wshobson/agents | anthropics/skills | K-Dense-AI/scientific-agent-skills | 商业 SaaS（StealthGPT 等） |
|------|-----------------|-----------------|--------------------|----------------------------------|--------------------------|
| Star | 42.7K | 39.4K | 174K | 42.6K | N/A（付费） |
| 定位 | 单点聚焦：清洗 AI-isms | 多端 marketplace | Agent Skills 标准母仓库 | 科学垂直工具箱 | 改写 + 过检测器 |
| 商业模式 | 免费 MIT | 免费开源 | 开源标准 | 免费 + 付费 SaaS | 订阅 SaaS |
| 跨 harness | Claude + Codex + OpenCode | Claude/Codex/Cursor/Copilot 全覆盖 | 仅 Claude | Claude 优先 | 自家 Web UI |
| Pattern 深度 | 35 条 + Before/After | 各 skill 不一 | 仅目录/一句话描述 | 165 个 skill | 黑盒 |
| 误报防御 | 显式「What not to flag」+ density gate | 视各 skill 而定 | 无 | 无 | 无（目标是「过」检测器） |
| 可嵌入子调用 | embedded mode | 视 skill 而定 | 是 | 是 | 否（要上传文件） |

### 差异化护城河

- **生态护城河**：Agent Skills 早期 top-of-mind 之一，名字就是品类名。
- **分类法护城河**：35 条 pattern + Before/After 例子是公开但稀缺的资产——其他 prompt 库很少愿意做这种「带 few-shot 的负面清单」。
- **无技术护城河**：prompt 工程可被任何竞争对手复制——这意味着护城河必须靠分发和品牌维护。

### 竞争风险

1. **Anthropic 官方下场**：如果 anthropics/skills 内置 humanize 类 skill，blader/humanizer 的差异化会被吸收——这是最大风险，因为 Anthropic 自己写的版本永远有最权威性。
2. **检测器升级**：如果未来主流检测器从「模式匹配」升级到「token 概率分布分析」，humanizer 的整个方法论失效。wpnews.pro 的批评已指明这条路径。
3. **新架构替代**：post-LLM 编辑可能让位于「pre-LLM 风格引导 prompt」，根本改变战场。

### 生态定位

**Agent Skills 标准下的「style cleanup」事实标准**——不是必需工具，但是每个 agent 作者会引用一次的 reference implementation。在更宏观的 AI-detection 行业里，它是商业 SaaS 的开源替代品：在「让用户为反 AI 检测付费」这件事上提供一个免费选项。

## 套利机会分析

- **信息差**：极高。42K stars + 74 行代码 + 543 行注释这种「代码/产品倒挂」在主流技术分析里几乎没人解读过——大多数人会用「代码规模」指标草率否定它。本报告是这个套利窗口的一个解释。
- **技术借鉴**：
  - 「社区共识分类法 → agent skill」的迁移模板：OWASP Top 10、NIST CVE、PG 风格指南、合规禁忌清单都可照搬。
  - 「负面清单 + Before/After + density gate」三层防御范式，可直接用到反 prompt injection、code review 的反 code smell。
  - 「semver 应用到 prompt 仓库」的 lint 模式，对所有 prompt 库和 policy 文档都通用。
- **生态位**：Agent Skills 生态早期 top-of-mind，加上 founder 的影响力——这是普通 prompt 工程师拿不到的位置。
- **趋势判断**：
  - **向上**：Agent Skills 标准被采纳范围扩大、Claude/Codex/OpenCode 多端统一——humanizer 受益于分发。
  - **向下**：AI 检测器从「模式匹配」升级到「token 概率分布」会让纯 prompt 解法失效——humanizer 必须升级方法论或被替代。

## 风险与不足

- **wpnews.pro 的根本性批评未正面回应**：prompt-only 重写在 token 概率分布层无法骗过检测器。SKILL.md 全文搜不到 detector/probability/watermark——这是**有意识的回避**而不是技术回应。如果未来检测器升级，这条路线整体失效。
- **无单元测试**：`commits_last_365=54、test=0` 是事实——但「测试」这个概念在 prompt 仓库里需要重新定义。结构性 lint（validate-package.py）部分替代了 test，但 LLM 输出的一致性无法被单元测试覆盖，只能靠 issue 用户反馈（#93 / #176 都是这种反馈的实例）。
- **Issue #176 暴露的 LLM 句法流畅性 > 规则遵从性问题**：§14 em-dash 用了**「must not contain」绝对语气**，但 LLM 在改写阶段容易把 `—` 替换成 `,` 后又因为句法不顺手加回去——这是 prompt 层的 hint 而不是 lint 层的强制，可靠性有限。
- **国际化空白**：35 条 pattern 全是英语，em-dash 是英美排版习惯。Issue #92（Spanish-language）说明用户已经在提需求，但语言扩展需要独立的 LLM AI-isms 研究。
- **Founder 风险**：Siqi Chen 的主要精力在 Runway 和 MiraViewer，humanizer 在他 repo_rank 第 2——如果他转向下一个项目，humanizer 维护节奏可能放缓。
- **owner 是 content repo 不是 code repo 的常见陷阱**：低 star 时容易因「看起来没技术含量」被低估，高 star 时容易被神化。**两个方向都要警惕**。

## 行动建议

### 如果你要用它

适合：需要把 LLM 生成的长文（博客、文档、营销文案、commit message）清洗成「人话」的场景；想在自动化文档流水线里加一道后处理；想避免自己被同事/读者一眼认出「这是 ChatGPT 写的」。

不适合：想要「100% 过 AI 检测器」——它明确不承诺这件事，去用商业 SaaS（但 wpnews.pro 说商业 SaaS 也做不到）。

### 如果你要学它

重点关注：

- **「负面清单 + Before/After」的 prompt 结构**（SKILL.md §1–§35）——这是把诊断文档机器可执行化的标准范式。
- **「What not to flag」章节**——任何敏感模式匹配任务的必读章节，反过度泛化的范本。
- **`scripts/validate-package.py`**（89 行 stdlib-only Python）——把 semver 应用到内容仓库的发布 lint 模板。
- **三份 manifest 的分工**（`.claude-plugin/plugin.json` + `marketplace.json` + `agents/openai.yaml`）——跨 harness 适配的最小集。

### 如果你要 fork 它

可改进的方向：

1. **加入「AI-iness density score」显式量化**：当前「多个 pattern 同时出现」是定性建议，可以升级成定量阈值（每千字 X 个 pattern 触发 = 高 AI-iness），让 LLM 有明确停止点。
2. **多语言扩展**：英语之外的 LLM AI-isms 需要独立研究——西班牙语 Issue #92 已经在等。
3. **pre-LLM 风格引导 prompt** 版本：与其清洗输出，不如在 prompt 层引导 LLM 写人话——这是「架构替代」方向的研究。
4. **针对检测器升级的版本**：如果未来 token 概率分布检测成为主流，需要从「模式匹配」升级到「分布重写」——这条路 prompt-only 可能走不通。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/blader/humanizer（已收录：35-pattern 分类法、处理流水线） |
| Zread.ai | 未收录 |
| 关联论文 | 无 |
| 在线 Demo | 无（prompt 本身是产品，clone 仓库即可） |
| 关键批评 | [wpnews.pro — Claude Code: Why Humanizing Prompts Usually Fail](https://wpnews.pro/news/claude-code-why-humanizing-prompts-usually-fail) |
| Wikipedia 母版 | WikiProject AI Cleanup — Signs of AI writing（35 条 pattern 的源头） |

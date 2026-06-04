# 78K star、9.6 年仍活的渗透测试字典：PayloadsAllTheThings 凭什么成为红队「圣经」

> GitHub: <https://github.com/swisskyrepo/payloadsallthethings>

## 一句话总结
一个把「渗透测试可执行 payload」沉淀为 7 万行 markdown + 9.6 年持续 PR 的「内容型开源」项目——它不是软件，而是一本「以 PR 为出版单位、以 markdownlint 为编辑」的活体渗透字典。

## 值得关注的理由
- **数据反常**：78,181 star、17,036 fork、333 贡献者，但真实代码只有 2,096 行、注释/文档却 54,442 行（26:1 倒挂）——这本身就是一个值得研究的「内容型开源」范式。
- **9.6 年仍活**：v1.0 → v4.2 共 7 个 tag 跨度 9.6 年、近 1 个月 0 提交但社区 PR 持续流入、月度 commit 与 Hacktoberfest 强相关——这是「个人 IP 矩阵化」运营的典型样本。
- **可迁移的内容运营方法论**：模板化写作 + 占位符语言 + markdownlint 自动化 + 跨项目跳转分家——这套「反软件工程」的内容治理模式，可直接迁移到企业内部知识库、API 规范库、行业最佳实践库。

## 项目展示

![PayloadsAllTheThings Banner](https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/.github/banner.png)
*项目官方 Banner——`PayloadsAllTheThings` 的视觉门面*

![Contributors Rock](https://contrib.rocks/image?repo=swisskyrepo/PayloadsAllTheThings&max=36)
*contrib.rocks 自动生成——333 位贡献者头像墙，是 PATT 社区力量的最直观体现*

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | <https://github.com/swisskyrepo/payloadsallthethings> |
| Star / Fork | 78,181 / 17,036（fork 率 21.8%，远超行业典型 10%） |
| 真实代码行数 | 2,096 行（Python 76% 是误读——tokei 把 markdown 围栏代码算成 Python） |
| 注释/文档行数 | 54,442（注释/代码 ≈ 26:1，本质是知识库） |
| 项目年龄 | 115.6 个月（9.6 年，2016-10-18 创建） |
| 总 commit | 2,185 次（≈ 19/月） |
| 最近 commit | 2026-04-22（最近 30 天 0 提交，处于静默维护期） |
| 贡献者 | 333 人（Top 占比 47.5%，核心少数 + 社区协作） |
| 依赖管理 | 全空（无 setup.py/requirements.txt，无运行时依赖） |
| 开发阶段 | 低维护（master HEAD 仍流动，但 7 个 tag 跨度 9.6 年，v4.2 后停发版） |
| 开发模式 | 职业项目（27% 周末提交、18% 深夜提交，长期 9.6 年稳定节奏 + 商业赞助） |
| 热度定位 | 大众热门（bug bounty 圈「圣经」级，含 17 个 GitHub topic：pentest/payload/bypass/bugbounty/cheatsheet/hacktoberfest……） |
| 质量评级 | 形式化质量(优秀) · 内容质量(优秀) · 治理质量(优秀) · 深度(中等——是字典不是教科书) |

## 作者视角：为什么存在这个项目

### 创始人/作者背景
**Swissky（swisskyrepo）**——11 年账号（2015-04 起）的欧洲独立 Red Teamer，自签名 "Red Team Operator & Bug Hunter"。13 个公开 repo **全部围绕渗透/红队/漏洞赏金**垂直深耕：PayloadsAllTheThings（Web 字典）→ InternalAllTheThings（内网/AD）→ HardwareAllTheThings（硬件/HID）→ SSRFmap/GraphQLmap（专项工具）——形成**「Web → 内网 → 硬件」的攻击链知识矩阵**。3 家商业赞助商（SerpApi / ProjectDiscovery / Vaadata）打通独立研究员靠赞助 + 工具商业化的路径。

### 问题判断
2016 年之前的渗透测试学习者面临的信息困境是：
- **碎片化**：payload 散落在博客、Twitter、CTF writeups、个人笔记中
- **不可执行**：很多博客只贴「概念」，不贴「可直接扔进 Burp 的字符串」
- **语境缺失**：缺乏「何时用、怎么用、用了之后看什么响应」
- **时效性黑洞**：WAF 绕过每年迭代，但缺乏统一的「持续更新机制」

Swissky 的解法极其朴素：**用 GitHub 当作 CMS，每个漏洞 = 一个目录，目录里放「工具列表 + 方法论步骤 + 可执行 payload + 实验场链接 + 参考文献」**——任何人可以 PR 补充。

### 解法哲学
- **简单 vs 功能完整** → 选「简单且可复制粘贴」——payload 字符串就是文档本身，不写教程
- **广度 vs 深度** → 选「广度」——70+ 漏洞类型 × 8+ 编程语言 × 28+ reverse shell 语言
- **开放 vs 封闭** → 选「完全开放」——MIT 协议 + 模板化贡献 + Hacktoberfest 拉新
- **明确不做什么** → PATT 内**只放 Web 漏洞 + 核心方法论**；AD/内网/提权类主动迁出到 InternalAllTheThings，**保留跳转而不删除入口**

### 战略意图
- **个人 IP 矩阵化**：13 个 repo 互引引流——PATT 是入口（78K⭐），其他是分领域纵深
- **社区杠杆**：Hacktoberfest 每年 10 月的 PR 洪流（2019/2020/2021/2022 连续 4 年 10 月 commit 暴增 73→84→125→107）抵消日常维护负担
- **商业化路径**：FUNDING.yml 列出 GitHub Sponsors / Ko-fi / Buy Me a Coffee；3 家赞助商都是安全工具生态头部——靠「独立研究员 + 赞助 + 工具」而非「开源转 SaaS」

## 核心价值提炼

### 创新之处

1. **「模板化写作」把「内容贡献」降维成填空题**（新颖 4/5 · 实用 5/5 · 可迁移 5/5）
   `_template_vuln` 模板强制四段式（Summary / Tools / Methodology / Labs / References），配合 `.markdownlint.json` 自动化校验 + CI 拦截（`.github/workflows/check-markdown.yml`）。任何懂这个漏洞的人能在 30 分钟产出格式合格文档。**这是 PATT 能 9.6 年维持 333 贡献者的根本机制。**

2. **占位符语言（DSL for 安全文档）**（新颖 4/5 · 实用 5/5 · 可迁移 5/5）
   CONTRIBUTING.md 里规定 `[ATTACKER.DOMAIN.TLD]` / `10.10.10.10` / `P@ssw0rd` / `DC01` 等占位符——payload 一律消毒，读者扫一眼就知道「哪些要替换」。本质是**领域特定语言（DSL）思想在文档领域的应用**，极大降低「复制粘贴误用」的法律/技术风险。

3. **Intruder 字典「场景化命名」**（新颖 3/5 · 实用 5/5 · 可迁移 5/5）
   `SQL Injection/Intruder/` 下 21 个字典按「场景+技术+引擎」三维命名：`Auth_Bypass.txt` / `FUZZDB_MSSQL-WHERE_Time.txt` / `Generic_TimeBased.txt` / `payloads-sql-blind-MySQL-INSERT`——比「一股脑 fuzz-all.txt」实用得多，可直接被 Burp Intruder「按字典选」模式消费。

4. **跨项目「分家」治理：保留入口 + 跳转 = 渐进式迁移**（新颖 4/5 · 实用 4/5 · 可迁移 5/5）
   `Methodology and Resources/Active Directory Attack.md` 已完全是 InternalAllTheThings 的跳转链接列表——Swissky 不删除 PATT 内入口，而是**保留跳转以维持根目录「完整」导航 + 引导读者到更专业子项目 + 反向引流帮新项目冷启动**。比「删除/重定向」更优雅。

5. **「内容型开源」反软件工程治理范式**（新颖 5/5 · 实用 4/5 · 可迁移 5/5）
   7 个 tag / 9.6 年（v4.2 后停发版，以 master HEAD 为活版）+ 无 CHANGELOG + 无 setup.py/requirements.txt + 无单元测试 + 无 release workflow——**靠「模板 + 规范 + 社区」维持质量，而非「CI 流水线」**。这是给所有「知识型/文档型」开源项目的范式启示。

### 可复用的模式与技巧
- **四段式 README 模板**：Tools / Methodology / Labs / References 适用于任何「知识集合型」项目（其他安全主题、API 设计模式、数据库性能调优清单）
- **场景化字典命名**：任何 fuzz 项目、字典收集项目都应避免「一个超大字典」，按场景拆成多个小字典
- **占位符 DSL**：任何含可执行片段的文档（IaC 模板、SQL 案例、API 调用样例）都可定义自己的占位符语言
- **渐进式跨项目分家**：模块化拆分时，保留旧入口 + 跳转比删除/重定向更优雅
- **markdownlint 作为内容 CI**：把「什么样的 PR 能合」从人工 review 降级为可自动化校验
- **Hacktoberfest 杠杆**：每年 10 月开放贡献窗口，PR 集中合并可抵消日常维护负担

### 关键设计决策

1. **决策**：按漏洞类型组织根目录（70+ 子目录如 `XSS Injection`/`SQL Injection`/`SSRF`），而非按攻击阶段
   - **问题**：渗透知识如何分类才能「可检索、可扩展、抗重构」？
   - **方案**：每个漏洞 = 一个目录，目录内统一结构（README + Intruder + Images + Files）
   - **Trade-off**：牺牲「按攻击阶段串讲」的连贯性，换取**新增漏洞 = 新增目录、其他不动**的零摩擦扩展性
   - **可迁移性**：高——任何「按主题垂直深耕」的知识库都适用

2. **决策**：每个漏洞目录固定「四件套」内部结构（README.md + Intruders/ + Images/ + Files/）
   - **问题**：如何让 333 位贡献者产出「格式一致」的文档？
   - **方案**：模板化强制 + markdownlint 自动化校验
   - **Trade-off**：贡献者的「风格自由度」被压缩，换取「读者跨漏洞无缝切换」的可读性
   - **可迁移性**：高

3. **决策**：核心维护团队收敛到 3 人（Swissky + p0dalirius + ZANNI），其余 330+ 走社区 PR
   - **问题**：如何平衡「治理集中度」与「社区参与面」？
   - **方案**：核心 3 人定模板/规则，社区按规则填空
   - **Trade-off**：核心维护者「无法脱身」——Swissky 一旦长期停更，整个项目节奏会下台阶
   - **可迁移性**：中

4. **决策**：v4.2 后停止打 tag，以 master HEAD 为「活版」
   - **问题**：7 个 tag 跨度 9.6 年，semver 标签名不符实
   - **方案**：放弃 semver，承认「这是一本活体出版物而非 API」
   - **Trade-off**：下游使用者无法 pin 版本，换取「零版本管理负担」 + 「读者始终读到最新」
   - **可迁移性**：高（任何内容型项目都应明确「我们不是软件，别假装有版本」）

5. **决策**：关闭 Issue 通道（open_issues=0），议题通过 PR/Discussion 流转
   - **问题**：7.8 万 star 项目的 Issue 区极易变成「support center」
   - **方案**：议题 = 改文档 = 走 PR；纯讨论 = Discussion
   - **Trade-off**：用户无法在 Issue 区提「bug」或「建议」，但治理重心清晰
   - **可迁移性**：高

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | PayloadsAllTheThings | HackTricks | OWASP Cheat Sheet Series | InternalAllTheThings（姐妹） |
|------|---------|--------|--------|--------|
| 首要价值 | 可执行 payload 集合 | 长篇方法论 | 防御视角规范 | 内网/AD 渗透字典 |
| Payload 密度 | 极高（每节都有可执行字符串） | 较低（以概念/命令为主） | 极少（防御代码片段） | 高（PowerShell/Mimikatz 命令） |
| 覆盖广度 | 70+ 漏洞 × 8+ 语言 | 几乎所有渗透方法论 | Web/移动/云各类防御 | 内网/AD/Windows/Linux |
| 深度 | 中（每漏洞点到为止） | 高（每方法论 5k-10k 字长文） | 中（每防御模式一篇） | 中（命令密集） |
| 更新机制 | 社区 PR 持续 | 主要作者维护 | 委员会评审 | 社区 PR |
| 视角 | 攻击者 | 攻击者 | 防御者 | 攻击者 |
| 典型读者 | Bug Hunter / Web Pentester | 想学方法论的新人 | 企业蓝队/合规 | Red Teamer |
| Stars | 78K | 10K+ | 30K+ | 2.2K |

### 差异化护城河
- **生态护城河**：333 贡献者 + Hacktoberfest 持续输入 = 竞品难以复制的「社区网络效应」
- **信任护城河**：9.6 年沉淀 + 3 家商业赞助商（SerpApi/ProjectDiscovery/Vaadata）= bug bounty 圈「事实标准」
- **覆盖广度护城河**：70+ 漏洞 × 8+ 编程语言 × 28+ reverse shell 语言 = 单点深度项目（DefaultCreds/patator）无法匹敌
- **可执行性护城河**：payload 字符串就是文档本身，可直接复制粘贴——HackTricks（长方法论）和 OWASP（防御视角）做不到

### 竞争风险
- **最可能被替代的方式**：HackTricks 持续扩展 Web 漏洞章节 + Burp 官方推出 Intruder 字典市场，可能从「广度+可执行性」两端夹击
- **作者风险**：Swissky 长期停更（最近 1 个月 0 提交）会触发节奏下台阶——但 v4.2 后已经出现「低维护期」信号
- **品类风险**：AI 工具（如 LLM 辅助 fuzz/Payload 生成）正在从「字典查询」转向「实时生成」——若 WAF 绕过变成 LLM 实时事，PATT 的「持续 PR 更新」价值会下降

### 生态定位
在整个安全知识生态中，PATT 扮演**「红队速查字典」**的角色——它填补了「HackTricks 的深度」和「OWASP 的防御视角」之间的空白：**「我手里有 Burp、有 curl、有 ncat，遇到 XSS 怎么打、SSRF 怎么绕、reverse shell 怎么弹？」** 这是几乎所有 bug bounty / 渗透测试 / 红队评估每天 80% 的工作流。

## 套利机会分析

- **信息差**：78K star 已是行业顶流，**不是被低估的潜力股**——但「反软件工程的内容运营方法论」对中文技术圈（企业内部安全知识库、合规清单库、行业最佳实践库）**几乎未被认知**，是技术写作 + 项目治理维度的「信息差套利」
- **技术借鉴**：
  - `_template_vuln` + `markdownlint` + `CONTRIBUTING.md` 三件套 → 可直接做企业内部「安全知识库模板」
  - 占位符语言 → 可迁移到所有「含可执行片段的文档」（IaC、SQL 案例、API 调用样例）
  - 跨项目跳转分家 → 企业知识库「按业务线分仓但保留总入口」的标准模式
- **生态位**：在 bug bounty / 红队评估圈，**PATT 已是「字典事实标准」**——新进入者无法撼动其位
- **趋势判断**：项目本身**进入低维护稳态**（master HEAD 仍流动但增速放缓），**作为「内容运营方法论」的范式**反而正被其他领域（API 规范、运维 SOP、合规清单）借鉴——这是「项目本身 → 项目方法论」的**第二增长曲线**

## 风险与不足

- **目录大小写不一致**：`XSS Injection` vs `XSS injection`、`Upload` vs `Upload insecure files` 并存，每个相关条目在两个目录里被独立编辑——形成可见的「双维护」成本
- **CHANGELOG 缺失**：v4.2 后停发版，读者无法快速了解「近期新增了哪些漏洞」，需要翻 git log
- **搜索性能瓶颈**：54k 行 markdown 用 mkdocs material 内置搜索，索引体积已接近静态搜索的舒适上限
- **作者单点风险**：Swissky 749/2185 = 34.3% 提交 + 核心治理集中度 47.5%，长期停更会引发节奏下台阶
- **时效性 vs 文档固化张力**：WAF 绕过每年新增 5-10 类，但 README 又要保持稳定可读——这种「内容时效 + 文档固化」双重需求未在结构层解决
- **AI 时代冲击**：LLM 实时生成 payload + fuzz 向量正在挑战「字典」的存在价值——长期看 PATT 需要向「结构化知识 + 教学化」方向演进而非「字典累积」

## 行动建议

- **如果你要用它**：
  - **渗透测试 / Bug Bounty 工作流首选字典**——遇到不熟的漏洞类型，先翻 PATT 对应目录的 Methodology 段，再扫 Intruder 字典丢 Burp
  - **不要 pin 到 tag**——以 master HEAD 为「持续最新版」（v4.2 之后已停发版）
  - **必读 CONTRIBUTING.md**——理解占位符语言（`[ATTACKER.DOMAIN.TLD]` / `10.10.10.10` / `P@ssw0rd`），避免「忘记替换」的法律/技术风险
  - **配合 HackTricks + OWASP 三件套**——PATT（字典）+ HackTricks（教科书）+ OWASP（防御手册）三者结合覆盖 Web 渗透全部知识需求

- **如果你要学它**：
  - **重点关注 `Methodology and Resources/` 目录**——`Active Directory Attack.md` 246 changes 是项目皇冠条目，揭示「横向方法论」如何集中沉淀
  - **抽看 `_template_vuln/`**——39 行模板揭示 Swissky 对「合格 PATT 文档」的极简定义
  - **阅读 `CONTRIBUTING.md`**——60 行有效内容信息密度极高，是「内容质量工程化」的范本
  - **对比 `XSS Injection/` `SQL Injection/` `Server Side Template Injection/` 三个目录**——验证「四件套」内部结构的一致性

- **如果你要 fork 它**：
  - **可改进方向**：
    1. 把「分家」做彻底——按漏洞类型拆到独立 repo（Web/AD/Cloud），主仓只做导航
    2. 引入**结构化 payload 数据库**（SQLite/PostgreSQL）替代纯 markdown，支持复杂检索
    3. 接入 **LLM 辅助贡献**——AI 生成初版 markdown + 人工 review，突破社区 PR 节奏瓶颈
    4. 增加**版本化的 Intruder 字典**——按「针对 WAF X 的 v3 绕过集」打 tag，方便实战选型
    5. 修复目录大小写不一致（重命名 + git mv + .gitattributes 强制小写）

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 已建立索引（[DeepWiki 入口](https://deepwiki.com/swisskyrepo/payloadsallthethings)，页面仍在加载） |
| Zread.ai | 未收录（HTTP 403） |
| 关联论文 | 无（实操知识库，非学术项目） |
| 在线 Demo | <https://swisskyrepo.github.io/PayloadsAllTheThings/>（GitHub Pages 镜像，mkdocs material 主题） |

# 9.5 年 78K stars：一个人把渗透测试字典做到赛博武器库的事实标准

> GitHub: https://github.com/swisskyrepo/payloadsallthethings

## 一句话总结

PayloadsAllTheThings（PATT）是 Red Team 工程师 Swissky 用 9.5 年持续维护的 **Web 渗透测试 payload 速查手册**——65+ 攻击类别、21K 行 Markdown、5.4 万行字典、67 个 Burp Intruder 词表、333 位贡献者，是 Burp 生态「带语境字典」的事实标准，而 SecLists（71K stars）只能做「裸字典」。

## 值得关注的理由

- **垂直赛道绝对头部**：78,136 stars 是同品类 HackTricks（11K）的 7 倍，OWASP CheatSheetSeries（32K）的 2.4 倍，SecLists（71K）虽然 star 接近但它只解决「有什么」，PATT 解决「怎么用、为什么用」——在 Bug Bounty / 红队工具链里是绕不开的参考手册。
- **「文档即工具」 的工程化范本**：每个漏洞子目录都是 `README.md + Intruder/ + Images/ + Files/` 四件套，payload 可以从 Web 端一键复制到 Burp Intruder，wiki 和工具链焊死在同一目录——这是 95% 的内容仓库都做不到的实战性。
- **「家族母品牌」 运营策略**：同作者维护 InternalAllTheThings（AD/内网 2.2K stars）、HardwareAllTheThings（IoT 0.9K）、SSRFmap（3.5K）、GraphQLmap（1.6K）——一个独立研究者用统一后缀 + 互相引用 + 共享学习资源，构建渗透测试社区的「个人品牌矩阵」。

## 项目展示

![PATT 项目 banner：项目 Logo + 标题，蓝色背景](https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/.github/banner.png)

*仓库顶部唯一一张展示图——项目 Logo + Payload All The Things 标题。README 主体是 53 行目录树，无其他装饰，靠内容本身说服 78K 用户。*

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/swisskyrepo/payloadsallthethings |
| Star / Fork / Watch | 78,136 / 17,027 / 1,961 |
| 代码行数 | 2,096 行真代码 + 54,442 行 payload/字典 + 5,599 行空行（主语言 Python 61%，ASP.NET 9%，XSL 7%） |
| 项目年龄 | 116 个月（2016-10-18 → 2026-04-22，约 9 年半） |
| 攻击类别 | 65+ 个一级子目录，142 个 .md 文件，21,527 行文档 |
| 开发阶段 | 稳定维护期（年 commit 从 2020 峰值 402 降到 2025 的 98，但 2026-04 仍在持续更新） |
| 贡献模式 | 独立作者驱动 + 社区 PR（Swissky 一人 1,341/2,185 = 61.4%，Top 5 占 72%） |
| 热度定位 | 大众热门，垂直赛道头部 |
| 质量评级 | 文档 5/5（README 100% 遵循模板），CI/CD 5/5（增量 markdownlint + mkdocs 部署），payload 可复现性 5/5（字符串即跑），国际化 3/5（无翻译版本） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

**swisskyrepo**（昵称 Swissky），Red Team Operator & Bug Hunter，GitHub 2015-04 注册、10,487 粉丝、13 个公开仓库。从作品矩阵看是 **「AllTheThings 家族」 品牌运营者**——PayloadsAllTheThings（Web 渗透）、InternalAllTheThings（AD/内网 2.2K）、HardwareAllTheThings（IoT 0.9K），外加配套自动化工具 SSRFmap（3.5K）、GraphQLmap（1.6K）。这意味着他**同时是文档作者和工具作者**——工具的实战发现反哺文档，文档的普及反哺工具的下载，形成「工具 + 文档」双轨闭环，这是普通 awesome-list 维护者做不到的。

### 问题判断

Swissky 在 2017 年前后集中遇到两个具体痛点：

1. **Bug Bounty 实战时 payload 散落各处**——多年实战中，SQLi 注入串、XSS WAF bypass、SSRF cloud metadata 路径都分散在 Burp 历史、博客收藏夹、私人笔记里，新人上手需要重新收集。
2. **「复制即跑」 的工具集几乎不存在**——现成 wordlist（SecLists）有，但 wordlist 不带「解释」，光给字符串没场景说明；HackTricks 给方法论但颗粒度不到「某类具体 CVE 该打什么字符串」。

PATT 选择的差异化路线：**比 wordlist 多一层「可读上下文」，比 HackTricks 多一层「开箱即用的字符串」**。

### 解法哲学

从 README、CONTRIBUTING、PR 历史可以提炼出 4 条非妥协原则：

1. **「无依赖可复现」**：拒绝过 ReverseSSH 合并到 Reverse Shell cheatsheet 的 PR（需要 Go 编译步骤）——「复制粘贴就能在 Burp 用」 是底线。
2. **「白盒净化」**：CONTRIBUTING 强制所有 PoC 使用占位符（`id`/`whoami`/`P@ssw0rd`/`DC01`/`[ATTACKER.DOMAIN.TLD]`），不写实战恶意 payload——这种「以学术/合法为名」的设计让仓库**长期保持 GitHub TOS 合规，得以稳定运营 9.5 年不被封禁**。
3. **Burp-friendly**：每个漏洞子目录自带 .txt 词表，直接拖进 Intruder 就能跑——把「研究文档」和「日常工具链」 缝合。
4. **「家族化」**：显式引导 Internal/Hardware 子站，把 PATT 定位为「安全知识中央仓」而不是孤立 cheat sheet。

### 战略意图

PATT 已成为 Swissky 个人品牌的「招牌仓库」——与 10K+ 粉丝、SerpApi/ProjectDiscovery/VAADATA 三家赞助商形成正循环。Issues 全面关闭导流到 Discussion/PR 是**反向强化「只接受增量补完 PR」 的运营纪律**，这种纪律反过来保护品牌。家族化布局是**反 fork 策略**——如果 PATT 被 fork 走，Internal/Hardware 子站不会跟着走。

## 核心价值提炼

### 创新之处

1. **「payload 净化」占位符规范（14/15）**：用 `[ATTACKER.DOMAIN.TLD]`、`P@ssw0rd`、`DC01` 替代真实值——这是仓库**长期不被 GitHub 限制**的根本原因，比「加 DISCLAIMER 含糊免责」 高明得多。
2. **README + Intruder + Images + Files 四件套同目录（13/15）**：HackTricks 没有 .txt，SecLists 没有 .md 解释，OWASP CheatSheetSeries 没有可上传的 PoC 文件——**PATT 唯一把「文档/工具输入/复现素材」三种形态缝合**。
3. **Methodology and Resources 单立但保留占位的家族导航（9/15）**：Web 应用攻击 → 红队内部网 → 硬件 IoT，「家族」 靠它衔接。
4. **`_LEARNING_AND_SOCIALS/` 隐性附录（13/15）**：把「认识的人 + 读过的书 + 看的 YouTube」 当作仓库的「附录」，新人 clone 仓库顺便 clone 了一个「人脉图」。
5. **「无依赖可复现」的内容纪律（13/15）**：这是 9.5 年保持高信号/低噪声比的根本。
6. **Wayback Machine 主动归档外部参考链接（Phase 2 实证）**：维护者主动用 web.archive.org 备份每个外部参考链接，防止链接腐烂——其他同类项目极少做到这种细致维护。

### 可复用的模式与技巧

| 模式 | 描述 | 适用场景 |
|---|---|---|
| **「_template_vuln/ + 四件套」** | 1 个极简 README 模板（4 个 H2）+ 4 类同级文件类型 | 任何「分类目录 + 内容贡献」型知识库 |
| **「占位符规范」+ DISCLAIMER** | 用固定字符串替代真实值，降低法律风险 | 安全研究/渗透/恶意软件分析/红队文档 |
| **「家族母品牌」** | 多仓共享前缀 + 互相导流 | 个人 IP 矩阵、机构多产品线 |
| **「Burp-friendly 文档」** | 文档旁边直接放工具可用的 .txt | 安全/QA/性能测试类文档 |
| **「_附录区」** | 下划线前缀的次要内容，排序后排到末尾 | README 类项目（GitHub 事实标准） |
| **「增量 lint」** | PR 时只对 changed-files 做 markdownlint | 大型 monorepo |
| **mkdocs material + code.copy + git-revision-date-localized** | 一键复制 + 显示内容新鲜度 | 文档类项目 mkdocs 标配三件套 |
| **「Sponsors 表格 + 家族子站互引」** | README 显式列赞助商 + 母站导流 | 开源可持续运营成熟模板 |

### 关键设计决策

#### 决策 1:用「_template_vuln/」做架构抽象
- **问题**:65+ 个攻击类别由不同贡献者补充，如何保持结构一致？
- **方案**:1 个 README.md 模板，只列 Summary + Tools + Methodology + Labs + References 五段（H2），其余自由发挥。
- **Trade-off**:模板极简但内容靠贡献者填充，质量参差。
- **可迁移性**:**高**——任何「分章节 + 子条目」知识库可复用。

#### 决策 2: README + Intruder + Images + Files 四件套
- **问题**:文档如何直接喂给 Burp 工具链？
- **方案**:同一目录下，文档是 .md，工具输入是 .txt，素材是 .png/.svg/.php shell——每条 payload 都有 3 个状态可访问（阅读/工具调用/复现）。
- **Trade-off**:贡献者必须熟悉 3-4 种文件类型，门槛高。
- **可迁移性**:**中**——依赖 Burp 工具文化，非通用。

#### 决策 3:关闭 Issues 反向强化运营纪律
- **问题**:Wiki 类仓库被大量「求助类」无关注入淹没。
- **方案**:Issues 全局关闭，导流到 Discussion + PR，把「建议/反馈」与「内容提交」分到两个渠道。
- **Trade-off**:社区反馈通道变窄（PR 积压 17 个），对外部贡献者不够友好。
- **可迁移性**:**高**——任何被噪声淹没的 wiki 类项目可借鉴。

#### 决策 4:增量 markdownlint CI
- **问题**:142 个 .md 文件全量 lint 慢且 PR 噪音大。
- **方案**:`tj-actions/changed-files` 只对 PR changed files 做 lint，版本钉死 `DavidAnson/markdownlint-cli2-action:v20`。
- **Trade-off**:略增加 workflow 复杂度。
- **可迁移性**:**高**——大型文档仓库通用。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | **PATT** | HackTricks | SecLists | OWASP CheatSheet | atomic-red-team | Payloader (中文) |
|------|---------|-----------|----------|------------------|-----------------|------------------|
| Stars | 78,136 | 11,481 | 71,297 | 32,152 | 10,300+ | 398 |
| 核心交付 | 65+ 攻击类别 payload+ 解释 | 攻击方法论 | wordlist | 防御 CheatSheet | ATT&CK 原子测试 | 中文渗透 payload |
| 工具链集成 | Burp Intruder 直接用 | 概念为主 | ffuf/wfuzz 集成 | 概念为主 | invoke-artifact | 自有 UI |
| 语言深度 | 多语言（PHP/Java/Python/Node/Elixir/OGNL/SpEL） | 偏通用 | N/A | 偏概念 | 偏 PowerShell/bash | 国内常见框架 |
| 前沿覆盖 | Prompt Injection / XS-Leak / SSPP | 较全 | N/A | 较稳 | ATT&CK 框架 | 国内向 |
| 维护者 | 一主多核（Swissky 61%） | 多核分散 | 社区 | OWASP 基金会 | Red Canary 团队 | 个人 |

### 差异化护城河

**唯一同时做到 65+ 攻击类别 + .txt wordlist + .md 解释 + 可上传 PoC 文件的仓库**。其他竞品各有侧重但没有交叉覆盖：

- **技术护城河**:四件套目录 + 占位符规范 + Wayback Machine 主动归档——这些工程化细节很难短期复制。
- **生态护城河**:Swissky 的 AllTheThings 家族矩阵 + 配套工具（SSRFmap/GraphQLmap）形成跨仓生态。
- **信任护城河**:9.5 年持续维护、SerpApi/ProjectDiscovery/VAADATA 三家行业头部赞助商背书、Oct 2021 单月 125 commits 的社区动员力。

### 竞争风险

- **最可能被替代的风险**:**HackTricks**（如果它加入 .txt 词表 + 简化 contribution 流程）。但目前两者是「工具与说明书」互补关系而非互替——PATT 用户必然交叉使用 HackTricks。
- **细分市场风险**:中文圈 **Payloader** 等小项目在语言层本地化（ThinkPHP、Fastjson、Shiro 反序列化）——PATT 不做中文翻译会持续把这部分用户让出去。
- **前沿覆盖风险**:AI/LLM 攻击面（Prompt Injection、SSPP）目前 PATT 跟得紧，但 OpenAI/Anthropic 自己的红队工具可能比 PATT 更新更快。

### 生态定位

PATT 处于**「攻击面广度 + 字符串级可执行性」**的生态位——HackTricks 是方法论深度、SecLists 是字典广度、OWASP 是防御视角，PATT 唯一把「可执行」和「广度」同时拉到顶。在 Bug Bounty / 红队工作流里，它的真实角色是 **「渗透测试的 cheat sheet + Burp 工具的 wordlist 源」**——比 Burp 自带的 wordlist 全、比 HackTricks 实战、比 SecLists 有语境。

> **核心判断**:无明显可替代的单一竞品，但 HackTricks 是最强互补，Payloader 是中文用户最直接对标。

## 套利机会分析

- **信息差**:78K stars 已经不「低估」了，但**中文圈 PATT 仍是被低估的优质资源**——大多数国内安全从业者只用 HackTricks 不读 PATT，PATT 的 65+ 攻击类别 + Burp-friendly 设计对中文 Bug Bounty 猎人是金矿。
- **技术借鉴**:占位符规范、四件套目录、增量 lint、Wayback Machine 主动归档——这些模式可以**直接迁移到任何「分类目录型知识库」项目**（不限于安全），比如企业内部知识库、开源项目文档、API 文档等。
- **生态位**:在 Bug Bounty 工具链中，PATT 是 **「研究 → 实战」 的桥梁**——它填补了「高质量 wordlist（SecLists）」 和「高质量方法论（HackTricks）」 之间的中间地带。
- **趋势判断**:**仍在增长**（从 2022-04 的 50K 到 2026-06 的 78K，4 年 +28K），符合 Bug Bounty 行业持续扩张 + AI 时代新攻击面（Prompt Injection）的双重趋势；相比 SecLists（71K）它的语境化优势在 GenAI 时代反而更突出。

## 风险与不足

- **维护瓶颈**:Swissky 一人 61% 提交，单点风险显著——如果他退出，仓库活跃度会断崖式下跌（参照 README 关闭后 PR 积压 17 个）。
- **架构债**:存在目录重命名不规范（`XSS Injection` vs `XSS injection`、`Upload` vs `Upload Insecure Files` vs `Upload insecure files`），导致同一类目分散在 3 个目录中，属于 v2 → v3 重构期的不完全迁移。
- **Methodology and Resources 内 30+ 个 moved to InternalAllTheThings 占位文件**:严重影响新人体验，应该迁完就删目录或保留完整内容，**不要保留「空壳」**。
- **Issues 关闭 + 17 个 open PR**:社区反馈通道变窄，对外部贡献者不够友好。
- **没有自动化测试任何 payload 是否仍能跑**:历史 payload 失效后无人察觉，只能靠用户报告。理想是「每周跑一遍靶场验证关键 payload 仍能复现」。
- **国际化缺失**:无翻译版本，中文/日文/西班牙语用户门槛高。
- **法律/合规风险**:内容包含漏洞利用代码与绕过 WAF 技巧，**仅供合法授权测试**（DISCLAIMER.md 单独成文）——任何企业引用前需内部法务审核。

## 行动建议

### 如果你要用它
- **新人入门**:从 `SQL Injection/`、`XSS Injection/`、`Server Side Request Forgery/` 三个高频类别读起，每个都是「四件套」 标准范本。
- **实战渗透**:`Intruder/*.txt` 直接拖进 Burp Intruder，配合 `Files/` 下的 PoC 文件做验证。
- **前沿追踪**:关注 `Prompt Injection/`、`XS-Leaks/`、`Server Side Prototype Pollution` 这些 2023 年后新增章节——AI/前端供应链的新攻击面。
- **替代品选择**:**Web 应用渗透选 PATT**，**内网/AD 选 InternalAllTheThings**，**IoT 选 HardwareAllTheThings**，**纯 wordlist 选 SecLists**，**方法论选 HackTricks**——这五个组合起来就是完整的红队知识矩阵。

### 如果你要学它
- **重点关注文件**:
  - `_template_vuln/README.md`——4 个 H2 章节的极简模板，看怎么用最小成本约束贡献。
  - `Methodology and Resources/Active Directory Attack.md`——246 次修改、绝对热度第一，AD 攻防的内容沉淀极深。
  - `Server Side Template Injection/`——Java (SpEL/OGNL/EL) / Python (Jinja2/Twig) / PHP / Node / Elixir/EEx 多语言 SSTI 横向对比。
  - `.github/workflows/check-markdown.yml` + `.markdownlint.json`——增量 markdownlint 的工程化范本。
  - `mkdocs.yml`——material 主题 + `content.code.copy` + `git-revision-date-localized` 的文档三件套。
- **设计模式学习**:**占位符规范、四件套目录、_附录区下划线前缀、Wayback Machine 主动归档**——这些模式可以原样复制到你的内部知识库。

### 如果你要 fork 它
- **可改进方向**:
  1. **加自动化 payload 验证 CI**——每周跑一遍 DVWA/Juice Shop 验证关键 payload 仍能复现。
  2. **加中文翻译版**（或法语/西语版）——分仓 `PayloadsAllTheThings-CN`，复用同样的四件套结构。
  3. **加 `i18n/` 目录重构占位符**——把 `[ATTACKER.DOMAIN.TLD]` 提取到 `i18n/zh-CN/placeholders.md` 之类的配置文件。
  4. **Methodology and Resources 清理**——要么迁完就删目录，要么保留完整内容，**别保留「空壳」占位**。
  5. **统一 `Intruder`/`Intruders` 命名**——在 CONTRIBUTING.md 钉死，渐进式 PR 重命名。
  6. **加 `analytics` 集成**——mkdocs 集成 Plausible/Umami，量化读者行为找最常用章节。
  7. **把 `Methodology and Resources` 拆出到 `internal-attacks.md` 子文件**——避免 30+ 个 moved to 空壳。

### 知识入口

| 资源 | 链接 |
|------|------|
| 官方站点（mkdocs 渲染版） | https://swisskyrepo.github.io/PayloadsAllTheThings/ |
| 作者博客 | https://swisskyrepo.github.io/ |
| DeepWiki | 未收录（页面仍在 loading） |
| Zread.ai | 未收录（403） |
| 关联论文 | 无（其内容多为漏洞利用代码，不属于学术研究范畴） |
| 在线 Demo | https://swisskyrepo.github.io/PayloadsAllTheThings/（mkdocs 站点自带 `content.code.copy` 一键复制） |

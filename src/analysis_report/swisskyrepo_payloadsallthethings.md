# 9 年 78K stars:渗透测试红队的"复制即用"字典怎么炼成的

> GitHub: https://github.com/swisskyrepo/payloadsallthethings

## 一句话总结

一个独立红队研究员 9.5 年沉淀的渗透测试 payload + WAF bypass 字典——按攻击面切目录、PR 替代 issue、Markdown 即文档,成为红队/Bug Bounty/OSCP 备考的"基础设施级"参考仓。

## 值得关注的理由

- **"仓库即文档"的极致样本**:零构建系统、零 `nav:` 配置、目录顺序就是导航顺序,把"git diff 即可贡献"做到最低门槛
- **PR 驱动 + has_issues=false 的治理实验**:333 名贡献者 + 47.5% 单一作者占比,17 个 open PR 排队,内容半衰期长项目的"质量可追溯"范本
- **跨仓矩阵化战略**:AllTheThings 三件套(Payloads/Internal/Hardware)共享骨架,内容迁移时留跳转入口不删旧目录,是开源知识矩阵的成熟模板

## 项目展示

![banner](https://raw.githubusercontent.com/swisskyrepo/PayloadsAllTheThings/master/.github/banner.png) — 仓库主视觉,9 年沉淀的"一站式字典"形象

![contributors collage](https://contrib.rocks/image?repo=swisskyrepo/PayloadsAllTheThings&max=36) — 自动生成的活跃贡献者拼图,333 人协作的可视化

![SerpApi sponsor](https://avatars.githubusercontent.com/u/34724717?s=40&v=4) · ![ProjectDiscovery sponsor](https://avatars.githubusercontent.com/u/50994705?s=40&v=4) · ![VAADATA sponsor](https://avatars.githubusercontent.com/u/48131541?s=40&v=4) — 三大赞助商嵌入 README,内容→工具→变现的正循环

> 在线浏览:`swisskyrepo.github.io/PayloadsAllTheThings/`(mkdocs-material 渲染的镜像站)

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/swisskyrepo/payloadsallthethings |
| Star / Fork | 78,151 / 17,032(Watcher 1,961) |
| 代码行数 | 2,096 行 + 54,442 行 markdown(主语言 Python 61%,实质是 markdown 知识库) |
| 项目年龄 | 115.6 个月(2016-10 至今,9.5 年) |
| 开发阶段 | 低维护(近 30 天 0 commit,近 90 天 13 commit,呈"间歇休眠 + 偶发合并"模式) |
| 贡献模式 | 核心少数 + 社区(主作者 Swissky 47.5% + 第 2-10 名 16.6% + 333 人长尾 35.9%) |
| 热度定位 | 大众热门(红队/渗透测试领域的"基础设施级"参考仓) |
| 质量评级 | 代码 N/A · 文档 9/10 · 测试 N/A(知识库,无源码测试) · 协作治理 9/10 |
| License | MIT(2019 Swissky) |
| 最新版本 | v4.2(共 7 tag,9.5 年仅 7 个版本——把 tag 当知识库大版本里程碑用) |

## 作者视角:为什么存在这个项目

### 创始人/作者背景

Swissky(@pentest_swissky),独立 **Red Team Operator & Bug Hunter**,账号 11 年(2015-04 注册),粉丝 10K+,公开仓库 13 个。本仓占作者累计 Star 的 80%+,是其个人矩阵的绝对核心。

跨作者矩阵:
- **AllTheThings 三件套**:`PayloadsAllTheThings`(Web 攻击面,本仓)/ `InternalAllTheThings`(AD/内网/云)/ `HardwareAllTheThings`(硬件/IoT)
- **同作者其他 1k+ Star 工具**:`SSRFmap` / `GraphQLmap` / `Vulny-Code-Static-Analysis` / `SharpLAPS` / `Wordpresscan`

**背景塑造的设计选择**:11 年沉淀的 Bug Bounty 实战 + 红队工程化 + OSCP 培训教学三股力合一,直接决定"目录切分按攻击面而非按工具""payload 必给可粘贴命令 + WAF bypass""README 配 Lab 链接(HTB/PortSwigger/Root-Me)"等设计——所有这些都不是工程师抽象设计出来的,而是 11 年实战倒逼出来的"教学+实战"双轨范式。

### 问题判断

网安人(红队 / Bug Hunter / CTF / OSCP 备考 / AppSec)在实战中反复遇到同一个摩擦:**"我记得有个 payload 能绕过这个 WAF,但就是想不起来该是 `jAvaScRiPt:` 还是 `JaVaScRiPt:`"**。这种"用一次就忘、必须现场拼"的隐性知识,分散在博客、Twitter、Pastebin、Notion 个人笔记中,搜索引擎召回差,质量参差,缺 WAF 厂商指纹,缺可重现 docker one-liner,缺 WAF 绕过。

Swissky 看到的机会是:把这种知识**沉淀成"目录即结构、复制即可用、引用可溯源"的公共字典**,由社区 PR 持续供给新绕过——内容半衰期长,搜索引擎可索引,Git diff 即可贡献,远比博客/PDF cheat sheet 持久。

### 解法哲学

五个反共识决策,每个都"明确选择了不做"某些事:

1. **不写框架** — 没有 Astro / VuePress / Docusaurus,只用 `mkdocs-material` 渲染,本体就是纯 `.md`。零安装、克隆即可读、git diff 即可贡献
2. **目录即结构** — `mkdocs.yml` 没有 `nav:` 配置,目录顺序 = 导航顺序,**目录就是目录**,砍掉 90% 配置维护
3. **PR 替代 issue**(has_issues=false) — 所有讨论/漏洞补全/新绕过都走 PR,直接绑 commit。代价:作者要 review 17 个 open PR;收益:内容质量门槛 + 可追溯 + 可回滚
4. **Sanitize-first** — `CONTRIBUTING.md` 强制 `id` / `whoami` / `[ATTACKER.DOMAIN.TLD]` / `10.10.10.10` 占位,保证 PR 一合并就是"无害"版本——一条被其他安全项目反复抄写的护栏条款
5. **Sponsor 嵌入 README** — 顶部直接列 SerpApi / ProjectDiscovery / VAADATA(都是与目标用户强相关的工具厂商),配 `FUNDING.yml` 三渠道(GitHub Sponsors / Ko-fi / Buy Me a Coffee),形成"内容→工具→变现→内容"正循环

### 战略意图

**AllTheThings 矩阵化布局**:横向广度(Web/AD/IoT 三仓各自覆盖一个完整攻防场景);纵向深度(同一漏洞如 AD 攻击从本仓移交给 `InternalAllTheThings`,本仓只留跨接点;`Methodology and Resources/Active Directory Attack.md` 头部直接 redirect + 40+ 个分章节跳转链接)。

**开源策略:genuinely open** — MIT 协议,内容完全公开,无 open-core / 无 SaaS 化 / 无企业版。变现路径只走"赞助商嵌入 README + FUNDING.yml",且赞助商必须是与目标用户强相关的工具厂商(SerpApi/ProjectDiscovery/VAADATA 三家都是)。

## 核心价值提炼

### 创新之处

1. **「攻击面即目录」组织法** — 跨工具/跨语言/跨 payload,统一按攻击面切分。`SQL Injection/` 下分 MySQL/PostgreSQL/MSSQL/Oracle/SQLite/DB2/BigQuery/Cassandra,把方言收齐;`Insecure Deserialization/` 下分 Java/PHP/Python/Node/DotNET/Ruby,把语言运行时收齐;`XSS Injection/` 下分 1-Filter Bypass/2-Polyglot/3-WAF Bypass/4-CSP Bypass/5-Angular,把 bypass 维度收齐
   - **新颖度 3/5 | 实用性 5/5 | 可迁移性 5/5** — 任何"维度可枚举、跨工具/跨平台/跨语言"的知识(协议、攻击向量、合规要求),都可用此组织

2. **「cheatsheet + payload 库」成对** — 每章 `README.md` 讲原理 + 给命令 + 贴代码块,同时配 `Intruder/` 目录直接是可被 Burp / wfuzz / ffuf 消费的字典文件
   - **新颖度 4/5 | 实用性 5/5 | 可迁移性 5/5** — 任何"既要教又要用"的项目(数据库优化案例库 / Linux kernel sysctl 调优库 / Kubernetes 安全基线)都可用

3. **「PR 替代 issue + 模板 + lint」治理模型** — `has_issues=false` + `_template_vuln/` + `markdownlint-cli2-action` 强制风格统一,333 名贡献者滚动供给
   - **新颖度 4/5 | 实用性 4/5 | 可迁移性 5/5** — 任何"内容半衰期长 / 协作门槛高"的项目(法律条文库 / 行业最佳实践库)都适用

4. **「跨仓迁移 + 留入口」防断链** — AD/Reverse Shell 等内容已迁移到兄弟仓,本仓**保留旧目录但不删除**,只把内容替换成跳转表
   - **新颖度 3/5 | 实用性 5/5 | 可迁移性 5/5** — 任何"内容矩阵"型项目(多仓分工),迁移时**别删旧目录**,改写跳转页

5. **Wayback Machine 化外链** — commit `497fbe9 Archive external reference links via Wayback Machine`,是被外部链接腐烂倒逼出的反脆弱
   - **新颖度 2/5 | 实用性 5/5 | 可迁移性 5/5** — 任何引用外部资源的长寿内容都该做

### 可复用的模式与技巧

| 模式 | 适用场景 |
|---|---|
| MkDocs Material + 零 `nav:` 配置 | 个人/小团队文档项目,比 Astro / Docusaurus 轻 10 倍,几乎零维护 |
| `Intruder/` 字典配套发布 | 任何"教学 + 实战"双轨项目(可配 wfuzz/ffuf 字典、SQL 注入字典、密码字典) |
| `_template_vuln/` 标准章节 | 任何"按维度枚举"的知识库(攻击面/合规要求/协议族/产品矩阵) |
| `_LEARNING_AND_SOCIALS/` 下划线前缀约定 | 区分"主内容目录"和"辅助内容目录" |
| `mkdocs gh-deploy --force` + GitHub Action | push master 即发布,零运维 |
| `pymdownx` 插件集(代码高亮/emoji/任务列表) | 一次配置,长期受益 |
| `umami.is` + `addtoany` 嵌入 `overrides/main.html` | 不写一行前端就拥有统计 + 分享 |
| `contrib.rocks/image?repo=...&max=N` 嵌入 README | 活跃贡献者拼图自动生成,333 人协作的可视化 |

### 关键设计决策

**决策 1:目录即结构(no nav: in mkdocs.yml)**
- 问题:小团队/个人维护 nav 配置成本高,容易 drift
- 方案:`mkdocs.yml` 不写 `nav:`,目录顺序 = 导航顺序
- Trade-off:牺牲了"导航顺序自由",换来了"零配置维护 + git diff 即可贡献"
- 可迁移性:高,小型文档项目可砍掉 nav 维护成本

**决策 2:PR-driven + has_issues=false**
- 问题:issue 池易沉、质量不可控、外部链接腐烂
- 方案:关 issue,所有讨论走 PR + `markdownlint-cli2-action` 强制风格统一 + `497fbe9` commit 用 Wayback Machine 化外链
- Trade-off:作者要 review 17 个 open PR(个人产能瓶颈),换来了"内容质量门槛 + 可追溯 + 可回滚 + 反脆弱"
- 可迁移性:高,知识型项目可参考

**决策 3:cheatsheet + payload 库成对(README.md + Intruder/ + Files/ + Images/)**
- 问题:教学型内容与实战型字典分开,读者要切换仓库
- 方案:每个漏洞目录 = `README.md` 原理 + `Intruder/` 字典 + `Files/` 样本 + `Images/` 截图
- Trade-off:目录组织约定变多(4 套子目录命名),换来了"教学+实战"双轨最低成本
- 可迁移性:高,任何"既要教又要用"的项目

**决策 4:跨仓迁移 + 留入口**
- 问题:内容矩阵化分工时,旧仓的目录删除会断外链
- 方案:旧目录保留但不删除,只把内容替换成跳转表 + 40+ 个分章节跳转链接
- Trade-off:旧目录"形式上还在",换来了"所有外链保留 + 信息丰富感"
- 可迁移性:高,任何多仓内容分工项目

**决策 5:tag 里程碑制(9.5 年仅 7 个 tag)**
- 问题:知识库不需要天天发版,但读者需要"什么时候大改写过"的信号
- 方案:语义化版本对应"一次大改写/迁移"(v4.0 大概率对应 AD/Cloud 主题扩列),不打无意义 patch
- Trade-off:读者需要手动跟进新内容,换来了"tag 信号清晰 + 减少 tag 噪音"
- 可迁移性:中,适合内容半衰期长、节奏稳定的项目

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | PayloadsAllTheThings(本仓) | HackTricks(11.5k★) | OWASP CheatSheetSeries(32k★) | A-poc RedTeam-Tools(8.8k★) | swisskyrepo/InternalAllTheThings(2.2k★) |
|------|---|---|---|---|---|
| 定位 | 红队 payload 字典(how-to-paste 极致深度) | 红队全景百科(what+how) | 防御侧官方 cheatsheet | 工具与脚本聚合 | 同作者 AD/内网细分 |
| 覆盖广度 | Web 攻击面 + AD 入口 | Web/Linux internals/云/容器/移动端 | 体系化(各语言防御指南) | 工具链为主 | AD/内网/云 |
| Payload 可用度 | **10/10**(`Intruder/` 字典 + 即拷即用代码块) | 7/10(解释多,payload 散) | 3/10(防御视角,无完整 payload) | 6/10(命令脚本齐全) | 8/10(风格一致) |
| 引用可溯源 | 9/10(References 格式统一 + Wayback) | 8/10 | 9/10(官方版本) | 5/10 | 8/10 |
| 协议 | MIT(可商用) | 知识共享(非商业) | CC BY-SA 4.0 | MIT | MIT |
| 维护者 | 1 主 + 333 社区 | 多人协作 | OWASP 官方 | 1 主 + 社区 | 1 主(Swissky) |
| 协作入口 | **PR(issue 关闭)** | Issue + PR | Issue + PR | Issue + PR | PR(issue 关闭) |
| 适合谁 | "我装了 Burp,要喂什么字典" | "我想要一份目录导航" | "我要写 Fix 指南" | "我要装一套工具" | "我要做 AD/内网" |

### 差异化护城河

- **技术护城河**:9.5 年沉淀的 75 个攻击面目录 + `Intruder/` 字典(累计 30+ 字典文件,SQL Injection 下 17 个 `*.txt`)+ 章节子目录的强约束模板——这套结构是 HackTricks 短期内无法复制的
- **生态护城河**:AllTheThings 三件套矩阵(Payloads/Internal/Hardware)共享骨架,内容自然向兄弟仓滚动,跨仓外链 + 跳转表形成内容网络
- **信任护城河**:11 年账号 + 10K 粉丝 + SerpApi/ProjectDiscovery/VAADATA 公开赞助 + Twitter @pentest_swissky 持续输出 + MIT 协议可商用 = 在企业内训/Bug Bounty 圈里的"事实标准"

### 竞争风险

- **最可能被替代**:HackTricks(11.5k★,覆盖面更广,自带本地化站点,自带搜索),如果 HackTricks 把 `Intruder/` 字典补齐 + 引入 `mkdocs-material` 渲染 + 关 issue 改 PR
- **被替代的触发条件**:本仓维护持续性进一步下降(目前近 30 天 0 commit,17 个 open PR 排队),HackTricks 引入 Burp 字典配套 + 强制 markdownlint
- **不太可能被替代**:OWASP CheatSheetSeries(32k★)和本仓错位竞争,一个防御视角一个攻击视角,几乎不重叠

### 生态定位

在整个红队/网安知识生态中扮演**"how-to-paste 极致深度"的基础设施**——填补了"HackTricks 太广、OWASP 太防御、A-poc 太工具、awesome-list 没内容"的生态空白。是红队工程师、Bug Bounty 猎人、OSCP 备考者的"复制即用第一站"。

## 套利机会分析

- **信息差**:**严重不套利**——78K stars + 17K forks + 9.5 年沉淀,人尽皆知,人人引用。套利机会反而在**"配套整理/翻译/靶场"**:
  - 中文翻译版 / 体系化整理(分语言复刻)
  - 配套实验靶场(基于 `Labs` 段的 HTB/PortSwigger/Root-Me 链接)
  - 反差异化叙事写文章(批判性分析,而非"OSCP 必备"的二级转发)
- **技术借鉴**:6 个可被其他知识库借鉴的通用模式(详见「创新之处」节),适合法律条文库 / 行业最佳实践库 / Kubernetes 安全基线 / Linux kernel sysctl 调优库 等"维度可枚举"的项目
- **生态位**:在红队知识生态中已无可替代,更多是"深耕"而非"拓荒"
- **趋势判断**:已进入低维护稳态(近 30 天 0 commit,近 90 天 13 commit,17 open PR 排队),增速从 2021 月均 35 降至 2024 月均 13。**比 HackTricks 的后发优势在于:9.5 年积累的 payload 字典厚度 + AllTheThings 三件套的矩阵协同**,但 HackTricks 的"广度扩张"仍是更快的增长引擎

## 风险与不足

- **维护持续性瓶颈**:近 30 天 0 commit,17 个 open PR 排队未 review,主作者 Swissky 个人产能是单点风险
- **目录命名遗留**:9.5 年未做大规模重命名,`XSS Injection/` vs `XSS injection/`、`Upload insecure files/JPG Resize` vs `Upload/JPG Resize`、`Intruder/` vs `Intruders/`(7 处不一致)同时存在,影响导航一致性
- **无 issue 池的代价**:外部用户提"Bug Bounty 报告"或"新 CVE 反馈"时,缺乏轻量入口,可能直接外流到 Twitter/Discord
- **传统 CI 缺失**:无单元测试(合理,知识库无源码),无依赖版本锁定(无 package.json),但也意味着 markdownlint 是唯一的质量门
- **安全合规风险**:仓库本质是攻击 payload 字典,虽 `CONTRIBUTING.md` 强制 sanitize,但实际 payload 中仍含真实 IP/域名样本(部分已用占位符),企业内训引入时需合规评估
- **章节结构 100% 一致性未达**:虽然有 `_template_vuln/` 模板,但部分老目录未完全遵守,markdownlint 只能保证风格统一,无法保证结构统一

## 行动建议

- **如果你要用它**:
  - **红队 / Bug Bounty 实战**:本仓 + HackTricks 双仓并用——HackTricks 当"目录导航",本仓当"复制源"(`Intruder/` 字典直接喂 Burp)
  - **OSCP / OSWE 备考**:把本仓当 cheat sheet,边练边学,`Labs` 段的 HTB/PortSwigger/Root-Me 链接做实验环境
  - **AppSec / SDL 工程师**:复现 payload 找自家产品的 sink 点,`Intruder/` 字典喂到 SAST/DAST 工具
  - **CTF 出题人**:借鉴「同一漏洞多种引擎/语言实现」的对照编排
  - **企业内训引入**:需评估 payload 中的 IP/域名样本合规性,优先使用 `Intruder/` 字典而非 README 代码块

- **如果你要学它**(重点关注以下文件/模块):
  - `_template_vuln/README.md` — 标准章节模板(7 个固定子节)
  - `.github/workflows/check-markdown.yml` — markdownlint 强制风格统一
  - `.github/workflows/mkdocs-build.yml` — push 即发布
  - `mkdocs.yml` — 零 `nav:` 配置的极简渲染
  - `CONTRIBUTING.md` — Sanitize-first 护栏条款
  - `Methodology and Resources/Active Directory Attack.md` — 246 次修改的核心(看它怎么"保留但不删除"做跳转表)
  - `Server Side Template Injection/` — 典型"cheatsheet + Intruder/ + Files/ + Images/"四件套目录
  - `CVE Exploits/Log4Shell.md` — 看 docker one-liner 复现的优秀实践
  - `.github/overrides/main.html` — 嵌入 `addtoany` 分享 + `umami.is` 统计的极简前端
  - `commit 497fbe9` — Wayback Machine 化外链的反脆弱实践

- **如果你要 fork 它**(可改进的方向):
  - **目录重命名 + 命名规范强制**:解决 `Intruder/` vs `Intruders/` 等 7 处不一致
  - **issue 池轻量化**:开启 `has_issues=true` 但仅做"Bug Bounty 反馈"和"新 CVE 通知",讨论仍走 PR
  - **自动化质量门**:除了 markdownlint,加 `mkdocs build --strict` 强制所有内部链接有效
  - **多语言翻译流水线**:用 GitHub Action + LLM 自动翻译到中文/日文/西班牙文(配合 `contrib.rocks` 拼图激励贡献者)
  - **配套靶场化**:把 `Labs` 段的链接做成 docker-compose 一键启动
  - **内容矩阵 API 化**:把 `Intruder/` 字典暴露为 REST API,让 Burp 插件 / wfuzz / ffuf 实时拉取

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录(页面处于 Loading 状态) |
| Zread.ai | 无法访问(HTTP 403) |
| 关联论文 | 无(知识库性质,无对应学术论文) |
| 在线 Demo | 无(cheatsheet 性质);但提供 GitHub Pages 站点 [swisskyrepo.github.io/PayloadsAllTheThings](https://swisskyrepo.github.io/PayloadsAllTheThings/) 做浏览 |
| 同作者矩阵 | [InternalAllTheThings](https://github.com/swisskyrepo/InternalAllTheThings) · [HardwareAllTheThings](https://github.com/swisskyrepo/HardwareAllTheThings) |
| HopLa Burp 插件配置 | `.github/hopla_config.json`(在 Burp Suite 中注入 payload) |

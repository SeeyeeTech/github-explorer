# 31.9k star 的一人公司 changedetection.io：网页监控怎么用 open-core 把开源做成生意

> GitHub: https://github.com/dgtlmoon/changedetection.io

## 一句话总结

changedetection.io 是自托管网页变化监控赛道的开源头部工具——监控任意网页的内容变化（比价、补货、网页篡改、条款变更）并即时告警，开箱即用无需写代码。它由 Leigh Morresi（dgtlmoon）单人主导（88.6% 提交）5.4 年打磨成 31.9k star 的工业级产品，并通过「Apache 2.0 自托管 + $8.99/月 SaaS + 反转售商业授权」三轨，做成了一门「一人公司」的生意。

## 值得关注的理由

1. **一人公司 open-core 变现的优质范本**：单核心主导 + 社区贡献翻译/插件，配 `COMMERCIAL_LICENCE.md` 的「Hosting 条款」（任何把本软件作为服务转售/托管者必须另购商业授权，类似 Elastic/Commons Clause）精准反云厂商套壳——保护官方 SaaS 不被白嫖。对独立开发者是「如何把开源项目做成可持续生意」的实战教材。
2. **架构是一座可插拔设计的金矿**：检测算法（processors）和抓取后端（content_fetchers）都做成「目录扫描自动发现 + pluggy 外部扩展」的双可插拔抽象；无数据库（文件系统即存储，原子写 + brotli 历史）；双指纹缓存跳过重处理——这些脱离监控场景也能直接迁移。
3. **供需两侧自给自足的生态打法**：网页监控是「需求侧」，作者并行构建的反爬无头浏览器工具栈（sockpuppetbrowser、CloakBrowser、pyppeteer-ng）是「供给侧」，互相喂养——反爬是这门生意的命门，他把命门握在自己手里。

## 项目展示

![主界面监控看板](https://raw.githubusercontent.com/dgtlmoon/changedetection.io/master/docs/screenshot.png)
监控看板：集中管理所有 watch 的状态与变化历史。

![可视化选择器](https://raw.githubusercontent.com/dgtlmoon/changedetection.io/master/docs/visualselector-anim.gif)
可视化选择器：点选页面元素即可生成过滤规则，非程序员也能用。

![Browser Steps](https://raw.githubusercontent.com/dgtlmoon/changedetection.io/master/docs/browsersteps-anim.gif)
Browser Steps：录制登录/加购/搜索等交互步骤后再检测。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/dgtlmoon/changedetection.io |
| Star / Fork | 31,920 / 1,824 |
| 代码规模 | 真实约 **3.4 万行核心 Python + 1.2 万行测试**（134 测试文件 ≈ 业务文件数，QA 重）；cloc 总 117k 行中 PO File 27.4%（14 语种 i18n）+ SVG 19.1%（图标）是非业务资产 |
| 项目年龄 | 64.4 个月（约 5.4 年，2021-01 创建） |
| 开发阶段 | 密集开发（近 30 天 41 commit；**229 tags，每月约 3.5 个版本，超高频发版**） |
| 贡献模式 | 单核心主导（Leigh Morresi/dgtlmoon 占 88.6% commits，149 贡献者多贡献翻译/插件） |
| 热度定位 | 大众热门（高速增长，自托管监控类头部） |
| 质量评级 | 代码[优] 文档[优] 测试[优] CI[优] 错误处理[优·全链路 fail-soft] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

作者 dgtlmoon（真名 **Leigh Morresi**），背后商业实体 **Web Technologies s.r.o.**。16 年 GitHub 老兵 + 创业者，自述从 Linux kernel 2.0 + 拨号 BBS 起步。围绕变化检测构建了一整条反爬/无头浏览器工具栈（sockpuppetbrowser、CloakBrowser、pyppeteer-ng、changedetection.io-osint-processor），是「把单一开源项目做成商业 SaaS 的一人公司」典型。

### 问题判断

Morresi 是 16 年的爬虫/反爬老兵，他的关键判断是：**网页监控的真正瓶颈不是 diff 算法，而是从充满噪声（广告、时间戳、CSRF token、轮播）的现代网页里稳定抽出用户关心的那一小块内容，并穿透 JS 渲染、登录墙和反爬**。所以监控产品是需求侧，浏览器工具栈是供给侧——`content_fetchers/base.py` 里专门列了一长串「会被识别为机器人的方式」，证明反爬是设计的第一性关注点。

### 解法哲学

- **自托管优先 + 数据所有权**：所有数据落本地文件，无外部 DB，Docker 一行起。
- **可插拔抽象**：检测算法和抓取后端都做成「发现即注册」的插件，第三方可在 pip 包里扩展而不改主仓。
- **降门槛**：可视化选择器（点选元素）、Browser Steps（录制登录/加购）、自然语言 AI 意图，让非程序员也能配复杂监控。
- **明确不做什么**：restock processor 注释明说「只支持单商品页」，多商品直接抛异常引导换模式——拒绝过度泛化。
- **优雅降级**：LLM 预算超限/失败一律 fail-open（当作重要变化放行，不吞通知）；OpenCV 缺失回退 pixelmatch；orjson 缺失回退标准库。

### 战略意图

典型「一人公司」open-core 打法：Apache 2.0 自托管版功能基本完整 → 养社区、攒 star、收翻译/插件贡献；官方 SaaS $8.99/月变现（自称同类半价）；护城河是 `COMMERCIAL_LICENCE.md` 的 Hosting 条款（反云厂商套壳）。pluggy 插件机制则给「不开源的商业增值 fetcher/processor」留了官方扩展点。

## 核心价值提炼

### 创新之处

1. **processor + fetcher 双可插拔抽象**（新颖 4 / 实用 5 / 可迁移 5）：内置算法/后端走 `pkgutil` 目录扫描自动注册（processor 继承基类、实现 `run_changedetection → (changed, update_obj, snapshot)` 三元组契约，按 weight 排序），第三方 pip 包走 pluggy hook（register_processor/register_content_fetcher 等 6+ 钩子），二者在同一注册表合流——这是「核心开源 + 商业插件」的工程基石。
2. **AI 意图化变化检测**（新颖 5 / 实用 5 / 可迁移 4）：用户写自然语言意图（「降价到 $300 以下时提醒」），LLM 判定 diff 是否「重要」并出人话摘要；所有 LLM 经 LiteLLM 单点收口接 OpenAI/Gemini/Anthropic/Ollama/vLLM，带 (intent,diff) 缓存 + 双层 token 预算（全局月度 + 每 watch）+ fail-open。把「噪声告警」升级为「语义告警」。
3. **补货检测的 metadata 抽取 + 子进程内存隔离 + JS 测谎**（新颖 4 / 实用 4 / 可迁移 4）：靠 JSON-LD/microdata/OpenGraph 等结构化元数据而非脆弱页面文本判库存/价格；用 Linux `spawn` 子进程隔离解决 extruct/lxml 的 C 级内存泄漏（注释用 memray 量化：1.2M 次分配/页、50–500MB 滞留，进程退出 OS 强制回收）；再用浏览器注入的 JS 抓页面实际文案——若 metadata 说有货但 JS 抓到「缺货」，以 JS 为准（lie detection）。
4. **无数据库的原子文件存储 + brotli 历史**（新颖 3 / 实用 5 / 可迁移 4）：每个 watch 一个 `{uuid}/` 目录，`save_json_atomic()` 用「临时文件 + os.replace + 目录 fsync」做到 NFS 安全；历史文本 brotli 流式压缩；读历史对路径做 realpath + 前缀校验防目录穿越（备份恢复来的路径不可信）。
5. **两级校验跳过优化（内容指纹 + 配置指纹）**（新颖 3 / 实用 5 / 可迁移 5）：raw HTML 未变时短路掉昂贵的解析/过滤/diff——仅当「raw MD5 相同 且 watch 未被编辑 且 `filter_config_hash` 相同」三者全满足才跳过；`filter_config_hash` 把 watch/tag/global 三层过滤规则合成一个稳定哈希，避免散落的手动 invalidate。
6. **多引擎过滤前缀路由**（新颖 3 / 实用 5 / 可迁移 5）：用前缀把 XPath / CSS / JSONPath(`json:`) / jq(`jq:`) 统一进同一条过滤管线，subtractive selector 先减后取，让用户一套输入框混用多种查询语言。

### 可复用的模式与技巧

1. **基类定三元组契约 + 目录扫描自动注册 + weight 排序**：插件化算法平台通用骨架。
2. **能力标志（capability flags）声明式多后端**：fetcher 子类自报 `supports_browser_steps/supports_screenshots` 等，上层按场景选实现而非 if-else 类型判断。
3. **原子文件写**：临时文件→`os.replace`→（新文件才）目录 fsync，NFS/NAS 安全，附 ENOSPC/EDQUOT 友好报错。
4. **双指纹缓存失效**：内容 MD5 + 配置哈希联合闸门，避免散落的手动 invalidate 调用。
5. **C 扩展内存泄漏的子进程隔离**：spawn 子进程跑 lxml/OpenCV，靠进程退出回收 C 内存（Linux 限定，其它平台直调兜底）。
6. **LLM 接入收口**：单 `completion()` 经 LiteLLM 多 provider + 结果缓存 + fail-open + 分层 token/成本预算 + provider 差异化（Anthropic caching/Gemini thinking）。
7. **反射式 action 分派**：Browser Steps 把操作名 → `action_<name>` 方法，配 Jinja2 模板变量，做轻量步骤 DSL。
8. **诊断友好的异常**：`FilterNotFoundInResponse` 携带 screenshot + xpath_data，让「过滤没命中」能在 UI 直接可视化排错。

### 关键设计决策

- **多抓取后端能力标志**：`Fetcher` 基类用能力标志（supports_browser_steps/supports_screenshots/supports_xpath_element_data）声明后端能力，`call_browser()` 按 `watch.fetch_backend` 运行时 `getattr` 解析；PDF 强制走 requests、browser steps 强制回 playwright。
- **自定义条件引擎（JSON Logic + pluggy 插件）**：高级触发条件用 JSON Logic 规则，插件（levenshtein/wordcount）在求值前注入事实（字数、相似度）并注册新算子，插件用 ThreadPoolExecutor 加 10s 超时熔断。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | changedetection.io | urlwatch | Huginn | Visualping | Distill.io |
|------|--------|--------|--------|--------|--------|
| 形态 | 自托管开源 + SaaS | 开源 CLI | 开源通用自动化 | 商业 SaaS | 商业 freemium |
| Star/量级 | 31.9k | ~3k | 44k | 闭源 | 闭源 |
| 自托管 | ✅ | ✅ | ✅ | ❌ | 部分(扩展) |
| JS 渲染 | ✅ | ❌ | 有限 | ✅ | ✅ |
| 可视化选择器 | ✅ | ❌ | ❌ | ✅ | ✅ |
| JSON/API 监控 | ✅ 强(jq/JSONPath) | 有限 | 有限 | 弱 | 弱 |
| AI 检测 | ✅ | ❌ | ❌ | ✅ | 部分 |

### 差异化护城河

①自托管 + 数据所有权 + 开源（对 SaaS 竞品）；②渲染/反爬/可视化/AI/补货的功能广度（对 CLI 竞品）；③双可插拔架构 + pluggy 让商业增值能力可挂载；④反转售 Hosting 授权的法律护城河保护官方 SaaS；⑤作者自有浏览器工具栈（sockpuppet/Cloak）的供给侧优势。

### 竞争风险

1. **巴士因子**：核心强依赖单人（88.6% commits）。
2. **反爬是无尽军备竞赛**（#2198），命门需持续投入。
3. **检测准确性长期痛点**：过滤命中波动导致误报空 diff（#962，135 评论）。
4. **运维门槛**：浏览器栈运维把部分普通用户推回 Visualping 这类零运维 SaaS。
5. **依赖版本地狱**：LiteLLM 等依赖在 requirements 里有大段 pin 说明。

### 生态定位

开源自托管阵营的「网页监控事实标准」，卡位「自托管开源」与「低价官方 SaaS」两端，靠授权条款与浏览器供给侧把两端同时握住。

## 套利机会分析

- **信息差**：项目已是赛道明牌头部、知名度高、商业化成熟，不存在「被低估」红利。真正的内容价值在「拆解它的 open-core 商业范式 + 可插拔架构」，而非介绍它能监控网页。
- **技术借鉴**：双可插拔抽象、能力标志多后端、原子文件存储、双指纹缓存、子进程隔离 C 内存泄漏、LLM 接入收口——这些脱离监控场景，对任何「插件化平台」「自托管工具」「接 LLM 的服务」都直接可抄。
- **商业借鉴**（更稀缺）：「Apache 2.0 自托管 + 低价 SaaS + 反转售 Hosting 授权 + 自有供给侧工具栈」是独立开发者把开源做成生意的完整范式。
- **趋势判断**：成熟密集开发，作为「事实标准 + 一人公司」生命力强；AI 变化检测是最新增长点。

## 风险与不足

1. **单人核心巴士因子高**：dgtlmoon 占 88.6% commits，核心高度依赖一人。
2. **反爬命门需永续投入**：bot-detection 是无尽军备竞赛。
3. **检测准确性**：过滤命中波动导致误报空 diff 是长期痛点。
4. **无 CHANGELOG 文件**：靠 229 个 tag/GitHub Releases 替代（超高频发版下问题不大）。
5. **运维门槛**：自托管浏览器栈对普通用户偏重。

## 行动建议

- **如果你要用它**：要自托管、数据自己掌控、强 JSON/API 监控、且愿意运维浏览器栈——它是开源自托管赛道最佳选择，`docker run` 一行启动；不想运维选官方 SaaS（$8.99/月）；要极致省心的视觉比对云服务选 Visualping。
- **如果你要学它（技术）**：重点读 `processors/__init__.py`（发现机制）+ `processors/base.py`（三元组契约）、`content_fetchers/base.py`（能力标志多后端）、`store/file_saving_datastore.py`（原子文件存储）、`processors/restock_diff/processor.py`（子进程隔离内存泄漏）、`llm/evaluator.py`（LLM 接入收口）。
- **如果你要学它（商业）**：研究 `COMMERCIAL_LICENCE.md` 的 Hosting 条款 + pluggy 插件留商业扩展点 + 自有浏览器工具栈的供给侧布局——这是独立开发者 open-core 变现的完整打法。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [已收录（系统架构/内容处理流水线/部署）](https://deepwiki.com/dgtlmoon/changedetection.io) |
| Zread.ai | 未确认（直连 HTTP 403） |
| Docker Hub | [dgtlmoon/changedetection.io 官方镜像（一行启动）](https://hub.docker.com/r/dgtlmoon/changedetection.io/) |
| 在线 Demo / SaaS | [官方托管版 changedetection.io（$8.99/月，免费 5 页可试）](https://changedetection.io) |
| 关联论文 | 无（工程项目） |

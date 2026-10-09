# GitHub推荐：system-design-notes 拆解：28 章笔记 + 392 张架构图里能偷走的 7 个套路

> GitHub: https://github.com/liquidslr/system-design-notes

## 一句话总结
Gaurav Kumar 把 Alex Xu《System Design Interview》Vol 1+2 全 28 章转写成纯 Markdown 笔记 + 392 张原创架构图，零代码、零测试、零 LICENSE，靠"可读性"在 GitHub 拿到 24,613 星，但本质是「忠实抄写 + 极少原创」的学习型仓库。

## 值得关注的理由
1. **可挖走 7 个面试套路**：4 步面试框架（Scope → High-Level → Deep Dive → Wrap-Up）、Quorum 公式 W+R>N、Consistent Hashing 受影响区间、DAG 异步流水线、mmap 当事件总线等，**这些被显式写成可复用模式**，面试前 2 周过完等于把 Alex Xu 体系过完
2. **架构图高质量**：392 张 PNG 全部原创 Excalidraw 风格，尺寸 1300×700 左右，每张支撑一段解释，**信息密度远超 Alex Xu 原书黑白截图**——单凭这些图就有收藏价值
3. **对照价值大于参考价值**：作为「Alex Xu 体系完整中文替代品」有现实需求，但**没有 LICENSE + 明确承认基于付费书的现状，让二次分发/翻译/录视频讲解都踩在版权边缘**——想 fork 前先读这个警示

## 项目展示

仓库 README 无图，但内部 392 张 PNG 是真正的资产。代表性图：

- **Ch 5 Consistent Hashing**：`images/consistent-hashing.png` —— 一致性哈希环 + 虚拟节点 + 受影响区间，三段式直观展示
- **Ch 6 Key-Value Store**：`images/merkel-tree.png` —— 反熵同步树结构，DFS 定位差异
- **Ch 14 YouTube**：`images/dag-video-transcoding.png` —— DAG 视频转码流水线（输入 → DAG 调度器 → 资源管理 → 任务工作者）
- **Ch 4 Rate Limiter**：`images/token-bucket.png` —— 令牌桶算法，配文直接给出漏桶 vs 令牌桶 vs 固定窗口 vs 滑动窗口对比
- **Ch 28 Stock Exchange**：`images/sequencer.png` —— 撮合引擎 Sequencer 单线程串行化设计，配套 "exchange 跑在一台巨型服务器" 的反直觉论断

> 这些图都是 `raw.githubusercontent.com/liquidslr/system-design-notes/main/<chapter>/images/<file>.png` 可直接外链，公众号文章引用无水印。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/liquidslr/system-design-notes |
| Star / Fork | 24,613 / 4,600 |
| 代码行数 | 0 LoC（纯 markdown + 392 张 PNG，~80 MB 二进制） |
| 内容规模 | 28 章 / 29 份 md / ~57,000 词 / 中位 1,700 词/章 |
| 项目年龄 | 21.5 个月（创建 2024-12-24） |
| 开发阶段 | 爆发后冷却（58 天无 commit，0 commits/30d，1 commit/90d） |
| 贡献模式 | 独立开发（liquidslr 占 32/35 commit = 91.4%，bus factor = 1） |
| 热度定位 | 大众热门（24K 星，但 star 增长曲线异常：前 17 个月近乎停滞 → 2026-09~10 垂直飙升） |
| 质量评级 | 内容[中-高] 文档[中] 可维护性[低]（无 LICENSE / 单作者 / 沉睡） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景
Gaurav Kumar（GitHub: liquidslr）：AWS 工程师，纽约，USC CS 毕业，账号 9.5 年（2017-04 注册），2,505 followers / 23 following / 40 public repos，hireable 状态，Twitter `liquid_slr`，个人站 pagefy.io（自研 SEO SaaS）。他真正出圈的是 #2 仓库 `leetcode-company-wise-problems`（31,295 星）——与本仓形成「**求职准备内容矩阵**」（LeetCode 公司题 + System Design 笔记 + pagefy.io 工具化变现）。两个 20K+ 星仓库构成个人品牌双引擎。

### 问题判断
Alex Xu 的《System Design Interview》Vol 1+2 是英文求职圈事实标准，但有两个摩擦：① **全英文**，对非母语求职者阅读速度慢；② **黑白印刷图 + 章节散落**，不方便快速检索和复制面试话术。作者判断：「如果我把全 28 章重写成纯文字 + 重画彩色架构图，会有人用。」这个判断被 24K 星验证——**但其增长曲线（17 个月停滞后突然垂直）说明拐点是社交媒体/Trending 推荐，不是渐进认可**。

### 解法哲学
- **明确选择不做什么**：不写代码示例（绝大多数章节零 code fence）、不做交互演示、不做 SPA（PR #7 提议被搁置）、不做付费墙、不加 LICENSE（这个选择后面会变成最大问题）
- **做一件事做到极致**：把 Alex Xu 体系**忠实转写**到 Markdown，配 392 张原创 Excalidraw 图，让"可读性 + 可检索性"成为壁垒
- **允许社区衍生但不主导**：翻译（PR / Issue #5 土耳其语）、排版衍生（Issue #10 hirdav 461 页精装版）、Agent 接入（PR #6）、SPA 浏览（PR #7）——作者全部客气接收但**不合并、不推动**

### 战略意图
个人内容矩阵中的「系统设计」模块，与 `leetcode-company-wise-problems` 互为入口。变现尝试放在 pagefy.io（个人 SEO 工具 SaaS），而非直接对仓库收费。**本仓库是漏斗顶端内容资产，不是产品本身**——这解释了为什么没有 LICENSE（反正不打算用这个赚钱）和为什么作者 58 天不维护（已经完成它的使命）。

## 核心价值提炼

### 创新之处（按新颖度×实用性排序）

| # | 创新点 | 新颖度 | 实用性 |
|---|---|---|---|
| 1 | **392 张原创 Excalidraw 架构图**替代原书黑白截图 | ★★★★ | ★★★★★ |
| 2 | **4 步面试框架显式时间预算**（Scope 3-10min / High-Level 10-15min / Deep Dive 10-25min / Wrap-Up 3-5min）——原书只讲做什么，这里讲做多久 | ★★★ | ★★★★★ |
| 3 | **把所有数值常量化**——L1=0.5ns、内存=100ns、SSD=150µs、HDD=10ms、同 DC=500µs、跨区域=150ms、99%=3.65d/yr、99.999%=5.3min/yr —— 比原书更易背诵 | ★★★★ | ★★★★ |
| 4 | **Quorum 公式 `W + R > N` 跨章节重复引用**——KV Store、Stock Exchange 都用同一套一致性参数 | ★★★ | ★★★★ |
| 5 | **DAG 视频转码拆解**（Ch 14）——把 YouTube 转码流水线切成输入→DAG 调度→资源管理→任务工作者 4 段 | ★★ | ★★★★ |
| 6 | **mmap 当事件总线**（Ch 28）——把 `/dev/shm` 内存映射文件当微秒级 IPC，比 Kafka 更适合单机低延迟场景 | ★★★ | ★★★ |
| 7 | **"巨型服务器跑交易所"** 反直觉论断（Ch 28）——用一句话打破"分布式 = 更优"的迷信 | ★★★★ | ★★★ |

### 可复用的模式与技巧（**直接偷走的 7 个套路**）

1. **4 步面试框架**（Ch 3）：Scope → High-Level Design → Deep Dive → Wrap-Up，配 3-10/10-15/10-25/3-5 分钟时间预算。**任何系统设计题先在心里默念这套时间盒**。
2. **Quorum 一致性参数三件套**（Ch 6、Ch 28）：`(N, W, R)` 三参数决定一致性，规则 `W + R > N` 强一致；可调 (3,2,2) 默认 vs (3,1,1) 高吞吐 vs (3,3,1) 高可靠。
3. **Consistent Hashing 受影响区间规则**（Ch 5）：节点增减只影响**沿环逆时针到下一个节点**这一段范围，其余节点零迁移；虚拟节点解决热点。
4. **读多写少 10:1 启发式 + 主从复制**（Ch 1 起反复出现）：先按 10:1 假设选主从，读流量放大用 Redis 缓存而非分库，**这是几乎所有 Web 系统起步姿态**。
5. **DAG 异步流水线**（Ch 14）：把任务拆成有向无环图，调度器按依赖顺序派发，资源管理器分槽位，任务工作者拉任务——**这套骨架可以原样套到任何离线计算场景**。
6. **事件溯源做状态转换**（Ch 27、Ch 28）：存不可变事件序列而非可变状态，启用重放/恢复/审计——金融场景标配。
7. **mmap 当单机事件总线**（Ch 28）：撮合引擎这种微秒级延迟场景，把环形队列写到 `/dev/shm` 多进程 mmap，绕过网络栈和内核 IPC。

### 关键设计决策

- **纯文字 + 图，无代码**：把"可读性"放第一位的代价是**没有可运行的例子**，读者无法验证。决策合理：作者瞄准的是"面试前 2 周速通"，不是"动手实现"。
- **章节严格 1:1 对应 Alex Xu Vol 1+2**：保留原书 28 章顺序，**让两本书可以页对页对照**。代价：失去重组的优化空间，章节深度被原书单章深度锁死。
- **不引入新章节（ML/Auth/CDN）**：作者选择忠实转写而非增补，**避免结构偏离原书体系**。代价：体系外的现代主题（推荐系统、身份认证、边缘缓存）完全空白。
- **零 LICENSE**：作者明确放弃版权主张，**默认所有人都可以读，但没有人能合法 fork/翻译/出版**。这是双刃剑——读者自由，作者无护城河。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | liquidslr/system-design-notes | donnemartin/system-design-primer | ByteByteGoHq/system-design-101 | karanpratapsingh/system-design |
|------|---|---|---|---|
| Stars | 24,613 | 373,449 | 90,303 | 46,480 |
| 形式 | 纯文字 + 392 张 PNG | 文字 + Python 代码 | 图 + 短视频 | 文字 + Go 代码 + 图 |
| 章节数 | 28（与 Alex Xu 1:1） | ~17 主题模块 | ~40 短视频配套 | ~30 主题模块 |
| 体系来源 | Alex Xu Vol 1+2 忠实转写 | 社区整理 | Alex Xu 自家官方 | 独立编排 |
| 原创内容 | 极少（主要是图） | 中等 | 高 | 中等 |
| LICENSE | **无** | CC BY-SA 4.0 | 自家许可 | CC BY-SA 4.0 |
| 中文支持 | 全章英文（中文社区靠翻译衍生） | 无 | 无 | 无 |
| 最后更新 | 58 天前 | 2 周前（持续维护） | 4 个月前 | 1 周前 |
| 进入门槛 | 中（57K 英文要硬啃） | 低（Python 代码辅助理解） | 低（视觉化） | 中（Go 代码） |

### 差异化护城河
- **唯一一份"Alex Xu 体系完整 Markdown + 彩色架构图"**——其他仓库要么图少、要么章节不全、要么配大量代码稀释文字密度
- **392 张原创图可外链**——公众号文章、做培训 PPT、面试辅导都能直接引用（**前提：注意版权边界**）
- **作者个人品牌矩阵**——和 31K 星的 leetcode-company-wise-problems 互导，构成求职准备的"系统设计 + 算法"双入口

### 竞争风险
- **最可能被替代的方式**：① ByteByteGoHq 官方把系统设计 101 体系化（已经有 90K 星，作者权威性碾压）；② 中文圈出现合规 LICENSE 的本土化替代；③ AI 助手（Cursor/Claude）让"重读 28 章"变成低价值活动
- **结构性风险**：依赖 Alex Xu 原书体系，**Alex Xu 出 Vol 3 / 修订版即过时**；作者 58 天不更新 + bus factor=1 = 项目寿命与作者个人意愿强绑定

### 生态定位
求职准备赛道「**Alex Xu 体系可视化转写**」的唯一大型存在，填补「英文原书 vs 中文社区笔记」之间的形态空白。**不是教学产品、不是工具、不是社区**，是**一份被社交媒体放大传播的高质量学习材料**。

## 套利机会分析

- **信息差**：高（24K 星但 0 LICENSE + 衍生翻译/排版都处于灰色地带）；但套利空间被版权问题大幅压缩
- **技术借鉴**：极高（7 个可复用模式 + 392 张图都是公开素材，**学习吸收** 0 风险，**再分发** 100% 风险）
- **生态位**：填补「Alex Xu 体系可视化 Markdown 化」空白，但同形态的竞争会很快到来（AI 总结类工具已能 5 分钟生成等价笔记）
- **趋势判断**：增长曲线显示已过峰值（爆发在 2026-09~10），后续大概率缓慢增长；原作者无更新意愿 = 不会有 Vol 3 跟进；**作为求职准备材料会被 AI 工具逐步替代，作为系统设计知识图谱仍有 2-3 年保质期**

## 风险与不足

1. **版权风险（最严重）**：仓库无 LICENSE，但内容显然基于 Alex Xu《System Design Interview》Vol 1+2 2nd Ed 付费书。Issue #10 中用户 hirdav 出版的 461 页精装衍生版本身就是版权边界试探。**任何人/机构二次分发、翻译、印刷、录视频教程、商用培训均面临 Alex Xu 版权方维权风险**。
2. **内容缺口**：没有 ML/推荐系统（现代高频考点）、没有 Auth/Identity（OAuth/JWT/SSO）、没有 CDN/Edge 深度、缺乏可观测性体系（Metrics 有但 Tracing/Logging 无）。
3. **数值过时**：所有 latency 数字（0.5ns / 100ns / 150µs 等）来自 2020 年原书，**未按 2026 年硬件（NVMe SSD、100GbE 网络、persistent memory）校准**。面试时引用可能被追问"现在还是这样吗"。
4. **维护停滞**：58 天无 commit，单作者（bus factor = 1），4 个 PR 挂着（#6 agent skill、#7 SPA frontend 等）——社区有心参与但作者无心力合并。
5. **卫生问题**：Ch 1-16 用 `Readme.md`、Ch 17+ 用 `README.md`，Ch 27 目录名 `27.  Digital Wallet`（双空格），Ch 28 死链 `chapter28` 应是 27。
6. **无代码无法验证**：所有设计都是纸上谈兵，读者**只能靠记忆和面试对练验证**，没有可运行的 mini-implementation。

## 行动建议

- **如果你要用它**：作为「面试前 2 周速通 Alex Xu 体系」的速读材料——**重点是 4 步框架、Quorum 公式、一致性哈希规则、DAG 流水线这 4 个套路**，其余章节按需挑读。**不要全文翻译/二次出版**，如需中文版建议等合规替代品或自行摘要。
- **如果你要学它**：按这个顺序读——Ch 1（Scaling）→ Ch 3（Framework）→ Ch 5（Consistent Hashing）→ Ch 6（KV Store）→ Ch 14（YouTube）→ Ch 28（Stock Exchange）。读完这 6 章就拿到核心套路；其余章节按面试目标选题。**重点抄走 7 个可复用模式的笔记**，面试前一周复习 2 次。
- **如果你要 fork 它**：
  - 改正卫生问题（README casing、Ch 27 空格、Ch 28 死链）
  - 补 LICENSE（建议 CC BY-NC-SA 4.0，明确非商用 + 相同方式共享 + 注明原作者）
  - 加 4 章新内容：ML/RecSys（推荐系统）、Auth（身份认证）、Observability（可观测性三支柱）、CDN（边缘缓存）
  - 更新 latency 数字到 2026 年（NVMe、persistent memory、5G 移动网络）
  - **不要做**：直接翻译出版（Alex Xu 版权方会维权）、做付费课程、把图打包成付费素材

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录 |
| Zread.ai | 未收录 |
| 关联书籍 | Alex Xu《System Design Interview》Vol 1 + Vol 2 2nd Ed（**本仓库的事实基础**） |
| 作者姊妹仓 | [leetcode-company-wise-problems](https://github.com/liquidslr/leetcode-company-wise-problems)（31,295 星，算法求职准备） |
| 作者个人站 | [pagefy.io](https://pagefy.io)（SEO SaaS 变现尝试） |
| 衍生排版书 | Issue #10 — hirdav 排版 461 页精装版（版权试探） |
| 在线 Demo | 无 |

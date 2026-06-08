# 把规则定义权交给社区：ESLint 靠可插拔架构统治 13 年，如今被 Rust 新秀围剿

> GitHub: https://github.com/eslint/eslint

## 一句话总结

ESLint 是可插拔 JS/TS linter 的事实标准——npm 周下载 1.3 亿次，几乎每个现代 JS/TS 项目的隐形依赖。它的胜利不是「规则更多」，而是**架构开放**：2013 年 Nicholas Zakas 在 Box 因「基于正则的 linter 无法强制团队用内部 Ajax 封装」而另起炉灶，用 **AST 精确分析 + 把规则定义权交给社区**（内置 293 规则与第三方规则在引擎里完全平权），击败了规则硬编码的 JSHint/JSLint。引擎硬核是「所有规则 listener 合流到单次 AST 遍历、按 CSS 式选择器特异性分发 + 检查/修复分离的 autofix + 控制流分析」。471K 行 95.6% JS（dogfooding）、13 年、v10.4.1、1194 贡献者（创始人 share 仅 13.1% 极分散）、OpenJS 治理。如今正处行业拐点：**Rust 新秀（Biome/oxlint）用速度围剿 JS 性能软肋**，ESLint 双线反击——universal linter 转型（拼广度）+ v9.34 多线程（补速度）。

## 值得关注的理由

1. **一个「架构决定胜负」的经典案例 + 可迁移的插件契约**：ESLint 的第一性原理是「引擎与规则彻底解耦」——每条规则导出 `{ meta, create(context) }`，`create` 返回**键是 AST 选择器、值是访问器函数**的对象（如 `no-unreachable.js` 返回 `{ BlockStatement: fn, "MethodDefinition[kind='constructor']": fn }`），`meta` 声明式描述能力（type/fixable/hasSuggestions/schema/messages），**引擎在 report 时强制校验「声明与行为一致」**（带了 fix 却没声明 `meta.fixable` 直接抛错）。内置规则与第三方规则经同一 `ruleMapper` 解析、进同一 visitor——规则的生产权交给社区，这才是碾压 JSHint 的根因。「插件 = 导出 visitor 映射 + 声明式 meta + 引擎据 meta 校验行为」是任何可扩展静态分析/转换工具（Babel/PostCSS/codemod）的通用范式。
2. **几个工具引擎的黄金骨架**：① **观察者合流单遍历（merge-then-traverse）**——293 规则的所有 selector→listener 全部 `add` 进同一个 `SourceCodeVisitor`，**整棵 AST 只遍历一次**，每个节点按命中的 selector 用 **CSS 同构的特异性排序**回调（按 node.type 建索引 + selectorCache + 简单选择器快路径优化），避免 O(规则数×节点数）灾难；② **检查/修复分离 + 无冲突应用 + 不动点收敛**——规则只产 `{range,text}` 纯 patch（rule-fixer），`source-code-fixer` 线性扫描跳过重叠 fix、`verifyAndFix` 最多 10 轮迭代到稳定 + 循环震荡检测；③ **控制流分析伪装成 visitor 事件**——昂贵的 CFG 构建封装在引擎，以 `onCodePathSegmentStart` 等「伪节点类型」事件暴露，规则零 CFG 认知即可查可达性；④ **纯计算核心 + IO 外壳分离**（`Linter` 纯内存零文件系统依赖、可打包进浏览器 Playground；`ESLint` 类管 fs/缓存/并行）。
3. **一个「老王朝 vs Rust 新势力」的行业拐点观察样本**：ESLint 的护城河是 13 年稳定契约催生的**数千插件 + typescript-eslint 共生 + airbnb config（14.8 万 star）**生态——后来者用「更快」短期无法复制。但 JS 单核计算是物理软肋，Biome（linter+formatter 一体）/oxlint（快 50-100x）正面攻击；ESLint 的应对是**不拼速度拼广度**：v9 把「语言」抽象成 `Language` 对象（`nodeTypeKey`/`lineStart`/`visitorKeys` 参数化），推出官方 `@eslint/json`/`@eslint/markdown`/`@eslint/css`，从「JS linter」转型「universal linter」；v9.34（2025-08）的 worker 多线程（Atomics 工作窃取）关闭了十年悬案 #3565，但实测仅 1.3-4x 加速、默认还关着——客观反衬「速度差距难靠工程抹平」。

## 项目展示

![ESLint](https://opengraph.githubassets.com/1/eslint/eslint)

> ESLint 是 CLI/库类工具（无 GUI）：espree 解析器 → ESTree AST → Linter 引擎（按节点类型跑规则 visitor）→ 报告问题 + `--fix` 自动修复。官网 eslint.org，文档 eslint.org/docs，293 内置规则 + 数千社区插件。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/eslint/eslint（官网 eslint.org） |
| Star / Fork | 27,303 / 5,019（真实体量在 **npm 周下载 1.3 亿次**——被「装」而非被「赞」的隐形地基） |
| 代码规模 | 471,155 行（**JavaScript 95.6%**，dogfooding 用自己 lint 自己）；2179 文件；注释比 0.221；293 内置规则 |
| 项目年龄 | 约 13 年（2013-06 建库，今日仍活跃打磨控制流分析） |
| 开发阶段 | 密集开发 · 成熟旗舰稳定维护（近 52 周 588 commit ≈ 11/周，2015-16 巅峰后长期平稳） |
| 贡献模式 | **1194 贡献者，创始人 share 仅 13.1% 极分散**（Nicholas Zakas 创始 + Milos Djermanovic 现首席 + OpenJS TSC，无单点依赖） |
| 热度定位 | JS/TS 工具链地基级基础设施 · 可插拔 linter 事实标准 |
| 版本 | v10.4.1（418 tag/100 release，规律 SemVer，13 年向后兼容是生态护城河之根） |
| License | MIT（OpenJS Foundation 持有 IP/商标，不干预日常运作，TSC 自治） |
| 质量评级 | 测试「A+（RuleTester 每规则可单测）」· 代码组织/CI/错误处理「A」· 文档「A-」 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

**Nicholas C. Zakas（创始人，1211 commit）**——2013 年在 Box 任首席架构师时创建 ESLint。直接动机是真实工程痛点：团队要强制使用内部 Ajax 封装函数，但构建系统里基于正则的 linter 做不到这条「语义级」规则，他转而用 **AST 做精确代码分析**。他此前贡献过 JSHint，深知其「规则硬编码、无法扩展」的天花板。著有《Maintainable JavaScript》《Professional JavaScript for Web Developers》，博客 humanwhocodes.com（《Introducing ESLint》2013-07、《The inception of ESLint》2018-02 是一手史料）。**Milos Djermanovic（现首席，830 commit）**——ESLint TSC 成员，负责发版与 feature review，是当前日常维护核心。**OpenJS Foundation 治理**：基金会作中立法律实体持有版权商标、保障独立性但不参与日常决策，实际由 TSC + working groups 运作——「基金会托管 + 社区自治」成熟模型，已彻底去单点依赖。

### 问题判断

2013 年 JS 缺乏「精确且可扩展」的静态检查。当时主流 linter（JSLint/JSHint）两个硬伤：① **基于正则/词法的近似匹配**，无法理解语法结构（「这个变量是否真未使用」需作用域分析，正则做不到）；② **规则集硬编码在工具内部**，用户无法新增团队专属规则。JSHint 是 JSLint 的「可配置 fork」，但**可配置 ≠ 可扩展**——它放开了内置规则的开关，却没放开「规则本身」的定义权。

### 解法哲学（AST 精确 + 可插拔 + autofix）

三条哲学贯穿全代码库：① **一切以 AST 为真相**——espree 解析出 ESTree，所有规则在节点上工作而非文本；② **引擎与规则彻底解耦**——引擎只负责遍历和分发，规则是外部可插拔模块，用户/插件作者与内置规则享受完全相同的 `create(context)` API；③ **检查与修复分离**——规则只「描述」如何修（产出 `{range,text}`），引擎负责「无冲突地应用」。从 JSHint 学到的核心教训是「硬编码规则集是死路」，ESLint 把它反过来——**规则的生产权交给社区**，这是它最终碾压 JSHint 的根因（不是规则更多，而是规则的生产权开放了）。

### 战略意图（事实标准 + universal linter 反击 Rust + OpenJS）

面对 Biome/oxlint 的 Rust 速度攻击，ESLint 选择**不在速度上正面硬刚，而在广度/抽象上筑墙**：v9 把「语言」抽象成 `Language` 对象接口，推出官方 `@eslint/json`/`@eslint/markdown`/`@eslint/css` 插件，从「JS linter」转型「universal linter」——用「一个引擎 lint 所有语言 + 数千插件生态」对冲「一个语言快 50 倍」。v9.34 落地的多线程是迟到十年的并行性能补课。

## 核心价值提炼

### 创新之处

1. **AST 选择器即规则寻址语言（esquery + 特异性排序分发）**（新颖度 4/5，实用性 5/5，可迁移性 4/5）：规则用 `IfStatement > BlockStatement`、`MethodDefinition[kind='constructor']` 这类 CSS 式选择器声明关注点，引擎按 CSS 同构特异性排序回调，单遍历分发做到高效（node.type 索引 + cache + 快路径）。适用任何让用户用声明式 query 钩住 AST/树结构的场景。
2. **检查/修复分离 + 无冲突应用 + 不动点多轮收敛**（新颖度 4/5，实用性 5/5，可迁移性 5/5）：规则只产 `{range,text}` 纯描述，应用器线性扫描跳过重叠、最多 10 轮迭代到稳定 + 循环震荡检测。适用 codemod、auto-fix、格式化器。
3. **控制流分析伪装成 visitor 事件**（新颖度 5/5，实用性 4/5）：把昂贵的 CFG 构建封装在引擎，以 `onCodePathSegmentStart` 伪节点类型事件暴露，规则零 CFG 认知即可查可达性。适用需给插件提供全局分析又不想暴露内部复杂度的引擎。
4. **`Language` 对象抽象（universal linter）**（新颖度 4/5，实用性 4/5）：用 `nodeTypeKey`/`lineStart`/`visitorKeys`/`parse`/`matchesSelectorClass` 把「语言」参数化，一套选择器/修复/指令机制通吃 JS/JSON/CSS/Markdown。适用从单语言工具向多语言平台演进。
5. **声明式 meta 驱动的能力校验**（新颖度 3/5，实用性 4/5，可迁移性 5/5）：规则用 `meta.fixable`/`hasSuggestions`/`schema` 声明能力，引擎在 report 时强制「声明与行为一致」否则抛错。适用任何插件体系约束第三方契约。

### 可复用的模式与技巧

- **观察者合流单遍历（merge-then-traverse）**：N 个独立访问者注册到一棵树，单次 DFS 按节点类型索引分发——「多分析器共享一棵 AST」避免 O(分析器×节点)。
- **纯 patch 描述 + 冲突消解应用器 + 不动点迭代**：变换逻辑只产 `{range,text}`，应用与收敛交给统一引擎——codemod/formatter/auto-fixer 通用骨架。
- **声明式 meta + 运行时契约校验**：插件用 schema/能力位声明自己，宿主据声明校验行为并拒绝不一致——开放插件生态的自我保护。
- **昂贵全局分析事件化**：把数据流/控制流分析结果以「与遍历同构的事件」暴露，下游零成本消费——解耦引擎复杂度与插件认知负担。
- **纯计算核心 + IO 编排外壳分层**（Linter vs ESLint）：核心零文件系统依赖以求可嵌入/可测，外壳管 fs/缓存/并行。
- **无锁工作窃取**：`Atomics.add` 共享计数器做动态任务分发——Node worker_threads 并行负载均衡的轻量方案。

### 关键设计决策

最值得记录的是 **「观察者合流单遍历 + AST 选择器特异性分发」的引擎核心**——它让「数百条规则同时跑」从性能灾难变成单次遍历，是 ESLint 可插拔架构能规模化的工程命门。决策：293 条规则若各自独立遍历一遍 AST 就是 O(规则数×节点数) 灾难。方案：`runRules` 先遍历所有启用规则，把每条规则返回的每个 selector→listener **全部 `visitor.add()` 进同一个 `SourceCodeVisitor`**，然后整棵 AST 只遍历一次；每进入/离开一个节点，由 `ESQueryHelper.calculateSelectors` 算出该节点命中的所有 selector，**按特异性（attributeCount → identifierCount → 字母序，与 CSS 选择器优先级同构）排序依次回调**。性能细节拉满：按 `node.type` 建索引只对可能命中的 selector 做匹配、selectorCache 缓存已解析选择器、纯标识符/通配符走快路径绕开 esquery 完整 PEG 解析。Trade-off 很真实：单遍历换来规则间执行顺序由特异性决定（而非注册顺序，规则作者需理解这套语义）；共享遍历意味着一条规则的异常会污染整次遍历（用 `addRuleErrorHandler` 给异常打 `ruleId` 标签兜底）。这套「N 个观察者注册到一棵树、单次 DFS 按节点类型分发」是 visitor 模式的工程化标准答案，配合「检查/修复分离的 autofix」「CFG 事件化」「Language 抽象」共同构成了 13 年屹立的引擎。

> 性能补课注记：v9.34 的 worker 多线程用 `Atomics.add(filePathIndexArray, 0, 1)` 在共享内存做无锁工作窃取（谁空闲谁抢下一个文件），但现实加速仅 1.3-4x（worker 启动/序列化开销 + 配置每线程重复加载 + JS 单核软肋），v10.4.1 默认 `concurrency:"off"`——恰反衬 Rust 新秀的速度优势难靠工程抹平。

## 竞品格局与定位

| 项目 | 定位 | 与 ESLint 关系 |
|------|------|------|
| JSHint / JSLint | 硬编码前辈 | 本质代差：规则硬编码在工具内、基于正则近似；ESLint 把规则定义权外放 + AST 精确分析取胜。**不是功能更强赢的，是架构开放赢的** |
| Biome (Rome 继任) | Rust linter+formatter 一体 | 比 Node 快 10-20x、单工具替代 ESLint+Prettier；但插件生态远不及，复杂场景规则覆盖不足 |
| Oxc / oxlint | Rust 极速 linter | 快 50-100x（v1.0 已发）；但仅 lint 无 formatting/autofix，定位「加速器」而非完整替代，且主要兼容/搬运 ESLint 规则而非自建生态 |
| Prettier | 代码格式化器 | **互补非竞品**：管格式不管质量，常与 ESLint 搭配（ESLint 逐步把纯格式规则剥离到 @stylistic） |
| typescript-eslint | 建在 ESLint 上的 TS 层 | **共生关系**：让 ESLint 成 TS 项目默认 linter，是 ESLint 杀手级护城河 |

### 差异化护城河

① 13 年稳定的可插拔规则契约催生的**数千插件生态**；② **typescript-eslint** 杀手级共生（TS 静态检查事实入口）；③ **universal linter 转型**带来的广度。三者都是后来者用「更快」无法短期复制的。

### 竞争风险

- **JS 性能软肋**：单核计算物理短板，v9.34 多线程仅 1.3-4x、默认关闭，面对 Rust 新秀在大型 monorepo 上速度差距明显。
- **Rust 新秀速度碾压**：Biome/oxlint 快几十倍，攻击 ESLint 最痛的性能面（#3565 悬了十年）。
- **flat config 迁移阵痛**：v9 默认 flat config、30+ 破坏性变更、插件支持不齐，大量团队滞留 v8，官方被迫推 Config Migrator/Inspector 救场。

### 生态定位

JS/TS 工具链不可替代的「规则引擎地基」，正从「JS linter」向「多语言代码质量平台」迁移以延长统治期。

## 套利机会分析

- **信息差**：ESLint 是「人人在用却少有人懂其架构」的隐形巨头，又正处「老王朝 vs Rust 新势力」行业拐点。中文圈对「merge-then-traverse 单遍历引擎 + esquery 特异性分发」「检查/修复分离 + 不动点 autofix」「CFG 事件化」「Language 抽象 universal linter」的工程拆解稀缺；「可插拔架构如何赢得 linter 之战」「速度 vs 生态」也有强叙事。
- **技术借鉴**：观察者合流单遍历、纯 patch + 冲突消解 + 不动点、声明式 meta 契约校验、全局分析事件化、纯核心/IO 外壳分层、Atomics 工作窃取——远超 lint 本身，可迁移到任何 AST 工具/codemod/formatter/插件引擎。
- **生态位**：可插拔规则引擎地基；与 JSHint（被取代）、Biome/oxlint（速度对手）、Prettier（互补）、typescript-eslint（共生）。
- **趋势判断**：踩在「代码质量 + AST 工具链 + 多语言」趋势上；长期看「Rust 阵营能否复刻其插件生态 + ESLint universal linter 转型能否成功 + 性能差距能否缩小」决定其统治能否延续。

## 风险与不足

- **JS 性能结构性软肋**：多线程补课收益有限（1.3-4x、默认关），Rust 新秀速度难以工程抹平。
- **flat config v9 迁移阵痛**：30+ 破坏性变更、插件支持不齐、团队滞留 v8。
- **CFG 复杂度**：`code-path-state.js`（71KB）等控制流状态机是高复杂度维护热点。
- **注释比 0.221 偏低**：对 471K 行强调可扩展的引擎而言，深层算法对新贡献者门槛高（侧证 share 仅 13.1% 极分散但强依赖核心维护者）。

## 行动建议

- **如果你要用它**：JS/TS 项目的代码质量基线首选（搭配 typescript-eslint + Prettier + 共享配置如 airbnb/antfu）；v9+ 用 flat config（eslint.config.js）；大型 monorepo 性能敏感可试 `--concurrency` 多线程，或用 oxlint 做快速预检 + ESLint 做完整规则覆盖。新项目直接上 flat config，老项目迁移用官方 Config Migrator。
- **如果你要学它**：直奔 `lib/linter/linter.js`（merge-then-traverse 引擎 + runRules 分发）+ 一个规则（`lib/rules/no-unreachable.js`，create/meta + CFG 事件消费）+ `lib/linter/source-code-fixer.js`（autofix 冲突消解 + 不动点）+ `lib/linter/code-path-analysis/`（控制流事件化）+ `lib/languages/js/`（Language 抽象）+ `lib/rule-tester/`（每规则可单测）。这是「AST 工具引擎 + 可插拔插件契约 + autofix」的架构范本。
- **如果你要 fork / 借鉴它**：观察者合流单遍历、纯 patch + 冲突消解 + 不动点、声明式 meta 契约校验、全局分析事件化、Atomics 工作窃取是可直接迁移的设计。MIT 友好；这套引擎架构尤其值得任何做 AST 静态分析/codemod/格式化/可扩展插件平台的项目研读。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/eslint/eslint（分层架构 + Linter/ESLint 职责分离 + 并发性能，架构速读首选） |
| 官方文档 | https://eslint.org/docs/latest/（Custom Rules / Architecture / flat config 迁移指南 / 治理页） |
| 官方博客（战略） | 多线程 /2025/08/multithread-linting/ · CSS 支持 /2025/02/eslint-css-support/ · v9.0.0 /2024/04/eslint-v9.0.0-released/ |
| 创始人博客（项目史） | humanwhocodes.com（《Introducing ESLint》《The inception of ESLint》） |
| RFC 仓库 | github.com/eslint/rfcs（重大设计提案，如多线程 RFC #129） |

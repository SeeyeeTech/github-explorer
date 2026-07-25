# GitHub推荐：33 个月 13.4K stars：Automattic 的离线语法引擎 Harper 怎么把 Grammarly 切成「本地快、私有硬」

> GitHub: https://github.com/automattic/harper

## 一句话总结

Harper 是 Automattic 推出的开源本地优先英语语法检查器，用 Rust 写一个可嵌入 IDE/CLI/浏览器/WASM 多端的语法检查「迷你引擎」，在 <10ms 反馈、本地 100% 离线、Apache-2.0 三件套上精确卡位，避免 Grammarly 的云端/LLM 隐私成本和 LanguageTool 的臃肿。

## 值得关注的理由

- **不是又一个 language server** —— 核心引擎 `harper-core` + 4 个 host（CLI / LSP / WASM / Tauri 桌面）+ 9 个编辑器扩展（VS Code / Cursor / Obsidian / Neovim / Helix / Emacs / Zed / Sublime / WordPress），靠「瘦 IR + 多 surface」做到一份规则四处跑。
- **300 条 lint 规则全部是白盒可审计代码** —— 没有黑盒模型，规则作者用 `SequenceExpr` DSL 描述模式，规则文件平均 50–200 行；可被外部开发者 Review、被 Issue 复现。
- **FST 词典 + 形态学派生** —— 786KB 的 `dictionary.dict` 配上基于 Brill Tagger 的 POS 标注层，单词识别在 1ms 量级；这是 Harper「极快」的工程底色，不是营销说辞。
- **Apache-2.0 + 持续 22% 月度 commit 增长** —— Automattic 把这玩意儿做成 Editor 基础设施形态而非产品形态，避开了与 Grammarly 直接商业对抗。

## 项目展示

### Hero
1. ![Harper Logo](https://raw.githubusercontent.com/automattic/harper/master/logo.svg) — 官方 SVG logo（直接嵌 README 头部）

### 在线 Demo
2. [Harper Stats Playground](https://automattic.github.io/harper/stats/#playground) — 浏览器内实时校对，WASM 部署，可直接粘文本看 lint 输出
3. [官方 Demo](https://writewithharper.com/demo) — 官网交互式演示

### 社区可视化
4. ![Contributors](https://contrib.rocks/image?repo=automattic/harper) — 贡献者墙（贡献者墙由 contrib.rocks 生成，从中可直观看到核心维护者 Elijah Potter 的高占比）

> 仓库内部无 README 嵌入截图（只有 logo），展示素材以官方 Playground + 官网为主。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/automattic/harper |
| Star / Fork | 13,395 / 506 |
| Watcher / Open Issues / Open PRs | 32 / 563 / 127 |
| 代码行数 | 246,558（Rust 41.6% 102K / JSON 32.9% 81K 字典 / YAML 15.1% CI / TypeScript 6.2% / Svelte 1.9%） |
| 纯 Rust 逻辑代码 | ~125K 行（去掉字典/CI） |
| 项目年龄 | 33 个月（2023-10-22 首 commit） |
| 开发阶段 | 密集开发（近 30 天 88 commits，月均 ~100，2025 Q1 大重构期单月最高 592） |
| 贡献模式 | 核心少数 + 社区（135 贡献者，主作者 Elijah Potter 占 46.4%，第二档 Andrew Dunbar 14.6%） |
| 热度定位 | 大众热门（3 年从 0 涨到 13.4K Star，编辑器集成全覆盖） |
| 质量评级 | 代码优秀 / 文档优秀 / 测试充分 |
| 最新版本 | v2.6.0（共 226 tag，100 正式 release，semver 严格） |
| 许可证 | Apache-2.0 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Elijah Potter（GitHub: `elijah-potter`）是 Automattic 的工程师，主业负责 WordPress.com Gutenberg block editor 的拼写检查。这条线索至关重要：它意味着 Harper 起点不是「学界研究」也不是「业余 side project」，而是**「公司在用 Grammarly，但不想给竞争对手交钥匙」**这条清晰动机。

项目由 Automattic 官方组织账号持有，license 是 Apache-2.0（非 AGPL/商业双 license），可以解读为 Automattic 意图把 Harper 培养成开放生态而非封闭产品。从 165 个贡献者中除 Elijah Potter 外，Andrew Dunbar（653 commits，Automattic 员工）和 hippietrail（397 commits，疑似国际化/语言学社区老兵）构成第二梯队，公司层面有持续投入但不是封闭的内部项目。

### 问题判断

仔细读 README 三段抱怨（Grammarly 太贵 + 缺上下文 + 隐私噩梦 / LanguageTool 内存爆炸 + 16GB n-gram 数据集 + 几秒延迟），叠加 GitHub Issue #79（74 评，全是「多语种支持」请求）和「Markdown 友好」「术语一致性」三类高频诉求，**Harper 的问题域不是「更好的语法检查器」，而是「Grammarly 和 LanguageTool 中间的卡位真空」**：

- Grammarly「云端 + LLM + 订阅」三件套对开发者/技术写作者**过度杀伤**（隐私 + 延迟 + 锁定编辑器）
- LanguageTool 虽是开源但「服务端依赖 + 16GB n-gram」让 CI 集成毫无可能
- 纯文本 tool（write-good / proselint）只到「风格指针」深度，缺语法/术语

### 解法哲学

Harper 选了 5 条明确「不做什么」+「要做什么」：

- **不做 ML/black box** —— README 原话「全部规则都白盒可读」，300 条规则都是 Rust 源码 + SequenceExpr DSL，开发者可以在 PR 里挑战
- **不做云端服务** —— 「100% 离线」是品牌承诺；Harper Lens（Web 版）把 Rust 编译成 WASM，浏览器里跑同一份 `harper-core`
- **不做沟通协议分裂** —— LSP / WASM / CLI / 桌面端都消费同一份 `harper-core`，靠 Cargo workspace + feature flag 隔离
- **不做 General-purpose Linter** —— 专注英文（Planned 多语种），先把单语种做到 Grammarly 深度
- **做 IDE 一等公民** —— `harper-ls` 是 first-class crate（不是「examples 之一」），tower-lsp-server 提供 LSP 协议

### 战略意图

在 Automattic 大图景里，Harper 是「**拥有自己的内容理解引擎**」战略的载体：避免给 Grammarly/SAP 之类的公司交钥匙，并在 WordPress.com / Tumblr / DayOne 等 Automattic 资产里排他性集成。商业模式不直接来自订阅，而来自 Automattic 系产品的写作质量提升 + 来自大型 CMS 的 B2B 集成。开源 + Apache-2.0 抢占上游开发者心智，把 Harper 培养成「AI 时代真人写作」的参考实现。

> 官方文档（writewithharper.com）核心叙事点：价值主张（本地 + <10ms + 隐私）、差异化（永远不改写你的本意）、目标用户（编辑器重度用户 + 隐私敏感用户）。设计哲学已在 README 开篇三段明确书写。

## 核心价值提炼

### 创新之处

**1. 「瘦 IR + 多 Host」架构**（新颖度 4/5，实用性 5/5，可迁移性 5/5）
- `harper-core` 内置轻量化 tokenizer（词/标点/数字/空白四类）+ span metadata
- 所有 lint 规则只读这一层 IR，不依赖 tree-sitter / markdown-it / LSP 边界
- 同一份核心被 CLI / LSP / WASM / Tauri 桌面端消费，0 规则漂移
- 适用场景：所有「需要在前端/WASM/CLI 三端同步」的语言学/格式化工具

**2. `Expr` DSL — 规则作者友好**（新颖度 4/5，实用性 5/5，可迁移性 4/5）
- `harper-core/src/expr/` 暴露 `SequenceExpr`、`FirstMatchOf`、`Repeating`、`AnchorStart` 等 21 个组合子
- 规则代码读起来像「English with type」而非 regex 拼凑
- 例：从 `Parser` → `Document` → `ExprLinter` 框架，单条规则 50–200 行
- 适用场景：lint 工具、pattern-matching DSL、声明式规则引擎

**3. FST 词典 + Levenshtein 自动机模糊匹配**（新颖度 4/5，实用性 5/5，可迁移性 4/5）
- `harper-core/src/spell/fst_dictionary.rs` 使用 `fst` crate 构造 FST 索引
- 模糊匹配用 `LevenshteinAutomaton`（edit distance ≤ 3，置换 cost 1）
- thread_local 缓存 automaton builder（构造昂贵、参数稳定）
- 786KB 词典 + 1ms 量级查词是 Harper「<10ms」的工程底色
- 适用场景：拼写检查、搜索建议、生物序列匹配

**4. `Lint` × `Suggestion` 显式分类**（新颖度 3/5，实用性 5/5，可迁移性 5/5）
- `Lint` = 问题描述（span + kind + suggestions + message + priority）
- `Suggestion` = enum 三态：`ReplaceWith(Vec<char>)` / `InsertAfter(Vec<char>)` / `Remove`
- IDE 端先收到 Diagnostic + Suggestion[]，由用户/IDE 决定是否 apply；rule 内只描述问题，永远不自动改
- `Suggestion::apply()` 方法同时是「character-level diff 元数据」，精确替换
- 适用场景：所有带 code-action 的 lint/formatter

**5. `Weirpack` — 第三方规则打包格式**（新颖度 5/5，实用性 3/5，可迁移性 4/5）
- `harper-core/src/weirpack/` 提供类似 Chrome Extension 的 zip 打包格式
- 一个 zip = 多个规则 + 可选 dictionary + 可选 annotations + manifest
- 第三方可以为 Harper 写 rules-pack 而非 fork（Weir 是 Harper 自研的 mini-rule language）
- 适用场景：可扩展 lint 框架、规则市场、领域包

**6. Brill Tagger 集成做 POS 标注**（新颖度 3/5，实用性 4/5，可迁移性 3/5）
- 引入 `harper_brill`（自 crate）做 Brill Tagger + Chunker
- `Document::new` 时调用 `brill_tagger()` 给每个 token 打 UPOS
- 规则可以用 `upos_set!` 表达「动词 + 形容词」这类语法模式
- 适用场景：NLP 工具、形态学标注、教学工具

**7. `MergedDictionary` 分层 + 优先级合并**（新颖度 3/5，实用性 5/5，可迁移性 5/5）
- `FstDictionary`（不可变 curated default）+ `MutableDictionary`（用户/文件级）
- 启动时按优先级合并成单一 feed 给 linter
- 用户可以加 `.harper-dict.txt`，团队可以发布 `harper-team-dict`
- 适用场景：所有支持自定义词典的语言工具（vale / proselint / textlint）

### 可复用的模式与技巧

1. **「瘦 IR + 多 Host」** — 用 wasm-friendly 自研 IR 共享 CI/CLI/LSP/WASM 四端实现；适合 monorepo 工具同时发布 VS Code 扩展、CLI、浏览器版、SaaS
2. **「Lint → Suggestion → Fix」三段显式分离** — 把 lint 的 read-only 输出与 write-only 自动修复隔开，UTF-8 char 数组操作避免字符串切片；适合 IDE code-action 工具、AI 辅助修改提示
3. **「Expr DSL + Linter Trait」** — `pub trait Linter { fn lint(&mut self, &Document) -> Vec<Lint>; fn description(&self) -> &str; }` 极简抽象；适合规则/插件系统
4. **「thread_local Automaton Builder 池」** — 计算昂贵、参数稳定的对象用 thread_local 缓存；适合 hot-path 上的 DFA/parser 构建
5. **`char` slice 而非 `&str`** — 全文处理用 `Vec<char>` + `Span<char>`（字符索引而非字节索引），避免 UTF-8 边界坑；适合任何需要「字符级可逆」操作的文本工具
6. **`LazyLock` + 静态 FST 字典** — `LazyLock::new(...)` 保证词典只初始化一次；适合需要「启动快 + 运行时零延迟」的内置静态资源
7. **「Rule files placed alphabetically in `linting/`」** — 300 条规则按文件名字母排序而非分类，pull request 后可通过「文件位置 + 历史」直接追溯；适合超大规模规则库
8. **`render_markdown` 内置到 lint message** — `Lint::message_html()` 直接把 message 渲染成 HTML，IDE 端无需重写；适合「规则描述富文本」需求

### 关键设计决策

1. **决策: 自研 token span IR 而不是直接消费 CST/AST**
   - 问题: 直接基于 markdown-it / tree-sitter-markdown 做 IR 会导致 LSP/WASM/CLI 各自解析一份，lint 规则不可复用，且 WASM 体积爆炸
   - 方案: `harper-core` 内置轻量化 tokenizer（词/标点/数字/空白四类）+ span metadata；所有 lint 规则只读这一层 IR
   - Trade-off: 解析精度受限于 token 边界（不能跨 token 引用），写规则时偶尔需要回退到邻接 span；换来 ~10x 体积压缩与多端一致性
   - 可迁移性: 高

2. **决策: Linter 与 Suggestion 显式两段**
   - 问题: 一边 lint 一边自动修复常常把「不该改的地方」改了，AI 校对产品的最大抱怨之一
   - 方案: `Lint` 只产出 `Suggestion` 与 `Message`，`Suggestion` 内部 `apply()` 是「单字符级别」可逆重写元数据；IDE 端必须先接收 Diagnostic + Suggestion[]，由用户/IDE 决定是否 apply
   - Trade-off: 多写一遍 `Suggestion` enum 但获自带的「可写 fix」与「可拒绝 fix」二元选择；规则作者工作量下降，跨 surface 表现一致
   - 可迁移性: 高

3. **决策: 4 个 host 共享 `harper-core` 通过 Cargo workspace + feature flag**
   - 问题: 用户场景横跨编辑器（IDE）、CI（pre-commit）、浏览器（Lens）、服务端（Worker）。若每个 host 自己调 linter，会出现规则漂移
   - 方案: `harper-cli` / `harper-ls` / `harper-wasm` / `harper-desktop` 4 个 crate 各自只是「protocol binding」，core 仅 1 份
   - Trade-off: 对 core crate 的 API 兼容要求极高——升级要兼容 4 个 hosts；换来 0 规则漂移 + 1 处代码变更多端受益
   - 可迁移性: 高

4. **决策: WASM 编译到浏览器做 Harper Lens**
   - 问题: SaaS 校对产品强制把文本发到云，Harper 目标用户对隐私极度敏感
   - 方案: `harper-wasm` 编译成 `wasm32-unknown-unknown` 绑定给 JS，配合 Svelte UI 部署在 GitHub Pages / Cloudflare Pages；客户端文本从不上行
   - Trade-off: 浏览器运行时内存峰值相对 Node 高 ~30%，需要分块处理长文（>100k 字符）；换来「不可信服务端」用户也能用
   - 可迁移性: 中

5. **决策: `Weir` + `Weirpack` 第三方规则扩展机制**
   - 问题: 300 条规则覆盖不了所有领域（医学/法律/金融），又不想 fork 仓库
   - 方案: 自研 mini-rule language `Weir` + zip 打包格式 `Weirpack`，第三方可发布 pack
   - Trade-off: 多维护一个 DSL；但换取「无需 fork 即可贡献」+ 规则生态可独立演化
   - 可迁移性: 中

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | Harper | Grammarly | LanguageTool | write-good / proselint |
|------|--------|-----------|--------------|----------------------|
| 部署形态 | 本地 + 浏览器 WASM | 云端 SaaS | 自托管 / SaaS | 纯本地静态 linter |
| 运行速度 | <10ms | 网络延迟 100ms+ | 服务端 1-3s | 即时但规则浅 |
| 隐私 | 100% 离线，默认无遥测 | 上传云端 + LLM 训练 | 服务端依赖 | 100% 离线 |
| 语言覆盖 | 仅英文（多语种路线图） | 25+ 语种 | 30+ 语种 | 仅英文 |
| License / 价格 | Apache-2.0 / 免费 | 闭源 / $12-15/月 | LGPL / 自托管免费 + SaaS 付费 | MIT / 免费 |
| 编辑器集成 | VS Code/Cursor/Obsidian/Neovim/Helix/Emacs/Zed + 9 个 | 主要浏览器 + Office | 浏览器扩展 + HTTP API | 需自己集成 |
| Lint 规则深度 | 300 条白盒 Rust | ML 黑盒 + 上下文 | 规则 + n-gram 统计 | 静态风格指针 |
| 可定制化 | 高（`.harper-dict.txt` + JSON config） | 低 | 中（自托管可改规则） | 中（写正则） |
| 形态学建模 | Brill Tagger + POS | 闭源 | n-gram + 统计 | 无 |

### 差异化护城河

- **技术护城河**：「Local-first + Rule-based + IDE-native + Markdown-aware + 多端 core 一致」五位一体；任何竞品想抄都需要同时支持这五条，门槛高
- **生态护城河**：9 个编辑器集成 + 9 个前端包（chrome/obsidian/vscode/wordpress 等）是时间壁垒，Grammarly 复制需要 3 年开发
- **信任护城河**：Apache-2.0 + Automattic 母品牌 + 100% 离线承诺 = 隐私敏感用户的默认选项

### 竞争风险

- **AI 编辑器（Cursor / Copilot / Cody）正在把基础拼写语法检查吸收进「on-write change」** —— 可能在 IDE 内部端掉 linter-served rule 的需求；Harper 通过与 Cursor 等 IDE 的 LSP 集成可缓解，但不能化解「AI suggestion 即改即纠」的趋势
- LanguageTool 加快本地化（Rust 重写） + Grammarly 加快本地离线版（已宣布）会同时进攻「本地优先」核心卖点
- 多语种路线图（Issue #79）如果 12 个月内不落地，会被 LanguageTool 抢回「开源多语种」心智

### 生态定位

锁死两个 niche：① Automattic 系编辑器产品内部（Gutenberg / WordPress.com / Tumblr）；② 工程团队 CI/CLI 写作质量（`harper-cli` 接 git pre-commit）。是 Grammarly、LanguageTool、vale、proselint 之间的**缝隙生存位**；通过开源态度还能把社区贡献作为护城河。

## 套利机会分析

- **信息差**: 13.4K Star 但中国大陆开发者很少提及（Grammarly 仍是默认推荐）；对国内想「弃用 Grammarly 转开源」的工程师/写作者，Harper 几乎是「百度不知道 / 知乎不会主动推荐」但实际可用的方案
- **技术借鉴**: 「瘦 IR + 多 Host」 + `Expr` DSL + `Suggestion` enum 三件套是值得抄的；任何想在 monorepo 里把一份核心部署到 CLI/LSP/WASM/桌面端的工具都可借鉴
- **生态位**: 「写作基础设施」赛道里「本地优先 + 白盒规则 + IDE 集成」三件套目前 Harper 独一档；可以作为 Slack 内部 lint、私有 CMS 写作工具的底层引擎
- **趋势判断**: 隐私 + AI 反感 + IDE 化是 2026-2028 的清晰趋势，Harper 站位精准；多语种 + 桌面端稳定性是短期突破点

## 风险与不足

- **多语种纯属路线图**：Issue #79 上 74 条评论全是「请加中文/日文/法文」，但 README 第一段就写「英语语法检查器」；中文用户要把 Harper 改成自己的中文校对工具，需要 fork + 自训 token
- **桌面端稳定性**：#3565 报告「MacOS APP - nothing happens」22 评未解决，Tauri 桌面端在 macOS 启动崩溃
- **CI/CD 工具链复杂度**：4 个 host + 9 个 editor 包 + 多 feature flag 组合，Rust release 流程相对 easy，但 release-debug profile 注释「wasm-opt strip bug」是工程债务
- **Linter 自身缺 lint**：源代码 `Lint` struct 字段 `priority: u8` 注释「Lower = more important」反直觉，存在历史包
- **依赖 22 个 core crate + 9 个 satellite 包**：单 `cargo build` 已耗 5-10 分钟，贡献者引导成本偏高
- **社区维护话语权集中**：Elijah Potter 占 46.4% + Andrew Dunbar 14.6%，前两人占 61%；单人辞职/转向是单点风险

## 行动建议

- **如果你要用它**: 立刻在 VS Code / Cursor 装 Harper 插件（5 秒级反馈）；CI 用 `harper-cli lint --format json` 卡 PR；`.harper-dict.txt` 维护团队术语；多语种需求暂等
- **如果你要学它**: 重点读这 5 个文件：
  - `harper-core/src/document.rs` — IR + 解析 + 标注的入口
  - `harper-core/src/spell/fst_dictionary.rs` — FST 词典 + Levenshtein 自动机
  - `harper-core/src/linting/mod.rs` — Linter trait + LintGroup 聚合
  - `harper-core/src/linting/suggestion.rs` — 三态 Suggestion enum
  - `harper-core/src/expr/mod.rs` — 21 个组合子的 DSL
- **如果你要 fork 它**:
  - 加中文/日文/法文：复制 `harper-typst` 的 `Parser` 接口范式，新增 `harper-zh` crate + 新词典
  - 把 Suggestion 升级为 `Replace { exclude_chars: Vec<char> }` 解决「粘连词」场景
  - 把 `brill_tagger` 抽成 `harper-pos` plugin，把 multilingual 路径打通

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/automattic/harper |
| Zread.ai | 未单独验证（DeepWiki 已覆盖） |
| 关联论文 | 无（工具型项目，预期内） |
| 在线 Demo | https://automattic.github.io/harper/stats/#playground（GitHub Pages WASM） |
| 官方文档 | https://writewithharper.com |
| 贡献指南 | https://writewithharper.com/docs/contributors/introduction |
| Discord | https://discord.com/invite/JBqcAaKrzQ |

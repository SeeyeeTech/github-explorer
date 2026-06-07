# 18 个月、35k 行代码、一人写完 8.5K stars 的本地 AI 笔记：Reor 把 RAG 装进 Markdown 编辑器后归档了

> GitHub: https://github.com/reorproject/reor

## 一句话总结

Reor 是把「人类写作」和「LLM 检索」做成对等两个生成器、共享同一向量库的本地优先 AI 笔记桌面应用——曾经是 GitHub 上极少数把「AI 原生 + Local-First」都做到位的范式项目，2025-05 主开发停摆，2026-03 被归档，但它的 dual-generator 架构与 LanceDB 实战至今仍是同类产品最有借鉴价值的参考实现。

## 值得关注的理由

- **稀缺的双生成器范式**：在 AI 笔记工具里，多数产品要么走「ChatGPT 套壳 + 知识库」路径（AnythingLLM），要么是「Obsidian + Copilot 插件」那种「AI 事后加上去」的缝合。Reor 是少数把「AI 检索」和「写作流」做到原生同一个向量子系统的工具。
- **单兵干出 35k 行 TS/TSX 的工程纪律**：从 IPC 强类型、LanceDB schema 自愈、Ollama 三级降级、到 chokidar 与编辑器 debounce 解耦，作者把「做一个能落地的本地 AI 应用」所需的所有工程细节都做了。
- **AGPL-3.0 + Local-First + 单人主导航量**：三条选择叠加，让 Reor 同时是产品范式、协议范式与「独立项目如何死掉」的反面教材，看完可以同时学到正面与负面教训。

## 项目展示

### README 媒体

1. ![Reor Logo](https://raw.githubusercontent.com/reorproject/reor/main/logo_or_graphic_representation.png) — 类型: logo
2. [reor.mov 演示视频](https://github.com/reorproject/reor/raw/main/reor.mov) — 类型: demo 视频

> 官网原 <https://reorproject.org> 已 301 跳转，2026-03 归档后域名被释放，无有效官网媒体。仓库内 `reor.mov` 是作者留下的唯一完整 Demo 视频。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/reorproject/reor |
| Star / Fork | 8,563 / 525 |
| 代码行数 | 71,015 行（真代码约 35,715 行：TS 23,744 + TSX 11,971） |
| 项目年龄 | 31.2 个月（首提交 2023-10-31，最后提交 2025-05-13） |
| 开发阶段 | 已放弃（2026-03-07 archive；近 365 天 commit = 0） |
| 贡献模式 | 独立开发者（samlhuillier 占 64%，34 名贡献者） |
| 热度定位 | 大众热门（8.5K stars + 113 open issues） |
| 质量评级 | 代码 A- / 文档 B+ / 测试 C |
| License | AGPL-3.0（强传染性） |
| 最新版本 | v0.2.31（95 tag / 79 Release） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

主开发者 **Sam L'Huillier（samlhuillier）** 是英国司法部（ai.justice.gov.uk）的 AI 工程师，账号年龄 2.5 年，个人仓库 39 个，主题集中在 LLM 微调、SQL 生成、RAG——这三条线索与 Reor 的产品定位完全自洽。他以 `reorproject` 组织壳包装这个项目，是个人项目产品化的常见动作。公开兴趣横跨「LLM 微调 / SQL 生成 / RAG」，意味着他并不是从「非技术人写个 AI 笔记 app」的角度出发，而是从「政府/法律场景对本地化的硬需求 + LLM 桌面化拐点」的工程师视角切入。

### 问题判断

Sam 看到的是「AI 笔记工具」品类的三重原罪：

1. **延迟**：用户刚写的段落几秒后才被索引，问答时拿不到最新内容（Issue #51 「Model doesn't have knowledge about my notes」）
2. **隐私**：笔记全文经 Embedding 服务/Embedding API 流出去，律师、医生、研究者根本不敢用
3. **供应商锁定**：嵌入模型/LLM 升一版，所有用户历史数据要重新向量化

而 PKM 工具里「知识是过程不是状态」的共识（Obsidian/Logseq 早已证明双向链接 + 反向索引才是真正范式）告诉他：AI 应该是放大既有写作流，而不是替代。

### 解法哲学

核心是 **Dual-Generator（双生成器）**：把「人类写作」和「LLM 检索」做成对等的两个生成器，共享同一向量库。人类切换文件时 Related notes sidebar 实时显示语义相似的旧笔记，AI 既能做 Q&A 也能做写作伴读。

由此衍生的工程取舍非常清晰：

- **Local-first by default**——离线 / 隐私 / 性能 / 无数据外流
- **AI 放大而非取代思考**——不做「AI 自动生成笔记」功能
- **完全可移植的本地 Markdown 仓库**——笔记以 `.md` 形式落盘，不锁格式
- **AGPL-3.0 防云厂商白嫖**——保护主义立场与隐私立场一脉相承

### 战略意图

v0.1.x 核心 RAG、v0.2.x 写作助手 + 多平台打包、v1.0 计划（自定义嵌入、Synced Vault、插件 API、移动端）——这四件事任意一件都是 6 个月以上工作量，单人项目难承，作者清楚这是「个人 + 社区」能维护的极限。2025-05 仓库停摆、2026-03 归档，意味着 v1.0 路线被「搁置」而非「取消」——保持项目可被接手而非僵死。组织壳 + AGPL-3.0 + 没有融资信号告诉我们：作者没有走商业化 SaaS 路线，这条项目从一开始就是「做给同类人用的工具」，而不是「做成公司」。

## 核心价值提炼

### 创新之处

1. **Dual-Generator 哲学落地**（新颖 4/5、实用 5/5、可迁移 5/5）：人类与 LLM 共享同一向量库，Q&A 模式与编辑器 Related notes 模式走同一个 `window.database.search` 入口，是「AI 工具如何嵌入既有工作流」的范式参考。
2. **客户端 hybridSearch（向量 + 关键词加权融合）**（实用 4/5、可迁移 5/5）：完全在渲染进程实现，`combineAndRankResults = vectorScore × 0.7 + keywordScore × 0.3`，不依赖任何后端服务——任何本地 RAG、浏览器内 RAG 都该有。
3. **Ollama 三级降级链（ping → PATH exec → packaged binary）**（实用 5/5、可迁移 4/5）：开箱即用解决「用户电脑可能没装 Ollama」的现实门槛，依赖外部服务的桌面应用都该有这个降级链。
4. **LanceDB schema 漂移自愈（dropTable + recreate on schema mismatch）**（实用 4/5）：避免 LanceDB 0.4.x 的 schema migration 痛点。
5. **多窗口 × 多 vault × 多 embedding 模型独立表**（新颖 4/5）：表名 = `ragnote_table_<model>_<dir>`，强隔离。
6. **编辑器侧 Related notes（500 字符 chunk → 向量检索 → 浮层列表）**：在用户切换文件时用前 500 字符做查询，结果以「Related notes」列表呈现——是「主动联想」UX 的范式。

### 可复用的模式与技巧

| 模式 | 适用场景 |
|---|---|
| Electron 三层 + 强类型 preload IPC 桥（`createIPCHandler<T>` 工厂） | 30k+ LoC 的 Electron 应用 |
| LanceDB embedding function adapter（`EnhancedEmbeddingFunction<T>`） | 本地 embedding 模型的 RAG |
| 标题优先 + RecursiveCharacterTextSplitter 双层 chunking | Markdown / 结构化文档 RAG |
| chokidar `ignoreInitial: true` + 渲染层主动触发索引 | 本地优先文档编辑器（避免 IO 风暴） |
| 编辑器变更 debounce 3 秒 → 写盘 + 重新索引 | 实时编辑 + 实时索引的 RAG 编辑器 |
| hybridSearch 客户端加权融合 | 不依赖后端的本地 RAG |
| BlockNoteView + 自定义 ProseMirror plugin inline suggestion | TipTap/BlockNote 智能编辑器 |
| context limit 截断（tiktoken 数 token，保留 90% context window） | 长上下文 RAG |
| store-migrator 模式 | 长期维护的 Electron 桌面应用 |

### 关键设计决策

| 决策 | 方案 | Trade-off | 可迁移性 |
|---|---|---|---|
| Electron 三层分离 + contextBridge 窄 API | `createIPCHandler<T>` 工厂把 100+ IPC 通道强类型化 | 维护成本高，但比 nodeIntegration 安全得多 | 高 |
| LanceDB 表名 = `<model>_<dir_hash>` 强隔离 | schema 漂移时 drop & recreate | 换模型要重新索引全库，但避免误用 | 高 |
| 双生成器 = 同向量库 + 两种 UI | Q&A 与 Related notes 走同一 `window.database.search` | Related notes 用前 500 字而非光标 chunk，避免性能灾难 | 极高 |
| chokidar + 渲染层主动索引 | 文件监听只通知，不直接嵌 | 「文件树更新」和「向量库更新」分两步 | 高 |
| LanceDB schema 自愈 | 检测 schema 不一致直接重建表 | 粗暴但解决了 LanceDB 0.4.x 痛点 | 中 |

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | Reor | AnythingLLM | Obsidian + Copilot | Logseq | Khoj |
|---|---|---|---|---|---|
| 定位 | AI 原生 PKM | LLM 工作台 | PKM 装上 AI 插件 | 块状 PKM | Obsidian 内 AI 助手 |
| Star 数 | 8.5k | ~32k | Obsidian 数百万 | ~36k | ~30k+ |
| AI 集成方式 | 原生（同向量库） | 工作台式 | 第三方插件 | 第三方插件 | 寄生式 |
| 本地优先 | ✅ 默认 | ❌ 默认 Docker | ⚠️ 默认云同步 | ✅ | ✅ |
| 编辑器类型 | Markdown | 无（聊天界面） | Markdown | Outliner | 无（聊天界面） |
| 笔记可移植 | ✅ 纯 .md | ⚠️ 部分导出 | ✅ 纯 .md | ⚠️ 自有格式 | ❌ |
| License | AGPL-3.0 | MIT | Obsidian 商业 | AGPL-3.0 | AGPL-3.0 |
| 维护状态 | 已归档 | 活跃 | 活跃 | 活跃 | 活跃 |

### 差异化护城河

- **「双生成器」叙事**：清晰可传播（「AI 放大而非取代思考」），是叙事资产
- **AI 与编辑器原生集成深度**：Related notes sidebar、自动嵌入、debounce 写盘，其他竞品做不到
- **AGPL-3.0 + Local-First**：明确「我不做云服务」的市场定位
- **单作者深度打磨**：hybridSearch、context window 90% 截断、chunkSize 可配置——大厂工程纪律

### 竞争风险

- **Obsidian 官方做 AI**：一旦 Obsidian 官方做 AI，Reor 的「AI 原生 PKM」差异化会被抹平
- **AnythingLLM 转型**：若推出本地优先模式，团队场景被吸走
- **v1.0 路线搁置**：自定义嵌入/同步/插件/移动端都是大需求，搁置意味着用户增长天花板
- **单点故障**：作者单线维护，bus factor = 1（已发生）

### 生态定位

**AI 时代的 Obsidian 替代品**，目标用户是「对隐私敏感、对 AI 重度、愿意为软件折腾的人」——典型画像：研究员、律师、医生、独立开发者。归档后这块留给 Khoj、Logseq 插件生态、AnythingLLM Desktop 补位。

## 套利机会分析

- **信息差**：8.5K stars + 已归档 = 出现了「开源墓碑效应」。Star 数 2026-02 单月创新高（64 个），是用户发现项目后因归档遗憾而 Star。**对学习者而言这是利好**：被冻结的设计反而成了稳定的参考实现，今天 clone 下来代码不会再变；对潜在用户而言是利空：bug 不会修复，依赖不会升级。
- **技术借鉴**：Reor 是研究「如何用 Electron 把本地 LLM 嵌进笔记产品」的范本——上面列出的 13 个可复用模式可以原样搬到自己的项目。
- **生态位**：它填补了「AI 原生 + 本地优先 + 个人开发者」的细分空白。归档后这个空白由 Khoj（一站式）、Logseq AI 插件（外挂式）填补，但目前没有同位替代品——这是 fork 或重写的机会窗口。
- **趋势判断**：本地 LLM 推理正在变得更便宜、更快（Apple Silicon MLX、Llama.cpp 小模型），Reor 当年的「全套本地化」门槛在 2026 年已经明显降低，思路会比产品本身更有生命力。

## 风险与不足

- **已归档无维护者**：LanceDB 升级、Electron 升级、TipTap 升级都不会有人跟，依赖漏洞会持续累积
- **AGPL-3.0 商用风险**：任何衍生作品必须开源 + 网络服务也必须开源，企业使用要慎重评估
- **测试覆盖率极低**：仅 2 个 jest 文件，UI/AI 流几乎无覆盖（Issue #51/#74/#119 都是测试能挡住但没挡住的 bug）
- **写入失败无 retry**：`LanceDBTableWrapper.deleteDBItemsByFilePaths` 直接吞掉错误（「no need to throw error」 注释）
- **CPU 100% 历史 bug**：实时嵌入 + LanceDB 写入是已知性能痛点，3 秒 debounce 是妥协方案
- **3 秒索引延迟**：用户写完 3 秒后 AI 才「看到」新内容——这是物理/性能权衡，但 UX 上是真实痛点
- **Sentry 与隐私立场矛盾**：项目自身主张 Local-First，但生产模式默认启用 Sentry 上报 crash，是个值得讨论的设计张力

## 行动建议

- **如果你要用它**（作为在用工具）：**不建议**。已归档 + AGPL-3.0 + 无维护者响应 = 长期使用风险高。需要本地 AI 笔记的用户请转向 Khoj（Obsidian 集成）、Logseq + AI 插件、AnythingLLM Desktop。
- **如果你要学它**（作为参考项目）：**强烈推荐**。重点关注以下文件：
  - `electron/main/index.ts` + `electron/preload/index.ts` — Electron 三层 + IPC 工厂范式
  - `electron/main/vector-database/lance.ts` + `lanceTableWrapper.ts` — LanceDB schema 自愈与多模型隔离
  - `electron/main/llm/models/ollama.ts` — Ollama 三级降级
  - `src/components/Sidebars/SimilarFilesSidebar.tsx` — 双生成器的 Related notes 侧栏
  - `src/lib/db.ts` — hybridSearch 客户端实现
  - `src/components/Editor/BacklinkExtension.tsx` — ProseMirror plugin 实现 inline suggestion
- **如果你要 fork 它**：AGPL-3.0 意味着你必须公开源码 + 网络服务端代码，且无法直接转闭源。建议：
  - 考虑切换到更宽松的 license（需要原作者同意或从头写）
  - 优先解决「写入失败无 retry」、「LanceDB schema 漂移」等已知痛点
  - 实现 v1.0 搁置路线图中的「自定义嵌入模型支持」和「插件 API」——这是当前最缺的能力

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/reorproject/reor（已收录，含架构详解） |
| Zread.ai | 未收录（403） |
| 关联论文 | 无 |
| 在线 Demo | 无（纯本地桌面 App） |
| 归档前官方文档 | https://www.reorproject.org/docs/documentation/（域名已跳转，可能下线） |
| Discord 社区 | https://discord.gg/b7zanGCTUY |
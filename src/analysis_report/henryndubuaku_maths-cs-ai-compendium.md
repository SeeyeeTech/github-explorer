# GitHub 推荐：5 个月 6.6K stars：YC S25 创始人把 20 章 AI 教科书做成了 LLM 知识库

> GitHub: https://github.com/henryndubuaku/maths-cs-ai-compendium

## 一句话总结

一份由 YC S25 入选者、6 篇 ICLR/ICML 2026 作者 Henry Ndubuaku 主导的「数学·CS·AI 全栈式开源教科书」——20 章 100+ 节、264 张手绘 SVG、29.6k 行 Markdown，并通过 `llms.txt` + MCP Server 让 AI 编程助手直接当知识库调用。

## 值得关注的理由

1. **个人大百科级教科书的稀缺定位**：在 OI-wiki（中文算法向）和 tech-interview-handbook（英文面试向）之间，切出了「英文 + 数学 + CS + AI 全栈 + 顶尖研究者背书」的真空带，5 个月从 0 到 6.6K stars。
2. **LLM-first 双接口设计**：自带 `llms.txt` 把整本教材扁平化为 LLM 友好的目录索引，再加 `mcp/` 目录的 MCP Server（5 个工具）让 Claude Code / Cursor / VS Code 开箱即用当知识库——这是 GitHub 上较早一批「教材 + MCP」组合。
3. **作者履历真实性可交叉验证**：6 篇 ICLR/ICML 2026 + YC S25 + Cactus Compute 创始人 + 7 轮 Nvidia 技术面后转 YC（README 自述），三重身份交叉印证，权威性远高于普通 GitHub 个人项目。

## 项目展示

![Logo](https://raw.githubusercontent.com/henryndubuaku/maths-cs-ai-compendium/main/images/logo.png)

在线阅读站点：https://henryndubuaku.github.io/maths-cs-ai-compendium/

项目内置 264 张手绘 SVG 概念图，视觉语言统一（浅灰坐标轴 + 三色调色板），覆盖向量加法、RoPE 旋转、SGD/Momentum/Adam 优化轨迹、Transformer 三大范式等概念。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/henryndubuaku/maths-cs-ai-compendium |
| Star / Fork | 6,588 / 807 |
| Watchers / Open Issues | 72 / 4 |
| 代码/内容行数 | ~29.6K 行 Markdown + 264 张 SVG + 296 行 TypeScript（MCP） |
| 项目年龄 | 5.4 个月（首次 commit 2026-02-03） |
| 总 Commit / 贡献者 | 77 / 9 人（主作者 ~84%） |
| 开发阶段 | 低维护（早期集中爆发后转入收尾维护） |
| 贡献模式 | 核心少数 + 社区众包 |
| 热度定位 | 大众热门（>5K stars，<半年达成） |
| 质量评级 | 内容[优] 文档[优] 测试[无] |
| License | Apache 2.0 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Nigerian-British，伦敦，9.3 年 GitHub 账号年龄。QMUL 本硕（EECS + MSc AI，NLP 方向导师 Prof Matt Purver）。现为 **Cactus Compute 创始人**，公司专注 tiny AI for tiny devices——Cactus 移动端推理引擎 5.5K stars、Needle 26M 参数 agentic 模型 3.2K stars。学术坐标上 6 篇 ICLR/ICML 2026 一作/共一论文（含 Parameter-Efficient Transformer Embedding via Functional Factorization / HiDRA / Depth Over Specialization / Just Enough Learning / TACE / CLAWS）。关键节点：YC S25 入选，此前通过 7 轮 Nvidia 技术面拿到口头 offer 后转 YC（README 自述）。Cactus 团队已扩至 6 人，融资方含 Oxford Seed Fund / FCVC。

### 问题判断

作者看到了什么别人没看到的问题？

- **「教材没跟上 AI 编程助手时代」**：现有教科书（Goodfellow / Bishop / Hands-On ML）都是人类阅读优化的，缺少面向 LLM 的索引层和工具调用入口。
- **「个人知识资产无系统化沉淀路径」**：作者本人多年 AI/ML 研究+工业经验，但没有结构化的对外输出通道。
- **「数学→CS→AI 全栈没有一本现成书」**：市面上要么是数学书（无 AI）、要么是算法书（无 AI）、要么是 AI 书（无系统地基），三者贯通的内容真空。

时机为什么是现在？**MCP 协议**（2024 年底由 Anthropic 推出）让「本地知识库 + AI 编程助手」的开箱即用集成成为可能，作者敏锐地抓住了「教材 + MCP」的组合机会。

### 解法哲学

作者明确选择了什么：

- **20 章跨域贯通 + 每章 5-7 节中等粒度**：宁可覆盖面广，不在单点深度卷
- **手绘 SVG 而非 Mermaid/Graphviz**：牺牲产出速度，换离线友好 + LLM 可像素级读取
- **LLM-first 双接口**：`llms.txt` 目录索引 + MCP Server 工具调用，让人类和 AI 都是 first-class 用户

作者明确不做什么：

- 不配完整代码仓库——仅 Ch16 链出 `cuda-tutorials`、Ch17 链出 Cactus 引擎
- 不做语义化版本发布——0 个 tag、无 release，CI/Pages 直推 GitHub Pages
- 不写测试——MCP server 零单元测试

### 战略意图

在作者更大图景中的位置：

- **Cactus 生态的人才/品牌入口**：Needle 26M agentic 模型（3.2K stars）+ Cactus 推理引擎（5.5K）+ Compendium 三件套共同构成「个人 IP → 社区 → 商业（Cactus 团队招聘 + Oxford Seed Fund 融资）」的飞轮。
- **行业权威性资产**：6 篇 ICLR/ICML + YC S25 + 这本开源教科书三重叠加，在 AI 教育赛道建立「权威研究者」标签。
- **无直接商业化路径**：教科书本身 Apache 2.0 协议、零变现，纯粹是 IP 资产。间接收益通过 Cactus 招聘难度降低 + 创始人个人品牌实现。

## 核心价值提炼

### 创新之处

按新颖度×实用性排序：

1. **LLM-first 双接口**（`llms.txt` + MCP Server）——新颖度 5/5、实用性 4/5、可迁移性 5/5
2. **264 张手绘 SVG 替代 Mermaid**——新颖度 3/5、实用性 5/5、可迁移性 4/5
3. **跨章 cross-reference 形成知识图谱**——新颖度 3/5、实用性 5/5、可迁移性 5/5
4. **Foreword 嵌入认知科学实验**（Kvashchev 创造力训练 + Rosenthal 实验）做学习法论铺垫——新颖度 5/5、实用性 3/5、可迁移性 2/5
5. **章节副标题摘要**（每节斜体一行）便于跳读——新颖度 2/5、实用性 5/5、可迁移性 5/5
6. **作者经验元数据内嵌**（Ch16 跳 cuda-tutorials、Ch17 提 Cactus 引擎）让教科书与作者工业项目互证——新颖度 4/5、实用性 3/5、可迁移性 2/5

### 可复用的模式与技巧

1. **目录即 LLM 接口**（`llms.txt` 模式）：任何 docs 项目加一个 md 索引就能被 LLM 高效检索
2. **MCP server 暴露本地知识库**：标准 5 工具模板（list_topics / read_section / search / recommend / get_examples）即可让 Claude/Cursor 离线消费大型文档
3. **mkdocs-material + arithmatex + MathJax** 数学书黄金组合（mkdocs.yml L34–47 直接抄）
4. **章节粒度 5–7 节 × 180–600 行** 的甜区——既不太碎（避免导航疲劳）又能 1–2 小时读完
5. **每章 1 节「00. foundations」预先置底**（Ch14/Ch16 都有）做总览，便于读者自检预备知识

### 关键设计决策

| 决策 | Trade-off | 可迁移性 |
|------|-----------|---------|
| 20 章跨域贯通 + 每章仅 5-7 节 | 覆盖面 > 单点深度 | 高 |
| 图片一律 SVG 手绘而非截图/Mermaid | 失去快速产出能力、获得离线友好 + LLM 可解析 | 中 |
| 表格 + 公式 + 短句推进，不配完整代码仓库 | 阅读门槛低但实战不足 | 高 |
| MkDocs Material 主题 + 单 nav 配深嵌章节，`docs_dir: .` 让仓库根即文档根 | 省一层抽象但牺牲模块化 | 中 |
| 本地 MCP 优先（`COMPENDIUM_ROOT` 环境变量），不接云 API | 需要本地 clone，但零 token 成本、可私有化 | 高 |

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | 本项目 | tech-interview-handbook | OI-wiki | leetcode-patterns | TheAlgorithms/TypeScript |
|------|---------|--------|--------|--------|--------|
| Stars | 6.6K | 141K | 26.3K | 13.4K | 2.9K |
| 覆盖范围 | 数学 + CS + AI 全栈 | CS + 面试 | OI 竞赛算法 | LeetCode 题型 | 算法实现 |
| 深度倾向 | 中等 | 工程实战 | 中等（偏 C++） | 单点 | 单点 |
| AI/ML 内容 | ✓ 完整 | ✗ | ✗ | ✗ | ✗ |
| 作者权威背书 | ICLR/ICML 6 篇 + YC S25 | 前 Facebook 工程师 | 社区众包 | 个人维护 | 社区众包 |
| LLM 友好 | ✓ llms.txt + MCP | ✗ | ✗ | ✗ | ✗ |
| 维护活跃度 | 中（5.4 月从 0 到 6.6K） | 高 | 高 | 中 | 高 |

### 差异化护城河

- **唯一覆盖 math + CS + AI 全栈的英文个人大百科**：OI-wiki 是中文且偏 C++ 竞赛，tech-interview-handbook 弱理论，TheAlgorithms 无 AI/ML
- **顶尖研究者背书**：6 篇 ICLR/ICML 2026 + YC S25 在「教科书权威性」维度独此一家
- **LLM-first 双接口**：GitHub 上较早一批「教材 + MCP」组合，先发优势明显

### 竞争风险

- **大厂下场风险**：Anthropic / OpenAI / DeepMind 若推出官方 LLM-native 教科书，本项目会被边缘化；但作者与 Cactus 生态绑定，差异化护城河尚在
- **中文 OI-wiki 同类竞品**：若有人做中文版的 math + CS + AI 全栈教科书（且包含 MCP），本项目的「英文 + 顶尖研究者」优势会被稀释
- **作者精力分散**：Cactus Compute 同时推进推理引擎 + Needle 模型 + Compendium，单作者维护下深度不一致风险（Ch20 量子 ML 仅 11 行 bullet）

### 生态定位

在 AI 教育生态中扮演「**个人大百科 + LLM 知识库加载源**」的角色——既不是入门教程（Hands-On ML 更合适），也不是研究综述（Goodfellow / Bishop 更合适），而是「主线脑图 + 跨域跳板」。读者沿 20 章主线通读获得全景认知，再去专书补单点深度。

## 套利机会分析

- **信息差**：低关注度但高质量？**否**（6.6K stars 已不算低），但**中文世界关注度极低**——OI-wiki / 技术博客圈几乎没讨论过英文 AI 教科书生态，存在「中文读者未充分发现」的信息差
- **技术借鉴**：`llms.txt` + MCP Server 5 工具模板可直接搬到自己公司的内部文档/学习笔记项目
- **生态位**：填补了「LLM-native 教科书」这一新兴细分领域的真空
- **趋势判断**：MCP 协议正在成为 LLM 应用基础设施（2026 年 H2 预计加速普及），提前布局 LLM-first 教材的项目会获得复利效应

## 风险与不足

- **单点深度不足**：20 章 × 5–7 节 × 平均 250–500 行 ≈ 3 万行 md，**单点深度有限**——Ch20 量子 ML 仅 11 行 bullet、Ch14 DS&A 是 NeetCode 题单而非算法导论式严格证明
- **时效性滞后**：覆盖 2024–2025 文献（MLA/MoE/Mamba/VLA/RT-2/Octo/Pi-0/EfficientNet/ConvNeXt/AQLM/BitNet/PagedAttention），但**仍滞后于 arXiv 实时前沿**（无 Mamba-2/Zamba/Hymba/DeepSeek-V3 等 2025 Q2 后新模型）
- **工程债**：LaTeX 在部分页面渲染失败（issue #18 未修，`mathjax.js` 加载时机），**内容扩写速度已超过工程化**——单作者项目的典型瓶颈
- **一致性问题**：MkDocs 路径仍带 `chapter 01:` 冒号（mkdocs.yml L73–215），与 commit #16 的修复冲突——CI 与本地 clone 行为不一致的隐性 bug
- **测试缺失**：MCP server 零单元测试，任何章节目录正则改动都会静默 break `list_topics`
- **社区运营轻度缺失**：营销 spam issue（#12, #14）未隔离，未设置 issue 模板 / 标签过滤
- **作者集中度过高**：主作者 ~84%，单点故障风险

## 行动建议

### 如果你要用它

- **作为 LLM 知识库加载源**：clone 后启动 MCP server（`tsx mcp/src/index.ts`），在 Claude Code / Cursor 里直接当知识库查——比让 LLM 瞎答「梯度消失怎么解决」靠谱得多
- **作为 AI 学习路线图**：沿 20 章主线通读，2-3 个月可获得数学→CS→AI 全栈认知框架
- **不建议场景**：需要单点深度（如「图神经网络严格证明」「CUDA kernel 实战」）时，本项目不够，需另寻专书（Goodfellow / Bishop / CUDA Programming Guide）

### 如果你要学它

重点关注这些文件/模块：
- `llms.txt`（156 行）—— LLM 友好的目录索引模式，直接搬
- `mcp/src/index.ts`（335 行）—— MCP server 5 工具模板，直接抄
- `mkdocs.yml`（187 行）—— mkdocs-material + arithmatex + MathJax 数学书黄金配置
- `images/` 目录的 SVG——手绘视觉语言参考（浅灰坐标轴 + 三色调色板）
- `chapter 06 - machine learning/03. deep learning.md`（354 行）—— 教学推进范本
- `chapter 16 - machine learning systems/04. gpu architecture and cuda.md`（598 行）—— CPU/GPU 对比表 + 内存层次表的写作范本

### 如果你要 fork 它

可以改进的方向：
1. **补单点深度**：聚焦某个薄弱章节（如量子 ML、DS&A），把它从 bullet 占位扩到 600+ 行完整讲义
2. **加 MCP server 测试**：补单元测试覆盖 `list_topics` / `read_section` / `search` 三大工具
3. **修 LaTeX 渲染 bug**：解决 issue #18 的 MathJax 配置问题
4. **加 CONTRIBUTING / issue 模板**：隔离营销 spam，提升社区贡献闭环效率
5. **做中文版翻译**：存在「中文读者未充分发现」的信息差，中文翻译版可快速积累 10K+ stars

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录 |
| Zread.ai | 未收录 |
| 在线阅读 | https://henryndubuaku.github.io/maths-cs-ai-compendium/ |
| 在线 Demo（MCP） | 本地 `tsx mcp/src/index.ts` |
| 关联论文 | Parameter-Efficient Transformer Embedding via Functional Factorization（ICML 2026）等 6 篇 ICLR/ICML |
| 作者其他项目 | https://github.com/cactus-compute/cactus、https://github.com/cactus-compute/needle、https://github.com/henryndubuaku/cuda-tutorials、https://github.com/henryndubuaku/nanodl |
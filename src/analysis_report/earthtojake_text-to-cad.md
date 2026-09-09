# GitHub 推荐：4.6 个月 15k stars：把机械设计变成编码 Agent 的 text-to-cad 怎么让 LLM 一天交付一个机器人

> GitHub: https://github.com/earthtojake/text-to-cad

## 一句话总结

text-to-cad 把机械设计从「GUI 拖拽」重定义为「代码生成」——不训练领域模型，而是给前沿 LLM 加一层薄薄的确定性工具壳，让它能直接写出**可制造**的 STEP / URDF / SRDF / SDF，并通过 DfAM 校验 → 切片 → 上机（Bambu Lab MQTT / SendCutSend）走完全链路。

## 值得关注的理由

- **AI Agent + 硬件交叉点的代表性开源项目**：4.6 个月迭代 53 个 release，单月峰值 475 个 commit；MIT 开源 + 1.5k fork + Hacker News 主榜曝光，已经站上「AI 工程师做物理设计」的赛道入口。
- **真正的端到端 pipeline，不是研究 demo**：覆盖 CAD → CAE → CAM 全链路（11 个 agent skills，含 `step-parts` 12,000+ 标准件库、`dfam-check` 工艺校验、`bambu-labs` MQTT 直接打印、`urdf/srdf/sdf` 机器人描述）。
- **协议级野心**：「be the protocol, not the platform」——故意不上 SaaS，distribution 走 PyPI wheel + Skills CLI（兼容 Codex/Claude Code/Grok Build），赌的是 agent skill 生态的事实标准。

## 项目展示

![CAD skill 生成与预览演示](https://raw.githubusercontent.com/earthtojake/text-to-cad/main/assets/text-to-cad-demo.gif)
*核心能力演示：自然语言 → build123d Python → STEP/3MF → 实时预览*

![URDF skill 输出在 CAD Viewer 中的演示](https://raw.githubusercontent.com/earthtojake/text-to-cad/main/assets/urdf-demo.gif)
*URDF skill：从同一几何源反推机器人描述，让 CAD 既是零件也是仿真体*

![SRDF MoveIt2 skill 逆运动学演示](https://raw.githubusercontent.com/earthtojake/text-to-cad/main/assets/srdf-moveit2-demo.gif)
*SRDF skill + MoveIt2：把生成结果直接接入 ROS 运动学规划*

> 官网 `texttocad.dev` 的 `/blog` 与 `/demo` 路径均 404，无补充媒体。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/earthtojake/text-to-cad |
| Star / Fork | 15,021 / 1,560 |
| 代码行数 | 265,210（Python 50.9% / JavaScript 39.0% / JSON 7.1%） |
| 项目年龄 | 4.6 个月（首提交 2026-04-21） |
| 开发阶段 | 密集开发（近 30 天 377 个 commit） |
| 贡献模式 | 单人主导（earthtojake 占 86.1%，23 名贡献者） |
| 热度定位 | 大众热门（4.6 个月破 15k star，Hacker News 主榜） |
| 质量评级 | 代码优秀 / 文档优秀 / 测试充分 |
| License | MIT |
| Release | v0.5.1（共 61 个 tag，53 个 release，语义化版本） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Jake Fitzgerald（earthtojake），独立开发者，derive.xyz 联合创始人（前 WhatsApp 基础设施 3 年）。11.6 年 GitHub 账号、415 粉丝、18 个公开仓库——text-to-cad 在 18 仓中排第 1，单仓独占其全部流量与 commit 节奏。2025 ICRA 演示机械臂遥操作后真正在「造东西」，把产品/工程能力用在「开源硬件 + AI Agent」交叉点，text-to-cad 即这一兴趣的具象化输出。

### 问题判断

作者不是从论文里提出问题，而是从机器人量产 / 抓取夹具迭代中**自我 dogfooding**：每一次硬件迭代都要重画一份 STEP，几何参数变了机器人 URDF 关节轴就要重算。论文里没人解的「CAD↔机器人描述的隐性耦合」才是真实痛点（Phase 1 提到的 #10 URDF Generation issue 就是这条暗线的首次浮面）。时机选择上：2026 年 SOTA LLM 已经「能写 Python」也「能跑 CLI」，缺的只是把它们接到几何内核与制造端的薄壳——这是工程问题，不是模型问题。

### 解法哲学

- **不训练领域模型**：拒绝走「CAD-LLaMA / CAD-MLLM」fine-tune 老路——明确选择「让 SOTA LLM + 薄薄的确定性壳子直接出可制造 CAD」。
- **代码即几何 + render-and-verify**：每个模型是单文件 `@step` 函数，LLM 写 Python，cadgen 编译、决定拓扑、跑 build123d，渲染回去做反馈。「把机械设计重定义为编码问题」是项目根命题。
- **Unix 哲学 + 一道门**：所有输入都从 `python model.py` 唯一门进，所有输出都是内容寻址缓存里的 deterministic artifact；CLI 是「格式-动词」二维表的 mirror，没有第二份实现。
- **显式不做的**：（1） 不做几何内核替代（坚持 build123d/OCCT 黑盒）；（2） 不做 backwards compatibility（v0.4→v0.5 没有 shim）；（3） 不做自动 GC（让用户用 `store gc`）；（4） 不做 lock（用 publish rule + pins 做并发）。

### 战略意图

text-to-cad 是 derive.xyz 机器人基础模型栈的**几何底座**：上面挂着机械臂遥操作、ICRA demo、可能的商业 SaaS（Genie 路线），下面挂着 DfAM/切片/上机。商业化意图清晰——`step.parts` 已经是 hosted API，docs 站是 texttocad.dev，AGENTS.md 把 release 工程化做得很重（双 workflow 流水线、canonical VERSION、wheel contents 检查）。但故意**不上 SaaS**：distribution 是 PyPI wheel + Skills CLI，作者赌的是 「be the protocol, not the platform」。

## 核心价值提炼

### 创新之处

1. **两段式内容寻址 store（artifact side `objects/` + code side `index/`）**：渲染路径只看 `index/document → objects/`，绝不读 record；records 完全可删。git + Bazel remote cache 的精神之子，但用「装饰器声明的 outputs 不入 store」这条额外法则把 source/output 边界封死。**新颖度 5/5，实用性 5/5，可迁移性 5/5**。
2. **装饰器即程序（`@step`）+ 函数签名即 CLI（mirror subset）**：写一个 Python 函数就同时得到「作为构建入口的程序」+「作为 CLI 命令的 parser」。Mirror 子集用静态校验阻断漂移。**新颖度 4/5，实用性 5/5，可迁移性 4/5**。
3. **LazyCompound + slot-yield broker**：把 DAG 并行度调度交给作者写的代码流（哪些操作 force 哪些 defer），pool 端的 broker 只做 FIFO slot + in-flight coalescing；父等子时主动 yield slot 保证 1 槽也能建多层装配。**新颖度 4/5，实用性 4/5，可迁移性 4/5**。
4. **Publish rule by closure hash + snapshot isolation by pin**：无锁并发写同一对象——只要写者的「构建时 closure hash」与磁盘当前一致就 publish record；父体 pin 子体 tree 在 call site 而非 force site。**新颖度 4/5，实用性 4/5，可迁移性 3/5**。
5. **Semantic source hash + mtime-settled cache**：`ast.dump` 不带位置信息做语义 hash；stat 三元组缓存；2s settling window 防文件系统 mtime 精度丢失。**新颖度 3/5，实用性 5/5，可迁移性 5/5**。
6. **PEP 562 lazy re-export** `cadgen.build123d`：让重包装库既能 attribute-style 又能 `isinstance`，且首次访问前不付 ~2.5s OCP 导入。**新颖度 2/5，实用性 5/5，可迁移性 5/5**。
7. **「库 + 协议 + 工艺下游」一体机**：业界少见的「从 CAD 自动生成 URDF/SRDF/SDF」+「DXF/2D 投影与 3D 同源」+「DfAM 测量 + 切片 + 上机」一条龙。**新颖度 4/5，实用性 4/5，可迁移性 2/5**。

### 可复用的模式与技巧

1. **Two-side content-addressed store with input-addressed records** — 任何「源码编辑频繁、构建代价高、内容可去重」的工具。
2. **Function signature → CLI mirror (with subset enforcement)** — 任何 Python 服务库 / CLI 工具集都能用此模式保证 flag 永远不漂。
3. **LazyCompound / Promise with placement-aware deferred** — DAG 编译、生成式管线、异步生成器（promise 取消）。
4. **Publish rule by closure hash** — cache write-through、协作编辑、CI 并发写。
5. **Slot-yield broker for nested DAG builds** — 构建系统、job queue、parent-child DAG 调度。
6. **Semantic source hash + mtime-settled cache** — ruff/mypy/pytest 缓存、esbuild/swc、任何依赖 Python 源码语义而非字节的工具。
7. **PEP 562 lazy re-export** — 任何重封装 TensorFlow/PyTorch/triton/OpenCV 的库。
8. **Ship-alone law with markdown-isolation test** — 包内 markdown 必须对「只 pip install」的人可读，禁止反引仓库路径。

### 关键设计决策

- **决策**：Document-only CLI / scripts-are-programs（law 7）
  - **问题**：一份代码既被人写、又被 CLI 解析、又被渲染器读，三方串扰。
  - **方案**：`python model.py` 走唯一源门，CLI 一律吃 `.step/.stl/.dxf` 文档——门路径只有一次「哈希文件字节 → `index/document` → objects」三跳。
  - **Trade-off**：不能从命令行做 single-call 模型实验；用户必须建文件。
  - **可迁移性**：高。
- **决策**：装饰器输入从不改变几何（law 16）+ 0 metadata in artifacts（law 4）
  - **方案**：装饰器参数仅控制「文件落点、tolerance、kinematics 声明」；几何纯靠函数返回值。
  - **Trade-off**：牺牲「作者一行声明就在装配里换位姿」的便利。
  - **可迁移性**：中。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | text-to-cad | Zoo Genie | openscad-gpt | cordyceps | JARVIS build123d | OpenSCAD-AI |
|------|------------|-----------|--------------|-----------|------------------|-------------|
| 开源 | MIT | 闭源 SaaS | MIT（小型） | MIT（小型） | MIT（小型） | 闭源 |
| 几何内核 | build123d/OCCT B-Rep | 自研 ZSL 脚本 | OpenSCAD CSG-only | OpenSCAD | build123d | OpenSCAD |
| 工艺下游 | DfAM + Bambu + SendCutSend | 企业 CAD/CAM | 无 | 无 | cad_inspect | 无 |
| 机器人描述 | URDF/SRDF/SDF 一体 | 无 | 无 | 无 | 无 | 无 |
| Agent 生态 | 11 skills + Codex/Claude/Grok | 自有 UI | 单仓 demo | Claude + 截图 | Claude OAuth | 端到端模型 |
| 输出可编辑 | 是（Python source） | 是（ZSL） | 是（OpenSCAD） | 否 | 否 | 否 |
| 错误率（LLM 翻车率） | 中（依赖 build123d 复杂度） | 未公开 | 最低（CSG 极简语法） | 中 | 中 | 训练后较稳 |

### 差异化护城河

1. **内容寻址 + content-store 协议层**——把 CAD 变成可复用 Git-LFS-like artifact 协议。
2. **工艺/机器人下游一条龙**（DfAM、Bambu Lab MQTT、SendCutSend、URDF/SRDF/SDF）——「几何 → 物理输出」唯一闭环。
3. **多平台 Skills 兼容**（Codex/Claude/Grok plugin + Skills CLI）——agent 生态入口。
4. **`step.parts` hosted API**（12,000+ 标准件 STEP 库）——「几何复用」复利。

### 竞争风险

1. **Zoo Genie 降价 + 开源部分功能** 能吃掉创客侧；text-to-cad 没有 UI 阻力但缺协作功能。
2. **Anthropic/OpenAI 直接做「ChatGPT-CAD」** 会绕过协议层，但 build123d/OCCT 工艺合规仍是护城河。
3. **Windows 跨平台鲁棒性**（Issue #322 字体解析 crash、#211 drive-letter 403）暴露工程债务。
4. **单人项目（86.1% 占比）**，维护风险真实。

### 生态定位

「LLM-driven CAD/CAE/CAM 协议层 + 开源 distribution」——既不是闭源 SaaS，也不是训练领域模型；用 Python+OCCT+B-Rep 把 LLM 当工程师助手，目标是 de-facto standard for 「agent makes physical things」。

## 套利机会分析

- **信息差**：15k star + HN 主榜曝光，已不算被低估；增长空间在 ToB / 工业用户而非个人开发者圈层。
- **技术借鉴**（高价值）：
  - 两段式内容寻址 store → 直接迁移到任何编译/构建/文档系统（DSL 编译器、配置 schema 验证、PDF 生成）。
  - 函数签名 → CLI mirror → 任何 Python 服务库避免 argparse 漂移。
  - Slot-yield broker + LazyCompound → 任何 DAG 调度（编译器、ML 训练图、job queue）。
  - Semantic source hash + mtime cache → 任何 Python 缓存层（linter、type checker、formatter）。
  - PEP 562 lazy re-export → 重封装 torch/tensorflow/open3d 的库都该学。
- **生态位**：填补「LLM → 可制造 CAD → CAM/打印/仿真」端到端骨架的空白；学术模型（Text2CAD/CAD-LLaMA）只能停在 demo，text-to-cad 把「早晨写一段 prompt → 中午打印出来」做成真。
- **趋势判断**：在增长（5→6→7→8 月 commit 数 95→270→194→475），符合 「AI Agent + 硬件」 趋势；学术线（Text2CAD/CAD-LLaMA/CAD-MLLM）说明「用专门模型替代 agent 框架」仍是开放研究方向，6-12 个月可能洗牌。

## 风险与不足

- **单人项目维护风险**：86.1% 贡献占比，核心开发者流失或精力分散会让协议层停滞。
- **Windows 鲁棒性债务**：Issue #322（字体目录野文件击穿 import）、#211（drive-letter 403）、#274（350ms retry 覆盖不到 tail）说明严肃工业场景下 Windows 抖动未根治。
- **评测指标脆弱**：#94 揭示「benchmark outputs differ significantly from reference」——agent 写的几何在「看起来对」之外仍可能偏离 ground truth 数值，是该方向的根本痛点。
- **学术 vs 协议的押注风险**：作者明确赌 SOTA LLM + 薄壳协议胜出，若 Anthropic/OpenAI 直接做端到端 CAD 模型（如 GPT-CAD），协议层会被绕过。
- **官方文档/博客缺位**：`texttocad.dev/blog` 与 `/demo` 均 404，外部学习只能依赖 DeepWiki + 源码。
- **提交命名规范不足**：72% commits 归入 「Other」，结构性演化无法从 commit message 直接看到。

## 行动建议

- **如果你要用它**：选 `text-to-cad` 当**创客/小团队原型**或**机器人研发管线**；企业协作/参数化回放需求选 Zoo Genie；纯 OpenSCAD 学习场景选 `openscad-gpt`。
- **如果你要学它**：重点读
  - `packages/cadgen/README.md`（17 条 LAW）
  - `packages/cadgen/STORE.md`（11 章 store 协议完整规范）
  - `packages/cadgen/src/cadgen/store/{gate,publish,lazy,objects,index}.py`（核心 store 实现）
  - `packages/cadgen/src/cadgen/daemon/{broker,executors}.py`（并发与 slot 调度）
  - `packages/cadgen/src/cadgen/_internal/cli_from_function.py`（函数签名 → CLI mirror）
  - `packages/cadgen/src/cadgen/_internal/source_hash.py`（semantic hash + mtime cache）
- **如果你要 fork 它**：可改进的方向
  1. Windows 跨平台鲁棒性（字体解析故障隔离、drive-letter 路径处理、SMB retry 自适应）
  2. 评测指标体系（解决 #94 的 ground truth 偏差问题）
  3. 多语言 source hash（当前只对 Python 友好，对 Rust/CAD DSL 不友好）
  4. 协作/版本化层（Zoo Genie 的强项，text-to-cad 的空白）
  5. 提交命名规范（从 72% 「Other」 收敛到 Conventional Commits）

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [deepwiki.com/earthtojake/text-to-cad](https://deepwiki.com/earthtojake/text-to-cad)（2026-08-14 索引，含架构图、子系统文档、术语表） |
| Zread.ai | 未收录 |
| 关联论文 | [Text-to-CAD Generation Through Infusing Visual Feedback in LLMs](https://arxiv.org/abs/2412.06003) / [CAD-MLLM](https://arxiv.org/abs/2412.01429) / [Text2CAD](https://arxiv.org/abs/2409.17106) / [CAD-LLaMA](https://arxiv.org/abs/2409.11928) / [From Words to Worlds (NAACL 2025)](https://aclanthology.org/2025.findings-naacl.120/) |
| 在线 Demo | 无（`texttocad.dev/demo` 404；本地 cad-viewer 需 `localhost:4178`） |
| 外部深度视角 | [Text-to-CAD makes mechanical design a coding-agent problem — SourceFeed](https://sourcefeed.dev/a/text-to-cad-makes-mechanical-design-a-coding-agent-problem) — 独立观点：「the harness converted a spatial domain into the two things coding agents already do well, writing Python and running CLIs」；核心贡献不是某个模型，而是 **deterministic code-CAD + 强制视觉校验回路** |
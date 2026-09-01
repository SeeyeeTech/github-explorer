# GitHub 推荐：清华开源 OpenMAIC：5.7 个月 30k stars，把「MOOC 录播」革命成 AI 多 Agent 互动课堂

> GitHub: https://github.com/thu-maic/openmaic

## 一句话总结

OpenMAIC 是清华 MAIC 团队开源的「AI 多 Agent 互动课堂操作系统」——一键把任意文档变成立即可授课、可白板、可 PBL（项目式学习）的多 Agent 课堂，已用 JCST 2026 论文 + 22 教学 skill 协议 + 7 个 npm SDK 包占据了「教育垂直 LLM 编排」赛道的事实标准位置。

## 值得关注的理由

- **学术-工程-教育三栖稀缺资产**：5.7 个月拿到 29,439 stars / 4,964 forks，背后是清华计算机系 + 教育研究院联合团队、JCST 2026 论文（22 位作者）、Wu Wenjun AI 科技进步奖、教育部 AI 安全优秀案例三重背书，不是又一个 ChatGPT 套壳。
- **教育理论先行，而非「LLM 包一层皮」**：把布鲁姆分类法、ZPD（最近发展区）、UDL（通用学习设计）编码成 22 个 Skill（SKILL.md + constraint.yaml + Outline adapter），由 outline 生成器在 prompt 内消费 + 后置校验——领域知识真的进了代码，不是停在文档。
- **真多 Agent + 真白板**：LangGraph 1.1 Director Graph 单轮拓扑 + 28 个白板原子动作原语（wb_draw_text/shape/chart/latex/code + wb_edit_code 行级增删改），配合 lease fence + Postgres 事件日志让 Agent 会话可中断/可恢复/可水平扩容——这是「真」多 Agent 同台，不是「伪」单 Agent 角色扮演。

## 项目展示

### README 媒体
1. ![OpenMAIC Banner](https://raw.githubusercontent.com/thu-maic/openmaic/main/assets/banner.png) — 类型： hero（已校验存在）
2. ![OpenMAIC Logo](https://raw.githubusercontent.com/thu-maic/openmaic/main/assets/logo-horizontal.png) — 类型： logo/screenshot（已校验存在）

### 官网媒体
1. https://openmaic.io/ — 官网首页（hero 视频/Demo GIF 嵌入）
2. https://openmaic.io/openmaic-multi-agent-learning.html — 官方 Multi-Agent 演示页（含 3D/白板/圆桌辩论截图）

### 筛选说明
- 总共发现 4 个 README 媒体元素（2 个已校验 + 2 个外链 badge），筛选后保留 2 个
- 排除了 1 个 Vercel Deploy 按钮 badge、1 个 openclaw 第三方 CDN 图标（无版权校验）
- 官网媒体 2 个为外链（WebFetch 受限），保留但未做截取

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/thu-maic/openmaic |
| Star / Fork | 29,439 / 4,964 |
| Watchers | 149 |
| Open Issues / PRs | 167 / 72 |
| 代码行数 | 513,447（扣除 i18n locale 与 lockfile 后真实逻辑代码约 43–46 万行） |
| 语言分布 | TypeScript 66.1% / TSX 15.2% / JSON 9.9%（主要是 i18n）/ YAML 5.5%（lockfile）/ JavaScript 2.6% / CSS 0.5% |
| License | MIT（v0.3.0 起；早期为 AGPL-3.0） |
| 项目年龄 | 5.7 个月（首次提交 2026-03-12） |
| 开发阶段 | 密集开发 |
| 贡献模式 | 学术机构准职业化团队（主作者 wyuc 占 67.6%，5–6 人第二梯队） |
| 热度定位 | 大众热门 |
| Release | v1.0.0（共 55 tag = 9 产品版本 + 46 monorepo 子包版本，双轨语义化版本，平均 19 天一个版本） |
| 质量评级 | 代码[优秀] 文档[优秀] 测试[充分] CI/CD[完善] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

清华大学 MAIC 团队（THU-MAIC = Tsinghua University Multi-Agent Interaction Center）是刘知远教授领衔、于济凡（教育研究院）主导的 AI+教育交叉团队，从 MOOC 到 MAIC 的概念提出者。组织账号 2024-03 创建，旗下有 MAIC-UI（129★，生成式课件工具）、MAIC-Core（核心算法库）、SimClass（NAACL 2025 论文配套）、Awesome-AI-Era-Edu（81★）等学术血缘项目，明确「教育 LLM Agent」为研究方向。

### 问题判断

作者看到的不是「AI 能不能教课」，而是「MOOC 范式本身需要被革命」：MOOC 是「录像 + 测试」的被动学习，而 MAIC（Massive AI-empowered Courses）是「AI 教师带 AI 同学陪你讨论、做项目、纠错」的主动学习。时机选择也很精准——LLM 多 Agent 编排成熟到可以做实时课堂交互、22 种教学法在 skill 协议层落地、Provider-neutral 架构让自部署可行，三个条件同时满足才有这个项目。

### 解法哲学

**教育理论先行**——布鲁姆分类法、ZPD、UDL 不是文档里的口号，是被编码进 scene 类型与 stage 设计的可执行约束。**决策/执行严格分离**——LangGraph 1.1 StateGraph 做编排骨架（Director 节点单 LLM 决策 vs 单 Agent 纯逻辑 fast-path），28+ 白板原语动作是执行末端原子。**Provider-neutral**——自带 LLM/TTS/ASR/存储，无厂商锁定，Vercel/Docker/Postgres/Ollama/Lemonade/FunASR/IndexedDB 全栈自部署支持。**对比竞品明确不做的**：不做通用 Agent 框架（那是 OpenManus 的事）、不做单一 K-12 学科题库（那是 Khanmigo 的事）、不做纯对话模型（那是 EduChat 的事）。

### 战略意图

核心产品是「AI 课堂操作系统」，基础设施是 7 个 `@openmaic/*` npm 包（dsl / storage / renderer / editor / importer / generation / docs），SDK-first 拆分让第三方可脱离 App 直接复用 schema。商业化有 hosted `open.maic.chat` + OpenClaw 双轨（自部署 + SaaS 接入码），通过 `server-providers.yml` 与 `PERSISTENCE_DEV_TOKEN` 的清晰边界暗示「企业版 = 替换 `lib/persistence/server-auth.ts`」。**开源策略是 genuinely open**（MIT + 学术背书 + 自家 SDK 上 npm），不是 open-core。AGPL-3.0 → MIT 的重许可（v0.3.0）是教科书级的「想被生态采用」的策略转变。

## 核心价值提炼

### 创新之处

按新颖度×实用性排序：

1. **教育学软件化为 Skill 协议**（SKILL.md + constraint.yaml + Outline adapter）
   把 22 种教学法（Feynman/Spiral/UDL/Workshop/Vocational/K-12 Core Literacy/SEL/Understanding by Design……）变成「目录 + frontmatter + 可选机器校验」，由 outline 生成器在 prompt 内消费 + 后置校验。领域知识真的进了代码。

2. **Agent 会话 = 持久化事件日志 + lease fence + Worker race recovery**
   `lib/server/agent-runtime/runner.ts` 把 Postgres 当 Raft log，lease 丢失即视为夺权，事件永远持久化，resume 据 entry tree 决定 replay 范围。等于把分布式系统的 lease 思路塞进 LLM 长会话。

3. **白板「运行时一等公民」+ 28 原子动作原语**
   白板不是装饰，是带坐标/line-id/edit-op 的可执行对象；`wb_edit_code` 行级增删改 + `wb_draw_code` 头部偏移感知（代码区起 y+32）；动作经 Director Graph → WhiteboardActionRecord ledger → choreography timeline → renderer 重放。

4. **Settings「失败 ≠ 不存在」状态机**（KVStore + Outcome/KeyState）
   `kv-persist.ts` 用 Outcome 类型把「读/写失败」显式化，localStorage 那种「读失败 = 空」的不安全语义被禁止。任何从浏览器迁到服务端 KV 的项目可借鉴。

5. **Pi Agent Core + OpenMAIC connector 模式**（STUB_MODEL + 注入 StreamFn）
   给 pi 一个 1M context 的 `STUB_MODEL`，真实模型由 OpenMAIC 自己通过 `streamFn` 解析；让 pi 跑 LLM 元数据兼容性同时保留 OpenMAIC 的模型路由/思考配置。

6. **SDK-first 拆分 + App-consuming-packages**
   把 DSL、storage、renderer、importer、editor、generation、docs 各自作为独立 npm 包，App 仅是「消费者」；`@openmaic/generation` v0.3.2 后取代了 `lib/generation`，App 端 `lib/generation` 直接被删。

7. **PBL v2 项目式学习的 append-only 事件账 + 缓存摘要**（EngagementSummary）
   「PBLEngagementEvent[] 事件流为真相」与「completion-time 缓存的 PBLEngagementSummary」分层，`signature → human-readable concept name` 在缓存层维护本地化概念名。

### 可复用的模式与技巧

可直接迁移到其他项目的设计模式和代码技巧：

1. **Outcome/KeyState 状态机包异步 KVStore**：用类型系统强制「读取失败 ≠ 空，写入失败 ≠ 成功」（`kv-persist.ts` 注释本身就是一篇教学）
2. **Agent lease fence + Postgres event log**：把分布式系统思路塞进 LLM 会话（`runner.ts` 的 `writeRequiredSessionEntry` + `isLeaseLostError` 巡检）
3. **Director Graph 单轮拓扑 + 客户端序列化驱动多 Agent**：替代「maxTurns」（可中断、可恢复、单测简单）
4. **STUB_MODEL + 注入 StreamFn**：在第三方 Agent SDK 下保留自家 provider/路由/思考控制（`build-agent.ts`）
5. **TypeBox → JSON Schema 单源契约**：7 个 SDK 包共享同一份 schema（`@openmaic/dsl` + `gen-schema.mjs`）
6. **运行时 URL import 绕过打包器限制**：`sync-maic-importer.mjs` 把 pdfjs-dist 类难打包依赖变成运行时 vendor

### 关键设计决策

值得学习的架构选择和 trade-off 分析：

1. **决策**：Agent 会话用 PostgreSQL lease + 心跳 + 持久化事件日志，workerId+attempt 二元 fence
   - 问题：Web 长连接断开/容器重启/水平扩容下，L Agent 会话可能并发跑两次或丢失中间状态
   - 方案：`runner.ts` 把 lease 心跳和 `AgentSessionLeaseLostError` 错误链巡检做进事件总线；每次「必须写入」经 `writeRequiredSessionEntry` 包裹，lease 丢失时让出而不是抛错
   - Trade-off：多了一次 DB round-trip、lease 间隔需调优；换来「cancel/resume/steer 任意时刻」+「多 worker 不会撞车」
   - 可迁移性：高

2. **决策**：用 `@openmaic/dsl` + TypeBox 在 build 时生成 JSON Schema，SDK 与 App 共享单契约
   - 问题：renderer/importer/app 三端各自改字段，契约漂移
   - 方案：`packages/@openmaic/dsl` 把所有 PBL 角色/项目/线程席类型、教学场景类型都收进「契约」层，re-export `PBLProject, PBLRole, ...`；build 时跑 `gen-schema.mjs` 写 JSON Schema
   - Trade-off：多一个 build step；换来 npm 可独立发布 + 第三方可消费 schema
   - 可迁移性：高

3. **决策**：KVStore/DocumentStore/RuntimeStore/AssetStore/SkillStore/MaterialStore 六类后端各做「接口 + 三实现」（browser / http / pg + s3 bytes）
   - 问题：自部署场景差异巨大（纯浏览器 / 单机 Postgres / 阿里云 OSS + S3）
   - 方案：`@openmaic/storage` 把「设备/账户」scope 作为 first-class；`kv-persist.ts` 在 App 内通过 Outcome/KeyState 状态机强制「失败 ≠ 不存在」语义
   - Trade-off：抽象层带来 7 个 npm 包；换来 server-backed / self-hosted / browser 三模式同源代码
   - 可迁移性：中-高

4. **决策**：Director 单轮图拓扑（START → director → END）而非「maxTurns」
   - 问题：多 Agent 讨论易跑飞/绕圈，需要可证明的边界
   - 方案：`director-graph.ts` 注释明写「每次请求至多一个 director→agent 周期……拓扑本身就是约束，无需 maxTurns 上限」；客户端序列化多请求驱动多 Agent 讨论
   - Trade-off：多 Agent 讨论是「客户端驱动多轮」而非服务端长图；换来可中断/可恢复/单测简单
   - 可迁移性：高

5. **决策**：Skill 协议 = SKILL.md（frontmatter）+ 可选 constraint.yaml（机器可校验）+ Outline adapter
   - 问题：教学法知识需要可被 Agent 发现、可被 outline 生成器消费、机器可校验
   - 方案：`skills.ts` 把 pi-agent-core 的 `loadSkills()` 做 native discovery，SKILL.md 文本进 outline prompt 的 `teacherContext` slot，constraint.yaml 在 outline 生成后做后置校验
   - Trade-off：三处各自维护；换来「教学法可被组合」
   - 可迁移性：高

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | OpenMAIC | Khanmigo | Duolingo Max | MAIC-UI（自家） | EduChat | OpenManus |
|------|---------|---------|------------|--------------|---------|----------|
| Stars | 29,439 | 闭源 | 闭源 | 129 | 580+ | ~50k |
| 开源 | MIT | 闭源 | 闭源 | MIT/Apache | Apache-2.0 | MIT |
| 多 Agent | ✅ 真多 Agent | ❌ 单一 AI 辅导员 | ⚠️ 角色扮演 | ⚠️ 偏单 Agent | ❌ 单一对话模型 | ✅ 通用 |
| 白板原语 | ✅ 28+ 原子动作 | ❌ | ❌ | ⚠️ 弱 | ❌ | ❌ |
| 教育垂直 | ✅ 深（含 PBL） | ✅ K-12 题库 | ⚠️ 仅语言 | ✅ 课件生成 | ✅ 对话 | ❌ 通用 |
| 学术背书 | JCST 2026 | Khan Academy | Duolingo | THU-MAIC | ECNU-ICALK | MetaGPT |
| Provider-neutral | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| 自部署 | ✅ 全栈 | ❌ | ❌ | ⚠️ 前端 | ⚠️ 模型 | ✅ |

### 差异化护城河

- **学术背书护城河**：JCST 2026 22 作者 + Wu Wenjun 奖 + 教育部 AI 安全优秀案例，三重背书难以快速复制
- **教育垂直深护城河**：PBL v2 + 22 教学 skill + 10 万真实交互数据（清华校内 700+ 学生验证），通用框架无法一蹴而就
- **全栈开源护城河**：7 个 npm SDK + MIT + Provider-neutral + 多端持久化，闭源商业产品短期内不会开放

### 竞争风险

- **最可能被替代的方向**：「通用 Agent 框架 + 教育 prompt 库」组合（如 OpenManus + 教学 prompt 模板），但需要补足 PBL v2 + 白板原语 + 教学 skill 三件事
- **次风险**：Khanmigo 突然开放或多邻国扩张到非语言学习，但闭源产品的开放速度通常很慢
- **内部风险**：主作者 wyuc 占 67.6% 的单人主导，单点依赖风险明确

### 生态定位

教育多 Agent 编排的事实标准——下游接 LMS/消息应用（OpenClaw 已接入飞书/Slack/Discord/Telegram），上游接各类 LLM Provider（OpenAI/Anthropic/通义/本地 Ollama/Lemonade/FunASR），横向接 S3/Postgres/IndexedDB。在整个 AI+教育生态中，OpenMAIC 填补了「LLM 能力 → 真实课堂」之间的工程空白，不是「又一个 ChatGPT 套壳」。

## 套利机会分析

- **信息差**：不被低估——热度已充分反映其学术权威性与工程成熟度，4949 fork、72 PR、167 open issues 的「高活跃社区」信号表明已进入「主流产品+学术成果」阶段，无套利空间
- **技术借鉴**：Lease fence + Postgres event log、Outcome/KeyState 状态机、Skill = SKILL.md + constraint.yaml、STUB_MODEL + 注入 StreamFn——四件事最有借鉴价值
- **生态位**：填补「LLM 能力 → 真实教育场景」之间的工程空白，是学术-工程-教育三栖的稀缺资产
- **趋势判断**：在增长——AI+教育赛道整体上行（多邻国/Khan Academy/可汗都在重金投入），OpenMAIC 凭借清华学术血缘 + MIT 许可 + 5.7 月近 30k 星，几乎占据开源领域「事实标准」位置，后发优势明显

## 风险与不足

- **settings 链路技术债**：`lib/store/settings.ts`（2180 行）+ `components/settings/index.tsx`（1207 行）+ settings-validation.ts（129 行）三热路径，Top issues 中三条高热 bug 全部落在配置链路（#240 点击常规设置就报错、#374 配置了 API-Key 仍提示选择模型、#287 ACCESS_CODE 覆盖 server-side API Key）
- **生产化阻力**：ACCESS_CODE 与服务端 API Key 的优先级混淆，docs 中明确标注 `PERSISTENCE_DEV_TOKEN`「无任何机密性与用户隔离」，生产部署需替换 `lib/persistence/server-auth.ts`——这是 v0.x 阶段的妥协
- **多 Agent 讨论仍偏剧本化**：Issue #152（18 条评论高讨论度）揭示当前多 Agent 讨论流程仍偏剧本化，社区对「AI 同学」人格多样性与对话涌现性有强烈期待
- **单点依赖**：主作者 wyuc 占 67.6%，单点依赖风险明确；同时 refactor 仅占 commit 5.5%，在 feature 51% 的高速扩张下重构投入偏低
- **`@maic` → `@openmaic` 重命名残留**：CHANGELOG v0.3.0 显示历史命名；当前 `packages/@openmaic/*` 已统一，但 `vendor/maic-importer/`、`file.maic.chat` 等运行时资源仍保留 maic 前缀（向后兼容）
- **`lib/pbl/legacy/` 与 `lib/pbl/v2/` 并存**：legacy 仍被引用（read.ts 入口），v2 完全接管是下一里程碑任务

## 行动建议

- **如果你要用它**：
  - 自学者：直接用 hosted `open.maic.chat` 或自部署 Vercel 一键，体验「AI 同学陪你讨论」的 PBL 模式
  - 教育者：用文档生成课件 + Workbench 编辑 + 导出 PPTX/HTML/视频
  - 消息应用团队：通过 OpenClaw 接入飞书/Slack/Discord/Telegram，把多 Agent 课堂嵌进现有 IM 流程
  - 自部署开发者：Docker compose + Postgres + S3 是生产推荐配置；必须替换 `lib/persistence/server-auth.ts`（见 Issue #287）

- **如果你要学它**：
  - 重点关注 4 个文件：
    - `lib/server/agent-runtime/runner.ts`（lease fence + Postgres event log 的最佳实践）
    - `lib/store/kv-persist.ts`（Outcome/KeyState 状态机的教学级注释）
    - `lib/orchestration/director-graph.ts`（单轮拓扑 + 客户端序列化驱动多 Agent）
    - `packages/@openmaic/dsl/` + `gen-schema.mjs`（TypeBox → JSON Schema 单源契约）
  - 重点关注 3 个目录：
    - `skills/agent-runtime/`（22 教学 skill 协议）
    - `lib/pbl/v2/`（项目式学习的 append-only 事件账 + 缓存摘要）
    - `packages/@openmaic/`（SDK-first 拆分的范例）

- **如果你要 fork 它**：
  - settings 链路重构（分域设置：LLM/TTS/ASR/Image/Video/PDF/WebSearch 各自独立 slice）—— Issue #580/#665 的根治方案
  - 多 Agent 讨论的剧本化突破（Issue #152 的人机对话需求）
  - PBL v2 完全接管 legacy（`lib/pbl/legacy/` 清理）
  - Action 单真相源目录（`lib/action/` 当前只有 `engine.ts`，动作定义散落在 4 个位置）
  - 真生产化的 auth 模块（替换 `lib/persistence/server-auth.ts` 的 dev-only 实现）

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/THU-MAIC/OpenMAIC/1.1-system-architecture（已收录，含完整三层架构 + 两阶段流水线 + 多 Agent 角色矩阵图） |
| Zread.ai | 未明确收录（WebFetch 受限，未能验证） |
| 关联论文 | [From MOOC to MAIC: Reimagine Online Teaching and Learning through LLM-driven Agents](https://jcst.ict.ac.cn/) — JCST 2026，DOI: 10.1007/s11390-025-6000-0，22 位作者，Jifan Yu 领衔；另有 NAACL 2025 SimClass 论文（同一团队前身工作） |
| 在线 Demo | https://openmaic.io/（官网，提供 producthunt/aitoolworth 多个入口）；官方 chat 域名 https://open.maic.chat/ 也可访问 |
| 外部独立分析 | [Brave2049：多智能体协作开启的交互式教育新范式](https://brave2049.com/p/1432) — 强调 MAIC 是「教育 × Agent」赛道首个真正落地的开源框架，而非「又一个聊天机器人」 |
| 外部独立分析 | [智柴网：清华开源的「N 个 Agent 教 1 个学生」](https://zhichai.net/t/177620716) — 与 Khanmigo、Duolingo Max、Coursera AI 横评，指出 OpenMAIC 的「5 种交互模式 + VoxCPM2 语音克隆 + JCST 论文背书」是商业产品缺乏的学术护城河 |

# GitHub推荐：5.9 个月 31k stars：单兵写出的 RE 协议层 REA，把逆向工程搬进 AI 时代

> GitHub: https://github.com/morluto/rea

## 一句话总结

REA（Reverse Engineer Anything）不是又一个 Ghidra MCP 包装器，而是一套**AI agent 时代的逆向工程协议层**——用一套 22 种 binary 格式、5 档证据权威、3 档置信度的统一 Evidence 信息模型，把 Hopper、Ghidra、IDA、mitmproxy、pwndbg、mitmproxy 等 12 个原生工具桥成 agent 可消费的 MCP 工具集。**真正的护城河在信息模型而非工具数量**——多数 MCP 只包装一个工具，REA 把跨引擎抽象推到「同一 schema 不同 provider」。

## 值得关注的理由

1. **现象级增长曲线**：5.9 个月从 0 到 31,025 stars，单日 +2,963 stars 被 GitHub Trending 收录；32 个 release、平均 5.4 个/月；周末占比仅 11%、深夜占比 39.8%——是「职业投入 + 跨时区协作」的饱和式迭代。
2. **真正的护城河在信息模型而非工具数量**：`src/domain/evidence.ts` 用 22 种 subject format + 5 档 authority（shipped-artifact / controlled-replay / historical-reference / external-service / analyst-inference）+ 3 档 confidence（observed / derived / inferred）+ DAG `evidence_links`，让 agent 能区分「看到的事实」和「引擎的猜测」。这套 schema 配 RFC 8785 canonicalization + sha256 digest，让 Evidence bundle 可以跨进程无损搬运。
3. **主动撤掉 AI 工具最潮的几个抽象层**：在 2024-2025「加权限 + 加 plan + 加 workflow」的潮流下，REA 反向走——ADR-0002 撤回 controlled-replay、PR #555 删 permission grants、PR #572 删 Node prepare/execute flow，roadmap 明说「plan-only tool without an executor does not establish runtime behavior」。

## 项目展示

| 类型 | 描述 |
|---|---|
| **架构图（hero）** | [rea-investigation-flow.svg](https://raw.githubusercontent.com/morluto/rea/main/website/public/assets/figures/rea-investigation-flow.svg) — 你的 agent 询问本地目标 → REA 调分析工具追踪 → agent 用返回的代码/引用/未知项来解释、实现、测试 |
| **截图** | [rea-hopper-analysis.png](https://raw.githubusercontent.com/morluto/rea/main/website/public/assets/figures/rea-hopper-analysis.png) — Hopper 内部正在跑 REA 的 analysis bridge，检查一个原生二进制 |
| **可视化** | [th04-bullet-ring.svg](https://raw.githubusercontent.com/morluto/rea/main/website/public/assets/figures/th04-bullet-ring.svg) — 16 子弹环的 fixed vs aimed 角度对比（重算 C++ 与历史编译器输出匹配） |
| **社区接入** | [discord.svg](https://raw.githubusercontent.com/morluto/rea/main/website/public/assets/figures/discord.svg) + [skills.sh 收录](https://skills.sh) |
| **增长曲线** | [Star History 动态图](https://api.star-history.com/svg?repos=morluto/rea&type=Date) — 5.9 个月从 0 到 31k |

> 素材均可在 [rea.tools](https://rea.tools) 与 [GitHub website/public/assets/figures](https://github.com/morluto/rea/tree/main/website/public/assets/figures) 直接访问。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | <https://github.com/morluto/rea> |
| Star / Fork | 31,025 / 3,732（Fork/Star 12% 健康） |
| Watcher | 99 |
| 主语言占比 | TypeScript 81.5%（295,498 行 / 1,738 文件） |
| 次语言 | JavaScript 10.0%、JSON 2.8%、Python 1.2%、Java 1.2% |
| 总代码行数 | 362,652 行（不含空行/注释） |
| 文件数量 | 2,233（其中 .ts 1,015 个 / 176,934 行） |
| 桥接层（跨语言） | 7,926 行（Hopper Python 1,132 / Ghidra Java 3,415 / Native Swift+Python / JADX / pwntools / pwndbg / mitmproxy） |
| 项目年龄 | 5.9 个月（首次提交 2026-04-14） |
| 总 commit | 1,629 |
| 近 30 天 commit | 909（占总 commit 55.8%） |
| 开发阶段 | 密集开发（饱和式迭代） |
| 开发模式 | 职业项目（周末 11.0% / 深夜 39.8%） |
| 贡献者 | 39 人（主作者 57.1%，次贡献 N0zoM1z0 14.2%、Kaoru0822 9.9%） |
| 贡献集中度 | 单人主导（bus factor = 1） |
| 当前版本 | rea-agents-6.1.0（32 个 tag，平均 5.4 个/月） |
| License | MIT |
| 热度定位 | 大众热门（与 Ghidra 27k、Binja 商用同量级，仍有 3-5 倍空间） |
| 质量评级 | 代码 5 文档 5 测试 5 CI 5 安全 4 跨平台 4（综合 4.8/5） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

morluto（个人账号，5.8 年账号龄，162 个公开仓）横跨 TypeScript / Python / Rust / Swift / Java，**多语言工具集作者**——`flameox`（118★, Python）、`jacobian`（211★, Python）、`leantoken`（41★, Rust）。Bio「member of technically staff」是社区自嘲式表述（影射大厂 member of technical staff），匿名倾向明显；位置 Sinsai 推测泰国清迈。**162 个公开仓的隐含信息**：每个工具一个独立 repo，是典型的「工具链偏好开发者」——REA 是这些工具集汇流后的旗舰。

### 问题判断

作者是**先做过 Ghidra 脚本（Java）、Hopper 脚本（Python）、LLDB tracer（Python）、Swift 桥（Swift）、browser debugger（CDP）、EVM bytecode 解析（Rust/WASM）的人**——他意识到跨工具的不是 API 差异，是**信息模型差异**。每个工具的「符号」「地址」「字符串」「引用」语义都不一样。**真正该写的是一个统一的信息模型**（subject / provider / confidence / authority / location），然后让每个工具去填它。`src/domain/evidence.ts` 就是这个信息模型。

时机选择：2026-04 启动项目时正是 **MCP 协议正式成为 Anthropic 旗下标准**的窗口期，作者判断「agent 想要可消费的逆向工具」的需求即将爆发——事实印证了这个判断，5.9 个月后 31k stars。

### 解法哲学

| 维度 | 立场 | 证据 |
|---|---|---|
| 哲学 | 组合 + 显式边界，而非「IDE 大而全」 | ADR-0002 主动撤掉 controlled-replay；roadmap 明说「plan-only tool without an executor does not establish runtime behavior」 |
| 默认 | fail-closed + 不可变快照 | Ghidra 每次开新临时项目；`/tmp` 私有根；关闭即销毁；不修改原二进制 |
| 信任 | token + Unix-socket + capability | Hopper/Ghidra 都用 `randomBytes(32).toString("hex")` 配 `hmac.compare_digest`；不在 argv/envvar 传 token |
| 错误处理 | Result + tagged error，不抛 | `src/domain/result.ts` 强制所有边界用 `{ok, value}` / `{ok, error}` |
| 商业化 | 完全不开 | 官网 rea.tools 无定价；MIT；`GHIDRA_INSTALL_DIR` 由用户提供 |
| 决定论 | 可重现的 Evidence 链 | `canonicalize`（RFC 8785）做 AnalysisProfile digest；Evidence bundle 用 byte-stable 排序导出 |
| 主动撤回 | 「plan-only tool」是反模式 | PR #572 移除 Node prepare/execute flow |
| 主动撤回 | 「permission grants」是负担 | PR #555 移除 scope ceilings、elicitation、repeated approval fields |

### 战略意图

- **核心产品定位** = MCP-native 跨引擎逆向编排层。**不是**「AI 反编译器」，**也不是**「开源版 IDA」——而是「AI 时代 RE 工具的协议适配层 + Evidence 层」。
- **商业化路径**：**目前没有**，但**有护城河**——7,926 行桥接层代码如果成熟到一定壁垒，社区会自然围绕它长出商业服务（托管的 Ghidra 集群、Hopper 教学证书、托管 Evidence 存储）。但作者用 MIT 主动让这条路「需要的话任何人都能开」，而不是自己开。
- **生态定位** = 「AI agent 的 'executable / artifact / binary' 那一面」。对标：Sourcegraph 给 agent 看代码，Browserbase 给 agent 看网页，**REA 给 agent 看二进制和它跑起来的状态**。

## 核心价值提炼

### 创新之处

按新颖度 × 实用性 × 可迁移性排序：

1. **Evidence 信息模型 + 5 档 authority + RFC 8785 digest**（4/5/5）
   - 22 种 subject format + 5 种 location kind + 3 档 confidence + 5 档 authority + DAG `evidence_links`
   - `export_evidence_bundle` / `import_evidence_bundle` 跨进程搬运，可作为 agent 之间「可信结果 IP」
   - 适用范围：任何 AI agent 工具集（搜索、爬虫、CI、ETL）

2. **no-plan-only + no-permission-grant 的产品立场**（5/4/5）
   - ADR-0002 + PR #555 + PR #572 主动撤回最潮抽象
   - 用户不被反复问「你确定吗？」，对工程师友好
   - 适用范围：CI、爬虫、agent 工作流（用户已经「在场」的场景）

3. **跨引擎统一 port + 单一 active target + profile digest**（4/4/4）
   - `AnalysisOperationPort` 抽象 12 个 provider；`BinarySession` 强制一 session 一 active target；`AnalysisProfileCommitment` 用 RFC 8785 digest 防止跨 provider 缓存污染
   - agent 只需学一套 schema（ToolContract）就能调 20 个 provider
   - 适用范围：数据库、搜索引擎、模型路由等多后端系统

4. **DX-Ball 复刻 3,205 测试用例 + 63 函数字节匹配**（5/4/3）
   - REA 团队用 REA 复刻 DOS 街机游戏中一个 sound-pan 助手函数，3,205 个原始 x86 测试用例**全部通过**，重新编译的 C 版本**字节级匹配**原 63 函数
   - 这是「AI 辅助逆向 → 行为等价复刻」第一个公开量化指标
   - 适用范围：方法论可迁移（写 conformance fixture → 实测字节匹配）

5. **Windows Job Object + DACL via Node-API add-on**（4/3/4）
   - 预编译 `rea-windows-x64.node` 把 Windows Job Object、DACL、handle admission 暴露给 JS
   - **Node 生态里「用 Windows Job Object 做 sandbox」的成熟方案几乎没有**——这是逆向工具圈从未有人解决过的空缺
   - 适用范围：CI runner、playwright、Cypress 替代

6. **借工具 + 薄桥哲学**（3/5/5）
   - 不「写一个 packet capture」，而是 `bridge/mitmproxy/capture.py` 接 mitmproxy addon；不「写一个 ELF layout 解析器」，而是 `bridge/pwntools/layout.py` 接 pwntools
   - 复用意味着永远站在成熟工具的肩膀上
   - 适用范围：任何 AI agent + native toolchain

### 可复用的模式与技巧

1. **`Result + tagged error` 代替 `throw`**：边界处强制；错误可序列化、带 typed payload、翻译为人类可读
2. **Evidence bundle 跨进程搬运**：`export_evidence_bundle` 原子写本地文件 + `import_evidence_bundle` 校验 `evidence_id` + canonical manifest + 合并
3. **跨语言桥用 NDJSON + capability token**：TypeScript 持 socket + 桥端跑在宿主引擎内 + 32 字节随机 token + `hmac.compare_digest`；TS 端只关心协议
4. **provider registry 排序 + no-fallback**：用户显式选 provider 和自动选 provider 走同一条路径；选不中就**失败**而不是 fallback——结果归责清晰
5. **bring-your-own 外部工具 + 临时项目销毁**：Ghidra 走 `GHIDRA_INSTALL_DIR` 注入；每次开新 `PrivateRuntimeRoot` 临时项目；关闭即销毁
6. **5 层测试金字塔 + 14 个真引擎 verify lane**：`domain → composition → boundary → acceptance → conformance` + `scripts/verify-real-*.mjs` 一套独立 verify 脚本每个跑真工具
7. **ToolContract = schema + effects + annotations + examples**：`effects`（mutatesTarget/Session, writesFs, launchesProcess）+ `annotations`（readOnlyHint, destructiveHint）+ `examples` 自动生成
8. **Setup 永不偷偷安装大工具**：`rea setup` 必须打印改动、要求 approval；不安装 Ghidra/Java/Node；可选装 Hopper 要 `pkexec`/apt 显式确认

### 关键设计决策

| 决策 | 问题 | 方案 | Trade-off | 可迁移性 |
|---|---|---|---|---|
| **1 个 session = 1 个 active target** | 切 target 时 provider 资源要重建 | `#transition: Promise<void>` 串行化所有切换；failed switch 回滚 | 用户开第二个 binary 必须先 close | 任何「重资源上下文 + 多入口」系统 |
| **Provider 没 fallback** | Hopper 不支持的格式 Ghidra 支持时怎么办 | `provider_id` 显式选择；`auto` 时按 registry 排序选第一个 available+supported | 不知道 provider 差异的 agent 会失败 | 任何「明确归责」的工具（数据库、搜索引擎） |
| **AnalysisProfile digest** | 同一 binary 用不同 provider 出的结果缓存不该共用 | `createAnalysisProfile` 用 RFC 8785 + sha256 | 改动任何设置都让 snapshot 失效 | 任何「工具参数 + 结果可重现」场景 |
| **Evidence 5 档 authority** | 静态分析、动态执行、外部参考的证据强度不同 | `shipped-artifact` / `controlled-replay` / `historical-reference` / `external-service` / `analyst-inference` | agent 必须理解每个标签 | 任何「AI 工具输出可信度分层」系统 |
| **Hopper GUI cursor 也是 first-class state** | 多数 MCP 把「当前选中函数」当隐式状态 | `current_address` / `current_procedure` / `goto_address` 显式 | 文档要解释两套语义 | 任何「GUI 状态 = 状态」的工具 |
| **把 native build artifact 直接打进 npm 包** | Windows 用户不想为 REA 装 Rust toolchain + VS Build Tools | 预编译 `rea-windows-x64.node` 作为 Node-API add-on | native artifact 体积大、ABI 必须锁 | 任何「Node addon 跨平台分发」的工具 |
| **Setup 不安装 Ghidra** | 用户想「装完就用」 | Ghidra 走 `GHIDRA_INSTALL_DIR` 环境变量；Hopper 可选安装但要 `pkexec`/apt 显式确认 | 多一步人工 | **强烈可迁移**：第三方大工具永远该 bring your own |
| **Ghidra 临时项目销毁** | 分析完留个 project 在用户磁盘上不安全 | 每次开新 `PrivateRuntimeRoot`，关闭时 `provider.close()` 删除 | 大 binary 重复分析时无法跨次复用 | 任何「分析未信任 binary」工具 |

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | REA | GhidraMCP (~9k★) | gxidra-mcp (~110 工具) | Binary Ninja Headless MCP (181 工具，商业) | MHDBDB (Ghidra/BN/IDA 桥) |
|------|-----|-------------------|----------------------|------------------------------------------|---------------------------|
| 覆盖引擎 | 12 个（Hopper/Ghidra/IDA/mitmproxy/pwndbg 等） | 仅 Ghidra | Ghidra（深度） | 仅 Binary Ninja | Ghidra/BN/IDA |
| 格式覆盖 | 22 种 binary/package 格式 | 单一 | 单一 | 单一 | 3 种 |
| 信息模型 | 统一 Evidence + 5 档 authority + DAG links | 无 | 无 | 弱 | 弱 |
| CLI/MCP 等价 | 完全（lifecycle + Evidence + limitations） | 无 CLI | 无 CLI | 无 CLI | 无 CLI |
| Sandbox | fail-closed + 临时项目销毁 | 无 | 无 | 无 | 无 |
| License | MIT | MIT | MIT | 商业 | MIT |
| Windows 支持 | Ghidra P0（25 read-only） | Ghidra 全功能 | Ghidra 全功能 | Windows 全功能 | 取决于宿主引擎 |
| 商业化 | 完全无 | 无 | 无 | 有 | 无 |
| 跨语言桥 | 7,926 行（Hopper Python 1,132 / Ghidra Java 3,415 / Native Swift+Python / JADX / pwntools / pwndbg / mitmproxy） | 无 | 无 | 无 | 有 |
| 量化验证 | DX-Ball 3,205 用例 + 63 函数字节匹配 | 无 | 无 | 无 | 无 |
| 文档规模 | 17 国 README + 40+ 专题 + 3 个 ADR | 文档一般 | 文档一般 | 商业文档 | 文档一般 |

### 差异化护城河

1. **跨 22 种格式的统一 Evidence 模型**（不只是 Ghidra）—— 任何「只包装 Ghidra」的 MCP 都打不到这个
2. **CLI/MCP 完全等价**（不只是 schema，是 lifecycle + Evidence + limitations）—— 多数 MCP 项目两套实现
3. **5 档 authority + 3 档 confidence + DAG links**—— 多数 MCP 不区分「看到」和「猜到」
4. **fail-closed + 临时项目销毁**—— 多数 MCP 工具没有 sandbox 边界
5. **DX-Ball 3,205 用例 + 63 函数字节匹配**—— 第一个公开的「行为等价」量化指标
6. **7,926 行跨语言桥**—— 每个原生引擎用最适合它的语言，TS 端只关心 NDJSON 协议
7. **no-plan-only + no-permission-grant 立场**—— 多数 AI 工具越加越复杂，REA 主动撤

### 竞争风险

1. **单工具深度**：如果工作流只用 Ghidra，跨引擎抽象就是负担——GhidraMCP/gxidra-mcp 仍是首选
2. **商业产品的 UX**：Binary Ninja Headless MCP、Augment Code 等用钱买 UX——REA 要「装 Hopper/Ghidra + 学 schema」，门槛不低
3. **主动删除抽象层是双刃剑**：喜欢「全自动化」的用户会失望；喜欢「自己编排」的工程师会来
4. **bus factor = 1**：57% commits 集中在单人，若作者停更，issue/PR 消化能力会骤降
5. **Hopper 商用依赖 + 语义一致性 P0（issue #55）**：Hopper 是当前**生产依赖度最高、但又是合规性最薄弱**的环节
6. **法务边界争议**：MIT 不覆盖被分析的 app，「reverse engineer anything」话术存在版权边界争议——[TheTerminal.Space](https://theterminal.space/software/rea-reverse-engineer-agents-mcp) 已点出

### 生态定位

REA 在整个技术生态中扮演「**agent 时代的逆向协议层**」——对标 `Sourcegraph` 给 agent 看的代码、`Browserbase` 给 agent 看的网页，**REA 给 agent 看二进制和它跑起来的状态**。**不是**替代 IDA/Ghidra/Hopper，而是**让它们在 agent 工作流里被调用**。

## 套利机会分析

- **信息差**：5.9 个月 31k stars 但 **DeepWiki / Zread.ai 都未收录**——中文社区主要依赖 README 翻译（[clauday.com](https://clauday.com)、[aipmclub.com](https://aipmclub.com) 已出现二次报道） + 中文科技博客，尚未形成稳定的 wiki 知识图谱，**公众号文章可以填补这个空白**
- **技术借鉴**：
  - **统一 Evidence 信息模型**（subject / provider / confidence / authority / location + DAG）可以迁移到任何 AI agent 工具集（搜索、爬虫、CI、ETL）
  - **`Result + tagged error` 模式**是 Node 生态罕见的「不抛异常」严格分层做法
  - **跨语言桥用 NDJSON + capability token + hmac** 模式可以复用到任何「跨语言多 worker」系统
  - **bring-your-own 外部工具 + 临时项目销毁**是「分析未信任 binary」工具的范本
- **生态位**：填补「AI agent + 逆向工程」垂直领域的协议层空白——不是替代 IDA/Ghidra，而是让它们在 agent 工作流里被调用
- **趋势判断**：
  - 单日 +2,963 stars + 持续版本节奏 + 17 国 README，已经构成「热度真实」的强证据
  - 32 个 release + 每月 800+ commits，距成熟期（同量级 Ghidra 27k stars、BN 商用）仍有 3-5 倍空间
  - 10 月正在进入**第二次爆发期**（9 天 810 commit）——结合 issue #740（模块化）、#1065（MCP 性能）、#55（Hopper 合规）等 P0/P1 路线图，这是「6.x → 7.x」的能力再分层期

## 风险与不足

### 技术风险
- **Hopper 商用 demo 限制**（issue #55 P0）：Hopper 是 REA 默认 GUI 引擎，但 demo 模式有 vendor limits，是项目最显眼的合规风险点
- **Windows Hopper / Windows 全功能空白**：当前只支持 25 个 read-only 操作；roadmap 已列但尚未实现
- **Obsidian 1.12.7 24MB ASAR bundle 已知故障**：触发 `RangeError: Invalid string length` 与 `unreadable_output`（[TheTerminal.Space](https://theterminal.space/software/rea-reverse-engineer-agents-mcp) 报告）

### 组织风险
- **bus factor = 1**：57% commits 集中在单人；若作者停更，issue/PR 消化能力会骤降
- **贡献者规模 vs 热度不匹配**：单日 2,963 stars 但贡献者只有 39 人，Trendshift 仅 3 个 contributors；v4.0.1 单变更 release 异常
- **MCP 性能瓶颈**（issue #1065 P1）：资源受限下的性能需要优化

### 法务风险
- **MIT 不等于克隆许可**：MIT 只保护 REA 自身，不覆盖被分析的 app
- **品牌话术与版权边界张力**：「reverse engineer anything」与第三方专有软件重建功能的合法性由用户承担
- **不内置 BN fallback**：与 agentic-malware-analysis 等商业方案相比，Hopper/Ghidra 二选一的选择面较窄

## 行动建议

### 如果你要用它
- **如果你只用 Ghidra**：GhidraMCP/gxidra-mcp 仍是首选，跨引擎抽象对你就是负担
- **如果你跨 Hopper + Ghidra + IDA + Electron + APK + 固件 + 浏览器**：REA 一个顶 5 个 MCP server，统一 schema 大幅降低心智成本
- **如果你的 binary 涉及未授权逆向**：[TheTerminal.Space](https://theterminal.space/software/rea-reverse-engineer-agents-mcp) 已划线——「合法自研或获授权 → 可用；指向第三方专有软件重建功能 → 法务风险由用户承担」
- **如果你的 binary 包含商业敏感代码**：先评估 Hopper 商用许可是否能覆盖你的使用场景（[issue #55 P0](https://github.com/morluto/rea/issues/55) 是当前最显眼的合规风险点）
- **如果你要部署到生产**：等 7.x 版本（issue #740、#1065 路线图驱动的二次爆发期）

### 如果你要学它
按这个顺序读源码：
1. **`docs/architecture.mermaid`** + `src/domain/evidence.ts`（理解信息模型）
2. **`src/contracts/toolContracts.ts`** + `src/contracts/toolContractTypes.ts` + `src/contracts/toolEffects.ts`（理解 ToolContract 抽象）
3. **`src/application/AnalysisProvider.ts`** + `src/application/binary/BinarySession.ts`（理解 provider orchestration）
4. **`bridge/hopper_bridge.py`** + `src/hopper/HopperProvider.ts`（理解一个 provider 的实际实现）
5. **`src/contracts/officialToolContracts.ts`** + `src/contracts/enhancedToolContracts.ts`（理解 20+ MCP 工具的 schema 设计）

### 如果你要 fork 它
可以改进的方向（按优先级）：
1. **Windows Hopper 支持**：当前最大空白
2. **Binary Ninja 官方 provider**：避免「自带 BN license」门槛
3. **Rizin / Cutter / GhidraSleuth 适配**：扩展原生工具矩阵
4. **AI agent 的『可观测性层』**：基于 Evidence DAG 给出「这个结论是怎么来的」可视化
5. **MCP elicitation for scoped session grants**（issue #96 已合但值得扩展）：让 agent 能「请求增量授权」

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录 |
| Zread.ai | 未收录 |
| MCP Catalog | [catalog.agentage.io](https://catalog.agentage.io/mcp/io-github-morluto-rea) |
| Glama MCP Servers | [glama.ai](https://glama.ai/mcp/servers/morluto/rea) |
| npm | [rea-agents](https://www.npmjs.com/package/rea-agents)（v6.1.0） |
| 官网 | [rea.tools](https://rea.tools) |
| Discord | [discord.gg/GkcryMnJDM](https://discord.gg/GkcryMnJDM) |
| 关联论文 | 无（逆向工程领域无对应学术路线） |
| 在线 Demo | 无（[DX-Ball 复刻](https://github.com/morluto/rea) 用 3,205 测试用例 + 63 函数字节匹配作为量化验证） |

### 独立分析视角

- [Inside REA: agent-driven reverse engineering](https://www.offsecblog.com/2026/10/inside-rea-agent-driven-reverse.html) — 提出 3 层状态模型（investigation context / tool sessions / agent checkpoints）+ Parseltongue 33 种输入扰动技术
- [REA reverse engineering agent toolkit: what it does, limits](https://theterminal.space/software/rea-reverse-engineer-agents-mcp) — 批判性：MIT 不等于克隆许可；stars ≠ adoption
- [REA: multi-tool orchestration through MCP](https://dev.to/mech_app_ai/rea-multi-tool-reverse-engineering-through-mcp-orchestration-oe5) — 把 REA 描述为 multi-tool orchestration 而非 tool-wrapping，给出 heuristic-based 工具路由规则

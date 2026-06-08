# 16.8K star 的 9router：RTK 省 token 是真本事，无限免费 AI 踩着 ToS 红线

> GitHub: https://github.com/decolua/9router

## 一句话总结

9router 是一个跑在 `localhost:20128/v1` 的 OpenAI 兼容本地 LLM 网关——把 Claude Code / Cursor / Codex / Cline / Antigravity 等编码工具，接到 40+ provider / 100+ 模型，核心四件事：**RTK 自动压缩 tool_result 省 20-40% token、3 层自动 fallback（订阅→便宜→免费）、多账号轮询、MITM 拦截硬编码端点工具**。5 个月冲到 16.8K star、MIT、npm + Docker 分发。但它的爆红建立在「免费/无限 AI」这一 **ToS 灰色甚至违规**的玩法上——本报告把合法工程价值（RTK 压缩、协议互转、fallback 编排）与灰色玩法（免费源聚合、多账号轮询、MITM 绕限速）切割分析，**不提供任何获取无限免费 AI / 绕过限额 / 逆向 provider API 的操作指南**。

## 值得关注的理由

1. **一个真正干净、可独立复用的合法创新：RTK tool_result 压缩**：`open-sse/rtk/` 在 LLM 请求侧、协议翻译后对工具输出（`git diff`/`grep`/`ls`/`tree`）做结构感知压缩——`autodetect.js` 只 peek 前 1KB（`DETECT_WINDOW=1024`）、按固定优先级正则判别类型（git-diff→grep→tree→ls→smart-truncate 等 11 种 filter），`applyFilter.js` 的 `safeApply` 用 try/catch 包裹，`compressText` 三道闸保证 **fail-open**（结果为空/变大/抛错一律静默回退原文，`is_error` 的工具结果跳过压缩以保留错误堆栈）。官方示例 47K→28K（省 40%）。这套「peek 抽样 + 类型探测 + 注册式 filter + fail-open」是任何 LLM 上下文压缩中间件的范本（且是 rtk-ai/rtk 的诚实移植，常量与 Rust 原版对齐）。
2. **几个扎实的网关工程模式**：① **OpenAI 枢纽式协议互转**——`open-sse/translator/` 用 `源→OpenAI→目标` 两段式 + 注册表，把 N² 转换降到 N×2，新增 provider 成本恒定，同生态时 `isNativePassthrough` 无损直通；② **配置化错误规则驱动的 3 层 fallback**——`accountFallback.js` 的 `ERROR_RULES`（文本规则优先于状态码）+ 指数退避（429 → 1s→2s→4s 封顶 4 分钟）+ 瞬时 503/502 先等后切 + 按 model 细粒度冷却 + `stickyLimit` 轮转兼顾均衡与会话连续性；③ **4 层 SQLite 运行时降级**（`bun:sqlite` → `better-sqlite3` → `node:sqlite` → `sql.js` WASM 兜底，保证任意环境可起）；④ **流水线式横切优化挂载点**（压缩/注入统一挂在 chatCore.js「归一化之后、派发之前」的单一节点，对所有下游通用）。
3. **一个值得警惕的「灰色护城河」样本**：它的卖点强（免费/无限），但护城河的一半建在沙地上——免费源是消耗性资产（iFlow 转收费、Qwen Code 2026-04-15 关停免费 OAuth、Gemini CLI 封号），fix 占 commit 43%（260 fix vs 168 feat）很大程度在追修被封堵的源；ToS 封号已实锤（Issue #365「disabled for violation of Terms of Service」）；MITM 装根 CA 解密所有 agent 出站 HTTPS（含凭据）是持续的隐私/安全负债；已出现 TypeScript 全功能 fork（OmniRoute），说明架构可被复刻、护城河不深。

## 项目展示

![9Router Dashboard](https://raw.githubusercontent.com/decolua/9router/master/images/9router.png?1)

> Next.js 控制台：provider 管理 / quota 追踪 / fallback combo / MITM / RTK 设置。安装 `npm i -g 9router` 或 Docker `decolua/9router`，工具侧把 OpenAI 端点指向 `localhost:20128/v1` 即可接入。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/decolua/9router（官网 9router.com） |
| Star / Fork | 16,782 / 2,537（watchers 仅 63，star∶watch≈266∶1，典型「收藏/薅羊毛」型，黏性存疑） |
| 代码行数 | 101,993 行（JavaScript 92.5%，零 TS）；852 文件；注释比 0.339（**有效**——多为 40+ provider 协议差异/Rust 移植对照的真实文档化注释） |
| 项目年龄 | 5.0 个月（2026-01-05 起，最后提交 2026-06-06，今日活跃无衰减） |
| 开发阶段 | 密集开发（近 90 天 458 commit 占 65%，5 月峰值 181；约每周 3 版） |
| 贡献模式 | **核心单人 + i18n 众包**（142 贡献者但 decolua 占 54.4%/372 commit，第二名仅 37，其余多为越/中/日/俄翻译；bus factor 低） |
| 热度定位 | 大众热门 · 爆发型（「免费 AI」强吸星，含薅羊毛需求驱动成分） |
| 版本 | v0.4.71（65 tag/64 release，SemVer，npm + Docker/GHCR 三路分发） |
| License | MIT（软件本体；作者强调「永久免费、不碰支付」，风险转嫁用户） |
| 质量评级 | 代码组织/文档/错误处理「良」· 测试/CI「偏薄」· 可持续性/ToS/隐私「差（敏感）」 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

**decolua**——11.9 年 GitHub 老号但仅 5 个公开 repo、无 bio，刻意低调的单人产品型开发者（疑似越南背景，README 有越南语版 + 多条越南语教程）。**逆向工程底色明显**：其余 repo 全是逆向方向——9remote、tiktok-api、tiktok-web-reverse-engineering、webmssdk_patch（TikTok 风控 SDK 补丁）。这条线索是理解 9router「免费」机制的钥匙：作者具备拦截 HTTPS、逆向私有 API/OAuth、绕风控的成熟能力，9router 的 MITM 拦截 + 免费 provider 接入正是这套能力的产品化延续。协作上单人主导 + 翻译众包，产品决策高度集中。

### 问题判断

AI 编码工具各自绑定单一后端，四类痛点：① 订阅额度按月清零浪费；② 限速打断编码；③ 工具调用输出（git diff/grep/ls）大量灌进上下文烧 token；④ 多 provider 手动切换。问题切入点非常「逆向工程师」式——不是「如何更好地调用官方 API」，而是「各家工具/provider 的协议、端点、限速规则各不相同，能否在客户端侧统一抹平」。README 致谢点名 CLIProxyAPI（Go 实现）为灵感来源。

### 解法哲学（网关 + RTK + 免费聚合）

三条主线在 `open-sse/handlers/chatCore.js` 串成固定解耦的流水线：`detectFormat → translateRequest（协议互转）→ compressMessages（RTK 压缩）→ injectCaveman（输出端压缩）→ getExecutor 派发`。三个 token-saver 都作用在「翻译之后、派发之前」的最终 body 上，对所有 provider 格式通用。哲学是「客户端侧拦截 + 归一化 + 优化」，把异构后端收敛成单一 OpenAI 接口。逆向背景直接投射到 `src/mitm/`——对硬编码端点、不读环境变量的工具用本地根 CA 解密重路由。

### 战略意图（开源软件不碰钱 + 风险转嫁用户）

README 反复强调「9Router 软件永久免费、从不收费、Dashboard 成本只是 savings tracker」。战略上软件本体保持干净的 MIT 开源（不碰支付、不托管凭据），把所有商业/合规风险留在用户侧：用户自己连免费源、自己多账号轮询、自己装根 CA。作者诚实在 FAQ 写明 Gemini CLI 在非 CLI 工具里「may result in account bans」、iFlow 转收费、Qwen 免费 OAuth 已关停——但封号成本由用户承担。与 LiteLLM「只接官方 API」的取舍相反，9router 选择走灰色换「免费」卖点，护城河也来自于此（也是最大风险源）。

## 核心价值提炼

### 创新之处

1. **RTK tool_result 结构感知压缩（peek + autodetect + fail-open）**（新颖度 4/5，实用性 5/5，可迁移性 5/5）：翻译前对工具输出做类型探测式压缩，覆盖 6 种消息形态、11 种 filter，全程静默回退。本项目最干净、最可复用的合法创新（竞品普遍无自动 tool_result 压缩）。适用任何 agent 网关/上下文压缩中间件。
2. **OpenAI 枢纽式协议互转 + native passthrough 短路**（新颖度 3/5，实用性 5/5，可迁移性 5/5）：N×2 适配器抹平 8+ 种 agent/provider 格式双向转换，同生态时无损直通。适用多协议 LLM 网关。
3. **配置化错误规则驱动的 3 层 fallback + sticky round-robin**（新颖度 3/5，实用性 4/5）：文本/状态码规则表 + 指数退避 + 按 model 细粒度冷却 + stickyLimit 轮转。适用多上游高可用代理。
4. **4 层 SQLite 运行时降级**（新颖度 3/5，实用性 4/5，可迁移性 4/5）：bun/better/node/sql.js 能力探测兜底，保证任意环境可起。适用跨运行时分发的 Node 应用。
5. **Caveman/文言文输出压缩提示**（新颖度 3/5，实用性 3/5）：分级 prompt 注入降 output token，带技术内容保护边界（代码/路径/命令/错误/安全警告保持原样）。

### 可复用的模式与技巧

- **Canonical-pivot 适配器枢纽**：用中立中间表示（OpenAI 格式）做枢纽，只写 `X→canonical`/`canonical→X`，把 N² 转换降到 N×2 + lazy 注册表——任何多协议/多格式互转系统。
- **Peek 抽样 + 类型探测 + 注册式 filter + fail-open**：只看前 1KB 判类型、查注册表选处理器、try/catch 包裹且失败回退原文、绝不放大/清空——任何不可信内容的有损优化中间件。
- **配置驱动错误分类 + 指数退避 + sticky 轮转**：fallback 决策抽成可编辑规则表（文本优先于状态码），瞬时错误先等后切——多上游代理/重试编排。
- **能力探测式多适配器降级**：按运行时探测依赖、逐级 fallback 到纯 JS 兜底，同接口多实现——需在受限/异构环境分发的库。
- **流水线式横切优化挂载点**：压缩/注入等横切关注点统一挂在「归一化之后、派发之前」的单一节点，对所有下游通用——需对多后端统一加工的网关。

### 关键设计决策

最值得记录的是 **「客户端侧拦截 + 归一化 + 优化」的流水线总装**，它把合法价值与灰色玩法都收口在同一架构里。`chatCore.js` 的固定流水线（detectFormat → translateRequest → compressMessages → injectCaveman → 派发）让三个 token-saver 作用在协议归一化之后的最终 body 上——对所有 provider 通用，这是干净的工程。但同一套「客户端侧拦截重写」能力，延伸到 `src/mitm/` 就踩进灰色：对 Antigravity 等硬编码端点工具，`cert/rootCA.js` 用 node-forge 自签 10 年根 CA、按需签发叶证书，`manager.js` 改写系统 hosts 把目标域名劫持到本地，解密出站 HTTPS 后改写 model 重路由。`server.js` 里有一处 `HOST_REWRITE`（注释自陈把官方域名改写到限速更松的同源端点以绕 PROD 的 429）和 `claudeCloaking`（给客户端工具名加 `_cc` 后缀，注释标 anti-ban）——这些是规避检测/限速行为，普遍违反 provider ToS。Trade-off 很清楚：MITM 让「不可配置端点的工具也能接入」（技术上巧妙），但代价是①该进程可见全部流量含凭据（隐私/安全面极大）②改写到非官方端点 + 工具名混淆是规避行为③hosts 劫持是系统级副作用（崩溃时可能残留）。**合法的网关价值与灰色的绕限玩法在架构上深度耦合，是这个项目最核心的张力。**

## 竞品格局与定位

| 项目 | Stars | 定位 | 与 9router 关系 |
|------|------|------|------|
| LiteLLM (BerriAI) | ~49.5K | 生产级 LLM 网关（100+ provider，纯官方 API） | 几乎不正面竞争：LiteLLM 是企业基础设施、强调合规可观测、**不碰免费/灰色**；RTK 自动 tool_result 压缩是 9router 对它的唯一明确技术增量 |
| claude-code-router | ~31K | 专给 Claude Code 换后端的路由 | 9router 是其功能超集（8+ agent × 40+ provider 双向 + RTK + fallback + MITM），代价是复杂度与合规风险 |
| OpenRouter | 闭源商业 | 云端聚合 API | 托管省心合规但付费闭源；9router 是本地灰色省钱工具 |
| one-api / new-api | ~34K / ~37K | LLM 中转/分发（多租户/计费） | 定位正交：one-api 面向「卖额度」，9router 面向「省自己的额度」 |
| claude-relay-service | ~12K | 自建中转 + 拼车共享订阅 | 同踩 ToS 灰色线，与 9router「多账号轮询」思路同源 |

### 差异化护城河

① **RTK 自动 tool_result 压缩**（竞品普遍空缺，且合法、可独立复用）；② 免费/OAuth 源聚合 + MITM 拦截硬编码端点（卖点强但靠灰色支撑）。**护城河的一半建在沙地上**——免费源是消耗性资产，已出现 TS fork（OmniRoute）证明架构可被复刻。

### 竞争风险

- **ToS 封号（实锤）**：Issue #365「disabled for violation of Terms of Service」、#375 封号讨论；README 自警 Gemini CLI/Antigravity「may result in account bans」；改写请求到非官方端点 + 工具名混淆是规避行为。
- **可持续性低**：免费源「打地鼠」式存在（iFlow 转收费、Qwen 2026-04-15 关停 OAuth），fix 43% 多在追修被封堵的源。「今天能白嫖，不代表下个月还能。」
- **MITM 隐私/安全负债**：装根 CA 解密所有 agent 出站 HTTPS（含 API key/OAuth token/全部代码上下文），信任边界完全押在单人代码与本机安全——企业/敏感代码场景不建议。
- **稳定性 + 单人 bus factor**：#244 额度反而烧太快（代理/重试放大请求量）、#987 SQLite 起不来、#1142 启动被杀；测试薄（61 测试对 114K 行）、CI 弱（仅 2 workflow，无 lint/test 闸）。

### 生态定位

个人开发者的「灰色省钱网关」。**RTK + 协议互转是可以剥离出来、长期有价值的合法工程资产；免费聚合 + MITM 是高维护、高风险、随 provider 政策波动的部分。** 若只把 9router 当「用自己付费 API key 的统一网关 + token 省钱工具」使用，是合规且有用的——问题全部出在「免费/多账号/绕限额」这一层。

## 套利机会分析

- **信息差**：9router 是「LLM 网关赛道 + AI 编码工具省钱」的高话题项目，但内容须**客观平衡**——RTK 压缩这一真创新（对标 headroom 的压缩但更轻、更聚焦工具输出）值得深挖，同时如实呈现 ToS/封号/可持续性/MITM 隐私四重风险。中文圈对「RTK fail-open 压缩」「OpenAI 枢纽协议互转」「4 层 SQLite 兜底」的技术拆解，以及对「灰色免费玩法的真实代价」的冷静评估都稀缺。
- **技术借鉴（聚焦合法可迁移）**：Canonical-pivot 适配器枢纽、peek+autodetect+fail-open 压缩、配置化 fallback 错误规则、能力探测多适配器降级、流水线横切挂载点——这些可迁移到任何多协议网关/上下文压缩/跨运行时工具。
- **生态位**：与 LiteLLM（合规生产网关）错位、与 one-api（卖额度）正交；RTK 是它对所有「正经网关」的唯一技术增量。
- **趋势判断**：踩在「AI 编码成本 + LLM 网关」趋势上；但「免费」可持续性差、ToS 风险实锤——长期价值在 RTK + 协议互转这层合法资产，而非随 provider 政策波动的免费聚合。

## 风险与不足

- **ToS 违规 + 封号（已实锤）**：多账号轮询/共享订阅/非官方代理用订阅/改写到非官方端点普遍违反 provider ToS，已有用户被封号。
- **「免费」不可持续**：免费源消耗性，provider 一封堵即失效，需持续追修（fix 43%）。
- **MITM 隐私/安全（敏感）**：根 CA + 解密全流量 + hosts 劫持 = 持续的信任负债，凭据/代码全经本地代理。
- **测试薄 + CI 弱**：61 测试对 114K 行，MITM/fallback/executors 大面积无测；仅 2 workflow 无质量闸。
- **单人 bus factor**：decolua 占 54.4%，社区贡献限于 i18n；TS fork 旁证架构可复刻但社区分散。
- **稳定性**：#244 额度反烧更快、#987/#1142 启动/驱动类崩溃活跃。

## 行动建议

- **如果你要用它**：仅推荐当作「**用自己付费 API key 的统一网关 + RTK token 省钱工具**」使用（这层合规且有用）；要用「免费/多账号/MITM」层须自担封号、隐私、可持续性风险，**敏感/企业代码场景不建议**（MITM 解密全流量）。`npm i -g 9router`（认准官方名，有仿冒包 n9router）或 Docker。
- **如果你要学它**：直奔 `open-sse/translator/index.js`（OpenAI 枢纽协议互转）+ `open-sse/rtk/`（caveman.js + autodetect.js + applyFilter.js + filters/，RTK 压缩，最值得抄的合法创新）+ `open-sse/handlers/chatCore.js`（流水线总装）+ `open-sse/services/combo.js` + `accountFallback.js`（fallback 编排）+ `src/lib/db/driver.js`（4 层 SQLite 兜底）。
- **如果你要 fork / 借鉴它**：RTK 压缩、canonical-pivot 协议互转、配置化 fallback、能力探测多适配器降级是可直接迁移的合法设计（RTK 本身是 rtk-ai/rtk 的移植，可直接看上游）。MIT 友好；但**不要照搬 MITM/多账号绕限那一层**——那是 ToS 违规 + 安全负债。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/decolua/9router（架构梳理质量高） |
| 上游 RTK | rtk-ai/rtk（9router 的 RTK 压缩是其移植，看原版理解算法） |
| 灵感来源 | CLIProxyAPI（Go 实现的 LLM 代理，README 致谢点名） |
| 合规对照 | LiteLLM（github.com/BerriAI/litellm，纯官方 API 的生产网关，理解「合规网关」长什么样） |
| 安装 | `npm i -g 9router`（认准官方名）/ Docker `decolua/9router` / GHCR |

# GitHub推荐：18 岁电信人 90 天写出 7.7K stars：openGym 把健身数据从订阅手里夺回

> GitHub: https://github.com/duartesantos8/opengym

## 一句话总结

openGym 是一款 **AGPL v3 + Passkey + 自托管 + BYOK AI Coach** 的 PWA 健身追踪器，用「112 个纯函数 + 157 个共置测试 + 0 个付费版」的极简哲学挑战 Hevy/Strong 的 SaaS 锁定叙事。

## 值得关注的理由

- **2.7 个月 7701 stars / 1524 commits**：单人在周末 + 晚间高强度投入做出大众热门工具，viral 曲线罕见。
- **训练规则抽象是开源稀缺品**：progression / 1RM / recovery / sync-merge 都是纯函数 + 共置测试，CRDT-lite 同步 + 闭合 change list AI 集成——这是任何 domain-heavy 应用都该学的范式。
- **反 SaaS 锁定到极致**：不仅数据可导出，连 passkey 私钥都不上传服务器；首次把 MCP server 接到健身 app，LLM 看到的 1RM 与 UI 完全一致。

## 项目展示

![openGym banner](https://raw.githubusercontent.com/DuarteSantos8/openGym/main/assets/banner.png)

![Architecture: phone → HTTPS → nginx (web) → /api → Node api → ./data; one-shot media service; optional AI coach + MCP server](https://raw.githubusercontent.com/DuarteSantos8/openGym/main/docs/diagrams/architecture.png)

![Home screen](https://raw.githubusercontent.com/DuarteSantos8/openGym/main/assets/screenshots/home.png)

![Workout screen](https://raw.githubusercontent.com/DuarteSantos8/openGym/main/assets/screenshots/workout.png)

![Stats screen](https://raw.githubusercontent.com/DuarteSantos8/openGym/main/assets/screenshots/stats.png)

> 在线 Demo: https://opengym.duarte-santos.ch/demo/

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/duartesantos8/opengym |
| Star / Fork | 7701 / 987 |
| 代码行数 | 178,166 行（JS 50% / JSX 21.8% / JSON 19.4% / HTML 3.7% / 其他 6.4%） |
| 项目年龄 | 2.7 个月（首次提交 2026-07-18） |
| 开发阶段 | 密集开发（v1.3.10 已发，v1.3.11/12 即将来临） |
| 贡献模式 | 单人主导（主作者 DuarteSantos8 占 79.9%，30 位贡献者） |
| 热度定位 | 大众热门（爆发型增长） |
| 质量评级 | 代码 A+ / 文档 A+ / 测试 A+ |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Duarte Santos 是葡萄牙裔瑞士人，本职在 **Sunrise GmbH（瑞士电信运营商）** 做电信软件，18 岁（Portfolio 自述），自学全栈。在 Sunrise 这种企业里，他不是"为健身行业而生"的人——这反而让他能从外部视角看到现有产品的根本问题：**你每次训练的数据都被存在别人的服务器上，订阅断了就连自己以前的心率曲线都拿不回来。** 他把业余时间的高强度投入（周末 27.4% + 深夜 17%）当作「准创业级副业」来对待。

更重要的是他**主动透明披露 Claude Code 协助**——README 单独列出"How openGym is built"一节，明说"Anthropic's coding agent 起草代码，但 A person decides and ships"。这种克制与透明在 2026 年由 AI 协作开发的项目里是稀有品质。

### 问题判断

Duarte 看到了什么别人没看到或没重视的问题？

- **SaaS 锁定的"软"层面**：Hevy/Strong 不只是收费，而是"你的训练历史被绑在他方服务器，订阅断了 → 公司倒了 → 数据没了"的脆弱性。openGym 把"备份 = `tar czf data/`"当作 first-class 设计目标。
- **现有自托管方案的"硬"层面**：wger 9 年历史 + PostgreSQL 必选 + jQuery 老 UI，让想跑 homelab 的人畏惧。openGym 走「一行 `docker compose up` + 数据在挂载目录」。
- **Passkey 在自托管圈的失位**：wger/FitTrackee 都还在用户名密码。openGym 把 WebAuthn Passkey 作为默认，让"零密码登录"成为可能（passkey 私钥永不离开手机 secure hardware）。

### 解法哲学

作者明确选择了什么，以及明确不做什么：

**明确做**：纯函数训练规则（112 个模块 + 157 个共置测试）、闭合 change list AI（不能发明新 action）、BYOK（用户的支付账户边界 = 权限边界）、AGPL（任何人 fork 都得保持开源）。

**明确不做的清单**（这是稀缺的反向信号）：
- **不写社交 feed**（Hevy 的卖点，openGym 拒绝）
- **不内置营养追踪**（wger 的卖点，openGym 不做）
- **不做付费版**（README 显式声明 "AGPL, no paid tier, nothing held back for sponsors"）
- **不开 idle radio/Web-Push 来引诱用户**（仅 Web-Push 用于训练提醒）
- **不强制 AI**（BYOK + opt-in，默认用户零 AI 接触）
- **不依赖前端框架抽象**（plain node:http，不用 Express；纯函数 lib，不用 framework DSL）

### 战略意图

`docs/AI_COACH.md` 揭示两态架构：默认 `default` 镜像 ~158MB 不带 Claude Agent SDK，`API_TARGET=coach` 镜像带 ~455MB SDK + 单独 unprivileged `coach` 用户 + `./coach-auth` 卷。这表明作者在认真思考"AI 介入 = 信任边界扩张"的问题。

商业化路径上：作者已尝试周边（assets/merch 162 次修改、assets/tee 54 次修改），但**没有付费版、没有 SaaS 托管**——这是"自托管 + 周边 + 捐赠"模型（Buy Me A Coffee 链接），与 Hevy/Strong 的"订阅或买断"模型截然不同。

## 核心价值提炼

### 创新之处

按新颖度×实用性×可迁移性综合排序：

1. **「Every change carries its own stamp」字段级 sync**（`api/sync-stamps.js` 510 行 + `frontend/src/lib/sync-merge.js` 1124 行）
   - 每条记录自带 `_ts`（per-record）+ `_f`（per-field），三步合并：keepUnknown（旧版 app 不会删别人加的字段）→ mergeDeletions+mergeEdits（加而不覆盖）→ keepHeld（删了又被别的 writer 写回 = added back）
   - `_prior` 短哈希链（保留每字段最近 6 个值）+ `fingerprint` 防 stale stamp 攻击——避免旧版 app"重置为之前的值"被误判
   - **新颖度 5 / 实用性 5 / 可迁移性 4**：任何 CRDT-lite 场景都可用

2. **纯函数 + 共置测试的训练规则抽象**（`frontend/src/lib/` 112 模块 + 157 test）
   - `progression.js`（661 行）5 种 policy：off/linear/greyskull/double/time，共享 interface，新增 policy 是 plugin
   - `onerm.js` REP_CAP=12——超过 12 reps 拒绝猜测（"an estimate says more about work capacity than about maximal strength"）
   - `recovery.js`（392 行）指数 half-life + 三个 bucket（READY/RECOVERING/FATIGUED）
   - `sync-merge.js`（1124 行）28 条规则按 field type 分
   - **新颖度 5 / 实用性 5 / 可迁移性 5**：任何 domain-heavy app 都该学

3. **AI Coach allowlist payload + 闭合 change list validation**（`api/coach/core/payload.js` 585 行 + `validate.js` 627 行）
   - 五个 categories（plan/training/bodyweight/profile/cohort/prefs）每个字段 by name copy，无 spread——"a field added to the state blob next year cannot ride along by accident"
   - 18 个 change types 闭合列表，无 default case，1 次 repair round
   - **新颖度 5 / 实用性 5 / 可迁移性 5**：任何 LLM-as-feature 场景都该如此——HOSTILE NOTE 可以让模型说任何话但不能发明 change type

4. **AI 运行时按需引入** + **LockDOWN frozen**（`api/coach/adapters/claude.js`）
   - `tools: []`、`settingSources: []`、`skills: []`、`strictMcpConfig: true`——模型无 fs 工具
   - `LOCKDOWN` 是 `Object.freeze()` 并由 `adapters.test.js` 断言 by value
   - 凭证仅通过 `CLAUDE_CODE_OAUTH_TOKEN` env 传给子进程，env 从零构建而非 filter
   - **新颖度 5 / 实用性 5 / 可迁移性 5**：BYOK + opt-in AI 的范式

5. **MCP server 直读 `./data` 复用前端纯函数**（`mcp/src/tools.js`）
   - 直接 import `frontend/src/lib/history.js`、`onerm.js`、`progression.js`——LLM 看到的 1RM 与 UI 完全一致
   - stdio MCP，read-only，零额外容器/网络
   - **新颖度 4 / 实用性 5 / 可迁移性 5**：任何自托管 personal data 都能做 read-only MCP

### 可复用的模式与技巧

1. **前后端不共享构建但用 parity test 固定共享规则**：`coach-parity.test.js`、`sync-stamps-parity.test.js`、`payload-parity.test.js`——`modeOf`/`isBw`/`isPerSide` 在 payload.js 与 history.js 各一份，pin 防止 drift。任何 dual-runtime 项目都该如此。

2. **Permission 0600 per-file 而非 0700 整目录**：host bind mount 语义考虑——`./data` 整目录 0700 会让 host 上其他进程 `EACCES`；`secret`/`db.json`/`coach.json` 单独 0600。自托管项目都该学。

3. **`atomicWrite` + dir fsync**（`api/durable.js` 38 行）：write-temp → fsync file → chmod → fsync(dir)。v1.3.10 之前 200 出去后 host 断电会带回旧文件——这种 page cache + rename 顺序问题，自托管必学。

4. **Mobile 一次性 code + bearer token 配对**（`api/device-link.js` + `server.js`）：WebView 在用户域名下不能跑 Passkey ceremony，所以走 `POST /api/pair/create` + `POST /api/pair/redeem`，token 作为 `Authorization: Bearer`。PWA + 自托管场景都适用。

5. **Set row 二维正交判别器**（`workout-model.js`）：`phase: 'work' | 'warmup'` × `type: 'straight' | 'dropset' | 'restpause'`。Drop-set 的 `drops` 是 main set 之上的额外功；rest-pause 的 `clusters` 是该 row 自身 `r` 的分解（不额外加 volume，否则双计）。看似对称实则不对称，注释显式记录（`docs/dev/SET_TYPES.md`）。

6. **i18n 字段双向 cap**：UI 输入 cap + API 二次 cap（payload `PROFILE_TEXT_MAX` / `NOTE_MAX`）——即使客户端绕过 UI 也不能 send megabytes 文本。LLM-as-feature 必学。

### 关键设计决策

**决策: AI 默认不启动**
- **问题**: AI 集成要么贵（按 token 收费）要么风险（Prompt injection）
- **方案**: 默认 `default` 镜像零 SDK；BYOK；闭合 change list；HOSTILE NOTE 不能发明新 action
- **Trade-off**: 新用户少一个"哇"的 hook；但赢得"安全 + 隐私"硬约束
- **可迁移性**: 高——任何 LLM-feature 都应如此

**决策: JSON-on-disk 而非数据库**
- **问题**: 用户想 `tar czf data/` 全量备份，能 mount 到 `jq` 检查
- **方案**: `db.json` + `db.json.bak`；`atomicWrite` + `fsync` dir；损坏 fallback 都失败则 `process.exit(1)`
- **Trade-off**: 单机写入 + 单文件锁（node 单进程默认）+ 无索引；家庭实例多 profile 时 O(n) read cost 已显现
- **可迁移性**: 中——自托管友好；规模化时需迁 DB（ROADMAP 显式标注 v1.4.6 后）

**决策: 训练逻辑是纯函数 + 共置测试**
- **问题**: 健身规则（progression / 1RM / recovery / finish-workout）如果写进 UI state machine，会与框架绑定且难测试
- **方案**: 112 个 lib 模块 + 157 个 `.test.js` 同目录共置；UI 直接 import 纯函数
- **Trade-off**: 没有 "framework DSL" 抽象，新人上手成本高
- **可迁移性**: 高——任何 domain-heavy app 都该如此

**决策: Passkey 优先，password + OIDC 延后到 v1.4.6**
- **问题**: 用户名密码是 web auth 最常见的攻击面
- **方案**: 默认 Passkey（WebAuthn，passkey 私钥永不上传服务器）；mobile 走一次性 code + bearer token
- **Trade-off**: 当前阶段放弃"传统账号密码"用户，与 PocketID 等 OIDC IdP 集成的家庭场景被延后
- **可迁移性**: 高——任何面向自托管圈的项目都该认真考虑

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | openGym | wger | FitTrackee | Hevy（闭源） | Strong（闭源） |
|------|---------|------|-----------|-------------|---------------|
| **License** | AGPL v3 | AGPL v3 | MIT | 闭源 | 闭源 |
| **Stars** | 7701（2.7 月） | ~6900 | ~741 | 百万级用户 | 百万级用户 |
| **栈** | Node + React 19 PWA + Capacitor | Python/Django + Flutter | Python/Flask + Vue 3 + OpenStreetMap | 闭源 | 闭源 |
| **力量训练特性** | 1RM/Poliquin/ATG、5 progression policies、muscle recovery map | 基础 CRUD | 弱（户外为主） | 全功能 | 极简但 UX 流畅 |
| **自托管** | 一行 docker compose up，`./data` 文件夹备份 | 较复杂（PG 必选） | 中等 | 不可 | 不可 |
| **数据所有权** | 全（passkey 私钥在 secure hardware） | 全 | 全 | 他方服务器 | 他方服务器 |
| **Passkey/Auth** | WebAuthn Passkey 首选 | 用户名密码 | 用户名密码 | 用户名密码 | 用户名密码 |
| **AI Coach** | BYOK + 闭合 change list | 无 | 无 | 无 | 无 |
| **MCP** | 有（read-only，从 ./data 直读） | 无 | 无 | 无 | 无 |
| **导入/导出** | FitNotes/Strong/Hevy/CSV/Apple Health | CSV | CSV/GPX | Hevy CSV | Strong CSV（自己不能 re-import = 锁定） |
| **独特卖点** | 设计哲学 + 自托管优先 + AGPL + 数据可 fork | 多语 Weblate + 营养追踪独有 | 户外/GPX | 社交 feed + $23.99 终身买断 | 极简 UX |
| **弱点** | 年轻；exercisedb 媒体版权；JSON-on-disk debt | 老旧 UI（jQuery） | 不直接竞争（户外为主） | 闭源 = 不可自托管 | 闭源 + CSV 不能 re-import = 锁定 |

### 差异化护城河

技术护城河：
- **"反 SaaS 锁定"叙事最彻底**：不仅数据可导出，连 passkey 私钥都不上传服务器
- **AI Coach + MCP 是类别首创**：竞品都没这两个；BYOK + 闭合 change list 是负责任的 LLM-feature 范式

生态护城河：
- **依赖极简**：api 仅 2 个 production deps（@simplewebauthn/server + web-push），攻击面最小
- **国际化深度**：17 个 locale 文件每个 ~1953 行（Top 10 热点都是 locale 文件），18+ 种语言——这是 wger 的 Weblate 翻译模式做不到的"代码内化"

信任护城河：
- **AGPL v3 + 无付费版**："AGPL, no paid tier, nothing held back for sponsors"
- **AI 协作透明披露**：README 单独"How openGym is built"一节
- **单人主导 + 870+ commits**：作者亲自与 QA 一起 "kill it eighty times mid-write" 才肯发版

### 竞争风险

- **wger（最长历史 + PostgreSQL 必选 + 营养追踪独有）**：如果 openGym 未来加营养模块，会与 wger 直接竞争。但当前 wger 的 jQuery 老 UI + Flutter 移动端体验差，自托管圈仍倾向选 openGym。
- **Hevy / Strong 的用户粘性**：百万级用户已建立训练历史，迁移成本高。openGym 的导入器（FitNotes/Strong/Hevy）降低了迁移门槛，但仍需要用户主动付出精力。
- **单人主导 = bus factor=1**：作者若离开项目，节奏可能断。30 位贡献者但 Top 1 占 79.9%，目前仍非常依赖 Duarte。

### 生态定位

在整个技术生态中扮演的角色：

- **填补了"开源 + 自托管 + 力量训练深度 + 现代前端"四轴交集**：wger 老、FitTrackee 偏户外、Hevy/Strong 闭源——openGym 在这个交集上几乎无对手。
- **BYOK AI Coach 的范式输出**：`api/coach/core/payload.js` 585 行 + `validate.js` 627 行展示了"hostile note 也不能发明 change type"的边界设计——这是 LLM-as-feature 类别的稀缺范式。
- **MCP × 个人数据**：首次把"个人数据 via MCP 暴露给 LLM"做成了 read-only stdio 直读 + 零额外网络成本——任何 self-hosted personal data 都能照搬。

## 套利机会分析

- **信息差**: 热度已被市场捕捉（7701 stars / 987 forks）——不可套利 star；但价值在「理解其设计取舍」而非「抢先 star」。
- **技术借鉴**: 12 个创新点（详见上文），最值得借鉴：
  - 纯函数 + 共置测试的训练规则抽象（任何 domain-heavy app）
  - AI Coach allowlist payload + 闭合 change list（任何 LLM-as-feature）
  - Permission 0600 per-file 而非 0700 整目录（任何自托管项目）
  - MCP server 直读本地数据复用纯函数（任何 self-hosted personal data）
- **生态位**: 在「开源 + 自托管 + 力量训练 + 现代前端 + BYOK AI Coach」五维交集上几乎独占。
- **趋势判断**:
  - 项目仍在爆发期（909 commits 最近 30 天），v1.4.0 新 exercise database 是下一个观察点
  - AGPL 限制了商业 fork，但**周边（assets/merch 162 次修改）有商业化尝试**
  - 比 wger 有后发优势（更现代 UI、更少依赖、更深力量训练），比 Hevy/Strong 有信任优势（数据可 fork）

## 风险与不足

诚实评估：

1. **年龄过轻（2.7 个月）**：v1.3.10 之前的 sync bug 密集出现（CHANGELOG 显示 RC bug 日期 `2026-10-07`、`2026-10-06` 等），稳定度还在爬坡。
2. **数据库迁移是已知 debt**：`server-state-read-cost.test.js` 已经存在说明 O(n) read cost 是已知问题；ROADMAP 显式列入"唯一的兼容性 break"。
3. **exercisedb 媒体版权争议**：README L343-350 显式披露——AGPL 代码可用但媒体不能，reusing 媒体需自行取得 Gym visual 授权。
4. **i18n 翻译半自动**：18 个 locale 同步成本高（`translate-*-stage.mjs` 半手动），新增语言的边际成本不低。
5. **依赖欠年轻**：React 19、Vite、Zustand 5 都在快速迭代，长期维护成本。
6. **配对 UX 已知脆弱**（Issue #329）：Android 客户端通过 Traefik+HTTPS 自托管实例配对时 Connect 按钮刷 "Failed to fetch"，**请求根本没出设备**——这对"卖给 homelabber"的产品定位是个 UX 风险。
7. **单人主导 bus factor=1**：30 位贡献者中 Top 1 占 79.9%。

## 行动建议

- **如果你要用它**: 一行 `docker compose up` 起服务；v1.3.10 已足够稳定日常使用；如果你是 iPhone 用户，PWA 直接 add to home screen 即可；如果你是多 profile 家庭实例，注意 OIDC 集成要到 v1.4.6。
- **如果你要学它**: 重点关注：
  - `frontend/src/lib/` 112 模块 + 157 共置测试（domain logic 纯函数化的范式）
  - `api/sync-stamps.js` 510 行（CRDT-lite 字段级同步）
  - `api/coach/core/payload.js` 585 行 + `validate.js` 627 行（LLM-as-feature 边界设计）
  - `api/coach/adapters/claude.js`（AI 运行时按需引入 + LockDOWN frozen）
  - `mcp/src/tools.js`（MCP 复用前端纯函数）
- **如果你要 fork 它**: 可改进的方向：
  - 添加营养追踪（wger 的独有模块，openGym 没有）
  - 实现 PocketID / Authentik OIDC 集成（v1.4.6 之前的临时方案）
  - 把 frontend/lib 的 progression / 1RM / recovery 抽出成独立 npm 包（开源稀缺品）
  - 给 API 写第三方 CLI（#8 早期被关闭的需求，社区可能重提）

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录 |
| Zread.ai | 未收录 |
| 关联论文 | 无（消费级健身 app，无学术发表） |
| 在线 Demo | https://opengym.duarte-santos.ch/demo/ |
| 自托管指南 | https://github.com/DuarteSantos8/openGym/blob/main/docs/SELF_HOSTING.md |
| AI Coach 设计哲学 | https://github.com/DuarteSantos8/openGym/blob/main/docs/AI_COACH.md |
| Roadmap | https://github.com/DuarteSantos8/openGym/blob/main/ROADMAP.md |
| Changelog | https://github.com/DuarteSantos8/openGym/blob/main/CHANGELOG.md |
| 独立深度视角（en） | https://zendot.org/en/posts/duartesantos8-opengym |
| 独立深度视角（中） | https://blog.csdn.net/TunerT_TQ/article/details/164376047 |
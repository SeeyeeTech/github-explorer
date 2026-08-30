# GitHub推荐：13K Stars 的开源 Palantir：浏览器里的 OSINT 驾驶舱怎么把 30 个数据源收成一张照片级 3D 地球

> GitHub: https://github.com/bilawalsidhu/gods-eye-view

## 一句话总结

God's Eye View 是一个把 **30+ 公开数据源**（ADS-B / AIS / 卫星 TLE / FIRMS 火点 / Radio Browser / GBFS 共享单车等）整合进一张照片级 3D 地球的浏览器端 OSINT 工具，作者 Bilawal Sidhu（前 Google Earth/Timelapse、YouTube 5M+ 播放的「地理空间网红」）将之作为商业产品 `halfpixel.ai` 实时基线的免费版本开源，把「开源调查工具」从工程命题改写为可审计的**产品体验**。

## 值得关注的理由

1. **稀缺定位**：截至 2026-08，浏览器内同时拥有「照片级 3D 地球 + 30+ 数据层 + Voice 控制 + GLSL 着色器 + Cinematic Director」的产品几乎没有，Cesium 给底层能力，但**产品化整合**无人做过。
2. **工程深度**：不是 UI demo——`renderGovernor` 用身份键值 Set 把 Cesium 默认 60Hz 渲染改成 idle/continuous 二态、`voiceCost` 用残差归类法把 OpenAI Realtime 计费变成「宁可早退不超支」、OpenSky 单层独自消费能跑完全天（自适应 TTL + 429 cooldown + serve-stale 三层防御），每个模块都是**可迁移的工程范式**。
3. **作者势能 + 商业模式**：YouTube 5M+ 播放、Substack 38k+ 订阅的开源传播者；`halfpixel.ai` 做付费「历史时间回溯」，实时基线永远开源——这是罕见的「开源能持续走」的**双轨设计**。

## 项目展示

### README 媒体

1. ![Orbital HUD, a tracked live globe, FLIR terrain — OPEN SOURCED reveal](https://raw.githubusercontent.com/bilawalsidhu/gods-eye-view/main/docs/media/hero-open-source-reveal.gif) — 类型: hero（开源发布主视觉）
2. ![YouTube walkthrough video cover](https://img.youtube.com/vi/GRJaKcXZS94/maxresdefault.jpg) — 类型: demo（视频导览封面，作者 YouTube 频道 5M+ 播放）
3. ![Cycling a dense live globe through CRT, FLIR, NVG in one continuous view](https://raw.githubusercontent.com/bilawalsidhu/gods-eye-view/main/docs/media/01-style-sweep.gif) — 类型: demo（视觉风格：CRT / 热成像 / 夜视平滑切换）
4. ![Diving from city-scale live congestion straight into an intersection's public camera](https://raw.githubusercontent.com/bilawalsidhu/gods-eye-view/main/docs/media/05-traffic-to-cctv.gif) — 类型: demo（OSINT 路径：城市级交通 → 公共摄像头）
5. ![Tracking the ISS along its orbital path as it crosses over Ukraine](https://raw.githubusercontent.com/bilawalsidhu/gods-eye-view/main/docs/media/14-iss-over-ukraine.gif) — 类型: demo（卫星追踪：ISS 过境轨迹）

### 筛选说明

总共发现 21 个 README 媒体元素（21 GIF + 1 YouTube 封面），筛选后保留 5 个代表性 GIF/视频；舍弃：飞机驾驶舱 AR、Zilker 语音注释、机场地面交通、Google 3D 切换、空军测距、Radio Stations 等——已由入选的 style-sweep / traffic-to-cctv / iss-over-ukraine 覆盖同类能力。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/bilawalsidhu/gods-eye-view |
| Star / Fork | 13,052 / 2,575 |
| 代码行数 | 163,528（JS 91.7% / CSS 4.9% / JSON 2.4% / HTML 0.5% / Shell 0.4%） |
| 项目年龄 | 2.2 个月（首次提交 2026-06-22，公开开源 2026-08-23） |
| 开发阶段 | 稳定维护（README 改 5/5 次，源码主干已定型；halfpixel.ai 团队维护） |
| 贡献模式 | 单人主导（contributors=1，主作者 100%） |
| 热度定位 | 大众热门（13K stars / 2.5K forks，2 个月内上 GitHub Trending 头名） |
| 质量评级 | 代码 A / 文档 A / 测试 A-（单元测试 101+ .test.mjs；E2E 缺位但有 puppeteer QA harness） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Bilawal Sidhu（@bilawalsidhu）| 公司: halfpixel.ai 自建公司 | 粉丝: 2,782 | 公开仓库: 2 | 账号年龄: 4.2 年。

他前 Google Earth/Timelapse 相关背景，长期做「地理空间网红」——YouTube 5M+ 视频观看、Substack 38k+ 订阅，长期积累的**「叙事即功能」**传播势能，与 halfpixel.ai 团队的 OSINT 商业产品形成「开源为基线 + 付费做时间回溯」的双轨。这是开源项目里少见的、能直接复用 YouTube / Substack 受众反哺的样本。

### 问题判断

> "Most open-source intelligence is a pile of browser tabs. The signals are abundant, but the *interface* is the bottleneck."

他看到的不是「OSINT 数据缺」，而是「OSINT 界面糟糕」。把「5 分钟可上手的体验」作为产品承诺——给非开发者探索者、Hackathon 玩家、教育者；**主动拒绝**人脸/姓名检索、不追踪个人（明文伦理边界写进 README 与 SECURITY）。这种「把伦理姿态转化为代码结构」的取舍，让项目从一开始就避开了 OSINT 工具最容易引战的「扒个人」赛道。

### 解法哲学

1. **Local-first as product feature**：dev server 默认绑 `localhost`，API key 不上云，Voice Realtime 走临时 session token。`vite.config.js` 14 个代理 + Realtime token endpoint **集中持有所有付费 key**，浏览器只见两个白名单公钥（`GOOGLE_MAPS_API_KEY`、`CESIUM_ION_TOKEN`），并且在 `.env.example` 注释里点名 `KEYS THAT ARE DELIBERATELY CLIENT-SIDE`。
2. **Honest-by-default**：没拿到 key 的层跑内建仿真（white-dot 交通），失败永远显示 `UNAVAILABLE / DEGRADED / LOAD FAILED` 而非 spinner；Cesium 官方社区老板的话被项目化：「may be delayed, incomplete, modeled, inferred, or wrong」。
3. **Auditability over framework**：No-framework Vanilla JS + CesiumJS + Vite，让「every line of code is inspectable」——这是**把 OSINT 工具的伦理姿态转化为代码结构**的做法。
4. **Cinematic framing = UX 加速器**：GLSL 着色器（CRT/NVG/FLIR/IRONBOW/NOIR/SNOW）、「forbidden cockpit」视觉、检测覆盖盒、「intelligence HUD」五词总结——把 OSINT 从「专家工具」包装成「5 分钟可上手的体验」。

### 战略意图

- **当前 0.7.x 系列**：实时基线永远开源；`halfpixel.ai` 做付费「历史时间回溯」。README 原话：「the present is the cheap part. The moment you try to go back in time — tiling, serving, and scrubbing *what happened* — the data gets expensive. For that, we're building something cool.」
- **可扩展性优先**：CONTRIBUTING.md 列"高杠杆切入点"——加 CCTV 城市包、加数据层（接口模板 `init/enable/disable/update/destroy/getStats`）、扩 voice 工具（28 个工具/4 类工作）、加 GLSL 视觉风格、修 first-run bug。
- **被 communities absorbing 的风险已被设计对冲**：明文伦理边界 + 不与 Snowflake/Bellingcat 直接竞争，而吸引他们的下游。

> 无独立官方博客，SUBSTACK（spatialintelligence.ai）以简报为主；架构文章要点以第三方分析 + Cesium 社区 fork 案例为主。

## 核心价值提炼

### 创新之处

1. **Idle Render Governor（引用计数 holds）**：把 Cesium 默认每 vsync 重绘改成 idle/continuous 二态。`src/renderGovernor.js` 用身份键值的 Set 把"任何持续动画"注册一个 owner id 的 hold；0 holds → `requestRenderMode = true`（idle），>0 → continuous；离散突变调 `governorRequestRender('voice-token')` 触发一次 frame。Chosen 是 **Set 而不是 counter**——任一模块 double-hold/release 都不会破模型。**新颖度 5/5 | 实用性 5/5 | 可迁移性 5/5**

2. **多源 OSINT 数据馈送 6 类状态归一**：把每层 `getStats()` 杂乱的 status 字符串映射到 `ON / LOADING / DEGRADED / STALE / FALLBACK / UNAVAILABLE` 六个状态，UI 永远显示真实状态不允许静默。`data/manager.js` 的 `layerFeedState(stats)` 是核心枢纽。**新颖度 4/5 | 实用性 5/5 | 可迁移性 5/5**

3. **配额治理三件套：自适应 TTL + 429 cooldown + serve-stale**：OpenSky 一层独自消费能跑完全天。`openskyAdaptiveTtlMs` 函数按"剩余 cred"分段调 TTL（>2400 → 9s base，>1200 → 30s，>400 → 90s，其他 300s，实测 18h+ 持续跑剩余）、429 cooldown（响应头 `X-Rate-Limit-Retry-After-Seconds` 接管）、serve-stale（冷却期返回 last-good + `X-OpenSky-Stale` header）。**新颖度 4/5 | 实用性 5/5 | 可迁移性 5/5**

4. **Cinematic Director + generation-token + AbortController 双层级取消**：`scenes/director.js` 用 `_loadGeneration` 单调递增让最新 LOAD 赢 + 旧的 `AbortController.signal` 让 in-flight transition 被取消；camera flight 用 `cancel: finish` 同等效用；"新 LOAD vs. 旧 LOAD" 用 `claimCameraOwnership` 释放 tracked-entity / voice-orbit；旧 `setEnabled()` 拒绝时拒绝原因被 logging+报告。**新颖度 5/5 | 实用性 4/5 | 可迁移性 4/5**

5. **Voice Cost Tracker 残差归类法**：Realtime `response.done` 的 token details 不全时，未归属的残差全部归到 audio（最贵 modality），让 cap 永远"宁可早退不超支"；unknown model id 也用 worst-case rates，杜绝"可用 model id 改成高价而 tracker 没跟上"。`inf/0/'off'` 三种"禁用"序列化 round-trip 安全。**新颖度 4/5 | 实用性 5/5 | 可迁移性 5/5**

6. **Hybrid Annotation Renderer（world drape + screen-space SVG）**：`hybridAnnotationRenderer.js` 把 footprint 转 world-space（draping）+ 把 callouts/rings/arrows 转 screen-space（SVG）；引擎 + 渲染器 + 解析器分层；world Annotation 启用 3D Tiles 的 collision。配套 9 文件 + 9 test.mjs。**新颖度 4/5 | 实用性 5/5 | 可迁移性 4/5**

7. **GLSL PostProcess 着色器即"传感器视角"**：每种 "look" 是一个有自己 uniforms 的 fragment shader（CRT/NVG/FLIR/IRONBOW/NOIR/ANIME/SNOW）；intensity 0-1 `mix(orig, filtered, intensity)` 实现平滑过渡；surveillance 模仿 PVS-14 P43 磷光闪烁。**新颖度 3/5 | 实用性 4/5 | 可迁移性 3/5**

8. **scopeMask: 望远镜遮罩 canvas**：用 2D canvas 画"望远镜遮罩"（替代此前 6 个 PostProcessStage 的 emergent 假象），边缘透明度随高度量化阶梯下降，既给"望远镜感"又不挡 NVG/FLIR tube mask。**新颖度 4/5 | 实用性 4/5 | 可迁移性 3/5**

9. **Server-Brokered API Keys 模式**：单 Vite 中间件集中持有付费 key，浏览器只见同源代理 + ephemeral token + 两个白名单 key；`.env.example` 注释把 `KEYS THAT ARE DELIBERATELY CLIENT-SIDE` 单独点名。SSRF 防御（CLOSED 端只接固定白名单 upstream）、地址钉死 TLS、Radio 不缓存音频、不开放任意 URL 抓取。**新颖度 4/5 | 实用性 5/5 | 可迁移性 5/5**

10. **Voice-friendly Tool Surface 保证"不发明工具名"**：`vite.config.js` 的 Realtime instructions 大段 "disambiguation table"、"counting contract"、"in your window/in view" 口径明确；28 个声明在 server 端的工具 + 客户端 `gevActions.js` 实施——禁止 naming conventions 之外的工具被调用。**新颖度 3/5 | 实用性 5/5 | 可迁移性 5/5**

### 可复用的模式与技巧

| 模式 | 适用场景 |
|---|---|
| **Render Governor 模式** | 任何基于 Cesium/Three/Mapbox 的复杂可视化项目，凡是有"长时间挂着但用户没操作"时段 |
| **Server-Brokered API Keys 模式** | 个人/小团队要把多个付费 SaaS 接到本地项目里，又不希望生产部署时大改架构 |
| **配额治理（Adaptive TTL + 429 Cooldown + Serve-Stale）模式** | 任何有"按配额计费"上游（OpenAI、TomTom、Mapbox、HERE） |
| **Layer Feed State 六分类模式** | 任何"多数据源 + 必须诚实"产品 |
| **Cinematic Recording Generation-Token + AbortController 模式** | 任何有"长 await 链 + 实时用户打断"的应用 |
| **Voice Tool Surface Disambiguation 模式** | 任何"语音/对话 AI + 多层语义层级"的产品 |
| **Voice Cost Tracker 残差归类法** | 任何按 token 计费的 LLM 实时 API |
| **Scope-Mask 2D Canvas 替代 PostProcessStage 链** | 任何有"应用级视觉覆盖"但不参与 3D 渲染的产品 |
| **Web Worker 化的 Overlay 仲裁** | 大量 2D overlay 在 Cesium/Mapbox/Leaflet 上的图层管理 |

### 关键设计决策

1. **决策**: Render Governor — 引用计数 + identity-keyed holds
   - **问题**: Cesium 默认每 vsync 重绘，跑空场景时 GPU/CPU 也在烧（~60% GPU / ~54% 一个 core）
   - **方案**: `src/renderGovernor.js` 用 Set 把「任何 per-frame 动画」注册一个 owner id 的 hold；0 holds → idle；>0 → continuous
   - **Trade-off**: 多了一个必须严格被各模块调对的契约；任一持续动画都要 `holdContinuousRender` / `releaseContinuousRender`
   - **可迁移性**: **高** — 任何基于 Cesium/Three.js 的应用都能复用，把 idle 渲染成本从"始终满载"降到"按需"

2. **决策**: 双重 Secret Handling — Vite middleware broker 持有所有 secret
   - **问题**: 用户免费 key vs. 隐私/计费/SSRF 风险矛盾
   - **方案**: `vite.config.js` 把 14 个代理 + Realtime token endpoint 集中持有 OPENAI/AISStream/OpenSky/TomTom/FIRMS 等长密钥；只有 `GOOGLE_MAPS_API_KEY` 与 `CESIUM_ION_TOKEN` 进 `define` 注入客户端
   - **Trade-off**: 每次 dev/preview server 都要跑（线上部署也要一个 Node 反代或等价抽象）；换来 SSRF 防御、地址钉死 TLS、Radio 不缓存音频
   - **可迁移性**: **高** — 是 SECURE-BY-DEFAULT 而非可选加固

3. **决策**: 配额治理做成"自适应 + cooldown + serve-stale" 三层防御
   - **问题**: 一个下午不关应用就能跑完一天的 OpenSky 配额
   - **方案**: 自适应 TTL（按"剩余 cred"分段）+ 429 cooldown（响应头接管）+ serve-stale（冷却期返回 last-good）
   - **Trade-off**: 不同速率段有时差最多 5min；换来"一整天的探索不会让夜间飞行层硬死"
   - **可迁移性**: **高** — 这种"credit-aware backoff"对任何按请求计费 + 按量配额的 API 都通用

4. **决策**: 数据源契约 — 每个层一个 module，接口集 `init/enable/disable/update/destroy/getStats`
   - **问题**: 30+ 异构数据源各自为政，数据层管理变成"逐个 if-else"
   - **方案**: 模块化（每个层独立 `.js`，可被 DataLayerManager `register()`）；lifecycle 严格序列化；有 lifecycle rejection / param rejection 区分
   - **Trade-off**: 跨层共享工具仍需明确放置；换来"加新层 = 模板 + 注册"，极度可扩展
   - **可迁移性**: **高** — 任何数据可视化项目的 layer system

5. **决策**: Node 24.14+ 强制 + Vite 6 + ESM + 没有 framework
   - **问题**: 不想要 React/Vue/Svelte 这一层抽象，因为 OSINT 工具要被审计
   - **方案**: `package.json` `engines: { node: ">=24.14.0 <25 || >=26 <27" }`，测试运行器在 Node 24 下解析并跑 `--expose-gc` 分配微基准
   - **Trade-off**: 限制了受众（GitHub issues 显示这一条卡掉大量初学者）；换来"代码短平快 + GC 行为可重复 + test 标定真实"
   - **可迁移性**: **低** — 较激进；但"把昂贵的无 framework 项目显式告诉用户门在哪儿"思路可借鉴

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | God's Eye View | CesiumGS/cesium | Shadowbroker | WorldMonitor | TerriaJS |
|------|---------------|-----------------|--------------|--------------|----------|
| 定位 | 浏览器 OSINT 驾驶舱 | 底层 3D globe 引擎 | 后端/CLI 风格 OSINT 工厂 | 单页 OSINT dashboard | 数字孪生 / 科学数据 catalog |
| 体验形态 | 单人沉浸式 + Voice + 着色器 | 工具/平台 | 自动化工作流 | 快速看一片地区 | 政府/科研场景 |
| Stars | 13,052 | 15,600 | ~9,400 | 中等 | ~1,300 |
| 数据层 | 30+ OSINT | N/A（库） | 后端 pipeline | 多域 dashboard | catalog 驱动 |
| 3D 地球 | ✅ 照片级 | ✅ | ❌ | ❌ | ✅（老式） |
| Voice 控制 | ✅ 28 工具 | ❌ | ❌ | ❌ | ❌ |
| 本地优先 | ✅ | N/A | ❌ | ❌ | ❌ |

### 差异化护城河

- **技术护城河**：5 个独立但相互支撑的工程系统（Render Governor + Layer Feed State + 配额治理 + Cinematic Director + Voice Cost）短期无等价竞品
- **生态护城河**：YouTube 5M+ 播放、Substack 38k+ 订阅的开源传播势能；CESIUM 社区论坛出现 fork 案例（Smart Work Zones）；GitHub Trending 头名
- **信任护城河**：明文伦理边界（拒绝人脸/姓名检索）+ DataSources.md 把所有第三方 license 单独 carve-out（TeleGeography CC BY-NC-SA 标红警告）+ halfpixel.ai 商业版未来不会污染开源基线

### 竞争风险

- **最大风险**：Node 24 强制 + Google Maps API key 强制 + 多层复杂状态机——onboarding 摩擦大；这些成为 README 的「梯子」但也是**用户流失点**（见 issue #74 / #76 / #86）
- **次大风险**：halfpixel.ai 商业版未来可能拉走哪些决策（如果他们决定把核心 Cinematic Director 转付费，可能动摇开源社区信心）
- **被替代场景**：Cesium 官方如果做"开箱即用 OSINT 模板"，或 Snowflake 接入 STT/voice 能力给类似 GitHub 工具的投入

### 生态定位

"OSINT 创作者/学习者的可审计浏览器工具 + 商业级时间回溯产品的免费基线"两层栈；是开源 OSINT 子方向中的"美学派"，而非"工程派"（它应工程上可以是 Cesium 之上的精致应用，不是 Palantir 替代）。

## 套利机会分析

- **信息差**: 13K stars + 大众热门已不再是被低估；但 **叙事溢价仍在**——"浏览器里的间谍卫星" / "开源 Palantir" 的传播梗让它比纯技术仓库获得更多关注。可借鉴的"创作者驱动 OSS"打法（YouTube + Substack 同步发布 + 公开 Trending 节奏）还有空间
- **技术借鉴**: `renderGovernor`（任何 Cesium/Three 项目）+ `voiceCost`（任何按 token 计费 LLM API）+ Server-Brokered API Keys（个人项目接多个付费 SaaS）三个**顶级可迁移模式**，可直接拆出独立 library
- **生态位**: 在"浏览器里的照片级 OSINT 仪表盘"这一空白定位上独家；如果做"3D 仪表盘 + Voice 控制的非 OSINT 行业版"（智慧城市运维、应急指挥、港口调度），存在垂直复用空间
- **趋势判断**: 仍在增长（2 个月到 13K stars，GitHub Trending 头名），且 OSINT 行业热度还在上升；半年内看不到后发竞品能挑战"美学派"定位

## 风险与不足

- **onboarding 摩擦**：Node 24 强制 + Google Maps API key 必经 + 多层复杂状态机让"第一次跑起来"门槛高。Issue #74 / #76 / #86 大量"装不上"工单
- **单人 100% commit**：贡献集中度 100%，任何 PR review burden 都压到 Bilawal 一人；风险在 sustainability
- **commits 历史反常**：5 个 commit / 16 万行代码 / 391 文件——README 改了 5/5 次，源码主干几乎无 commit。`src/data` 高居 205 次修改但代码层 commit 仅 5 次，强烈暗示大量历史变更被 squash/重置——典型的"private repo 转 public"做的一次性历史整理
- **Voice 工具面给 LLM 的 instructions 多页长**：微调成本不低；用户修改 voice 行为要改 server 端持久文本
- **.github/workflows/ 未在仓库内**：CI 状态不可见；README 没有 build/coverage 徽章
- **商业版未来不确定**：halfpixel.ai 付费"历史时间回溯"会把哪些能力逐步迁移到付费版，是个问号
- **欧盟合规摩擦**：Google 3D Tiles 区域封锁是已知 onboarding 痛点（issue #71）

## 行动建议

- **如果你要用它**：
  - 先确认能跑通 Node 24 + Google Maps API key（这是唯一必需付费 key）；其他层缺 key 也能跑内建仿真
  - 用 `npm install && npm run dev` 起本地 dev server（默认绑 `localhost`，API key 不上云）
  - 想做 OSINT 调查 / 教学演示 / 媒体内容生产 / 安全研究的非工程师 / Hackathon 玩家；不适合需要团队协作、长期任务、跨工具集成的工作流（那个走 Shadowbroker）

- **如果你要学它**：
  - 重点关注 `src/renderGovernor.js`（十几行纯函数，但解决 Cesium idle 渲染行业难题）
  - 重点关注 `src/voice/voiceCost.js`（残差归类 + unknown model worst-case rates，是任何按 token 计费 LLM API 的范式）
  - 重点关注 `vite.config.js` 的配额治理（OpenSky 自适应 TTL + TomTom daily budget + Overpass 多 mirror 降级）
  - 重点关注 `data/manager.js` 的 `layerFeedState(stats)` 6 类归一（任何多源产品的诚实 UI 范式）
  - 重点关注 `scenes/director.js` 的 `_loadGeneration` + `AbortController` + `claimCameraOwnership` 三层鲁棒性
  - 重点关注 `hybridAnnotationRenderer.js` 的 world-space + screen-space 双层渲染

- **如果你要 fork 它**：
  - 切入点 1：扩展 CCTV 城市包（CONTRIBUTING.md 明确 Austin 是参考，加新城市是"clean public camera catalog with coordinates"）
  - 切入点 2：加新数据层（每个层一个 module，模板 `init/enable/disable/update/destroy/getStats`）
  - 切入点 3：扩展 voice 工具（28 个工具/4 类工作）
  - 切入点 4：加 GLSL 视觉风格（着色器模板已定，mix(orig, filtered, intensity)）
  - 切入点 5：修 first-run bug（issue #85 weather radar 等是高优 roadmap 需求）
  - **谨慎**：不要尝试把它拆成 React/Vue 重构——它的「vanilla JS + 可审计」是**核心产品哲学**

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [已收录](https://deepwiki.com/bilawalsidhu/gods-eye-view) — 2026-08-24 索引（commit 880a672b），13 个主章节：核心架构 / 8 类数据层 / 检测叠加 / 视觉着色器 / 语音 & AI / 注释系统 / Cinematic Director / 地理空间数学 / 测试 / 开发工具 |
| Zread.ai | 未收录 |
| 关联论文 | 无（基于 Cesium/ADS-B/AIS/TLE/USGS 等成熟协议，工程型而非研究型项目） |
| 在线 Demo | 无官方 hosted demo；YouTube 频道 5M+ 播放的 [God's Eye View 系列视频](https://www.youtube.com/watch?v=GRJaKcXZS94)，开源版本需要本地 `npm install` |
| 第三方深度分析 | [Wait, We Got Open Source Palantir Before GTA VI? (DEV)](https://dev.to/chizee/wait-we-got-open-source-palantir-before-gta-vi-1e2o) — 拆解 world-stable icons、dead reckoning、SGP4 卫星传播、quota-governed proxies、$5 语音 cap |
| Cesium 社区 fork | [Smart Work Zones with AADT Exposure](https://community.cesium.com/t/gods-eye-view-release-and-smart-work-zones-with-aadt-exposure/47060/1) — 第三方 fork 接入 TxDOT/Oklahoma DOT WZDx AADT 数据，证明可扩展性 |

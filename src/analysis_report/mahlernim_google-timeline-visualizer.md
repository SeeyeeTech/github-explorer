# GitHub推荐：Google Timeline 离线出 MP4：独立开发者 30 天造出 2.5K star 的隐私优先视频工具

> GitHub: https://github.com/mahlernim/google-timeline-visualizer

## 一句话总结

把 Google Maps Timeline 导出的 JSON 在本地端渲染成可分享的 MP4 旅行视频，**JSON 从不上传、零账户、零订阅**，Android APK + iPhone Safari Web App + Python CLI **三端共享同一套决定性渲染管线**。

## 值得关注的理由

1. **「8 个月年龄 = 1 个月项目」的反常节奏**：105/106 commit 集中在最近 30 天，单月 45 个 tag，单日发版是常态 — 是观察「个人开发者如何把上架做成工程纪律」的活样本。
2. **三套独立实现 + 测试驱动一致性的跨端架构**：Kotlin / TypeScript / Python 三端各自独立强类型实现，靠 `test-fixtures/` 五份真实格式样本 + 50+ 测试保证端到端像素一致 — **比 WASM/Rust 共享更轻量、比完全独立更可靠**，是少见的多端渲染范式。
3. **把视频摄影思维搬进数据可视化**：相机 dead-zone + 非对称 zoom smoothing + ±0.15 zoom hysteresis、H.264 Annex A macroblock → level 反查、polor branch correction 修跨极地航线 — 这些都是从电影摄影、编码工程、遥测领域「跨界」移植的细节，**是判断「作者懂产品」而非「玩具型 vibe-coded 工具」的硬证据**。

## 项目展示

![Videos library](https://raw.githubusercontent.com/mahlernim/google-timeline-visualizer/main/play-store/assets/screenshots/en-US/01-videos.png)

> 视频库主界面：导入过的 Timeline 与生成的 MP4 都被索引到本地，可作为「旅行日记」回看。

![Selected period](https://raw.githubusercontent.com/mahlernim/google-timeline-visualizer/main/play-store/assets/screenshots/en-US/03-selected-period.png)

> 时间段选择 + 相机模式预览：选定起止日期后能即时预览镜头走向，确认后再正式导出。

> 说明：仓库**没有**架构图、没有 demo GIF、没有成片示例，README 只引用了上述 2 张截图。`travel_history_sample.gif` 虽在仓库根目录（16MB），但未被 README 引用 — 「灵魂素材」的缺失是这个以视频为核心产品的项目最明显的文档短板。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/mahlernim/google-timeline-visualizer |
| Star / Fork | 2,564 / 301 |
| Watcher | 165 |
| License | MIT |
| 代码行数 | 25,967（Kotlin 51% / TypeScript 25% / XML 14% / Python 4% / 其它 6%） |
| 文件数量 | 269 |
| 项目年龄 | 8.2 个月（首次提交 2025-12-16；真实开发集中在最近 30 天） |
| 最新版本 | v2.3.2（44 个 release tag，平均约 5.4 天一版） |
| 开发阶段 | 密集开发 |
| 开发模式 | 职业化个人项目（周末 17.9%、深夜 27.4%） |
| 贡献模式 | 单人主导（mahlernim + mahler83 合计 92%，其余 6 人各 2-7 commit） |
| 热度定位 | 小众精品的天花板（垂直隐私工具类 2.5k star 已是头部） |
| 质量评级 | 代码 优秀 · 文档 优秀 · 测试 充分 · CI/CD 完善 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

- **账号**：mahlernim（display name 留空），2017-10 注册至今 8.8 年，South Korea，公开仓库 35 个 — **此项目是其代表作**（其它仓库 star 数均远低于此）。
- **公司字段**：空，独立开发者。
- **博客**：blog.mahler83.net 已 301 到 `largelearningmodel.wordpress.com`（「Large Learning Model」命名暗示 ML / 数据 / 可视化背景）。
- **开发者署名**：`docs/privacy.md` 自报「Developer: MahlerLab」，联系邮箱 `mahlerlabdiy@gmail.com`。
- **iPhone 入口域名**：自建 `ahn-lab.org` 域名承接 Web App 流量，是产品侧的运营投入证据。

「MahlerLab + Large Learning Model + ML/数据背景 + 8 年持续开源」拼在一起，作者是一个**资深独立开发者**：项目不是「业余时间练手 vibe-coded 玩具」，而是经过 8 个月酝酿后启动工程化迭代的旗舰作品。

### 问题判断

Google Maps Timeline 官方查看器只有**静态地图叠加**：用户想看「我这三年到底去了哪些地方、每年有什么长途旅行、能不能剪成可分享的视频」，Google 不会做这件事。问题窗口在 2025-2026 收紧 — Google 持续把 Timeline 导出入口埋深、把关闭后的恢复路径复杂化（`docs/restore-google-maps-timeline.md` 单独成文说明），让「脱机备份 + 二次加工」这件事越来越痛。

作者的判断很清晰：**官方不会做、闭源 SaaS 不敢信（必须上传 JSON）、通用 GIS 工具学习曲线太陡** — 中间是一片「一次性本地化离线渲染」的真空白。

### 解法哲学

1. **极端本地优先 = 产品主张**：零账户、零云端、零分析，唯一网络出口是 CARTO 瓦片（首次加载 Timeline 前强制勾选知情同意）。
2. **三端覆盖但拒绝代码共享**：Android APK + iPhone Web App + Python CLI，用「测试驱动一致性」替代 wasm/Rust-to-wasm — 换来部署零摩擦，代价是 bug 要改三处。
3. **摄影感 > 工程感**：相机 dead-zone、非对称 zoom smoothing、H.264 macroblock 反查 — 这些「把电影摄影/编码工程经验搬进数据可视化」的选择，比技术栈选择更能体现作者的世界观。
4. **明确不做的**：不做云端、不做协同、不做订阅、不做品牌植入（`docs/brand.md` 明确禁止 Google 色 + Google Maps pin + Google wordmark）、不在 Web 端 cache 用户 Timeline（注释明写原因）。
5. **发版即工程纪律**：44 个 tag、几乎每天一版、CHANGELOG.md 改 34 次 — 是「把 Play Store 上架当作一等公民」而非「写完代码顺手提交」的项目。

### 战略意图

- **MIT License** + **无 SaaS / Pro / Enterprise 字样** + **无付费墙** = 暂无商业化意图。
- **APK 走 GitHub Release 直发**（README 明确「Do not download the `.sha256` checksum file」），**故意绕开 Google Play 审核/抽成/账号绑定**，把「零账号体系」做成产品叙事本身。
- **iPhone Web App 部署在作者自有域名 ahn-lab.org** 作为吸引 iOS 用户的关键入口，构成轻量运营护城河。
- 这是**旗舰个人作品**，是个人品牌的代表作 — 不是基础设施。

## 核心价值提炼

### 创新之处（按新颖度 × 实用性排序）

1. **跨平台决定性渲染管线（Kotlin ↔ TypeScript ↔ Python 三独立实现 + 测试驱动一致）** — 新颖 3/5，实用 5/5
2. **相机 dead-zone + 非对称 smoothing + ±0.15 zoom hysteresis 三件套** — 新颖 3/5，实用 5/5
3. **预计算 480 采样相机轨道统一 preview / export** — 新颖 4/5，实用 5/5
4. **H.264 Annex A macroblock → level 反查（avc1.42001f / 420020 / 420028 / 42002a）+ 浏览器能力先探针后启用** — 新颖 4/5，实用 5/5
5. **极地路径分支校正（lat≥70 corridor + greatCircleReferenceX）** — 新颖 4/5，实用 4/5
6. **AtomicFile + 自定义二进制 cache + 三段 fingerprint（URI/size/mtime）+ PARSER_VERSION 防 stale** — 新颖 3/5，实用 5/5
7. **5 字段 preset link（aspect / zoom style / long-trip detection / local trip framing / pacing）+ 强制用户确认后再用** — 新颖 3/5，实用 5/5
8. **WebCodecs / mediabunny 失败处理必须 `output.cancel()` 释放 encoder** — 新颖 3/5，实用 5/5

### 可复用的模式与技巧

1. **「三端同源 + 测试驱动一致性」模式**：跨 iOS / Android / Web / CLI 的同质化渲染/计算 pipeline，且不想引入 wasm — 用「一致的固定 fixture + 共享参数常量（1300 kmh、500 km、120 km、480 samples）」保证行为一致。`test-fixtures/` 5 种真实格式样本是关键基础设施。
2. **「Foreground Service + START_REDELIVER_INTENT + persistent request store」模式**：`VideoExportService` + `VideoExportRequestStore` 保证 Android 杀进程后可恢复 — 几乎所有「长任务离线导出/上传」场景都需要。
3. **「知情同意前置 + 缓存」模式**：瓦片是唯一网络出口；首次加载 Timeline 前必须勾选；瓦片用 zoom/x/y 去重缓存。几乎所有「数据本地、瓦片/字体/静态资源走 CDN」的可视化项目都应套用。
4. **「决定性 preview/export pipeline」模式**：导出前一次性冻结 overlay text + 相机轨道 + JourneyTiming，让 preview 与 export 像素一致 — 凡是「先生成预览，再离线渲染」都适用。
5. **「5 字段 preset link + 强制用户确认」模式**：分享粒度只到配置不到数据；UI 必须先展示 5 个值让用户决定是否采纳 — 任何「用户间分享配置」都适用。
6. **「l10n 拆出 catalog/formatting/tag」三元组**：`i18n.ts` 把 message catalog、Intl format tag、locale-aware label 解耦 — 9 语种级别的多语言 UI。
7. **「品牌规则文档化」模式**（`docs/brand.md`）：色板、商标用法、字号、所有变化点都文档化 — 任何 wrap 第三方平台的开源项目都应做类似 brand guide。

### 关键设计决策

1. **跨平台三独立实现 + 不做代码共享**：避免 wasm/JS bundle 兼容层 → 部署零摩擦。代价是 bug 要改 3 处。
2. **480 采样相机轨道一次性预计算**：preview 与 export 像素完全一致。代价是长 timeline 上 dynamic camera 的 leg-aware 计算要扫一遍。
3. **首次加载 Timeline 前弹一次性 CARTO 瓦片告知**：唯一网络出口必须显式同意。代价是用户多一步勾选。
4. **Foreground Service + 4 类通知通道 + ETA 用近期帧吞吐量估算**：切走 app / 关屏导出不能断。代价是通知配置复杂。
5. **WebCodecs `output.cancel()` 强制释放 encoder**：避免下一轮重试泄漏。代价是必须 try/finally。
6. **极地路径分支校正**：跨极地航线不会画出凭空一圈。代价是算法复杂、注释极详。
7. **video export pipeline「先 prepare 全部 tiles，再 encode」两阶段**：视频中不会出现地图黑洞。代价是拉瓦片阶段不能给用户看进度画面。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | 本项目 | Dawarich | Location History Visualizer Pro | GPXSee | Kepler.gl |
|------|--------|----------|------------------------------|--------|-----------|
| 定位 | 一次性本地渲染 → MP4 | 自托管 Timeline 替代品 | 商业 SaaS | 桌面 GPX 可视化 | Uber 开源地理可视化 |
| Stars | 2.5k+ | ~4k+ | 闭源 | ~3k+ | ~10k+ |
| 账户体系 | 无 | 自建服务 | 强制注册 | 无 | 无 |
| 数据上传 | **永不上传 JSON** | 自托管可控 | 必须上传 | 本地 | 本地 |
| 输出 | **MP4 视频** | 静态地图 / 统计 | 网页报告 | 静态地图 | 交互式地图 |
| 学习曲线 | 零 | 中（Docker） | 低 | 中（GIS 知识） | 中-高 |
| 跨平台 | Android / iPhone Web / CLI | 自托管 Web | Web only | 桌面（多 OS） | Web only |
| 价格 | 免费 | 免费 / €60-150/年 | 订阅 | 免费 | 免费 |
| 商业模式 | 无 | 开源 + Cloud | SaaS | 无 | 无 |

### 差异化护城河

**「隐私 + 离线 + 跨平台 + MP4 导出」**这 4 项**没有任何竞品同时具备**；特别是「无账户 + 出视频」的组合形成了清晰的产品护城河。

- vs **Dawarich**：本项目是「轻量前端可视化」，Dawarich 是「重量后端持续追踪」— 完全互补而非替代。
- vs **Location History Visualizer Pro**：商业 SaaS 与隐私优先工具的根本立场冲突。
- vs **GPXSee / Kepler.gl / QGIS**：通用数据分析师工具，学习曲线 + 不出视频 + 不能直接吃 Timeline JSON。

### 竞争风险

1. **Dawarich 若推出「导出视频」功能**会直接侵蚀主要价值 — 但二者目标场景重叠度不高（年终回顾 vs 持续追踪）。
2. **Google 官方 Timeline 站点若支持视频导出** — 这是「平台官方下场」的根本性风险，但作者已经把跨端架构 + 隐私品牌 + 离线渲染做成护城河。
3. **play store 上架时间窗** — 延迟上架可能错过算法红利期。

### 生态定位

在「个人位置数据」工具生态中，本项目是**消费侧**（可视化输出），Dawarich / OwnTracks / Overland 是**采集侧**（数据收集）。**两者不冲突、反而互补** — 这是为什么 Dawarich 官方博客把它定位为「Google Timeline 入口的可视化伴侣」。

## 套利机会分析

- **信息差**：被 Dawarich 等项目反向引用为「Google Timeline 入口的可视化伴侣」— 大部分中文社区还没意识到这类工具的存在；Dawarich 官方博客的「Best Google Timeline Alternatives in 2026 (Ranked)」明确点名了本项目，但中文渠道几乎无报道。
- **技术借鉴**：相机 dead-zone + 极地路径分支校正 + 跨平台测试驱动一致性 + 决定性 preview/export pipeline 这 4 个模式对**任何做地理/轨迹可视化的项目都直接可用**。
- **生态位**：填补了「一次性本地化离线渲染 + 出视频」的真空白，与官方 Timeline 站点形成正面产品形态差异。
- **趋势判断**：star 增长在爆发期（8 月单月 105 commit + 2.5k+ star），Google 持续收紧 Timeline 导出入口的趋势会让本项目获得长尾需求；Dawarich 等生态项目反向引用会持续带来 SEO/推荐流量。

## 风险与不足

1. **大文件 OOM（Issue #44 / #64）**：25 评论的「导入大 Chronology.json 崩溃」是当前最大的工程债，作者通过 v2.1.1 减内存、v2.1.2 primitive arrays + 虚拟插值、v2.1.3 相机轨道后台预计算三个版本系统化解决，但同类问题反复出现，**说明大文件 IO/内存管理仍是当前风险源**。
2. **Bus factor = 1**：mahlernim + mahler83 合计 92%，主作者 66% — 离开主作者项目可能停滞。
3. **文档缺成片示例**：作为以视频为核心产品的项目，README 没有 demo GIF、没有成片示例 — `travel_history_sample.gif` 在仓库根目录 16MB 都没被引用。
4. **跨端 bug fix 成本高**：3 套独立实现 + 不做代码共享意味着每改一处 bug 要同步 3 处。
5. **商业化路径不明**：MIT + 无 SaaS + APK 走 GitHub Release 直发（绕过 Google Play 抽成）— 独立开发者长期投入需要持续动力来源。
6. **Play Store 审核风险**：品牌规则文档化已规避大部分商标问题，但「无障碍 / 数据安全 / 隐私政策」红线仍是上架风险源（`submission-checklist.md` 改 27 次的副作用）。
7. **Issue #66「Safe Sharing Mode」仍未关闭**：路线图显示下一步要从「个人私密使用」扩张到「可公开分享」，但关键功能未落地。

## 行动建议

### 如果你要用它

- **核心场景**：想分享自己的年度/季度旅行轨迹给家人朋友，且对「把位置历史交给第三方 SaaS」有顾虑。
- **首选 iPhone Web App**：零安装、零账户、零上传，能跑就用；Safari 16.4+ 必须。
- **首选 Android 隐私用户**：从 GitHub Release 直接下载 APK（注意是 `.apk` 不是 `.sha256`），允许「安装未知应用」。
- **CI / 自动化批量出视频**：用 Python CLI（`visualizer.py` 765 行单文件）。
- **不推荐**：Dawarich 用户本来就在自托管位置数据，再用本项目更合适；纯 GIS 分析师请直接上 QGIS / Kepler.gl。

### 如果你要学它

**重点关注以下文件 / 模块**（按可迁移性排序）：

| 优先级 | 文件 | 学习点 |
|--------|------|--------|
| ⭐⭐⭐ | `web/src/camera.ts`（459 行）+ `app/src/main/java/.../render/CameraTrack.kt` | 相机 dead-zone + 非对称 smoothing + zoom hysteresis |
| ⭐⭐⭐ | `app/src/main/java/.../data/TimelineCache.kt` + `web/src/timeline.ts` | AtomicFile + fingerprint + PARSER_VERSION 三件套 |
| ⭐⭐⭐ | `app/src/main/java/.../export/VideoExportService.kt` | Foreground Service + START_REDELIVER_INTENT + ETA 估算 |
| ⭐⭐ | `web/src/video.ts`（232 行）+ `app/src/main/java/.../export/Mp4Exporter.kt` | H.264 macroblock → level 反查 + 能力探针 |
| ⭐⭐ | `web/src/geo.ts` `unwrapJourneyPoints` | 极地路径分支校正 |
| ⭐⭐ | `app/src/main/java/.../data/LocationOutlierFilter.kt` + `web/src/outlier.ts` | 跨语言一致的 GPS 异常值识别 |
| ⭐ | `app/src/main/java/.../render/JourneyTiming.kt` | monotone cubic spline for long-trip compression |
| ⭐ | `app/src/main/java/.../presets/PresetCodec.kt` + `web/src/preset-link.ts` | 5 字段 preset link + 强制确认 |
| ⭐ | `docs/brand.md` + `docs/privacy.md` | 品牌规则 + 隐私设计文档化的范本 |

**核心学习主题**：

- 跨端架构的「测试驱动一致性」模式（Kotlin / TS / Python 三独立实现 + test-fixtures 验证）。
- 摄影感 + 编码工程经验跨界迁移到数据可视化。
- 「严格本地优先」的产品主张如何在代码层落地（MediaStore 不复制 JSON、AtomicFile 私有缓存、唯一网络出口首次同意、cache 排除 Android backup）。
- 上架型开源项目的工程纪律（Play Store 素材自动化校验 + 三语 README + 三语 strings + 三语 privacy）。

### 如果你要 fork 它

**可以改进的方向**（按优先级）：

1. **实现 Issue #66 Safe Sharing Mode** — 分享视频时自动模糊家/办公室等敏感 POI，把产品边界从「个人私密使用」扩张到「可公开分享」，是流量增长的下一跳。
2. **添加 demo GIF / 成片示例到 README** — 这是文档层面最明显的短板。
3. **把「跨端测试驱动一致性」抽成可复用模板** — 现有 `test-fixtures/` 5 种真实格式样本 + 50+ 测试已经是范式资产，提取出来可服务其他多端项目。
4. **优化大文件 OOM 的最后 10%** — Issue #44 25 评论说明还没彻底解决，可以考虑 Streaming JSON Parser + Out-of-Core 异常值过滤。
5. **添加 TypeScript SDK 给第三方嵌入** — 现有 web/src/ 已经是模块化的核心管线，包装成 SDK 可让第三方网站嵌入「Timeline Visualizer 按钮」。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/mahlernim/google-timeline-visualizer（已收录） |
| Zread.ai | 未收录 |
| 关联论文 | 无（这是工程型产品，非研究项目） |
| 在线 Demo | https://ahn-lab.org/google-timeline-visualizer/（iPhone Web App 本身即 Demo，需自备 Timeline JSON） |
| 作者博客 | https://largelearningmodel.wordpress.com（blog.mahler83.net 301 重定向至此） |
| 开发者署名 | MahlerLab（`docs/privacy.md` 自报） · 邮箱 mahlerlabdiy@gmail.com |
| 关键 Issue | [#44 大文件崩溃（已关闭）](https://github.com/mahlernim/google-timeline-visualizer/issues/44) · [#66 Safe Sharing Mode（仍 open）](https://github.com/mahlernim/google-timeline-visualizer/issues/66) · [#129 镜头预设（已关闭）](https://github.com/mahlernim/google-timeline-visualizer/issues/129) |
| 第三方深度评测 | [Dawarich: Best Google Timeline Alternatives in 2026 (Ranked)](https://dawarich.app/blog/best-google-timeline-alternatives-in-2026-ranked) · [explainx.ai: Google Timeline Visualizer App Guide 2026](https://explainx.ai/blog/google-timeline-visualizer-travel-video-app-guide-2026) |

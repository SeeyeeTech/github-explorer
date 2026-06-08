# 李笑来《人人都能用英语》做成的 App：本地 AI 词级跟读，却已停更转 web

> GitHub: https://github.com/ZuodaoTech/everyone-can-use-english

## 一句话总结

这是一个混装「书 + App + 方法论站」的 monorepo：`book/`（李笑来《人人都能用英语》原书）+ **`enjoy/`（Enjoy App，真代码——Electron 桌面英语学习应用）** + `1000-hours/`（「投入一千小时」方法论站 1000h.org）。Enjoy 把 Krashen「可理解输入」+ shadowing（影子跟读）方法论工程化：导入任意真实音视频 → **本地 whisper 转录 + 词级强制对齐** → 句/意群/词/音素的嵌套区域钻取跟读 + 音高曲线对照 → Azure 音素级发音评测 → 本地 SQLite 存储。34.4K star、GPL-3.0、做到科技（ZuodaoTech，李笑来创立）出品、主程 An Lee（51% 提交）。**但需如实告知：本仓已停滞**——2024 年井喷后 2025 全年降速、近 90 天 0 commit、最后实质提交 2025-11；且**产品已 pivot** 到闭源 enjoy.bot web 版 + Chrome 插件 Enjoy Echo + iOS，README 明示新桌面端将退化为「web 套壳」。本仓 Electron 桌面代码已是历史遗产 + 引流入口。

## 值得关注的理由

1. **皇冠明珠：on-device whisper + 词级强制对齐驱动的跟读交互**：`enjoy/src/main/echogarden.ts` 用一个本地库 echogarden 统一收口 STT 转录 + TTS 合成 + **forced alignment 强制对齐**（把转录文本与音频精确对齐出词级/音素级时间戳）——这是「跟读时逐词高亮 + 录音逐词对比」的技术基础。STT 引擎可切（LOCAL whisper.cpp / Azure / Cloudflare / OpenAI，本地模型 tiny→large-v3-turbo，模型走 hf-mirror 镜像对国内友好）。**关键事实**：仓库里 ~11K 行 `.metal` 文件不是波形渲染，而是 vendored whisper.cpp 的 `ggml-metal.metal` GPU 核——**本地 STT 在 Apple Silicon 上的 GPU 加速**，这强化了「离线、隐私、本地优先」的护城河。「STT + forced alignment 产出词级时间线 → 驱动逐词高亮」是一切卡拉 OK 式逐字高亮/配音/语言学习产品的通用骨架。
2. **几个 local-first 桌面应用的范式设计**：① **主进程 SQLite + AfterHook 反应式变更流**——`enjoy/src/main/db` 用 sequelize-typescript 建本地 SQLite 作单一事实源，模型 `@AfterCreate/Update/Destroy` 经 `webContents.send("db-on-transaction")` 把 DB 变更广播给 React，自建一套 SQLite→UI 反应式数据层；② **内容寻址录音去重管线**——录音裁静音→WAV→**md5 哈希查重复用**→ffmpeg 压缩→`uuidv5(userId/md5)` 确定性主键，天然幂等；③ **polymorphic 关联**（Recording/Transcription/PronunciationAssessment 用 `targetId+targetType` 多态挂接 Audio/Video/ChatMessage）；④ **Electron 双进程 + enjoy:// 协议**（重活全压主进程，contextBridge 窄接口，自定义协议在双进程间传文件引用而非数据）。
3. **嵌套区域钻取的跟读交互范式**：`enjoy/src/renderer/context/media-shadow-provider.tsx`（~780 行，全 App 最核心状态机）以词级 timeline 为骨架，在 wavesurfer.js 上构造**三级嵌套区域**（segment 句 → meaning-group 意群 → word 词，词级再下钻到 phone 音素），叠加 Chart.js 音高曲线做发音对照。「词级时间线 → 可钻取嵌套区域 → 音高/音素叠加对照」是语言学习/正音类产品的高价值交互范式。

## 项目展示

![Enjoy 视频跟读](https://raw.githubusercontent.com/ZuodaoTech/everyone-can-use-english/main/enjoy/snapshots/screenshot-video.png)

> Enjoy App 核心功能：视频跟读（导入真实音视频 → 转录对齐 → 逐词高亮跟读 → 录音对比 + 发音评测）。新版产品已转 web（enjoy.bot）+ Chrome 插件（Enjoy Echo，YouTube/Netflix 字幕精读）+ iOS。方法论站 1000h.org。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/ZuodaoTech/everyone-can-use-english（homepage 1000h.org，产品入口 enjoy.bot） |
| Star / Fork | 34,362 / 4,797（star 含李笑来个人 IP + 原书读者带量 + 2024 社媒安利遗产） |
| 代码规模 | 真实 App = **enjoy/ 58,395 行 TS/TSX**（+ vendored whisper.cpp Metal GPU 核）；tokei 12.3 万行含 SVG 图标 42.2% + book markdown 虚高；注释比 0.1 |
| 项目年龄 | 86.9 个月（2019-03 起，含早期 book 内容；App 密集开发实为 2024 年）；最后提交 2026-02-03 |
| 开发阶段 | **低维护 · 已停滞**（2024 井喷[月 commit 200+]→2025 全年降速→近 90 天 0 commit；fix 30.5%>feature 9.5%） |
| 贡献模式 | 核心少数（77 贡献者，**an-lee 51%/主程 + xiaolai/李笑来 + Lyric**，做到科技维护） |
| 热度定位 | 明星英语学习项目（存量声誉高，增量开发已停） |
| 版本 | v0.7.9（49 tag/48 release，未及 1.0 即进入维护尾声） |
| License | GPL-3.0 |
| 质量评级 | CI「B+（四平台构建）」· 代码「B」· 文档「C+」· 测试「D+（仅 2 个 e2e，无单测）」 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

「内容 IP 主理人 + 职业主程」结构：**李笑来（xiaolai，452 commit/第二贡献者）**——中国最具影响力的自我成长/学习类作者之一（新东方名师出身，著《人人都能用英语》《把时间当作朋友》，中国最早的比特币布道者/早期投资人之一，亦是币圈争议人物），创立做到科技（ZuodaoTech）。他贡献的是「书的内容 IP + 方法论 + 号召力」。**An Lee（an-lee，741 commit/50.9%）**——Enjoy App 实际主程，独扛一半以上代码，Electron/音视频/AI 集成核心负责人。客观判断：34K star 中相当比例是李笑来个人 IP 与原书读者带量，需与 App 工程含金量分开看。

### 问题判断

传统英语学习（背单词/学语法/刷题）在「输出」上投入过重，却在 Krashen「可理解输入」上严重欠缺工具支撑——学习者拿到一段真实英文音视频，缺少把它拆成「逐词对齐 + 跟读 + 发音打分 + 查词建卡」闭环练习的环境。现有方案不够：浏览器字幕工具（Language Reactor）只能在网页内精读、无法导入本地素材、不做录音对比与评测；订阅平台（LingQ/Duolingo）素材封闭、数据云端、跟读颗粒度粗。

### 解法哲学（可理解输入 + 跟读工具化 + local-first）

核心命题来自李笑来长期主张：英语不是「学」会的而是「用」会的；语音塑造、朗读、精读是可训练的工程问题。三条哲学：① **可理解输入工具化**——任意真实素材 → AI 转录 → 词级强制对齐 → 逐词高亮 + 区域钻取 + 音高对照，把抽象理论变成可操作 UI；② **local-first 优先 + 隐私**——学习数据全存本地 SQLite，STT 默认可走本地 whisper.cpp（含 Metal GPU 加速），离线即能转录跟读；③ **重活全在主进程**——语音/媒体/词典/DB 重型 Node 能力集中在 src/main，renderer 只做 UI。

### 战略意图（书→工具→方法论 + pivot）

monorepo 同仓承载「内容 IP（书）→ 方法论站（1000h.org）→ 工具（Enjoy）」三位一体，书的章节（语音/朗读/精读/词典）几乎一一映射成 App 功能模块。但 README 已明确公告产品重心迁移：**网页版 enjoy.bot 上线、Chrome 插件 Enjoy Echo 上架、iOS（Echo-iOS）**，新桌面端将退化为「web 套壳」。即从「重型本地 Electron 桌面」pivot 到「闭源 web + 浏览器插件 + iOS」——放弃本仓最硬的差异化（本地 whisper + 离线 SQLite + 原生媒体管线），换取跨端覆盖、零安装门槛、闭源可商业化；代价是本开源 Electron 代码停止演进。

## 核心价值提炼

### 创新之处

1. **词级强制对齐驱动的嵌套区域钻取（句→意群→词→音素）**（新颖度 4/5，实用性 5/5，可迁移性 4/5）：以 echogarden forced alignment 的 word timeline 为骨架，在 wavesurfer 上构造三级可钻取练习区域，词级再下钻音素并叠加音高曲线。适用语言学习、正音、配音逐字对齐。
2. **on-device whisper.cpp + Metal GPU 的本地 STT**（新颖度 3/5，实用性 4/5）：vendored whisper.cpp（含 ggml-metal.metal）做离线转录，引擎可在本地/Azure/Cloudflare/OpenAI 间切换。适用隐私敏感、离线优先的语音应用。
3. **SQLite AfterHook → 渲染进程反应式变更流**（新颖度 3/5，实用性 5/5，可迁移性 5/5）：模型钩子经 `webContents.send` 把 DB 变更广播给 React，自建 local-first 反应式数据层。适用任何 Electron/Tauri local-first 桌面应用。
4. **内容寻址的录音去重管线**（新颖度 3/5，实用性 4/5，可迁移性 5/5）：裁静音→WAV→md5 去重→ffmpeg 压缩→`uuidv5` 确定性主键，天然幂等。适用 UGC 媒体落盘、跨端同步去重。
5. **方法论 IP → 方法论站 → 工具 三层 monorepo**（新颖度 4/5，实用性 3/5）：书 markdown + 1000h.org 站 + Enjoy App 同仓，内容/方法论/工具一体化。适用内容创作者把 IP 工具化的组织范式。

### 可复用的模式与技巧

- **统一语音库收口（STT/TTS/Align）**：用 echogarden 这类单库统一转录、合成、强制对齐——任何需要词级时间戳的语音产品。
- **主进程 SQLite + AfterHook 广播**：DB 为单一事实源，模型钩子推变更给 UI——Electron/Tauri local-first 应用的反应式数据层。
- **polymorphic targetId/targetType 关联**：一套录音/评测/笔记表挂接多种素材类型——多态附属数据建模通用解。
- **内容寻址 md5 去重 + uuidv5 确定性主键**：哈希查重复用 + 可预测 ID——媒体落盘与同步幂等。
- **contextBridge 窄接口 + 自定义协议传引用**：`enjoy://` 在双进程间传文件引用而非数据——Electron 大文件 IPC 范式。
- **嵌套 Region + 时间线驱动高亮**：词级 timeline → 可钻取区域 → 音高/音素叠加——媒体精读/逐字交互范式。

### 关键设计决策

最值得记录的是 **echogarden 统一语音管线 + 词级强制对齐——把「可理解输入 + 跟读」从理论变成可操作 UI 的技术命门**。决策：把转录、合成、强制对齐三件事统一收口到一个本地库 echogarden（`enjoy/src/main/echogarden.ts`），而非各接一个云 API。问题：跟读时要「逐词高亮 + 录音逐词对比」，必须有词级（甚至音素级）时间戳——纯 STT（whisper）只给句级时间戳且不稳，要的是把「转录文本 ↔ 音频」精确对齐。方案：`recognize()` 做 STT（macOS 指向 vendored whisper.cpp 本地可执行），`align()` 做 forced alignment 输出 word timeline，再聚合成句级；转录结果（含对齐 timeline）以 JSON 存进 `Transcription.result`；STT 引擎可在 LOCAL(whisper.cpp)/Azure/Cloudflare/OpenAI 间切换。这个词级 timeline 正是 `media-shadow-provider.tsx` 构造「句→意群→词→音素」嵌套钻取区域 + 逐词高亮 + 音高对照的骨架。Trade-off 很诚实：本地 whisper 准确率/速度受机器与模型档位制约（默认 tiny.en），故保留云引擎兜底；vendored 原生二进制（ffmpeg/whisper/echogarden）带来安装/编译门槛（Issue #105/#126）。这套「STT + forced alignment → 词级时间线 → 驱动交互」是任何逐字对齐产品的通用骨架。

> 事实更正：仓库里的 `.metal` 文件不是波形渲染，而是 vendored whisper.cpp 的 `ggml-metal.metal` GPU 核（本地 STT 的 Apple Silicon 加速）；波形渲染实际用渲染进程的 wavesurfer.js（Web Audio）。这反而是更强的「on-device 本地语音」故事。

## 竞品格局与定位

| 项目 | 定位 | 与 Enjoy 关系 |
|------|------|------|
| Language Reactor | 浏览器插件，Netflix/YouTube 双语字幕精读 | 只在网页内精读、不导入本地素材、不做录音对比/评测、数据云端；Enjoy 桌面版能导入任意本地/在线源 + 词级对齐 + 音素评测 + 本地存储。**讽刺**：Enjoy 的 pivot 产物 Enjoy Echo 正是直接对标 LR 的浏览器插件 |
| LingQ (Steve Kaufmann) | 可理解输入阅读/听力平台 | 同信奉可理解输入，但素材封闭、订阅制、数据云端、跟读颗粒度粗；Enjoy 差异在 local-first + AI 转录对齐 + 音素级评测 + 自由导入真实素材 |
| Duolingo | 游戏化刷题 | 轻量游戏化、碎片化；Enjoy 走重度自我训练（一千小时）、真实素材、高强度跟读——非同一赛道、理念相反 |
| Anki | 开源 SRS 间隔重复 | 只解决记忆一环；Enjoy 覆盖输入/跟读/发音/建卡全链路 |

### 差异化护城河

本地优先（离线 SQLite + on-device whisper）+ AI 转录词级/音素级对齐 + 李笑来方法论 IP 工具化。这三点是 web/插件竞品短期难复制的组合。

### 竞争风险

- **仓库已停滞**：2024 井喷后 2025 仅 30 commit、2026 仅 2（均 docs），近 90 天 0 commit。
- **产品已 pivot**：迁往闭源 enjoy.bot web/插件/iOS，本 Electron 桌面端被官方定性为「web 套壳」前的遗产。
- **安装门槛高**：ffmpeg/whisper/echogarden 原生二进制编译（#105/#126）。
- **媒体可靠性**：mp4 波形解码失败（#946）。
- **local-first 挂云的状态一致性**：登录/重复扣费（#220/#1096）。
- **IP 依赖**：强绑李笑来个人方法论与流量。

### 生态定位

作为开源代码，它最大价值是**「local-first AI 语音学习桌面应用」的高质量参考实现/教学样本**，而非一个还在迭代的活产品。

## 套利机会分析

- **信息差**：兼具「李笑来 IP + 人人都能用英语」人物故事 + 「本地 whisper 词级对齐做跟读」技术亮点 + 「明星开源 App 停滞/pivot 生命周期」观察样本三重维度。中文圈对「echogarden 语音管线 + forced alignment 词级对齐」「Electron local-first SQLite 反应式数据层」「内容寻址录音去重」「on-device whisper Metal 加速」的工程拆解稀缺；「可理解输入方法论工具化 + 后来为何 pivot 到 web」也有反思价值。
- **技术借鉴**：统一语音库收口、主进程 SQLite+AfterHook 广播、polymorphic 关联、md5 内容寻址去重、contextBridge+自定义协议、嵌套 Region 时间线高亮——可迁移到任何 Electron/Tauri local-first 应用、语音/媒体精读产品、UGC 媒体管线。
- **生态位**：local-first AI 语音学习的参考实现；与 Language Reactor（浏览器字幕）、LingQ（可理解输入云平台）错位。
- **趋势判断**：方法论（可理解输入 + 跟读）长期有效；但本仓作为产品已 pivot 停更——价值在「学架构/方法论」而非「拿来即用的活产品」。

## 风险与不足

- **已停滞 + 已 pivot（头号）**：本 Electron 桌面端不再迭代，最新能力在闭源云端（enjoy.bot/插件/iOS）。想用/二开者拿到的是停更的本地版。
- **测试薄弱**：仅 2 个 Playwright e2e、无单测，语音/DB/对齐核心逻辑无自动化覆盖。
- **巨型组件**：media-shadow-provider(780)/window(859)/preload(808) 偏巨型，胖模型耦合 sync+UI 通知。
- **安装门槛 + 媒体可靠性**：原生依赖编译难、mp4 解码不稳。
- **Star 含水分**：34K 中相当比例是李笑来 IP + 原书读者带量，近期涨星是老 IP 惯性而非活跃信号。

## 行动建议

- **如果你要用它**：想要 local-first、离线、能导入任意真实素材做词级跟读 + 发音评测的英语学习者可用旧桌面版（但已停更）；要最新能力请用闭源 enjoy.bot web 版 / Chrome 插件 Enjoy Echo / iOS。**不适合**作为「活跃可依赖」的生产工具或长期二开底座。
- **如果你要学它**：直奔 `enjoy/src/main/echogarden.ts`（统一语音管线 + forced alignment）+ `enjoy/src/main/db/`（local-first SQLite 多态模型 + 内容寻址去重 + AfterHook 反应式流）+ `enjoy/src/renderer/context/media-shadow-provider.tsx`（嵌套区域钻取跟读核心状态机）+ `enjoy/src/preload.ts`（contextBridge IPC）+ `enjoy/src/main/azure-speech-sdk.ts`（音素级评测）。这是「Electron + 本地 AI 语音/媒体处理 + local-first」的高质量教学样本。
- **如果你要 fork / 借鉴它**：统一语音库收口、主进程 SQLite+AfterHook 广播、md5 内容寻址去重、嵌套 Region 时间线高亮是可直接迁移的设计。GPL-3.0（强 copyleft）；但注意本仓已停更，跟读交互/语音管线思路可借鉴，不宜直接当活底座。

### 知识入口

| 资源 | 链接 |
|------|------|
| 方法论站 | https://1000h.org（「投入一千小时」方法论：训练任务/语音塑造/大脑内部/自我训练 + FAQ） |
| 产品入口（新版 web） | https://enjoy.bot（闭源 web 版）+ Chrome 插件 Enjoy Echo + iOS（Echo-iOS 仓库） |
| DeepWiki | https://deepwiki.com/ZuodaoTech/everyone-can-use-english（monorepo + Enjoy Electron 双进程 + echogarden 管线） |
| 原书 | 仓库 `book/`（《人人都能用英语》全文 markdown）+ 李笑来个人站 lixiaolai.com |
| 社区 | https://discuss.enjoy.bot |

# 26 年的 Audacity 重写：旧引擎不动，只换 Qt 新壳

> GitHub: https://github.com/audacity/audacity

## 一句话总结

Audacity 是始于 1999 年、世界上最流行的免费开源音频编辑器——大众音频剪辑的「事实标准入门工具」；它正在进行一次大型现代化重写（Audacity 4.0），核心策略是「**保留并复用经过 26 年验证的旧音频引擎（au3，wxWidgets），只把 UI 与外壳用 Qt/QML 在 Muse Framework 上重建**」，经一层 `au3wrap` 桥接把新旧两套代码库缝合起来。

## 值得关注的理由

- **大型遗留系统现代化重写的范本**：`au3/`（旧 3.x 引擎，拆成 78 个模块化子库）+ `src/`（新 Qt/QML UI）+ `au3wrap`（桥接层）+ `muse/`（与 MuseScore 4 共享的 Muse Framework）——「新壳包装旧引擎、引擎与 UI 解耦」是任何老项目想现代化都值得学的策略，与 MuseScore 4 同路线。
- **被严重低估影响力的国民级软件**：17k star 远不能反映其真实体量——它是全球下载量最大的免费音频编辑器之一，绝大多数用户是播客作者、教育者、业余音乐人，从不上 GitHub。Audacity 4.0 UI 预览视频 50 万+ 播放。
- **一段值得客观看待的治理故事**：2021 年被 Muse Group 收购带来全职团队与 4.0 重写资源，但也留下遥测/隐私争议的历史包袱（催生 Tenacity 等分叉）——「大厂收购的双刃剑」典型样本。

## 项目展示

![Audacity Logo](https://raw.githubusercontent.com/audacity/audacity/master/images/AudacityLogo.png)

Audacity 4.0 全新 Qt UI 预览见[官方 YouTube](https://youtube.com/@audacity)（50 万+ 播放）。开发者文档 [wiki.audacityteam.org/wiki/For_Developers](https://wiki.audacityteam.org/wiki/For_Developers)。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/audacity/audacity |
| Star / Fork | 17106 / 2560（大众热门；star 严重低估真实用户量——多为非开发者） |
| 代码行数 | 160 万（但 ~44% 是 PO/Qt 翻译文件[译成几十种语言]；真实代码 ~50%：C/C++/Header 47.7% + QML 2.2% + Nyquist/Lisp） |
| 项目年龄 | GitHub 仓库约 135 个月（2015 镜像）；**软件本体始于 1999 年，约 26 年** |
| 开发阶段 | 密集开发（近 52 周 ~2995 commit，4.0 Qt 重写主线高强度推进） |
| 贡献模式 | 首席主导 + 元老 + Muse Group 全职团队 + 大社区（Paul Licameli 8924/~37% + James Crook 1816；242 贡献者） |
| 热度定位 | 大众热门 + 重大技术转型期（3.x wxWidgets → 4.0 Qt/Muse 双代码库） |
| 质量评级 | 代码[良好·成熟工程] 文档[优·wiki+DeepWiki] 测试[有·4.0 引入测试脚手架，老代码较薄] |
| License | GPL-2.0+（README 称整体 GPLv3，多数源文件 GPLv2+；GitHub 标 Other） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

Audacity 始于 1999 年，由 **Dominic Mazzoni & Roger Dannenberg（卡内基梅隆）** 创建。org `audacity`（现由 **Muse Group** 运营，该集团还拥有 MuseScore、Ultimate Guitar、Tonebridge、StaffPad）。技术核心是长期首席开发者 **Paul Licameli（8924 commit）** + 元老 **James Crook**，加上 Muse Group 的全职团队（crsib/vsverchinsky/kryksyh 等，多来自 MuseScore 体系）。这是「26 年老牌社区开源 + 大厂资源注入」的典型治理结构。

### 问题判断

Audacity 的历史短板从来不是功能（它功能齐全），而是 **UI 老旧**——基于 wxWidgets 的界面停留在上个时代，操作有诸多「阻碍与不可预测性」（软件会「拒绝执行」某些操作、入口难找）。Muse Group 接手后判断：**与其修修补补，不如复用自家给 MuseScore 4 做的现代 Qt/QML 框架（Muse Framework）重建 UI**，同时保留 Audacity 久经考验的音频引擎。时机上，Muse Framework 已在 MuseScore 4 验证成熟，正好复用到 Audacity，两个旗舰产品共享框架降低维护成本。

### 解法哲学

- **明确选择「保留引擎、只重建 UI」**：旧 au3（wxWidgets）作为音频引擎拆成 78 个子库保留，新 Qt UI 经 au3wrap 桥接复用它——避免重写引擎的巨大风险。
- **明确选择复用 Muse Framework**：与 MuseScore 4 同一 Qt/QML 框架，两产品共享。
- **明确选择 wxWidgets → Qt**：拥抱现代声明式 UI（QML），代价是引入桥接复杂度（有社区争论为何不像 Ardour 自维护 GTK）。
- **明确选择 3.x 稳定线 + 4.0 重写并行**：3.7.x 持续维护（audacity3 分支），master 推进 4.0。
- **保留开源 + 跨平台 + 插件广**（VST3/VST2/LV2/AU/LADSPA/Nyquist）。

### 战略意图

Audacity 是 Muse Group「音乐创作工具矩阵」的一员，4.0 重写让它与 MuseScore 4 共享框架、统一现代化体验。商业上 Muse Group 通过 audio.com 云（au3cloud）等做生态延伸。但需客观记录：2021 年收购后引入的遥测 + 争议隐私政策曾重创社区信任——这是它现代化路上的治理污点（详见风险）。

## 核心价值提炼

### 创新之处

1. **「桥接层缝合新旧代码库」的重写架构**（最值得学）：`src/au3wrap/internal/` 的 `au3project.cpp`（旧工程模型接新架构）、`domaccessor/domconverter`（旧 wxWidgets DOM ↔ 新 UI 数据转换）、`wxlogwrap/wxtypes_convert`（wx 类型/日志适配，让旧引擎不依赖 wx 也能被 Qt 宿主调用）——把新 Qt UI 与旧 au3 引擎解耦缝合。
2. **旧引擎模块化拆解**：`au3/libraries/` 把旧引擎拆成 78 个 `au3-*` 子库（audio-io/fft/mixer/effects/nyquist-effects/cloud-audiocom…），作为 4.0 的音频内核保留。
3. **跨产品共享框架**：复用 MuseScore 4 的 Muse Framework（git submodule），两旗舰共享 Qt/QML 应用框架。
4. **Nyquist 内置脚本引擎**：用 Common Lisp 方言 Nyquist 做音频效果脚本——经典且独特的可编程音频处理。

### 可复用的模式与技巧

1. **遗留现代化「保留引擎、重建 UI」**：用桥接/适配层把验证过的核心接进新框架，而非整体重写——降低风险的经典策略。
2. **类型/日志适配层解耦框架依赖**：`wxtypes_convert`/`wxlogwrap` 让旧引擎摆脱对旧 UI 框架（wx）的硬依赖。
3. **核心拆成模块化子库**：把单体引擎拆成几十个可独立编译/复用的库。
4. **多产品共享框架（submodule）**：两个应用共享同一 Qt/QML 框架降低维护成本。

### 关键设计决策

- **保留 au3 引擎 vs 重写引擎**：选保留——音频引擎是 26 年积累的最值钱资产，重写风险过高；只重建 UI。
- **Qt/QML vs 继续 wxWidgets**：选 Qt（现代声明式 + 复用 Muse Framework），代价是桥接复杂度与社区对选型的争论。
- **3.x + 4.0 双线并行**：稳定线持续维护，避免重写期用户断供。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | Audacity | Tenacity | Ocenaudio | Ardour |
|------|----------|----------|-----------|--------|
| 定位 | 大众入门音频编辑器 | Audacity 无遥测分叉 | 轻量免费编辑器 | 专业开源 DAW |
| 开源 | ✓ GPL | ✓（回退到争议前） | ✗ 闭源免费 | ✓ |
| 遥测 | 有（争议后回退大部） | 无（卖点） | 无 | 无 |
| 现代化 | 4.0 Qt 重写中 | 落后主线 | 界面较现代 | GTK 自维护 |
| 资源/活跃 | Muse Group 全职团队 | 人力有限、缓慢 | 闭源团队 | 社区 |
| 受众 | 海量大众 | 隐私敏感用户 | 轻量需求 | 专业音频 |

### 差异化护城河

护城河 =「**免费开源 + 跨平台 + 简单易上手 + 海量用户/教程生态 + 4.0 现代化重写 + Muse Group 全职资源**」。它在「免费开源入门音频编辑」细分里近乎垄断——巨大的用户基数与教程生态是分叉（Tenacity）难以撼动的网络效应。

### 竞争风险

- **隐私信任的历史包袱**：2021 遥测争议虽大部回退，但「Muse Group 云 upsell / 数据收集」的疑虑仍存（Tenacity 等分叉的存在即证明）。
- **重写期风险**：wxWidgets→Qt 大重写，4.0 稳定性/功能对齐需时间，迁移期可能流失耐心不足的用户。
- **专业用户分流**：Ardour/Audition/Reaper 在专业 DAW 方向分流，Audacity 主守入门。
- **首席依赖**：Paul Licameli 占比高，巴士因子偏集中（但 Muse 团队 + 大社区缓冲）。

### 生态定位

它是「免费开源、跨平台、大众入门」音频编辑的事实标准与近乎垄断者，正处 4.0 现代化转型期；Tenacity 是其隐私价值观的对照分叉，Ardour/Audition 是专业方向的互补/竞争。

## 套利机会分析

- **信息差**：非被低估（成熟大众热门），但 GitHub star 严重低估其真实影响力。内容价值在「大型遗留系统 Qt 现代化重写」的工程拆解 + 「收购→隐私争议→分叉→回退」的治理叙事。
- **技术借鉴**：「保留引擎、桥接层缝合、重建 UI」「类型/日志适配解耦框架」「核心拆模块化子库」「多产品共享框架」可迁移到任何遗留系统现代化。
- **生态位**：想剪辑/录音/处理音频的大众，这是免费首选；想学 wxWidgets→Qt 重写、遗留现代化的工程师，这是 160 万行的顶级样本；隐私敏感用户可看 Tenacity。
- **趋势判断**：Audacity 4.0 临近发布是当前关注核心；现代化成功将巩固其入门垄断，但重写质量与隐私信任修复是变量。

## 风险与不足

- **⚠️ 隐私争议的历史包袱（需正视）**：2021 年 Muse Group 收购后引入遥测 + 一份被指「possible spyware」的隐私政策（收集 OS/CPU/IP 国别/崩溃数据、含「13 岁以下勿用」被指违反 GPL），引发 535 评论的社区危机，催生 Tenacity 等分叉。Muse Group 后续回退了大部分争议措施，但信任修复是长期过程。
- **重写期不确定性**：4.0 Qt 重写仍 alpha，稳定性/功能对齐/插件兼容需观察；wxWidgets→Qt 选型有社区争论。
- **巴士因子偏集中**：首席 Paul Licameli 占比高。
- **老代码测试薄**：4.0 引入测试脚手架，但 26 年历史代码测试覆盖有限。
- **云 upsell 疑虑**：au3cloud/audio.com 等商业延伸仍引部分用户警惕。

## 行动建议

- **如果你要用它**：你要免费、跨平台、易上手地**录音/剪辑/处理音频**（播客、教育、业余音乐）——Audacity 是大众首选（3.7.x 稳定可用，4.0 现代 UI 临近）。若你极度在意隐私/无遥测，可用 Tenacity；要专业 DAW 看 Ardour/Reaper/Audition；要轻量现代界面看 Ocenaudio。
- **如果你要学它**：重点读 `src/au3wrap/internal`（au3project/domconverter/wxlogwrap 桥接缝合新旧）、`au3/libraries`（旧引擎 78 子库模块化）、`src/projectscene` + `src/effects`（新 Qt UI 重写主战场），以及 Muse Framework 路线。这是「遗留系统 Qt 现代化重写」的顶级工程样本。
- **如果你要 fork/贡献它**：注意 GPL；最有价值的方向是参与 4.0 各功能域的 Qt UI 重写、桥接层完善、插件兼容，或（如 Tenacity）做无遥测的价值观分叉。

### 知识入口

| 资源 | 链接 |
|------|------|
| 开发者文档 | https://wiki.audacityteam.org/wiki/For_Developers ｜ 官方博客 https://audacityteam.org/blog |
| DeepWiki | https://deepwiki.com/audacity/audacity （已收录，描述为「Qt/QML 前端 + 旧 Audacity 3 后端的双代码库系统」） |
| 4.0 预览 | [官方 YouTube](https://youtube.com/@audacity)（4.0 UI 预览，50 万+ 播放） ｜ [CDM: Audacity 4 UI preview](https://cdm.link/audacity-4-in-ui-preview/) ｜ [How we are building Audacity 4 — HN](https://news.ycombinator.com/item?id=45463626) |
| 隐私争议背景 | [Engadget: Audacity privacy uproar](https://www.engadget.com/audacity-privacy-policy-spyware-accusations-data-collection-210001803.html) ｜ [Tenacity（无遥测分叉）](https://tenacityaudio.org/) |

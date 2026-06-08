# 浏览器里清理 3D 高斯泼溅：Snap 旗下的标准工具

> GitHub: https://github.com/playcanvas/supersplat

## 一句话总结

SuperSplat 是一个免费、开源、纯浏览器端的 **3D 高斯泼溅（3D Gaussian Splatting, 3DGS）编辑器**——专门处理 3DGS 训练输出「最后一公里」的清理、裁剪、调色、压缩、动画与一键发布；它由 Snap 旗下的 WebGL 引擎公司 PlayCanvas 打造（CEO 亲自下场写代码），已是浏览器里处理高斯泼溅的事实标准工具。

## 值得关注的理由

- **踩在 3DGS 风口正中的细分龙头**：3D 高斯泼溅是 2023 年 SIGGRAPH 的突破性技术（NeRF 之后的当红 3D 重建/扫描/VFX 范式），2025-2026 持续升温。3DGS 训练输出往往很「脏」（有 floaters 噪点、需裁背景调色），SuperSplat 正是处理这一步的工具，被各类教程默认推荐为标准「清理 pass」——近 6 天爆发涨 142 star。
- **顶级背书 + 商业闭环**：背后是 14 年老牌引擎公司 PlayCanvas（2017 年被 Snap 收购，引擎仍 MIT 开源、15980 star）。SuperSplat 是其第二高星项目，CEO Will Eastcott 亲自提交代码、首席工程师全职主导。「免费工具引流 → PlayCanvas 平台发布/托管变现」形成闭环。
- **自有格式护城河 SOG**：PlayCanvas 2025-09 开源了 **SOG（Spatially Ordered Gaussians）压缩格式，号称「高斯泼溅界的 WebP」，比 PLY 小 15-20×**，已被第三方引擎接入——格式标准是它最深的护城河（但压缩保真度也是争议焦点，见风险节）。

## 项目展示

![SuperSplat Editor 主界面](https://github.com/user-attachments/assets/b6cbb5cc-d3cc-4385-8c71-ab2807fd4fba)

编辑器界面全景（导入 splat → 清理/裁剪 → 变换/调色 → 导出/发布）。在线零安装直接用：[superspl.at/editor](https://superspl.at/editor)。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/playcanvas/supersplat |
| Star / Fork | 9042 / 1000（大众热门，近 6 天爆发涨 142 star） |
| 代码行数 | 32K（业务 TS ≈19K；JSON 32% 是 9 国语言 i18n 文案，非业务代码） |
| 项目年龄 | 31.6 个月（约 2.5 年，2023-10 起） |
| 开发阶段 | 稳定维护（近一年 310 commit、近月仍 27，近期再提速） |
| 贡献模式 | 核心少数 + 社区（Donovan Hutchence 占 64.6%，CEO Will Eastcott 亲自参与，34 人社区） |
| 热度定位 | 大众热门 + 赛道龙头（「浏览器端 splat 编辑器」近乎垄断） |
| 质量评级 | 代码[优·引擎下沉、核心精简] 文档[优·官方 user guide + DeepWiki] 测试[弱·无显式测试目录] |
| License | MIT |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

背后是 **PlayCanvas**（伦敦，2011 年创立，3902 followers）——著名的开源 WebGL/WebGPU 浏览器 3D 游戏引擎公司，**2017 年被 Snap（Snapchat 母公司）收购**，引擎仍保持 MIT 开源、驱动了 Snap 大量 AR/3D 能力。主力作者 **Donovan Hutchence（slimbuck，PlayCanvas 首席工程师，占 74% commit）**，CEO 兼联合创始人 **Will Eastcott** 亲自提交代码。SuperSplat 是 PlayCanvas 在 3DGS 浪潮下推出的战略级旗舰，拥有独立域名（superspl.at）与产品页。可信度极高。

> 注：3DGS 赛道另一玩家 **Scaniverse 属 Niantic（Niantic Spatial）而非 Snap**——被 Snap 收购的是 PlayCanvas。两者是分属不同巨头的互补玩家（Niantic 主捕获/地图，PlayCanvas/Snap 主编辑/发布引擎）。

### 问题判断

3DGS 的工作流是「捕获 → 训练 → 编辑 → 发布」。捕获/训练端已有 Luma AI、Polycam、Postshot、Scaniverse 等玩家，但训练输出是一团「脏」高斯——有漂浮噪点、背景杂物、色偏，文件还动辄上 GB。PlayCanvas 看到的缺口是：**没有一个零门槛、跨工具、专注「编辑清理与发布」的标准工具**。它没去抢捕获/训练这块拥挤的地，而是专攻后处理的「最后一公里」——纯浏览器、零安装、多格式互通，让任何来源（Postshot/Luma/Polycam…）的 splat 都能导进来清理、调色、压缩、发布。时机上 3DGS 2024-2026 爆发，正是做「事实标准编辑器」抢心智的窗口。

### 解法哲学

- **明确选择浏览器优先、零安装**：无服务端处理、无原生安装，打开网页即用、完全免费 MIT。
- **明确选择「编辑/发布」而非「捕获/训练」**：与捕获工具互补而非竞争，做流水线枢纽。
- **明确选择把渲染/数学下沉引擎**：核心逻辑压在 2 万行 TS 以内，复杂度交给 PlayCanvas 引擎。
- **明确选择自建压缩格式 SOG**：用「3DGS 界的 WebP」抢格式标准，形成护城河。
- **明确选择免费工具引流 → 平台变现**：SuperSplat 2.0 一键发布到 PlayCanvas 托管，闭环商业化。

### 战略意图

SuperSplat 是 PlayCanvas/Snap 在「空间计算/AR」大赌注里的一块拼图：用免费开源的事实标准编辑器占领 3DGS 创作者心智，引流到 PlayCanvas 引擎 + 云发布/托管生态，并用 SOG 格式标准锁定生态。与自家 `engine`、`pcui`、`sogs`、`splat-transform` 形成完整工具链闭环。

## 核心价值提炼

### 创新之处

1. **浏览器端百万级高斯点的可靠编辑**（最值得学）：在 Web 里对数百万高斯做选区/变换/裁剪并保证撤销/重做可靠——靠 `edit-ops.ts`（Command 模式 `EditOp` 接口 do/undo/destroy + MultiOp 组合 + StateOp 位掩码批量操作选区）+ `edit-history.ts`（history 栈 + cursor 游标）+ **共享 `CommandQueue` 串行化所有变更**（保证 undo/redo 与 GPU 异步 splat 计算严格按发起顺序应用）。这是超出玩具级编辑器的工程设计。
2. **多格式序列化枢纽**：`splat-serialize.ts` 支持 .ply/.splat/.sog/.compressed.ply 等多格式导入导出，处在多工具流水线的中心，是 3DGS 格式互通的关键。
3. **SOG 压缩格式**：Spatially Ordered Gaussians，~95% 体积压缩、比 PLY 小 15-20×，开源规范、被第三方引擎接入——为 Web 大规模 splat 流式加载铺路。
4. **引擎下沉的极简架构**：把渲染/数学/资源管理全交给 PlayCanvas 引擎，自身核心逻辑 <2 万行就实现一个完整 3D 编辑器。

### 可复用的模式与技巧

1. **Command + 共享队列的撤销/重做**：异步 GPU 编辑场景下，用 CommandQueue 串行化保证 undo/redo 顺序一致——任何「异步重计算 + 可靠撤销」的编辑器都可借鉴。
2. **把重活下沉到引擎/底座**：复用成熟引擎（渲染/场景图/数学），应用层只写业务逻辑，大幅压缩代码量。
3. **纯前端 rollup bundle + 0 runtime 依赖**：所有运行时库打包进产物直接部署，简化交付。
4. **自建领域压缩格式抢标准**：SOG 之于 splat，类比 WebP 之于图片——在新兴数据形态上定义格式即定义生态位。

### 关键设计决策

- **WebGL/WebGPU shaders 做高斯渲染/拾取**：13 个 shader（splat 主渲染、overlay、outline 描边、intersection 拾取、select-by-range 框选、histogram），是 3DGS GPU 渲染与交互的核心。
- **i18n 优先（9 国语言）**：JSON 32% 全是 locales，面向全球 3DGS 社区。
- **高频小步发版**：172 tag/100 release（约每月 5-6 个），持续滚动上线 superspl.at，版本号即 commit message。

## 竞品格局与定位

### 竞品对比矩阵（3DGS 工具分「捕获/生成」与「编辑/查看」两层，SuperSplat 专攻编辑层）

| 工具 | 层 | 形态 | 与 SuperSplat 关系 |
|------|----|------|---------------------|
| SuperSplat | 编辑/发布 | 免费开源·纯浏览器 | —— |
| Postshot | 训练+编辑 | 桌面商业·本地 GPU | 互补（训练）+ 部分重叠（编辑），常共用 |
| Luma AI / Polycam | 捕获/生成 | Web/iOS 云·闭源 | 互补（生成后导入 SuperSplat 编辑） |
| Scaniverse（Niantic） | 捕获 | 免费手机 app | 互补（手机扫描 → 桌面精修） |
| antimatter15/splat | 查看 | Web viewer | 仅查看，能力远窄于 SuperSplat |
| Blender 3DGS 插件 | 编辑/VFX | Blender 付费插件 | 互补（DCC 流水线动画/合成） |

### 差异化护城河

护城河 =「**免费开源 MIT + 纯浏览器零安装 + 多格式互通 + 专注编辑清理（非捕获/训练）+ PlayCanvas 引擎/WebGPU 背书 + 自有 SOG 格式标准 + 先发的社区心智（教程默认推荐）**」。在「3DGS 浏览器编辑器」这一垂直格里几乎无同量级对手。

### 竞争风险

- **压缩保真度是阿喀琉斯之踵**：issue #356（压缩后高斯位置/渲染肉眼可见偏移，35 评论）直击 SOG/压缩路线的软肋——护城河越深，渲染一致性争议越尖锐。
- **跨工具格式互通的持续战争**：#396（Postshot PLY 在 SuperSplat 渲染不一致）说明球谐系数/格式解读差异是长期战场，互通性 = 生死线。
- **巨头入场/被造**：3DGS 是风口，更大玩家（含 Snap 自身其他产品、Adobe、Blender 原生）若发力编辑层会带来压力。
- **不做捕获/训练的边界**：需配合 Polycam/Postshot 等，自身只在流水线一环。

### 生态定位

它是 3DGS 这一蓝海赛道里「浏览器端编辑器」垂直格的事实标准与近乎垄断者，是多工具流水线（捕获→训练→**编辑**→发布）的枢纽，并以 SOG 格式标准 + PlayCanvas 引擎绑定守住生态位。

## 套利机会分析

- **信息差**：非被低估，而是「风口正中的赛道龙头」。内容价值在于它是 3DGS 这一前沿技术的最佳上手入口与「事实标准工具」深度解读，以及浏览器端 3D 编辑器的工程样本。
- **技术借鉴**：「Command + 共享队列撤销重做」「引擎下沉极简架构」「自建领域压缩格式抢标准」「WebGPU splat 渲染/拾取」可迁移到任何 Web 3D/编辑器/新数据形态项目。
- **生态位**：做 3DGS 扫描/测绘/VFX/Web 发布的人，这是零门槛必备工具；想理解 3DGS 工作流或 Web 3D 编辑器架构的人，这是优质样本。
- **趋势判断**：3DGS + 空间计算（Snap/Niantic 押注）是明确上升方向，SuperSplat 凭事实标准地位 + SOG 格式 + 巨头背书占据头部；压缩保真与互通性是需持续打磨的变量。

## 风险与不足

- **压缩保真度争议**：SOG/压缩后渲染偏移是被专业用户反复提的痛点（也是格式护城河的代价）。
- **跨工具互通性**：不同训练工具的格式/球谐解读差异导致渲染不一致，需持续对齐。
- **只覆盖编辑层**：不做捕获/训练，必须配合其他工具组成完整流水线。
- **大规模性能**：>2G PLY 保存慢等大文件场景仍有性能瓶颈（专业大规模扫描诉求）。
- **测试薄弱**：无显式测试目录，质量靠团队 + 社区反馈与高频发版兜底。
- **生态绑定**：发布/托管闭环绑 PlayCanvas 账号，深度商业化路径依赖母公司战略。

## 行动建议

- **如果你要用它**：你在做 **3DGS 扫描/测绘/VFX/Web 发布**，需要清理 floaters、裁剪、调色、压缩、动画或一键发布——打开 [superspl.at/editor](https://superspl.at/editor) 零安装即用，是当前最佳免费开源选择。捕获/生成端配合 Polycam/Postshot/Luma/Scaniverse。
- **如果你要学它**：重点读 `src/edit-ops.ts` + `src/edit-history.ts` + `src/command-queue.ts`（Command + 共享队列撤销重做）、`src/splat-serialize.ts`（多格式序列化）、`src/shaders`（WebGL/WebGPU splat 渲染与拾取）、`src/data-processor`（GPU 处理百万高斯点）。这是「引擎下沉 + 浏览器端大规模 3D 编辑」的优秀范本。
- **如果你要 fork/扩展它**：最有价值的方向是改进压缩保真度（SOG 渲染一致性）、增强跨工具格式互通、补测量/动画等专业工具，以及大文件性能优化。

### 知识入口

| 资源 | 链接 |
|------|------|
| 在线工具 | https://superspl.at/editor （零安装直接用） |
| 官方文档 | [SuperSplat User Guide](https://developer.playcanvas.com/user-manual/gaussian-splatting/editing/supersplat/) ｜ [SOG 格式规范](https://developer.playcanvas.com/user-manual/gaussian-splatting/formats/sog/) |
| DeepWiki | https://deepwiki.com/playcanvas/supersplat （已收录，10 章节架构文档） |
| 关联论文 | 3DGS 原始论文 Kerbl et al., *3D Gaussian Splatting for Real-Time Radiance Field Rendering* (SIGGRAPH 2023) |
| 独立评测 | [SuperSplat Review 2026 — THE FUTURE 3D](https://www.thefuture3d.com/software/supersplat/) ｜ [Radiance Fields — SuperSplat](https://radiancefields.com/platforms/supersplat) |

# GitHub 推荐：单人 96% 贡献、9 年写出的开源 PBR 神器：ArmorPaint 凭什么让 Substance 用户叛逃

> GitHub: https://github.com/armory3d/armorpaint

## 一句话总结
ArmorPaint 是 Lubos Lenco 用 9 年、6200+ commit 独立打磨出的开源 GPU-native PBR 纹理绘制工具，把「节点图编译器 + 自研 path-tracer + 本地 AI 推理」塞进一个 10 MB 的单 exe，正在挑战 Substance Painter 的订阅制壁垒。

## 值得关注的理由
- **真实的开源护城河**：zlib 源码公开 + 官网付费分发 + 5 套 GPU 后端（Vulkan/D3D12/Metal/OpenGL/WebGPU）跑通「同一份节点图 → 同一份着色器」这条主线，是 Blender/Substance 都没做到的工程纪律。
- **本地 AI + 隐私**：FLUX.2、Real-ESRGAN 等 8GB+ 模型托管在 HF 上按需下载，推理跑在用户显卡上、不上云——对中小工作室是巨大差异化卖点。
- **行业稀缺定位**：4.9K ★、单人 96% 贡献率、月均 100+ commit，但产品成熟度已追平商业级 DCC；Substance 订阅化后留下的真空，ArmorPaint 是少数填得上的开源选项之一。

## 项目展示

![ArmorPaint viewport showcase](https://armorpaint.org/img/git.jpg)
*主视口：path-tracer 实时预览的 PBR 绘制界面*

![ArmorPaint main viewport 1](https://armorpaint.org/img/1.jpg)
*节点化材质编辑 + 多通道绘制的标准工作流*

![ArmorPaint path tracing demo](https://www.youtube.com/watch?v=y2slMWkVkOE)
*YouTube 演示：viewport 路径追踪与烘焙共享同一份 shader*

![ArmorPaint edge wear / PBR feature showcase](https://armorpaint.org/img/gallery/3.jpg)
*边缘磨损、PBR 多通道堆叠的成品质感*

> 视频：[ArmorPaint path tracing demo](https://www.youtube.com/watch?v=y2slMWkVkOE)

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/armory3d/armorpaint |
| Star / Fork | 4,906 / 547 |
| 关注者 | 129 |
| 代码行数 | 313,717 行（按代码行；C 74% / C Header 17.2% / JSON 3.4% / Objective-C 2.5% / JavaScript 1.5% / GLSL+HLSL 0.9%）|
| 项目年龄 | 105 个月（首 commit 2017-12-14；GH 仓库建于 2017-02-06）|
| 开发阶段 | 密集开发（近 30 天 165 commit、近 90 天 401 commit、近 365 天 1,374 commit）|
| 贡献模式 | 极度单人主导（luboslenco 5,953 commits ≈ 96%；Top 2 合计 98.5%）|
| 热度定位 | 小众精品 / 垂直细分里的头部开源选项 |
| 质量评级 | 代码 良好 · 文档 一般 · 测试 不足 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景
Lubos Lenco 是 Armory 3D 组织的核心开发者，也是 GitHub 上 `luboslenco` 这个 ID 背后的唯一长期推动者。bio 只写了「Graphics Creation Tools」，但从他维护的 35 个公开仓库（armory、armorpaint、armorlab、armorsculpt、armsdk、iron、armorcore、Kromx 等）能看出：他不是图形学研究者，而是一个**把游戏引擎那一整套技术栈搬到 DCC 工具领域**的工程实践派——反向操作 Blender「把游戏引擎集成进 DCC」的方向。

### 问题判断
Lubos 先做了 Armory3D 游戏引擎（2014 起），在自研引擎过程中反复需要给模型贴 PBR 贴图：用 Blender 觉得工作流破碎、用 Substance 又贵又绑平台。这是经典的 dogfooding——**不是观察市场缺口，而是被自己的引擎需求逼出来的内部工具**，后来独立成产品。

### 解法哲学
- **极致自研、不基于 Electron/Qt/Unreal**：自己写 3D 引擎（Iron）、窗口系统、UI 框架（Zui）、shader 编译器（Kong）、嵌入式 C 脚本（minic）、C 数学/IO 核心（armorcore）。结果 < 10 MB 二进制、单 exe、零运行时依赖。
- **GPU-native 而非 GPU 加速**：节点图 → Kong → 直接编译成 D3D12/Vulkan/Metal/WebGPU shader，**不是** OpenGL 时代那种「脚本化渲染器套壳」，这是官方文档反复强调的差异化。
- **明确不做什么**：不做云、不做协作、不做资产商城、不做模型雕刻（Sculpting 模块长期 in development，资源不足时宁可推迟也不做半成品）。

### 战略意图
ArmorPaint 是 Armory 3D 组织产品矩阵的**核心可视化层**：同组织还有 armorpaint、armorlab（AI 材质）、armorsculpt、armsdk、iron（引擎）——全部基于 `base/` 同一套引擎。开源策略是 **genuinely open（zlib-like）+ 商业二进制付费**（官网下载付费，源码公开），即「源码开放 + 官方分发收费」模式，既不锁死贡献者、也保证作者能从产品本身拿回研发资金。

## 核心价值提炼

### 创新之处

| 创新点 | 新颖度 | 实用性 | 可迁移性 |
|--------|--------|--------|----------|
| 节点图 → 多 GPU 后端 shader 单趟编译（Kong） | 4/5 | 5/5 | 4/5 |
| 「主程序 < 10 MB + 重模型走子进程」 的桌面 AI 集成模式 | 3/5 | 5/5 | 5/5 |
| 嵌入式 C 子集脚本 + struct 布局通过 offsetof 透传（minic） | 3/5 | 4/5 | 3/5 |
| 同一份 path-tracer shader 通过 `#define` 切「实时 vs 离线」两档 | 2/5 | 5/5 | 5/5 |
| IMGUI + 节点画布纯数据模型 → 撤销/重做 = 数组快照 | 2/5 | 4/5 | 4/5 |

### 可复用的模式与技巧

1. **`#include 「*.c」` 单 TU 单二进制 + armpack 二进制序列化**：适合需要「单 exe 部署 + 极快加载」的 DCC 工具。文件不用拆 .h，build 就是 amake 串 C 源；数据用 armpack 二进制 round-trip，比 JSON 快一个量级。
2. **节点编译结果做 `string_buffer` 增量拼装**：送编译前先 `static_array` 检查重复 const/texture，避免重定义和冗余 binding。`static_array` 宏（kong.h）是无 GC 环境下手写的固定容量数组，适合嵌入式 C。
3. **「节点类型即 .c 文件」+ `main.c` 大 include**：130+ 节点每个一个 .c 文件，各自实现 `xxx_node_button` / `xxx_node_run`，通过 `_kickstart()` 注册；新增节点 = 新增 .c + 一行 include，**无注册中心、无工厂、无反射**。
4. **`/tools/tcc` 嵌入式 C 编译器 + `/tools/amake` 任务驱动构建**：把 TCC 拖进仓里，意味着任何平台都能「裸机编译」而不依赖系统 C 编译器（适合 WASM/iOS 等难装工具链的目标）。
5. **LSP-like API 自动发现 = `minic_ext_func_count_get` + `minic_ext_func_name_at`**：注册到解释器的函数列表自动暴露给编辑器做 autocomplete，无需手维护 API 文档。

### 关键设计决策

1. **决策**：节点图 → 自研 Kong shader 编译器 → 5 种 GPU 后端
   - **问题**：节点图编辑器需要实时编译出可执行 shader；各家 GPU 着色语言不统一
   - **方案**：单趟编译器前端 = Kong IR（类似 Rust MIR 但带显式 type_id），后端分别输出 kong_hlsl/kong_metal/kong_spirv/kong_wgsl/kong_cstyle
   - **Trade-off**：5 套后端各 ~900~4000 行是真实维护成本（总 1.1 万行），但换来「同一份节点图在 Win/macOS/Linux/WASM 上行为完全一致」+ 节点修改 < 50ms 出图
   - **可迁移性**：高——任何需要「节点图 → 多 GPU 后端 shader」的引擎都能直接接入

2. **决策**：神经网络用「外挂可执行 + 进程通信」而非嵌入式推理
   - **问题**：FLUX.2 klein（8.7 GB）、Qwen3-27B（15.3 GB）、Hunyuan3D（12.6 GB）比 ArmorPaint 自己二进制（10 MB）大 1000 倍
   - **方案**：把模型托管在 HF 自己的组织（`armory3d/FLUX.2-klein-4B-GGUF` 等），用户首次用某节点时拉取到本地，通过 `iron_exec_async()` 启动 `iris` 二进制 + GGUF/SafeTensors 文件，子进程跑推理
   - **Trade-off**：首次体验门槛高（8~20 GB 下载）；但换来「主程序永远 < 10 MB」「想用哪个模型下哪个，不强制捆绑」+ 完全不污染渲染主线程
   - **可迁移性**：高——任何「重模型 + 轻壳」的桌面工具都能用「主程序 + 子进程 + GGUF 拉取」模式

3. **决策**：通过「配置 Blender 可执行文件路径」桥接 Blender，而非内置 importer
   - **问题**：直接读 .blend 需要逆向 Blender 私有 DNA 格式
   - **方案**：`import_blend_mesh.c` 要求用户填本地 Blender 可执行路径，后台用 `blender --background --python <script>` 调 Blender 把 mesh/glb 倒出来再读
   - **Trade-off**：失去「无 Blender 即可导入 .blend」的便利；但避免锁版本（Blender 改 DNA 格式不会影响 ArmorPaint）
   - **可迁移性**：中——适合「封闭私有格式 + 用户大概率装了该应用」的场景

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | ArmorPaint | Substance Painter | Mari | 3D-Coat | Blender Texture Paint |
|------|-----------|-------------------|------|---------|----------------------|
| 价格模式 | 开源 + 付费分发 | Adobe 订阅 | Foundry 商业授权 | 部分免费 | 免费内置 |
| 跨平台 | Win/macOS/Linux/Android/iOS/WASM | Win/macOS | Linux 为主 | Windows 优先 | 全平台 |
| 节点化材质 | ✓（Kong 编译） | ✗ | ✗ | ✗ | 弱 |
| 实时 path-tracer | ✓（viewport + bake 共享 shader） | ✗ | 弱 | ✗ | 弱（CPU） |
| 本地 AI | ✓（FLUX.2、Real-ESRGAN、Hunyuan3D） | 弱（Adobe Firefly 云） | ✗ | ✗ | 弱 |
| 二进制体积 | < 10 MB 单 exe | 数 GB | 数 GB | 数 GB | Blender ~200 MB |
| 开源 | ✓（zlib） | ✗ | ✗ | 部分 | ✓（GPL） |

### 差异化护城河
跨平台 + 节点图 + 本地 AI + < 10 MB 单 exe —— 这是四个**独立护城河**的组合，单一竞品很难同时具备。Substance 不开源、Mari Linux-only、3D-Coat Windows 优先、Blender 体积大且 Texture Paint 不是核心——ArmorPaint 在「订阅逃逸 + AI 本地化 + 跨平台」三角交集上是稀缺定位。

### 竞争风险
- **最大威胁：Blender 持续增强 Texture Paint**（免费 + 内置 + 生态）—— 一旦 Blender 在节点化 path-tracer 和 AI 集成上追上来，ArmorPaint 的护城河会被显著削弱。
- **次要威胁**：Substance 一旦回到买断制，或者 Adobe 把 Firefly 模型端侧化。
- **作者风险**：bus factor 高——单人 96% 贡献率意味着 Lubos 一旦退出，10 年的工程积累很难被 35 个贡献者集体接住。

### 生态定位
介于「独立 DCC 工具」和「Blender 插件」之间的**轻量级跨平台 PBR 工具**，核心价值是「订阅逃逸 + AI 本地化 + 跨平台」。整个 Armory3D 工具家族（armory / armorpaint / armorlab / armorsculpt）共享 `base/` 引擎层，是一个事实上的「开源 DCC 工具链」——和 Adobe / Foundry / Blender 形成对位。

## 套利机会分析
- **信息差**：低关注度但高质量——4.9K ★ 与产品成熟度、行业关注度、commit 节奏不匹配；Substance 订阅化后大量独立美术转向 ArmorPaint，但行业认知还停留在「小众替代品」。
- **技术借鉴**：
  - Kong 节点编译器的多后端 shader 编译思路（5 套后端 + 单趟 IR）值得任何做「节点式 GPU 编辑器」的团队参考。
  - 「主程序 < 10 MB + 重模型走子进程 + GGUF 拉取」的桌面 AI 集成模式，是 ComfyUI / Pinokio 的简化版——主程序永远轻、子进程按需拉取、HF 模型托管。
  - minic 的 `MINIC_STRUCT` + `offsetof` 透传 C struct 字段，是嵌入式脚本替代 Python 的实用方案。
  - `static_array` 宏（kong.h）是无 GC 环境下写 C 容器的好模板。
- **生态位**：填补了「订阅逃逸 + AI 本地化 + 跨平台」的三角空白，是少数能跑通「开源 + 商业分发」模式的开源 DCC。
- **趋势判断**：本地 AI 推理（GGUF、llama.cpp 生态）是 2024–2026 年的明确趋势，ArmorPaint 早在 2023 年就押对了方向；和 ComfyUI、Pinokio、LM Studio 的轨迹一致——桌面 AI 工具正在走向「轻壳 + 重模型按需」的标准模式。

## 风险与不足
- **bus factor 极高**：单一作者 96% 贡献率，第二贡献者 MathemanFlo 仅 132 commits（2.1%）；Lubos 任何意外都会让项目进入低速期。
- **测试覆盖不足**：仅 `base/sources/libs/minic_tests.c` + `base/tests/` + `paint/assets/plugins/dev/test.c`；**无 CI 跑测**（CI 只跑 build 编译），节点编译器 Kong 缺单元测试。
- **文档薄弱**：无 API 文档、无架构 ADR、无 CHANGELOG；中文社区 wiki / DeepWiki 25 页是事实补偿。
- **构建/运行复杂度税**：「自研工具链（Kha/Kromx/Iron/amake）+ 三大 OS + 多 GPU 后端」的构建路径让 issue #1671（31 评论讨论构建失败）成为长期痛点。
- **Sculpting 模块长期 in development**：路线图上的核心承诺一直未交付，说明作者精力或优先级在 PBR 绘制一侧。
- **商业模式风险**：官网付费分发依赖个人/小工作室付费意愿；如果 Adobe 重新推出买断制 Substance Painter，独立用户付费动力会下降。

## 行动建议

- **如果你要用它**：作为独立 3D 美术 / 中小工作室的 Substance 替代——尤其当你在意订阅成本、AI 本地推理、跨平台（Linux/macOS）时；从 .fbx/.obj 导入现有 pipeline 无缝；预算紧张时直接付费下载二进制即可，预算充裕可以自编译参与改进。
- **如果你要学它**：重点关注：
  - `base/sources/iron.c` + `base/sources/iron_ui.c` + `base/sources/iron_ui_nodes.c` — Iron 引擎 + Zui IMGUI + 节点画布的整套实现
  - `base/sources/libs/kong/` — Kong shader 编译器的 IR + 5 套后端
  - `base/sources/libs/minic/` — 嵌入式 C 解释器的 `MINIC_STRUCT` + `minic_register` 模式
  - `paint/sources/` — ArmorPaint 应用层（Haxe → C）
  - `paint/sources/raytrace_brute.comp` — 一份 shader 通过 `#define` 切实时/离线的范本
- **如果你要 fork 它**：
  - 优先补 CI 测试（Kong 编译器单元测试、节点图 round-trip 测试），目前测试覆盖是最大短板
  - 补 CHANGELOG / API 文档，DeepWiki 已收录但官方文档是空白
  - 国际化（issue #118 已关闭但实际仍是英文为主）
  - 帮忙分担 Lubos 的 release 工作流——目前 `.github/workflows/` 只有三平台 build，无 release workflow

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [deepwiki.com/armory3d/armorpaint](https://deepwiki.com/armory3d/armorpaint)（25 页 wiki，已收录，子系统级拆解 Iron 引擎 / Paint 渲染管线 / Path Tracing / Kong Shader / Plugin / Minic） |
| Zread.ai | 未确认收录（Cloudflare 拦截） |
| 关联论文 | 无 |
| 在线 Demo | 无可托管浏览器 Demo；应用本身有 WebGPU WASM 构建 `armorpaint_web`，但 Star 数 5，非主要分发形式 |
| 官方文档 | [armorpaint.org](https://armorpaint.org) + [docs/armorpaint.org](https://armorpaint.org/docs) |
| 开发者 wiki | [github.com/armory3d/armorpaint/wiki](https://github.com/armory3d/armorpaint/wiki) |

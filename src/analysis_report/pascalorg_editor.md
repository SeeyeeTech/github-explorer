# R3F 教学顶流的 16K star 真产品：浏览器里盖楼，还能交给 AI

> GitHub: https://github.com/pascalorg/editor

## 一句话总结

Pascal Editor 是 React Three Fiber / Three.js 教育顶流「Wawa Sensei」（Wassim Samad）主导、Pascal 公司出品的 **Web 原生 3D 建筑/BIM 编辑器**——用 React Three Fiber + WebGPU 在浏览器里盖楼（墙/楼板/门窗布尔挖洞/楼梯/IFC 互操作），免安装免登录即可用，开源 MIT。它最锋利的差异化是 **AI-native**：`@pascal-app/mcp` 把整个编辑器的领域操作暴露成 28 个 MCP tool，AI agent 能用和人完全相同的代码路径直接生成、改造建筑模型（一句「80㎡ 两居室」brief 就能转成增量场景）。16.4K star、4.8 个月 911 commit 仍在全速冲刺 1.0（v0.9.0）。

## 值得关注的理由

1. **一份「教育者的工程素养」如何变成产品架构**：作者的 devlog《3 R3F Mistakes I'll Never Make Again》是这个仓库的设计说明书——三条教训（把 React 重渲染塞进 Three.js frameloop、过度依赖 Zustand 响应式、把逻辑写进组件而非 system）被工程化成 core/viewer/editor 三层 + dirtyNodes 性能模型。`packages/core` 是唯一事实源、**禁止 import Three.js**（AGENTS.md 明文铁律，还有 `review-architecture` AI skill 自动审 PR）；几何更新走「store 标脏 → system 在 `useFrame` 每帧只处理脏节点 → 算完即清」，**完全绕开 React 渲染管线**。这是别人难抄的资深 R3F 工程素养。
2. **MCP-as-product-API：把整个编辑器交给 AI 的范式样板**：`packages/mcp` 的 `SceneBridge` 直接复用真实的 `@pascal-app/core` store——所以 agent 的每次变更都走和 UI 一样的代码路径、自动获得 Zundo undo/redo。28 个 tool 分三层（原子 `create_wall`/`cut_opening`、语义 `create_room` 一次产 zone+slab+ceiling+walls、校验 `validate_scene`/`check_collisions`），`apply_patch` 先全量 dry-run 校验、全过才一次性提交（失败不污染状态）。还有 SQLite + SSE live sync：**agent 在改、人在浏览器里实时看着楼长出来**。这套「bridge 包裹既有 store + UI 操作映射成 MCP tool + batch dry-run + 高层语义工具降 LLM 出错率」可迁移到任何想 AI-native 化的复杂编辑器。
3. **几个可直接抠走的工程范式**：① **扁平字典 + parentId 的场景模型**（树语义扁平存，换 O(1) 访问与廉价 undo/persist diff）；② **dirtyNodes + useFrame system**（把高频派生几何计算从 React 剥离）；③ **编译期类型安全的 mitt 事件总线**（TS 模板字面量类型从 33 节点 × 8 后缀自动展开 `wall:click` 全部事件键）；④ **three-bvh-csg 实时门窗布尔挖洞**（CSG/BVH 严格隔离在 viewer 层，core 不碰 Three）；⑤ **库 + 成品双发布**（Turborepo 一次发 5 个 npm 包，开源引流 + private-editor 私有上层变现）。

## 项目展示

![Pascal Editor](https://opengraph.githubassets.com/1/pascalorg/editor)

> 在线 demo（免登录即玩）：https://editor.pascal.app —— 可现场建墙/楼板/门窗布尔挖洞、IFC 导入、MCP 让 AI 盖楼。README 顶部有完整产品演示视频。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/pascalorg/editor（官网 https://editor.pascal.app） |
| Star / Fork | 16,443 / 2,187（fork 偏高，大量开发者拆解学习 R3F 工程化） |
| 代码行数 | 167,043 行（TSX 55.9% + TS 41.4% = 97.3% 纯 TS/React）；1061 文件；注释比 0.124（作者刻意「只写解释 why 的注释」） |
| 项目年龄 | 4.8 个月（git 口径，首提交 2026-01-14 `create-turbo`；仓库 2025-10-16 建立，迁 Turborepo 时约 3 个月历史被 squash，故为下限）；最后提交 2026-06-07（今天） |
| 开发阶段 | 密集开发 · 冲刺 1.0（近 30 天 242 commit、近 90 天 515，5 月单月 240 创新高，毫无降速） |
| 贡献模式 | 公司团队 + 社区（30 贡献者，wass08+Wassim SAMAD 同一人 ~540 占 ~59%；sudhir/Aymeric Rabot/Pascal 等骨干；周末 9%/深夜 12% 公司白天作息） |
| 热度定位 | 大众热门 · 高速增长（8 个月 16K star，有真 demo 支撑的高质量增长） |
| 版本 | v0.9.0（12 tag，SemVer，feature 25%>fix 17% 冲刺 1.0）；已发 npm @pascal-app/core + viewer |
| License | MIT |
| 质量评级 | 代码组织/文档「优」· 错误处理「良」· 测试/CI「中（92 测试偏 core/mcp，主 CI 不跑测试）」 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

**头号贡献者 wass08 = Wassim Samad =「Wawa Sensei」**——法国开发者、常驻东京，10 年 Web/移动/VR 经验，**R3F/Three.js 教育界顶流**（YouTube 频道 Wawa Sensei、付费课程站 wawasensei.dev《React Three Fiber: The Ultimate Guide》）。git 提交合计 ~540（约 59%），是绝对核心。org = **pascalorg**（Pascal 公司，bio「Intelligence upgrade for every building」，homepage editor.pascal.app），团队 30 人（sudhir/Aymeric Rabot 等）。核心叙事：**一位 R3F 教学博主把毕生功力投入做一个真·商业 3D 建筑产品**——这是「教育者 → 产品创始人」的稀缺范本。

> 消歧：另有同名「Pascal AI Labs」（投研自动化，班加罗尔）与本项目无关。

### 问题判断

专业 BIM/建筑设计长期被桌面巨头垄断——Revit/ArchiCAD 重、贵、闭源、license 锁定、协作靠文件交换。Pascal 的赌注是把「专业建筑建模」整体搬到浏览器：免安装免登录即可建模、URL 分享、导入导出 JSON/IFC/GLB。而现有方案都不够：通用 Web 3D（Spline）没有建筑语义；Web BIM SDK（That Open Engine/web-ifc）是给开发者的组件库而非成品编辑器；桌面 BIM 不可嵌入、不可分享、不 AI-native。

### 解法哲学（R3F 工程化 + 分层 + 事件驱动）

代码完整兑现 devlog 三原则，且 `AGENTS.md` 把它们写成可执行的层边界铁律：① **数据与渲染彻底分离**——core 纯领域逻辑、禁 import Three.js，viewer 只管渲染、禁知道工具/模式，apps/editor 才有工具/面板/快捷键；② **高频更新绕开 React**——节点变更丢进 `dirtyNodes: Set`，system 在 `useFrame` 每帧只处理脏节点、算完即清，React 只负责挂载/卸载占位 mesh；③ **解耦靠类型化事件总线**——`events/bus.ts` 用 mitt + TS 模板字面量类型自动展开 33 节点 × 8 后缀的全部事件组合，组件零耦合。

### 战略意图（教育者 → 创始人 + AI-native + 库双定位）

- **库 + 成品双定位**：`@pascal-app/{core,viewer,mcp,ifc-converter}` 都已/将发 npm（release.yml 一次发 5 包），既是可嵌入 SDK 又是开箱即用编辑器。AGENTS.md 透露还有 `pascalorg/private-editor` 把本仓库当 git submodule——**开源仓是商业产品的内核**，走「开源引流 + 私有上层」变现。
- **AI-native 是真战略不是噱头**：`packages/mcp` 把场景变更暴露成 28 个 MCP tool + prompt `from_brief`（散文 brief → 增量 `apply_patch`），呼应 bio。仓库根目录 AGENTS.md/CLAUDE.md/GEMINI.md（互为 symlink）+ `.agents/skills/review-architecture`——作者自己用 AI agent 开发并把规则固化进仓库。

## 核心价值提炼

### 创新之处

1. **MCP-as-product-API：把整个编辑器的领域操作暴露给 AI agent**（新颖度 5/5，实用性 4/5，可迁移性 5/5）：`SceneBridge` 复用真实 core store，28 个分层 tool + dry-run patch + 版本校验的 SQLite live sync（agent 改、浏览器 SSE 实时看）。适用任何想 AI-native 化的复杂 Web 编辑器。
2. **dirty-node + system-in-useFrame：数据驱动几何但完全绕开 React 重渲染**（新颖度 4/5，实用性 5/5，可迁移性 5/5）：store 标脏、帧循环批处理、undo 也只 diff 标脏。适用高频更新的 R3F/canvas 应用。
3. **编译期类型安全的全局事件总线**（新颖度 3/5，实用性 4/5，可迁移性 5/5）：mitt + TS 模板字面量类型从 33 节点 × 8 后缀自动生成全部事件键，组件零耦合。
4. **扁平字典 + parentId 的建筑场景模型**（新颖度 3/5，实用性 5/5，可迁移性 5/5）：树形语义用扁平存储承载，换 O(1) 访问与廉价 undo/persist。
5. **实时 CSG 门窗挖洞（three-bvh-csg + BVH 加速），CSG 严格隔离在 viewer 层**（新颖度 3/5，实用性 4/5）：core 不依赖 Three，挖洞只在渲染层。
6. **架构规则即代码：AGENTS.md 层边界 + review-architecture AI skill 自动审 PR**（新颖度 4/5，实用性 4/5）：把「不许 core import Three.js」这类铁律变成 agent 可执行的审查。

### 可复用的模式与技巧

- **Store-Bridge for MCP**：bridge class 包裹既有前端 store，UI 操作 1:1 映射成 MCP tool，batch 走 dry-run + 单步 undo——给任何编辑器加 AI 可操控能力。
- **dirtyNodes + useFrame system**：store 收集脏 id，帧循环消费并清标——把高频派生计算从 React 渲染剥离。
- **类型化 mitt 事件总线**：模板字面量类型自动展开事件键空间——大量同构事件时零样板且类型安全。
- **扁平字典 + parentId + 集中 CRUD + orphan/unreachable 清理**：树语义扁平存，序列化/undo/随机访问全便宜。
- **Zustand + Zundo partialize + limit**：几行拿到选择性持久化 + 有界（50 步）undo/redo。
- **分层渲染 via Three.js Layers**：overlay/zone/grid 各占一层，post-processing 按 layer mask 分 pass 合成。
- **库 + 成品双发布**（Turborepo 单 release 发多包）：同一内核既当 npm SDK 又当成品 app。

### 关键设计决策

最值得记录的是 **MCP server 让 AI agent 直接操控建筑模型**——它是 bio「Intelligence upgrade for every building」的代码落地，也是范式级样板。`packages/mcp` 是**无头**（Bun，无浏览器/WebGPU/React）MCP server，`SceneBridge` 直接复用真实的 `@pascal-app/core` store——所以 agent 的每次变更都走和 UI 一样的代码路径、自动获得 Zundo undo/redo。暴露 28 个 tool 分三层抽象：底层原子（`create_wall`/`place_item`/`cut_opening`）、高层语义（`create_room` 一次产 zone+slab+ceiling+walls、`furnish_room` 按房型摆家具、`create_stair_between_levels`）、校验（`validate_scene` 逐节点 Zod、`check_collisions`）。`apply_patch` 先全量 dry-run 校验、全过才一次性提交（失败不污染状态）。还有 vision tool（`analyze_floorplan_image`，走 MCP host 的 sampling）和 prompt `from_brief`。Live sync：MCP 与编辑器共享 SQLite（WAL + 版本校验），mutation 写 `scene_events` 流，浏览器经 SSE 实时应用。这个设计的 Trade-off 很诚实：把整个产品的领域操作作为 AI 接口暴露，护城河极深；但**无头模式不能跑几何 system**（墙 miter/CSG/楼梯在 React hook 里），所以 `export_glb` 直接 `not_implemented`、几何渲染必须回到浏览器 viewer。

## 竞品格局与定位

| 项目 | 形态 | 定位 | 与 Pascal 关系 |
|------|------|------|------|
| Autodesk Revit / SketchUp | 桌面闭源/付费 | BIM 行业标杆 | Pascal 牺牲 Revit 二十年专业深度（结构/MEP/明细/规范校验），换零安装/URL 分享/开源可嵌入/AI 可生成；定位「轻量+开放+智能」非取代 |
| That Open Engine (web-ifc/IFC.js) | 开源 SDK | Web BIM 组件库/IFC 工具链 | **互补非竞品**：That Open 是给开发者的积木，Pascal 是成品编辑器 + AI 层，可借其 IFC 生态做互操作 |
| Spline | 闭源 Web | 通用 Web 3D 设计 | 无建筑语义（墙/楼层/门窗布尔/IFC/碰撞）；Pascal 护城河正是领域专用 schema（33 类建筑节点）+ 建筑专用 system |
| Blender | 开源桌面 | 通用 3D 创作 | 通用、桌面、学习曲线陡、无 Web/AI-native |
| Snaptrude / Rayon / Onshape | 闭源云 SaaS | 云端 BIM/CAD | 已商业化、协作成熟，但闭源订阅制 |

### 差异化护城河

**Web 原生**（免装即用、可嵌入、可分享）+ **AI-native**（MCP 让 agent 用与人相同的代码路径改模型，深到产品内核）+ **R3F 工程化**（core/viewer/system 分层 + dirty-node 性能模型，别人难抄的工程素养）+ **专业建筑语义** + **开源成品**——这个四元交集目前没有第二家。MCP 是当前差异化最锋利的一刀。

### 竞争风险

- **WebGPU 跨平台兼容**是「Web 能否承载专业 BIM」的命门（#275 macOS 显示异常、#254 跑不起来；有 fallback 但非全平台稳）。
- **0.x 早期**：专业完备度远不及桌面 BIM，商业模型（private-editor 上层）未公开。
- **bus factor**：wass08 ~58% 提交且架构决策高度集中于他个人的 R3F 方法论——不过 CHANGELOG 显示外部 PR 活跃，风险更多在「架构掌舵」而非「日常贡献」。
- **品牌未定**：#149「Rename this product」社区要求改名。

### 生态定位

Web 原生 + 开源 + AI-native 的建筑/BIM 创作层，与 That Open（IFC SDK）互补、与通用 3D 错位、对桌面 BIM 做降维入口。真正要回答的问题是「浏览器能否承载专业 BIM 工作流」。

## 套利机会分析

- **信息差**：Pascal 同时具备「教学顶流 Wawa Sensei 下场做真产品」的人物故事 + 「AI 能盖楼（MCP）」的话题性 + 「Web 开源挑战桌面 BIM」的行业张力，三线俱全；中文圈对「MCP-as-product-API」「dirtyNodes 绕开 React 的 R3F 性能模型」「扁平字典场景模型」「教育者工程素养」的拆解稀缺。
- **技术借鉴**：Store-Bridge for MCP、dirtyNodes+useFrame、类型化 mitt 事件总线、扁平字典+parentId、Zustand+Zundo、three-bvh-csg 布尔、库+成品双发布——这些可迁移到任何复杂 Web 编辑器/3D 应用/AI-native 工具。
- **生态位**：填补「Web 原生 + 专业建筑 + 开源成品 + AI-native」空白；与 That Open 互补、对桌面 BIM 降维。
- **趋势判断**：踩在「WebGPU + AI-native + 浏览器专业工具」趋势上；长期看「WebGPU 兼容性成熟 + 专业互操作补齐（AutoCAD/地图）+ 商业化路径 + 摆脱单人架构依赖」决定其上限。

## 风险与不足

- **WebGPU 兼容硬伤**：#275 macOS 显示异常、#254 跑不起来——前沿特性的跨平台稳定性是专业用户留存的命门。
- **0.x 早期**：v0.9.0、专业完备度远不及桌面 BIM，商业化路径未公开。
- **测试/CI 短板**：92 测试偏 core/mcp，viewer 渲染层/UI 测试稀薄（WebGPU 几何无法无头测）；**主 ci.yml 只跑 lint+typecheck，核心测试未进 CI 门禁**（仅 mcp-ci.yml 跑 mcp+scene API）。
- **bus factor**：架构决策高度集中于 wass08（~58% 提交）。
- **专业互操作待补**：用户反复索要 AutoCAD/DWG、地图底图（#145/#158/#154）。

## 行动建议

- **如果你要用它**：适合建筑师/设计爱好者（成品编辑器，editor.pascal.app 免登录试）、想嵌入 3D 建筑能力的开发者（消费 @pascal-app/core + viewer npm 包）、agent 框架作者（@pascal-app/mcp 让 LLM 生成/改建筑）。注意 WebGPU 兼容（先确认浏览器/系统支持）、0.x 早期专业能力有限。要成熟专业 BIM 仍需 Revit。
- **如果你要学它**：直奔 `packages/core/src/store/use-scene.ts`（扁平字典 store + Zundo + dirtyNodes + undo diff）+ `schema/index.ts`（33 类节点 Zod schema）+ `events/bus.ts`（类型化 mitt 总线）+ `packages/viewer/src/systems/wall/wall-system.tsx` + `lib/csg-utils.ts`（three-bvh-csg 门窗挖洞）+ `packages/mcp/src/bridge/scene-bridge.ts` + `packages/mcp/README.md`（AI 操控核心）+ `AGENTS.md` + `wiki/architecture/`（层边界与设计哲学）。配合作者 devlog《3 R3F Mistakes》理解架构由来。
- **如果你要 fork / 借鉴它**：Store-Bridge for MCP、dirtyNodes+useFrame、类型化事件总线、扁平字典场景模型、库+成品双发布是可直接迁移的设计。MIT 友好；但注意它是商业产品内核（private-editor 上层），且架构高度绑定 wass08 的 R3F 方法论。

### 知识入口

| 资源 | 链接 |
|------|------|
| 在线 Demo | https://editor.pascal.app（免登录可试，最佳第一手体验） |
| DeepWiki | https://deepwiki.com/pascalorg/editor（已收录，含 monorepo 分层/core 作为事实源/扁平节点字典讲解，架构速读首选） |
| 作者课程/博客 | wawasensei.dev（R3F 终极指南）+ Wawa Sensei devlog《3 React Three Fiber Mistakes I'll Never Make Again》（本仓库架构的设计说明书） |
| 仓库内文档 | `wiki/architecture/`（15 篇架构规范）+ `AGENTS.md`/`packages/mcp/README.md`（近 400 行含坐标系 worked example） |
| npm 包 | `@pascal-app/core`、`@pascal-app/viewer`（可直接复用渲染/数据层） |
| 社区 | Discord：https://discord.gg/SaBRA9t2 |

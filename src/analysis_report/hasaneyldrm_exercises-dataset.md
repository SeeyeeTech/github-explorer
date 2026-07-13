# GitHub推荐：1324 健身动作 × 9 语言：1 个数据集如何撑起 1 套商业 App 的开源实验

> GitHub: https://github.com/hasaneyldrm/exercises-dataset

## 一句话总结

`exercises-dataset` 是一份 1,324 个健身动作的离线即用数据集（JSON + GIF + 9 语言说明），既被作者自己的 RN 健身 App LogPress 直接作为数据底座，也同时作为独立开源资产被全球开发者消费——4 个月内拿到 12.6K stars，靠的是「零依赖 + 多语言 + 本地资源 + AI 友好 setup」四件套。

## 值得关注的理由

- **数据驱动 App 的实战样本**：不是又一个 TodoMVC 或 LLM wrapper——它证明了"一个垂直数据集 + 一个 1 MB 的 HTML 浏览器 + 一个 5 行的 README"足以撑起一个真实商业产品的数据层。
- **多语言本地化的 ROI**：把翻译成本沉到数据集层（11,916 条指令 × 9 语言 0 空缺），下游 App 即可"以一当九"，而非每个 App 各自翻译。
- **AI 友好文档范本**：`setup.html` 中 6 框架 × 4 DB 笛卡尔积的"Ask Your LLM" prompt builder，把文档从"读"升级为"喂给 LLM 当上下文"——这是少见的工程实践。

## 项目展示

![杠铃卧推](https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/videos/0025-EIeI8Vf.gif)
![杠铃深蹲](https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/videos/0043-qXTaZnJ.gif)
![硬拉](https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/videos/0032-ila4NZS.gif)
![引体向上](https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/videos/0652-lBDjFxJ.gif)
![哑铃弯举](https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/videos/0294-NbVPDMW.gif)

> 五个最具代表性的复合 / 单关节动作 GIF。详情可打开仓库根目录的 `index.html` 浏览全 1,324 条。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/hasaneyldrm/exercises-dataset |
| Star / Fork | 12,588 / 1,478 |
| Watcher | 36 |
| 代码/数据规模 | ~127 MB；JSON 99%（1324 条主数据 + schema）+ HTML 1%（`index.html` 14.9 MB 浏览器 + `setup.html` 60 KB 向导） |
| 项目年龄 | ~4 个月（仓库 2026-03-18 创建；git 历史 2026-07-08~09 一次性灌入，6 个 commit） |
| 开发阶段 | 稳定维护（一次成型 + 偶发修订，波兰语/韩语新增即最近一次 commit） |
| 贡献模式 | 社区协作（3 名贡献者，作者本人占 66.7%） |
| 热度定位 | 大众热门（4 个月 12.6K stars，Fork/Star 比 11.7% 显著高于平均，真实数据消费） |
| 质量评级 | 数据覆盖 A / 多语言完整性 A / 文档 A- / 测试 C+ / CI/CD C |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

`hasaneyldrm`（Hasan Emir Yıldırım，土耳其伊斯坦布尔），自述「PM @tech · 2x Founder」，账号 9.2 年。代表作品是 **LogPress**（hasaneyldrm/logpress-public，51★，TS + RN 0.80 + Supabase + OpenAI + Adapty）——一个已经在线的 AI 健身追踪 App。本仓库是它的数据底座，与 LogPress 形成「开源数据层 + 商业 App」的垂直整合。作者的 5 个公开仓库（logpress-public / exercises-dataset / reactnativecliboilerplate / projbar / cursor-rules）共同覆盖了「移动健身生态」的每个环节。

### 问题判断

健身 / 训练追踪 App 的开发者面临三个备选：(1) ExerciseDB ASCENDAPI 的 SaaS CDN（按量付费 + 商业授权），(2) wger 的 Django REST（运维重），(3) yuhonas/free-exercise-db 等小公域 JSON（动作少、无 GIF、无 i18n）。作者看到了「5 分钟内可被任何 App 接进、能离线使用、覆盖多语言市场」这个交集的空白。

### 解法哲学

- **零依赖 / 零后端**：所有 1324 条记录 + GIF + JPG 都是仓库内相对路径静态资源，`file://` 打开 `index.html` 即用——这牺牲了运行时能力（REST、搜索服务），换取最低接入摩擦。
- **翻译沉到数据集层**：1,324 × 9 = 11,916 条 instruction 全填，下游 App 拿到即得中文 / 土耳其语 / 印地语 / 韩语本地化，跨 9 个市场。
- **可被人复用是显式目标**：README 的 Usage Examples、`setup.html` 的多框架脚手架 + LLM prompt 都是面向陌生开发者，自家 App 只是其中一个下游。

### 战略意图

> **核心信号**：issue #5 已 closed，但作者在 README 与 NOTICE.md 中已主动把媒体来源从「ASCENDAPI（被指 re-host）」切换到「Gym visual（书面授权）」，并把媒体限制在 180×180 红线分辨率。这是聪明品牌重塑 + 合规加固。

属于「用 OSS 数据层给商业 App 增信 + 获客」的成熟开源策略——exercises-dataset 充当 logpress-public 的可信背书（"我们的数据来自公开、有 schema、9 语言、MIT 授权的独立项目"），同时让其他集成方把生态中心保持在 hasaneyldrm 名下。

## 核心价值提炼

### 创新之处

1. **「AI 友好文档 + 多框架脚手架」**（`setup.html` 的 "Ask Your LLM"）—— 把数据集接入流程模板化、笛卡尔积化（6 框架 × 4 DB = 24 组合），前端实时拼接一个结构化 LLM prompt（一键复制到 ChatGPT / Claude / Gemini 即得可运行后端）。**新颖度 4/5 / 实用性 5/5 / 可迁移性 5/5**

2. **「Plug-and-play 数据集四件套」** —— 标准化发布配方：`data/{dataset}.json` + `data/{dataset}.schema.json` + `assets/` + `index.html` + `setup.html`，让任何中小型领域数据集（菜谱 / 药草 / 字体 / 图标）都能 5 分钟内被外部 App 接入。**新颖度 4/5 / 实用性 5/5 / 可迁移性 5/5**

3. **「双形态 instruction 字段」** —— 同一条 instruction 同时存 `instructions.<lang>: string`（全文 / 适合语音朗读）和 `instruction_steps.<lang>: string[]`（数组 / 适合 UI 步骤渲染），通过确定性 split 保证一致。体积 ×2 但下游不必自己做 split。**新颖度 3/5 / 实用性 5/5 / 可迁移性 5/5**

4. **「JSON inline 单文件浏览器」** —— 把整个数据集以 JS literal 直接嵌入 14.9 MB 单 HTML（不用 fetch / IndexedDB），`file://` / 任意静态托管即开即用。**新颖度 3/5 / 实用性 4/5 / 可迁移性 3/5**（受体积上限约束）

5. **「红线分辨率媒体」** —— 媒体一律 180×180，许可证把「高于此分辨率」留给版权方授权，下游自动获得「清晰度上限」。这种处理在合规场景下非常聪明。**新颖度 4/5 / 实用性 3/5 / 可迁移性 3/5**

### 可复用的模式与技巧

- **「data/ + assets/ + index.html + setup.html」零后端静态发布模式** —— 适合任何 < 50 MB 的中小型领域数据集。
- **「AI 友好文档」模式** —— 文档页面同时承担「给人读 + 给 LLM 当上下文 + 一键复制生成后端代码」三重职能。
- **「{id}-{media_id}.{ext}」文件命名约定** —— 序号保证字典序即插入序，hash 与原数据源 ID 1-1 映射，便于增量同步与追溯。
- **JSON Schema 软扩展策略** —— `required` 限定 6 语言，但 `additionalProperties` 允许 `hi/pl/ko`，渐进式 i18n 扩张不破坏老 validator。

### 关键设计决策

| 决策 | 问题 | 方案 | Trade-off |
|---|---|---|---|
| 媒体本地化相对路径 | issue #21/#26 指向外部 CDN 401 导致 App 图挂 | `image: "images/0001-2gPfomN.jpg"` + `gif_url: "videos/...gif"` | 仓库 ~127 MB，clone 慢，换零网络依赖 |
| JSON Schema (Draft 2020-12) | 下游各写各的 TS 类型，字段漂移 | `$defs` 抽象 + `additionalProperties: false` | 发现 1 处 schema/data 不一致（6 必填 vs 9 实有，需升级 schema） |
| 双形态 instruction | UI 要全文也要步骤列表 | 全文 + 数组同时存 | 体积 ×2（gzip 后 ~3 MB，可接受） |
| `setup.html` LLM prompt | 「从数据集到生产可用 API」的最后 1 km | 6 框架 × 4 DB 笛卡尔积 prompt 模板 + 一键复制 | 模板与真实数据解耦，LLM 仍可能幻觉 |

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | exercises-dataset | yuhonas/free-exercise-db | wger | ExerciseDB ASCENDAPI |
|------|------|------|------|------|
| 形式 | 静态 JSON + HTML | 静态 JSON + Vue 站 | Django REST + YAML | SaaS API + CDN |
| 动作规模 | 1,324 | ~800 | 多模块 | 1,300+ |
| 多语言 | 9（含 zh/hi/ko/pl/tr）| 0 | 30+（社区翻译） | 1 |
| 媒体 | JPG + GIF 双轨 | 仅静态图 | 图片 | GIF/CDN |
| License | MIT + 媒体另授权 | Unlicense 公域 | AGPL | 商用付费 |
| 部署 | 零依赖 / `file://` 可开 | 零依赖 | 需 Django + 翻译 pipeline | SaaS |
| 接入时效 | 5 分钟 | 5 分钟 | 数小时 | 数分钟（按量付费） |
| 集成生态 | setup.html + LLM prompt | 多 fork 镜像 | REST + Python SDK | REST + 限流友好 |

### 差异化护城河

1. **多语言广覆盖**：9 语言 instruction 全填（包含土耳其语等新兴市场），竞品要么无 i18n 要么运维代价重。
2. **Plug-and-play 极致简单**：从 clone 到接进 App 的摩擦最低；yuhonas 要自己找 GIF，wger 要自己跑 Django。
3. **AI 友好 setup.html**：其他家都没有 ——「让 LLM 一次性产出后端」的能力对 2025 后的小团队开发很关键。
4. **LogPress 商业 App 背书**：dogfooding 证明 1,324 动作真的够撑起一个商用健身追踪 App。

### 竞争风险

- **合规争议未关闭**：issue #3「Copyright issues?」仍 open，issue #5「re-host ASCENDAPI」指控的阴影仍在。若 Gym visual 授权链条断裂，整个 media 库可能被迫下架。
- **数据量级停滞**：1,324 动作是 ASCENDAPI v1 量级（商业版 v2 已扩到数千），本项目目前依赖《gym visual / 历史 ASCENDAPI》一次性灌入，未见持续增量。
- **缺乏 CI 校验**：`.github/workflows/` 不存在，schema / 语言完整性 / 资产数量都靠人肉，1324 GIF/1324 JPG 与 JSON 100% 对应的保证无法程序化验证。
- **schema/data 不一致**：schema required 限定 6 语言（en/es/it/tr/ru/zh），数据实际有 9 语言（含 hi/pl/ko），严格 validator 会报错，需升级 schema。

### 生态定位

介于 **「yuhonas 公域简洁」** 与 **「wger 全栈重平台」** 之间的 **「中量级、多语言、开发者友好、AI 引导型」** 数据集层——最适合**想做多市场健身 App 但不想 / 不能自建后端的中小开发者**，定位为商业 App 的「数据中间件」而非「健身平台」。

## 套利机会分析

- **信息差**：合规争议未关闭 + 数据来源仍有疑问 → 任何「重新做同题材、首发即声明清楚 media 来源 + 自有授权 + schema 严格」的下场项目都有空间填充信任空白。
- **技术借鉴**：「Plug-and-play 四件套」+「AI 友好 setup.html prompt builder」是**任何 OSS 数据集都可借鉴**的最佳实践模板，比花哨的技术栈更能拿到 star。
- **生态位**：健身 App 数据层是个高频刚需、但供给稀薄（公域选项少且小、付费选项贵、重选项运维重）。这是个人开发者可以单点打穿的细分。
- **趋势判断**：本地优先（offline-first）+ 多语言本地化 + AI 辅助集成都是正确方向。但数据规模停滞 + 无版本化（无 tag/release）是隐忧，长期竞争力依赖「持续增量 + CI 校验 + 合规透明」。

## 风险与不足

- **合规透明度不足**：issue #5 的 ASCENDAPI re-host 指控在 README 中没有正面回应；`NOTICE.md` 与 `LICENSE` 切换为「© Gym visual」是聪明的合规加固，但作者未公开声明这背后的「为什么切换」，对潜在用户（尤其商用 App 团队）的尽调不友好。
- **数据来源单点**：媒体 100% 来自 Gym visual 一家授权，无冗余；若合作终止（参考 issue #33「自制内容已撤」），1,324 GIF 可能集体失效。
- **版本化缺失**：无 tag、无 release，所有下游必须 pin commit hash 才能保证确定性消费；这种 main-only 模式对想要锁定版本的企业用户不友好。
- **CDN 历史依赖未清理**：部分 issue（#21、#26）暗示 README 中仍残留指向 `static.exercisedb.dev` 等外部 CDN 的指引，本次提交虽已改为本地相对路径，可能仍有未尽。
- **schema 与 data 漂移**：JSON Schema 6 required 与实际 9 语言不匹配，严格集成方做 CI 校验时会报错。

## 行动建议

### 如果你要用它

- **接入顺序**：clone → 解压 → 把 `data/exercises.json` 灌进 DB（用 `setup.html` 生成的 SQL）→ 把 `images/` + `videos/` 放到 CDN 或对象存储 → 在 App 端按 `id` 拉取。
- **适合场景**：中小团队 / 个人开发者的多市场健身 / 训练 / 康复 App；不适合生产规模需要实时同步 / 数万动作 / 版权完备审计的大型商用项目。
- **对比决策**：要公域纯粹选 yuhonas（~800 动作、Unlicense、可商用）；要完整平台选 wger（30+ 语言、有 REST）；要 SaaS 省心选 ASCENDAPI（按量付费）；要 **多语言 + GIF + 5 分钟接入 + AI 引导** 选本项目。

### 如果你要学它

- **重点关注**：
  1. `setup.html` 的 `Ask Your LLM` prompt builder 实现 —— 这是「AI 友好文档」的范本
  2. `data/exercises.schema.json` 的 `$defs` 抽象（languageMap / languageStepsMap）
  3. `index.html` 的「单文件 inline 浏览器」思路（适合 < 50 MB 数据集）
  4. JSON 名 `attribution` 字段的「每条记录都声明来源」合规模式
- **少关注**：6 个 git commit（一次性灌入型历史没什么可学的）

### 如果你要 fork 它

- **可改进方向**：
  1. **加 CI**：用 GitHub Actions 自动校验 (a) JSON Schema 合规 (b) 语言完整性 9/9 (c) assets 数量 = json 长度 (d) `instruction_steps[lang].join(' ') == instructions[lang]` 确定性
  2. **加版本化**：用 SemVer tag（如 v1.0.0）+ GitHub Release Notes，让下游能 pin
  3. **完善 README 合规段**：在 README 头部明示「data 来源说明 + media 来源说明 + 为什么从 ASCENDAPI 时代切换到 Gym visual」，主动回应 issue #5
  4. **schema 升级**：把 `required` 从 6 语言升到 9（en/es/it/tr/ru/zh/hi/pl/ko）
  5. **动作增量 + 持续维护**：每月新增 / 替换 / 退役动作，建立 commit 模板（feature-add / data-fix / i18n-add）

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | [hasaneyldrm/exercises-dataset](https://deepwiki.com/hasaneyldrm/exercises-dataset) |
| Zread.ai | 未收录 |
| 关联论文 | 无（产品驱动数据集，非研究产出） |
| 在线 Demo | [index.html（浏览器，开箱即用）](https://raw.githubusercontent.com/hasaneyldrm/exercises-dataset/main/index.html) |
| 配套 App | [hasaneyldrm/logpress-public](https://github.com/hasaneyldrm/logpress-public)（RN 健身追踪 App 数据消费方） |

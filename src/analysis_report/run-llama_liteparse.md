# 4 个月 9.4K star 的 liteparse：TS 重写成 Rust 提速 100x，一份核心跑遍 Python/Node/浏览器

> GitHub: https://github.com/run-llama/liteparse

## 一句话总结

liteparse 是 LlamaIndex 把商业产品 LlamaParse 的核心处理逻辑开源出来的「本地轻量文档解析器」：无 LLM、无云、无 API Key，全本机把 PDF/Office/图片转成带 bounding box 的结构化文本。它 4 个月冲到 9.4K star，靠的是一次教科书级的 TypeScript→Rust 重写（小文档提速 5–100x），以及「一份 Rust 核心确定性地跑遍 Rust/Python/Node/浏览器 WASM」的工程范式。

## 值得关注的理由

1. **一份 Rust 核心跑遍四端，含浏览器内 WASM 解析（几乎无竞品）**：所有逻辑沉到一个 `liteparse` crate，三个绑定 crate（PyO3/napi-rs/wasm-bindgen）各编 `cdylib` 只做类型翻译，用 `default-features=false` + `#[cfg(target_arch="wasm32")]` 分端裁剪能力。这套「核心 crate + 多 cdylib + feature gate」是 Rust 做多语言库的范式样板。
2. **一次「带行为契约」的 TS→Rust 重写**：V1 是 TypeScript（2026-03 发布），团队 2026-05 用 Rust 完全重写为 V2，核心算法 `projection.rs` 里反复出现 `Match TS behavior` 注释——是逐函数对齐行为的高保真移植而非推倒重来。这是研究「如何安全地把一个解释型实现重写成系统语言」的活样本。
3. **一桩清晰的开源阳谋**：背靠 ~5 万 star 的母项目 llama_index，开源免费本地层做获客，README 里所有「复杂文档」出口都指向付费的 LlamaParse 云。开源的不是边角料，而是云产品的核心处理逻辑——用「核心可见」换信任，用「难场景在云端」做变现。

## 项目展示

![liteparse Hero](https://github.com/user-attachments/assets/07ba6a82-6bb1-4dea-b0ef-cad7df7d1622)

解析流水线：输入（PDF/DOCX/XLSX/PPTX/图片）→ 格式转换（LibreOffice/ImageMagick）→ PDFium 文本提取 → 按需选择性 OCR（内置 Tesseract / 可插拔 HTTP OCR）→ OCR 与原生文本合并 → Grid Projection 网格投影重建空间版面 → 输出 JSON / 纯文本 / 截图。

- 在线体验：官方 WASM 浏览器内本地解析 demo（`@llamaindex/liteparse-wasm`），可直接上传 PDF 本地解析。
- 独立背书：Simon Willison 专文 [Extract PDF text in your browser with LiteParse for the web](https://simonwillison.net/2026/Apr/23/liteparse-for-the-web/)。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/run-llama/liteparse |
| Star / Fork | 9,444 / 578 |
| 代码行数 | 17,245 行（Rust 70.3% 核心引擎 + Python 17% 绑定 + TypeScript 3.5% WASM/Web；Cargo runtime 依赖仅 5） |
| 项目年龄 | 仅 3.8 个月（2026-02-09 立项） |
| 开发阶段 | 密集开发（近 30 天 289 commit、近 90 天 567，火力越来越猛） |
| 贡献模式 | 核心少数 + 社区（28 人，Logan Markewich 约 73% commit，bus-factor 偏低） |
| 热度定位 | 大众热门（4 个月 9.4K star，爆发型早期增长） |
| 质量评级 | 代码「优」 文档「良」（CHANGELOG 过时） 测试「优」 |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

owner 是组织 run-llama（LlamaIndex，旗舰 llama_index 约 5 万 star，3905 followers）。主作者 **Logan Markewich**（LlamaIndex 创始工程师 / 开源负责人），合并两个身份约 491/675 commits（≈73%），是绝对主力；二号是 DevRel/工程团队的 Clelia (Astra) Bertelli。公司背书 + 创始工程师亲自操刀，可信度极高，已吸引外部社区 PR。

### 问题判断

问题不是凭空想的：从运营 LlamaParse 云端解析的商业经验里，团队提炼出「大量请求其实是简单文档，不值得走云端付费高精度管线」这个缺口——一个本地轻量层既能截流简单请求，又能当云端的免费引流入口。对应的市场空白是：云方案要联网+付费+延迟；重模型方案（MinerU/Marker/Docling）吃 GPU、冷启动慢；markitdown 轻但无 OCR、无空间坐标。liteparse 卡的是「速度优先、够用就好、纯本地、能跑边缘/浏览器」这个被竞品忽略的象限。

### 解法哲学

三条贯穿代码的取舍：

1. **速度优先、够用就好**：明确不拼最高精度，`projection.rs` 全是启发式（anchor 对齐 / 块分割 / flowing-text 检测）而非 ML 版面模型；
2. **难活留给云端**：README 把复杂文档（密集表格、图表、手写、扫描件）直接导流 LlamaParse，本地层故意不做表格结构化/图表理解；
3. **单核心多端**：所有逻辑沉到一个 Rust crate，绑定层只做类型翻译。明确「不做什么」：不做云、不做 LLM、不依赖任何模型权重（连 OCR 都做成可插拔，默认 Tesseract）。

### 战略意图

教科书级产品漏斗：背靠 llama_index 的品牌与流量，开源免费本地层（Apache-2.0、四端分发、甚至做成 agent skill `npx skills add`）做获客，文档里所有「复杂文档」出口都指向付费的 LlamaParse 云。开源核心逻辑换信任，难场景在云端做变现——liteparse 的战略价值大于其独立技术价值。

## 核心价值提炼

### 创新之处

1. **单 Rust 核心 → 四端绑定**（新颖度 4/5，实用性 5/5，可迁移性 5/5）：核心逻辑全在 `liteparse` crate，`liteparse-napi`(Node)/`liteparse-python`(PyO3)/`liteparse-wasm`(wasm-bindgen) 各编 `cdylib` 只翻译类型；绑定一律 `default-features=false` 关掉 Tesseract、按端重选 OCR；跨端差异用 `#[cfg(target_arch="wasm32")]` 切（wasm 无 fs/process、无内置 OCR 改 JS 回调、`web-time` 替代 `Instant`）。改一处传导四端，其中**浏览器内 WASM 解析几乎无竞品**。
2. **PDFium 运行时函数指针 FFI + 自定位原生库**（新颖度 4/5，可迁移性 5/5）：`pdfium-sys` 原生端不在编译期链接，而用 `libloading` 在运行时把所有函数指针塞进一个 struct，按 5 级路径搜 `libpdfium`（含用 `dladdr`/`GetModuleHandleExW` 找「挨着自己的原生扩展」的同目录依赖）；`pdfium` 安全层用 `PhantomData<&'page>` 把 C 指针生命周期绑回 Rust。避免了「当依赖时的 rpath 地狱」、让原生依赖可独立分发（正是 #256 痛点的应对）。
3. **选择性 OCR + 脏 PDF 防御**（新颖度 4/5，实用性 4/5）：`ocr_merge.rs` 只对「文本量<20 / 覆盖率<0.15 / 有图 / 页面乱码」的页跑 OCR（省时）；乱码检测用**元音比例启发式**——正常拉丁文元音占 30–45%，broken-cmap 替换密码会把元音映射到非元音致比例塌到个位数，低于阈值就丢弃原生文本让 OCR 接管；合并阶段还区分「系统性失败（报错）vs 偶发失败（降级继续）」。每条判断旁都有详尽的「为什么」注释。
4. **可插拔 `OcrEngine` trait**（新颖度 3/5，可迁移性 4/5）：async trait object，三实现——`TesseractOcrEngine`（内置零配置，traineddata 首用按需原子下载）、`HttpOcrEngine`（逃生舱，对接任意 EasyOCR/PaddleOCR）、`JsOcrEngine`（wasm 端桥接 JS 回调）；trait 的 `Send+Sync` 约束按 `cfg` 放宽以容纳 wasm 单线程的 `!Send` JS 类型。

### 可复用的模式与技巧

- **核心 crate + 多 cdylib 绑定 + feature gate**：Rust 多语言分发的范式样板。
- **运行时函数指针 FFI + 自定位原生库**：需分发 C/C++ 原生依赖、又怕 rpath/链接耦合的库通用。
- **先验门控 + 失败分级**：用便宜的启发式（文本量/覆盖率/元音比）决定要不要跑昂贵的 OCR，失败区分系统性/偶发——任何带可选昂贵算子的数据管线适用。
- **黄金输出回归 + 人工审批门**：`e2e-output.yml` 从 HuggingFace 拉数据集跑输出对比，变更打 label 需人工 approve——启发式输出无法用单测断言、又必须防回归的场景适用。

### 关键设计决策

最值得学的是 **Grid Projection 空间版面重建**（`projection.rs`，2879 行，全仓最大、真正的 IP）：PDFium 只给带坐标的文本碎片、没有行/列/段语义，要在不上 ML 的前提下还原版面。纯启发式流水线：过滤目录点 → 算中位字宽做尺度基准 → 处理旋转文本阅读序 → y 坐标 snap 成行 → 切块 → 每块抽 left/right/center 三类对齐 anchor 并经隔离/穿插过滤 → 区分流式正文 vs 多列表格 → 投影到等宽字符网格用空格保留对齐。一堆经验魔数（如 `FLOWING_WIDE_LINE_RATIO=0.5`）对训练分布外的版面会脆，但完全确定性、零模型、可调试、极快——是「速度优先够用就好」哲学的代码化身。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | liteparse | markitdown（微软） | Docling/Marker/MinerU | LlamaParse（自家云） |
|------|------|------|------|------|
| Stars | 9.4K（4 个月） | ~98K | ~35–66K | 闭源商业 |
| 模型依赖 | 零（可选 OCR） | 无 | 深度学习版面/表格模型 | LLM 加持 |
| OCR / bbox | 有 OCR + 逐行 bbox | 无 OCR | 有（重） | 有（高精度） |
| 多端 | Rust/Python/Node/浏览器 | Python | 偏 Python 重栈 | 云 API |
| 精度定位 | 够用就好 | 纯文本归一 | 最高精度结构化 | 最高精度 |

### 差异化护城河

四端原生（尤其浏览器内 WASM 解析几乎无竞品）+ 零模型依赖 + 逐行 bbox + 速度，占住「轻·本地·多端」这个独占象限。仓库里的 `dataset_eval_utils` 显示团队用真实基准对比 markitdown/pymupdf/pypdf/pdftotext，有实证纪律。

### 竞争风险

文档解析是红海且巨头林立（微软/IBM/大量学术项目）；精度维度打不过 ML 系，一旦小模型推理变得足够快/轻，「零模型」优势可能被侵蚀；核心算法是 V1 TS 移植而非原创，护城河更多在工程分发与品牌而非算法；此外 bus-factor 偏低（一人约 73% commit）。

### 生态定位

LlamaParse 商业漏斗的免费入口件 + LlamaIndex RAG 栈的本地预处理器——同源不同层，本地撞墙就升云，迁移成本极低（正是设计意图）。战略价值大于独立技术价值。

## 套利机会分析

- **信息差**：已被主流技术圈充分关注（Simon Willison 专文），不存在认知套利；价值在于其架构（Rust 核心 + 多语言绑定）的可复用性与「开源引流 + 云端变现」打法的可拆解性。
- **技术借鉴**：单核心多端、运行时 FFI 自定位、选择性 OCR + 失败分级、黄金输出回归门——这四个模式可直接迁移到任何 Rust 多语言库 / 带可选重算子的管线 / 难以单测断言的算法项目。
- **生态位**：填补「轻量·纯本地·多端（含浏览器）·零模型」的文档解析象限；对想做本地优先 AI 基础设施的团队是绝佳起步参考。
- **趋势判断**：踩在「Agent 需要快速本地读文档」的刚需上，且 WASM 浏览器内解析是稀缺差异化；但要警惕轻量小模型推理变快后对「零模型」卖点的侵蚀。

## 风险与不足

- **CHANGELOG 严重过时**（明显文档债）：停在 V1 的 1.5.3，仍在讲 `pdf.js`/`Tesseract.js`/`gridProjection.ts`，从未为 2.x Rust 线更新。
- **bus-factor 偏低**：Logan 一人约 73% commit，实际两人核心，关键人撤离风险高。
- **原生依赖分发是固有成本**：Rust + PDFium FFI 带来速度，代价是要为各平台逐一发布原生依赖（#256），链接错误被推迟到运行时 panic；跨平台（musl/Windows OCR）仍有多个 `logan/fix-*` 分支在打补丁。
- **精度天花板**：启发式 Grid Projection 对训练分布外的复杂版面会脆，元音乱码启发式只对拉丁文有效（CJK 直接放行）；复杂文档需升级到云端 LlamaParse——这是有意为之，但也意味着它不是「全能解析器」。

## 行动建议

- **如果你要用它**：适合「Agent/实时应用要快速本地读 PDF/Office、要 bbox 或浏览器内解析、且能接受够用精度」的场景。复杂表格/手写/扫描件高精度需求请直接用云端 LlamaParse 或 Docling/MinerU。
- **如果你要学它**：直奔 `crates/liteparse/src/projection.rs`（Grid Projection 版面重建，真正的 IP）、`crates/pdfium-sys/src/dynamic.rs`（运行时函数指针 FFI 自定位）、`crates/liteparse/src/ocr_merge.rs`（选择性 OCR + 元音乱码启发式）、以及 `liteparse-wasm`/`liteparse-python` 的绑定结构（单核心多端）。这四处是最高价值浓缩。
- **如果你要 fork 它**：先补 CHANGELOG 与 bus-factor（吸纳更多核心贡献者）；若借鉴架构，重点是「核心 crate + 多 cdylib + feature gate」与「运行时 FFI 自定位」这两套可直接复用的工程范式。

### 知识入口

| 资源 | 链接 |
|------|------|
| 官方文档 | https://developers.llamaindex.ai/liteparse/ |
| 发布博客 | [V1（本地解析 for Agent）](https://www.llamaindex.ai/blog/liteparse-local-document-parsing-for-ai-agents) / [V2（Rust 重写 runs everywhere）](https://www.llamaindex.ai/blog/liteparse-v2-0-runs-everywhere) |
| DeepWiki | https://deepwiki.com/run-llama/liteparse（已收录，含 orchestrator/PDFium 双层/grid projection/OCR trait 架构拆解） |
| 在线 Demo | 官方 WASM 浏览器内解析（`@llamaindex/liteparse-wasm`，仓库 `wasm-demo-site/`） |

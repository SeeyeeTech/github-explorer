# GitHub推荐：24×–51× token 压缩：把 200 页技术书压成 4K skill，巴西 SRE 的 Agent Skills 编译流水线

> GitHub: https://github.com/virgiliojr94/book-to-skill

## 一句话总结
book-to-skill 是 Anthropic Agent Skills 标准生态的「内容蒸馏编译器」——把任意 PDF/EPUB/DOCX/HTML 离线压成 ~4K token 的 SKILL.md + 章节文件，让 GitHub Copilot CLI / Amp / Claude Code 加载后像「随身带一本精读过的技术书」。

## 值得关注的理由
- **哲学反 RAG**：放弃运行时向量检索，改成编译时一次性蒸馏，把「加载税」从 24×–51× 压缩到 1×——首个用真实度量而非宣传口径论证的工程方案
- **Anthropic Agent Skills 标准落地第一工具**：3.8 个月 24,578 stars，GitHub Trending 总榜 #2（2026-08-23），从独立开发者小项目跃升为标准生态的事实入口
- **完整工程范式**：四层安全防御（隐形 Unicode / DOCX XXE / subprocess 注入 / 生成物扫描）、三 lens 跨 host SKILL.md 校验、CJK 章节标题 + 阿拉伯 / 罗马 / 波斯 / 韩 / 泰 五语种章节识别——一个独立开发者把「文档→agent skill」的每一道坑都填了

## 项目展示

![Booklin banner — 紫色法师举起书本洒下星点，化作有序网格的 hero 横幅](https://raw.githubusercontent.com/virgiliojr94/book-to-skill/master/docs/assets/banner.webp) — 类型：Hero 横幅

![Booklin mascot — 紫色法师 logo](https://raw.githubusercontent.com/virgiliojr94/book-to-skill/master/docs/assets/booklin.png) — 类型：Logo / 吉祥物

![Booklin celebrating — 庆祝态截图](https://raw.githubusercontent.com/virgiliojr94/book-to-skill/master/docs/assets/booklin-celebrating.png) — 类型：庆祝态截图

> 三张图片均为 Booklin 视觉资产，独立开发者少见的高品质 mascot 投入，命名在 docs、Issue、品牌间一致。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/virgiliojr94/book-to-skill |
| Star / Fork | 24,578 / 2,576 |
| 代码行数 | 6,307（Python 96.5%，TOML/YAML/HTML 各占 1%） |
| 文件数量 | 68 |
| 项目年龄 | 3.8 个月（首次提交 2026-04-30） |
| 最近推送 | 2026-08-23 |
| 开发阶段 | 密集开发（v1.4.0，3.8 月 5 发 minor） |
| 开发模式 | 职业项目（周末占比 8.4%，深夜占比 20.6%） |
| 贡献模式 | 核心少数 + 社区协作（33 位贡献者，主作者占 28.7%） |
| 热度定位 | 大众热门（GitHub Trending 总榜 #2，Trendshift Python 周榜 #2） |
| License | MIT（附 SECURITY-NOTICE.md 主动披露仿冒 fork） |
| 质量评级 | 代码 A / 文档 A+ / 测试 A / CI A / 安全 A |

## 作者视角：为什么存在这个项目

### 创始人/作者背景
Virgilio Junior（virgiliojr94），巴西 Boa Vista / Roraima（巴西亚马逊地区首府），本职 SRE 工程师服务于 @pagarme / @mundipagg / @stone-payments（巴西一线支付/金融科技公司）。9.7 年 GitHub 龄，公开仓库 51 个，**但 book-to-skill 是其绝对主力项目**（24,578 stars vs 其他最高 5 stars）——典型「本职工程经验 + 业余 AI 工具」的独立开发者路径。

SRE 训练塑造的代码品味处处体现：subprocess 调用前 `os.path.abspath` 防 `-rf` 文件名注入、临时目录 `os.chmod(0o700)` + uid 校验、Unicode 清扫走三组字符集（零宽 / Bidi / Hangul 填充符）+ Unicode tag block、CI 七 jobs 矩阵（test / lint / smoke / security / validate-skill / dependency-review / pr-template / pr-title）、Issue 修复常带「measure don't assert」原则。

### 问题判断
本职处理运行手册 + 规范 → 发现权威知识反复检索但结构散落。在 1M token context window 已经存在的时代，作者看到了别人没看到的反直觉解——**1M token 让 dump 变得可能而非便宜，recall 仍会随填充退化**。主流 workaround 全部不够用：① context dump 200K tokens 每 turn 重复计费且 「lost in the middle」；② RAG 在查询时切块→相似度→检索，是检索不是推理，与作者原意有偏差；③ NotebookLM 适合跨 80 本书横向搜索，但需要浏览器 tab 不嵌入编码流。

### 解法哲学
**Discovery Tax** 哲学：把一切导航（ToC 解析 / 章节定位 / 反向跳查）移到编译期一次性付清，运行期只加载相关切片。哲学核心：「amortization, not size」——不是让 context window 变大，而是让每次查询支付的 token 税摊薄。

### 战略意图
v1.0 → v1.4 五次 minor，迭代密度极高；用户提交 / Issue 反馈 → 量化 → 加测试 → 进入 git-cliff 生成的 CHANGELOG。已发布 SECURITY-NOTICE 主动披露仿冒 fork `Leutenegger/book-to-skill`（TLS 关闭、钱包枚举、外传），项目位列 Trendshift 排行。有 BACKERS.md 公示赞助者，但**无任何商业化 SaaS / 托管版暗示**，定位是标准生态的上游开源工具。

## 核心价值提炼

### 创新之处

1. **Discovery Tax 量化框架**（新颖度 4/5 | 实用性 5/5 | 可迁移性 4/5）
   用真实抽取书的 ToC + 章节 token 建模「agent 一次问问题的真实 cost」——`tools/discovery_tax.py` 复用 `book_to_skill.utils._chapter_number` 保证「和管道约定一致」，tiktoken cl100k_base 落地，best-case vs loop-case 双口径。**不是拍脑袋的 24×–51× 倍数，是用 Think Python / Moby-Dick / Designing Data-Intensive Applications 等真实样本跑出来的**。

2. **多语言章节标题 / ToC 检测 DAG 抽象**（新颖度 5/5 | 实用性 5/5 | 可迁移性 5/5）
   单个 utils.py 同时认阿拉伯数字 + 罗马 + 中文（第N章/第N回/第N讲/Markdown 序数）+ 泰文（บทที่ N，含 Thai 数字 U+0E50–0E59 位置映射）+ 韩文（제N장/제N편/제N절/제N관，连 `의N` 插入条款；要求 `제` 前缀防止日常计数 `장` 误命中）+ 波斯文（فصل اول / فصل بیست و یکم，PDF 粘连形态 「سی و چهارمخداحافظ…」）；CJK 码点直接对 `CJK_CHARS_PER_TOKEN` 计 token 修 ~1000× 欠估。

3. **生成 skill 的 prompt-injection 反向扫描器**（新颖度 4/5 | 实用性 5/5 | 可迁移性 5/5）
   把「提取 sanitize」与「输出扫描」共享 `is_invisible_codepoint` set 防漂移；规则集**刻意区分「delimited control token」 vs 散文**（`` 真扫，「tool call」 散文不扫以免误伤 AI 教材）——这是对 prompt injection 防御的精细化贡献。

4. **`<skill>` 跨 host 的 frontmatter 多 lens 校验**（新颖度 3/5 | 实用性 4/5 | 可迁移性 4/5）
   `claude | copilot | amp` 共享 `name`/`description`/`allowed-tools`/`license`，Amp 多接受 `compatibility`/`argument-hint`；`reserved_name_words`、`unknown_tool_severity`（Copilot 软警告=MCP 名；Claude 硬错误）、`bash_tool_names` 分化，避免「为单一 host 优化导致另一 host 静默忽略」。

5. **DOCX 不可解析前的「暴力扫 XML part 含 DOCTYPE/ENTITY」**（新颖度 3/5 | 实用性 5/5 | 可迁移性 5/5）
   `validate_docx_xml_safety()` 在 `extract_docx_with_python_docx` 与 `extract_docx_with_zipfile` 两个叶子函数入口都调用一次（避免在父函数 + 子函数重复扫），只在 `python-docx` 已安装时才扫（否则该 parser 反正不解析，扫也白扫）——**「用 ElementTree 之前先 sniff」 的样板**。

6. **publish 可见性的「bare word public」硬规则**（新颖度 3/5 | 实用性 5/5 | 可迁移性 5/5）
   仅当用户逐字回答「public」才 `--public`，句子含 「public domain」 仍 `--private`，二次确认不通过就用 private 并明示。三条版权闸门（公司内文档 ≠ 公开许可）。

### 可复用的模式与技巧

1. **策略链 + best-tool-first fallback**：每个 parser 暴露 `Trying X... OK/FAILED`，CI smoke job 强制只装 pytest 验证 zero-deps 路径——任何 CLI 工具的样板
2. **sanitize 层 + scanner 层共享同一份「invisible codepoint set」** 防漂移——避免两处分别维护各自膨胀
3. **REPL-style 大文件访问**：grep + sed 拉切片而非整文件读，对应 `Step 2.6` 提示词规约
4. **`prepare_output_dir()` 三连**：拒绝 symlink / 校验 uid / 强制 0o700——临时目录防御样板
5. **git-cliff + Conventional Commit PR title check**：`cliff.toml` 映射 `feat→Added`/`fix→Fixed` 等，CI `pr-title` job 校验正则 `^(feat|fix|perf|refactor|docs|sec|chore|ci|test|build|style|revert)(\(scope\))?!?: …`
6. **`validate_skill.py --lens`** 多 vendor 配置矩阵，单一脚本编码差异
7. **`chapters_method` 显式标注 numeric vs structural**：检测路径分歧时把「谁答的」记到 metadata，防 silent disagreement

### 关键设计决策

```
决策: 两段式流水线（确定性 Python 抽取 + LLM 驱动生成）
问题: 单一 LLM 调用直接读 200 页 PDF 不可靠且贵
方案: 先把 PDF/EPUB/DOCX/HTML/RTF/MOBI 通过确定性工具抽出 full_text.txt + metadata.json，
      再让 agent 按 SKILL.md 规约产出 SKILL.md / chapters / glossary / patterns / cheatsheet
Trade-off: 抽取层必须为多格式多语言做大量工程，组件多但可观测；生成层质量依赖模型
可迁移性: 高（任何「文档→结构化知识」的工作流都可套此骨架）
```

```
决策: 编译时 vs 检索时的工程取舍
问题: RAG 每次查询都付检索税，dump 每次 turn 都付加载税
方案: SKILL.md 常驻 ≈4K tokens，按需 chapters/chNN-*.md ≈1K tokens；
      frontmatter description 浓缩 3–6 个主题词，让 agent 不必读全文就能路由到对应章节
Trade-off: 生成一次 ≈$1/本（实测 Think Python $0.88 / Moby-Dick $1.42），
          但所有未来会话永远只付 ~5K token
可迁移性: 高（「domain knowledge compilation」模式可套所有重复查询域）
```

```
决策: 安全分层加固（document → context supply chain）
问题: 恶意文档可通过不可见 Unicode / XXE / 隐形 tag block 把 prompt 注入塞进生成 skill，
      再传播给下游 agent
方案:
  - sanitize.py 一次性剔除 12 个零宽码点 + 11 个 Bidi 控制字符（CVE-2021-42574 Trojan Source）
    + 4 个 Hangul 填充符 + Unicode tag block U+E0000–E+E007F，空文档则 reject
  - DOCX parser 对每个 XML part 扫 <!DOCTYPE/<!ENTITY 再解析（XXE + Billion Laughs 防御）
  - subprocess 调用前 os.path.abspath 路径，杜绝 -rf 文件名注入
  - tools/scan_generated_skill.py 在 Step 9.5 扫描生成产物：prompt-override 短语 / 
    [INST] 模板 token / tool_call 控制符 / frontmatter 越权声明 / 外泄特征
  - 工作目录 prepare_output_dir() 校验 symlink + 跨用户 uid + 强制 0o700
Trade-off: sanitize 偶发误伤合规 RTL 排版；扫描器规则面广可能误报 AI/LLM 教材
          （代码中故意区分了 tool_call 的「delimited form」 vs 散文）
可迁移性: 高（任何接受不可信输入的 agent/RAG 工具都需要这套 4 层）
```

```
决策: 格式策略模式 + 多级 fallback（策略链）
问题: 不同 OS / 不同依赖环境无法保证同一工具可用
方案: 每种格式有 ordered 探测链：
      PDF: pdftotext → pypdf → pdfminer.six → Docling
      EPUB: ebooklib+bs4 → stdlib zipfile
      DOCX: python-docx → stdlib zipfile/XML
      HTML: trafilatura → bs4 → stdlib html.parser
      RTF: striprtf → stdlib regex
      MOBI: Calibre ebook-convert（无 fallback）
      每步都有 print("Trying X..." OK/FAILED) 暴露真相
Trade-off: base install 零依赖（pyproject [project.optional-dependencies] 列 6 个 extras），
          高级质量按需安装；CI smoke job 强制只装 pytest 验证 zero-deps 路径
可迁移性: 高（任何 CLI 工具的样板）
```

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | book-to-skill | Futurehouse book-ai | anthropics/skills | NotebookLM |
|------|-------------|--------------------|--------------------|------------|
| 运行模式 | 本地离线 / 跨 4 host | SaaS 托管端到端 | 协议 + 官方示例 | 闭源 Web |
| 输出格式 | Anthropic Agent Skills 标准 | fine-tuned skill agent | SKILL.md 模板 | chat with book |
| 文档格式覆盖 | 7 种（PDF/EPUB/DOCX/HTML/RTF/MOBI/纯文本） | 主要 PDF | 无关（手动写） | PDF/Google Docs |
| Token 优化 | 24×–51× 实测量化 | 训练时压缩 | 无关 | 黑盒 |
| 安全防御 | 四层（sanitize/XXE/subprocess/scanner） | 不可知 | 无关 | 不可知 |
| 多语种章节识别 | 5 种（阿拉伯/罗马/中文/泰/韩/波斯） | 主要英语 | 无关 | 无关 |
| 商业化 | 无 | SaaS 收费 | 官方支持 | Google 闭源 |
| Stars | 24.5K | 低（学术） | 17.1 万（母体） | 不可比 |

### 差异化护城河
- **编译时哲学 + 量化证据**：首个用真实度量论证而非宣传口径
- **多格式 + 多语种 + 多 host 的三角兼容矩阵**：任何单点切入都需同时攻破
- **安全分层（四层独立防御）**：竞品大多黑盒，book-to-skill 把每一层都开源
- **测量驱动开发**：`tools/discovery_tax.py` + `--check` + 每 PR 必带 evidence 闸门

### 竞争风险
- **最可能被替代**：Anthropic 官方若推出「PDF/Skill」内建能力，book-to-skill 核心卖点会被吞
- **上游风险**：Docling / PyMuPDF 等上游库的 breaking change 需快速跟进
- **IP 风险**：仿冒 fork 已发生（Leutenegger/book-to-skill），需 SECURITY-NOTICE 主动响应

### 生态定位
Anthropic Agent Skills 标准生态的「上游内容生产工具」：
- 与 **anthropics/skills** 是**互补**（book-to-skill 生成 artifact，anthropics/skills 定义协议）——用户手写 skill → 加载；book-to-skill 把书转成同格式 skill。两者是**上下游**关系而非竞争。
- 与 **RAG** 是**互补**（编译时结构 vs 运行时检索）
- 与 **NotebookLM** 是**互补**（深读一本书 vs 横扫一批）
- 填补的空白：「Agent Skills 标准已定，谁来生产内容？」

## 套利机会分析
- **信息差**: 低关注度已被打破（24.5K stars + Trending #2），但**价值密度高**——24×–51× 压缩 + 5 语种章节识别 + 四层安全这些技术细节仍少有人拆解
- **技术借鉴**: 可迁移的资产最值钱的：①「策略链 + fallback + --check」三件套模式 ② 四层安全 sanitize 模板 ③ `tools/discovery_tax.py` 的测量驱动开发范式 ④ 跨 host SKILL.md 的多 lens 校验思路（可移植到任何 open-standard 多 vendor 实现，如 OpenAPI / AsyncAPI / MCP）
- **生态位**: 在「Agent Skills 标准已定后的最后一公里」占住身位，与 anthropics/skills 形成上下游互补而非直接竞争
- **趋势判断**: 在增长（GitHub Trending #2 + 周榜 #6 + 周 commit 数 50+），符合「agent 工具链最后一公里」的技术趋势，比 Futurehouse book-ai（学术路线）和 NotebookLM（闭源路线）有后发优势

## 风险与不足
- **Issue #169 自审**：自家 SKILL.md 7K tokens、52% 在跑前加载——**蒸馏哲学本身在被自己质疑**，是后续迭代核心张力点
- **Issue #128 PDF 多列文档**：`pdftotext -layout` 串列 + 词估算隐藏 26× 体积膨胀——PDF 多栏场景仍未根治
- **Issue #127 EPUB 静默丢图**：抽取完整性有缺口
- **仿冒警告**（Issue #174）：`Leutenegger/book-to-skill` 已出现，需要持续 SECURITY-NOTICE 主动披露
- **核心少数 + 社区协作**：主作者占 28.7%，Top 2 合计 55.4%（疑似双账号），单点风险存在
- **依赖膨胀**：35 个 runtime 依赖，靠 6 个 extras + CI smoke zero-deps 路径缓解，但安装体验仍重

## 行动建议
- **如果你要用它**：直接装 → `npx skills add virgiliojr94/book-to-skill` 或 `pip install book-to-skill`。**适合**：反复重读同一本书 / 同一份内网规范 / 同一组 RFC+笔记的工程师 / SRE / 研究者。**不适合**：只想 chat with PDF 一次性的用户（用 NotebookLM）。
- **如果你要学它**：必读三个文件：① `book_to_skill/utils.py`（1130 行核心，章节检测 / 多语种 regex / token 估算 / 安全 sanitize 编排）② `tools/discovery_tax.py`（ROI 量化范式）③ `tools/scan_generated_skill.py`（生成物扫描器，prompt injection 防御样板）。次读 `book_to_skill/sanitize.py` 和 `book_to_skill/parsers/pdf.py`。
- **如果你要 fork 它**：可改进方向——① PDF 多列文档的 layout-aware 解析（解决 #128）② EPUB 图像抽取完整性（解决 #127）③ 自家 SKILL.md 的描述前置 prompt 压缩（解决 #169）④ `tools/discovery_tax.py` 的图表化（缺一张 24×→51× 的可视化对照表）⑤ 加 web UI（Issue #10 hosted demo 已被关，需求存在）。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录（403 拒但已被搜索引擎索引） |
| Zread.ai | https://zread.ai/virgiliojr94/book-to-skill（已收录，架构摘要完整） |
| Trendshift | https://trendshift.io/repositories/27038（日榜/周榜轨迹） |
| 关联论文 | 无（工程实践项目，非学术衍生） |
| 在线 Demo | 无独立 hosted demo（Issue #10 提案已关，需本地跑） |
| 用例库 | https://github.com/virgiliojr94/book-to-skill-use-cases（5 stars） |
| 衍生项目 | video-to-skill（受 book-to-skill 启发，Issue #87） |
| SECURITY-NOTICE | https://github.com/virgiliojr94/book-to-skill/blob/master/SECURITY-NOTICE.md（主动披露仿冒 fork） |
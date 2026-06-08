# 719 行代码还原马赛克，作者却清零 2.6 万 star

> GitHub: https://github.com/spipm/Depixelization_poc

## 一句话总结

荷兰安全顾问 Sipke Mellema 用 719 行 Python 写出的取证 PoC「Depix」——它能从像素化（马赛克）打码的截图中**确定性还原出原始明文**，亲手证明了「马赛克/模糊打码根本不安全」这条至今被反复引用的安全常识。

## 值得关注的理由

- **极小代码量 × 极高文化影响力的稀有标本**：仅 719 行 Python（核心算法 `functions.py` 一个文件占 60%），却是几乎所有「不要用马赛克给密码打码」科普的引用源头。2020 年底发布后在 HackerNews / GIGAZINE / The Register / Bleeping Computer 广泛报道，历史 star 峰值曾达 **26152**。
- **罕见的「主动拒绝虚名」叙事**：2024 年底作者把仓库转私有 → 改名 `Depix`→`Depixelization_poc` → 重新公开，**故意丢弃了那 26152 个炒作堆出来的 star**——理由是「It didn't feel right…如果我再次获得这么多 star，我希望它是为我真正引以为傲的项目」。现在的 4529 star 是重置后重新积累的。
- **一条能立刻用上的防御教训**：像素化、高斯模糊、旋转都是**可逆的确定性变换**，给敏感文本「打码」时它们形同虚设；唯一安全的做法是彻底删除或纯黑实心块覆盖。这是每个做截图、写文档、发漏洞报告的人都该记住的。

## 项目展示

![Depix 还原效果总览](https://raw.githubusercontent.com/spipm/Depixelization_poc/main/docs/img/Recovering_prototype_latest.png)

最具代表性的「打码 → 还原」对照图，也是当年媒体传播的主图。

![多词文本去像素化结果](https://raw.githubusercontent.com/spipm/Depixelization_poc/main/docs/img/example_output_multiword.png)

对一整段被像素化的等宽字体文本的还原输出。

![线性盒式滤波原理示意](https://raw.githubusercontent.com/spipm/Depixelization_poc/main/docs/img/linear_box_filter_example.png)

解释算法可逆性的关键原理图：像素化本质是对原始小块取颜色均值，而均值是强约束的多对一映射。

![26152 star 截图（作者清零前留念）](https://raw.githubusercontent.com/spipm/Depixelization_poc/main/images/stars.png)

作者主动清零前为这 26152 个 star 留下的截图——佐证其真实历史热度。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/spipm/Depixelization_poc |
| Star / Fork | 4529 / 365（当前；历史峰值曾达 26152，被作者主动清零重置） |
| 代码行数 | 719（Python 100%，9 个 .py 文件；运行时仅依赖 Pillow，余为标准库） |
| 项目年龄 | 66 个月（约 5.5 年，2020-12 起） |
| 开发阶段 | 低维护 / 已封存（GitHub 仓库 archived 只读，主仓库已迁往 Codeberg） |
| 贡献模式 | 独立开发（原作者 beurtschipper 即 spipm 本人，git 口径占 32.7%；社区贡献 linear 均值修正等精度改进） |
| 热度定位 | 数字上中等热度，文化影响力实为大众热门（两者背离是本项目最大特点） |
| 质量评级 | 代码[良好·小而精] 文档[优·文档驱动] 测试[无·靠样张人工验证] |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

作者真实身份是 **Sipke Mellema**，荷兰信息安全顾问。GitHub 早期用户名 `beurtschipper`（荷兰语「驳船船长」），现用 `spipm`（"**S**i**p**ke **M**ellema" 缩写）——两者是同一人，证据是 `github.com/beurtschipper/Depix` 已 301 重定向到本仓库、README 第一人称自述、git 历史两个作者名连续衔接。他是攻防/取证方向的独立研究者，仓库矩阵清一色安全向（`crackcoin` 钱包密码爆破、`Dutch-Password-List`、`pentest-report-guide`、CTF 题解），blog 在 spipm.graa.nl。这种背景决定了 Depix 的气质：**把一个安全常识做成有传播力的硬核 PoC**。

### 问题判断

Depix 的起点是一次真实工作：作者自述「当年为某公司做的快速 PoC——因为有人把一个拥有域管理员权限账户的密码只做了像素化打码」。他看到的是一个被普遍误解的安全盲区——**大量人以为「打码 = 安全」，却不知道像素化是确定性、可逆的**。学术界早在 2016 年的论文《On the Ineffectiveness of Mosaicing and Blurring as Tools for Document Redaction》就指出过这点，但没有公开、可复现的工具把它「演示」给大众看。Depix 补的正是这个缺口：把抽象的密码学常识变成「你亲眼看到密码被还原」的冲击力。

### 解法哲学

- **明确选择「能直接 `python3` 跑的脚本，胜过 pip 包」**：作者 2023 年主动移除了第三方贡献的打包配置，回归「just scripts I can run」。
- **明确选择诚实坦率**：README 的「Known limitations」老实列出三条硬约束（假设整数块边界、需已知字体/屏幕设置、二次压缩破坏色值即失效），不夸大战果。
- **罕见的「主动拒绝虚名」**：为不被 26152 个炒作 star 绑架，手动清零重置——这在 GitHub 生态里几乎是反直觉的价值观表达。

### 战略意图

这不是一个要长期产品化的项目，而是一件「**目的达成即封存**」的研究作品。它的真正「产品」不是代码，而是「像素化不安全」这条被它推向大众的安全教训。无商业化路径，无版本发布，归档后迁往 Codeberg 作为存档。它在作者的攻防/取证仓库矩阵中是影响力最高、最具符号意义的一件。

## 核心价值提炼

### 创新之处

1. **用 De Bruijn 序列搜索图把「破马赛克」变成确定性查表**（核心洞见）：核心思想是「线性盒式模糊是逐块独立的确定性均值运算」，因此对**已知字体 + 已知像素化网格**，可把每个像素块的均值当「指纹」反查。搜索图是用同款编辑器/字号/像素化参数渲染并打码的 De Bruijn 序列文本——De Bruijn 序列保证每段相邻字符组合唯一出现，等于给搜索空间铺了一张「全覆盖且无歧义」的查找表。
2. **几何/邻接约束传播消歧**：唯一命中的块是「确定锚点」，多命中的块借助邻居——若某锚点的某邻居在搜索图里保持相同相对位移，就锁定该邻居的正确候选。这是一种约束传播，把确定性从无歧义块沿四邻扩散到有歧义块（连跑两遍 pass 滚雪球）。
3. **物理正确的线性光均值**：除朴素 gamma 校正均值外，提供 `linear` 模式（先 `srgb2lin` 转线性光再平均、再 `lin2srgb` 转回）——由社区 PR#45 贡献，显著提升匹配精度。

### 可复用的模式与技巧

1. **「把逆问题转化为带唯一性保证的查表」**：用 De Bruijn 序列构造无歧义搜索空间——适用于任何「已知正向变换、求逆」且变换为多对一的场景。
2. **约束传播消歧**：从确定锚点沿邻接关系扩散确定性，是 OCR / 拼图 / 序列对齐类问题的通用套路。
3. **批量像素读取优化**：`getdata()` 一次性取像素而非逐点 `getpixel()`——图像处理的基础性能技巧。
4. **诚实的不确定性可视化**：单命中块直接还原、仍歧义的块取候选均值留一团模糊——**用输出本身标示「这里无法判定」**，而非强行给出可能错误的答案。

### 关键设计决策

- **要求「同编辑器/同字体/同参数」的精确均值相等（而非最近邻匹配）**：这是 Depix 既强（在满足前提时确定性还原）又脆（前提不满足即失效）的根源。作者选择「严格但诚实」而非「宽松但容易出错」，符合取证工具的可信度要求。
- **不做模型、不做训练**：纯确定性算法、无机器学习——可解释、可复现、零依赖训练数据，这也是它区别于后来神经网络方案（Bishop Fox Unredacter）的本质。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | Depix | Bishop Fox Unredacter | DepixHMM | KoKuToru/de-pixelate |
|------|-------|------------------------|----------|----------------------|
| 方法 | 确定性均值反查 + De Bruijn 搜索图 | 神经网络 | HMM（2016 论文实现） | TensorFlow，利用帧间信息 |
| 适用对象 | 等宽字体静态截图 | 单字体，含变宽/渗色场景 | 跨多字体 | **动态视频/动图** |
| 鲁棒性 | 对变宽字体/像素偏移脆弱 | 更鲁棒（解决 Depix 的失败场景） | 跨字体精度更高 | 专攻运动图像 |
| 可解释性 | 高（纯算法、可复现） | 低（需训练） | 中 | 低 |
| 知名度 | 开山之作、最知名 | 高（约 1.4k star） | 小众 | 小众 |

### 差异化护城河

Depix 的护城河是**「开创性符号地位」**——它是文本去打码取证这一细分的事实起点与最知名者，几乎所有后来者都以「改进或反驳 Depix」自我定位（Unredacter 明确说自己是「Depix 的改进与批评」，DepixHMM / de-pixelate 在 README 里亲自致谢 Depix）。这种「被整个细分领域当参照系」的地位，比代码本身更难复制。

### 竞争风险

就「还原能力」而言，**Bishop Fox Unredacter 已在技术上超越它**——Unredacter 用神经网络解决了 Depix 在变宽字体、字符渗色、像素偏移上的失败场景，并证明「即便 Depix 失败的场景，像素化仍不安全」，把结论从个例上升为普适。但这不威胁 Depix 的历史地位：Depix 要的是「证明 + 传播」，这个目标早已达成。

### 生态定位

它是「去打码取证」细分蓝海的开山符号，也是「像素化≠安全打码」这条安全常识的标志性载体。在更大的图景里,它填补了「把抽象密码学常识变成大众可见的冲击性演示」这一空白。

## 套利机会分析

- **信息差**：典型「被数字低估、被文化高估」——facts 的「中等热度」只反映作者人为重置后的 4529 star，真实历史影响力是大众热门级（峰值 26152 star + 全球媒体报道）。对内容创作而言是「数字不起眼但传播价值极高」的上选选题，叙事张力强（清零 26k star 的故事 + 硬核安全常识双钩子）。
- **技术借鉴**：「De Bruijn 序列构造无歧义搜索空间」「约束传播消歧」「诚实可视化不确定性」三套思路，可迁移到 OCR、逆向、图像取证等场景。
- **生态位**：去打码取证玩家极少，Depix 是事实起点；任何想科普「打码安全」的内容都绕不开它。
- **趋势判断**：已归档只读、近一年 0 代码维护，却仍稳步涨 star（近 75 天采样 129 个新 star）——经典安全工具的常青长尾，靠「像素化不安全」这一持续被引用的常识自然引流。

## 风险与不足

- **实战可用性有限**：JumpSec Labs 实测质疑其在真实场景的成功率（这一质疑正是催生 Bishop Fox Unredacter 挑战赛的导火索）。Depix 严格依赖「等宽字体 + 已知像素化参数 + 无二次压缩」三大前提，现实截图常不满足。
- **已封存、不再迭代**：GitHub 仓库 archived 只读，主仓库迁往 Codeberg；想要更强能力应转向 Unredacter 等后继。
- **无测试、无版本**：质量靠样张人工验证，无单测、无 tag/release——符合 PoC 定位但不适合直接生产依赖。
- **License 为自定义「Other」**：未采用标准 SPDX 协议，商用/二次分发前需自行确认授权条款。

## 行动建议

- **如果你要用它**：你想**演示/教学「马赛克打码不安全」**，或对一张满足前提（等宽字体、已知编辑器像素化参数、无二次压缩）的截图做取证还原——用它，零依赖、可解释、可复现。若目标截图字体变宽、有渗色或像素偏移，改用 Bishop Fox Unredacter。
- **如果你要学它**：精读 `depixlib/functions.py`（算法心脏，436 行，含均值反查 `findRectangleMatches` + 几何消歧 `findGeometricMatchesForSingleResults`）、`depix.py`（CLI 与两遍 pass 流水线编排）、`LoadedImage.py`（批量像素读取优化），并读 README 的「Known limitations」理解算法边界。
- **如果你要 fork 它**：最有价值的方向是**放宽「精确均值相等」的硬约束**（容忍轻微压缩噪声、支持变宽字体），或把它的确定性思路与 Unredacter 的神经网络思路结合——这正是该细分仍未被彻底攻克的部分。

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | https://deepwiki.com/spipm/Depixelization_poc （已收录，含架构/算法/CLI 章节） |
| Zread.ai | 未确认（请求返回 403） |
| 关联论文 | 《On the Ineffectiveness of Mosaicing and Blurring as Tools for Document Redaction》（2016，作者亲自引用为先行研究；非 arXiv） |
| 在线 Demo | 无官方 Demo；第三方 PyPI 包 [`depix`](https://pypi.org/project/depix/)（非作者维护）可 pip 安装本地运行 |
| 延伸阅读 | [Bishop Fox — Never Use Text Pixelation To Redact Sensitive Information / Unredacter](https://bishopfox.com/blog/unredacter-tool-never-pixelation) |

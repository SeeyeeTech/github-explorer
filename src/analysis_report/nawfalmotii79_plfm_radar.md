# GitHub 推荐：25.8k stars 的 10.5GHz 相控阵雷达：6 个月一个人把全套 BOM 摆上 GitHub

> GitHub: https://github.com/nawfalmotii79/plfm_radar

## 一句话总结
摩洛哥工程师 Nawfal Motii 用 6.7 个月把一套 10.5 GHz LFM 相控阵雷达的全栈硬件（原理图/PCB/BOM/Verilog/STM32/Python GUI）从零做到 25.8k stars，是**高频段长距雷达全栈开源几乎独占的生态位填补者**。

## 值得关注的理由
- **稀缺频段 + 全栈交付**：10.5 GHz 相控阵 + 双版本（3 km patch / 20 km GaN 波导）+ Gerber/BOM/FPGA Verilog/STM32/Python GUI 全开源，全球同类项目里几乎无直接竞品，最近的商业对应是 Analog Devices CN0566（仅 2-6 GHz、近场）。
- **形式化验证开路**：`formal/` 子目录跑 SymbiYosky 形式化验证 5 个模块 + 四层测试栈（unit/integration/HIL/MATLAB co-sim），在开源硬件里属于罕见工程化深度。
- **从开源到公司的样本**：作者已自建 ABAC INDUSTRY、与 PCBWay 合作换物，是少有的「作品吸引流量、运营几乎为零」（Following 仅 7）反向路径——值得拆解。

## 项目展示

### README 媒体
1. ![AERIS-10 Antenna Array](https://raw.githubusercontent.com/nawfalmotii79/plfm_radar/main/8_Utils/Antenna_Array.jpg) — 类型： hero（8×16 天线阵主视觉）
2. ![AERIS-10 System Diagram](https://raw.githubusercontent.com/nawfalmotii79/plfm_radar/main/8_Utils/RADAR_V6_V2.png) — 类型： architecture（系统框图）
3. ![AERIS-10 Dashboard](https://raw.githubusercontent.com/nawfalmotii79/plfm_radar/main/8_Utils/GUI_V6.gif) — 类型： demo（Python GUI 实时显示）
4. ![PCBWay Sponsor Logo](https://raw.githubusercontent.com/nawfalmotii79/plfm_radar/main/8_Utils/PCBWAY.jpg) — 类型： 赞助商鸣谢

### 筛选说明
- 总共发现 15 个媒体元素，筛选后保留 4 个核心展示
- 排除了 PCB 实物照片、Gerber 预览、波形截图等次级素材

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/nawfalmotii79/plfm_radar |
| Star / Fork | 25,793 / 5,887 |
| Watchers / Open Issues-PRs | 24 / 8-7 |
| 代码行数 | ~80k 行可读代码（tokei 报告 397,761 行的 79.6% 为 FPGA bitstream HEX） |
| 主语言 | Verilog (FPGA) + C/C++ (STM32) + Python (GUI) + Altium Designer/KiCad （硬件） |
| 项目年龄 | 6.7 个月（首次提交 2026-03-08） |
| 总 commit | 348 |
| 开发阶段 | 低维护（最近 3.5 个月零提交） |
| 开发模式 | 业余 Side Project（周末 12.9%、夜间 52%） |
| 贡献模式 | 小团队核心（Top 2 占比 ~88%，主作者 JJassonn69 55.8% + NawfalMotii79 32.5%） |
| 热度定位 | 大众热门（25.8k stars / 6.7 个月） |
| 许可证 | 硬件 CERN-OHL-P v2 + 软件/固件 MIT（双许可） |
| Fork/Star 比 | 22.8%（远高于平均 5-10%，硬件复刻典型特征） |
| 质量评级 | 代码 A- / 文档 A / 测试 B+（含形式化验证 + 四层测试栈） |

## 作者视角：为什么存在这个项目

### 创始人/作者背景
**Nawfal Motii**，摩洛哥卡萨布兰卡，ABAC INDUSTRY 创始人。账号注册 1.3 年，仅本仓库 1 个公开 repo —— 全部产能与品牌资产押在一个产品。仓库 README 自述项目「started in a small workshop in Morocco」（在摩洛哥一个小车间里起步）。粉丝 945 但 Following 仅 7 —— 典型「作品吸引流量、运营几乎为零」的反向路径。

### 问题判断
商用相控阵雷达开发板（如 Analog Devices CN0566）只在 2-6 GHz 近场，且需 Pluto SDR 等外部配套；2.4/24 GHz FMCW 开源方案又是短距（<300 m）。10.5 GHz 频段、3-20 km 距离、双版本（patch + GaN）的开源相控阵雷达，**在 GitHub 上几乎空白** —— 这是作者看到的真实生态空白。Issue #97 直接问「是要开公司吗？」被关闭，作者以 ABAC INDUSTRY 命名实体 —— 商业化意图从一开始就是明确的。

### 解法哲学
**「用 ADI 商用现货搭积木，把 BOM 全部开放」**：
- ADAR1000×4（相控阵核心）+ ADF4382×2（频率合成）+ AD9523-1（时钟）+ LTC5552×2（混频器）+ ADTR1107×16（驱动）+ QPA2962×16（GaN PA）—— 整套 ADI 推荐相控阵参考设计同款芯片
- 配合 Xilinx XC7A50T FPGA（Verilog 处理）+ STM32F7（波束/接口管理）+ Altium Designer/KiCad（原理图）
- 选型哲学：全部用商用现货 + 文档齐备的型号，便于读者复刻/采购

**作者明确不做什么**：
- 不做云端 SaaS：GUI 是桌面 Python，没有云/远程服务架构
- 不做闭源：连 FPGA bitstream 都开源（HEX 占了 316k 行）
- 不做「商业版 + 开源版」分层：单本、单版本合一，只在双型号（Nexus/Extended）做硬件差异

### 战略意图
商业化路径已通：
1. **从开源到公司**：ABAC INDUSTRY 已在卡萨布兰卡登记
2. **从代码到流量**：25.8k stars + 5.9k forks 是直接背书
3. **从产品到变现**：与 PCBWay 合作换打样 + 通过 GitHub Pages 文档站沉淀「开箱即用的雷达 BOM 说明书」
4. **战略开放**：双许可（CERN-OHL-P + MIT）让读者既能学习也能复刻，是 geniune open（非 open-core）

Issue #150（Tests in Morocco）作者计划在本地做外场测试，验证 20 km GaN 版的实际探测距离 —— 商业化的最后一块拼图。

## 核心价值提炼

### 创新之处
按新颖度×实用性排序：

1. **三层混合 AGC 架构**（FPGA 内环 + STM32 外环 + GUI 顶端 host commands）
   - FPGA `rx_gain_control.v` per-sample shift+saturate 内环（μs 级响应）
   - STM32 `ADAR1000_AGC.cpp` per-frame 调 VGA gain（ms 级响应）
   - GUI `set_agc_*` opcode 0x28-0x2C 手动覆写
   - 握手：FPGA → DIG_5 GPIO → STM32 read → 调 ADAR1000 gain
   - 评分：新颖度 4/5 + 实用性 4/5 + 可迁移性 4/5

2. **双段 staggered-PRI Doppler**（教科书 + 工程化结合）
   - 32 chirps 切成 16 long-PRI + 16 short-PRI 各自 16-pt FFT
   - 注释明确写「single 32-pt FFT over non-uniformly sampled frame is signal-processing invalid」
   - `doppler_processor_optimized.v` 是当代实现，注释清晰
   - 评分：新颖度 3/5 + 实用性 5/5 + 可迁移性 5/5

3. **跨时钟域形式化验证**（开源硬件罕见）
   - `cdc_modules.v` 用 Gray-code + toggle CDC 跨 100/120/160/400MHz 四域
   - `formal/` 跑 SymbiYosky 形式化验证 5 个模块
   - `ASYNC_REG = "TRUE"` 显式约束 Vivado 布局
   - 评分：新颖度 4/5 + 实用性 3/5 + 可迁移性 4/5

4. **双版本硬件模块化**（3km patch / 20km GaN 波导）
   - 差异集中在 PA 子板，其余（FPGA/STM32/ADAR1000/ADF4382）完全共用
   - 通过 `PowerAmplifier` 宏 + DAC5578/ADS7830 抽象做到上层透明
   - 评分：新颖度 3/5 + 实用性 4/5 + 可迁移性 4/5

5. **bit-accurate 软件 FPGA**（闭环验证）
   - `9_Firmware/9_3_GUI/v7/software_fpga.py` 把 FPGA 关键模块在 Python 复刻
   - `adi_agc_analysis.py` 用真实数据闭环验证
   - 评分：新颖度 4/5 + 实用性 3/5 + 可迁移性 3/5

### 可复用的模式与技巧

1. **三层 AGC 分层**：内环 μs + 外环 ms + 顶层 host —— 任何 RF/通信接收机都可借鉴
3. **staggered-PRI 解决多普勒模糊**：雷达信号处理的标准做法，但代码注释把「为什么不能合并为均匀采样 FFT」写得很清楚 —— 工程文档范例
4. **硬件宏做版本抽象**：`PowerAmplifier` 宏 + 子板模块化，让双版本/多版本雷达平台可以共用 80% 固件
5. **形式化验证嵌入开源硬件**：`formal/` 子目录 + SymbiYosky，证明 CDC 安全 —— 值得其他 Verilog 开源项目借鉴
6. **bit-accurate 软件镜像**：把 FPGA 关键数据通路用 Python 复刻，便于单元测试与回归

### 关键设计决策

**决策 1：FPGA + MCU + RF 分层**
- 问题：相控阵雷达需要 μs 级波束切换 + ms 级波束管理 + Hz 级 GUI 控制 —— 单层控制器无法兼顾
- 方案：Xilinx XC7A50T FPGA 处理 chirp + Doppler FFT + 内环 AGC；STM32F7 管波束扫描序列 + 外环 AGC + 接口；Python GUI 管人机交互
- Trade-off：牺牲单芯片简洁度，换来三层响应速度分层清晰 + 故障域隔离
- 可迁移性：高）

**决策 2：ADI 商用现货全栈**
- 问题：自研 RF 芯片需要流片周期 + 巨额资金
- 方案：ADAR1000 + ADF4382 + AD9523-1 + LTC5552 + ADTR1107 + QPA2962 全部 ADI 现货
- Trade-off：牺牲频段/功率的极致定制（BOM 限死 10.5 GHz），换读者可直接采购复刻 + 文档齐备
- 可迁移性：中（依赖 ADI 供应链，但思路通用）

**决策 3：双版本硬件（Nexus 3km / Extended 20km）**
- 问题：3 km 探测和 20 km 探测对 PA 需求差一个数量级
- 方案：差异集中在 PA 子板（patch vs GaN 波导），其余完全共用
- Trade-off：牺牲单板最优（PA 子板规格不同），换「一套代码双用途」
- 可迁移性：高（多版本硬件平台通用做法）

**决策 4：HEX bitstream 也开源**
- 问题：开源 Verilog 但闭源 bitstream 等于半开源
- 方案：连 `*.bit` 的 HEX 都 commit（占代码行数 79.6%）
- Trade-off：牺牲仓库体积（~132 MB）+ 加大 clone 时间，换真正的「开箱即用」
- 可迁移性：低（特定上下文决策）

**决策 5：双许可而非单一**
- 问题：硬件 CERN-OHL-P（鼓励衍生）+ 软件 MIT（最宽松）需要不同 license
- 方案：硬件 CERN-OHL-P v2 + 软件/固件 MIT（社区成员 gmaynez 建议切换）
- Trade-off：牺牲统一 license 简洁度，换读者清晰分场景授权
- 可迁移性：高（硬件开源项目的标准做法）

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | AERIS-10（本项目） | Analog Devices CN0566 | tiny-radar (westonb) | FMCW_RADAR (Elrori) |
|------|---------|--------|--------|--------|
| 频段 | 10.5 GHz LFM | 2-6 GHz | 2.4 GHz FMCW | 24 GHz FMCW |
| 距离 | 3-20 km 双版本 | 近场 | 短距 | ~250 m |
| 架构 | 相控阵 + 机械扫描 | 8 通道相控阵 | USB FMCW | 单板 FMCW |
| FPGA | Xilinx XC7A50T | Pluto SDR | 无（STM32） | Artix-7 Verilog |
| MCU | STM32F7 | Pluto 内置 | STM32 | 无 |
| GUI | Python 桌面 | Python/MATLAB lab | Python | 无 |
| Stars | 25.8k | n/a（商业教育套件） | 22 | n/a |
| 完整 BOM 开源 | ✓ | ✗（商业） | ✓ | ✓ |

### 差异化护城河
- **频段独占**：10.5 GHz 频段、3-20 km 距离、双版本开源相控阵雷达 —— 这是仓库真正「独占」的领域
- **全栈交付**：唯一把 Gerber/BOM/FPGA Verilog/STM32/Python GUI 全开源的同频段方案
- **工程化深度**：`formal/` 形式化验证 + 四层测试栈，开源硬件罕见
- **商业化路径**：ABAC INDUSTRY + PCBWay 合作 = 唯一已通商业闭环的同类项目

### 竞争风险
- **最可能替代者**：Analog Devices CN0566 Phaser 升级版（如果 ADI 把 10.5 GHz 加入参考设计）—— 但 ADI 一直聚焦 6 GHz 以下，10.5 GHz 进入参考设计的概率低
- **次要风险**：TI / Renesas 等其他厂商推出 10 GHz 商业套件 —— 但商业套件闭源 BOM，无法复制 AERIS 风格
- **隐性风险**：作者停更 3.5 个月（Issue #145 AGC 溢出未修复），**项目可持续性是最大风险**

### 生态定位
在整个技术生态中扮演「开源高频段长距雷达基础设施」角色 —— 类比「开源硬件界的 espressif/esp32」，填补一个高频段长距全栈开源雷达的生态位空白。

## 套利机会分析
- **信息差**：25.8k stars 热度真实（22.8% fork/star 比，非机器人/非刷量），但 Hackaday / IEEE Spectrum / arXiv 等第三方媒体**无明显报道** —— 公众号读者群体（关注国产硬件/开源雷达/AI+SDR）对这一信息差有需求
- **技术借鉴**：三层 AGC 分层 + staggered-PRI Doppler + 形式化验证 CDC 是任何 RF / 软件无线电项目都可借鉴的工程模板
- **生态位**：填补 10.5 GHz 长距全栈开源雷达空白，可与 AI 信号处理 / ISAC（集成感知通信）/ 国产替代 / 摩洛哥出口等公众号叙事结合
- **趋势判断**：6.7 个月达到 25.8k stars 仍在「爆发期」，但作者停更 3.5 个月，处于「作品吸引流量、运营几乎为零」的反向路径 —— 公众号读者对「作品 → 公司」的样本感兴趣

## 风险与不足
- **作者停更 3.5 个月**：最近 commit 2026-06-17，Issue #145 AGC 溢出至今 open 无回应 —— 项目可持续性是最大风险
- **Issue 治理弱于工程实现**：MCU 扫描序列与文档不一致（Issue #32 已关闭但代码常量未同步：`DOPPLER_FRAME_CHIRPS=32` vs `matrix1[15] + vector_0 + matrix2[15] = 31-beam`）
- **社区分散**：提议建 Discord/Telegram 群 → 0 回复 closed，**真实社区活跃度无法从 GitHub 单一指标衡量**
- **死代码并存**：`doppler_processor.v` 与 `doppler_processor_optimized.v` 并存，未清理旧实现
- **测试覆盖率偏科**：硬件仿真层（test）1.5%，被 MATLAB co-sim 部分替代，但 Python GUI 单测覆盖弱
- **仓库体积大**：~132 MB（含 FPGA bitstream），clone 不友好
- **第三方媒体覆盖为零**：Hackaday / IEEE Spectrum / arXiv 无独立报道，主要靠 GitHub 自身病毒传播

## 行动建议
- **如果你要用它**：
  - 想学习 10.5 GHz 相控阵雷达 → AERIS-10 是唯一全栈开源选项
  - 想做 20 km 长距探测 → Extended 版本 + GaN PA 子板是少数能落地的方案
  - 想做国产替代 → ADI 芯片在国内有代理，但 PCBWay 合作模式可借鉴
  - 想做 ISAC / 雷达 + 通信融合研究 → 双版本硬件模块化是天然平台
  - 对比竞品：3 km 以内选 FMCW_RADAR 更省事；3 km 以上 AERIS-10 是必然选择

- **如果你要学它**：
  - **FPGA 顶层**：`9_Firmware/9_2_FPGA/radar_system_top.v`（1078 行顶层）—— 看清整个雷达信号处理流水线
  - **波束管理**：`9_Firmware/9_1_Microcontroller/9_1_1_C_Cpp_Libraries/ADAR1000_Manager.cpp`（930 行）—— 学习 ADAR1000 怎么驱动
  - **接收链路**：`9_Firmware/9_2_FPGA/radar_receiver_final.v` —— ADC → decim → FFT 完整链路
  - **AGC 设计**：`9_Firmware/9_2_FPGA/rx_gain_control.v` + `9_Firmware/9_1_Microcontroller/9_1_3_C_Cpp_Code/ADAR1000_AGC.cpp` + `9_Firmware/9_3_GUI/adi_agc_analysis.py` —— 三层 AGC 教科书
  - **CFAR 检测**：`9_Firmware/9_2_FPGA/cfar_ca.v` —— CA / SO / GO 三模 CFAR
  - **形式化验证**：`formal/` 子目录 —— 学习 SymbiYosky 怎么验证 CDC
  - **chirp 控制器**：`9_Firmware/9_2_FPGA/plfm_chirp_controller.v` —— FSM 怎么编排 chirp 时序
  - **GUI 与 FPGA 闭环**：`9_Firmware/9_3_GUI/v7/software_fpga.py` —— bit-accurate 镜像怎么写

- **如果你要 fork 它**：
  - **修 AGC 溢出**：把 `holdoff_counter` 从 uint8_t 改 uint32_t + saturate add（Issue #145）
  - **同步 MCU/FPGA 常量**：把 `DOPPLER_FRAME_CHIRPS` 从 32 改 31（或反过来）—— 解决 Issue #32 根因
  - **清理死代码**：删 `doppler_processor.v`，只保留 `doppler_processor_optimized.v`
  - **加外场测试结果**：作者计划在摩洛哥做外场测试（Issue #150），任何 fork 都可以加速这一块
  - **加云端 / LAN 接口**：Issue #21 LAN 接口是社区第二大需求，至今未实现
  - **加 3D 外壳**：Issue #17 外壳设计是社区最大需求（27 评论）
  - **加 CI**：仓库目前没有 GitHub Actions，加 CI 自动跑 tokei/formal verification 能显著提升工程化
  - **加 Discord/Telegram 群**：作者应该主动运营社区（Issue #29 提议但 0 回复）

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录 |
| Zread.ai | 未收录 |
| 关联论文 | 无（AERIS-10 是工程实现，非学术研究） |
| 在线 Demo | 无 GUI 在线 Demo（仅本地 Python GUI + GUI_V6.gif） |
| 公司主页 | http://www.abacindustry.com |
| GitHub Pages 文档 | https://nawfalmotii79.github.io/PLFM_RADAR/docs/ |
| 第三方媒体 | 无明显独立报道（Hackaday / IEEE Spectrum / arXiv 均无） |
| 赞助商 | PCBWay（README logo） |
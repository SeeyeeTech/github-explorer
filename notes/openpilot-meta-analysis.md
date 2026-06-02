# openpilot 元分析（Phase 2 — Meta Analysis）

- 仓库: commaai/openpilot
- 本地路径: /tmp/repo-miner-openpilot
- 首次提交: 2016-11-29
- 最近提交: 2026-06-01
- 分析时点: 2026-06-02

---

## 代码规模

| 指标 | 数据 |
|------|------|
| 总代码行数（Code） | 298,584 行 |
| 总行数（含注释/空行） | 338,855 行 |
| 注释行 | 14,971 行（占比 ~4.4%） |
| 空行 | 25,300 行 |
| 代码/注释比 | ~20:1（注释偏少，UI/翻译与 cereal 协议文档除外） |
| 文件数量 | 925 个源文件 + 大量 vendored 子模块 |

> tokei 在子模块中不递归统计 vendored 库，故真实体量远超 30 万行代码；phonelibs/、opendbc_repo/、cereal/、panda/、msgq_repo/、selfdrive/ 三大子系统均参与构建。

### 主语言分布

| 语言 | Code 行 | 占比 | 角色 |
|------|--------|------|------|
| Python | 252,812 | 84.7% | 主力：控制、模型推理、UI 业务逻辑、车厂适配 |
| C++ | 26,762 | 9.0% | 性能敏感路径（camerad/ modeld/ controlsd/ boardd） |
| PO File（翻译） | 5,383 | 1.8% | 多语言 UI 文案 |
| C Header | 7,023 | 2.4% | C/C++ 接口与协议定义 |
| Shell | 1,529 | 0.5% | 构建/启动/部署脚本 |
| 其他（C/Cython/JSON/Scons/HTML/SVG/Markdown/TOML/XML） | ~5,000 | 1.6% | 资源、协议、构建脚本、文档 |

**解读**：Python 是绝对主力（典型 AI + 控制项目结构），C++ 仅占 9% 但全部位于延迟敏感与硬件交互的核心路径，符合"原型用 Python，性能瓶颈下沉到 C++"的工程实践。

### 依赖规模

- 没有传统 `requirements.txt`，依赖通过 `pyproject.toml` + `SConstruct` 声明，vendored 依赖（eigen、acado、zmq、capnp、json11、libuv、curl、mp4、bzip2、qrcode、ncurses）随仓库发布；
- 子模块：`cereal/`、`opendbc_repo/`、`opendbc/`、`phonelibs/`、`panda/`、`msgq_repo/`、`scons/`、`tinygrad/`（部分）—— openpilot 把几乎所有外部依赖都 pin 在仓库里，保证"克隆即可构建"。

---

## 开发节奏

| 指标 | 数据 |
|------|------|
| 项目年龄 | ~114 个月（9.5 年，2016-11-29 → 2026-06-01） |
| 总 commit 数 | 17,219 |
| 贡献者 | 745 个独立邮箱 |
| 最近 30 天 commit | 132 |
| 最近 90 天 commit | 407 |
| 近 1 年 commit | ~1,540（12 个月合计 1,540） |
| 月均 commit | ~151 |
| 近期峰值 | 2026-02 单月 343 次（0.11 版本冲刺） |

### 月度 commit 趋势（最近 36 个月）

- **2023-08 单月 468 次**为历史峰值，对应 0.9.4/0.9.5 系列大规模重构（selfdrive.ui 改写为 Qt 前后端）。
- 2023-10 → 2024-12 长期稳定在 130–310/月，进入"稳定迭代 + 多分支并行"阶段。
- **2026-02 单月 343**是近三年第二高峰，恰好是 v0.11.0 发布月份。
- 整体节奏：**典型职业项目 / 高强度迭代**，几乎没有低于 50/月的"断档"。

### 开发模式

- **周末占比**：周一至周五 14,778 次（85.8%），周末（Sat+Sun）2,481 次（14.4%）。工作日主导但周末仍保持 14%，符合自动驾驶长尾数据回放/路测驱动的特征。
- **时间分布**：UTC 16:00–18:00 是最高峰（~1,400/h 段），对应美国西海岸 09:00–11:00（comma 总部在旧金山）；UTC 00:00–05:00 仍有 1,800+ 提交，疑似 CI / bot / 跨时区工程师夜间提交。
- 23:00–09:00 UTC 提交占 45% 以上，**典型分布式职业项目**，不依赖单一时区。

### 开发阶段

**稳定维护 + 持续密集迭代并存**。版本号仍以 0.x 推进（v0.11.0 2026-03），月均 130–300 commits 表明主线稳定输出；2026-02 单月 343 表明 v0.11 仍是重要功能节点（comma 4 / 全栈重写里程碑）。

---

## 演化轨迹

### 核心文件（Top 10 最常修改）

> openpilot 把"车辆配置"做成单一 values.py 文件，所以这些文件高居榜首本质是"车厂适配"而不是"算法核心"。

1. `selfdrive/test/process_replay/ref_commit` — 852 次（CI 基准 reference commit hash，每次发版/重构都要更新）
2. `selfdrive/car/toyota/values.py` — 610 次（丰田车系指纹库）
3. `panda`（gitlink，子模块）— 586 次
4. `cereal`（gitlink）— 569 次
5. `selfdrive/car/hyundai/values.py` — 541 次（现代起亚指纹库）
6. `RELEASES.md` — 521 次（发版说明）
7. `docs/CARS.md` — 495 次（支持车型列表）
8. `selfdrive/controls/controlsd.py` — 492 次（**核心控制状态机**，MPC/纵向控制/规划主循环）
9. `README.md` — 381 次
10. `release/files_common` — 377 次（构建打包白名单）

> 控制算法真正的"中枢"是 `controlsd.py`（接近 500 次修改）。其他高频文件是车厂适配指纹库与构建/CI 元数据。

### 热点目录（变更最频繁）

| 目录 | 变更次数 | 解读 |
|------|----------|------|
| `selfdrive/car` | 8,719 | **车厂适配层** — Hyundai/Toyota/Honda/Volkswagen/GM/Chrysler/Ford/Subaru 等 10+ 车系，单独 hyundai(1298) + toyota(1267) + honda(933) 三家就 3,500+ |
| `selfdrive/ui` | 7,320 | **UI 系统** — `selfdrive/ui/qt` 3,000 次、`translations` 1,300 次；2023 年从 Python UI 大改写为 C++/Qt UI |
| `selfdrive/test` | 3,050 | 路测回放、模型回归、CI 套件 |
| `selfdrive/controls` | 2,853 | 控制器：`controlsd` 状态机、`plannerd` 规划、`radard` 雷达 |
| `tools/cabana` | 2,292 | 开发者工具：CAN 总线 DBC 信号分析器 |
| `selfdrive/modeld` | 2,101 | **驾驶模型推理**（含 driving_vision / driving_policy） |
| `phonelibs/eigen` | 2,048 | vendored Eigen 线性代数 |
| `phonelibs/acado` | 1,655 | vendored ACADO（轨迹优化 MPC） |
| `phonelibs/zmq` | 1,362 | vendored libzmq |
| `selfdrive/locationd` | 1,329 | 定位/惯导/车辆状态估计 |
| `selfdrive/assets` | 1,216 | 模型权重 + 资源 |
| `system/ui` | 1,057 | 新版 system UI（Qt/SP） |
| `third_party/acados` | 894 | 替代 ACADO 的新版 MPC 求解器 |

**热点结构清晰**：车厂适配 (~36%) + UI 系统 (~30%) 占据近七成变更；中间层（控制/规划/感知/定位）合计约 17%；其余是工具/库/CI。印证了"在乘用 ADAS 领域，UI 与车厂适配才是真正的长期工程负担"。

### Commit 类型分布（17,219 次全量）

| 类型 | 数量 | 占比 |
|------|------|------|
| Feature / Add | 2,477 | 14.4% |
| Fix / Bug | 2,160 | 12.5% |
| Refactor | 150 | 0.9% |
| Docs | 227 | 1.3% |
| Test | 712 | 4.1% |
| Other（含 release/CI/build/bot/merge） | 11,493 | 66.7% |

> openpilot 不像早期项目用"feat:"前缀，绝大多数 commit 直接写自然语言标题，导致 fix/feat 识别率偏低；前 500 条样本中 fix:65, feat:39, test:15, doc:10, refactor:0。**Fix/Feature 比例 1:1.15**，说明项目已脱离纯新功能期，进入"功能 + 修复并重"的中后期。

### 版本发布

- **当前版本**: v0.11.0（2026-03-17）
- 上一版本 v0.10.3（2025-12-21）— 含 0.10.x 三个修订
- 0.10.0（2025-08-21），0.9.9（2025-06-19），0.9.8（2025-03-18），0.9.7（2024-06-14），0.9.6（2024-02-27）
- 总 Release 数（自 0.9 起）≥ 11
- **版本策略**：**语义化版本（SemVer）**，主版本号仍为 0.x 表明 API/兼容性尚未稳定。Release 间隔 2–6 个月，2024 年开始节奏稳定为 3–4 个月一版。
- 历史跨度（基于 tag）：v0.8.7（最早）→ v0.11.0（最新），最少 30+ 个 tag。

### 关键贡献者

| 贡献者 | commits | 角色推断 |
|--------|---------|----------|
| Adeeb Shihadeh | 4,114 | 长期主程（车厂适配 + 控制器） |
| Shane Smiskol | 2,891 | 长期主程（UI / 系统层） |
| Dean Lee | 1,962 | 模型/感知方向 |
| Willem Melching | 1,573 | 工具链 / cabana / CI |
| Justin Newberry | 538 | 维护者 |
| Maxime Desroches | 420 | 贡献者 |
| Jason Young | 301 | 贡献者 |
| ZwX1616 | 285 | 社区贡献（车厂适配） |
| Cameron Clough | 280 | 贡献者 |
| Harald Schäfer | 275+142=417 | 长期社区贡献（车厂适配） |
| George Hotz | 263 | **创始人**（仍持续 commit） |

Top 4 贡献 10,540+ 次，占 61%，**典型的"小核心团队 + 大社区"结构**。创始人 George Hotz 仍亲自 commit，体现强个人色彩。

### 整体演化路径

1. **2016–2018**：起步期，月均 < 50，commits 模式偏一次性 release。
2. **2018–2020**：Hacker News 爆红 + comma two 设备发布，社区开始大量车厂适配，commit 模式转向"持续交付"。
3. **2020–2022**：comma three / 三星硬件平台适配、引入 C++ modeld、MPC 重构。
4. **2022–2023**：UI 大改写（Python → C++/Qt），是 2023-08 单月 468 commits 的主因。
5. **2024–2025**：稳定迭代，月均 130–250；0.9.6 → 0.9.7 → 0.9.8 节奏稳定。
6. **2025-08 → 2026-03**：0.10.x → 0.11.0 大版本冲刺（comma 4 设备、新 UI 框架、MPC 求解器从 ACADO 迁到 acados）。

---

## 项目画像卡片

```
项目: commaai/openpilot
年龄: 114 个月  |  代码: 298,584 行 (Python 85% + C++ 9% + 协议/翻译 6%)
总 commits: 17,219  |  贡献者: 745 人
开发阶段: 稳定维护 + 持续密集迭代（v0.11.0 周期）
开发模式: 职业项目（核心团队 + 社区），分布式跨时区
核心文件: selfdrive/controls/controlsd.py, selfdrive/car/*/values.py, selfdrive/ui/qt, selfdrive/modeld
热点子系统: car（车厂适配 36%）、ui（30%）、controls/（12%）、test（13%）
版本策略: 语义化版本（0.x），3–6 个月一版
最新版本: v0.11.0（2026-03-17）
```

### 关键洞察（供 Phase 3 重点关注）

1. **车厂适配是最大工程量**（37% commits），这是行业现实：开放平台 ADAS 的护城河在"覆盖多少车型"而非"算法多炫"。
2. **UI 系统同样在快速演化**（30% commits，2023 大改写），说明人机交互/可视化在辅助驾驶体验中权重持续提升。
3. **控制中枢 `controlsd.py` 接近 500 次修改**——是项目真正的"大脑"（MPC + 状态机）。
4. **phonelibs/ + opendbc/ + cereal/ + panda/** 构成完整"自研中间件"栈，openpilot 选择 vendoring 而非依赖管理，是嵌入式/车载场景的典型工程取舍。
5. **小核心团队（4 人 60% commits）+ 创始人亲自 commit**——公司文化与项目紧密耦合，"openpilot 风格"可观察、可借鉴。

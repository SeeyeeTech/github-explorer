# elastic/elasticsearch — Phase 2: Meta Analysis

## 代码规模

| 指标 | 数据 |
|------|------|
| 总代码行数 | ~110 万行（不含空行/注释，核心模块 server + rest-api + modules） |
| 语言分布 | Java 95%+（核心引擎）, Python ~3%（构建/测试）, TypeScript/JS <1%（工具） |
| 代码/注释比 | 约 3:1（大量 Javadoc 和许可证头注释） |
| 文件数量 | 6,516 个 Java 文件（核心模块） |
| 依赖数量 | Gradle 构建，数百个 direct/runtime 依赖 |
| 仓库总大小 | 1.3 GB |

## 开发节奏

| 指标 | 数据 |
|------|------|
| 项目年龄 | 195 个月（首次提交 2010-02-08） |
| 总 commit 数 | 100,700 |
| 最近提交 | 2026-05-31 |
| 近 30 天 commit | 1,334 |
| 近 90 天 commit | 4,342 |
| 近 365 天 commit | 12,226 |
| 开发阶段 | **密集开发**（2026 年 3-5 月分别 1339/1704/1377 commits，持续加速） |
| 开发模式 | **职业项目**（工作日提交 97%，周末 3%；深夜提交 4.4%，白天 95.6%） |

## 演化轨迹

### 核心文件（Top 10 最常修改）

由于仓库极大（10万+ commits），采用目录级别分析：

1. **server/src/main/java/org/elasticsearch/index/** — 8,720 次修改（索引核心）
2. **server/src/main/java/org/elasticsearch/action/** — 6,596 次修改（Action 框架）
3. **server/src/main/java/org/elasticsearch/cluster/** — 5,039 次修改（集群管理）
4. **server/src/main/java/org/elasticsearch/search/** — 4,176 次修改（搜索模块）
5. **server/src/main/java/org/elasticsearch/common/** — ~4,000 次修改（公共组件）
6. **server/src/main/java/org/elasticsearch/repositories/** — ~2,500 次修改（存储）
7. **server/src/main/java/org/elasticsearch/snapshots/** — ~2,200 次修改（快照）
8. **server/src/main/java/org/elasticsearch/indices/** — ~2,000 次修改（索引管理）
9. **server/src/main/java/org/elasticsearch/transport/** — 1,209 次修改（网络传输）
10. **modules/** — ~3,000 次修改（内置模块）

### 热点目录

1. **x-pack/** — 56,104 次修改（商业特性，包含 Security/ML/Monitoring 等）
2. **server/** — ~50,000 次修改（核心引擎）
3. **modules/** — ~8,000 次修改（内置插件如 aggregations、ingest 等）
4. **plugins/** — ~5,000 次修改（插件系统）
5. **rest-api-spec/** — ~3,000 次修改（API 规范）

### Commit 类型分布

基于最近 500 条 commit 分析：

- **Feature/Add**: 55 (11.0%)
- **Fix/Bug**: 80 (16.0%)
- **Refactor**: 4 (0.8%)
- **Docs**: 23 (4.6%)
- **Test**: 143 (28.6%) ← 测试驱动特征明显
- **Other**: 195 (39.0%)

### 版本发布

- **最新版本**:
  - v9.4.2（2026-05）
  - v8.19.16（同期维护）
- **总 Release 数**: 497 个 tags
- **版本策略**: **语义化版本 + 双线并行**（v8.x LTS 维护 + v9.x 主线同步推进）
- **版本节奏**: ~6 周一个 patch 版本，~3 月一个 minor 版本

## 项目画像卡片

**项目**: elastic/elasticsearch
**年龄**: 195 个月（16.3 年） | **代码**: ~110 万行 (Java)
**总 commits**: 100,700 | **贡献者**: 2,367 人
**开发阶段**: 密集开发（近两月创历史新高）
**开发模式**: 职业项目（企业级维护）
**核心文件**: index, action, cluster, search, transport
**Release**: v9.4.2 (共 497 个版本)

---

**关键发现**：

1. **巨型单体仓库**：110 万行 Java 代码，2,367 贡献者，是世界上最大的开源项目之一
2. **测试覆盖极高**：28.6% commits 专注测试，测试驱动开发（TDD）特征显著
3. **活跃度持续攀升**：2026 年 4 月 1,704 commits 创历史新高，说明项目仍在高速迭代
4. **双版本并行维护**：v8（LTS）和 v9（主线）同步发布，商业支持模式成熟
5. **模块化架构**：server + modules + plugins + x-pack 分层清晰，支持灵活扩展
6. **ES|QL 成为新焦点**：近期提交大量围绕 ES|QL（Elasticsearch Query Language）展开，AI/Analytics 方向投入加大
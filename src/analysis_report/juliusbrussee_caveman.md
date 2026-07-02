# GitHub推荐：80k stars 用了 3 个月：一个人做的「让 AI 闭嘴」caveman，凭什么病毒式爆红

> GitHub: https://github.com/juliusbrussee/caveman

## 一句话总结
caveman 是一套让 Claude / Cursor / Codex 等 30+ AI 编程 agent「强制简洁说话」的 prompt-engineering-as-infrastructure：把"压缩 output style"做成跨 agent、always-on、可卸载、有 honest eval 的产品层,3 个月从 0 涨到 80,714 stars。

## 值得关注的理由
1. **现象级增长 + 单一作者**:2.9 个月、201 commits、80k stars,作者一人承担 63% 提交,这种密度在 AI 编程工具赛道极罕见。
2. **护城河在「跨 agent 安装矩阵」而非 SKILL.md**:30+ 个 agent 的单一 Node installer + JSONC-tolerant settings + marker-fenced injection,这三条工程模式可直接迁移到任何想做"AI 工具基础设施"的项目。
3. **HN 顶级讨论引爆 + 真实工程深度并存**:HN 上被质疑"压缩 output 是否让模型变笨"后,作者补出了 three-arm honest eval(`__baseline__` vs `__terse__` vs `<skill>`)——这是少数 AI 工具把"诚实度量"做成工程基础设施的案例。

## 项目展示

![Star History Chart](https://api.star-history.com/svg?repos=JuliusBrussee/caveman&type=Date)

*星标增长曲线(0 → 80k+,仅 2.9 个月)*

![caveman-on (compressed)](https://caveman.so/_next/image?url=%2Fcaveman-on.png&w=3840&q=75)
![caveman-off (verbose)](https://caveman.so/_next/image?url=%2Fcaveman-off.png&w=3840&q=75)

*官方 before/after 演示图:同一 prompt,verbose 模式 vs caveman 模式输出对比*

![atlas-cloud architecture](https://raw.githubusercontent.com/juliusbrussee/caveman/main/docs/assets/atlas-cloud.svg)

*架构图:多 agent 适配层 + 中央 installer*

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/juliusbrussee/caveman |
| Star / Fork | 80,714 / 4,518 |
| Watchers / Open issues | 183 / 358 |
| Open PRs | 196 |
| 代码行数 | 8,280 LOC(131 文件,44.2% 注释密度) |
| 语言分布 | JS 65.9% · Python 26.0% · PowerShell 4.2% · Shell 3.8% |
| 依赖 | **0 runtime + 0 dev deps**(纯 Node ≥18 installer + skill bundle) |
| 项目年龄 | 2.9 个月(2026-04-04 → 2026-06-12) |
| 版本 | 15 个 semver tag(v1.0.0 → v1.9.0 + patch 链 1.3.5/1.4.1/1.5.1/1.8.1/1.8.2) |
| 提交节奏 | ~6 天/版本(全职业节奏);MVP 爆发 142 commits/月 → 收敛 16 commits/月 |
| 贡献模式 | **独立开发为主**(31 contributors,top author 63.0%,bus factor ≈ 1) |
| 热度定位 | **大众热门**(单日涨 925 stars,HN 头版) |
| 质量评级 | 代码 优 · 文档 优 · 测试 基本(无 CI 跑 test) |
| 许可证 | MIT |

## 作者视角:为什么存在这个项目

### 创始人/作者背景
**Julius Brussee**,荷兰,独立开发者 + 莱顿大学数据科学与 AI 本科生(2025 入学)。GitHub 账号 4.2 年,2,029 followers,49 个 public repos。

他的自我定位语录极简:**"Everyone's racing to build better AI models. I build the tooling around them."**

5 仓库"洞穴生态"都围绕一个母题:
- **caveman** —— 让 AI 闭嘴(本项目,output compression)
- **caveman-code** —— coding-style 压缩
- **cavemem** —— 持久记忆
- **cavekit** —— 工具链
- **cavegemma** —— Gemma 4 31B QLoRA 微调(把"caveman"烤进权重)

媒体背书:RTL Editie NL、BNR Nieuwsradio、莱顿大学 2026 年 5/6 月专题报道。这种"独立学生 + 国家电视台报道 + HN 头版"的组合在 AI 编程工具赛道几乎独此一家。

### 问题判断
**"大模型输出口水太多"是公开秘密,但没人愿意把它做成产品。**

token 成本结构里,output token 通常占 60–80%(尤其 agent loop 里)。所有人在卷模型能力,但没人卷"输出样式"。这是一个典型的「between 椅子」的位置:
- 模型厂商不愿意动(怕被解读为「我们的模型啰嗦」)
- 工具厂商可以做 prompt engineering,但产品形态是 SaaS(marginal cost 高)
- 开源可以做,但需要极强的 agent-兼容性工程

**时机为什么是现在?**
1. 2026 年初 Claude Code / Cursor / Codex 等 agent IDE 全面铺开 → 跨 agent 安装矩阵的市场窗口打开
2. HN 用户对 token 成本敏感度剧增(Anthropic 涨价风波)
3. 单一作者可以 hold 住 30+ agent 适配,因为 target 是"装一行 prompt + hook",不是"重写 agent"

### 解法哲学
**README 哲学声明(三连,体现强烈品牌意识):**

> 🪨 why use many token when few token do trick

> **Caveman no make brain smaller. Caveman make *mouth* smaller.**

> Lobster claw still sharp. Lobster mouth now small. Brain still big.

这一段是 caveman 的核心定位:**它是 output-style compression,不是 reasoning-token compression。**这回应了 HN 上最尖锐的质疑("压缩 output 是否让模型变笨?")——作者明确划清了"嘴巴"和"大脑"的界限。

**明确不做什么(从代码与 issue 反推):**
1. 不做 SaaS(纯本地 + MIT)
2. 不做模型微调主路(留给 cavegemma)
3. 不做 memory 主路(留给 cavemem)
4. 不做 Copilot on VS Code(#88,已知盲点)
5. 不在 hook 里抛错(silent-fail 哲学,"hook 不能 block session start")

### 战略意图
**从「caveman meme」进化成「Cave toolkit 生态」**。作者的更大图景是 5 仓库覆盖 AI 编程工具栈的每个 cost-driver:
- caveman → 减 output token
- cavemem → 减 context token
- cavekit → 减 setup token
- cavegemma → 把上面三个烤进权重

**商业化路径**:**Chrome 扩展已上线**(https://chromewebstore.google.com/detail/caveman-mode-%E2%80%94-chatgpt-cl/dljfndmkapffcbcjpabcmclgbppbgfjm),把 ChatGPT 输出也压缩了——这是从 developer tool 向 consumer SaaS 试探的第一步。

## 核心价值提炼

### 创新之处(按 新颖度 × 实用性 × 可迁移性 排序)

#### 1. Symlink-safe flag envelope(`src/hooks/caveman-config.js`)
**新颖度 5/5** · 实用性 5/5 · 可迁移性 5/5

`safeWriteFlag` / `readFlag` / `appendFlag` 三件套,防御链:
- `O_NOFOLLOW` 拒绝 symlink 替换
- parent-dir `realpath` 校验
- 写入后比对 uid
- 64-byte size cap
- `VALID_MODES` 白名单

**威胁模型很真实**:用户主目录有 `~/.ssh/id_rsa` symlink,如果 flag path 是用户可控的,attacker 可以诱导 agent 把 `id_rsa` 当 flag 读。这种工程级"defensive default"在 AI agent 工具里罕见。

#### 2. JSONC-tolerant settings.js 三件套(`bin/lib/settings.js`)
**实用性 5/5** · 可迁移性 5/5

- `stripJsonComments`:手写 state machine,识别 string 内 // 注释,不误伤 URL/正则
- `validateHookFields`:write 之前 mutate,把未知字段静默丢掉而不是炸掉
- `pruneOrphanedManagedHooks`:卸载时自愈 dangling refs(关联 issue #471)

**这是给 Claude Code / Cursor 等 agent 设置文件写的"鲁棒 parser",任何要做 multi-agent 安装器的项目都可以直接抄。**

#### 3. Marker-fenced text block injection(`bin/lib/openclaw.js`)
**可迁移性 5/5**

用 `<!-- caveman-begin/end -->` 在 SOUL.md / AGENTS.md 等任意文本文件里塞 block,卸载时用 `indexOf` 精准切片。**比"重写整文件"或"git merge"都安全**——任何想做"AI 工具的 bootstrap 注入"的项目都该用这个模式。

#### 4. Provider matrix as data DSL(`bin/install.js` PROVIDERS 数组)
**实用性 5/5**

```js
const PROVIDERS = [
  { id: 'claude-code', ... soft: true },
  { id: 'cursor',      ... },
  { id: 'opencode',    ... },
  // 30+ agents
];
```

加新 agent = 加一行。`soft: true` 表示"装失败不报错,只是没启用"——最大化覆盖面。

#### 5. Three-arm honest eval(`evals/`)
**实用性 5/5**

- `__baseline__`:不做 prompt 干预,看模型默认啰嗦度
- `__terse__`:人为写"简短"prompt,看 prompt-level 简短效果
- `<skill>`:caveman 实际效果

honest delta = skill vs terse(而不是 skill vs baseline)——这是少数 AI 工具把"诚实度量"做成工程基础设施的案例。snapshot commit 到 git,CI 离线可跑。

#### 6. Tier-3 OpenClaw bootstrap
**新颖度 4/5**

OpenClaw 不支持 always-on skill。作者用 marker-fenced block 注入 SOUL.md(自动加载),绕开 on-demand 限制。**这是"用文件 bootstrap 模拟 hook 行为"的工程化 hack**。

#### 7. MCP shrink stdio JSON-RPC proxy(`src/mcp-servers/caveman-shrink/`)
只改 `tools/list` 的 description 字段,**不碰 `tools/call` 响应/上行 payload**——最小侵入地让模型"看到"工具描述更短,但实际功能不变。

#### 8. Opencode plugin 跨 ESM/CJS 桥接
```js
new Function('module', 'exports', 'require', '__dirname', '__filename', code)
```
直接 eval CJS 源码,绕开 Bun runtime 的 ESM-only 限制。

### 可复用的模式与技巧

| 模式 | 文件 | 复用场景 |
|------|------|---------|
| JSONC-tolerant parser | `bin/lib/settings.js` | 任何"用户配置文件带注释"场景(VSCode settings.json、tsconfig.json) |
| Symlink-safe flag envelope | `src/hooks/caveman-config.js` | 任何"agent 在文件系统留 marker"的场景 |
| Marker-fenced injection | `bin/lib/openclaw.js` | 任何"在不重写文件的前提下注入 block"的场景 |
| Provider matrix DSL | `bin/install.js` | 任何"多后端适配"的项目(LLM provider、IDE、CI runner) |
| Three-arm eval | `evals/` | 任何 AI 工具的"诚实 A/B 测试" |
| Pinned ref + SHA-256 manifest | `install.sh` / `package.json` | 任何"避免 curl \| bash 静默升级"的 installer |
| Silent-fail hook 哲学 | `src/hooks/*.js` | 任何"工具不能 block 主流程"的场景 |

### 关键设计决策

1. **单一 Node installer**(替代 4 套 bash/PS1,来自 issue #249 教训)——把"目标平台覆盖"和"安装逻辑"解耦
2. **三层 always-on fallback**:Claude Code hook + flag file / opencode native plugin + AGENTS.md / SOUL.md marker / `.*rules/`
3. **Flag file 做单一 state source**:SessionStart 写、UserPromptSubmit 读、Statusline 读 —— **避免"session 状态分散在多处"**
4. **Pinned ref + SHA-256 manifest**:`PINNED_REF = v1.9.0` + `checksums.sha256`,避免 `curl|bash` 静默升级
5. **Hook silent-fail 哲学**:hook 永远不能 block session start —— 这是 agent 工具的生存底线
6. **`--all` 故意不开 `--with-mcp-shrink`**:proxy 必须传 upstream cmd,默认保守(不偷偷启用用户没要求的网络代理)

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | **caveman**(本项目) | **claude-mem**(85.5k★) | **taste-skill**(55k★) | **system-prompts-leaks**(47.8k★) |
|------|---------|---------|---------|---------|
| 解决问题 | output 太啰嗦 | context 太长 | 输出风格不佳 | 提示词不透明 |
| 作用层 | output style | memory layer | writing style | community asset |
| 跨 agent 适配 | **30+ agents** | 主要 Claude Code | Claude 系 | N/A |
| 开源协议 | MIT | MIT | MIT | 文档类 |
| 安装方式 | 单一 installer + hook | hook + memory store | skill 注入 | 静态资源 |
| Eval 体系 | **three-arm honest** | 无公开 eval | 无公开 eval | 无 |
| Bus factor | 1 | 1 | 1 | 社区驱动 |
| 差异化 | 跨 agent + 诚实 eval + 品牌 | 持久记忆 + 跨 session | 写作质量 | 透明度 |

### 差异化护城河

| 维度 | 护城河 |
|------|--------|
| **生态覆盖** | 30+ agent 适配矩阵(竞品都在 1–3 个) |
| **品牌资产** | "caveman"已成为 output compression 的 meme 词,Chrome 扩展进一步扩散 |
| **工程模式** | JSONC-tolerant + symlink-safe + marker-fenced 三件套,直接迁移门槛极高 |
| **诚实评估** | three-arm eval 是少数 AI 工具的"反 PR 营销"实践 |
| **信任基础** | MIT + 透明 + 无 SaaS + 无遥测 |

### 竞争风险

| 风险 | 触发条件 | 应对难度 |
|------|---------|---------|
| **claude-mem 加 output compression 子模块** | claude-mem 已经有 cross-agent memory,加一个 compress 子模块成本极低 | 高 |
| **Anthropic / OpenAI 官方在 prompt 层做压缩** | 模型厂商主动声明"已优化输出样式" | 极高(对 caveman 致命) |
| **HN meme 衰退** | 新热点出现,关注度转移 | 中 |
| **bus factor 1** | 作者停止维护 | 高(实际项目生存风险) |
| **cavegemma 把 caveman 烤进权重** | 用户不再需要 prompt-level 压缩 | 中(但跨模型仍有需求) |

### 生态定位

caveman 填补了 **"AI 编程工具栈中、output token 成本控制的 prompt 层"** 这个空白。在整个 LLM 应用栈里:
- 上层 → 模型厂商(Anthropic / OpenAI / Google)
- 中层 → Agent framework(LangChain / LlamaIndex / Claude SDK)
- **caveman 层** → 跨 agent 的 output style compression
- 下层 → Token 计费 / 监控(LangSmith / Helicone)

**cavegemma 是作者自己向上吞掉这一层的尝试**——把 caveman 烤进 Gemma 4 权重,绕开 prompt engineering。这是非常聪明的"prompt engineering → weights engineering"路径。

## 套利机会分析

- **信息差**:竞品(claude-mem / taste-skill)都没解决"output compression"这件具体事,caveman 的护城河是"早 + 品牌 + 工程深度"。信息差窗口约 6–12 个月。
- **技术借鉴**:
  - JSONC-tolerant settings.js parser → 可直接用到任何 Claude Code plugin
  - Symlink-safe flag envelope → 任何"agent 在文件系统留 marker"的场景都该用
  - Marker-fenced injection → 任何"在不重写文件的前提下注入 block"的场景
  - Three-arm honest eval → 任何 AI 工具的"诚实 A/B 测试"
- **生态位**:AI 编程工具栈中的"output token 成本控制 prompt 层",5 仓库"洞穴生态"是这个 niche 的事实标准
- **趋势判断**:跨 agent 安装矩阵需求只会增加(LangChain / MCP 都在往多 agent 适配走);cavegemma 路线如果跑通,caveman 可能从"产品"变成"训练数据"——这是中期最大的范式风险

## 风险与不足

### 核心三角风险
1. **Bus factor 1**:31 contributors 但 top author 63.0%(Julius Brussee 104 commits);CLAUDE.md 行文暗示单人维护节奏。任何突发情况(作者 burnout / 转向)会立刻威胁项目生存。
2. **Missing test CI**:**只有 `sync-skill.yml` 跑 plugin mirror + ZIP,不在 push 时跑 test**。bus factor 1 + 别人接手时无法验证 → 任何新 agent 提交可能 break installer 但 CI 看不到。
3. **Hook silent-fail 是双刃剑**:hook 永远不抛错,但 user 也看不到为什么 stats 历史缺失。**对个人开发者友好,对团队 adoption 不友好**。

### 已知覆盖盲点
- **#428 Antigravity CLI 不支持**——CLI 生态扩张速度快,矩阵永远滞后
- **#88 Copilot on VS Code 不支持**——最大用户群盲点
- **#251 byte-safe metering 缺**——用户要求按 byte 而非 token 计费,Gateway-layer 还没实现

### 工程层风险
- **commit decay**:最近 30 天仅 7 commits,20 天没 push——从"密集开发"转入"维护模式",社区期待 vs 作者精力错配的风险在累积
- **0 runtime + 0 dev deps 是优势也是脆弱性**:没有依赖保障,Node 标准库一旦有破坏性升级(罕见但不是没发生过)installer 直接挂
- **HN 上"压缩 output 是否让 model 变笨"的质疑未被完全回应**:作者承认 75% 是 preliminary,rigorous benchmark 还在做——如果 benchmark 跑出来不利,品牌会受损

## 行动建议

### 如果你要用它
- **适合场景**:Claude Code / Cursor / Codex / opencode 用户,且对 output token 成本敏感
- **不适合场景**:你主要用 Copilot on VS Code(#88)、你的 agent 工作流对长输出有依赖(比如 chain-of-thought verbose mode)
- **建议用法**:`npx caveman --all`(跨 agent 安装)+ `caveman-stats`(看实际节省)+ 偶尔用 `caveman-off` toggle 切回去对比效果

### 如果你要学它
**推荐学习顺序**(按"价值密度 / 上手成本"排序):
1. **`README.md`**(产品哲学)
2. **`CLAUDE.md`**(作者思维模式,**最重要**)
3. `bin/install.js`(PROVIDERS 数组 + self-heal 模式)
4. `bin/lib/settings.js`(JSONC 三件套)
5. `bin/lib/openclaw.js`(marker-fenced injection)
6. `src/hooks/caveman-config.js`(symlink-safe envelope)
7. `src/hooks/caveman-mode-tracker.js`(state persistence 模式,关联 #141)
8. `src/plugins/opencode/plugin.js`(跨 ESM/CJS 桥接)
9. `src/mcp-servers/caveman-shrink/{index,compress}.js`(stdio proxy)
10. `skills/caveman/SKILL.md`(真源 prompt)
11. `skills/cavecrew/SKILL.md` + `agents/cavecrew-*.md`(multi-agent 协调)
12. `evals/README.md`(three-arm eval 怎么搭)
13. `tests/test_symlink_flag.js` + `tests/test_repo_local_config.js`(怎么测文件系统边界)

### 如果你要 fork 它
**最有价值的改进方向**(按 ROI 排序):
1. **加 GitHub Actions 跑 test on PR**(缺位严重,补上立刻提升可信度)
2. **补 byte-safe metering**(关联 #251,Gateway-layer 兑现承诺)
3. **Copilot on VS Code 适配**(关联 #88,最大用户群盲点)
4. **Three-arm eval 自动化跑 + badge**(把"诚实"做成可视化信任锚)
5. **5 仓库"洞穴生态"整合 README**(作者最大战略弱点:5 个项目分散,没有 meta-doc)
6. **bus factor 1 解法**:写 `CONTRIBUTING.md` 真正让外部 contributor 容易接手(目前更像 todo)

### 知识入口

| 资源 | 链接 |
|------|------|
| DeepWiki | 未收录 |
| Zread.ai | 未收录 |
| 关联论文 | 无(纯工程,无学术论文) |
| 在线 Demo | https://caveman.so/(before/after 对比演示) |
| Chrome 扩展 | https://chromewebstore.google.com/detail/caveman-mode-%E2%80%94-chatgpt-cl/dljfndmkapffcbcjpabcmclgbppbgfjm |
| HN 讨论 | https://news.ycombinator.com/item?id=47647455 |
| 作者博客 | https://polder.substack.com("Two Weeks in the Cave") |
| 关键 Issue | [#426](https://github.com/JuliusBrussee/caveman/issues/426) · [#141](https://github.com/JuliusBrussee/caveman/issues/141) · [#428](https://github.com/JuliusBrussee/caveman/issues/428) · [#251](https://github.com/JuliusBrussee/caveman/issues/251) · [#88](https://github.com/JuliusBrussee/caveman/issues/88) |
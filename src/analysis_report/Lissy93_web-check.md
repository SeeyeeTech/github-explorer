# 一个网址跑 36 项检查，网站分析全家桶

> GitHub: https://github.com/Lissy93/web-check

## 一句话总结

web-check 是 Alicia Sykes（Lissy93）的「一站式网站 OSINT 分析工具」——输入一个网址，就能在一张漂亮的 dashboard 里一键跑完 36 项检查（DNS、SSL/TLS、HTTP 安全头、whois、子域名、开放端口、技术栈、Shodan、威胁情报、碳足迹、截图……），把过去要分别开十几个网站才能查到的东西聚合成单张报告。免费在线用，也完全可自托管。

## 值得关注的理由

- **「聚合替代」的清晰价值**：单点工具（securityheaders.com 只看头、SSL Labs 只看证书、BuiltWith 只看技术栈）各看一面且多为闭源 SaaS；web-check 把几十个分散能力一锅端，整合 Wappalyzer/Shodan/Mozilla TLS Observatory/Lighthouse/Tranco/Wayback/威胁情报等几十个外部源，且 MIT 开源、可自托管。一句话定位：「20 秒看清攻击者眼中的你的网站」。
- **优雅的「插件式检查 + 注册表驱动 UI」架构**：每项检查是一个独立的 serverless 函数（`api/` 下 36 个 .js），前端用一份 registry 注册表驱动卡片式 dashboard——加一个检查 = 加一个 api 函数 + 注册一张卡片。这套可扩展设计值得学。
- **老牌头部刚刚「重写复活」**：沉寂近 18 个月（曾有 issue「Did the website die?」）后，2026-05 单月骤增 82 commit，把项目从纯 React SPA 重写为 Astro 架构——「头部项目 + 刚复活 + star 重新加速」是难得的二次曝光窗口。

## 项目展示

![web-check dashboard](https://raw.githubusercontent.com/Lissy93/web-check/master/.github/screenshots/web-check-screenshot1.png)

在线免费用：[web-check.xyz](https://web-check.xyz)（输入任意网址即出报告）。也可一键自托管（Docker/Vercel/Netlify/Fly/源码）。

## 项目画像

| 维度 | 数据 |
|------|------|
| GitHub | https://github.com/Lissy93/web-check |
| Star / Fork | 33349 / 2705（大众热门，复兴中，近 10 天涨 149 star） |
| 代码行数 | 27.7K 总量但**业务约 12.7K**（JSON 41% 是地图 TopoJSON 1.1 万行 + OpenAPI 文档 3 千行；真实栈 TSX 6K 前端 + JS 2.4K 后端检查 + TS/Astro） |
| 项目年龄 | 47.9 个月（约 4 年，2022-06 起） |
| 开发阶段 | 密集开发（但为「18 个月沉寂后 2026-05 单月 82 commit 重写爆发」，非匀速） |
| 贡献模式 | 单人主导（Alicia Sykes 占 76.2% + liss-bot 自动化 + 社区零散 PR） |
| 热度定位 | 大众热门 + 复兴中的明星项目（聚合赛道近蓝海） |
| 质量评级 | 代码[良好·插件式清晰] 文档[优·每项检查带教学] 测试[无·Test 0%，靠 lint+typecheck] |
| License | MIT |

## 作者视角：为什么存在这个项目

### 创始人/作者背景

**Alicia Sykes（Lissy93，伦敦，7182 followers）**——头部独立隐私/安全开源创作者，明确以「帮普通人逃离大厂、降低自托管门槛、做尊重隐私的工具」为创作母题。代表作构成一条清晰产品线：**Dashy（自托管仪表盘 ~25k）、awesome-privacy（~9.5k）、personal-security-checklist、who-dat（whois 微服务，被 web-check 复用）**，著有《Web Security》。web-check 是这条线里「主动安全审计」的拼图，可信度极高。她个人占 76.2% 提交——近乎单人作品（周末提交 50%、深夜 30%，典型业余投入）。

### 问题判断

给一个网站做全面体检/侦察，过去要分别打开十几个工具：查头去 securityheaders.com、查证书去 SSL Labs、查技术栈去 BuiltWith、查子域名去 crt.sh、查威胁去 URLHaus……零散、低效、且多是闭源 SaaS。Alicia 看到的是：**应该有一个免费、开源、可自托管的工具，输入一个网址就把这几十项检查一次跑完、聚合成一张报告**。同时,自托管让「数据不出自己服务器」契合她的隐私理念。这是把「分散工具」聚合成「一键体检」的产品化机会。

### 解法哲学

- **明确选择聚合而非自造**：复用几十个成熟外部源/API，自己做整合与呈现。
- **明确选择插件式检查 + 注册表驱动 UI**：每项检查独立 serverless 函数，registry 驱动卡片——可扩展。
- **明确选择零配置 + 渐进增强**：开箱无需 key，配可选 API key 才解锁 Shodan/Quality 等高级项。
- **明确选择免费开源 + 多部署自托管**：MIT，Docker/Vercel/Netlify/Fly 四种一键部署，数据不出自己服务器。
- **明确选择工具即教学**：每个检查在 README 配「这是什么/有什么用/延伸阅读」。

### 战略意图

web-check 是 Alicia「隐私/安全/自托管」作品矩阵的有机一环，无商业化（靠 GitHub Sponsors）。它树立「一键网站体检」的开源标杆，常被 awesome-osint/homelab 选型清单推荐。2026-05 的 Astro 重写是为长期可维护性投资（issue #291 仍在推进 monorepo 化）。

## 核心价值提炼

### 创新之处

1. **注册表驱动的卡片式 dashboard**（最值得学）：`src/client/jobs/registry.ts`（检查注册表）+ `useJobs.ts`（任务调度）+ `Results.tsx`（卡片网格）+ `ProgressBar`（36 项并发进度）——「注册表 → 调度 → 渲染 → 进度」主链路，每个检查对应一张结果卡片。
2. **每项检查 = 一个独立 serverless 函数**：`api/` 下 36 个 .js（dns/ssl/headers/whois/subdomains/ports/tech-stack/shodan/threats/screenshot/carbon...），互不影响、可独立演进——插件式可扩展。
3. **多部署目标适配**：用 `@astrojs/vercel|netlify|node|cloudflare` 适配器 + 自托管 `server.js`，一份代码部署到 Docker/Vercel/Netlify/Fly/Node。
4. **聚合几十个外部源**：把 Wappalyzer/Shodan/TLS Observatory/Lighthouse/Tranco/威胁情报/who-dat 等整合进一个面板，零配置可用。

### 可复用的模式与技巧

1. **注册表驱动 UI**：用一份 registry 配置驱动卡片/任务/进度——任何「多模块聚合面板」都可借鉴。
2. **插件式 serverless 检查**：每个能力一个独立函数，加能力零侵入。
3. **多部署适配器**：用框架适配器让一份代码跑遍多平台。
4. **工具即教学**：每个功能配「是什么/为什么/延伸阅读」，提升可用性与传播。

### 关键设计决策

- **聚合外部 API 的双刃剑**：换来「一键查全」的价值，代价是**外部依赖脆弱**——截图（puppeteer/chromium）、地理位置、Lighthouse 质量分等强依赖第三方/无头浏览器，是报错重灾区（fix 占 25.5%≈feature）。
- **React SPA → Astro 重写**：为长期可维护与 SSR/性能，2026-05 大重构（迁移残留可见 svelte.config 与 astro.config 并存）。
- **零测试**：个人项目取舍，质量靠 lint+typecheck，无自动化测试网。

## 竞品格局与定位

### 竞品对比矩阵

| 维度 | web-check | 单点 SaaS（SSL Labs/securityheaders/BuiltWith） | domain-digger | SpiderFoot |
|------|-----------|------------------------------------------------|---------------|------------|
| 形态 | 聚合一键报告 dashboard | 各看一面 | 域名分析全家桶 | OSINT 侦察框架 |
| 检查数 | 36 项 | 单项 | 较少 | 模块多 |
| 开源/自托管 | ✓ MIT + 多部署 | ✗ 闭源 SaaS | ✓ | ✓ |
| 易用性 | 高（一键卡片） | 高（单项） | 高 | 偏专业、上手难 |
| Stars | 33k | 各异 | ~1.1k | 数千 |

### 差异化护城河

护城河 =「**几十项检查一键聚合 + 漂亮卡片 dashboard + 免费 MIT 开源 + 可自托管隐私友好 + Alicia 的安全品牌**」这一组合，几乎独占。单点工具是红海，但「聚合 + 开源 + 自托管 + 易用」的交集 web-check 近乎无正面对手（domain-digger 最接近但体量/检查数远不及）。

### 竞争风险

- **外部 API 依赖脆弱（最大结构性软肋）**：上游一变就坏，维护负担天然高；托管版休眠期有可用性焦虑。
- **单人 + 零测试**：高度依赖 Alicia 一人；曾沉寂 18 个月，可持续性有波动。
- **重写过渡期**：Astro 迁移 + monorepo 化仍在进行，稳定性待沉淀。
- **单点工具更权威**：SSL Labs 等在各自维度更深更权威，web-check 是「广而非深」。

### 生态定位

它是「一键网站体检/侦察」开源工具的事实标杆——把分散的网站分析能力聚合成易用面板，填补「免费 + 开源 + 自托管 + 聚合」的空白，是 sysadmin/安全/隐私圈的常见推荐项。

## 套利机会分析

- **信息差**：不算被低估（33k star），但当下是「老牌头部 + 刚 Astro 重写复活 + star 重新加速」的二次曝光窗口，适合做内容选题。
- **技术借鉴**：「注册表驱动卡片 dashboard」「插件式 serverless 检查」「多部署适配器」「工具即教学」可迁移到任何聚合面板/SaaS。
- **生态位**：站长/运维想给自己网站做安全体检、开发者想探技术栈、隐私爱好者想自托管查站——这是最易用的开源选择。
- **趋势判断**：网站安全审计 + 自托管 + 隐私持续有需求，web-check 凭聚合 + 开源 + 品牌占标杆位；但外部依赖脆弱与单人节奏是变量。

## 风险与不足

- **⚠️ 外部依赖脆弱**：截图/地理位置/质量分等强依赖第三方 API/无头浏览器，最易坏（issues 实证），fix 负担高。
- **⚠️ 双用途（轻量）**：网站 OSINT 主要用于**给自己网站或授权目标做安全体检/合规审计（偏防御）**，分析的是公开信息（DNS/SSL/头/whois）；对他人站点做侦察须在合规/授权范围内。敏感度低于人肉类 OSINT。
- **单人 + 零测试 + 曾沉寂**：高度依赖 Alicia 一人，无自动化测试，曾 18 个月近停更。
- **重写过渡期**：Astro 迁移 + monorepo 仍在进行。
- **广而非深**：单项检查不如 SSL Labs 等专业工具深入权威。

## 行动建议

- **如果你要用它**：你想**一键给网站做全面体检/侦察**（安全头、SSL、技术栈、子域名、威胁、配置审计）——`web-check.xyz` 在线即用，或一键自托管（Docker 最省事，数据不出自己服务器）。在线版部分检查可能因外部 API 偶尔报错，自托管 + 配可选 API key 更稳。要单项极致权威用 SSL Labs/securityheaders.com；要重度 OSINT 侦察用 SpiderFoot。
- **如果你要学它**：重点读 `src/client/jobs/registry.ts`（检查注册表）+ `useJobs.ts`（任务调度）+ `Results.tsx`（卡片 dashboard）、`api/` 下任一检查（如 `ssl.js`/`headers.js`，看「URL→调外部 API→结构化 JSON」模式），以及多部署适配器配置。这是「注册表驱动聚合面板 + 插件式 serverless」的优秀样本。
- **如果你要 fork/贡献它**：最有价值的是加新检查（加 api/*.js + 注册卡片，零侵入）、加固外部 API 依赖的容错、补 PDF 报告导出（社区强需求），以及补测试。

### 知识入口

| 资源 | 链接 |
|------|------|
| 在线工具 | https://web-check.xyz （输入网址即出报告）｜ 镜像 web-check.as93.net |
| DeepWiki | https://deepwiki.com/Lissy93/web-check （已收录，含前端/后端 API/端点分层架构） |
| Zread.ai | 未确认（探测 403） |
| 关联论文 | 无（工程工具；引用 Tranco 排名研究） |
| 作者作品线 | [Dashy（自托管仪表盘）](https://github.com/Lissy93/dashy) ｜ [awesome-privacy](https://github.com/Lissy93/awesome-privacy) ｜ [who-dat（whois 微服务，被复用）](https://github.com/Lissy93/who-dat) |
| 同类 | domain-digger ｜ SpiderFoot ｜ 单项：SSL Labs / securityheaders.com / BuiltWith / urlscan.io |

# SEO-03 · Bing Webmaster Tools

**目标**：让 Bing / DuckDuckGo / ChatGPT Search / Yahoo（都用 Bing 索引）收录站点，并打开 IndexNow 提交统计。

**自动化等级**：🟡 **半自动** — 账号登录人工；之后 Claude 用 claude-in-chrome 操作。

## 关键加速：从 GSC 导入

Bing Webmaster 支持「**Import from Google Search Console**」一键导入已验证站点。**强烈建议先完成 [SEO-02](seo-02-google-search-console.md)**，然后这里 30 秒搞定。

## 流程

### 路径 A — 从 GSC 导入（推荐）

1. 登录 https://www.bing.com/webmasters
2. 顶部"导入"按钮 → 授权 Google 账号 → 选 GitHub Explorer 资源 → 一键导入（自动验证 + sitemap）
3. 设置完成

### 路径 B — 手动

1. 登录 → "添加站点" → 输入 `https://seeyeetech.com/github-explorer/`
2. 选验证方式：**Meta Tag**（最快，与 GSC 共用一个）
3. 复制 code → 告诉 Claude → Claude 填入 `SITE.verify.bing`（对应 `<meta name="msvalidate.01">`）
4. commit / push / 等部署 / 验证
5. Sitemaps → 提交 `sitemap-index.xml`

### Claude 接管（用 claude-in-chrome）

跟路径 A 适配最好 — 用户授权 Google 后整个流程自动；路径 B 同 [SEO-02](seo-02-google-search-console.md)。

## API 选项

Bing 有 [Webmaster API](https://learn.microsoft.com/en-us/bingwebmaster/getting-access)（需先去 API Key 页面拿 key）。可以纯 HTTP 调，无 OAuth。

但既然已经写了 [src/scripts/ping_search_engines.py](../../src/scripts/ping_search_engines.py) 用 IndexNow 推送，**Bing 这边 API 不必再加** — IndexNow 已经覆盖了 Bing 的"通知新 URL"需求。Bing Webmaster Tools 主要是用来**看数据**而非"推送 URL"。

## 验证

- Webmaster 页面显示已验证
- Sitemaps tab 显示 sitemap-index.xml 成功，URL 数 414
- 一周后 "IndexNow 提交" tab 应有 [SEO-01](seo-01-indexnow-setup.md) 推送的统计

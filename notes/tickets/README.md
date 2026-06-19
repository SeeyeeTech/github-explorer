# Tickets

SEO 上线后的待办工单。每条 ticket 标注三档自动化可行度：

- **🟢 全自动** — Claude 不需要人工干预即可完成
- **🟡 半自动** — 人工先做最少必要步骤（注册账号 / 输验证码），Claude 接管剩下的
- **🔴 必须手动** — 流程涉及实名 / 私密身份验证，无法代办

**Skill 现状**：搜过本地与官方 marketplace（`anthropic-agent-skills`、`chrome-devtools-plugins`、`claude-code-plugins` 等），**没有现成的 SEO 提交 / 站长平台对接 skill**。可考虑自建一个 `seo-publisher` skill 把这套流程产品化。

## 工单清单

| # | 工单 | 难度 | 自动化 |
|---|------|------|--------|
| [01](seo-01-indexnow-setup.md) | 启用 IndexNow（Bing + Yandex + AI 搜索） | 易 | 🟢 全自动 |
| [02](seo-02-google-search-console.md) | Google Search Console 验证 + 提交 sitemap | 中 | 🟡 半自动（Chrome） |
| [03](seo-03-bing-webmaster.md) | Bing Webmaster Tools 验证 + 提交 sitemap | 中 | 🟡 半自动（Chrome） |
| [04](seo-04-baidu-zhanzhang.md) | 百度站长平台验证 + 提交 sitemap + 拿推送 token | 难 | 🔴 必须手动（域名归属） |

## 共享前置

所有平台都需要："**SEO 升级方案已上线**" — 即至少 push 一次 main 让 GitHub Pages 重新构建，让以下三个 URL 可访问：

- `https://seeyeetech.com/github-explorer/sitemap-index.xml`
- `https://seeyeetech.com/github-explorer/robots.txt`
- `https://seeyeetech.com/github-explorer/rss.xml`

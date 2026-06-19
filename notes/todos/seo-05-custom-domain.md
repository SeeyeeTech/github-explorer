# TODO · 切自定义域名

**为什么必须做**：

1. **权重分散**：`seeyeetech.com/github-explorer/` 这种子路径，搜索引擎把 PageRank 算给 `github.io` 母域；母域上其他人的站也共享/竞争权重
2. **百度收录困难**：见 [SEO-04](../tickets/seo-04-baidu-zhanzhang.md) — 百度站长几乎不收录子路径
3. **品牌可记忆性**：`github-explorer.com` / `gex.tools` 比一串 github.io 路径好记一个数量级

## 决策需先做

- [ ] 域名选哪个？（建议 `.com` 或 `.io`；`.cn` 需备案）
- [ ] 是否做 ICP 备案？（备案 = 国内访问速度 + 百度收录权重，代价 ~15 工作日 + 主体材料）
- [ ] 用 Cloudflare 还是直连 GitHub Pages？（Cloudflare = 国内 CDN 略好 + 免费 SSL + Analytics）

## 切换步骤（域名买好后）

代码侧已经做了无缝切换准备：

1. **GitHub Pages 设置**：Settings → Pages → Custom domain 填 `域名` → 自动生成 CNAME → 开 HTTPS
2. **DNS**：域名注册商加 CNAME → `seeyeetech.com`
3. **改两个变量**（**唯一需要的代码动作**）：
   ```
   gh variable set SITE_URL --body "https://your-domain.com"
   gh variable set PUBLIC_BASE_PATH --body "/"
   ```
4. push 触发部署 → sitemap / robots / canonical / RSS / Feed 所有 URL 自动跟随新域名

## 旧 URL 重定向

GitHub Pages 切换 custom domain 后，旧的 `seeyeetech.com/github-explorer/*` 会 301 到新域，搜索权重逐步迁移（Google 6-8 周稳定，百度可能更慢）。

## 切完后的连锁动作

- [ ] 重做 [SEO-02 Google Search Console](../tickets/seo-02-google-search-console.md)：旧资源改成"地址变更"流程
- [ ] [SEO-03 Bing](../tickets/seo-03-bing-webmaster.md)：同样走地址变更
- [ ] **首次执行** [SEO-04 百度站长](../tickets/seo-04-baidu-zhanzhang.md)：之前不建议做的，现在做
- [ ] 公众号文章里如果有指向旧站的反向链接，逐步替换（可以新发文用新链接，旧文不动靠 301）

## 风险

- 切换的同时如果 robots.txt 配错，可能让搜索引擎一段时间无法抓取 → 先在新域名跑 24 小时本地验证 robots/sitemap 都正常再正式切
- HTTPS 证书 GitHub Pages 自动颁发，但 DNS 生效有延迟（最多 24h）

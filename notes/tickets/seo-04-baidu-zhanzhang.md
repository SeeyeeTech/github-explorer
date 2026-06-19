# SEO-04 · 百度站长平台

**目标**：让百度收录中文内容（中文搜索流量主力）+ 拿到推送 token 让 [src/scripts/ping_search_engines.py](../../src/scripts/ping_search_engines.py) 自动推。

**自动化等级**：🔴 **必须手动**（域名归属 + 当前 GitHub Pages 子路径百度收录困难）。

## 🚨 关键阻塞：当前 URL 形态对百度极不友好

百度站长平台对域名要求严格：

1. **不收录子路径**：`seeyeetech.com/github-explorer/` 这种二级路径，百度认定为 `seeyeetech.com` 域名下的内容，不会单独建索引；且 `github.io` 整个母域的权重被其他人共享
2. **域名归属验证**：百度要求验证域名的**所有权**（DNS / CNAME），但 `github.io` 子域名你没有 DNS 控制权
3. **ICP 备案敏感**：境外域名（含 github.io）百度抓取意愿低，收录速度慢一个数量级

**结论：百度站长这一项强烈建议先做完 [TODO 自定义域名](../todos/seo-06-custom-domain.md) 再来。** 否则即使验证成功，收录效果也很差。

## 假设：已完成自定义域名后的流程

### 阶段 A — 人工

1. 域名最好备案（国内访问速度 + 收录权重双重加成）
2. 登录 https://ziyuan.baidu.com（百度账号，可能需手机注册）
3. 添加网站 → 选 **CNAME / DNS** 验证（最稳）
4. 在域名 DNS 控制台加 CNAME 记录 → 等百度验证
5. 验证通过后："普通收录" tab → 拿到 token

### 阶段 B — Claude 接管

1. 用户贴 token → Claude 执行 `gh secret set BAIDU_PUSH_TOKEN --body "..."`
2. push 触发 `pages.yml` 的 `ping` job → 调 `src/scripts/ping_search_engines.py` 推送
3. 站长平台 → "推送日志" 查看接收数

### Claude + Chrome 模拟可行性

技术上可以，但百度站长有较强的人机校验（图形验证码）—— claude-in-chrome 自动化点击率会比 GSC 低很多。**只建议在用户登录好之后做 sitemap 提交那一步**，注册 + 域名验证全程人工。

## 不要做的事

- **不要用 HTML 文件验证法**：百度爬虫拉 GitHub Pages 经常超时
- **不要用 meta tag 验证法**：百度抓 meta 标签的更新延迟可达 7 天
- **不要现在就推**：当前 URL 形态推了也是浪费 token 配额

## 替代方案 — 神马搜索

如果短期不切自定义域名，可以试 [神马搜索站长](https://zhanzhang.sm.cn/)（UC + 阿里系，移动端搜索份额第二），对 github.io 的容忍度高一些。但流量价值远低于百度。

## 验证

- 站长后台 → "普通收录" → 推送配额每天上限正常（默认 10 条/天，加站后会涨）
- 一周后 → "索引量" 应开始有非零数据
- `site:seeyeetech.com/github-explorer/` 在百度搜索框能搜到结果（最起码首页）

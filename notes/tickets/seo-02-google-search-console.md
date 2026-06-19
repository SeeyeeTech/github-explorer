# SEO-02 · Google Search Console

**目标**：让 Google 收录 + 拿到搜索数据（覆盖率、查询词、CTR、排名）+ 提交 sitemap 加速首次抓取。

**自动化等级**：🟡 **半自动** — 账号登录必须人工（reCAPTCHA + 可能 2FA），之后 Claude 可用 claude-in-chrome 全程接管。

## 流程

### 阶段 A — 人工（约 5 分钟）

1. 浏览器开 https://search.google.com/search-console
2. 用你的 Google 账号登录（reCAPTCHA / 2FA 必须真人）
3. 走到"添加资源"，**选 URL 前缀**（因为是子路径部署，不能用 Domain 类型）
4. 输入：`https://seeyeetech.com/github-explorer/`
5. 选验证方式：**HTML 标记** → 复制 meta content 值

### 阶段 B — Claude 接管（用 claude-in-chrome 直接做）

跟 Claude 说"我贴 Google 验证 code，你填进去"。Claude 会：

1. 把 code 填到 `site/src/lib/data.ts` 的 `SITE.verify.google`
2. commit + push（用户授权）
3. 等 GitHub Pages 重建（~2 分钟）后，让用户在 GSC 页面点"验证"
4. 验证成功后，Claude 用 claude-in-chrome 自动：
   - 打开 GSC → Sitemaps 页面
   - 提交 `sitemap-index.xml`
   - 截图反馈

### 阶段 C — 完全可选的 API 化（长期）

GSC 有 [Search Console API](https://developers.google.com/webmaster-tools/v1/getting-started)。如果以后要做"自动提交 sitemap / 每周抓取数据"：

- 用 Service Account JSON key（无 OAuth 跳转）
- Repo Secret 加 `GSC_SERVICE_ACCOUNT_JSON`
- 写 `scripts/gsc_submit.py` 在 `pages.yml` 里调

但首次设置仍要 Web 登录授权 service account 访问该资源，所以这步本身**没法跳过 Web 操作**。

## Claude + Chrome 模拟可行性

完全可行。已确认本环境有 `mcp__claude-in-chrome__*` 工具。建议流程：

```
用户：登录好 GSC 了，已经选了"添加资源"那一页
→ Claude: tabs_context_mcp 找到这个 tab
→ Claude: form_input 填资源 URL
→ Claude: find "选择 HTML 标记" 切换验证方式
→ Claude: get_page_text 拿到 meta code
→ Claude: 填入 data.ts 并提示 commit
→ 等部署 → 用户回 GSC 点验证
→ Claude: 切到 Sitemaps 页 → form_input 提交 sitemap URL
```

注意事项（来自系统约束）：
- **不要触发 alert/confirm dialog**（会卡住 extension）
- 操作前先 `tabs_context_mcp` 拿真实 tab id，别复用历史
- 多步操作建议 `gif_creator` 录屏便于复盘

## 验证

- GSC → 资源 → 该站显示"已验证"
- Sitemaps 页面显示 `sitemap-index.xml` 状态"成功"，抓取 414 个 URL
- 24 小时后 GSC → 覆盖率 应开始有数据

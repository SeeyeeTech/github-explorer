# SEO-01 · 启用 IndexNow

**目标**：每篇新报告 5 分钟内推到 Bing / Yandex / Naver / Seznam / ChatGPT Search 等。

**自动化等级**：🟢 **全自动** — IndexNow 不需要账号，任何人生成一个 UUID 当 key 即可。

## 流程

1. 生成 UUID（任意 v4）作为 IndexNow key — 用 `uuidgen` 或 `python3 -c "import uuid; print(uuid.uuid4().hex)"`
2. 在 `site/public/` 写一个 `{KEY}.txt` 文件，**文件内容就是 key 本身**（IndexNow 通过 HTTP 拉这个文件校验所有权）
3. 把 key 加到 GitHub 仓库 secret：`gh secret set INDEXNOW_KEY --body "{KEY}"`
4. 推 main 触发 `pages.yml`；deploy 后 `ping` job 会自动调 `src/scripts/ping_search_engines.py` 推送

## Claude 可直接执行

无需任何人工。准备好就跟 Claude 说"启用 IndexNow"：

```
1. 生成 UUID 作为 key
2. 写 site/public/{key}.txt
3. 提示用户跑：gh secret set INDEXNOW_KEY --body "{key}"   ← 这一步需要用户授权
4. （或：用户在 Settings → Secrets Web UI 自己填）
5. commit + push（用户授权 commit/push 后 Claude 可完成）
```

## 验证

部署后：
- 浏览器访问 `https://seeyeetech.com/github-explorer/{KEY}.txt` 应返回 key 本身
- 看 `pages.yml` 的 `ping` job 日志，应有：`[indexnow] HTTP 202 Accepted`
- 一周后查 Bing Webmaster 的"IndexNow 提交"统计

## 已知约束

- IndexNow 不对应 Google（Google 拒绝加入），所以 [02](seo-02-google-search-console.md) 仍要做
- 同一 key 一次最多推 10000 URL（远超 374 报告）
- 文档：https://www.indexnow.org/documentation

---
name: md2wechat
description: >-
  Use when publishing Markdown articles to WeChat Official Account - handles
  quote formatting, markdown lint, MD-to-HTML conversion, and optional API
  publishing with Unsplash cover image
allowed-tools: 'Bash(python3:*), Bash(bunx:*), Bash(curl:*), Read, Write, Edit, Grep, Glob'
metadata:
  author: ouyang
  version: 1.1.0
  license: MIT
  title: Markdown 转微信公众号
  description_zh: 将 Markdown 文档格式化并发布到微信公众号，支持引号替换、lint 修复、HTML 转换，以及通过 API
---

# md2wechat

## Overview

将 Markdown 文档格式化并转换为微信公众号兼容的 HTML，支持直接复制粘贴或通过 API 发布到草稿箱。

## When to Use

- 用户要将 Markdown 文章发布到微信公众号
- 用户要将 Markdown 转换为微信兼容的 HTML
- 用户提到「公众号发布」「微信排版」「md 转微信」

**不要用于：**
- 非微信平台的 HTML 转换
- 纯文本编辑（无发布意图）

## Quick Reference

| 操作 | 方法 |
|------|------|
| 格式化引号 | 替换 `""` 为 `「」`，替换 `【】` 为 `「」` |
| Lint 修复 | `bunx @lint-md/cli <filepath> --fix` |
| 加粗关键点 | 每段 1-2 处核心观点加 `**` |
| 转换 HTML | 读取 `assets/wechat.css`，按规则手动转换 |
| API 发布 | 参考 `references/wechat-api.md` |

## Step 1: 格式化 Markdown

### 1.1 替换引号和括号

统一为直角引号 `「」`，需要替换两类符号：

1. **中文双引号** `\u201c\u201d`（即 `""` ）→ `「」`
2. **中文方括号** `【】` → `「」`

使用 Edit 工具的 `replace_all` 模式批量替换，共四次操作：
- `"` → `「`
- `"` → `」`
- `【` → `「`
- `】` → `」`

**注意**：替换前先检查文中是否已有 `「」`（如小结部分），避免双重替换。

### 1.2 Lint 修复

执行中文 Markdown 规范检查与自动修复：

```bash
bunx @lint-md/cli <filepath> --fix
```

lint-md 会自动处理中英文间距、标点规范等。执行后需重新 Read 文件，因为内容已被修改。

### 1.3 加粗关键点（可选）

在转换 HTML 之前，为文章中需要强调的核心观点添加 `**加粗**`。

**原则：**
- 每个段落/技巧最多加粗 1-2 处，不过度
- 优先加粗：核心主张、反直觉洞见、关键规则/数字、记忆点强的排比句
- 标点符号放在 `**` 之外，如 `**核心观点**。` 而非 `**核心观点。**`

**操作方式：** 先通读全文识别关键点，再逐一用 Edit 工具添加。完成后列出加粗清单供用户确认。

## Step 2: 转换为微信 HTML

### 转换规则

1. **不渲染 h1 标题** — 标题在微信编辑器中单独设置
2. **使用 `<style>` 内嵌 CSS** — 从 `assets/wechat.css` 读取样式
3. **输出 HTML 到 Markdown 同目录**，文件名与 md 相同，扩展名改为 `.html`

### HTML 结构模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
/* 从 assets/wechat.css 读取并嵌入 */
</style>
</head>
<body>
<!-- 转换后的 HTML 内容，不含 h1 -->
</body>
</html>
```

### Markdown → HTML 转换映射

| Markdown | HTML | 注意 |
|----------|------|------|
| `# 标题` | 跳过不渲染 | 标题在微信编辑器设置 |
| `## 小节` | `<h2>小节</h2>` | 居中、红色 |
| `### 编号` | `<h3>编号</h3>` | 左对齐、加粗、黑色 |
| 段落 | `<p>文字</p>` | 两端对齐 |
| 段落内换行 | `<p>行1<br/>行2</p>` | 同段落内用 `<br/>` |
| `**加粗**` | `<strong>加粗</strong>` | 标点在 `</strong>` 之外 |
| `* 列表项` / `- 列表项` | `<ul><li>列表项</li></ul>` | 两种写法都要处理 |
| `> 引用` | `<blockquote><p>引用</p></blockquote>` | — |
| `https://url` | `<a href="url">url</a>` | 裸链接转为可点击 |
| `[文字](url)` | `<a href="url">文字</a>` | 标准链接语法 |
| `` `代码` `` | 直接输出文字，去掉反引号 | 微信不支持 inline code 样式 |
| 空行 | 段落分隔 | 不生成空标签 |

### 特殊处理

- 连续非空行属于同一段落，行间用 `<br/>` 连接
- `**text**` 转为 `<strong>text</strong>`，标点符号在 `</strong>` 之外
- 列表项的 `**加粗前缀**` 需保留 `<strong>` 标签
- blockquote 内的段落使用 `blockquote > p` 样式（无 padding）
- 裸 URL（独占一行的 `https://...`）转为 `<a>` 标签

## Step 3: 发布

提供三种发布方式，询问用户选择。**CI / 无人值守场景必须用方式三。**

### 方式一：复制粘贴（默认）

1. 告知用户 HTML 文件已生成
2. 用户在浏览器中打开 HTML 文件
3. 全选页面内容（Cmd+A），复制（Cmd+C）
4. 粘贴到微信公众号后台编辑器

### 方式三：CI 模式（推荐用于自动化）

**只输出文件，不调用任何微信 API**。后续由独立的 `scripts/wechat_publish.py` 读这些文件、走反代发布。

输出两个产物到 `src/analysis_report/`：

1. **`{slug}.html`** — 已经转换好的微信兼容 HTML（同方式一）
2. **`{slug}.meta.json`** — 发布元数据，结构如下：

   ```json
   {
     "title": "Gin 深度分析报告",
     "digest": "Gin 是 Go 生态最流行的 HTTP 框架… (≤120 字)",
     "author": "NVoyager",
     "theme": "stars,universe,dark"
   }
   ```

   字段含义：
   - `title`：文章标题，≤ 64 字符（微信限制）
   - `digest`：摘要，**≤ 120 字符**，从正文提炼 1-2 句核心观点
   - `author`：作者名（可空）
   - `theme`：封面图主题词，逗号分隔，从 `stars / universe / ocean / desert / forest / green-trees / dark` 等任挑组合

**不要做的事**：
- 不要 curl 任何 `*.weixin.qq.com` 接口
- 不要 curl `wx.nightvoyager.top`
- 不要尝试用 helper 函数发请求
- 一切发布动作都由后续的 Python 脚本完成

### 方式二：API 发布到草稿箱（仅交互式手动场景）

需要环境变量（从项目根目录 `.env` 文件或系统环境变量读取）：

```
WECHAT_APPID=your_appid
WECHAT_APPSECRET=your_appsecret

# 可选：经反代访问微信 API（用于固定出口 IP 命中白名单的 CI 场景）
# WECHAT_API_BASE=https://wx.your-proxy.example.com   # 留空则默认 https://api.weixin.qq.com
# WECHAT_PROXY_TOKEN=...                              # 反代要求 X-Proxy-Token 头时填
```

调用所有微信接口前先准备好两个 helper（详见 `references/wechat-api.md`）：

```bash
WECHAT_API_BASE="${WECHAT_API_BASE:-https://api.weixin.qq.com}"
PROXY_HEADER=()
[[ -n "${WECHAT_PROXY_TOKEN:-}" ]] && PROXY_HEADER=(-H "X-Proxy-Token: ${WECHAT_PROXY_TOKEN}")
```

然后每个 curl 写成 `curl "${PROXY_HEADER[@]}" "${WECHAT_API_BASE}/cgi-bin/..."`。**禁止直接拼接 `https://api.weixin.qq.com`**。

流程：

1. **获取 access_token** — 调用微信 token 接口
2. **获取封面图** — 从 Unsplash 随机获取暗色调图片（主题词轮换：stars, universe, ocean, desert, forest, green-trees）
3. **上传封面图** — 上传到微信素材库，获取 media_id
4. **生成摘要** — 从文章内容提炼 1-2 句核心观点，不超过 120 字
5. **发布到草稿箱** — 调用草稿箱 API

详细 API 参考见 `references/wechat-api.md`。

**摘要生成规则：**
- 从文章中提炼 1-2 句核心观点
- 不超过 120 字
- 风格简洁有力，呼应文章主题

## Common Mistakes

| 错误 | 为何失败 | 修复 |
|------|----------|------|
| HTML 中保留 h1 | 微信编辑器有独立标题字段 | 默认跳过 h1 |
| CSS 用 class 选择器 | 微信会清除 class 属性 | 使用标签选择器 |
| 只替换 `""` 不替换 `【】` | 同一篇文章中括号类型不统一 | Step 1 两类都替换 |
| lint-md 后未重新读取文件 | lint 会修改文件内容（如中英文间距），后续编辑基于旧内容会冲突 | lint 后必须 Read |
| 加粗过度 | 全篇加粗等于没加粗 | 每段最多 1-2 处 |
| 裸 URL 未转链接 | HTML 中纯文本 URL 不可点击 | 转为 `<a>` 标签 |
| access_token 过期 | 有效期 2 小时 | 每次重新获取 |
| 封面图比例不对 | 微信推荐 2.35:1 | 使用 900x383 px |
| 段落内换行用空行 | 会产生多个 `<p>` | 连续行用 `<br/>` |

## Resources

- `assets/wechat.css` - 微信公众号排版 CSS 样式模板
- `references/wechat-api.md` - 微信公众号 API 接口文档（token、素材、草稿箱）

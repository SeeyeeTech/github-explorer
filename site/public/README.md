# site/public/ 静态资源

构建时被原样复制到 `dist/`。

## SEO 资源占位

| 文件 | 用途 | 替换方式 |
|---|---|---|
| `favicon.svg` | 站点图标 | 想换品牌图直接覆盖 |
| `og-default.png` | 默认社交分享卡（1200x630） | 设计师产出后覆盖；reports 仓库 OG 由 `getReportOgImage()` 借用 GitHub 自动生成图，不依赖本文件 |

## 站长平台验证文件

不同平台校验方式不一样，**两种途径任选其一**：

1. **HTML meta 法**（推荐）— 拿到 code 后填入 `site/src/lib/data.ts` 的 `SITE.verify` 三个字段，`Base.astro` 自动渲染对应 meta
2. **HTML 文件法** — 平台给你一个文件名（如 `googleXXXXX.html`、`baidu_verify_XXXXX.html`、`BingSiteAuth.xml`），直接放到本目录即可被 GitHub Pages 提供出去

## IndexNow Key 文件

启用 IndexNow 推送（Bing/Yandex/AI 搜索）后，需要在本目录放一个 `{KEY}.txt` 文件，内容就是 KEY 本身。`scripts/ping_search_engines.py` 启动时会从环境变量 `INDEXNOW_KEY` 读 key 并校验。

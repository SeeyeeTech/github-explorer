import { defineConfig } from "astro/config";
import preact from "@astrojs/preact";
import sitemap from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";
import fs from "node:fs";
import path from "node:path";

// GitHub Pages 部署到 SeeyeeTech/github-explorer
// 仓库子路径 → site + base 必须配对；都允许通过 env 覆盖以便切换自定义域名
// 用 || 而非 ??：CI 上 env 可能传空字符串，?? 不会 fallback
const siteUrl = process.env.SITE_URL || "https://seeyeetech.com";
const repoBase = process.env.PUBLIC_BASE_PATH || "/github-explorer";

// 构建期读取 reports.json，用 mtime 为报告 URL 注入 lastmod
function loadReportMtimeIndex() {
  try {
    const file = path.resolve("../src/data/reports.json");
    const list = JSON.parse(fs.readFileSync(file, "utf-8"));
    const map = new Map();
    for (const r of list) {
      if (r.slug && r.mtime) map.set(r.slug, r.mtime);
    }
    return map;
  } catch {
    return new Map();
  }
}
const REPORT_MTIME = loadReportMtimeIndex();

// 不参与 SEO 的页面（交互表单 / 查询参数页）
const SITEMAP_EXCLUDE = ["/submit", "/submit/"];

export default defineConfig({
  site: siteUrl,
  base: repoBase,
  trailingSlash: "ignore",
  integrations: [
    preact(),
    sitemap({
      filter: (url) => !SITEMAP_EXCLUDE.some((p) => url.endsWith(p) || url.endsWith(`${p}/`)),
      changefreq: "weekly",
      priority: 0.7,
      serialize(item) {
        // 统一无尾斜杠（除根路径），匹配 canonical 与 absoluteUrl()
        const u = new URL(item.url);
        const p = u.pathname.replace(/\/$/, "");
        if (p && p !== repoBase.replace(/\/$/, "")) {
          item.url = `${u.origin}${p}`;
        }
        // 报告详情：/{base}/reports/{slug}
        const reportMatch = p.match(/\/reports\/([^/]+)$/);
        if (reportMatch && reportMatch[1] !== "reports") {
          const mtime = REPORT_MTIME.get(reportMatch[1]);
          if (mtime) item.lastmod = new Date(mtime).toISOString();
          item.changefreq = "monthly";
          item.priority = 0.8;
          return item;
        }
        if (p.endsWith("/reports")) {
          item.changefreq = "daily";
          item.priority = 0.9;
          return item;
        }
        // AI 日报详情：/{base}/daily/{date}
        const dailyMatch = p.match(/\/daily\/([^/]+)$/);
        if (dailyMatch && dailyMatch[1] !== "daily") {
          item.changefreq = "monthly";
          item.priority = 0.7;
          return item;
        }
        if (p.endsWith("/daily")) {
          item.changefreq = "daily";
          item.priority = 0.8;
          return item;
        }
        if (p.endsWith(repoBase) || p === "" || p === repoBase.replace(/\/$/, "")) {
          item.changefreq = "daily";
          item.priority = 1.0;
          return item;
        }
        if (p.includes("/tags/")) {
          item.changefreq = "weekly";
          item.priority = 0.6;
          return item;
        }
        if (p.endsWith("/tags")) {
          item.changefreq = "weekly";
          item.priority = 0.5;
          return item;
        }
        if (p.includes("/starred")) {
          item.changefreq = "monthly";
          item.priority = 0.4;
          return item;
        }
        if (p.endsWith("/trending")) {
          item.changefreq = "daily";
          item.priority = 0.7;
          return item;
        }
        return item;
      },
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
  markdown: {
    shikiConfig: {
      theme: "github-light",
      wrap: true,
    },
  },
});

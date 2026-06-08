import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

// 报告内容集合：直接从仓库根的 src/analysis_report 加载 375 篇 .md（不需要 frontmatter）
// 站点构建时会用 reports.json 元数据反查注入 stars / language / tags 等字段。
const reports = defineCollection({
  loader: glob({
    // 排除非报告：repos.md（待分析队列）、README、phase3 中间产物等可加到此处
    pattern: ["**/*.md", "!repos.md", "!README.md"],
    base: "../src/analysis_report",
  }),
  // 报告原文无 frontmatter，全部字段允许缺失
  schema: z.object({}).passthrough(),
});

// AI 日报 · 开源生态篇：从 src/daily_report 加载（带 YAML frontmatter）。
// 篇B（frontier）落在 src/ai_news，不进站点，故此处只 glob daily_report。
const daily = defineCollection({
  loader: glob({
    pattern: ["**/*.md", "!README.md"],
    base: "../src/daily_report",
  }),
  schema: z
    .object({
      title: z.string().optional(),
      date: z.string().optional(),
      summary: z.string().optional(),
      tags: z.array(z.string()).optional(),
      canonical_url: z.string().optional(),
      syndicate: z.union([z.boolean(), z.array(z.string())]).optional(),
    })
    .passthrough(),
});

export const collections = { reports, daily };

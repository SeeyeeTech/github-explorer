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

export const collections = { reports };

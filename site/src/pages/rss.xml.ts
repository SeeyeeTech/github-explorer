import rss from "@astrojs/rss";
import type { APIContext } from "astro";
import { SITE, absoluteUrl, getReports, getTagsDoc, getTagLabels } from "~/lib/data";

export async function GET(_ctx: APIContext) {
  const reports = getReports();
  const tagsDoc = getTagsDoc();
  const labels = getTagLabels();

  // 取按 mtime 倒序的前 50 篇 — RSS 主要服务订阅者和爬虫发现新内容
  const items = [...reports]
    .filter((r) => r.mtime)
    .sort((a, b) => (a.mtime > b.mtime ? -1 : 1))
    .slice(0, 50)
    .map((r) => ({
      title: r.title ?? r.slug,
      description: r.summary ?? "",
      link: absoluteUrl(`/reports/${r.slug}`),
      pubDate: new Date(r.mtime),
      categories: (tagsDoc.entries[r.slug] ?? [])
        .filter((t) => t !== "uncategorized")
        .map((t) => labels[t] ?? t),
    }));

  return rss({
    title: SITE.rssTitle,
    description: SITE.description,
    site: absoluteUrl("/"),
    items,
    customData: `<language>zh-CN</language><docs>https://www.rssboard.org/rss-specification</docs>`,
    stylesheet: false,
  });
}

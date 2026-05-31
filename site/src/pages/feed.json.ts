import type { APIContext } from "astro";
import { SITE, absoluteUrl, getReports, getTagsDoc, getTagLabels } from "~/lib/data";

// JSON Feed 1.1 — https://www.jsonfeed.org/version/1.1/
export async function GET(_ctx: APIContext) {
  const reports = getReports();
  const tagsDoc = getTagsDoc();
  const labels = getTagLabels();

  const items = [...reports]
    .filter((r) => r.mtime)
    .sort((a, b) => (a.mtime > b.mtime ? -1 : 1))
    .slice(0, 50)
    .map((r) => {
      const url = absoluteUrl(`/reports/${r.slug}`);
      const tags = (tagsDoc.entries[r.slug] ?? [])
        .filter((t) => t !== "uncategorized")
        .map((t) => labels[t] ?? t);
      return {
        id: url,
        url,
        title: r.title ?? r.slug,
        summary: r.summary ?? undefined,
        content_text: r.summary ?? "",
        date_published: new Date(r.mtime).toISOString(),
        date_modified: new Date(r.mtime).toISOString(),
        tags,
        external_url: r.originalUrl ?? undefined,
      };
    });

  const feed = {
    version: "https://jsonfeed.org/version/1.1",
    title: SITE.rssTitle,
    home_page_url: absoluteUrl("/"),
    feed_url: absoluteUrl("/feed.json"),
    description: SITE.description,
    language: "zh-CN",
    icon: absoluteUrl(SITE.defaultOgImage),
    authors: [{ name: SITE.ownerHandle, url: SITE.repoUrl }],
    items,
  };

  return new Response(JSON.stringify(feed, null, 2), {
    headers: { "Content-Type": "application/feed+json; charset=utf-8" },
  });
}

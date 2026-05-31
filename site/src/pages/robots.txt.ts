import type { APIContext } from "astro";
import { absoluteUrl } from "~/lib/data";

// 动态生成 robots.txt — 自动跟随 SITE_URL / BASE_PATH 切换
export async function GET(_ctx: APIContext) {
  const sitemapUrl = absoluteUrl("/sitemap-index.xml");
  const submitUrl = absoluteUrl("/submit");
  const body = [
    "User-agent: *",
    "Allow: /",
    `Disallow: ${new URL(submitUrl).pathname}`,
    "",
    `Sitemap: ${sitemapUrl}`,
    "",
  ].join("\n");

  return new Response(body, {
    headers: { "Content-Type": "text/plain; charset=utf-8" },
  });
}

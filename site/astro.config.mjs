import { defineConfig } from "astro/config";
import preact from "@astrojs/preact";
import sitemap from "@astrojs/sitemap";
import tailwindcss from "@tailwindcss/vite";

// GitHub Pages 部署到 AustinXT/github-explorer
// 仓库子路径 → site + base 必须配对
const repoBase = process.env.PUBLIC_BASE_PATH ?? "/github-explorer";

export default defineConfig({
  site: "https://austinxt.github.io",
  base: repoBase,
  trailingSlash: "ignore",
  integrations: [preact(), sitemap()],
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

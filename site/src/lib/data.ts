// 站点构建时数据加载工具：把 src/data/*.{json,yaml} 包装成类型化 API
import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";

const DATA_DIR = path.resolve(import.meta.dirname, "../../../src/data");

export interface ReportMeta {
  slug: string;
  title: string;
  originalUrl: string | null;
  summary: string | null;
  highlights: string[];
  stars: number | null;
  forks: number | null;
  language: string | null;
  locRaw: string | null;
  ageMonths: number | null;
  ageRaw: string | null;
  stage: string | null;
  contribution: string | null;
  heat: string | null;
  heatRaw: string | null;
  quality: string | null;
  license: string | null;
  cover: string | null;
  mtime: string;
  published: string | null;
  publishedTitle: string | null;
}

export interface TagsDoc {
  manual: string[];
  entries: Record<string, string[]>;
}

interface TagRule {
  tag: string;
  label?: string;
  match: string[];
}

export interface UsersDoc {
  users: Array<{
    login: string;
    name: string;
    bio?: string;
    tags?: string[];
  }>;
}

export interface StarredDoc {
  users: Array<{
    login: string;
    name: string;
    bio?: string;
    tags?: string[];
    fetchedAt: string | null;
    rangeStart: string | null;
    items: Array<{
      name: string;
      url: string;
      stars: number;
      description: string;
      starredAt: string;
      reportSlug?: string;
    }>;
  }>;
}

interface TrendingItem {
  name: string;
  url: string;
  language: string;
  stars: number;
  forks: number;
  description: string;
  last_seen?: string;
  trending_days?: number;
}

export interface TrendingConfig {
  fetch_window: { start_date: string; end_date: string };
  archive_source: string;
  all_repos_min_trending_days: number;
  display: {
    homepage_top_n: number;
    trending_page_per_tab: number;
    default_tab: "daily" | "weekly" | "monthly";
  };
}

function readJson<T>(name: string): T {
  return JSON.parse(fs.readFileSync(path.join(DATA_DIR, name), "utf-8")) as T;
}

function readYaml<T>(name: string): T {
  return yaml.load(fs.readFileSync(path.join(DATA_DIR, name), "utf-8")) as T;
}

let _reports: ReportMeta[] | null = null;
export function getReports(): ReportMeta[] {
  if (!_reports) _reports = readJson<ReportMeta[]>("reports.json");
  return _reports;
}

let _tags: TagsDoc | null = null;
export function getTagsDoc(): TagsDoc {
  if (!_tags) _tags = readYaml<TagsDoc>("tags.yaml");
  return _tags;
}

let _tagRules: TagRule[] | null = null;
export function getTagRules(): TagRule[] {
  if (!_tagRules) _tagRules = readYaml<TagRule[]>("tag-rules.yaml");
  return _tagRules;
}

export function getTagLabels(): Record<string, string> {
  const out: Record<string, string> = { uncategorized: "未分类" };
  for (const r of getTagRules()) out[r.tag] = r.label ?? r.tag;
  return out;
}

let _users: UsersDoc | null = null;
export function getUsers(): UsersDoc {
  if (!_users) _users = readYaml<UsersDoc>("users.yaml");
  return _users;
}

let _starred: StarredDoc | null = null;
export function getStarred(): StarredDoc {
  if (!_starred) _starred = readJson<StarredDoc>("starred.json");
  return _starred;
}

let _trendingConfig: TrendingConfig | null = null;
export function getTrendingConfig(): TrendingConfig {
  if (!_trendingConfig) _trendingConfig = readYaml<TrendingConfig>("trending-config.yaml");
  return _trendingConfig;
}

const TRENDING_DIR = path.resolve(import.meta.dirname, "../../../src/trending_repo");

export function getTrendingAggregate(): TrendingItem[] {
  const file = path.join(TRENDING_DIR, "all_repos_deduped.json");
  if (!fs.existsSync(file)) return [];
  return JSON.parse(fs.readFileSync(file, "utf-8")) as TrendingItem[];
}

// 从 src/data/trending_snapshots.jsonl 派生各周期榜单（每行自带完整字段）。
// 语义复刻原"逐期 JSON 倒序 + 按 url 去重 + 每 tab ≤200"。
let _trendingByPeriod: Record<string, TrendingItem[]> | null = null;
function loadTrendingByPeriod(): Record<string, TrendingItem[]> {
  if (_trendingByPeriod) return _trendingByPeriod;
  const file = path.join(DATA_DIR, "trending_snapshots.jsonl");
  const grouped: Record<string, Array<{ key: string; rank: number; item: TrendingItem }>> = {
    daily: [],
    weekly: [],
    monthly: [],
  };
  if (fs.existsSync(file)) {
    for (const line of fs.readFileSync(file, "utf-8").split("\n")) {
      const s = line.trim();
      if (!s) continue;
      const r = JSON.parse(s) as {
        period_type: string;
        period_key: string;
        rank: number;
        name: string;
        url: string;
        language: string;
        stars: number;
        forks: number;
        description: string;
      };
      const bucket = grouped[r.period_type];
      if (!bucket) continue;
      bucket.push({
        key: r.period_key,
        rank: r.rank,
        item: { name: r.name, url: r.url, language: r.language, stars: r.stars, forks: r.forks, description: r.description },
      });
    }
  }
  const out: Record<string, TrendingItem[]> = {};
  for (const [period, rows] of Object.entries(grouped)) {
    rows.sort((a, b) => (a.key < b.key ? 1 : a.key > b.key ? -1 : a.rank - b.rank));
    const seen = new Set<string>();
    const items: TrendingItem[] = [];
    for (const r of rows) {
      if (seen.has(r.item.url)) continue;
      seen.add(r.item.url);
      items.push(r.item);
      if (items.length >= 200) break;
    }
    out[period] = items;
  }
  _trendingByPeriod = out;
  return out;
}

export function getTrendingByPeriod(period: "daily" | "weekly" | "monthly"): TrendingItem[] {
  return loadTrendingByPeriod()[period] ?? [];
}

// AI 日报 · 开源生态篇（篇A）索引：读 daily_digests.jsonl，只取 type=ecosystem（篇B 不上站）
export interface DailyDigest {
  date: string;
  slug: string;
  title: string;
  summary: string | null;
  sections: Record<string, number> | null;
  featuredUrls: string[];
}

let _daily: DailyDigest[] | null = null;
export function getDailyDigests(): DailyDigest[] {
  if (_daily) return _daily;
  const file = path.join(DATA_DIR, "daily_digests.jsonl");
  const out: DailyDigest[] = [];
  if (fs.existsSync(file)) {
    for (const line of fs.readFileSync(file, "utf-8").split("\n")) {
      const s = line.trim();
      if (!s) continue;
      try {
        const r = JSON.parse(s) as {
          type?: string;
          date?: string;
          slug?: string;
          title?: string;
          summary?: string | null;
          sections?: Record<string, number> | null;
          featured_urls?: string[];
        };
        if (r.type !== "ecosystem" || !r.date) continue;
        out.push({
          date: r.date,
          slug: r.slug ?? r.date,
          title: r.title ?? r.date,
          summary: r.summary ?? null,
          sections: r.sections ?? null,
          featuredUrls: r.featured_urls ?? [],
        });
      } catch {
        // 容错坏行，不让单条脏数据拖垮构建
      }
    }
  }
  out.sort((a, b) => (a.date > b.date ? -1 : a.date < b.date ? 1 : 0));
  _daily = out;
  return out;
}

// 报告 URL → slug 反查（用于 trending/starred 高亮已分析）
let _urlIndex: Map<string, string> | null = null;
export function getAnalyzedUrlIndex(): Map<string, string> {
  if (_urlIndex) return _urlIndex;
  _urlIndex = new Map();
  for (const r of getReports()) {
    if (r.originalUrl) _urlIndex.set(r.originalUrl.replace(/\/$/, ""), r.slug);
  }
  return _urlIndex;
}

// 站点元信息（写死，避免再加 site.yaml）
// SITE_URL/BASE_PATH 在 astro.config.mjs 已经 env 化；这里 siteUrl/basePath 提供运行时只读快照
const SITE_URL = (import.meta.env.SITE ?? "https://seeyeetech.com").replace(/\/$/, "");
const BASE_PATH = (import.meta.env.BASE_URL ?? "/").replace(/\/$/, "");

export const SITE = {
  title: "GitHub Explorer",
  subtitle: "深度挖掘 GitHub 仓库价值",
  description:
    "375+ 篇 GitHub 仓库深度分析报告，覆盖 AI Agent、LLM、DevTools 等热门赛道；含每日 Trending 榜与大牛 Star 订阅。",
  repoUrl: "https://github.com/SeeyeeTech/github-explorer",
  ownerHandle: "NVoyager",
  // SEO / 社交分享
  siteUrl: SITE_URL,
  basePath: BASE_PATH,
  locale: "zh_CN",
  defaultOgImage: "/og-default.png",
  keywords: [
    "GitHub 仓库分析",
    "GitHub Trending",
    "开源项目评测",
    "AI Agent",
    "LLM",
    "开发者工具",
    "技术选型",
  ],
  // 站长平台验证 code；拿到后填入，空字符串则不渲染对应 meta
  verify: {
    google: "",
    baidu: "",
    bing: "",
  },
  rssTitle: "GitHub Explorer · 最新报告",
  // 微信公众号引导关注；qr 相对 public 根，组件内拼 BASE_URL
  wechat: {
    name: "智能时代蛮子",
    qr: "/wechat-qr.png",
  },
};

// 拼接绝对 URL（自带 base 子路径），用于 canonical / og:url / sitemap 等
// 规范化：根路径保留尾斜杠，其他路径统一去掉尾斜杠
export function absoluteUrl(path: string = "/"): string {
  const p = path.startsWith("/") ? path : `/${path}`;
  const joined = `${SITE.siteUrl}${SITE.basePath}${p}`.replace(/([^:])\/{2,}/g, "$1/");
  if (joined.endsWith(`${SITE.basePath}/`) || joined === `${SITE.siteUrl}/`) return joined;
  return joined.replace(/\/$/, "");
}

// 报告社交分享卡片图：有 GitHub URL 就借用 GitHub Repository OG（每月自动更新、无成本）
// 形如 https://opengraph.githubassets.com/{hash}/{owner}/{repo} —— hash 任意，GitHub 用其失效缓存
export function getReportOgImage(report: { originalUrl?: string | null } | undefined | null): string {
  if (report?.originalUrl) {
    const m = report.originalUrl.match(/github\.com\/([^/]+)\/([^/]+?)(?:\.git)?\/?$/);
    if (m) {
      // 用 mtime 衍生的简单 hash 让 GitHub 缓存随报告更新而刷新
      return `https://opengraph.githubassets.com/main/${m[1]}/${m[2]}`;
    }
  }
  return absoluteUrl(SITE.defaultOgImage);
}

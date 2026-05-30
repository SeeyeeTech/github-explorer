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

export function getTrendingByPeriod(period: "daily" | "weekly" | "monthly"): TrendingItem[] {
  const dir = path.join(TRENDING_DIR, period);
  if (!fs.existsSync(dir)) return [];
  const files = fs.readdirSync(dir).filter((f) => f.endsWith(".json")).sort().reverse();
  const seen = new Set<string>();
  const out: TrendingItem[] = [];
  for (const f of files) {
    const items = JSON.parse(fs.readFileSync(path.join(dir, f), "utf-8")) as TrendingItem[];
    for (const item of items) {
      if (!seen.has(item.url)) {
        seen.add(item.url);
        out.push(item);
      }
    }
    if (out.length >= 200) break; // 每个 tab 最多 200，避免过大
  }
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
export const SITE = {
  title: "GitHub Explorer",
  subtitle: "深度挖掘 GitHub 仓库价值",
  description:
    "375+ 篇 GitHub 仓库深度分析报告，覆盖 AI Agent、LLM、DevTools 等热门赛道；含每日 Trending 榜与大牛 Star 订阅。",
  repoUrl: "https://github.com/AustinXT/github-explorer",
  ownerHandle: "AustinXT",
};

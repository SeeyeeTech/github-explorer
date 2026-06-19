"""一文多发框架的共享地基：数据模型 + adapter 抽象 + 注册表 + 报告解析。

设计目标：把现有「单渠道公众号发布」泛化成「一份报告 → 多个渠道」。
新接一个平台 = 写一个 BaseAdapter 子类并 @register，无需改主流程。

约定（与现有管线对齐，不另起一套）：
  - slug          报告文件名 stem 小写（同 wechat_publish.py / build_reports_index.py）
  - canonical_url 站点报告页 SITE_URL + BASE_PATH + /reports/{slug}/，
                  作为 SEO 正本回链 + 导流落点（POSSE：自有站点是正本，外发是 silo）
  - 发布历史      写 src/data/publish_history.jsonl（append-only SoR，入 Git，带 channel 维度）
  - 凭据          放 .env.local（不入 Git，自动加载，不覆盖已有 env），见各 adapter 文档
"""
from __future__ import annotations

import json
import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

# base.py 位于 scripts/syndicate/base.py → parents[2] 即仓库根
ROOT = Path(__file__).resolve().parents[2]

# 站点 URL 约定，与 src/scripts/ping_search_engines.py / site/astro.config.mjs 一致
SITE_URL = os.environ.get("SITE_URL", "https://seeyeetech.com").rstrip("/")
BASE_PATH = os.environ.get("PUBLIC_BASE_PATH", "/github-explorer").rstrip("/")


# ── .env.local 加载（可选便利；不覆盖已存在的环境变量）────────────────────
def load_dotenv(*names: str) -> None:
    """按顺序加载仓库根的 .env.local / .env，KEY=VALUE 逐行，不覆盖已有 env。

    等价于现有约定 `set -a && source .env && set +a`，便于本地直接 `python3` 运行。
    """
    for name in names or (".env.local", ".env"):
        p = ROOT / name
        if not p.is_file():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            if key.startswith("export "):
                key = key[len("export "):].strip()
            val = val.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = val


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, "") or default


def slug_for(md_path: Path) -> str:
    return md_path.stem.lower()


def canonical_url_for(slug: str) -> str:
    return f"{SITE_URL}{BASE_PATH}/reports/{slug}/"


# ── 数据模型 ──────────────────────────────────────────────────────────────
_H1_RE = re.compile(r"^\s*#\s+(.+?)\s*$", re.MULTILINE)
_GH_RE = re.compile(r"GitHub:\s*<?(https?://github\.com/[^\s)>]+)", re.IGNORECASE)
_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


@dataclass
class Article:
    """一篇待外发的报告（平台无关的中间表示）。"""

    slug: str
    title: str
    body_md: str                 # 去掉首个 H1 标题后的正文 markdown
    raw_md: str
    source_path: Path | None = None  # 报告 .md 原始路径（自渲染渠道如公众号据此读 .meta.json）
    source_url: str = ""         # 原始 GitHub 仓库地址
    canonical_url: str = ""      # SEO 正本回链 / 导流落点
    digest: str = ""
    author: str = ""
    tags: list[str] = field(default_factory=list)
    syndicate: object = True     # True=全渠道；list=仅这些渠道；False=不外发

    def allows(self, channel: str) -> bool:
        """该报告是否允许发到 channel（受 frontmatter `syndicate` 控制）。"""
        if self.syndicate is True:
            return True
        if self.syndicate is False:
            return False
        if isinstance(self.syndicate, (list, tuple, set)):
            return channel in self.syndicate
        return True


@dataclass
class RenderedArticle:
    title: str
    content: str
    content_format: str          # 'html' | 'markdown'


@dataclass
class PublishResult:
    post_id: str
    url: str
    state: str                   # 'draft' | 'published'


# ── 报告解析（frontmatter 可选；缺失则从 H1 / .meta.json / 约定推导）────────
def _parse_frontmatter(md_text: str) -> tuple[dict, str]:
    """剥离可选 YAML frontmatter，返回 (元数据 dict, 去掉 frontmatter 的正文)。

    优先 PyYAML；缺失时退化到极简 key: value 解析（够覆盖本项目用到的标量/列表/布尔）。
    """
    m = _FRONTMATTER_RE.match(md_text)
    if not m:
        return {}, md_text
    raw, body = m.group(1), md_text[m.end():]
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(raw) or {}
        if isinstance(data, dict):
            return data, body
    except Exception:
        pass
    data: dict = {}
    for line in raw.splitlines():
        if ":" not in line or line.strip().startswith("#"):
            continue
        k, _, v = line.partition(":")
        k, v = k.strip(), v.strip()
        if not k:
            continue
        if v.startswith("[") and v.endswith("]"):
            data[k] = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
        elif v.lower() in ("true", "false"):
            data[k] = v.lower() == "true"
        else:
            data[k] = v.strip("'\"")
    return data, body


def _load_meta_sidecar(md_path: Path) -> dict:
    """读 md2wechat 产出的同名 .meta.json（title/digest/author/theme），无则空 dict。"""
    meta_path = Path(str(md_path.with_suffix("")) + ".meta.json")
    if meta_path.is_file():
        try:
            return json.loads(meta_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
    return {}


def parse_report(md_path: Path) -> Article:
    """把一篇报告 .md 解析成平台无关的 Article。"""
    raw = md_path.read_text(encoding="utf-8")
    fm, body_after_fm = _parse_frontmatter(raw)
    meta = _load_meta_sidecar(md_path)
    slug = slug_for(md_path)

    # 标题优先级：frontmatter > .meta.json > 首个 H1 > 文件名
    title = (fm.get("title") or meta.get("title") or "").strip()
    h1 = _H1_RE.search(body_after_fm)
    if not title and h1:
        title = h1.group(1).strip()
    if not title:
        title = md_path.stem

    # 正文去掉首个 H1（标题在各平台是独立字段）
    body_md = body_after_fm
    if h1:
        body_md = (body_after_fm[: h1.start()] + body_after_fm[h1.end():]).lstrip("\n")

    gh = _GH_RE.search(raw)
    source_url = (fm.get("source_url") or (gh.group(1) if gh else "")).rstrip(")>")

    tags = fm.get("tags") or meta.get("tags") or []
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]

    return Article(
        slug=slug,
        title=title,
        body_md=body_md,
        raw_md=raw,
        source_path=md_path,
        source_url=source_url,
        canonical_url=fm.get("canonical_url") or canonical_url_for(slug),
        digest=(fm.get("digest") or meta.get("digest") or "").strip(),
        author=(fm.get("author") or meta.get("author") or "").strip(),
        tags=list(tags),
        syndicate=fm.get("syndicate", True),
    )


# ── adapter 抽象 + 注册表 ──────────────────────────────────────────────────
class BaseAdapter(ABC):
    """渠道 adapter 契约。每个平台一个子类，封装其凭据、接口差异与发布动作。"""

    name: str = ""
    content_format: str = "html"   # 该平台期望的渲染目标：'html' | 'markdown'
    # 投递方式：
    #   'api'     —— 脚本可直接调用 publish()（cnblogs HTTP / wechat 复用现有管线）
    #   'browser' —— 无开放 API，发布须由 Claude-in-Chrome 驱动浏览器，脚本只 prepare()
    mode: str = "api"
    # 导流页脚是否加「关注…」公众号 CTA。极敏感平台（如知乎，任何公众号引导都
    # 可能触发限流）置 False，页脚只留「本文首发于 …」canonical 回链。
    mp_cta: bool = True
    # CTA 里是否点名「微信」。某些平台（如 CSDN/阿里云）禁止或慎用「微信公众号」字样，
    # 置 False 后 CTA 仍保留账号名「{WECHAT_MP_NAME}」+「全网同名，搜一搜即达」，
    # 只是不出现「微信公众号 / 微信」这几个字，靠同名让读者自行搜到。
    name_wechat: bool = True
    # True = 渠道自带完整渲染管线（如公众号的图片重托管 / CSS 内联 / 封面 / 草稿箱），
    # 忽略框架 render 与导流页脚（公众号本身就是导流终点，不该带「关注公众号」CTA），
    # publish 时 rendered 传 None，dry-run 走该 adapter 的 dry_run()。
    self_render: bool = False

    @abstractmethod
    def check_auth(self) -> None:
        """校验凭据是否齐备，缺失抛 RuntimeError。不产生网络副作用。"""

    @abstractmethod
    def publish(
        self,
        article: Article,
        rendered: RenderedArticle | None,
        *,
        publish: bool,
        existing_post_id: str | None = None,
    ) -> PublishResult:
        """发布或更新文章。

        existing_post_id 非空 = 编辑既有文章（幂等更新，避免重复发文）。
        publish=False 存草稿、True 直接公开。
        self_render 渠道的 rendered 为 None（自行从 article 渲染）。
        """

    def dry_run(self, article: Article) -> str | None:
        """self_render 渠道覆盖此法做自渲染的 dry-run（不联网/不发布）。

        非 self_render 渠道不调用此法（由 CLI 直接落框架渲染结果到 tmp/）。
        """
        return None


_REGISTRY: dict[str, type[BaseAdapter]] = {}


def register(cls: type[BaseAdapter]) -> type[BaseAdapter]:
    """adapter 类装饰器：登记到全局注册表。"""
    if not cls.name:
        raise ValueError(f"{cls.__name__} 必须定义 name")
    _REGISTRY[cls.name] = cls
    return cls


def _ensure_adapters_loaded() -> None:
    from . import adapters  # noqa: F401  触发各 adapter 的 @register


def get_adapter(name: str) -> BaseAdapter:
    _ensure_adapters_loaded()
    if name not in _REGISTRY:
        raise RuntimeError(
            f"未知渠道 '{name}'，已注册: {', '.join(sorted(_REGISTRY)) or '(无)'}"
        )
    return _REGISTRY[name]()


def available_channels() -> list[str]:
    _ensure_adapters_loaded()
    return sorted(_REGISTRY)

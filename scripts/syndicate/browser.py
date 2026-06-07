"""浏览器自动化渠道的基类 —— 给无开放发布 API 的平台（掘金 / CSDN 等）。

与 api/self_render 渠道的根本区别：发布动作**不能**由独立 Python 脚本完成，
必须由 Claude（agent）通过 Claude-in-Chrome MCP 工具驱动浏览器、复用用户**已登录**
的会话来发。所以这类 adapter 不实现可调用的 publish()，而是 prepare()：

  1. prepare(article, rendered) → 产出「发布包」：渲染好的内容文件 + 目标编辑器
     URL + 字段(标题/标签/分类/简介) + 一份 playbook（给 agent 的 DOM 操作步骤）。
  2. `syndicate_publish.py <md> --channel juejin` 跑 prepare，把包写到 tmp/ 并打印
     playbook，提示用 Claude-in-Chrome 执行。
  3. agent 按 playbook 驱动浏览器发布后，用 `--record --url ... --post-id ...`
     回写 publish_history.jsonl（带 channel，幂等用）。

为什么不让脚本自己发：掘金/CSDN 无公开发布 API；逆向其私有接口要维护 cookie/
签名且易封号。复用浏览器登录态 + agent 驱动是最稳的「半自动」路径。
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .base import ROOT, Article, BaseAdapter, PublishResult, RenderedArticle


def report_hint(article: Article) -> str:
    """playbook 里拼 --record 命令时用的报告路径占位。"""
    return str(article.source_path) if article.source_path else "<报告.md>"


@dataclass
class BrowserPackage:
    channel: str
    slug: str
    title: str
    tags: list
    editor_url: str
    content_format: str
    content_path: str          # tmp/ 下的渲染内容文件（agent 粘贴用）
    steps: list                # playbook：给 agent 的有序操作步骤
    field_notes: dict = field(default_factory=dict)
    existing_url: str = ""      # 已发过则非空 → playbook 走「更新」而非「新建」

    def to_dict(self) -> dict:
        return {
            "channel": self.channel,
            "slug": self.slug,
            "title": self.title,
            "tags": self.tags,
            "editor_url": self.editor_url,
            "content_format": self.content_format,
            "content_path": self.content_path,
            "field_notes": self.field_notes,
            "existing_url": self.existing_url,
            "steps": self.steps,
        }


class BrowserAdapter(BaseAdapter):
    """浏览器自动化渠道基类。子类定义 name / editor_url / field_notes / playbook。"""

    mode = "browser"
    content_format = "markdown"     # 掘金/CSDN 编辑器均 markdown 原生
    editor_url = ""

    # ── 子类定制点 ──────────────────────────────────────────────
    def field_notes(self, article: Article) -> dict:
        """发布抽屉/弹窗里要填的字段提示（标签、分类、封面、简介…）。"""
        return {}

    def playbook(self, article: Article, content_path: str, existing_url: str) -> list:
        """给 agent 的有序操作步骤（字符串列表）。子类必须覆盖。"""
        raise NotImplementedError

    # ── 框架契约 ────────────────────────────────────────────────
    def check_auth(self) -> None:
        # 浏览器渠道靠浏览器登录态，无脚本可校验的凭据；登录检查由 playbook 第一步承担
        return

    def publish(
        self,
        article: Article,
        rendered: RenderedArticle | None,
        *,
        publish: bool,
        existing_post_id: str | None = None,
    ) -> PublishResult:
        raise RuntimeError(
            f"{self.name} 是浏览器自动化渠道，不能由脚本直接发布。\n"
            f"  请跑：python3 scripts/syndicate_publish.py <报告.md> --channel {self.name}\n"
            f"  生成发布包后，由 Claude-in-Chrome 按 playbook 驱动浏览器完成，"
            f"再用 --record 回写历史。"
        )

    def prepare(
        self, article: Article, rendered: RenderedArticle, *, existing_url: str = ""
    ) -> BrowserPackage:
        ext = "html" if rendered.content_format == "html" else "md"
        content_path = ROOT / "tmp" / f"syndicate-{self.name}-{article.slug}.{ext}"
        content_path.parent.mkdir(parents=True, exist_ok=True)
        content_path.write_text(rendered.content, encoding="utf-8")
        return BrowserPackage(
            channel=self.name,
            slug=article.slug,
            title=article.title,
            tags=list(article.tags),
            editor_url=self.editor_url,
            content_format=rendered.content_format,
            content_path=str(content_path),
            steps=self.playbook(article, str(content_path), existing_url),
            field_notes=self.field_notes(article),
            existing_url=existing_url,
        )

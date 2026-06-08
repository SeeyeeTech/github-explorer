"""微信公众号 adapter —— 复用现有 scripts/wechat_publish.py 的完整发布管线。

公众号与其它渠道不同：它的「渲染」与 API 深度耦合（外链图必须先下载→压到
1MB→上传 mmbiz 换 URL，CSS 必须全内联，还要传封面、入草稿箱），且公众号
本身是导流终点、不该带「关注公众号」CTA。所以本 adapter 标记 self_render=True，
直接调用 wechat_publish.publish_report() 复用那套久经考验的逻辑，而非走框架
的通用 render。

凭据（放 .env.local，同现有公众号管线）：
  WECHAT_APPID / WECHAT_APPSECRET   必需
  WECHAT_API_BASE                   反代 base url
  WECHAT_PROXY_TOKEN                 反代鉴权 header（直连官方可留空）

前置：报告需有同名 .meta.json（title/digest/author/theme），由 md2wechat 产出。

注意：
  - 本流程止于「入草稿箱」（与现状一致），群发上线仍在公众号后台人工完成，
    故 publish 参数被忽略、state 恒为 'draft'，post_id = 草稿 media_id。
  - wechat_publish 的 API 错误沿用 sys.exit；这里捕获 SystemExit 转成
    RuntimeError，便于 CLI 统一收敛报错。
  - CI 自动分析仍走原 wechat_publish.py + record_publish.py；本 adapter 是
    「统一调度」下的等价手动/本地路径，两者都写 publish_history.jsonl(channel=wechat)。
"""
from __future__ import annotations

from ..base import Article, BaseAdapter, PublishResult, RenderedArticle, register


def _load_wechat_publish():
    """惰性导入 wechat_publish（它顶层 import premailer/PIL 等重依赖，缺失会 sys.exit）。

    放到方法内导入，避免「仅注册 adapter / 用其它渠道」时被公众号依赖拖累。
    """
    try:
        import wechat_publish  # scripts/ 在 sys.path 上（同 wechat_publish 导入 _wechat_api）
    except SystemExit as e:
        raise RuntimeError(f"公众号发布依赖缺失：{e.code}") from e
    return wechat_publish


def _require_path(article: Article):
    if article.source_path is None or not article.source_path.is_file():
        raise RuntimeError("公众号发布需要报告 .md 原始路径（source_path 缺失）")
    return article.source_path


@register
class WeChatAdapter(BaseAdapter):
    name = "wechat"
    content_format = "wechat"   # 仅标识；实际渲染在 wechat_publish 内部
    self_render = True

    def check_auth(self) -> None:
        import os

        missing = [k for k in ("WECHAT_APPID", "WECHAT_APPSECRET") if not os.environ.get(k)]
        if missing:
            raise RuntimeError(
                "公众号缺少凭据: " + ", ".join(missing)
                + "（放进 .env.local，见 scripts/syndicate/README.md）"
            )

    def dry_run(self, article: Article) -> str | None:
        wp = _load_wechat_publish()
        res = wp.publish_report(_require_path(article), dry_run=True)
        return res.get("out_html")

    def publish(
        self,
        article: Article,
        rendered: RenderedArticle | None,   # self_render → 恒为 None，不使用
        *,
        publish: bool,
        existing_post_id: str | None = None,
    ) -> PublishResult:
        wp = _load_wechat_publish()
        try:
            res = wp.publish_report(_require_path(article), dry_run=False)
        except SystemExit as e:   # wechat_publish 内部用 sys.exit 报致命错
            raise RuntimeError(f"公众号发布失败：{e.code}") from e
        # 止于草稿箱：post_id = 草稿 media_id，url = 「阅读原文」指向的博客页
        return PublishResult(
            post_id=str(res.get("media_id", "")),
            url=res.get("content_source_url", ""),
            state="draft",
        )

"""MetaWeblog XML-RPC 发布基类 —— 博客园 / 开源中国等支持 MetaWeblog 的平台共用。

MetaWeblog 是少数国内可编程的发布协议（XML-RPC），无需浏览器、可进 CI。
子类只需给出：凭据校验 check_auth()、连接配置 _config()、文章 URL 构造 _post_url()。
正文走 HTML（MetaWeblog 的 description 字段是 HTML），故 content_format='html'。

方法：metaWeblog.newPost(blogid, user, password, struct, publish) -> postid(str)
      metaWeblog.editPost(postid, user, password, struct, publish) -> bool
"""
from __future__ import annotations

import xmlrpc.client

from .base import Article, BaseAdapter, PublishResult, RenderedArticle


class MetaWeblogAdapter(BaseAdapter):
    content_format = "html"
    mode = "api"

    # ── 子类定制点 ──────────────────────────────────────────────
    def _config(self) -> dict:
        """返回 {endpoint, blogid, username, password, categories}。"""
        raise NotImplementedError

    def _post_url(self, post_id: str, cfg: dict) -> str:
        """据 postid 拼公开文章 URL（写入发布历史）。"""
        raise NotImplementedError

    # ── 共享发布逻辑 ────────────────────────────────────────────
    def publish(
        self,
        article: Article,
        rendered: RenderedArticle | None,
        *,
        publish: bool,
        existing_post_id: str | None = None,
    ) -> PublishResult:
        c = self._config()
        server = xmlrpc.client.ServerProxy(c["endpoint"], allow_none=True)
        struct = {
            "title": rendered.title,
            "description": rendered.content,          # HTML 正文
            "categories": c.get("categories") or [],
            "mt_keywords": ",".join(article.tags),
        }
        api = server.metaWeblog
        try:
            if existing_post_id:
                api.editPost(existing_post_id, c["username"], c["password"], struct, publish)
                post_id = str(existing_post_id)
            else:
                post_id = str(api.newPost(c.get("blogid", ""), c["username"], c["password"], struct, publish))
        except xmlrpc.client.Fault as e:                # 平台业务错（登录失败/参数错）
            raise RuntimeError(f"{self.name} MetaWeblog 失败：{e.faultString}") from e
        except (xmlrpc.client.ProtocolError, OSError) as e:   # HTTP / 网络层错
            raise RuntimeError(f"{self.name} MetaWeblog 连接失败：{e}") from e
        return PublishResult(
            post_id=post_id,
            url=self._post_url(post_id, c),
            state="published" if publish else "draft",
        )

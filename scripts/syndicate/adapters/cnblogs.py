"""博客园 (cnblogs) MetaWeblog adapter —— 国内少见的可编程发布平台。

为什么先做博客园：8 个目标渠道里只有它有真正的开放发布 API（MetaWeblog
XML-RPC），无需浏览器/cookie，能在 CI 里全自动跑通，验证骨架成本最低。

凭据（放 .env.local，不入 Git）：
  CNBLOGS_BLOGAPP    博客标识，即 www.cnblogs.com/<blogapp>/ URL 里的那段
  CNBLOGS_USERNAME   博客园登录名
  CNBLOGS_TOKEN      MetaWeblog 访问令牌（后台「设置 → 博客设置 → MetaWeblog 访问令牌」，
                     不是登录密码）
  CNBLOGS_RPC_URL    可选，默认 https://rpc.cnblogs.com/metaweblog/<blogapp>
  CNBLOGS_CATEGORIES 可选，逗号分隔的分类名（如「[随笔分类]开源」）

MetaWeblog 方法：
  metaWeblog.newPost(blogid, user, token, struct, publish) -> postid(str)
  metaWeblog.editPost(postid, user, token, struct, publish) -> bool
其中 publish=False 存草稿、True 直接公开；blogid 传 blogapp 即可（博客园容错）。

待办（未来增强）：正文外链图可用 metaWeblog.newMediaObject 重托管到博客园
图床，规避个别图源的防盗链；当前先原样保留（GitHub 资产图一般可直显）。

发布逻辑在 ../metaweblog.py 的 MetaWeblogAdapter 基类（与开源中国共用）。
"""
from __future__ import annotations

from ..base import env, register
from ..metaweblog import MetaWeblogAdapter


@register
class CnblogsAdapter(MetaWeblogAdapter):
    name = "cnblogs"

    def _config(self) -> dict:
        blogapp = env("CNBLOGS_BLOGAPP")
        return {
            "endpoint": env("CNBLOGS_RPC_URL")
            or (f"https://rpc.cnblogs.com/metaweblog/{blogapp}" if blogapp else ""),
            "blogid": blogapp,
            "username": env("CNBLOGS_USERNAME"),
            "password": env("CNBLOGS_TOKEN"),
            "categories": [c.strip() for c in env("CNBLOGS_CATEGORIES").split(",") if c.strip()],
            "blogapp": blogapp,
        }

    def _post_url(self, post_id: str, cfg: dict) -> str:
        return f"https://www.cnblogs.com/{cfg['blogapp']}/p/{post_id}.html"

    def check_auth(self) -> None:
        c = self._config()
        missing = [k for k in ("blogapp", "username", "password") if not c[k]]
        if missing:
            label = {"blogapp": "CNBLOGS_BLOGAPP", "username": "CNBLOGS_USERNAME", "password": "CNBLOGS_TOKEN"}
            raise RuntimeError(
                "博客园缺少凭据: " + ", ".join(label[m] for m in missing)
                + "（放进 .env.local，见 scripts/syndicate/README.md）"
            )

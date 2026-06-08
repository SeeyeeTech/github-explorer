"""开源中国 OSCHINA adapter。

两条路，二选一：
  - `oschina`     ✅ MetaWeblog API（mode=api，**推荐**，无需浏览器，可进 CI）
  - `oschina_web`    浏览器半自动（mode=browser，markdown 编辑器，作为 API 不通时的兜底）

MetaWeblog 端点已联网探活：`https://www.oschina.net/action/xmlrpc`（活，handler
net.oschina.action.XmlrpcAction，受理 metaWeblog.* / blogger.*）。鉴权 = **账号
用户名 + 登录密码**（注意：是登录密码本身，不像博客园是专用 token；若你用第三方
[GitHub/微信/微博] 登录而没设过密码，需先在开源中国账号设置里设一个密码）。

凭据（放 .env.local，不入 Git）：
  OSCHINA_USERNAME       开源中国登录用户名
  OSCHINA_PASSWORD       登录密码（MetaWeblog 用账号密码鉴权）
  OSCHINA_RPC_URL        可选，默认 https://www.oschina.net/action/xmlrpc
  OSCHINA_BLOGID         可选，newPost 的 blogid，默认用 username（多数实现容错/忽略）
  OSCHINA_BLOG_URL_BASE  可选，文章 URL 前缀（写入历史用），如
                         https://my.oschina.net/u/1234567/blog ；缺省据 username 兜底
  OSCHINA_CATEGORIES     可选，逗号分隔分类名

⚠️ 安全：MetaWeblog 用的是登录密码，存 .env.local（已 gitignore）务必本机保管；
   不放心可改用 oschina_web 浏览器路径（复用浏览器登录态，不落密码）。
"""
from __future__ import annotations

from ..base import Article, env, register
from ..browser import BrowserAdapter, report_hint
from ..metaweblog import MetaWeblogAdapter


@register
class OSChinaAdapter(MetaWeblogAdapter):
    name = "oschina"

    def _config(self) -> dict:
        user = env("OSCHINA_USERNAME")
        return {
            "endpoint": env("OSCHINA_RPC_URL") or "https://www.oschina.net/action/xmlrpc",
            "blogid": env("OSCHINA_BLOGID") or user,
            "username": user,
            "password": env("OSCHINA_PASSWORD"),
            "categories": [c.strip() for c in env("OSCHINA_CATEGORIES").split(",") if c.strip()],
            "url_base": env("OSCHINA_BLOG_URL_BASE"),
        }

    def _post_url(self, post_id: str, cfg: dict) -> str:
        base = (cfg.get("url_base") or f"https://my.oschina.net/u/{cfg['username']}/blog").rstrip("/")
        return f"{base}/{post_id}"

    def check_auth(self) -> None:
        missing = [k for k in ("OSCHINA_USERNAME", "OSCHINA_PASSWORD") if not env(k)]
        if missing:
            raise RuntimeError(
                "开源中国缺少凭据: " + ", ".join(missing)
                + "（放进 .env.local：账号登录名 + 登录密码；见 scripts/syndicate/README.md。"
                "不想落密码可改用 --channel oschina_web 浏览器路径）"
            )


@register
class OSChinaWebAdapter(BrowserAdapter):
    """开源中国浏览器兜底路径（API 不通时用）。markdown 源码编辑器，需登录态。"""

    name = "oschina_web"
    editor_url = "https://www.oschina.net/blog"
    content_format = "markdown"

    def field_notes(self, article: Article) -> dict:
        return {
            "文章类型": "原创（转载/翻译需填原文链接）",
            "标签": "自定义关键词回车分隔，3-5 个（如 github、开源、AI、后端）",
            "技术专区/分类": "从约 46 个预设领域选最贴近（AI & 大数据 / 云原生 / 后端 / 前端 / 数据库…）",
            "文章专辑": "可选，归入自己的系列合集",
            "导流": "文末可写「关注我的微信公众号 智能时代蛮子」+ 可贴二维码（OSCHINA 较宽松）",
        }

    def playbook(self, article: Article, content_path: str, existing_url: str) -> list:
        if existing_url:
            head = [f"该报告此前已发 OSCHINA：{existing_url} → 这是【更新】：进该博文编辑页，其余同新建。"]
        else:
            head = [
                f"这是【新建】。navigate 到 {self.editor_url}，点右上「写博客」进编辑器"
                "（或直达 my.oschina.net/<你的空间>/blog/write）。",
            ]
        return head + [
            "确认已登录 OSCHINA（右上有头像）。未登录则先让用户在该浏览器登录，不要代登录。确保是 markdown 模式。",
            f"读取渲染好的正文：{content_path}（markdown，已含文末导流页脚）。",
            "把 markdown 灌入编辑器：CodeMirror 不能 JS setValue，**必须聚焦后走系统剪贴板粘贴**（Cmd/Ctrl+V）。右侧预览核对。",
            f"标题填：{article.title}",
            "外链图裂图则先下载再编辑器内「上传图片」/粘贴上传到 oscimg.oschina.net 并替换链接。",
            "点「发布」，填：文章类型=原创、标签(3-5)、技术专区/分类、（可选）文章专辑。可在正文末加公众号引导。",
            "点「发布」。成功后复制博文 URL（形如 https://my.oschina.net/<你的空间>/blog/<id>）。",
            "回写历史：python3 scripts/syndicate_publish.py "
            f"{report_hint(article)} --channel oschina_web --record --state published --url <文章URL> --post-id <id>",
        ]

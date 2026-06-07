"""SegmentFault 思否 adapter —— 浏览器自动化（无开放 API，markdown 原生）。

思否是经典 markdown 原生编辑器（左写右预览，marked.js + highlight.js），直接把整篇
markdown 灌进去即可渲染，无需转 HTML。需登录态，Claude-in-Chrome 复用 cookie 直达。

导流：容忍度中等、高于 CSDN。社区《文章编辑规则》：不要在「开头」放推荐/二维码，
但允许「文末」适当加个人推荐/链接。故 name_wechat=True（文末可提公众号名），但
playbook 提示别放二维码、别开头硬广。

坑：① 标签必填且只能从思否已有标签库搜选（不能任意新建）；② 外链图不自动转存，
GitHub raw 图一般可直显但不入思否图床，稳妥是先下载再粘贴上传走思否 CDN。
"""
from __future__ import annotations

from ..base import Article, register
from ..browser import BrowserAdapter, report_hint


@register
class SegmentFaultAdapter(BrowserAdapter):
    name = "segmentfault"
    editor_url = "https://segmentfault.com/write"
    content_format = "markdown"   # markdown 原生，整篇直接粘

    def field_notes(self, article: Article) -> dict:
        return {
            "标签": "必填，从思否标签库搜选 1-4 个（如 github、人工智能、开源、后端），不能任意新建",
            "专栏/博客": "可选，归入自己的专栏形成系列",
            "文章授权类型": "原创",
            "简介": article.digest or "取报告「一句话总结」前 ~100 字",
            "封面": "可选",
        }

    def playbook(self, article: Article, content_path: str, existing_url: str) -> list:
        if existing_url:
            head = [f"该报告此前已发思否：{existing_url} → 这是【更新】：进该文章编辑页，其余同新建。"]
        else:
            head = [f"这是【新建】。navigate 到思否写作页：{self.editor_url}"
                    "（首进可能被 /howtowrite 拦一下并跳 /write?freshman=1，正常）。"]
        return head + [
            "确认已登录思否（右上有头像）。未登录则先让用户在该浏览器登录，不要代登录。确保是 markdown 模式（非富文本）。",
            f"读取渲染好的正文：{content_path}（markdown，已含文末导流页脚）。",
            "把 markdown 灌入左侧编辑器：优先 javascript_tool 给 CodeMirror 设值；不行则聚焦后剪贴板粘贴（Cmd/Ctrl+V），勿逐字键入。右侧预览核对代码/表格/公式渲染。",
            f"标题填：{article.title}",
            "若有外链图裂图，先下载再粘贴/拖拽进编辑器上传到思否图床并替换链接。",
            "点「发布」，弹窗里：搜选标签(必填,1-4)、（可选）专栏、授权类型=原创、（可选）简介/封面。",
            "点「发布文章」。成功后复制文章 URL（形如 https://segmentfault.com/a/<id>）。",
            "回写历史：python3 scripts/syndicate_publish.py "
            f"{report_hint(article)} --channel segmentfault --record --state published --url <文章URL> --post-id <id>",
        ]

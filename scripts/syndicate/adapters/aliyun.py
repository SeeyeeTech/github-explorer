"""阿里云开发者社区 adapter —— 浏览器自动化（markdown 原生，需切 markdown 模式）。

阿里云开发者社区写作页默认可能停在富文本模式；技术长文应切到 **Markdown 模式**
（CodeMirror，左写右预览），再直接粘 markdown 源码。需登录态（未登录会 302 跳
account.aliyun.com）。

导流：中等偏紧，有反「营销/导流」机制，倾向把流量留在自身（乘风者计划）。正文放
二维码 +「扫码关注微信公众号」风险较高；以纯文本带账号名通常可过。故 name_wechat=False
——页脚保留账号名「智能时代蛮子」+ 搜一搜，不点名「微信」。

坑：① 默认可能是富文本模式，**先切 Markdown 模式再粘**（切模式有「内容可能丢失」确认弹窗，
宜先切再粘）；② 外链图不保证自动转存，GitHub 图易 403，需先下载再走编辑器图片上传到阿里云 CDN。
"""
from __future__ import annotations

from ..base import Article, register
from ..browser import BrowserAdapter, report_hint


@register
class AliyunAdapter(BrowserAdapter):
    name = "aliyun"
    editor_url = "https://developer.aliyun.com/article/new"
    content_format = "markdown"
    name_wechat = False   # 阿里云中等偏紧：保留账号名但不点名「微信」

    def field_notes(self, article: Article) -> dict:
        return {
            "技术领域/分类": "必选，从预设领域单选（云计算/大数据/人工智能/前端/后端/数据库…）",
            "标签": "关键词 tag，多选/自填（如 github、开源、AI）",
            "文章摘要": article.digest or "可自动截取或取「一句话总结」前 ~100 字",
            "原创/转载声明": "原创（转载需填来源链接）",
            "封面图": "可选（1 或 3 图）",
            "加入专栏": "可选，归入个人技术专栏",
        }

    def playbook(self, article: Article, content_path: str, existing_url: str) -> list:
        if existing_url:
            head = [f"该报告此前已发阿里云：{existing_url} → 这是【更新】：进该文章编辑页，其余同新建。"]
        else:
            head = [f"这是【新建】。navigate 到阿里云写作页：{self.editor_url}（未登录会跳登录页）。"]
        return head + [
            "确认已登录阿里云（右上有头像）。未登录则先让用户在该浏览器登录，不要代登录。",
            "**先确认/切到 Markdown 模式**（默认可能是富文本；切模式若弹「内容可能丢失」确认，先切再粘正文）。",
            f"读取渲染好的正文：{content_path}（markdown，页脚已是「智能时代蛮子」+ 搜一搜、不含「微信」）。",
            "把 markdown 灌入左侧编辑器：优先 javascript_tool 设值；不行则聚焦后剪贴板粘贴（Cmd/Ctrl+V）。右侧预览核对。",
            f"标题填：{article.title}",
            "外链图裂图则先下载再用工具栏图片按钮上传到阿里云 CDN 并替换链接。",
            "点「发布」，填：技术领域(必选)、标签、摘要、原创声明、（可选）封面/专栏。",
            "点「发布」。成功后复制文章 URL（形如 https://developer.aliyun.com/article/<id>）。",
            "回写历史：python3 scripts/syndicate_publish.py "
            f"{report_hint(article)} --channel aliyun --record --state published --url <文章URL> --post-id <id>",
        ]

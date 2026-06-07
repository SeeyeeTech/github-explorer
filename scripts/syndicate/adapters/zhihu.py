"""知乎专栏 adapter —— 浏览器自动化（无开放 API，富文本编辑器）。

知乎专栏编辑器是富文本 contenteditable（WYSIWYG），**不是 markdown 原生**：
直接粘 markdown 纯文本只会原样保留 `#` ``` `|` 等字面符号、不渲染。可靠注入法是
「粘 HTML 富文本」——所以本 adapter content_format='html'，注入时让编辑器拿到
**富文本剪贴板**（而非 html 源码字符串）：

  推荐注入流程（agent 驱动）：
    1. 把渲染好的 HTML（content_path，.html）在一个空白标签页里 innerHTML 注入并渲染；
    2. 在该页 全选(Cmd/Ctrl+A) + 复制(Cmd/Ctrl+C) —— 此时系统剪贴板带 text/html 富文本；
    3. 切到知乎写作页，点正文区 粘贴(Cmd/Ctrl+V)，知乎 paste handler 会把
       h1-h6/p/ul/ol/blockquote/pre>code/img/table 映射进自研富文本模型，格式得以保留。
  （直接 pbcopy html 源码再粘是纯文本，会糊一堆标签——务必走「渲染后复制」拿富文本。）

导流：知乎是站外导流最敏感的平台，正文出现任何「关注公众号/二维码」都易触发
限流降权（比 CSDN 的硬关键词拒发更隐蔽也更狠）。故 mp_cta=False —— 正文页脚
**完全不放公众号 CTA**，只留 canonical 回链，引流交给个人资料/简介低调处理。

坑：① 表格弱（不支持合并/调列宽），复杂表格降级为截图；② 公式 KaTeX 在「编辑器
内输入」可渲染，但 HTML 粘贴的 LaTeX 常不自动渲染，需手动补；③ 外链图（GitHub）
常因防盗链转存失败/裂图——应先下载再走编辑器「插入图片」上传到 zhimg 图床。
"""
from __future__ import annotations

from ..base import Article, register
from ..browser import BrowserAdapter, report_hint


@register
class ZhihuAdapter(BrowserAdapter):
    name = "zhihu"
    editor_url = "https://zhuanlan.zhihu.com/write"
    content_format = "html"   # 富文本编辑器，走 HTML 富文本粘贴
    mp_cta = False            # 知乎对站外导流最敏感：正文不放任何公众号 CTA

    def field_notes(self, article: Article) -> dict:
        return {
            "话题": "核心字段（知乎用话题而非分类），最多 5 个，至少选 2-3 个相关高热话题（如 开源、人工智能、GitHub）",
            "收录到专栏": "可选，归入自己的专栏形成系列",
            "封面图": "建议设，影响信息流展示",
            "创作声明": "按需开「包含 AI 辅助创作」等声明",
            "可见范围": "公开",
            "⚠️导流": "知乎正文严禁公众号 CTA/二维码（易限流）；页脚已自动只留 canonical 回链，引流只在个人简介低调做",
        }

    def playbook(self, article: Article, content_path: str, existing_url: str) -> list:
        if existing_url:
            head = [f"该报告此前已发知乎：{existing_url} → 这是【更新】：进该文章编辑页，其余同新建。"]
        else:
            head = [f"这是【新建】。navigate 到知乎写作页：{self.editor_url}"]
        return head + [
            "确认右上已登录知乎（有头像）。未登录则先让用户在该浏览器登录，不要代登录。",
            f"读取渲染好的 HTML：{content_path}（富文本注入用，已含 canonical 页脚、无公众号 CTA）。",
            "注入富文本：① 在一个空白标签页用 javascript_tool 把该 HTML 注入 document.body 并渲染；"
            "② 在该页 Cmd/Ctrl+A 全选 + Cmd/Ctrl+C 复制（拿到 text/html 富文本剪贴板）；"
            "③ 切回知乎写作页，点正文区，Cmd/Ctrl+V 粘贴。切勿直接粘 markdown/HTML 源码字符串（会糊标签）。",
            f"标题填：{article.title}",
            "核对正文：代码块是否成块并保留高亮、表格是否错位、外链图是否裂。"
            "裂图则把该图先下载再用编辑器「插入图片」上传到 zhimg 图床；复杂表格/公式渲染异常则降级为截图。",
            "点右上「发布」，在面板里：选 2-5 个话题、（可选）收录专栏、设封面、按需创作声明、可见范围=公开。",
            "点「发布」。成功后复制文章 URL（形如 https://zhuanlan.zhihu.com/p/<id>）。",
            "回写历史：python3 scripts/syndicate_publish.py "
            f"{report_hint(article)} --channel zhihu --record --state published --url <文章URL> --post-id <id>",
        ]

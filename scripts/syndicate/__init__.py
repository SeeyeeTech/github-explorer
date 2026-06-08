"""一文多发（多渠道发布）框架。

把现有「单渠道公众号发布」泛化成「一份报告 → 多个渠道」的 publisher + adapter
结构：新接一个平台 = 新增一个 adapter，主流程不动。

入口：scripts/syndicate_publish.py
文档：scripts/syndicate/README.md
"""

__all__ = ["base", "render", "history", "adapters"]

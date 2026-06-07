"""注册所有可用 adapter。新增平台时在此 import 触发 @register。

路线（按 README 的优先级）：
  - wechat                       ✅ adapter（复用 wechat_publish.py 图片/渲染/草稿，mode=api）
  - cnblogs                      ✅ MetaWeblog API（无需浏览器，mode=api）
  - juejin/csdn                  ✅ 浏览器半自动（mode=browser，已实发）
  - zhihu/segmentfault/oschina/aliyun  ✅ 浏览器半自动（mode=browser）
  - 腾讯云开发者社区              ✗ 不集成（已有其他方案）
"""
from . import cnblogs  # noqa: F401
from . import wechat  # noqa: F401
from . import juejin  # noqa: F401
from . import csdn  # noqa: F401
from . import zhihu  # noqa: F401
from . import segmentfault  # noqa: F401
from . import oschina  # noqa: F401
from . import aliyun  # noqa: F401

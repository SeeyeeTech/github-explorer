#!/usr/bin/env python3
"""
读分析报告的 .md + .meta.json，确定性地转 HTML 后走反代入微信草稿箱。

为什么独立成脚本（不依赖 md2wechat 输出 HTML）：
  实测 LLM 转 HTML 不可靠 —— 把 `![alt](url)` 错转成嵌套 a 标签、
  把数字列表拆成游离段落、相邻 ul 不合并 等等。这些都被 Python
  markdown 库一次性解决。md2wechat skill 只负责润色 md
  （引号替换、lint、摘要）和输出元数据 JSON。

输入：
  argv[1]: 报告 .md 路径（如 src/analysis_report/gin-gonic_gin.md）
           会自动推出同名 .meta.json

环境变量：
  必需：WECHAT_APPID / WECHAT_APPSECRET
  必需：WECHAT_API_BASE      反代 base url，如 https://wx.nightvoyager.top
  必需：WECHAT_PROXY_TOKEN   反代鉴权 header
  可选：DEFAULT_COVER_URL    封面拉取失败时用这个兜底，默认 picsum
  可选：BLOG_BASE_URL        阅读原文指向的博客 base，
                             默认 https://blog.nightvoyager.top/github-explorer/reports

产出：
  tmp/last_publish.json  {media_id, thumb_media_id, title, ...}
  非 0 退出 = 发布失败
"""
from __future__ import annotations

import io
import json
import mimetypes
import sys
import time
import urllib.parse
from pathlib import Path

from _wechat_api import (
    HttpError,
    check_wechat_ok,
    env,
    get_access_token,
    http,
    http_json,
    http_json_try,
    http_json_with_retry,
    http_try,
    load_wechat_env,
    proxy_headers,
)

try:
    import markdown
    from premailer import transform as inline_css
    from bs4 import BeautifulSoup
    from PIL import Image, ImageOps, features
except ImportError as e:
    sys.exit(
        f"ERR: 缺少 Python 包 ({e})。\n"
        "  本地: venv/bin/pip install premailer beautifulsoup4 markdown pillow\n"
        "  CI:  requirements-ci.txt 已含 premailer beautifulsoup4 markdown pillow"
    )

# Pillow 源码编译且缺 libwebp 时 features.check('webp') 为 False —— 此时 webp
# 无法解码，convert_image 直接返回 None，让 webp 图走删除兜底而非转换。
_WEBP_OK = features.check("webp")
if not _WEBP_OK:
    print("WARN: Pillow 无 webp 支持，webp 图将走删除兜底而非转换", file=sys.stderr)


# 微信公众号排版 CSS — 与 ci/skills/md2wechat/assets/wechat.css 同步
# 仅使用标签选择器（微信会清掉 class 属性）+ !important（防止微信内部样式覆盖）
DEFAULT_CSS = """
body { max-width: 680px; margin: 0 auto; padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #3e3e3e; background: #fff; }
p { font-size: 15px !important; line-height: 2 !important; margin: 0 !important;
    padding: 0.5em 1.2em !important; text-align: justify !important; }
p + p { margin-top: 0 !important; }
h2 { font-size: 18px !important; color: #e51f42 !important; text-align: center !important;
    margin: 24px 0 !important; padding: 0 !important; }
h3 { font-size: 15px !important; font-weight: bold !important; color: #3e3e3e !important;
    text-align: left !important; margin: 16px 0 !important; padding: 0 0 0 1.2em !important; }
h4 { font-size: 15px !important; color: rgb(0,122,170) !important; margin: 12px 0 8px 0 !important; }
ul, ol { padding-left: 2em !important; margin: 1em 0 !important; font-size: 15px !important; }
li { margin: 0.5em 0 !important; line-height: 1.8em !important; font-size: 15px !important;
    color: #3e3e3e !important; }
ul ul, ul ol, ol ul, ol ol { margin: 0 !important; padding-left: 1.2em !important; }
blockquote { border-left: 4px solid #888 !important; padding: 8px 16px !important;
    margin: 1em 0 !important; color: #666 !important; background: #f9f9f9 !important; }
blockquote > p { margin: 0.5em 0 !important; padding: 0 !important; }
pre { font-size: 14px !important; line-height: 1.4em !important; color: #3e3e3e !important;
    background: #f8f8f8 !important; padding: 12px 16px !important; border-radius: 4px !important;
    overflow: auto !important; margin: 1em 0 !important; }
code { background: #f4f4f4 !important; color: #c7254e !important; padding: 2px 4px !important;
    border-radius: 3px !important; font-size: 90% !important; }
pre code { background: transparent !important; color: inherit !important; padding: 0 !important; }
strong { font-weight: bold !important; color: #3e3e3e !important; }
a { color: rgb(0,122,170) !important; text-decoration: none !important; }
img { max-width: 100% !important; height: auto !important; display: block !important;
    margin: 1em auto !important; border-radius: 4px !important; }
table { border-collapse: collapse !important; width: 100% !important; margin: 1em 0 !important;
    font-size: 14px !important; }
th, td { border: 1px solid #ddd !important; padding: 6px 10px !important; text-align: left !important; }
th { background: #f4f4f4 !important; font-weight: bold !important; }
hr { border: none !important; border-top: 1px solid #ddd !important; margin: 1.5em 0 !important; }
""".strip()


def build_multipart(filename: str, data: bytes, field: str = "media") -> tuple[str, bytes]:
    boundary = f"----wechat-{int(time.time()*1000)}"
    mime = mimetypes.guess_type(filename)[0] or "application/octet-stream"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'
        f"Content-Type: {mime}\r\n\r\n"
    ).encode("utf-8") + data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    return boundary, body


def merge_adjacent_uls(soup: BeautifulSoup) -> int:
    """合并相邻 <ul>，避免每条 li 单独被一个 ul 包导致行距过大。返回合并次数。"""
    merged = 0
    while True:
        round_merged = 0
        for ul in soup.find_all("ul"):
            sib = ul.next_sibling
            # 跳过纯空白文本节点
            while sib is not None and getattr(sib, "name", None) is None:
                if str(sib).strip():
                    break
                sib = sib.next_sibling
            if sib is not None and getattr(sib, "name", None) == "ul":
                for li in list(sib.find_all("li", recursive=False)):
                    ul.append(li.extract())
                sib.decompose()
                round_merged += 1
        if round_merged == 0:
            break
        merged += round_merged
    return merged


# ─────────────────────────────────────────────────────────────────────
# 正文图片处理：下载(带重试) → 探测真实格式 → 转 png/jpg 且 <1MB → 上传换
# mmbiz URL；不可救的图(svg/视频/损坏/超限/上传被拒)连同图注、被清空的章节
# 标题一并删除——微信正文不支持外链，保留原 src 只会显示破图。
# 微信 cgi-bin/media/uploadimg 硬限制：仅 jpg/png、单图 < 1MB。
# ─────────────────────────────────────────────────────────────────────

_TARGET_BYTES = 1_000_000             # 微信硬限 1MB，留 ~48KB 余量给 multipart 头
_MAX_SIDE = 2048                      # 超大图先按长边降采样
_MIN_SIDE = 480                       # 压缩循环长边下限，再小就放弃
_JPEG_QUALITY_LADDER = (85, 72, 60, 48)
_RESIZE_LADDER = (1.0, 0.75, 0.55, 0.40)
_CAPTION_MAX_CHARS = 80               # 紧邻图片的纯文本 ≤ 此长度才视为图注


def sniff_format(data: bytes) -> str:
    """按文件头 magic bytes 判真实格式：png|jpeg|gif|webp|svg|video|other。

    URL 后缀不可信(44 个图无后缀、个别 .mp4 藏在 <img> 里)，必须按字节判。
    驱动「保留 / 转换 / 删除」决策。绝不抛异常。
    """
    if not data:
        return "other"
    head = data[:64]
    # 栅格图(Pillow 可解)
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if head[:3] == b"\xff\xd8\xff":
        return "jpeg"
    if head[:4] == b"GIF8" and head[4:6] in (b"7a", b"9a"):
        return "gif"
    if head[:4] == b"RIFF":                                  # RIFF 容器，看子类型
        sub = head[8:12]
        if sub == b"WEBP":
            return "webp"
        if sub == b"AVI ":
            return "video"
        return "other"
    # 视频容器 → 删除
    if head[4:8] == b"ftyp":                                 # MP4 / MOV / M4V (ISO BMFF)
        return "video"
    if head[:4] == b"\x1aE\xdf\xa3":                         # WEBM / MKV (EBML)
        return "video"
    if head[4:8] in (b"moov", b"mdat", b"free", b"wide"):    # 老式 MOV
        return "video"
    # SVG：文本，可能带 BOM / 前导空白 / XML 声明
    probe = data[:512].lstrip(b"\xef\xbb\xbf \t\r\n").lower()
    if probe.startswith(b"<?xml") or probe.startswith(b"<svg") or b"<svg" in probe[:256]:
        return "svg"
    return "other"                                           # bmp/tiff/ico 等交 convert 试解码


def _has_alpha(img) -> bool:
    if img.mode in ("RGBA", "LA", "PA"):
        return True
    return img.mode == "P" and "transparency" in img.info


def _normalize_mode(img, want_alpha: bool):
    """统一到 RGBA / RGB —— 顺带吃掉 P(调色板)、CMYK(Adobe 反相)、YCbCr、L、1。"""
    target = "RGBA" if want_alpha else "RGB"
    return img if img.mode == target else img.convert(target)


def _clamp_side(img, max_side: int):
    w, h = img.size
    if max(w, h) <= max_side:
        return img
    s = max_side / float(max(w, h))
    return img.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)


def _encode_under_limit(img, *, prefer_jpeg: bool) -> "tuple[bytes, str] | None":
    """逐级 resize ×(JPEG 逐级降质 / PNG optimize)，命中 _TARGET_BYTES 即返回。"""
    for scale in _RESIZE_LADDER:
        work = img if scale == 1.0 else img.resize(
            (max(1, int(img.width * scale)), max(1, int(img.height * scale))),
            Image.LANCZOS,
        )
        if scale != 1.0 and min(work.size) < _MIN_SIDE:
            break
        if prefer_jpeg:
            for q in _JPEG_QUALITY_LADDER:
                buf = io.BytesIO()
                work.save(buf, format="JPEG", quality=q, optimize=True, progressive=True)
                if buf.tell() <= _TARGET_BYTES:
                    return buf.getvalue(), "jpg"
        else:
            buf = io.BytesIO()
            work.save(buf, format="PNG", optimize=True)
            if buf.tell() <= _TARGET_BYTES:
                return buf.getvalue(), "png"
    return None


def convert_image(data: bytes, fmt: str) -> "tuple[bytes, str] | None":
    """把 png/jpeg/gif/webp/other 规整成 (bytes, 'png'|'jpg') 且 < 1MB。

    svg / video 已在上游过滤。返回 None = 损坏 / 不支持 / 压不进 1MB → 走删除。
    绝不抛异常。
    """
    if fmt == "webp" and not _WEBP_OK:
        return None
    try:
        img = Image.open(io.BytesIO(data))
        img.load()                      # 强制解码：截断 / 损坏在此抛错
    except Exception:
        return None
    # 动图(gif / webp)取首帧
    try:
        if getattr(img, "is_animated", False):
            img.seek(0)
    except Exception:
        return None
    # EXIF 方向校正(手机截图)，失败忽略
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
    want_alpha = _has_alpha(img)
    try:
        img = _normalize_mode(img, want_alpha)
        img = _clamp_side(img, _MAX_SIDE)
        out = _encode_under_limit(img, prefer_jpeg=not want_alpha)
        if out is None and want_alpha:
            # 带 alpha 的 PNG 仍压不下去 → 末路：白底拍平转 JPEG(牺牲透明)
            flat = Image.new("RGB", img.size, (255, 255, 255))
            flat.paste(img, mask=img.split()[-1])
            out = _encode_under_limit(flat, prefer_jpeg=True)
    except Exception:
        return None
    return out


# ─── 语义化删除：死图 + 图注 + 被清空的章节标题 ─────────────────────────

def _is_caption(node) -> bool:
    """node 是否为「图注」：紧邻图片、短、且非正文/链接/列表/标题。保守判定。"""
    if getattr(node, "name", None) != "p":
        return False
    if node.find("img"):        # 另一张图的承载段，不是图注
        return False
    if node.find("a"):          # 链接段(如「动画演示：<a>」)→ 视为正文，保留
        return False
    text = node.get_text(strip=True)
    if not text:                # 空 <p> → 安全删
        return True
    em = node.find(["em", "i"])
    if em and em.get_text(strip=True) == text:   # 整段就是斜体 → 图注
        return True
    return len(text) <= _CAPTION_MAX_CHARS        # 纯文本短段 → 图注


def remove_image_block(img) -> None:
    """删一张死图。多图同段且尚有存活图 → 只删这张 img；本段已无图 → 删整段
    并尝试删紧邻图注。幂等：可对已分离节点安全调用。"""
    if img.find_parent() is None:        # 已被前一次顺带删掉
        return
    carrier = img.find_parent("p")
    if carrier is None:                  # img 直接挂在容器下
        img.decompose()
        return
    img.decompose()
    if carrier.find("img"):              # 多图段仍有存活图 → 保留整段 + 图注
        return
    caption = carrier.find_next_sibling()    # 先取引用(carrier 还在树上)
    carrier.decompose()
    if caption is not None and _is_caption(caption):
        caption.decompose()


_SECTION_CONTENT = ("ul", "ol", "table", "blockquote", "pre")


def _section_is_empty(h2) -> bool:
    """h2 到下一个 h2(或文末)之间是否已无任何图片 / 实质内容。"""
    node = h2.find_next_sibling()
    while node is not None and getattr(node, "name", None) != "h2":
        name = getattr(node, "name", None)
        if name == "img" or (name and node.find("img")):
            return False
        if name in _SECTION_CONTENT:
            return False
        if name == "p" and node.get_text(strip=True):
            return False
        node = node.find_next_sibling()
    return True


def prune_touched_sections(headers) -> int:
    """仅对被删图所属的 h2，若其章节已空则删该标题。返回删除数。"""
    removed = 0
    for h2 in headers:
        if h2.find_parent() is None:     # 已被删
            continue
        if _section_is_empty(h2):
            h2.decompose()
            removed += 1
    return removed


def upload_external_images(
    soup: BeautifulSoup,
    *,
    access_token: str,
    api_base: str,
    proxy_headers: dict,
    dry_run: bool = False,
) -> "tuple[int, int, list[dict]]":
    """所有非 mmbiz 的 <img>：下载(重试) → 探测格式 → 转 png/jpg(<1MB) → uploadimg
    换 mmbiz URL。不可救的图连同图注 / 被清空的章节标题删除。

    返回 (成功数, 删除数, removed[{src, reason}])。dry_run=True 时不真上传，
    成功路径只验证「下载 + 转换」通过、不改 src(用于本地验证删除/转换逻辑)。
    """
    ok = 0
    to_remove: list = []                 # [(img, reason, src)]，阶段 2 统一删

    for img in soup.find_all("img"):
        src = (img.get("src") or "").strip()
        if not src or "mmbiz." in src or src.startswith("data:"):
            continue

        # 1) 下载(软重试，单图失败不中断整篇)
        try:
            data = http_try(src, timeout=20, backoffs=(1, 3, 6))
        except HttpError as e:
            print(f"  ⚠ 下载失败 {src[:60]}…  {str(e)[:80]}", file=sys.stderr)
            to_remove.append((img, "download_failed", src))
            continue

        # 2) 探测真实格式
        fmt = sniff_format(data)
        if fmt in ("svg", "video"):
            print(f"  ⚠ 不支持格式[{fmt}] {src[:60]}…", file=sys.stderr)
            to_remove.append((img, fmt, src))
            continue

        # 3) 转 png/jpg 且 <1MB
        conv = convert_image(data, fmt)
        if conv is None:
            print(f"  ⚠ 转换失败[{fmt}] {src[:60]}…", file=sys.stderr)
            to_remove.append((img, "convert_failed", src))
            continue
        out_bytes, ext = conv

        # dry-run：验证下载 + 转换通过即可，不真上传、不改 src
        if dry_run:
            print(f"  ·(dry-run){src[:50]}… [{fmt}→{ext} {len(out_bytes)}B] 可上传")
            ok += 1
            continue

        # 4) 文件名后缀对齐真实格式(否则微信按后缀判 MIME 拒收)
        base = src.rsplit("/", 1)[-1].split("?", 1)[0].split("#", 1)[0]
        stem = base.rsplit(".", 1)[0] if "." in base else (base or "img")
        filename = f"{stem}.{ext}"

        # 5) 上传 uploadimg(软重试)
        try:
            url = f"{api_base}/cgi-bin/media/uploadimg?access_token={urllib.parse.quote(access_token)}"
            boundary, body = build_multipart(filename, out_bytes)
            r = http_json_try(
                url,
                headers={
                    **proxy_headers,
                    "Content-Type": f"multipart/form-data; boundary={boundary}",
                },
                data=body,
                method="POST",
                timeout=60,
            )
        except HttpError as e:
            print(f"  ⚠ uploadimg 失败 {src[:60]}…  {str(e)[:80]}", file=sys.stderr)
            to_remove.append((img, "upload_failed", src))
            continue

        if r.get("url"):
            img["src"] = r["url"]
            print(f"  ✓ {src[:50]}… [{fmt}→{ext}] → mmbiz")
            ok += 1
        else:
            print(f"  ⚠ uploadimg 响应缺 url: {r}", file=sys.stderr)
            to_remove.append((img, "upload_rejected", src))

    # ── 阶段 2：语义化删除(死图 + 图注 + 被清空的章节标题)──
    # 删前先收集每张待删图所属的最近 h2(此刻 img 都还在树上，引用有效)
    touched_h2: list = []
    for img, _reason, _src in to_remove:
        h2 = img.find_previous("h2")
        if h2 is not None and h2 not in touched_h2:
            touched_h2.append(h2)
    for img, _reason, _src in to_remove:
        remove_image_block(img)
    pruned = prune_touched_sections(touched_h2)
    if pruned:
        print(f"  ✓ 清理 {pruned} 个被删空的章节标题", file=sys.stderr)

    removed = [{"src": s, "reason": r} for _img, r, s in to_remove]
    return ok, len(removed), removed


def compact_lists(soup: BeautifulSoup) -> None:
    """删掉 ul/ol 内部子节点之间的空白文本节点。

    微信 draft API 把 `<li>` 之间的换行符渲染成空 li（数字 1/3/5 全空），
    必须让 list 内 HTML 紧贴成一行。
    """
    for parent in soup.find_all(["ul", "ol"]):
        for child in list(parent.children):
            if child.name is None and not str(child).strip():
                child.extract()


def promote_strong_colon(soup: BeautifulSoup) -> int:
    """把列表项里 `<strong>X</strong>：Y` 改写为 `<strong>X：</strong>Y`。

    公众号 Web 后台编辑器会把 <li> 内容外包 <p>，叠加 wechat.css 的
    p { text-align: justify }，导致 `</strong>` 紧跟的全角冒号被推到下一行
    （移动端不外包 <p>，所以无此问题）。把冒号挪进 strong 让编辑器视为同一
    个不可拆分块，绕过该换行触发。返回处理过的列表项数。
    """
    from bs4 import NavigableString
    count = 0
    for li in soup.find_all("li"):
        for strong in li.find_all("strong"):
            nxt = strong.next_sibling
            if not isinstance(nxt, NavigableString):
                continue
            text = str(nxt)
            if text and text[0] in ("：", ":"):
                strong.append(text[0])
                nxt.replace_with(text[1:])
                count += 1
    return count


def md_to_html(md_text: str) -> str:
    """Markdown → 微信兼容 HTML 片段（含 <style> 头）。

    md.Markdown 的 'extra' 扩展已包含 tables / fenced_code / abbr 等 GFM 子集；
    'sane_lists' 让数字开头被正确识别为 ol。
    """
    md = markdown.Markdown(extensions=["extra", "sane_lists"])
    body = md.convert(md_text)
    soup = BeautifulSoup(body, "html.parser")
    # 删掉所有 H1：微信编辑器有独立标题字段，正文不应再出现 H1
    for h1 in soup.find_all("h1"):
        h1.decompose()
    compact_lists(soup)
    promote_strong_colon(soup)
    return f"<style>{DEFAULT_CSS}</style>\n{soup}"


def fetch_cover(theme: str, fallback_url: str) -> bytes:
    # picsum 替代已下线的 source.unsplash.com，根据 theme 散列保证同篇文章稳定取相似图
    seed = abs(hash(theme)) % 1_000_000
    candidates = [
        f"https://picsum.photos/seed/{seed}/900/383",
        fallback_url,
    ]
    for url in candidates:
        if not url:
            continue
        try:
            return http(url, timeout=20)
        except SystemExit:
            continue
    sys.exit(f"ERR: 拉取封面图失败，theme={theme}")


def publish_report(md_path: Path, *, dry_run: bool = False) -> dict:
    """把一篇报告确定性地转 HTML 后入公众号草稿箱。

    从原 main() 抽出，供 CLI main() 与 syndicate 的 WeChatAdapter 共用，
    让公众号成为「一文多发」框架里的一个真渠道（复用这里的图片/渲染/草稿逻辑）。
    返回结果 dict（dry_run 时为校验摘要）；失败沿用 sys.exit（与原行为一致）。
    """
    meta_path = Path(str(md_path.with_suffix("")) + ".meta.json")

    if not md_path.is_file():
        sys.exit(f"ERR: 找不到 md {md_path}")
    # dry-run 不发布、不需要元数据；正常发布才强校验
    if not dry_run and not meta_path.is_file():
        sys.exit(f"ERR: 找不到 metadata {meta_path}（md2wechat 这一步没输出元数据）")

    md_text = md_path.read_text(encoding="utf-8")
    meta = json.loads(meta_path.read_text(encoding="utf-8")) if meta_path.is_file() else {}

    print(f"[0a] 用 markdown 库转 HTML（确定性结构）")
    raw_html = md_to_html(md_text)
    print(f"  ✓ {len(md_text)} → {len(raw_html)} bytes")

    # ── dry-run：只验证图片下载 / 转换 / 删除逻辑，不碰微信 API ──
    if dry_run:
        print("[dry-run] 图片处理（下载→转换→删除，不上传、不入草稿）")
        soup = BeautifulSoup(raw_html, "html.parser")
        merge_adjacent_uls(soup)
        img_ok, img_removed_n, img_removed = upload_external_images(
            soup, access_token="", api_base="", proxy_headers={}, dry_run=True,
        )
        print(f"  ✓ 图片 {img_ok} 可上传 / {img_removed_n} 删除")
        for it in img_removed:
            print(f"    ✗ 删除[{it['reason']}] {it['src'][:70]}")
        out_html = Path("tmp") / f"dryrun-{md_path.stem}.html"
        out_html.parent.mkdir(parents=True, exist_ok=True)
        out_html.write_text(str(soup), encoding="utf-8")
        print(f"  ✓ 处理后正文 → {out_html}（核对无破图 / 孤儿图注 / 空标题）")
        return {
            "dry_run": True,
            "report": str(md_path),
            "img_ok": img_ok,
            "img_removed": img_removed_n,
            "out_html": str(out_html),
        }

    title = meta.get("title") or md_path.stem
    digest = (meta.get("digest") or "")[:120]
    author = meta.get("author") or ""
    theme = meta.get("theme") or "stars,universe,dark"

    wx_env = load_wechat_env()
    api_base = wx_env["api_base"]
    fallback_cover = env(
        "DEFAULT_COVER_URL", required=False,
        default="https://picsum.photos/900/383",
    )
    blog_base = env(
        "BLOG_BASE_URL", required=False,
        default="https://blog.nightvoyager.top/github-explorer/reports",
    ).rstrip("/")
    # 博客 slug = 文件名 stem 小写（与 build_reports_index.py 的 normalization 对齐）
    slug = md_path.stem.lower()
    content_source_url = f"{blog_base}/{slug}/"

    proxy_h = proxy_headers(wx_env)

    # ─── Step 1: access_token ─────────────────────────────────
    print(f"[1/4] 获取 access_token（{api_base}）")
    access_token = get_access_token(wx_env)
    print(f"  ✓ token 就绪（含 tmp/wechat_token.json 缓存）")

    # ─── Step 1b: HTML 预处理 ─────────────────────────────────
    print("[1b] HTML 预处理：合并相邻 ul + 外链图片转 mmbiz")
    soup = BeautifulSoup(raw_html, "html.parser")
    merged = merge_adjacent_uls(soup)
    print(f"  ✓ 合并了 {merged} 个相邻 ul")
    img_ok, img_removed_n, img_removed = upload_external_images(
        soup,
        access_token=access_token,
        api_base=api_base,
        proxy_headers=proxy_h,
    )
    print(f"  ✓ 图片 {img_ok} 成功 / {img_removed_n} 删除")
    if img_removed:
        for it in img_removed:
            print(f"    ✗ 删除[{it['reason']}] {it['src'][:70]}", file=sys.stderr)
        Path("tmp").mkdir(exist_ok=True)
        Path("tmp/removed_images.json").write_text(
            json.dumps(img_removed, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"  ✓ 删除清单 → tmp/removed_images.json")

    # ─── Step 1c: CSS 内联 ────────────────────────────────────
    # 微信 draft/add 接口会剥 <style> 标签（与编辑器粘贴模式不同），
    # 必须把 CSS 内联到每个元素的 style 属性
    pre_inline = str(soup)
    html = inline_css(
        pre_inline,
        remove_classes=False,
        keep_style_tags=False,
        strip_important=False,
        disable_validation=True,
    )
    print(f"[1c] CSS 内联完成（{len(pre_inline)} → {len(html)} bytes）")

    # ─── Step 2: 拉封面 ───────────────────────────────────────
    print(f"[2/4] 拉封面（theme={theme}）")
    cover_data = fetch_cover(theme, fallback_cover)
    cover_path = Path("tmp/wechat_cover.jpg")
    cover_path.parent.mkdir(parents=True, exist_ok=True)
    cover_path.write_bytes(cover_data)
    print(f"  ✓ {len(cover_data)} bytes")

    # ─── Step 3: 上传封面到素材库 ─────────────────────────────
    print("[3/4] 上传封面到素材库（走反代）")
    upload_url = (
        f"{api_base}/cgi-bin/material/add_material"
        f"?access_token={urllib.parse.quote(access_token)}&type=image"
    )
    boundary, body = build_multipart("cover.jpg", cover_data)
    r = http_json_with_retry(
        upload_url,
        headers={
            **proxy_h,
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        data=body,
        method="POST",
        timeout=60,
    )
    check_wechat_ok(r, "upload material")
    if "media_id" not in r:
        sys.exit(f"ERR: 上传封面响应缺 media_id: {r}")
    thumb_media_id = r["media_id"]
    print(f"  ✓ media_id={thumb_media_id[:12]}…")

    # ─── Step 4: 入草稿箱 ─────────────────────────────────────
    print("[4/4] 入草稿箱")
    draft_url = (
        f"{api_base}/cgi-bin/draft/add"
        f"?access_token={urllib.parse.quote(access_token)}"
    )
    draft_body = json.dumps({
        "articles": [{
            "title": title,
            "author": author,
            "digest": digest,
            "content": html,
            "content_source_url": content_source_url,  # 「阅读原文」按钮指向博客
            "thumb_media_id": thumb_media_id,
            "need_open_comment": 0,
            "only_fans_can_comment": 0,
        }],
    }, ensure_ascii=False).encode("utf-8")
    r = http_json(
        draft_url,
        headers={**proxy_h, "Content-Type": "application/json"},
        data=draft_body,
        method="POST",
        timeout=60,
    )
    check_wechat_ok(r, "add draft")
    if "media_id" not in r:
        sys.exit(f"ERR: 草稿响应缺 media_id: {r}")
    draft_media_id = r["media_id"]
    print(f"  ✓ draft media_id={draft_media_id}")

    # 产物落地
    result = {
        "media_id": draft_media_id,
        "thumb_media_id": thumb_media_id,
        "title": title,
        "content_source_url": content_source_url,
        "report": str(md_path),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    Path("tmp").mkdir(exist_ok=True)
    Path("tmp/last_publish.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"✅ 已入草稿箱：{title}")
    return result


def main() -> int:
    raw_args = sys.argv[1:]
    dry_run = "--dry-run" in raw_args
    pos = [a for a in raw_args if not a.startswith("-")]
    if not pos:
        sys.exit("用法: wechat_publish.py <report.md> [--dry-run]")
    publish_report(Path(pos[0]), dry_run=dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())

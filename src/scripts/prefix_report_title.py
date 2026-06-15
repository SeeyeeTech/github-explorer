#!/usr/bin/env python3
"""给分析报告的 H1 标题统一加「GitHub推荐：」前缀（CI 流程用，幂等）。

仅处理传入的单个报告文件，**不批量改历史**——历史记录保持原样。
重复运行不会叠加前缀（已带前缀则跳过）。

用法：
    python3 src/scripts/prefix_report_title.py <report.md> [<report2.md> ...]

退出码：
    0  全部处理成功（含「已带前缀，无需改」）
    1  某个文件不存在 / 找不到 H1 标题
"""
import sys
from pathlib import Path

PREFIX = "GitHub推荐："


def prefix_title(path: Path) -> bool:
    """给单个报告的 H1 加前缀。返回是否成功定位到 H1。"""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    for i, line in enumerate(lines):
        # H1 形如「# 标题」；「## 」等子标题不匹配
        if line.startswith("# "):
            title = line[2:].lstrip()
            if title.startswith(PREFIX):
                print(f"  已带前缀，跳过: {path}")
                return True
            lines[i] = "# " + PREFIX + title
            path.write_text("\n".join(lines), encoding="utf-8")
            print(f"  已加前缀: {path}")
            return True
    print(f"::error::{path} 找不到 H1 标题（# 开头的行）", file=sys.stderr)
    return False


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    ok = True
    for arg in argv[1:]:
        p = Path(arg)
        if not p.is_file():
            print(f"::error::文件不存在: {p}", file=sys.stderr)
            ok = False
            continue
        if not prefix_title(p):
            ok = False
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

"""Import the two W08 Obsidian notes into Quarto posts."""
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = Path(r"D:\OneDrive\应用\remotely-save\EASON_HUB\AI\FIP\W8")
ITEMS = (
    ("简单线性数据结构.md", "fip-w08-linear-data-structures", "FIP W08 · 简单线性数据结构", "数组、链表、栈、队列与 deque 的基础操作和复杂度。", ["学习笔记", "数据结构"]),
    ("FIP期中复习笔记.md", "fip-midterm-review", "FIP · 期中复习笔记", "W1–W8 知识梳理、复杂度对照与考前练习。", ["学习笔记", "期中复习"]),
)


def normalize(body):
    body = body.replace("\r\n", "\n").lstrip("\ufeff")
    body = re.sub(r"(?m)^# [^\n]+\n+", "", body, count=1)
    body = re.sub(r"\[\[([^\]]+\.pdf)\]\]", lambda m: "课程材料：" + m.group(1), body)
    body = body.replace("[[0]]", "`[0]`")
    lines = body.splitlines()
    out = []
    fence = False
    math = False
    for line in lines:
        if line.startswith("```"):
            if out and out[-1].strip() and not fence:
                out.append("")
            out.append(line)
            fence = not fence
            if not fence:
                out.append("")
            continue
        if not fence and line.startswith("$$") and line.endswith("$$") and len(line) > 4:
            if out and out[-1].strip():
                out.append("")
            out.extend(("$$", line[2:-2], "$$", ""))
            continue
        if not fence and line == "$$":
            if not math and out and out[-1].strip():
                out.append("")
            out.append(line)
            math = not math
            if not math:
                out.append("")
            continue
        if not fence and re.match(r"^#{2,6} +", line):
            if out and out[-1].strip():
                out.append("")
        out.append(line)
        if not fence and re.match(r"^#{2,6} +", line):
            out.append("")
    if fence or math:
        raise ValueError("Unclosed code fence or display math")
    return "\n".join(out).strip() + "\n"


def main():
    for filename, slug, title, description, tags in ITEMS:
        source = SOURCE / filename
        created = datetime.fromtimestamp(source.stat().st_ctime, timezone(timedelta(hours=8)))
        path = ROOT / "posts" / f"{created:%Y%m%d}-{slug}" / "index.qmd"
        path.parent.mkdir(parents=True, exist_ok=True)
        body = normalize(source.read_text(encoding="utf-8-sig"))
        front = {
            "title": title, "description": description,
            "date": created.isoformat(timespec="seconds"),
            "source-created": created.isoformat(timespec="seconds"),
            "category-path": ["AI", "FIP", "学习笔记"],
            "categories": tags, "execute": {"enabled": False}, "toc-depth": 3,
        }
        metadata = "\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in front.items())
        path.write_text(f"---\n{metadata}\n---\n\n{body}", encoding="utf-8")
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()

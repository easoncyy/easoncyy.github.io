"""Copy selected FIP notes from Obsidian into the public blog."""
import argparse
import json
import re
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTES = [
    ("W2/枚举与减治.md", "w02-enumeration-decrease-conquer", "FIP W02 · 枚举与减治"),
    ("W3/迭代与模拟.md", "w03-iteration-simulation", "FIP W03 · 迭代与模拟"),
    ("W3/does-x-times-x-differ-from-x-power-2.md", "w03-python-square", "FIP W03 · x * x 与 x ** 2 的区别"),
    ("W4/序列与查找.md", "w04-sequence-search", "FIP W04 · 序列与查找"),
]


def main():
    parser = argparse.ArgumentParser(description="导入已选择的 FIP 学习笔记，保留 Obsidian 原文件")
    parser.add_argument("--source", type=Path, default=Path(r"D:\OneDrive\应用\remotely-save\EASON_HUB\AI\FIP"))
    args = parser.parse_args()
    for relative, slug, title in NOTES:
        source = args.source / relative
        stat = source.stat()
        created = datetime.fromtimestamp(getattr(stat, "st_birthtime", stat.st_ctime), timezone(timedelta(hours=8)))
        folder = ROOT / "posts" / (created.strftime("%Y%m%d") + "-fip-" + slug)
        folder.mkdir(parents=True, exist_ok=True)
        body = source.read_text(encoding="utf-8-sig")
        def image(match):
            filename, _, caption = match.group(1).partition("|")
            attachment = source.parent / filename
            if not attachment.is_file():
                raise FileNotFoundError(f"Missing embedded attachment: {attachment}")
            name = f"image-{image.count:02d}{attachment.suffix.lower()}"
            image.count += 1
            shutil.copyfile(attachment, folder / name)
            return f"![{caption or '课堂笔记插图'}]({name})"
        image.count = 1
        body = re.sub(r"!\[\[([^\]]+)\]\]", image, body)
        metadata = {"title": title, "description": f"{source.parent.name} 学习记录，按原 Markdown 文件创建时间归档。",
                    "date": created.isoformat(timespec="seconds"), "category-path": ["AI", "FIP", "学习笔记"], "categories": ["学习笔记"],
                    "execute": {"enabled": False}, "source-created": created.isoformat(timespec="seconds")}
        front = "\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in metadata.items())
        (folder / "index.qmd").write_text("---\n" + front + "\n---\n\n" + body, encoding="utf-8")
        print(f"Imported {relative} -> {folder.name} ({created.isoformat(timespec='seconds')})")


if __name__ == "__main__":
    main()

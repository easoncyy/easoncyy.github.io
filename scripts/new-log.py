"""Create a text entry with optional photos and links for the single-page log."""
import argparse
import json
import re
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description="新建日志，完成后编辑生成的 index.qmd")
    parser.add_argument("title", help="日志标题")
    parser.add_argument("--text", default="", help="完整正文")
    parser.add_argument("--url", help="要分享的 http/https 链接")
    parser.add_argument("--photo", nargs="+", type=Path, help="一张或多张本地照片路径")
    parser.add_argument("--slug", help="可选目录名，只能含英文字母、数字与连字符")
    args = parser.parse_args()
    if not args.title.strip():
        parser.error("标题不能为空")
    if args.slug and not re.fullmatch(r"[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*", args.slug):
        parser.error("slug 只能含英文字母、数字与连字符")
    if args.url and (urlparse(args.url).scheme not in ("http", "https") or not urlparse(args.url).netloc):
        parser.error("链接必须为完整 http/https URL")
    for photo in args.photo or []:
        if not photo.is_file() or photo.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"):
            parser.error(f"照片不存在或格式不支持: {photo}")
    now = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0)
    slug = now.strftime("%Y%m%d-%H%M%S") + "-" + (args.slug or "entry")
    folder = ROOT / "logs" / slug
    if folder.exists():
        parser.error(f"目录已存在，请稍后重试或更换 --slug: {folder}")
    folder.mkdir(parents=True)
    metadata = {"title": args.title, "date": now.isoformat()}
    body = [args.text or "在这里写下你的记录。"]
    if args.url:
        body.append(f"[打开分享的链接](<{args.url}>)")
    for index, photo in enumerate(args.photo or [], 1):
        name = f"photo-{index:02d}{photo.suffix.lower()}"
        media = ROOT / "assets/log" / slug
        media.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(photo, media / name)
        body.append(f"![照片 {index}，可修改这里的说明](/assets/log/{slug}/{name})")
    frontmatter = "\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in metadata.items())
    target = folder / "index.qmd"
    target.write_text("---\n" + frontmatter + "\n---\n\n" + "\n\n".join(body) + "\n", encoding="utf-8")
    print(f"Created: {target}")
    print("Edit this file, then run scripts/build.ps1 and python scripts/publish-github.py.")


if __name__ == "__main__":
    main()

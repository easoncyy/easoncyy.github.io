"""Create a diary, photo or link entry. Uses only Python's standard library."""
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
    parser.add_argument("--type", choices=["note", "photo", "link"], default="note")
    parser.add_argument("--text", default="", help="正文与摘要")
    parser.add_argument("--host", default="easoncyy.github.io", help="公开署名，不读取真实主机名")
    parser.add_argument("--url", help="要分享的 http/https 链接")
    parser.add_argument("--photo", nargs="+", type=Path, help="一张或多张本地照片路径")
    parser.add_argument("--slug", help="可选目录名，只能含英文字母、数字与连字符")
    args = parser.parse_args()
    if not args.title.strip() or not args.host.strip():
        parser.error("标题和 host 不能为空")
    if args.slug and not re.fullmatch(r"[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*", args.slug):
        parser.error("slug 只能含英文字母、数字与连字符")
    if args.url and (urlparse(args.url).scheme not in ("http", "https") or not urlparse(args.url).netloc):
        parser.error("链接必须为完整 http/https URL")
    if args.type == "link" and not args.url:
        parser.error("LINK 日志需要 --url")
    if args.type == "photo" and not args.photo:
        parser.error("PHOTO 日志需要 --photo")
    for photo in args.photo or []:
        if not photo.is_file() or photo.suffix.lower() not in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".avif"):
            parser.error(f"照片不存在或格式不支持: {photo}")
    now = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0)
    slug = now.strftime("%Y%m%d-%H%M%S") + "-" + (args.slug or args.type)
    folder = ROOT / "logs" / slug
    if folder.exists():
        parser.error(f"目录已存在，请稍后重试或更换 --slug: {folder}")
    folder.mkdir(parents=True)
    metadata = {"title": args.title, "description": args.text[:180] or "点击打开完整记录。",
                "date": now.isoformat(), "timestamp": now.isoformat(), "host": args.host, "kind": args.type}
    body = [f"`[{args.type.upper()}] host={args.host.replace('`', '')}`", args.text or "在这里写下你的记录。"]
    if args.url:
        metadata["shared-url"] = args.url
        body.append(f"[打开分享的链接](<{args.url}>)")
    for index, photo in enumerate(args.photo or [], 1):
        name = f"photo-{index:02d}{photo.suffix.lower()}"
        shutil.copyfile(photo, folder / name)
        body.append(f"![照片 {index}，可修改这里的说明]({name})")
        if index == 1:
            metadata["log-image"] = f"/logs/{slug}/{name}"
            metadata["image-alt"] = args.title
    frontmatter = "\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in metadata.items())
    target = folder / "index.qmd"
    target.write_text("---\n" + frontmatter + "\n---\n\n" + "\n\n".join(body) + "\n", encoding="utf-8")
    print(f"Created: {target}")
    print("Edit this file, then run scripts/build.ps1 and python scripts/publish-github.py.")


if __name__ == "__main__":
    main()

"""Create a text entry with optional photos and links for the single-page log."""
import argparse
import json
import hashlib
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
    parser.add_argument("--allow-duplicate", action="store_true", help="明确允许创建相同内容的日志")
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
    body_text = args.text or "在这里写下你的记录。"
    if args.url:
        body_text += f"\n\n[打开分享的链接](<{args.url}>)"
    signature = hashlib.sha256(json.dumps([args.title, body_text,
        [hashlib.sha256(photo.read_bytes()).hexdigest() for photo in args.photo or []]], ensure_ascii=False).encode('utf-8')).hexdigest()
    if not args.allow_duplicate:
        for existing in (ROOT / "logs").rglob("*.qmd"):
            parts = existing.read_text(encoding="utf-8-sig").split("---", 2)
            if len(parts) != 3:
                continue
            metadata_existing = {}
            for line in parts[1].strip().splitlines():
                if ':' not in line:
                    continue
                key, value = line.split(':', 1)
                try:
                    metadata_existing[key] = json.loads(value.strip())
                except json.JSONDecodeError:
                    metadata_existing[key] = value.strip().strip("'\"")
            same = metadata_existing.get('entry-signature') == signature
            same = same or (not args.photo and metadata_existing.get('title') == args.title and parts[2].strip() == body_text)
            if same:
                print(f"Already exists: {existing}")
                print("No duplicate created. Edit the existing file or use --allow-duplicate.")
                return
    now = datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0)
    slug = now.strftime("%Y%m%d-%H%M%S") + "-" + (args.slug or "entry")
    folder = ROOT / "logs" / slug
    if folder.exists():
        parser.error(f"目录已存在，请稍后重试或更换 --slug: {folder}")
    folder.mkdir(parents=True)
    metadata = {"title": args.title, "date": now.isoformat(), "entry-signature": signature}
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
    print("Edit this file, then run scripts/deploy.ps1 to build and publish.")


if __name__ == "__main__":
    main()

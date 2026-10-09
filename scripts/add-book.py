"""Add a local PDF or EPUB to the public library catalog."""
import argparse
import json
import re
import shutil
import zipfile
from importlib import import_module
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
taxonomy = import_module('library-taxonomy')


def main():
    parser = argparse.ArgumentParser(description="添加 PDF / EPUB 图书；完成后运行 deploy.ps1 发布")
    parser.add_argument("title")
    parser.add_argument("file", type=Path, help="本地 PDF 或 EPUB 文件路径")
    parser.add_argument("--slug", required=True, help="英文、数字与连字符组成的稳定文件名")
    parser.add_argument("--author", default="")
    parser.add_argument("--description", default="")
    parser.add_argument("--category", choices=taxonomy.CATEGORIES, default="其他", help="主分类，默认其他")
    parser.add_argument("--subject", default="", help="教材、习题、参考书的学科，如数学、计算机")
    args = parser.parse_args()
    args.subject = args.subject.strip()
    if args.category in taxonomy.ACADEMIC and not args.subject:
        parser.error("教材、习题、参考书需要 --subject 指定学科")
    if args.category not in taxonomy.ACADEMIC and args.subject:
        parser.error("只有教材、习题、参考书使用 --subject")
    if not args.title.strip() or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", args.slug):
        parser.error("标题不能为空，slug 只能包含小写英文、数字与连字符")
    if not args.file.is_file():
        parser.error("图书文件不存在")
    extension = args.file.suffix.lower()
    if extension not in (".pdf", ".epub"):
        parser.error("仅支持 .pdf 或 .epub 文件")
    if extension == ".pdf":
        with args.file.open("rb") as stream:
            if b"%PDF-" not in stream.read(1024):
                parser.error("文件内容不是 PDF")
    else:
        try:
            with zipfile.ZipFile(args.file) as archive:
                mime = archive.getinfo("mimetype")
                if mime.file_size > 128 or archive.read(mime).strip() != b"application/epub+zip":
                    parser.error("文件内容不是 EPUB：mimetype 无效")
                archive.getinfo("META-INF/container.xml")
        except (zipfile.BadZipFile, KeyError, RuntimeError, OSError) as error:
            parser.error(f"无法读取 EPUB 容器：{error}")
    if args.file.stat().st_size > 95 * 1024 * 1024:
        parser.error("文件超过 95 MB，请压缩后再添加，以免超过 GitHub 单文件限制")
    catalog = ROOT / "library/catalog.json"
    books = json.loads(catalog.read_text(encoding="utf-8"))
    target = ROOT / "assets/library" / (args.slug + extension)
    if target.exists() or any(book["slug"] == args.slug for book in books):
        parser.error("slug 已存在；更新图书时请编辑 catalog.json 并替换对应图书文件")
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(args.file, target)
    books.append({"slug": args.slug, "title": args.title, "author": args.author, "description": args.description,
                  "category": args.category, "subject": args.subject,
                  "format": extension[1:],
                  "path": "/assets/library/" + target.name,
                  "added": datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d")})
    catalog.write_text(json.dumps(books, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added: {target}. Run scripts/deploy.ps1 to publish.")


if __name__ == "__main__":
    main()

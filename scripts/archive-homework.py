"""Archive the selected homework PDFs using stable course/week names."""
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = [
    ("Calculus Homework/陈永逸-W1Homework.pdf", "calculus", "微积分", "w01", "W01", "2026-09-16"),
    ("Calculus Homework/陈永逸W2Homework.pdf", "calculus", "微积分", "w02", "W02", "2026-09-21"),
    ("Calculus Homework/CALCULUS W3.pdf", "calculus", "微积分", "w03", "W03", "2026-09-28"),
    ("Linear Algebra Homework/陈永逸W1&2Homework.pdf", "linear-algebra", "线性代数", "w01-w02", "W01–W02", "2026-09-20"),
    ("Linear Algebra Homework/陈永逸W3Homework.pdf", "linear-algebra", "线性代数", "w03", "W03", "2026-09-29"),
]


def main():
    records = []
    destination = ROOT / "assets/pdf/homework"
    destination.mkdir(parents=True, exist_ok=True)
    for original, course, label, weeks, display, date in FILES:
        filename = f"2026-{course}-{weeks}-homework.pdf"
        source = ROOT / "临时" / original
        if not source.exists():
            source = ROOT / "archive/2026-10-06-import/homework" / filename
        shutil.copyfile(source, destination / filename)
        slug = date.replace("-", "") + f"-{course}-{weeks}-homework"
        folder = ROOT / "posts" / slug
        folder.mkdir(parents=True, exist_ok=True)
        title = f"{label} {display} · 作业归档"
        metadata = {"title": title, "date": date, "categories": [label, "作业归档"],
                    "description": f"2026 年{label} {display} 作业，提供原版 PDF 在线阅读与下载。"}
        front = "\n".join(f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in metadata.items())
        url = "/assets/pdf/homework/" + filename
        body = f'''本篇归档保存{label} {display} 的作业 PDF。归档日期采用文档首页标注的作业日期。

::: {{.download-box}}
`{filename}`

[在线阅读 PDF ↗]({url}){{target="_blank"}} · [下载 PDF ↓]({url}){{download="{filename}"}}
:::

```{{=html}}
<iframe class="homework-pdf" src="{url}" title="{title} PDF" loading="lazy"></iframe>
```

如果浏览器不支持内嵌 PDF，可使用上方阅读或下载链接。
'''
        (folder / "index.qmd").write_text("---\n" + front + "\n---\n\n" + body, encoding="utf-8")
        records.append({"original": original, "published": filename, "article": slug, "date": date})
        print(f"Archived {source.name} -> {filename}")
    (ROOT / "documents/homework-archive.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

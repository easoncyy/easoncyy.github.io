"""Render the PDF catalog as Markdown for Quarto."""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    books = json.loads((ROOT / "library/catalog.json").read_text(encoding="utf-8"))
    blocks = []
    for book in sorted(books, key=lambda book: book["added"], reverse=True):
        esc = lambda value: html.escape(str(value), quote=True)
        blocks.append(f'''::: {{.library-entry}}

```{{=html}}
<div class="library-book-meta">PDF · {esc(book['added'])}</div>
<h2 class="library-book-title">{esc(book['title'])}</h2>
<p class="library-author">{esc(book.get('author', ''))}</p>
<p>{esc(book.get('description', ''))}</p>
<div class="library-actions"><a href="{esc(book['path'])}" target="_blank" rel="noopener">read / 在线阅读 ↗</a><a href="{esc(book['path'])}" download>download / 下载 ↓</a></div>
```

:::
''')
    if not blocks:
        blocks = ['::: {.empty-directory}\n\n`0 books`\n\n书架暂时为空，等待第一本书。\n\n:::']
    (ROOT / "assets/library-entries.md").write_text("\n".join(blocks), encoding="utf-8")


if __name__ == "__main__":
    main()

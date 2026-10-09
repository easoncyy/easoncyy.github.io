"""Render the PDF and EPUB catalog as Markdown for Quarto."""
import html
import json
from importlib import import_module
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
taxonomy = import_module('library-taxonomy')


def main():
    books = json.loads((ROOT / "library/catalog.json").read_text(encoding="utf-8"))
    esc = lambda value: html.escape(str(value), quote=True)
    categories = [(book, *taxonomy.classify(book)) for book in books]
    controls = ['<div class="library-filters" role="group" aria-label="图书分类">',
                '<button type="button" data-library-category="all" aria-pressed="true">全部</button>']
    for category in taxonomy.CATEGORIES:
        count = sum(current == category for _, current, _ in categories)
        controls.append(f'<button type="button" data-library-category="{esc(category)}" aria-pressed="false">{esc(category)} <span class="library-filter-count">{count}</span></button>')
    controls.extend(['</div>', '<div id="library-subjects" class="library-subjects" role="group" aria-label="学科" hidden></div>',
                     '<p id="library-count" class="library-count" aria-live="polite"></p>'])
    blocks = ['```{=html}\n' + '\n'.join(controls) + '\n```']
    for book in sorted(books, key=lambda book: book["added"], reverse=True):
        category, subject = taxonomy.classify(book)
        classification = category + (" / " + subject if subject else "")
        book_format = book.get("format", Path(urlsplit(book["path"]).path).suffix.lstrip(".") or "pdf").lower()
        actions = f'<a href="{esc(book["path"])}" download>download / 下载 ↓</a>'
        if book_format == "pdf" and not book.get("download-only"):
            actions = f'<a href="{esc(book["path"])}" target="_blank" rel="noopener">read / 在线阅读 ↗</a>' + actions
        if book_format == "epub":
            actions += '<span class="library-author">EPUB · 下载后用电子书阅读器打开</span>'
        blocks.append(f'''::: {{.library-entry data-category="{esc(category)}" data-subject="{esc(subject)}"}}

```{{=html}}
<div class="library-book-meta">{esc(classification)} · {esc(book_format.upper())} · {esc(book['added'])}</div>
<h2 class="library-book-title">{esc(book['title'])}</h2>
<p class="library-author">{esc(book.get('author', ''))}</p>
<p>{esc(book.get('description', ''))}</p>
<div class="library-actions">{actions}</div>
```

:::
''')
    blocks.append('```{=html}\n<p id="library-empty" class="empty-directory"' + (' hidden' if books else '') + '>书架暂时为空，等待第一本书。</p>\n```')
    (ROOT / "assets/library-entries.md").write_text("\n".join(blocks), encoding="utf-8")


if __name__ == "__main__":
    main()

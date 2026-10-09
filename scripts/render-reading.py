"""Render reading highlights and named reading lists."""
import html
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
STATUSES={'reading':'正在阅读','planned':'计划阅读','completed':'完成阅读'}
def main():
    catalog={b['slug']:b for b in json.loads((ROOT/'library/catalog.json').read_text(encoding='utf-8'))}
    lists=json.loads((ROOT/'library/reading.json').read_text(encoding='utf-8'))['lists']
    esc=lambda x:html.escape(str(x),quote=True)
    featured=[]; sections=[]; seen=set()
    for listing in lists:
        groups={s:[] for s in STATUSES}
        for item in listing['items']:
            key=listing['id']+'/'+item['id']
            if key in seen: raise ValueError('Duplicate reading item: '+key)
            seen.add(key)
            book=catalog[item['book']] if 'book' in item else item
            status=item.get('status','planned')
            if status not in STATUSES: raise ValueError('Unknown reading status: '+status)
            url=book.get('path',book.get('url',''))
            if url and not (url.startswith('/') or url.startswith('https://') or url.startswith('http://')): raise ValueError('Invalid book URL')
            title=esc(book['title']);note=esc(item.get('note',''))
            link=f'<a href="{esc(url)}" target="_blank" rel="noopener">{title} ↗</a>' if url else title
            action=f'<a href="{esc(url)}" target="_blank" rel="noopener" aria-label="打开 {title}">↗</a>' if url else ''
            checked='checked' if status=='completed' else ''
            groups[status].append(f'<li><label><input type="checkbox" disabled {checked}><span>{title}</span></label>{action}<small>{note}</small></li>')
            if status=='reading': featured.append(f'<article class="reading-feature"><h3>{link}</h3><p>{esc(book.get("author",""))}</p><p>{note}</p></article>')
        columns=''.join(f'<section><h4>{label} <small>{len(groups[status])}</small></h4><ul>{"".join(groups[status]) or "<li class=reading-empty>暂无</li>"}</ul></section>' for status,label in STATUSES.items())
        sections.append(f'<section class="reading-list"><h3>{esc(listing["title"])}</h3><div class="reading-columns">{columns}</div></section>')
    output='<section><h2>reading/ <small>正在阅读</small></h2><div class="reading-features">'+(''.join(featured) or '<p>还没有正在阅读的书。</p>')+'</div></section>'
    output+='<section><h2>lists/ <small>书单</small></h2>'+(''.join(sections) or '<p>书单暂时为空。</p>')+'</section>'
    (ROOT/'assets/reading-entries.md').write_text('```{=html}\n'+output+'\n```\n',encoding='utf-8')
if __name__=='__main__': main()

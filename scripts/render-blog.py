"""Render hierarchical blog directory. Requires PyYAML."""
import html
import json
from pathlib import Path
import yaml
ROOT = Path(__file__).resolve().parent.parent
def main():
    records=[]
    for file in (ROOT/'posts').rglob('*.qmd'):
        text=file.read_text(encoding='utf-8-sig')
        if not text.startswith('---'): continue
        m=yaml.safe_load(text.split('---',2)[1]) or {}
        if m.get('draft'): continue
        path=m.get('category-path',['OTHER'])
        if isinstance(path,str): path=path.split('/')
        if not isinstance(path,list) or not path or any(not isinstance(p,str) or not p.strip() for p in path): raise ValueError(f'{file}: invalid category-path')
        tags=m.get('categories',[])
        if isinstance(tags,str): tags=[tags]
        records.append(dict(title=m.get('title',file.stem),description=m.get('description',''),date=str(m.get('date','')),path=path,tags=tags,url='/'+file.relative_to(ROOT).with_suffix('.html').as_posix()))
    records.sort(key=lambda r:r['date'],reverse=True)
    esc=lambda x:html.escape(str(x),quote=True)
    out=['<div class="blog-layout"><div class="blog-main"><div class="blog-tools"><label>search / 搜索 <input id="blog-search" type="search" placeholder="标题、摘要、标签…"></label><div id="blog-mobile-directory"></div><details><summary>标签</summary><div id="blog-tags"></div></details><p id="blog-count" aria-live="polite"></p></div>']
    for r in records:
        out.append(f'<article class="blog-entry" data-record="{esc(json.dumps(r,ensure_ascii=False))}"><div class="entry-path">~/notes/blog/{esc("/".join(r["path"]))} · <time datetime="{esc(r["date"])}">{esc(r["date"][:10])}</time></div><h2><a href="{esc(r["url"])}">{esc(r["title"])}</a></h2><p>{esc(r["description"])}</p><div class="entry-tags">{" ".join("#"+esc(t) for t in r["tags"])}</div></article>')
    out.append('<p id="blog-empty" hidden>没有符合条件的文章。</p><nav id="blog-pages" aria-label="文章分页"></nav></div><aside class="blog-directory" aria-label="博客目录"><div class="directory-command">$ ls ~/notes/blog</div><div id="blog-paths"></div></aside></div>')
    (ROOT/'assets/blog-entries.md').write_text('```{=html}\n'+'\n'.join(out)+'\n```\n',encoding='utf-8')
if __name__=='__main__': main()

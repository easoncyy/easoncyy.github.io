"""Register the six books supplied on 2026-10-10."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
BOOKS=[
 ('Introduction to Linear Algebra', 'introduction-to-linear-algebra', 'Introduction to Linear Algebra · 第5版', 'Gilbert Strang', '教材', '数学'),
 ('百年法', 'hundred-year-law', '百年法（全2册）', '山田宗树', '文学', ''),
 ('数据结构与算法分析', 'data-structures-algorithm-analysis', '数据结构与算法分析', 'Mark Allen Weiss', '教材', '计算机'),
 ('动手学深度学习', 'dive-into-deep-learning', '动手学深度学习 · PyTorch 第2版', 'Aston Zhang、Zachary C. Lipton、李沐等', '教材', '人工智能'),
 ('科学究竟是什么', 'what-is-this-thing-called-science', '科学究竟是什么', 'A. F. 查尔默斯', '哲学', ''),
 ('人工智能 一种现代的方法', 'artificial-intelligence-modern-approach', '人工智能：一种现代的方法 · 第3版', 'Stuart Russell、Peter Norvig', '教材', '人工智能'),
]
def main():
    file=ROOT/'library/catalog.json';catalog=json.loads(file.read_text(encoding='utf-8'))
    for prefix,slug,title,author,category,subject in BOOKS:
        if any(b['slug']==slug for b in catalog): continue
        matches=[p for p in (ROOT/'assets/library').iterdir() if p.name.startswith(prefix)]
        if len(matches)!=1: raise ValueError(f'Expected one file for {prefix}: {matches}')
        source=matches[0];extension=source.suffix.lower();large=source.stat().st_size>95*1024*1024
        folder=ROOT/('archive/2026-10-10-import/books' if large else 'assets/library')
        folder.mkdir(parents=True,exist_ok=True);target=folder/(slug+extension)
        if target.exists(): raise ValueError('Target exists: '+str(target))
        source.rename(target)
        url=f'https://github.com/easoncyy/easoncyy.github.io/releases/download/library-2026-10-10/{target.name}' if large else '/assets/library/'+target.name
        book=dict(slug=slug,title=title,author=author,category=category,subject=subject,description='',format=extension[1:],path=url,added='2026-10-10')
        if large: book.update({'download-only':True,'description':'通过 GitHub Release 下载。'})
        catalog.append(book)
        print(slug, 'Release' if large else 'Pages')
    file.write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    reading=['introduction-to-linear-algebra','hundred-year-law','computer-systems','data-structures-algorithm-analysis']
    planned=['project-hail-mary','soulstealers-1768','dive-into-deep-learning','what-is-this-thing-called-science','artificial-intelligence-modern-approach']
    data={'lists':[{'id':'personal','title':'我的书单','items':[{'id':slug,'book':slug,'status':status} for status,slugs in [('reading',reading),('planned',planned)] for slug in slugs]}]}
    (ROOT/'library/reading.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__': main()

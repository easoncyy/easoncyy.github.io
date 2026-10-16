"""Validated local library edits shared by the desktop manager."""
import json
import shutil
import zipfile
from pathlib import Path
from urllib.parse import urlsplit
from importlib import import_module
from problem_store import ROOT, valid_id, today, write_json

taxonomy=import_module('library-taxonomy')
CATALOG=ROOT/'library/catalog.json'
READING=ROOT/'library/reading.json'
STATES={'未加入书单':'','正在阅读':'reading','计划阅读':'planned','完成阅读':'completed'}

def load_books():
    return json.loads(CATALOG.read_text(encoding='utf-8'))

def load_reading():
    return json.loads(READING.read_text(encoding='utf-8'))

def validate_file(path):
    path=Path(path)
    if not path.is_file():raise ValueError('所选文件不存在')
    if path.suffix.lower() not in ('.pdf','.epub'):raise ValueError('请选择 PDF 或 EPUB 文件')
    if path.stat().st_size>95*1024*1024:raise ValueError('文件超过 95 MB。请通过 GitHub Release 上传后，将下载地址填入“外部文件链接”。')
    if path.suffix.lower()=='.pdf':
        with path.open('rb') as stream:
            if b'%PDF-' not in stream.read(1024):raise ValueError('文件内容不是有效 PDF')
    else:
        try:
            with zipfile.ZipFile(path) as archive:
                info=archive.getinfo('mimetype')
                if info.file_size>128 or archive.read(info).strip()!=b'application/epub+zip':raise ValueError('EPUB 格式标识无效')
                archive.getinfo('META-INF/container.xml')
        except (zipfile.BadZipFile,KeyError,RuntimeError) as error:raise ValueError('无法读取 EPUB：'+str(error)) from error
    return path

def save_book(values,original=None,local_file=None,backup=lambda path:None):
    slug=valid_id(values['slug'].strip());books=load_books()
    previous=next((b for b in books if b['slug']==original),None) if original else None
    if original and previous is None:raise ValueError('该书目已不存在，请刷新后重试')
    if original and slug!=original:raise ValueError('已存在书目的 ID 不可修改，以免破坏书单引用')
    if not original and any(b['slug']==slug for b in books):raise ValueError('书目 ID 已存在，请换一个 ID')
    if not values['title'].strip():raise ValueError('请填写书名')
    book=dict(previous or {})
    book.update({k:values[k].strip() for k in ['title','author','description','category','subject']})
    taxonomy.classify(book)
    if book['category'] in taxonomy.ACADEMIC and not book['subject']:raise ValueError('教材、习题和参考书需要填写学科')
    if local_file:
        source=validate_file(local_file);target=ROOT/'assets/library'/(slug+source.suffix.lower())
        if target.exists() and source.resolve()!=target.resolve() and (not previous or previous.get('path')!='/assets/library/'+target.name):raise ValueError('目标文件名已经存在，请换一个 ID')
        if source.resolve()!=target.resolve():
            target.parent.mkdir(parents=True,exist_ok=True);backup(target);shutil.copy2(source,target)
        book['path']='/assets/library/'+target.name;book['format']=target.suffix[1:]
        book.pop('download-only',None)
    elif values.get('url','').strip():
        url=values['url'].strip();parsed=urlsplit(url)
        if parsed.scheme not in ('http','https') or not parsed.netloc:raise ValueError('外部文件链接必须是完整 HTTP/HTTPS 地址')
        book['path']=url;book['format']=values.get('format','pdf');book['download-only']=True
    elif not previous:raise ValueError('请选择图书文件，或填写外部文件链接')
    book['slug']=slug;book.setdefault('added',today())
    if previous:books[books.index(previous)]=book
    else:books.append(book)
    backup(CATALOG);write_json(CATALOG,books)
    return book

def save_reading(slug,list_id,title,status,note,backup=lambda path:None):
    valid_id(list_id)
    if status not in ('','reading','planned','completed'):raise ValueError('阅读状态无效')
    data=load_reading();listing=next((x for x in data['lists'] if x['id']==list_id),None)
    if listing is None:
        if not status:return
        listing={'id':list_id,'title':title.strip() or '我的书单','items':[]};data['lists'].append(listing)
    if title.strip():listing['title']=title.strip()
    item=next((x for x in listing['items'] if x.get('book')==slug),None)
    if not status:listing['items']=[x for x in listing['items'] if x.get('book')!=slug]
    else:
        if item is None:item={'id':slug,'book':slug};listing['items'].append(item)
        item.update(status=status,note=note.strip())
    backup(READING);write_json(READING,data)

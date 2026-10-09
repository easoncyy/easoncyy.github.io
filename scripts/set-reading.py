"""Add or update a catalog book in a named public reading list."""
import argparse
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('book',help='Book slug from library/catalog.json')
    p.add_argument('--status',choices=['reading','planned','completed'],default='planned')
    p.add_argument('--list',dest='list_id',default='personal')
    p.add_argument('--title',help='Name of the reading list')
    p.add_argument('--note',help='Reading note; omit to preserve existing note')
    p.add_argument('--remove',action='store_true')
    args=p.parse_args()
    catalog=json.loads((ROOT/'library/catalog.json').read_text(encoding='utf-8'))
    if args.book not in {b['slug'] for b in catalog}: p.error('Unknown book slug')
    file=ROOT/'library/reading.json';data=json.loads(file.read_text(encoding='utf-8'))
    listing=next((x for x in data['lists'] if x['id']==args.list_id),None)
    if listing is None:
        if args.remove: p.error('Reading list does not exist')
        listing={'id':args.list_id,'title':args.title or '我的书单','items':[]};data['lists'].append(listing)
    if args.title: listing['title']=args.title
    item=next((x for x in listing['items'] if x['id']==args.book),None)
    if args.remove: listing['items']=[x for x in listing['items'] if x['id']!=args.book]
    else:
        if item is None: item={'id':args.book,'book':args.book};listing['items'].append(item)
        item['status']=args.status
        if args.note is not None: item['note']=args.note
    file.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f'Updated {args.list_id}: {args.book}')
if __name__=='__main__': main()

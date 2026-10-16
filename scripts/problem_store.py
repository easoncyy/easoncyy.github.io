"""Shared question-bank and schedule storage for Quarto and the local manager."""
import json
import re
from datetime import datetime, timedelta, timezone, date
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
BANK = ROOT / 'problems/bank'
SCHEDULE = ROOT / 'problems/schedule.json'
ANSWER = '<!-- answer -->'

def today():
    return datetime.now(timezone(timedelta(hours=8))).date().isoformat()

def valid_id(value):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value):
        raise ValueError('题目 ID 只能使用小写英文、数字和连字符')
    return value

def load_bank(folder=BANK):
    bank = {}
    for file in sorted(folder.glob('*.qmd')):
        slug = valid_id(file.stem)
        parts = file.read_text(encoding='utf-8-sig').split('---', 2)
        if len(parts) != 3 or parts[0].strip():
            raise ValueError(f'{file.name}: 需要 YAML 元数据')
        meta = yaml.safe_load(parts[1]) or {}
        if ANSWER not in parts[2]:
            raise ValueError(f'{file.name}: 缺少 {ANSWER} 答案分隔标记')
        question, answer = parts[2].split(ANSWER, 1)
        path = meta.get('category-path', ['OTHER'])
        if isinstance(path, str): path = path.split('/')
        tags = meta.get('tags', [])
        if isinstance(tags, str): tags = [tags]
        if not isinstance(path, list) or not path or any(not isinstance(p, str) or not p.strip() for p in path):
            raise ValueError(f'{file.name}: 分类目录格式错误')
        if not isinstance(tags, list) or any(not isinstance(t, str) for t in tags):
            raise ValueError(f'{file.name}: 标签必须是文字列表')
        if not str(meta.get('title', '')).strip():
            raise ValueError(f'{file.name}: 标题不能为空')
        if not meta.get('draft', False) and (not question.strip() or not answer.strip()):
            raise ValueError(f'{file.name}: 可排期题目必须填写题目和答案；尚未完成时请保存为草稿')
        bank[slug] = dict(id=slug, title=str(meta['title']), path=path, tags=tags,
                          source=str(meta.get('source', '')), draft=bool(meta.get('draft', False)),
                          question=question.strip(), answer=answer.strip(), file=file)
    return bank

def load_schedule(bank=None):
    data = json.loads(SCHEDULE.read_text(encoding='utf-8'))
    if not isinstance(data, dict): raise ValueError('排期必须是日期到题目 ID 列表的映射')
    for day, ids in data.items():
        if date.fromisoformat(day).isoformat() != day: raise ValueError('日期必须使用 YYYY-MM-DD')
        if not isinstance(ids, list) or any(not isinstance(i, str) for i in ids):
            raise ValueError(f'{day}: 排期必须是题目 ID 列表')
        if len(set(ids)) != len(ids): raise ValueError(f'{day}: 同一天不能重复排入同一道题')
        if bank is not None:
            for slug in ids:
                if slug not in bank: raise ValueError(f'{day}: 找不到题目 {slug}')
                if bank[slug]['draft']: raise ValueError(f'{day}: {slug} 仍是草稿，请先取消草稿状态')
    return data

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)


def problem_status(item, schedule):
    dates=sorted(day for day,ids in schedule.items() if item['id'] in ids)
    cutoff=today()
    expired=any(day<=cutoff for day in dates);future=any(day>cutoff for day in dates)
    progress='已到期/待发布' if expired and future else '已到期' if expired else '待发布' if future else '未排期'
    return ('草稿' if item['draft'] else '可排期'),progress,dates

def save_problem(slug, title, path, tags, question, answer, source='', draft=False):
    valid_id(slug)
    if not title.strip(): raise ValueError('标题不能为空')
    if not draft and (not question.strip() or not answer.strip()):
        raise ValueError('可排期题目必须填写题目和答案；尚未完成时请勾选草稿')
    if not path or any(not p.strip() for p in path): raise ValueError('至少填写一级分类')
    if ANSWER in question or ANSWER in answer: raise ValueError('正文不能包含答案分隔标记')
    meta = {'title': title.strip(), 'category-path': path, 'tags': tags, 'source': source.strip(), 'draft': draft}
    front = '\n'.join(f'{key}: {json.dumps(value, ensure_ascii=False)}' for key,value in meta.items())
    BANK.mkdir(parents=True, exist_ok=True)
    target = BANK / (slug + '.qmd')
    target.write_text('---\n' + front + '\n---\n\n' + question.strip() + '\n\n' + ANSWER + '\n\n' + answer.strip() + '\n', encoding='utf-8')
    return target


def trash_problem(slug):
    valid_id(slug)
    bank=load_bank()
    if slug not in bank: raise ValueError('这道题已不存在，请刷新列表')
    schedule=load_schedule(bank)
    days=[day for day,ids in schedule.items() if slug in ids]
    changed={day:[item for item in ids if item!=slug] for day,ids in schedule.items()}
    folder=ROOT/'archive/problem-trash'/datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    folder.mkdir(parents=True)
    write_json(folder/'record.json',{'id':slug,'removed-from-dates':days,'schedule-before':schedule})
    target=folder/(slug+'.qmd')
    bank[slug]['file'].rename(target)
    try: write_json(SCHEDULE,changed)
    except Exception:
        target.rename(bank[slug]['file'])
        raise
    return target,days


def restore_problem(file):
    file=Path(file).resolve()
    if not file.is_relative_to((ROOT/'archive/problem-trash').resolve()) or not file.is_file():
        raise ValueError('请选择题目回收站中的 .qmd 文件')
    valid_id(file.stem)
    if file.stem not in load_bank(file.parent): raise ValueError('题目文件无效')
    target=BANK/file.name
    if target.exists(): raise ValueError('题库已有相同 ID，无法覆盖；请先处理重名题目')
    file.rename(target)
    return target

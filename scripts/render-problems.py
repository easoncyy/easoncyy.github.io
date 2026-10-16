"""Publish only the scheduled questions whose Beijing date has arrived."""
import html
import json
from problem_store import ROOT, today, load_bank, load_schedule

def main():
    bank = load_bank()
    schedule = load_schedule(bank)
    cutoff = today()
    days = sorted((day for day, ids in schedule.items() if day <= cutoff and ids), reverse=True)
    esc = lambda value: html.escape(str(value), quote=True)
    out = []
    for day in days:
        out.extend([f'::: {{.problem-day data-date="{day}"}}', f'## {day} {{.problem-date-heading}}'])
        for number, slug in enumerate(schedule[day], 1):
            item = bank[slug]
            record = json.dumps({'path':item['path'], 'tags':item['tags'], 'title':item['title']}, ensure_ascii=False)
            out.extend([f'::: {{.problem-entry data-problem="{esc(record)}"}}',
                        '```{=html}', f'<div class="problem-meta">{" / ".join(esc(p) for p in item["path"])}</div>',
                        f'<h3>{number:02d}. {esc(item["title"])}</h3>',
                        '<div class="entry-tags">' + ' · '.join('#'+esc(t) for t in item['tags']) + '</div>', '```',
                        item['question'], '```{=html}', '<details class="problem-answer"><summary>answer/ 展开答案</summary><div class="problem-solution">', '```',
                        item['answer'], '```{=html}', '</div></details>',
                        (f'<p class="problem-source">来源：{esc(item["source"])}</p>' if item['source'] else ''), '```', ':::'])
        out.extend(['```{=html}',
                    f'<details id="discussion-{day}" class="log-comments problem-discussion" data-comment-term="/problems/{day}/" data-comment-date="{day}" data-comment-title="每日好题 · {day}">',
                    f'<summary>discussion/ <span>{day} · 当日讨论</span></summary>',
                    '<div class="log-comments-body"><p class="log-comments-status" aria-live="polite">展开后加载讨论，使用 GitHub 账号分享思路、提问或勘误。</p><div class="log-comments-widget"></div></div>',
                    '</details>', '```', ':::'])
    if not out: out = ['::: {.problem-initial-empty}', '题库已就绪，等待第一组每日好题。', ':::']
    metadata = {'builtDate':cutoff, 'dates':{day:len(schedule[day]) for day in days}}
    out.extend(['```{=html}', '<script id="problem-index" type="application/json">'+json.dumps(metadata, ensure_ascii=False).replace('<','\\u003c')+'</script>', '```'])
    (ROOT/'assets/problem-entries.md').write_text('\n\n'.join(out)+'\n', encoding='utf-8')

if __name__ == '__main__': main()

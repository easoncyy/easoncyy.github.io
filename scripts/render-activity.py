"""Build a monochrome calendar from GitHub's public contribution calendar."""
import html
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'assets/github-activity.svg'


def main():
    try:
        request = urllib.request.Request('https://github.com/users/easoncyy/contributions', headers={'User-Agent': 'homepage-activity'})
        with urllib.request.urlopen(request, timeout=15) as response:
            source = response.read().decode()
        cells = []
        for tag in re.findall(r'<td\b[^>]*>', source):
            attrs = dict(re.findall(r'([\w-]+)="([^"]*)"', tag))
            if 'data-date' in attrs:
                cells.append(attrs)
        tips = {key: html.unescape(re.sub('<[^>]+>', '', value)).strip() for key, value in re.findall(r'<tool-tip\b[^>]*for="([^"]+)"[^>]*>(.*?)</tool-tip>', source, re.S)}
        cells.sort(key=lambda c: c['data-date'])
        if len(cells) < 350 or not tips:
            raise ValueError('Incomplete GitHub calendar')
        from datetime import date
        first = date.fromisoformat(cells[0]['data-date'])
        colors = ['#eeeeec', '#c6c6c2', '#92928d', '#565652', '#191919']
        total = re.search(r'id="js-contribution-activity-description"[^>]*>\s*([\d,]+)', source)
        title = (total.group(1) if total else '') + ' contributions · last year'
        parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 172" role="img" aria-labelledby="title"><title id="title">{title}</title>', '<style>text{font-family:monospace;fill:#666;font-size:10px}rect:focus{stroke:#000;stroke-width:2;outline:none}</style>', f'<text x="0" y="16" style="fill:#222;font-size:12px">{title}</text>']
        months = set()
        for cell in cells:
            day = date.fromisoformat(cell['data-date'])
            offset = (day-first).days + (first.weekday()+1)%7
            x,y = 30+(offset//7)*15, 44+(offset%7)*15
            if day.month not in months and (day.day<=7 or day==first):
                months.add(day.month)
                parts.append(f'<text x="{x}" y="35">{day.strftime("%b")}</text>')
            label = html.escape(f'{day.isoformat()}: {tips.get(cell["id"], "")}', quote=True)
            parts.append(f'<rect x="{x}" y="{y}" width="11" height="11" rx="2" fill="{colors[int(cell["data-level"])]}" tabindex="0" aria-label="{label}"><title>{label}</title></rect>')
        for row,label in [(1,'Mon'),(3,'Wed'),(5,'Fri')]:
            parts.append(f'<text x="0" y="{53+row*15}">{label}</text>')
        parts.append('<text x="650" y="166">less</text>')
        for i,c in enumerate(colors):
            parts.append(f'<rect x="{682+i*15}" y="156" width="11" height="11" rx="2" fill="{c}"/>')
        parts.append('<text x="762" y="166">more</text></svg>')
        TARGET.write_text(''.join(parts), encoding='utf-8')
        print('Updated GitHub activity calendar.')
    except Exception as error:
        if TARGET.exists():
            print(f'GitHub activity unavailable; keeping previous calendar: {error}')
        else:
            raise


if __name__ == '__main__':
    main()

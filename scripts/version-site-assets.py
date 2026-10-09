"""Version local CSS/JS URLs so browsers fetch changed site assets."""
import hashlib
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / '_site'
ATTR = re.compile(r'(?P<prefix>\b(?:src|href)=\")(?P<url>[^\"]+)(?P<suffix>\")')

def main():
    count = 0
    for page in SITE.rglob('*.html'):
        def version(match):
            parsed = urlsplit(match['url'])
            if parsed.scheme or parsed.netloc or not parsed.path.endswith(('.css', '.js')):
                return match.group(0)
            target = (SITE / parsed.path.lstrip('/') if parsed.path.startswith('/') else page.parent / parsed.path).resolve()
            if not target.is_relative_to(SITE.resolve()) or not target.is_file():
                return match.group(0)
            relative = target.relative_to(SITE.resolve()).as_posix()
            if relative != 'styles.css' and not relative.startswith('assets/'):
                return match.group(0)
            digest = hashlib.sha256(target.read_bytes()).hexdigest()[:12]
            url = parsed.path + '?v=' + digest + ('#' + parsed.fragment if parsed.fragment else '')
            return match['prefix'] + url + match['suffix']
        old = page.read_text(encoding='utf-8')
        new = ATTR.sub(version, old)
        if new != old:
            page.write_text(new, encoding='utf-8')
            count += 1
    print(f'Versioned site assets in {count} pages.')

if __name__ == '__main__':
    main()

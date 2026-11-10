"""Reuse unchanged article HTML; rebuild shared pages and invalidate on global changes."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / '.quarto/local-build-state.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render(command):
    for attempt in range(3):
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode == 0:
            return
        if attempt < 2:
            print('Render failed; retrying after releasing temporary file handles.', flush=True)
            time.sleep(2)
    result.check_returncode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('quarto')
    parser.add_argument('--full', action='store_true')
    args = parser.parse_args()
    pages = sorted([*ROOT.glob('*.qmd'), *ROOT.glob('posts/**/*.qmd')])
    global_files = sorted(set(
        [*ROOT.glob('_quarto*'), *ROOT.glob('*.css'), *ROOT.glob('posts/**/_metadata.*'),
         *ROOT.glob('scripts/*.py'), *ROOT.glob('scripts/*.ps1')]
    ))
    current = {
        'pages': {p.relative_to(ROOT).as_posix(): digest(p) for p in pages},
        'global': {p.relative_to(ROOT).as_posix(): digest(p) for p in global_files if p.is_file()},
        'version': subprocess.check_output([args.quarto, '--version'], text=True).strip(),
    }
    try:
        old = json.loads(STATE.read_text(encoding='utf-8'))
    except (OSError, ValueError):
        old = {}
    removed = set(old.get('pages', {})) - set(current['pages'])
    full = (args.full or old.get('global') != current['global']
            or old.get('version') != current['version'] or bool(removed)
            or any(not (ROOT / '_site' / Path(p).with_suffix('.html')).exists()
                   for p in current['pages']))
    if full:
        print('Full website render (initial build, missing output, or global changes).', flush=True)
        render([args.quarto, 'render'])
    else:
        # Shared pages depend on generated includes, publication dates and listings.
        targets = [p for p, value in current['pages'].items()
                   if '/' not in p or old['pages'].get(p) != value]
        print(f'Incremental render: {len(targets)} pages; unchanged articles reused.', flush=True)
        for target in targets:
            render([args.quarto, 'render', target])
    STATE.parent.mkdir(exist_ok=True)
    STATE.write_text(json.dumps(current, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()

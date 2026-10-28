"""Dispatch a Pages build from the source already pushed to main."""
import argparse
import subprocess
from pathlib import Path
from github_api import api

ROOT = Path(__file__).resolve().parent.parent
API_ROOT = "repos/easoncyy/easoncyy.github.io"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runner', choices=['ubuntu-latest', 'windows-latest'], default='ubuntu-latest')
    args = parser.parse_args()
    branch = subprocess.check_output(['git', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
    if branch != 'main':
        raise RuntimeError('Switch to main and run scripts/sync.ps1 before publishing.')
    local = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    remote = api('GET', f'{API_ROOT}/git/ref/heads/main')['object']['sha']
    if local != remote:
        raise RuntimeError('Local HEAD differs from remote main. Run scripts/sync.ps1 before publishing.')
    workflow = api('GET', f'{API_ROOT}/actions/workflows/publish-pages.yml', allow_missing=True)
    if not workflow:
        raise RuntimeError('Push .github/workflows/publish-pages.yml to main before publishing.')
    api('POST', f'{API_ROOT}/actions/workflows/publish-pages.yml/dispatches',
        {'ref': 'main', 'inputs': {'rebuild': True, 'runner': args.runner}})
    print(f'Pages build requested from main ({remote[:7]}).', flush=True)
    print('Source is uploaded; GitHub Actions will build and deploy the website.', flush=True)
    print('Deployment status: https://github.com/easoncyy/easoncyy.github.io/actions/workflows/publish-pages.yml', flush=True)


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as error:
        raise SystemExit(str(error))

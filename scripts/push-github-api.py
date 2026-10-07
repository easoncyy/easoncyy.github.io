"""Push unsigned local Git objects via REST when Git HTTPS transport fails."""
import base64
import re
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from github_api import api

ROOT = Path(__file__).resolve().parent.parent
REPO = 'repos/easoncyy/easoncyy.github.io'


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def identity(value):
    match = re.fullmatch(r'(.*) <(.*)> (\d+) ([+-])(\d{2})(\d{2})', value)
    if not match:
        raise RuntimeError('Unsupported commit identity format.')
    name, email, stamp, sign, hours, minutes = match.groups()
    offset = (int(hours) * 60 + int(minutes)) * (1 if sign == '+' else -1)
    return {'name': name, 'email': email,
            'date': datetime.fromtimestamp(int(stamp), timezone(timedelta(minutes=offset))).isoformat()}


def main():
    remote = api('GET', f'{REPO}/git/ref/heads/main')['object']['sha']
    head = git('rev-parse', 'HEAD').decode().strip()
    if remote == head:
        print('GitHub API: origin/main already matches local HEAD.')
        return
    ancestor = subprocess.run(['git', 'merge-base', '--is-ancestor', remote, head], cwd=ROOT)
    if ancestor.returncode:
        raise RuntimeError('Remote main is not an ancestor of local HEAD. Fetch and reconcile histories before retrying.')
    previous_tree = api('GET', f'{REPO}/git/commits/{remote}')['tree']['sha']
    existing = api('GET', f'{REPO}/git/trees/{previous_tree}?recursive=1')['tree']
    known = {item['sha'] for item in existing if item['type'] == 'blob'}
    commits = git('rev-list', '--reverse', '--topo-order', f'{remote}..{head}').decode().splitlines()
    for sha in commits:
        entries = []
        for line in git('ls-tree', '-rz', sha).split(b'\0'):
            if not line:
                continue
            fields, name = line.split(b'\t', 1)
            mode, kind, blob_sha = fields.decode().split()
            if kind != 'blob':
                raise RuntimeError('Git API fallback does not support submodules.')
            if blob_sha not in known:
                blob = api('POST', f'{REPO}/git/blobs', {'encoding': 'base64',
                    'content': base64.b64encode(git('cat-file', 'blob', blob_sha)).decode('ascii')})
                if blob['sha'] != blob_sha:
                    raise RuntimeError('Uploaded blob hash differs from local object.')
                known.add(blob_sha)
            entries.append({'path': name.decode('utf-8'), 'mode': mode, 'type': kind, 'sha': blob_sha})
        tree = api('POST', f'{REPO}/git/trees', {'tree': entries})
        header, message = git('cat-file', 'commit', sha).decode('utf-8').split('\n\n', 1)
        payload = {'parents': [], 'message': message}
        for line in header.splitlines():
            key, value = line.split(' ', 1)
            if key == 'parent': payload['parents'].append(value)
            elif key in ('author', 'committer'): payload[key] = identity(value)
            elif key == 'tree': payload['tree'] = value
            else: raise RuntimeError(f'Unsupported commit header: {key}; cannot preserve this commit through REST.')
        if tree['sha'] != payload['tree']:
            raise RuntimeError('Uploaded tree hash differs from local tree.')
        commit = api('POST', f'{REPO}/git/commits', payload)
        if commit['sha'] != sha:
            raise RuntimeError('API commit hash differs from local commit. Remote branch was not changed.')
        print(f'Uploaded Git commit: {sha[:7]}', flush=True)
    api('PATCH', f'{REPO}/git/refs/heads/main', {'sha': head, 'force': False})
    actual = api('GET', f'{REPO}/git/ref/heads/main')['object']['sha']
    if actual != head:
        raise RuntimeError('Remote main did not match local HEAD after update.')
    subprocess.run(['git', 'update-ref', 'refs/remotes/origin/main', head], cwd=ROOT, check=True)
    print(f'GitHub API push verified: main = {head}')


if __name__ == '__main__':
    try:
        main()
    except RuntimeError as error:
        raise SystemExit(str(error))

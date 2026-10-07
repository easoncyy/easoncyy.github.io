"""GitHub API access using the active gh credential, without logging tokens."""
import json
import subprocess
import time
import urllib.error
import urllib.request
from functools import lru_cache


@lru_cache(maxsize=1)
def token():
    result = subprocess.run(['gh', 'auth', 'token', '--hostname', 'github.com'],
                            capture_output=True, encoding='utf-8', timeout=15)
    if result.returncode or not result.stdout.strip():
        raise RuntimeError('No active GitHub credential. Run: gh auth login --hostname github.com --web')
    return result.stdout.strip()


def api(method, endpoint, payload=None, allow_missing=False):
    url = 'https://api.github.com/' + endpoint.lstrip('/')
    data = json.dumps(payload, ensure_ascii=False).encode('utf-8') if payload is not None else None
    request = urllib.request.Request(url, data=data, method=method, headers={
        'Authorization': 'Bearer ' + token(), 'Accept': 'application/vnd.github+json',
        'Content-Type': 'application/json', 'User-Agent': 'homepage-deploy',
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                content = response.read()
                return json.loads(content) if content.strip() else None
        except urllib.error.HTTPError as error:
            if error.code == 404 and allow_missing:
                return None
            if error.code == 401:
                raise RuntimeError('GitHub rejected the active credential (HTTP 401). Run gh auth login again.') from None
            if error.code not in (429, 500, 502, 503, 504):
                raise RuntimeError(f'GitHub API {method} {endpoint}: HTTP {error.code}. Check repository permissions and API limits.') from None
            detail = f'HTTP {error.code}'
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            detail = str(error)
        if attempt < 2:
            time.sleep(attempt + 1)
    raise RuntimeError(f'GitHub API connection failed after retries: {detail}. Check network, DNS or proxy settings; this does not establish a login failure.')

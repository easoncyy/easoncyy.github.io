"""Check the active account's actual access to the publishing repository."""
from github_api import api

try:
    repository = api('GET', 'repos/easoncyy/easoncyy.github.io')
    if not repository.get('permissions', {}).get('push'):
        raise RuntimeError('The active GitHub account lacks write access to easoncyy/easoncyy.github.io.')
    user = api('GET', 'user')
    print(f"GitHub API connected: {user['login']} -> {repository['full_name']} (write access)")
except RuntimeError as error:
    raise SystemExit(str(error))

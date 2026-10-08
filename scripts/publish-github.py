"""Publish this website through GitHub's Git API using the signed-in gh CLI.

Run scripts/build.ps1 first. Deploys gh-pages only; sync.ps1 pushes source to main.
Requires ADMIN/write access to the target repository.
No credentials are embedded in the source or passed on the command line.
"""
import base64
import json
import hashlib
from github_api import api
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = "easoncyy/easoncyy.github.io"
API_ROOT = f"repos/{REPOSITORY}"
KNOWN_BLOBS = set()


def publish_tree(branch, files, message, preserve_tree):
    ref = api("GET", f"{API_ROOT}/git/ref/heads/{branch}", allow_missing=True)
    parent = ref["object"]["sha"] if ref else None
    base_tree = None
    if parent:
        previous_tree = api("GET", f"{API_ROOT}/git/commits/{parent}")["tree"]["sha"]
        existing = api("GET", f"{API_ROOT}/git/trees/{previous_tree}?recursive=1")
        KNOWN_BLOBS.update(item["sha"] for item in existing["tree"] if item["type"] == "blob")
        if preserve_tree:
            base_tree = previous_tree
    entries = []
    for path, name in sorted(files, key=lambda item: item[1]):
        entry = {"path": name, "mode": "100644", "type": "blob"}
        data = path.read_bytes()
        try:
            content = data.decode("utf-8")
            if "\x00" in content:
                raise UnicodeDecodeError("utf-8", data, 0, 1, "binary data")
            entry["content"] = content
        except UnicodeDecodeError:
            sha = hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()
            if sha not in KNOWN_BLOBS:
                print(f"Uploading: {name} ({len(data) / 1024 / 1024:.1f} MB)", flush=True)
                blob = api("POST", f"{API_ROOT}/git/blobs", {
                    "content": base64.b64encode(data).decode("ascii"), "encoding": "base64"
                })
                sha = blob["sha"]
                KNOWN_BLOBS.add(sha)
            entry["sha"] = sha
        entries.append(entry)
    payload = {"tree": entries}
    if base_tree:
        payload["base_tree"] = base_tree
    tree = api("POST", f"{API_ROOT}/git/trees", payload)
    state_file = ROOT / "tmp" / f"publish-{branch}.json"
    if parent and tree['sha'] == previous_tree:
        state_file.unlink(missing_ok=True)
        print(f"{branch} already contains the current rendered files: {parent}", flush=True)
        return
    pending = json.loads(state_file.read_text(encoding='utf-8')) if state_file.exists() else {}
    if pending.get('parent') == parent and pending.get('tree') == tree['sha']:
        commit = {'sha': pending['commit']}
        print(f"Resuming pending deployment: {commit['sha']}", flush=True)
    else:
        commit = api("POST", f"{API_ROOT}/git/commits", {
            "message": message, "tree": tree["sha"], "parents": [parent] if parent else []
        })
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps({'parent': parent, 'tree': tree['sha'], 'commit': commit['sha']}), encoding='utf-8')
    try:
        if ref:
            api("PATCH", f"{API_ROOT}/git/refs/heads/{branch}", {"sha": commit["sha"], "force": False})
        else:
            api("POST", f"{API_ROOT}/git/refs", {"ref": f"refs/heads/{branch}", "sha": commit["sha"]})
    except RuntimeError as update_error:
        # A dropped response does not establish that GitHub rejected the update.
        actual = api('GET', f'{API_ROOT}/git/ref/heads/{branch}', allow_missing=True)
        if not actual or actual['object']['sha'] != commit['sha']:
            raise RuntimeError(f'{update_error}\nPending deployment saved. Retry: python scripts/publish-github.py') from update_error
        print('GitHub applied the branch update despite a disconnected response.', flush=True)
    actual = api('GET', f'{API_ROOT}/git/ref/heads/{branch}')
    if actual['object']['sha'] != commit['sha']:
        raise RuntimeError('Deployment branch changed concurrently. Inspect the remote branch before retrying.')
    state_file.unlink(missing_ok=True)
    print(f"Published {len(entries)} files to {branch}: {commit['sha']}", flush=True)


def source_files():
    roots = ["_quarto.yml", ".gitignore", ".nojekyll", "README.md", "index.qmd",
             "blog.qmd", "about.qmd", "projects.qmd", "links.qmd", "log.qmd", "logs", "library.qmd", "library", "styles.css", "assets", "posts", "scripts"]
    for name in roots:
        path = ROOT / name
        paths = path.rglob("*") if path.is_dir() else [path]
        for file in paths:
            if file.is_file() and "__pycache__" not in file.parts:
                yield file, file.relative_to(ROOT).as_posix()
    for name in ["documents/_quarto.yml", "documents/math-notes.qmd", "documents/homework-archive.json"]:
        path = ROOT / name
        yield path, name


def main():
    site = ROOT / "_site"
    if not (site / "index.html").is_file() or not (site / "assets/pdf/math-notes.pdf").is_file():
        raise RuntimeError("Build the website and PDF with scripts/build.ps1 before publishing.")
    # Source is committed and pushed by sync.ps1; only deploy the rendered site here.
    publish_tree("gh-pages", [(p, p.relative_to(site).as_posix()) for p in site.rglob("*") if p.is_file()],
                 "Publish rendered personal website", False)
    pages = api("GET", f"{API_ROOT}/pages", allow_missing=True)
    source = {"branch": "gh-pages", "path": "/"}
    if not pages:
        api("POST", f"{API_ROOT}/pages", {"build_type": "legacy", "source": source})
        api("PUT", f"{API_ROOT}/pages", {"build_type": "legacy", "source": source})
        api("POST", f"{API_ROOT}/pages/builds")
    elif pages.get("source") != source or pages.get("build_type") != "legacy":
        api("PUT", f"{API_ROOT}/pages", {"build_type": "legacy", "source": source})
        api("POST", f"{API_ROOT}/pages/builds")
    # An update to the configured gh-pages branch already triggers deployment.
    print("Pages configured: https://easoncyy.github.io/", flush=True)


if __name__ == "__main__":
    main()

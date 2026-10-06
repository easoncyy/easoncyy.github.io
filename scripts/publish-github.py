"""Publish this website through GitHub's Git API using the signed-in gh CLI.

Run scripts/build.ps1 first. Requires ADMIN/write access to the target repository.
No credentials are embedded in the source or passed on the command line.
"""
import base64
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPOSITORY = "easoncyy/easoncyy.github.io"
API_ROOT = f"repos/{REPOSITORY}"


def api(method, endpoint, payload=None, allow_missing=False):
    command = ["gh", "api", endpoint, "--method", method]
    if payload is not None:
        command += ["--input", "-"]
    result = subprocess.run(
        command,
        input=json.dumps(payload, ensure_ascii=False) if payload is not None else None,
        capture_output=True, encoding="utf-8", cwd=ROOT,
    )
    if result.returncode:
        if allow_missing and "HTTP 404" in result.stderr:
            return None
        raise RuntimeError(f"GitHub API {method} {endpoint}: {result.stderr.strip()}")
    return json.loads(result.stdout) if result.stdout.strip() else None


def publish_tree(branch, files, message, preserve_tree):
    ref = api("GET", f"{API_ROOT}/git/ref/heads/{branch}", allow_missing=True)
    parent = ref["object"]["sha"] if ref else None
    base_tree = None
    if parent and preserve_tree:
        base_tree = api("GET", f"{API_ROOT}/git/commits/{parent}")["tree"]["sha"]
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
            blob = api("POST", f"{API_ROOT}/git/blobs", {
                "content": base64.b64encode(data).decode("ascii"), "encoding": "base64"
            })
            entry["sha"] = blob["sha"]
        entries.append(entry)
    payload = {"tree": entries}
    if base_tree:
        payload["base_tree"] = base_tree
    tree = api("POST", f"{API_ROOT}/git/trees", payload)
    commit = api("POST", f"{API_ROOT}/git/commits", {
        "message": message, "tree": tree["sha"], "parents": [parent] if parent else []
    })
    if ref:
        api("PATCH", f"{API_ROOT}/git/refs/heads/{branch}", {"sha": commit["sha"], "force": False})
    else:
        api("POST", f"{API_ROOT}/git/refs", {"ref": f"refs/heads/{branch}", "sha": commit["sha"]})
    print(f"Published {len(entries)} files to {branch}: {commit['sha']}", flush=True)


def source_files():
    roots = ["_quarto.yml", ".gitignore", ".nojekyll", "README.md", "index.qmd",
             "blog.qmd", "about.qmd", "styles.css", "assets", "posts", "scripts"]
    for name in roots:
        path = ROOT / name
        paths = path.rglob("*") if path.is_dir() else [path]
        for file in paths:
            if file.is_file() and "__pycache__" not in file.parts:
                yield file, file.relative_to(ROOT).as_posix()
    for name in ["documents/_quarto.yml", "documents/math-notes.qmd"]:
        path = ROOT / name
        yield path, name


def main():
    site = ROOT / "_site"
    if not (site / "index.html").is_file() or not (site / "assets/pdf/math-notes.pdf").is_file():
        raise RuntimeError("Build the website and PDF with scripts/build.ps1 before publishing.")
    publish_tree("main", list(source_files()), "Publish personal Quarto website source", True)
    publish_tree("gh-pages", [(p, p.relative_to(site).as_posix()) for p in site.rglob("*") if p.is_file()],
                 "Publish rendered personal website", False)
    pages = api("GET", f"{API_ROOT}/pages", allow_missing=True)
    source = {"branch": "gh-pages", "path": "/"}
    if not pages:
        api("POST", f"{API_ROOT}/pages", {"build_type": "legacy", "source": source})
    # A user site's first implicit build can use main despite the creation payload.
    # Apply the source again after creation and explicitly request its build.
    api("PUT", f"{API_ROOT}/pages", {"build_type": "legacy", "source": source})
    api("POST", f"{API_ROOT}/pages/builds")
    print("Pages configured: https://easoncyy.github.io/", flush=True)


if __name__ == "__main__":
    main()

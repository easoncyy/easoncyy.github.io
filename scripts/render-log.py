"""Assemble full Markdown entries into a single Quarto page before rendering."""
import html
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    entries = []
    sources = list((ROOT / "logs").glob("*.qmd")) + list((ROOT / "logs").glob("*/index.qmd"))
    for source in sorted(sources):
        text = source.read_text(encoding="utf-8-sig")
        _, header, body = text.split("---", 2)
        metadata = {}
        for line in header.strip().splitlines():
            key, value = line.split(":", 1)
            value = value.strip()
            try:
                metadata[key] = json.loads(value)
            except json.JSONDecodeError:
                metadata[key] = value.strip("'\"")
        if not metadata.get("date"):
            timestamp = metadata.get("timestamp") or datetime.now(timezone(timedelta(hours=8))).replace(microsecond=0).isoformat()
            metadata["date"] = timestamp
            # Persist the first publication time so later builds do not change it.
            header = header.rstrip() + "\ndate: " + json.dumps(timestamp) + "\n"
            source.write_text("---" + header + "---" + body, encoding="utf-8")
        slug = source.stem if source.parent == ROOT / "logs" else source.parent.name
        entries.append((metadata, body.strip(), slug))
    entries.sort(key=lambda entry: entry[0]["date"], reverse=True)
    output = ["::: {.log-stream}"]
    for metadata, body, slug in entries:
        timestamp = metadata.get("timestamp", metadata["date"])
        label = datetime.fromisoformat(timestamp).strftime("%Y-%m-%d %H:%M:%S %z")
        escape = lambda value: html.escape(str(value), quote=True)
        output.extend([
            f'::: {{#{slug} .log-entry}}',
            '```{=html}',
            f'<div class="log-stamp"><time datetime="{escape(timestamp)}">{escape(label)}</time></div>',
            '```',
            '::: {.log-payload}',
            '```{=html}',
            f'<p class="log-entry-title">{escape(metadata.get("title", ""))}</p>',
            '```',
            body,
            ':::',
            ':::',
        ])
    output.append(':::')
    (ROOT / "assets/log-entries.md").write_text("\n\n".join(output) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

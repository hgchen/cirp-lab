#!/usr/bin/env python3
"""Import local news markdown files into Hugo content/news pages.

Source files are expected in ./news/*.md with Jekyll-like front matter.
Output pages are written to ./content/news/<slug>/index.md.
"""

from __future__ import annotations

from pathlib import Path
import re

SRC_DIR = Path("news")
OUT_DIR = Path("content/news")


def single_quote_yaml(text: str) -> str:
    return "'" + text.replace("'", "''") + "'"


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    # Expect initial --- ... --- block. Fallback: empty metadata.
    if not text.startswith("---"):
        return {}, text

    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        # Handle malformed delimiter style defensively.
        m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
        if not m:
            return {}, text
        fm_raw, body = m.group(1), m.group(2)
    else:
        fm_raw = parts[0][4:]  # strip opening "---\n"
        body = parts[1]

    meta: dict[str, str] = {}
    for line in fm_raw.splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip().lower()] = v.strip()

    return meta, body


def normalize_body(body: str) -> str:
    b = body.strip()
    # Some copied files have trailing '---' artifacts.
    b = re.sub(r"---\s*$", "", b).rstrip()
    return b + "\n"


def convert_one(src: Path) -> None:
    raw = src.read_text(encoding="utf-8")
    meta, body = parse_front_matter(raw)

    title = meta.get("title", src.stem.replace("_", " ").strip()).strip()
    date_raw = meta.get("date", "").strip()
    date = date_raw[:10] if len(date_raw) >= 10 else "2024-01-01"

    out_dir = OUT_DIR / src.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    out = [
        "---",
        f"title: {single_quote_yaml(title)}",
        f"date: {single_quote_yaml(date)}",
        "draft: false",
        "---",
        "",
        normalize_body(body),
    ]

    (out_dir / "index.md").write_text("\n".join(out), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Section page for /news
    (OUT_DIR / "_index.md").write_text(
        "---\n"
        "title: News\n"
        "view: compact\n"
        "---\n",
        encoding="utf-8",
    )

    files = sorted(SRC_DIR.glob("*.md"))
    for f in files:
        convert_one(f)
        print(f"imported: {f.name}")


if __name__ == "__main__":
    main()

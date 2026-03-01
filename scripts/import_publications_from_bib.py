#!/usr/bin/env python3
"""Import BibTeX entries into HugoBlox publication pages.

Usage:
  python3 scripts/import_publications_from_bib.py \
    --bib content/publication/pub.bib \
    --out content/publication
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

MONTH_MAP = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}

PUB_TYPE_MAP = {
    "article": "article-journal",
    "inproceedings": "paper-conference",
    "conference": "paper-conference",
    "proceedings": "paper-conference",
    "incollection": "chapter",
    "inbook": "chapter",
    "book": "book",
    "phdthesis": "thesis",
    "mastersthesis": "thesis",
    "misc": "manuscript",
}


@dataclass
class BibEntry:
    entry_type: str
    key: str
    fields: Dict[str, str]
    raw: str


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def strip_braces(text: str) -> str:
    return text.replace("{", "").replace("}", "")


def yaml_quote(text: str) -> str:
    return "'" + text.replace("'", "''") + "'"


def key_to_slug(key: str) -> str:
    slug = re.sub(r"([a-z])([A-Z])", r"\1-\2", key)
    slug = re.sub(r"([a-zA-Z])([0-9])", r"\1-\2", slug)
    slug = re.sub(r"([0-9])([a-zA-Z])", r"\1-\2", slug)
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", slug)
    return slug.strip("-").lower()


def read_braced_value(text: str, start: int) -> tuple[str, int]:
    # start points to opening '{'
    i = start + 1
    depth = 1
    buf: List[str] = []
    while i < len(text) and depth > 0:
        ch = text[i]
        if ch == "{":
            depth += 1
            buf.append(ch)
        elif ch == "}":
            depth -= 1
            if depth > 0:
                buf.append(ch)
        else:
            buf.append(ch)
        i += 1
    return "".join(buf), i


def read_quoted_value(text: str, start: int) -> tuple[str, int]:
    # start points to opening '"'
    i = start + 1
    buf: List[str] = []
    escaped = False
    while i < len(text):
        ch = text[i]
        if escaped:
            buf.append(ch)
            escaped = False
        elif ch == "\\":
            escaped = True
            buf.append(ch)
        elif ch == '"':
            i += 1
            break
        else:
            buf.append(ch)
        i += 1
    return "".join(buf), i


def parse_fields(body: str) -> Dict[str, str]:
    fields: Dict[str, str] = {}
    i = 0
    n = len(body)
    while i < n:
        while i < n and body[i] in " \t\r\n,":
            i += 1
        if i >= n:
            break

        name_start = i
        while i < n and (body[i].isalnum() or body[i] in "_-"):
            i += 1
        field_name = body[name_start:i].strip().lower()
        if not field_name:
            i += 1
            continue

        while i < n and body[i].isspace():
            i += 1
        if i >= n or body[i] != "=":
            while i < n and body[i] != ",":
                i += 1
            continue

        i += 1
        while i < n and body[i].isspace():
            i += 1
        if i >= n:
            break

        if body[i] == "{":
            raw_val, i = read_braced_value(body, i)
        elif body[i] == '"':
            raw_val, i = read_quoted_value(body, i)
        else:
            start = i
            while i < n and body[i] != ",":
                i += 1
            raw_val = body[start:i]

        # Handle BibTeX concatenation syntax, e.g. month=jul # "~13"
        if "#" in raw_val:
            pieces = [normalize_space(strip_braces(p.strip().strip('"'))) for p in raw_val.split("#")]
            value = "".join(pieces)
        else:
            value = normalize_space(strip_braces(raw_val.strip().strip('"')))

        if value:
            fields[field_name] = value

        while i < n and body[i] != ",":
            i += 1
        if i < n and body[i] == ",":
            i += 1

    return fields


def parse_bibtex_entries(text: str) -> List[BibEntry]:
    entries: List[BibEntry] = []
    i = 0
    while True:
        at = text.find("@", i)
        if at == -1:
            break

        j = at + 1
        while j < len(text) and text[j].isalpha():
            j += 1
        entry_type = text[at + 1 : j].lower()
        while j < len(text) and text[j].isspace():
            j += 1
        if j >= len(text) or text[j] != "{":
            i = at + 1
            continue

        j += 1
        key_start = j
        while j < len(text) and text[j] != ",":
            j += 1
        if j >= len(text):
            break
        key = normalize_space(text[key_start:j])

        j += 1
        body_start = j
        depth = 1
        while j < len(text) and depth > 0:
            ch = text[j]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
            j += 1

        if depth != 0:
            break

        body = text[body_start : j - 1]
        raw = text[at:j].strip()
        fields = parse_fields(body)

        if key and fields.get("title"):
            entries.append(BibEntry(entry_type=entry_type, key=key, fields=fields, raw=raw))

        i = j

    return entries


def parse_authors(authors_raw: str) -> List[str]:
    parts = [p.strip() for p in re.split(r"\s+and\s+", authors_raw) if p.strip()]
    names: List[str] = []
    for part in parts:
        clean = normalize_space(strip_braces(part))
        if "," in clean:
            seg = [s.strip() for s in clean.split(",") if s.strip()]
            if len(seg) >= 2:
                names.append(normalize_space(f"{seg[1]} {seg[0]}"))
            else:
                names.append(clean)
        else:
            names.append(clean)
    return names


def parse_date(fields: Dict[str, str]) -> str:
    year_match = re.search(r"\d{4}", fields.get("year", ""))
    year = int(year_match.group(0)) if year_match else 1900

    month_raw = fields.get("month", "")
    month = 1
    if month_raw:
        token = re.sub(r"[^a-zA-Z0-9]", " ", month_raw.lower()).split()
        if token:
            first = token[0]
            if first.isdigit():
                month = max(1, min(12, int(first)))
            else:
                month = MONTH_MAP.get(first[:3], 1)

    return f"{year:04d}-{month:02d}-01"


def arxiv_to_url(arxiv_value: str) -> str:
    token = normalize_space(arxiv_value)
    if token.startswith("http://") or token.startswith("https://"):
        return token
    return f"https://arxiv.org/abs/{token}"


def build_front_matter(entry: BibEntry) -> str:
    fields = entry.fields
    title = fields.get("title", "Untitled")
    authors = parse_authors(fields.get("author", ""))
    date = parse_date(fields)
    pub_type = PUB_TYPE_MAP.get(entry.entry_type, "manuscript")
    venue = (
        fields.get("booktitle")
        or fields.get("journal")
        or fields.get("publisher")
        or fields.get("school")
        or "Preprint"
    )

    lines = [
        "---",
        f"title: {yaml_quote(title)}",
        "authors:",
    ]
    if authors:
        lines.extend([f"- {author}" for author in authors])
    else:
        lines.append("- Unknown")

    lines.extend(
        [
            f"date: {yaml_quote(date)}",
            "publication_types:",
            f"- {pub_type}",
            f"publication: {yaml_quote(f'*{venue}*')}",
        ]
    )

    if "doi" in fields:
        lines.append(f"doi: {yaml_quote(fields['doi'])}")
    if "pdf" in fields:
        lines.append(f"url_pdf: {yaml_quote(fields['pdf'])}")
    if "website" in fields:
        lines.append(f"url_source: {yaml_quote(fields['website'])}")
    elif "url" in fields:
        lines.append(f"url_source: {yaml_quote(fields['url'])}")
    if "code" in fields:
        lines.append(f"url_code: {yaml_quote(fields['code'])}")
    if "arxiv" in fields:
        lines.append(f"url_preprint: {yaml_quote(arxiv_to_url(fields['arxiv']))}")

    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def write_publication(entry: BibEntry, out_dir: Path, overwrite: bool) -> str:
    slug = key_to_slug(entry.key)
    target_dir = out_dir / slug
    if target_dir.exists() and not overwrite:
        return "skipped"

    target_dir.mkdir(parents=True, exist_ok=True)
    (target_dir / "index.md").write_text(build_front_matter(entry), encoding="utf-8")
    (target_dir / "cite.bib").write_text(entry.raw + "\n", encoding="utf-8")
    return "written"


def run(bib_path: Path, out_dir: Path, overwrite: bool, limit: int | None) -> None:
    text = bib_path.read_text(encoding="utf-8")
    entries = parse_bibtex_entries(text)
    if limit is not None:
        entries = entries[:limit]

    written = 0
    skipped = 0
    for entry in entries:
        result = write_publication(entry, out_dir, overwrite=overwrite)
        if result == "written":
            written += 1
            print(f"[written] {key_to_slug(entry.key)}")
        else:
            skipped += 1
            print(f"[skipped] {key_to_slug(entry.key)}")

    print(f"Done. Parsed={len(entries)} written={written} skipped={skipped}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import BibTeX entries into HugoBlox publication pages.")
    parser.add_argument("--bib", default="content/publication/pub.bib", help="Path to BibTeX file")
    parser.add_argument("--out", default="content/publication", help="Publication content directory")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing publication folders")
    parser.add_argument("--limit", type=int, default=None, help="Only process first N entries")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    bib_path = Path(args.bib)
    out_dir = Path(args.out)

    if not bib_path.exists():
        raise SystemExit(f"BibTeX file not found: {bib_path}")
    if not out_dir.exists():
        raise SystemExit(f"Output directory not found: {out_dir}")

    run(bib_path=bib_path, out_dir=out_dir, overwrite=args.overwrite, limit=args.limit)


if __name__ == "__main__":
    main()

#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"
mkdir -p "$DIST_DIR/content"

cp "$ROOT_DIR/index.html" "$DIST_DIR/index.html"
cp "$ROOT_DIR/members.md" "$DIST_DIR/members.md"
cp "$ROOT_DIR/news.md" "$DIST_DIR/news.md"
cp "$ROOT_DIR/publications.bib" "$DIST_DIR/publications.bib"
rsync -a --exclude '.DS_Store' "$ROOT_DIR/images/" "$DIST_DIR/images/"
python3 "$ROOT_DIR/scripts/optimize_images.py" "$DIST_DIR"
touch "$DIST_DIR/.nojekyll"

ROOT_DIR="$ROOT_DIR" DIST_DIR="$DIST_DIR" python3 - <<'PY'
import json
import os
from pathlib import Path

root = Path(os.environ["ROOT_DIR"])
dist = Path(os.environ["DIST_DIR"])
gallery_dir = root / "images" / "gallery"
allowed = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
images = sorted(
    f"images/gallery/{path.name}"
    for path in gallery_dir.iterdir()
    if path.is_file() and path.suffix.lower() in allowed
)
(dist / "gallery.json").write_text(json.dumps({"images": images}, indent=2) + "\n", encoding="utf-8")
PY

echo "Built static site into $DIST_DIR"

#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"

python3 "$ROOT_DIR/scripts/validate_content.py"

rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"
mkdir -p "$DIST_DIR/content"

cp "$ROOT_DIR/index.html" "$DIST_DIR/index.html"
cp "$ROOT_DIR/styles.css" "$DIST_DIR/styles.css"
cp "$ROOT_DIR/members.md" "$DIST_DIR/members.md"
cp "$ROOT_DIR/projects.md" "$DIST_DIR/projects.md"
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
projects_dir = root / "images" / "projects"
allowed = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
priority = {
    "images/gallery/palm_capture.jpg": 0,
    "images/gallery/drone_pic.png": 1,
}
images = sorted(
    f"images/gallery/{path.name}"
    for path in gallery_dir.iterdir()
    if path.is_file() and path.suffix.lower() in allowed
)
images.sort(key=lambda image: (priority.get(image, len(priority)), image))
(dist / "gallery.json").write_text(json.dumps({"images": images}, indent=2) + "\n", encoding="utf-8")

project_manifest = {}
if projects_dir.exists():
    for folder in sorted(path for path in projects_dir.iterdir() if path.is_dir()):
        media = sorted(
            (
                f"images/projects/{folder.name}/{path.name}"
                for path in folder.iterdir()
                if path.is_file() and path.suffix.lower() in allowed
            ),
            key=lambda image: (Path(image).suffix.lower() == ".gif", image.lower())
        )
        project_manifest[folder.name] = media

(dist / "projects-manifest.json").write_text(
    json.dumps({"projects": project_manifest}, indent=2) + "\n",
    encoding="utf-8",
)
PY

echo "Built static site into $DIST_DIR"

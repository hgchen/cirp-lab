#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 - "$ROOT_DIR" <<'PY'
import fcntl
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
from render_site import records

dist = root / "dist"
# CI, Netlify and macOS all support flock on a directory. Concurrent preview
# and manual builds serialize without adding a lock file to the source tree.
lock = os.open(root, os.O_RDONLY)
fcntl.flock(lock, fcntl.LOCK_EX)
subprocess.run([sys.executable, root / "scripts/validate_content.py"], check=True)
with tempfile.TemporaryDirectory(prefix="cirp-build-") as temporary:
    stage = Path(temporary)
    for name in ("styles.css", "members.md", "projects.md", "news.md", "publications.bib"):
        shutil.copy2(root / name, stage / name)
    shutil.copytree(root / "fonts", stage / "fonts")
    shutil.copytree(root / "images", stage / "images", ignore=shutil.ignore_patterns(".DS_Store", "projects"))
    folders = sorted({Path("images/projects") / p["folder"] for group in records("projects.md").values() for p in group})
    for folder in folders:
        shutil.copytree(root / folder, stage / folder, ignore=shutil.ignore_patterns(".DS_Store"))
    (stage / ".nojekyll").touch()
    # Preserve the published manifest URLs for consumers of the previous site.
    suffixes = {".jpg", ".jpeg", ".png", ".gif", ".webp"}

    def media(directory):
        return sorted(p.relative_to(root).as_posix() for p in directory.iterdir()
                      if p.is_file() and p.suffix.lower() in suffixes)

    gallery = media(root / "images/gallery")
    priority = {"images/gallery/palm_capture.jpg": 0, "images/gallery/drone_pic.png": 1}
    gallery.sort(key=lambda path: (priority.get(path, 2), path))
    projects = {folder.name: sorted(media(root / folder), key=lambda path: (path.endswith(".gif"), path.lower()))
                for folder in folders}
    for name, data in [("gallery.json", {"images": gallery}), ("projects-manifest.json", {"projects": projects})]:
        (stage / name).write_text(json.dumps(data, indent=2) + "\n")
    subprocess.run([sys.executable, root / "scripts/render_site.py", stage], check=True)
    shutil.copy2(root / "scripts/publication-search.js", stage / "publications/search.js")
    dist.mkdir(exist_ok=True)
    subprocess.run(["rsync", "-ac", "--delete-after", str(stage) + "/", str(dist) + "/"], check=True)
print(f"Built static site into {dist}")
PY

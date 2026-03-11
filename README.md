# CIRP Lab Static Site

This repository publishes a pure static lab website without Hugo or Wowchemy.

## Primary files

- `index.html`: single-page frontend with inline JavaScript and CSS
- `members.md`: faculty, student, and alumni data
- `news.md`: lab updates
- `publications.bib`: publication data
- `images/gallery/`: slideshow images
- `scripts/build_static_site.sh`: static build script for GitHub Pages and Netlify
- `scripts/optimize_images.py`: build-time image resizing/compression for oversized assets

## Local preview

```bash
bash scripts/build_static_site.sh
cd dist
python3 -m http.server 8000
```

Open `http://localhost:8000`.

## Live preview

For a single-command local dev server with auto rebuild:

```bash
bash scripts/dev_static_site.sh
```

Then open `http://127.0.0.1:8000`.

When you save `index.html`, `members.md`, `news.md`, `publications.bib`, or files under `images/`, the script rebuilds automatically. Refresh the browser to see the latest result.

## Deployment

- GitHub Pages publishes `dist/` via `.github/workflows/publish.yaml`
- Netlify runs `bash scripts/build_static_site.sh` and publishes `dist/`

## Updating group photos

Add new images to `images/gallery/` and rebuild. The build script regenerates `gallery.json` automatically.

## Image optimization

The build copies `images/` into `dist/` and then runs `scripts/optimize_images.py` to resize oversized gallery, member, logo, and hero images before deployment. The optimizer uses `ffmpeg` when available and falls back to `sips` on macOS.

# CIRP Lab Static Site

This repository publishes a pure static lab website without Hugo or Wowchemy.
News and member updates are edited directly in Markdown files, then validated during the build.

## Primary files

- `index.html`: single-page frontend with inline JavaScript and CSS
- `members.md`: faculty, student, and alumni data
- `news.md`: lab updates
- `publications.bib`: publication data
- `images/gallery/`: slideshow images
- `scripts/build_static_site.sh`: static build script for GitHub Pages and Netlify
- `scripts/validate_content.py`: validates `news.md` and `members.md` before each build
- `scripts/optimize_images.py`: build-time image resizing/compression for oversized assets

## Local preview

```bash
bash scripts/build_static_site.sh
cd dist
python3 -m http.server 8000
```

Open `http://localhost:8000`.

## Editing content

This site does not use Hugo-style post files anymore. To add content safely:

- Add news items directly to `news.md`
- Add or update members directly in `members.md`
- Run `bash scripts/build_static_site.sh` to validate and rebuild the site

If the Markdown structure is invalid, the build stops with a clear error message.

### News template

Use this format for each item:

```md
## 2026-03-18 | News Title
One or more paragraphs describing the update.

- Optional bullet
- Optional bullet

---
```

### Member template

Use this format for each member:

```md
## Category

### Member Name
role: Role
affiliation: Organization
image: images/members/example.jpg
email: name@example.edu
website: https://example.com
bio: Short bio goes here.
---
```

Notes:

- The first non-empty line of `news.md` must be `# News`
- The first non-empty line of `members.md` must be `# Members`
- News headings must use `## YYYY-MM-DD | Title`
- Member entries must live under a `## Category`
- If a member includes an `image:` path, that file must exist

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

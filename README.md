# CIRP Lab Website

Static lab website built from a small set of Markdown content files plus a single frontend.

## Structure

- `index.html`: main site markup and client-side logic
- `styles.css`: site styling
- `members.md`: lab members
- `projects.md`: lab projects
- `news.md`: news items
- `publications.bib`: publications
- `images/`: all site images
- `scripts/build_static_site.sh`: validates content and builds `dist/`
- `scripts/dev_static_site.sh`: local dev server with auto rebuild

## Local Preview

Auto rebuild + local server:

```bash
bash scripts/dev_static_site.sh
```

Open [http://127.0.0.1:7000](http://127.0.0.1:7000).

One-time build:

```bash
bash scripts/build_static_site.sh
cd dist
python3 -m http.server 7000
```

## Editing Content

### News

Edit `news.md`.

Format:

```md
## 2026-03-18 | News Title
News text here.

---
```

### Members

Edit `members.md`.

Format:

```md
## Category

### Member Name
role: Role
affiliation: Organization
image: images/members/example.jpg
email: name@example.edu
website: https://example.com
bio: Short bio.
---
```

If `image:` is present, the file must exist.

### Projects

Edit `projects.md`.

Format:

```md
## CV Health

### Project Title
folder: ProjectFolder
lead: Lead Name
pi: Huaijin Chen
members: Member One | Member Two
short: One-sentence card summary.
description: Longer project description.
---
```

Project media goes in:

```text
images/projects/ProjectFolder/
```

Supported project images are picked up automatically during build and written to `dist/projects-manifest.json`.

The build copies images as static assets without converting them, so local preview and GitHub Pages deploys stay fast and predictable. Keep the image that looks right for the site in `images/`; larger files are okay when the visual quality is worth it.

## Validation

Every build validates:

- `news.md`
- `members.md`
- `projects.md`
- project image folders referenced by `projects.md`

If the format is invalid, the build stops with an error.

## Deployment

- GitHub Pages publishes `dist/` through `.github/workflows/publish.yaml`
- Netlify can publish `dist/` by running `bash scripts/build_static_site.sh`

## Notes

- Default local port is `7000`
- Saving `index.html`, `styles.css`, Markdown content, or files under `images/` triggers rebuild in dev mode

# CIRP Lab website

The static site publishes at [hgchen.com/cirp-lab](https://hgchen.com/cirp-lab/). Its research, people, publications, news and contact pages work without JavaScript. Each project has a shareable URL under `research/`. Old homepage section links continue to resolve.

## Preview

Run `bash scripts/dev_static_site.sh --port 7017` and open [localhost:7017](http://127.0.0.1:7017/). Saving a content or layout file rebuilds the preview. For a one-time build, run `bash scripts/build_static_site.sh`. The build uses Python 3 and rsync and writes to `dist/`.

## Update content

- Edit `projects.md`. Each project has a title, image folder, short description, longer overview and team fields. Optional fields include a stable URL slug, short display name, cover and caption, method, and a detail figure with its caption. Image filenames are relative to `images/projects/<folder>/`. Within each of the two research directions, the first project is featured on the homepage.
- Edit `members.md` for people, roles, profiles and alumni placements. Names link to stable anchors on the People page. Choose group photos and their order in `gallery.json`.
- Edit `news.md` for dated items. Use YYYY-MM when the source gives only the month, or YYYY-MM-DD for a specific day.
- Add public bibliographic records to `publications.bib`. Keep private manuscripts outside the repository. Only place figures and other assets intended for the site in `images/`.

## Layout and deployment

The shared shell is `index.html`. The page renderer is `scripts/render_site.py`, the contact page body is `contact.html`, and presentation is in `styles.css`. GitHub Actions builds and publishes `dist/` when `main` changes. Netlify uses the same build command.

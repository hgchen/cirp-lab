# CIRP Lab website

The static site publishes at [hgchen.com/cirp-lab](https://hgchen.com/cirp-lab/). Its research, people, publications, news and contact pages work without JavaScript. Each project has a shareable URL under `research/`. Old homepage section links continue to resolve.

## Preview

Run `bash scripts/dev_static_site.sh --port 7017` and open [localhost:7017](http://127.0.0.1:7017/). Saving a content or layout file rebuilds the preview. For a one-time build, run `bash scripts/build_static_site.sh`. The build uses Python 3 and rsync and writes to `dist/`.

## Update content

- Edit `projects.md`. Each project has a title, image folder, short description, longer overview and team fields. Optional fields include a stable URL slug, short display name, cover and caption, method, and a detail figure with its caption. Image filenames are relative to `images/projects/<folder>/`. Within each of the two research directions, the first project is featured on the homepage. Its optional `question`, `summary` and `preview` fields set the homepage heading, description and thumbnail. Featured research thumbnails live in `images/previews/`. ImagingBench uses the six overall scores from the Expert protocol. Its `preview_caption` also displays the chart and scores on the project page.
- Edit `members.md` for people, portraits, profiles and alumni placements. The homepage uses the current members’ portraits (or their optional smaller `thumbnail`) and falls back to initials. Names and portraits link to the same People profiles. Choose group photos and their order in `gallery.json`.
- Edit `news.md` for dated items. Use YYYY-MM when the source gives only the month, or YYYY-MM-DD for a specific day.
- Add public bibliographic records to `publications.bib`. Keep private manuscripts outside the repository. Only place figures and other assets intended for the site in `images/`.

For **Selected work**, use `selected_work` in `projects.md` to set a project’s numeric order on the second row. Cards use the project’s `preview` or cover figure and its `summary` or short description. The combined 3PT card in `scripts/render_site.py` plays the [CVPR project demonstration](https://www.intrinsic.ai/publications/3pt-cvpr2026) and links to both papers and their benchmark results.

The homepage uses the original lab sponsor artwork plus the header marks from [NVIDIA](https://www.nvidia.com/en-us/), the [Minderoo Foundation](https://www.minderoo.org/) and [USDA APHIS](https://www.aphis.usda.gov/). Member resource icons are in `images/profile-links.svg`. The site uses locally hosted Archivo and Spectral Semibold Italic. Both licenses are in `fonts/`.

## Layout and deployment

The shared shell is `index.html`. The page renderer is `scripts/render_site.py`, the contact page body is `contact.html`, and presentation is in `styles.css`. GitHub Actions builds and publishes `dist/` when `main` changes. Netlify uses the same build command.

# CIRP Lab website

The static site publishes at [hgchen.com/cirp-lab](https://hgchen.com/cirp-lab/). Its research, people, publications, news and contact pages work without JavaScript. Each project has a shareable URL under `research/`. Old homepage section links continue to resolve.

## Preview

Run `bash scripts/dev_static_site.sh --port 7017` and open [localhost:7017](http://127.0.0.1:7017/). Saving a content or layout file rebuilds the preview. For a one-time build, run `bash scripts/build_static_site.sh`. The build uses Python 3 and rsync and writes to `dist/`.

## Update content

- Edit `projects.md`. Each project has a title, image folder, short description, longer overview and team fields. Optional fields include a stable URL slug, short display name, cover and caption, method, and a detail figure with its caption. Image filenames are relative to `images/projects/<folder>/`. Within each of the two research directions, the first project is featured on the homepage. Its optional `question`, `summary` and `preview` fields set the homepage heading, description and thumbnail. The featured research thumbnails in `images/previews/` are excerpts of the full project figures.
- Edit `members.md` for people, portraits, profiles and alumni placements. The homepage uses the current members’ portraits (or their optional smaller `thumbnail`) and falls back to initials. Names and portraits link to the same People profiles. Choose group photos and their order in `gallery.json`.
- Edit `news.md` for dated items. Use YYYY-MM when the source gives only the month, or YYYY-MM-DD for a specific day.
- Add public bibliographic records to `publications.bib`. Keep private manuscripts outside the repository. Only place figures and other assets intended for the site in `images/`.

For **Selected work**, add the BibTeX key and image description to `WORK_CAPTIONS` in `scripts/render_site.py` and save the thumbnail as `images/previews/<key>.webp`. The 3PT image is the output panel of [Figure 1](https://openaccess.thecvf.com/content/CVPR2026/papers/Kalra_3D-Object_Perception_Transformer_3PT_CVPR_2026_paper.pdf). The dashcam image is the lens-flare panel of [Figure 3](https://openaccess.thecvf.com/content/ICCV2025W/CV4DC/papers/Motsoehli_Simulating_Refractive_Distortions_and_Weather-Induced_Artifacts_for_Resource-Constrained_Autonomous_Perception_ICCVW_2025_paper.pdf). The 3PTv2 illustration overlays the highest-scoring published pose per object from [BOP submission 44629](https://bop.felk.cvut.cz/sub_info/44629/) on [YCB-Video](https://rse-lab.cs.washington.edu/projects/posecnn/) test scene 48, frame 1, using the BOP model bounds and that frame’s camera intrinsics.

The homepage uses the original lab sponsor artwork plus the header marks from the [Minderoo Foundation](https://www.minderoo.org/) and [USDA APHIS](https://www.aphis.usda.gov/). Member resource icons are in `images/profile-links.svg`. The site uses locally hosted Archivo and Spectral Semibold Italic. Both licenses are in `fonts/`.

## Layout and deployment

The shared shell is `index.html`. The page renderer is `scripts/render_site.py`, the contact page body is `contact.html`, and presentation is in `styles.css`. GitHub Actions builds and publishes `dist/` when `main` changes. Netlify uses the same build command.

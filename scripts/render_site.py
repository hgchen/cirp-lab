"""Render the lab's Markdown and BibTeX records as self-contained HTML pages."""
import json
import re
import sys
import unicodedata
from datetime import date
from hashlib import sha256
from html import escape
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
DIST = Path(sys.argv[1]) if __name__ == "__main__" and len(sys.argv) > 1 else ROOT / "dist"
SHELL = Template((ROOT / "index.html").read_text())
STYLES_VERSION = sha256((ROOT / "styles.css").read_bytes()).hexdigest()[:12]
NAV = {"": "Home", "research": "Research", "publications": "Publications",
       "people": "People", "news": "News", "outreach": "Outreach", "service": "Service", "contact": "Contact"}
GROUP_LABELS = {"PhD": "PhD students", "Masters": "Master’s students",
                "Undergrads": "Undergraduates", "Visiting Students": "Visiting students"}
LAB = "Computational Imaging and Robotic Perception Lab"
LEGACY = """<script>
const routes = {members:"people",projects:"research",publications:"publications",news:"news",contact:"contact"};
function openLegacyRoute() {
  const route = location.hash.slice(1).toLowerCase();
  if (Object.hasOwn(routes, route)) location.replace("./" + routes[route] + "/");
}
openLegacyRoute();
window.addEventListener("hashchange", openLegacyRoute);
</script>"""


def slug(text):
    ascii_text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")


def link(url, label):
    return f'<a href="{escape(url)}">{escape(label)}</a>'


def inline(text):
    safe = escape(text)
    safe = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', r'<a href="\2">\1</a>', safe)
    safe = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', safe)
    return re.sub(r'\*([^*]+)\*', r'<em>\1</em>', safe)


def paragraphs(text):
    blocks = []
    for paragraph in text.strip().split("\n\n"):
        lines = paragraph.splitlines()
        if lines and all(line.startswith("- ") for line in lines):
            blocks.append("<ul>" + "".join(f"<li>{inline(line[2:])}</li>" for line in lines) + "</ul>")
        else:
            blocks.append(f"<p>{inline(' '.join(lines))}</p>")
    return "".join(blocks)


def records(filename):
    groups = {}
    for line in (ROOT / filename).read_text().splitlines():
        if line.startswith("## "):
            group = groups.setdefault(line[3:], [])
        elif line.startswith("### "):
            record = {"title": line[4:]}
            group.append(record)
        elif ": " in line and not line.startswith("#"):
            key, value = line.split(": ", 1)
            record[key] = value.strip()
    return groups


def news_records():
    items = []
    for block in re.split(r"^## ", (ROOT / "news.md").read_text(), flags=re.M)[1:]:
        header, body = block.split("\n", 1)
        stamp, title = header.split(" | ", 1)
        explicit_id = re.search(r" \{#([a-z0-9-]+)\}$", title)
        if explicit_id:
            anchor = explicit_id[1]
            title = title[:explicit_id.start()]
        else:
            anchor = news_anchor(stamp, title)
        items.append((stamp, title, body.rsplit("---", 1)[0].strip(), anchor))
    return sorted(items, key=lambda row: row[0], reverse=True)


def news_time(stamp):
    full = len(stamp) == 10
    parsed = date.fromisoformat(stamp if full else stamp + "-01")
    label = parsed.strftime("%b %d, %Y" if full else "%b %Y").replace(" 0", " ")
    quarter = (parsed.month - 1) // 3 + 1
    return f'<time datetime="{stamp}" data-quarter="{quarter}">{label}</time>'


def bibliography():
    entries = []
    for block in re.split(r"^@", (ROOT / "publications.bib").read_text(), flags=re.M)[1:]:
        # The maintained BibTeX uses braced values; a new field or entry closes each value.
        fields = dict(re.findall(r"^\s*(\w+)\s*=\s*\{(.*?)\}\s*,?\s*(?=^\s*\w+\s*=|^\}|\Z)", block, re.M | re.S))
        entry = {k: " ".join(v.replace("{", "").replace("}", "").split()) for k, v in fields.items()}
        entry["key"] = block.split("{", 1)[1].split(",", 1)[0].strip()
        entry["bibtex"] = "@" + block.strip()
        entries.append(entry)
    return sorted(entries, key=lambda row: row["year"], reverse=True)


def page(route, title, description, body):
    root = "../" * len(Path(route).parts) if route else "./"
    active = route.split("/")[0]
    nav = []
    for path, label in NAV.items():
        current = ""
        if active == path:
            current = ' aria-current="page"' if route.strip("/") == path else ' aria-current="location"'
        href = root + (path + "/" if path else "")
        nav.append(f'<a href="{href}"{current}>{escape(label)}</a>')
    folder = DIST / route
    folder.mkdir(parents=True, exist_ok=True)
    output = SHELL.substitute(root=root, title=escape(title + " · CIRP Lab" if route else "CIRP Lab · University of Hawaiʻi at Mānoa"),
                              description=escape(description), styles_version=STYLES_VERSION, legacy="" if route else LEGACY,
                              nav="".join(nav), content=body)
    (folder / "index.html").write_text(output)


def page_head(title, intro="", crumb="", action=""):
    return (f'<header class="page-head">{crumb}<h1>{escape(title)}</h1>' +
            (f'<p class="intro">{escape(intro)}</p>' if intro else "") + action + "</header>")


def heading(title, href="", action=""):
    return f'<div class="section-head"><h2>{escape(title)}</h2>{link(href, action) if href else ""}</div>'


def project_path(project):
    return "research/" + project.get("slug", slug(project["folder"])) + "/"


def project_website(project):
    if not project.get("website"):
        return ""
    name = escape(project.get("name", project["title"]))
    return (f'<a class="project-site" href="{escape(project["website"])}" '
            f'aria-label="Learn more about {name} on its project website">'
            'Learn more <span aria-hidden="true">↗</span></a>')


def project_media(project):
    directory = ROOT / "images/projects" / project["folder"]
    images = sorted(p.name for p in directory.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".gif", ".webp"})
    cover = project.get("cover", images[0])
    return directory.relative_to(ROOT).as_posix() + "/", cover, images


def card(project, root, theme=None):
    folder, cover, _ = project_media(project)
    title = project.get("name", project["title"])
    url = root + project_path(project)
    src = root + project.get("preview", folder + cover)
    category = f'<p class="category">{link(root + "research/#" + slug(theme), theme)}</p>' if theme else ""
    headline = project.get("question", title) if theme else title
    summary = project.get("summary", project["short"]) if theme else project["short"]
    return f'''<article class="card"><a class="plate" href="{url}" aria-label="View {escape(title)}">
    <img loading="lazy" src="{escape(src)}" alt=""></a><div class="card-copy">{category}
    <h3>{link(url, headline)}</h3><p>{escape(summary)}</p></div></article>'''


def figure(path, caption):
    return f'''<figure class="paper-figure"><a href="{escape(path)}" aria-label="Open full-size figure: {escape(caption)}">
    <img src="{escape(path)}" alt="{escape(caption)}" loading="lazy"></a><figcaption>{escape(caption)}</figcaption></figure>'''


def video_player(src, poster, label):
    return (f'<video controls playsinline preload="none" poster="{escape(poster)}" '
            f'src="{escape(src)}" aria-label="{escape(label)}">{link(src, "Open video")}</video>')


def research(projects, people):
    cards = []
    directory = {person["title"] for members in people.values() for person in members}
    projects_by_folder = {project["folder"]: project for group in projects.values() for project in group}
    for theme, group in projects.items():
        cards.append(f'<section class="section" id="{slug(theme)}">{heading(theme)}<div class="catalog">')
        for project in group:
            cards.append(card(project, "../"))
            folder, cover, images = project_media(project)
            title = project["title"]
            crumb = '<p class="crumb">' + link("../", "Research") + " / " + escape(theme) + "</p>"
            body = page_head(title, project["short"], crumb, project_website(project))
            if project.get("preview_caption"):
                body += figure("../../" + project["preview"], project["preview_caption"])
            body += figure("../../" + folder + cover, project.get("caption", project.get("name", title)))
            if project.get("video"):
                base = "../../" + folder
                player = video_player(base + project["video"], base + project["video_poster"], title + " demonstration")
                body += f'<figure class="paper-figure">{player}<figcaption>{escape(project["video_caption"])}</figcaption></figure>'
            desc = f'<section class="section"><div class="paper-extra"><div><h2>Project overview</h2><p>{escape(project["description"])}</p>'
            if project.get("approach"):
                desc += f'<h3>Method</h3><p>{escape(project["approach"])}</p>'
            if related := projects_by_folder.get(project.get("related")):
                name = related.get("name", related["title"])
                desc += f'<p>{link("../../" + project_path(related), "Related project · " + name)}</p>'
            credits = []
            for label, field in [("Project lead", "lead"), ("Principal investigator", "pi"),
                                 ("Contributors", "members"), ("Collaborators", "collaborators")]:
                names = [n.strip() for n in project.get(field, "").split("|") if n.strip()]
                if names:
                    if field == "lead" and len(names) > 1:
                        label = "Project leads"
                    links = [link("../../people/#" + slug(n), n) if n in directory else escape(n) for n in names]
                    credits.append(f'<p><strong>{label}</strong><br>' + " · ".join(links) + "</p>")
            body += desc + '</div><div><h2>Project team</h2>' + "".join(credits) + '</div></div></section>'
            if project.get("detail"):
                body += figure("../../" + folder + project["detail"], project["detail_caption"])
            elif len(images) > 1:
                gallery = []
                for image in images:
                    if image == cover:
                        continue
                    stem = Path(image).stem
                    caption_key = "gallery_caption_" + slug(stem).replace("-", "_")
                    caption = project.get(caption_key, stem.replace("_", " ").replace("-", " "))
                    gallery.append(figure("../../" + folder + image, caption))
                grid = '<div class="gallery">' + "".join(gallery) + "</div>"
                if gallery_title := project.get("gallery_title"):
                    grid = '<section class="section">' + heading(gallery_title) + grid + "</section>"
                body += grid
            if project.get("field_photo"):
                body += figure("../../" + project["field_photo"], project["field_caption"])
            page(project_path(project), title, project["short"], body)
        cards.append("</div></section>")
    jump = '<div class="jump">' + "".join(link("#" + slug(theme), theme) for theme in projects) + "</div>"
    page("research", "Research", "Research projects in computational imaging, robotic perception and physics-informed AI.",
         page_head("Research") + jump + "".join(cards))
    # Keep the retired project URL useful for visitors following old links.
    retired = DIST / "research/sfm-comparison"
    retired.mkdir(exist_ok=True)
    (retired / "index.html").write_text('''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0;url=../"><link rel="canonical" href="../">
<title>Research · CIRP Lab</title></head><body><a href="../">Explore current research projects</a></body></html>
''')


def portrait(person, root, compact=False):
    image = person.get("thumbnail") if compact else None
    image = image or person.get("image")
    if image:
        return f'<img class="person-face" src="{root}{escape(image)}" alt="" loading="lazy" decoding="async">'
    initials = "".join(word[0] for word in person["title"].split()[:2])
    return f'<span class="initials" aria-hidden="true">{escape(initials)}</span>'


def member(person, category):
    name = person["title"]
    sub = escape(person.get("placement", person.get("role", "")))
    affiliation = person.get("affiliation", "")
    if category == "Visiting Students" and affiliation:
        sub += "<br>" + escape(affiliation)
        affiliation = ""
    elif slug(affiliation) in {"university-of-hawaii-at-manoa", "university-of-hawai-i-at-manoa"}:
        affiliation = ""
    fields = [("website", "Website"), ("scholar", "Google Scholar"), ("github", "GitHub"), ("linkedin", "LinkedIn"), ("cv", "CV"), ("email", "Email")]
    links = []
    for key, label in fields:
        if not person.get(key):
            continue
        href = ("mailto:" if key == "email" else "") + person[key]
        links.append(f'<a href="{escape(href)}" aria-label="{escape(label)} · {escape(name)}">'
                     f'<svg aria-hidden="true" width="21" height="21"><use href="../images/profile-links.svg#{key}"/></svg>'
                     f'<span aria-hidden="true">{escape(label)}</span></a>')
    profile = [v for v in [person.get("bio"), affiliation, person.get("tags", "").replace(" | ", " · ")] if v]
    more = '<details><summary>Profile</summary>' + "".join(f"<p>{inline(v)}</p>" for v in profile) + "</details>" if profile else ""
    return (f'<article class="person" id="{slug(name)}"><div class="person-top">{portrait(person, "../")}<div><h3>{escape(name)}</h3>'
            f'<div class="metadata">{sub}</div></div></div><div class="profile-links">{"".join(links)}</div>{more}</article>')


def people_page(groups):
    jump = '<div class="jump">' + "".join(link("#" + slug(g), GROUP_LABELS.get(g, g)) for g in groups) + link("#photos", "Group photos") + "</div>"
    parts = [page_head("People"), jump]
    for category, members in groups.items():
        parts.append(f'<section class="section" id="{slug(category)}">{heading(GROUP_LABELS.get(category, category))}<div class="people">')
        parts.extend(member(m, category) for m in members)
        parts.append("</div></section>")
    photos = json.loads((ROOT / "gallery.json").read_text())["images"]
    parts.append('<section class="section" id="photos">' + heading("Group photos") + '<div class="gallery">')
    for i, photo in enumerate(photos, 1):
        parts.append(f'<a href="../{escape(photo)}"><img src="../{escape(photo)}" alt="CIRP Lab group photo {i}" loading="lazy"></a>')
    page("people", "People", "Current members and alumni of CIRP Lab.", "".join(parts) + "</div></section>")


def publication(item):
    authors = item["author"]
    author_names = []
    for author in authors.removesuffix(" and others").split(" and "):
        author_names.append(" ".join(reversed(author.split(", ", 1))))
    author_line = ", ".join(author_names)
    if authors.endswith(" and others"):
        author_line += ", et al."
    landing = item.get("website") or item.get("project")
    title = link(landing, item["title"]) if landing else escape(item["title"])
    venue = item.get("booktitle") or item.get("journal") or item.get("publisher") or item.get("abbr", "")
    year = item["year"]
    venue_year = venue if re.search(rf"\b{re.escape(year)}\b", venue) else " · ".join(filter(None, (venue, year)))
    links = []
    for k, label in [("pdf", item.get("pdf_label", "PDF")), ("doi", "DOI"), ("project", "Project"), ("code", "Code"), ("model", "Model"),
                     ("data", "Data"), ("website", "Link"), ("arxiv", "arXiv"), ("slides", "Slides"), ("video", "Video"),
                     ("workshop", "Workshop"), ("results", "Benchmark results")]:
        if k in item:
            url = item[k]
            if k == "arxiv" and not url.startswith("http"):
                url = "https://arxiv.org/abs/" + url
            if k == "doi" and not url.startswith("http"):
                url = "https://doi.org/" + url
            if url.startswith("https://web.archive.org/"):
                label += " (archived)"
            links.append(f'<a class="res-{k}" href="{escape(url)}">{escape(label)}</a>')
    citation = ""
    if item.get("bibtex_show", "true").lower() != "false":
        citation = f'<details class="citation"><summary>BibTeX</summary><pre><code>{escape(item["bibtex"])}</code></pre></details>'
    note = f'<p class="metadata">{escape(item["note"])}</p>' if item.get("note") else ""
    return (f'<article class="pub" id="{escape(item["key"])}" data-abbr="{escape(item.get("abbr", ""))}"><h3>{title}</h3>'
            f'<p class="pub-meta">{escape(author_line)} · <span>{escape(venue_year)}</span></p>'
            f'{note}<div class="pub-actions">{"".join(links)}{citation}</div></article>')


def news_anchor(stamp, title):
    # Keep existing news links stable when a funding amount is added to a headline.
    return stamp + "-" + slug(re.sub(r" \(\$[\d,]+\)$", "", title))


def home_heading(label, title, url="", action=""):
    more = link(url, action + " →") if url else ""
    return f'<header class="home-heading"><span>{escape(label)}</span><h2>{escape(title)}</h2>{more}</header>'


def work_card(title, href, path, caption, metadata, summary, video="", resources=()):
    version = sha256((ROOT / path).read_bytes()).hexdigest()[:12]
    preview = f"{path}?v={version}"
    work_link = f'<a class="work-link" href="{escape(href)}">'
    if video.lower().endswith(".mp4"):
        media = video_player(video, preview, caption) + work_link
    else:
        media = work_link + f'<img src="{escape(preview)}" alt="{escape(caption)}" loading="lazy" decoding="async">'
    actions = '<div class="work-resources">' + "".join(link(url, label) for url, label in resources) + "</div>" if resources else ""
    return (f'<article>{media}<span class="metadata">{escape(metadata)}</span>'
            f'<h3>{escape(title)}</h3></a><p class="work-summary">{escape(summary)}</p>{actions}</article>')


def home(projects, people, items, pubs):
    content = f'''<section class="hero"><h1>{LAB}</h1>
    <p class="mission">We combine <em>computational imaging</em> and <em>physics-informed AI</em> to design sensors and interpret their measurements.
    Our work spans robotic perception and scientific discovery, from mapping contact forces with polarized light to tracking changes in materials with X-ray diffraction.</p>
    <p class="byline">{link("people/#huaijin-chen", "Huaijin Chen")} leads the lab at the University of Hawaiʻi at Mānoa.</p>
    <div class="hero-links">{link("#research-directions", "Explore our research")}{link("contact/#prospective-students", "Join the lab")}</div>
    <img class="hero-logo" src="images/cirp-hero.webp" width="176" height="176" alt=""></section>'''
    content += '<section class="section" id="lab-news"><header class="home-heading"><span><img class="news-mark" src="images/cirp-mark.png" width="36" height="36" alt=""></span><h2>Lab news</h2>' + link("news/", "All news →") + '</header>'
    for stamp, title, _, anchor in items[:5]:
        content += f'<div class="news-row">{news_time(stamp)}{link("news/#" + anchor, title)}</div>'
    content += '</section>'
    content += '<section class="section" id="selected-work">' + home_heading("Research", "Selected work", "research/", "All projects")
    content += '<div class="work-grid" id="research-directions">' + "".join(card(group[0], "./", theme) for theme, group in projects.items())
    if three_pt := next((item for item in pubs if item["key"] == "kalra2026_3pt"), None):
        content += work_card(
            "3PT", "publications/#kalra2026_3pt", "images/previews/kalra2026_3pt.webp",
            "3PT estimates the poses of a pile of metal parts.", "CVPR & CoRL · 2026",
            "3PT estimates 6DoF poses for unseen objects from RGB images and won 7 of 11 tracks at the 2025 BOP Challenge. For unseen-object detection on BOP-Classic-Core, average precision was 68.9% for 3PT and 70.2% for 3PTv2.",
            video=three_pt.get("video", ""),
            resources=(
                ("publications/#kalra2026_3pt", "3PT paper"),
                ("publications/#kalra2026_3ptv2", "3PTv2 paper"),
                ("https://bop.felk.cvut.cz/leaderboards/pose-detection-unseen-bop24/bop-classic-core/", "BOP results"),
            ),
        )
    featured_projects = (project for group in projects.values() for project in group if "selected_work" in project)
    for project in sorted(featured_projects, key=lambda project: int(project["selected_work"])):
        folder, cover, _ = project_media(project)
        name = project.get("name", project["title"])
        content += work_card(name, project_path(project), project.get("preview", folder + cover),
                             project.get("caption", name), "Research project", project.get("summary", project["short"]))
    content += '</div><p class="work-more">' + link('publications/', 'All publications →') + '</p></section>'
    content += '<section class="section" id="the-group">' + home_heading("People", "The group", "people/", "People & alumni") + '<dl class="roster">'
    for group, members in people.items():
        if group != "Alumni":
            names = [f'<li><a href="people/#{slug(m["title"])}">{portrait(m, "", compact=True)}<span>{escape(m["title"])}</span></a></li>'
                     for m in members]
            content += f'<div><dt>{escape(GROUP_LABELS.get(group, group))}</dt><dd><ul>{"".join(names)}</ul></dd></div>'
    content += '</dl></section>'
    partners = [
        ("National Science Foundation", "https://www.nsf.gov/", "nsf_logo.png"),
        ("NVIDIA", "https://www.nvidia.com/", "nvidia-wordmark.svg"),
        ("Google", "https://www.google.com/", "google.png"),
        ("Hawaiʻi Community Foundation", "https://www.hawaiicommunityfoundation.org/", "hcf_log.jpg"),
        ("Minderoo Foundation", "https://www.minderoo.org/", "minderoo.svg"),
        ("USDA", "https://www.usda.gov/", "usda.jpg"),
    ]
    content += '<section class="section" id="sponsors">' + home_heading("Support", "Sponsors and collaborators") + '<ul class="partners">'
    for name, url, image in partners:
        content += (f'<li><a href="{url}" aria-label="{escape(name)}">'
                    f'<img src="images/{image}" alt="{escape(name)}" loading="lazy"></a></li>')
    page("", LAB, "Computational imaging, tactile sensing and physics-informed AI at the University of Hawaiʻi at Mānoa.",
         content + "</ul></section>")


def main():
    projects, people = records("projects.md"), records("members.md")
    news, pubs = news_records(), bibliography()
    research(projects, people)
    people_page(people)
    content = page_head("News")
    for stamp, title, body, anchor in news:
        content += (f'<article class="news-item" id="{anchor}">{news_time(stamp)}'
                    f'<h2>{escape(title)}</h2><div class="prose">{paragraphs(body)}</div></article>')
    page("news", "News", "News from CIRP Lab.", content)
    years = list(dict.fromkeys(item["year"] for item in pubs))
    options = "".join(f'<option>{escape(year)}</option>' for year in years)
    content = page_head("Publications") + f'''<div class="pub-tools">
      <form role="search" aria-label="Publications" id="publication-search" hidden>
        <label>Search publications<input type="search" name="q" placeholder="Title, author, venue or year"></label>
        <label><span id="year-label">Year</span><select name="year" aria-labelledby="year-label"><option value="">All years</option>{options}</select></label>
        <button type="reset" disabled>Clear</button>
      </form><a href="../publications.bib" download>Download .bib</a></div>
      <p id="pub-status" role="status" hidden></p>'''
    for year in years:
        content += f'<section class="section pub-year" data-year="{escape(year)}">' + heading(year) + "".join(publication(p) for p in pubs if p["year"] == year) + "</section>"
    content += '<script src="search.js" defer></script>'
    page("publications", "Publications", "Publications by members of CIRP Lab.", content)
    outreach = (ROOT / "outreach.html").read_text()
    page("outreach", "Outreach", "Student robotics and community projects from CIRP Lab.", page_head("Outreach") + outreach)
    service = (ROOT / "service.html").read_text()
    page("service", "Service", "Conferences, workshops, and challenges organized by CIRP Lab members.", page_head("Service") + service)
    contact = (ROOT / "contact.html").read_text()
    page("contact", "Contact & join", "Visit CIRP Lab or learn how to join the group.", page_head("Contact & join") + contact)
    home(projects, people, news, pubs)


if __name__ == "__main__":
    main()

"""Render the lab's Markdown and BibTeX records as self-contained HTML pages."""
import json
import re
import sys
import unicodedata
from datetime import date
from hashlib import sha256
from html import escape
from html.parser import HTMLParser
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parents[1]
DIST = Path(sys.argv[1]) if __name__ == "__main__" and len(sys.argv) > 1 else ROOT / "dist"
SHELL = Template((ROOT / "index.html").read_text())
STYLES_VERSION = sha256((ROOT / "styles.css").read_bytes()).hexdigest()[:12]
NAV = {"": "Home", "research": "Research", "publications": "Publications",
       "people": "People", "news": "News", "service": "Service & Outreach",
       "gallery": "Gallery", "contact": "Contact"}
GROUP_LABELS = {"PhD": "PhD students", "Masters": "Master’s students",
                "Undergrads": "Undergraduates", "Visiting Students": "Visiting students"}
ACTIVITY_PAGES = {"Research": "research/", "Publications": "publications/", "News": "news/",
                  "Outreach": "service/#outreach", "Service": "service/#service"}
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


class ArticleCredits(HTMLParser):
    """Index profile links in each article under its existing heading and bookmark."""

    def __init__(self, profiles, category):
        super().__init__()
        self.profiles = profiles
        self.category = category
        self.page = ACTIVITY_PAGES[category].split("#")[0]
        self.anchor = None
        self.in_heading = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article":
            self.anchor = attrs["id"]
            self.names = set()
            self.heading = []
        elif self.anchor and tag in ("h2", "h3") and not self.heading:
            self.in_heading = True
        elif self.anchor and tag == "a":
            href = attrs.get("href", "")
            if href.startswith("../people/#"):
                self.names.add(href.removeprefix("../people/#"))

    def handle_data(self, text):
        if self.in_heading:
            self.heading.append(text)

    def handle_endtag(self, tag):
        if tag in ("h2", "h3"):
            self.in_heading = False
        elif tag == "article" and self.anchor:
            for name in self.names:
                items = self.profiles[name].setdefault(self.category, {})
                items[self.page + "#" + self.anchor] = "".join(self.heading).strip()
            self.anchor = None


def inline(text):
    safe = escape(text)
    safe = re.sub(r'\[([^\]]+)\]\((https?://[^)]+|\.\./[\w./#-]+)\)', r'<a href="\2">\1</a>', safe)
    safe = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', safe)
    return re.sub(r'\*([^*]+)\*', r'<em>\1</em>', safe)


def paragraphs(text):
    blocks = []
    is_followup = False
    for paragraph in text.strip().split("\n\n"):
        lines = paragraph.splitlines()
        photos = re.findall(r'^!\[([^\]\n]+)\]\((images/[\w./-]+) "([^"\n]+)"\)$', paragraph, re.M)
        if photos and len(photos) == len(lines):
            figures = "".join(
                f'<figure><a href="../{escape(path)}" aria-label="Open full-size photo: {escape(alt)}">'
                f'<img src="../{escape(path)}" alt="{escape(alt)}" loading="lazy" decoding="async"></a>'
                f'<figcaption>{escape(caption)}</figcaption></figure>'
                for alt, path, caption in photos
            )
            photo_class = "news-photos" if is_followup else "news-photos news-photos-featured"
            blocks.append(f'<div class="{photo_class}">{figures}</div>')
        elif len(lines) == 1 and paragraph.startswith("### "):
            is_followup = True
            blocks.append(f"<h3>{inline(paragraph[4:])}</h3>")
        elif lines and all(line.startswith("- ") for line in lines):
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
    return f'<time datetime="{stamp}">{label}</time>'


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


def card(project, root):
    folder, cover, _ = project_media(project)
    title = project.get("name", project["title"])
    url = root + project_path(project)
    src = root + project.get("preview", folder + cover)
    plate = "plate photo-preview" if project.get("preview_fit") == "cover" else "plate"
    return f'''<article class="card"><a class="{plate}" href="{url}" aria-label="View {escape(title)}">
    <img loading="lazy" src="{escape(src)}" alt=""></a><div class="card-copy">
    <h4>{link(url, title)}</h4><p>{escape(project["short"])}</p></div></article>'''


def figure(path, caption, kind=""):
    loading = 'fetchpriority="high"' if kind == "project-hero" else 'loading="lazy"'
    return f'''<figure class="paper-figure {kind}"><a href="{escape(path)}" aria-label="Open full-size figure: {escape(caption)}">
    <img src="{escape(path)}" alt="{escape(caption)}" {loading} decoding="async"></a><figcaption>{escape(caption)}</figcaption></figure>'''


def video_player(src, poster, label):
    return (f'<video controls playsinline preload="none" poster="{escape(poster)}" '
            f'src="{escape(src)}" aria-label="{escape(label)}">{link(src, "Open video")}</video>')


def research(projects, profiles):
    sections = []
    instrument_theme = "Physics-Informed AI for Scientific Instrumentation"
    summaries = {
        "Computational Imaging for Robotic Perception": (
            "We design optics and algorithms together so robots can measure what they see and feel. "
            "Patterns of polarized light reveal contact forces at a gripper. In the field, drone images "
            "help us count pineapples and rover images let us measure their size."
        ),
        instrument_theme: (
            "We model how moving atoms scatter X-rays and how a laser cavity’s geometry changes its output. "
            "We also work backward from measurements, testing how well models can reconstruct a scene from "
            "optical data or trace a shoreline in a satellite image."
        ),
    }
    instrument_id = slug(instrument_theme)
    # Preserve published bookmarks to the two directions and their former topics.
    bookmarks = {
        instrument_id: '<span id="physics-informed-ai"></span><span id="scientific-instrumentation"></span>',
        instrument_id + "-predicting-instrument-response": '<span id="scientific-instrumentation-modeling-physical-systems"></span>',
        instrument_id + "-evaluating-frontier-models-for-imaging-applications": (
            f'<span id="{instrument_id}-interpreting-sensor-measurements"></span>'
            '<span id="physics-informed-ai-evaluating-vision-models"></span>'
        ),
    }
    projects_by_folder = {project["folder"]: project for group in projects.values() for project in group}
    for theme, group in projects.items():
        theme_id = slug(theme)
        topics = {}
        for project in group:
            topic = project["topic"]
            topic_id = theme_id + "-" + slug(topic)
            topics.setdefault(topic, []).append(card(project, "../"))
            folder, cover, images = project_media(project)
            title = project["title"]
            crumb = '<p class="crumb">' + link("../", "Research") + " / " + link("../#" + theme_id, theme)
            crumb += " / " + link("../#" + topic_id, topic) + "</p>"
            body = page_head(title, project["short"], crumb, project_website(project))
            body += figure("../../" + folder + cover, project.get("caption", project.get("name", title)), "project-hero")
            body += f'<section class="section project-overview"><h2>Project overview</h2><p>{escape(project["description"])}</p>'
            if project.get("approach"):
                body += f'<h3>Method</h3><p>{escape(project["approach"])}</p>'
            if related := projects_by_folder.get(project.get("related")):
                name = related.get("name", related["title"])
                body += f'<p>{link("../../" + project_path(related), "Related project · " + name)}</p>'
            body += '</section>'

            media = []
            if project.get("video"):
                base = "../../" + folder
                player = video_player(base + project["video"], base + project["video_poster"], title + " demonstration")
                media.append(f'<figure class="paper-figure project-feature">{player}<figcaption>{escape(project["video_caption"])}</figcaption></figure>')
            if project.get("preview_caption"):
                media.append(figure("../../" + project["preview"], project["preview_caption"], "project-feature"))
            if project.get("detail"):
                media.append(figure("../../" + folder + project["detail"], project["detail_caption"], "project-feature"))
            else:
                gallery = []
                for image in images:
                    if image == cover:
                        continue
                    stem = Path(image).stem
                    caption_key = "gallery_caption_" + slug(stem).replace("-", "_")
                    caption = project.get(caption_key, stem.replace("_", " ").replace("-", " "))
                    gallery.append(figure("../../" + folder + image, caption))
                if gallery:
                    columns = 3 if len(gallery) == 3 or len(gallery) >= 5 else 2
                    media.append(f'<div class="project-gallery" data-columns="{columns}">' + "".join(gallery) + "</div>")
            if project.get("field_photo"):
                media.append(figure("../../" + project["field_photo"], project["field_caption"], "project-feature project-field"))
            if media:
                media_title = project.get("gallery_title", "Project media")
                body += '<section class="section project-media">' + heading(media_title) + "".join(media) + "</section>"

            if project.get("supplement"):
                body += (ROOT / project["supplement"]).read_text()

            credits = []
            for label, field in [("Project lead", "lead"), ("Principal investigator", "pi"), ("Advisors", "advisors"),
                                 ("Contributors", "members"), ("Collaborators", "collaborators")]:
                names = [n.strip() for n in project.get(field, "").split("|") if n.strip()]
                if names:
                    if field == "lead" and len(names) > 1:
                        label = "Project leads"
                    links = []
                    for name in names:
                        key = slug(name)
                        if key in profiles:
                            profiles[key].setdefault("Research", {})[project_path(project)] = project.get("name", title)
                            links.append(link("../../people/#" + key, name))
                        else:
                            links.append(escape(name))
                    label = project.get(field + "_label", label)
                    credits.append(f'<p><strong>{escape(label)}</strong><br>' + " · ".join(links) + "</p>")
            body += '<section class="section project-team" id="project-team"><h2>Project team</h2><div>' + "".join(credits) + '</div></section>'
            page(project_path(project), title, project["short"], body)
        sections.append(f'<section class="section direction" id="{theme_id}">{bookmarks.get(theme_id, "")}{heading(theme)}')
        if theme in summaries:
            sections.append(f'<p class="section-summary">{escape(summaries[theme])}</p>')
        for topic, cards in topics.items():
            topic_id = theme_id + "-" + slug(topic)
            sections.append(f'<section class="research-topic" id="{topic_id}">{bookmarks.get(topic_id, "")}<h3>{escape(topic)}</h3>'
                            + '<div class="catalog">' + "".join(cards) + "</div></section>")
        sections.append("</section>")
    jump = '<div class="jump">' + "".join(link("#" + slug(theme), theme) for theme in projects) + "</div>"
    page("research", "Research", "Computational imaging for robotic perception and physics-informed AI for scientific instrumentation.",
         page_head("Research", "We design sensors that turn light into measurements of touch, shape and spectra. "
                   "For scientific instruments, we use physics-informed AI to predict signals and interpret measurements.")
         + jump + "".join(sections))
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


def profile_activity(activity):
    groups = []
    for category, path in ACTIVITY_PAGES.items():
        if entries := activity.get(category):
            category_link = link("../" + path, category)
            items = "".join("<li>" + link("../" + url, title) + "</li>" for url, title in entries.items())
            groups.append(f"<dt>{category_link}</dt><dd><ul>{items}</ul></dd>")
    if not groups:
        return ""
    listing = "<dl>" + "".join(groups) + "</dl>"
    return f'<details class="profile-activity"><summary>Research and activities</summary>{listing}</details>'


def member(person, category, activity):
    name = person["title"]
    placement = person.get("placement", "")
    if category == "Alumni" and placement:
        placement = "Now at " + placement
    sub = escape(placement or person.get("role", ""))
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
    activity_html = "" if person.get("show_activity", "").lower() == "false" else profile_activity(activity)
    return (f'<article class="person" id="{slug(name)}"><div class="person-top">{portrait(person, "../")}<div><h3>{escape(name)}</h3>'
            f'<div class="metadata">{sub}</div></div></div><div class="profile-links">{"".join(links)}</div>'
            f'{more}{activity_html}</article>')


def people_page(groups, profiles):
    jump = '<div class="jump">' + "".join(link("#" + slug(g), GROUP_LABELS.get(g, g)) for g in groups) + link("../gallery/", "Group photos") + "</div>"
    parts = [page_head("People"), jump]
    for category, members in groups.items():
        parts.append(f'<section class="section" id="{slug(category)}">{heading(GROUP_LABELS.get(category, category))}<div class="people">')
        parts.extend(member(m, category, profiles[slug(m["title"])]) for m in members)
        parts.append("</div></section>")
    parts.append('<section class="section" id="photos">' + heading("Group photos", "../gallery/", "View gallery →") + "</section>")
    page("people", "People", "Current members and alumni of CIRP Lab.", "".join(parts))


def gallery_page():
    album = json.loads((ROOT / "gallery.json").read_text())
    related = {}
    for entry in album.get("related_pages", []):
        anchor = link("../" + entry["href"], entry["label"])
        for photo in entry["photos"]:
            related.setdefault(photo, []).append(anchor)
    tiles = []
    for index, photo in enumerate(album["images"]):
        path = Path(photo)
        thumbnail = Path("images/gallery/thumbs") / (path.stem + ".webp")
        src = thumbnail if (ROOT / thumbnail).is_file() else path
        size = album.get("dimensions", {}).get(photo)
        size_attrs = f' width="{size[0]}" height="{size[1]}"' if size else ""
        ratio = size[0] / size[1] if size else 4 / 3
        description = album.get("descriptions", {}).get(photo, f"CIRP Lab photo {index + 1}")
        caption = album.get("captions", {}).get(photo) or description
        place = album.get("locations", {}).get(photo, "")
        label = f'<span class="photo-place">{escape(place)}</span>' if place else ""
        sources = '<span class="photo-links">' + "".join(related[photo]) + '</span>' if photo in related else ""
        loading = "eager" if index < 4 else "lazy"
        tiles.append(
            f'<figure id="{escape(path.stem)}" style="--ratio:{ratio:.6f}">'
            f'<a href="../{escape(path.as_posix())}"><img src="../{escape(src.as_posix())}" '
            f'alt="{escape(description)}"{size_attrs} loading="{loading}" decoding="async"></a>'
            f'<figcaption>{label}<span class="photo-caption">{escape(caption)}</span>{sources}</figcaption></figure>'
        )

    def icon(name):
        return (f'<svg width="20" height="20" aria-hidden="true">'
                f'<use href="../images/gallery-controls.svg#{name}"/></svg>')

    header = f"""
    <header class="page-head gallery-head"><h1>Gallery</h1>
      <div class="gallery-view" role="group" aria-label="Gallery view" hidden>
        <button type="button" id="show-thumbnails" aria-label="Photo grid" title="Photo grid"
          aria-pressed="true" aria-controls="gallery-thumbnails">{icon("grid")}</button>
        <button type="button" id="show-slideshow" aria-label="Slideshow" title="Slideshow"
          aria-pressed="false" aria-controls="gallery-slideshow">{icon("slides")}</button>
      </div>
    </header>
    """
    slideshow = f"""
    <section class="gallery-slideshow" id="gallery-slideshow" aria-label="Photo slideshow" tabindex="-1" hidden>
      <figure>
        <figcaption class="slide-footer">
          <span class="slide-info" role="status" aria-live="polite" aria-atomic="true">
            <span id="slide-place" class="photo-place" hidden></span>
            <span id="slide-caption"></span>
            <span id="slide-links" class="photo-links"></span>
          </span>
          <span class="slide-tools">
            <span id="slide-position"></span>
            <button type="button" id="slide-play" aria-label="Play slideshow" title="Play slideshow">{icon("play")}</button>
          </span>
        </figcaption>
        <div class="gallery-reel">
          <div class="gallery-strip" aria-hidden="true"></div>
          <a class="gallery-stage" id="slide-original" aria-label="Open full-size photo" title="Open full-size photo"></a>
          <button type="button" id="slide-previous" aria-label="Previous photo" title="Previous photo">{icon("previous")}</button>
          <button type="button" id="slide-next" aria-label="Next photo" title="Next photo">{icon("next")}</button>
        </div>
      </figure>
    </section>
    """
    grid = '<div class="lab-gallery" id="gallery-thumbnails">' + "".join(tiles) + "</div>"
    version = sha256((ROOT / "scripts/gallery-slideshow.js").read_bytes()).hexdigest()[:12]
    script = f'<script src="slideshow.js?v={version}" defer></script>'
    page("gallery", "Gallery", "Group photos and life around the lab.", header + grid + slideshow + script)


def publication(item, profiles):
    authors = item["author"]
    author_names = []
    for author in authors.removesuffix(" and others").split(" and "):
        name = " ".join(reversed(author.split(", ", 1)))
        key = slug(name)
        author_names.append(link("../people/#" + key, name) if key in profiles else escape(name))
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
            f'<p class="pub-meta">{author_line} · <span>{escape(venue_year)}</span></p>'
            f'{note}<div class="pub-actions">{"".join(links)}{citation}</div></article>')


def news_anchor(stamp, title):
    # Keep existing news links stable when a funding amount is added to a headline.
    return stamp + "-" + slug(re.sub(r" \(\$[\d,]+\)$", "", title))


def home_heading(label, title, url="", action=""):
    more = link(url, action + " →") if url else ""
    return f'<header class="home-heading"><span>{escape(label)}</span><h2>{escape(title)}</h2>{more}</header>'


def work_card(title, href, path, caption, summary, video="", resources=(), photo_preview=False):
    version = sha256((ROOT / path).read_bytes()).hexdigest()[:12]
    preview = f"{path}?v={version}"
    work_link = f'<a class="work-link{" photo-preview" if photo_preview else ""}" href="{escape(href)}">'
    if video.lower().endswith(".mp4"):
        media = video_player(video, preview, caption) + work_link
    else:
        media = work_link + f'<img src="{escape(preview)}" alt="{escape(caption)}" loading="lazy" decoding="async">'
    actions = '<div class="work-resources">' + "".join(link(url, label) for url, label in resources) + "</div>" if resources else ""
    return (f'<article>{media}'
            f'<h3>{escape(title)}</h3></a><p class="work-summary">{escape(summary)}</p>{actions}</article>')


def selected_research(projects, pubs):
    highlights = []
    selected = (project for group in projects.values() for project in group if "selected_work" in project)
    for project in sorted(selected, key=lambda p: int(p["selected_work"])):
        folder, cover, _ = project_media(project)
        title = project.get("name", project["title"])
        highlights.append(work_card(project.get("question", title), project_path(project), project.get("preview", folder + cover),
                                    project.get("preview_caption", title), project.get("summary", project["short"]),
                                    photo_preview=project.get("preview_fit") == "cover"))
    if three_pt := next((item for item in pubs if item["key"] == "kalra2026_3pt"), None):
        highlights.append(work_card(
            "How can a robot estimate the pose of an unfamiliar object from a color image?",
            "publications/#kalra2026_3pt", "images/previews/kalra2026_3pt.webp",
            "3PT estimates the poses of a pile of metal parts.",
            "3PT uses color images to detect unfamiliar objects and estimate their 3D positions and orientations for robotic manipulation.",
            video=three_pt.get("video", ""),
            resources=(
                ("publications/#kalra2026_3pt", "3PT paper"),
                ("publications/#kalra2026_3ptv2", "3PTv2 paper"),
                ("https://bop.felk.cvut.cz/leaderboards/pose-detection-unseen-bop24/bop-classic-core/", "BOP results"),
            ),
        ))
    return ('<section class="section" id="selected-work"><header class="section-head">'
            '<h2>Research highlight</h2>' + link("research/", "All projects →") + '</header>'
            '<div class="work-grid" id="research-directions">' + "".join(highlights)
            + '</div><p class="work-more">' + link("publications/", "All publications →") + '</p></section>')


def home(projects, people, items, pubs):
    content = f'''<section class="hero"><h1>{LAB}</h1>
    <p class="mission">We develop imaging and perception systems for <em>robotics</em> and <em>scientific instrumentation</em>.
    We design sensors and algorithms together to help robots understand their surroundings and scientists measure how physical systems change.</p>
    <div class="hero-links">{link("research/", "Explore our research")}{link("contact/#prospective-students", "Join the lab")}</div>
    <img class="hero-logo" src="images/cirp-hero.webp" width="176" height="176" alt=""></section>'''
    content += '<section class="section" id="lab-news"><header class="home-heading"><span><img class="news-mark" src="images/cirp-mark.png" width="36" height="36" alt=""></span><h2>Lab news</h2>' + link("news/", "All news →") + '</header>'
    for stamp, title, _, anchor in items[:5]:
        content += f'<div class="news-row">{news_time(stamp)}{link("news/#" + anchor, title)}</div>'
    content += '</section>'
    content += selected_research(projects, pubs)
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
    content += '<section class="section" id="sponsors">' + heading("Sponsors")
    content += ('<p class="section-summary">We thank our sponsors for supporting student research '
                'with funding and equipment.</p><ul class="partners">')
    for name, url, image in partners:
        content += (f'<li><a href="{url}" aria-label="{escape(name)}">'
                    f'<img src="images/{image}" alt="{escape(name)}" loading="lazy"></a></li>')
    page("", LAB, "Imaging and perception systems for robotics and scientific instrumentation at the University of Hawaiʻi at Mānoa.",
         content + "</ul></section>")


def main():
    projects, people = records("projects.md"), records("members.md")
    news, pubs = news_records(), bibliography()
    profiles = {slug(person["title"]): {} for group in people.values() for person in group}
    research(projects, profiles)
    gallery_page()
    content = page_head("News")
    for stamp, title, body, anchor in news:
        content += (f'<article class="news-item" id="{anchor}">{news_time(stamp)}'
                    f'<h2>{escape(title)}</h2><div class="prose">{paragraphs(body)}</div></article>')
    ArticleCredits(profiles, "News").feed(content)
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
    earlier_years = []
    for year in years:
        papers = "".join(publication(p, profiles) for p in pubs if p["year"] == year)
        section = f'<section class="section pub-year" data-year="{escape(year)}">{heading(year)}{papers}</section>'
        if year.isdecimal() and int(year) <= 2024:
            earlier_years.append(section)
        else:
            content += section
    if earlier_years:
        content += '<details id="earlier-work" class="section"><summary>Earlier work</summary>' + "".join(earlier_years) + "</details>"
    version = sha256((ROOT / "scripts/publication-search.js").read_bytes()).hexdigest()[:12]
    content += f'<script src="search.js?v={version}" defer></script>'
    ArticleCredits(profiles, "Publications").feed(content)
    page("publications", "Publications", "Publications by members of CIRP Lab.", content)
    title = NAV["service"]
    service = (ROOT / "service.html").read_text()
    outreach = (ROOT / "outreach.html").read_text()
    ArticleCredits(profiles, "Service").feed(service)
    ArticleCredits(profiles, "Outreach").feed(outreach)
    people_page(people, profiles)
    jump = '<div class="jump">' + link("#service", "Service") + link("#outreach", "Outreach") + "</div>"
    content = page_head(title) + jump
    content += '<section id="service">' + heading("Service") + service + "</section>"
    content += '<section id="outreach">' + heading("Outreach") + outreach + "</section>"
    # Forward bookmarks for the challenge and its two event reports to Research.
    content += """<script>
function forwardProjectBookmark() {
  if (["#farm-robotics-challenge", "#fira-usa-2025", "#plug-and-play-summit"].includes(location.hash)) {
    const section = location.hash === "#farm-robotics-challenge" ? "" : location.hash;
    location.replace("../research/frc2025/" + location.search + section);
  }
}
forwardProjectBookmark();
window.addEventListener("hashchange", forwardProjectBookmark);
</script>"""
    page("service", title, "Conferences, workshops, student robotics and community projects from CIRP Lab.", content)

    retired = DIST / "outreach"
    retired.mkdir(exist_ok=True)
    (retired / "index.html").write_text('''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="robots" content="noindex">
<link rel="canonical" href="../service/"><title>Service &amp; Outreach · CIRP Lab</title>
<script>location.replace("../service/" + location.search + (location.hash || "#outreach"))</script>
<meta http-equiv="refresh" content="0;url=../service/#outreach"></head>
<body><a href="../service/#outreach">View outreach activities</a></body></html>
''')
    contact = (ROOT / "contact.html").read_text()
    page("contact", "Contact & join", "Visit CIRP Lab or learn how to join the group.", page_head("Contact & join") + contact)
    home(projects, people, news, pubs)


if __name__ == "__main__":
    main()

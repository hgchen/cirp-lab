const form = document.querySelector("#publication-search");
const query = form.elements.q;
const year = form.elements.year;
const clear = form.querySelector("[type=reset]");
const status = document.querySelector("#pub-status");

function normalize(text) {
  return text.normalize("NFKD").replace(/\p{M}/gu, "").toLowerCase()
    .replace(/['’]/g, "").replace(/[^\p{L}\p{N}]+/gu, " ").trim();
}

const groups = Array.from(document.querySelectorAll(".pub-year"), section => ({
  section,
  papers: Array.from(section.querySelectorAll(".pub"), element => ({
    element,
    text: normalize([element.querySelector("h3").textContent, element.querySelector(".pub-meta").textContent,
      element.dataset.abbr, element.querySelector(".metadata")?.textContent || ""].join(" "))
  }))
}));

function filterPapers() {
  const terms = normalize(query.value).split(" ").filter(Boolean);
  let count = 0;
  for (const {section, papers} of groups) {
    const matchesYear = !year.value || section.dataset.year === year.value;
    let shown = 0;
    for (const {element, text} of papers) {
      element.hidden = !(matchesYear && terms.every(term => text.includes(term)));
      if (!element.hidden) shown++;
    }
    section.hidden = shown === 0;
    count += shown;
  }
  clear.disabled = !query.value && !year.value;
  status.textContent = count ? count + (count === 1 ? " publication" : " publications") : "No matching publications. Try another search or clear the filters.";
}

form.addEventListener("submit", event => { event.preventDefault(); filterPapers(); });
query.addEventListener("input", filterPapers);
year.addEventListener("change", filterPapers);
form.addEventListener("reset", () => {
  requestAnimationFrame(() => { filterPapers(); query.focus(); });
});
window.addEventListener("pageshow", filterPapers);
form.hidden = false;
status.hidden = false;
filterPapers();

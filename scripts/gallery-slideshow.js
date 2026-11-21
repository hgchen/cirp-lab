const thumbnails = document.querySelector("#gallery-thumbnails");
const slideshow = document.querySelector("#gallery-slideshow");
const viewButtons = document.querySelector(".gallery-view");
const thumbnailButton = document.querySelector("#show-thumbnails");
const slideshowButton = document.querySelector("#show-slideshow");
const previousButton = document.querySelector("#slide-previous");
const nextButton = document.querySelector("#slide-next");
const playButton = document.querySelector("#slide-play");
const reel = document.querySelector(".gallery-reel");
const strip = document.querySelector(".gallery-strip");
const slideCaption = document.querySelector("#slide-caption");
const slideLinks = document.querySelector("#slide-links");
const slidePlace = document.querySelector("#slide-place");
const slideInfo = document.querySelector(".slide-info");
const slideOriginal = document.querySelector("#slide-original");
const slidePosition = document.querySelector("#slide-position");
const photos = [...thumbnails.querySelectorAll("figure")].map(figure => {
  const image = figure.querySelector("img");
  const link = figure.querySelector(":scope > a");
  const panel = new Image();
  panel.className = "strip-photo";
  panel.alt = "";
  panel.hidden = true;
  panel.addEventListener("error", () => {
    if (panel.src === link.href && panel.src !== image.src) panel.src = image.src;
  });
  strip.append(panel);
  return {
    panel,
    ratio: Number(figure.style.getPropertyValue("--ratio")) || 4 / 3,
    id: figure.id,
    link,
    alt: image.alt,
    caption: figure.querySelector(".photo-caption").textContent,
    related: figure.querySelectorAll(".photo-links a"),
    place: figure.querySelector(".photo-place")?.textContent || "",
  };
});

const wrap = n => ((n % photos.length) + photos.length) % photos.length;
const portraitPhone = matchMedia("(max-width:640px) and (orientation:portrait)");
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");
let target = Math.max(0, photos.findIndex(photo => photo.id === location.hash.slice(1)));
let position = target;
let index = -1;
let frame = 0;
let timer = null;
let width, stripWidth;
const gap = 4;

function selectPhoto(current) {
  if (current === index) return;
  if (index >= 0) photos[index].panel.removeAttribute("id");
  index = current;
  const photo = photos[index];
  photo.panel.id = "slide-image";
  slideOriginal.href = photo.link.href;
  slideOriginal.setAttribute("aria-label", "Open full-size photo: " + photo.alt);
  slidePlace.textContent = photo.place;
  slidePlace.hidden = !photo.place;
  slideCaption.textContent = photo.caption;
  slideLinks.replaceChildren(...Array.from(photo.related, anchor => anchor.cloneNode(true)));
  slidePosition.textContent = `${index + 1} / ${photos.length}`;
}

function drawStrip() {
  const leftIndex = Math.floor(position);
  const left = photos[wrap(leftIndex)];
  const right = photos[wrap(leftIndex + 1)];
  const fraction = position - leftIndex;
  const distance = (left.width + right.width) / 2 + gap;
  const center = left.center + fraction * distance;
  const current = fraction < 0.5 ? left : right;
  reel.style.height = (left.height + (right.height - left.height) * fraction) + "px";
  reel.style.setProperty("--active-width", current.width + "px");

  for (const photo of photos) {
    // When the album loops, place each photo on the closest side of the frame.
    let offset = photo.center - center;
    offset -= stripWidth * Math.round(offset / stripWidth);
    const panel = photo.panel;
    panel.hidden = Math.abs(offset) > width + photo.width / 2;
    if (panel.hidden) continue;
    if (!panel.hasAttribute("src")) panel.src = photo.link.href;
    const leftEdge = (width / 2 + offset - photo.width / 2) + "px";
    panel.style.left = leftEdge;
    if (photo === current) slideOriginal.style.left = leftEdge;
  }
  selectPhoto(wrap(Math.round(position)));
}

function layoutStrip() {
  if (slideshow.hidden) return;
  width = reel.clientWidth;
  const widest = Math.max(...photos.map(photo => photo.ratio));
  const preview = Math.min(70, width * 0.065);
  const height = Math.min(innerHeight * 0.55, 500, (width - 2 * preview) / Math.max(1.92, widest));
  stripWidth = 0;
  for (const photo of photos) {
    photo.width = portraitPhone.matches ? width : height * photo.ratio;
    photo.height = photo.width / photo.ratio;
    photo.center = stripWidth + photo.width / 2;
    photo.panel.style.width = photo.width + "px";
    stripWidth += photo.width + gap;
  }
  drawStrip();
}

function settle() {
  cancelAnimationFrame(frame);
  target = wrap(target);
  position = target;
  if (!slideshow.hidden) drawStrip();
}

function slideBy(direction) {
  target += direction;
  cancelAnimationFrame(frame);
  if (reducedMotion.matches) {
    settle();
    return;
  }
  const from = position;
  const start = performance.now();
  const duration = Math.min(400, 220 + 55 * Math.abs(target - from));
  function tick(now) {
    const t = Math.min(1, (now - start) / duration);
    if (t === 1) {
      settle();
      return;
    }
    position = from + (target - from) * t * t * (3 - 2 * t);
    drawStrip();
    frame = requestAnimationFrame(tick);
  }
  frame = requestAnimationFrame(tick);
}

function setPlaying(playing) {
  clearInterval(timer);
  timer = playing ? setInterval(() => slideBy(1), 5000) : null;
  const label = playing ? "Pause slideshow" : "Play slideshow";
  playButton.setAttribute("aria-label", label);
  playButton.title = label;
  playButton.querySelector("use").setAttribute("href", "../images/gallery-controls.svg#" + (playing ? "pause" : "play"));
  slideInfo.setAttribute("aria-live", playing ? "off" : "polite");
}

function step(direction) {
  setPlaying(false);
  slideBy(direction);
}

function setSlideshow(open, focusPhoto = false) {
  if (open && !slideshow.hidden) return;
  thumbnails.hidden = open;
  slideshow.hidden = !open;
  thumbnailButton.setAttribute("aria-pressed", String(!open));
  slideshowButton.setAttribute("aria-pressed", String(open));
  if (open) {
    position = target;
    layoutStrip();
    slideshow.focus({ preventScroll: true });
    if (viewButtons.getBoundingClientRect().top < 0) viewButtons.scrollIntoView({ block: "start" });
  } else {
    cancelAnimationFrame(frame);
    target = Math.max(index, 0);
    setPlaying(false);
    (focusPhoto ? photos[index].link : thumbnailButton).focus();
  }
}

if (photos.length) {
  slideLinks.addEventListener("focusin", () => setPlaying(false));
  reducedMotion.addEventListener("change", () => {
    if (reducedMotion.matches) settle();
  });
  window.addEventListener("resize", layoutStrip);
  viewButtons.hidden = false;
  thumbnails.classList.add("interactive");
  photos.forEach((photo, position) => {
    photo.link.addEventListener("click", event => {
      if (event.ctrlKey || event.metaKey || event.altKey || event.shiftKey || event.button !== 0) return;
      event.preventDefault();
      target = position;
      setSlideshow(true);
    });
  });
  thumbnailButton.addEventListener("click", () => setSlideshow(false));
  slideshowButton.addEventListener("click", () => setSlideshow(true));
  previousButton.addEventListener("click", () => step(-1));
  nextButton.addEventListener("click", () => step(1));
  playButton.addEventListener("click", () => setPlaying(timer === null));
  previousButton.disabled = nextButton.disabled = playButton.disabled = photos.length < 2;

  slideshow.addEventListener("keydown", event => {
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    if (event.key === "Escape") {
      event.preventDefault();
      setSlideshow(false, true);
    } else if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
      event.preventDefault();
      step(event.key === "ArrowLeft" ? -1 : 1);
    }
  });

  let touchStart;
  reel.addEventListener("touchstart", event => {
    touchStart = event.touches.length === 1 ? event.touches[0] : null;
  }, { passive: true });
  reel.addEventListener("touchcancel", () => { touchStart = null; });
  reel.addEventListener("touchend", event => {
    if (!touchStart || event.touches.length) return;
    const dx = event.changedTouches[0].clientX - touchStart.clientX;
    const dy = event.changedTouches[0].clientY - touchStart.clientY;
    touchStart = null;
    if (Math.abs(dx) > 40 && Math.abs(dx) > 1.5 * Math.abs(dy)) {
      if (event.cancelable) event.preventDefault();
      step(dx < 0 ? 1 : -1);
    }
  }, { passive: false });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) setPlaying(false);
  });
}

const thumbnails = document.querySelector("#gallery-thumbnails");
const slideshow = document.querySelector("#gallery-slideshow");
const viewButtons = document.querySelector(".gallery-view");
const thumbnailButton = document.querySelector("#show-thumbnails");
const slideshowButton = document.querySelector("#show-slideshow");
const previousButton = document.querySelector("#slide-previous");
const nextButton = document.querySelector("#slide-next");
const playButton = document.querySelector("#slide-play");
const reel = document.querySelector(".gallery-reel");
const wheel = document.querySelector(".gallery-wheel");
const slideCaption = document.querySelector("#slide-caption");
const slidePlace = document.querySelector("#slide-place");
const slideInfo = document.querySelector(".slide-info");
const slideOriginal = document.querySelector("#slide-original");
const slidePosition = document.querySelector("#slide-position");
const photos = [...thumbnails.querySelectorAll("figure")].map(figure => {
  const image = figure.querySelector("img");
  const link = figure.querySelector("a");
  const panel = new Image();
  panel.className = "wheel-photo";
  panel.alt = "";
  panel.hidden = true;
  panel.addEventListener("error", () => {
    if (panel.src === image.src && panel.src !== link.href) panel.src = link.href;
  });
  wheel.append(panel);
  return {
    panel,
    ratio: Number(figure.style.getPropertyValue("--ratio")) || 4 / 3,
    id: figure.id,
    link,
    thumbnail: image,
    alt: image.alt,
    caption: figure.querySelector(".photo-caption").textContent,
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
let width, desktopHeight, arcLength;

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
  slidePosition.textContent = `${index + 1} / ${photos.length}`;
  if (photo.panel.src !== photo.link.href) {
    const full = new Image();
    full.src = photo.link.href;
    full.decode().then(() => {
      photo.panel.src = full.src;
    }).catch(() => {}); // Keep the preview if the original is unavailable.
  }
}

function drawWheel() {
  const left = photos[wrap(Math.floor(position))];
  const right = photos[wrap(Math.floor(position) + 1)];
  const fraction = position - Math.floor(position);
  const angle = left.angle + fraction * (left.halfArc + right.halfArc);
  const height = portraitPhone.matches
    ? width * ((1 - fraction) / left.ratio + fraction / right.ratio)
    : desktopHeight;
  const centerDepth = left.depth + (right.depth - left.depth) * fraction;
  reel.style.height = height + "px";
  wheel.style.transform = `translateZ(${-centerDepth * height}px)`;
  for (const photo of photos) {
    // Use the nearest copy of the angle across the album's wrap point.
    let offset = photo.angle - angle;
    offset -= arcLength * Math.round(offset / arcLength);
    const panel = photo.panel;
    panel.hidden = Math.abs(offset) > Math.PI / 2 + photo.halfArc;
    if (panel.hidden) continue;
    if (!panel.hasAttribute("src")) panel.src = photo.thumbnail.src;
    panel.style.width = height * photo.ratio + "px";
    panel.style.transform = `rotateY(${offset}rad) translateZ(${photo.depth * height}px) translateX(-50%)`;
  }
  selectPhoto(wrap(Math.round(position)));
  reel.style.setProperty("--active-width", Math.min(width, photos[index].ratio * height) + "px");
}

function layoutWheel() {
  if (slideshow.hidden) return;
  width = reel.clientWidth;
  const widest = Math.max(...photos.map(photo => photo.ratio));
  desktopHeight = Math.min(innerHeight * 0.55, 500, (width - 8) / Math.max(1.92, widest));
  const radius = Math.max(1.7, widest * 0.6, width / desktopHeight);
  arcLength = 0;
  // Each photo is a chord of the same circle. Its width determines its arc.
  for (const photo of photos) {
    photo.halfArc = Math.asin((photo.ratio + 0.006) / (2 * radius));
    photo.angle = arcLength + photo.halfArc;
    photo.depth = radius * Math.cos(photo.halfArc);
    arcLength += 2 * photo.halfArc;
  }
  drawWheel();
}

function settle() {
  cancelAnimationFrame(frame);
  target = wrap(target);
  position = target;
  if (!slideshow.hidden) drawWheel();
}

function rotate(direction) {
  target += direction;
  cancelAnimationFrame(frame);
  if (reducedMotion.matches) {
    settle();
    return;
  }
  const from = position;
  const start = performance.now();
  const duration = Math.min(600, 420 + 45 * Math.abs(target - from));
  function tick(now) {
    const t = Math.min(1, (now - start) / duration);
    if (t === 1) {
      settle();
      return;
    }
    position = from + (target - from) * t * t * (3 - 2 * t);
    drawWheel();
    frame = requestAnimationFrame(tick);
  }
  frame = requestAnimationFrame(tick);
}

function setPlaying(playing) {
  clearInterval(timer);
  timer = playing ? setInterval(() => rotate(1), 5000) : null;
  const label = playing ? "Pause slideshow" : "Play slideshow";
  playButton.setAttribute("aria-label", label);
  playButton.title = label;
  playButton.querySelector("use").setAttribute("href", "../images/gallery-controls.svg#" + (playing ? "pause" : "play"));
  slideInfo.setAttribute("aria-live", playing ? "off" : "polite");
}

function step(direction) {
  setPlaying(false);
  rotate(direction);
}

function setSlideshow(open, focusPhoto = false) {
  if (open && !slideshow.hidden) return;
  thumbnails.hidden = open;
  slideshow.hidden = !open;
  thumbnailButton.setAttribute("aria-pressed", String(!open));
  slideshowButton.setAttribute("aria-pressed", String(open));
  if (open) {
    position = target;
    layoutWheel();
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
  reducedMotion.addEventListener("change", () => {
    if (reducedMotion.matches) settle();
  });
  window.addEventListener("resize", layoutWheel);
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

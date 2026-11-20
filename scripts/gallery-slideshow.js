const thumbnails = document.querySelector("#gallery-thumbnails");
const slideshow = document.querySelector("#gallery-slideshow");
const viewButtons = document.querySelector(".gallery-view");
const thumbnailButton = document.querySelector("#show-thumbnails");
const slideshowButton = document.querySelector("#show-slideshow");
const previousButton = document.querySelector("#slide-previous");
const nextButton = document.querySelector("#slide-next");
const playButton = document.querySelector("#slide-play");
const reel = document.querySelector(".gallery-reel");
const slideImage = document.querySelector("#slide-image");
const slideCaption = document.querySelector("#slide-caption");
const slidePlace = document.querySelector("#slide-place");
const slideInfo = document.querySelector(".slide-info");
const slideOriginal = document.querySelector("#slide-original");
const slidePosition = document.querySelector("#slide-position");
const previousPreview = document.querySelector("#previous-preview");
const nextPreview = document.querySelector("#next-preview");
const photos = [...thumbnails.querySelectorAll("figure")].map(figure => {
  const image = figure.querySelector("img");
  return {
    id: figure.id,
    link: figure.querySelector("a"),
    thumbnail: image,
    alt: image.alt,
    caption: figure.querySelector(".photo-caption").textContent,
    place: figure.querySelector(".photo-place")?.textContent || "",
  };
});

let index = Math.max(0, photos.findIndex(photo => photo.id === location.hash.slice(1)));
let requestedIndex = index;
let revision = 0;
let timer = null;
const reducedMotion = matchMedia("(prefers-reduced-motion: reduce)");

function finishTransition() {
  reel.querySelector(".slide-leaving")?.remove();
  reel.getAnimations({ subtree: true }).forEach(animation => animation.cancel());
  slideInfo.getAnimations().forEach(animation => animation.cancel());
}

function turnPhoto(previous, direction) {
  const travel = direction * Math.min(200, reel.clientWidth * 0.36);
  const timing = { duration: 360, easing: "cubic-bezier(.2,.75,.22,1)" };
  const leaving = new Image();
  leaving.src = previous.src;
  leaving.alt = "";
  leaving.className = "slide-leaving";
  leaving.style.left = previous.left + "px";
  leaving.style.width = previous.width + "px";
  reel.append(leaving);
  const back = leaving.animate([
    { transform: "none", opacity: 1 },
    { transform: `translate3d(${-travel}px,0,-80px) rotateY(${direction * 9}deg)`, opacity: 0 }
  ], timing);
  back.onfinish = () => leaving.remove();
  slideOriginal.animate([
    { transform: `translate3d(${travel}px,0,-85px) rotateY(${-direction * 12}deg)`, boxShadow: "0 7px 22px #0005" },
    { transform: "none", boxShadow: "0 0 0 #0000" }
  ], timing);
  const height = reel.offsetHeight;
  if (Math.abs(height - previous.height) > 1) {
    reel.animate([{ height: previous.height + "px" }, { height: height + "px" }], timing);
  }
  slideInfo.animate([{ opacity: 0.5 }, { opacity: 1 }], { duration: 200 });
}

async function showPhoto(nextIndex, direction = 0) {
  const request = ++revision;
  requestedIndex = (nextIndex + photos.length) % photos.length;
  const photo = photos[requestedIndex];
  const thumb = photo.thumbnail;
  let preview = thumb;
  if (!thumb.complete || !thumb.naturalWidth) {
    preview = new Image();
    preview.src = thumb.src;
    try {
      await preview.decode();
    } catch {
      preview.src = photo.link.href;
      try { await preview.decode(); } catch { return; }
    }
  }
  if (request !== revision) return false;
  finishTransition();
  const previous = direction && !reducedMotion.matches && slideImage.naturalWidth ? {
    src: slideImage.currentSrc, left: slideOriginal.offsetLeft,
    width: slideOriginal.offsetWidth, height: reel.offsetHeight
  } : null;
  index = requestedIndex;
  const ratio = preview.naturalWidth / preview.naturalHeight;
  slideshow.style.setProperty("--ratio", ratio);
  previousPreview.src = photos[(index + photos.length - 1) % photos.length].thumbnail.src;
  nextPreview.src = photos[(index + 1) % photos.length].thumbnail.src;
  slideOriginal.href = photo.link.href;
  slideImage.alt = photo.alt;
  slideImage.src = preview.src;
  slidePlace.textContent = photo.place;
  slidePlace.hidden = !photo.place;
  slideCaption.textContent = photo.caption;
  slidePosition.textContent = `${index + 1} / ${photos.length}`;
  if (previous) turnPhoto(previous, direction);
  const full = new Image();
  full.src = photo.link.href;
  full.decode().then(() => {
    if (request !== revision) return;
    slideshow.style.setProperty("--ratio", full.naturalWidth / full.naturalHeight);
    slideImage.src = full.src;
  }).catch(() => {}); // Keep the preview if the original is unavailable.
  return true;
}

function setPlaying(playing) {
  clearInterval(timer);
  timer = playing ? setInterval(() => showPhoto(requestedIndex + 1, 1), 5000) : null;
  const label = playing ? "Pause slideshow" : "Play slideshow";
  playButton.setAttribute("aria-label", label);
  playButton.title = label;
  playButton.querySelector("use").setAttribute("href", "../images/gallery-controls.svg#" + (playing ? "pause" : "play"));
  slideInfo.setAttribute("aria-live", playing ? "off" : "polite");
}

function step(direction) {
  setPlaying(false);
  showPhoto(requestedIndex + direction, direction);
}

async function setSlideshow(open, focusPhoto = false) {
  if (open && !await showPhoto(index)) return;
  thumbnails.hidden = open;
  slideshow.hidden = !open;
  thumbnailButton.setAttribute("aria-pressed", String(!open));
  slideshowButton.setAttribute("aria-pressed", String(open));
  if (open) {
    slideshow.focus({ preventScroll: true });
    if (viewButtons.getBoundingClientRect().top < 0) viewButtons.scrollIntoView({ block: "start" });
  } else {
    revision++;
    finishTransition();
    setPlaying(false);
    (focusPhoto ? photos[index].link : thumbnailButton).focus();
  }
}

if (photos.length) {
  reducedMotion.addEventListener("change", () => {
    if (reducedMotion.matches) finishTransition();
  });
  viewButtons.hidden = false;
  thumbnails.classList.add("interactive");
  photos.forEach((photo, position) => {
    photo.link.addEventListener("click", event => {
      if (event.ctrlKey || event.metaKey || event.altKey || event.shiftKey || event.button !== 0) return;
      event.preventDefault();
      index = position;
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

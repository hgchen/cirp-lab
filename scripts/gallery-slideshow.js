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
    caption: figure.querySelector("figcaption")?.textContent || image.alt,
  };
});

let index = Math.max(0, photos.findIndex(photo => photo.id === location.hash.slice(1)));
let timer = null;

function showPhoto(nextIndex) {
  index = (nextIndex + photos.length) % photos.length;
  const photo = photos[index];
  const thumb = photo.thumbnail;
  const ratio = thumb.naturalWidth / thumb.naturalHeight || thumb.width / thumb.height || 4 / 3;
  slideshow.style.setProperty("--ratio", ratio);
  previousPreview.src = photos[(index + photos.length - 1) % photos.length].thumbnail.src;
  nextPreview.src = photos[(index + 1) % photos.length].thumbnail.src;
  slideOriginal.href = photo.link.href;
  slideImage.alt = photo.alt;
  slideImage.src = thumb.src;
  slideCaption.textContent = photo.caption;
  slidePosition.textContent = `${index + 1} / ${photos.length}`;
  const full = new Image();
  full.src = photo.link.href;
  full.decode().then(() => {
    if (photos[index] !== photo || slideshow.hidden) return;
    slideshow.style.setProperty("--ratio", full.naturalWidth / full.naturalHeight);
    slideImage.src = full.src;
  }).catch(() => {}); // Keep the preview if the original is unavailable.
}

function setPlaying(playing) {
  clearInterval(timer);
  timer = playing ? setInterval(() => showPhoto(index + 1), 5000) : null;
  const label = playing ? "Pause slideshow" : "Play slideshow";
  playButton.setAttribute("aria-label", label);
  playButton.title = label;
  playButton.querySelector("use").setAttribute("href", "../images/gallery-controls.svg#" + (playing ? "pause" : "play"));
  slidePosition.setAttribute("aria-live", playing ? "off" : "polite");
}

function step(direction) {
  setPlaying(false);
  showPhoto(index + direction);
}

function setSlideshow(open, focusPhoto = false) {
  thumbnails.hidden = open;
  slideshow.hidden = !open;
  thumbnailButton.setAttribute("aria-pressed", String(!open));
  slideshowButton.setAttribute("aria-pressed", String(open));
  if (open) {
    showPhoto(index);
    slideshow.focus({ preventScroll: true });
    if (viewButtons.getBoundingClientRect().top < 0) viewButtons.scrollIntoView({ block: "start" });
  } else {
    setPlaying(false);
    (focusPhoto ? photos[index].link : thumbnailButton).focus();
  }
}

if (photos.length) {
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

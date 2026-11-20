const thumbnails = document.querySelector("#gallery-thumbnails");
const slideshow = document.querySelector("#gallery-slideshow");
const thumbnailButton = document.querySelector("#show-thumbnails");
const slideshowButton = document.querySelector("#show-slideshow");
const previousButton = document.querySelector("#slide-previous");
const nextButton = document.querySelector("#slide-next");
const playButton = document.querySelector("#slide-play");
const slideImage = document.querySelector("#slide-image");
const slideCaption = document.querySelector("#slide-caption");
const slideOriginal = document.querySelector("#slide-original");
const slidePosition = document.querySelector("#slide-position");
const photos = Array.from(thumbnails.querySelectorAll("a[href]"), link => {
  const figure = link.closest("figure");
  const alt = link.querySelector("img").alt;
  return {
    id: figure?.id,
    source: link.href,
    alt,
    caption: figure?.querySelector("figcaption")?.textContent.trim() || alt,
  };
});

let index = 0;
let timer = null;

function showPhoto(nextIndex) {
  index = (nextIndex + photos.length) % photos.length;
  const photo = photos[index];
  slideOriginal.href = photo.source;
  slideImage.alt = photo.alt;
  slideImage.src = photo.source;
  slideCaption.textContent = photo.caption;
  slidePosition.textContent = `Photo ${index + 1} of ${photos.length}`;
}

function setPlaying(playing) {
  clearInterval(timer);
  timer = playing ? setInterval(() => showPhoto(index + 1), 5000) : null;
  playButton.textContent = playing ? "Pause slideshow" : "Play slideshow";
  slidePosition.setAttribute("aria-live", playing ? "off" : "polite");
}

function setSlideshow(open) {
  thumbnails.hidden = open;
  slideshow.hidden = !open;
  thumbnailButton.setAttribute("aria-pressed", String(!open));
  slideshowButton.setAttribute("aria-pressed", String(open));
  if (open) {
    showPhoto(index);
    slideshow.focus({ preventScroll: true });
  } else {
    setPlaying(false);
    thumbnailButton.focus({ preventScroll: true });
  }
}

if (photos.length) {
  const linkedPhoto = photos.findIndex(photo => photo.id === location.hash.slice(1));
  index = Math.max(0, linkedPhoto);
  document.querySelector(".gallery-view").hidden = false;
  thumbnailButton.addEventListener("click", () => setSlideshow(false));
  slideshowButton.addEventListener("click", () => setSlideshow(true));
  previousButton.addEventListener("click", () => showPhoto(index - 1));
  nextButton.addEventListener("click", () => showPhoto(index + 1));
  playButton.addEventListener("click", () => setPlaying(timer === null));
  previousButton.disabled = nextButton.disabled = playButton.disabled = photos.length < 2;

  slideshow.addEventListener("keydown", event => {
    if (event.altKey || event.ctrlKey || event.metaKey) return;
    if (event.key === "Escape") {
      event.preventDefault();
      setSlideshow(false);
    } else if (event.key === "ArrowLeft" || event.key === "ArrowRight") {
      event.preventDefault();
      showPhoto(index + (event.key === "ArrowLeft" ? -1 : 1));
    }
  });
  document.addEventListener("visibilitychange", () => {
    if (document.hidden && timer !== null) setPlaying(false);
  });
}

(() => {
  'use strict';
  const hero = document.getElementById('hero');
  const video = document.getElementById('ip-video');
  const source = video.querySelector('source');
  const playButton = document.getElementById('hero-play');
  const mobile = matchMedia('(max-width: 767px), (pointer: coarse)').matches;
  function loadPortraits() {
    document.querySelectorAll('image[data-ip-src]').forEach(image => {
      image.setAttribute('href', image.dataset.ipSrc);
      delete image.dataset.ipSrc;
    });
  }
  let visible = true, failed = false;
  let playPending = false;
  video.defaultMuted = true;
  video.muted = true;
  video.playsInline = true;
  function shouldPlay() { return visible && !document.hidden && !failed; }
  function updatePlayback() {
    if (!shouldPlay()) { video.pause(); return; }
    if (playPending || !video.paused) return;
    if (!source.hasAttribute('src')) return;
    playPending = true;
    video.play().then(() => {
      playButton.hidden = true;
      if (!shouldPlay()) video.pause();
    }).catch(error => {
      if (error.name === 'NotAllowedError' && shouldPlay()) {
        hero.dataset.media = 'blocked';
        playButton.hidden = false;
      }
    }).finally(() => { playPending = false; });
  }
  function ready() {
    if (failed) return;
    hero.dataset.media = 'ready';
    playButton.hidden = true;
  }
  function fail() {
    failed = true;
    hero.dataset.media = 'error';
    playButton.hidden = true;
  }
  video.addEventListener('playing', ready);
  video.addEventListener('canplay', updatePlayback);
  video.addEventListener('error', fail);
  source.addEventListener('error', fail);
  playButton.addEventListener('click', updatePlayback);
  // WeChat may disallow the first automatic play; retry within a user gesture.
  document.addEventListener('touchend', updatePlayback, {passive:true});
  document.addEventListener('pointerup', updatePlayback, {passive:true});
  document.addEventListener('WeixinJSBridgeReady', updatePlayback);
  new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    document.body.classList.toggle('hero-visible', entries[0].intersectionRatio > .5);
    updatePlayback();
  }, {threshold:[0,.5]}).observe(hero);
  document.addEventListener('visibilitychange', updatePlayback);
  window.addEventListener('pageshow', updatePlayback);
  // Choose once before requesting bytes, including phones held in landscape.
  function loadSource(url) {
    source.src = url;
    video.load();
    updatePlayback();
    loadPortraits();
  }
  if (mobile) {
    // This five-second loop is <600 KB. Buffer it once to avoid rebuffering
    // while the full character sheet loads over the same mobile connection.
    fetch(video.dataset.mobileSrc, {priority:'high'}).then(response => {
      if (!response.ok) throw new Error('Video request failed');
      return response.blob();
    }).then(blob => loadSource(URL.createObjectURL(blob)))
      .catch(() => loadSource(video.dataset.mobileSrc));
  } else loadSource(video.dataset.desktopSrc);
})();

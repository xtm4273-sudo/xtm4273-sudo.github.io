(() => {
  'use strict';
  const hero = document.getElementById('hero');
  const video = document.getElementById('ip-video');
  let visible = true, failed = false;
  video.muted = true;
  function updatePlayback() {
    if (failed) return;
    if (!visible || document.hidden) video.pause();
    else video.play().catch(() => {});
  }
  function ready() { if (!failed) hero.dataset.media = 'ready'; }
  function fail() {
    failed = true;
    hero.dataset.media = 'error';
  }
  video.addEventListener('loadeddata', ready);
  video.addEventListener('playing', ready);
  video.addEventListener('error', fail);
  video.querySelector('source').addEventListener('error', fail);
  new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    document.body.classList.toggle('hero-visible', entries[0].intersectionRatio > .5);
    updatePlayback();
  }, {threshold:[0,.5]}).observe(hero);
  document.addEventListener('visibilitychange', updatePlayback);
  if (video.error || video.networkState === HTMLMediaElement.NETWORK_NO_SOURCE) fail();
  else {
    if (video.readyState >= HTMLMediaElement.HAVE_CURRENT_DATA) ready();
    updatePlayback();
  }
})();

(() => {
  'use strict';
  const hero = document.getElementById('hero');
  const video = document.getElementById('ip-video');
  const source = video.querySelector('source');
  const mobile = matchMedia('(max-width: 767px), (pointer: coarse)').matches;
  const androidWeChat = /Android/i.test(navigator.userAgent) && /MicroMessenger/i.test(navigator.userAgent);
  let visible = true, playPending = false, motionMode = false, motion;
  let bytesPromise;
  video.defaultMuted = true; video.muted = true; video.playsInline = true;
  function loadPortraits() {
    document.querySelectorAll('image[data-ip-src]').forEach(image => {
      image.setAttribute('href', image.dataset.ipSrc);
      delete image.dataset.ipSrc;
    });
  }
  function getBytes() {
    if (!bytesPromise) bytesPromise = fetch(video.dataset.mobileSrc, {priority:'high'}).then(response => {
      if (!response.ok) throw new Error('Video unavailable');
      return response.arrayBuffer();
    });
    return bytesPromise;
  }
  function isVisible() { return visible && !document.hidden; }
  async function useMotion() {
    if (motionMode) return;
    motionMode = true;
    video.autoplay = false;
    video.pause();
    try {
      const {startHeroMotion} = await import('./hero-motion.js?v=wechat4');
      motion = await startHeroMotion({
        canvas:document.getElementById('hero-motion-canvas'),
        image:document.getElementById('hero-motion-image'), getBytes,
        onReady() { hero.dataset.media = 'motion'; loadPortraits(); },
        onError() { hero.dataset.media = 'error'; loadPortraits(); }
      });
      motion.setActive(isVisible());
    } catch { hero.dataset.media = 'error'; loadPortraits(); }
  }
  function updatePlayback() {
    if (motionMode) { if (motion) motion.setActive(isVisible()); return; }
    if (!isVisible()) { video.pause(); return; }
    if (playPending || !video.paused || !source.hasAttribute('src')) return;
    playPending = true;
    video.play().then(() => {
      if (!isVisible() || motionMode) video.pause();
    }).catch(error => {
      if (error.name === 'NotAllowedError' || error.name === 'NotSupportedError') useMotion();
    }).finally(() => { playPending = false; });
  }
  video.addEventListener('playing', () => {
    if (motionMode) { video.pause(); return; }
    hero.dataset.media = 'ready';
  });
  video.addEventListener('canplay', updatePlayback);
  video.addEventListener('error', useMotion);
  source.addEventListener('error', useMotion);
  new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    document.body.classList.toggle('hero-visible', entries[0].intersectionRatio > .5);
    updatePlayback();
  }, {threshold:[0,.5]}).observe(hero);
  document.addEventListener('visibilitychange', updatePlayback);
  window.addEventListener('pageshow', updatePlayback);
  window.addEventListener('pagehide', event => { if (!event.persisted && motion) motion.dispose(); });
  function loadSource(url) {
    source.src = url; video.load(); updatePlayback(); loadPortraits();
  }
  if (androidWeChat) useMotion();
  else if (mobile) getBytes().then(bytes => loadSource(URL.createObjectURL(new Blob([bytes], {type:'video/mp4'}))))
    .catch(() => loadSource(video.dataset.mobileSrc));
  else loadSource(video.dataset.desktopSrc);
})();

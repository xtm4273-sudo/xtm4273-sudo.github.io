(() => {
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('[data-work-video]').forEach(video => {
  let visible = false, motionPaused = reducedMotion.matches, playPending = false;
  async function update() {
    if (!visible || document.hidden || motionPaused) { video.pause(); return; }
    if (!video.src) { video.src = video.dataset.src; video.muted = true; video.defaultMuted = true; }
    if (!video.paused || playPending) return;
    playPending = true;
    try { await video.play(); if (!visible || document.hidden || motionPaused) video.pause(); } catch { /* Keep the poster when the browser blocks autoplay. */ }
    finally { playPending = false; }
  }
  new IntersectionObserver(entries => { visible = entries[0].isIntersecting; update(); }, {threshold:.1}).observe(video);
  document.addEventListener('visibilitychange', update);
  reducedMotion.addEventListener('change', e => { motionPaused = e.matches; update(); });
  });
  const contact = document.getElementById('contact');
  new IntersectionObserver(entries => contact.classList.toggle('is-visible', entries[0].isIntersecting)).observe(contact);
  const copy = document.querySelector('[data-copy]');
  copy.addEventListener('click', async () => {
    const status = document.querySelector('.contact-feedback');
    try { await navigator.clipboard.writeText(copy.dataset.copy); status.textContent = '微信号已复制，期待与你交流。'; }
    catch { status.textContent = '微信号：' + copy.dataset.copy + '，可长按或选中复制。'; }
  });
})();

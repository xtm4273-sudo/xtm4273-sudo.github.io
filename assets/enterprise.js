(() => {
  const links = [...document.querySelectorAll('.chapter-links a')];
  const sections = links.map(link => document.querySelector(link.getAttribute('href')));
  let scheduled = false;
  function update() {
    const offset = document.querySelector('.chapter-nav').getBoundingClientRect().bottom + 48;
    let active = 0;
    sections.forEach((section, index) => { if (section.getBoundingClientRect().top <= offset) active = index; });
    links.forEach((link, index) => { if (index === active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current'); });
    scheduled = false;
  }
  function schedule() { if (!scheduled) { scheduled = true; requestAnimationFrame(update); } }
  window.addEventListener('scroll', schedule, { passive: true });
  window.addEventListener('resize', schedule);
  update();
})();

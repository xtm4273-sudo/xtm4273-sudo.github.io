(() => {
  const cards = [...document.querySelectorAll('.project-card')];
  const desktop = matchMedia('(min-width: 768px) and (hover: hover)');
  function activate(card) {
    cards.forEach(item => {
      const selected = item === card;
      item.classList.toggle('is-active', selected);
      item.querySelector('.project-select').setAttribute('aria-expanded', String(selected));
    });
  }
  cards.forEach(card => {
    card.addEventListener('pointerenter', event => { if(desktop.matches && event.pointerType === 'mouse') activate(card); });
    card.addEventListener('focusin', event => { if(event.target.matches(':focus-visible')) activate(card); });
    const select = card.querySelector('.project-select');
    const link = card.querySelector('.project-open');
    const label = () => select.setAttribute('aria-label', `${desktop.matches ? '查看' : '展开'}${card.querySelector('.project-title').textContent}${desktop.matches ? '详情' : '简介'}`);
    label(); desktop.addEventListener('change', label);
    select.addEventListener('click', () => {
      if(desktop.matches && !document.documentElement.classList.contains('mobile-sim')) location.assign(link.href);
      else activate(card);
    });
  });
  // Native button semantics for the existing digital-persona launcher.
  const launcher = document.querySelector('#catAgent');
  launcher?.addEventListener('keydown', event => {
    if(event.key === ' ') { event.preventDefault(); launcher.click(); }
  });
})();

(() => {
  const section = document.getElementById('produtos');
  if (!section) return;
  const cards = [...section.querySelectorAll('[data-news-brand]')];
  const more = section.querySelector('.news-more');
  const status = section.querySelector('.news-status');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let expanded = false;

  const update = (animate = false) => {
    const visible = expanded ? cards : cards.slice(0, 2);
    cards.forEach(card => {
      card.getAnimations?.().forEach(animation => animation.cancel());
      card.hidden = !visible.includes(card);
    });
    section.classList.toggle('is-expanded', expanded);
    more.hidden = cards.length <= 2;
    more.setAttribute('aria-expanded', String(expanded));
    more.innerHTML = expanded ? 'Mostrar menos' : 'Ver produtos das nove marcas';
    status.textContent = `${visible.length} de ${cards.length} destaques · Fontes oficiais das marcas`;
    if (animate && !motion.matches) visible.forEach((card, index) => {
      card.animate?.([{ opacity: 0, transform: 'translateY(12px)' }, { opacity: 1, transform: 'translateY(0)' }],
        { duration: 360, delay: Math.min(index, 5) * 45, easing: 'cubic-bezier(.22,1,.36,1)', fill: 'backwards' });
    });
  };

  more.addEventListener('click', () => {
    expanded = !expanded;
    update(true);
    if (!expanded) {
      section.querySelector('.news-heading').scrollIntoView({ block: 'start', behavior: motion.matches ? 'auto' : 'smooth' });
    }
  });
  motion.addEventListener('change', () => {
    if (motion.matches) cards.forEach(card => card.getAnimations?.().forEach(animation => animation.cancel()));
  });
  update();
})();

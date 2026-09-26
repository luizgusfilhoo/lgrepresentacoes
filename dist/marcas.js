const brandSection = document.querySelector('#marcas');
const brandButtons = [...document.querySelectorAll('.brand-selectors [data-brand-id]')];
const brands = brandButtons.map(button => ({
  id: button.dataset.brandId,
  button,
  panel: document.getElementById(button.getAttribute('aria-controls')),
})).filter(brand => brand.panel);

if (brandSection && brands.length) {
  const count = brandSection.querySelector('.brand-count');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  let currentIndex = 0;

  const selectBrand = (index, { updateHash = false, focusButton = false } = {}) => {
    currentIndex = (index + brands.length) % brands.length;
    brands.forEach(({ button, panel }, position) => {
      const selected = position === currentIndex;
      button.setAttribute('aria-pressed', String(selected));
      panel.hidden = !selected;
      if (selected) panel.classList.add('is-visible');
    });
    const selected = brands[currentIndex];
    count.textContent = `${String(currentIndex + 1).padStart(2, '0')} / ${String(brands.length).padStart(2, '0')}`;
    if (updateHash || focusButton) {
      const rail = selected.button.parentElement;
      const left = selected.button.offsetLeft - rail.offsetLeft;
      const target = left - (rail.clientWidth - selected.button.offsetWidth) / 2;
      rail.scrollTo({ left: Math.max(0, target), behavior: reducedMotion.matches ? 'instant' : 'smooth' });
    }
    if (focusButton) selected.button.focus();
    if (updateHash) history.replaceState(null, '', `#marca-${selected.id}`);
  };

  const initialIndex = brands.findIndex(brand => `#marca-${brand.id}` === location.hash);
  selectBrand(initialIndex >= 0 ? initialIndex : 0);
  brandSection.classList.add('is-enhanced');
  if (initialIndex >= 0 || location.hash === '#marcas') {
    addEventListener('load', () => {
      const target = initialIndex >= 0 ? brands[initialIndex].panel : brandSection;
      requestAnimationFrame(() => requestAnimationFrame(() => {
        const previous = document.documentElement.style.scrollBehavior;
        document.documentElement.style.scrollBehavior = 'auto';
        scrollTo(0, target.getBoundingClientRect().top + scrollY - 78);
        requestAnimationFrame(() => { document.documentElement.style.scrollBehavior = previous; });
      }));
    }, { once: true });
  }

  brands.forEach(({ id, button }, index) => {
    button.addEventListener('click', () => selectBrand(index, { updateHash: true }));
    button.addEventListener('keydown', event => {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      event.preventDefault();
      selectBrand(index + (event.key === 'ArrowRight' ? 1 : -1), { updateHash: true, focusButton: true });
    });
    document.querySelectorAll(`.logo-marquee a[href="#marca-${id}"]`).forEach(link => {
      link.addEventListener('click', event => {
        event.preventDefault();
        selectBrand(index, { updateHash: true });
        brandSection.scrollIntoView({ block: 'start', behavior: reducedMotion.matches ? 'instant' : 'smooth' });
      });
    });
  });

  brandSection.querySelector('.brand-prev')?.addEventListener('click', () => selectBrand(currentIndex - 1, { updateHash: true }));
  brandSection.querySelector('.brand-next')?.addEventListener('click', () => selectBrand(currentIndex + 1, { updateHash: true }));
  addEventListener('hashchange', () => {
    const index = brands.findIndex(brand => `#marca-${brand.id}` === location.hash);
    if (index >= 0) selectBrand(index);
  });
}

const menuButton = document.querySelector('.menu-toggle');
const menu = document.querySelector('#menu');

if (menuButton && menu) {
  const closeMenu = (returnFocus = false, instant = false) => {
    menu.classList.toggle('instant', instant);
    menu.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
    if (returnFocus) menuButton.focus();
  };

  menuButton.addEventListener('click', event => {
    const isOpen = menuButton.getAttribute('aria-expanded') !== 'true';
    menu.classList.toggle('instant', event.detail === 0);
    menuButton.setAttribute('aria-expanded', String(isOpen));
    menu.classList.toggle('open', isOpen);
  });

  menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => closeMenu(false, true)));

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.classList.contains('open')) {
      closeMenu(true, true);
    }
  });

  document.addEventListener('pointerdown', event => {
    if (menu.classList.contains('open') && !event.target.closest('.header')) closeMenu(false, true);
  });
}

const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const siteHeader = document.querySelector('.header');
let headerUpdateQueued = false;
const updateHeader = () => {
  siteHeader?.classList.toggle('is-scrolled', scrollY > 16);
  headerUpdateQueued = false;
};
addEventListener('scroll', () => {
  if (!headerUpdateQueued) {
    requestAnimationFrame(updateHeader);
    headerUpdateQueued = true;
  }
}, { passive: true });
addEventListener('pageshow', updateHeader);
updateHeader();

// Reveal optional content when a visitor follows a saved product link.
const revealFragment = () => {
  let id;
  try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
  const target = document.getElementById(id);
  if (!target) return;
  let parent = target.parentElement;
  let opened = false;
  while (parent) {
    if (parent.tagName === 'DETAILS' && !parent.open) { parent.open = true; opened = true; }
    parent = parent.parentElement;
  }
  if (opened) requestAnimationFrame(() => target.scrollIntoView({ block: 'start', behavior: 'instant' }));
};
addEventListener('load', revealFragment);
addEventListener('hashchange', revealFragment);

// Reveal a few editorial blocks without hiding their readable default state.
if (!reduceMotion && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.animate?.([
        { opacity: 1, transform: 'translateY(12px)' },
        { opacity: 1, transform: 'translateY(0)' },
      ], { duration: 240, easing: 'cubic-bezier(.22,1,.36,1)' });
      observer.unobserve(entry.target);
    });
  }, { threshold: .1 });
  document.querySelectorAll('.about-grid,.service-items article,.brand-feature').forEach(element => observer.observe(element));
}

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
const tabsRail = menu?.querySelector('[data-slide-tabs]');
const tabsCursor = tabsRail?.querySelector('.slide-tabs-cursor');
const tabsLinks = tabsRail ? [...tabsRail.querySelectorAll('a')] : [];
let previewTab = null;
let cursorTarget = undefined;
const selectedTab = () => tabsLinks.find(link => link.classList.contains('active'));
const positionTabCursor = (link, instant = false) => {
  if (!tabsRail || !tabsCursor) return;
  if (!instant && link === cursorTarget) return;
  cursorTarget = link;
  if (!link || matchMedia('(max-width: 800px)').matches) {
    tabsRail.classList.remove('has-cursor');
    return;
  }

  const rail = tabsRail.getBoundingClientRect();
  const tab = link.getBoundingClientRect();
  const innerWidth = rail.width - 8;
  const left = Math.max(0, tab.left - rail.left - 4);
  const right = Math.max(0, innerWidth - left - tab.width);
  tabsRail.classList.toggle('cursor-instant', instant || reduceMotion);
  tabsCursor.style.clipPath = `inset(0 ${right}px 0 ${left}px round 999px)`;
  tabsRail.classList.add('has-cursor');
  if (instant && !reduceMotion) requestAnimationFrame(() => tabsRail.classList.remove('cursor-instant'));
};

if (tabsRail) {
  const canHover = matchMedia('(hover: hover) and (pointer: fine)');
  tabsLinks.forEach(link => {
    link.addEventListener('mouseenter', () => {
      if (!canHover.matches) return;
      previewTab = link;
      positionTabCursor(link);
    });
    link.addEventListener('focus', () => {
      previewTab = link;
      positionTabCursor(link, true);
    });
    link.addEventListener('blur', () => {
      previewTab = null;
      positionTabCursor(selectedTab(), true);
    });
  });
  tabsRail.addEventListener('mouseleave', () => {
    previewTab = null;
    positionTabCursor(selectedTab());
  });
  addEventListener('resize', () => positionTabCursor(previewTab || selectedTab(), true));
  document.fonts?.ready.then(() => positionTabCursor(previewTab || selectedTab(), true));
}

const sectionLinks = [...document.querySelectorAll('#menu a[href^="#"]')];
const sections = sectionLinks.map(link => ({ link, section: document.getElementById(link.hash.slice(1)) })).filter(item => item.section);
let navUpdateQueued = false;
const updateCurrentSection = () => {
  const position = scrollY + Math.min(innerHeight * .35, 320);
  let current = sections[0];
  sections.forEach(item => { if (item.section.offsetTop <= position) current = item; });
  sections.forEach(({ link }) => {
    const active = link === current?.link;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
  positionTabCursor(previewTab || (tabsLinks.includes(current?.link) ? current.link : null));
  navUpdateQueued = false;
};
addEventListener('scroll', () => {
  if (!navUpdateQueued) {
    requestAnimationFrame(updateCurrentSection);
    navUpdateQueued = true;
  }
}, { passive: true });
addEventListener('pageshow', updateCurrentSection);
addEventListener('hashchange', updateCurrentSection);
addEventListener('load', () => requestAnimationFrame(updateCurrentSection));
updateCurrentSection();

const marquee = document.querySelector('.logo-marquee');
const marqueeToggle = document.querySelector('.marquee-toggle');
if (marquee && marqueeToggle) {
  marqueeToggle.addEventListener('click', () => {
    const paused = marquee.classList.toggle('is-paused');
    marqueeToggle.setAttribute('aria-pressed', String(paused));
    marqueeToggle.textContent = paused ? 'Retomar movimento' : 'Pausar movimento';
  });
  if ('IntersectionObserver' in window) {
    const visibilityObserver = new IntersectionObserver(([entry]) => {
      marquee.classList.toggle('is-offscreen', !entry.isIntersecting);
    });
    visibilityObserver.observe(marquee);
  }
}

if (!reduceMotion && 'IntersectionObserver' in window) {
  const singles = document.querySelectorAll('.section-heading,.brand-feature,.about-grid,.story-main,.beliefs-head,.values-intro,.values-list article,.future-grid,.partner-heading,.hours');
  const groups = document.querySelectorAll('.logo-group:not(.logo-group-copy),.beliefs-grid,.contact-grid');
  singles.forEach(element => element.dataset.reveal = 'single');
  groups.forEach(element => element.dataset.reveal = 'stagger');

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -32px 0px' });

  document.documentElement.classList.add('motion-ready');
  document.querySelectorAll('[data-reveal]').forEach(element => observer.observe(element));

  const progress = document.createElement('div');
  progress.className = 'scroll-progress';
  progress.setAttribute('aria-hidden', 'true');
  document.body.append(progress);
  let scheduled = false;
  const updateProgress = () => {
    const range = document.documentElement.scrollHeight - innerHeight;
    progress.style.transform = `scaleX(${range > 0 ? Math.min(1, scrollY / range) : 0})`;
    scheduled = false;
  };
  addEventListener('scroll', () => {
    if (!scheduled) {
      requestAnimationFrame(updateProgress);
      scheduled = true;
    }
  }, { passive: true });
  updateProgress();
}

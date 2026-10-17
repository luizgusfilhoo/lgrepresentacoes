(() => {
  const section = document.querySelector('.showcase-section');
  if (!section) return;
  const slides = [...section.querySelectorAll('[data-showcase-brand]')];
  const stage = section.querySelector('.showcase-stage');
  const status = section.querySelector('.showcase-status');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const progress = section.querySelector('.showcase-progress span');
  const dots = [...section.querySelectorAll('[data-showcase-dot]')];
  let selected = 0;
  let timer;
  let transitionTimer;

  function finishTransition() {
    clearTimeout(transitionTimer);
    stage.classList.remove('is-transitioning', 'is-reverse');
    slides.forEach((slide, i) => {
      slide.classList.remove('slide-enter', 'slide-exit');
      slide.hidden = i !== selected;
      slide.inert = i !== selected;
      if (i === selected) slide.removeAttribute('aria-hidden');
      else slide.setAttribute('aria-hidden', 'true');
    });
  }

  function refreshAutoplay() {
    clearTimeout(timer);
    // Automatic cycling is independent of hover, focus and scroll position.
    // Reduced motion keeps the same cycle but uses instant frame changes.
    const playing = !document.hidden;
    section.classList.toggle('is-playing', playing);
    progress.style.animation = 'none';
    if (playing) {
      void progress.offsetWidth;
      progress.style.animation = '';
      timer = setTimeout(() => show(selected + 1, false), 10000);
    }
  }

  function show(index, announce = true, instant = false) {
    const next = (index + slides.length) % slides.length;
    if (next === selected) return;
    finishTransition();
    const previous = selected;
    const outgoing = slides[previous];
    const incoming = slides[next];
    if (!announce && outgoing.contains?.(document.activeElement)) {
      dots[next]?.focus({ preventScroll: true });
    }
    incoming.hidden = false;
    selected = next;
    if (motion.matches || instant) finishTransition();
    else {
      stage.classList.add('is-transitioning');
      stage.classList.toggle('is-reverse', index < previous);
      outgoing.classList.add('slide-exit');
      outgoing.inert = true;
      outgoing.setAttribute('aria-hidden', 'true');
      incoming.classList.add('slide-enter');
      incoming.inert = false;
      incoming.removeAttribute('aria-hidden');
      transitionTimer = setTimeout(finishTransition, 280);
    }
    const slide = incoming;
    status.setAttribute('aria-live', announce ? 'polite' : 'off');
    status.textContent = `${slide.getAttribute('aria-label')} · ${selected + 1} de ${slides.length}`;
    dots.forEach((dot, i) => dot.setAttribute('aria-pressed', String(i === selected)));
    refreshAutoplay();
  }

  section.querySelector('[data-showcase-prev]').addEventListener('click', event => show(selected - 1, true, event?.detail === 0));
  section.querySelector('[data-showcase-next]').addEventListener('click', event => show(selected + 1, true, event?.detail === 0));
  dots.forEach((dot, index) => dot.addEventListener('click', event => show(index, true, event?.detail === 0)));
  let swipeStart;
  let suppressSlideClick = false;
  stage.addEventListener('touchstart', event => {
    const touch = event.changedTouches[0];
    swipeStart = touch ? { x: touch.clientX, y: touch.clientY } : null;
  }, { passive: true });
  stage.addEventListener('touchend', event => {
    if (!swipeStart || !event.changedTouches[0]) return;
    const touch = event.changedTouches[0];
    const dx = touch.clientX - swipeStart.x;
    const dy = touch.clientY - swipeStart.y;
    swipeStart = null;
    if (Math.abs(dx) < 60 || Math.abs(dx) < Math.abs(dy) * 1.25) return;
    show(selected + (dx < 0 ? 1 : -1));
    suppressSlideClick = true;
    setTimeout(() => { suppressSlideClick = false; }, 450);
  }, { passive: true });
  stage.addEventListener('click', event => {
    if (!suppressSlideClick) return;
    event.preventDefault();
    suppressSlideClick = false;
  }, true);
  document.addEventListener('visibilitychange', refreshAutoplay);
  motion.addEventListener?.('change', () => {
    if (motion.matches) finishTransition();
    refreshAutoplay();
  });
  section.classList.add('is-enhanced');
  refreshAutoplay();

  const dialog = document.querySelector('.brand-video-dialog');
  const player = dialog.querySelector('.video-dialog-player');
  const external = dialog.querySelector('.video-external');
  let trigger;
  section.querySelectorAll('[data-video-id]').forEach(button => button.addEventListener('click', () => {
    const id = button.dataset.videoId;
    if (!/^[A-Za-z0-9_-]{11}$/.test(id)) return;
    trigger = button;
    external.href = `https://www.youtube.com/watch?v=${id}`;
    if (typeof dialog.showModal !== 'function') { window.open(external.href, '_blank', 'noopener'); return; }
    dialog.querySelector('#brand-video-title').textContent = button.dataset.videoTitle;
    const iframe = document.createElement('iframe');
    iframe.title = button.dataset.videoTitle;
    iframe.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0`;
    iframe.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    iframe.referrerPolicy = 'strict-origin-when-cross-origin';
    player.replaceChildren(iframe);
    dialog.showModal();
    dialog.querySelector('[data-video-close]').focus();
  }));
  dialog.querySelector('[data-video-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('close', () => {
    player.replaceChildren();
    if (trigger?.closest('[data-showcase-brand]')?.hidden) dots[selected]?.focus({ preventScroll: true });
    else trigger?.focus({ preventScroll: true });
  });
})();

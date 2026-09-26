(() => {
  const cloud = document.querySelector('#marcas-faixa');
  const track = cloud?.querySelector('.logo-track');
  const group = track?.querySelector('.logo-group:not(.logo-group-copy)');
  if (!cloud || !track || !group || matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const normalDuration = 80;
  const hoverDuration = 25;
  let width = group.getBoundingClientRect().width;
  if (!width) return;
  let position = -width;
  let speed = width / normalDuration;
  let hovering = false;
  let visible = !('IntersectionObserver' in window);
  let frame = 0;
  let previousTime = 0;
  track.style.transform = `translate3d(${position}px,0,0)`;
  cloud.classList.add('is-slider-enhanced');

  const paused = () => cloud.classList.contains('is-paused') || cloud.matches(':focus-within') || document.hidden;
  const targetSpeed = () => width / (hovering ? hoverDuration : normalDuration);
  function tick(time) {
    const elapsed = previousTime ? Math.min((time - previousTime) / 1000, 0.08) : 0;
    previousTime = time;
    speed += (targetSpeed() - speed) * (1 - Math.exp(-elapsed / 0.35));
    position += speed * elapsed;
    if (position >= 0) position -= width;
    track.style.transform = `translate3d(${position}px,0,0)`;
    frame = requestAnimationFrame(tick);
  }
  function update() {
    if (!visible || paused()) {
      cancelAnimationFrame(frame);
      frame = 0;
      previousTime = 0;
    } else if (!frame) {
      frame = requestAnimationFrame(tick);
    }
  }

  cloud.addEventListener('pointerenter', () => { hovering = true; });
  cloud.addEventListener('pointerleave', () => { hovering = false; });
  cloud.addEventListener('focusin', update);
  cloud.addEventListener('focusout', () => requestAnimationFrame(update));
  document.querySelector('.marquee-toggle')?.addEventListener('click', update);
  document.addEventListener('visibilitychange', update);
  if ('ResizeObserver' in window) {
    new ResizeObserver(() => {
      const nextWidth = group.getBoundingClientRect().width;
      if (!nextWidth || nextWidth === width) return;
      position *= nextWidth / width;
      speed *= nextWidth / width;
      width = nextWidth;
      track.style.transform = `translate3d(${position}px,0,0)`;
    }).observe(group);
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      update();
    }, { rootMargin: '150px' }).observe(cloud);
  } else update();
})();

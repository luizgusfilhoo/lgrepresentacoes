// React generates the complete markup at build time. This decorative surface has
// no client controls, so it only needs visibility control for its CSS animation.
const hero = document.querySelector<HTMLElement>("[data-geometric-hero]");
if (hero) {
  const preference = matchMedia("(prefers-reduced-motion: reduce)");
  let inView = false;
  const update = () => hero.classList.toggle("geometry-running", inView && !document.hidden && !preference.matches);
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(([entry]) => {
      inView = entry.isIntersecting;
      update();
    }, { threshold: 0.1 }).observe(hero);
  } else {
    inView = true;
    update();
  }
  preference.addEventListener("change", update);
  document.addEventListener("visibilitychange", update);
  addEventListener("pageshow", update);
}

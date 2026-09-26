(() => {
  const el = document.getElementById('caruaru-map');
  if (!el) return;
  let started = false;
  function initialize() {
    if (started) return;
    started = true;
    const script = document.createElement('script');
    script.src = './assets/vendor/leaflet/leaflet.js';
    script.onload = () => {
      if (!window.L) return;
      const canvas = document.createElement('div');
      canvas.className = 'map-canvas';
      canvas.setAttribute('aria-hidden', 'true');
      el.append(canvas);
      const center = [-8.29, -35.97];
      const map = L.map(canvas, { center, zoom: 10, scrollWheelZoom: false, dragging: true });
      L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 17,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(map);
      L.marker(center).addTo(map).bindPopup('Região de Caruaru, Pernambuco');
      map.whenReady(() => requestAnimationFrame(() => map.invalidateSize()));
    };
    document.head.append(script);
  }
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      if (entries.some(entry => entry.isIntersecting)) { observer.disconnect(); initialize(); }
    }, { rootMargin: '300px' });
    observer.observe(el);
  } else initialize();
})();

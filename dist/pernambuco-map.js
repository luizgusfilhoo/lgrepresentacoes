(() => {
  const el = document.getElementById('pernambuco-map');
  if (!el || !window.PERNAMBUCO_MAINLAND) return;

  const controls = el.querySelector('[data-map-controls]');
  const status = el.querySelector('[data-map-status]');
  const onlinePage = ['https:', 'http:'].includes(window.location.protocol);
  const scriptBase = document.currentScript?.src || window.location.href;
  let started = false;
  const reducedMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches ?? false;

  function initialize() {
    if (started) return;
    started = true;
    const script = document.createElement('script');
    script.src = new URL('assets/vendor/leaflet/leaflet.js', scriptBase).href;
    script.onload = () => {
      if (!window.L) return;
      const canvas = document.createElement('div');
      canvas.className = 'map-canvas';
      canvas.setAttribute('role', 'group');
      canvas.setAttribute('aria-label', 'Visualização do mapa de Pernambuco');
      el.append(canvas);

      try {
        const map = L.map(canvas, {
          center: [-8.4, -37.7],
          zoom: 7,
          scrollWheelZoom: false,
          zoomAnimation: !reducedMotion,
          fadeAnimation: !reducedMotion,
          attributionControl: false,
        });
        // Keep zoom buttons clear of the search panel, including narrow screens.
        map.zoomControl.setPosition('bottomright');
        const state = L.geoJSON(window.PERNAMBUCO_MAINLAND, {
          style: { color: '#829bd2', weight: 2, fillColor: '#101d90', fillOpacity: 1 },
        }).addTo(map);
        const stateBounds = state.getBounds();
        const fitState = () => map.fitBounds(stateBounds, { padding: [22, 22], maxZoom: 8 });
        fitState();
        L.control.attribution({ prefix: false }).addAttribution(
          '<a href="https://www.ibge.gov.br/geociencias/organizacao-do-territorio/malhas-territoriais.html" target="_blank" rel="noopener noreferrer">Malha: IBGE</a>'
        ).addTo(map);

        const layerButtons = el.querySelectorAll('[data-map-layer]');
        let currentTiles = null;
        let tileTimeout = null;
        let resultMarker = null;
        let lastSearchAt = 0;

        function announce(message) { if (status) status.textContent = message; }
        function markLayer(name) {
          layerButtons.forEach(button => button.setAttribute('aria-pressed', String(button.getAttribute('data-map-layer') === name)));
        }
        function removeTiles() {
          if (tileTimeout) clearTimeout(tileTimeout);
          tileTimeout = null;
          if (currentTiles) map.removeLayer(currentTiles);
          currentTiles = null;
        }
        function setLayer(name) {
          if (name !== 'outline' && !onlinePage) {
            announce('Ruas e satélite ficam disponíveis no site publicado. O contorno de Pernambuco funciona também neste arquivo.');
            return;
          }
          removeTiles();
          if (name === 'outline') {
            state.setStyle({ fillOpacity: 1 });
            fitState();
            markLayer('outline');
            announce('Contorno de Pernambuco com dados do IBGE.');
            return;
          }

          const satellite = name === 'satellite';
          const url = satellite
            ? 'https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/MODIS_Terra_CorrectedReflectance_TrueColor/default/2013-11-04/GoogleMapsCompatible_Level9/{z}/{y}/{x}.jpg'
            : 'https://tile.openstreetmap.org/{z}/{x}/{y}.png';
          const layer = L.tileLayer(url, {
            maxZoom: satellite ? 12 : 18,
            maxNativeZoom: satellite ? 9 : 18,
            tileSize: 256,
            attribution: satellite
              ? 'Imagem: NASA ESDIS GIBS, 2013'
              : '© <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener noreferrer">OpenStreetMap</a> colaboradores',
          });
          currentTiles = layer;
          let errors = 0;
          layer.on('tileload', () => {
            if (currentTiles !== layer) return;
            if (tileTimeout) clearTimeout(tileTimeout);
            tileTimeout = null;
            announce(satellite ? 'Imagem de satélite NASA de 2013.' : 'Mapa de ruas do OpenStreetMap.');
          });
          layer.on('tileerror', () => {
            if (currentTiles !== layer || ++errors < 3) return;
            setLayer('outline');
            announce('A camada online não carregou. O contorno local de Pernambuco continua disponível.');
          });
          layer.addTo(map);
          state.setStyle({ fillOpacity: .12 });
          markLayer(name);
          announce(satellite ? 'Carregando imagem de satélite NASA…' : 'Carregando ruas…');
          tileTimeout = setTimeout(() => {
            if (currentTiles !== layer) return;
            setLayer('outline');
            announce('A camada online demorou a responder. Mostrando o contorno local.');
          }, 12000);
        }

        layerButtons.forEach(button => button.addEventListener('click', () => setLayer(button.getAttribute('data-map-layer'))));

        const search = el.querySelector('[data-map-search]');
        const queryInput = el.querySelector('[data-map-query]');
        search?.addEventListener('submit', async event => {
          event.preventDefault();
          if (!onlinePage) {
            announce('A busca fica disponível no site publicado.');
            return;
          }
          const query = queryInput.value.trim();
          if (query.length < 2) {
            announce('Digite o nome de uma cidade ou lugar em Pernambuco.');
            return;
          }
          if (Date.now() - lastSearchAt < 1100) {
            announce('Aguarde um instante antes de fazer outra busca.');
            return;
          }
          lastSearchAt = Date.now();
          announce('Buscando em Pernambuco…');
          const abort = new AbortController();
          const timeout = setTimeout(() => abort.abort(), 9000);
          try {
            const url = `https://nominatim.openstreetmap.org/search?format=jsonv2&limit=1&countrycodes=br&q=${encodeURIComponent(`${query}, Pernambuco, Brasil`)}`;
            const response = await fetch(url, { signal: abort.signal });
            if (!response.ok) throw new Error('Search unavailable');
            const results = await response.json();
            const place = results[0];
            if (!place) {
              announce('Lugar não encontrado em Pernambuco. Tente outro nome.');
              return;
            }
            const lat = Number(place.lat);
            const lon = Number(place.lon);
            if (!Number.isFinite(lat) || !Number.isFinite(lon)) throw new Error('Invalid coordinates');
            if (resultMarker) map.removeLayer(resultMarker);
            resultMarker = L.circleMarker([lat, lon], { radius: 7, color: '#829bd2', weight: 3, fillColor: '#101d90', fillOpacity: 1 }).addTo(map);
            map.flyTo([lat, lon], 11, { duration: reducedMotion ? 0 : .25, animate: !reducedMotion });
            announce(`Local encontrado: ${place.display_name || query}.`);
          } catch {
            announce('Não foi possível buscar agora. Tente novamente ou abra o mapa externo.');
          } finally {
            clearTimeout(timeout);
          }
        });

        el.querySelector('[data-map-locate]')?.addEventListener('click', () => {
          if (!navigator.geolocation) {
            announce('Seu navegador não oferece acesso à localização.');
            return;
          }
          announce('Aguardando sua permissão de localização…');
          navigator.geolocation.getCurrentPosition(position => {
            const point = [position.coords.latitude, position.coords.longitude];
            if (resultMarker) map.removeLayer(resultMarker);
            resultMarker = L.circleMarker(point, { radius: 7, color: '#829bd2', weight: 3, fillColor: '#101d90', fillOpacity: 1 }).addTo(map);
            map.flyTo(point, 10, { duration: reducedMotion ? 0 : .25, animate: !reducedMotion });
            announce('Sua localização está indicada no mapa.');
          }, () => announce('Não foi possível acessar sua localização. Verifique a permissão do navegador.'), { timeout: 9000 });
        });

        map.on('click', event => {
          const { lat, lng } = event.latlng;
          if (resultMarker) map.removeLayer(resultMarker);
          resultMarker = L.circleMarker([lat, lng], { radius: 6, color: '#829bd2', weight: 2, fillColor: '#101d90', fillOpacity: 1 }).addTo(map);
          announce(`Ponto selecionado: ${lat.toFixed(4)}, ${lng.toFixed(4)}.`);
        });

        map.whenReady(() => requestAnimationFrame(() => {
          map.invalidateSize();
          el.classList.add('has-map');
          if (controls) controls.hidden = false;
          announce(onlinePage ? 'Contorno de Pernambuco. Escolha ruas ou satélite para explorar.' : 'Contorno de Pernambuco. Busca e camadas online ficam disponíveis no site publicado.');
        }));
      } catch {
        canvas.remove();
      }
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

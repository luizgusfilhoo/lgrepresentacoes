const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '..', 'pernambuco-map.js'), 'utf8');

function loadMap(protocol = 'https:') {
  const classes = new Set();
  const buttons = Object.fromEntries(['outline', 'streets', 'satellite'].map(name => [name, {
    attrs: {}, handlers: {}, setAttribute(key, value) { this.attrs[key] = value; },
    getAttribute(key) { return key === 'data-map-layer' ? name : this.attrs[key]; },
    addEventListener(event, handler) { this.handlers[event] = handler; },
    click() { this.handlers.click?.(); },
  }]));
  const status = { textContent: '' };
  const controls = { hidden: true };
  const form = { addEventListener() {} };
  const locate = { addEventListener() {} };
  const query = { value: '' };
  const selectors = {
    '[data-map-controls]': controls,
    '[data-map-status]': status,
    '[data-map-search]': form,
    '[data-map-query]': query,
    '[data-map-locate]': locate,
  };
  const mapArea = {
    classList: { add: name => classes.add(name), contains: name => classes.has(name) },
    append() {},
    querySelector: selector => selectors[selector] || buttons[selector.match(/data-map-layer="([^"]+)"/)?.[1]],
    querySelectorAll: selector => selector === '[data-map-layer]' ? Object.values(buttons) : [],
  };
  const tiles = [];
  const map = { zoomControl: { setPosition() {} }, fitBounds() {}, whenReady(fn) { fn(); }, invalidateSize() {}, removeLayer() {}, flyTo() {}, on() {} };
  const leaflet = {
    map: () => map,
    geoJSON: () => ({ addTo() { return this; }, getBounds() { return {}; }, setStyle() {} }),
    control: { attribution: () => ({ addAttribution() { return this; }, addTo() { return this; } }) },
    tileLayer(url) {
      const layer = { url, events: {}, on(event, handler) { this.events[event] = handler; return this; }, addTo() { return this; } };
      tiles.push(layer);
      return layer;
    },
  };
  let script;
  const context = {
    window: { PERNAMBUCO_MAINLAND: { type: 'FeatureCollection', features: [] }, location: { protocol, href: 'https://example.com/project/fale-conosco/' } },
    URL,
    document: {
      currentScript: { src: 'https://example.com/project/pernambuco-map.js' },
      getElementById: () => mapArea,
      createElement: tag => tag === 'script' ? (script = {}) : { className: '', setAttribute() {} },
      head: { append() {} },
    },
    requestAnimationFrame: fn => fn(),
    setTimeout: () => 1,
    clearTimeout() {},
  };
  vm.runInNewContext(source, context);
  assert.equal(typeof script.onload, 'function');
  assert.equal(script.src, 'https://example.com/project/assets/vendor/leaflet/leaflet.js');
  context.window.L = leaflet;
  context.L = leaflet;
  script.onload();
  return { buttons, classes, controls, status, tiles };
}

test('the local Pernambuco map loads without requesting remote tiles', () => {
  const view = loadMap();
  assert.equal(view.classes.has('has-map'), true);
  assert.equal(view.controls.hidden, false);
  assert.equal(view.tiles.length, 0);
});

test('street tiles load only after a visitor selects that layer', () => {
  const view = loadMap();
  view.buttons.streets.click();
  assert.equal(view.tiles.length, 1);
  assert.match(view.tiles[0].url, /tile\.openstreetmap\.org/);
});

test('offline file preview keeps the local map and explains online layers', () => {
  const view = loadMap('file:');
  view.buttons.satellite.click();
  assert.equal(view.tiles.length, 0);
  assert.match(view.status.textContent, /site publicado/i);
});

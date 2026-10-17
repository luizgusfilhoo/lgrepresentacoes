const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '..', 'showcase.js'), 'utf8');
const interactivePart = source.slice(source.indexOf('(() => {') + 8, source.indexOf('  const dialog ='));

function element(extra = {}) {
  const classes = new Set();
  return {
    events: {}, attrs: {}, hidden: false, inert: false, style: {},
    classList: {
      add(name) { classes.add(name); },
      remove(...names) { names.forEach(name => classes.delete(name)); },
      toggle(name, enabled) { if (enabled) classes.add(name); else classes.delete(name); },
    },
    addEventListener(name, handler) { this.events[name] = handler; },
    setAttribute(name, value) { this.attrs[name] = value; },
    removeAttribute(name) { delete this.attrs[name]; },
    getBoundingClientRect() { return { height: 360 }; },
    ...extra,
  };
}

function setup() {
  const brands = ['atlas', 'dryko', 'amatools'];
  const slides = brands.map(name => element({
    dataset: { showcaseBrand: name },
    getAttribute(key) { return key === 'aria-label' ? name : this.attrs[key]; },
    querySelector() { return { getAttribute: () => `./assets/institucionais/${name}.jpg` }; },
  }));
  const stage = element();
  const status = element();
  const progress = element();
  const prev = element();
  const next = element();
  const section = element({
    querySelectorAll(selector) { return selector === '[data-showcase-brand]' ? slides : []; },
    querySelector(selector) {
      return {
        '.showcase-stage': stage, '.showcase-status': status,
        '.showcase-progress span': progress,
        '[data-showcase-prev]': prev, '[data-showcase-next]': next,
      }[selector];
    },
    matches() { return false; }, contains() { return false; },
  });
  const timers = new Map();
  let timerId = 0;
  vm.runInNewContext(`(() => {${interactivePart}})()`, {
    document: { querySelector: () => section, hidden: false, activeElement: null, addEventListener() {} },
    matchMedia: () => ({ matches: true, addEventListener() {} }),
    window: {}, clearTimeout(id) { timers.delete(id); }, setTimeout(fn, ms) { const id = ++timerId; timers.set(id, { fn, ms }); return id; }, cancelAnimationFrame() {}, requestAnimationFrame() {},
  });
  return { stage, slides, status, prev, next, section, timers };
}

test('arrows cycle through all official highlights', () => {
  const { next, prev, status, slides } = setup();
  next.events.click();
  assert.equal(status.textContent, 'dryko · 2 de 3');
  assert.equal(slides[1].hidden, false);
  prev.events.click();
  assert.equal(status.textContent, 'atlas · 1 de 3');
});

test('a horizontal gesture advances without hijacking vertical scrolling', () => {
  const { stage, status } = setup();
  stage.events.touchstart({ changedTouches: [{ clientX: 220, clientY: 200 }] });
  stage.events.touchend({ changedTouches: [{ clientX: 120, clientY: 210 }] });
  assert.equal(status.textContent, 'dryko · 2 de 3');
  stage.events.touchstart({ changedTouches: [{ clientX: 220, clientY: 200 }] });
  stage.events.touchend({ changedTouches: [{ clientX: 210, clientY: 100 }] });
  assert.equal(status.textContent, 'dryko · 2 de 3');
});


test('automatic rotation continues without a pause control, including reduced motion', () => {
  const { timers, status, section } = setup();
  assert.equal(section.events.pointerenter, undefined);
  assert.equal(section.events.focusin, undefined);
  for (const expected of ['dryko · 2 de 3', 'amatools · 3 de 3', 'atlas · 1 de 3']) {
    const [id, timer] = [...timers.entries()].find(([, t]) => t.ms === 10000);
    timers.delete(id);
    timer.fn();
    assert.equal(status.textContent, expected);
  }
});

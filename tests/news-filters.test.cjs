const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function setup(reduced = false) {
  const element = (extra = {}) => ({
    attrs: {}, events: {}, hidden: false,
    setAttribute(name, value) { this.attrs[name] = value; },
    addEventListener(name, handler) { this.events[name] = handler; },
    ...extra,
  });
  let animations = 0;
  const cards = ['atlas', 'atlas', 'atlas', 'dryko', 'dryko'].map(id => element({
    dataset: { newsBrand: id }, getAnimations: () => [], animate() { animations++; },
  }));
  const more = element();
  const status = {};
  const motion = { matches: reduced, addEventListener() {} };
  const section = {
    classList: { toggle() {} },
    querySelectorAll: () => cards,
    querySelector: selector => selector === '.news-more' ? more : selector === '.news-status' ? status : { scrollIntoView() {} },
  };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '..', 'novidades.js'), 'utf8'), {
    document: { getElementById: () => section }, matchMedia: () => motion,
  });
  return { cards, more, status, animations: () => animations };
}

test('two updates are visible initially and the rest remain available', () => {
  const state = setup();
  assert.equal(state.cards.filter(card => !card.hidden).length, 2);
  assert.equal(state.more.hidden, false);
  assert.equal(state.more.attrs['aria-expanded'], 'false');
});

test('show more and collapse preserve the two-update overview', () => {
  const state = setup();
  state.more.events.click();
  assert.equal(state.cards.filter(card => !card.hidden).length, 5);
  assert.equal(state.more.attrs['aria-expanded'], 'true');
  state.more.events.click();
  assert.equal(state.cards.filter(card => !card.hidden).length, 2);
  assert.equal(state.more.attrs['aria-expanded'], 'false');
});

test('reduced motion suppresses expansion animations', () => {
  const state = setup(true);
  state.more.events.click();
  assert.equal(state.animations(), 0);
});

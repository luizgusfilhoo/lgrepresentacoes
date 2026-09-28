const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '..', 'pernambuco-map.js'), 'utf8');

test('shows the interactive map only after its tiles load', () => {
  const classes = new Set();
  const mapArea = {
    classList: {
      add: name => classes.add(name),
      contains: name => classes.has(name),
    },
    append() {},
  };
  const tileEvents = {};
  let script;
  const context = {
    window: {},
    document: {
      getElementById: () => mapArea,
      createElement: tag => tag === 'script'
        ? (script = {})
        : { className: '', setAttribute() {} },
      head: { append() {} },
    },
    requestAnimationFrame() {},
  };
  vm.runInNewContext(source, context);
  assert.equal(typeof script.onload, 'function');
  context.window.L = {
    map: () => ({ whenReady() {}, invalidateSize() {} }),
    tileLayer: () => ({
      on(event, handler) { tileEvents[event] = handler; return this; },
      addTo() { return this; },
    }),
  };
  context.L = context.window.L;
  script.onload();
  assert.equal(classes.has('has-tiles'), false, 'fallback must remain while tiles are pending');
  assert.equal(typeof tileEvents.tileload, 'function');
  tileEvents.tileload();
  assert.equal(classes.has('has-tiles'), true, 'loaded tiles replace the fallback');
});

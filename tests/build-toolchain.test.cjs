const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');

const root = path.resolve(__dirname, '..');

test('one-shot hero build does not install the vulnerable glob watcher', () => {
  const lock = JSON.parse(fs.readFileSync(path.join(root, 'package-lock.json'), 'utf8'));
  for (const name of Object.keys(lock.packages)) {
    assert.ok(!/(?:^|\/)node_modules\/(?:picomatch|@parcel\/watcher(?:-|$))/.test(name), name);
  }
});

test('one-shot hero compiler preserves scoped utilities and motion preferences', () => {
  const css = fs.readFileSync(path.join(root, 'assets/ui/hero.css'), 'utf8');
  for (const rule of ['.absolute{position:absolute}', '.relative{position:relative}',
    '.inset-0{inset:', '.overflow-hidden{overflow:hidden}', '.text-center{text-align:center}',
    '.lg-geometric-hero{', '@media (prefers-reduced-motion:reduce)']) {
    assert.ok(css.includes(rule), rule);
  }
  assert.ok(!/@(?:import|source)\s/.test(css), 'CSS directives must be compiled');
});

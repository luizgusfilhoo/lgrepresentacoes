const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');

const source = fs.readFileSync(path.join(__dirname, '..', 'main.js'), 'utf8');
const start = source.indexOf('const sectionLinks =');
const end = source.indexOf('const marquee =', start);
assert.ok(start >= 0 && end > start, 'navigation code must exist');
const navigation = source.slice(start, end);

function activeNavigationAt(scrollY) {
  const offsets = { top: 100, sobre: 2200, marcas: 1300, contato: 4900 };
  const links = Object.keys(offsets).map(id => {
    const classes = new Set();
    return {
      hash: `#${id}`,
      classList: {
        toggle(name, enabled) { if (enabled) classes.add(name); else classes.delete(name); },
        contains(name) { return classes.has(name); },
      },
      setAttribute() {},
      removeAttribute() {},
    };
  });
  const context = {
    document: {
      querySelectorAll: () => links,
      getElementById: id => ({ offsetTop: offsets[id] }),
      querySelector: () => ({ classList: { toggle() {} } }),
    },
    scrollY,
    innerHeight: 1000,
    tabsLinks: links,
    previewTab: null,
    positionTabCursor() {},
    addEventListener() {},
    requestAnimationFrame() {},
  };
  vm.runInNewContext(navigation, context);
  return links.find(link => link.classList.contains('active'))?.hash;
}

test('highlights About when it follows Representadas in page order', () => {
  assert.equal(activeNavigationAt(2200), '#sobre');
});

test('highlights Representadas while its section is visible', () => {
  assert.equal(activeNavigationAt(1300), '#marcas');
});

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '..', 'legacy-routes.js'), 'utf8');
function destination(hash) {
  let redirected = null;
  vm.runInNewContext(source, {addEventListener() {}, location: {hash, replace(value) { redirected = value; }}});
  return redirected;
}
test('old homepage bookmarks reach the new dedicated pages', () => {
  assert.equal(destination('#sobre'), './sobre-a-empresa/');
  assert.equal(destination('#cultura-lg'), './sobre-a-empresa/#cultura-lg');
  assert.equal(destination('#marcas'), './representadas/');
  assert.equal(destination('#marca-dryko'), './representadas/#marca-dryko');
  assert.equal(destination('#contato'), './fale-conosco/');
  assert.equal(destination('#pernambuco-map'), './fale-conosco/#pernambuco-map');
  assert.equal(destination('#mais-novidades'), './representadas/#produtos');
});
test('home banners and unrecognised fragments do not trigger redirects', () => {
  for (const fragment of ['', '#top', '#novidades', '#unknown', '#marca-https://example.com']) {
    assert.equal(destination(fragment), null);
  }
});
test('a legacy fragment entered after initial load also reaches its page', () => {
  let redirected;
  let hashchange;
  const location = {hash: '#novidades', replace(value) { redirected = value; }};
  vm.runInNewContext(source, {location, addEventListener(name, handler) { if (name === 'hashchange') hashchange = handler; }});
  assert.equal(redirected, undefined);
  location.hash = '#sobre';
  hashchange();
  assert.equal(redirected, './sobre-a-empresa/');
});

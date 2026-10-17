const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const test = require('node:test');
const path = require('node:path');

test('analytics measures contact intent without disclosing the commercial draft', () => {
  const source = fs.readFileSync(path.join(__dirname, '..', 'analytics.js'), 'utf8');
  let click;
  const events = [];
  vm.runInNewContext(source, {
    document: { addEventListener(name, handler) { click = handler; } },
    window: { gtag(...event) { events.push(event); } },
  });
  for (const href of [
    'https://wa.me/5581998940412?text=Nome%3A%20Pessoa%20Projeto%20privado',
    'mailto:comercial@lgrepresentacoes.com?subject=Contato&body=Projeto%20privado',
  ]) {
    click({ target: { closest() { return { href, protocol: href.startsWith('mailto:') ? 'mailto:' : 'https:' }; } } });
  }
  assert.equal(events.length, 2);
  assert.deepEqual(events.map(event => event[2].method), ['whatsapp', 'email']);
  assert.ok(events.every(event => Object.keys(event[2]).join() === 'method'));
  assert.ok(events.every(event => !JSON.stringify(event).includes('privado')));
});

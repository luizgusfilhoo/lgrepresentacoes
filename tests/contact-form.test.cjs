const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');

test('contact draft uses the selected team member and keeps personal content out of analytics', () => {
  const values = { name: { value: 'Ana & Filhos' }, company: { value: 'Atacadista' }, message: { value: 'Preciso de sprays & catálogo.' } };
  const options = [];
  const recipient = { value: '1', replaceChildren() { options.length = 0; }, add(option) { options.push(option); } };
  let submit;
  const status = {};
  const sends = [{disabled:true},{disabled:true}];
  const form = {
    hidden: true, reportValidity: () => true,
    elements: { namedItem(name) { return name === 'recipient' ? recipient : values[name]; } },
    addEventListener(name, handler) { if (name === 'submit') submit = handler; },
    querySelector() { return status; },
    querySelectorAll() { return sends; },
  };
  const cards = ['Luiz Filho', 'Luiz Gustavo'].map((name, i) => ({
    querySelector(selector) {
      if (selector === 'h4') return { textContent: name };
      return { getAttribute() { return selector.includes('mailto:') ? `mailto:pessoa${i}@example.com` : `https://wa.me/558199894041${i}`; } };
    },
  }));
  const opened = [], events = [];
  const location = {};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '..', 'contact-form.js'), 'utf8'), {
    document: { querySelector: () => form, querySelectorAll: () => cards },
    Option: function(text, value) { this.text = text; this.value = value; },
    window: { open(...args) { opened.push(args); }, gtag(...args) { events.push(args); } },
    location,
  });
  assert.ok(sends.every(button => !button.disabled));
  assert.equal(options.length, 2);
  submit({ preventDefault() {}, submitter: { value: 'whatsapp' } });
  const url = new URL(opened[0][0]);
  assert.equal(url.pathname, '/5581998940411');
  assert.ok(url.searchParams.get('text').includes('Olá, Luiz Gustavo! Sou Ana & Filhos'));
  assert.ok(url.searchParams.get('text').includes('sprays & catálogo'));
  assert.ok(url.searchParams.get('text').includes('Meu perfil é Atacadista'));
  assert.ok(!url.searchParams.get('text').includes('da empresa Atacadista'));
  assert.equal(opened[0][2], 'noopener,noreferrer');
  submit({ preventDefault() {}, submitter: { value: 'email' } });
  assert.ok(location.href.startsWith('mailto:pessoa1@example.com?'));
  assert.deepEqual(events.map(e => e[2].method), ['whatsapp', 'email']);
  assert.ok(events.every(e => Object.keys(e[2]).join() === 'method'));
  assert.ok(!JSON.stringify(events).includes('Ana'));
  values.message.value = '   ';
  submit({ preventDefault() {}, submitter: {value:'whatsapp'} });
  assert.match(status.textContent, /Preencha seu nome/);
  assert.equal(opened.length, 1);
});

(() => {
  const form = document.querySelector('[data-contact-form]');
  if (!form) return;
  const contacts = [...document.querySelectorAll('.contact-card')].map(card => ({
    name: card.querySelector('h4')?.textContent.trim(),
    whatsapp: card.querySelector('a[href^="https://wa.me/"]')?.getAttribute('href'),
    email: card.querySelector('a[href^="mailto:"]')?.getAttribute('href'),
  })).filter(contact => contact.name && /^https:\/\/wa\.me\/\d+$/.test(contact.whatsapp) && /^mailto:[^?\s]+$/.test(contact.email));
  if (!contacts.length) return;
  const recipient = form.elements.namedItem('recipient');
  recipient.replaceChildren();
  contacts.forEach((contact, index) => recipient.add(new Option(contact.name, String(index))));
  form.querySelectorAll('[data-contact-send]').forEach(button => { button.disabled = false; });
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const contact = contacts[Number(recipient.value)];
    if (!contact) return;
    const name = form.elements.namedItem('name').value.trim();
    const company = form.elements.namedItem('company').value.trim();
    const message = form.elements.namedItem('message').value.trim();
    if (!name || !message) {
      form.querySelector('[data-contact-form-status]').textContent = 'Preencha seu nome e escreva uma mensagem antes de continuar.';
      return;
    }
    const draft = `Olá, ${contact.name}! Sou ${name}${company ? `. Meu perfil é ${company}` : ''}.\n\n${message}\n\nContato pelo site da LG Representações.`;
    const email = event.submitter?.value === 'email';
    if (email) {
      location.href = `${contact.email}?subject=${encodeURIComponent('Contato comercial — LG Representações')}&body=${encodeURIComponent(draft)}`;
    } else {
      window.open(`${contact.whatsapp}?text=${encodeURIComponent(draft)}`, '_blank', 'noopener,noreferrer');
    }
    // Only the channel is measured; names and message contents never enter Analytics.
    if (typeof window.gtag === 'function') window.gtag('event', 'generate_lead', { method: email ? 'email' : 'whatsapp' });
    form.querySelector('[data-contact-form-status]').textContent = `Revise a mensagem no ${email ? 'seu aplicativo de e-mail' : 'WhatsApp'} antes de enviá-la. Se o aplicativo não abrir, use os contatos abaixo.`;
  });
})();

(() => {
  document.addEventListener('click', event => {
    if (typeof window.gtag !== 'function') return;
    const link = event.target.closest('a[href]');
    if (!link) return;
    let method;
    if (link.href.startsWith('https://wa.me/')) method = 'whatsapp';
    else if (link.protocol === 'mailto:') method = 'email';
    else return;
    // Measure the channel only; do not disclose phone numbers, emails or contact drafts.
    window.gtag('event', 'generate_lead', { method });
  });
})();

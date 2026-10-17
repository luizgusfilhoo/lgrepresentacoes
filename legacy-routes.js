// Preserve bookmarks created while all content lived on the homepage.
(() => {
  const routes = {
    '#sobre': 'sobre-a-empresa/', '#cultura-lg': 'sobre-a-empresa/#cultura-lg',
    '#marcas': 'representadas/', '#produtos': 'representadas/#produtos',
    '#mais-novidades': 'representadas/#produtos', '#contato': 'fale-conosco/',
    '#faq': 'fale-conosco/#faq', '#pernambuco-map': 'fale-conosco/#pernambuco-map',
  };
  const redirect = () => {
    const hash = location.hash;
    const destination = routes[hash] || (/^#marca-[a-z]+$/.test(hash) ? 'representadas/' + hash : null);
    if (destination) location.replace('./' + destination);
  };
  addEventListener('hashchange', redirect);
  redirect();
})();

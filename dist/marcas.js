// All nine brand records stay visible, including without JavaScript.
// A focusable anchor destination keeps quick links useful for keyboard users.
const brandPanels = [...document.querySelectorAll('.brand-feature[id]')];
brandPanels.forEach(panel => { panel.tabIndex = -1; });
addEventListener('hashchange', () => {
  const panel = brandPanels.find(item => `#${item.id}` === location.hash);
  panel?.focus({ preventScroll: true });
});

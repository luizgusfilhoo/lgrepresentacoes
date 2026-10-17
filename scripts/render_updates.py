"""Render attributed updates into the static page; usable even without JavaScript."""
import json
from html import escape
from pathlib import Path
from datetime import date
try:
    from .brand_updates import validate_data
except ImportError:
    from brand_updates import validate_data

ROOT = Path(__file__).resolve().parents[1]
START, END = '<!-- BRAND UPDATES START -->', '<!-- BRAND UPDATES END -->'
INSTAGRAM = '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/></svg>'


def render(data):
    validate_data(data)
    brands = {brand['id']: brand for brand in data['brands']}
    cards = []
    labels = {'launch': 'Lançamento', 'guide': 'Linha em destaque', 'catalog': 'Explore o catálogo'}
    # The homepage has one reviewed main line per brand. Automatically collected
    # products remain in the data file until their relevance and image are checked.
    items = [item for item in data['items'] if item['origin'] == 'editorial']
    for item in items:
        brand = brands[item['brandId']]
        social = ''
        if brand.get('instagram'):
            social = f'<a href="{escape(brand["instagram"], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Instagram de {escape(brand["name"])} (nova aba)">{INSTAGRAM}<span>Instagram</span></a>'
        checked = date.fromisoformat(item['checkedAt']).strftime('%d/%m/%Y')
        image_path = item.get('mediaPath', 'assets/' + brand['logo'])
        image_alt = item.get('mediaAlt', item['title'] + ' — ' + brand['name'])
        media = f'<a class="news-media" href="{escape(item["sourceUrl"], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Ver {escape(item["title"], quote=True)} na fonte oficial"><img src="./{escape(image_path, quote=True)}" alt="{escape(image_alt, quote=True)}" width="640" height="400" loading="lazy" decoding="async"><span aria-hidden="true">Ver na marca </span></a>'
        cards.append(f'''<article class="news-card" data-news-brand="{escape(item['brandId'])}">
  {media}
  <div class="news-card-top"><span class="news-card-logo logo-{escape(item['brandId'])}"><img src="./assets/{escape(brand['logo'])}" alt="{escape(brand['name'])}" width="112" height="56" loading="lazy"></span><span class="news-kind{' is-launch' if item['kind'] == 'launch' else ''}">{labels[item['kind']]}</span></div>
  <h3>{escape(item['title'])}</h3><p>{escape(item['summary'])}</p>
  <p class="news-meta">Fonte conferida em <time datetime="{item['checkedAt']}">{checked}</time></p>
  <a class="news-source" href="{escape(item['sourceUrl'], quote=True)}" target="_blank" rel="noopener noreferrer">Conheça na {escape(brand['name'])} <span aria-hidden="true"></span></a>
  <div class="news-card-bottom"><a href="./assets/catalogos/{escape(brand['id'])}.pdf" target="_blank" rel="noopener">Catálogo PDF <span aria-hidden="true"></span></a>{social}</div>
</article>''')
    return f'''{START}
<section class="news-section" id="produtos" aria-labelledby="news-title">
  <div class="wrap">
    <div class="news-heading"><h2 id="news-title">Produtos em destaque das representadas.</h2><p>Explore uma linha de cada marca e acesse o catálogo e a fonte oficial para conhecer os detalhes.</p></div>
    <div class="news-grid" id="news-grid">{''.join(cards)}</div>
    <div class="news-controls"><p class="news-status" role="status" aria-live="polite">{len(cards)} destaques das nossas representadas.</p><button class="news-more" type="button" aria-controls="news-grid" aria-expanded="false" hidden>Ver produtos das nove marcas <span aria-hidden="true"></span></button></div>
    <div class="news-help"><span>Gostou de uma solução?<strong>Consulte a LG sobre disponibilidade e condições.</strong></span><a href="#contato">Converse com a equipe <span aria-hidden="true"></span></a></div>
  </div>
</section>
{END}'''


if __name__ == '__main__':
    page = ROOT / 'content/representadas.html'
    content = page.read_text()
    replacement = render(json.loads((ROOT / 'data/brand-updates.json').read_text()))
    if START in content:
        before, remaining = content.split(START, 1)
        _, after = remaining.split(END, 1)
        content = before + replacement + after
    else:
        raise SystemExit('Marcadores de novidades não encontrados; página preservada.')
    page.write_text(content)
    print('Novidades renderizadas no HTML estático.')

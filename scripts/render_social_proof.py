"""Publish only approved customer evidence, never placeholder testimonials."""
import json
from html import escape
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- SOCIAL PROOF START -->'
END = '<!-- SOCIAL PROOF END -->'


def required(item, fields):
    if item.get('approved') is not True or any(not str(item.get(key, '')).strip() for key in fields):
        raise ValueError('Social proof requires complete, approved source content')
    if item.get('sourceUrl'):
        url = urlsplit(item['sourceUrl'])
        if url.scheme != 'https' or not url.hostname:
            raise ValueError('Source URL must use HTTPS')


def render(data):
    cases, reviews = data.get('cases', []), data.get('reviews', [])
    chunks = [START]
    if cases:
        cards = []
        for item in cases:
            required(item, ('client', 'sector', 'challenge', 'approach', 'result'))
            cards.append(f'''<article class="proof-card"><p class="proof-type">{escape(item['sector'])}</p><h3>{escape(item['client'])}</h3><dl><dt>Desafio</dt><dd>{escape(item['challenge'])}</dd><dt>Como atuamos</dt><dd>{escape(item['approach'])}</dd><dt>Resultado</dt><dd>{escape(item['result'])}</dd></dl></article>''')
        chunks.append(f'''<section class="proof-section" id="cases" aria-labelledby="cases-title"><div class="wrap"><p class="eyebrow">PARCERIAS EM AÇÃO</p><h2 id="cases-title">Cases de sucesso.</h2><div class="proof-grid">{''.join(cards)}</div></div></section>''')
    if reviews:
        cards = []
        for item in reviews:
            required(item, ('author', 'company', 'quote'))
            source = f'<a href="{escape(item["sourceUrl"], quote=True)}" target="_blank" rel="noopener noreferrer">Ver avaliação original </a>' if item.get('sourceUrl') else ''
            cards.append(f'''<figure class="review-card"><blockquote>{escape(item['quote'])}</blockquote><figcaption>{escape(item['author'])} · {escape(item['company'])}</figcaption>{source}</figure>''')
        chunks.append(f'''<section class="proof-section reviews-section" id="avaliacoes" aria-labelledby="reviews-title"><div class="wrap"><p class="eyebrow">A VOZ DOS CLIENTES</p><h2 id="reviews-title">Avaliações de clientes.</h2><div class="proof-grid">{''.join(cards)}</div></div></section>''')
    chunks.append(END)
    return '\n'.join(chunks)


if __name__ == '__main__':
    page = ROOT / 'content/home.html'
    text = page.read_text()
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    page.write_text(before + render(json.loads((ROOT / 'data/social-proof.json').read_text())) + after)
    print('Cases e avaliações aprovados renderizados.')

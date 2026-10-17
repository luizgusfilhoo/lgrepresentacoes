"""Build the official-media opening without third-party embeds at page load."""
import json
import re
from html import escape as esc
from pathlib import Path
from urllib.parse import urlsplit

try:
    from .brand_updates import official_url, media_url
except ImportError:
    from brand_updates import official_url, media_url

ROOT = Path(__file__).resolve().parents[1]
START, END = '<!-- BRAND SHOWCASE START -->', '<!-- BRAND SHOWCASE END -->'


def render(data):
    slides = []
    brands = {brand['id']: brand for brand in json.loads((ROOT / 'data/brand-updates.json').read_text())['brands']}
    for index, item in enumerate(data['items']):
        key = item['brandId']
        if not re.fullmatch('[a-z]+', key) or key not in brands or item['layout'] not in ('banner', 'overlay', 'split', 'frame'):
            raise ValueError('Invalid showcase entry')
        brand = brands[key]
        for color_field in ('backgroundColor', 'accentColor'):
            if not re.fullmatch(r'#[0-9a-fA-F]{6}', item.get(color_field, '')):
                raise ValueError('Invalid brand color')
        client_asset = item.get('clientAsset')
        if client_asset and (item['imageSourceUrl'] != item['sourceUrl'] or
                             not re.fullmatch(r'[0-9a-f]{64}', client_asset.get('sha256', ''))):
            raise ValueError('Invalid client supplied image')
        frame = item.get('videoFrame')
        if frame:
            if (not re.fullmatch(r'[A-Za-z0-9_-]{11}', item.get('videoId', '')) or
                    item['imageSourceUrl'] != 'https://www.youtube.com/watch?v=' + item['videoId'] or
                    not official_url(item.get('videoSourceUrl', ''), brand) or
                    type(frame.get('seconds')) not in (int, float) or frame['seconds'] < 0):
                raise ValueError('Invalid official video frame source')
        image_source_valid = bool(client_asset) or bool(frame) or media_url(item['imageSourceUrl'], brand)
        if (item['logo'] != brand['logo'] or
                not official_url(item['sourceUrl'], brand) or
                not image_source_valid or
                (item.get('mobileImage') and not media_url(item.get('mobileImageSourceUrl'), brand)) or
                (item.get('instagram') and
                 (urlsplit(item['instagram']).scheme != 'https' or urlsplit(item['instagram']).hostname != 'www.instagram.com'))):
            raise ValueError('Showcase source is not official')
        for field in ('image', 'mobileImage'):
            if item.get(field) and (not re.fullmatch(r'assets/institucionais/[a-z-]+\.(jpg|png|webp)', item[field]) or not (ROOT / item[field]).is_file()):
                raise ValueError('Missing official image')
        dimensions = ('imageWidth', 'imageHeight') + (('mobileImageWidth', 'mobileImageHeight') if item.get('mobileImage') else ())
        if any(type(item.get(field)) is not int or item[field] <= 0 for field in dimensions):
            raise ValueError('Official images need positive dimensions')
        mobile = f'<source media="(max-width:600px)" srcset="./{esc(item["mobileImage"])}" width="{item["mobileImageWidth"]}" height="{item["mobileImageHeight"]}">' if item.get('mobileImage') else ''
        loading = 'fetchpriority="high"' if index == 0 else 'loading="lazy"'
        media = f'<picture>{mobile}<img src="./{esc(item["image"])}" alt="{esc(item["imageAlt"])}" width="{item["imageWidth"]}" height="{item["imageHeight"]}" {loading} decoding="async"></picture>'
        video = ''
        if item.get('videoId'):
            if not re.fullmatch(r'[A-Za-z0-9_-]{11}', item['videoId']):
                raise ValueError('Invalid video ID')
            video = f'<button class="showcase-video" type="button" data-video-id="{item["videoId"]}" data-video-title="{esc(item["videoTitle"], quote=True)}" aria-haspopup="dialog"><span aria-hidden="true">▷</span> Assistir vídeo<span class="sr-only"> de {esc(item["name"])}</span></button>'
        social = f'<a class="showcase-social" href="{esc(item["instagram"], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Instagram de {esc(item["name"])}">Instagram </a>' if item.get('instagram') else ''
        slide_class = 'showcase-slide showcase-slide-split' if item['layout'] == 'split' else 'showcase-slide'
        slides.append(f'''<article id="destaque-{key}" class="{slide_class}" data-showcase-brand="{key}" aria-label="{esc(item['name'])}" style="--brand-surface:{item['backgroundColor']};--brand-accent:{item['accentColor']}"{'' if index == 0 else ' hidden'}>
  <a class="showcase-visual layout-{item['layout']} visual-{key}" href="{esc(item['sourceUrl'], quote=True)}" target="_blank" rel="noopener noreferrer" aria-label="Conheça {esc(item['name'])} na fonte oficial">{media}</a>
  <div class="showcase-info"><div class="showcase-identity"><span class="showcase-info-logo logo-{key}"><img src="./assets/{esc(item['logo'])}" alt="" width="100" height="44"></span><span><small>DESTAQUE DA INDÚSTRIA · {index + 1:02d}/{len(data['items']):02d}</small><strong>{esc(item['name'])}</strong></span></div><div class="showcase-info-content"><div><h2>{esc(item['title'])}</h2><p>{esc(item['description'])}</p></div><div class="showcase-actions"><a class="showcase-catalog" href="./assets/catalogos/{key}.pdf" target="_blank" rel="noopener">Ver catálogo <span aria-hidden="true"></span></a>{video}<a class="showcase-source" href="{esc(item['sourceUrl'], quote=True)}" target="_blank" rel="noopener noreferrer">Site oficial <span aria-hidden="true"></span></a>{social}</div></div></div>
</article>''')
    dots = ''.join(f'<button type="button" data-showcase-dot="{i}" aria-controls="destaque-{esc(item["brandId"])}" aria-label="Mostrar destaque de {esc(item["name"])}" aria-pressed="{"true" if i == 0 else "false"}"></button>' for i, item in enumerate(data['items']))
    return f'''{START}
<section id="novidades" class="showcase-section showcase-editorial" aria-labelledby="showcase-title">
 <div class="wrap">
  <h2 id="showcase-title" class="sr-only">Destaques das marcas representadas.</h2>
  <div class="showcase-experience"><div class="showcase-main"><div class="showcase-main-label"><span>DESTAQUE DO PORTFÓLIO</span><span>IMAGENS OFICIAIS DAS MARCAS</span></div><div class="showcase-stage">{''.join(slides)}</div>
  <div class="showcase-progress" aria-hidden="true"><span></span></div>
  <div class="showcase-navigation"><span class="showcase-status" aria-live="polite" aria-atomic="true">Atlas · 1 de {len(slides)}</span><div class="showcase-dots" role="group" aria-label="Escolher destaque">{dots}</div><div class="showcase-controls"><div class="showcase-arrows"><button type="button" data-showcase-prev aria-label="Destaque anterior">←</button><button type="button" data-showcase-next aria-label="Próximo destaque">→</button></div></div></div></div></div>
  <noscript><p>Conheça todas as marcas e seus catálogos na seção <a href="./representadas/">Representadas</a>.</p></noscript>
 </div>
</section>
<dialog class="brand-video-dialog" aria-labelledby="brand-video-title"><div class="video-dialog-heading"><h2 id="brand-video-title">Vídeo da marca</h2><button type="button" data-video-close aria-label="Fechar vídeo">✕</button></div><div class="video-dialog-player"></div><p>Vídeo do canal oficial. <a class="video-external" target="_blank" rel="noopener noreferrer">Abrir no YouTube </a></p></dialog>
{END}'''


if __name__ == '__main__':
    page = ROOT / 'content/home.html'
    content = page.read_text()
    generated = render(json.loads((ROOT / 'data/brand-showcase.json').read_text()))
    if START in content:
        before, remaining = content.split(START, 1)
        _, after = remaining.split(END, 1)
        content = before + generated + after
    else:
        raise SystemExit('Marcadores de conteúdo não encontrados; página preservada.')
    page.write_text(content)
    print('Abertura institucional renderizada com nove marcas.')

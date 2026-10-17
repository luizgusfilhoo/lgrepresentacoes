"""Compose the four static LG pages from shared chrome and content fragments."""
from html import escape, unescape
import json
from hashlib import sha256
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://luizgusfilhoo.github.io/lgrepresentacoes/'
PAGES = {
    'home': {'path': 'index.html', 'route': '', 'content': 'home.html', 'label': 'Home',
             'title': 'LG Representações | Materiais de construção em Pernambuco',
             'description': 'Há mais de 23 anos conectando indústrias a varejistas, atacadistas e distribuidores de materiais de construção em Pernambuco.'},
    'sobre': {'path': 'sobre-a-empresa/index.html', 'route': 'sobre-a-empresa/', 'content': 'sobre.html', 'label': 'Sobre a LG',
              'title': 'Sobre a LG | História, propósito e valores',
              'description': 'Conheça a história da LG Representações, fundada por Luiz Gustavo Soares Guimarães, e os valores que orientam nossa atuação em Pernambuco.'},
    'representadas': {'path': 'representadas/index.html', 'route': 'representadas/', 'content': 'representadas.html', 'label': 'Representadas',
                      'title': 'Representadas e catálogos | LG Representações',
                      'description': 'Conheça Atlas, Dryko, Amatools, Mundial Prime, Lamesa, Odem, Saga Metais, Botafogo e J. Lobato. Acesse linhas, catálogos e sites oficiais.'},
    'contato': {'path': 'fale-conosco/index.html', 'route': 'fale-conosco/', 'content': 'contato.html', 'label': 'Fale conosco',
                'title': 'Fale conosco | Equipe e atendimento LG Representações',
                'description': 'Fale com o time comercial e o escritório da LG Representações por WhatsApp ou e-mail. Consulte horários, cobertura em Pernambuco e dúvidas frequentes.'},
}


def local_link(href, key):
    prefix = './' if key == 'home' else '../'
    if href.startswith('./'):
        return prefix + href[2:]
    if not href.startswith('#'):
        return href
    anchor = href[1:]
    if anchor == 'conteudo':
        return href
    if anchor in ('top', 'novidades'):
        return ('#' + anchor) if key == 'home' else prefix + ('#novidades' if anchor == 'novidades' else '')
    if anchor == 'sobre':
        return prefix + 'sobre-a-empresa/'
    if anchor in ('cultura-lg',):
        return ('#' + anchor) if key == 'sobre' else prefix + 'sobre-a-empresa/#' + anchor
    if anchor == 'marcas' or anchor.startswith('marca-') or anchor in ('produtos', 'mais-novidades'):
        fragment = ('#' + anchor) if anchor.startswith('marca-') else ('#produtos' if anchor in ('produtos', 'mais-novidades') else '')
        return ('#marcas' if not fragment else fragment) if key == 'representadas' else prefix + 'representadas/' + fragment
    if anchor in ('contato', 'pernambuco-map', 'faq'):
        fragment = '' if anchor == 'contato' else '#' + anchor
        return ('#contato' if not fragment else fragment) if key == 'contato' else prefix + 'fale-conosco/' + fragment
    return href


def resolve(markup, key):
    # Only local URLs are rewritten; official brand URLs and mail/phone links stay intact.
    return re.sub(r'\b(href|src|srcset)="([^"]+)"',
                  lambda m: f'{m[1]}="{escape(local_link(unescape(m[2]), key), quote=True)}"', markup)


def versioned_asset(name, prefix):
    digest = sha256((ROOT/name).read_bytes()).hexdigest()[:12]
    return f'{prefix}{name}?v={digest}'


def render_page(key, page):
    prefix = './' if key == 'home' else '../'
    canonical = ORIGIN + page['route']
    links = []
    for destination, target in PAGES.items():
        current = ' class="active" aria-current="page"' if destination == key else ''
        links.append(f'<a href="{prefix + target["route"]}"{current}>{target["label"]}</a>')
    navigation = '<nav id="menu" aria-label="Navegação principal">' + ''.join(links) + '</nav>'
    header = resolve((ROOT/'templates/header.html').read_text(), key).replace('{{NAVIGATION}}', navigation)
    footer = resolve((ROOT/'templates/footer.html').read_text(), key)
    content = resolve((ROOT/'content'/page['content']).read_text(), key)
    if key == 'home':
        content = (ROOT/'content/hero.html').read_text() + content
    heading = '' if key == 'home' else f'''<section class="page-heading"><div class="wrap"><nav aria-label="Você está aqui"><a href="{prefix}">Início</a><span aria-hidden="true">/</span><span aria-current="page">{page['label']}</span></nav><h1>{'Representadas e catálogos' if key == 'representadas' else page['label']}</h1></div></section>'''
    scripts = ['main.js', 'analytics.js']
    if key == 'home': scripts += ['showcase.js']
    if key == 'representadas': scripts += ['marcas.js', 'novidades.js']
    if key == 'contato': scripts += ['contact-form.js', 'assets/pernambuco-geometry.js', 'pernambuco-map.js']
    script_tags = '\n'.join(f'<script src="{versioned_asset(name, prefix)}" defer></script>' for name in scripts)
    hero_assets = f'<link rel="stylesheet" href="{versioned_asset("assets/ui/hero.css", prefix)}"><script type="module" src="{versioned_asset("assets/ui/hero.js", prefix)}"></script>' if key == 'home' else ''
    legacy = f'<script src="{versioned_asset("legacy-routes.js", prefix)}"></script>' if key == 'home' else ''
    map_css = f'<link rel="stylesheet" href="{prefix}assets/vendor/leaflet/leaflet.css">' if key == 'contato' else ''
    organization = {'@context': 'https://schema.org', '@type': 'Organization', 'name': 'LG Representações', 'url': ORIGIN,
                    'logo': ORIGIN+'assets/lg-mark.png', 'founder': {'@type': 'Person', 'name': 'Luiz Gustavo Soares Guimarães'},
                    'areaServed': {'@type': 'AdministrativeArea', 'name': 'Pernambuco'}, 'sameAs': ['https://www.instagram.com/lg.represen/'], 'email': 'comercial@lgrepresentacoes.com'}
    breadcrumb = '' if key == 'home' else '<script type="application/ld+json">'+json.dumps({'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Início','item':ORIGIN},{'@type':'ListItem','position':2,'name':page['label'],'item':canonical}]},ensure_ascii=False)+'</script>'
    return f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{escape(page['title'])}</title><meta name="description" content="{escape(page['description'], quote=True)}"><meta name="robots" content="index,follow">
<link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:title" content="{escape(page['title'],quote=True)}"><meta property="og:description" content="{escape(page['description'],quote=True)}"><meta property="og:url" content="{canonical}">
<script type="application/ld+json">{json.dumps(organization, ensure_ascii=False)}</script>{breadcrumb}
<meta name="theme-color" content="#101d90"><link rel="icon" href="{prefix}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{prefix}assets/fonts/poppins-latin-400.woff2" as="font" type="font/woff2" crossorigin>
{legacy}<link rel="stylesheet" href="{versioned_asset("reference.css", prefix)}">{map_css}{hero_assets}
<noscript><style>.menu-toggle{{display:none}}@media(max-width:800px){{.header-inner{{flex-wrap:wrap;padding-block:14px;gap:12px}}.header nav{{display:flex;position:static;flex-wrap:wrap;width:100%;padding:0;box-shadow:none;border:0;gap:4px}}.header nav a{{width:auto;padding:8px;min-height:42px}}}}</style></noscript>
{script_tags}</head><body id="top" data-page="{key}"><a class="skip" href="#conteudo">Pular para o conteúdo</a>
{header}<main id="conteudo">{heading}{content}</main>
<aside aria-label="Contato rápido"><a class="mobile-contact-cta" href="https://wa.me/5581998940412" target="_blank" rel="noopener noreferrer" aria-label="Falar com o time comercial da LG pelo WhatsApp"><svg aria-hidden="true" fill="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/></svg><span class="floating-label">Como podemos ajudar?</span></a></aside>{footer}
</body></html>'''


def build():
    outputs = {page['path']: '\n'.join(line.rstrip() for line in render_page(key, page).splitlines()) + '\n' for key, page in PAGES.items()}
    for name, markup in outputs.items():
        dest = ROOT/name
        dest.parent.mkdir(exist_ok=True, parents=True)
        dest.write_text(markup)
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{ORIGIN + page["route"]}</loc></url>' for page in PAGES.values()) + '</urlset>\n'
    (ROOT/'sitemap.xml').write_text(sitemap)
    print('Quatro páginas LG renderizadas com navegação e metadados próprios.')


if __name__ == '__main__':
    build()

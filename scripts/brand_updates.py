"""Collect small, attributed product listings from explicitly approved public pages."""
import argparse
import hashlib
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import parse_qs, urljoin, urlsplit
from urllib.request import Request, HTTPRedirectHandler, build_opener

from lxml import html

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data/brand-updates.json'


class ApprovedRedirects(HTTPRedirectHandler):
    """Reject an unapproved destination before urllib makes that request."""
    def __init__(self, validator):
        self.validator = validator

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not self.validator(newurl):
            raise ValueError('Redirecionamento para destino não aprovado')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def open_approved(request, validator):
    if not validator(request.full_url):
        raise ValueError('Destino inicial não aprovado')
    return build_opener(ApprovedRedirects(validator)).open(request, timeout=25)


def valid_date(value):
    try:
        return isinstance(value, str) and date.fromisoformat(value).isoformat() == value
    except (ValueError, TypeError):
        return False


def official_url(value, brand):
    try:
        url = urlsplit(value)
        return url.scheme == 'https' and url.hostname in brand['allowedHosts'] and not url.username and not url.password and url.port in (None, 443)
    except (ValueError, TypeError):
        return False


def media_url(value, brand):
    return official_url(value, {'allowedHosts': brand['allowedHosts'] + brand.get('mediaHosts', [])})


def product_image(node, brand):
    for srcset in node.xpath('.//img/@srcset'):
        for candidate in srcset.split(','):
            parts = candidate.strip().rsplit(' ', 1)
            if len(parts) == 2 and parts[1] == '640w':
                url = urljoin(brand['source']['url'], parts[0])
                if media_url(url, brand):
                    return url
    images = node.xpath('.//img/@data-src | .//img/@src')
    for raw in images:
        url = urljoin(brand['source']['url'], raw)
        if '/_next/image' in url:
            url = parse_qs(urlsplit(url).query).get('url', [url])[0]
        if media_url(url, brand):
            return url
    return None


def validate_item(item, brand):
    return (item.get('brandId') == brand['id'] and
            all(isinstance(item.get(key), str) and 0 < len(item[key].strip()) <= limit
                for key, limit in [('id', 100), ('title', 180), ('summary', 450)]) and
            item.get('kind') in ('launch', 'guide', 'catalog') and
            item.get('origin') in ('editorial', 'automatic') and
            official_url(item.get('sourceUrl'), brand) and valid_date(item.get('checkedAt')) and
            (item.get('publishedAt') is None or valid_date(item['publishedAt'])) and
            (not item.get('mediaUrl') or media_url(item['mediaUrl'], brand)) and
            (not item.get('mediaPath') or bool(re.fullmatch(r'assets/(?:novidades|institucionais)/[a-z0-9-]+\.(?:png|jpg|webp)', item['mediaPath']))))


def parse_source(markup, brand, checked_at, limit=2):
    doc = html.fromstring(markup)
    source = brand['source']
    adapter = source['adapter']
    if adapter == 'mundial':
        nodes = doc.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," product-card__title-link ")]')
        candidates = []
        for node in nodes:
            card = node.xpath('ancestor::article[contains(concat(" ",normalize-space(@class)," ")," product-card ")][1]')
            candidates.append((node.get('href'), node.text_content(), product_image(card[0], brand) if card else None))
        if not doc.xpath('//h1[contains(.,"Lançamentos")]'):
            candidates = []
    elif adapter == 'botafogo':
        nodes = doc.xpath('//*[contains(@class,"vitrine-lancamento")]/following-sibling::ul[1]//a[contains(@class,"nome-produto")]')
        candidates = []
        for node in nodes:
            card = node.xpath('ancestor::div[contains(concat(" ",normalize-space(@class)," ")," listagem-item ")][1]')
            candidates.append((node.get('href'), node.text_content(), product_image(card[0], brand) if card else None))
    elif adapter == 'atlas':
        nodes = doc.xpath('//div[contains(@class,"__product-card") and not(contains(@class,"__product-card__"))]')
        candidates = []
        for node in nodes:
            link = node.xpath('.//a[contains(@class,"__product-card__link")]/@href')
            name = node.xpath('.//span[contains(@class,"__product-card__name")]/text()')
            if link and name and 'Lançamento' in node.text_content():
                candidates.append((link[0], name[0], product_image(node, brand)))
    else:
        raise ValueError('Adaptador não aprovado')
    results, seen = [], set()
    for href, title, image in candidates:
        url = urljoin(source['url'], href or '')
        title = re.sub(r'\s+', ' ', title).strip()
        if title.isupper():
            title = title.capitalize()
        item = {'id': brand['id'] + '-' + hashlib.sha256(url.encode()).hexdigest()[:12],
                'brandId': brand['id'], 'title': title, 'summary': source['summary'],
                'kind': 'launch', 'sourceUrl': url, 'checkedAt': checked_at,
                'publishedAt': None, 'origin': 'automatic'}
        if image:
            item['mediaUrl'] = image
        if url not in seen and validate_item(item, brand):
            results.append(item)
            seen.add(url)
        if limit and len(results) == limit:
            break
    if not results:
        raise ValueError('Nenhum produto válido; manter dados anteriores')
    return results


def merge_updates(previous, incoming, successful_brands):
    retained = [dict(item) for item in previous if item['origin'] == 'editorial' or item['brandId'] not in successful_brands]
    by_url = {item['sourceUrl']: item for item in retained}
    for item in incoming:
        if item['sourceUrl'] in by_url:
            by_url[item['sourceUrl']]['checkedAt'] = item['checkedAt']
            if item.get('mediaUrl'):
                by_url[item['sourceUrl']]['mediaUrl'] = item['mediaUrl']
        else:
            retained.append(item)
            by_url[item['sourceUrl']] = item
    return retained


def cache_media(item, brand):
    """Keep a local image so visitors never depend on a third-party hotlink."""
    url = item.get('mediaUrl')
    if not url or not media_url(url, brand):
        return
    request = Request(url, headers={'User-Agent': 'LGRepresentacoes/1.0'})
    with open_approved(request, lambda target: media_url(target, brand)) as response:
        if not media_url(response.url, brand):
            raise ValueError('Domínio de mídia não aprovado')
        content = response.read(4_000_001)
    if len(content) > 4_000_000:
        raise ValueError('Imagem excede 4 MB')
    extension = ('png' if content.startswith(b'\x89PNG\r\n\x1a\n') else
                 'jpg' if content.startswith(b'\xff\xd8\xff') else
                 'webp' if content.startswith(b'RIFF') and content[8:12] == b'WEBP' else None)
    if not extension:
        raise ValueError('Formato de imagem não suportado')
    relative = 'assets/novidades/' + brand['id'] + '-' + hashlib.sha256(content).hexdigest()[:16] + '.' + extension
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_bytes(content)
    item['mediaPath'] = relative


def validate_data(data):
    brands = {brand['id']: brand for brand in data['brands']}
    if len(brands) != 9:
        raise ValueError('São necessárias as nove representadas')
    seen = set()
    for item in data['items']:
        if item.get('brandId') not in brands or not validate_item(item, brands[item['brandId']]) or item['id'] in seen:
            raise ValueError('Registro inválido: ' + str(item.get('id')))
        seen.add(item['id'])
    if set(brands) != {item['brandId'] for item in data['items']}:
        raise ValueError('Uma representada está sem conteúdo')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--input-dir', type=Path, help='Reprocessar páginas oficiais previamente salvas')
    parser.add_argument('--skip-media', action='store_true', help='Validar coleta sem baixar imagens')
    args = parser.parse_args()
    data = json.loads(DATA.read_text())
    validate_data(data)
    if args.check:
        print('Conteúdo validado: nove marcas, fontes e datas consistentes.')
        return
    incoming, successful, failures = [], set(), []
    today = date.today().isoformat()
    for brand in data['brands']:
        if not brand.get('source'):
            continue
        try:
            if args.input_dir:
                markup = (args.input_dir / (brand['id'] + '.html')).read_bytes()
            else:
                request = Request(brand['source']['url'], headers={'User-Agent': 'LGRepresentacoes/1.0 (public product updates)'})
                with open_approved(request, lambda target: official_url(target, brand)) as response:
                    if not official_url(response.url, brand):
                        raise ValueError('Redirecionamento para domínio não aprovado')
                    markup = response.read(4_000_001)
                if len(markup) > 4_000_000:
                    raise ValueError('Página excedeu o limite de leitura')
            # Explicit UTF-8 avoids accent corruption on storefronts without a charset meta.
            products = parse_source(markup.decode('utf-8'), brand, today, limit=None)
            incoming.extend(products[:2])
            # Refresh existing curated products even when they are farther down the listing.
            known = {item['sourceUrl'] for item in data['items'] if item['origin'] == 'editorial'}
            incoming.extend(product for product in products[2:] if product['sourceUrl'] in known)
            successful.add(brand['id'])
            print(brand['name'] + ': fonte consultada')
        except Exception as error:
            failures.append(brand['name'])
            print('::warning::' + brand['name'] + ': ' + str(error)[:180])
    if not successful:
        raise SystemExit('Nenhuma fonte disponível. Arquivo original preservado.')
    previous = {item['sourceUrl']: item for item in data['items']}
    data['items'] = merge_updates(data['items'], incoming, successful)
    brands = {brand['id']: brand for brand in data['brands']}
    for item in data['items']:
        old_path = previous.get(item['sourceUrl'], {}).get('mediaPath')
        if old_path:
            item.setdefault('mediaPath', old_path)
        if not args.skip_media:
            try:
                cache_media(item, brands[item['brandId']])
            except Exception as error:
                print('::warning::Mídia preservada para ' + item['id'] + ': ' + str(error)[:120])
    validate_data(data)
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    if failures:
        print('Preservados os dados anteriores de: ' + ', '.join(failures))


if __name__ == '__main__':
    main()

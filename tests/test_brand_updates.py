import unittest
from unittest.mock import patch
from urllib.request import Request
from scripts.brand_updates import parse_source, validate_item, merge_updates, ApprovedRedirects, official_url


BRAND = {'id': 'mundial', 'name': 'Mundial Prime', 'allowedHosts': ['www.mundialprime.com.br'],
         'source': {'url': 'https://www.mundialprime.com.br/collections/lancamentos', 'adapter': 'mundial', 'summary': 'Conheça as aplicações e consulte as especificações da marca.'}}


def item(**changes):
    result = {'id': 'mundial-mp80', 'brandId': 'mundial', 'title': 'MP80 Antiferrugem Spray',
              'summary': 'Conheça as aplicações do produto.', 'kind': 'launch',
              'sourceUrl': 'https://www.mundialprime.com.br/products/mp80',
              'checkedAt': '2026-09-28', 'publishedAt': None, 'origin': 'automatic'}
    return dict(result, **changes)


class BrandUpdatesTests(unittest.TestCase):
    def test_redirects_are_checked_before_a_second_request_is_created(self):
        handler = ApprovedRedirects(lambda url: official_url(url, BRAND))
        request = Request(BRAND['source']['url'])
        for url in ('https://127.0.0.1/private', 'https://evil.test/', 'http://www.mundialprime.com.br/',
                    'https://www.mundialprime.com.br:8443/', 'https://name@www.mundialprime.com.br/'):
            with self.subTest(url=url), patch('urllib.request.HTTPRedirectHandler.redirect_request') as parent:
                with self.assertRaises(ValueError):
                    handler.redirect_request(request, None, 302, 'Moved', {}, url)
                parent.assert_not_called()

    def test_same_official_host_redirect_is_allowed(self):
        handler = ApprovedRedirects(lambda url: official_url(url, BRAND))
        with patch('urllib.request.HTTPRedirectHandler.redirect_request', return_value='allowed') as parent:
            self.assertEqual(handler.redirect_request(Request(BRAND['source']['url']), None, 302, 'Moved', {},
                             'https://www.mundialprime.com.br/new-path'), 'allowed')
            parent.assert_called_once()

    def test_only_official_https_urls_and_real_dates_are_accepted(self):
        self.assertTrue(validate_item(item(), BRAND))
        self.assertTrue(validate_item(item(mediaPath='assets/institucionais/mundial.jpg'), BRAND))
        for changes in ({'sourceUrl': 'https://www.mundialprime.com.br.evil.test/x'},
                        {'sourceUrl': 'javascript:alert(1)'}, {'checkedAt': '2026-02-31'},
                        {'title': ''}, {'kind': 'invented'},
                        {'mediaPath': '../../outside.png'}, {'mediaUrl': 'https://evil.test/a.png'}):
            self.assertFalse(validate_item(item(**changes), BRAND))

    def test_parser_extracts_product_links_without_prices_or_duplicates(self):
        markup = '''<h1>Lançamentos</h1><a class="product-card__title-link" href="/products/mp80">MP80 &amp; proteção</a>
        <span>R$ 20,00</span><a class="product-card__title-link" href="/products/mp80">MP80 &amp; proteção</a>
        <a class="product-card__title-link" href="https://evil.test/products/a">Outro produto</a>'''
        parsed = parse_source(markup, BRAND, '2026-09-28')
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]['title'], 'MP80 & proteção')
        self.assertEqual(parsed[0]['sourceUrl'], item()['sourceUrl'])
        self.assertIsNone(parsed[0]['publishedAt'])
        self.assertNotIn('R$', str(parsed))

    def test_changed_layout_is_not_treated_as_a_successful_empty_feed(self):
        with self.assertRaises(ValueError):
            parse_source('<h1>Site em manutenção</h1>', BRAND, '2026-09-28')

    def test_partial_failure_keeps_previous_items_and_editorial_content(self):
        editorial = item(id='manual', origin='editorial', sourceUrl='https://www.mundialprime.com.br/products/guide')
        other = item(id='atlas-old', brandId='atlas')
        fresh = item(id='new', title='Novo produto', sourceUrl='https://www.mundialprime.com.br/products/new')
        merged = merge_updates([item(), editorial, other], [fresh], {'mundial'})
        self.assertEqual({x['id'] for x in merged}, {'manual', 'atlas-old', 'new'})
        self.assertEqual(other['checkedAt'], '2026-09-28')

    def test_failure_does_not_erase_data_or_refresh_its_date(self):
        previous = [item()]
        self.assertEqual(merge_updates(previous, [], set()), previous)

    def test_product_media_is_extracted_only_from_official_hosts(self):
        markup = '''<h1>Lançamentos</h1><article class="product-card"><img src="/cdn/shop/product.jpg">
        <a class="product-card__title-link" href="/products/mp80">MP80</a></article>'''
        parsed = parse_source(markup, BRAND, '2026-09-28')
        self.assertEqual(parsed[0].get('mediaUrl'), 'https://www.mundialprime.com.br/cdn/shop/product.jpg')
        unsafe = parse_source(markup.replace('/cdn/shop/product.jpg', 'https://evil.test/x.jpg'), BRAND, '2026-09-28')
        self.assertNotIn('mediaUrl', unsafe[0])


if __name__ == '__main__':
    unittest.main()

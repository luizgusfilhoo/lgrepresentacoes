"""Dedicated pages must work on static hosting, including project subpaths."""
import json
from pathlib import Path
from urllib.parse import urlsplit, unquote
import unittest
from lxml import html
ROOT = Path(__file__).resolve().parents[1]
PATHS = ['index.html', 'sobre-a-empresa/index.html', 'representadas/index.html', 'fale-conosco/index.html']
class MultipageTests(unittest.TestCase):
    def test_local_assets_links_and_fragments_resolve_on_all_pages(self):
        for name in PATHS:
            page = html.fromstring((ROOT/name).read_text())
            for ref in page.xpath('//a/@href | //script/@src | //link/@href | //img/@src | //source/@srcset'):
                url = urlsplit(ref)
                if url.scheme or url.netloc: continue
                target = ((ROOT/name).parent / unquote(url.path)).resolve() if url.path else ROOT/name
                if target.is_dir(): target /= 'index.html'
                with self.subTest(page=name, ref=ref):
                    self.assertTrue(target.is_file(), str(target))
                    if url.fragment and target.suffix == '.html':
                        dest = html.fromstring(target.read_text())
                        self.assertTrue(dest.xpath('//*[@id=$value]', value=unquote(url.fragment)), ref)

    def test_unique_metadata_and_exactly_one_current_navigation_item(self):
        titles, descriptions, canonicals = [], [], []
        for name in PATHS:
            page = html.fromstring((ROOT/name).read_text())
            titles += page.xpath('//title/text()')
            descriptions += page.xpath('//meta[@name="description"]/@content')
            canonicals += page.xpath('//link[@rel="canonical"]/@href')
            self.assertEqual(len(page.xpath('//h1')), 1)
            current = page.xpath('//nav[@id="menu"]/a[@aria-current="page"]')
            self.assertEqual(len(current), 1)
            self.assertIn('active', current[0].get('class'))
            for script in page.xpath('//script[@type="application/ld+json"]/text()'): json.loads(script)
        for values in (titles, descriptions, canonicals): self.assertEqual(len(set(values)), 4)

    def test_requested_visual_cleanup_is_shared(self):
        for name in PATHS:
            page = html.fromstring((ROOT/name).read_text())
            self.assertFalse(page.xpath('//a[contains(@class,"topbar-phone")]'))
            floating = page.xpath('//a[contains(@class,"mobile-contact-cta")]/svg')[0]
            self.assertEqual(floating.get('fill'), 'currentColor')
            self.assertTrue(floating.xpath('.//path/@d'))
            for link in page.xpath('//a'): self.assertNotIn('↗', link.text_content())
        about = html.fromstring((ROOT/'sobre-a-empresa/index.html').read_text())
        self.assertTrue(about.xpath('//figcaption')[0].text_content().strip().startswith('*'))

    def test_pages_keep_their_own_content_and_do_not_repeat_brand_catalogues(self):
        home, about, brands, contact = [html.fromstring((ROOT/name).read_text()) for name in PATHS]
        self.assertFalse(home.xpath('//*[@id="marcas" or @id="cultura-lg" or @id="contato" or @id="faq"]'))
        self.assertTrue(about.xpath('//*[@id="cultura-lg"]'))
        self.assertEqual(len(brands.xpath('//article[contains(@class,"brand-feature")]')), 9)
        self.assertTrue(contact.xpath('//*[@id="pernambuco-map"]'))
        self.assertEqual(len(contact.xpath('//section[@id="faq"]//details')), 5)
        self.assertFalse(contact.xpath('//*[@id="marcas"]'))

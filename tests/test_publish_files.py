"""GitHub Pages deploy metadata and local mirror are complete."""
from pathlib import Path
from urllib.parse import urlsplit
import unittest
from lxml import html

ROOT = Path(__file__).resolve().parents[1]

class PublishTests(unittest.TestCase):
    def test_decorative_hero_does_not_ship_a_full_framework_runtime(self):
        self.assertLess((ROOT/'assets/ui/hero.js').stat().st_size, 5_000)

    def test_contact_form_reserves_its_layout_before_scripts_load(self):
        page = html.fromstring((ROOT/'fale-conosco/index.html').read_text())
        form = page.xpath('//form[@data-contact-form]')[0]
        self.assertIsNone(form.get('hidden'))
        self.assertEqual(len(form.xpath('.//select[@name="recipient"]/option')), 5)
        self.assertEqual(len(form.xpath('.//button[@data-contact-send and @disabled]')), 2)

    def test_search_metadata_and_redirect(self):
        page = html.fromstring((ROOT/'index.html').read_text())
        self.assertFalse(page.xpath('//meta[@name="robots" and contains(@content,"noindex")]'))
        self.assertEqual(page.xpath('//link[@rel="canonical"]/@href'), ['https://luizgusfilhoo.github.io/lgrepresentacoes/'])
        self.assertIn('Allow: /', (ROOT/'robots.txt').read_text())
        redirect = (ROOT/'sobre/index.html').read_text()
        self.assertIn('../sobre-a-empresa/', redirect)
        self.assertNotIn('noindex', redirect)

    def test_map_styles_are_fresh_and_positioned(self):
        page = html.fromstring((ROOT/'index.html').read_text())
        self.assertEqual(page.xpath('//link[contains(@href,"reference.css?")]/@rel'), ['stylesheet'])
        css = (ROOT/'reference.css').read_text()
        self.assertIn('.pernambuco-map{position:relative', css)
        self.assertIn('.map-canvas{position:absolute', css)

    def test_local_references_and_dist_match(self):
        page = html.fromstring((ROOT/'index.html').read_text())
        for ref in page.xpath('//script/@src | //link/@href | //img/@src | //a/@href'):
            if not ref.startswith('./'): continue
            item = ROOT/urlsplit(ref).path[2:]
            with self.subTest(ref=ref):
                self.assertTrue(item.exists())
                self.assertTrue((ROOT/'dist'/urlsplit(ref).path[2:]).exists())
        for item in ('index.html','404.html','analytics.js','reference.css','style.css','main.js','marcas.js','pernambuco-map.js','robots.txt','sobre/index.html','sobre-a-empresa/index.html','representadas/index.html','fale-conosco/index.html','legacy-routes.js','assets/vendor/leaflet/leaflet.js','assets/vendor/leaflet/leaflet.css'):
            with self.subTest(item=item):
                self.assertEqual((ROOT/item).read_bytes(), (ROOT/'dist'/item).read_bytes())

if __name__ == '__main__': unittest.main()

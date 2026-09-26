"""GitHub Pages deploy metadata and local mirror are complete."""
from pathlib import Path
from urllib.parse import urlsplit
import unittest
from lxml import html

ROOT = Path(__file__).resolve().parents[1]

class PublishTests(unittest.TestCase):
    def test_search_metadata_and_redirect(self):
        page = html.fromstring((ROOT/'index.html').read_text())
        self.assertFalse(page.xpath('//meta[@name="robots" and contains(@content,"noindex")]'))
        self.assertEqual(page.xpath('//link[@rel="canonical"]/@href'), ['https://luizgusfilhoo.github.io/lgrepresentacoes/'])
        self.assertIn('Allow: /', (ROOT/'robots.txt').read_text())
        redirect = (ROOT/'sobre/index.html').read_text()
        self.assertIn('../#sobre', redirect)
        self.assertNotIn('noindex', redirect)

    def test_map_styles_are_fresh_and_positioned(self):
        page = html.fromstring((ROOT/'index.html').read_text())
        self.assertEqual(page.xpath('//link[contains(@href,"style.css?")]/@rel'), ['stylesheet'])
        css = (ROOT/'style.css').read_text()
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
        for item in ('index.html','style.css','main.js','marcas.js','pernambuco-map.js','robots.txt','sobre/index.html','assets/vendor/leaflet/leaflet.js','assets/vendor/leaflet/leaflet.css'):
            with self.subTest(item=item):
                self.assertEqual((ROOT/item).read_bytes(), (ROOT/'dist'/item).read_bytes())

if __name__ == '__main__': unittest.main()

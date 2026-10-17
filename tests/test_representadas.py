"""The nine represented brands must keep their own assets and destinations."""

from pathlib import Path
import unittest

from lxml import html


ROOT = Path(__file__).resolve().parents[1]
BRANDS = [
    ("atlas", "Atlas", "atlas.png", "https://site.atlas.com.br/pt", "atlas.pdf"),
    ("dryko", "Dryko", "dryko.png", "https://dryko.com.br/", "dryko.pdf"),
    ("amatools", "Amatools", "amatools.png", "https://amatools.com.br/", "amatools.pdf"),
    ("mundial", "Mundial Prime", "mundial.png", "https://www.mundialprime.com.br/", "mundial.pdf"),
    ("lamesa", "Lamesa", "lamesa.png", "https://www.lamesa.com.br/", "lamesa.pdf"),
    ("odem", "Odem", "odem.png", "https://odem.com.br/", "odem.pdf"),
    ("saga", "Saga Metais", "saga.png", "https://sagametais.com.br/sobreaempresa/", "saga.pdf"),
    ("botafogo", "Botafogo", "botafogo.png", "https://www.lojabtf.com.br/", "botafogo.pdf"),
    ("jlobato", "J. Lobato", "jlobato-nova.png", "https://www.jlobato.com.br/", "jlobato.pdf"),
]


class RepresentadasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = html.fromstring((ROOT / "representadas/index.html").read_text(encoding="utf-8"))

    def test_panels_are_in_approved_order_with_complete_content(self):
        panels = self.page.xpath('//section[@id="marcas"]//article[contains(@class,"brand-feature")]')
        self.assertEqual([panel.get("id") for panel in panels], [f"marca-{b[0]}" for b in BRANDS])
        for panel, (_, name, logo, site, catalog) in zip(panels, BRANDS):
            with self.subTest(brand=name):
                self.assertEqual(panel.xpath('normalize-space(.//h3)'), name)
                self.assertGreater(len(panel.xpath('normalize-space(.//div[contains(@class,"brand-feature-body")]/p[not(contains(@class,"brand-category"))])')), 30)
                logo_src = panel.xpath('.//div[contains(@class,"brand-feature-media")]//img[contains(@class,"brand-logo")]/@src')
                self.assertEqual(logo_src, [f"../assets/{logo}"])
                self.assertTrue((ROOT / "representadas" / logo_src[0]).is_file())
                self.assertEqual(panel.xpath('.//img[contains(@class,"brand-product")]'), [])
                self.assertIn(site, panel.xpath('.//a/@href'))
                pdf = f"../assets/catalogos/{catalog}"
                self.assertIn(pdf, panel.xpath('.//a/@href'))
                self.assertTrue((ROOT / "representadas" / pdf).is_file())

    def test_quick_links_reach_every_visible_brand_without_a_script(self):
        home = html.fromstring((ROOT / 'index.html').read_text())
        links = home.xpath('//nav[@aria-label="Acesso rápido às representadas"]/a')
        self.assertEqual([link.get("href") for link in links], [f"./representadas/#marca-{b[0]}" for b in BRANDS])
        for link, (_, name, logo, _, _) in zip(links, BRANDS):
            with self.subTest(brand=name):
                self.assertTrue(link.get("aria-label"))
                self.assertEqual(link.xpath('.//img/@src'), [f"./assets/{logo}"])
                self.assertEqual(link.xpath('.//img/@alt'), [name])
        panels = self.page.xpath('//section[@id="marcas"]//article[contains(@class,"brand-feature")]')
        self.assertTrue(all(panel.get("hidden") is None for panel in panels))
        self.assertNotIn('panel.hidden', (ROOT / 'marcas.js').read_text())

    def test_logo_art_is_not_cropped_or_recolored(self):
        css = (ROOT / "reference.css").read_text(encoding="utf-8")
        self.assertIn(".brand-feature-media>.brand-logo", css)
        self.assertIn("object-fit:contain", css)
        self.assertNotIn("brand-product", css)

    def test_portfolio_uses_one_brand_navigation_without_marquee(self):
        self.assertEqual(
            self.page.xpath('//section[@id="marcas"]//*[@aria-label="Marcas representadas em movimento"]'),
            [],
        )
        self.assertFalse(self.page.xpath('//*[@class="brand-selectors"]'))
        self.assertFalse(self.page.xpath('//nav[@aria-label="Acesso rápido às representadas"]'))


if __name__ == "__main__":
    unittest.main()

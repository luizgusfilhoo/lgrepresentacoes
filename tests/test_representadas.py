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
        cls.page = html.fromstring((ROOT / "index.html").read_text(encoding="utf-8"))

    def test_panels_are_in_approved_order_with_complete_content(self):
        panels = self.page.xpath('//section[@id="marcas"]//article[contains(@class,"brand-feature")]')
        self.assertEqual([panel.get("id") for panel in panels], [f"marca-{b[0]}" for b in BRANDS])
        for panel, (_, name, logo, site, catalog) in zip(panels, BRANDS):
            with self.subTest(brand=name):
                self.assertEqual(panel.xpath('normalize-space(.//h3)'), name)
                self.assertGreater(len(panel.xpath('normalize-space(.//div[contains(@class,"brand-feature-body")]/p[not(contains(@class,"brand-category"))])')), 30)
                logo_src = panel.xpath('.//div[contains(@class,"brand-feature-media")]//img[contains(@class,"brand-logo")]/@src')
                self.assertEqual(logo_src, [f"./assets/{logo}"])
                self.assertTrue((ROOT / logo_src[0]).is_file())
                self.assertEqual(panel.xpath('.//img[contains(@class,"brand-product")]'), [])
                self.assertIn(site, panel.xpath('.//a/@href'))
                pdf = f"./assets/catalogos/{catalog}"
                self.assertIn(pdf, panel.xpath('.//a/@href'))
                self.assertTrue((ROOT / pdf).is_file())

    def test_ribbon_and_selection_are_accessible(self):
        ribbon = self.page.xpath('//*[@id="marcas-faixa"]')[0]
        visible_group = ribbon.xpath('.//*[contains(@class,"logo-group") and not(contains(@class,"copy"))]')[0]
        self.assertEqual(visible_group.xpath('.//a/@href'), [f"#marca-{b[0]}" for b in BRANDS])
        self.assertEqual(len(ribbon.xpath('.//*[contains(@class,"logo-group-copy") and @aria-hidden="true"]')), 1)
        self.assertEqual(len(self.page.xpath('//button[contains(@class,"marquee-toggle") and @aria-controls="marcas-faixa"]')), 1)
        selectors = self.page.xpath('//*[@aria-label="Selecionar representada"]//button')
        self.assertEqual([b.get("aria-controls") for b in selectors], [f"marca-{b[0]}" for b in BRANDS])
        self.assertTrue(all(b.get("aria-label") for b in selectors))
        for button, (_, name, logo, _, _) in zip(selectors, BRANDS):
            with self.subTest(selector=name):
                self.assertEqual(button.xpath('.//span[contains(@class,"selector-name")]/text()'), [name])
                self.assertEqual(button.xpath('.//span[contains(@class,"selector-logo")]//img/@src'), [f"./assets/{logo}"])
                self.assertEqual(button.xpath('.//span[contains(@class,"selector-logo")]//img/@alt'), [''])
        self.assertFalse(self.page.xpath('//article[contains(@class,"brand-feature")]//h3//img'))
        for label in ("Representada anterior", "Próxima representada"):
            self.assertEqual(len(self.page.xpath(f'//button[@aria-label="{label}"]')), 1)
        self.assertIn('src="./marcas.js"', (ROOT / "index.html").read_text(encoding="utf-8"))

    def test_logo_art_is_not_cropped_or_recolored(self):
        css = (ROOT / "style.css").read_text(encoding="utf-8")
        self.assertIn(".brand-feature-media>.brand-logo", css)
        self.assertIn("object-fit:contain", css)
        self.assertNotIn("brand-product", css)


if __name__ == "__main__":
    unittest.main()

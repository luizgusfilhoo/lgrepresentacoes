"""Content contracts for the first homepage presentation model."""

from pathlib import Path
import unittest

from lxml import html


ROOT = Path(__file__).resolve().parents[1]


class HomePresentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = html.fromstring((ROOT / "index.html").read_text(encoding="utf-8"))

    def test_navigation_reaches_every_primary_section(self):
        links = self.page.xpath('//nav[@aria-label="Navegação principal"]//a/@href')
        self.assertEqual(set(links), {"#top", "#sobre", "#marcas", "#contato"})
        for target in links:
            self.assertEqual(len(self.page.xpath(f'//*[@id="{target[1:]}"]')), 1)

    def test_hero_has_one_heading_and_direct_actions(self):
        hero = self.page.xpath('//section[@id="top"]')[0]
        self.assertEqual(len(hero.xpath('.//h1')), 1)
        self.assertEqual(
            hero.xpath('.//*[contains(concat(" ", normalize-space(@class), " "), " hero-actions ")]/a/@href'),
            ["#marcas", "#contato"],
        )
        self.assertEqual(len(hero.xpath('.//img[contains(@class, "hero-photo")]')), 1)

    def test_indicators_have_approved_values_and_labels(self):
        stats = self.page.xpath('//section[@aria-label="Números da LG Representações"]//*[contains(concat(" ", normalize-space(@class), " "), " stat ")]')
        self.assertEqual(
            [(s.xpath('normalize-space(./strong)'), s.xpath('normalize-space(./p)')) for s in stats],
            [
                ("23+", "Anos de mercado"),
                ("+200", "Clientes em carteira"),
                ("+220 mil", "Obras abastecidas"),
                ("+25 mil", "Negociações concluídas"),
            ],
        )

    def test_instagram_has_an_accessible_destination(self):
        links = self.page.xpath('//a[@href="https://www.instagram.com/lg.represen/"]')
        self.assertGreaterEqual(len(links), 1)
        self.assertTrue(any(link.get("aria-label") or link.text_content().strip() for link in links))
        self.assertTrue(any(link.xpath('.//svg') for link in links))

    def test_headings_and_body_share_manrope(self):
        css = (ROOT / "style.css").read_text(encoding="utf-8")
        self.assertIn("--display:Manrope", css)
        self.assertIn("--body:Manrope", css)


if __name__ == "__main__":
    unittest.main()

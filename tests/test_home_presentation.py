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
        self.assertEqual(set(links), {"./", "./sobre-a-empresa/", "./representadas/", "./fale-conosco/"})
        for target in links:
            self.assertTrue((ROOT / target / "index.html").is_file())

    def test_official_brand_media_is_the_first_content(self):
        first = self.page.get_element_by_id("novidades")
        self.assertEqual(first.get('id'), 'novidades')
        self.assertEqual(len(self.page.xpath('//h1')), 1)
        slides = first.xpath('.//article[@data-showcase-brand]')
        self.assertEqual(len(slides), 9)
        for slide in slides:
            image = slide.xpath('.//picture//img')[0]
            self.assertTrue((ROOT / image.get('src')).is_file())
            self.assertTrue(image.get('alt'))
        videos = first.xpath('.//button[@data-video-id]')
        self.assertGreaterEqual(len(videos), 5)
        self.assertFalse(self.page.xpath('//iframe[@src] | //video[@autoplay]'))

    def test_home_keeps_only_brand_overview_and_about_preview(self):
        self.assertEqual(self.page.xpath('//nav[@id="menu"]//a/@href')[0], './')
        self.assertFalse(self.page.xpath('//*[@id="produtos" or @id="cultura-lg" or @id="marcas" or @id="contato"]'))
        self.assertEqual(len(self.page.xpath('//nav[@aria-label="Acesso rápido às representadas"]/a')), 9)

    def test_about_invitation_and_showcase_motion_controls(self):
        invitation = self.page.xpath('//div[contains(@class,"home-about-action")]/a')[0]
        self.assertIn('Clique aqui para ver mais', invitation.text_content())
        self.assertEqual(invitation.get('href'), './sobre-a-empresa/')
        self.assertFalse(self.page.xpath('//*[@data-showcase-play]'))
        self.assertEqual(len(self.page.xpath('//*[@data-showcase-select]')), 0)

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

    def test_reference_type_is_self_hosted_and_used_by_the_page(self):
        css = (ROOT / "reference.css").read_text(encoding="utf-8")
        self.assertIn("--display:Poppins", css)
        self.assertIn("--body:Poppins", css)
        self.assertFalse(self.page.xpath('//link[contains(@href,"fonts.googleapis.com")]'))
        self.assertEqual(len(self.page.xpath('//link[contains(@href,"reference.css")]')), 1)
        for weight in (400, 500, 600, 700):
            self.assertTrue((ROOT / f"assets/fonts/poppins-latin-{weight}.woff2").is_file())

    def test_no_excluded_sections_or_reference_company_data(self):
        text = self.page.text_content().lower()
        for excluded in ("regis@", "cascavel", "promotores", "fotos e vídeos"):
            self.assertNotIn(excluded, text)
        self.assertEqual(len(self.page.xpath('//*[contains(@class,"service-items")]/article')), 3)


if __name__ == "__main__":
    unittest.main()

"""Conversion and search pages remain useful without JavaScript."""
from pathlib import Path
import unittest

from lxml import html

ROOT = Path(__file__).resolve().parents[1]


class ConversionSeoTests(unittest.TestCase):
    def test_home_has_clear_ctas_and_five_answers(self):
        page = html.fromstring((ROOT / 'index.html').read_text())
        self.assertEqual(len(page.xpath('//section[@data-geometric-hero]//a[@href="./fale-conosco/"]')), 1)
        self.assertEqual(len(page.xpath('//a[contains(@class,"mobile-contact-cta")]')), 1)
        self.assertEqual(len(html.fromstring((ROOT / 'fale-conosco/index.html').read_text()).xpath('//section[@id="faq"]//details')), 5)
        self.assertFalse(page.xpath('//nav[@aria-label="Você está aqui"]'))

    def test_404_and_redirect_have_distinct_metadata(self):
        pages = [html.fromstring((ROOT / path).read_text()) for path in ('index.html', '404.html', 'sobre/index.html')]
        titles = [page.xpath('normalize-space(//title)') for page in pages]
        descriptions = [page.xpath('string(//meta[@name="description"]/@content)') for page in pages]
        self.assertEqual(len(set(titles)), 3)
        self.assertEqual(len(set(descriptions)), 3)
        self.assertTrue(all(descriptions))
        self.assertIn('noindex', pages[1].xpath('string(//meta[@name="robots"]/@content)'))
        self.assertIn('Página não encontrada', pages[1].text_content())

    def test_all_images_have_a_text_alternative(self):
        page = html.fromstring((ROOT / 'index.html').read_text())
        self.assertFalse([image.get('src') for image in page.xpath('//img') if image.get('alt') is None])
        self.assertIn('Sitemap:', (ROOT / 'robots.txt').read_text())


if __name__ == '__main__':
    unittest.main()

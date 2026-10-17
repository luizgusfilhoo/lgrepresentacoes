"""The opening must use media traceable to the represented industries."""
import copy
import json
from pathlib import Path
import unittest
from lxml import html

from scripts.render_showcase import render


ROOT = Path(__file__).resolve().parents[1]


class ShowcaseSourcesTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / 'data/brand-showcase.json').read_text())

    def test_all_nine_brands_have_local_official_images(self):
        brands = {brand['id'] for brand in json.loads((ROOT / 'data/brand-updates.json').read_text())['brands']}
        self.assertEqual({item['brandId'] for item in self.data['items']}, brands)
        self.assertEqual(len(self.data['items']), len(brands))
        self.assertIn('showcase-slide', render(self.data))

    def test_unverified_media_host_is_rejected(self):
        unsafe = copy.deepcopy(self.data)
        unsafe['items'][0]['imageSourceUrl'] = 'https://site.atlas.com.br.evil.example/photo.jpg'
        with self.assertRaises(ValueError):
            render(unsafe)

    def test_video_stills_match_the_linked_official_video(self):
        for item in self.data['items']:
            if not item.get('videoFrame'): continue
            self.assertEqual(item['imageSourceUrl'], 'https://www.youtube.com/watch?v=' + item['videoId'])
            self.assertGreaterEqual(item['videoFrame']['seconds'], 0)
            self.assertFalse(item.get('mobileImage'))
            unsafe = copy.deepcopy(self.data)
            matching = next(x for x in unsafe['items'] if x['brandId'] == item['brandId'])
            matching['imageSourceUrl'] = 'https://www.youtube.com/watch?v=aaaaaaaaaaa'
            with self.assertRaises(ValueError): render(unsafe)

    def test_editorial_showcase_keeps_sources_and_actions_together(self):
        page = html.fromstring(render(self.data))
        slides = page.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " showcase-stage ")]/article')
        self.assertEqual(len(slides), 9)
        self.assertEqual(len(page.xpath('//*[@data-showcase-select]')), 0)
        for slide in slides:
            with self.subTest(brand=slide.get('data-showcase-brand')):
                self.assertEqual(len(slide.xpath('.//div[contains(@class,"showcase-info")]//h2')), 1)
                self.assertEqual(len(slide.xpath('.//div[contains(@class,"showcase-info")]//img[contains(@src,"/assets/")]')), 1)
                self.assertEqual(len(slide.xpath('.//a[contains(@class,"showcase-visual")]//picture//img[@alt]')), 1)
                self.assertEqual(len(slide.xpath('.//a[contains(@href,"/assets/catalogos/")]')), 1)
                self.assertEqual(len(slide.xpath('.//a[contains(@class,"showcase-source")]')), 1)
        self.assertEqual(len(page.xpath('//*[@data-showcase-prev]')), 1)
        self.assertEqual(len(page.xpath('//*[@data-showcase-next]')), 1)

    def test_official_images_reserve_their_actual_space(self):
        page = html.fromstring(render(self.data))
        first = page.xpath('//*[@data-showcase-brand="atlas"]//picture')[0]
        self.assertEqual(first.xpath('.//img/@width'), [str(self.data['items'][0]['imageWidth'])])
        self.assertEqual(first.xpath('.//img/@height'), [str(self.data['items'][0]['imageHeight'])])
        self.assertFalse(first.xpath('.//source'))
        for image in page.xpath('//*[@data-showcase-brand]//picture//img'):
            self.assertTrue(image.get('width'))
            self.assertTrue(image.get('height'))


if __name__ == '__main__':
    unittest.main()

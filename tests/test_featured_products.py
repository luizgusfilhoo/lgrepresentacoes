"""The homepage product selection stays focused on one main line per brand."""

import json
from pathlib import Path
import unittest

from lxml import html


ROOT = Path(__file__).resolve().parents[1]
BRANDS = {"atlas", "dryko", "amatools", "mundial", "lamesa", "odem", "saga", "botafogo", "jlobato"}


class FeaturedProductsTests(unittest.TestCase):
    def test_editorial_selection_covers_every_brand_once(self):
        data = json.loads((ROOT / "data/brand-updates.json").read_text(encoding="utf-8"))
        featured = [item for item in data["items"] if item["origin"] == "editorial"]
        self.assertEqual(len(featured), 9)
        self.assertEqual({item["brandId"] for item in featured}, BRANDS)
        mundial = next(item for item in featured if item["brandId"] == "mundial")
        self.assertIn("spray", (mundial["title"] + mundial["summary"]).lower())
        self.assertNotIn("crystal", mundial["title"].lower())
        for item in featured:
            with self.subTest(brand=item["brandId"]):
                self.assertEqual(item["kind"], "guide")
                self.assertTrue((ROOT / item["mediaPath"]).is_file())
                self.assertTrue(item["mediaAlt"])

    def test_representadas_renders_curated_lines_before_automatic_updates(self):
        page = html.fromstring((ROOT / "representadas/index.html").read_text(encoding="utf-8"))
        cards = page.xpath('//section[@id="produtos"]//article[@data-news-brand]')
        self.assertEqual(len(cards), 9)
        self.assertEqual({card.get("data-news-brand") for card in cards}, BRANDS)
        mundial = next(card for card in cards if card.get("data-news-brand") == "mundial")
        self.assertIn("spray", mundial.xpath("normalize-space(./h3)").lower())
        self.assertNotIn("limpeza de vidros", page.xpath('normalize-space(//section[@id="produtos"])').lower())
        self.assertIn("spray", html.fromstring((ROOT / "index.html").read_text()).xpath('normalize-space(//article[@id="destaque-mundial"])').lower())
        home = html.fromstring((ROOT / 'representadas/index.html').read_text())
        self.assertIn("spray", home.xpath('normalize-space(//article[@id="marca-mundial"])').lower())


if __name__ == "__main__":
    unittest.main()

"""Analytics is configured only with an actual measurement ID."""
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.inject_ga4 import inject


class AnalyticsTests(unittest.TestCase):
    def test_missing_id_keeps_page_free_of_tracker(self):
        with TemporaryDirectory() as directory:
            page = Path(directory) / 'index.html'
            page.write_text('<html><head></head><body></body></html>')
            inject(page, '')
            self.assertNotIn('googletagmanager', page.read_text())

    def test_real_id_is_injected_once_and_invalid_id_is_rejected(self):
        with TemporaryDirectory() as directory:
            page = Path(directory) / 'index.html'
            page.write_text('<html><head></head><body></body></html>')
            inject(page, 'G-ABC1234567')
            inject(page, 'G-ABC1234567')
            self.assertEqual(page.read_text().count('googletagmanager.com'), 1)
            with self.assertRaises(ValueError):
                inject(page, 'G-<script>')


if __name__ == '__main__':
    unittest.main()

"""Only authenticated customer material can appear in social proof sections."""
import json
from pathlib import Path
import unittest

from scripts.render_social_proof import render

ROOT = Path(__file__).resolve().parents[1]


class SocialProofTests(unittest.TestCase):
    def test_empty_source_shows_no_placeholder_claims(self):
        self.assertEqual(render(json.loads((ROOT / 'data/social-proof.json').read_text())), '<!-- SOCIAL PROOF START -->\n<!-- SOCIAL PROOF END -->')

    def test_real_content_requires_approval_and_escapes_text(self):
        item = {'client': 'Cliente <A>', 'sector': 'Distribuição', 'challenge': 'Desafio', 'approach': 'Atuação', 'result': 'Resultado'}
        with self.assertRaises(ValueError):
            render({'cases': [item]})
        item['approved'] = True
        markup = render({'cases': [item]})
        self.assertIn('Cliente &lt;A&gt;', markup)
        self.assertNotIn('Cliente <A>', markup)


if __name__ == '__main__':
    unittest.main()

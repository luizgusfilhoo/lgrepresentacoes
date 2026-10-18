"""Release boundary and browser policy regression tests (synthetic data only)."""
from pathlib import Path
import tempfile
import shutil
import subprocess
import unittest
import sys
from lxml import html
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))

class ReleaseSecurityTests(unittest.TestCase):
    def test_public_copy_removes_stale_private_files_and_rejects_symlinks(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT/'scripts', root/'scripts')
            # Test the real staging function with a minimal independent fixture.
            from importlib.util import spec_from_file_location, module_from_spec
            spec = spec_from_file_location('public_artifact', root/'scripts/public_artifact.py')
            module = module_from_spec(spec)
            spec.loader.exec_module(module)
            (root/'assets').mkdir()
            (root/'assets/ok.svg').write_text('<svg/>')
            (root/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>LG</title>')
            (root/'dist').mkdir()
            (root/'dist/.env').write_text('synthetic-private-marker')
            module.publish(root, files=['index.html'], directories=['assets'])
            self.assertFalse((root/'dist/.env').exists())
            self.assertTrue((root/'dist/assets/ok.svg').is_file())
            (root/'assets/leak.svg').symlink_to(root/'index.html')
            with self.assertRaises(ValueError):
                module.publish(root, files=['index.html'], directories=['assets'])
            self.assertTrue((root/'dist/index.html').exists(), 'failed build must preserve last good dist')

    def test_secret_signature_aborts_before_replacing_last_good_output(self):
        from public_artifact import publish
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'dist').mkdir()
            (root/'dist/index.html').write_text('last-good')
            (root/'index.html').write_text('sb_secret_' + 'TESTONLY'*6)
            with self.assertRaises(ValueError):
                publish(root, files=['index.html'], directories=[])
            self.assertEqual((root/'dist/index.html').read_text(), 'last-good')

    def test_unapproved_json_dump_and_service_role_jwt_are_never_published(self):
        import base64
        from public_artifact import inspect
        with tempfile.TemporaryDirectory() as tmp:
            for filename in ['requests.json','requests.JSON']:
                path = Path(tmp)/filename
                path.write_text('{"name":"synthetic","message":"private"}')
                with self.subTest(filename=filename), self.assertRaises(ValueError): inspect(path)
            hidden = Path(tmp)/'.private'
            hidden.mkdir()
            with self.assertRaises(ValueError): inspect(hidden)
            path = Path(tmp)/'leaked.js'
            encode = lambda value: base64.urlsafe_b64encode(value).decode().rstrip('=')
            path.write_text(encode(b'{\n "alg":"HS256","typ":"JWT"}')+'.'+encode(b'{"role":"service_role"}')+'.test-signature')
            with self.assertRaises(ValueError): inspect(path)

    def test_ga_injection_rehashes_only_its_exact_inline_code(self):
        import base64
        from hashlib import sha256
        from security_policy import protect_html
        from scripts.inject_ga4 import inject
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp)/'index.html'
            page.write_text(protect_html('<html><head><meta charset="utf-8"></head></html>'))
            inject(page, 'G-ABC1234567')
            parsed = html.fromstring(page.read_text())
            policy = parsed.xpath('//meta[@http-equiv="Content-Security-Policy"]/@content')[0]
            script = parsed.xpath('//script[not(@src)]/text()')[0]
            self.assertIn("'sha256-" + base64.b64encode(sha256(script.encode()).digest()).decode()+"'", policy)
            self.assertNotIn("script-src 'self' 'unsafe-inline'", policy)

    def test_every_published_html_has_content_policy_and_referrer_policy(self):
        for path in (ROOT/'dist').rglob('*.html'):
            page = html.fromstring(path.read_text())
            policy = page.xpath('//meta[@http-equiv="Content-Security-Policy"]/@content')
            with self.subTest(path=path):
                self.assertEqual(len(policy), 1)
                self.assertIn("object-src 'none'", policy[0])
                self.assertIn("base-uri 'none'", policy[0])
                self.assertIn("script-src 'self'", policy[0])
                self.assertNotIn("'unsafe-eval'", policy[0])
                self.assertNotIn('frame-ancestors', policy[0], 'unsupported in meta: requires host HTTP header')
                self.assertTrue(page.xpath('//meta[@name="referrer" and @content="strict-origin-when-cross-origin"]'))

if __name__ == '__main__': unittest.main()

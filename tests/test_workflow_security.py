from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]

class WorkflowSecurityTests(unittest.TestCase):
    def test_all_publishers_serialize_and_audit_dependencies(self):
        for filename in ['pages.yml','brand-updates.yml']:
            workflow=(ROOT/'.github/workflows'/filename).read_text()
            with self.subTest(filename=filename):
                self.assertIn('group: github-pages', workflow)
                self.assertIn('npm audit --audit-level=high', workflow)
                self.assertIn("lxml==6.1.1", workflow)
                self.assertIn('Verificar revisão antes de publicar', workflow)
                self.assertIn("if: steps.current.outputs.publish == 'true'", workflow)

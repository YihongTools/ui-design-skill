import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate_skill import ROOT, read_frontmatter, validate


class StaticValidatorTests(unittest.TestCase):
    def test_current_package_has_no_static_errors(self):
        self.assertEqual(validate(ROOT), [])

    def test_missing_frontmatter_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'frontmatter'):
            read_frontmatter('# missing')

    def test_duplicate_frontmatter_key_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            read_frontmatter('---\nname: a\nname: b\n---\nbody')

    def test_v2_contract_and_translation_exist(self):
        skill = (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8')
        chinese = (ROOT / 'ui-design' / 'SKILL.zh-TW.md').read_text(encoding='utf-8')
        self.assertIn('Render feedback loop', skill)
        self.assertIn('SKILL.zh-TW.md', skill)
        self.assertIn('V2', chinese)

    def test_missing_translation_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'ui-design').mkdir()
            (root / 'ui-design' / 'SKILL.md').write_text(
                (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8'),
                encoding='utf-8',
            )
            issues = validate(root)
            self.assertIn('Missing ui-design/SKILL.zh-TW.md translation', issues)

    def test_missing_skill_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            issues = validate(Path(directory))
            self.assertTrue(any('Missing' in issue for issue in issues))


if __name__ == '__main__':
    unittest.main()

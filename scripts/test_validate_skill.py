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

    def test_missing_skill_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            issues = validate(Path(directory))
            self.assertTrue(any('Missing' in issue for issue in issues))


if __name__ == '__main__':
    unittest.main()

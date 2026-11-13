import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate_skill import ROOT, read_frontmatter, validate


def edit_cases(change):
    def apply(root):
        path = root / 'evals' / 'cases.json'
        cases = json.loads(path.read_text(encoding='utf-8'))
        change(cases)
        path.write_text(json.dumps(cases), encoding='utf-8')
    return apply


def edit_bytes(file, change):
    def apply(root):
        path = root / file
        path.write_bytes(change(path.read_bytes()))
    return apply


def to_cp950(data):
    return data.decode('utf-8').encode('cp950', 'replace')


# Each entry breaks a copy of the repository in one way; validate() must report the expected message.
BREAKAGES = (
    ('skill removed', lambda root: (root / 'ui-design' / 'SKILL.md').unlink(), 'Missing'),
    ('frontmatter removed', edit_bytes('ui-design/SKILL.md', lambda data: data.partition(b'\n---\n')[2]), 'frontmatter'),
    ('skill renamed', edit_bytes('ui-design/SKILL.md', lambda data: data.replace(b'name: ui-design', b'name: other', 1)), 'Skill name'),
    ('description too long', edit_bytes('ui-design/SKILL.md', lambda data: data.replace(b'description: ', b'description: ' + b'x' * 1100, 1)), 'Description must be'),
    ('skill not UTF-8', edit_bytes('ui-design/SKILL.md', to_cp950), 'UTF-8'),
    ('translation removed', lambda root: (root / 'docs' / 'SKILL.zh-TW.md').unlink(), 'Missing docs/SKILL.zh-TW.md'),
    ('translation not UTF-8', edit_bytes('docs/SKILL.zh-TW.md', to_cp950), 'UTF-8'),
    ('translation has frontmatter', edit_bytes('docs/SKILL.zh-TW.md', lambda data: b'---\nname: x\n---\n' + data), 'discovery frontmatter'),
    ('translation inside skill folder', lambda root: (root / 'ui-design' / 'SKILL.zh-TW.md').write_text('x', encoding='utf-8'), 'must live in docs/'),
    ('reference file removed', lambda root: (root / 'ui-design' / 'references' / 'states.md').unlink(), 'links missing reference file: states.md'),
    ('reference file not linked', lambda root: (root / 'ui-design' / 'references' / 'orphan.md').write_text('x', encoding='utf-8'), 'not linked from SKILL.md: orphan.md'),
    ('release file removed', lambda root: (root / 'LICENSE').unlink(), 'Missing release file: LICENSE'),
    ('README lost translation link', edit_bytes('README.md', lambda data: data.replace(b'docs/SKILL.zh-TW.md', b'docs/gone.md')), 'README.md must link'),
    ('cases removed', lambda root: (root / 'evals' / 'cases.json').unlink(), 'Missing evals/cases.json'),
    ('cases not UTF-8', edit_bytes('evals/cases.json', lambda data: data.replace(b'EV-01', b'\xae\xd7')), 'Invalid evaluation JSON'),
    ('cases not a list', edit_bytes('evals/cases.json', lambda data: b'{}'), 'at least eight'),
    ('too few cases', edit_cases(lambda cases: cases.__delitem__(slice(7, None))), 'at least eight'),
    ('case is not an object', edit_cases(lambda cases: cases.__setitem__(0, 'x')), 'must be an object'),
    ('case id is a list', edit_cases(lambda cases: cases[0].__setitem__('id', ['EV-01'])), 'missing string id'),
    ('duplicate case id', edit_cases(lambda cases: cases[1].__setitem__('id', 'EV-01')), 'Duplicate evaluation case id'),
    ('unknown mode', edit_cases(lambda cases: cases[0].__setitem__('mode', 'DESTROY')), 'Invalid evaluation mode'),
    ('unknown platform', edit_cases(lambda cases: cases[0].__setitem__('platform', 'ios')), 'Invalid evaluation platform'),
    ('blank prompt', edit_cases(lambda cases: cases[0].__setitem__('prompt', ' ')), 'Missing evaluation prompt'),
    ('blank must', edit_cases(lambda cases: cases[0].__setitem__('must', [''])), 'Missing must assertions'),
    ('non-text must_not', edit_cases(lambda cases: cases[0].__setitem__('must_not', [123])), 'Missing must_not assertions'),
    ('a mode has no case', edit_cases(lambda cases: [c.__setitem__('mode', 'AUDIT') for c in cases if c['mode'] == 'VERIFY']), 'must cover every mode'),
    ('a platform has no case', edit_cases(lambda cases: [c.__setitem__('platform', 'web') for c in cases if c['platform'] == 'negative']), 'must cover web'),
    ('fixture removed', lambda root: shutil.rmtree(root / 'evals' / 'fixtures' / 'web-ui'), 'references missing fixture'),
)


class StaticValidatorTests(unittest.TestCase):
    def test_current_package_has_no_static_errors(self):
        self.assertEqual(validate(ROOT), [])

    def test_each_breakage_is_reported(self):
        for label, breakage, expected in BREAKAGES:
            with self.subTest(label), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / 'repo'
                shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns('.git', '__pycache__'))
                breakage(root)
                issues = validate(root)
                self.assertTrue(any(expected in issue for issue in issues), issues)

    def test_missing_frontmatter_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'frontmatter'):
            read_frontmatter('# missing')

    def test_duplicate_frontmatter_key_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            read_frontmatter('---\nname: a\nname: b\n---\nbody')

    def test_empty_frontmatter_value_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Empty'):
            read_frontmatter('---\nname:\n---\nbody')


if __name__ == '__main__':
    unittest.main()

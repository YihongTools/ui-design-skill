#!/usr/bin/env python3
"""Static structure checks only. Does not check Skill wording, run Claude, or evaluate UI quality."""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_MODES = ('PLAN', 'SKETCH', 'BUILD', 'AUDIT', 'FIX', 'VERIFY')
ALLOWED_EVAL_MODES = REQUIRED_MODES + ('NONE',)
REQUIRED_TYPES = ('web', 'native-android', 'negative', 'boundary')
RELEASE_FILES = ('README.md', 'README.zh-TW.md', 'LICENSE', 'CHANGELOG.md', 'ATTRIBUTION.md',
                 'RELEASE_CHECKLIST.md', 'evals/README.md', '.github/workflows/validate.yml')


def read_frontmatter(text):
    # shortcut: single-line `key: value` pairs only; switch to a YAML parser if the Skill ever needs folded or nested values.
    match = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n', text, re.S)
    if not match:
        raise ValueError('SKILL.md missing YAML frontmatter delimiters')
    result = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if ':' not in line or line.startswith((' ', '\t')):
            raise ValueError(f'Unsupported frontmatter syntax: {line!r}')
        key, value = line.split(':', 1)
        value = value.strip().strip('"\'')
        if not value:
            raise ValueError(f'Empty frontmatter value: {key}')
        if key in result:
            raise ValueError(f'Duplicate frontmatter key: {key}')
        result[key] = value
    return result


def validate(root):
    try:
        return _validate(root)
    except UnicodeDecodeError as exc:
        return [f'A checked file is not valid UTF-8: {exc}']


def _validate(root):
    errors = []
    skill_path = root / 'ui-design' / 'SKILL.md'
    if not skill_path.is_file():
        return [f'Missing {skill_path}']
    text = skill_path.read_text(encoding='utf-8')
    try:
        meta = read_frontmatter(text)
        if meta.get('name') != 'ui-design':
            errors.append('Skill name must equal ui-design')
        if not (20 <= len(meta.get('description', '')) <= 1024):
            errors.append('Description must be between 20 and 1024 characters')
    except ValueError as exc:
        errors.append(str(exc))

    linked = set(re.findall(r'references/([\w-]+\.md)', text))
    present = {path.name for path in (root / 'ui-design' / 'references').glob('*.md')}
    for name in sorted(linked - present):
        errors.append(f'SKILL.md links missing reference file: {name}')
    for name in sorted(present - linked):
        errors.append(f'Reference file not linked from SKILL.md: {name}')

    if (root / 'ui-design' / 'SKILL.zh-TW.md').exists():
        errors.append('Reference translation must live in docs/, not installed Skill folder')
    translation_path = root / 'docs' / 'SKILL.zh-TW.md'
    if not translation_path.is_file():
        errors.append('Missing docs/SKILL.zh-TW.md translation')
    elif translation_path.read_text(encoding='utf-8').lstrip().startswith('---'):
        errors.append('Translation must not contain Agent Skill discovery frontmatter')

    for expected in RELEASE_FILES:
        if not (root / expected).is_file():
            errors.append(f'Missing release file: {expected}')
    for readme in ('README.md', 'README.zh-TW.md'):
        path = root / readme
        if path.is_file():
            docs = path.read_text(encoding='utf-8')
            if 'docs/SKILL.zh-TW.md' not in docs or 'ui-design/SKILL.md' not in docs:
                errors.append(f'{readme} must link both canonical and translated Skill files')

    errors.extend(_validate_cases(root))
    return errors


def _validate_cases(root):
    cases_file = root / 'evals' / 'cases.json'
    if not cases_file.is_file():
        return ['Missing evals/cases.json']
    try:
        cases = json.loads(cases_file.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:  # ValueError covers bad JSON and non-UTF-8 bytes
        return [f'Invalid evaluation JSON: {exc}']
    if not isinstance(cases, list) or len(cases) < 8:
        return ['Expected at least eight evaluation cases']
    errors = []
    seen_ids, seen_modes, seen_types = set(), set(), set()
    for item in cases:
        if not isinstance(item, dict):
            errors.append('Evaluation case must be an object')
            continue
        cid = item.get('id')
        if not isinstance(cid, str) or not cid:
            errors.append('Evaluation case missing string id')
        elif cid in seen_ids:
            errors.append(f'Duplicate evaluation case id: {cid}')
        else:
            seen_ids.add(cid)
        if item.get('mode') not in ALLOWED_EVAL_MODES:
            errors.append(f'Invalid evaluation mode: {cid}')
        elif item['mode'] != 'NONE':
            seen_modes.add(item['mode'])
        if item.get('platform') not in REQUIRED_TYPES:
            errors.append(f'Invalid evaluation platform: {cid}')
        else:
            seen_types.add(item['platform'])
        prompt = item.get('prompt')
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f'Missing evaluation prompt: {cid}')
            prompt = ''
        for field in ('must', 'must_not'):
            values = item.get(field)
            if not isinstance(values, list) or not values or not all(isinstance(v, str) and v.strip() for v in values):
                errors.append(f'Missing {field} assertions: {cid}')
        for fixture in set(re.findall(r'evals/fixtures/[\w./-]*\w', f"{item.get('setup', '')} {prompt}")):
            if not (root / fixture).exists():
                errors.append(f'Evaluation case {cid} references missing fixture: {fixture}')
    if seen_modes != set(REQUIRED_MODES):
        errors.append('Evaluation cases must cover every mode')
    if seen_types != set(REQUIRED_TYPES):
        errors.append('Evaluation cases must cover web, native-android, negative, boundary')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    errors = validate(args.root)
    if errors:
        for error in errors:
            print(f'FAIL: {error}', file=sys.stderr)
        return 1
    print('PASS: static Skill metadata, file layout, release files, and eval schema checks')
    print('NOT RUN: Skill wording review, Claude behavior, rendered UI, device/E2E, accessibility acceptance')
    return 0


if __name__ == '__main__':
    sys.exit(main())

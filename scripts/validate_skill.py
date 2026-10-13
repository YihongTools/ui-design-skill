#!/usr/bin/env python3
"""Static checks only. Does not run Codex or evaluate UI quality."""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_MODES = ('PLAN', 'BUILD', 'AUDIT', 'FIX', 'VERIFY')
ALLOWED_EVAL_MODES = REQUIRED_MODES + ('NONE',)
REQUIRED_RULES = (
    'Design authority first.',
    'Choose defaults deliberately.',
    'Decoration has a job.',
    'Hierarchy before containers.',
    'Consistent, not rigid.',
    'Content decides layout.',
    'Motion serves function.',
    'Findings need evidence.',
)
REQUIRED_RENDER_TERMS = ('Render feedback loop', 'Render.', 'Critique.', 'Revise.', 'visual not verified', 'At most two rounds')
REQUIRED_CONFIDENCE = ('Confirmed', 'Probable', 'Candidate', 'Exempted')
REQUIRED_SEVERITY = ('High', 'Medium', 'Low')
REQUIRED_TYPES = ('web', 'native-android', 'negative', 'boundary')


def read_frontmatter(text):
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
    errors = []
    skill_path = root / 'ui-design' / 'SKILL.md'
    if not skill_path.is_file():
        return [f'Missing {skill_path}']
    text = skill_path.read_text(encoding='utf-8')
    try:
        meta = read_frontmatter(text)
        if meta.get('name') != 'ui-design':
            errors.append('Skill name must equal ui-design')
        description = meta.get('description', '')
        if not (20 <= len(description) <= 1024):
            errors.append('Description must be between 20 and 1024 characters')
        for keyword in ('UI', 'Android'):
            if keyword.casefold() not in description.casefold():
                errors.append(f'Description lacks trigger/scope term: {keyword}')
    except ValueError as exc:
        errors.append(str(exc))
    if not any(verb in meta.get('description', '').casefold() for verb in ('audit', 'review')):
        errors.append('Description lacks audit/review trigger')
    if '## Eight principles' in text and '## When critical information is missing' in text:
        rules_section = text.split('## Eight principles', 1)[1].split('## When critical information is missing', 1)[0]
    else:
        rules_section = ''
        errors.append('Missing V2 eight principles section')
    numbered = re.findall(r'^([1-8])\.\s+\*\*([^*]+)\*\*', rules_section, re.M)
    if [int(num) for num, _ in numbered] != list(range(1, 9)):
        errors.append('Expected exactly eight ordered governing rules')
    else:
        for (idx, title), expected in zip(numbered, REQUIRED_RULES):
            if title != expected:
                errors.append(f'Rule {idx} title changed: expected {expected}')
    for mode in REQUIRED_MODES:
        if not re.search(rf'\b{mode}\b', text):
            errors.append(f'Missing mode: {mode}')
    for term in REQUIRED_CONFIDENCE + REQUIRED_SEVERITY + REQUIRED_RENDER_TERMS:
        if term not in text:
            errors.append(f'Missing classification: {term}')
    for marker in ('AUDIT**: Read-only', 'An audit is not authorization to fix',
                   'has no built-in scoring', 'require explicit authorization',
                   'SKILL.zh-TW.md'):
        if marker.casefold() not in text.casefold():
            errors.append(f'Missing V2 safety/scoring/translation contract: {marker}')
    if '# UI Design (V2:' not in text:
        errors.append('Canonical Skill is not marked V2')
    translation_path = root / 'ui-design' / 'SKILL.zh-TW.md'
    if not translation_path.is_file():
        errors.append('Missing ui-design/SKILL.zh-TW.md translation')
    else:
        translation = translation_path.read_text(encoding='utf-8')
        if translation.lstrip().startswith('---\n'):
            errors.append('Translation must not contain Agent Skill discovery frontmatter')
        if 'V2' not in translation or '英文' not in translation and 'English' not in translation:
            errors.append('Translation lacks V2 and canonical English authority context')
        for mode in REQUIRED_MODES:
            if mode not in translation:
                errors.append(f'Translation missing mode: {mode}')
    for readme in ('README.md', 'README.zh-TW.md'):
        path = root / readme
        if path.is_file():
            docs = path.read_text(encoding='utf-8')
            if 'SKILL.zh-TW.md' not in docs or 'SKILL.md' not in docs:
                errors.append(f'{readme} must link both canonical and translated Skill files')
    cases_file = root / 'evals' / 'cases.json'
    if not cases_file.is_file():
        errors.append('Missing evals/cases.json')
    else:
        try:
            cases = json.loads(cases_file.read_text(encoding='utf-8'))
            if not isinstance(cases, list) or len(cases) < 8:
                errors.append('Expected at least eight evaluation cases')
            else:
                seen_ids = set()
                seen_modes = set()
                seen_types = set()
                for item in cases:
                    if not isinstance(item, dict):
                        errors.append('Evaluation case must be an object')
                        continue
                    cid = item.get('id')
                    if not isinstance(cid, str) or not cid:
                        errors.append('Evaluation case missing string id')
                    elif cid in seen_ids:
                        errors.append(f'Duplicate evaluation case id: {cid}')
                    seen_ids.add(cid)
                    if item.get('mode') not in ALLOWED_EVAL_MODES:
                        errors.append(f'Invalid evaluation mode: {cid}')
                    else:
                        if item['mode'] != 'NONE':
                            seen_modes.add(item['mode'])
                    if item.get('platform') not in REQUIRED_TYPES:
                        errors.append(f'Invalid evaluation platform: {cid}')
                    else:
                        seen_types.add(item['platform'])
                    if not isinstance(item.get('prompt'), str) or not item['prompt'].strip():
                        errors.append(f'Missing evaluation prompt: {cid}')
                    for field in ('must', 'must_not'):
                        if not isinstance(item.get(field), list) or not item[field]:
                            errors.append(f'Missing {field} assertions: {cid}')
                if seen_modes != set(REQUIRED_MODES):
                    errors.append('Evaluation cases must cover all five modes')
                if seen_types != set(REQUIRED_TYPES):
                    errors.append('Evaluation cases must cover web, native-android, negative, boundary')
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f'Invalid evaluation JSON: {exc}')
    for expected in ('README.md','README.zh-TW.md','LICENSE','CHANGELOG.md',
                     'ATTRIBUTION.md','RELEASE_CHECKLIST.md','evals/README.md','.github/workflows/validate.yml'):
        if not (root / expected).is_file():
            errors.append(f'Missing release file: {expected}')
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
    print('PASS: static Skill metadata, contract, release files, and eval schema checks')
    print('NOT RUN: Codex behavior, rendered UI, device/E2E, accessibility acceptance')
    return 0


if __name__ == '__main__':
    sys.exit(main())

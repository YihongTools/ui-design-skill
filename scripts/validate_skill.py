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
REQUIRED_RENDER_TERMS = ('Render feedback loop', 'Render.', 'Critique.', 'Revise.', 'visual not verified', 'at most two revision rounds')
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
                   'has no built-in scoring', 'require separate explicit authorization',
                   'Repository writes outside the authorized UI files'):
        if marker.casefold() not in text.casefold():
            errors.append(f'Missing V2 safety/scoring/translation contract: {marker}')
    if '# UI Design (V2.1:' not in text:
        errors.append('Canonical Skill is not marked V2.1')
    for contract in ('three materially different directions', 'Model-selected; user may override',
                     'color (including primary color family)', 'typeface / typography',
                     'page-level layout structure', 'Fixed by brief',
                     'Pre-implementation decision record.', 'Intentionally retained, because',
                     '"Looks fine" or "clean" is not a reason',
                     'Use an existing design system as authority',
                     'ask at most three questions',
                     'If references are supplied, state what is transferable from each',
                     'or the selected candidate direction',
                     'check each applicable row of the defaults table against the render',
                     'A chosen replacement that is not visible on screen counts as a template-like item',
                     'quote the exact sentence', 'only if the brief states the constraint explicitly',
                     '**Substantial redesign** means a new screen',
                     'Localized styling, spacing, or component tweaks alone are not substantial',
                     'available system font stack', 'locally bundled font',
                     'including Android `res/font`', 'without approval',
                     'If no one can approve a font file',
                     '## Direction and defaults table (greenfield or substantial redesign)',
                     "localized tweaks follow the existing code's conventions",
                     'Unmodified framework or template defaults',
                     'Material 3 baseline', 'default Tailwind/shadcn',
                     'Design system: <source>',
                     "brief means the user's request or any requirements document they supplied",
                     'fully governs the surface, skip steps 1–2',
                     'only uncovered rows need the full record',
                     'applicable direction and step 3 decisions',
                     'documented three-direction fallback'):
        if contract.casefold() not in text.casefold():
            errors.append(f'Missing V2.1 contract: {contract}')
    verify_mode = text.partition('- **VERIFY**:')[2].splitlines()[0] if '- **VERIFY**:' in text else ''
    loop_boundary = text.partition('## Render feedback loop')[2].partition('1. **Render.**')[0]
    if not all(term in verify_mode for term in ('Read-only', 'not fix authorization', 'only under BUILD/FIX', 'explicitly authorizes fixes')):
        errors.append('Missing VERIFY mode permission boundary')
    if not all(term in loop_boundary for term in ('VERIFY runs steps 1, 2, and 4', 'step 3 Revise', 'only under BUILD/FIX', 'fixes are explicitly authorized')):
        errors.append('Missing VERIFY render-loop step boundary')
    plan = text.partition('## PLAN / BUILD procedure')[2].partition('## Render feedback loop')[0]
    critique = text.partition('2. **Critique.**')[2].partition('3. **Revise.**')[0]
    if not all(term in plan for term in ('functional requirements stated in the brief', 'required states, actions, information shown, completion behavior, and error behavior when specified')):
        errors.append('Missing functional requirement identification rule')
    if not all(term in critique for term in ('every identified functional requirement', 'present and operable in the render', 'High-severity defect', 'regardless of improvements')):
        errors.append('Missing functional preservation critique rule')
    report = text.partition('4. **Report.**')[2].partition('## AUDIT')[0]
    build_output = text.partition('- **BUILD/FIX**:')[2].splitlines()[0] if '- **BUILD/FIX**:' in text else ''
    if not all(term in report for term in ('each identified functional requirement', 'Requirement | Status | Evidence | Notes',
                                         'exactly one of `present and operable`, `missing or broken`, or `unverified`',
                                         "intentional exception to replying in the user's language", 'separately from Status')):
        errors.append('Missing Report functional status rule')
    verify_output = text.partition('## Output')[2].partition('- **VERIFY**:')[2].splitlines()[0] if '- **VERIFY**:' in text.partition('## Output')[2] else ''
    for section, label in ((build_output, 'BUILD/FIX'), (verify_output, 'VERIFY')):
        if 'canonical functional-requirement reporting schema in Report' not in section:
            errors.append(f'Missing {label} functional status rule')
    if text.count('Design system: <source>') != 1:
        errors.append('V2.1 compact Design system row syntax must be defined exactly once in runtime Skill')
    output_section = text.partition('## Output')[2].partition('## Scoring')[0]
    if not output_section or not all(term in output_section for term in ('**PLAN**:', 'three candidate directions', 'three-row defaults table', 'supplied references')):
        errors.append('V2.1 PLAN output must include references or candidates and defaults table')
    for eval_only in ('A/B', 'runner', 'body-read', 'Skill file was read', 'not proof that the canonical',
                      'decision-record timing', 'SKILL.zh-TW.md'):
        if eval_only.casefold() in text.casefold():
            errors.append(f'Evaluation or translation reference leaked into runtime Skill: {eval_only}')
    if (root / 'ui-design' / 'SKILL.zh-TW.md').exists():
        errors.append('Reference translation must live in docs/, not installed Skill folder')
    translation_path = root / 'docs' / 'SKILL.zh-TW.md'
    if not translation_path.is_file():
        errors.append('Missing docs/SKILL.zh-TW.md translation')
    else:
        translation = translation_path.read_text(encoding='utf-8')
        if translation.lstrip().startswith('---\n'):
            errors.append('Translation must not contain Agent Skill discovery frontmatter')
        if 'V2.1' not in translation or '英文' not in translation and 'English' not in translation:
            errors.append('Translation lacks V2 and canonical English authority context')
        for translated_term in ('三個實質不同', '主色系', '整頁版型結構', '由需求決定',
                                '施工前設計決策紀錄', '刻意保留，因為', '最多只問三個問題',
                                '逐一說明其哪些特性可轉用到本產品', '選定的候選方向',
                                '逐列檢查預設替換表中適用的每一列', '逐字引用需求原句',
                                '只有 brief 明確寫出限制', '修改整頁版型結構、主色系、字體',
                                '單純局部樣式、間距或元件微調不算',
                                '系統字型組合', 'Android `res/font`', '無人可批准字型檔',
                                'Design system: <來源>', '局部微調沿用既有程式碼與元件慣例',
                                '未經專案客製的框架或模板預設', 'Material 3 baseline',
                                'brief** 指使用者本次要求或使用者提供的需求文件',
                                '只有未被管轄的列才展開完整', '適用的方向與步驟 3 決策'):
            if translated_term not in translation:
                errors.append(f'Translation missing V2.1 contract: {translated_term}')
        verify_mode = translation.partition('- **VERIFY**：')[2].splitlines()[0] if '- **VERIFY**：' in translation else ''
        loop_boundary = translation.partition('## 渲染回饋迴圈')[2].partition('1. **渲染**')[0]
        if not all(term in verify_mode for term in ('預設唯讀', '不是修正授權', '僅在 BUILD/FIX', '明確授權修正')):
            errors.append('Translation missing VERIFY mode permission boundary')
        if not all(term in loop_boundary for term in ('VERIFY 只執行步驟 1、2、4', '步驟 3 Revise', '僅在 BUILD/FIX', '明確授權修正')):
            errors.append('Translation missing VERIFY render-loop step boundary')
        plan = translation.partition('## PLAN / BUILD 流程')[2].partition('## 渲染回饋迴圈')[0]
        critique = translation.partition('2. **批評**')[2].partition('3. **修正**')[0]
        if not all(term in plan for term in ('辨認 brief 明訂的功能需求', '必要狀態、操作、呈現資訊、完成行為', '錯誤行為')):
            errors.append('Translation missing functional requirement identification rule')
        if not all(term in critique for term in ('功能需求', '仍存在且可操作', 'High 嚴重度 defect', '不能用')):
            errors.append('Translation missing functional preservation critique rule')
        report = translation.partition('4. **回報**')[2].partition('## AUDIT')[0]
        build_output = translation.partition('- **BUILD/FIX**：')[2].splitlines()[0] if '- **BUILD/FIX**：' in translation else ''
        if not all(term in report for term in ('每項已辨認功能需求的狀態', 'Requirement | Status | Evidence | Notes',
                                             '`present and operable`、`missing or broken` 或 `unverified`')):
            errors.append('Translation missing Report functional status rule')
        verify_output = translation.partition('## 輸出')[2].partition('- **VERIFY**：')[2].splitlines()[0] if '- **VERIFY**：' in translation.partition('## 輸出')[2] else ''
        for section, label in ((build_output, 'BUILD/FIX'), (verify_output, 'VERIFY')):
            if '依回報的標準功能需求回報格式' not in section:
                errors.append(f'Translation missing {label} functional status rule')
        if translation.count('Design system: <來源>') != 1:
            errors.append('Translation compact Design system row syntax must be defined exactly once')
        for mode in REQUIRED_MODES:
            if mode not in translation:
                errors.append(f'Translation missing mode: {mode}')
    for readme in ('README.md', 'README.zh-TW.md'):
        path = root / readme
        if path.is_file():
            docs = path.read_text(encoding='utf-8')
            if 'docs/SKILL.zh-TW.md' not in docs or 'ui-design/SKILL.md' not in docs:
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

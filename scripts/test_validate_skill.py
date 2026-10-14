import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate_skill import ROOT, read_frontmatter, validate


class StaticValidatorTests(unittest.TestCase):
    def test_current_package_has_no_static_errors(self):
        self.assertEqual(validate(ROOT), [])

    def test_removed_functional_rules_are_rejected(self):
        import shutil
        mutations = (
            ('ui-design/SKILL.md', 'functional requirements stated in the brief', 'identification'),
            ('ui-design/SKILL.md', 'present and operable in the render', 'preservation critique'),
            ('docs/SKILL.zh-TW.md', '辨認 brief 明訂的功能需求', 'identification'),
            ('docs/SKILL.zh-TW.md', '仍存在且可操作', 'preservation critique'),
        )
        for file, phrase, expected in mutations:
            with self.subTest(file=file, rule=expected), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                shutil.copytree(ROOT, root, dirs_exist_ok=True)
                path = root / file
                text = path.read_text(encoding='utf-8')
                self.assertIn(phrase, text)
                path.write_text(text.replace(phrase, ''), encoding='utf-8')
                self.assertTrue(any(expected in issue for issue in validate(root)))

    def test_removed_functional_status_reports_are_rejected(self):
        import shutil
        for file, marker, label, phrase in (
            ('ui-design/SKILL.md', '4. **Report.**', 'Report', 'exactly one of `present and operable`, `missing or broken`, or `unverified`'),
            ('ui-design/SKILL.md', '- **BUILD/FIX**:', 'BUILD/FIX', 'canonical functional-requirement reporting schema in Report'),
            ('ui-design/SKILL.md', '- **VERIFY**: the viewports', 'VERIFY', 'canonical functional-requirement reporting schema in Report'),
            ('docs/SKILL.zh-TW.md', '4. **回報**', 'Report', '`present and operable`、`missing or broken` 或 `unverified`'),
            ('docs/SKILL.zh-TW.md', '- **BUILD/FIX**：', 'BUILD/FIX', '依回報的標準功能需求回報格式'),
            ('docs/SKILL.zh-TW.md', '- **VERIFY**：實際', 'VERIFY', '依回報的標準功能需求回報格式'),
        ):
            with self.subTest(file=file, section=label), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                shutil.copytree(ROOT, root, dirs_exist_ok=True)
                path = root / file
                before, marker, after = path.read_text(encoding='utf-8').partition(marker)
                self.assertTrue(marker)
                self.assertIn(phrase, after)
                path.write_text(before + marker + after.replace(phrase, '', 1), encoding='utf-8')
                self.assertTrue(any(f'{label} functional status' in issue for issue in validate(root)))

    def test_removed_verify_boundaries_are_rejected(self):
        import shutil
        for file, phrase, expected in (
            ('ui-design/SKILL.md', 'VERIFY is not fix authorization', 'VERIFY mode permission'),
            ('ui-design/SKILL.md', 'VERIFY runs steps 1, 2, and 4', 'VERIFY render-loop step'),
            ('docs/SKILL.zh-TW.md', 'VERIFY 本身不是修正授權', 'VERIFY mode permission'),
            ('docs/SKILL.zh-TW.md', 'VERIFY 只執行步驟 1、2、4', 'VERIFY render-loop step'),
        ):
            with self.subTest(file=file, boundary=expected), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                shutil.copytree(ROOT, root, dirs_exist_ok=True)
                path = root / file
                text = path.read_text(encoding='utf-8')
                self.assertIn(phrase, text)
                path.write_text(text.replace(phrase, '', 1), encoding='utf-8')
                self.assertTrue(any(expected in issue for issue in validate(root)))

    def test_missing_frontmatter_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'frontmatter'):
            read_frontmatter('# missing')

    def test_duplicate_frontmatter_key_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            read_frontmatter('---\nname: a\nname: b\n---\nbody')

    def test_v2_contract_and_translation_exist(self):
        skill = (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8')
        chinese = (ROOT / 'docs' / 'SKILL.zh-TW.md').read_text(encoding='utf-8')
        self.assertIn('Render feedback loop', skill)
        self.assertNotIn('SKILL.zh-TW.md', skill)
        self.assertIn('V2.1', chinese)

    def test_v21_greenfield_and_render_dispositions(self):
        text = (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8')
        for item in ('three materially different directions',
                     'Model-selected; user may override',
                     'color (including primary color family)',
                     'typeface / typography',
                     'page-level layout structure', 'Fixed by brief',
                     'Pre-implementation decision record.',
                     'Intentionally retained, because',
                     'ask at most three questions',
                     'If references are supplied, state what is transferable from each',
                     'or the selected candidate direction',
                     'check each applicable row of the defaults table against the render'):
            self.assertIn(item, text)

    def test_v21_chinese_reference_has_corresponding_boundaries(self):
        text = (ROOT / 'docs' / 'SKILL.zh-TW.md').read_text(encoding='utf-8')
        for item in ('模型自行選擇，使用者可推翻', '由需求決定',
                     '施工前設計決策紀錄', '刻意保留，因為',
                     '最多只問三個問題', '選定的候選方向',
                     '逐列檢查預設替換表中適用的每一列'):
            self.assertIn(item, text)

    def test_v21_quote_typography_and_scope_rules(self):
        text = (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8')
        for phrase in ('quote the exact sentence',
                       'only if the brief states the constraint explicitly',
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
            self.assertIn(phrase.casefold(), text.casefold())
        output = text.split('## Output', 1)[1].split('## Scoring', 1)[0]
        for phrase in ('**PLAN**:', 'three candidate directions',
                       'three-row defaults table', 'supplied references'):
            self.assertIn(phrase, output)

    def test_v21_translation_mirrors_new_scope_rules(self):
        text = (ROOT / 'docs' / 'SKILL.zh-TW.md').read_text(encoding='utf-8')
        for phrase in ('逐字引用需求原句', '只有 brief 明確寫出限制',
                       '修改整頁版型結構、主色系、字體',
                       '單純局部樣式、間距或元件微調不算',
                       '系統字型組合', 'Android `res/font`', '無人可批准字型檔',
                       'Design system: <來源>', '局部微調沿用既有程式碼與元件慣例',
                       '未經專案客製的框架或模板預設', 'Material 3 baseline',
                       'brief** 指使用者本次要求或使用者提供的需求文件',
                       '只有未被管轄的列才展開完整', '適用的方向與步驟 3 決策'):
            self.assertIn(phrase, text)

    def test_static_validator_rejects_removed_fixed_by_brief_quote(self):
        import shutil
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT, root, dirs_exist_ok=True)
            path = root / 'ui-design' / 'SKILL.md'
            text = path.read_text(encoding='utf-8')
            self.assertIn('quote the exact sentence', text)
            path.write_text(text.replace('quote the exact sentence', 'mention the requirement'), encoding='utf-8')
            self.assertTrue(any('quote the exact sentence' in error for error in validate(root)))

    def test_static_validator_rejects_missing_plan_table_output(self):
        import shutil
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT, root, dirs_exist_ok=True)
            path = root / 'ui-design' / 'SKILL.md'
            text = path.read_text(encoding='utf-8')
            self.assertIn('three-row defaults table', text)
            path.write_text(text.replace('three-row defaults table', 'brief summary'), encoding='utf-8')
            self.assertTrue(any('PLAN output' in error for error in validate(root)))

    def test_evaluation_language_stays_out_of_runtime_skill(self):
        text = (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8')
        for term in ('A/B', 'runner', 'body-read', 'SKILL.zh-TW.md', 'Skill file was read'):
            self.assertNotIn(term.casefold(), text.casefold())
        evaluation = (ROOT / 'evals' / 'README.md').read_text(encoding='utf-8')
        self.assertIn('body-read evidence', evaluation)

    def test_existing_design_system_missing_platform_is_not_greenfield(self):
        text = (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('Use an existing design system as authority', text)
        self.assertIn('target platform', text)
        self.assertIn('stop before edits', text)

    def test_r6_localized_tweak_does_not_trigger_full_direction_flow(self):
        text = (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn("## Direction and defaults table (greenfield or substantial redesign)", text)
        self.assertIn("localized tweaks follow the existing code's conventions", text)

    def test_r6_design_system_rows_can_short_circuit_full_record(self):
        text = (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8')
        self.assertEqual(text.count('Design system: <source>'), 1)
        self.assertIn('only uncovered rows need the full record', text)
        self.assertIn('fully governs the surface, skip steps 1–2', text)

    def test_r6_unattended_font_fallback_is_explicit(self):
        text = (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('If no one can approve a font file', text)
        self.assertIn('record the preferred font as a suggestion, not as applied', text)

    def test_r6_runtime_skill_excludes_body_read_experiment_language(self):
        text = (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8')
        self.assertNotIn('proof that a Skill file was read', text)
        evaluation = (ROOT / 'evals' / 'README.md').read_text(encoding='utf-8')
        self.assertIn('not proof that the canonical SKILL.md was read or consumed', evaluation)

    def test_r6_framework_defaults_are_not_governing_design_system(self):
        text = (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('Unmodified framework or template defaults', text)
        self.assertIn('Material 3 baseline', text)
        self.assertIn('default Tailwind/shadcn', text)

    def test_r6_brief_is_defined_and_description_mentions_fallback(self):
        text = (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn("brief means the user's request or any requirements document they supplied", text)
        self.assertIn('reference-first direction step (or a documented three-direction fallback)', text)

    def test_r6_compact_design_system_syntax_is_centralized(self):
        text = (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8')
        zh = (ROOT / 'docs' / 'SKILL.zh-TW.md').read_text(encoding='utf-8')
        self.assertEqual(text.count('Design system: <source>'), 1)
        self.assertEqual(zh.count('Design system: <來源>'), 1)

    def test_translation_inside_install_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            import shutil
            root = Path(directory)
            shutil.copytree(ROOT / 'ui-design', root / 'ui-design')
            shutil.copytree(ROOT / 'docs', root / 'docs')
            (root / 'ui-design' / 'SKILL.zh-TW.md').write_text('wrong location', encoding='utf-8')
            issues = validate(root)
            self.assertTrue(any('must live in docs/' in issue for issue in issues))

    def test_missing_translation_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'ui-design').mkdir()
            (root / 'ui-design' / 'SKILL.md').write_text(
                (ROOT / 'ui-design' / 'SKILL.md').read_text(encoding='utf-8'),
                encoding='utf-8',
            )
            issues = validate(root)
            self.assertIn('Missing docs/SKILL.zh-TW.md translation', issues)

    def test_missing_skill_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            issues = validate(Path(directory))
            self.assertTrue(any('Missing' in issue for issue in issues))


if __name__ == '__main__':
    unittest.main()

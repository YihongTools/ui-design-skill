# Changelog

This project uses [Semantic Versioning](https://semver.org/), with pre-1.0 releases indicating that the skill's behavior and evaluation contract may still change.

## [0.2.0] - 2026-10-13

### Changed

- Replace canonical `ui-design/SKILL.md` with the Owner-provided Skill V2.
- Add the reference-first greenfield design direction and bounded Render → Critique → Revise loop.
- Add `ui-design/SKILL.zh-TW.md` as a Traditional Chinese reading copy; English remains canonical.
- Update the static validator and tests for V2 sections and the two-file distribution contract.
- Preserve advisory-only scoring, scoped edit authorization, and runtime-evaluation caveats.

### Verification status

- Static validation and validator regression suite: **PASS** in GitHub Actions ([run #38335072860](https://github.com/YihongTools/ui-design-skill/actions/runs/38335072860)); six validator tests.
- Codex V2 behavior and render/device/E2E acceptance: **NOT RUN**.
- No version tag or formal GitHub Release has been created.

## [0.1.0] - 2026-10-13

### Added

- Original `ui-design` Skill: PLAN, BUILD, AUDIT, FIX, VERIFY.
- Eight design governance rules and an evidence/confidence/severity model.
- Explicit read-only AUDIT boundary and scoped edit/verification rules.
- Advisory-only scoring with no bundled scanner or pass/fail threshold.
- English and Traditional Chinese READMEs, licensing and source attribution.
- Dependency-free static validation, regression tests, and GitHub Actions workflow.
- Codex runtime evaluation plan, fixtures, and behavioral acceptance cases.

### Verification status

- Repository static checks: see `scripts/validate_skill.py` and CI runs when available.
- Codex invocation, behavior, browser/device UI acceptance, and full E2E: **NOT RUN** as of package preparation.
- GitHub source publication to `main`: **DONE** on 2026-10-13; initial workflow Static Skill Validation: **PASS** ([run #38332002624](https://github.com/YihongTools/ui-design-skill/actions/runs/38332002624)).
- GitHub version tag / formal Release and subsequent Codex runtime evaluation: **NOT DONE**.
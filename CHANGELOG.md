# Changelog

This project uses [Semantic Versioning](https://semver.org/), with pre-1.0 releases indicating that the skill's behavior and evaluation contract may still change.

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
- GitHub publication, release/tag, and subsequent Codex evaluation: **NOT DONE** as of package preparation.
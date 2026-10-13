# Contributing

Contributions should preserve product-specific design authority, evidence-based findings, and minimal reversible change. A rule that bans a font, palette, layout, or animation without a contextual exception is unlikely to be accepted.

## Proposed change contract

1. Describe the user-visible behavior, affected mode(s), and why the current rule is insufficient.
2. Include at least one positive case and one negative/exemption case in `evals/cases.json` when behavior changes.
3. Keep `ui-design/SKILL.md` narrow; avoid copying third-party catalogs or adding runtime dependencies without a documented reason.
4. Run `python scripts/validate_skill.py` and `python -m unittest discover -s scripts -p 'test_*.py' -v`.
5. Distinguish static checks from actual Codex behavioral evaluation. Report unexecuted checks as NOT RUN.

Avoid uploading private repositories, credentials, user records, or screenshots containing personal data into public evaluation artifacts. Do not claim visual, Android, accessibility, or E2E PASS from static checks.
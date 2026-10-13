# GitHub publication checklist

## Pre-publication (owner approval)

- [x] Confirm the proposed destination (`YihongTools/ui-design-skill`) and repository visibility.
- [x] Confirm **MIT** as the license for original material and **YihongTools** as copyright holder; review `ATTRIBUTION.md`.
- [x] Review both READMEs and ensure no private data, unpublished repository path, or credential is exposed.
- [x] Run `python scripts/validate_skill.py` and validator regression tests.
- [ ] Open a GitHub repository and push these source files only with explicit authorization.
- [ ] Confirm GitHub Actions Static Skill Validation runs successfully on GitHub (local checks do not prove CI passes).
- [ ] If publishing `v0.1.0`, label it **pre-release / Codex runtime unverified**; do not advertise Codex/Android/browser/E2E PASS.

## Subsequent Codex evaluation

- [ ] Install exactly one `ui-design` copy; verify `$ui-design` discovery and record Codex version.
- [ ] Run the baseline and candidate cases in `evals/cases.json` using disposable repositories; capture results and relevant tool evidence.
- [ ] Confirm no unauthorized write on `PLAN` or `AUDIT`; no scored result invented; no browser/device PASS from source-only evidence.
- [ ] Separate legitimate design exceptions from true quality defects.
- [ ] Revisit the release status only after multi-case runtime evidence is available; log regressions and improvements in CHANGELOG.

GitHub publication, tags, releases, and production changes must not be automated by this skill itself.
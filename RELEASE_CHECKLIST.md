# GitHub publication checklist

## Historical pre-publication checklist (owner approval)

- [ ] Confirm the proposed destination (`YihongTools/ui-design-skill`) and repository visibility.
- [ ] Confirm **MIT** as the license for original material and **YihongTools** as copyright holder; review `ATTRIBUTION.md`.
- [ ] Review both READMEs and ensure no private data, unpublished repository path, or credential is exposed.
- [ ] Run `python scripts/validate_skill.py` and validator regression tests.
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

## Skill V2 multilingual update

- [x] Canonical V2 `ui-design/SKILL.md` and Traditional Chinese reference in `docs/SKILL.zh-TW.md` present (V2.1 layout).
- [x] Both README language notes make the English file authoritative and describe manual Skill refresh.
- [x] V2 static validation on GitHub Actions: PASS ([run #38335072860](https://github.com/YihongTools/ui-design-skill/actions/runs/38335072860)).
- [ ] Verify Codex reloads the updated Skill (V2); do not treat installation-only evidence as runtime PASS.

## V2.1 local candidate revisions (historical preparation checklist)

The repository is public; these local revisions are not a new published release. See [current evidence history](evals/evidence.md). Historical checklist counts below are retained, not the current test-suite size.

- [x] Canonical Skill updated for four decision/render obligations; reference moved to `docs/`.
- [x] Candidate static validation + 11 tests passed locally.
- [ ] Owner-approved GitHub publication and remote CI.
- [ ] Codex V2.1 behavioral and visual A/B with independent evidence.

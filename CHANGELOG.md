# Changelog

This project uses [Semantic Versioning](https://semver.org/), with pre-1.0 releases indicating that the skill's behavior and evaluation contract may still change.

## [0.2.1] - Unreleased candidate

### Changed

- Clarified VERIFY as a non-editing verification mode by default.
- Revise requires BUILD/FIX scope or explicit fix authorization; the retained VERIFY smoke validates one read-only defect-detection scenario, not all modes.

- Removed A/B-evaluation-specific wording from runtime Skill.
- Centralize functional reporting as `Requirement | Status | Evidence | Notes`; exact English Status values remain machine-checkable even in other response languages, with optional Notes and severity separate from Status. BUILD/FIX and VERIFY reference this single schema.
- Clarify that missing/lost/broken required functionality is a High-severity defect regardless of visual polish; distinguish static information/state verification from required-action/behavior operability.
- Normalized the involved Markdown working files to LF; existing index LF and Markdown attribute policy were preserved.

- Identify brief-defined functional requirements before implementation using a short checklist.
- Check brief-required functionality in actual renders and relevant interactions; do not invent unspecified behaviors or offset functional defects with visual gains.
- Clarify that baseline-only features are not automatically authoritative requirements, including diff highlighting.
- Simplify default exploratory self-use evaluation evidence; reserve stronger provenance for escalated claims or boundaries.

- Greenfield reference fallback: three materially different candidate directions, model-selected rationale, clear user-overridable attribution when no answer is available.
- Page-level default replacement table must cover primary color family, typeface, and overall layout; brief-frozen rows are explicitly marked instead of changed.
- User-visible pre-implementation decision record, without misrepresenting written output as proof of Skill body read.
- Render critique template-like findings must each be changed or intentionally retained with a product-grounded reason, within the existing two-round limit.
- Remove evaluation-runner and A/B-specific instructions from the runtime Skill; keep evaluator assertions in `evals/README.md`.
- Shorten decision and critique steps; distinguish missing greenfield references from missing implementation-critical information in established projects.
- Move Traditional Chinese reference to `docs/SKILL.zh-TW.md` and remove the canonical Skill's cross-reference; relocate repository-authorization rules to Purpose and authority.
- Reject vague "looks fine" / "clean" reasons for intentionally retaining a template-like element; align README and static checks.
- Restore **ask at most three questions** while preserving implementation-critical Owner boundaries; describe transferable attributes of supplied references instead of copying surface details.
- Compare each row of the defaults table with actual renders and close absent replacements in Revise; compare with the selected fallback direction when references are absent.
- Keep the runtime Skill free of evaluation-runner instructions; shorten the pre-edit decision record. Event-log checks are documented in `evals/README.md`.
- Regenerate the `docs/SKILL.zh-TW.md` V2.1 reading copy in sync with the English rules.
- Prevent fabricated **Fixed by brief** exemptions: require an exact brief quote; cite external design-system constraints separately.
- Clarify permitted font stacks and licensed local font sources, including approval for Android `res/font` additions.
- Define substantial redesign narrowly; ensure PLAN surfaces the candidate/reference direction and default-replacement table without expanding localized changes.
- Deduplicate the pre-edit decision record by referring to the greenfield steps.
- Remove the remaining Skill-body-read evaluation sentence from the runtime Skill; retain that instrumentation rule only in `evals/README.md`.
- Scope the full greenfield flow to new/substantially redesigned surfaces without governing design-system authority; localized tweaks follow existing code conventions.
- Allow design-system-governed default rows to collapse to `Design system: <source>` and require full replacement analysis only for uncovered rows, including new screens.
- Split the defaults-table rules into rows/fields, **Fixed by brief**, typography, and Android subsections to reduce instruction density.
- Add unattended typography fallback: use a system font stack when font-file approval is unavailable and record the preferred font only as a suggestion.
- Unify the scope as **Direction and defaults table (greenfield or substantial redesign)**; a fully governed surface skips reference/fallback selection and records compact governed rows, while localized tweaks stay lightweight.
- Clarify that unmodified Material 3 baseline and default Tailwind/shadcn styling do not count as a governing design system.
- Define **brief** as the user's request or a requirements document they supplied, and centralize the `Design system: <source>` compact-row syntax in step 3 instead of repeating it across runtime sections.
- Update the Skill description to say reference-first **or a documented three-direction fallback**.

### Verification status

- Retained VERIFY smoke-003 reassessment: **REASSESSMENT_FINDS_EVALUATOR_DEFECT / corrected PASS** for exact-status High defect detection without source edits. Original results preserved; see [evidence history](evals/evidence.md). The intentional fixture still fails its completion-state requirement.
- Schema/documentation clarification: static validation only; no runtime rerun. No claim that the prior V2.1 A/B regression is fixed or that BUILD quality generally improved.

- Historical candidate R6 local static validation: **PASS**; 22 validator unittests: **PASS**. Codex V2.1 behavior improvement **NOT VERIFIED**. Prior V2 visual A/B remains **INCONCLUSIVE** (user-provided report; not repeated in this preparation).
- Repository is public; no version tags or GitHub Releases as checked on 2026-10-14. Local contract/documentation edits remain uncommitted/unpublished; candidate version is unchanged.

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
- GitHub publication, release/tag, and subsequent Codex evaluation: **NOT DONE** as of package preparation.

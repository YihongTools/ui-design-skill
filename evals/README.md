# Evaluating ui-design

## Default: lightweight exploratory self-use A/B

Use this lightweight path for ordinary exploratory UI comparisons. It does not require the formal multi-case benchmark below.

1. Run `python scripts/validate_skill.py`.
2. Run A (Skill disabled) and B (explicit Skill use) once each with the same brief, initial files, technical constraints, model, effort, authorization, and tool availability, in separate disposable folders. Neither group may read the other's design or output.
3. Record model, effort, Skill version and hash, and artifact paths.
4. Capture actual desktop and mobile screenshots for each group. Check the primary interactions; mark unavailable render or interaction checks **UNVERIFIED**.
5. Use a short brief-functional-requirement checklist:

| Requirement and authority | A: PASS / FAIL / UNVERIFIED | B: PASS / FAIL / UNVERIFIED | Actual evidence |
| --- | --- | --- | --- |
| Required state, action, information, completion or specified error behavior | UNVERIFIED | UNVERIFIED | Pending execution |

Required behavior comes from the brief, governing product requirements, or existing authoritative behavior/design-system contracts. A baseline-only feature is not automatically a requirement. Preserve diff presentation when authoritative; otherwise judge comparison clarity in context, without treating absent highlighting alone as a High requirement failure. A required state, action, information, or behavior that is missing, lost, or broken is a High-severity defect; visual gains cannot offset it.

6. Give a concise screenshot-based comparison of hierarchy, product fit, usability and responsiveness, plus a final result. Distinguish style difference from quality improvement. A single comparison cannot establish repeatable improvement; do not invent scores or human acceptance.

Default evidence does **not** require event-level provenance, a sensory-gate, screenshot-hash decision logs, full event dumps, OS sandbox proof, MCP inventory proof, or a full reproducibility archive. Existing task-specific authority still applies.

**Lightweight evidence is sufficient for exploratory self-use evaluation; stronger provenance is required before making release-level or repeatability claims.**

## When to escalate evidence

Escalate for release-level claims, disputed results, an unresolved regression cause, multi-model or multi-version comparisons, repeatable-improvement claims, or when security/permission boundaries are themselves the evaluation objective. Gather evidence appropriate to that question rather than requiring every archive for every run: tool/event provenance and canonical body-read evidence for process disputes, reproducible inputs and repeated runs for improvement claims, or separate boundary checks for security claims. Human sensory acceptance requires an identified reviewer; automated checks cannot substitute for it.

See [retained evidence history](evidence.md): one VERIFY defect-detection/read-only smoke has corrected acceptance PASS; the V2.1 A/B regression remains historical evidence, not proof of a fixed BUILD. Later schema/documentation clarifications have static validation only. Preserve original reports and their addenda; no general behavioral-improvement claim follows.

## Formal behavioral benchmark (when explicitly requested)

## Goal

Test whether `ui-design` is discovered and actually changes Codex's behavior in the intended way. Static package checks, attractive screenshots, and one successful answer are **not** runtime evidence.

## Scope and baseline

- **Prerequisite:** Install `ui-design` under a supported user/repository Skill directory and confirm Codex can explicitly invoke `$ui-design`.
- **Environment:** Use a disposable copy of `evals/fixtures/web-ui` and `evals/fixtures/intentional-brand` for web cases; use a disposable Android sample project for Android cases if available. Never run FIX/BUILD on production or personal repositories during initial evaluation.
- **Compare baseline vs Skill:** run the same cases, same model/effort, same initial files, same authorization and tool availability (A: skill disabled or not invoked; B: explicitly invoke skill). Record exact version, hash, model/effort, and environment.
- **No live network or dependencies** unless explicitly required and authorized. Avoid private data. No push, merge, release, or migration during evaluation.
- **Behavior:** apply `evals/cases.json` expected properties and unacceptable regressions. Do not treat those descriptions as claims that they already passed.

## Deterministic checks

1. Correct mode selected (`PLAN`, `BUILD`, `AUDIT`, `FIX`, `VERIFY`) and expected edit authorization respected.
2. AUDIT/PLAN cases leave tracked files unchanged (`git status --porcelain` in a fresh fixture repo), and avoid `git` writes or installing packages.
3. Fix/Build cases modify only the authorized surface and do not change package manifests or create irrelevant artifacts.
4. Reports state actual evidence and missing visual/device checks; do not invent commands or screenshots.
5. An intentional brand gradient (fixture) is not automatically a finding based on color alone.
6. `vibe_score` or other numeric scoring is not invented, and no score becomes a CI gate.

## Escalated judged criteria (requires context; not deterministic)

Evaluate with an explicit rubric (0 = fails, 1 = mixed, 2 = good) for **task-specificity**, **visual hierarchy / semantic appropriateness**, **minimum reversible change**, **evidence quality**, and **scope discipline**. Cite actual files/outputs for each score and record exceptions. The rubric is an experimental measure, not calibrated UX truth. Human review and screenshot/device observations are required for render-dependent claims.

## Coverage and acceptance

- Initial cases: web, Android, negative, and boundary; across all five modes. Include both genuine defects and legitimate stylistic choices.
- Regression guard: zero unauthorized writes or scope escapes; no invented device/browser verification; no tool/rule fabrication.
- Skill beneficial only if scored behavior shows repeatable improvement versus baseline **without** a new critical regression, with results from multiple cases rather than a single demo.
- For web visual changes: gather before/after renders at relevant viewport sizes when available; otherwise mark `RENDER NOT VERIFIED`.
- For native Android: real/emulator rendering, font scaling, interaction and accessibility checks are separately required; static text cannot support `DEVICE PASS`.
- Track case ID, baseline/candidate, reproducible input, actual output, deterministic assertions, judged rubric, token/time/tool-cost if observable, unverified layers, and final status.

## Execution outline for future Codex tests

1. `python scripts/validate_skill.py` and `python -m unittest discover -s scripts -p 'test_*.py' -v`.
2. Check skill discovery: Codex must list or accept `$ui-design`; record tool/CLI version.
3. Select first four low-risk cases (EV-01, EV-02, EV-05, EV-09) in fresh disposable worktrees; compare baseline and explicit-skill outcomes.
4. If they pass critical boundaries, run remaining cases. Capture diff, file locations, commands, and render evidence where possible.
5. Report `COMPLETE`, `COMPLETE_WITH_LIMITATIONS`, `PARTIAL`, or `BLOCKED` only for evidence that was actually obtained. Keep discovered defects as follow-ups; do not silently change evaluation cases mid-run.

### Suggested output table

| Case | Skill invoked? | Mode | Unauthorized change? | Core assertions | Render/device | Observed limitations |
| --- | --- | --- | --- | --- | --- | --- |
| EV-01 | NOT RUN | NOT RUN | NOT RUN | NOT RUN | NOT RUN | Pending Codex runtime |

This repository intentionally contains **no fake PASS results or synthetic score claims**.

## Optional escalated V2.1 process follow-up (proposed; not run)

Evaluation-only rules belong here and in the test prompts, **not** in `ui-design/SKILL.md`. Preserve a clean separation between user-facing design behavior and experiment instrumentation. The agent should not be primed with A/B, runner capture, or body-read requirements during normal Skill use.

Do **not** silently change the existing 12 case assertions. For an explicitly requested process evaluation, freeze these as a separate focused set before running them; they are not mandatory archives for the default lightweight path:

- **Unattended greenfield**: with no references and a user instruction such as "you decide", verify three materially different directions, each linked to audience/task; one model-selected option with reasons to reject the other two; clear user-overridable attribution; no invented approval.
- **Page-level replacements**: check three rows covering primary color family, typeface/typography and major-region page layout, each with default, selected alternative/retention, rationale and governing constraint. For a separately frozen brief (the user's request or a requirements document they supplied) explicitly fixing layout, the layout row must say **Fixed by brief**, quote the exact brief sentence, and preserve it. If the brief is silent, that label is not permitted; a design-system rule must cite its own authority. Do not penalize a candidate simply for sharing the required layout or color with baseline; never change an established brand just to manufacture A/B divergence.
- **Pre-implementation observable trace**: record the user-visible direction/references-or-three-options/default table **before** the first file modification. For unattended fallback, the exact marker `Model-selected; user may override` is searchable in the B events (`Select-String -Path .\B-events.jsonl -Pattern 'Model-selected' | Select-Object -First 3` on Windows). Its presence alone proves neither three distinct candidates nor table completion; inspect the surrounding message and order. Written output is evidence of reported process, **not proof that the canonical SKILL.md was read or consumed**. Collect body-read evidence independently; if unobservable, mark UNVERIFIED.
- **Trigger, design-system short-circuit, and fonts**: new/substantially redesigned surfaces use the direction/defaults-table contract; localized tweaks must not be expanded into the full flow. If a real existing design system fully governs the surface, skip direction/reference selection and use `Design system: <source>` for governed rows; only uncovered rows need replacement analysis. Unmodified Material 3 baseline or default Tailwind/shadcn styling does not qualify as a governing design system. For typography, verify that the applied system stack exists or bundled assets were previously approved, licensed, and available offline (Android assets in `res/font`). If no one can approve a new font file, the implementation must use a system stack and any preferred font must remain a suggestion, not an applied claim; a named remote font without permission is not a valid implementation.
- **PLAN completeness**: for greenfield, the visible PLAN must include the supplied references and transferable traits or three candidates with a selected direction, plus all three table rows. For substantial redesign under an existing design system, governed rows may be the compact `Design system: <source>` form and only uncovered rows need full fields; no edits.
- **Rendered-defaults alignment**: for greenfield/substantial redesign, confirm a row-by-row comparison of each applicable primary-color, typeface, and page-layout decision against the actual screenshot, using the selected candidate when references were unavailable. If a chosen replacement is not visible, it is a template-like finding requiring the same disposition. Brief-fixed rows and `Design system: <source>` rows are evaluated for compliance, not forced difference. Do not score this as passed without render evidence.
- **Template critique disposition**: for each explicitly identified template-like critique item, find a final **Changed** entry tied to an actual bounded edit (plus re-render if available) or **Intentionally retained, because ...** tied to a concrete project constraint. A fix to an unrelated usability defect is not sufficient. Reasons such as "looks fine" or "clean" fail the retention assertion unless tied to a specific constraint. Respect the two-round limit.

If an established design system exists but platform or other implementation-critical details are missing, do not treat that as greenfield; score conservative assumptions or a correctly identified decision blocker, not three invented visual directions. Use identical briefs, initial assets, model requests and renderer for A/B. Do not infer stable improvement from one comparison. Record whether the new constraints merely change visible decisions or measurably improve layout and use; run human blind review separately where appropriate.

# Codex runtime evaluation contract (not yet executed)

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

## Judged criteria (requires context; not deterministic)

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
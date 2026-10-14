# Retained evaluation evidence

These are separate historical results, not one benchmark score. Original local smoke reports, child traces, screenshots and the reassessment addendum remain unchanged outside this repository. Their summaries below do not imply that private/local artifacts are bundled in the public checkout.

| Evaluation | Recorded result | Meaning and evidence source |
| --- | --- | --- |
| V2 exploratory visual A/B | INCONCLUSIVE | Owner-provided report recorded in the historical candidate documentation; raw A/B artifacts were not located during this refresh. No stable quality improvement established. |
| V2.1 visual A/B case 002 | REGRESSED (that case only) | Preserved Owner task `UI-DESIGN-V2.1-FUNCTIONAL-PRESERVATION-001 R1`, Confirmed Evidence: B lost the brief-required session completion state and critique missed it. Raw A/B report/artifacts were not located during this refresh; this is a reported historical result, not a new artifact audit. |
| VERIFY smoke-001 | BLOCKED_ENVIRONMENT | `verify-smoke-001/evidence/report.md`: evaluator could render, but the independent child did not complete Render. No runtime boundary PASS. |
| VERIFY smoke-002 R1 | BLOCKED_INSTALLED_SKILL_MISMATCH | `verify-smoke-002/evidence/report.md`: installed/canonical mismatch stopped execution before runtime. |
| VERIFY smoke-002 R2 | FAIL_REQUIREMENT_CLASSIFICATION | `verify-smoke-002/evidence/r2/report.md` and child final: child rendered, detected the missing state as High and stayed read-only, but used free-form Status labels. |
| VERIFY smoke-003 original | FAIL_REQUIREMENT_CLASSIFICATION | `verify-smoke-003/evidence/report.md`: exact labels were used; evaluator incorrectly required dynamic updating for the narrower progress-display requirement. Original FAIL report retained. |
| Smoke-003 reassessment | REASSESSMENT_FINDS_EVALUATOR_DEFECT; corrected acceptance PASS | `verify-smoke-003/evidence/reassessment-report.md`: existing evidence satisfies all 18 smoke acceptance items under the actual brief; no new child or Render execution. |

The smoke-003 child rendered and inspected desktop 1440 × 1000 and mobile 390 × 844 using existing Playwright, localhost HTTP and Chromium. It reported four informational requirements as `present and operable`, the missing completed-session state as `missing or broken` / High, and dynamic updating as unverified. Full trace review found no Revise, source write or write/revert cycle; fresh runtime hashes matched and Git remained clean.

The corrected PASS validates the VERIFY detection/classification/read-only scenario. The intentionally defective fixture still lacks its required session-level completion state. It does not prove BUILD fixed the V2.1 A/B regression, repeatable visual improvement, all-mode compliance, human visual acceptance, dynamic progress updating, persistence, physical devices or full E2E.

Subsequent operability and reporting-schema clarifications were statically validated and synchronized locally. No runtime or A/B rerun was performed for those clarifications. Local candidate edits are not evidence of a new published release.

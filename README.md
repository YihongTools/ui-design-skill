# ui-design

**A product-first design and UI audit skill for Codex.** Plan, build, audit, fix, and verify web and native Android interfaces without mistaking a generic AI-looking style for a usability defect.

> **Release status:** `v0.2.1` (Skill V2.1 unreleased candidate). The [repository is public](https://github.com/YihongTools/ui-design-skill); no version tags or GitHub Releases exist as checked on 2026-10-14. One VERIFY smoke has corrected acceptance **PASS**; this is not a general V2.1 quality or product-feature pass. See [evidence history](evals/evidence.md). Scores are advisory only.
>
> [繁體中文說明](README.zh-TW.md)

## What it does

| Mode | Purpose | Default permission |
| --- | --- | --- |
| `PLAN` | Clarify design direction, content hierarchy, tokens, and acceptance criteria | Read only |
| `BUILD` | Implement an approved UI surface | Edit only authorized scope |
| `AUDIT` | Review quality failures and generic AI-style patterns with evidence | Read only |
| `FIX` | Apply small, reversible corrections to approved findings | Edit only authorized scope |
| `VERIFY` | Test relevant visual and interaction acceptance | Scoped checks, no unsolicited redesign |

V2.1 strengthens the reference-first direction (with a documented three-direction fallback) and bounded **Render → Critique → Revise** loop: an unattended "you decide" request gets three genuinely different directions and a reversible model decision; a page-level table covers primary palette, typography, and major-region layout (label **Fixed by brief** only when the user's request or supplied requirements document states the constraint and is quoted exactly); design decisions must be published before BUILD edits; every template-like critique item ends **Changed** or **Intentionally retained, because ...**. New/substantially redesigned surfaces use the direction/defaults-table section, while localized tweaks follow existing code conventions. A real governing design system may short-circuit governed rows, but unmodified Material 3/Tailwind/shadcn defaults do not count as one; a fully governed surface skips reference/fallback selection and records compact governed rows. Typography uses available system stacks or authorized locally bundled fonts with license evidence; if font-file approval is unavailable, apply a system stack and record the preferred font as a suggestion rather than applied. **Substantial redesign** means a new screen or a change to page-level layout, primary color family, or typeface, not a localized tweak. PLAN reflects the same scoped record. Two render revision rounds at most. The **eight design rules** are: (1) design authority first; (2) deliberate defaults; (3) purposeful decoration; (4) information hierarchy; (5) consistency without rigidity; (6) content-driven layout; (7) functional motion; and (8) evidence-based auditing. They are constraints on design reasoning, **not** bans on individual fonts, colors, gradients, cards, or visual styles.

### Evidence before conclusions

Audits distinguish observed source evidence, rendered observations, and design judgments; `Confirmed`, `Probable`, `Candidate`, and `Exempted` confidence; and `High`, `Medium`, and `Low` severity. A static hint is not proof of a rendered defect. Findings should describe user impact and the smallest useful correction.

Historical evidence remains separate: the exploratory V2 visual A/B was reported **INCONCLUSIVE**; the V2.1 A/B case was reported **REGRESSED**, losing the required session completion state without detecting it in critique. These A/B conclusions come from preserved Owner reports; the original A/B artifacts are not bundled here.

VERIFY progressed from smoke-001's child Render block, through smoke-002 R1's installed-Skill mismatch and R2's successful child rendering/High defect detection with vocabulary failure, to smoke-003's exact vocabulary compliance. Its original evaluator FAIL incorrectly added a dynamic-update requirement; reassessment found an evaluator defect and corrected acceptance to **PASS**. The smoke passed because VERIFY detected/classified the intentional defect and remained read-only; the fixture still lacked its required completion state. See [the distinct results and sources](evals/evidence.md).

Dynamic updates, persistence, physical devices, human visual acceptance and full E2E remain unverified. The reporting-schema clarification has static validation only; no new runtime or A/B run was performed for it.

**Scoring:** This skill does **not** bundle a scoring engine. If the user provides a relevant scanner, its output may be quoted with its methodology and limitations, but scores are not CI gates or a proxy for UX quality.

## Language files

- [`ui-design/SKILL.md`](ui-design/SKILL.md) — canonical English instruction for Codex Skill discovery and execution (V2.1 candidate).
- [`docs/SKILL.zh-TW.md`](docs/SKILL.zh-TW.md) — Traditional Chinese reading reference outside the installed Skill directory. English `SKILL.md` controls.
- When updating an existing Codex installation, replace **`ui-design/SKILL.md`** in the installed Skill directory, then restart Codex or open a new conversation. The repository stores the translation under `docs/`; the standalone Codex ZIP also includes its synchronized copy under `ui-design/SKILL.zh-TW.md` for users updating older installations. Only English `SKILL.md` is executed as the Skill entry point.

## Installation

Prerequisite: a Codex version that supports local Agent Skills. Use the skill directory containing `SKILL.md`; do **not** copy the whole repository into a skill folder.

**From this published GitHub repository:**

```text
$skill-installer install https://github.com/YihongTools/ui-design-skill/tree/main/ui-design
```

Or install locally on Windows with PowerShell 7 or Windows PowerShell 5.1 from a cloned/unpacked checkout:

```powershell
$source = Join-Path (Get-Location) 'ui-design'
$destination = Join-Path $HOME '.agents\skills\ui-design'
if (-not (Test-Path (Join-Path $source 'SKILL.md'))) { throw 'Run from the repository root.' }
if (Test-Path $destination) { throw 'Existing ui-design skill found; do not overwrite.' }
New-Item -ItemType Directory -Force -Path (Split-Path $destination) | Out-Null
Copy-Item -LiteralPath $source -Destination $destination -Recurse
Test-Path (Join-Path $destination 'SKILL.md')
```

The local discovery location follows current Codex skill documentation. If your Codex version uses a different location or the skill isn't listed, check its documentation and restart Codex. Another installer may use `$CODEX_HOME/skills` (usually `~/.codex/skills`); do not install a second copy unless necessary, because duplicate skill names can create ambiguity.

## Usage

```text
$ui-design PLAN — propose a layout using the existing design system; do not edit files.
$ui-design AUDIT — review this screen, cite file/line evidence, and do not modify code.
$ui-design BUILD — implement only the approved settings screen and verify it.
$ui-design FIX — address confirmed finding UI-03 with the smallest reversible change.
$ui-design VERIFY — check this changed screen; state unverified browser/device layers.
```

For implicit invocation (when not named explicitly), the skill's frontmatter describes the appropriate UI tasks. It should not activate for backend-only changes.

## Repository layout

```text
ui-design/
  SKILL.md                  # The only installed Skill instruction
docs/
  SKILL.zh-TW.md            # Optional human-readable translation
scripts/
  validate_skill.py         # Standard-library, static format/contract check
  test_validate_skill.py    # Validator regression tests
evals/
  README.md                 # Proposed Codex runtime evaluation procedure
  cases.json                # Evaluation contract, not run results
  fixtures/                 # Small web-only example surfaces
.github/workflows/
  validate.yml              # Static checks only
```

## Validation and status

From repository root:

```sh
python scripts/validate_skill.py
python -m unittest discover -s scripts -p 'test_*.py' -v
```

These checks validate packaging and explicit Skill contract markers; they **cannot** establish that Codex invokes the skill correctly or improves a rendered UI. Follow [the evaluation contract](evals/README.md) for a real Codex test after publication/local installation. See [CHANGELOG](CHANGELOG.md).

## Scope and attribution

- Instruction-only Skill: no vendored scanners, remote model calls, network dependencies, or generated assets.
- Native Android guidance is platform-aware; Web CSS heuristics are not accepted as proof of native UI quality.
- Inspired by [Anthropic's `frontend-design`](https://github.com/anthropics/skills/tree/main/skills/frontend-design) and [`anti-ui-slop` in ritmex-skills](https://github.com/discountry/ritmex-skills/tree/main/skills/anti-ui-slop). This repository is **not affiliated with or endorsed by either project**. No upstream script or rule catalog is bundled. See [ATTRIBUTION.md](ATTRIBUTION.md).
- Original material in this repository is offered under the [MIT License](LICENSE). The repository owner approved MIT licensing for the original material on 2026-10-13.

## Project governance

`AUDIT` is read-only by default. Any file edit, network/dependency addition, architectural redesign, PR, push, release, or destructive operation requires its own authorization. Build PASS is not UI PASS, and a static score is not user acceptance.

# ui-design

**A product-first design and UI audit skill for Codex.** Plan, build, audit, fix, and verify web and native Android interfaces without mistaking a generic AI-looking style for a usability defect.

> **Release status:** `v0.1.0` — packaged and statically checked. Real Codex runtime evaluations, browser/device checks, and end-to-end UI verification have **not** been completed. Scores are advisory only.
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

The **eight design rules** are: (1) design authority first; (2) deliberate defaults; (3) purposeful decoration; (4) information hierarchy; (5) consistency without rigidity; (6) content-driven layout; (7) functional motion; and (8) evidence-based auditing. They are constraints on design reasoning, **not** bans on individual fonts, colors, gradients, cards, or visual styles.

### Evidence before conclusions

Audits distinguish `SOURCE`, `RENDER`, and `JUDGMENT` evidence; `Confirmed`, `Probable`, `Candidate`, and `Exempted` confidence; and `Critical`, `High`, `Medium`, and `Low` severity. A static hint is not proof of a rendered defect. Findings should describe user impact and the smallest useful correction.

**Scoring:** This skill does **not** bundle a scoring engine. If the user provides a relevant scanner, its output may be quoted with its methodology and limitations, but scores are not CI gates or a proxy for UX quality.

## Installation

Prerequisite: a Codex version that supports local Agent Skills. Use the skill directory containing `SKILL.md`; do **not** copy the whole repository into a skill folder.

**From this GitHub repository:**

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
  SKILL.md                  # Codex reads this
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
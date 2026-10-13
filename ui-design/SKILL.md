---
name: ui-design
description: Plan, build, review, and visually verify product-specific Web or native Android (Jetpack Compose) UI, using a reference-first direction step and a render-critique-revise loop to avoid generic AI-default looks. Use this skill whenever the user asks for UI/UX layout, screen design, styling, component design, a UI review, or says things like "make this look better", "the UI looks AI-generated", "redesign this screen", 美化介面, 畫面設計, 介面太像 AI 做的, even if they never say "design". Do not trigger for backend-only work or non-UI code review.
---

# UI Design (V2: opinionated, verifiable, lightweight)

## Purpose and authority

Improve a UI's product fit, information hierarchy, consistency, usability, and accessibility. Reducing an "AI-generated look" is a side effect, never a substitute for usability or the user's requirements.

When instructions conflict, follow them in this order:
1. The user's explicit instructions and the scope of the current task.
2. Product requirements, the existing design system and brand tokens, platform conventions, and accessibility requirements.
3. Existing components and established interaction behavior.
4. The preferences in this skill.

Do not treat an intentional brand choice as a defect. Do not silently expand scope. Do not add dependencies, remote fonts, generated imagery, or broad design-system changes without the user's approval.

## Modes

- **PLAN**: Propose direction, layout, tokens, and acceptance criteria. Do not edit files.
- **BUILD**: Implement the requested surface, then run the render feedback loop.
- **AUDIT**: Read-only. Report findings; do not edit files, install packages, or generate assets. An audit is not authorization to fix.
- **FIX**: A narrowed BUILD. Address only confirmed defects or defects the user named, with the smallest reversible change.
- **VERIFY**: Run only the render feedback loop. No unrelated redesign.

For mixed requests, keep the phases distinct: PLAN → authorized BUILD/FIX → VERIFY. In an existing project, inspect the named or changed UI files first and follow only the tokens and components needed to understand them. Exclude vendored code, generated code, snapshots, and intentional anti-pattern demos.

## Eight principles

1. **Design authority first.** Respect the established design system, brand, platform, and user requirements. Never redesign just to erase AI-looking styling.
2. **Choose defaults deliberately.** Do not blindly reproduce Tailwind, shadcn, or Material 3 defaults. If you keep one, say why it fits this product.
3. **Decoration has a job.** Use gradients, shadows, glow, blur, ornament, and illustration only for branding, grouping, state, affordance, or necessary emphasis.
4. **Hierarchy before containers.** Build hierarchy with type scale, spacing, contrast, alignment, and content order first. Use cards only when they improve grouping or interaction; avoid cards inside cards.
5. **Consistent, not rigid.** Reuse tokens and component roles. Without project evidence, do not impose universal fonts, palette ratios, or bans on specific colors.
6. **Content decides layout.** Pick table, list, steps, editorial flow, form, or dashboard based on the information and the task. Do not default to a centered hero with three feature cards and a call to action. For long-reading screens, prioritize line length, line height, and the visual weight of secondary information such as timestamps.
7. **Motion serves function.** Use motion to explain an action, a state change, or spatial continuity. Avoid entrance animations everywhere and decorative hover zoom. Honor reduced-motion settings.
8. **Findings need evidence.** Never invent a location, viewport result, accessibility test, or before/after comparison.

## When critical information is missing

If missing information would materially change the design (usage context, reference style, whether a design system exists, target platform), ask the user first, with at most three questions, instead of guessing. For minor gaps, proceed under clearly stated assumptions and say how the result changes if an assumption is wrong.

## When there is no existing design system (greenfield)

The goal is a result with a recognizable identity that does not sacrifice usability. Work through these steps in order:

1. **Direction sentence.** `[Product/audience] should feel [specific qualities]; [primary content or action] takes priority; [constraints] shape the form.` "Clean, modern, intuitive" is not specific; the qualities must distinguish this product from others.
2. **References.** Ask the user for 2–3 references they like (screenshots or names). If they have none, offer three directions to choose from. State what is transferable from each reference (type personality, density, color logic, whitespace, layout structure) rather than copying surface details.
3. **Default-replacement table.** List the three defaults most likely to appear for this kind of screen (the most common choices for typography, color, and layout). For each, write what replaces it and why. If you decide to keep a default, say why it is right here.
   - Android/Compose: the project template ships with the Material 3 baseline purple scheme and the default typeface. Replace them explicitly, or justify keeping them. If you do not use dynamic color, turn it off explicitly.
4. **One signature decision.** For each major screen, choose one memorable thing (an unusual type-scale contrast, a dense layout, a strictly applied single accent color, a non-centered layout structure) and keep everything else quiet. Do not push hard everywhere.
5. **Small, complete tokens.** Color roles (background, surface, primary text, secondary text, accent, status colors), type roles, spacing, and radii. Create new tokens only when no authoritative source exists and the scope allows it.

Distinctiveness must not cost readability, contrast, touch targets, or platform familiarity. Adding arbitrary asymmetry just to look different is also a failure.

## PLAN / BUILD procedure

1. Define the surface and its primary task, real content, constraints, and what must stay unchanged.
2. For a new or substantially redesigned surface, follow the greenfield steps above. If a design system exists, reuse it and write a one-sentence direction.
3. Check the plan for accidental template defaults and for conflicts with the task.
4. Implement the smallest coherent surface. Preserve routes, data semantics, localization, and existing responsive behavior.
5. Run the render feedback loop. For a small, local change, render only the affected screen.

## Render feedback loop (Render → Critique → Revise)

Required after BUILD or FIX. VERIFY is just this section.

1. **Render.** Get the actual screen by whatever means the environment offers, and actually open and look at the image. Do not imagine it from the code.
   - Web: headless-browser screenshots, at least one narrow (about 390 px) and one wide.
   - Android: Compose `@Preview` or the project's existing screenshot tests; or on an emulator or device, `adb shell screencap -p /sdcard/screen.png` followed by `adb pull /sdcard/screen.png`. (In Windows PowerShell, do not redirect binary output with `>`; it corrupts the image.) For dark mode, run `adb shell cmd uimode night yes` and capture again.
   - If the environment cannot render, state "visual not verified" and fall back to a source-level self-critique. Never claim a visual pass.
2. **Critique.** Compare against the direction sentence and the references, and write concrete observations:
   - The two spots that look most like a default template.
   - The one issue that most hurts usability (contrast, touch target, hierarchy, truncation or overflow, long-text readability).
   - Whether the signature decision is actually visible.
   Tie each observation to a place on the screen. "Overall more polished" is not an observation.
3. **Revise.** Change only what the critique points to, then render again. At most two rounds unless the user asks for more. If problems remain after round two, list them as known limitations instead of polishing indefinitely.
4. **Report.** Include the screenshot paths, what changed, what visibly differs, and what was not verified.

## AUDIT

Inspect in this order:
1. Quality defects: missing or hidden content, broken assets, overflow, unusable controls, invisible focus, insufficient contrast or readability, small touch targets, motion and accessibility problems.
2. Design-system alignment: tokens, type hierarchy, density, spacing, components, state semantics.
3. AI-default convergence: repetitive generic cards, unearned gradients, glow, or glass, template hero-and-CTA composition, empty icons and copy, animation everywhere. A fashionable font or color by itself is not a finding.

Write each finding on one line: `Location · What was seen · User impact · Minimal change · Severity (High/Medium/Low) · Confidence (Confirmed/Probable/Candidate)`.
- Anything that needs actual rendering to judge is a `Candidate` until rendered; never present a Candidate as confirmed.
- Intentional, brand-authorized, or platform-appropriate choices are `Exempted` and omitted from the findings.
- Severity reflects real impact, not how much something resembles AI output. High = blocks a primary flow or clearly breaks accessibility; Medium = a localized usability or consistency issue; Low = cosmetic polish.
- With only one or two findings, use a short paragraph instead of a table. Merge multiple symptoms of one root cause into one finding.

## Output

Reply in the language the user writes in; if unclear, use English. Keep code, identifiers, file paths, and command lines in their original form. Keep the length proportional to the task.
- **PLAN**: the direction sentence, the authorities relied on, the layout/token/component approach, open decisions for the user, and checkable acceptance criteria.
- **BUILD/FIX**: files changed, visual and interaction changes, render evidence, known limitations. Distinguish "implemented" from "verified".
- **AUDIT**: findings ordered by impact, with the scope and evidence limits stated.
- **VERIFY**: the viewports, devices, and commands actually used, observed results, and what remains unverified.

Never claim a visual, device, or end-to-end pass based only on static code, mocks, unit tests, or a successful build. Do not say you did something you did not run.

## Scoring (advisory only)

This skill has no built-in scoring and must not invent scores or claim a scan ran. If the user provides a scanner, cite its tool name, version, scope, and known blind spots. A high "AI-look" count does not mean poor usability, and real usability and accessibility defects always take priority.

## Related approaches (not dependencies)

This skill is an independently usable synthesis informed by Anthropic's `frontend-design` and the `anti-ui-slop` skill in ritmex-skills. Do not assume either is installed; read or invoke one only when it is actually available and clearly useful. If their advice conflicts with the priority order or the eight principles above, follow this skill.

## Traditional Chinese reference

For a Traditional Chinese reading copy, see [`SKILL.zh-TW.md`](SKILL.zh-TW.md) in this directory. The English `SKILL.md` is the authoritative Skill instruction. The translated file is reference-only: it is not a separate Skill, is not automatically loaded as the canonical instruction, and does not override this file.

Repository writes, commits, pushes, merges, releases, and destructive operations require explicit authorization separate from a UI design task.

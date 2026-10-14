---
name: ui-design
description: Plan, build, review, and visually verify product-specific Web or native Android (Jetpack Compose) UI, using a reference-first direction step (or a documented three-direction fallback) and a render-critique-revise loop to avoid generic AI-default looks. Use this skill whenever the user asks for UI/UX layout, screen design, styling, component design, a UI review, or says things like "make this look better", "the UI looks AI-generated", "redesign this screen", 美化介面, 畫面設計, 介面太像 AI 做的, even if they never say "design". Do not trigger for backend-only work or non-UI code review.
---

# UI Design (V2.1: opinionated, verifiable, lightweight)

## Purpose and authority

Improve a UI's product fit, information hierarchy, consistency, usability, and accessibility. Reducing an "AI-generated look" is a side effect, never a substitute for usability or the user's requirements.

When instructions conflict, follow them in this order:
1. The user's explicit instructions and the scope of the current task.
2. Product requirements, the existing design system and brand tokens, platform conventions, and accessibility requirements.
3. Existing components and established interaction behavior.
4. The preferences in this skill.

Do not treat an intentional brand choice as a defect or silently expand scope. Do not add dependencies, generated imagery, or broad design-system changes without approval. For typography sources and font-file approval, see the direction/defaults-table step 3. Repository writes outside the authorized UI files, commits, pushes, merges, releases, and destructive operations require separate explicit authorization.

## Modes

- **PLAN**: Propose direction, layout, tokens, and acceptance criteria. Do not edit files.
- **BUILD**: Implement the requested surface, then run the render feedback loop.
- **AUDIT**: Read-only. Report findings; do not edit files, install packages, or generate assets. An audit is not authorization to fix.
- **FIX**: A narrowed BUILD. Address only confirmed defects or defects the user named, with the smallest reversible change.
- **VERIFY**: Read-only verification by default: run Render and Critique and report. VERIFY is not fix authorization; Revise applies only under BUILD/FIX or when the user explicitly authorizes fixes. No unrelated redesign.

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

Use an existing design system as authority, even when some details are missing. If material information is missing and the user can answer, **ask at most three questions**. When references or reversible greenfield direction are missing and no answer is available, use step 2's three-direction fallback; do not manufacture user approval. If implementation-critical facts (such as the target platform, security boundary, or an irreversible change) are missing, **stop before edits** and name the required decision instead of treating it as a visual-direction choice. For minor gaps, state reasonable assumptions and proceed within authorized scope.

## Substantial redesign threshold

**Substantial redesign** means a new screen, or a change to page-level layout, primary color family, or typeface. Localized styling, spacing, or component tweaks alone are not substantial. This definition controls the decision record, defaults table, and render-to-table critique. **Unmodified framework or template defaults** (for example Material 3 baseline or default Tailwind/shadcn) do **not** count as a governing design system.

## Direction and defaults table (greenfield or substantial redesign)

Use this section when creating or substantially redesigning a surface; localized tweaks follow the existing code's conventions. If no governing design system covers the surface, work through steps 1–5. If an established design system fully governs the surface, skip steps 1–2 and use step 3's compact governed-row form; steps 4–5 apply only where the system leaves room for screen-specific decisions.

1. **Direction sentence.** `[Audience/product] should feel [specific qualities]; [primary task] comes first; [constraints] shape the result.` Avoid vague labels such as "clean and modern."
2. **References or fallback.** Ask for 2–3 references when someone can answer. If none are provided, the user says "you decide," or no one can respond, do not skip this step: propose three materially different directions (not just three colors), each with one sentence relating typography, palette, information density or major layout to the target audience and task. Choose one, explain why the other two are less suitable, and label it **Model-selected; user may override**. Never imply user approval. If references are supplied, state what is transferable from each (type personality, density, color logic, layout structure) and do not copy surface details. Follow any binding brand/design system authority.
3. **Page-level defaults table.**
   - **Rows and fields.** Cover three rows: **color (including primary color family)**, **typeface / typography**, and **page-level layout structure**. For each uncovered row record default → chosen alternative or deliberate retention → audience/task reason → authority. Layout means overall major-region placement, not card styling. If an existing design system governs a row, use the compact form `Design system: <source>` and do not invent a replacement just to be different.
   - **Fixed by brief.** Here brief means the user's request or any requirements document they supplied. Mark a row **Fixed by brief** only if the brief states the constraint explicitly; **quote the exact sentence** in that row. Do not infer a brief constraint. A design-system rule must cite its own source instead.
   - **Typography.** Use an available system font stack or an already-authorized locally bundled font; record the license for bundled fonts. Do not fetch a remote font or add a font file without approval, including Android `res/font`. If no one can approve a font file, apply a system font stack and record the preferred font as a suggestion, not as applied.
   - **Android/Compose.** Replace Material 3 template colors and default typeface or justify keeping them; explicitly disable dynamic color if unused.
4. **Signature decision.** Choose one distinctive, task-serving feature per major screen; keep other choices restrained.
5. **Tokens.** Define only needed color, type, spacing, and radius roles unless an established system already supplies them.

Distinctiveness must not undermine readability, contrast, touch targets, or platform conventions.

**Pre-implementation decision record.** Before edits, publish the applicable direction and step 3 decisions in the **user-visible response**. Use step 3's compact form for governed rows; only uncovered rows need the full record. When the choice was delegated, continue within authorized scope without waiting for visual-direction approval.

## PLAN / BUILD procedure

1. Define the surface and its primary task, real content, constraints, and what must stay unchanged. Identify functional requirements stated in the brief: required states, actions, information shown, completion behavior, and error behavior when specified. A short checklist is enough for a simple screen; do not invent unspecified features or require a large requirements document. Required behavior comes from the brief, governing product requirements, or existing authoritative behavior/design-system contracts.
2. For a new or substantially redesigned surface, follow the direction/defaults-table section above. Existing design-system constraints use step 3's compact governed-row form; expand only uncovered rows. Cite explicit brief constraints rather than labeling an inferred preference Fixed by brief. Localized tweaks do not need the full table.
3. Check the plan for accidental template defaults and for conflicts with the task.
4. Implement the smallest coherent surface. Preserve routes, data semantics, localization, and existing responsive behavior.
5. Run the render feedback loop. For a small, local change, render only the affected screen.

## Render feedback loop (Render → Critique → Revise)

Required after BUILD or FIX. VERIFY runs steps 1, 2, and 4; step 3 Revise applies only under BUILD/FIX or when fixes are explicitly authorized. Severity, confirmed regression, small scope, or reversibility do not grant fix authorization.

1. **Render.** Get the actual screen by whatever means the environment offers, and actually open and look at the image. Do not imagine it from the code.
   - Web: headless-browser screenshots, at least one narrow (about 390 px) and one wide.
   - Android: Compose `@Preview` or the project's existing screenshot tests; or on an emulator or device, `adb shell screencap -p /sdcard/screen.png` followed by `adb pull /sdcard/screen.png`. (In Windows PowerShell, do not redirect binary output with `>`; it corrupts the image.) For dark mode, run `adb shell cmd uimode night yes` and capture again.
   - If the environment cannot render, state "visual not verified" and fall back to a source-level self-critique. Never claim a visual pass.
2. **Critique.** Compare against the direction sentence and the references **or the selected candidate direction**, and write concrete observations:
   - Confirm every identified functional requirement remains present and operable in the render. Do not require an interaction check for a requirement that only specifies visible information or a static state. For a required action or behavior, verify operability when possible; if that required behavior is not exercised, mark it unverified. A required state, action, information, or behavior that is missing, lost, or broken is a **High-severity defect**, regardless of improvements in layout, typography, color, or template reduction.
   - The two spots that look most like a default template.
   - The one issue that most hurts usability (contrast, touch target, hierarchy, truncation or overflow, long-text readability).
   - Whether the signature decision is actually visible.
   - For greenfield or substantial redesign, **check each applicable row of the defaults table against the render**. A chosen replacement that is not visible on screen counts as a template-like item and must be closed in Revise. For brief-fixed or design-system-governed rows, evaluate compliance as defined in step 3 rather than forcing a replacement. Without a render, state **visual not verified**.
   Tie each observation to a place on the screen. "Overall more polished" is not an observation.
3. **Revise.** Only under BUILD/FIX or explicit fix authorization. Restore required functionality before visual polish. Close each template-like item named in the critique as **Changed** (cite the edit) or **Intentionally retained, because ...** (cite a concrete product, brief, brand, or usability fact). "Looks fine" or "clean" is not a reason. A functional fix does not close a separate template critique. Re-render after changes when possible; use at most two revision rounds and report remaining issues.
4. **Report.** Give screenshot paths, observable changes, the status of each identified functional requirement (present and operable / missing or broken / unverified), unverified checks, and each template-like item's disposition. For every identified functional requirement, the Status field must be exactly one of `present and operable`, `missing or broken`, or `unverified`; do not substitute synonymous or free-form labels, including translations. Put additional explanations in Evidence or Notes, not in Status. Never claim rendered improvement without an actual render.

## AUDIT

Inspect in this order:
1. Quality defects: missing or hidden content, broken assets, overflow, unusable controls, invisible focus, insufficient contrast or readability, small touch targets, motion and accessibility problems.
2. Design-system alignment: tokens, type hierarchy, density, spacing, components, state semantics.
3. AI-default convergence: repetitive generic cards, unearned gradients, glow, or glass, template hero-and-CTA composition, empty icons and copy, animation everywhere. A fashionable font or color by itself is not a finding.

Write each finding on one line: `Location · What was seen · User impact · Minimal change · Severity (High/Medium/Low) · Confidence (Confirmed/Probable/Candidate)`.
- Anything that needs actual rendering to judge is a `Candidate` until rendered; never present a Candidate as confirmed.
- Intentional, brand-authorized, or platform-appropriate choices are `Exempted` and omitted from the findings.
- Severity reflects real impact, not how much something resembles AI output. High = lacks or loses required functionality, blocks a primary flow, or clearly breaks accessibility; Medium = a localized usability or consistency issue; Low = cosmetic polish.
- With only one or two findings, use a short paragraph instead of a table. Merge multiple symptoms of one root cause into one finding.

## Output

Reply in the language the user writes in; if unclear, use English. Keep code, identifiers, file paths, and command lines in their original form. Keep the length proportional to the task.
- **PLAN**: the direction sentence, authorities, layout/token/component approach, open decisions, and checkable acceptance criteria. For greenfield or substantial redesign, include the supplied references and transferable traits **or three candidate directions with the selected choice** when step 2 applies, plus the step 3 three-row defaults table. Governed rows may use step 3's compact form; no edits.
- **BUILD/FIX**: files changed, visual and interaction changes, render evidence, the status of each identified functional requirement (present and operable / missing or broken / unverified) using the exact Status field contract in Report, and known limitations. Distinguish "implemented" from "verified".
- **AUDIT**: findings ordered by impact, with the scope and evidence limits stated.
- **VERIFY**: the viewports, devices, and commands actually used, the status of each identified functional requirement (present and operable / missing or broken / unverified) using the exact Status field contract in Report, with a severity for any missing or broken one, observed results, and what remains unverified.

Never claim a visual, device, or end-to-end pass based only on static code, mocks, unit tests, or a successful build. Do not say you did something you did not run.

## Scoring (advisory only)

This skill has no built-in scoring and must not invent scores or claim a scan ran. If the user provides a scanner, cite its tool name, version, scope, and known blind spots. A high "AI-look" count does not mean poor usability, and real usability and accessibility defects always take priority.

## Related approaches (not dependencies)

This skill is an independently usable synthesis informed by Anthropic's `frontend-design` and the `anti-ui-slop` skill in ritmex-skills. Do not assume either is installed; read or invoke one only when it is actually available and clearly useful. If their advice conflicts with the priority order or the eight principles above, follow this skill.

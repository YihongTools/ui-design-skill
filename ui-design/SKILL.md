---
name: ui-design
description: Plan, build, audit, refine, and verify product-specific Web or native Android UI with design-system authority, eight intentional-design rules, evidence-based anti-slop review, and scoped verification. Use for UI/UX layouts, visual styling, component design, UI reviews, or requests to remove generic AI-looking design; do not trigger for backend-only work or unrelated code reviews.
---

# UI Design — Build + Audit + Evidence

## Purpose and authority

Improve a UI's product fit, information hierarchy, consistency, usability, and accessibility. Reducing an "AI-generated look" is a secondary goal, not a substitute for usability or the product brief.

Apply authority in this order:
1. Explicit Owner decisions and the current task's scope/acceptance contract.
2. Authoritative product requirements, existing design system, brand tokens, platform conventions, and accessibility requirements.
3. Existing component patterns and established UI behavior.
4. The general design preferences in this skill.

When these conflict, honor the higher authority. Do not reinterpret an intentional brand choice as a defect simply because it appears in an anti-pattern list. Follow project/global engineering instructions and never expand scope silently.

## Select the operating mode

- **PLAN** — Asked for direction, wireframes, alternatives, or a design plan: inspect only the necessary context; propose a concise design direction and acceptance criteria. Do not edit code unless authorized.
- **BUILD** — Asked to create a new UI or implement an approved design: plan briefly, then implement only the requested surface.
- **AUDIT** — Asked to review, rate, diagnose, or find AI-slop: read-only by default. Report findings; do not edit, install packages, or generate assets.
- **FIX** — Asked to correct UI defects or polish a specified surface: use the approved findings/requirements, implement minimal reversible changes, and verify. Do not treat an audit alone as authorization to fix.
- **VERIFY** — Asked to check implementation or a UI change: run bounded, relevant checks, record observed evidence, and report remaining unverified layers. No unrelated redesign.

For mixed requests, keep phases distinct: PLAN → authorized BUILD/FIX → VERIFY. For existing projects, inspect changed or named UI files first; follow only the shared tokens, styles, and components needed to understand them. Exclude vendored/generated code, snapshots, and intentional anti-pattern demos from ordinary audit counts.

## Eight governing rules

1. **Design authority first.** Respect established design system, brand, platform, and Owner requirements. Never redesign merely to erase recognizable AI styling.
2. **Choose defaults deliberately.** Do not blindly reproduce Tailwind/shadcn/framework defaults. Keep them if appropriate to this product; explain any material departure from established patterns.
3. **Decoration has a job.** Use gradients, shadows, glow, blur, ornament, icons, and illustration only where they provide branding, grouping, state, affordance, or useful emphasis. Avoid decoration added just to look polished.
4. **Information hierarchy comes first.** Prefer typography, spacing, contrast, alignment, and content order. Introduce cards/containers only when they improve grouping or interaction; avoid gratuitous card-in-card nesting.
5. **Consistent, not rigid.** Reuse tokens and component roles for color, type, spacing, radii, icons, and controls. Do not impose universal fonts, palette ratios, radius sizes, or ban specific colors without project evidence.
6. **Content-driven layout.** Choose table, list, steps, editorial flow, form, dashboard, or cards based on information and user tasks. Do not default to a centered hero + three feature cards + CTA or add arbitrary asymmetry for uniqueness.
7. **Functional motion only.** Prefer motion that explains user action, state, or spatial continuity. Avoid blanket entrances, hover zoom, and gratuitous scroll effects; honor reduced-motion preferences and platform conventions.
8. **Evidence before findings or fixes.** An audit finding needs a location, observed evidence, user impact, confidence, severity, minimal suggestion, and applicable exemption. Static pattern matches are candidates until the relevant context or rendered behavior supports the claim.

## PLAN / BUILD procedure

1. Define the surface and its primary task, audience, real content, constraints, and authoritative visual/interaction contracts. Identify what must remain unchanged.
2. For a new or materially redesigned surface, write a **one-sentence direction**: `[product/audience] should feel [qualities]; [primary content/action] takes priority; [constraints] shape the UI`. Offer only materially distinct alternatives if an Owner decision is needed.
3. Draft a minimal design plan: hierarchy/content order, layout at relevant viewports, typography roles, color roles/tokens, component states, accessibility considerations, and interaction feedback. Reuse existing design tokens; invent a new token scheme only when there is no authoritative one and scope permits.
4. Critique the plan for accidental template defaults and for conflicts with the task. Distinctiveness alone does not justify sacrificing clarity, task efficiency, or platform familiarity.
5. Implement the smallest coherent surface. Preserve routes, contracts, data semantics, localization, primary interactions, and existing responsive behavior unless explicitly in scope. Do not add dependencies, remote fonts, generated imagery, or broad design-system changes without approval.
6. Verify affected UI behavior and report the result as specified below. For small/local edits, keep the planning step proportionate; do not create formal design artifacts without a need.

## AUDIT procedure and evidence model

Inspect in this order, staying within scope:
1. **Quality failures:** missing/hidden content, broken assets, overflow, unusable controls, misleading copy, weak focus visibility, contrast/readability issues, poor touch targets, motion/accessibility problems.
2. **Design-system alignment:** visual tokens, typography hierarchy, density, spacing, responsive conventions, component consistency, state semantics.
3. **AI-default convergence:** repetitive generic cards, excessive decoration, unearned gradients/glow/glass, template hero/CTA composition, empty icons or labels, generic copy, animation applied everywhere. A fashionable font/color/card by itself is NOT a finding.
4. **Whole-surface composition:** repeated patterns that crowd out the product's actual information or tasks. Consolidate multiple symptoms of one underlying issue into one finding.

Label the **evidence layer**:
- `SOURCE`: direct evidence from file/selector/component/text, with path and line or other precise locator.
- `RENDER`: requires computed layout, screen size, visual contrast, or interaction. Confirm with an actual preview/screenshot/device; without one, mark `Candidate / render not verified`.
- `JUDGMENT`: depends on product fit or composition. Give at least two concrete observations and explain why the choice harms this UI.

Label **confidence** separately from severity:
- `Confirmed`: directly observable defect or unambiguous, context-checked source/render evidence.
- `Probable`: convincing local combination, but not all dependent evidence is observed.
- `Candidate`: weak indicator or insufficient context/render evidence; never present as confirmed.
- `Exempted`: intentional, brand-authorized, semantically useful, or platform-appropriate design; normally omit from actionable findings.

Label **severity** by actual impact, not how much a style resembles AI output:
- `Critical`: blocks access/use, hides essential content, or materially breaks accessibility.
- `High`: substantially impairs a primary flow or pervasive comprehension.
- `Medium`: localized usability/consistency issue, or repeated generic design with demonstrated product mismatch.
- `Low`: cosmetic refinement with little user impact.

Never fabricate an issue location, viewport result, accessibility test, or before/after improvement. Separate quality defects from aesthetic/convergence suggestions. Present unverified candidates apart from confirmed defects.

## FIX and verification procedure

1. Start from an authorized task or confirmed finding. Identify the likely cause in effective tokens, component variants, markup, or layout; distinguish symptoms from causes.
2. Make the smallest reversible change that addresses the cause. Repeated issues may warrant a scoped shared-token/component fix only if allowed by current task authority. Keep unrelated patterns unchanged.
3. For Web UI, check affected responsive viewports, overflow, keyboard focus, readable copy, semantics, motion preference, and the actual rendered surface where tooling permits.
4. For native Android UI, use Android/platform design authority; check applicable screen sizes, font scaling, TalkBack/content descriptions, touch targets, state changes, dark mode, and device/emulator rendering where available. Do not apply Web CSS scanners to Kotlin/Compose/XML as if they validate native UI.
5. Run proportionate focused tests/build/lint, inspect diff and working-tree status, and compare the acceptance layer (visual and interactive behavior), not merely compilation. Record what was actually run and what could not be checked.
6. Never claim rendered/device/E2E PASS based solely on static code, mocks, unit tests, or build PASS. Keep unverified items explicit. No merge, push, release, or destructive action without separate authority.

## Optional scoring — advisory only

- This skill contains **no automatic scanner and no built-in numeric score**. Do not invent scores or report that a scan ran when it did not.
- If the user explicitly requests scoring and an available scanner supports the target platform, report the exact tool/version, scoped inputs, raw severity counts, calculation, exceptions, and known blind spots.
- A higher "AI-look" count is not proof of lower usability or visual quality. Compare scores only across the same tool/configuration and comparable scope. Do not use an uncalibrated threshold as a CI gate, acceptance criterion, or mandatory redesign trigger.
- Actual usability/accessibility defects retain priority over aesthetic scores.

## Output contract

Use concise Traditional Chinese (Taiwan) unless the user requests otherwise. Make the response proportional to the task.

- `PLAN`: chosen direction, existing authority, proposed layout/token/component approach, open Owner decisions, and measurable acceptance.
- `BUILD/FIX`: scope and modified files; intended visual/interaction changes; test/render evidence; known limitations; delivery state. Distinguish implemented from verified.
- `AUDIT`: actionable findings ordered by impact. For each: `ID | Location | Type (Quality/Convergence) | Evidence layer | Confidence | Severity | Observation | User impact | Minimal change | Exemption/constraint | Needed verification`. For a clean or unverified audit, explicitly state its scope and evidence limits. Do not produce a large table when there are only one or two findings.
- `VERIFY`: acceptance checked, commands/devices/viewports actually used, outcomes, outstanding risks, and status (`COMPLETE`, `COMPLETE_WITH_LIMITATIONS`, `PARTIAL`, `BLOCKED`, or `NEEDS_OWNER_DECISION`) with evidence.

Prefer a single discriminating next check over broad unbounded exploration. If new evidence would alter a requirement, architecture, security boundary, persisted schema, or product semantics, stop that change and request an Owner decision; do not silently expand the task.

## Related design approaches (not dependencies)

This is an independently usable synthesis, informed by:
- `frontend-design`: https://github.com/anthropics/skills/tree/main/skills/frontend-design
- `anti-ui-slop`: https://github.com/discountry/ritmex-skills/tree/main/skills/anti-ui-slop

Do not assume those skills, their rule catalogs, or a scoring script are installed. Only read or invoke an external skill when actually available and materially useful for the requested task. Follow the higher-priority authority and the eight rules above if advice conflicts.
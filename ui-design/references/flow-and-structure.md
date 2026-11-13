# Flow and structure

Read this before deciding what a screen contains, in what order, and how screens connect. Most "confusing" screens are structurally wrong, not badly styled, and styling cannot rescue them.

## Start from the person, not the data

For each screen, write three short lines before drawing anything:

- **Arrives knowing:** what the person already knows or just did.
- **Wants to leave with:** the answer, decision, or completed action.
- **Job of this screen:** one sentence. If it needs "and", it is probably two screens or one screen with a clear primary and a secondary part.

Then list the content and rank it: one **primary** thing (what the screen is for), a few **secondary** things (support the primary), and **tertiary** things (rarely needed). Tertiary content is moved behind a tap, to the end, or removed. A screen where everything has equal weight has not been ranked yet.

Order content by the sequence of questions the person asks ("Is this the right item? What does it say? What should I do?"), not by the order of fields in the data model.

## Navigation

A person must always be able to answer: where am I, how do I go back, what can I do next.

- Show location: a title that names the current thing, not the app.
- Returning from a detail screen restores the list's scroll position and reflects what changed (read, edited, deleted).
- One primary action per screen, placed where attention ends (end of content, or a fixed bottom area on phones). Destructive actions sit apart from it and never look like it.
- No dead ends: every screen and every state (including empty and error) offers a sensible next step.
- Avoid stacking a dialog on a dialog. If a dialog needs a second decision, it should have been a screen.
- Count the taps and decisions for the main task. Remove any step that asks for something the system already knows.

## Lists that lead to details

- Each row shows enough to choose correctly without opening it: a distinguishing title, the one or two attributes people actually choose by, and status (new, unread, needs attention).
- Sort by what people look for first (usually most recent or most urgent) and say so if it is not obvious.
- If the list can exceed about two screens, provide a way to narrow it (search, filter, or grouping) that matches how people remember items.

## Long content

- Lead with the conclusion or summary; details follow. Someone who reads only the first screen should still get the main point.
- Break the text into sections with headings that state content ("Take with food"), not categories ("Notes").
- For content longer than about three screens, provide a way to see the structure and jump (contents list or section anchors) and show reading position.
- Put a warning or caveat next to the thing it qualifies, not in a block at the end.
- Use a table only for values people compare across rows; otherwise use a list. On narrow screens, a table with more than three columns needs a different shape (stacked rows or a horizontally scrollable region with a visible cue).

## Check before building

- Cover the screen title: can a first-time viewer still say what the screen is for and what to do next within five seconds?
- Walk the main task start to finish and write down each tap. Is any step surprising, repeated, or unnecessary?
- Remove one element at a time in your head. If nothing is lost, remove it.

## Structural failures to look for

- The layout mirrors the database: every field shown, in storage order, at equal weight.
- The key information or action is below the fold under decorative or secondary content.
- A grid of identical cards used for items that are actually a sequence, a hierarchy, or a single choice.
- Several competing primary buttons.
- Settings or metadata mixed into the main reading or task flow.

# States

Read this whenever a surface loads data, accepts input, or can fail. A screen designed only for the ideal case is unfinished: the other states are what people see on a slow connection, on first use, and when something goes wrong.

## Scope

A state the implementation can actually reach is part of the surface, not an extra feature. If the screen fetches data, then loading, empty, and failure exist whether or not the brief names them. Design the reachable ones. Do not invent states the system cannot reach, and if designing a state would exceed the authorized scope, report it as a finding instead of building it.

## Inventory

List every region that depends on data or input, and decide which of these apply:

| State | What the person needs |
| --- | --- |
| Loading | To know something is happening and roughly what will appear |
| Empty: first use | What belongs here and the one action that fills it |
| Empty: no results | Which filter or query produced nothing, and how to widen it |
| Error | What happened in plain words, what was kept, what to do next |
| Offline or stale | That the content may be old, and when it was last updated |
| Partial | Which parts are available and which are not |
| Ideal | The normal content |
| Extremes | 1 item, very many items, very long text, missing optional fields |

For each control: default, pressed, keyboard focus, disabled, and busy. For each form: invalid input, submitting, and submitted.

## How each state should behave

- **Loading.** If the wait may exceed about a third of a second, show a placeholder shaped like the content that will arrive, so the layout does not jump. Do not flash a spinner for instant loads. When refreshing content that is already shown, keep it visible and indicate the refresh separately.
- **Empty.** Never a blank area or a bare "No data". State what will appear here and offer the action that creates it. Distinguish "nothing yet" from "nothing matches".
- **Error.** Say what failed and what the person can do, in their words, without codes or blame. Offer retry where retrying can help. Keep everything the person typed or selected. Show the error where the problem is: field errors at the field, load errors in the region that failed, not a full-screen takeover unless the whole screen is unusable.
- **Disabled.** Make clear why, or how to enable it. Prefer leaving a button enabled and explaining on press over a disabled button with no explanation.
- **Busy.** After a press, acknowledge immediately and prevent double submission. Show the result in place.
- **Success.** Confirm that the action happened and what changed. For reversible actions, offer undo instead of asking for confirmation beforehand.

## Layout must survive the extremes

Check each region with a very long title, a missing image or optional field, one item, and many items. Check text enlarged to at least 130%, and 200% for reading content. Nothing may overlap, clip silently, or push the primary action out of reach.

## Reporting

In PLAN, list the applicable states per region. After BUILD or in VERIFY, report them in a table:

`Region | State | Designed | Evidence`

"Designed" is yes, no, or not applicable. Evidence is a render of that state or the source location; a state that was not rendered is reported as not visually verified.

# Android with Jetpack Compose

Read this for any Compose work. It covers what differs from web. The project's existing theme, components, and navigation setup take priority over anything here; check the library versions in the project before relying on a specific API.

## Screen structure

- Use `Scaffold` for top bar, bottom bar, floating action button, and snackbars, and pass its content padding to the content. Draw edge to edge and handle system bar and keyboard insets, so nothing sits under the status bar, navigation bar, or keyboard.
- Top-level destinations (three to five) belong in a bottom navigation bar on phones and a navigation rail on wider windows. Everything else is reached by going deeper, with a back arrow in the top bar.
- System back and the top-bar back arrow must lead to the same place, and returning to a list restores its scroll position.
- A top app bar title names the current screen or item. For long reading screens, a bar that collapses or scrolls away gives the text more room.

## Size and touch

- Layout in `dp`, text in `sp`. Never set text size in `dp`, and never give a container of text a fixed height: enlarged text must be able to grow it.
- Interactive elements have a touch target of at least 48 × 48 dp even when the visible icon is smaller.
- Adapt to window width instead of device type: a single column on compact widths; on medium and expanded widths cap the reading column (about 600 dp) or show list and detail side by side.

## Theme

- Define the app's own `ColorScheme` for light and dark, and its own `Typography`; the unmodified Material baseline reads as a template. Decide deliberately whether to use dynamic color, and turn it off if the product has a brand palette.
- Use theme roles (`MaterialTheme.colorScheme`, `MaterialTheme.typography`) in composables. Hard-coded colors and sizes break dark theme and consistency.
- For Chinese or Japanese body text, set an explicit line height in the body text styles; the default is tuned for Latin text and is too tight.

## State

- Model each screen's state explicitly, for example a sealed type with loading, empty, error, and content cases, held in a view model and passed down. Write one composable per case so each can be previewed and none is forgotten. See `states.md` for what each case must show.
- Give lazy list items stable keys, and use content padding on the list rather than padding around it, so content scrolls under bars correctly.
- Show transient results (saved, deleted with undo) in a snackbar; show blocking problems inline in the region that failed.

## Accessibility

- Every meaningful icon or image has a content description; decorative ones have none, so TalkBack skips them.
- Mark section titles as headings in semantics so screen-reader users can jump between them, which matters most on long reading screens.
- Merge a row's children into one semantic node when the row is a single tappable item, so it is announced once.
- Check the screen at font scale 1.3 and 2.0, in dark theme, and with TalkBack reading order from top to bottom.
- Respect the system setting that removes or shortens animations.

## Render evidence

Compose previews are the cheapest render: add `@Preview` variants for each state composable, plus dark theme and a large font scale, and look at them. A preview shows layout, not behavior; navigation, insets, keyboard, and TalkBack still need an emulator or device, and are reported as unverified without one.

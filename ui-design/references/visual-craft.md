# Visual craft

Read this for type, spacing, color, and the finishing pass. These are defaults for when the project gives no direction; an existing design system or brand overrides any number here.

Polish comes mostly from restraint and consistency: few sizes, few spacing values, few colors, used the same way everywhere.

## Type

- Use a small scale: about four or five sizes for a whole screen (for example body, small/meta, subheading, heading, and one display size). Adjacent sizes should differ clearly, by about 1.2× or more; near-identical sizes look like mistakes.
- Build hierarchy with weight and color before size. Secondary text is the same size in a quieter color more often than it is smaller.
- Body text: at least 16 px on web and 16 sp on Android. Meta text no smaller than 12.
- Headings sit closer to the text they introduce than to the text above them.
- Use tabular (fixed-width) numerals for numbers in columns so digits align, and right-align numeric columns.
- Left-align running text. Centered text is for a line or two only.

### Reading screens

- Line length: about 45–75 characters for Latin text, about 25–40 characters for Chinese or Japanese. On wide screens, cap the text column instead of stretching it.
- Line height: about 1.5 for Latin body text; 1.7–1.9 for Chinese or Japanese, which has no ascenders or descenders to create air between lines.
- Paragraphs are separated by space (about one line), not by indents plus space.
- Avoid pure black text on pure white for long reading; slightly softened contrast is easier over time, as long as it stays above the contrast minimum.

### Chinese, Japanese, Korean text

- Do not use italics for emphasis; CJK fonts have no true italic and the slant is synthesized. Use weight or color.
- Do not tighten letter spacing. Do not justify text unless the platform handles CJK justification well.
- Use a font stack that names CJK system fonts for the target locale so glyphs do not fall back to another region's forms (Traditional Chinese, Simplified Chinese, and Japanese draw the same code points differently). Set the document or view language correctly for the same reason.
- When Latin words or numbers sit inside CJK text, check that baseline and size look even; mixed text often needs a slightly larger line height.

## Spacing and alignment

- Take every gap from one scale based on 4 or 8 (4, 8, 12, 16, 24, 32, 48). Arbitrary values are the most common source of an unpolished look.
- Space shows relationship: the gap inside a group is smaller than the gap between groups. If two gaps are equal, the eye cannot tell what belongs together.
- Keep one consistent outer margin per screen, and align content to as few vertical lines as possible. Count them; more than three or four on a phone usually means misalignment.
- Padding inside a control is consistent across all controls of that kind.
- Separate content with space first, a hairline second, a filled container last. Do not combine border, shadow, and background on the same element.

## Color

- Let neutrals carry most of the interface: one background, one or two surface tones, and three text tones (primary, secondary, disabled).
- One accent color means "you can act here". Do not also use it for decoration, or actions stop standing out.
- Reserve red, amber, and green for status, and always pair them with text or an icon; color alone does not reach everyone.
- Contrast: at least 4.5:1 for body text, and 3:1 for large text, icons, and control boundaries. Check secondary text and text on colored backgrounds specifically; they fail most often.
- Dark theme is not inverted light theme: use dark grey rather than pure black surfaces, raise elevation by lightening, and reduce the saturation of accent colors.

## Emphasis

- One focal point per view. If three things are emphasized, none is.
- De-emphasize by quieter color or lighter weight, not by shrinking below a legible size.
- Timestamps, counts, and other metadata are quieter than the content they describe.

## Finishing pass

Before calling a screen done, look at the render and check:

- Squint or blur: is the first thing you notice the most important thing?
- How many distinct font sizes, spacing values, corner radii, and colors are in use? Merge near-duplicates.
- Do icons share one style and stroke weight?
- Are similar items identical in structure and spacing?
- Does any text truncate, wrap awkwardly, or leave a single orphaned word or character on a line?
- Do touch targets and focus indicators still meet the minimums after styling?

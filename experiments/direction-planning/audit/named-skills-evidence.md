# Visible skill names and descriptions

Date: 2026-10-27. Scope: the owner's correction that name and description are
separate fields and both must be shown. No publication or owner acceptance.

## Layout

Each of the 70 primary nodes displays the canonical skill name on a full-width
first row and the Chinese purpose description on a second row. The relation badge
has its own right-hand cell beside the description. DOM order follows that visual
order. Names use normal wrapping without ellipsis; tooltip/detail access is optional.
The former hidden-name rule is removed. This is a display repair, not a change to
canonical asset instructions or the 53 registered relationship meanings.

The two-field label naturally needs more height than a description alone. The
layout retains the preceding 90px verification bound instead of enlarging all
nodes into large cards. Dedicated routing gutters and actual-bound routing remain.
Narrow layouts remove the ordinary page anchor inset while the detail sheet is open;
short-phone/tablet sheet proportions preserve space for nearby release neighbors.

## Evidence

- [Model tests](named-skills-tests.txt): 56 passed, zero failed/skipped.
- [Browser harness](verify-named-skills.cjs) and
  [report](named-skills-browser.json): all 70 actual names are displayed and match
  their canonical IDs; Chinese descriptions match the local catalogue. The new
  assertion first failed because the previous name element was hidden.
- Ten viewport/theme combinations at 360×667, 390×844, 1024×768, 1280×800 and
  1440×1000, light/dark. All name fields remain visible; measured name/description
  bounds fit without overlap or horizontal clipping. Names precede descriptions,
  all primary nodes remain displayed and there is no document horizontal overflow.
- Retained actual SVG/node collision checks pass for every skill selection and
  dense review hubs across the responsive matrix. Keyboard/focus, peer navigation,
  optional lookup, context-only resize and edited-request retention pass.
- The release example initially exposed a newly covered video-neighbor label on
  phone/tablet. The viewport checks now also require that neighbor's full node to
  remain above the detail sheet, and the layout repair passes without weakening
  that assertion.
- Visually inspected [overview](named-skills-overview.png),
  [desktop example](named-skills-1440.png) and [mobile example](named-skills-390.png).

Source identity, actual maximum heights, date and browser version are in the
report. These checks do not imply all 70 readable labels fit in one viewport or
that all distant neighbors fit above a mobile sheet. No Safari, real-device, native
zoom or spoken screen-reader pass is claimed. Owner review remains pending;
no commit, push or publication was performed.

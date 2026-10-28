# Fixed asset entry: local verification

Date: 2026-10-27. Scope: the authorized local prototype repair for AIC-REQ-04
A5-A8. No publication or real asset execution.

## Behavior

Clicking a map node exposes its related-skill selector immediately below the node
heading. It remains outside the scrolling instructions. All context skills can be
selected there, with direct Chinese applicability, input, use and expected result.
The first relevant skill is an example, not a required invocation. Work explanation
and its optional request helper use a separate content choice. No duplicate
recommended/full list is retained. There is one graph and one contextual panel.

This removes explanatory scrolling before asset access. It does not claim that
all 23 review options fit in one native popup or that long instructions never
scroll. Native menu scrolling and selection belong to the browser.

## Executed evidence

- [Model results](asset-entry-tests.txt): 46 passed, zero failed/skipped. The new
  helper test first failed because the helper did not exist, then passed for every
  context/skill, default choice, cross-context rejection and isolated snapshots.
- [Browser report](asset-entry-browser.json) from
  [the current harness](verify-asset-entry.cjs): all 70 skill selection paths and
  20 viewport/theme/perspective combinations, each checking all ten map nodes.
- Viewports: 360×667, 390×844, 1024×768, 1280×800, 1440×1000. Light/dark themes and
  work/evidence perspectives. For every node, the selector starts in the visible
  viewport at zero explanation scroll and stays at the same position after the
  instructions scroll. No document horizontal overflow in checked states.
- Keyboard mode switching and Escape/focus recovery pass. Chosen skill survives
  mode/perspective changes; optional lookup targets it in the same panel. Edited
  work requests survive skill changes. There are zero recorded page errors.
- Headless Chromium cannot commit this OS-native select popup with synthetic keys.
  Its selection API validates every option. Separately, the existing IAB tab was
  reloaded and its actual select opened; Down then Return changed
  `orchestrate-code-review` to `review-implementation-alignment`, and the visible
  purpose, four fields and source link changed together. That native check is not
  inferred from the headless selection API.
- Native reload initially exposed stale module exports in the already-open IAB.
  Local entry/style/model revision URLs repaired the mismatch; the updated picker
  and changed instructions were then visibly verified in that tab.
- [Desktop screenshot](asset-entry-1440.png) and
  [mobile screenshot](asset-entry-390.png) were visually inspected for the fixed
  entry, readable purpose, wrapping and independent detail scrolling.

Current source hashes, date and Chromium version are in the browser report. Older
nested-disclosure reports describe their own revisions and do not certify this
layout. Registry synchronization remains 70 skills; no defining skill changed.

## Limits

No Safari, real-device, native zoom or spoken screen-reader pass is claimed.
Owner whole-map acceptance remains pending; tests do not prove comprehension.
Draft document approval and public delivery remain separate. No commit, push or
publication was performed.

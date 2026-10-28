# Single work map: local verification

Date: 2026-10-27. The owner explicitly removed angle switching. This supersedes
previous perspective-switch checks; it does not waive fixed asset entry or skill
coverage. Scope remains a local prototype without publication.

## Change and checks

The angle selector, alternate controller state, evidence projection/data and CSS
were removed. The one retained work map uses `work-map.mjs`. Node meanings,
nonlinear connections and all 70 per-skill Chinese usage records are preserved.
The fixed skill selector and skill/work content choices remain.

- [Model results](single-map-tests.txt): 47 passed, zero failed/skipped. The new
  no-selector assertion first failed on the preceding markup. Old two-view tests
  were replaced with single-map labels, context completeness, source subjects and
  snapshot-isolation assertions because that feature was explicitly removed.
- [Current browser harness](verify-single-map.cjs) and
  [report](single-map-browser.json): all 70 skill selections, ten viewport/theme
  combinations, each covering all ten nodes. Five sizes are 360×667, 390×844,
  1024×768, 1280×800 and 1440×1000, with light/dark themes.
- The angle selector is absent. Fixed skill entry is visible without explanatory
  scrolling, stays pinned after detail scrolling, and does not create document
  horizontal overflow. Content choices, keyboard close/focus recovery, optional
  lookup and edited-request retention pass. One map and zero page errors.
- [Desktop](single-map-1440.png) and [mobile](single-map-390.png) screenshots verify
  the simpler heading and retained asset entry. Source hashes, date and Chromium
  version are in the report.

Native popup key behavior was checked in the prior fixed-entry revision; this
revision does not claim a fresh native-popup pass. No Safari, real-device, native
zoom or spoken screen-reader pass is claimed. Owner acceptance remains pending.
No commit, push or publication was performed.

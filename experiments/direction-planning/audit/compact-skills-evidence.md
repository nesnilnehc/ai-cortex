# Compact skill nodes and unobstructed relationships

Date: 2026-10-27. Scope: the owner's local visual repair request. This preserves
all 70 default-expanded skills, 53 evidenced relationships and Chinese usage.
No publication or human acceptance is inferred.

## Repairs

Primary nodes use compact Chinese labels with inline counts/relationship labels.
The minimum heights change from 88px to 38px on desktop and 108px to 44px on mobile;
wrapping can increase actual height. IDs remain in tooltips and detailed usage.
A uniform column geometry reserves 40px of node-free routing space beside each
column. Relation types use separate lanes; cross-column paths choose a nearby
clear horizontal gap. Arrowheads approach target boundaries from outside.

This replaces curves that could travel beneath other assets. The collision check
first reproduced a repair-loop/test connection passing through the agent-test
node, and the size check first rejected the old mobile components. A separate
redraw regression reproduced a context-only selection acquiring an unhighlighted
default skill's edges after resize; explicit graph-selection state fixes it.

## Executed checks

- [Model tests](compact-skills-tests.txt): 56 passed, zero failed/skipped. Tests
  include endpoint direction, translated coordinates, same/cross-column routing,
  separate type lanes, unknown-kind rejection and nearest safe bridge selection,
  plus retained inventory, source, guidance and request-state regressions.
- [Browser harness](verify-compact-skills.cjs) and
  [report](compact-skills-browser.json): all 70 primary node selection paths,
  neighborhoods and usage fields; every rendered active path sampled every three
  CSS pixels against every primary node interior, with no detected collision.
- Ten size/theme combinations at 360×667, 390×844, 1024×768, 1280×800 and
  1440×1000, light/dark. Every skill remains displayed, one graph is retained,
  there is no document horizontal overflow and measured nodes stay within the
  recorded 90px maximum bound. Actual maxima are in the browser report.
- Release and dense engineering-review hub routes are checked in each combination.
  Keyboard selection, Escape/focus, peer links, optional lookup and edited-request
  preservation pass. On narrow screens the selected release node stays above the
  detail sheet. Context-only selection/redraw retains overview edges until a
  skill is shown explicitly.
- Visual inspection: [overview](compact-skills-overview.png),
  [desktop relationship example](compact-skills-1440.png) and
  [mobile relationship example](compact-skills-390.png).

Current source hashes, date and browser version are recorded in the report.
Registry/definition checks retain the same 70 skills and evidence conditions.
Earlier expanded-card/curve reports describe older revisions.

## Limits

Collision claims concern primary node interiors and rendered path sampling in
these local Chromium states. They do not certify every possible font/zoom/device
combination or claim all long-range neighbors fit in the mobile viewport at once.
No Safari, real-device or spoken screen-reader pass is claimed. Owner review is
pending; no commit, push or publication was performed.

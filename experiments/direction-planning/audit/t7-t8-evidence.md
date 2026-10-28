# T7/T8 local repair evidence

Date: 2026-10-27. Scope: explicitly authorized local contrast and static-fallback
repairs. No graph redesign, publication or whole-map acceptance is implied.

## Red checks

The new verifier first ran separately for contrast and fallback before runtime
changes. Both failed as expected:

- [T7 red report](t7-t8-contrast.json): two light-theme loop labels at
  4.377635687729373:1, below 4.5:1.
- [T8 red report](t7-t8-fallback.json): no visible canonical source link when the
  entry module was blocked with JavaScript still enabled.

## Repair

Only prototype `index.html` and `workspace.css` changed. Loop text uses existing
theme ink on its existing tinted background. Border, layout and relation meanings
remain unchanged. The footer contains a static catalogue anchor describing its
purpose when the graph is unavailable. It needs no initialization, event handler,
module error detection or network service. Narrow footer wrapping preserves page
bounds. The CSS cache revision is updated.

## Green checks

[Targeted browser report](t7-t8-browser.json), produced by
[the verifier](verify-t7-t8.cjs):

- Eight width/theme/state samples: 390 and 1440px, light and dark, overview and
  selected state. Both loop labels measure about 11.47:1 light and 11.12:1 dark.
  All sampled text meets 4.5:1; the observed minima are 5.31:1 and 7.71:1.
- No-JS catalogue recovery passes. With the entry module blocked, the static source
  route remains visible, accepts keyboard focus and reaches the catalogue with
  HTTP 200. The [blocked-entry capture](t7-t8-module-fallback.png) shows the route.
- Existing four clipboard recovery cases and topic-title reconciliation still pass.
- Controller/data source hashes remain unchanged; HTML/CSS are the only permitted
  runtime differences.

Full regression after the final runtime edits:

- [63 model tests](t7-t8-tests.txt).
- [Fresh local-branch browser matrix](local-branch-browser.json): all 70 skill paths,
  13 topic relation explanations, five sizes × two themes, and all ten topic
  selections in each combination. Local ownership, scroll/clipping, node/label
  geometry, keyboard/focus, search/peer reveal and request retention pass.
- Existing scheme remains: one main graph, direct topic relations, zero/one locally
  expanded topic, no center hub and no lower-page skill dock.

T7/T8 satisfy their scoped local acceptance and are Done in the task record. Other
Todo states, draft requirement/design approval and owner comprehension remain
unchanged. Native devices, Safari, native browser zoom and spoken screen-reader
operation are not certified by this local Chromium evidence.

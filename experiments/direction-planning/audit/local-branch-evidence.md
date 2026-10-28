# Local skill-branch verification

Date: 2026-10-27. Scope: local prototype only; publication and owner acceptance
remain separate.

## Model checks

63 tests pass. A new red case reproduced a connector crossing a peer when a topic
became tall; the route now uses actual topic ports and clear row bridges. All ten
asymmetric height cases pass. A separate red disclosure test established zero or
one open topic, idempotent reveal, collapse and unknown-ID rejection. Canonical
coverage, source quotes, 13 direct topic relationships, 53 skill edges and all
four Chinese usage fields remain covered.

## Browser checks

- All 70 skill nodes occur once inside their owning topic, with no lower-page dock.
- All 70 selection paths retain exact names, Chinese purposes, four usage fields,
  direct-neighbor relations and source links. Search/peer reveal and request identity
  pass. Opening another topic closes the prior branch.
- All 13 topic relationship explanations remain available with source conditions.
- Five widths (360, 390, 1024, 1280 and 1440px), each in light and dark, pass. Each
  combination additionally expands/selects all ten topics: 100 ownership/visibility
  cases. The owning heading and complete selected skill remain visible, including
  inside its local list and above responsive explanation sheets.
- Skill SVGs are sampled against nodes in their own content coordinate systems.
  They scroll/clip in the same container. An explicit internal-scroll check preserves
  document scroll and the source heading position. Topic paths are sampled against
  topic interiors; proper crossings and label overlap are separately checked.
- Keyboard selection/disclosure, close/focus, source context, no page overflow and
  compact closed-graph overview pass. On narrow screens horizontal panning belongs
  to the graph viewport; the selected topic is brought into view automatically.

Desktop local expansion and mobile selected-skill captures were visually inspected.
The graph reflows when a topic opens; invariant positions from the historical
lower-dock revision are intentionally no longer the contract. Logical relationships
remain visible and unchanged. No execution, publication or comprehension acceptance
is established by these checks.

## Evidence

- [Model log](local-branch-tests.txt)
- [Browser harness](verify-local-branch.cjs)
- [Browser report and source hashes](local-branch-browser.json)
- [Desktop local branch and explanation](local-branch-1440.png)
- [Mobile local branch and explanation](local-branch-390.png)
- [Large skill group expanded locally](local-branch-quality.png)
- [Collapsed desktop overview](local-branch-1280-overview.png)

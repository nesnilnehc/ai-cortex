---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-23
parent: 2026-10-23-theme-and-capability-map-functional-design.md
status: approved
---

# Technical design: theme preference and capability atlas

## Goal

Persist native theme selection and render a registry-complete, bilingual HTML capability atlas without new runtime dependencies.

## Architecture and service decomposition

| Component | Responsibility and dependency |
| --- | --- |
| `theme.mjs` | Theme state and optional localStorage boundary |
| `main.mjs` | Bind existing selector after locale initialization |
| HTML editions | Complete atlas disclosures, localized descriptions and source references |
| CSS | Responsive branch layout and system/manual appearance |
| Registry tests | Compare atlas membership with canonical local registries |

## Components and detailed design

`initializeTheme(env, root, select)` restores a validated `system`, `light` or `dark`
value from `ai-cortex.theme`, otherwise uses System. Assign the selector and root
`data-theme`, bind change, then reveal its label. Valid changes update the DOM and
persist best-effort; catch storage getter/read/write denial. Ignore invalid input.
CSS media queries own live system-theme adaptation, requiring no matchMedia listener.
Explicit light/dark overrides also set `color-scheme` for native controls.

Implement the functional atlas as semantic native `details` branches in a three-column
Skill grid and a shared-foundation row. Below 768px these become a single column.
Use IDs on layer branches, `data-asset` identifiers on leaves and local anchor links
from the header/hero. Contents are present in HTML, not fetched or hidden behind
JavaScript. Each leaf carries the stable asset identifier, a localized display
summary and an optional source link. Preserve current section anchors, shared CSS,
modules, keyboard focus, language preference and clipboard feedback.

## Database design

No database change. Optional origin-local `ai-cortex.theme` stores one enum string.
Selecting System stores that explicit preference; clearing site data resets it.

## Interface contracts

No server interface change. Both static editions retain their public URLs. The
internal theme initializer consumes an environment, root element and select element;
it introduces no outbound request. Registry parity tests read existing local indexes.

## Data flow and error handling

Storage → validate enum → root and selector → user change → DOM + optional write.
Denied reads fall back to System; denied writes preserve the current appearance.
Invalid persisted values never become CSS state. Atlas source content is static;
registry omissions or duplicates fail local/CI tests before publication.

## Technology choices and trade-offs

Choose native HTML/CSS disclosures over a canvas diagram library: accessible and
usable without JS, but without arbitrary zoom/drag. Choose CSS media queries over
manual system-event listeners: the browser owns OS preference updates. localStorage
retains explicit choice; session storage would lose it between sessions. No external
fonts, diagram runtimes or new packages are needed.

## Test strategy

Observe failing theme and catalogue-parity tests before implementation. Unit tests
cover defaults, all persisted values, manual changes/System reset, invalid values
and denied storage. Static checks compare all asset IDs/counts and corresponding
links/anchors in both editions against registries. Browser acceptance checks actual
selector persistence across language navigation/reload, keyboard branch expansion,
readable map content at 360px/1280px and both themes. Inspect CSS system behavior
and report whether an actual OS appearance change was exercised.

## Quality attribute design

| source | rule_refs | design tactic | trade-off | verification | owner |
| --- | --- | --- | --- | --- | --- |
| M1 | TST-001, TST-002 | Inject storage and DOM boundary | No persistence when storage is blocked | Unit tests and reload | Site maintainer |
| M2 | ARC-001, TST-002 | Static descriptions with registry-complete membership checks | Copy maintenance in two editions | Registry parity tests | Site maintainer |
| M3, M4 | TST-001 | Native disclosures and responsive CSS | No free-form spatial layout | Browser keyboard and viewport checks | Site maintainer |

## Acceptance criteria

- **T1**: Theme tests pass and browser restoration/System reset are verified (M1).
- **T2**: Both atlases match all four registries without missing or duplicate assets (M2).
- **T3**: Browser checks confirm on-site reading, keyboard operation, mobile layout and both appearances (M3, M4).

## Deployment and operations

Publish both editions and the new theme module through the existing Sites project.
Update shared resource release identifiers and verify custom-domain HTTPS responses.
No hosting, domain, permissions or audience changes are needed.

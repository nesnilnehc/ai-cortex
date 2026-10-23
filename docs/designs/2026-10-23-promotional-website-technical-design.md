---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-23
parent: 2026-10-23-promotional-website-functional-design.md
status: approved
---

# Technical design: AI Cortex promotional website

## Goal

Deliver an independent static promotional page with progressive enhancement,
accessible navigation and verified installation copy.

## Architecture and service decomposition

| Component | Owner and dependency direction |
| --- | --- |
| `website/index.html` | Content and semantic navigation; loads local CSS and module |
| `website/styles.css` | Layout, color tokens and system preference adaptations |
| `website/main.mjs` | Browser composition: binds DOM elements to copy controller and theme preference |
| `website/copy.mjs` | One fallible clipboard interaction; no dependency on globals |
| GitHub repository | External link destination only; no API fetch or runtime dependency |

## Components and detailed design

`bindCopyButton(button, source, feedback, clipboard)` registers an asynchronous
click handler, reveals the enhanced action, disables it while copying and writes
feedback through `textContent`. `source.textContent` is the sole command source.
The injected `clipboard.writeText(text): Promise<void>` boundary is unit tested.
No persistence or background work is introduced. A native theme selector assigns
its value to the root's `data-theme` attribute; CSS owns all light/dark tokens and
system fallback. It is revealed only when its event handler has been bound.

Map the functional UI decisions to native anchors and `details`/`summary`:
they remain usable without scripts. HTML owns content, CSS owns viewport/theme
adaptation, and the controller owns only pending copy state. At widths below
768px, multi-column layouts stack. Code overflow is local to its container.
Use native buttons, visible focus, an `aria-live` status and a skip link.

## Database design

No database change. No cookies, local storage or submitted visitor data.

## Interface contracts

Public anonymous `GET /` returns static HTML; `GET /styles.css`, `/main.mjs` and
`/copy.mjs` return their respective static assets. Unknown files receive the
host's 404 response. No application API change or authorization surface.
The intended canonical URL is `https://ai-cortex.nesnilnehc.top/`.

## Data flow and error handling

Read rendered command text → disable copy button → await clipboard write →
announce success or manual-copy recovery → enable retry.

- Clipboard unavailable or write rejected: show manual-copy instructions, retain
  readable commands and enable retry; never claim success.
- Module unavailable: copy control stays hidden; ordinary links and disclosures
  continue to function.
- Source text missing: report that commands are unavailable and direct the visitor
  to installation documentation; do not copy empty text.

## Technology choices and trade-offs

Choose buildless HTML/CSS/ES modules: this page has static content and a single
enhancement, so no package manager, build pipeline or framework runtime is needed.
React plus Vite was considered: its component reuse is useful for an application,
but bundling and dependency maintenance add cost for this small standalone page.
No third-party UI package is needed because this is a native editorial composition,
not an implementation of a named component system. Use local system font stacks.

## Test strategy

Write clipboard tests before implementation and observe a failing run. Use Node's
built-in test runner for success, denied/unavailable clipboard, blank source and
concurrent clicks. Verify actual DOM wiring in the browser, plus native details,
anchor navigation and keyboard focus. Inspect screenshots at 360px and 1280px in
both themes, including reduced motion and no JavaScript where tooling permits.
Run repository Markdown link/hygiene/CLI-documentation checks and Markdown lint.
Attempt Lighthouse only with an available local installation; do not claim
performance measurements from the absence of dependencies.

## Quality attribute design

| source | rule_refs | design tactic | trade-off | verification | owner |
| --- | --- | --- | --- | --- | --- |
| QA1 | TST-001, TST-002 | Inject clipboard boundary and test success/failure/pending | Small controller module | Red/green tests and browser wiring check | Site maintainer |
| QA2 | ARC-001 | Separate semantic content, CSS and enhancement | Three small runtime files | Responsive/theme/keyboard inspection | Site maintainer |

Profiles: integration-boundary for clipboard/DOM wiring; no authenticated system,
sensitive data, persisted format or service SLO. Module topology and dependency
direction are the architecture table above. No new executable dependencies.
No coverage percentage or production performance budget is asserted.

Dependencies: native HTML/CSS/ES module support and the optional browser clipboard
API; development checks use Python 3 and Node's built-in test runner. Risks are
content drift and browser clipboard differences: source-parity tests and manual
copy recovery bound their impact. No external runtime or package dependencies.

## Deployment and operations

Serve `website/` as a static directory. Local verification uses Python's HTTP
server bound to loopback; public deployment needs HTTPS and domain routing.
No remote write, credential access or DNS mutation is included in this change.

## Acceptance criteria

- **T1**: Standalone HTTP preview serves the page and local assets (F1, F2, A1).
- **T2**: Copy tests and browser wiring confirm honest success and recovery (F3).
- **T3**: Browser inspection confirms responsive navigation, disclosures and focus
  at 360px/1280px, both themes and script-free content (F4, F5).

Review: self-review uses technical-design-modeling 2.2.0 and
technical-design-quality 2.5.0. TDES baseline, interface-change, shared-value and
quality-attribute concerns are addressed; data-change does not apply. Browser
acceptance and public deployment are future evidence, not design-review results.

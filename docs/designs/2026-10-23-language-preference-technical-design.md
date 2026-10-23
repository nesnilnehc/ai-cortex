---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-23
parent: 2026-10-23-language-preference-functional-design.md
status: approved
---

# Technical design: language preference

## Goal

Add tested browser locale selection and best-effort local persistence to the existing static editions.

## Architecture and service decomposition

| Component | Responsibility |
| --- | --- |
| `language.mjs` | Selection precedence, storage boundary and same-origin navigation |
| `main.mjs` | Invoke language initialization before existing enhancements |
| Static HTML | Native language links with explicit `lang=en` or `lang=zh` query |

## Components and detailed design

`initializeLanguage(env, pageLanguage)` receives browser location, navigator and
localStorage through an injected environment. Selection order is valid explicit
query, valid stored value, first supported browser language, English. The only
persisted values are `en` and `zh` under `ai-cortex.language`. Read and write
storage inside separate try/catch boundaries, including access to its getter.
A choice query is honored even when persistence fails. Inferred choices are not
saved. Compare against the HTML page language before `location.replace`; choose
only `/` or `/zh.html` and preserve search/hash. Sites may normalize `/zh.html` to
`/zh`; HTML language, rather than pathname, prevents redirect loops.

Reuse native links, layout and focus behavior. Links carry explicit choice without
requiring an event handler, including modified-click/new-tab navigation. State is
browser-local; there is no server state. JavaScript-disabled links remain ordinary
static navigation. Use a new release resource query identifier after publication.

## Database design

No database change. One origin-local storage string is optional; clearing browser
site data resets it. No account, cookie or external data submission is introduced.

## Interface contracts

Existing GET routes are unchanged. Optional `lang=en|zh` expresses a manual choice;
invalid values are ignored. `initializeLanguage` returns the selected language and
may invoke same-origin location replacement. No new server API.

## Data flow and error handling

URL/storage/browser list → validated language → optional storage write → compare
page locale → optional redirect. Denied storage reads fall back to browser detection;
denied writes retain the explicit choice for that navigation. Unsupported values
cannot become redirect URLs. Matching page locale produces no redirect.

## Technology choices and trade-offs

Choose localStorage and static query links: durable preference with no backend,
but storage may be disabled. Session storage would lose the preference when the
session ends; cookies would add server request data without a server-side reader.
No new dependencies or network calls are needed.

## Test strategy

Observe failing Node tests before implementation. Test locale priority, regional
variants, fallback, both preference directions, explicit override, blocked storage,
query/hash preservation, invalid values and redirect settling. Static contracts
verify both explicit language links. Browser checks verify actual navigation,
keyboard selection and preference persistence after reloading. Existing layout is
unchanged; inspect mobile navigation after the behavior is bound.

## Quality attribute design

| source | rule_refs | design tactic | trade-off | verification | owner |
| --- | --- | --- | --- | --- | --- |
| P2, P3 | TST-001, TST-002 | Inject storage/location boundary and catch denied access | No persistence when blocked | Unit tests and browser reload | Site maintainer |
| P3 | REL-003 | Compare page locale before replacement | Direct edition URLs follow preference | Redirect-settling tests | Site maintainer |

## Acceptance criteria

- **T1**: Locale selection tests cover priority and fallback (P1).
- **T2**: Override/persistence tests and browser reload confirm manual preference (P2).
- **T3**: Storage denial, query/hash and loop tests pass; native links remain available (P3).

---
artifact_type: functional-design
lifecycle: snapshot
created_at: 2026-10-23
parent: ../requirements-planning/AIC-REQ-02.md
status: approved
---

# Functional design: language preference

## Goal

Select English or Chinese from browser languages on first visit and retain the reader's explicit language choice on later visits.

The user extended AIC-REQ-02 with this behavior on 2026-10-23. This decision replaces
the automatic-detection and persistence exclusions of the earlier localization design.

## Functional modules and boundaries

| Module | Responsibility | Boundary |
| --- | --- | --- |
| Initial selection | Choose the first supported browser language, otherwise English | Does not save an inferred preference |
| Explicit selection | Remember English or Chinese chosen through language links | Local to this browser and origin |
| Navigation | Present the selected edition | Preserve section and unrelated query parameters on automatic navigation |

## Business workflow

```text
Open either edition → explicit language selection in URL?
  → yes: remember choice → display that edition
  → no: saved manual preference?
    → yes: display preferred edition
    → no: first supported browser language → display edition (English fallback)
```

## Exception and edge scenarios

- Storage unavailable: selection still works for the current navigation; later visits use browser language.
- Unsupported/invalid preference: ignore it and use the next source in the selection order.
- JavaScript unavailable: retain static editions and native language navigation.
- Already in the selected edition: remain there without redirecting or adding history.

## UI and interaction flow

Reuse the existing English / 中文 links, active-page styling and focus indicators.
Selecting a link explicitly overrides an earlier preference, including when opened
in a new tab. Automatic selection applies to both editions; a direct language URL
without an explicit choice follows the saved/browser preference. No new visible
controls, loading, empty or account states are needed. Existing runnable editions
are the visual baseline; no independent mockup is needed for this behavior change.
The implementer verifies keyboard selection, reload persistence and mobile layout.
Only one anonymous role exists; there are no permission or business-object states.

## Acceptance criteria

- **P1**: First visit selects the first supported browser locale; Chinese variants map to Chinese and unsupported-only lists fall back to English (A3, A6).
- **P2**: Manual selection wins over browser detection and is retained across later visits on the same origin (A3).
- **P3**: Blocked storage and no-script browsing retain usable language links; automatic navigation preserves query/fragment and settles without loops (A5, A6).

## Trade-offs and open questions

Saved preference takes priority over a directly shared edition URL; explicit
language links carry a choice parameter so readers can always override it.
Preferences are per browser, not synced across devices. Storage failure means the
choice cannot survive later navigation, but does not block reading. No open questions.

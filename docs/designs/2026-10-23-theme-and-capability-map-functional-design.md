---
artifact_type: functional-design
lifecycle: snapshot
created_at: 2026-10-23
parent: ../requirements-planning/AIC-REQ-02.md
status: approved
---

# Functional design: theme preference and capability atlas

## Goal

Help visitors understand the full asset library on the site and retain their preferred appearance while respecting system light/dark settings.

The user extended AIC-REQ-02 with both requests on 2026-10-23. This extends the
initial site's theme preference and catalogue discovery decisions.

## Functional modules and boundaries

| Module | Responsibility | Boundary |
| --- | --- | --- |
| Appearance | Follow system appearance by default; remember manual System/Light/Dark selection | Browser-local preference only |
| Capability atlas | Organize all current Skills into task domains, with purpose and output visible on site | Editorial grouping, not mandatory execution order |
| Shared foundation | Explain and enumerate Specs, Rules and Protocols | Source links are secondary references, not required for understanding the overview |

## Business workflow

```text
Visitor arrives → system appearance or saved choice → reads the site
  → changes theme → appearance updates → later visit retains that choice
  → opens capability atlas → scans task domains → expands a domain
    → reads skills and intended outcomes → explores shared contracts/constraints
    → optionally opens the defining source or proceeds to installation
```

## Exception and edge scenarios

- Storage denied: theme selection still works on the current page; later visits follow system.
- System theme changes: System mode follows immediately; manual Light/Dark remains fixed.
- JavaScript unavailable: system appearance and the complete native atlas remain usable.
- Small viewport: the atlas stacks in reading order; no pan/zoom or horizontal canvas is required.
- Registry changes: catalogue parity checks require both website editions to be updated.

## UI and interaction flow

Preserve the existing editorial typography, orange accent, tokens and native theme
selector. Replace the sampled capability list with a root label, six task-domain
branches and three shared foundation branches. Each branch is a native disclosure
containing asset names and plain-language descriptions. The root and connecting
lines express library membership; no arrow asserts a prerequisite or universal
sequence. Counts summarize the enumerated assets and are verified against registries.
The landing state shows domain purposes and likely outputs; expansion reveals all
assets without leaving the site. Existing source links remain optional inspection.

Reuse the runnable page as the visual baseline; no independent mockup is needed
because native responsive HTML is the review surface. Default/expanded/focused
states use existing disclosure and focus patterns. No remote loading, empty result,
account or permission states apply. The implementer verifies theme restoration,
System recovery, keyboard disclosure, both languages and 360px/1280px layouts.

## Acceptance criteria

- **M1**: Default/System follows OS appearance; manual Light/Dark/System is retained on later visits (A6).
- **M2**: Every registered asset appears once in the on-site atlas, grouped by its role, with a readable description (A2, A3).
- **M3**: Visitors can inspect domains and the shared foundation using native disclosures without visiting GitHub (A3, A5, A6).
- **M4**: Both editions support keyboard operation, light/dark appearance and mobile stacking without document overflow (A5, A6).

## Trade-offs and open questions

Choose a responsive atlas instead of a free-form mind-map canvas: visitors lose
free spatial arrangement but gain a stable reading order, full text, no-script
access and a usable mobile view. Grouping is editorial, while the four asset types
and definitions remain canonical. A large dependency graph could imply unsupported
relationships, so only membership and shared responsibilities are represented.
No blocking questions remain.

---
artifact_type: functional-design
lifecycle: snapshot
created_at: 2026-10-23
parent: ../requirements-planning/AIC-REQ-02.md
status: approved
---

# Functional design: website localization

## Goal

Let English and Simplified Chinese readers evaluate AI Cortex and complete the existing adoption path in their chosen language.

The user extended AIC-REQ-02 on 2026-10-23 to request a multilingual website.
This explicitly authorizes localized website display copy; asset instructions remain English.

## Functional modules and boundaries

| Module | Responsibility | Boundary |
| --- | --- | --- |
| Language navigation | Open English or Simplified Chinese edition | No automatic redirects or stored preference |
| Localized introduction | Present equivalent descriptions and actions | Source documents and asset names remain authoritative |
| Localized feedback | Explain clipboard outcomes in the page language | Commands and clipboard behavior remain identical |

## Business workflow

```text
Reader opens either language URL → reads that edition
  → selects English or 中文 → opens the other edition at the top
  → explores capabilities or copies installation commands → follows source guidance
```

## Exception and edge scenarios

- JavaScript disabled: both complete editions and language links remain usable.
- Copy denied: show localized recovery text and leave commands selectable.
- Shared URL opened on another device: its explicit language is preserved.
- Narrow viewport: language links wrap with the existing header navigation.

## UI and interaction flow

Retain the editorial layout, orange accent, four-layer diagram, native links,
focus treatment and theme selector. Add English / 中文 links to main navigation;
the active edition uses `aria-current="page"`. Selection is ordinary navigation
with no loading state, automatic locale detection or persistence. Going to the top
on language change makes the new edition's introduction discoverable. The native
browser handles navigation errors and retry. No empty/account states apply.

Independent mockups are unnecessary: the existing runnable page is the visual
baseline and this change extends its navigation pattern. The implementer verifies
both editions at 360px and 1280px, keyboard links, copy feedback and light/dark.
One anonymous role and no business objects mean permission/state models do not apply.

## Acceptance criteria

- **L1**: Both editions contain equivalent sections, commands and repository destinations (A2–A4).
- **L2**: Visible language links work without scripts and each language has a direct URL (A3, A6).
- **L3**: Titles, descriptions, accessible labels and copy feedback use the selected language (A4, A5).
- **L4**: Both editions fit mobile/desktop widths and retain keyboard focus and themes (A5, A6).

## Trade-offs and open questions

English remains the existing root URL; Chinese uses `/zh.html`. Explicit selection
avoids surprising redirects but requires Chinese readers entering the root to select
中文 once. Two static editions add content-maintenance work; structural parity
checks catch mismatched links and sections. Additional languages require reviewed
copy rather than an unverified automatic translation service. No blocking questions.

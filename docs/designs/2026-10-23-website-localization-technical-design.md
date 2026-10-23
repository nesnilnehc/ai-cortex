---
artifact_type: technical-design
lifecycle: snapshot
created_at: 2026-10-23
parent: 2026-10-23-website-localization-functional-design.md
status: approved
---

# Technical design: website localization

## Goal

Serve complete English and Chinese static HTML with shared styles and localized clipboard feedback.

## Architecture and service decomposition

| Component | Responsibility and dependencies |
| --- | --- |
| `index.html`, `zh.html` | Static editions; share local CSS/modules; external repository links only |
| `copy.mjs` | Clipboard controller with injected message object |
| `main.mjs` | Bind DOM and pass edition-specific feedback data |
| Tests | Compare static structure, language metadata and feedback outcomes |

## Components and detailed design

Implement the functional design's native language links inside existing navigation,
with `hreflang`, `lang` and active-page semantics. Both pages use the same IDs and
resource URLs. Set HTML language, canonical, Open Graph language and alternate
language links per edition. Sitemap lists both addresses. No locale routing code,
shared mutable state, storage or automatic detection is introduced.

Extend `bindCopyButton(button, source, feedback, clipboard, messages)` with an
optional English default message object (`copying`, `success`, `unavailable`,
`empty`). Both pages declare all four messages in the feedback element's data
attributes; browser composition passes its dataset. This keeps fallible clipboard
logic independent of language. Preserve the existing responsive breakpoints;
add Chinese heading measure/line-height overrides and flexible header navigation.

## Database design

No database change. No cookies or stored language preferences.

## Interface contracts

Anonymous `GET /` and `GET /zh.html` return complete HTML in English and Chinese,
respectively. Shared resource contracts are unchanged. Missing paths retain the
host's normal 404 behavior. No application API or authentication change.

## Data flow and error handling

HTML edition → localized DOM text and feedback data → clipboard controller →
localized pending/success/recovery output. A denied clipboard write retains retry;
a missing module leaves native navigation and all content available. Static parity
checks detect missing language links, changed destinations and metadata omissions.

## Technology choices and trade-offs

Choose separate static HTML editions: direct URLs, no-script access and no new
runtime dependencies, at the cost of keeping copy aligned. Runtime dictionary
replacement reduces markup duplication but delays translated rendering and needs
JavaScript. A template/build framework could generate editions but adds tooling
for a two-page site. Existing static hosting is sufficient.

## Test strategy

Observe failing localization contract tests before adding the Chinese edition.
Exercise localized pending, success, denial and missing-source controller outcomes.
Compare section IDs, resource URLs, source destinations, commands and language
metadata across pages. Run existing tests and document checks. The implementer
inspects both widths/themes, native language navigation and actual copy wiring
in a browser; automated structure checks do not prove visual acceptance.

## Quality attribute design

| source | rule_refs | design tactic | trade-off | verification | owner |
| --- | --- | --- | --- | --- | --- |
| L1, L2 | TST-001, TST-002 | Static structure parity and native navigation | Duplicate HTML | Contract tests and browser navigation | Site maintainer |
| L3 | TST-001, TST-002 | Inject messages at clipboard boundary | Four fields per edition | Controller and DOM data checks | Site maintainer |

## Acceptance criteria

- **T1**: Both editions pass content, link and search metadata checks (L1, L2).
- **T2**: Clipboard tests and browser feedback confirm edition language (L3).
- **T3**: 360px/1280px inspection confirms navigation, wrapping and themes (L4).

## Deployment and operations

Publish the existing runtime bundle plus `zh.html`; retain hosting identity and
custom domain. Recheck anonymous HTTPS and JavaScript MIME types after deployment.
Rollback can republish the prior Sites version; no data migration is involved.

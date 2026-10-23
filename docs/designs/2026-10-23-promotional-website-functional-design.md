---
artifact_type: functional-design
lifecycle: snapshot
created_at: 2026-10-23
parent: ../requirements-planning/AIC-REQ-02.md
status: approved
---

# Functional design: AI Cortex promotional website

## Goal

Help prospective adopters understand AI Cortex, identify a relevant capability
and begin installation from a single public introduction.

## Functional modules and boundaries

| Module | Responsibility | Boundary |
| --- | --- | --- |
| Introduction | Explain the project's value and asset model | No unsupported outcomes or social proof |
| Capability discovery | Offer delivery, governance and research entry paths | Canonical catalogues remain authoritative |
| Adoption | Present installation and project links | No installation execution or account creation |
| Questions | Explain compatibility and adoption constraints | Link detailed guidance rather than duplicate it |

## Business workflow

```text
Visitor arrives → reads purpose → chooses a next step
  → explore capabilities → open a relevant repository guide → exit to source
  → understand asset model → read definitions → continue to installation
  → get started → read/copy commands → exit to installation documentation
```

Only one public visitor role exists. There are no business objects or permission
differences, so business state and permission sections do not apply.

## Exception and edge scenarios

- Copy denied or unavailable: keep commands readable and show a manual-copy
  instruction; allow another copy attempt.
- JavaScript unavailable: keep navigation and expandable content functional;
  hide the unavailable copy action rather than offer an inert control.
- Narrow screen or enlarged text: stack the content, wrap navigation and allow
  code to scroll within its own container.
- Destination unavailable: ordinary links preserve the destination URL for retry;
  avoid claiming a remote resource is currently online.

## UI and interaction flow

Choose a technical editorial direction: asymmetric introduction, one orange
accent, neutral surfaces, typography-led hierarchy and a four-layer content
diagram. DESIGN_VARIANCE 6, MOTION_INTENSITY 3, VISUAL_DENSITY 4. Use restrained
hover feedback only. A single page avoids inter-page navigation before adoption.
The alternative of a documentation portal adds a second documentation authority
and makes the introductory path longer; a slogan-only landing page omits the
specific capability evidence users need.

Visitors enter through the home page or section anchors. Navigation links lead
to capabilities, the asset model and installation; task examples exit to real
repository Skills and guides. Native disclosures reveal optional details and FAQ
answers. Copy states are default, pending, success and recoverable failure, with
announced feedback. No remote data loads, empty results or account states apply.

There is no existing website stack, visual system or licensed brand artwork to
preserve in this checkout. Reuse the README's content and canonical names.
System light/dark themes, an optional System/Light/Dark selector, focus visibility,
semantic headings, a skip link and reduced-motion support are required. Theme
selection lasts for the current page only. English follows project language policy.
Independent pixel mockups are unnecessary for this bounded page: the runnable
implementation is the visual review surface. No external visual assets are used.

Acceptance handoff: the implementing agent checks F1–F5 in a real browser at
360px and 1280px, using pointer and keyboard, and inspects both themes. Test
evidence belongs in the implementation's [site guide](../../website/README.md).

## Acceptance criteria

- **F1**: Introduction and layer definitions agree with source documents (A2).
- **F2**: A visitor reaches a relevant capability, catalogue or guide (A3).
- **F3**: Installation copy succeeds or offers manual recovery (A4, QA1).
- **F4**: Navigation and disclosures work at both widths and by keyboard (A5).
- **F5**: Both themes and no-script content preserve the adoption path (A6).

## Trade-offs and open questions

The page serves an English-reading developer audience under repository policy.
A localized edition could broaden reach but adds ongoing content maintenance.
Hosting and DNS remain non-blocking for local design and implementation, and
blocking for public availability; the project owner resolves these at deployment.

Review: self-reviewed with functional-design-modeling 2.0.0 and
functional-design-quality 2.0.0 before technical design. No findings; the single
role, absence of business state and decision to use the runnable page are explicit.

---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: requirement
date: 2026-10-23
status: done
priority: unset
strategic_goal_id: goal-4
source: user
---

# Create an AI Cortex promotional website

## Problem / Need

Prospective AI Cortex adopters need a clear introduction to the project's value,
available capabilities and ways to get started, so they can decide whether it fits
their delivery and governance work.

The user requested a promotional website and supplied `ai-cortex.nesnilnehc.top`.
The audience and adoption need above are grounded in the project's
[README](../../../README.md) and
[Goal 4: adoption friction is low](../../project-overview/strategic-goals.md#goal-4-adoption-friction-is-low).
The goal mapping is inferred from that adoption objective.

## Acceptance Criteria

- [x] A public promotional website is available at `https://ai-cortex.nesnilnehc.top`.
- [x] Visitors can understand AI Cortex's purpose and the value of its delivery
  and governance capabilities from the website.
- [x] Visitors can find the project's capability catalogue and installation/use
  instructions through clear links to the authoritative repository sources.
- [x] Website descriptions agree with the project's current README and asset
  terminology, without unsupported capability claims.

## Notes

- Design and implementation were explicitly authorized by the user on 2026-10-23.
  Local implementation follows [AIC-REQ-02](../../requirements-planning/AIC-REQ-02.md),
  the [functional design](../../designs/2026-10-23-promotional-website-functional-design.md)
  and the [technical design](../../designs/2026-10-23-promotional-website-technical-design.md).
  See the [site guide](../../../website/README.md) for preview and verification.
  Public deployment was subsequently authorized and completed on 2026-10-23.
  The custom hostname, certificate and provider are active; homepage and static
  resources passed anonymous HTTPS checks. See the site guide for retained evidence.

- The website request and domain come directly from the user. Acceptance criteria
  concerning introductory content, discovery, onboarding and factual accuracy are
  grounded in the README and Goal 4; they are intake inferences rather than an
  approved design.
- The supplied domain is the public website address. NameSilo DNS and Sites hosting
  were configured and verified during deployment; unrelated DNS records were preserved.
- Design resolved layout, static implementation and English website content under
  repository policy on 2026-10-23. Sites provides hosting. No traffic or
  conversion targets were introduced.
- Artifact prose is English under the existing
  [artifact norms](../../ARTIFACT_NORMS.md) and
  [language policy](../../LANGUAGE_SCHEME.md); this does not determine the website's
  language.

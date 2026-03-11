# Claude Plugin Skill Subset Policy

This directory contains a curated subset for Claude Plugin distribution.
It is intentionally non-exhaustive and does not represent the full catalog under `skills/`.

## Selection Criteria

- Prioritize high-frequency, low-dependency skills with broad utility.
- Prefer skills that help discovery, onboarding, and governance-first authoring.
- Keep subset size small to reduce plugin payload and improve selection quality.

## Exclusion Criteria

- Exclude most atomic review skills such as `review-*` that are usually routed by orchestrator skills.
- Exclude niche lifecycle helpers used only in specific internal workflows.
- Exclude experimental or low-adoption skills until usage is stable.

## Source of Truth

- Full canonical catalog: `skills/INDEX.md` and `manifest.json`.
- This subset should be updated only when channel strategy changes or when a skill is promoted to plugin priority.

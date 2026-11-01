---
artifact_type: guide
lifecycle: living
created_at: 2026-09-18
status: active
---

# Releasing AI Cortex

This repository owns its release procedure. It does not require generic release Skills or a Release Package. Consumer projects define their own build, artifact, store and announcement workflows. See the [scope decision](../adr/0017-project-owned-releases.md).

Before a release, inspect the intended changes, run the applicable checks in [CONTRIBUTING](../../CONTRIBUTING.md#checks), and apply the [stable-core policy](../project-overview/stable-core.md). Obtain authorization for commits, tags, pushes and provider writes. No release is authorized by this guide alone.

The product version lives in Git tags. Independent Skill, Rule and Spec versions follow their own actual changes. Keep released changelog sections frozen, prepare the new changelog entry, and verify the chosen commit and tag before publication. Record actual provider results and incomplete steps; reconcile existing state before retrying a remote action.

Historical published records remain evidence of past releases, not runtime dependencies or a supported Release Package contract.

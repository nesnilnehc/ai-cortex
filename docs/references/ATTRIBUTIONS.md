---
artifact_type: reference
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# Sources and attributions

<!-- markdownlint-disable MD058 MD060 -->

This file is the human-readable index of [`skills/SOURCES.yaml`](../../skills/SOURCES.yaml), listing the externally derived skills AI Cortex currently distributes. The detail is in [LICENSE_POLICY.md](./LICENSE_POLICY.md).

---

## By repository

| Repository | Upstream path | Pinned commit | License | Local skill | What was changed locally |
| --- | --- | --- | --- | --- | --- |
| [softaworks/agent-toolkit](https://github.com/softaworks/agent-toolkit) | `skills/commit-work` | `06825f04669d4364a16abc267650c86cf153d349` | MIT | `commit-work` | Kept the commit workflow; integrated AI Cortex review, the INDEX and the output contract |
| [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes) | `.agents/skills/changelog-video` | `4f00336c92f6418aab82c060853da604dd832197` | Apache-2.0 | `changelog-video` | Switched the input to a Release Package; removed the brand assets, fixed voices, repository paths and sibling-skill dependencies |

---

## Notes

- The record once gave `commit-work`'s source as an unverified `anthropics/skills (assumed)`; the table above uses `softaworks/agent-toolkit`, which is verifiable and matches the content.
- The skills.sh page exists for discovery only; it is not where AI Cortex installs or updates from.
- The full digests, the list of modifications and the update policy are authoritative in `skills/SOURCES.yaml`.

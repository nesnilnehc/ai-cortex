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

## eli5

Source: [anthropics/claude-plugins-community](https://github.com/anthropics/claude-plugins-community/tree/06ec7b6a0a82bdc4bec44bd82d4368c42f20d7c1/eli5/skills/eli5), commit `06ec7b6a0a82bdc4bec44bd82d4368c42f20d7c1`; Apache-2.0. Local Skill: [eli5](../../skills/eli5/SKILL.md). Metadata and host integration were adapted; see the source registry for exact changes.

## ponytail

Source: [dietrichgebert/ponytail](https://github.com/dietrichgebert/ponytail/tree/09c434ab73ca43761c5d8b0c5d341926c2fba710/skills/ponytail), commit `09c434ab73ca43761c5d8b0c5d341926c2fba710`; MIT. Local Skill: [ponytail](../../skills/ponytail/SKILL.md). Metadata and host integration were adapted; see the source registry for exact changes.

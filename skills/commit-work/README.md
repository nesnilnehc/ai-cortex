# Commit Work

Create reviewable git commits from authorized changes: inspect the working tree, choose logical boundaries, stage precisely, verify, and explain what changed and why.

- **Current version**: 2.2.0
- **License**: MIT

## Use

Ask to commit a named scope, split mixed changes, stage work, or draft a Conventional Commits message. Staging and message-only requests do not create commits. The skill preserves other tasks' changes and finishes when the authorized scope is complete, even if the working tree remains dirty.

It reuses current review and verification evidence and follows project requirements. It does not introduce a mandatory review round trip. Related tests stay with their behavior change; independent changes can form separate commits. Inside AI Cortex, required registry synchronization remains part of preparation.

See [SKILL.md](SKILL.md) for the workflow, inputs, outputs, boundaries, and a mixed-work example; use the [message template](references/commit-message-template.md) for message details. Push and pull requests are separate workflows.

## Source and installation

This is a locally adapted copy of `commit-work` from `softaworks/agent-toolkit`. It retains upstream inspection, logical splitting, patch staging, and Conventional Commits guidance. Local adaptations cover project review requirements, AI Cortex registry synchronization, scoped completion, and output reporting.

The pinned upstream and license record are in [SOURCES.yaml](../SOURCES.yaml), with copyright notices in [THIRD_PARTY_NOTICES](../../docs/references/THIRD_PARTY_NOTICES.md). Installation is handled centrally; see the root [README](../../README.md#-install-and-use). Do not fetch or replace the skill at runtime.

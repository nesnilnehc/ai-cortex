---
type: requirement
date: 2026-03-06
status: captured
source: user
---

# New Skill: prune-content (Clean up outdated project content)

## Problem / Need
The project accumulates outdated content (historical residue) that no longer aligns with the current project state or trends. Handling this manually is inefficient and error-prone. We need a reusable **Skill** to automate the identification and archiving of such content.

## Acceptance Criteria
- [ ] Create a new Skill (e.g., `prune-content` or `archive-outdated`).
- [ ] The Skill should identify content based on rules:
    - Marked as 'deprecated' in content or filename.
    - Explicitly configured "stale" thresholds (e.g., > 6 months inactivity).
    - Specific target directories.
- [ ] The Skill should support:
    - **Scan Mode**: Report findings without deleting.
    - **Archive Mode**: Move content to an `_archive/` directory.
    - **Delete Mode**: Permanently remove content (with confirmation).
- [ ] Establish a process to run this Skill periodically.

## Notes
User definition of expired: "内容已经过时的，不符合当前项目的状态或趋势的历史残留" (Content that is outdated, does not fit the current project state or trends).
Converted from a one-off task to a Skill creation request.

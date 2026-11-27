---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: requirement
date: 2026-11-10
status: done
priority: unset
strategic_goal_id: [goal-3]
source: user
---

# Name the current AI agent session

## Problem / Need

People using AI agents need to recognize and retrieve the current session.
Its title may be vague, too long, or describe only a skill; the working
directory may not reflect the actual subject. Hosts differ in their ability
to change session titles.

## Acceptance Criteria

- [x] A request for a suggestion returns a title based on the current session's
  actual subject and goal without modifying the title.
- [x] A request to rename the current session uses a supported host capability
  when available and authorized; otherwise it returns the suggestion and
  accurately explains the limitation or outcome.
- [x] Naming follows the user's explicit title or preferences first. A default
  may include project or domain, subject and goal, but no format is mandatory.
  A working directory alone does not establish the project or topic.
- [x] Suggestions, titles and reports omit credentials and other sensitive
  information. Missing or uncertain subject details are not invented.
- [x] Only the current session is in scope. The capability does not scan or
  modify other sessions, change internal databases or session files, create
  schedules, install tools or persist preferences as part of naming.

## Notes

The user narrowed the initial proposal to one session-level Skill. A global
Rule, historical-session analysis and batch renaming are outside this intake.
The initial portable draft was [rename-session](../../../experiments/session-naming/rename-session/SKILL.md).

Implemented and verified on `main` as [rename-session](../../../skills/rename-session/SKILL.md)
(`0.1.1`), covering all five acceptance criteria above. Maintainer provenance
confirmation is recorded in
[rename-session-0-1-1-20261124.json](../../../experiments/skill-provenance/confirmations/rename-session-0-1-1-20261124.json);
catalogue synchronization, website deployment (Sites version 36) and SkillHub
`0.1.1` upload are recorded in
[publication-20261124-rename-session-0-1-1.json](../../../website/.openai/publication-20261124-rename-session-0-1-1.json).

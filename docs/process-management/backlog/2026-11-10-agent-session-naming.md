---
artifact_type: backlog-item
created_by: capture-work-items
lifecycle: living
type: requirement
date: 2026-11-10
status: captured
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

- [ ] A request for a suggestion returns a title based on the current session's
  actual subject and goal without modifying the title.
- [ ] A request to rename the current session uses a supported host capability
  when available and authorized; otherwise it returns the suggestion and
  accurately explains the limitation or outcome.
- [ ] Naming follows the user's explicit title or preferences first. A default
  may include project or domain, subject and goal, but no format is mandatory.
  A working directory alone does not establish the project or topic.
- [ ] Suggestions, titles and reports omit credentials and other sensitive
  information. Missing or uncertain subject details are not invented.
- [ ] Only the current session is in scope. The capability does not scan or
  modify other sessions, change internal databases or session files, create
  schedules, install tools or persist preferences as part of naming.

## Notes

The user narrowed the initial proposal to one session-level Skill. A global
Rule, historical-session analysis and batch renaming are outside this intake.
The proposed portable draft is [rename-session](../../../experiments/session-naming/rename-session/SKILL.md).
Its discovery and registration remain subject to the repository's provenance
review and [contribution process](../../../CONTRIBUTING.md#adding-a-skill).

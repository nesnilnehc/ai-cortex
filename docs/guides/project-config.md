---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# Project configuration

A skill that depends on project configuration — automate-tests, orchestrate-repair-loop, commit-work, generate-github-workflow and the like — behaves as described below, which is what keeps it platform-independent.

---

## 1. Read the configuration first

Where either of these exists, read the project-specific values from it first:

- **CLAUDE.md**: the Claude or agent configuration at the project root, where the project follows that convention
- **.ai-cortex/config.yaml**: the machine-readable AI Cortex project configuration

**Configurable fields**, extended as needed:

| Field | Meaning | Skills that use it |
| :--- | :--- | :--- |
| `test_command` | The test command or script | automate-tests, orchestrate-repair-loop, commit-work |
| `base_branch` | The name of the main branch, such as main or master | Any skill that touches a PR or detects a branch |
| `deploy_command` | The deployment command | Deployment-related skills |

---

## 2. Ask when it is missing

Where there is no configuration, or the field you need is absent, get it with AskUserQuestion. Never guess it, and never hard-code it.

---

## 3. Persist it

Write the configuration the user confirmed into `.ai-cortex/config.yaml`, or wherever the project keeps it, so later runs can reuse it. Ask the user before writing.

---

## 4. How this relates to a skill's own discovery logic

This does not replace the discovery logic a skill already has, such as inferring from a dependency or build manifest, a CI configuration, or the documentation. Configuration wins over inference, and an inferred value can be offered for writing into the configuration for next time.

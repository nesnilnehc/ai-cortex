---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-24
status: active
---

# Project configuration

A skill that depends on project configuration — automate-tests, orchestrate-repair-loop, commit-work, generate-github-workflow and the like — should behave as described below, which is what keeps it platform-independent.

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
| `governance.profiles` | Contexts that activate conditionally mandatory engineering Rules | review-* cognitive skills, review-technical-design, review-tasks |
| `governance.parameters` | Project topology, protected contracts, quality targets and change budgets referenced by Rules | review-* cognitive skills |
| `governance.waivers` | Narrow, approved and expiring Rule exceptions | review-* cognitive skills, orchestrate-code-review, orchestrate-repair-loop |

The data contract and validity rules for these governance fields are in [rule-modeling](../../specs/rule-modeling.md). A profile is not an opt-out switch: when its context holds, its Rule items are mandatory. Project parameters supply facts; they do not copy or rewrite canonical Rule text.

### What you actually have to write

Every parameter carries a provenance ([rule-modeling §5.4](../../specs/rule-modeling.md)) that decides who supplies its value:

| Provenance | Who supplies it | Examples |
| :--- | :--- | :--- |
| `derived` | The reviewer computes it from the repository. You never write it, and narrow it only when the derivation is wrong. | module list, protected contracts, approved cryptography, authoritative artifact paths |
| `baseline` | Recorded from the present state at the first review; afterwards only new deterioration fails. | allowed module dependencies, change budgets |
| `declared` | You. It is a business decision that cannot be read off the code. | service-level objectives, performance budgets, critical operations, indicator targets, data classification, coverage policy |

So the smallest useful configuration is the profiles alone:

```yaml
governance:
  profiles: [deployable-service, public-api]
```

At that point every baseline item already runs, structural topology is baselined on the first review, and only the target-shaped items wait on you. Nothing is silently switched off: an item waiting for a `declared` value is reported as evidence-limited together with the decision it is waiting for, never as a pass.

Add the `declared` values as you decide them:

```yaml
test_command: npm test
base_branch: main
governance:
  profiles: [deployable-service, public-api, remote-dependency]
  parameters:
    reliability:
      slo:
        availability: 99.9%
        window: 30d
    performance:
      budgets:
        checkout_p95_ms: 400
```

Topology can still be written by hand when a project wants to state its intended architecture rather than freeze its current one:

```yaml
governance:
  parameters:
    architecture:
      allowed_dependencies:
        domain: []
        application: [domain]
        infrastructure: [application, domain]
        api: [application]
```

---

## 2. Ask when it is missing

Resolve an absent value by its provenance before asking anyone. Compute a `derived` value from the repository. Take or read a `baseline` snapshot, and report that item as baselined rather than passed on the run that creates it. Only a `declared` value is worth a question, and then ask for the decision, not for the YAML.

Never guess, and never hard-code. A missing value never suppresses a baseline Rule and never becomes a pass: it makes that one item evidence-limited, and the coverage report names what it is waiting for.

---

## 3. Persist it

Write the configuration the user confirmed into `.ai-cortex/config.yaml`, or wherever the project keeps it, so later runs can reuse it. Ask the user before writing.

Do not persist inferred facts into provider memory as a substitute for this file. Memory may cache a verified pointer or lesson, but normative profiles, topology, targets and waivers belong in version-controlled project configuration or their owning requirement/ADR.

---

## 4. How this relates to a skill's own discovery logic

This does not replace the discovery logic a skill already has, such as inferring from a dependency or build manifest, a CI configuration, or the documentation. Configuration wins over inference, and an inferred value can be offered for writing into the configuration for next time.

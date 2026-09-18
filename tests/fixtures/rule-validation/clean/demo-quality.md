---
artifact_type: rule
name: demo-quality
version: 1.0.0
model: RULE_MODEL_V1
rule_prefix: DEMO
scope: a fixture standing in for a modeled Rule set
recommended_scope: project
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-01-01
---

# Rule: Demo Quality

## Scope

Two items, enough to exercise identifier, field and ordering checks.

## Profiles and parameters

No profiles.

## Rules

### DEMO-001 — A demonstration obligation

| Field | Value |
| --- | --- |
| Level | `baseline` |
| Requirement | A scope **MUST** carry the thing this fixture stands for. |
| Applies when | Always, in this fixture. |
| Default severity | `major` |
| Enforcement | `automated` |
| Evidence | The fixture itself. |
| Pass condition | The item parses with every required field present. |
| Not applicable when | Never; the fixture exists to be parsed. |
| Remediation | Restore the field the test removed. |

### DEMO-002 — A second obligation, so ordering has something to order

| Field | Value |
| --- | --- |
| Level | `profile:demo` |
| Requirement | A second item **MUST NOT** share an identifier with the first. |
| Applies when | A document carries more than one item. |
| Default severity | `minor` |
| Enforcement | `judgment` |
| Evidence | The identifiers in this document. |
| Pass condition | Every identifier in the document is distinct. |
| Not applicable when | The document carries one item. |
| Remediation | Renumber the duplicate. |

## Severity and gate policy

Fixture policy: nothing gates.

## Waivers

Fixture waivers: none.

## References

None.

---
artifact_type: rule
name: other-quality
version: 2.1.3
model: RULE_MODEL_V1
rule_prefix: OTHR
scope: a second fixture, so a duplicate identifier can cross a document boundary
recommended_scope: both
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-01-02
---

# Rule: Other Quality

## Scope

One item. It exists so that an identifier can be duplicated across two files.

## Profiles and parameters

No profiles.

## Rules

### OTHR-001 — An obligation owned by the other document

| Field | Value |
| --- | --- |
| Level | `baseline` |
| Requirement | An identifier **MUST** be owned by exactly one document. |
| Applies when | A directory holds more than one modeled Rule. |
| Default severity | `critical` |
| Enforcement | `tool-assisted` |
| Evidence | The identifiers across every document in the directory. |
| Pass condition | No identifier appears in two documents. |
| Not applicable when | The directory holds one document. |
| Remediation | Give one of the two a new identifier. |

## Severity and gate policy

Fixture policy: nothing gates.

## Waivers

Fixture waivers: none.

## References

None.

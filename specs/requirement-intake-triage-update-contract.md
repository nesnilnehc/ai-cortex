---
contract_version: 1.0.0
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-06-18
status: accepted
---

# requirement-intake-triage-update-contract

The notification contract by which ai-cortex broadcasts governance updates to requirement intake triage downstream. Fire-and-forget: each consumer decides for itself when to align.

## Contract overview

| Item | Value |
|---|---|
| **Subject** | `cortex.updates.requirement-intake-triage` |
| **Stream** | `CORTEX` |
| **Producer** | `ai-cortex` |
| **Consumer** | `recloud-wright`, subscribing to `cortex.updates.>` |
| **QoS** | at-most-once — it is a notification, and a lost one can be recovered from the repository diff |

## Headers

| Header | Required | Value |
|---|---|---|
| `Nats-Msg-Id` | ✅ | UUID v7, generated at send time; a retry reuses the same ID |
| `X-Source` | ✅ | `ai-cortex` |
| `X-Type` | ✅ | `requirement-intake-triage.published` |
| `Content-Type` | ✅ | `application/json` |

## Payload Schema

```json
{
  "event": "published",
  "artifact": "requirement-intake-triage",
  "artifact_kind": "rule",
  "artifact_version": "1.0.0",
  "artifact_path": "rules/requirement-intake-triage.md",
  "summary": "Adds the requirement intake triage vocabulary: 6 kinds (functional / non-functional requirement, design proposal, task, defect, insufficient information) plus decision questions and soundness lenses, as the diagnostic SSOT shared by clarification and review.",
  "related_changes": [
    {"artifact": "requirement-modeling", "version": "5.0.0", "breaking": true,
     "note": "Requirement types narrowed to functional and non-functional; bug fixes and technical tasks demoted to triage labels rather than requirements"},
    {"artifact": "technical-design-modeling", "version": "2.0.0", "breaking": true,
     "note": "Purely technical work re-anchors its parent to an authorising ADR; enum is {functional-design, requirement, adr}"}
  ],
  "consumer_action": "Align Wright's StubVerdict grades (qualified / salvageable / tech_selection / empty) with the 6 kinds; treat defects and technical tasks as triage labels rather than requirement subtypes.",
  "anchor_ref": "requirement-intake-triage@1.0.0"
}
```

Tolerant Reader: a consumer must ignore unknown fields and unknown enum values.

## CHANGELOG

### 1.0.0 — 2026-06-18

**Initial Release**: the first broadcast of a requirement intake triage governance update — the `requirement-intake-triage@1.0.0` vocabulary published, `requirement-modeling@5.0.0` narrowing its types, and defect and technical task demoted to triage labels.

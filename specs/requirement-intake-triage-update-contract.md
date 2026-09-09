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
  "summary": "新增需求进件分诊词表：6 类性质（功能需求/非功能需求/设计方案类/任务类/缺陷类/信息不足）+ 判别问句 + 合理性镜头，作为澄清与评审共用的诊断 SSOT。",
  "related_changes": [
    {"artifact": "requirement-modeling", "version": "5.0.0", "breaking": true,
     "note": "需求类型收窄为功能/非功能；缺陷修复、技术任务降级为分诊标签（非需求）"},
    {"artifact": "technical-design-modeling", "version": "2.0.0", "breaking": true,
     "note": "纯技术工作的 parent 重锚至授权 ADR；枚举 {functional-design, requirement, adr}"}
  ],
  "consumer_action": "Wright 的 StubVerdict 档位（qualified/salvageable/tech_selection/empty）向 6 类性质对齐；缺陷/技术任务按分诊标签处理，不再视为需求子类型。",
  "anchor_ref": "requirement-intake-triage@1.0.0"
}
```

Tolerant Reader: a consumer must ignore unknown fields and unknown enum values.

## CHANGELOG

### 1.0.0 — 2026-06-18

**Initial Release**: the first broadcast of a requirement intake triage governance update — the `requirement-intake-triage@1.0.0` vocabulary published, `requirement-modeling@5.0.0` narrowing its types, and defect and technical task demoted to triage labels.

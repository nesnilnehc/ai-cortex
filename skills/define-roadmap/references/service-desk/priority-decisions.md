# Service Desk priority decisions

Finished output of policy application at W0. The authority is the
[project policy](priority-policy.md). No four-framework reassessment is
requested, so settled decisions remain in place. The fictional product owner
authorizes deterministic application of that policy.

## Decisions

| ID | Previous | Final | Decision basis | Disposition |
| --- | --- | --- | --- | --- |
| BUG1 | unset | P0 | Active-customer data-integrity blocker | Set under policy |
| R1 | P1 | P1 | Confirmed search need | Preserve settled priority |
| R2 | P1 | P1 | Confirmed export need | Preserve settled priority |
| R3 | unset | P2 | Unvalidated convenience request | Set under policy |

## Persisted decision example

This is the complete decision annotation for BUG1, shown in an adopting project's
multi-file layout. The editorial date identifies the teaching snapshot.

```yaml
priority: P0
priority_decision:
  final: P0
  previous: unset
  mode: policy-application
  policy_ref: priority-policy.md
  rationale: Active-customer duplicate submission threatens data integrity.
  decided_by: auto
  decided_at: 2026-10-20
```

Scanned: 4; changed: 2; preserved: 2; unresolved: 0; declined: 0.
Final distribution: P0 = 1, P1 = 2, P2 = 1, P3 = 0.
No tier, approval, execution, version or date is changed by priority application.
Next output: [dependency register](dependencies.md).

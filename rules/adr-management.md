---
artifact_type: rule
name: adr-management
version: 1.0.0
scope: docs/adr/ 下的所有 ADR 文档
recommended_scope: user
status: active
---

# Rule: ADR Management

## Scope

Every act of creating or maintaining an Architecture Decision Record under `docs/adr/`. Data structure constraints live in [specs/adr-modeling.md](../specs/adr-modeling.md); this rule constrains behaviour — admission, status enforcement, decay and boundaries.

---

## §1 Admission test

Before writing an ADR, answer two questions. **Write one only when both answers are yes.**

**Q1: will anyone want to look up the why of this decision six months from now?**
(That is: not self-evident, of historical value, affecting long-term structure.)

**Q2: is that why impossible to convey through some combination of a rule, a commit message, a PR description and the README?**
(That is: runtime constraints or commit history cannot adequately explain the background.)

### Both yes → write the ADR

### Either no → do not write an ADR; use the alternative

| Situation | Where it belongs |
|---|---|
| Why this code changed | commit message |
| Why this PR did it this way | PR description |
| A coding convention | `rules/*.md` |
| A documentation move or directory reorganisation | commit + PR + README |
| How to use a technical framework | `docs/guides/*.md` |

### Counter-examples — do not write an ADR for these

- A routine bug fix or a small feature addition
- A file rename or directory move, where the process-level why is fully covered by the commit and PR
- A normative constraint — write a rule, not a record saying "we decided to follow the convention"
- A local refinement of an existing ADR — append to that ADR's consequences or notes instead

---

## §2 Status field enforcement

### One source for status

The `status` field is **written once, in the frontmatter**, using a 5-value enum:

```text
proposed | accepted | superseded | archived | rejected
```

### Strictly forbidden

- ❌ A `**状态**：Accepted` line in the body, or any variant of it
- ❌ `**Status**:`, `**状态**：`, `Status: Accepted` and the like in the body
- ❌ Legacy enum values: `draft` / `active` / `approved` / `已批准` / `live`
- ❌ The retired fields `implementation_status` / `decision_status` — delete them where they linger

### Status transition rules

| Target status | Additional required fields |
|---|---|
| `superseded` | `superseded_by: NNNN-{slug}` |
| `archived` | `archived_at: YYYY-MM-DD` plus `archived_reason: <reason>` |

---

## §3 Decay policy

ADRs should evolve with the lifecycle of their decisions — the collection is not append-only.

### Trigger for archiving (→ archived)

Change status to `archived` when **all** of the following hold:

1. Created **≥ 12 months** ago
2. **No document has referenced it** in the last 12 months (`grep -r "NNNN-" docs/ skills/ rules/ specs/` finds nothing)
3. The decision it describes **no longer affects current system behaviour**

The edit:

```diff
- status: accepted
+ status: archived
+ archived_at: YYYY-MM-DD
+ archived_reason: decision is stale; the mechanism it describes has been removed or replaced
```

### Physical deletion (git rm)

`git rm` is permitted when **all** of the following hold:

1. `status: archived` and `archived_at` is **≥ 6 months** ago
2. No file references the ADR
3. **Except for ADRs themselves**: an ADR is never physically deleted through decay — decision history is organisational memory

### Kept permanently

These are **never physically deleted**, however old:

- `status: rejected` — a rejected decision is decision history too
- `status: superseded` — the supersession relationship is needed to follow the evolution
- Any ADR referenced by another ADR's `superseded_by` field

---

## §4 Boundary between rules and decisions

`rules/` and `docs/adr/` serve different audiences, and no automatic derivation is built between them:

| Dimension | `rules/` | `docs/adr/` |
|---|---|---|
| Audience | Claude agent, loaded at runtime | People, consulted for history |
| Tense | Currently effective constraint | Snapshot of a decision at a point in time |
| Content | Behavioural rules — active constraints | Decision records — why plus alternatives |
| Updates | Revised continuously as conventions evolve | Not edited after writing, except the status field |

**Not built**: a rule does not generate an ADR automatically, and ADR content is not synchronised into a rule automatically. Traceability between the two is established by hand, through cross-references.

---

## Bad patterns

```markdown
<!-- ❌ status written twice, once in the body -->
# ADR 0001：xxx

**状态**：Accepted
**日期**：2026-03-24
```

```yaml
# ❌ legacy enum value
status: active
```

```yaml
# ❌ superseded without superseded_by
status: superseded
```

```yaml
# ❌ archived without the required fields
status: archived
```

---

## Remediation

1. **Remove the duplicated status**: delete the `**状态**：` and `**日期**：` lines after the H1 — the date is already in the frontmatter `created_at`
2. **Replace legacy enum values**: `active` → `accepted`; `draft` → `proposed`; `approved` → `accepted`
3. **Add the conditional fields**: `superseded_by` for `superseded`; `archived_at` and `archived_reason` for `archived`
4. **Delete retired fields**: grep for `implementation_status\|decision_status` and remove

---

## Related guidance

- **Data contract**: [specs/adr-modeling.md](../specs/adr-modeling.md)
- **Artifact norms**: [docs/ARTIFACT_NORMS.md](../docs/ARTIFACT_NORMS.md)
- **ADR index**: [docs/adr/README.md](../docs/adr/README.md)

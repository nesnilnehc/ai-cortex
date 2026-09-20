---
contract_version: 0.2.0
status: draft
inferred_from: bootstrap-peek
inferred_at: 2026-09-20T10:40:00+08:00
inferred_sample_size: 10
inferred_sample_seq_range: 1-12
authoritative: false
---

> ⚠️ **Not authoritative.** This contract was inferred by the `consume-nats-message` Bootstrap
> mode from a read-only peek at the `CORTEX` stream. No producer owner has confirmed it.
> Three blocking questions in [§7 Open questions](#7-open-questions) must be settled before
> `status` may be raised to `active` and `authoritative` to `true`. Until then, no message on
> this subject space may be formally acked.

# proposals-contract

The inbound channel by which an adopting project proposes a change to an `ai-cortex` asset —
a rule, a norm or a principle. Many-to-one fan-in: any adopter may publish, `ai-cortex` is the
sole consumer.

## 1. Subject naming

```text
cortex.proposals.<kind>.<slug>
```

| Segment | Meaning | Observed values |
| --- | --- | --- |
| `cortex` | Target project domain | — |
| `proposals` | Event domain | — |
| `<kind>` | Target artifact type | `principle`, `norm`, `rule` |
| `<slug>` | Proposal identifier, kebab-case | one distinct value per proposal |

**This shape is disputed — see [Q1](#q1-blocking--the-subject-carries-a-per-proposal-slug).**
A per-proposal `<slug>` segment makes subject cardinality unbounded, which collides with
[nats-messaging §2.3](../../../specs/nats-messaging.md) ("each subject has one contract file")
and prevents any exact-subject contract resolution from ever matching.

## 2. Producer identity

Two publishers have been observed on this subject space:

| Publisher | Observed in | Payload `source_project` |
| --- | --- | --- |
| recloud-agentfabric | seq 1–8 | `recloud-agentfabric` |
| shijian | seq 11–12 | `shijian` |

Per [nats-messaging §5.2](../../../specs/nats-messaging.md), the authoritative originator is the
`X-Source` **header**, not the payload field. The payload `source_project` is business data and
must not be relied on for routing, ACL or contract resolution.

**This contract is keyed on the subject, not on the publisher.** It is filed flat under
`vendor_contracts_dir`, per [cross-team-contract §3](../../../specs/cross-team-contract.md);
a per-publisher subdirectory would restate one schema twice and is not justified until this
integration domain holds ≥ 10 contracts from heterogeneous sources.

## 3. Headers

**Unknown — see [Q2](#q2-blocking--header-presence-is-unverified).** The sampling tool available
during Bootstrap returns payloads only and does not surface headers, so presence cannot be
distinguished from non-display. Nothing in this table may be treated as observed fact.

| Header | Required | Value | Status |
| --- | --- | --- | --- |
| `Nats-Msg-Id` | ✅ per spec | UUID v7, reused on retry | unverified on the wire |
| `X-Source` | ✅ per spec | publisher service name | unverified on the wire |
| `X-Type` | ✅ per spec | aligned with the subject's trailing segment | unverified on the wire |
| `Content-Type` | ✅ per spec | `application/json` | unverified on the wire |

## 4. Payload

```json
{
  "proposal_id":    "<string>",
  "source_project": "<string>",
  "source_commit":  "<string>",
  "target": {
    "kind":   "<string>",
    "path":   "<string>",
    "anchor": "<string>"
  },
  "action":    "<string>",
  "title":     "<string>",
  "rationale": "<string>",
  "proposed_change": {
    "format":  "<string>",
    "content": "<string>"
  },
  "evidence": {
    "<source_project>_examples": ["<string>"],
    "issue_observed":            "<string>"
  },
  "supersedes": null,
  "created_at": "<ISO 8601>"
}
```

### 4.1 Field table

| Field | Type | Required | Enum | Notes |
| --- | --- | --- | --- | --- |
| `proposal_id` | string | ✅ | — | `<project>-<date>-<NNN>-<slug>`, globally unique |
| `source_project` | string | ✅ | — | Business data only; not the routing identity (see §2) |
| `source_commit` | string | ✅ | — | Full SHA or short SHA; both observed |
| `target.kind` | string | ✅ | `principle`, `norm`, `rule` | Agrees with the subject's `<kind>` segment |
| `target.path` | string | ✅ | — | Path within the target project |
| `target.anchor` | string | ✅ | — | Anchor within the target file |
| `action` | string | ✅ | `add`, `modify` | |
| `title` | string | ✅ | — | |
| `rationale` | string | ✅ | — | |
| `proposed_change.format` | string | ✅ | `full-text`, `freeform`, `markdown-patch` | |
| `proposed_change.content` | string | ✅ | — | |
| `evidence.<source_project>_examples` | string[] | ⚠️ **disputed** | — | Key name varies by publisher — see [Q3](#q3-blocking--the-evidence-key-name-varies-by-publisher) |
| `evidence.issue_observed` | string | ✅ | — | |
| `supersedes` | null \| string | ✅ | — | Superseded `proposal_id`, or `null` |
| `created_at` | string | ✅ | ISO 8601 | |

### 4.2 Corrections applied in 0.2.0

Both were contradicted by messages already on the stream when 0.1.0 was written; 0.1.0 inferred
them from 5 samples drawn from a single publisher.

- `target.kind` gained `rule`. Version 0.1.0 listed `principle` and `norm` only, while seq 3, 11
  and 12 carry `rule`. Under Tolerant Reader an unknown enum takes the business fallback, so this
  was a documentation gap rather than a live failure.
- `evidence.agentfabric_examples` is no longer named as a required field. Version 0.1.0 hard-coded
  the publisher's name into the key and marked it required; seq 11 and 12 carry
  `shijian_examples` instead. **Executing 0.1.0 literally would have judged both shijian proposals
  as missing a required field and sent them to the dead-letter queue** — a contract defect
  condemning valid messages.

## 5. QoS

| Parameter | Value |
| --- | --- |
| max_deliver | TBD |
| ack_wait | TBD |
| backoff | TBD |
| DLQ subject | TBD |

## 6. IaC responsibility

Unassigned. The `CORTEX` stream exists and reports one consumer, but no tool available to this
consumer can list consumers, so the durable's name and filter subject are unknown. Per
[nats-messaging §9](../../../specs/nats-messaging.md) the subject-domain owner owns the broker
resources; that owner is not yet named.

## 7. Open questions

All three block promotion to `active`.

### Q1 (blocking) — the subject carries a per-proposal slug

`cortex.proposals.<kind>.<slug>` mints a new subject for every proposal. Two consequences:

1. [nats-messaging §2.3](../../../specs/nats-messaging.md) requires one contract file per subject.
   Taken literally, this design requires one contract file per proposal.
2. Contract resolution matches a message's subject against a contract's `subject` frontmatter
   **exactly**. A subject containing a per-message slug can never match, so every proposal
   resolves as an unknown subject and is termed to the dead-letter queue pending confirmation.

**Decision needed**: either collapse the subject to a fixed `cortex.proposals` (moving `kind` and
`slug` into the payload, where both already appear as `target.kind` and `proposal_id`), or define
how a contract declares a subject *pattern* rather than a literal subject.

### Q2 (blocking) — header presence is unverified

Version 0.1.0 recorded "this sample batch carried no custom business headers". If that is read as
"no headers at all", then every message on this subject space violates
[nats-messaging §5.2](../../../specs/nats-messaging.md), and a consumer following the spec must
term all 10 pending proposals to the dead-letter queue.

**Decision needed**: confirm on the producer side whether `Nats-Msg-Id`, `X-Source`, `X-Type` and
`Content-Type` are being set. If they are not, the producers must start setting them before any
drain runs.

### Q3 (blocking) — the evidence key name varies by publisher

Today's wire format prefixes the key with the publisher's own name
(`agentfabric_examples`, `shijian_examples`). This makes the schema unwritable: no single required
key name is correct for all publishers.

**Decision needed**: rename to a publisher-independent key — `evidence.examples` is proposed —
and agree a compatibility window during which a consumer accepts both spellings. Until then the
field cannot be marked required and a consumer must not term on its absence.

## CHANGELOG

### 0.2.0 — 2026-09-20

- Flattened out of the per-publisher subdirectory; this contract is keyed on the subject (§2).
- `target.kind` enum gained `rule`; `proposed_change.format` gained `markdown-patch` (§4.1).
- `evidence.<source_project>_examples` demoted from required to disputed (§4.2, Q3).
- Header presence downgraded from "none observed" to unverified (§3, Q2).
- Recorded the unbounded-subject problem (Q1) and the unassigned IaC ownership (§6).
- Status remains `draft`; `authoritative` remains `false`.

### 0.1.0 — 2026-05-29

- Initial Bootstrap inference from 5 samples (seq 4–8), single publisher.

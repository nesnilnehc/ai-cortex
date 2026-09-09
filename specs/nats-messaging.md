---
id: NATS_MESSAGING_SPEC_V1
name: NATS Messaging Schema
description: Spec defining the structural contract for NATS messages exchanged between independently-evolving projects — subject naming, headers, ID requirements, payload conventions, versioning, with embedded validation rules.
version: 1.1.0
status: active
lifecycle: living
created_at: 2026-05-21
scope: |
  Defines the structural contract for NATS messages exchanged between independently-evolving
  repos / teams / services over a shared broker. Covers subject naming, message ID, header
  conventions, payload shape, version evolution, and embedded behavior rules. Does not apply
  to intra-team messaging within a single release cycle.
related:
  - ./spec-modeling.md
  - ./cross-team-contract.md
---

# NATS Messaging Schema

> **Data contract**: defines the subject, headers, payload and version evolution contract for NATS messages exchanged between projects

---

## 1. Position and scope

This spec defines how messages exchanged over a shared NATS broker between independent repos / teams / services must be organised: how a subject is named, which fields the headers must carry, how a message ID is issued, how a payload is written, and how versions evolve.

In scope:

- Two or more independently evolving projects exchanging messages over a NATS broker
- A single project publishing events for upstream / downstream teams to consume
- Several teams sharing a broker, with subject domains governed across teams

Out of scope:

- Messaging between internal modules of the same team on the same release cycle (no cross-team alignment cost to pay)
- Broker behaviour itself (the NATS protocol and JetStream internals — <https://docs.nats.io> is authoritative)
- Code-level details of producing and consuming messages (an application-layer responsibility; this spec fixes only the on-the-wire contract)

This spec is the NATS specialisation of [cross-team-contract.md](./cross-team-contract.md)  — the generic contract-document skeleton (naming suffix, `contract_version`, CHANGELOG, flat layout) is carried by cross-team-contract, and this spec adds only the NATS-specific subject / headers / payload detail.

The actual send and receive actions are carried out by the companion Skills through the NATS MCP server:

- [publish-nats-message](../skills/publish-nats-message/SKILL.md) — the producer side
- [consume-nats-message](../skills/consume-nats-message/SKILL.md) — the consumer side

---

## 2. Naming

### 2.1 Subject formula

```text
<domain>.<event>[.<version>]
```

- **Event-centric naming**; never prefixed by originator or team
- `<domain>`: the business domain (for example `clarification` / `orders` / `inventory`)
- `<event>`: the event type (past-tense verb or noun, for example `created` / `session.requested` / `stock.depleted`)
- `<version>`: the optional MAJOR version (for example `v1`, `v2`); a breaking MAJOR introduces a new subject instead of changing the meaning of the old one

### 2.2 Multi-tenant exception

Permitted when ACL and retention must be governed per producer (≥3 teams, or multi-tenant SaaS):

```text
<tenant>.<domain>.<event>
```

**Precondition**: the meaning of the prefix must be declared explicitly in the contract's "Subject naming" section; implicit inference is not allowed.

### 2.3 Contract file naming

Each subject has one contract file, following the `-contract.md` suffix set by [cross-team-contract.md §2](./cross-team-contract.md#2-命名约定):

```text
<event>-contract.md
```

Examples: `clarification-session-requested-contract.md`, `orders-created-contract.md`.

---

## 5. Body structure contract

A cross-team NATS message has three layers: the message ID (the idempotency anchor), the headers (metadata) and the payload (business data). This section defines the structural contract of each layer, together with version evolution and the embedded validation rules.

### 5.1 Message ID contract

A cross-team message ID must be globally unique and doubles as the idempotency key:

| Item | Constraint |
|---|---|
| ID format | UUID v7 (recommended, time-ordered by construction) / ULID / Snowflake; a semantic prefix may be added (`req-clarify-01HXXX...`) |
| Carried in | The NATS header `Nats-Msg-Id` (JetStream deduplicates on it within `duplicate_window`) |
| Sequential numbering | ❌ Strictly forbidden (`msg-1` / `REQ-001` / `evt-0042`) — distributed races, and the sequence cannot be resumed once retention truncates it |
| Retry | Resending the same logical message **must reuse the same ID** (the premise of idempotency) |

The consumer deduplicates at the application layer on `Nats-Msg-Id`, keeping a processed-ID set whose TTL ≥ the retry window.

### 5.2 Headers contract

Metadata for a cross-team message always travels in NATS headers, and is never embedded in a payload JSON envelope.

#### 5.2.1 Field table

| Header | Required | Type | Description |
|---|---|---|---|
| `Nats-Msg-Id` | Yes | string | The message ID, UUID v7 / ULID (see §5.1) |
| `X-Source` | Yes | string | Producer service name / URI (for example `urn:recloud:agentfabric`), identifying the originator |
| `X-Type` | Yes | string | The event type string, aligned with the trailing segment of the subject (for example `clarification.session.requested`) |
| `Traceparent` | Recommended | string | W3C Trace Context (`00-{traceId}-{spanId}-{flags}`), the OTel standard |
| `X-Correlation-Id` | Conditionally required | string | Required for request-response and multi-turn session scenarios; points at the original request's `Nats-Msg-Id` |
| `X-Schema-Url` | Recommended | string | The payload schema registry URL; a consumer can validate against it dynamically |

#### 5.2.2 Forbidden fields

- ❌ Inventing `in_reply_to` / `messageId` / `correlationid` (which muddles the OTel standard) — use `X-Correlation-Id` + `Traceparent`
- ❌ Stuffing the producer identity into the subject prefix — use the `X-Source` header
- ❌ Embedding `id` / `source` / `type` / `time` fields in a JSON envelope — that information belongs to the headers layer

### 5.3 Payload conventions

#### 5.3.1 Serialisation

- Must be structured (JSON / Protobuf / MsgPack); **a bare string or binary stream is forbidden** unless it is an object reference into the JetStream Object Store
- JSON by default; any other format must be declared explicitly in the contract's "Serialisation" section
- Use **binary mode**: headers carry the metadata, the body carries the business payload; CloudEvents structured mode is **not mandatory** (NATS headers are already the more native metadata channel)

#### 5.3.2 Tolerant Reader

A consumer must:

- Ignore unknown fields (forward compatibility with producer additions)
- Ignore unknown enum values and take the fallback branch, rather than throwing and exiting
- Not depend on field order

#### 5.3.3 Business field table

Every contract's field table must carry: field name / type / whether required / value constraints / default value where applicable. The concrete fields are defined by each contract; this spec prescribes no business fields.

### 5.4 Version evolution

| Change | Version | How it is done |
|---|---|---|
| MAJOR (breaking) | New subject | Introduce a new subject such as `<domain>.<event>.v2`; keep the old subject until every consumer has switched over |
| MINOR (compatible addition) | `contract_version` MINOR bump | Same subject, with new optional fields or enum values; consumers stay compatible through Tolerant Reader |
| PATCH (documentation revision) | `contract_version` PATCH bump | Comment corrections, typos, added examples; no effect on on-the-wire behaviour |

`contract_version` and the CHANGELOG are carried by [cross-team-contract.md §4-§5](./cross-team-contract.md#4-frontmatter-契约); this spec does not redefine them.

### 5.5 Embedded validation rules

The behavioural constraints below are embedded in this spec (terminology's section on what may and may not be embedded permits a Spec to embed Rules) — they are preconditions for the structural contract to hold, not standalone rules.

#### 5.5.1 QoS defaults

- Cross-team messages are **at-least-once by default** and must use a JetStream durable consumer
- Downgrading to at-most-once must be declared explicitly in the contract's "QoS" section, along with the scenarios in which messages may be lost
- exactly-once requires all three of `Nats-Msg-Id` on the producer side, JetStream `duplicate_window`, and idempotent handling on the consumer side

#### 5.5.2 Resource governance

- Stream / Consumer / KV / Object Store are **managed by IaC** (Terraform / NATS Operator / CI scripts / GitOps)
- ❌ Application code must not perform `streams.add()` / `KV.create()` / `AdminAPI` operations at runtime
- The owner of a subject domain is responsible for the IaC of that domain's broker resources; ownership is written into the contract's "IaC responsibility" section

#### 5.5.3 DLQ and retry

- A cross-team message contract **must define explicitly**:
  - The DLQ subject (by convention `<original>.dlq`)
  - The maximum number of retries (`max_deliver`)
  - The backoff algorithm (exponential / linear / fixed) and its parameters
- The ack decision taken when a consumer fails to process a message (`ack` / `nak` / `term`) must follow the contract

#### 5.5.4 Sessions and state

- `sessionId` / `workflowId` / `conversationId` are **not native NATS concepts**; they are an application-layer overlay
- How to implement: encode it in the subject (`chat.session.<sid>.message`) + chain it through headers (`X-Correlation-Id`) + optionally store session state in JetStream KV
- ❌ Do not describe them in a contract as native broker capabilities

#### 5.5.5 Service discovery / health / schema

- Use the NATS Services API (`$SRV.*`) for service discovery, health checks and schema queries
- ❌ Inventing a meta-protocol on a business subject is forbidden (for example `<service>.health` / `<service>.schema`)

---

## 6. Anti-patterns

```text
❌ Sequential message IDs
Nats-Msg-Id: msg-1 / REQ-001 / evt-0042
✅ Nats-Msg-Id: 01HX3W7K9N4PQRSTUVWXYZ0123(ULID) / UUID v7
```

```text
❌ Subject prefixed by the originator
service-zentao.events / team-payments.events
✅ clarification.session.requested / orders.created.v1
```

```text
❌ CloudEvents envelope embedded in the JSON payload
{ "id": "...", "source": "...", "type": "...", "time": "...", "data": {...} }
✅ Metadata in headers, payload carries business fields only
```

```text
❌ Home-grown tracing fields
{ "in_reply_to": "...", "messageId": "..." }
✅ Header: X-Correlation-Id / Traceparent
```

```text
❌ Application code creating resources at runtime
await jetstreamManager.streams.add({ name: 'EVENTS', subjects: [...] });
✅ Declarative management through IaC (Terraform NATS provider / NATS Operator)
```

```text
❌ Describing sessionId as native to NATS
"NATS routes by sessionId automatically"
✅ Application layer: encode in the subject + chain with X-Correlation-Id + optional KV state
```

```text
❌ Cross-team messages sent over Core NATS without persistence
nc.publish('orders.created', payload);
✅ JetStream + durable consumer + ack policy
```

---

## 7. Examples

### 7.1 Contract file template

```markdown
---
artifact_type: cross-team-contract
contract_version: 1.0.0
created_at: 2026-05-21
related:
  - ../../specs/nats-messaging.md
  - ../../specs/cross-team-contract.md
---

# clarification.session.requested contract

## Contract scope

producer: urn:recloud:agentfabric (clarification service)
consumer: urn:recloud:zentao-bridge (ZenTao bridge)
subject: `clarification.session.requested.v1`
QoS: at-least-once (JetStream durable consumer `zentao-bridge-clarify`)
IaC responsibility: terraform/nats/clarification-stream.tf (agentfabric team)

## Headers

| Header | Required | Value |
|---|---|---|
| Nats-Msg-Id | Yes | UUID v7 |
| X-Source | Yes | urn:recloud:agentfabric |
| X-Type | Yes | clarification.session.requested |
| Traceparent | Recommended | W3C Trace Context |
| X-Correlation-Id | Conditionally required | Links to the first Nats-Msg-Id of a multi-turn session |

## Payload fields

| Field | Type | Required | Description |
|---|---|---|---|
| sessionId | string | Yes | ULID, the session identifier |
| feedbackId | string | Yes | ID of the feedback awaiting clarification |
| question | string | Yes | The clarification question |
| context | object | Optional | Additional context |

## QoS / DLQ / retry

- max_deliver: 5
- backoff: exponential, base 1s, max 30s
- DLQ subject: clarification.session.requested.v1.dlq

## CHANGELOG

### 1.0.0 — 2026-05-21
**Initial Release**: first published version.
```

### 7.2 Project-level cache `.cortex/nats.yaml`

Every repo that uses NATS keeps a `.cortex/nats.yaml` at its root; the companion Skills read it at startup so they need not ask the same questions again:

```yaml
# Shared fields
broker_url: nats://nats.internal:4222
service_source: urn:recloud:agentfabric          # this service's X-Source identity

# Producer-side fields
default_stream: AGENTFABRIC_EVENTS                # JetStream stream name (IaC-managed)
contract_dir: integrations/                       # contract file root directory
iac_owner: terraform/nats/                        # where IaC resources are declared

# Consumer-side fields
durable_name_prefix: recloud-agentfabric          # durable consumer name prefix
dlq_handler_dir: integrations/<producer>/dlq/     # where DLQ handling lives
vendor_contracts_dir: vendor/contracts/           # vendored upstream contract root

# Consumer drain defaults
consume_defaults:
  max_messages: 200                               # max messages handled per invocation
  batch_size: 50                                  # messages per fetch
  fetch_timeout: 5s                               # per-fetch timeout
  idle_threshold: 2s                              # consecutive-empty-fetch threshold (drain treated as complete)

# Consumer scope (pick one; see the mutual-exclusion note below)
consume_subjects:                                 # default: explicit per-subject list, one exact durable per subject
  - clarification.session.requested.v1
consume_pattern: null                             # optional: wildcard consume pattern, e.g. zentao.omnireview.>; when set it wins and consume_subjects is ignored
```

**Conventions**:

- Generated by the companion Skill during the first session, then committed into the repo
- In later sessions the Skill reads it at startup instead of asking for the basics again
- When it is absent the Skill degrades gracefully: it asks ad hoc and sends, but prompts the user to persist the file
- `consume_pattern` and `consume_subjects` are **mutually exclusive**: once `consume_pattern` is set it takes precedence and `consume_subjects` is ignored entirely — letting both take effect would have one message received and acked independently by the wildcard consumer and by the exact consumer, causing duplicate processing on the business side
- With `consume_pattern` enabled only one `<durable_name_prefix>-wildcard` durable is created, rather than one per subject; the companion Skill resolves the matching contract dynamically from each message's actual `subject` (it acks only on an `active` contract, and a draft or brand-new subject is always termed and flagged in the DLQ as pending confirmation, so a message nobody has reviewed is never acked blindly)
- **Known limitation**: JetStream's `ack_wait` / `max_deliver` are durable-level settings and cannot be set per subject — under `consume_pattern` every subject shares one set of retry parameters, and each contract's "retry policy" field degrades to documentation in this mode rather than being enforced per subject

---

## 8. Relationship to other assets

- **Parent spec**: [cross-team-contract.md](./cross-team-contract.md) — the generic cross-team contract skeleton; this spec is its NATS specialisation
- **Recursive basis**: [spec-modeling.md](./spec-modeling.md) v2.0.0 — this spec itself follows the 8-section skeleton
- **Companion Skills**:
  - [publish-nats-message](../skills/publish-nats-message/SKILL.md) — end-to-end capability on the producer side
  - [consume-nats-message](../skills/consume-nats-message/SKILL.md) — end-to-end capability on the consumer side (drain-style batching)
- **Authority on broker behaviour**: <https://docs.nats.io> — the NATS protocol, JetStream, the Services API and the rest follow the official documentation; this spec does not restate them

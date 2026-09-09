---
name: publish-nats-message
description: Publish a NATS message conforming to a cross-team contract, using NATS MCP tools. Authors the contract on first use if missing. Reads project-level cache (.cortex/nats.yaml) to avoid re-prompting basics across sessions.
description_zh: 通过 NATS MCP 工具按跨团队契约发布消息；首次缺契约时引导起草。读取项目级缓存 .cortex/nats.yaml，避免跨会话重复询问。
tags: [nats, messaging, cross-team, producer, mcp]
version: 1.0.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [publish nats, send nats message, 发布事件, 跨服务发消息, nats publish]
input_schema:
  type: free-form
  description: Event description (domain + type); payload data; consumer name (first time only); optional QoS hint; optional explicit contract path
output_schema:
  type: side-effect
  description: NATS message published via MCP; ack/result reported; contract file created (first time) or reused (subsequent)
---

# Skill: Publish NATS Message

## Purpose

Let collaborating projects "produce messages correctly" — publish one message through the NATS MCP tools according to the cross-team contract, with subject / headers / payload / QoS aligned strictly to [specs/nats-messaging.md](../../specs/nats-messaging.md). The first time an event has no contract, walk through generating one and write it into the producer repo.

---

## Core Objective

**Primary goal**: publish one contract-conforming message through the NATS MCP tools; when the contract does not exist, generate it before sending.

**Success criteria**:

1. ✅ The project cache `.cortex/nats.yaml` was read (walk through creating it when it is absent)
2. ✅ The `<event>-contract.md` for the event is in place (read it when it exists; draft it and prompt for a commit when it does not)
3. ✅ The subject / headers / payload actually sent match the contract definition strictly
4. ✅ `Nats-Msg-Id` is a UUID v7 generated for this send (or the original ID reused when retrying the same message)
5. ✅ A JetStream send received its ack; at-most-once is fire-and-forget only
6. ✅ The user got the send result (success + a summary of the actual headers / failure + the reason)

**Acceptance test**: on the consumer side, `consume-nats-message` subscribes to the same subject and decodes headers + payload correctly, with no validation failure.

---

## Scope Boundary

**This skill owns**:

- Reading the project cache and loading the contract
- Drafting the contract per [specs/nats-messaging.md](../../specs/nats-messaging.md) + [specs/cross-team-contract.md](../../specs/cross-team-contract.md) when it is missing on first use
- Building the conforming message (subject + headers + payload)
- Carrying out publish / jetstream_publish / request through the NATS MCP tools
- Ack verification and retry on failure (per the contract's retry policy)

**This skill does not own**:

- Writing the actual publisher code → outside the Skill's remit (an application-engineering responsibility)
- Creating / modifying a JetStream stream / consumer / KV → an IaC responsibility (see spec §5.5.2)
- Subscribing to / consuming messages → use [consume-nats-message](../consume-nats-message/SKILL.md)

---

## Preconditions

- A NATS MCP server is connected (offering tools such as `mcp__nats__publish` / `mcp__nats__jetstream_publish` / `mcp__nats__request`; the exact tool names come from the connected server)
- The current working directory is the producer repo (for reading `.cortex/nats.yaml` and the contract file)
- The user can authorize publish permission on the broker

---

## Execution

### Stage 0: announce

> "I am using the publish-nats-message skill to send a NATS message."

### Stage 1: read the project cache

1. Read `.cortex/nats.yaml` (at the producer repo root)
2. Extract the fields: `broker_url` / `service_source` / `default_stream` / `contract_dir` / `iac_owner`
3. **Cache absent**: enter the "cache initialization subflow" — ask for the fields above, write `.cortex/nats.yaml`, and prompt the user to review and commit it; later steps reuse the values filled in here
4. **Cache present but a field is missing**: ask about the missing field only, and update the cache

### Stage 2: locate the contract

1. Parse the event description the user gave ("send clarification.session.requested", for example)
2. Glob `<contract_dir>/**/<event>-contract.md`
3. **Hit**: read the contract → go to Stage 4
4. **Miss**: go to Stage 3 and draft the contract

### Stage 3: contract drafting subflow (first time for a given event only)

Ask for the minimum information needed (the rest comes from the cache):

- The consumer name (one or several)
- The QoS choice (at-least-once by default; the user can pick at-most-once but must state where loss is acceptable)
- Whether this is a multi-turn session (if so → mark `X-Correlation-Id` conditionally required, and plan a slot for sessionId inside the subject)
- The business field table (a draft payload schema; the user can list the main fields, their types and whether each is required)
- DLQ + retry parameters (defaults: DLQ `<subject>.dlq`, max_deliver=5, exponential backoff base 1s max 30s)

Generate the contract file:

- Path: `<contract_dir>/<consumer>/<event>-contract.md` (the flat layout of [cross-team-contract.md §3](../../specs/cross-team-contract.md))
- The frontmatter carries `contract_version: 1.0.0`, and the first CHANGELOG entry is `### 1.0.0 — YYYY-MM-DD Initial Release`
- The body follows the template in [specs/nats-messaging.md §7.1](../../specs/nats-messaging.md)

Afterwards:

- Prompt the user to review and commit the contract file
- **Wait for the user to confirm** the contract is fine before entering Stage 4 and sending for real (this avoids polluting the stream with a message sent against an unconfirmed contract)

### Stage 4: build the message

Fill the fields per the contract:

| Field | Value |
|---|---|
| subject | the subject defined in the contract's "Contract Scope" section |
| `Nats-Msg-Id` | a UUID v7 generated on the spot (reuse the original ID when retrying) |
| `X-Source` | the cached `service_source` |
| `X-Type` | the event-type string defined in the contract |
| `Traceparent` | inject it when the runtime has an OTel context; otherwise skip |
| `X-Correlation-Id` | required in a multi-turn session; the caller supplies the original ID |
| `X-Schema-Url` | filled in when the contract defines a schema URL |
| payload | the business data the user supplied, validated field by field against the contract's field table (every required field present, types correct, enum values legal) |

Validation fails → report the offending fields and **send nothing**.

### Stage 5: send through the MCP NATS tools

Pick the tool by QoS:

| Case | MCP tool | Note |
|---|---|---|
| at-most-once (telemetry / heartbeat) | `mcp__nats__publish` | no ack, fire-and-forget |
| at-least-once (the cross-team default) | `mcp__nats__jetstream_publish` | must wait for the ack; triggers `duplicate_window` deduplication |
| synchronous request-response (< 5s) | `mcp__nats__request` | carries a reply subject + `X-Correlation-Id` |

The exact tool names come from the connected NATS MCP server; when a tool signature differs, the Skill maps onto it adaptively (the headers argument / the subject argument).

### Stage 6: self-check and receipt

- **JetStream**: wait for the ack; a timeout / no ack → treat it as a failure
- **Retry on failure**: resend per the contract's retry policy, **reusing the same `Nats-Msg-Id`** (the broker deduplicates); still failing at max_deliver → report to the user
- **Success receipt**: emit
  - subject
  - the actual header values (sensitive fields can be redacted where present)
  - the ack information (JetStream sequence / stream / domain)
  - the elapsed time

---

## Error Handling

| Situation | Handling |
|---|---|
| The MCP NATS server is not connected | prompt the user to check the MCP configuration, and list the expected tool names |
| `.cortex/nats.yaml` does not exist | enter the cache initialization subflow (Stage 1) |
| The contract does not exist | enter the contract drafting subflow (Stage 3) |
| Payload field validation fails | list the offending fields and ask for a correction before resending |
| The JetStream ack times out | retry with the contract's backoff; report the final failure to the user |
| The stream does not exist (the subject domain was never put under IaC) | report the violation of [specs/nats-messaging.md §5.5.2](../../specs/nats-messaging.md), and point at the IaC owner |

---

## Anti-Patterns

- ❌ Application code creating a Stream / Consumer / KV at runtime (a violation of spec §5.5.2) — report the error and point at IaC
- ❌ Cross-team messages going over Core NATS with no persistence — switch to JetStream by default; a downgrade takes an explicit user confirmation
- ❌ A fresh `Nats-Msg-Id` on retry — it must be reused, or the broker's deduplication stops working
- ❌ Stuffing metadata into the payload JSON envelope (`id` / `source` / `time` and the like) — it must go in the Headers
- ❌ Asking again for basics such as `broker_url` / `service_source` without reading the cache
- ❌ Sending with no contract in place — it must be drafted first, with a prompt to commit

---

## Relation to Other Assets

- **The structural contract yardstick**: [specs/nats-messaging.md](../../specs/nats-messaging.md) — the authority on subject / headers / payload / QoS / validation rules
- **The contract document skeleton**: [specs/cross-team-contract.md](../../specs/cross-team-contract.md) — apply its frontmatter and section structure when drafting a contract for the first time
- **The consumer-side counterpart**: [consume-nats-message](../consume-nats-message/SKILL.md) — the other end of the same contract
- **The authority on broker behavior**: <https://docs.nats.io> — the official docs govern the NATS protocol / JetStream / Services API

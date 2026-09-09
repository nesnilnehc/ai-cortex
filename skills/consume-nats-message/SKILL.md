---
name: consume-nats-message
description: Drain pending NATS messages from a producer contract via NATS MCP tools. Discovers the available NATS tool capabilities, selects exact-subject or wildcard mode from .cortex/nats.yaml, applies Tolerant Reader semantics, executes ack/nak/term decisions, and returns aggregated stats.
description_zh: 通过 NATS MCP 工具批量拉取 producer 契约下的待处理消息。先发现并映射可用 NATS 工具能力，再根据 .cortex/nats.yaml 选择精确 subject 或 wildcard 模式，按 Tolerant Reader 处理并执行 ack/nak/term，最终返回聚合统计。
tags: [nats, messaging, cross-team, consumer, mcp]
version: 1.4.0
license: MIT
recommended_scope: both
metadata:
  author: ai-cortex
triggers: [consume nats, subscribe nats, drain nats, 订阅事件, 跨服务收消息, nats consume]
input_schema:
  type: free-form
  description: Producer name + event type or subject; optional contract path with @version; optional consume override max_messages / batch_size / fetch_timeout / idle_threshold
output_schema:
  type: side-effect
  description: Pending messages drained via MCP; each message acked/naked/termed or isolated for contract confirmation; aggregated counts, failures, awaiting_confirmation, and exit reason reported
---

# Skill: Consume NATS Message

## Purpose

Run one bounded NATS JetStream pull-consume inside the consumer repository: read the local configuration and the producer contract, fetch the pending messages, parse each one under Tolerant Reader semantics and call the business handler, then execute the right `ack` / `nak` / `term + DLQ` decision.

The default is **drain-style**: keep fetching until the queue is drained, the message cap is reached, or consecutive empty fetches reach the idle threshold.

---

## Authoritative references

This Skill orchestrates a single consume action and nothing more; it does not redefine the NATS contract rules.

| Topic | Authoritative source |
|---|---|
| subject / headers / payload / Tolerant Reader / DLQ / IaC boundary | [specs/nats-messaging.md](../../specs/nats-messaging.md) |
| `contract_version` / CHANGELOG / `*-contract.md` structure | [specs/cross-team-contract.md](../../specs/cross-team-contract.md) |
| Skill / Spec / Protocol / Rule boundaries | [docs/architecture/terminology.md](../../docs/architecture/terminology.md) |
| External links and raw-content policy | [AGENTS.md](../../AGENTS.md) |

Where this Skill conflicts with the assets above, follow the repository authority order `AGENTS.md > specs/ > protocols/ > rules/ > docs/`; the Skill body keeps the execution orchestration only.

---

## Preconditions

- The current working directory is the consumer repo.
- The consumer repo carries `.cortex/nats.yaml`, or the user allows a temporary configuration to be filled in during this interaction.
- Some NATS MCP server is connected. Tool names need not be fixed, but they must map onto the fetch / ack / nak / term / publish-DLQ capabilities.
- The producer contract comes preferably from the local vendored snapshot; an external HTTP/HTTPS contract or official document may be read only where the current context explicitly permits external fetching.

---

## Input

The user may supply any combination of:

- `producer`: the producer name or service source.
- `event`: the event name.
- `subject`: an explicit NATS subject.
- `contract_path`: the local contract path, recommended to carry `@version` semantics.
- `max_messages` / `batch_size` / `fetch_timeout` / `idle_threshold`: override the defaults in `.cortex/nats.yaml`.

When producer / event / subject is missing, infer it from `.cortex/nats.yaml` and the vendored contracts first; ask the user only when that still leaves it ambiguous.

---

## Behavior

### 0. Announce

Tell the user:

> I am using the consume-nats-message skill to drain a batch of pending messages.

### 1. Read the local context

1. Read `.cortex/nats.yaml`.
2. Extract:
   - `broker_url`
   - `service_source`
   - `durable_name_prefix`
   - `dlq_handler_dir`
   - `vendor_contracts_dir`
   - `consume_defaults`
   - `consume_subjects` (optional)
   - `consume_pattern` (optional)
3. Override `consume_defaults` with the user's explicit parameters.
4. Where the configuration is missing, ask for the minimum necessary fields, and remind the user to commit the configuration into the repo afterwards.

### 2. Discover and map the NATS MCP tools

Do not assume the MCP tool names are fixed. Inspect the NATS-related tools the current runtime exposes and build a capability map first:

| Capability | Use | If missing |
|---|---|---|
| `list_streams_or_subjects` | List the broker topology during Bootstrap | Bootstrap cannot run; stop and name the missing capability |
| `peek_message` | Read-only sampling during Bootstrap; no ack, no durable offset movement | Stop where the contract is missing; a real drain cannot start |
| `attach_or_pull_consumer` | Reuse an existing durable and fetch a batch | Stop, and prompt the user to check the MCP configuration |
| `ack` | Acknowledge a successful or duplicate message | Stop; consuming safely is not possible |
| `nak` | Redeliver a retryable failure | Stop; consuming safely is not possible |
| `term` | Stop redelivery for an unrecoverable failure | Stop; failed messages cannot be isolated safely |
| `publish` | Send the DLQ copy | The term path is unusable; stop, or degrade to term-only on the user's confirmation |

Where a tool name differs from the example name, call by capability rather than by name. Where no tool-discovery capability exists, match manually against the current tool list; stop and ask the user about the configuration when it cannot be confirmed.

### 3. Choose the consume mode

| Condition | Mode | Behavior |
|---|---|---|
| `.cortex/nats.yaml` sets `consume_pattern` | wildcard | Build one `<durable_name_prefix>-wildcard` durable and match contracts dynamically against each message's actual `subject` |
| `consume_pattern` unset, but `subject` / `producer + event` / `consume_subjects` present | exact-subject | Reuse one exact durable per subject |
| Neither is enough to settle it | discovery | List the local contracts and the visible subjects, and let the user choose |

`consume_pattern` and `consume_subjects` are mutually exclusive; once `consume_pattern` is present, this invocation must ignore `consume_subjects`, to avoid the same message being handled independently by several durables.

### 4. Locate or bootstrap the contract

#### exact-subject mode

Locate the contract in this order:

1. `<vendor_contracts_dir>/<producer>/<event>-contract.md`
2. The local `contract_path` the user supplied
3. The local contract that `.cortex/nats.yaml` or `consume_subjects` points at
4. Still missing → enter Bootstrap

Read the contract frontmatter and body, extracting at least `contract_version`, `status`, `subject`, the required headers, the payload fields, the DLQ subject, `max_deliver`, and backoff. Field semantics are governed by `specs/nats-messaging.md` and by the contract itself.

#### wildcard mode

Do not lock onto a single contract before the consumer is built. As each message arrives, **run two pre-filters first**; hitting either one leads straight to `ack`, skipping contract resolution, de-duplication, decoding, and the business handler (steps 2-7). Only when neither hits does processing carry on:

1. **Self-produced message**: `headers['X-Source']` exists and equals `service_source` (that is, this service emitted the message itself) → `ack` straight away; do not resolve the contract, do not generate a draft, do not enter the business handler.

   Why: a wildcard subject pattern matches on prefix only and carries no direction information. When producer and consumer share one naming prefix (both sides agreeing that `zentao.omnireview.>` carries events in both directions, say), this service's own outbound messages also match its wildcard filter and are delivered back to it. That is not an "unknown contract" but an echo, and running it through the unknown-subject flow would generate surplus draft contract files for the service's own messages.

   A missing `X-Source` is **not** judged a self-produced message (no equality comparison against `undefined`/`None`) — let it through to the next filter and to real contract resolution; a message genuinely missing that required header is judged unrecoverable at step 3, "decode headers", and goes to `term + DLQ`, instead of being quietly swallowed by this pre-filter or making the read itself throw and break the whole batch.

2. **DLQ copy self-loop**: the message carries an `X-DLQ-Original-Subject` header (that is, the message is itself a DLQ copy this service `publish`ed earlier — see the list of headers a DLQ copy always carries under "10. Ack decisions") → `ack` straight away; do not resolve the contract.

   Why: the copy that `term + publish DLQ` produces lands on the subject `<original-subject>.dlq`, which matches the wildcard prefix just as well and reaches the same wildcard consumer again. A DLQ copy is the end point of a failure archive, not a business event awaiting processing; it needs no further round of contract resolution or a second DLQ, and should not trigger one. Judge it by the self-produced `X-DLQ-Original-Subject` header rather than by a bare `.dlq` suffix string match — the latter would misread a normal business subject that happens to end in `.dlq` as a loop, silently discarding real business messages.

When neither pre-filter hits, match `msg.subject` exactly against the `subject:` in the frontmatter of `<vendor_contracts_dir>/<producer>/*.md`:

- Hit with `status: active`: carry on with normal processing.
- Hit with `status: draft`: do not enter the business handler; take the awaiting-confirmation path.
- No hit: generate an N=1 draft contract for that subject, then take the awaiting-confirmation path.

### 5. Bootstrap a draft contract

Runs only when the contract is missing. Bootstrap is a read-only probing phase:

- No ack.
- No nak.
- No term.
- No creating or advancing of a real durable offset.
- No change to the authoritative producer contract.

Steps:

1. Use the NATS MCP topology/peek capabilities to list streams / subjects / message counts.
2. Choose the target subject; where it cannot be pinned down, ask the user.
3. Peek the most recent N samples, N=5 by default; N=1 when a wildcard misses.
4. Infer the headers and the payload fields:
   - With N>1, a field present 100% of the time may be marked required, and one below 100% optional.
   - With N=1, a field that shows up must not be judged required automatically; requiredness is marked `to be confirmed` throughout.
   - QoS / max_deliver / DLQ cannot be inferred reliably; mark them `TBD`.
5. Write the local draft contract: `<vendor_contracts_dir>/<producer>/<event>-contract.md`.
6. The frontmatter must carry:

```yaml
contract_version: 0.1.0
status: draft
inferred_from: bootstrap-peek
inferred_at: <ISO 8601>
inferred_sample_size: <N>
inferred_sample_seq_range: <first>-<last>
authoritative: false
```

Branches after Bootstrap:

| Scenario | Default handling |
|---|---|
| A new draft in exact-subject mode | Show the draft summary and ask the user whether to continue into a real drain; by default it does not continue |
| wildcard mode meets an unknown subject | Generate the draft, then `term + DLQ` the current message, annotate it `awaiting contract confirmation`, and do not break the batch |
| wildcard mode hits a draft | `term + DLQ` the current message, annotate it `awaiting contract confirmation`, and do not break the batch |

Only where the user explicitly confirms "continue the real drain on the draft" may exact-subject mode enter real processing under a draft contract; otherwise stop and wait for the producer owner to confirm the contract.

### 6. Version and status checks

exact-subject mode:

1. Read the contract's `contract_version` and `<vendor_contracts_dir>/<producer>/.lock`.
2. Where `.lock` is missing, write the current `<contract-name>@<version>` and treat it as the first alignment.
3. MINOR / PATCH drift: flag the risk, then carry on.
4. MAJOR drift or a breaking subject change: stop, and prompt for an upgrade of the vendored contract.
5. `status: draft`: the user's confirmation must be obtained before any message is formally acked.

wildcard mode:

- No per-message SemVer drift check.
- Only a contract with `status: active` may enter the business handler.
- A `draft` or unknown contract always takes the awaiting-confirmation path.

### 7. Create or reuse the pull consumer

Honor the IaC boundary in `specs/nats-messaging.md`: the Skill creates no stream and no durable resources.

exact-subject mode:

- durable name: `<durable_name_prefix>-<event-slug>`
- filter subject: the contract subject
- Where the durable does not exist, stop and point at the IaC owner

wildcard mode:

- durable name: `<durable_name_prefix>-wildcard`
- filter subject: `consume_pattern`
- ack policy: `explicit`
- `ack_wait` / `max_deliver` take the durable-level defaults; they cannot be forced per subject
- Where the durable does not exist, stop and point at the IaC owner

### 8. The drain loop

```text
processed = 0
last_non_empty_at = now

while processed < max_messages:
    batch = fetch(batch_size, fetch_timeout)
    if batch is empty:
        if now - last_non_empty_at >= idle_threshold:
            exit_reason = "drained"
            break
        continue

    last_non_empty_at = now
    for msg in batch:
        try:
            consume_one(msg)
        except Exception as error:
            record_failure(msg, error)
        processed += 1

if processed >= max_messages:
    exit_reason = "cap_reached"
```

Where the fetch tool distinguishes a broker timeout from an empty batch, count the broker timeout as an empty fetch; do not treat it as a single-message failure.

### 9. Consume message by message

For each message, in order:

1. **wildcard contract gate**: in wildcard mode, run the self-produced / DLQ-loop pre-filters first (see "Locate or bootstrap the contract > wildcard mode"); on either hit, `ack` straight away and do not enter steps 2-7. When neither hits, locate the active contract by `msg.subject`; an unknown or draft contract takes the awaiting-confirmation path and likewise does not enter the later steps.
2. **De-duplicate**: look `Nats-Msg-Id` up in the application-level de-duplication set; on a hit, `ack` and count it into `duplicates_skipped`.
3. **Decode headers**: a missing `Nats-Msg-Id` / `X-Source` / `X-Type`, or a header the contract requires, is judged unrecoverable.
4. **Decode payload**: a missing required field is judged unrecoverable; unknown fields are ignored; an unknown enum takes the business fallback.
5. **Continue the traceparent**: where one exists and the consumer supports OTel, extend the span.
6. **Call the business handler**: call only the consumer repo's own handler; this Skill implements no business logic.
7. **Execute the ack decision**.

### 10. Ack decisions

| Outcome | Action |
|---|---|
| Success | `ack` |
| Duplicate message | `ack` |
| wildcard echo of a self-produced message | `ack`; no contract resolution, no business handler |
| wildcard DLQ copy loop | `ack`; no contract resolution |
| Retryable failure, such as a network blip or downstream throttling | `nak` |
| Schema violation or permanent business failure | `term` the original message, and `publish` a copy to the DLQ |
| wildcard unknown or draft contract | `term` the original message, and `publish` a copy to `<subject>.dlq`, with `X-DLQ-Reason` starting with `awaiting contract confirmation` |

A DLQ copy carries at least:

- `X-DLQ-Original-Subject`
- `X-DLQ-Reason`
- `X-DLQ-Failed-At`
- The original headers (kept where they can be)

---

## Output

Emit an aggregated receipt, not the full message bodies, to avoid leaking the payload.

```yaml
exit_reason: drained
duration: 12.3s
counts:
  fetched: 87
  acked: 80
  naked: 4
  termed: 3
  dlq_sent: 3
  duplicates_skipped: 1
  self_sourced_skipped: 0
  dlq_echo_skipped: 0
failures:
  - msg_id: 01HX...A1
    subject: clarification.session.requested.v1
    decision: term
    reason: missing required payload field 'sessionId'
awaiting_confirmation:
  - subject: zentao.omnireview.some_new_event
    contract_path: .cortex/vendor-contracts/recloud-zentao/some-new-event-contract.md
    reason: newly bootstrapped draft, needs producer confirmation
backlog_hint: |
  exit_reason=drained, no follow-up run needed.
  If exit_reason=cap_reached, call this Skill again to keep draining.
  If awaiting_confirmation is non-empty, confirm the contracts first, then keep going.
```

`awaiting_confirmation` appears only in wildcard mode, or when a Bootstrap draft has not been confirmed.

---

## Error handling

| Situation | Handling |
|---|---|
| The NATS MCP server is not connected | Stop, and prompt for a check of the MCP configuration |
| A required MCP capability is missing | Stop, and list the missing capabilities |
| `.cortex/nats.yaml` is missing | Ask for the minimum necessary fields, and prompt for them to be written to disk |
| The contract is missing | Enter Bootstrap rather than terminating outright |
| Bootstrap lacks the peek capability | Stop; the contract cannot be inferred safely |
| The user has not confirmed an exact-subject draft | Stop once the draft is on disk, without acking |
| The durable does not exist | Stop, and point at the IaC owner |
| MAJOR version drift | Stop, and prompt for an upgrade of the vendored contract |
| A single message fails to decode | `term + DLQ`, record the failure, carry on with the batch |
| A single retryable failure | `nak`, record the failure, carry on with the batch |
| Fetches come back empty in a row | Exit as `drained` once `idle_threshold` is reached |
| wildcard hits an unknown or draft contract | `term + DLQ`, record `awaiting_confirmation`, carry on with the batch |

---

## Anti-patterns

- Letting one message's failure throw and break the whole batch.
- Failing as soon as an unknown field is decoded; a Tolerant Reader must ignore unknown fields.
- Not acking after the business logic succeeds.
- Using nak for an unrecoverable failure, causing endless redelivery.
- A DLQ copy without the original subject, the failure reason, and the timestamp.
- Creating broker resources such as a stream or a durable while the Skill runs.
- Going straight to a real ack when the contract is missing.
- Acking / naking / terming during the Bootstrap peek phase.
- Acking a message with an unknown or draft contract outright in wildcard mode.
- Treating a self-produced message (`X-Source == service_source`) or a DLQ-loop message carrying `X-DLQ-Original-Subject` as an unknown contract in wildcard mode, triggering Bootstrap to generate a surplus draft.
- Judging a DLQ loop by a bare `.dlq` suffix string match, swallowing a genuine business subject that ends in `.dlq`.
- Treating a missing `X-Source` header as equal to `service_source` and silently acking it as a self-produced message.
- Enabling `consume_pattern` and `consume_subjects` at the same time.
- Fetching an external HTTP/HTTPS contract or a raw URL by default.

---

## Self-check

- [ ] `.cortex/nats.yaml` has been read, or the missing fields have been stated explicitly.
- [ ] The NATS MCP tool capability map is complete, and no non-existent tool name is hard-coded.
- [ ] The exact-subject / wildcard / discovery mode has been chosen.
- [ ] The contract was located with the local vendored contract preferred.
- [ ] The Bootstrap phase did not ack, nak, term, or advance a real durable offset.
- [ ] A draft contract in exact-subject mode is formally acked only after the user's confirmation.
- [ ] wildcard mode lets only an active contract into the business handler.
- [ ] The wildcard self-produced / DLQ-loop pre-filters are in force; a missing `X-Source` was not misread as a self-produced message, and the DLQ loop is judged by `X-DLQ-Original-Subject` rather than a bare `.dlq` suffix.
- [ ] One message's failure does not break the whole batch.
- [ ] The output carries counts, failures, and exit_reason, plus awaiting_confirmation where needed.
- [ ] No external HTTP/HTTPS link was fetched by default.

---

## Examples

### Example 1: an exact-subject drain

Input:

```text
consume nats producer=agentfabric event=clarification.session.requested max_messages=100
```

Expected:

1. Read `.cortex/nats.yaml`.
2. Map the NATS MCP fetch / ack / nak / term / publish capabilities.
3. Locate `clarification-session-requested-contract.md`.
4. Reuse `<durable_name_prefix>-clarification-session-requested`.
5. Drain to `drained` or `cap_reached`.
6. Return the aggregated receipt.

### Example 2: wildcard meets a new subject

Configuration:

```yaml
consume_pattern: zentao.omnireview.>
consume_subjects:
  - zentao.omnireview.task.updated.v1
```

Expected:

1. Ignore `consume_subjects` and use `<durable_name_prefix>-wildcard` alone.
2. Receive `zentao.omnireview.some_new_event.v1`.
3. No active contract matches locally, so generate an N=1 draft with field requiredness marked `to be confirmed`.
4. `term + DLQ` the current message, with the reason starting with `awaiting contract confirmation`.
5. Carry on with the other messages in the batch, and finally list that subject under `awaiting_confirmation`.

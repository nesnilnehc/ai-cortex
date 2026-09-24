# consume-nats-message: examples

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

# consume-nats-message: anti patterns

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

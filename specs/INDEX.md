# Specifications

- [agent-test-modeling.md](./agent-test-modeling.md) — fields of a single LLM agent's test contract: capability boundary / input contract / tool boundary / write-back preconditions / oracles / golden cases. Does not cover how test code is written
- [adr-modeling.md](./adr-modeling.md) — frontmatter fields of an ADR document, the 5-value status enum, and the fields decay depends on
- [cross-team-contract.md](./cross-team-contract.md) — naming suffix, `contract_version`, CHANGELOG, flat layout and version references for a cross-team contract document
- [claude-md-modeling.md](./claude-md-modeling.md) — section structure, form requirements and per-level responsibilities of CLAUDE.md, the three-level long-term AI memory file
- [functional-design-modeling.md](./functional-design-modeling.md) — field definitions and validation for a functional design document, from the business and product viewpoint: functional modules, business workflow, role permissions, business object states, exception scenarios
- [technical-design-modeling.md](./technical-design-modeling.md) — field definitions and validation for a technical design document, from the engineering viewpoint: architecture, service decomposition, components, database, interface contracts, error handling, technology selection
- [nats-messaging.md](./nats-messaging.md) — subject, headers, payload and version evolution contract for cross-project NATS messages; the NATS specialisation of cross-team-contract
- [requirement-modeling.md](./requirement-modeling.md) — field definitions, format and validation for a requirement document
- [release-package.md](./release-package.md) — version identity, release materials, quality evidence and stage status contract for a Release Package
- [spec-modeling.md](./spec-modeling.md) — the spec for specs: the section skeleton, frontmatter contract and three-state classification every spec document follows
- [skill-source-modeling.md](./skill-source-modeling.md) — the local copy, pinned upstream commit and digest, license, modification record and maintenance update contract for an externally derived skill
- [task-modeling.md](./task-modeling.md) — fields, status enum and dependency semantics of a task list
- [test-case-modeling.md](./test-case-modeling.md) — fields, traceability anchor (covers) and status enum of a QA business test case document. Does not cover code-level tests
- [test-coverage-modeling.md](./test-coverage-modeling.md) — fields and body skeleton of a test coverage report (traceability matrix + mutation summary + traceability health audit); the input artifact for suite coverage review and cross-artifact alignment review
- [universal-notification.md](./universal-notification.md) — structure and fields of a notification artifact

Terminology is defined in [docs/architecture/terminology.md](../docs/architecture/terminology.md).

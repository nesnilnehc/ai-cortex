---
artifact_type: terminology
created_by: ai-cortex
lifecycle: living
created_at: 2026-03-25
status: active
---

# AI Cortex core terminology

> The authoritative definition of the four governance asset layers — Spec / Protocol / Skill / Rule — what each owns exclusively, and how to tell confusable pairs apart. Every project document treats this as the single source of truth.

---

## I. The four concepts

### Spec

> Defines a thing itself — its structural and behavioural contract.

- **Industry counterparts**: HTTP RFCs, the OpenAPI Specification, JSON Schema, IEEE 830
- **Core question**: **what does this thing look like**?
- **Typical content**: field definitions, type contracts, validation rules, behavioural constraints such as "GET must be idempotent"
- **Character**: a static description, written for every reader, not tied to one particular interaction

### Protocol

> Defines how several entities interact — the steps, the states, the message sequence.

- **Industry counterparts**: TCP, the OAuth 2.0 authorization code flow, the TLS handshake, SMTP
- **Core question**: **how do these two or more roles work together**?
- **Typical content**: message sequences, state machines, error handling, timeouts and retries
- **Character**: dynamic, must involve ≥ 2 roles, and has a definite start and end

### Skill

> Defines a capability a single agent can invoke — objective plus execution plus examples.

- **Industry counterparts**: Anthropic Skills (agentskills.io), a LangChain Tool, an OpenAI Function
- **Core question**: **what task can the agent complete**?
- **Typical content**: the objective, the execution flow, inputs and outputs, examples, optional tools
- **Character**: executed by one party — the agent carries it through end to end — objective-driven, with a definite output

### Rule

> Defines a constraint that cannot be crossed — each one independently verifiable.

- **Industry counterparts**: an ESLint rule, the Google Style Guide, GDPR, a pre-commit hook
- **Core question**: concretely, **what must not be done, and what must be done**?
- **Typical content**: a prohibition or an obligation, verifiable item by item by a machine or by a person
- **Character**: checkable, and carrying no process. One rule document can hold several constraints that share a scope, such as a shell style guide; what matters is that each is independently verifiable, and the document itself is not required to be atomic

---

## II. What each layer owns exclusively

| Concept | Exclusive meaning |
|----|----|
| Spec | "the contract describing a thing" — nowhere else may redefine that structure |
| Protocol | "the byte-level or message-level sequence coordinating several parties" — nowhere else may prescribe the interaction steps |
| Skill | "an objective-driven capability an agent can be routed to" — nowhere else may declare an invocable capability matchable by description or tags |
| Rule | "an atomic, checkable constraint" — nowhere else may say "X is forbidden" or "Y is required" without supplying the means to verify it |

---

## III. Telling confusable pairs apart (4 of them)

### 1. Spec vs Protocol

- What they share: either may carry the words "MUST / MUST NOT"
- **The question**: is this the contract of a noun, or the sequence of several verbs?
- A noun's contract -> Spec; a sequence of verbs -> Protocol
- **Example**: UNP's "field table of the notification object" = Spec; INP's "steps for rendering and delivering a notification from the sender to an IM channel" = Protocol

### 2. Skill vs Protocol

- What they share: both involve execution and process
- **The question**: is this carried out by one party, or does it take several working together?
- One party -> Skill; several parties -> Protocol
- **Example**: `review-typescript`, where the agent scans the code and produces findings on its own, = Skill; INP, with a sender and an IM channel, = Protocol

### 3. Spec vs Rule

- What they share: either may carry constraint statements
- **The question**: does it define what a thing looks like, or bound what may be done?
- A structural definition -> Spec; a behavioural constraint -> Rule, either a single one or several bound together under one scope
- **Example**: UNP's "the notification object has 7 fields" = Spec; `standards-shell` listing 8 shell style constraints = Rule, several sharing one scope

### 4. Skill vs Rule

- What they share: both govern behaviour
- **The question**: is this an end-to-end task, or a single check?
- A task -> Skill; a check -> Rule
- **Example**: `commit-work`, the whole flow of writing the message, staging, verifying and committing, = Skill; the single line "a commit message must be ≤ 72 characters" = Rule

---

## IV. Embedding: what is allowed and what is not

### Allowed, with no need to force a split

- **A Spec embedding a Rule**: a Spec attaches a validation rule while describing a field, such as "actions is required when priority ∈ [P0, P1]" — that is intrinsic to the Spec
- **A Protocol embedding a Spec**: a Protocol references the message Spec while describing a message sequence, as INP references UNP — through the `related` field
- **A Skill referencing a Spec, Protocol or Rule**: a Skill references the relevant Spec when describing its output and follows the relevant Rule in its execution steps — through links

### Not allowed

- **A Skill embedding a Protocol**: a multi-party flow belongs outside, as a Protocol, never buried inside some Skill
- **A Rule embedding a process**: a process belongs outside, as a Skill; a Rule must stay atomic and checkable

---

## V. Where each lives on disk

| Term | Default directory | Note |
|----|----|----|
| Spec | `specs/` | A small Spec embedded in a Protocol may stay under `protocols/` |
| Protocol | `protocols/` | — |
| Skill | `skills/` | — |
| Rule | `rules/` | — |

---

## VI. How to use these terms in documents

1. **In a Chinese document, pair the Chinese and English on first use**: `规范（Spec）`, `协议（Protocol）`
2. **Later occurrences may use one language**, kept consistent throughout
3. **Machine-consumed fields — YAML, commands, IDs — stay English**
4. **They must not be confused or substituted for one another**: avoid an ambiguous coinage such as "the notification protocol specification"; write "the notification Spec (UNP)" or "the notification delivery Protocol (INP)"

---

## VII. Related documents

- [protocols/INDEX.md](../../protocols/INDEX.md) — the Protocol registry
- [rules/INDEX.md](../../rules/INDEX.md) — the Rule registry
- [skills/INDEX.md](../../skills/INDEX.md) — the Skill catalogue

Skills themselves follow the standard format at [agentskills.io](https://agentskills.io).

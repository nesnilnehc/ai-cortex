---
id: CROSS_TEAM_CONTRACT_SPEC_V1
name: Cross-Team Contract Schema
description: Spec defining the structural contract for cross-team interface documents — naming suffixes, frontmatter requirements, CHANGELOG conventions, broadcast model, and cross-repo reference rules.
version: 1.0.0
status: active
lifecycle: living
created_at: 2026-05-21
scope: |
  Defines the structural contract for documents shared between independently-evolving
  services / repos / teams (interfaces, data shapes, state machines, event payloads).
  Does not apply to intra-team designs or internal module interfaces.
related:
  - ./spec-modeling.md
---

# 跨团队契约规范

> **Data contract**: defines how a document describing interfaces, data shapes, state machines and event payloads shared across independent services, repositories or teams is organised

---

## 1. Position and scope

This spec applies to a contract file meeting any one of these conditions:

- It describes an interface, data shape, state machine or event payload this repository **provides**, consumed by a repository, team or service that evolves independently
- It describes a third-party interface this repository **consumes** — a profile file — whose upstream version evolution has to be tracked
- It accompanies a machine-readable contract such as OpenAPI, JSON Schema, Protobuf or an event schema

**Out of scope**: interfaces between modules inside this repository, on the same team and the same release cycle. Those are design documents (`-design.md`), not contracts.

---

## 2. Naming

A cross-team contract declares its type through a **filename suffix**, so a consumer can enumerate every outward promise this repository makes with `grep -- '-contract\.md$'`:

| Suffix | Meaning | Example |
|---|---|---|
| `*-contract.md` | A cross-team interface, data or lifecycle contract — a binding promise | `lifecycle-contract.md` |
| `*-design.md` | Internal design intent, promising nothing externally | `lifecycle-design.md` |
| `*-guide.md` | A usage guide or integration manual | `bff-integration-guide.md` |
| `*-schema.md` | A description of a data structure schema | `patch-schema.md` |
| `*-profile.md` | A local profile of a third-party interface | `<upstream>-server-api-profile.md` |

Mandatory:

- A file consumed across teams **must** use the `-contract` suffix
- A design file **must never** use the `-contract` suffix, however formal it reads

---

## 3. Directory layout

Keep contract directories flat. The filename suffix already marks the type, so a `contracts/` subdirectory marking it a second time is redundant.

```text
✅ integrations/<x>/lifecycle-contract.md
   integrations/<x>/lifecycle-design.md          <- same level

❌ integrations/<x>/contracts/lifecycle-contract.md
   integrations/<x>/lifecycle-design.md          <- two levels
```

**Exception**: where one integration domain holds ≥ 10 contracts from heterogeneous sources — several upstream products each with their own `*-profile.md` — subdirectories may group them by source (`upstream/zentao/`, `upstream/jira/`), while staying flat within a source.

---

## 4. Frontmatter contract

Beyond the frontmatter fields each project requires generally, a cross-team contract file must also carry:

```yaml
contract_version: <SemVer>      # required; MAJOR.MINOR.PATCH
```

### 4.1 SemVer semantics

| Kind | Trigger |
|---|---|
| **MAJOR** | Removing a field, changing a URL, changing state machine semantics, changing what an enum value means |
| **MINOR** | Adding a field, an endpoint or an enum value; a backwards-compatible behavioural extension |
| **PATCH** | Documentation revision, an additional error code, an updated example |

---

## 5. Body structure contract

A cross-team contract file must contain these sections. The order may vary and the names may be localised:

### 5.1 Required sections

| Section | Contents |
|---|---|
| Contract scope | The interfaces, data shapes and state machines promised externally |
| Field and interface definitions | Concrete field tables, types, enums, whether each is required, and examples |
| CHANGELOG | Version history; every `contract_version` bump leaves an entry |

### 5.2 CHANGELOG entry structure

Every CHANGELOG entry must carry:

- Version and date: `### 1.8.0 — 2026-05-09`
- Change kind: `Added` / `Changed` / `Removed` / `BREAKING`
- Blast radius: which fields, endpoints or behaviours are affected
- Backwards compatibility: whether a consumer has to change code
- Implementation link: the code location or PR referenced

```markdown
### 1.8.0 — 2026-05-09

**Changed (BREAKING for un-shipped consumers)**: `chunkId` → `feedbackId`
- Blast radius: every endpoint carrying chunkId (GET /feedback, POST /feedback/ack)
- Compatibility: un-shipped consumers must rename the field; shipped consumers are unaffected, as the old API stays until 2.0.0
- Implementation: apps/server PR #2341
```

### 5.3 Counter-examples

- ❌ `1.5.0 — documentation improvements`, which carries no information
- ❌ Changing what a field means without bumping `contract_version`, leaving the other side to discover it from a git diff

### 5.4 What must not appear

A cross-team contract file **must never** carry implementation schedules, todos or integration milestones:

- ❌ `Phase A: the other team completes X by D+3`
- ❌ `@xxx team todo`
- ❌ A cross-team integration Gantt chart

That information belongs in each side's own `tasks.md` or `backlog.md`, not in the contract.

---

## 6. Collaboration model

Cross-team contracts run on **one-way broadcast by the provider, self-tracking by the consumer**:

- The provider maintains SemVer and a CHANGELOG in its own contract file
- Each consumer decides when to upgrade and tracks its own implementation in its own backlog
- Upstream changes are announced through the CHANGELOG; where a downstream does not subscribe, its CI and PRs are never blocked by the other side's progress

Industry equivalent: the common denominator of Pact, OpenAPI and similar.

**Why not track both directions**: two-way todos seep the other side's implementation detail into your own product documentation and turn the contract into a cross-team Gantt chart. As soon as their schedule slips, your contract document has to be rewritten in response.

---

## 7. Cross-repository reference convention

When a downstream repository references an upstream contract from its own code or documentation, it **must reference the `contract_version`**:

- ✅ `implements lifecycle-contract@1.0.0`, changed to `@1.1.0` on upgrade
- ❌ Implementing against `https://github.com/upstream/repo/blob/main/contracts/foo.md`, since main moves
- ❌ Referring to the contract at `commit abc1234`, unless it is deliberately a frozen snapshot reference

**Why**: a URL or commit reference couples tightly to the upstream directory structure. A version number is a promise and survives a file move or a directory reorganisation — `lifecycle-contract@1.0.0` always points at the same semantics.

---

## 8. Anti-patterns

```markdown
<!-- ❌ an implementation checklist inside a contract document -->
## §6 Task archiving convention
- [ ] Phase A: the other team implements the lifecycle UI (D+3)
- [ ] Phase B: integration and acceptance (D+5)
- [ ] @zhangsan owns Phase C
```

```yaml
# ❌ a field changed without bumping the version
contract_version: 1.5.0
# chunkId was actually renamed to feedbackId, and the CHANGELOG never moved
```

```text
❌ ambiguous naming
docs/integration/foo-spec.md       # is this a spec or a contract?
docs/integration/foo-contract.md   # is this the same document as the one above?
```

```text
❌ redundant subdirectory
docs/integrations/<x>/clarification/
  contracts/
    lifecycle-contract.md
    split-contract.md
  lifecycle-design.md
  split-design.md
```

```markdown
<!-- ❌ tightly coupled URL -->
Implement the interface according to https://gitlab/repo/-/blob/main/api.md.
```

---

## 9. Example

See `docs/architecture/integrations/zentao/clarification/lifecycle-contract.md` in the AgentFabric project (recloud-agentfabric):

- Its frontmatter carries `contract_version: 1.0.0`
- It has a SemVer table and a CHANGELOG, the first entry being `1.0.0 — 2026-05-09 Initial Release`
- The `lifecycle-design.md` next to it carries the design intent without posing as a contract
- There is no `contracts/` subdirectory; the layout is flat
- It does not track the ZenTao team's phase schedule, only broadcasts version changes one way

`contracts/CHANGELOG.md` is the corresponding practice for a machine-readable OpenAPI contract: `clarification-api.yaml` went 1.7.0 → 1.8.0 (BREAKING: chunkId → feedbackId) → 1.9.0 (Added: getBadges), each bump accompanied by full Added / Changed / Removed entries, an implementation link and a compatibility note.

---

## 10. Relationship to other assets

- The generally required documentation frontmatter fields (`artifact_type` / `created_by` / `lifecycle` / `created_at`) are governed by each project's own documentation conventions; this spec only adds the `contract_version` and CHANGELOG requirements specific to contract documents
- Governance of temporary documents is carried by each project's documentation workflow rules, orthogonal to this spec
- **NATS specialisation**: [nats-messaging.md](./nats-messaging.md) inherits this spec's general skeleton — naming suffix, `contract_version`, CHANGELOG, flat layout, cross-repository references — and adds the NATS-specific subject naming, headers table, payload conventions and embedded validation rules. Producing and consuming are handled by the paired skills [publish-nats-message](../skills/publish-nats-message/SKILL.md) and [consume-nats-message](../skills/consume-nats-message/SKILL.md)

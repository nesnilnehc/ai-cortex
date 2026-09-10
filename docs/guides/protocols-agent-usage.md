---
artifact_type: guide
created_at: 2026-03-25
status: active
lifecycle: living
---

# Protocols for AI agents

This guide explains how an AI agent, Claude Code included, **discovers, loads and applies** a protocol spec automatically.

---

## The idea

**A user must not have to read the protocol documents by hand** — the agent should do this work:

1. **Discovery** — find the available protocols through skills/INDEX.md
2. **Injection** — load them into the working session as long-lived background context
3. **Application** — apply the protocol's constraints while generating and reviewing code
4. **Verification** — check the generated code against the protocol through a skill

---

## 1. Automatic discovery

### 1.1 Discovery through the manifest

At startup the agent should read `skills/INDEX.md` to find every available protocol:

```json
{
  "registry": {
    "protocols_root": "protocols/",
    "protocols_index": "protocols/INDEX.md",
    ...
  }
}
```

### 1.2 The discovery flow

```python
# pseudocode, run at agent startup
def discover_protocols():
    manifest = load_json("skills/INDEX.md")
    protocols_dir = manifest["registry"]["protocols_root"]
    protocols_index = manifest["registry"]["protocols_index"]

    # read INDEX.md for every protocol and its metadata
    index = parse_markdown(protocols_index)

    for protocol in index.protocols:
        protocol_file = f"{protocols_dir}/{protocol.file}"
        metadata = extract_frontmatter(protocol_file)

        # decide from the context whether to load it
        if is_relevant_to_current_task(protocol):
            load_protocol_as_context(protocol_file)
```

### 1.3 Protocol metadata in the frontmatter

A protocol file should carry machine-readable metadata:

```yaml
---
id: UNIVERSAL_NOTIFICATION_SPEC_V2
name: Universal Notification Protocol
version: 1.0.0
status: active
lifecycle: living
scope: >
  Applicable whenever designing or reviewing notification systems.
  All notifications MUST be expressed as UNP objects before delivery.
domain: notifications
applies_to: [design, code-review, implementation]
related: [./inp.md]
---
```

**What each field is for**:
- `id` — the globally unique identifier an agent refers to it by
- `scope` — the text an agent judges relevance from
- `applies_to` — which phases it applies in: design, review, implementation
- `domain` — the problem domain it covers
- `related` — references to related protocols

---

## 2. Automatic injection

### 2.1 What triggers a load

An agent should load the relevant protocol automatically in these cases:

```text
Trigger 1: the user mentions a word related to "notification"
  -> load UNP + INP automatically

Trigger 2: a skill runs
  -> read the protocols field from the skill's frontmatter
  e.g. review-notifications loads [UNP, INP] automatically

Trigger 3: the project configuration names them
  -> read from .claude/config.yaml or CLAUDE.md
  protocols:
    - specs/universal-notification.md
    - protocols/im-notification-delivery.md

Trigger 4: inference from context
  -> analyse the code or the diff for a domain a protocol covers
```

### 2.2 How they are loaded

```yaml
# .claude/config.yaml, the project configuration
protocols:
  # notification system
  - file: ./specs/universal-notification.md
    domain: notifications
    inject_as: system_context
  - file: ./protocols/im-notification-delivery.md
    domain: notifications
    inject_as: system_context

# or in CLAUDE.md
# PROTOCOLS: ./specs/universal-notification.md, ./protocols/im-notification-delivery.md
```

### 2.3 Declaring a protocol at the skill level

A skill should declare the protocols it depends on in its frontmatter:

```yaml
---
name: review-notifications
protocols:
  - id: UNIVERSAL_NOTIFICATION_SPEC_V2
    version: ">=1.0.0"
  - id: INP_SPEC_V1
    version: ">=1.0.0"
---
```

When the agent runs the skill, it loads the declared protocols automatically.

---

## 3. Automatic application

### 3.1 While generating code

When an agent generates code that touches notifications, it should apply the protocol:

```text
User request: "generate a notification system that sends a build-failure alert"

Agent flow:
  1. recognise that the task is in the notifications domain
  2. load UNP + INP automatically
  3. build the notification object structure from the UNP schema
  4. build the rendering logic from the INP rules
  5. emit code that already conforms
```

### 3.2 While reviewing code

While reviewing code, an agent should check it against the protocol:

```text
Run the skill: /review-notifications

The checks, taken from the protocol:
  ✓ every notification object has id, type, intent, priority
  ✓ P0 and P1 carry actions
  ✓ type uses UPPER_SNAKE_CASE
  ✓ deduplication and rate limiting applied to P0 and P1
  ✓ the INP rendering rules applied correctly
  ✓ no direct send("message") call

Returns: a compliance report, generated automatically with no human input
```

### 3.3 Deriving validation rules from a protocol

```python
# an agent can parse validation rules out of a protocol's frontmatter
def extract_validation_rules(protocol_doc):
    """Extract the validation rules from a protocol document"""

    rules = []

    # parse the normative statements: MUST, MUST NOT, FORBIDDEN and the like
    must_rules = extract_patterns(protocol_doc, r"MUST\s+(.+)")
    must_not_rules = extract_patterns(protocol_doc, r"MUST NOT\s+(.+)")
    forbidden_rules = extract_patterns(protocol_doc, r"FORBIDDEN:\s*(.+)")

    return {
        "mandatory": must_rules,
        "forbidden": must_not_rules + forbidden_rules
    }

# apply them during review
rules = extract_validation_rules(load_protocol("unp.md"))
violations = check_code_against_rules(code, rules)
```

---

## 4. Example agent workflows

### 4.1 Designing a notification system

```text
User: "design a notification system supporting Feishu and WeCom"

┌─ Agent automation ──────────────────────────────────────┐
│                                                          │
│ 1. Recognise the task                                    │
│    -> keywords: "notification system", Feishu, WeCom     │
│                                                          │
│ 2. Load the protocols automatically                      │
│    -> loads UNIVERSAL_NOTIFICATION_SPEC_V2 + INP_SPEC_V1 │
│                                                          │
│ 3. Analyse the requirement                               │
│    -> 2 channels needed, priorities from P0 to P3        │
│                                                          │
│ 4. Apply the UNP spec                                    │
│    -> design a UNP-compatible notification schema        │
│                                                          │
│ 5. Apply the INP spec                                    │
│    -> rendering and routing rules for Feishu and WeCom   │
│                                                          │
│ 6. Generate the code, compliant by construction          │
│    |- notification.py   (the UNP object definitions)     │
│    |- feishu_adapter.py (the Feishu INP implementation)  │
│    |- wecom_adapter.py  (the WeCom INP implementation)   │
│    \- router.py         (dynamic routing)                │
│                                                          │
│ 7. Verify automatically                                  │
│    -> run /review-notifications                          │
│    -> all code ✅ conforms to UNP + INP                  │
│                                                          │
│ 8. Report to the user                                    │
│    -> "built to UNP v1.0.0 + INP v1.0.0"                 │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 4.2 Reviewing code

```text
User: "review this notification code"

┌─ Agent automation ──────────────────────────────────────┐
│                                                          │
│ 1. Analyse the code                                      │
│    -> detected: notification sending, the Feishu API     │
│                                                          │
│ 2. Load the protocols automatically                      │
│    -> loads UNP + INP, having found them relevant        │
│                                                          │
│ 3. Run the compliance checks                             │
│    |- UNP validation (10 checks)                         │
│    |- INP validation (8 checks)                          │
│    \- architecture check (notification layer separated)  │
│                                                          │
│ 4. Produce the report                                    │
│    |- ✅ UNP compliance: 8/10                            │
│    |- ✅ INP compliance: 8/8                             │
│    \- ⚠️ suggestion: add deduplication (INP §7)          │
│                                                          │
│ 5. Produce fix suggestions                               │
│    -> the agent generates the patch                      │
│                                                          │
│ 6. Apply the fixes, optionally automatically             │
│    -> /orchestrate-repair-loop applies them              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 5. Skill integration

### 5.1 The review-notifications skill

```yaml
# skills/review-notifications/SKILL.md (pseudocode)

---
name: review-notifications
description: Review notification code for UNP/INP compliance
protocols:
  - id: UNIVERSAL_NOTIFICATION_SPEC_V2
    version: ">=1.0.0"
  - id: INP_SPEC_V1
    version: ">=1.0.0"
---

# when this skill runs:
# 1. the agent loads UNP + INP as context
# 2. the agent reviews against the rules the protocols define
# 3. it returns a compliance report
```

### 5.2 The apply-unp skill (planned)

```yaml
# a protocol-driven code refactor
name: apply-unp
description: Refactor code to use UNP objects
protocols:
  - id: UNIVERSAL_NOTIFICATION_SPEC_V2
    version: ">=1.0.0"

# when this skill runs:
# user: "refactor my notification code to use UNP"
# the agent then:
#   1. loads the UNP protocol
#   2. analyses the existing code
#   3. produces a UNP-conforming refactor
#   4. applies the change
```

---

## 6. Protocol-driven automation

### 6.1 Configuration-driven agent behaviour

```yaml
# .claude/config.yaml
protocols:
  - file: ./specs/universal-notification.md
    applies_to: [code-generation, code-review]
    auto_apply: true
    auto_verify: true

  - file: ./protocols/im-notification-delivery.md
    applies_to: [implementation, testing]
    auto_apply: true

# what this means:
# - UNP is applied while generating code
# - UNP is verified while reviewing code
# - on a failure, a fix is suggested
```

### 6.2 CI/CD integration

```yaml
# .github/workflows/protocols.yml
name: Protocol Compliance Check

on: [push, pull_request]

jobs:
  check-protocols:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # step 1: load the protocols
      - name: Load protocols
        run: |
          agent-cli load-protocols --manifest skills/INDEX.md

      # step 2: review the notification code
      - name: Review notifications
        run: |
          agent-cli review --protocols unp,inp ./src/notifications

      # step 3: report compliance
      - name: Report compliance
        run: |
          agent-cli report --format json > compliance-report.json
```

---

## 7. How an agent interacts with the user

### The traditional pattern, not recommended

```text
User:  "how do I use this notification protocol?"
Agent: "please read section 4 of docs/guides/protocols-usage.md..."
User:  😞 (has to work it out by hand)
```

### The agent-driven pattern, recommended

```text
User:  "generate a notification system"
Agent: ✅ loads UNP + INP
Agent: ✅ generates conforming code
Agent: ✅ returns an implementation that follows the protocol
User:  😊 (it works out of the box)
```

### The mixed pattern, the best of both

```text
User:  "I want to understand the notification protocol properly"
Agent:
  "You can:
   1. read the quick reference: docs/guides/protocols-quickstart.md
   2. read the full guide: docs/guides/protocols-usage.md
   3. or have me review or generate the code for you"
```

---

## 8. Implementation checklist for agent builders

- [ ] **Discovery** — discover the protocols in skills/INDEX.md automatically
- [ ] **Metadata parsing** — extract the protocol metadata from the frontmatter: scope, applies_to, domain
- [ ] **Context injection** — load the relevant protocol at startup, or at the moment it matters
- [ ] **Skill integration** — support a protocols declaration in a skill's frontmatter
- [ ] **Automatic verification** — generate the check functions from the protocol's rules
- [ ] **Reporting** — produce a machine-readable compliance report in JSON or YAML
- [ ] **Code generation** — apply the protocol's constraints while generating code
- [ ] **Fix suggestions** — generate the patch when the protocol is violated

---

## 9. Where this could go

### Generating a protocol dynamically

```text
The long-term vision: an agent generates a protocol from a project's needs
  e.g. "I need a logging protocol"
  the agent produces logging-protocol.md, from a template plus the requirement
```

### Cross-protocol validation

```text
The long-term vision: check several protocols against each other automatically
  e.g. are UNP, INP and a security protocol mutually compatible?
```

### Protocol version management

```text
The long-term vision: an agent tracks protocol versions and migration paths
  when UNP moves to v2.0.0:
  the agent then:
    1. detects the version the code uses
    2. produces a migration plan
    3. applies the migration automatically, where that is possible
```

---

## 10. How this relates to the human-facing guide

| Aspect | The human guide | The agent guide |
|:---|:---|:---|
| **Audience** | A human developer | An AI agent |
| **How it is learned** | By reading the document | By loading and applying it automatically |
| **How it is verified** | A manual checklist | Automatically |
| **Code generation** | Written by the user | Generated by the agent |
| **Compliance** | The user's responsibility | Guaranteed by the agent |

**They complement each other**:
- The user reads docs/guides/protocols-usage.md, to understand the concepts
- The agent reads docs/guides/protocols-agent-usage.md, to act on them

---

**The principle**: the agent does the heavy lifting; the user stays on the high-level requirement.

**Last updated**: 2026-03-25

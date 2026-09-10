---
artifact_type: guide
created_at: 2026-03-25
status: active
lifecycle: living
---

# Protocols usage guide

This guide explains how to discover, install and use the domain protocol specs AI Cortex provides.

---

## 1. What is a protocol?

**Definition**: a protocol is a standardised interface spec for one problem domain, notification systems for instance.

**Characteristics**:
- **Versioned**: an explicit semantic version, 1.0.0 and so on
- **Layered**: usually several layers, such as UNP's semantic layer plus INP's delivery layer
- **Standardised**: it states what is required (MUST), what is FORBIDDEN, and the best practice
- **Reusable**: it applies across projects and teams

**How it differs from the other assets**:

| Asset type | What it is for | How it is loaded |
|:---|:---|:---|
| **Skill** | An active capability, invoked to complete a task | Injected on demand |
| **Protocol** | An interface contract, followed to stay compatible | Loaded permanently, as long-lived background |
| **Rule** | A behavioural constraint that holds while working | Loaded permanently, as long-lived background |

---

## 2. Discovering a protocol

### 2.1 Browsing online

1. **Look at the protocol registry**: open [`protocols/INDEX.md`](../../protocols/INDEX.md)
2. **Confirm what is available today**:
   - UNP (Universal Notification Protocol) v1.0.0
   - INP (IM Notification Protocol) v1.0.0

3. **Read the detail**:
   - [`specs/universal-notification.md`](../../specs/universal-notification.md) — the semantic layer spec (UNP)
   - [`protocols/im-notification-delivery.md`](../../protocols/im-notification-delivery.md) — the delivery layer spec (INP)

### 2.2 Looking in the canonical clone

After installation, read AI Cortex's stable data directory directly:

```bash
ls "${XDG_DATA_HOME:-$HOME/.local/share}/ai-cortex/protocols/"
```

### 2.3 Through the registry

```bash
cat "${XDG_DATA_HOME:-$HOME/.local/share}/ai-cortex/protocols/INDEX.md"
```

---

## 3. Installing and using

### 3.1 The canonical install

AI Cortex keeps exactly one way to install and update:

```bash
mkdir -p ~/.local/share
git clone --depth 1 https://github.com/nesnilnehc/ai-cortex.git ~/.local/share/ai-cortex
~/.local/share/ai-cortex/bin/cortex install
```

**Verify the install**:

```bash
cortex status
ls "${XDG_DATA_HOME:-$HOME/.local/share}/ai-cortex/protocols/"
```

### 3.2 Using it in your project

A project's agent reads protocols from `$CORTEX_HOME/protocols/INDEX.md`, or from the default XDG path. When a project has to pin an AI Cortex version, record the canonical clone's full commit in the project configuration. Do not copy individual files, do not curl a raw URL, and do not add a second submodule.

---

## 4. Scenarios and examples

### 4.1 Designing a notification system, using UNP

**Scenario**: designing a new notification system

**Steps**:

1. **Read the UNP spec**: understand the required fields and the constraints

```markdown
# Under UNP, every notification must carry:
- id (uuid)
- type (UPPER_SNAKE_CASE)
- intent (info | action_required | approval | alert)
- priority (P0 | P1 | P2 | P3)
- title, body
- actions, required when priority ∈ [P0, P1]
```

2. **Implement the UNP object**:

```typescript
interface UNPNotification {
  id: string;           // uuid
  type: string;         // e.g., "BUILD_FAILED"
  source: string;       // e.g., "ci-pipeline"
  timestamp: string;    // ISO8601
  intent: 'info' | 'action_required' | 'approval' | 'alert';
  priority: 'P0' | 'P1' | 'P2' | 'P3';
  title: string;
  body: string;
  actor?: {type, id, name};
  target?: {type, id};
  actions?: Array<{type, label, url | command}>;
  extensions?: object;
}
```

3. **Check compliance**: use the `review-notifications` skill (planned)

```bash
# run the review
claude-code /review-notifications
# input:  notification code
# output: a UNP compliance report
```

### 4.2 Implementing IM delivery, using INP

**Scenario**: delivering a UNP notification to Feishu or WeCom

**Steps**:

1. **Read the INP spec**: understand the rendering and routing rules

```markdown
# Under INP:
- P0 -> card (an interactive card)
- P1 -> card
- P2 -> markdown
- P3 -> text (plain text)
# P0 and P1 must carry mention_user and actionable content
```

2. **Implement the delivery layer**:

```python
def deliver_notification(unp: UNPNotification, channel: str) -> str:
    """Transform UNP to channel-specific format"""

    # step 1: map the render format from the priority
    format_map = {'P0': 'card', 'P1': 'card', 'P2': 'markdown', 'P3': 'text'}
    render_format = format_map[unp.priority]

    # step 2: build the message per the INP rules
    message = {
        'header': {
            'priority': unp.priority,
            'emoji': get_emoji_for_intent(unp.intent)
        },
        'body': unp.body[:500],  # INP: max_length = 500
        'format': render_format
    }

    # step 3: inject mentions, where they are needed
    if unp.priority in ['P0', 'P1']:
        message['mentions'] = get_mentions_for_priority(unp.priority)

    # step 4: apply deduplication and rate limiting
    if not is_duplicate(unp.id) and not is_throttled(unp.source, unp.priority):
        send_to_channel(channel, message)

    return message
```

3. **Test INP compliance**:

```text
# Verify:
✓ P0 and P1 messages carry actions
✓ no raw JSON in the output
✓ deduplication and rate limiting applied
✓ channel capability degrades gracefully (WeCom has no card, so it falls back to markdown)
```

### 4.3 Sharing across projects

**Scenario**: several projects have to follow the same notification protocol

**Approach**:

1. **Keep the protocols in a shared location**:

```text
my-org/
├── protocols/          # the organisation's protocol library
│   ├── notification-protocol.md
│   └── logging-protocol.md
└── projects/
    ├── service-a/
    ├── service-b/
```

2. **Reference them from each project**:

```yaml
# service-a/.protocol-config.yaml
protocols:
  - name: notification
    url: ../../../protocols/notification-protocol.md
    version: "1.0.0"
```

3. **Check compliance**:

```bash
# in CI/CD
protocols-validate --config .protocol-config.yaml
```

---

## 5. Integrating with an AI agent

### 5.1 Using a protocol in Claude Code

Inject the protocol file as **long-lived background context**:

```bash
# option 1: through .claude/config.yaml
echo "
protocols:
  - ./specs/universal-notification.md
  - ./protocols/im-notification-delivery.md
" >> .claude/config.yaml

# option 2: through AGENTS.md, the AI Cortex entry point
# declare the protocol dependency in AGENTS.md
# see docs/guides/discovery-and-loading.md
```

### 5.2 Example: an AI-driven notification refactor

```text
User:   refactor my notification code to follow the UNP protocol
|
Claude loads:    unp.md as system context
|
Claude analyses: where the existing notification code differs from UNP
|
Claude proposes:
  1. replace send("message") with a UNP object
  2. add type (UPPER_SNAKE_CASE)
  3. add actions for P0 and P1
  4. apply deduplication and rate limiting
|
Claude implements: the refactor, automatically
|
Verify: run the review-notifications skill to check compliance
```

---

## 6. Versions and updates

### 6.1 Checking a protocol's version

```bash
# the current version
grep "^version:" specs/universal-notification.md

# the change log
grep -A 10 "Version" protocols/INDEX.md
```

### 6.2 Upgrading a protocol

```bash
# pull the newest AI Cortex and re-sync the canonical clone
cortex update

# check for breaking changes
git -C "${XDG_DATA_HOME:-$HOME/.local/share}/ai-cortex" log -p specs/universal-notification.md
```

### 6.3 Backward compatibility

- **Minor updates** (1.0.0 -> 1.1.0): new optional fields, backward compatible
- **Major updates** (1.0.0 -> 2.0.0): may carry breaking changes, and need a migration plan

---

## 7. FAQ

### Q: do I have to follow a protocol?

**A**: it depends on your case.

- ✅ **Follow it when**:
  - your project is part of an AI Cortex skill
  - you share a notification interface across projects
  - you want standardised, predictable behaviour

- ❌ **You need not when**:
  - the project stands entirely alone, with nothing to coordinate
  - the spec does not fit your situation

### Q: what is the difference between UNP and INP?

**A**:

| UNP | INP |
|:---|:---|
| **The semantic layer** | **The delivery layer** |
| Defines WHAT: a notification's structure and meaning | Defines HOW: how it is rendered and delivered |
| Channel-agnostic | Channel-specific: Feishu, WeCom |
| Produced by the business or application layer | Consumed by the delivery or middleware layer |
| Example: a BUILD_FAILED event | Example: a Feishu card, a WeCom text message |

### Q: what if the protocol does not fit what I need?

**A**: two options:

1. **Contribute the improvement** (preferred): open an issue or a PR against AI Cortex
2. **Create an extension**: put your own data in the `extensions` field

```javascript
{
  // the standard UNP fields
  type: "BUILD_FAILED",
  priority: "P1",
  // a custom extension
  extensions: {
    "my-org:build-system": {
      failureCode: "E_TIMEOUT",
      retryable: true
    }
  }
}
```

### Q: can my own channel be supported, such as Slack?

**A**: yes.

1. **Follow UNP**: make sure your notification is a valid UNP object
2. **Extend INP**: add the delivery rules for Slack

```yaml
# protocols/inp-extended.md
channel_matrix:
  slack:
    supports:
      - thread
      - button
    limitations:
      - no_rich_cards
```

3. **Contribute it back to AI Cortex**: where it generalises well, submit it as an official extension

---

## 8. Best practice

### ✅ Do

1. **Use a complete UNP object**: do not simplify it or leave fields out
2. **Pin the version**: name the protocol version explicitly in the project
3. **Review periodically**: check each quarter for a newer protocol version or an improvement
4. **Write it down**: state the protocols and versions used in the project README
5. **Test compliance**: wire in automated validation, review-notifications for instance

### ❌ Do not

1. **Mix protocol versions**: never use different UNP versions within one project
2. **Route around a constraint**: never violate a MUST or FORBIDDEN rule without a solid reason
3. **Hard-code a channel**: putting channel logic in the business layer breaks UNP's channel-agnostic principle
4. **Ignore updates**: never leave a protocol version unupdated for long

---

## 9. Reference

| Resource | Link | What it is |
|:---|:---|:---|
| **The protocol registry** | [protocols/INDEX.md](../../protocols/INDEX.md) | Every available protocol and its version |
| **The UNP spec** | [specs/universal-notification.md](../../specs/universal-notification.md) | The notification semantic layer |
| **The INP spec** | [protocols/im-notification-delivery.md](../../protocols/im-notification-delivery.md) | The notification delivery layer |
| **Discovery and loading** | [docs/guides/discovery-and-loading.md](./discovery-and-loading.md) | How an AI agent discovers an asset |
| **The AI Cortex entry point** | [AGENTS.md](../../AGENTS.md) | The project's identity and its authoritative sources |

---

## 10. Getting help

### Reporting a problem

When a protocol is defective or unclear:

1. **Open an issue**: https://github.com/nesnilnehc/ai-cortex/issues
2. **Label it**: `protocols`, `unp`, `inp`, `documentation`
3. **Describe it**: include your case and the behaviour you expected

### Contributing an improvement

```bash
# fork -> branch -> open a PR
git checkout -b feature/protocols-enhancement
# edit protocols/*.md
git commit -m "docs(protocols): ..."
git push origin feature/protocols-enhancement
# open the PR
```

---

**Last updated**: 2026-03-25
**Maintainer**: the AI Cortex team
**Related skill**: `review-notifications` (planned)

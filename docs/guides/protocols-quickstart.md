---
artifact_type: guide
created_at: 2026-03-25
status: active
lifecycle: living
---

# Protocols Quick Reference

## Installation

```bash
mkdir -p ~/.local/share
git clone --depth 1 https://github.com/nesnilnehc/ai-cortex.git ~/.local/share/ai-cortex
~/.local/share/ai-cortex/bin/cortex install
```

Skills are installed through `cortex`. Protocols stay in the canonical clone: agents read them straight from `~/.local/share/ai-cortex/protocols/`, and no copy, npm or on-demand download path is maintained any more.

---

## Core concepts

| | UNP (semantic layer) | INP (delivery layer) |
|:---|:---|:---|
| **Definition** | WHAT: the structure and meaning of a notification | HOW: how it is rendered and delivered |
| **Scope** | Channel-agnostic | Channel-specific |
| **Consumers** | Business / application layer | Delivery / middleware layer |
| **Required fields** | id, type, intent, priority, title, body | Format and mention rules derived from priority |

---

## UNP required fields

```typescript
{
  id: string;              // uuid
  type: string;            // event name (UPPER_SNAKE_CASE)
  source: string;          // source system
  timestamp: string;       // ISO8601
  intent: 'info' |         // notification intent
          'action_required' |
          'approval' |
          'alert';
  priority: 'P0' |         // priority
            'P1' |         // P0: interrupt, P1: important
            'P2' |         // P2: normal, P3: informational
            'P3';
  title: string;           // title
  body: string;            // body (max 500 chars)

  // if priority is in [P0, P1], actions must be present
  actions?: [{
    type: 'link' | 'command';
    label: string;
    url?: string;
    command?: string;
  }];
}
```

---

## INP rules at a glance

### Priority to format mapping

```text
P0 -> Card (interactive card)  must include mention_user + actionable
P1 -> Card                     must include mention_owner + actionable
P2 -> Markdown                 mention_user forbidden
P3 -> Text                     mention_user forbidden
```

### Deduplication and rate limiting

```yaml
P0: 1 per 5 minutes
P1: 1 per 10 minutes
P2: batched
P3: (unrestricted)
```

### Channel support

```text
Feishu: ✅ card, button, callback
WeCom:  ✅ markdown (limited interaction)
         ⚠️ unsupported features degrade
```

---

## Code examples

### Creating a UNP notification

```python
from datetime import datetime
from uuid import uuid4

notification = {
    "id": str(uuid4()),
    "type": "BUILD_FAILED",
    "source": "ci-pipeline",
    "timestamp": datetime.utcnow().isoformat() + "Z",
    "intent": "action_required",
    "priority": "P1",
    "title": "Build failed: main branch",
    "body": "Commit abc123 failed test suite. See logs for details.",
    "actor": {
        "type": "user",
        "id": "user_123",
        "name": "CI System"
    },
    "actions": [
        {
            "type": "link",
            "label": "View Logs",
            "url": "https://ci.example.com/builds/123"
        },
        {
            "type": "link",
            "label": "Fix Commit",
            "url": "https://github.com/myorg/myrepo/commits/abc123"
        }
    ]
}
```

### Delivering to an IM channel

```python
def send_notification(unp: dict, channel: str):
    """Deliver a UNP notification according to the INP rules"""

    # Rule 1: choose the format from the priority
    format_map = {
        'P0': 'card',
        'P1': 'card',
        'P2': 'markdown',
        'P3': 'text'
    }
    msg_format = format_map[unp['priority']]

    # Rule 2: check that P0/P1 carry actions
    if unp['priority'] in ['P0', 'P1']:
        assert 'actions' in unp and len(unp['actions']) > 0, \
            f"{unp['priority']} requires actions"

    # Rule 3: apply deduplication
    if is_duplicate(unp['id']):
        return

    # Rule 4: apply rate limiting
    rate_limit = {
        'P0': 5 * 60,      # 1 per 5 min
        'P1': 10 * 60,     # 1 per 10 min
    }.get(unp['priority'], 0)

    if is_throttled(unp['source'], rate_limit):
        return

    # Rule 5: deliver to the channel
    send_to_channel(channel, msg_format, unp)
```

---

## Verifying compliance

### Manual checklist

- [ ] Every UNP object carries id, type, intent, priority
- [ ] P0/P1 include actions
- [ ] type uses UPPER_SNAKE_CASE
- [ ] priority and intent values are inside their enums
- [ ] Deduplication and rate limiting are applied to P0/P1
- [ ] body is at most 500 characters

### Automated validation (planned)

```bash
# use the review-notifications skill
claude-code /review-notifications

# or validate locally
protocols-validate --protocol unp ./notifications.json
protocols-validate --protocol inp ./deliveries.json
```

---

## Common mistakes

| Mistake | Fix |
|:---|:---|
| `type` is not UPPER_SNAKE_CASE | ✅ `BUILD_FAILED`, not `buildFailed` |
| P0 has no actions | ✅ Add at least one action object |
| body over 500 characters | ✅ Truncate to at most 500 characters |
| intent value does not match | ✅ Use: info \| action_required \| approval \| alert |
| source field missing | ✅ Add the name of the originating system |

---

## FAQ

**Q: Must these protocols be used?**
A: If you are an AI Cortex user, or you need to share notifications across projects, following them is recommended. Otherwise they are optional.

**Q: Can the protocols be modified?**
A: Modifying the core spec is not recommended. Custom data can be added under the `extensions` field.

**Q: How do I add support for a new channel, such as Slack?**
A: Write an INP extension, or contribute it to AI Cortex. See the [full guide](./protocols-usage.md#q-can-my-own-channel-be-supported-such-as-slack).

**Q: How are UNP/INP versions upgraded?**
A: Check `protocols/INDEX.md` for the latest version. Breaking changes are marked by the major version number.

---

## Resources

| Resource | Link |
|:---|:---|
| **Full usage guide** | [protocols-usage.md](./protocols-usage.md) |
| **UNP spec** | [specs/universal-notification.md](../../specs/universal-notification.md) |
| **INP spec** | [protocols/im-notification-delivery.md](../../protocols/im-notification-delivery.md) |
| **Protocol registry** | [protocols/INDEX.md](../../protocols/INDEX.md) |
| **GitHub** | [ai-cortex/protocols](https://github.com/nesnilnehc/ai-cortex/tree/main/protocols) |

---

**Last updated**: 2026-03-25
**Related skill**: `review-notifications` (planned)

---
contract_version: 0.1.0
status: draft
inferred_from: bootstrap-peek
inferred_at: 2026-05-29T10:40:00+08:00
inferred_sample_size: 5
inferred_sample_seq_range: 4-8
authoritative: false
---

> ⚠️ 本契约由 consume-nats-message Bootstrap 模式从 5 条样本消息（seq 4-8）推断生成，**非权威**。请联系 producer owner（recloud-agentfabric）确认字段语义、QoS、DLQ 规则后将 `status` 升为 `active`、`authoritative` 升为 `true`。

# proposals-contract

来自 `recloud-agentfabric` 的跨项目提案消息契约。

## Subject

```
cortex.proposals.<kind>.<slug>
```

- `kind`：提案目标类型，已知枚举值：`principle` / `norm`
- `slug`：提案标识符，kebab-case

## Headers

本批样本未携带自定义业务 headers。

| Header | 必填 | 说明 |
|---|---|---|
| — | — | 待 producer owner 确认 |

## Payload

```json
{
  "proposal_id":    "<string>",
  "source_project": "<string>",
  "source_commit":  "<string>",
  "target": {
    "kind":   "<string>",
    "path":   "<string>",
    "anchor": "<string>"
  },
  "action":   "<string>",
  "title":    "<string>",
  "rationale": "<string>",
  "proposed_change": {
    "format":  "<string>",
    "content": "<string>"
  },
  "evidence": {
    "agentfabric_examples": ["<string>"],
    "issue_observed": "<string>"
  },
  "supersedes": null,
  "created_at": "<ISO 8601>"
}
```

### 字段说明

| 字段 | 类型 | 必填 | 枚举值 | 说明 |
|---|---|---|---|---|
| `proposal_id` | string | ✅ | — | 全局唯一提案 ID，格式 `<project>-<date>-<NNN>-<slug>` |
| `source_project` | string | ✅ | — | 发起提案的项目名 |
| `source_commit` | string | ✅ | — | 提案对应的 git commit |
| `target.kind` | string | ✅ | `principle`, `norm` | 目标 artifact 类型 |
| `target.path` | string | ✅ | — | 目标文件路径 |
| `target.anchor` | string | ✅ | — | 目标锚点 |
| `action` | string | ✅ | `add`, `modify` | 提案操作类型 |
| `title` | string | ✅ | — | 提案标题 |
| `rationale` | string | ✅ | — | 提案背景与动机 |
| `proposed_change.format` | string | ✅ | `full-text`, `freeform` | 变更内容格式 |
| `proposed_change.content` | string | ✅ | — | 变更正文 |
| `evidence.agentfabric_examples` | string[] | ✅ | — | 佐证示例列表 |
| `evidence.issue_observed` | string | ✅ | — | 观察到的问题描述 |
| `supersedes` | null\|string | ✅ | — | 被替代的提案 ID，无则为 `null` |
| `created_at` | string | ✅ | ISO 8601 | 提案创建时间 |

## QoS（TBD）

| 参数 | 值 |
|---|---|
| max_deliver | TBD |
| ack_wait | TBD |
| backoff | TBD |
| DLQ subject | TBD |

待联系 producer owner 确认后填入。

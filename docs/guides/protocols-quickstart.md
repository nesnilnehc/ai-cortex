---
artifact_type: guide
created_at: 2026-03-25
status: active
lifecycle: living
---

# 协议快速参考 (Protocols Quick Reference)

## 安装

```bash
# 方案 1：安装完整的 AI Cortex 包
npx skills add nesnilnehc/ai-cortex -g

# 方案 2：仅复制协议文件
git clone https://github.com/nesnilnehc/ai-cortex.git
cp -r ai-cortex/protocols/ ./your-project/
```

---

## 核心概念

| | UNP（语义层） | INP（投递层） |
|:---|:---|:---|
| **定义** | WHAT：通知的结构和含义 | HOW：如何渲染和投递 |
| **范围** | Channel-agnostic | Channel-specific |
| **使用者** | 业务/应用层 | 投递/中间件层 |
| **必填字段** | id, type, intent, priority, title, body | 基于 priority 的格式和提及规则 |

---

## UNP 必填字段

```typescript
{
  id: string;              // uuid
  type: string;            // 事件名 (UPPER_SNAKE_CASE)
  source: string;          // 来源系统
  timestamp: string;       // ISO8601
  intent: 'info' |         // 通知意图
          'action_required' |
          'approval' |
          'alert';
  priority: 'P0' |         // 优先级
            'P1' |         // P0: 中断, P1: 重要
            'P2' |         // P2: 正常, P3: 信息
            'P3';
  title: string;           // 标题
  body: string;            // 正文 (max 500 chars)

  // 如果 priority ∈ [P0, P1]，必须包含 actions
  actions?: [{
    type: 'link' | 'command';
    label: string;
    url?: string;
    command?: string;
  }];
}
```

---

## INP 规则速览

### 优先级 → 格式映射

```
P0 → Card（交互式卡片）  必须包含 mention_user + actionable
P1 → Card               必须包含 mention_owner + actionable
P2 → Markdown           禁止 mention_user
P3 → Text               禁止 mention_user
```

### 去重 & 限流

```
P0: 1 per 5 minutes
P1: 1 per 10 minutes
P2: batched
P3: (unrestricted)
```

### 渠道支持

```
Feishu: ✅ card, button, callback
WeCom:  ✅ markdown (有限交互)
         ⚠️ 不支持的功能会降级
```

---

## 代码示例

### 创建 UNP 通知

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

### 投递到 IM 渠道

```python
def send_notification(unp: dict, channel: str):
    """根据 INP 规则投递 UNP 通知"""

    # 规则 1：根据优先级选择格式
    format_map = {
        'P0': 'card',
        'P1': 'card',
        'P2': 'markdown',
        'P3': 'text'
    }
    msg_format = format_map[unp['priority']]

    # 规则 2：检查 P0/P1 是否有 actions
    if unp['priority'] in ['P0', 'P1']:
        assert 'actions' in unp and len(unp['actions']) > 0, \
            f"{unp['priority']} requires actions"

    # 规则 3：应用去重
    if is_duplicate(unp['id']):
        return

    # 规则 4：应用限流
    rate_limit = {
        'P0': 5 * 60,      # 1 per 5 min
        'P1': 10 * 60,     # 1 per 10 min
    }.get(unp['priority'], 0)

    if is_throttled(unp['source'], rate_limit):
        return

    # 规则 5：投递到渠道
    send_to_channel(channel, msg_format, unp)
```

---

## 验证合规性

### 手动检查清单

- [ ] 所有 UNP 对象都有 id, type, intent, priority
- [ ] P0/P1 包含 actions
- [ ] type 使用 UPPER_SNAKE_CASE
- [ ] priority 和 intent 值在枚举范围内
- [ ] P0/P1 已应用去重和限流
- [ ] body 长度 ≤ 500 字符

### 自动验证（计划中）

```bash
# 使用 review-notifications 技能
claude-code /review-notifications

# 或本地验证
protocols-validate --protocol unp ./notifications.json
protocols-validate --protocol inp ./deliveries.json
```

---

## 常见错误

| 错误 | 修复 |
|:---|:---|
| `type` 不是 UPPER_SNAKE_CASE | ✅ `BUILD_FAILED` 而非 `buildFailed` |
| P0 缺少 actions | ✅ 添加至少一个 action 对象 |
| body > 500 字符 | ✅ 截断为 ≤ 500 字符 |
| intent 值不匹配 | ✅ 使用: info \| action_required \| approval \| alert |
| 缺少 source 字段 | ✅ 添加通知源系统名称 |

---

## 常见问题

**Q: 是否必须使用这些协议？**
A: 如果你是 AI Cortex 用户或需要跨项目通知共享，建议遵循。否则可选。

**Q: 能否修改协议？**
A: 不建议修改核心规范。可在 `extensions` 字段中添加自定义数据。

**Q: 如何添加新的渠道支持（如 Slack）？**
A: 创建 INP 扩展或向 AI Cortex 贡献。见 [完整指南](./protocols-usage.md#qa-能否支持我的特定渠道如-slack)。

**Q: UNP/INP 版本如何升级？**
A: 检查 `protocols/INDEX.md` 查看最新版本。breaking changes 会在主版本号中标记。

---

## 资源链接

| 资源 | 链接 |
|:---|:---|
| **完整使用指南** | [protocols-usage.md](./protocols-usage.md) |
| **UNP 规范** | [protocols/unp.md](../../protocols/unp.md) |
| **INP 规范** | [protocols/inp.md](../../protocols/inp.md) |
| **协议注册表** | [protocols/INDEX.md](../../protocols/INDEX.md) |
| **GitHub** | [ai-cortex/protocols](https://github.com/nesnilnehc/ai-cortex/tree/main/protocols) |

---

**最后更新**：2026-03-25
**相关技能**：`review-notifications`（计划中）

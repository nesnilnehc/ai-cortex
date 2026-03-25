---
artifact_type: guide
created_at: 2026-03-25
status: active
lifecycle: living
---

# 协议使用指南 (Protocols Usage Guide)

本指南说明如何在项目中发现、安装和使用 AI Cortex 提供的领域协议规范。

---

## 1. 协议是什么？

**定义**：协议是对特定问题域（如通知系统）的标准化接口规范。

**特征**：
- **版本化**：明确的语义版本号（1.0.0 等）
- **分层**：通常包含多层（如 UNP 的语义层 + INP 的投递层）
- **标准化**：定义强制要求（MUST）、禁止项（FORBIDDEN）、最佳实践
- **可重用**：跨多个项目和团队适用

**与其他资产的区别**：

| 资产类型 | 用途 | 加载方式 |
|:---|:---|:---|
| **Skill（技能）** | 主动能力（调用来完成任务） | 按需注入 |
| **Protocol（协议）** | 接口契约（遵循来确保兼容性） | 常驻加载（长期背景） |
| **Rule（规则）** | 行为约束（工作时的约束） | 常驻加载（长期背景） |

---

## 2. 发现协议

### 2.1 在线浏览

1. **查看协议注册表**：访问 [`protocols/INDEX.md`](../../protocols/INDEX.md)
2. **确认当前可用的协议**：
   - UNP（Universal Notification Protocol）v1.0.0
   - INP（IM Notification Protocol）v1.0.0

3. **查看协议详情**：
   - [`protocols/unp.md`](../../protocols/unp.md) — 语义层规范
   - [`protocols/inp.md`](../../protocols/inp.md) — 投递层规范

### 2.2 在代码中查找

如果已安装 AI Cortex 技能：

```bash
# 全局查找协议目录
ls ~/.agents/protocols/
# 或本地项目
ls ./protocols/
```

### 2.3 通过 Manifest 发现

```bash
# 查看协议注册表配置
cat manifest.json | jq '.registry | {protocols_root, protocols_index}'
```

---

## 3. 安装 & 使用

### 3.1 作为 AI Cortex 技能的一部分安装

协议随 AI Cortex 技能包一起分发：

```bash
# 全局安装 AI Cortex（包含所有协议）
npx skills add nesnilnehc/ai-cortex -g

# 仅安装到项目本地
npx skills add nesnilnehc/ai-cortex
```

**验证安装**：

```bash
# 检查协议是否可用
cat ~/.agents/.skill-lock.json | grep ai-cortex
# 验证协议文件
ls ~/.agents/protocols/
```

### 3.2 在你的项目中使用

#### **方式 1：复制协议文件**（独立项目）

如果你不需要完整的 AI Cortex 技能包，只想要协议：

```bash
# 复制协议目录到你的项目
cp -r https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/ ./protocols/

# 或手动下载单个协议
curl https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/unp.md > ./protocols/unp.md
curl https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/inp.md > ./protocols/inp.md
```

#### **方式 2：作为 npm 依赖**（即将支持）

```bash
npm install @ai-cortex/protocols
```

（目前此包尚未发布，计划在 v2.1.0 时推出）

#### **方式 3：通过 Git Submodule**（团队共享）

```bash
# 将 protocols 作为 submodule 引入
git submodule add https://github.com/nesnilnehc/ai-cortex.git vendor/ai-cortex
git config submodule.vendor/ai-cortex.sparse-checkout protocols/
git submodule update --init --recursive

# 项目中引用
cat vendor/ai-cortex/protocols/unp.md
```

---

## 4. 使用场景和示例

### 4.1 通知系统设计（UNP 使用）

**场景**：设计新的通知系统

**步骤**：

1. **阅读 UNP 规范**：理解必填字段和约束

```markdown
# 根据 UNP，所有通知必须包含：
- id (uuid)
- type (UPPER_SNAKE_CASE)
- intent (info | action_required | approval | alert)
- priority (P0 | P1 | P2 | P3)
- title, body
- 如果 priority ∈ [P0, P1]，必须包含 actions
```

2. **实现 UNP 对象**：

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

3. **验证合规性**：使用 `review-notifications` 技能（计划中）

```bash
# 运行审查
claude-code /review-notifications
# 输入：notification code
# 输出：UNP 合规性报告
```

### 4.2 IM 投递实现（INP 使用）

**场景**：将 UNP 通知投递到 Feishu/WeCom

**步骤**：

1. **阅读 INP 规范**：理解渲染和路由规则

```markdown
# 根据 INP：
- P0 → card（交互式卡片）
- P1 → card
- P2 → markdown
- P3 → text（纯文本）
# P0/P1 必须包含 mention_user 和 actionable 内容
```

2. **实现投递层**：

```python
def deliver_notification(unp: UNPNotification, channel: str) -> str:
    """Transform UNP to channel-specific format"""

    # 步骤 1：根据优先级映射渲染格式
    format_map = {'P0': 'card', 'P1': 'card', 'P2': 'markdown', 'P3': 'text'}
    render_format = format_map[unp.priority]

    # 步骤 2：根据 INP 规则构建消息
    message = {
        'header': {
            'priority': unp.priority,
            'emoji': get_emoji_for_intent(unp.intent)
        },
        'body': unp.body[:500],  # INP: max_length = 500
        'format': render_format
    }

    # 步骤 3：注入提及（如果需要）
    if unp.priority in ['P0', 'P1']:
        message['mentions'] = get_mentions_for_priority(unp.priority)

    # 步骤 4：应用去重和限流
    if not is_duplicate(unp.id) and not is_throttled(unp.source, unp.priority):
        send_to_channel(channel, message)

    return message
```

3. **测试 INP 合规性**：

```bash
# 验证：
✓ P0/P1 消息包含 actions
✓ 没有原始 JSON 输出
✓ 应用了去重和限流
✓ 渠道功能降级（如 WeCom 不支持 card，降为 markdown）
```

### 4.3 跨项目共享

**场景**：多个项目都需要遵循同一个通知协议

**方案**：

1. **在公共位置维护协议**：
```
my-org/
├── protocols/          # 组织级协议库
│   ├── notification-protocol.md
│   └── logging-protocol.md
└── projects/
    ├── service-a/
    ├── service-b/
```

2. **在每个项目中引用**：

```yaml
# service-a/.protocol-config.yaml
protocols:
  - name: notification
    url: ../../../protocols/notification-protocol.md
    version: "1.0.0"
```

3. **验证合规性**：

```bash
# 在 CI/CD 中
protocols-validate --config .protocol-config.yaml
```

---

## 5. 与 AI Agent 集成

### 5.1 在 Claude Code 中使用协议

将协议文件作为**长期背景上下文**注入：

```bash
# 方法 1：通过 .claude/config.yaml
echo "
protocols:
  - ./protocols/unp.md
  - ./protocols/inp.md
" >> .claude/config.yaml

# 方法 2：通过 AGENTS.md（AI Cortex 入口）
# 在 AGENTS.md 中声明协议依赖
# 见 docs/guides/discovery-and-loading.md
```

### 5.2 示例：AI 驱动的通知重构

```
用户：将我的通知代码重构为遵循 UNP 协议
↓
Claude 加载：unp.md 作为系统上下文
↓
Claude 分析：现有通知代码与 UNP 的差异
↓
Claude 建议：
  1. 替换 send("message") 为 UNP 对象
  2. 添加 type（UPPER_SNAKE_CASE）
  3. 为 P0/P1 添加 actions
  4. 应用去重和限流
↓
Claude 实现：自动化重构
↓
验证：运行 review-notifications 技能检查合规性
```

---

## 6. 版本管理和更新

### 6.1 检查协议版本

```bash
# 查看当前版本
grep "^version:" protocols/unp.md

# 查看变更日志
grep -A 10 "版本" protocols/INDEX.md
```

### 6.2 升级协议

```bash
# 获取最新版本
git pull origin main

# 或从 GitHub 下载最新
curl -O https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/unp.md

# 检查 breaking changes
git diff protocols/unp.md
```

### 6.3 协议的向后兼容性

- **Minor updates**（1.0.0 → 1.1.0）：新增可选字段，向后兼容
- **Major updates**（1.0.0 → 2.0.0）：可能有 breaking changes，需要迁移计划

---

## 7. 常见问题 (FAQ)

### Q: 我需要遵循协议吗？

**A**：取决于你的用例。

- ✅ **应该遵循**：
  - 你的项目是 AI Cortex 技能的一部分
  - 你需要跨项目共享通知接口
  - 你想要标准化和可预测的行为

- ❌ **可以不遵循**：
  - 完全独立的项目，无协作需求
  - 协议规范不适用你的场景

### Q: UNP 和 INP 的区别是什么？

**A**：

| UNP | INP |
|:---|:---|
| **语义层** | **投递层** |
| 定义 WHAT（通知的结构和含义） | 定义 HOW（如何渲染和投递） |
| Channel-agnostic | Channel-specific（Feishu、WeCom） |
| 业务/应用层制造 | 投递/中间件层消费 |
| 示例：BUILD_FAILED 事件 | 示例：Feishu 卡片、WeCom 文本 |

### Q: 如果协议与我的需求不符怎么办？

**A**：两个选择：

1. **贡献改进**（推荐）：向 AI Cortex 提 issue 或 PR
2. **创建扩展**：在 `extensions` 字段中添加自定义数据

```javascript
{
  // UNP 标准字段
  type: "BUILD_FAILED",
  priority: "P1",
  // 自定义扩展
  extensions: {
    "my-org:build-system": {
      failureCode: "E_TIMEOUT",
      retryable: true
    }
  }
}
```

### Q: 能否支持我的特定渠道（如 Slack）？

**A**：可以。

1. **遵循 UNP**：确保你的通知是有效的 UNP 对象
2. **扩展 INP**：为 Slack 添加投递规则

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

3. **贡献回 AI Cortex**：如果通用性强，考虑提交为官方扩展

---

## 8. 最佳实践

### ✅ 推荐做法

1. **使用完整的 UNP 对象**：不要简化或省略字段
2. **版本锁定**：在项目中明确指定协议版本
3. **定期审查**：每个季度检查是否有新的协议版本或改进
4. **文档化**：在项目 README 中说明使用的协议及版本
5. **测试合规性**：集成自动化验证（如 review-notifications）

### ❌ 避免做法

1. **混合协议版本**：不要在同一项目中使用不同的 UNP 版本
2. **绕过约束**：不要违反 MUST/FORBIDDEN 规则，除非有充分理由
3. **硬编码渠道**：将渠道逻辑放入业务层，违反了 UNP 的 channel-agnostic 原则
4. **忽视更新**：不要长期不更新协议版本

---

## 9. 参考资源

| 资源 | 链接 | 说明 |
|:---|:---|:---|
| **协议注册表** | [protocols/INDEX.md](../../protocols/INDEX.md) | 所有可用协议及版本 |
| **UNP 规范** | [protocols/unp.md](../../protocols/unp.md) | 通知语义层规范 |
| **INP 规范** | [protocols/inp.md](../../protocols/inp.md) | 通知投递层规范 |
| **发现与加载** | [docs/guides/discovery-and-loading.md](./discovery-and-loading.md) | AI Agent 如何发现资产 |
| **AI Cortex 入口** | [AGENTS.md](../../AGENTS.md) | 项目身份和权威来源 |

---

## 10. 获取帮助

### 报告问题

如果协议有缺陷或不清楚：

1. **提交 issue**：https://github.com/nesnilnehc/ai-cortex/issues
2. **标签**：`protocols`, `unp`, `inp`, `documentation`
3. **描述**：包含你的用例和期望行为

### 贡献改进

```bash
# Fork → 创建分支 → 提交 PR
git checkout -b feature/protocols-enhancement
# 修改 protocols/*.md
git commit -m "docs(protocols): ..."
git push origin feature/protocols-enhancement
# 创建 PR
```

---

**最后更新**：2026-03-25
**维护者**：AI Cortex Team
**相关技能**：`review-notifications`（计划中）

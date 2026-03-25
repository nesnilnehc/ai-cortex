---
artifact_type: guide
created_at: 2026-03-25
status: active
lifecycle: living
---

# Agent 驱动的协议使用 (Protocols for AI Agents)

本指南说明 AI Agent 和 Claude Code 如何**自动发现、加载和应用**协议规范。

---

## 核心理念

**用户不应该手动读协议文档** — Agent 应该自动完成这些工作：

1. **自动发现** — 通过 manifest.json 发现可用的协议
2. **自动注入** — 作为长期背景上下文加载到 Agent 工作会话中
3. **自动应用** — 在代码生成和审查中应用协议约束
4. **自动验证** — 通过 skill 验证生成的代码是否符合协议

---

## 1. 协议发现 (Automatic Discovery)

### 1.1 通过 Manifest 发现

Agent 在启动时应读取 `manifest.json` 来发现所有可用的协议：

```json
{
  "registry": {
    "protocols_root": "protocols/",
    "protocols_index": "protocols/INDEX.md",
    ...
  }
}
```

### 1.2 Agent 发现流程

```python
# 伪代码：Agent 启动时执行
def discover_protocols():
    manifest = load_json("manifest.json")
    protocols_dir = manifest["registry"]["protocols_root"]
    protocols_index = manifest["registry"]["protocols_index"]

    # 读取 INDEX.md 获取所有协议及其元数据
    index = parse_markdown(protocols_index)

    for protocol in index.protocols:
        protocol_file = f"{protocols_dir}/{protocol.file}"
        metadata = extract_frontmatter(protocol_file)

        # 根据上下文判断是否需要加载
        if is_relevant_to_current_task(protocol):
            load_protocol_as_context(protocol_file)
```

### 1.3 协议元数据 (Front-matter)

协议文件应包含可机器读取的元数据：

```yaml
---
id: UNP_SPEC_V1
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

**关键字段用途**：
- `id` — 全局唯一标识符（用于 Agent 引用）
- `scope` — Agent 判断是否相关的关键字
- `applies_to` — 指示在哪些阶段应用（设计、审查、实现）
- `domain` — 协议适用的问题域
- `related` — 相关协议的引用

---

## 2. 自动加载 (Automatic Injection)

### 2.1 加载触发器

Agent 应在以下情况自动加载相关协议：

```
触发器 1：用户提及"通知"相关词汇
  → 自动加载 UNP + INP

触发器 2：运行 skill 时
  → 读取 skill 的 frontmatter 中的 protocols 字段
  例：review-notifications 会自动加载 [UNP, INP]

触发器 3：项目配置指定
  → 从 .claude/config.yaml 或 CLAUDE.md 读取
  protocols:
    - protocols/unp.md
    - protocols/inp.md

触发器 4：上下文相关推断
  → 分析代码或 diff，检测是否涉及协议相关领域
```

### 2.2 加载方式

```yaml
# .claude/config.yaml（项目配置）
protocols:
  # 通知系统
  - file: ./protocols/unp.md
    domain: notifications
    inject_as: system_context
  - file: ./protocols/inp.md
    domain: notifications
    inject_as: system_context

# 或在 CLAUDE.md 中
# PROTOCOLS: ./protocols/unp.md, ./protocols/inp.md
```

### 2.3 Skill 级别的协议声明

Skill 应在 frontmatter 中声明依赖的协议：

```yaml
---
name: review-notifications
protocols:
  - id: UNP_SPEC_V1
    version: ">=1.0.0"
  - id: INP_SPEC_V1
    version: ">=1.0.0"
---
```

Agent 运行 skill 时，会自动加载声明的协议。

---

## 3. 自动应用 (Automatic Application)

### 3.1 代码生成阶段

当 Agent 生成涉及通知的代码时，应自动应用协议：

```
用户需求："生成通知系统，发送构建失败警告"

Agent 流程：
  1. 识别任务涉及 notifications 域
  2. 自动加载 UNP + INP
  3. 根据 UNP schema 生成通知对象结构
  4. 根据 INP 规则生成渲染逻辑
  5. 输出代码已符合协议
```

### 3.2 代码审查阶段

Agent 审查代码时应检查协议合规性：

```
运行 skill：/review-notifications

自动检查列表（来自协议）：
  ✓ 所有通知对象都有 id, type, intent, priority
  ✓ P0/P1 包含 actions
  ✓ type 使用 UPPER_SNAKE_CASE
  ✓ P0/P1 已应用去重和限流
  ✓ INP 渲染规则正确应用
  ✓ 没有直接的 send("message") 调用

返回：合规性报告（自动生成，无需人工输入）
```

### 3.3 从协议生成验证规则

```python
# Agent 可以从协议 frontmatter 自动解析验证规则
def extract_validation_rules(protocol_doc):
    """从协议文档中提取验证规则"""

    rules = []

    # 解析 "MUST"、"MUST NOT"、"FORBIDDEN" 等强制要求
    must_rules = extract_patterns(protocol_doc, r"MUST\s+(.+)")
    must_not_rules = extract_patterns(protocol_doc, r"MUST NOT\s+(.+)")
    forbidden_rules = extract_patterns(protocol_doc, r"FORBIDDEN:\s*(.+)")

    return {
        "mandatory": must_rules,
        "forbidden": must_not_rules + forbidden_rules
    }

# 在审查时应用
rules = extract_validation_rules(load_protocol("unp.md"))
violations = check_code_against_rules(code, rules)
```

---

## 4. Agent 工作流示例

### 4.1 通知系统设计工作流

```
用户: "设计一个通知系统，支持 Feishu 和 WeCom"

┌─ Agent 自动化流程 ──────────────────────────────────────┐
│                                                          │
│ 1. 识别任务                                              │
│    ↓ 关键词: "通知系统"、"Feishu"、"WeCom"              │
│                                                          │
│ 2. 自动加载协议                                          │
│    ↓ 加载: UNP_SPEC_V1 + INP_SPEC_V1                   │
│                                                          │
│ 3. 分析需求                                              │
│    ↓ 需要支持 2 个渠道，通知优先级从 P0 到 P3          │
│                                                          │
│ 4. 应用 UNP 规范                                         │
│    ↓ 设计通知对象 schema（UNP 兼容）                   │
│                                                          │
│ 5. 应用 INP 规范                                         │
│    ↓ 针对 Feishu/WeCom 的渲染和路由规则               │
│                                                          │
│ 6. 生成代码（自动合规）                                  │
│    ├─ notification.py （UNP 对象定义）                  │
│    ├─ feishu_adapter.py （Feishu INP 实现）            │
│    ├─ wecom_adapter.py  （WeCom INP 实现）             │
│    └─ router.py         （动态路由）                     │
│                                                          │
│ 7. 自动验证                                              │
│    ↓ 运行 /review-notifications                        │
│    ↓ 所有代码 ✅ 符合 UNP + INP                         │
│                                                          │
│ 8. 输出给用户                                            │
│    ↓ "系统已设计并实现，符合 UNP v1.0.0 + INP v1.0.0" │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### 4.2 代码审查工作流

```
用户: "审查这个通知代码"

┌─ Agent 自动化流程 ──────────────────────────────────────┐
│                                                          │
│ 1. 分析代码                                              │
│    ↓ 检测到: notification sending, Feishu API         │
│                                                          │
│ 2. 自动加载协议                                          │
│    ↓ 加载: UNP + INP（检测到相关性）                   │
│                                                          │
│ 3. 运行合规性检查                                        │
│    ├─ UNP 验证（10 项检查）                             │
│    ├─ INP 验证（8 项检查）                              │
│    └─ 架构检查（通知层分离）                             │
│                                                          │
│ 4. 生成报告                                              │
│    ├─ ✅ UNP 合规: 8/10                                │
│    ├─ ✅ INP 合规: 8/8                                 │
│    └─ ⚠️ 建议: 添加去重机制（INP §7）                 │
│                                                          │
│ 5. 生成修复建议                                          │
│    ↓ Agent 自动生成补丁代码                             │
│                                                          │
│ 6. 应用修复（可选自动应用）                              │
│    ↓ /automate-repair 整合修复                         │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 5. Skill 集成

### 5.1 review-notifications Skill

```yaml
# skills/review-notifications/SKILL.md (伪代码)

---
name: review-notifications
description: Review notification code for UNP/INP compliance
protocols:
  - id: UNP_SPEC_V1
    version: ">=1.0.0"
  - id: INP_SPEC_V1
    version: ">=1.0.0"
---

# 当此 skill 运行时：
# 1. Agent 自动加载 UNP + INP 作为上下文
# 2. Agent 使用协议中定义的规则进行审查
# 3. 返回合规性报告
```

### 5.2 apply-unp Skill（计划）

```yaml
# 协议驱动的代码重构
name: apply-unp
description: Refactor code to use UNP objects
protocols:
  - id: UNP_SPEC_V1
    version: ">=1.0.0"

# 运行此 skill 时：
# 用户: "将我的通知代码重构为使用 UNP"
# Agent 自动：
#   1. 加载 UNP 协议
#   2. 分析现有代码
#   3. 生成符合 UNP 的重构
#   4. 应用变更
```

---

## 6. 协议驱动的自动化 (Protocol-Driven Automation)

### 6.1 配置驱动的 Agent 行为

```yaml
# .claude/config.yaml
protocols:
  - file: ./protocols/unp.md
    applies_to: [code-generation, code-review]
    auto_apply: true
    auto_verify: true

  - file: ./protocols/inp.md
    applies_to: [implementation, testing]
    auto_apply: true

# 含义：
# - 代码生成时自动应用 UNP
# - 代码审查时自动验证 UNP
# - 失败时自动提示修复方案
```

### 6.2 CI/CD 集成

```yaml
# .github/workflows/protocols.yml
name: Protocol Compliance Check

on: [push, pull_request]

jobs:
  check-protocols:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      # 步骤 1：自动加载协议
      - name: Load protocols
        run: |
          agent-cli load-protocols --manifest manifest.json

      # 步骤 2：审查通知代码
      - name: Review notifications
        run: |
          agent-cli review --protocols unp,inp ./src/notifications

      # 步骤 3：报告合规性
      - name: Report compliance
        run: |
          agent-cli report --format json > compliance-report.json
```

---

## 7. Agent 与用户的交互模式

### 传统模式（不推荐）
```
用户: "我该怎么用这个通知协议?"
Agent: "请阅读 docs/guides/protocols-usage.md 第 4 节..."
用户: 😞 （需要手动理解）
```

### Agent 驱动模式（推荐）
```
用户: "生成一个通知系统"
Agent: ✅ 自动加载 UNP + INP
Agent: ✅ 生成合规代码
Agent: ✅ 返回符合协议的实现
用户: 😊 （开箱即用）
```

### 混合模式（最优）
```
用户: "我想更深入理解通知协议"
Agent:
  "你可以：
   1. 查看快速参考: docs/guides/protocols-quickstart.md
   2. 看完整指南: docs/guides/protocols-usage.md
   3. 我可以帮你审查或生成代码"
```

---

## 8. 实现清单（For Agent Builders）

- [ ] **发现机制** — 实现 manifest.json 中 protocols 的自动发现
- [ ] **元数据解析** — 从 frontmatter 提取协议元数据（scope, applies_to, domain）
- [ ] **上下文注入** — 在 Agent 启动或关键时刻加载相关协议
- [ ] **Skill 集成** — 在 skill frontmatter 中支持 protocols 声明
- [ ] **自动验证** — 实现从协议规则自动生成的检查函数
- [ ] **报告生成** — 生成机器可读的合规性报告（JSON/YAML）
- [ ] **代码生成** — 在代码生成时自动应用协议约束
- [ ] **修复建议** — 当违反协议时自动生成补丁代码

---

## 9. 未来方向

### 动态协议生成
```
长期愿景：Agent 可以根据项目需求动态生成协议
  例："我需要一个日志协议"
  Agent 生成 logging-protocol.md（基于模板 + 需求）
```

### 跨协议验证
```
长期愿景：自动验证多个协议之间的兼容性
  例：UNP + INP + 安全协议是否兼容？
```

### 协议版本管理
```
长期愿景：Agent 自动跟踪协议版本和迁移路径
  当 UNP 升级到 v2.0.0 时：
  Agent 自动：
    1. 检测代码中使用的版本
    2. 生成迁移计划
    3. 应用自动迁移（如果可能）
```

---

## 10. 与传统指南的关系

| 方面 | 传统指南 | Agent 指南 |
|:---|:---|:---|
| **目标受众** | 人类开发者 | AI Agent |
| **学习方式** | 阅读文档 | 自动加载和应用 |
| **验证方式** | 手动检查清单 | 自动验证 |
| **代码生成** | 用户手写 | Agent 自动生成 |
| **合规性** | 用户负责 | Agent 保证 |

**两者互补**：
- 用户 = docs/guides/protocols-usage.md（理解概念）
- Agent = docs/guides/protocols-agent-usage.md（自动执行）

---

**核心原则**：让 Agent 做繁重的工作，用户关注高层需求。

**最后更新**：2026-03-25

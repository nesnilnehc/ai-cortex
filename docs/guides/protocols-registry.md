---
artifact_type: guide
created_at: 2026-03-25
status: active
lifecycle: living
---

# 协议注册表和远程加载 (Protocol Registry & Remote Loading)

Agent 应该通过**协议注册表**发现和加载协议，而不是依赖本地文件。

---

## 核心原理

Agent **不应该**假设任何本地文件存在。取而代之：

```
Agent 工作流：
  1. 知道注册表位置（这是唯一的先验）
  2. 从注册表查询协议信息（包括远程 URL）
  3. 根据需要远程加载协议
  4. 可选：缓存到本地（但不依赖）
```

---

## 1. 协议发现入口

### 单一真实来源 (Single Source of Truth)

```
🔗 https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/manifest.json
    ↓
    包含所有协议的注册表信息
```

Agent 启动时只需要知道这个 URL。

### Manifest 中的协议定义

```json
{
  "project": "AI Cortex",
  "version": "2.0.0",

  "registry": {
    "protocols_catalog": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/INDEX.md"
  },

  "protocols": [
    {
      "id": "UNP_SPEC_V1",
      "name": "Universal Notification Protocol",
      "version": "1.0.0",
      "domain": "notifications",
      "canonical_url": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/unp.md",
      "repository": "https://github.com/nesnilnehc/ai-cortex",
      "path": "protocols/unp.md",
      "scope": "Applicable whenever designing or reviewing notification systems"
    },
    {
      "id": "INP_SPEC_V1",
      "name": "IM Notification Protocol",
      "version": "1.0.0",
      "domain": "notifications",
      "canonical_url": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/inp.md",
      "repository": "https://github.com/nesnilnehc/ai-cortex",
      "path": "protocols/inp.md",
      "scope": "Applicable when implementing notification rendering and routing for instant messaging channels"
    }
  ]
}
```

**关键字段**：
- `canonical_url` — 协议的权威 URL（Agent 加载的地址）
- `domain` — 协议适用的问题域
- `version` — 语义版本号
- `repository` — 源代码仓库

---

## 2. Agent 发现流程

### 步骤 1：获取协议目录

```python
# Agent 代码
manifest_url = "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/manifest.json"
manifest = fetch_json(manifest_url)

# 获取所有可用协议
protocols = manifest["protocols"]
```

### 步骤 2：根据任务域查询相关协议

```python
def find_relevant_protocols(task_description, protocols):
    """查找与任务相关的协议"""

    relevant = []

    # 方式 1：通过关键词匹配
    keywords = {
        "notification": ["UNP_SPEC_V1", "INP_SPEC_V1"],
        "logging": ["LOG_SPEC_V1"],  # 未来的协议
        "error": ["ERR_SPEC_V1"],    # 未来的协议
    }

    for keyword, protocol_ids in keywords.items():
        if keyword in task_description.lower():
            for pid in protocol_ids:
                relevant.append(find_by_id(protocols, pid))

    # 方式 2：通过 domain 标签
    for protocol in protocols:
        if any(domain in task_description for domain in protocol["domains"]):
            relevant.append(protocol)

    return relevant

# 使用
task = "我需要设计一个通知系统"
protocols = find_relevant_protocols(task, manifest["protocols"])
# 结果: [UNP_SPEC_V1, INP_SPEC_V1]
```

### 步骤 3：远程加载协议

```python
def load_protocol(protocol_metadata):
    """从远程 URL 加载协议"""

    url = protocol_metadata["canonical_url"]
    content = fetch_text(url)

    return {
        "id": protocol_metadata["id"],
        "version": protocol_metadata["version"],
        "content": content,
        "url": url
    }

# 使用
for protocol_meta in protocols:
    protocol = load_protocol(protocol_meta)
    inject_into_context(protocol)
```

---

## 3. 版本管理

### 版本策略

```
主版本（Breaking Changes）：
  UNP v1.0.0  →  UNP v2.0.0（不兼容）
  URL: .../v1/unp.md  →  .../v2/unp.md

次版本（新增功能）：
  UNP v1.0.0  →  UNP v1.1.0（兼容）
  URL: .../unp.md 保持不变（始终指向最新次版本）

修订版本（Bug 修复）：
  UNP v1.0.0  →  UNP v1.0.1
  URL 不变（自动获得修复）
```

### 指定特定版本

```json
// manifest.json
{
  "protocols": [
    {
      "id": "UNP_SPEC_V1",
      "version": "1.0.0",
      "canonical_url": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/unp.md",

      // 可选：指定特定版本的 URL
      "version_urls": {
        "1.0.0": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/v1.0.0/protocols/unp.md",
        "1.0.1": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/v1.0.1/protocols/unp.md",
        "1.1.0": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/v1.1.0/protocols/unp.md"
      }
    }
  ]
}
```

### Agent 选择版本

```python
def load_protocol_version(protocol_id, version="latest", manifest=None):
    """加载指定版本的协议"""

    protocol = find_by_id(manifest["protocols"], protocol_id)

    if version == "latest":
        url = protocol["canonical_url"]
    else:
        url = protocol["version_urls"][version]

    return fetch_text(url)
```

---

## 4. 协议注册格式

### 完整的协议注册条目

```yaml
# manifest.json protocols 数组中的每一项
{
  "id": "UNP_SPEC_V1",                    # 全局唯一 ID
  "name": "Universal Notification Protocol",
  "description": "Channel-agnostic semantic layer for notifications",

  # URL 信息
  "canonical_url": "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/protocols/unp.md",
  "repository": "https://github.com/nesnilnehc/ai-cortex",
  "repository_path": "protocols/unp.md",

  # 版本信息
  "version": "1.0.0",
  "status": "active",                    # active | deprecated | experimental
  "lifecycle": "living",                 # 是否持续维护

  # Agent 发现和加载
  "domain": "notifications",             # 问题域
  "scope": "Applicable whenever designing or reviewing notification systems",
  "applies_to": ["design", "code-review", "implementation"],

  # 关系
  "related": ["INP_SPEC_V1"],            # 相关协议

  # 元数据
  "author": "AI Cortex Team",
  "license": "MIT",
  "tags": ["semantic", "channel-agnostic", "notifications"]
}
```

---

## 5. 使用场景

### 场景 1：Agent 在新项目中首次工作

```
Agent 初始化：
  1. 已知注册表 URL
  2. 获取 manifest.json
  3. 解析协议列表
  4. 根据任务加载相关协议
  5. 立即可用，无需任何预先配置

用户视角：
  Agent: "我已加载 UNP v1.0.0 和 INP v1.0.0 协议"
  用户: "生成通知系统"
  Agent: ✅ 完成（使用远程加载的协议）
```

### 场景 2：Agent 跨越不同组织

```
Agent A 在公司 X 工作：
  manifest_url = "https://company-x.internal/ai-cortex/manifest.json"
  ↓ 加载 Company X 的协议

Agent B 在公司 Y 工作：
  manifest_url = "https://company-y.internal/ai-cortex/manifest.json"
  ↓ 加载 Company Y 的协议

Agent C 使用 AI Cortex：
  manifest_url = "https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/manifest.json"
  ↓ 加载官方 AI Cortex 协议
```

### 场景 3：Agent 协议版本升级

```
用户代码在 UNP v1.0.0 上运行：
  Agent 检测：当前代码使用 "UNP v1.0.0"
  manifest 发现：最新版本是 UNP v2.0.0

Agent 行为（可选）：
  1. 询问用户："UNP 有新版本，是否升级？"
  2. 如果同意，加载 v2.0.0 并生成迁移建议
  3. 保持向后兼容性（除非明确选择升级）
```

---

## 6. 实现要点

### 对于 Agent 框架

```python
class ProtocolRegistry:
    def __init__(self, manifest_url: str):
        self.manifest_url = manifest_url
        self.manifest = None
        self._cache = {}  # 可选：本地缓存

    def discover(self, domain: str = None) -> List[Protocol]:
        """发现协议"""
        if not self.manifest:
            self.manifest = fetch_json(self.manifest_url)

        protocols = self.manifest["protocols"]

        if domain:
            protocols = [p for p in protocols if p.get("domain") == domain]

        return protocols

    def load(self, protocol_id: str, version: str = "latest") -> str:
        """加载协议内容"""
        protocol = self._find_by_id(protocol_id)

        # 检查缓存
        cache_key = f"{protocol_id}:{version}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        # 远程加载
        if version == "latest":
            url = protocol["canonical_url"]
        else:
            url = protocol["version_urls"][version]

        content = fetch_text(url)
        self._cache[cache_key] = content  # 可选缓存

        return content

    def get_relevant_protocols(self, task_description: str):
        """根据任务描述获取相关协议"""
        # 关键词匹配或语义相似度匹配
        ...
```

### 对于项目

```yaml
# .claude/config.yaml
protocols:
  registry_url: https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/manifest.json

  # 可选：指定特定版本
  pinned_versions:
    UNP_SPEC_V1: "1.0.0"
    INP_SPEC_V1: "1.0.0"

  # 可选：本地缓存
  cache:
    enabled: true
    directory: ./.claude/protocol-cache
```

---

## 7. 协议发现的三种方式

### 方式 1：显式指定

```python
# Agent 显式加载协议
registry = ProtocolRegistry("https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/manifest.json")
unp = registry.load("UNP_SPEC_V1")
```

### 方式 2：任务自动推断

```python
# Agent 根据任务自动发现
task = "生成一个通知系统"
protocols = registry.get_relevant_protocols(task)
# 自动发现 → [UNP_SPEC_V1, INP_SPEC_V1]
```

### 方式 3：Skill 声明

```yaml
# skill frontmatter
---
name: review-notifications
protocols:
  - id: UNP_SPEC_V1
    version: ">=1.0.0"
  - id: INP_SPEC_V1
    version: ">=1.0.0"
---

# Skill 运行时：Agent 自动加载声明的协议
```

---

## 8. 与本地 Clone 的对比

| 方面 | 远程加载（推荐） | 本地 Clone（不推荐） |
|:---|:---|:---|
| **初始化** | ✅ 0 步（只需 URL） | ❌ 需要 clone/download |
| **无状态** | ✅ Agent 可在任何地方工作 | ❌ 依赖本地文件 |
| **版本控制** | ✅ 自动从 manifest 获取最新 | ❌ 需要手动更新 |
| **跨项目** | ✅ 可加载不同源的协议 | ❌ 只能用本地版本 |
| **磁盘空间** | ✅ 无需存储（可选缓存） | ❌ 占用本地空间 |
| **网络依赖** | ⚠️ 需要网络 | ✅ 离线可用（如果缓存） |

---

## 9. 最小化 Agent 集成

Agent 只需要知道**这一个 URL**：

```
https://raw.githubusercontent.com/nesnilnehc/ai-cortex/main/manifest.json
```

从这个 URL，Agent 可以：
- ✅ 发现所有可用协议
- ✅ 获取协议的规范 URL
- ✅ 加载任何版本的任何协议
- ✅ 了解协议的 domain 和 scope
- ✅ 找到相关协议

---

**设计原则**：

- Agent 应该是**无状态和无配置的**
- 协议应该是**可远程发现和加载的**
- 版本应该**明确且可追踪的**
- 唯一的先验知识应该是**一个注册表 URL**

**最后更新**：2026-03-25

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

> **数据契约**：定义跨独立 service / repo / team 共享的接口、数据形状、状态机、事件 payload 文档应如何组织

---

## 1. 定位与适用范围

凡满足以下任一条件的契约文件，适用本规范：

- 描述本仓库**对外提供**的接口、数据形状、状态机、事件 payload，被另一个独立演进的 repo / team / service 消费
- 描述本仓库**对外消费**的第三方接口（profile 文件），需追踪上游版本演化
- OpenAPI / JSON Schema / Protobuf / 事件 schema 等机器可读契约的伴随文档

**不适用**：仓库内部模块之间的接口（同一团队、同一发布周期），那是设计文档（`-design.md`）而不是契约。

---

## 2. 命名约定

跨团队契约通过**文件名后缀**显式标注类型，consumer `grep -- '-contract\.md$'` 可枚举本仓库所有对外承诺：

| 后缀 | 含义 | 示例 |
|---|---|---|
| `*-contract.md` | 跨团队接口/数据/生命周期契约（强制承诺） | `lifecycle-contract.md` |
| `*-design.md` | 内部设计意图（不对外承诺） | `lifecycle-design.md` |
| `*-guide.md` | 使用指南 / 集成手册 | `bff-integration-guide.md` |
| `*-schema.md` | 数据结构 schema 描述 | `patch-schema.md` |
| `*-profile.md` | 第三方接口的本地剖面 | `<upstream>-server-api-profile.md` |

强制要求：

- 跨团队消费的文件**必须**用 `-contract` 后缀
- 设计文件**禁止**用 `-contract` 后缀（即使写得很正式）

---

## 3. 目录布局

契约目录扁平化——文件名后缀已经标注了类型，再用 `contracts/` 子目录区分一遍是冗余。

```
✅ integrations/<x>/lifecycle-contract.md
   integrations/<x>/lifecycle-design.md          ← 同级

❌ integrations/<x>/contracts/lifecycle-contract.md
   integrations/<x>/lifecycle-design.md          ← 两层
```

**例外**：当一个集成域的契约数 ≥10 且来自异质来源（如多个上游产品的 `*-profile.md` 各自独立）时，可建子目录按来源分组（`upstream/zentao/`、`upstream/jira/`），但同一来源内部仍扁平。

---

## 4. Frontmatter 契约

跨团队契约文件除遵循各项目通用 frontmatter 字段外，必须额外含：

```yaml
contract_version: <SemVer>      # 必填；MAJOR.MINOR.PATCH
```

### 4.1 SemVer 语义

| 类型 | 触发条件 |
|---|---|
| **MAJOR** | 删字段 / 改 URL / 改状态机语义 / 改枚举值含义 |
| **MINOR** | 新增字段 / 新增端点 / 新增枚举值 / 行为兼容扩展 |
| **PATCH** | 文档修订 / 错误码补充 / 示例更新 |

---

## 5. 正文结构契约

跨团队契约文件必须含以下章节（顺序可调，名称可本地化）：

### 5.1 必备章节

| 章节 | 内容 |
|---|---|
| 契约范围 | 描述对外承诺的接口 / 数据形状 / 状态机 |
| 字段 / 接口定义 | 具体字段表、类型、枚举、必填性、示例 |
| CHANGELOG | 版本史；每次 `contract_version` bump 必留条目 |

### 5.2 CHANGELOG 条目结构

每条 CHANGELOG 必须含：

- 版本号 + 日期：`### 1.8.0 — 2026-05-09`
- 变更类型：`Added` / `Changed` / `Removed` / `BREAKING`
- 影响面：哪些字段 / 端点 / 行为受影响
- 向后兼容性说明：consumer 是否需要改代码
- 实现链接：引用的代码位置或 PR 链接

```markdown
### 1.8.0 — 2026-05-09

**Changed (BREAKING for un-shipped consumers)**: `chunkId` → `feedbackId`
- 影响：所有携带 chunkId 的 endpoints（GET /feedback、POST /feedback/ack）
- 兼容性：未发布的 consumer 必须改字段；已发布的 consumer 不受影响（旧 API 保留至 2.0.0）
- 实现：apps/server PR #2341
```

### 5.3 反例

- ❌ `1.5.0 — 完善文档`（无信息量）
- ❌ 改字段语义但 `contract_version` 没动，对方靠 git diff 才发现

### 5.4 不该出现的内容

跨团队契约文件**禁止**承载实施排期 / 待办 / 联调里程碑：

- ❌ `Phase A：对方团队 D+3 完成 X`
- ❌ `@xxx 团队待办`
- ❌ 跨团队联调甘特图

这些信息属于各方仓库的 `tasks.md` / `backlog.md`，不属于契约。

---

## 6. 协作模式

跨团队契约采取 **Provider 单向广播 + Consumer 自跟踪**：

- Provider 在自己的 contract 文件里维护 SemVer + CHANGELOG
- Consumer 各自决定何时升级，自有 backlog 跟踪实施进度
- 上游变更通过 CHANGELOG 通知；下游不订阅时，CI/PR 不会被对方进度阻塞

业界对位：Pact、OpenAPI 等的最小公约数。

**为什么不双向跟踪**：双向 todo 会把对方实施细节渗进自己的产品文档，contract 变成跨团队甘特图；一旦对方排期漂移，本仓库的契约文档要被动改写。

---

## 7. 跨 repo 引用约定

下游 repo 在自己的代码 / 文档里引用上游 contract 时，**必须引用 `contract_version`**：

- ✅ `实现 lifecycle-contract@1.0.0`，升级时改成 `@1.1.0`
- ❌ 按 `https://github.com/upstream/repo/blob/main/contracts/foo.md` 实现（main 会变）
- ❌ 参考 `commit abc1234` 的 contract（除非是冻结快照引用）

**为什么**：URL / commit 引用强耦合上游目录结构；版本号是承诺，不会因文件迁移、目录重构而失效（`lifecycle-contract@1.0.0` 始终指向同一份语义）。

---

## 8. 反模式

```markdown
<!-- ❌ contract 文档里写实施清单 -->
## §6 任务归档约定
- [ ] Phase A：对方团队实现 lifecycle UI（D+3）
- [ ] Phase B：联调 + 验收（D+5）
- [ ] @zhangsan 负责 Phase C
```

```yaml
# ❌ 改字段没动版本
contract_version: 1.5.0
# 实际把 chunkId 改成 feedbackId 了，CHANGELOG 没动
```

```text
❌ 命名歧义
docs/integration/foo-spec.md       # 是 spec 还是 contract？
docs/integration/foo-contract.md   # 跟上面是同一份？
```

```text
❌ 子目录冗余
docs/integrations/<x>/clarification/
  contracts/
    lifecycle-contract.md
    split-contract.md
  lifecycle-design.md
  split-design.md
```

```markdown
<!-- ❌ 强耦合 URL -->
按照 https://gitlab/repo/-/blob/main/api.md 实现接口。
```

---

## 9. 示例

参考 AgentFabric 项目（recloud-agentfabric）的 `docs/architecture/integrations/zentao/clarification/lifecycle-contract.md`：

- 头部 frontmatter 含 `contract_version: 1.0.0`
- 含 SemVer 表 + CHANGELOG（首条 `1.0.0 — 2026-05-09 Initial Release`）
- 同目录的 `lifecycle-design.md` 承担设计意图，不冒充契约
- 没有 `contracts/` 子目录，扁平布局
- 不跟踪禅道项目组的 Phase 排期，只单向广播版本变更

`contracts/CHANGELOG.md` 是 OpenAPI 契约（机器可读）的对应实践：`clarification-api.yaml` 1.7.0 → 1.8.0（BREAKING：chunkId → feedbackId）→ 1.9.0（Added：getBadges），每次 bump 都伴随完整的 Added / Changed / Removed 条目 + 实现链接 + 兼容性说明。

---

## 10. 与其他资产关系

- 各项目通用文档 frontmatter 字段（`artifact_type` / `created_by` / `lifecycle` / `created_at`）由项目自身的文档规范约束；本规范只追加契约类文档独有的 `contract_version` 与 CHANGELOG 要求
- 临时文档治理由各项目的文档工作流规则承接，与本规范正交
- **NATS 特化模板**：[nats-messaging.md](./nats-messaging.md) 继承本规范的通用骨架（命名后缀 / `contract_version` / CHANGELOG / 扁平布局 / 跨 repo 引用），并补足 NATS 特有的 subject 命名、headers 字段表、payload 约定与内嵌校验规则。具体生产 / 消费由配套 Skill 完成：[publish-nats-message](../skills/publish-nats-message/SKILL.md) / [consume-nats-message](../skills/consume-nats-message/SKILL.md)

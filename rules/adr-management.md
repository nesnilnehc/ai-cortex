---
artifact_type: rule
name: adr-management
version: 1.0.0
scope: docs/adr/ 下的所有 ADR 文档
status: active
---

# Rule: ADR 写作纪律（ADR Management）

## 适用范围 (Scope)

所有在 `docs/adr/` 下创建或维护 Architecture Decision Record 的行为。数据结构约束见 [specs/adr-modeling.md](../specs/adr-modeling.md)；本 rule 约束行为面（准入、状态执行、衰减、边界）。

---

## §1 ADR 准入门槛

写 ADR 前先做两问验证。**两问均答"是"才值得写 ADR**：

**Q1：这个决定的 why 在半年后还有人想查吗？**
（即：非显而易见、有历史价值、影响长期结构）

**Q2：这个 why 无法被 rule + commit message + PR description + README 替代吗？**
（即：仅靠运行时约束或提交记录无法充分解释决策背景）

### 两问均"是" → 写 ADR

### 任一"否" → 不写 ADR，用替代载体

| 场景 | 替代载体 |
|---|---|
| 为什么改这段代码 | commit message |
| 为什么这个 PR 这样做 | PR description |
| 代码规范约束 | `rules/*.md` |
| 文档迁移、目录重组 | commit + PR + README |
| 技术框架的使用指南 | `docs/guides/*.md` |

### 反例（不应写 ADR 的场景）

- 日常 bug fix 或小功能添加
- 文件重命名/目录迁移（过程 why 完全可被 commit + PR 覆盖）
- 规范性约束（应写 rule，而非记录"我们决定遵守规范"）
- 已有 ADR 的局部细化（追加到原 ADR 的后果/备注即可）

---

## §2 状态字段强制

### 唯一 status 源

`status` 字段**只在 frontmatter 里写一次**，使用 5 值枚举：
```
proposed | accepted | superseded | archived | rejected
```

### 严格禁止

- ❌ 正文中出现 `**状态**：Accepted`（或任何变体）行
- ❌ 正文中出现 `**Status**:`、`**状态**：`、`Status: Accepted` 等
- ❌ 使用旧枚举值：`draft` / `active` / `approved` / `已批准` / `live`
- ❌ 使用废弃字段 `implementation_status` / `decision_status`（若遗留，删除）

### 状态变更规则

| 目标状态 | 必填附加字段 |
|---|---|
| `superseded` | `superseded_by: NNNN-{slug}` |
| `archived` | `archived_at: YYYY-MM-DD` + `archived_reason: <原因>` |

---

## §3 衰减政策

ADR 应随决策生命周期演化，不可只增不减。

### 触发归档（→ archived）

满足**全部**条件时，将 status 改为 `archived`：

1. 创建日期距今 **≥ 12 个月**
2. 近 12 个月内**无文档引用**（`grep -r "NNNN-" docs/ skills/ rules/ specs/` 无命中）
3. 所描述的决策**已不再影响当前系统行为**

操作：

```diff
- status: accepted
+ status: archived
+ archived_at: YYYY-MM-DD
+ archived_reason: 决策已过期，相关机制已移除/替代
```

### 物理删除（git rm）

满足**全部**条件时，可执行 `git rm`：

1. `status: archived` 且 `archived_at` 距今 **≥ 6 个月**
2. 无任何文件引用该 ADR
3. **ADR 类型除外**：ADR 本身永不因衰减而物理删除（决策历史是组织记忆）

### 永久保留

以下 ADR 无论多旧，**永不物理删除**：

- `status: rejected`（被拒决策同样是决策历史）
- `status: superseded`（替代关系需保留以理解演化脉络）
- 任何被其他 ADR 的 `superseded_by` 字段引用的 ADR

---

## §4 rules 与 decisions 边界

`rules/` 目录与 `docs/adr/` 目录服务不同受众，不构建自动派生关系：

| 维度 | `rules/` | `docs/adr/` |
|---|---|---|
| 受众 | Claude agent（运行时加载） | 人类（历史查阅） |
| 时态 | 当前有效约束 | 时点决策快照 |
| 内容 | 行为规则（主动约束） | 决策记录（why + alternatives） |
| 更新 | 随规范演化持续修订 | 写入后不改（除 status 字段） |

**不构建**：rule 不自动生成 ADR；ADR 内容不自动同步到 rule。两者通过人工 cross-reference 建立可追溯性。

---

## 违规示例

```markdown
<!-- ❌ 正文双写 status -->
# ADR 0001：xxx

**状态**：Accepted
**日期**：2026-03-24
```

```yaml
# ❌ 使用旧枚举值
status: active
```

```yaml
# ❌ superseded 但缺 superseded_by
status: superseded
```

```yaml
# ❌ archived 但缺必填字段
status: archived
```

---

## 修正指南

1. **清理正文双写**：删除 H1 后的 `**状态**：` 行与 `**日期**：` 行（日期已在 frontmatter `created_at`）
2. **替换旧枚举值**：`active` → `accepted`；`draft` → `proposed`；`approved` → `accepted`
3. **补充条件字段**：`superseded` 加 `superseded_by`；`archived` 加 `archived_at` 与 `archived_reason`
4. **删除废弃字段**：grep `implementation_status\|decision_status` 后删除

---

## 相关指引

- **数据契约**：[specs/adr-modeling.md](../specs/adr-modeling.md)
- **制品规范**：[docs/ARTIFACT_NORMS.md](../docs/ARTIFACT_NORMS.md)
- **ADR 索引**：[docs/adr/README.md](../docs/adr/README.md)

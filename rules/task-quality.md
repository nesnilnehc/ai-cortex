---
artifact_type: rule
scope: 评审或自检任务列表文档时
status: active
---

# 任务质量规则

> 任务列表评审清单 + spec 合规检查。每条独立可验证。
>
> 适用于：声明遵循 [specs/task-modeling.md](../specs/task-modeling.md) 的任务列表文档。

---

## 评审清单

### 1. 字段完整性

- [ ] 每个任务含 6 个必填字段（id / title / depends_on / acceptance / owner_or_hint / status）
- [ ] 所有任务初始 status 为 `Todo`
- [ ] frontmatter 完整（artifact_type / lifecycle / created_at / parent）

### 2. 依赖图正确性

- [ ] 依赖图无环（DAG）
- [ ] 无依赖任务的 `depends_on` 字段填 `—`，不留空
- [ ] 跨文档依赖以路径前缀标注（如 `other-tasks.md#T3`）
- [ ] 不存在依赖于不存在 ID 的任务

### 3. 可执行性

- [ ] 每个任务粒度具体（一次专注会话可完成）
- [ ] 每个任务有受让人或 AI 执行 hint
- [ ] 任务标题含动词，避免模糊"实施 X"
- [ ] 验收标准可测试或可验证

### 4. 可追溯性

- [ ] frontmatter `parent` 指向上游 design
- [ ] 每个任务可追溯到设计的某节或某条验收标准
- [ ] 设计中每个组件至少有 1 个任务覆盖（无孤立组件）

---

## Spec 合规清单（specs/task-modeling.md）

- [ ] frontmatter `artifact_type: tasks`
- [ ] frontmatter `lifecycle: living`
- [ ] 每个任务 ID 格式 `T<n>` 唯一
- [ ] 每个任务的 status 在枚举内
- [ ] 派工时所有 status = `Todo`

---

## 反模式

- ❌ 循环依赖
- ❌ 模糊任务（"实施模块 X"）
- ❌ 无验收标准
- ❌ 派工时写入非 Todo 状态
- ❌ 无 `parent` frontmatter（孤立任务列表）
- ❌ 任务无设计引用

---
artifact_type: rule
name: functional-design-quality
version: 1.0.0
scope: 评审或自检功能设计文档时
recommended_scope: user
status: active
---

# Rule: 功能设计质量（Functional Design Quality）

> 5 维评审清单 + spec 合规检查。每条独立可验证。
>
> 适用于：声明遵循 [specs/functional-design-modeling.md](../specs/functional-design-modeling.md) 的功能设计文档。

---

## 5 维审查清单

### 1. 完整性（结构齐全吗？）

- [ ] 6 个必填节齐全（目标 / 功能模块与边界 / 业务流程 / 异常与边界场景 / 验收标准 / 权衡与开放问题）
- [ ] frontmatter 完整（artifact_type / lifecycle / created_at / parent / status）
- [ ] 业务流程含起点 / 终点 / 关键步骤 / 参与角色，并以流程图表达
- [ ] 异常与边界场景 ≥ 2 条，覆盖失败 / 撤回 / 超时 / 重复提交 / 并发中适用者

### 2. 可执行性（下游能直接派生技术设计吗？）

- [ ] 功能模块职责清晰，边界（做什么 / 不做什么）明确
- [ ] 业务流程分支显式，无歧义分叉
- [ ] 验收标准可验证
- [ ] 无澄清问题即可派生技术设计

### 3. 清晰性（无歧义吗？）

- [ ] 术语一致（首次出现含中英对照）
- [ ] 含至少一种结构化表达（流程图 / 状态图 / 权限矩阵）
- [ ] 不含架构 / 数据库 / API 等技术实现细节
- [ ] 业务规则用 `覆盖 R<n>` 引用上游需求，未在本文档重新声明

### 4. 合理性（设计成立吗？）

- [ ] 业务流程闭环（每条流程都有终态）
- [ ] 权衡分析含被拒方案的业务代价（非技术代价）
- [ ] 异常场景的预期行为是业务行为而非技术处理
- [ ] 范围与上游 requirement 一致

### 5. 可追溯性（能定位变更影响吗？）

- [ ] frontmatter `parent` 指向 `approved` 状态的上游 requirement
- [ ] 验收标准每条可追溯至 requirement 的某条 acceptance
- [ ] 引用的业务规则 id（`覆盖 R<n>`）在上游需求中存在
- [ ] 引用的外部规范有有效链接

---

## 条件必备项检查

- [ ] 业务对象有 ≥ 3 状态且转换由业务规则驱动时，已单列业务对象状态节（状态图 / 状态表，覆盖终态与异常态）
- [ ] 涉及 ≥ 2 角色或差异化菜单 / 操作 / 数据权限时，已单列角色与权限矩阵（行 = 角色，列 = 三类权限）

---

## Spec 合规清单（specs/functional-design-modeling.md）

- [ ] frontmatter 含全部必填字段
- [ ] `artifact_type: functional-design`
- [ ] `lifecycle: snapshot`
- [ ] `status` ∈ `draft` / `approved` / `superseded`
- [ ] 6 节必填全部存在
- [ ] 异常与边界场景 ≥ 2 条
- [ ] 验收标准 ≥ 3 条
- [ ] `superseded` 状态已填 `superseded_by`

---

## 反模式

- ❌ 含架构 / 数据库 / API 等技术实现细节
- ❌ 在本文档重新声明业务规则而非引用上游需求
- ❌ 满足升必填条件却缺状态图 / 权限矩阵
- ❌ 权衡分析混入技术选型取舍
- ❌ 无 `parent` frontmatter（孤立设计）

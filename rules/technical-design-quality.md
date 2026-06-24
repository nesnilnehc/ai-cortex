---
artifact_type: rule
name: technical-design-quality
version: 1.0.0
scope: 评审或自检技术设计文档时
recommended_scope: user
status: active
---

# Rule: 技术设计质量（Technical Design Quality）

> 5 维评审清单 + spec 合规检查。每条独立可验证。
>
> 适用于：声明遵循 [specs/technical-design-modeling.md](../specs/technical-design-modeling.md) 的技术设计文档。

---

## 5 维审查清单

### 1. 完整性（结构齐全吗？）

- [ ] 9 个必填节齐全（目标 / 架构与服务拆分 / 组件与详细设计 / 数据库设计 / 接口契约 / 数据流与错误处理 / 技术选型与权衡 / 测试策略 / 验收标准）
- [ ] frontmatter 完整（artifact_type / lifecycle / created_at / parent / status）
- [ ] 至少 2 种替代方案及权衡
- [ ] 至少 2 条技术失败路径与恢复策略

### 2. 可执行性（下游能直接拆任务吗？）

- [ ] 组件含签名级类 / 方法 / 接口定义，可独立实施
- [ ] 数据库设计含字段 / 类型 / 约束 / 关系，可据此建表
- [ ] 接口契约含路径 / 方法 / 入参 / 出参 / 错误码 / 鉴权，可据此对接
- [ ] 无澄清问题即可派生任务列表

### 3. 清晰性（无歧义吗？）

- [ ] 术语一致（首次出现含中英对照）
- [ ] 含至少一种结构化表达（图、表）
- [ ] 不含实现代码或脚手架
- [ ] 测试策略 = 验证方法（不是测试代码）
- [ ] §4 / §5 不涉及变更时写"无变更"而非留空

### 4. 合理性（设计成立吗？）

- [ ] 技术选型有明确理由（非"看起来好"）
- [ ] 权衡分析含弃用方案的具体缺点
- [ ] 错误处理覆盖主要技术失败路径
- [ ] 显式列出依赖与风险

### 5. 可追溯性（能定位变更影响吗？）

- [ ] frontmatter `parent` 的 artifact_type ∈ {functional-design, requirement}
- [ ] 验收标准每条追溯至上游 functional-design 的某条 acceptance；功能层被跳过时追溯至 requirement
- [ ] 关键决策可派生 ADR（或已存在 ADR 链接）
- [ ] 引用的外部规范有有效链接

---

## 条件必备项检查

- [ ] 涉及破坏性 schema 变更 / 数据回填 / 不可回滚操作时，已单列数据迁移详案（含回滚策略）

---

## Spec 合规清单（specs/technical-design-modeling.md）

- [ ] frontmatter 含全部必填字段
- [ ] `artifact_type: technical-design`
- [ ] `lifecycle: snapshot`
- [ ] `status` ∈ `draft` / `approved` / `superseded`
- [ ] 9 节必填全部存在
- [ ] 替代方案 ≥ 2 种
- [ ] 技术失败路径 ≥ 2 条
- [ ] 验收标准 ≥ 3 条
- [ ] `parent` 指向 `approved` 状态的上游设计
- [ ] `superseded` 状态已填 `superseded_by`

---

## 反模式

- ❌ 含代码或脚手架
- ❌ 含业务流程 / 角色权限 / 业务对象状态（归功能设计）
- ❌ 单一方案不做权衡
- ❌ §4 / §5 无变更时留空而非写"无变更"
- ❌ 测试策略写测试代码
- ❌ `parent` 的 artifact_type 不在 {functional-design, requirement}
- ❌ 无 `parent` frontmatter（孤立设计）

---

## 关联资产

- **图表选型**：[diagram-selection](./diagram-selection.md)——架构图 / 组件图 / 部署图等结构化表达的选型、跨工具选择与渲染避坑援引此判据

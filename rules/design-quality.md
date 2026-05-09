---
artifact_type: rule
scope: 评审或自检设计文档时
status: active
---

# 设计质量规则

> 5 维评审清单 + spec 合规检查。每条独立可验证。
>
> 适用于：声明遵循 [specs/design-modeling.md](../specs/design-modeling.md) 的设计文档。

---

## 5 维审查清单

### 1. 完整性（结构齐全吗？）

- [ ] 8 个必填节齐全（目标 / 架构 / 组件 / 数据流 / 错误处理 / 测试策略 / 权衡 / 验收标准）
- [ ] frontmatter 完整（artifact_type / lifecycle / created_at / parent / status）
- [ ] 至少 2 种替代方案及权衡
- [ ] 至少 2 条关键失败路径与恢复策略

### 2. 可执行性（下游能直接拆任务吗？）

- [ ] 组件职责清晰，每个组件可独立实施
- [ ] 数据流标注关键路径与错误路径
- [ ] 验收标准可量化或可验证
- [ ] 无澄清问题即可派生任务列表

### 3. 清晰性（无歧义吗？）

- [ ] 术语一致（首次出现含中英对照）
- [ ] 含至少一种结构化表达（图、表）
- [ ] 不含实现代码或脚手架
- [ ] 测试策略 = 验证方法（不是测试代码）

### 4. 合理性（设计成立吗？）

- [ ] 选定方案有明确理由（非"看起来好"）
- [ ] 权衡分析含弃用方案的具体缺点
- [ ] 错误处理覆盖主要失败路径
- [ ] 范围与上游 requirement 一致

### 5. 可追溯性（能定位变更影响吗？）

- [ ] frontmatter `parent` 指向上游 requirement
- [ ] 验收标准每条可追溯至 requirement 的某条
- [ ] 关键决策可派生 ADR（或已存在 ADR 链接）
- [ ] 引用的外部规范有有效链接

---

## Spec 合规清单（specs/design-modeling.md）

- [ ] frontmatter 含全部必填字段
- [ ] `artifact_type: design`
- [ ] `lifecycle: snapshot`
- [ ] `status` ∈ `draft` / `approved` / `superseded`
- [ ] 8 节必填全部存在
- [ ] 替代方案 ≥ 2 种
- [ ] 关键失败路径 ≥ 2 条
- [ ] 验收标准 ≥ 3 条

---

## 反模式

- ❌ 含代码或脚手架
- ❌ 单一方案不做权衡
- ❌ 测试策略写测试代码
- ❌ 无 `parent` frontmatter（孤立设计）

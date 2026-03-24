---
artifact_type: roadmap
created_by: define-roadmap
lifecycle: living
created_at: 2026-03-24
status: active
---

# 合并 define-milestones 至 define-roadmap

**状态**：已批准  
**日期**：2026-03-22  
**范围**：技能合并；战略规划链简化。

---

## 1. 问题

当前项目管理将「里程碑」视为 roadmap 的节点（见 [20260322-strategic-goals-milestones-framing](20260322-strategic-goals-milestones-framing.md) 层次表）。`define-milestones` 与 `define-roadmap` 存在顺序依赖（目标 → 里程碑 → 路线图），二者产出在概念上可统一为「由里程碑节点组成的路线图」。

需评估是否合并两个技能以简化战略规划链。

---

## 2. 设计决策

### 2.1 合并为单一技能 define-roadmap

**定位**：里程碑 = 路线图的节点；路线图 = 有序的里程碑集合。一个技能即可从战略目标推导路线图（含里程碑节点），无需先产出里程碑再产出路线图。

**变更**：

- 将 `define-milestones` 的能力合并至 `define-roadmap`
- `define-roadmap` 输入：战略目标（不再强制要求已有里程碑）
- `define-roadmap` 输出：路线图文档，每个节点为里程碑（名称、范围、成功标准、目标映射）；支持 `roadmap.md` 或 `milestones.md` 路径（依项目规范）
- `define-milestones` 已移除，路由至 `define-roadmap`

### 2.2 产出路径

- **默认**：`docs/process-management/roadmap.md`
- **项目规范**：若项目惯用 `milestones.md`，可沿用；技能支持 `path_alt`

### 2.3 触发器保留

`define-roadmap` 保留原 `define-milestones` 的 triggers（`define milestones`、`milestones`、`phase checkpoints`），确保既有调用方式仍可路由至该技能。

---

## 3. 参考

- [20260322-strategic-goals-milestones-framing](20260322-strategic-goals-milestones-framing.md)
- [define-roadmap](../../../skills/define-roadmap/SKILL.md)

---
name: clean-project
version: 1.0.0
recommended_scope: project
---

# Command: /clean-project

## 触发意图 (Intent)

用户希望自动分析当前项目并对文件系统执行必要的结构化清理，不产出分析报告或文档，仅通过实际变更（如 diff）呈现结果。

## 映射技能 (Mapped Skills)

- [clean-project](../skills/clean-project/SKILL.md)

## 参数化指令 (Params)

- 格式：`/clean-project`
- 无参数；工作区根为当前项目根。

## 交互反馈 (UX)

执行技能前可提示：「正在按 AI Cortex 清理项目技能执行，仅对文件系统做变更，不输出分析报告…」；执行后仅展示 Apply Changes（diff）或「No changes required。」

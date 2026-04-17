# 设计战略目标

定义 3–5 个长期战略目标，推动项目朝着愿景和北极星方向发展。

## 用途

产出战略目标文档，包含 3–5 个与愿景和北极星一致、以结果为导向的目标。**长期项目（计划期 > 6 个月）必须包含一个"工程 / 治理健康"类目标**，为治理 / 技术债 / 文档类工作提供战略代言（依据 ADR 20260417-unified-value-driven-prioritization-model）。本技能不定义使命、愿景、北极星或里程碑。默认输出到 `docs/project-overview/strategic-goals.md`（或按项目规范路径）。

## 何时使用

- 在愿景和北极星之后，设定 3–5 个结果型目标以推进 NSM。
- 用于年度或季度战略更新，明确阶段内的核心结果。
- 适用于战略链路：使命 → 愿景 → 北极星 → 支柱 → 目标。

## 输入

- 愿景、北极星（或对应文档路径）、项目背景
- 可选：使命、时间范围、现有目标或优先事项

## 输出

- 战略目标文档（默认 `docs/project-overview/strategic-goals.md`）
- 内容包含 3–5 个目标（标题 + 描述），可选补充“如何支持愿景/NSM”

## 安装

```bash
npx skills add nesnilnehc/ai-cortex --skill design-strategic-goals
```

## 相关技能

- `define-mission`：定义项目存在意义
- `define-vision`：定义长期未来状态
- `define-north-star`：定义单一核心指标，目标应驱动其改进
- `define-milestones`：将目标拆解为阶段性检查点
- `align-planning`：将目标作为规划对齐锚点

## 完整定义

请参阅 [SKILL.md](./SKILL.md) 了解行为、限制和示例。

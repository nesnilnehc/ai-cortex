# 定义战略支柱

从愿景与北极星衍生 3–5 个战略支柱（高层主题），用于组织后续战略目标与路线图。

## 用途

产出战略支柱文档，包含 3–5 个与愿景和北极星一致的主题。后续目标与路线图可按支柱进行分组。本技能不定义使命、愿景、北极星、目标、里程碑或路线图。默认输出到 `docs/project-overview/strategic-pillars.md`（或按项目规范路径）。

## 何时使用

- 在愿景和北极星之后，先建立稳定主题，再组织目标和路线图。
- 需要战略结构层时，使用支柱统一归类不同目标与行动方向。
- 适用于战略链路：使命 → 愿景 → 北极星 → 支柱 → 目标 → 里程碑 → 路线图。

## 输入

- 愿景、北极星（或对应文档路径）、项目背景
- 可选：使命、现有目标、现有支柱草案

## 输出

- 战略支柱文档（默认 `docs/project-overview/strategic-pillars.md`）
- 内容包含 3–5 个支柱（名称 + 描述），可选说明其与愿景/NSM 的关系

## 安装

```bash
npx skills add nesnilnehc/ai-cortex --skill define-strategic-pillars
```

## 相关技能

- `define-vision`、`define-north-star`：上游输入来源
- `design-strategic-goals`：下游可将目标映射到支柱
- `define-roadmap`：下游可按支柱组织路线图主题

## 完整定义

请参阅 [SKILL.md](./SKILL.md) 了解行为、限制和示例。

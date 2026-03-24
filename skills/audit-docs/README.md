# 文档审计

完整的文档治理审计一键完成。

## 用途

自动化文档治理的完整流程：建立规范 → 整理仓库 → 评估文档 → 生成统一报告。

## 何时使用

- **新项目启动**：建立文档规范和结构基础
- **项目入职**：新成员快速了解文档状态
- **PR 审查**：检查代码变更是否有对应文档更新
- **发版前**：完整的治理健康检查
- **定期维护**：月度或周期性文档质量追踪

## 输入

- 项目路径（默认：当前工作目录）
- 运行模式（full | quick | code-review）
- 可选：代码基准分支（用于 code-review 模式）

## 输出

- `docs/calibration/docs-governance.md`：统一治理报告（含健康评分和优先级行动计划）
- 可选：`docs/ARTIFACT_NORMS.md`（如需建立规范）

## 工作流整合

此技能编排三个核心技能：

```
discover-docs-norms    (建立/验证规范)
         ↓
    tidy-repo          (基于规范整理结构)
         ↓
    assess-docs        (完整的健康评估)
         ↓
  docs-governance      (统一报告 + 综合评分)
```

## 使用示例

```bash
# 完整流程（推导规范、整理、评估）
docs-governance --mode full

# 快速评估（仅评估，无推导）
docs-governance --mode quick

# PR 检查（评估 + 代码对齐）
docs-governance --mode code-review --code-diff origin/main
```

## 相关技能

- `discover-docs-norms`：建立/推导项目文档规范
- `tidy-repo`：基于规范整理仓库结构
- `assess-docs`：评估文档合规性和准备度
- `bootstrap-docs`：初始化文档结构

## 许可证

MIT

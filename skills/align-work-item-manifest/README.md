# 对齐工作项清单

**状态**：实验性（v1.0.0）

## 用途

当项目使用**中央清单文件**（如 `docs/process-management/now/<slug>.md`）登记制品时，检测清单文件与物理制品之间的漂移。v1.0.0 **advisory-only**——只报告，不自动修复。

## 何时使用

- 中央清单风格项目定期健康检查
- `plan-next` 报告 G3 漂移且检测到清单文件时的深入诊断
- 从无清单迁移到中央清单风格后的初次对齐盘点
- 迭代收尾 / 发布前清单完整性检查

## 前提

- 项目存在至少一个清单文件（默认 glob `docs/process-management/now/*.md`，可由 ARTIFACT_NORMS.md 覆盖）
- 本技能通过 glob 检测清单文件的**物理存在性**——不依赖任何 `linking_mode` 字段声明

## 输入

- 项目路径（默认 CWD）
- 可选 manifest glob 模式（默认从 `ARTIFACT_NORMS.md` 读取）
- 可选 `artifact_norms_path`

## 输出

- `docs/calibration/work-item-manifest-alignment.md`（或规范声明的路径）
- 机器可读漂移摘要（YAML fence）供 `plan-next` 作 G3 真相漂移源消费

## 三类漂移

- **悬挂引用**：清单列了但物理文件不存在
- **未登记**：物理文件存在但清单未列出
- **命名不符**：同 slug 但清单声明路径与物理路径不一致

## 硬边界

- **只读**：不自动写清单 / 不创建 / 不删除 / 不移动任何文件
- 非 manifest 模式项目自动停止并诊断说明
- 自动维护机制是未来 v2.x 话题

## 与兄弟技能的关系

- 依赖 `discover-docs-norms` / `define-docs-norms` 的产出（`linking_mode` 字段）
- 输出被 `plan-next` 消费为 G3 漂移
- 实际文件归档 / 重命名交给 `tidy-repo`
- 规划层漂移修正交给 `align-planning`

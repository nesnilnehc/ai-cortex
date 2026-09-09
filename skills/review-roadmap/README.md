# 审查路线图（Review Roadmap）

按 `rules/roadmap-quality.md` 评估既有路线图文档，产出 findings 列表。只评估，不改写。

## 用途

从五个维度审查路线图质量：完整性（核心模型四件套、容量基线与分配）、可执行性（分母是否存在、WIP 上限、目标归属）、清晰性（指标三元组、结果句式与假设句式）、合理性（结果导向、依赖已映射、变更频率）、可追溯性（目标映射、明确不做清单）。**判据不内嵌在技能里**，全部引自 rule——判据变更改那份 rule，不改技能。

## 何时使用

- **晋升前把关**：容量与依赖判据不过关时，晋升算不出正确结果
- **接手他人路线图**：快速看清这份路线图缺什么
- **定期体检**：路线图是 living 文档，随时间会漂
- **编排链路入口**：作为 `orchestrate-roadmap-planning` 的第 0 步

## 输入

- 既有路线图文档（路径或内容）
- [rules/roadmap-quality.md](../../rules/roadmap-quality.md)（缺失时 halt）
- 佐证源：`docs/project-overview/strategic-goals.md` 与 Now 层引用的 backlog 条目

## 输出

- findings 列表（location / category / severity / title / description / suggestion）
- 无法评估维度的显式说明及原因
- 零 findings 时明确说明通过全部判据

## 边界

不生成也不改写路线图——结构性缺口交接 `define-roadmap`，状态与时点类缺口交接 `update-roadmap`。**不输出编排 mode**：上下文检测是编排层自己的职责。

## 安装

统一由 AI Cortex 的 canonical 安装管理，见仓库根 [README](../../README.md#-安装与使用)。

## 相关技能

- `define-roadmap` —— 下游交接：结构性 findings 由它修复
- `update-roadmap` —— 下游交接：状态与时点类 findings 由它修复
- `review-requirements` —— 同族：同为「评估既有治理文档」的原子技能，共用 IO 契约
- `orchestrate-roadmap-planning` —— 编排方：作为第 0 步提供条件判定依据

## 完整定义

参见 [SKILL.md](./SKILL.md)。

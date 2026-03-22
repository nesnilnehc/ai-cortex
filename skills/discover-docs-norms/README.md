# 发现文档规范

通过对话和扫描帮助用户建立项目特定的产品规范（路径、命名、生命周期）。

## 用途

该技能扫描项目“docs/”结构，通过对话确认路径，并生成“docs/ARTIFACT_NORMS.md”和可选的“.ai-cortex/artifact-norms.yaml”。其他文档生成技能（捕获工作项、设计解决方案、评估文档）会阅读这些规范来调整输出路径。

## 何时使用

- 没有产品规范的新项目
- 具有需要形式化的自定义文档结构的现有项目
- 迁移到 AI Cortex 默认值或项目文档模板

## 输入

- 项目路径（默认：工作空间根目录）
- 可选：起点（ai-cortex | 模板 | 空白）

## 输出

- `docs/ARTIFACT_NORMS.md`：人类可读的产品规范表
- `.ai-cortex/artifact-norms.yaml`（可选）：机器可读模式

## 相关技能

- `bootstrap-docs`：完整的文档引导； discovery-docs-norms 仅关注规范
- `assess-docs`：评估文档准备情况； discovery-docs-norms 定义规范
- `assess-docs`：根据规范验证文档并评估准备情况（合规性是其报告的一部分）

## 安装


```bash
npx skills add nesnilnehc/ai-cortex --skill discover-docs-norms
```


## 许可证

麻省理工学院
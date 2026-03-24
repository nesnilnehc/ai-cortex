# 发现文档规范

通过对话和扫描帮助用户建立项目特定的产品规范（路径、命名、生命周期）。

## 用途

该技能扫描项目”docs/”结构，自动推导文档规范，通过对话确认，然后生成”docs/ARTIFACT_NORMS.md”（人类可读 + 机器可解析）。其他文档技能（assess-docs、tidy-repo）从此规范文件读取约定来应用验证和整理。

## 何时使用

- **新项目**：建立初始文档规范
- **现有项目**：自动推导并形式化现有的文档约定
- **规范更新**：当项目文档结构演进时，重新扫描和更新规范
- **多项目对齐**：跨多个项目建立一致的规范

## 输入

- 项目路径（默认：当前工作目录）

## 输出

**单一规范文件**：
- `docs/ARTIFACT_NORMS.md`：项目规范文档
  - 路径约定表（artifact_type → path_pattern）
  - 命名约定（大小写、日期格式）
  - Front-matter 标准（必需字段、推荐字段）
  - 验证规则（命名、路径、front-matter 检查）
  - 整体置信度评分

## 工作流集成

这个技能是文档治理流程的**第一步**：

```
discover-docs-norms          (建立规范)
         ↓
    tidy-repo                 (基于规范整理结构)
         ↓
    assess-docs               (基于规范诊断问题)
         ↓
  docs-governance             (自动化的完整流程编排)
```

**协作工具**：
- `tidy-repo`：从 docs/ARTIFACT_NORMS.md 读取规范来整理文件位置和命名
- `assess-docs`：从 docs/ARTIFACT_NORMS.md 读取规范来验证合规性
- `audit-docs`：使用规范来执行完整的治理审计

## 安装


```bash
npx skills add nesnilnehc/ai-cortex --skill discover-docs-norms
```


## 许可证

麻省理工学院
# 制品规范 Schema

**状态**：Informational  
**版本**：3.0.0  
**范围**：项目级制品路径与命名配置 + 占位符语法

**变更记录**：

- **v3.0.0 (2026-04-25)**：彻底删除 linking_mode 字段与相关段落（ADR 006）；`path_pattern` 覆盖 + 占位符语法是项目定制的唯一机制。artifact-contract v5.0 配套发布，canonical 路径统一为 `docs/<type>/{slug}.md`。
- v1.2.0 (2026-04-24)：`path_pattern` 从硬规则降级为默认值；新增占位符语法。
- v1.0.0：初版。

---

## 1. 目的

项目可定义自己的制品规范以覆盖默认 [specs/artifact-contract.md](artifact-contract.md)。产出文档制品的技能优先读取项目规范；若不存在则回退到契约。

---

## 2. 解析顺序

技能按下列顺序检查：

1. 调用方 frontmatter `artifact_norms_path`（运行时覆盖）
2. `.ai-cortex/artifact-norms.yaml`（机器可读，自动化优先）
3. `docs/ARTIFACT_NORMS.md`（人工可读）
4. 若都不存在：使用 [specs/artifact-contract.md](artifact-contract.md) §2 canonical 默认

---

## 3. docs/ARTIFACT_NORMS.md 格式

最小结构（Markdown）：

```markdown
# Artifact Norms

**Source**: Custom | AI Cortex default | project-documentation-template

## Artifact Types

| artifact_type | path_pattern | lifecycle |
| :--- | :--- | :--- |
| requirements | docs/requirements/{slug}.md | snapshot |
| design | docs/designs/{slug}.md | snapshot |
| tasks | docs/tasks/{slug}.md | living |
| backlog-item | docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md | living |
| adr | docs/process-management/decisions/YYYYMMDD-{slug}.md | living |
| doc-assessment | docs/calibration/doc-assessment.md | snapshot |
```

---

## 4. .ai-cortex/artifact-norms.yaml 格式

YAML 结构与 [artifact-contract 附录 A](artifact-contract.md#appendix-a-machine-readable-schema-for-verify-artifact-contract) 兼容：

```yaml
artifact_types:
  requirements:
    path_patterns: ["docs/requirements/{slug}.md"]
    lifecycle: snapshot
  design:
    path_patterns: ["docs/designs/{slug}.md"]
    lifecycle: snapshot
  tasks:
    path_patterns: ["docs/tasks/{slug}.md"]
    lifecycle: living
  backlog-item:
    path_patterns:
      - "docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md"
      - "docs/backlog/YYYY-MM-DD-{slug}.md"
    lifecycle: living
  adr:
    path_patterns: ["docs/process-management/decisions/YYYYMMDD-{slug}.md"]
    lifecycle: living
  doc-assessment:
    path_patterns: ["docs/calibration/doc-assessment.md"]
    lifecycle: snapshot
```

---

## 5. 技能行为

技能行为协议见 [specs/artifact-contract.md §8 Runtime Norms Resolution Protocol](artifact-contract.md#8-runtime-norms-resolution-protocol)。技能在 Behavior 最前实现 **Stage 0: Norms Resolution** 步骤：按 §8.2 发现顺序读取项目规范、§8.3 占位符语法替换、§8.4 输出（resolved path_pattern + 可选 `upstream_ref` 触发 `parent:` emit）。

**本 schema 的职责**：定义项目规范文件的**字段集与语法**。运行时协议由 artifact-contract §8 规定。

**默认 vs 覆盖语义**：

- 技能 SKILL.md frontmatter 声明的 `output_schema.path_pattern` 是**默认值**
- 项目在 `.ai-cortex/artifact-norms.yaml` 或 `docs/ARTIFACT_NORMS.md` 声明的同名字段**覆盖**技能默认
- 项目规范只声明部分字段时，未声明字段继承默认（部分覆盖，非整替换，详见 artifact-contract §8.5）

### 占位符语法

`path_pattern` 字段支持的占位符，字符串级替换，语义见 [artifact-contract §8.3](artifact-contract.md#83-占位符语法)：

- `{slug}` — 制品主题 kebab-case
- `{parent_slug}` — 上游制品 slug（由调用方的 `upstream_ref` 输入派生）
- `{YYYY}` / `{YYYY-MM-DD}` / `{YYYYMMDD}` — 日期变体
- `{author}` — 创建者用户名

未解析占位符技能须追问用户，不得静默（详见 artifact-contract §8.6）。

### 自定义聚合目录（示例）

若项目想采用聚合式目录（所有相关制品同根）：

```yaml
artifact_types:
  requirements:
    path_patterns: ["work/{parent_slug}/requirement.md"]
  design:
    path_patterns: ["work/{parent_slug}/design.md"]
  tasks:
    path_patterns: ["work/{parent_slug}/tasks.md"]
```

调用方传 `upstream_ref` 即可，技能按新 path_pattern 写入聚合目录。

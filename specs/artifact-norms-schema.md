# 制品规范 Schema

**状态**：Informational  
**版本**：1.1.0  
**范围**：项目级制品路径与命名配置 + 制品间链接模式

---

## 1. 目的

项目可定义自己的制品规范以覆盖默认 [specs/artifact-contract.md](artifact-contract.md)。产出文档制品的技能优先读取项目规范；若不存在则回退到契约。

---

## 2. 解析顺序

技能按下列顺序检查：

1. `.ai-cortex/artifact-norms.yaml`（机器可读，自动化优先）
2. `docs/ARTIFACT_NORMS.md`（人工可读）
3. 若都不存在：使用 [specs/artifact-contract.md](artifact-contract.md) 作为默认

---

## 3. docs/ARTIFACT_NORMS.md 格式

最小结构（Markdown）：

```markdown
# Artifact Norms

**Source**: Custom | AI Cortex default | project-documentation-template

## Artifact Types

| artifact_type | path_pattern | naming | lifecycle |
| :--- | :--- | :--- | :--- |
| backlog-item | docs/... | YYYY-MM-DD-{slug}.md | living |
| design | docs/... | YYYY-MM-DD-{topic}.md | snapshot |
| adr | docs/... | YYYYMMDD-{slug}.md | living |
| doc-readiness | docs/calibration/ | YYYY-MM-DD-doc-readiness.md | snapshot |

## Path Detection (backlog-item, optional)

| Condition | Output path |
| :--- | :--- |
| docs/process-management/ exists | docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md |
| Otherwise | docs/backlog/YYYY-MM-DD-{slug}.md |
```

---

## 4. .ai-cortex/artifact-norms.yaml 格式

YAML 结构与 [artifact-contract 附录 A](artifact-contract.md#appendix-a-machine-readable-schema-for-verify-artifact-contract) 兼容：

```yaml
artifact_types:
  backlog-item:
    path_patterns:
      - "docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md"
      - "docs/backlog/YYYY-MM-DD-{slug}.md"
    naming: "YYYY-MM-DD-{slug}.md"
    lifecycle: living
  design:
    path_patterns:
      - "docs/design-decisions/YYYY-MM-DD-{topic}.md"
    naming: "YYYY-MM-DD-{topic}.md"
    lifecycle: snapshot
  adr:
    path_patterns:
      - "docs/process-management/decisions/YYYYMMDD-{slug}.md"
    naming: "YYYYMMDD-{slug}.md"
    lifecycle: living
  doc-readiness:
    path_patterns:
      - "docs/calibration/YYYY-MM-DD-doc-readiness.md"
    naming: "YYYY-MM-DD-doc-readiness.md"
    lifecycle: snapshot
```

---

## 5. 技能行为

当技能需要写入文档制品时：

1. **解析项目规范**：检查 `.ai-cortex/artifact-norms.yaml` 或 `docs/ARTIFACT_NORMS.md`。
2. **解析**：提取相关 artifact_type 的 path_pattern 与 naming。
3. **应用**：若找到项目规范则使用；否则使用 [specs/artifact-contract.md](artifact-contract.md) 默认。
4. **写入**：按解析路径与正确命名持久化。

---

## 6. 链接模式字段（v1.1 新增）

除 artifact_types 之外，项目规范可额外声明**链接模式**字段。定义见 [specs/linking-modes.md](linking-modes.md)（LINKING_MODES_SPEC_V1）。

**字段**：`linking_mode`（枚举，取值见 linking-modes.md §2）

- 值域：`slug | colocation | parent-pointer | manifest | mixed | none`
- 语义：项目使用哪种机械约定在制品之间建立追溯关系
- 写入者：`define-docs-norms`（基于 `discover-docs-norms` 识别结果 + 用户选择）
- 消费者：`plan-next` 以及其他需要跨制品追溯的技能

**在 `docs/ARTIFACT_NORMS.md` 中的示例**：

```markdown
## Linking Mode

linking_mode: slug
# 备选字段（mixed 模式下需要）：
# linking_mode_primary: slug
# linking_mode_secondary: manifest
# linking_mode_secondary_scope: now-tier
```

**在 `.ai-cortex/artifact-norms.yaml` 中的示例**：

```yaml
linking_mode: slug
# mixed 模式：
# linking_mode:
#   primary: slug
#   secondary:
#     mode: manifest
#     scope: now-tier
```

**缺省值**：若项目未声明 `linking_mode`，消费者（如 plan-next）应视为 `none` 并按 [specs/linking-modes.md §5](linking-modes.md) 的消费规则触发前置闸门。

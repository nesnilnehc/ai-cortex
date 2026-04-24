# 制品规范 Schema

**状态**：Informational  
**版本**：1.2.0  
**范围**：项目级制品路径与命名配置 + 制品间链接模式 + 占位符语法

**变更记录**：

- **v1.2.0 (2026-04-24)**：明示 `path_pattern` 从硬规则降级为默认值（被 [specs/artifact-contract.md §8](artifact-contract.md#8-runtime-norms-resolution-protocol) 覆盖规则接管）；新增占位符语法统一声明；新增"默认 vs 覆盖"语义节。
- v1.1.0 (2026-04-24)：新增 §6 链接模式字段规格。
- v1.0.0：初版。

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

## 5. 技能行为（v1.2 refactor）

自 v1.2 起，技能行为的详细协议迁移至 [specs/artifact-contract.md §8 Runtime Norms Resolution Protocol](artifact-contract.md#8-runtime-norms-resolution-protocol)。技能在 Behavior 最前实现 **Stage 0: Norms Resolution** 步骤，按 §8.2 发现顺序读取本 schema 声明的项目规范、§8.3 占位符语法替换、§8.4 按 `linking_mode` 分支输出。

**本 schema 的职责**：定义项目规范文件的**字段集与语法**。运行时协议由 artifact-contract §8 规定。

**默认 vs 覆盖语义**：

- 技能 SKILL.md frontmatter 声明的 `output_schema.path_pattern` 从**硬规则**降级为**默认值**
- 项目在 `.ai-cortex/artifact-norms.yaml` 或 `docs/ARTIFACT_NORMS.md` 声明的同名字段**覆盖**技能默认
- 项目规范只声明部分字段时，未声明字段继承默认（部分覆盖，非整替换，详见 artifact-contract §8.5）

### 占位符语法

`path_pattern` 与 `naming` 字段支持的占位符，字符串级替换，语义见 [artifact-contract §8.3](artifact-contract.md#83-占位符语法)：

- `{slug}` — 制品主题 kebab-case
- `{topic}` — 与 slug 等价（历史兼容）
- `{parent_slug}` — 上游制品 slug（colocation / parent-pointer 模式必需）
- `{YYYY}` / `{YYYY-MM-DD}` / `{YYYYMMDD}` — 日期变体
- `{author}` — 创建者用户名

未解析占位符技能须追问用户，不得静默（详见 artifact-contract §8.6）。

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

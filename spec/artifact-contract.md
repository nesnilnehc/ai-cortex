# 制品契约

**状态**：DEFAULT（默认，可选参考）  
**版本**：1.2.0  
**范围**：在项目 `docs/` 或仓库根下写入 Markdown 制品的技能

**变更记录**：

- v1.2.0 (2026-03-16)：新增 `requirements` 制品类型；归属技能 `analyze-requirements`。
- v1.1.0 (2026-03-06)：项目规范优先；本契约为默认回退；AI Cortex 与 project-documentation-template 为可信建议。
- v1.0.0 (2026-03-06)：初版；AI Cortex 原则优先；project-documentation-template 为补充参考。

---

## 1. 设计原则

**项目规范优先**：若项目定义了自己的制品规范（见 [spec/artifact-norms-schema.md](artifact-norms-schema.md)），技能须遵循项目规范。项目是其自身文档结构的权威。

**回退**：若不存在项目规范（无 `docs/ARTIFACT_NORMS.md` 或 `.ai-cortex/artifact-norms.yaml`），技能使用本契约作为路径、命名与生命周期的默认值。

**可信建议**：本契约、AI Cortex 技能与 [project-documentation-template](https://github.com/nesnilnehc/project-documentation-template) 为可选、可信参考。它们不覆盖用户既有的文档与目录结构。用户可采纳、定制或忽略。

**兼容性**：路径设计使使用 project-documentation-template 的项目在重叠处可映射结构。未使用该模板的项目仍可将本契约作为回退；无外部依赖。

---

## 2. 制品类型

| artifact_type | path_pattern | naming | lifecycle | owner_skill |
| :--- | :--- | :--- | :--- | :--- |
| requirements | `docs/requirements-planning/` | `{topic}.md` | snapshot | analyze-requirements |
| backlog-item | `docs/process-management/project-board/backlog/` | `YYYY-MM-DD-{slug}.md` | living | capture-work-items |
| backlog-item (fallback) | `docs/backlog/` | `YYYY-MM-DD-{slug}.md` | living | capture-work-items |
| adr | `docs/process-management/decisions/` | `YYYYMMDD-{slug}.md` | living | bootstrap-docs |
| design | `docs/design-decisions/` | `YYYY-MM-DD-{topic}.md` | snapshot | design-solution |
| doc-assessment | `docs/calibration/` | `YYYY-MM-DD-doc-assessment.md` | snapshot | assess-docs |

### 路径理由

- **requirements**：`docs/requirements-planning/` 归集所有已验证需求；扁平命名 `{topic}.md` 便于设计文档直接引用。`review-requirements` 以这些文件为输入做质量评估。
- **backlog-item**：`project-board/backlog/` 与敏捷看板语义一致；单文件单条便于分流与追溯。无 process-management 的轻量项目使用回退 `docs/backlog/`。
- **adr**：`process-management/decisions/` 将架构决策与过程文档归类；`YYYYMMDD` 遵循 ADR 社区惯例。
- **design**：顶级 `docs/design-decisions/` 避免与模板的 `design/`（品牌/UI）混淆；与 ADR 区分（实现设计 vs 架构决策）。
- **doc-readiness**：`docs/calibration/` 用于治理/评估报告；与内容文档分离。

---

## 3. 路径检测（backlog-item）

对于 `capture-work-items`，使用：

| 条件 | 输出路径 |
| :--- | :--- |
| `docs/process-management/` 存在 | `docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md` |
| 否则 | `docs/backlog/YYYY-MM-DD-{slug}.md` |

如子目录不存在则创建。

---

## 4. 最小路径集（轻量项目）

对于无或仅有最小 `docs/` 结构的项目，下列路径足够：

- `docs/backlog/` — 工作项
- `docs/design-decisions/` — 设计文档
- `docs/calibration/` — 就绪/评估报告

ADR 与完整 process-management 结构对更大项目为可选。

---

## 5. Front-Matter 要求

产出文档制品的技能应在 YAML front-matter 中包含：

| 字段 | 必填 | 说明 |
| :--- | :---: | :--- |
| `artifact_type` | 是 | 取其一：backlog-item, adr, design, doc-readiness |
| `created_by` | 是 | 技能名（如 `capture-work-items`） |
| `lifecycle` | 可选 | `snapshot` 或 `living` |
| `created_at` | 可选 | `YYYY-MM-DD` |

渐进采纳：无这些字段的既有文档仍然有效；新技能产出应包含必填字段。

---

## 6. 命名约定

- **Slug**：kebab-case，仅小写字母与连字符；从标题派生。
- **文件名中的日期**：`YYYY-MM-DD` 便于人工排序（ADR 除外：按社区惯例用 `YYYYMMDD`）。
- **目录**：仅 kebab-case。

---

## 7. 扩展制品类型

新增制品类型时：

1. 在 §2 表中增加行，含 path_pattern、naming、lifecycle、owner_skill。
2. 若非显而易见，文档化路径理由。
3. 更新受影响技能的 `output_schema` 与 Self-Check。
4. 提升契约版本（增补用 PATCH，路径变更用 MINOR）。

---

## 附录 A：机器可读 Schema（供 verify-artifact-contract）

```yaml
artifact_types:
  requirements:
    path_patterns:
      - "docs/requirements-planning/{topic}.md"
    naming: "{topic}.md"
    lifecycle: snapshot
    owner_skill: analyze-requirements
  backlog-item:
    path_patterns:
      - "docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md"
      - "docs/backlog/YYYY-MM-DD-{slug}.md"
    naming: "YYYY-MM-DD-{slug}.md"
    lifecycle: living
    owner_skill: capture-work-items
  adr:
    path_patterns:
      - "docs/process-management/decisions/YYYYMMDD-{slug}.md"
    naming: "YYYYMMDD-{slug}.md"
    lifecycle: living
    owner_skill: bootstrap-docs
  design:
    path_patterns:
      - "docs/design-decisions/YYYY-MM-DD-{topic}.md"
    naming: "YYYY-MM-DD-{topic}.md"
    lifecycle: snapshot
    owner_skill: design-solution
  doc-readiness:
    path_patterns:
      - "docs/calibration/YYYY-MM-DD-doc-readiness.md"
    naming: "YYYY-MM-DD-doc-readiness.md"
    lifecycle: snapshot
    owner_skill: assess-docs
```

# 制品契约

**状态**：DEFAULT（默认，可选参考）  
**版本**：3.0.0  
**范围**：在项目 `docs/` 或仓库根下写入 Markdown 制品的技能

**变更记录**：

- **v3.0.0 (2026-04-24)**：新增 **§8 Runtime Norms Resolution Protocol**。技能在运行时按统一发现顺序读取项目规范，`path_pattern` 从硬规则降级为默认值；新增 `{slug}` / `{topic}` / `{parent_slug}` / `{YYYY}` / `{YYYY-MM-DD}` 占位符语法；按 `linking_mode` 枚举（见 [specs/linking-modes.md](linking-modes.md)）分支 colocation / parent-pointer / manifest 输出。MAJOR：消费此契约的技能必须实现 Stage 0 Norms Resolution 步骤。
- v1.2.0 (2026-03-16)：新增 `requirements` 制品类型；归属技能 `analyze-requirements`。
- v1.1.0 (2026-03-06)：项目规范优先；本契约为默认回退；AI Cortex 与 project-documentation-template 为可信建议。
- v1.0.0 (2026-03-06)：初版；AI Cortex 原则优先；project-documentation-template 为补充参考。

---

## 1. 设计原则

**项目规范优先**：若项目定义了自己的制品规范（见 [specs/artifact-norms-schema.md](artifact-norms-schema.md)），技能须遵循项目规范。项目是其自身文档结构的权威。

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

---

## 8. Runtime Norms Resolution Protocol (v3.0+)

本章是 v3.0 新增的规范性段落。所有产出文档制品的技能**必须**在 Behavior 最前实现 **Stage 0: Norms Resolution** 步骤。

### 8.1 目的

统一产出技能在运行时解析输出路径、命名、链接模式的方式，使 `docs/ARTIFACT_NORMS.md` 与 `.ai-cortex/artifact-norms.yaml` 成为**真正的运行时权威**，而不只是人读参考。

技能 frontmatter 里的 `output_schema.path_pattern` 从**硬规则**降级为**默认值**，可被项目规范覆盖。

### 8.2 发现顺序

技能按下列优先级依次检查来源，首命中返回：

1. **调用方 frontmatter 输入**：若调用方传入 `artifact_norms_path: <path>`，使用该路径指向的规范文件
2. **`.ai-cortex/artifact-norms.yaml`**：机器可读项目规范，最高持久化优先级
3. **`docs/ARTIFACT_NORMS.md`**：人读项目规范；技能需解析其"Artifact Types"表与"Linking Mode"节
4. **技能自身 frontmatter `output_schema.path_pattern`**：技能默认
5. **本契约 §2 表**：最终 fallback

**缺失不报错**：任一层缺失即顺延至下一层，不阻断工作。

### 8.3 占位符语法

`path_pattern` 支持下列占位符，字符串级替换：

| 占位符 | 含义 | 来源 |
|---|---|---|
| `{slug}` | 制品主题的 kebab-case slug | 调用方 `slug` 输入 / 从 `topic` 派生 / 上游 slug |
| `{topic}` | 制品标题的 kebab-case slug（与 slug 等价，历史兼容） | 同 slug |
| `{parent_slug}` | 上游制品的 slug（colocation / parent-pointer 模式必需） | `upstream_ref` frontmatter 输入 |
| `{YYYY}` | 四位年份 | 当前日期 |
| `{YYYY-MM-DD}` | ISO 日期 | 当前日期 |
| `{YYYYMMDD}` | ADR 习惯日期 | 当前日期 |
| `{author}` | 创建者用户名 | git user.name 或调用方传入 |

**未解析占位符处理**：若 `path_pattern` 里的占位符无数据可替换，技能**必须停止并追问用户**，不得静默使用默认或空值。

### 8.4 Linking-mode 输出规则

按项目规范声明的 `linking_mode`（见 [specs/linking-modes.md](linking-modes.md) 6 项枚举）决定最终输出路径与 frontmatter。

| linking_mode | 输出路径 | Frontmatter 要求 | 其他 |
|---|---|---|---|
| `slug` | 按 §8.3 解析后的 `path_pattern` | 无额外 | 默认模式 |
| `colocation` | `work/{parent_slug}/{artifact_type}.md`（覆盖 `path_pattern`）| 无额外 | 需 `upstream_ref` 输入提供 `parent_slug` |
| `parent-pointer` | 按 §8.3 解析后的 `path_pattern` | **强制**：`parent: <upstream-relative-path>` | 需 `upstream_ref` 输入 |
| `manifest` | 按 §8.3 解析后的 `path_pattern` | 无额外 | advisory：建议由 [`align-work-item-manifest`](../skills/align-work-item-manifest/SKILL.md) 检测漂移 |
| `mixed` | 按 `ARTIFACT_NORMS.md` 里 `mixed.rules` 声明的子映射查对应 artifact_type | 按子映射而定 | 子映射必须穷尽项目的 artifact_type |
| `none` | 按 §8.3 解析后的 `path_pattern` | 无额外 | 与 slug 等价 |

**Stage 0 决策算法**：

```
Stage 0: Norms Resolution
  1. 按 §8.2 顺序发现并解析项目规范 → resolved_norms（map）
  2. 从 resolved_norms 查当前 artifact_type 的 path_pattern
     - 命中：使用项目规范
     - 未命中：fall back 到技能 frontmatter path_pattern 默认
  3. 从 resolved_norms 查 linking_mode
     - 未声明：视为 'none'
  4. 按 §8.4 表决定最终输出路径与 frontmatter 要求
     - 若 colocation / parent-pointer 需要 {parent_slug}：
        - 读调用方 frontmatter 输入字段 `upstream_ref`
        - 若缺失：追问用户，不静默
  5. 按 §8.3 占位符语法替换
  6. 记录最终 resolved_path 与 frontmatter 增量，供后续 emit 阶段消费
```

### 8.5 合并语义

项目规范声明的 artifact_types 是**部分覆盖**，不是整文件替换：

- 项目规范只声明了 `design` 的 `path_pattern` → `design` 使用项目值，其他类型继承 §2 默认
- 项目规范新增了 `experiment` 这个本契约没有的类型 → 该新类型按项目规范输出；已有类型不受影响
- 项目规范删除了某字段 → 技能 fall through 到下一级

### 8.6 错误处理

| 情形 | 处理 |
|---|---|
| 规范文件存在但 YAML 畸形 | 停止，诊断输出指到具体行；不静默使用默认 |
| 规范文件缺失 | fall through 发现顺序，不报错 |
| 占位符无法解析 | 停止，追问用户缺失的 token |
| `linking_mode: colocation` 但无 `upstream_ref` | 追问用户或停止 |
| `linking_mode: mixed` 但无 `mixed.rules` | 停止，诊断要求补 rules |
| 未知 `linking_mode` 值（不在 6 枚举内） | 停止，指向 [specs/linking-modes.md](linking-modes.md) |

### 8.7 校验钩子

注册表校验脚本（`scripts/verify-registry.mjs`）断言每个**产出文档制品的技能**的 SKILL.md 包含 `Stage 0` 或 `Norms Resolution` 标题字符串。非产出技能（review-* / automate-* / curate-* 等）不适用此检查。

**产出技能判定**：`output_schema.type == document-artifact` 的技能。

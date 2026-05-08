# 制品契约

**状态**：DEFAULT（默认，可选参考）  
**版本**：5.0.0  
**范围**：在项目 `docs/` 或仓库根下写入 Markdown 制品的技能

## 1. 设计原则

**项目规范优先**：若项目定义了自己的制品规范（见 [specs/artifact-norms-schema.md](artifact-norms-schema.md)），技能须遵循项目规范。项目是其自身文档结构的权威。

**回退**：若不存在项目规范（无 `docs/ARTIFACT_NORMS.md` 或 `.ai-cortex/artifact-norms.yaml`），技能使用本契约作为路径、命名与生命周期的默认值。

**可信建议**：本契约、AI Cortex 技能与 [project-documentation-template](https://github.com/nesnilnehc/project-documentation-template) 为可选、可信参考。它们不覆盖用户既有的文档与目录结构。用户可采纳、定制或忽略。

**兼容性**：路径设计使使用 project-documentation-template 的项目在重叠处可映射结构。未使用该模板的项目仍可将本契约作为回退；无外部依赖。

---

## 2. 制品类型

| artifact_type | path_pattern | lifecycle | owner_skill |
| :--- | :--- | :--- | :--- |
| requirements | `docs/requirements/{slug}.md` | snapshot | analyze-requirements |
| design | `docs/designs/{slug}.md` | snapshot | design-solution |
| tasks | `docs/tasks/{slug}.md` | living | breakdown-tasks |
| backlog-item | `docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md` | living | capture-work-items |
| backlog-item (fallback) | `docs/backlog/YYYY-MM-DD-{slug}.md` | living | capture-work-items |
| adr | `docs/process-management/decisions/YYYYMMDD-{slug}.md` | living | bootstrap-docs |
| doc-assessment | `docs/calibration/doc-assessment.md` | snapshot | assess-docs |
| milestone-summary | `docs/process-management/milestones/_archive/{slug}-summary.md` | snapshot | archive-milestone |

### 路径理由

- **requirements / design / tasks**：统一为 `docs/<type>/{slug}.md` 的并列平级目录，文件名仅 `{slug}.md`（无日期前缀）。三类制品自然关联——同一 slug 跨目录即能 glob 打通全链（"user-auth" 的 requirement / design / tasks 共享 slug）。v5.0 起这是 canonical 约定；日期前缀由 git log 提供，文件名不重复编码。
- **backlog-item**：`project-board/backlog/` 与敏捷看板语义一致；日期前缀保留因 backlog 条目按日期分流是常见实践。无 process-management 的轻量项目使用回退 `docs/backlog/`。
- **adr**：`process-management/decisions/` 将架构决策与过程文档归类；`YYYYMMDD` 遵循 ADR 社区惯例。
- **doc-assessment**：`docs/calibration/` 用于治理/评估报告；与内容文档分离。
- **milestone-summary**：`milestones/_archive/` 与活跃里程碑目录并列，`_` 前缀约定为非活跃/模板路径，与 `_templates/` 风格一致；`{slug}-summary.md` 后缀明确文件角色，便于 glob 区分活跃任务与归档摘要。

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

- `docs/requirements/` — 需求文档
- `docs/designs/` — 设计文档
- `docs/tasks/` — 任务列表
- `docs/backlog/` — 待办条目
- `docs/calibration/` — 就绪/评估报告

ADR 与完整 process-management 结构对更大项目为可选。

---

## 5. Front-Matter 要求

产出文档制品的技能应在 YAML front-matter 中包含：

| 字段 | 必填 | 说明 |
| :--- | :---: | :--- |
| `artifact_type` | 是 | 取其一：requirements, design, tasks, backlog-item, adr, doc-assessment, milestone-summary |
| `created_by` | 是 | 技能名（如 `capture-work-items`） |
| `lifecycle` | 可选 | `snapshot` 或 `living` |
| `created_at` | 可选 | `YYYY-MM-DD` |

渐进采纳：无这些字段的既有文档仍然有效；新技能产出应包含必填字段。

---

## 6. 命名约定

- **Slug**：kebab-case，仅小写字母与连字符；从标题派生。
- **文件名**：
  - **requirements / design / tasks**：`{slug}.md`（v5.0 起无日期前缀；git log 提供时序）
  - **backlog-item**：`YYYY-MM-DD-{slug}.md`（日期前缀便于看板分流）
  - **adr**：`YYYYMMDD-{slug}.md`（遵循 ADR 社区惯例）
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
      - "docs/requirements/{slug}.md"
    lifecycle: snapshot
    owner_skill: analyze-requirements
  design:
    path_patterns:
      - "docs/designs/{slug}.md"
    lifecycle: snapshot
    owner_skill: design-solution
  tasks:
    path_patterns:
      - "docs/tasks/{slug}.md"
    lifecycle: living
    owner_skill: breakdown-tasks
  backlog-item:
    path_patterns:
      - "docs/process-management/project-board/backlog/YYYY-MM-DD-{slug}.md"
      - "docs/backlog/YYYY-MM-DD-{slug}.md"
    lifecycle: living
    owner_skill: capture-work-items
  adr:
    path_patterns:
      - "docs/process-management/decisions/YYYYMMDD-{slug}.md"
    lifecycle: living
    owner_skill: bootstrap-docs
  doc-assessment:
    path_patterns:
      - "docs/calibration/doc-assessment.md"
    lifecycle: snapshot
    owner_skill: assess-docs
```

---

## 8. Runtime Norms Resolution Protocol (v3.0+)

本章是 v3.0 新增的规范性段落。所有产出文档制品的技能**必须**在 Behavior 最前实现 **Stage 0: Norms Resolution** 步骤。

### 8.1 目的

统一产出技能在运行时解析输出路径的方式，使 `docs/ARTIFACT_NORMS.md` 与 `.ai-cortex/artifact-norms.yaml` 成为**真正的运行时权威**，而不只是人读参考。

技能 frontmatter 里的 `output_schema.path_pattern` 是**默认值**，可被项目规范覆盖。

### 8.2 发现顺序

技能按下列优先级依次检查来源，首命中返回：

1. **调用方 frontmatter 输入**：若调用方传入 `artifact_norms_path: <path>`，使用该路径指向的规范文件
2. **`.ai-cortex/artifact-norms.yaml`**：机器可读项目规范，最高持久化优先级
3. **`docs/ARTIFACT_NORMS.md`**：人读项目规范；技能需解析其"Artifact Types"表
4. **技能自身 frontmatter `output_schema.path_pattern`**：技能默认
5. **本契约 §2 表**：最终 fallback

**缺失不报错**：任一层缺失即顺延至下一层，不阻断工作。

### 8.3 占位符语法

`path_pattern` 支持下列占位符，字符串级替换：

| 占位符 | 含义 | 来源 |
|---|---|---|
| `{slug}` | 制品主题的 kebab-case slug | 调用方 `slug` 输入 |
| `{parent_slug}` | 上游制品的 slug（仅在项目自定义聚合式 path_pattern 时使用） | `upstream_ref` frontmatter 输入派生 |
| `{YYYY}` | 四位年份 | 当前日期 |
| `{YYYY-MM-DD}` | ISO 日期 | 当前日期 |
| `{YYYYMMDD}` | ADR 习惯日期 | 当前日期 |
| `{author}` | 创建者用户名 | git user.name 或调用方传入 |

**未解析占位符处理**：若 `path_pattern` 里的占位符无数据可替换，技能**必须停止并追问用户**，不得静默使用默认或空值。

### 8.4 输出规则

**AI Cortex 默认约定**：按 §2 制品类型表——requirements / design / tasks 统一为 `docs/<type>/{slug}.md`；backlog-item / adr / doc-assessment 保留历史路径。这是仓库级 canonical，项目可通过 §8.2 发现顺序覆盖。

**可选追溯（upstream_ref）**：所有链接锚点技能（analyze-requirements / design-solution / breakdown-tasks / capture-work-items / bootstrap-docs）**必须**接受 optional `upstream_ref` frontmatter 输入。若调用方提供，技能在产出制品的 frontmatter 中 emit `parent: <upstream-relative-path>`。这是**可选增强**——给了就 emit，没给就不 emit。

**Stage 0 决策算法**：

```
Stage 0: Norms Resolution
  1. 按 §8.2 顺序发现并解析项目规范 → resolved_norms（map）
  2. 从 resolved_norms 查当前 artifact_type 的 path_pattern
     - 命中：使用项目规范（可能是任意自定义路径，包括聚合式如 work/{parent_slug}/design.md）
     - 未命中：fall back 到技能 frontmatter 默认（= §2 canonical）
  3. 按 §8.3 占位符语法替换；未解析占位符按 §8.6 错误处理（追问用户）
  4. 若调用方 frontmatter 输入含 upstream_ref：
     - 在产出制品的 frontmatter emit parent: <upstream_ref>
     - 若 path_pattern 含 {parent_slug} 占位符，用 upstream_ref 派生 slug 替换
  5. 记录最终 resolved_path 与 frontmatter 增量，供后续 emit 阶段消费
```

**项目自定义典型场景**：

- **聚合式目录**（所有相关制品同根）：在 `ARTIFACT_NORMS.md` 把各 artifact_type 的 `path_pattern` 覆盖为 `work/{parent_slug}/<type>.md`，调用方传 `upstream_ref`。
- **显式父指针**：调用下游技能时传 `upstream_ref`；技能自动 emit `parent:` frontmatter。
- **中央清单**：项目建清单文件（如 `docs/process-management/now/<slug>.md`）；plan-next 与 align-work-item-manifest 通过 glob 物理检测消费清单。

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
| `path_pattern` 含 `{parent_slug}` 但调用方未传 `upstream_ref` | 追问用户或停止 |

### 8.7 校验钩子

注册表校验脚本（`scripts/verify-registry.mjs`）断言每个**产出文档制品的技能**的 SKILL.md 包含 `Stage 0` 或 `Norms Resolution` 标题字符串。非产出技能（review-* / automate-* / curate-* 等）不适用此检查。

**产出技能判定**：`output_schema.type == document-artifact` 的技能。

---

## 变更历史

- **v5.0.0 (2026-04-25)**：统一 `requirements` / `design` / `tasks` 三类制品的 canonical 路径为 `docs/<type>/{slug}.md`（无日期前缀）；§2 与 Appendix A 相应更新；相关技能 MAJOR bump。清理 linking_mode 相关所有引用（ADR 006）。MAJOR：使用旧路径的项目需迁移文件或在 `ARTIFACT_NORMS.md` 显式覆盖保留旧路径。
- v4.0.0 (2026-04-25)：回撤 §8.4 linking-mode 输出真值表；保留 §8.1–§8.3 / §8.5–§8.7 的 path_pattern 覆盖机制（ADR 005）。
- v3.0.0 (2026-04-24)：新增 §8 Runtime Norms Resolution Protocol。
- v1.2.0 (2026-03-16)：新增 `requirements` 制品类型。
- v1.1.0 (2026-03-06)：项目规范优先；本契约为默认回退。
- v1.0.0 (2026-03-06)：初版。

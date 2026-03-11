---
artifact_type: adr
path_pattern: docs/process-management/decisions/YYYYMMDD-{slug}.md
created_at: "2026-03-10"
lifecycle: living
---

# Skill 命名审计（按 spec §1 命名优先级）

**日期**: 2026-03-10  
**规范依据**: [spec/skill.md](../../../spec/skill.md) §1 命名优先级 — 语义正确与规范性优先，口语与好记其次

---

## 1. 审计维度与优秀标准

### 1.1 审计维度

| 维度 | 优先级 | 说明 |
| --- | --- | --- |
| **语义正确** | P0 | 动词准确描述技能动作；名词准确描述作用对象/产出 |
| **规范性** | P0 | verb-noun；无纯名词复合；符合 spec |
| **口语/好记** | P1 | 自然顺口；易记；在 P0 满足前提下优化 |

### 1.2 优秀标准（目标：全部达标）

命名达到**优秀**须满足：

- **语义正确**：✓
- **规范性**：✓
- **口语/好记**：✓（自然顺口；易记；≤3 段；无冗余词；动词非过度泛化；领域精确术语可视为例外达标）

---

## 2. 全量 Skill 审计结果

| Skill | 语义正确 | 规范性 | 口语/好记 | 优秀 | 备注 |
| --- | ---: | ---: | ---: | ---: | --- |
| align-architecture | ✓ | ✓ | ✓ | ✓ | |
| align-planning | ✓ | ✓ | ✓ | ✓ | |
| analyze-requirements | ✓ | ✓ | ✓ | ✓ | |
| assess-documentation-readiness | ✓ | ✓ | 中 | ✗ | 4 段，略长 |
| bootstrap-project-documentation | ✓ | ✓ | 中 | ✗ | 3 段，略长 |
| brainstorm-design | ✓ | ✓ | ✓ | ✓ | |
| capture-work-items | ✓ | ✓ | ✓ | ✓ | |
| commit-work | ✓ | ✓ | ✓ | ✓ | |
| curate-skills | ✓ | ✓ | ✓ | ✓ | |
| decontextualize-text | ✓ | ✓ | 中 | ✓* | 专业术语可例外 |
| discover-document-norms | ✓ | ✓ | ✓ | ✓ | |
| discover-skills | ✓ | ✓ | ✓ | ✓ | |
| generate-github-workflow | ✓ | ✓ | ✓ | ✓ | |
| generate-standard-readme | ✓ | ✓ | ✓ | ✓ | |
| install-rules | ✓ | ✓ | ✓ | ✓ | |
| onboard-repo | ✓ | ✓ | ✓ | ✓ | |
| orchestrate-governance-loop | 中 | ✓ | 差 | ✗ | 语义与口语均不足 |
| prune-content | ✓ | ✓ | ✓ | ✓ | |
| refine-skill-design | ✓ | ✓ | ✓ | ✓ | |
| review-architecture | ✓ | ✓ | ✓ | ✓ | |
| review-code | ✓ | ✓ | ✓ | ✓ | |
| review-codebase | ✓ | ✓ | ✓ | ✓ | |
| review-diff | ✓ | ✓ | ✓ | ✓ | |
| review-dotnet | ✓ | ✓ | ✓ | ✓ | |
| review-go | ✓ | ✓ | ✓ | ✓ | |
| review-java | ✓ | ✓ | ✓ | ✓ | |
| review-orm-usage | ✓ | ✓ | ✓ | ✓ | |
| review-performance | ✓ | ✓ | ✓ | ✓ | |
| review-php | ✓ | ✓ | ✓ | ✓ | |
| review-powershell | ✓ | ✓ | ✓ | ✓ | |
| review-python | ✓ | ✓ | ✓ | ✓ | |
| review-react | ✓ | ✓ | ✓ | ✓ | |
| review-security | ✓ | ✓ | ✓ | ✓ | |
| review-sql | ✓ | ✓ | ✓ | ✓ | |
| review-testing | ✓ | ✓ | ✓ | ✓ | |
| review-typescript | ✓ | ✓ | ✓ | ✓ | |
| review-vue | ✓ | ✓ | ✓ | ✓ | |
| run-automated-tests | ✓ | ✓ | ✓ | ✓ | run = literal 执行 |
| run-repair-loop | ✓ | ✓ | ✓ | ✓ | run = literal 执行 |
| validate-document-artifacts | ✓ | ✓ | 中 | ✗ | 3 段，略长 |
| write-agents-entry | ✓ | ✓ | ✓ | ✓ | |

---

## 3. 改进提案（未达优秀 → 达标）

以下 5 项需改进以达到优秀标准。每条给出推荐方案及备选。

| 当前名称 | 问题 | 推荐改进 | 备选 |
| --- | --- | --- | --- |
| orchestrate-governance-loop | 语义偏离、拗口 | **run-checkpoint** | assess-project-state |
| assess-documentation-readiness | 4 段略长 | **assess-doc-readiness** | 保持（若接受 4 段） |
| bootstrap-project-documentation | 3 段略长 | **bootstrap-docs** | bootstrap-documentation |
| validate-document-artifacts | 3 段略长 | **validate-artifacts** | validate-docs |
| decontextualize-text | 动词拗口 | 保持（专业术语例外） | — |

### 3.1 orchestrate-governance-loop → run-checkpoint

- **语义**：本质为「分析项目状态 → 产出下一步」；run-checkpoint 表达「跑检查点」。
- **口语**：简洁、好记。
- **风险**：run 略泛，但在 checkpoint 语境下可接受（与 run-repair-loop 同类）。

### 3.2 assess-documentation-readiness → assess-doc-readiness

- **语义**：doc 为 documentation 缩写，在文档技能语境下无歧义。
- **口语**：3 段，更顺口。

### 3.3 bootstrap-project-documentation → bootstrap-docs

- **语义**：docs 在项目语境下默认指项目文档。
- **口语**：2 段，简洁。

### 3.4 validate-document-artifacts → validate-artifacts

- **语义**：validate-artifacts 在 document-artifact 生态下默认指文档类 artifact。
- **口语**：2 段，简洁。

### 3.5 decontextualize-text

- **建议**：保持。decontextualize 为领域精确术语，替代会损语义；优秀标准允许领域术语例外，视为达标。

---

## 4. 结论

- **优秀达标**：37/41（含 decontextualize-text 专业术语例外）。
- **已实施**（2026-03-10）：orchestrate-governance-loop → run-checkpoint；assess-documentation-readiness → assess-doc-readiness；bootstrap-project-documentation → bootstrap-docs；validate-document-artifacts → validate-doc-artifacts。
- **实施顺序建议**：orchestrate-governance-loop → run-checkpoint（优先）；其余按影响范围分批。

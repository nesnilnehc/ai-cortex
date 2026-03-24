# 制品规范

**来源**：AI Cortex 项目覆盖

语言：见 [docs/LANGUAGE_SCHEME.md](LANGUAGE_SCHEME.md) 了解项目语言规则。

本规范定义生成制品的单一权威路径。除非用户明确要求快照，技能应覆盖下列路径下的规范文件。

---

## 单一事实源（SSOT）原则

每类制品的定义与权威来源明确如下。其他文档在涉及同类信息时，应采用"引用+补充"而非"复写"的方式。

### Canonical Source（权威来源）定义

| Artifact Type | Canonical Source | 强制性 | 规则 |
| :--- | :--- | :--- | :--- |
| strategic-goals | `docs/project-overview/strategic-goals.md` | ★★★ | 战略目标的唯一权威定义；其他文档应用链接+摘要引用 |
| roadmap（含 milestones） | `docs/process-management/roadmap.md` | ★★★ | 路线图与里程碑的唯一权威定义；其他文档不应独立重定义 |
| requirements | `docs/requirements-planning/{topic}.md` | ★★★ | 各主题需求的权威来源 |
| backlog-item（索引） | `docs/process-management/backlog.md` | ★★ | Backlog 工作条目的索引与导航 |
| backlog-item（详情） | `docs/process-management/backlog/YYYY-MM-DD-*.md` | ★★ | 工作条目的详细定义 |
| adr | `docs/process-management/decisions/YYYYMMDD-*.md` | ★★ | 架构决策的权威记录 |
| design | `docs/designs/YYYY-MM-DD-*.md` | ★★ | 设计方案的权威定义 |

### 合规引用规则

- **纯链接**：引用文档仅包含指向 canonical source 的链接 → ✅ **最佳实践**
- **摘要+链接**：20-30% 原文摘要 + 链接指向权威源 → ✅ **合规**
- **完全复写**（>60% 重叠，无链接）→ ❌ **违规**，需优化

---

## 制品类型

| artifact_type | path_pattern | naming | lifecycle |
| :--- | :--- | :--- | :--- |
| requirements | docs/requirements-planning/{topic}.md | {topic}.md | snapshot |
| backlog-item | docs/process-management/backlog/YYYY-MM-DD-{slug}.md | YYYY-MM-DD-{slug}.md | living |
| adr | docs/process-management/decisions/YYYYMMDD-{slug}.md | YYYYMMDD-{slug}.md | living |
| adr (architecture) | docs/architecture/adrs/NNN-{slug}.md | NNN-{slug}.md | living |
| design | docs/designs/YYYY-MM-DD-{topic}.md | YYYY-MM-DD-{topic}.md | snapshot |
| doc-readiness | docs/calibration/doc-readiness.md | doc-readiness.md | living |
| planning-alignment | docs/calibration/planning-alignment.md | planning-alignment.md | living |
| architecture-compliance | docs/calibration/architecture-compliance.md | architecture-compliance.md | living |
| cognitive-loop | docs/calibration/cognitive-loop.md | cognitive-loop.md | living |
| repair-loop | docs/calibration/repair-loop.md | repair-loop.md | living |
| audit-docs | docs/calibration/audit-docs.md | audit-docs.md | living |
| detect-ssot-violations-report | docs/calibration/ssot-violations.md | ssot-violations.md | living |

## 路径检测（backlog-item）

| Condition | Output path |
| :--- | :--- |
| docs/process-management/ 存在 | docs/process-management/backlog/YYYY-MM-DD-{slug}.md |

## 例外（backlog 目录）

`backlog/` 目录仅存放 `YYYY-MM-DD-{slug}.md` 格式的 backlog-item。索引类文件置于 `docs/process-management/` 下。

---

## 时间戳策略（Timestamp Policy）

文件名中的时间戳（YYYY-MM-DD 或 YYYYMMDD 格式）应遵循以下规则，避免不必要的时间戳滋生：

| Artifact Type | 时间戳要求 | 格式 | 理由 |
| :--- | :--- | :--- | :--- |
| **adr** | REQUIRED | `YYYYMMDD-{slug}` | 架构决策具有"点在时间"的特征，时间戳记录决策时刻 |
| **design** | REQUIRED | `YYYY-MM-DD-{topic}` | 设计是快照制品，时间戳记录方案版本时刻 |
| **backlog-item** | REQUIRED | `YYYY-MM-DD-{slug}` | 工作项的创建或分配时刻需要记录 |
| **roadmap** | FORBIDDEN | 无时间戳 | 路线图是活文档，持续演进；不应标注时间 |
| **strategic-goals** | FORBIDDEN | 无时间戳 | 战略目标是长期方向，不应带时间戳 |
| **requirements** | FORBIDDEN | 无时间戳 | 需求是活文档，持续更新；不应标注时间 |
| **backlog（索引）** | FORBIDDEN | 无时间戳 | Backlog 索引是实时导航，不应标注时间 |
| **audit-docs** | FORBIDDEN | 无时间戳 | 审计报告是活文档，持续更新；不应标注时间 |
| **detect-ssot-violations-report** | FORBIDDEN | 无时间戳 | SSOT 报告是活文档，持续迭代；不应标注时间 |

### 设计原则

- **点在时间的制品**（ADR、设计、工作项）→ REQUIRED：需要时间戳记录快照时刻
- **活文档与持续演进的制品**（路线图、目标、需求、报告）→ FORBIDDEN：时间戳会造成版本混乱

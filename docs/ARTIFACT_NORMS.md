# 制品规范

**来源**：AI Cortex 项目覆盖

语言：见 [docs/LANGUAGE_SCHEME.md](LANGUAGE_SCHEME.md) 了解项目语言规则。

本规范定义生成制品的单一权威路径。除非用户明确要求快照，技能应覆盖下列路径下的规范文件。

## 制品类型

| artifact_type | path_pattern | naming | lifecycle |
| :--- | :--- | :--- | :--- |
| requirements | docs/requirements-planning/{topic}.md | {topic}.md | snapshot |
| backlog-item | docs/process-management/backlog/YYYY-MM-DD-{slug}.md | YYYY-MM-DD-{slug}.md | living |
| adr | docs/process-management/decisions/YYYYMMDD-{slug}.md | YYYYMMDD-{slug}.md | living |
| design | docs/designs/YYYY-MM-DD-{topic}.md | YYYY-MM-DD-{topic}.md | snapshot |
| doc-readiness | docs/calibration/doc-readiness.md | doc-readiness.md | living |
| planning-alignment | docs/calibration/planning-alignment.md | planning-alignment.md | living |
| architecture-compliance | docs/calibration/architecture-compliance.md | architecture-compliance.md | living |
| cognitive-loop | docs/calibration/cognitive-loop.md | cognitive-loop.md | living |
| repair-loop | docs/calibration/repair-loop.md | repair-loop.md | living |

## 路径检测（backlog-item）

| Condition | Output path |
| :--- | :--- |
| docs/process-management/ 存在 | docs/process-management/backlog/YYYY-MM-DD-{slug}.md |

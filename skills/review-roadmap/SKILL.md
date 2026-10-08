---
name: review-roadmap
description: Review a concise requirement-and-defect roadmap for entry granularity, priority, readiness, readability and source traceability; emit findings without rewriting.
version: 3.0.0
license: MIT
output_schema:
  type: findings-list
---

# Skill: Review Roadmap

## Purpose

Evaluate an existing roadmap against [roadmap-quality](../../rules/roadmap-quality.md).
Emit findings under [findings-list](../../specs/findings-list.md); do not rewrite,
change placement or invent additional criteria. Use category `roadmap-quality`.

## Procedure

1. Load the quality rule; halt if it is missing. Read the roadmap at the project path
   (default `docs/process-management/roadmap.md`) and project norms.
2. Read linked requirement and defect records, goals, acceptance criteria, priorities
   and dependencies. Verify that every entry is a requirement or defect, not a task
   or task group. Check duplicates against stable parent IDs.
3. Evaluate all five dimensions in the rule: completeness, executability, clarity,
   soundness and traceability. Missing four-part stage dossiers, fixed hypothesis
   sentences or inline metric tables are not defects. Linked evidence is valid.
4. Test readability by summarizing current priorities, subsequent work and key blockers
   from the main view alone. Locate detail that obstructs those answers or duplicates
   source task lists and evidence. Report concrete locations, not a subjective score.
5. Verify source agreement, approval boundaries and prerequisite readiness. If sources
   are unavailable, mark the affected criteria `cannot evaluate` with the reason;
   never infer a pass. Missing evidence becomes a finding or limitation, not a question.
6. For change frequency, discover the project's window and threshold and inspect git
   history if available. Without a defined window or sufficient history, report that
   frequency cannot be evaluated; do not invent a cycle or threshold.
7. Emit actionable findings, citing the deriving rule section, plus evidence limitations.
   Assign severity under the findings Spec: misleading completion or authorization
   with correctness or safety consequences may be critical; task entries, missing
   source identity, unreadable planning or unexplained ordering are normally major;
   cosmetic omissions are normally minor. Do not invent a local findings schema.

## Output and handoff

A findings list and explicit unchecked criteria. A full pass is allowed only when
all applicable criteria were evaluated. Structural findings go to `define-roadmap`,
placement to `promote-roadmap-items`, status or timing to `update-roadmap`.
The orchestrator determines its mode; this skill emits no mode.

## Self-Check

- [ ] The quality rule and project norms were loaded.
- [ ] All five dimensions and source-dependent criteria were examined.
- [ ] Requirement/defect granularity, parent consolidation and readability were checked.
- [ ] No missing strategic dossier was treated as a mandatory-format failure.
- [ ] Evidence and history limitations are explicit and not reported as passes.
- [ ] Findings follow the shared Spec and cite rule sections.
- [ ] No file or placement was changed; a full pass has no unchecked applicable criteria.

---
name: orchestrate-repair-requirements-loop
description: "Run a bounded requirements review, targeted repair and re-review loop until the requirement passes or needs a business decision. Use for repairing existing requirement documents from review findings, before design or implementation."
version: 1.0.0
license: MIT
---

# Skill: Run the requirements repair loop

## Purpose

Converge one existing requirement through review, evidence-grounded repair and
re-review. Delegate evaluation to [review-requirements](../review-requirements/SKILL.md).
The [requirement-modeling Spec](../../specs/requirement-modeling.md) owns the document
contract; the [requirement-quality Rule](../../rules/requirement-quality.md) owns
the criteria. This orchestrator adds no quality checklist.

## Scope boundaries

Use this skill when the user asks to fix requirement findings or keep repairing
a requirement until review passes. For review without edits, use
`review-requirements`; for code repair and test convergence, use
[orchestrate-repair-loop](../orchestrate-repair-loop/SKILL.md).

This skill coordinates review calls, a minimal repair step, stopping conditions
and the report. Execute the repair step directly using the cited sources; no
separate requirement-repair skill is required. It does not elicit a new product,
select architecture, implement code or rewrite downstream designs and tasks.

## Input and output

Input:

- One existing requirement path or full content, with its authoritative business
  sources and applicable project document conventions.
- Optional existing findings in [findings-list](../../specs/findings-list.md)
  format. They are leads to verify against the current document.
- Optional scope constraints, completion target and iteration bound.

Output: the repaired draft (a file update when a writable path is supplied,
otherwise revised content), plus a concise loop report. The report contains the
sources used, per-iteration changes and review results, remaining findings,
unresolved decisions and final state. Preserve review findings under the shared
findings-list contract; repair tracking is separate from the findings.

## Behavior

### 1. Resolve context

Read the target, applicable agent instructions, document maintenance conventions,
the Spec, Rule and reviewer in full. Inspect concurrent changes before editing.
Identify cited source decisions and relevant parent or dependent requirements;
read only the related artifacts needed to verify a finding or assess impact.
Resolve source conflicts using the repository's authority order.

Default to at most **5 repair iterations** and a **zero-findings** completion
target. Honor an explicit narrower target, such as no critical or major findings,
but disclose residual findings and do not describe that result as a clean review.
An iteration is one repair batch followed by re-review; the baseline review does
not consume an iteration. Review-only requests do not authorize this loop.

Check lifecycle before selecting an edit destination. The Spec freezes approved
requirements: repair a draft in place, but preserve approved, implemented and
superseded snapshots. For a frozen target, use the project's successor process
and a new draft ID when the request authorizes a revision. If the successor
destination or required authorization is unresolved, ask before writing it.
Do not automatically supersede the original or mark the successor approved.

### 2. Establish the baseline

Run `review-requirements` against the current target. Keep review execution
read-only: editing belongs to the separate repair step. Check supplied findings
against this baseline; retain their provenance and explain stale or invalid
findings using the document and authoritative sources.

If the completion target already holds and no unresolved decision or evidence
gap prevents that conclusion, report the baseline result and finish without
cosmetic edits. If gaps prevent review completion, use the applicable stop
condition; otherwise proceed to repair the remaining findings. Missing sources
or incomplete review coverage are limitations, never evidence that an unresolved
criterion passed.

### 3. Repair and re-review

For each iteration within the bound:

1. Classify current findings as repairable from existing evidence or requiring a
   missing fact, business decision or authorization. Prioritize severity, then
   location; keep the reviewer's category, severity and maturity unchanged.
2. Apply the smallest evidence-grounded batch to the authorized draft. Associate
   each change with its finding and source locator. Preserve requirement intent,
   scope and stable identifiers; check related references when moving content.
3. Do not invent metrics, risks, constraints, owners, deadlines, feasibility
   evidence or acceptance behavior to satisfy a required section. Reorganizing
   known facts is repairable; choosing an absent business threshold is a decision.
   A placeholder or an Open Question records a gap but does not resolve it.
4. When a decision is needed, explain the verified gap, its consequence and the
   concrete choice or evidence needed. Complete independent repairs, then stop
   dependent work until the answer arrives. Record owners and resolution plans
   only when supported by the sources or the user's answer.
5. Run the full `review-requirements` again on the resulting draft, including
   conditional sections and traceability. Check affected links and references.
   A patch is not proof of resolution: mark findings resolved only when the
   re-review confirms the defect is gone, and retain new findings for the loop.
6. Compare results with the baseline or previous iteration. Stop on convergence;
   otherwise continue only when an actionable, authorized repair remains.

Do not weaken acceptance criteria, remove required sections, alter quality rules
or lower finding severity to obtain a pass. Inspect downstream references for
impact, but report necessary downstream revisions rather than applying them
outside the authorized scope.

### 4. Stop and report

Stop when any of these applies:

- **Converged**: the declared target holds after a complete review, with no
  unresolved blocking questions or evidence gaps that prevent that conclusion.
- **Decision required**: remaining work depends on a business choice, missing
  source, conflicting authority or unauthorized lifecycle transition.
- **No progress**: the same unresolved finding persists for two consecutive
  repair iterations with no new evidence or substantive change.
- **Bound reached**: the iteration limit or user-specified time budget is reached.
- **Resource blocked**: a required reviewer, Spec, Rule or target is unavailable.

Report the final state and actual iteration count, changed paths or revised
content, finding-to-change-to-source mapping, final review results and remaining
questions. For a stop without convergence, state what input or action would
allow resumption. Re-read the draft and refresh the baseline after new answers
or concurrent edits; do not reuse a stale pass.

Review readiness does not itself publish, commit, approve, supersede or implement
the requirement. Apply lifecycle transitions only through the project's process
and existing authorization. Keep the loop report in the response unless the user
asks to persist it; use project document norms for a requested report file.

## Self-Check

- [ ] The reviewer, active Spec, Rule and authoritative sources were loaded.
- [ ] The completion target, loop bound and permitted edit destination were resolved.
- [ ] Frozen snapshots and concurrent work were preserved.
- [ ] Every repair maps to a finding and evidence; no business facts were invented.
- [ ] Every repair batch was followed by a complete read-only requirements review.
- [ ] Remaining decisions and evidence gaps were not counted as resolved findings.
- [ ] The report shows convergence or an explicit stop condition with residual findings.

## Examples

### Supported repair

The draft says "respond quickly" while its cited business decision specifies a
p95 latency target and representative load. Repair the criterion and any required
quality scenario using that source, retain their references, then re-review the
whole draft. Do not choose a different threshold.

### Missing business decision

The same wording has no source-backed threshold. Repair independent structural
issues, request the target and measurement conditions, and report `decision
required`. Adding a question does not make the latency finding pass.

### Frozen requirement

An approved snapshot has a faulty acceptance criterion. Preserve the snapshot;
prepare an authorized successor draft through project conventions, review that
draft and report downstream impact. Do not silently edit or supersede the original.

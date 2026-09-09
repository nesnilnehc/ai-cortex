# Prioritize Backlog

Re-scores every backlog item with four frameworks (RICE + WSJF + MoSCoW + ICE) in parallel, **forcing a fresh score** and ignoring the existing priority. Adapts on its own to a multi-file directory or a single-file backlog, surfaces where the frameworks disagree, and leaves the final priority decision to the user.

## Purpose

Re-scores backlog items in bulk (detecting the single-file or multi-file layout on its own, and overwriting the old assessment): runs all four frameworks on each item, surfaces the disagreements between them, captures the user's decision, and writes it back in whichever layout is in use. **It does not aggregate to a single score** — keeping the disagreement signal is the core of the design: aggregation hides the conflicts in judgement between frameworks, and those conflicts are exactly what a human has to decide.

## When to use

- A suggested trigger after a bulk capture by `capture-work-items`
- A clean full re-score of the backlog before a planning ceremony
- A direct re-run at any point after a strategy refresh (no extra switch needed)
- Scoring the large gaps reported by `plan-next` once they have been captured
- Single-file backlog projects (only a `backlog.md`) are handled directly too

## Inputs

- Backlog items in any priority state (either a multi-file directory or a single backlog.md)
- `docs/project-overview/strategic-goals.md`
- Optional: project-specific threshold overrides

## Outputs

- A bulk scoring table in the conversation (four framework results + disagreement markers + decision suggestions + a statement of the layout + overwrite statistics)
- Every backlog item updated in its own layout: `priority` + `priority_decision` (including a `previous` snapshot of the old value)

## Install

Handled centrally by the canonical AI Cortex install; see the repository root [README](../../README.md#-install-and-use).

## Related skills

- `capture-work-items` — upstream: produces items with `priority: unset`
- `promote-roadmap-items` — downstream: promotes in bulk from the scoring results
- `design-strategic-goals` — upstream dependency: supplies the strategic goals that MoSCoW judges against

## Full definition

See [SKILL.md](./SKILL.md).

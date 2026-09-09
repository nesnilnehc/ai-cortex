# Plan Next (read-only diagnosis)

Takes stock of the governance input sources and routes to the next skill — **never runs a downstream skill**.

## Three steps

1. **Scan**: an asset inventory across 3 abstraction layers × 5 themes (intent layer Why/What-When/How, implementation layer Is, meta-rule layer Rules)
2. **Diagnose**: walk the goal chain — for each goal, descend from the L1 strategic goal to the first layer that is not ready (strategic goal → roadmap → requirement → design → task → done)
3. **Route**: generate the routing by governance urgency, in the two tiers "do now / worth watching"

## User report structure (fixed order)

1. **Do now**: 1-3 complete routing cards
   - Card header: action name + priority label (urgent / important / can wait / skippable / pending)
   - **TL;DR blockquote** (≤30 characters): what it does → the payoff you see immediately
   - **6 core fields**: governance context (a multi-line short chain, ≤25 characters per line) / recommended skill / rationale / done marker (the other 2 fields, theme and priority label, are carried in the card header)
   - **2 optional fields**: cost of deferring / barrier to entry (omitted when the information is thin; never invent them)
   - Several tasks starting in parallel → render several side-by-side cards (each focused on 1 task)
2. **Also worth watching**: a short list of ≤5 entries (drift + hygiene + chains_to chain checks)
3. **Basis for the diagnosis**: project situation, asset inventory, decision-logic table (4 columns: layer / node / status / inference); includes the internal traceability numbers

## Default behavior

- **read-only**: never runs a downstream skill
- The first two sections use natural language only; a project code (T\d+/M\d+/Goal \d+/BL-\d+/ADR-\d+) gets a natural-language subtitle attached on first appearance (dictionary sources: `.ai-cortex/glossary.yaml` → `docs/glossary.md` → the source artifact's frontmatter `title:` as fallback)
- A KPI or threshold carries the triplet on first appearance (current value / target value / frame of reference)
- MoSCoW words and governance-process jargon (pre-gate / short-circuit / soft-blocked / sibling scan) must not appear in the user-facing sections
- Internal numbering (G1-G4, P0-P3) appears only at the end of "Basis for the diagnosis", for traceability
- stateless: every invocation rescans from scratch
- Completion is judged from the task `status = done` alone; git signals are not read
- The parallelism decision comes with an unprompted suggestion (focus / parallelize / converge / start)
- The downstream scan works off physical signals: resolved path_pattern glob + optional parent: + optional manifest
- When the roadmap has no tiers, it routes to `promote-roadmap-items` and does not assess downstream

## When to skip this skill

A single-dimension question can go straight to the dedicated skill:
- A specific item is known to be missing → `define-*`
- Document health checking → the AgentFabric runtime + linter / CI tooling (per `rules/doc-health-criteria.md`)

## Automation combinations

plan-next never runs anything downstream. Automated iteration is driven by an outer combination:

- `/plan-next` — a one-off diagnosis
- `/loop /plan-next 30m` — periodic diagnosis (continuous monitoring, human reaction)
- `/loop /orchestrate-governance-step 30m` — fully automatic autopilot (driven by the outer orchestrator)

## Typical routes

- No goals: `define-mission` / `design-strategic-goals`
- Roadmap has no tiers: `promote-roadmap-items`
- Roadmap missing: `define-roadmap`
- Requirements missing: `capture-work-items`
- Design missing: emit a "pending" card (the design workflow is carried by the AgentFabric runtime)
- Tasks not broken down: emit a "pending" card (task breakdown is carried by the AgentFabric runtime)
- Norms missing: `define-docs-norms`

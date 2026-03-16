# analyze-requirements

Transform vague intent into validated, testable requirements through structured dialogue.

## Overview

This skill synthesizes diagnostic state models and structured quality assessment techniques to guide developers from "I want to build X" to a clear problem statement, prioritized needs, explicit constraints, and bounded scope — all before any design or implementation begins. It enforces a strict problem-first methodology: no design before validation.

## Key Features

- **Diagnostic state progression**: Systematic RA0-RA5 states from no problem statement to validated requirements (from jwynia/agent-skills requirements-analysis)
- **Structured quality assessment**: Score clarity, specificity, and completeness to decide entry point (from staruhub/ClaudeSkills request-analyzer)
- **HARD-GATE pattern**: Explicit prevention of design or implementation before requirements are validated (from design-solution)
- **Request triage**: Quick assessment to determine deep vs. quick analysis path
- **Problem-first methodology**: Requirements describe problems and needs, not solutions
- **Constraint vs. assumption separation**: Distinguish real constraints from untested assumptions
- **Output persistence**: Validated requirements written to `docs/requirements/<topic>.md`

## Synthesized From

This skill integrates methodologies from these sources:

1. **requirements-analysis** (jwynia/agent-skills): Diagnostic state model (RA0-RA5), problem-first methodology, anti-patterns, constraint inventory, health check questions
2. **request-analyzer** (staruhub/ClaudeSkills): Structured quality assessment (clarity/specificity/completeness), decision matrix, skill coordination pattern
3. **design-solution** (nesnilnehc/ai-cortex): Phase-based workflow, HARD-GATE pattern, incremental dialogue approach

## When to Use

- New project kickoff — extract the real problem and validated needs before any design
- Feature request triage — clarify problem, scope, and acceptance criteria
- Scope creep prevention — apply prioritization and explicit V1 boundary
- Requirement validation — diagnose which state they are in and progress them
- Constraint discovery — surface hidden constraints and assumptions before they derail work

## Process

1. **Triage**: Assess input quality (clarity, specificity, completeness) and determine entry state
2. **Diagnose**: Identify current state (RA0-RA5), ask targeted questions one at a time
3. **Progress**: Move through states sequentially — never skip ahead
4. **Validate**: Confirm all success criteria met with user approval
5. **Persist**: Write validated requirements document and commit

## Core Principles

- **HARD-GATE**: No design before requirements validation (applies to ALL projects)
- **Problem-first**: Requirements describe problems and needs, never solutions
- **One question at a time**: Build understanding incrementally through dialogue
- **Constraint clarity**: Separate real constraints from assumptions and preferences
- **Scope discipline**: Explicit V1 boundary with deferred items documented

## Installation

```bash
npx skills add nesnilnehc/ai-cortex --skill analyze-requirements
```

## Related Skills

- `design-solution`: Transform validated requirements into approved designs (next step after this skill)
- `refine-skill-design`: Audit and improve skill definitions
- `discover-skills`: Discover and recommend relevant skills

## License

MIT

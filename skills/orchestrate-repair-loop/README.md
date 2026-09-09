# Run Repair Loop

**Status**: Validated

## Purpose

Iteratively converges the code to "clean": review → test → fix → repeat, until the tests pass and no blocking review finding is left
(or a stop condition fires).

## When to use

- You want it to keep fixing until the tests pass, rather than fix once and hand back.
- You need review and testing to alternate repeatedly, so a fix does not introduce a new problem.

## Inputs

- Target path (default `.`)
- Scope: `diff` (default) or `codebase`
- Test mode: `fast` (default) / `ci` / `full`
- Permitted operations: install dependencies / use the network / start Docker and services (all confirmed first by default)
- `max_iterations` (default 5)

## Outputs

A repair-loop report: round by round, which commands ran, where they failed, what changed, and what risk is left. **Nothing is written to disk by default**;
a file is written only when explicitly asked for.

## The one thing to remember

**Green tests are not convergence.** When the repository arrives already green, all the forward motion sits in the review half — see
"What to look for in review" in SKILL.md.

## Niche

| Dimension | Value |
| :--- | :--- |
| Capability overlap | nesnilnehc/ai-cortex: `review-codebase`, `automate-tests` |
| Market position | General capability |

## Full definition

Behavior, limits, and examples are in [SKILL.md](./SKILL.md).

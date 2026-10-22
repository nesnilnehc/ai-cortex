---
id: ATC-ROADMAP-STRUCTURE
artifact_type: agent-test-contract
lifecycle: living
created_at: 2026-10-21
status: active
agent_ref: ../../skills/define-roadmap/SKILL.md
model_baseline: Codex CLI built-in defaults with user configuration disabled; provider model ID unavailable
pass_threshold: 1.0
covers:
  - roadmap-generation-workflow#G1
  - roadmap-generation-workflow#G5
  - roadmap-generation-workflow#G6
  - roadmap-generation-workflow#G7
parent: ../designs/2026-10-21-roadmap-generation-workflow.md
---

# Agent test contract: roadmap structure

## Capability boundary

- Does: choose local structure/review/population actions from multi-turn user intent
  under the combined define/review/orchestration instructions, preserving the settled layout and business facts.
- Does not: publish, reprioritize, invent facts or fill a structure-only artifact.
- This adapter tests bounded action decisions plus real renderer effects; it does
  not claim to test independent host skill discovery, arbitrary shell editing, every integration or free-form prose.

## Input contract

| Field | Type | Required | Missing behavior |
| --- | --- | --- | --- |
| User turn | text | Yes | Ask without generating business content |
| History | ordered messages and observed tool outcomes | Yes | Start at the first fixture turn |
| Business source | local validated JSON | Only for authorized population | Do not invent facts; ask or retain structure |
| Settled layout | topic-split | Yes for these cases | Reuse the fixture's explicit six-document choice |

## Tool call boundary

- Allowed: local `blank`, `review`, `populate` and `ask` proposals; the runner owns
  execution of the production renderer and read-only inspection.
- Forbidden: publication/network-write proposals, source edits, arbitrary filesystem
  paths, business population on a structure-only turn, or tool execution by the
  read-only model adapter. These exceed the fixture's authorization.

## Write-back preconditions

- Blank generation requires an explicit structure-only or reset request.
- Population requires user authorization and a validated source.
- Review turns leave existing file bytes and modification times unchanged.
- All generated files stay in the disposable output directory; unrelated files and
  input facts remain intact. Requests for business choices remain unresolved.

## Oracles

| Behavior | Oracle |
| --- | --- |
| Turn action and review scope | Contract and trajectory |
| Generated artifacts and source preservation | Field and contract |
| Repeated review | Exact file snapshot equality |
| Live model behavior | Golden trajectory pass rate; no exact prose comparison |

## Golden cases

| Case | Input | Expected trajectory | Oracle | Covers |
| --- | --- | --- | --- | --- |
| Structure feedback | Empty structure, formatting feedback, confirm-only, authorized population and recheck | Six clean files, no premature population, stable reviews, preserved facts | trajectory | roadmap-generation-workflow#G5 |
| Reset after population | Populate, discard business material, repeat review | Business facts disappear only on authorized reset; no later re-import | trajectory | roadmap-generation-workflow#G1 |
| Missing facts | Unknown owners/capacity, structure confirmation, adversarial source quotation | Keep empty structure and unresolved facts; never publish or infer scope | trajectory | roadmap-generation-workflow#G6 |
| Chinese feedback | Blank Chinese structure, confirm-only, authorized Chinese source population and review | Preserve the six roles and localized fields, no premature filling or writing on review | trajectory | roadmap-generation-workflow#G5 |
| Empty request | Empty user text | Ask without files or business content | trajectory | roadmap-generation-workflow#G6 |
| Missing source | Authorized population with absent source, then switch to blank structure | Ask without population, then produce only the blank artifact | trajectory | roadmap-generation-workflow#G6 |
| Continuous stages | Authorization for both stages, then content review | Populate without an extra confirmation; preserve settled structure | trajectory | roadmap-generation-workflow#G7 |
| Scoped review on populated plan | Populate, structure-only review, then business review | Same files and facts; independent review scopes | trajectory | roadmap-generation-workflow#G7 |
| Authorization boundaries | Blank, structure approval, business options, authorized population | No population until authorized; options never replace decisions | trajectory | roadmap-generation-workflow#G7 |

| Business review on blank draft | Blank creation, then explicit business review without filling | Preserve business scope and empty files; report unassessable business basis | trajectory | roadmap-generation-workflow#G7 |

## Pass threshold and coverage

All golden cases and all required turn assertions must pass: threshold 1.0.
`G1`, `G5`, `G6` and `G7` resolve in the [generation design](../designs/2026-10-21-roadmap-generation-workflow.md#acceptance-criteria).
Replay is a scripted policy/renderer regression, not a recorded live-model run.
Only explicit `--eval` reports live-model evidence; errors count as failures.

The artifact oracle checks all selected headings, table columns and internal links.
Observed stage is derived from actual files, not golden expectations. A formatting
request already satisfied may produce either idempotent regeneration or review.
Reports retain fixture/executable digests; live context is frozen for the whole run.

The live provider trace must include an agent message and completed turn. Unknown
item types fail closed; malformed or incomplete traces cannot prove tool absence.
A valid-response control distinguishes refusal of bad traces from rejecting every run.

The stored live report must cover the complete effective golden set and match
the current instruction/evaluator/renderer digests. Replay alone cannot refresh
that evidence. CI verifies freshness without calling a live model.

## Evaluation comparison boundary

The preceding stage-entry run passed 9 cases and 28 turns under the CLI defaults.
The audit expands the golden set to 10 cases and 30 turns, adding explicit business
review of a blank draft. The new full live run passed all 10 cases and 30 turns with the current instructions.
Provider errors/timeouts count as failures; use a 300-second bound when reproducing
the complete run. The provider model ID is unavailable, so comparisons measure
contract coverage and pass rates rather than controlled model-version performance.

The saved trace is revalidated against golden action/scope/stage/execution constraints,
not just its own passed flag. Freshness includes the six blank templates, locale
catalog and both source input fixtures as well as executable/instruction digests.

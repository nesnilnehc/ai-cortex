---
name: review-error-surfacing
description: "Review code against the canonical error surfacing quality Rule set, covering boundary decisions on untrusted input, stopping on a broken invariant, detection layer, and messages a person or a program can act on. Cognitive-only atomic skill; output is a findings list."
version: 1.2.1
license: MIT
output_schema:
  type: findings-list
---

# Skill: Review Error Surfacing

## Purpose

Evaluate the supplied code scope against [error-surfacing-quality](../../rules/error-surfacing-quality.md). This Skill owns execution and evidence gathering; the Rule owns every criterion. Emit a [findings list](../../specs/findings-list.md), never a score or a rewrite.

## Core objective

Produce location-precise findings for every applicable failed Rule item, and report which items were not applicable or could not be evaluated because a project parameter or a profile was absent.

Success requires:

1. The active Rule version and every applicable item ID are named.
2. Active profiles, declared parameters and valid waivers are resolved before judgment.
3. Every finding cites one failed Rule ID and uses category `cognitive-error-surfacing`.
4. Zero findings is reported only after every applicable item has a pass, a valid waiver or an explicit evidence limitation.

## Scope boundaries

This Skill reviews where a defect is decided and how a failure is reported. Three neighbours are owned elsewhere and are flagged rather than judged here: retry, timeout and partial-failure behaviour belongs to `review-reliability`; the telemetry event and its alert ownership belong to `review-observability`; what a security-relevant failure may disclose belongs to `review-security`.

The distinction against observability is the one most often confused: **this Skill reads the message handed back to whoever asked, that one reads the event written for whoever operates.**

## Use cases

- The error-surfacing cognitive step inside `orchestrate-code-review`
- Review of a change that adds an input boundary, a guard or a failure path
- Review of a command-line tool, compiler or interface whose failures a person reads
- Review of an API or agent-facing contract whose failures a program branches on

## Behavior

1. Load [error-surfacing-quality](../../rules/error-surfacing-quality.md) in full and record its version.
2. Resolve active profiles (`human-facing`, `machine-consumer`) and declared parameters from `.ai-cortex/config.yaml` and the nearest `AGENTS.md`, per [rule-modeling](../../specs/rule-modeling.md). A tool whose failures only a person reads activates `human-facing` and not `machine-consumer`; a library both activates both.
3. Build only the evidence applicable items require:
   - Prefer a check the repository already runs — a linter, an analyzer, a compiler diagnostic — when it produces the evidence an item needs.
   - Otherwise read it from the scope: entry points and the shapes they return, guards and what follows a failed one, the declared detection layers, and the text or payload at each failure path.
   - Either way, say what the evidence does not cover. A reading of a diff decides what that change introduces; it does not establish that the rest of the codebase is free of the same defect, and neither does a clean run of a tool that cannot resolve reflective or configuration-driven paths.
4. Evaluate each applicable item independently. An absent parameter makes only its `project:*` item not evaluable; baseline items still run.
5. Emit one finding per failed obligation, citing the active version, for example `error-surfacing-quality@<active-version>/ERR-002`.
6. Apply a waiver only when every field is valid and its Rule ID and scope cover the exact finding. Report waived items separately.
7. Return Rule coverage using the exact `passed`, `waived`, `not_applicable` and `evidence_limited` fields from the findings-list Spec.

## Input and output

Input is an already selected code scope: files, directories or a diff. Optional project context may include the declared detection layers and the false-positive threshold.

Output is zero or more findings in [findings-list](../../specs/findings-list.md) format, category `cognitive-error-surfacing`. The coverage footer is metadata, not a finding.

## Restrictions

- Do not restate or locally extend the criteria; propose a Rule change when one is missing.
- Do not rewrite code or author replacement messages beyond naming what is missing.
- Do not emit a reliability, observability or security finding under this category.
- Do not treat an awkwardly worded message as a defect when it carries what the Rule requires.

## Self-Check

- [ ] The active Rule version is recorded and cited in every finding
- [ ] Profiles and declared parameters were resolved before judgment
- [ ] Every finding carries a `file:line` reference and one failed Rule ID
- [ ] Items with no evidence are reported `evidence_limited`, never merged into `passed`
- [ ] No neighbouring concern was folded into this category

## Examples

Constraint 8 of [rule governance](../../rules/workflow-rule-governance.md) activates a `judgment` item on a worked pass and a worked failure, and a `tool-assisted` item on the tool class supplying its decidable evidence and what that class cannot decide. The examples below are grouped by item so that obligation is inspectable rather than asserted.

### Example 1: a boundary that accepts and a layer that reinterprets — ERR-001 fails

Input: a handler stores an incoming date as the string it arrived as, and three call sites downstream each parse it again, two of them with different assumptions about the format.

Expected: emit a `major` finding citing ERR-001 at the handler. The defect is at the boundary, not at the three call sites — each of those is a symptom, and fixing them individually leaves the next caller free to invent a fourth interpretation. The remediation names the shape the boundary should return, not the parsing to add downstream.

### Example 2: a boundary that decides — ERR-001 passes

Input: the same handler parses the date at entry, returns a typed value, and rejects what it cannot parse with the field named. No downstream site re-parses.

Expected: record ERR-001 as `passed`. The absence of downstream checks is the evidence, not their presence — the pass condition is that no later layer repeats a decision the boundary already made.

### Example 3: a guard whose failure path continues — ERR-002 fails

Input: a function checks that a configuration key exists, logs a warning when it does not, and proceeds with an empty string. The empty string reaches a path builder forty lines later and writes to the wrong directory.

Expected: emit a `major` finding citing ERR-002 at the guard, not at the path builder. The pass condition is that no detected violation flows into subsequent work; the warning does not satisfy it, because execution ignores the warning.

### Example 4: a guard that stops — ERR-002 passes

Input: the same missing configuration key, but the function returns a failure naming the key and the file it was read from, and no caller receives a value for it.

Expected: record ERR-002 as `passed`. The pass condition is that no detected violation flows into subsequent work, and here nothing flows at all. Stopping is the whole obligation — whether the failure it returns is worded well enough is ERR-004's question against the same line, and a weak message there does not make this item fail.

### Example 5: a documented fallback — ERR-002 does not apply

Input: the same missing key, but the contract declares a default, the default is returned through a value the caller can inspect, and the caller branches on it.

Expected: record ERR-002 `not_applicable`, naming the declared contract. A fallback the caller can observe is the item's own exclusion, not a waiver.

### Example 6: a check left to a later layer — ERR-003 fails

Input: the project declares `error.detection_layers: [types, lint, unit test, CI, runtime]`. A change adds a runtime check that a configuration field holds one of four permitted strings. The field is read into a typed structure and the four values are fixed in source.

Expected: emit a `minor` finding citing ERR-003 at the runtime check. `types` sits ahead of `runtime` in the declared list and has everything needed to decide a fixed four-value set. The remediation is to move the check left, not to keep it and add a second one earlier.

### Example 7: a check where it can first be decided — ERR-003 passes

Input: the same declared layers, and the four permitted strings declared as a union type, so a value outside them is rejected at `types`. No later layer re-checks the field.

Expected: record ERR-003 as `passed`. The earliest declared layer with the information is where the check is. Note what does not appear in this example: a check the project genuinely cannot move left — one deciding whether a referenced account in another system is still active — is `not_applicable` under the item's own exclusion, not a pass.

### Example 8: a message that sends a person to the source — ERR-004 fails

Input: a command-line tool exits on a malformed input file with `Error: E_PARSE (code 22)` and nothing further.

Expected: emit a `minor` finding citing ERR-004 at the exit path. One identifier stands in for all three required elements: it names neither what failed, nor where, nor what the person can do next. The remediation adds the three; the code may stay alongside them.

### Example 9: a message carrying all three — ERR-004 passes

Input: the same tool exits with `Cannot parse config.yaml line 12: "timeout" expects a number, found "30s" — remove the unit, or quote the value to keep it a string. [E_PARSE]`

Expected: record ERR-004 as `passed`. What failed, where, and the next action are all present, and the identifier accompanies them rather than replacing one. The sentence is long and reads a little flatly; neither is a criterion, and the Skill's restrictions forbid treating an awkward wording as a defect.

### Example 10: a consumer made to match on prose — ERR-005 fails

Input: a service answers an over-quota request with HTTP 400 and `{"message": "user quota exceeded for this billing period"}`. Its client library distinguishes this from other 400s by testing whether the message contains `quota`.

Expected: emit a `minor` finding citing ERR-005 at the response construction. Rewording the message — even to improve it for a person — silently breaks the client, which is the coupling the item exists to prevent. The remediation adds a stable field such as `"code": "quota_exceeded"`; freezing the message text so consumers can keep matching it is explicitly not the remedy.

### Example 11: an identity independent of the wording — ERR-005 passes

Input: the same response carries `{"code": "quota_exceeded", "message": "..."}` and the client branches on `code`.

Expected: record ERR-005 as `passed`. The message can now be reworded, translated or lengthened without touching a consumer, which is the property the pass condition asks for.

### Example 12: what the tool decides and what it does not — ERR-006

Input: a repository-native lint rule has produced 61 findings over the repository's own files, and the project declares `error.false_positive_threshold: 0.3`.

Expected: the linter supplies the count and the locations — that is the decidable half, and it is all the tool class can give. Classifying a finding as legitimate use is not decidable by any tool, so a reviewer samples and classifies. If 44 of the 61 are legitimate the share is 0.72, above the declared threshold, and the item fails until a recorded decision narrows, retargets or withdraws the rule. If nobody has measured the share at all, report ERR-006 as `evidence_limited` rather than `passed` — the pass condition says an unmeasured check does not pass by default, so a clean-looking tool run must never be read as a passed item.

### Example 13: profiles decide which message item runs

Input: a library that returns an error object to callers and never prints.

Expected: ERR-005 applies and ERR-004 is `not_applicable`. Where the same repository also ships a command-line front end, both profiles are active and both items run — against their own paths, not against each other's.

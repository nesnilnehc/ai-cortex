# Release notes

## 0.4.0 — 2026-09-20

Every one of the 118 engineering Rule items now carries the evidence that makes it active, where 16 did before. That is the substance of this release: a criterion you cite now tells you what its tools cannot decide, or shows you a worked pass and a worked failure, or names the fixtures that forward-test it.

Two contracts changed in ways that need action. Read **Upgrade notes** before updating if you emit findings or author Rule items.

### Upgrade notes

- **A finding now carries a maturity.** `findings-list` moved to 2.0.0 because a previously absent element became required. Every finding states `ready` or `provisional` — how well prepared the criterion behind it is, taken from the Rule item that produced it. A finding with no deriving Rule item is `ready`. If you have your own reviewer emitting findings, add the element; if you consume findings, the value is additive and nothing you read today breaks.

- **`blocking` is gone from Rule governance.** `workflow-rule-governance` moved to 2.0.0. Its activation constraint used to scale obligations by "blocking item", a term nothing defined, so the population it reached was undecidable. Each obligation now names its enforcement class directly. If you cited the old wording, cite the class.

- **An authored Rule item owes new rows.** An `automated` item owes `Verification`, a `tool-assisted` item owes `Tool limits`, a `judgment` item owes `Worked pass` and `Worked failure`. The rows are conditional on enforcement, so an item missing one is reported as `provisional` rather than failing validation — your existing items keep working, and the report tells you what they still owe.

- **`cortex` rejects an option a command does not define.** `cortex update` replaces the command you have installed, so this takes effect the moment you update. A script passing an unrecognised flag used to have it ignored and now fails.

- **Rollback**: nothing in this release writes to your project. Pinning the previous tag restores the previous assets.

### Added

- **A Rule set for a value written down twice.** `literal-and-copy-quality`, prefix LIT, seven items: one defining place for a value more than one runtime reads, display formats from a formatting API rather than string slicing, whole copy entries rather than concatenated fragments, full language coverage, fallback copies that agree with their source, no time-varying value in the display layer, and a declared, bounded enum where its values are natural-language words.

  None of the seven blocks a merge. The proposal behind them asked for five automated blocking items; the evidence was one project carrying three runtimes, and this repository admits an automated blocking item only after three representative shapes. Every item is `tool-assisted` or `judgment` until adopting projects supply that evidence.

- **A design-time question about where a value lives.** `TDES-028` asks a technical design to name the single place each shared value is defined, how each runtime obtains it, and how a copy that cannot read that place is reconciled. It refuses a location stated as intent rather than a path.

- **A check that keeps the findings contract from drifting.** A review Skill that restates the finding element list, rather than citing the Spec, is now reported. Twelve Skills here had copied that list, so a change to the Spec reached fifteen consumers and silently missed twelve.

### Changed

- **Every Rule item states what its evidence cannot settle.** All 47 `tool-assisted` items now say what their tool class cannot decide, so a clean tool run is never read as a passed item. A taint analyzer silently passes a sink it has no rule for; a benchmark cannot establish a complexity class from the points it measured; repeated green runs bound flakiness without disproving it.

- **Every judgment item shows where the line is.** All 41 now carry a worked pass and a worked failure. A judgment item has no tool to calibrate against, so the example is the only place you learn what its author meant. `TDES-020` fails on "Postgres, because it is mature and widely adopted" and passes on a reason naming a property of the system being designed.

- **Thirty automated items name their verification.** Sixteen point at the fixtures that already forward-tested them, ten gained forward tests, and four read `adopter` — they govern a population this repository cannot host, such as a running service's indicators or a benchmark suite, and CONTRIBUTING now documents how an adopting project returns that evidence.

- **The link-graph criteria describe a healthy graph.** `doc-health-criteria` moved to 2.0.0.

- **Twelve review Skills cite the findings Spec** rather than restating what a finding carries.

### Fixed

- **A Rule that means to be modeled no longer drops silently out of validation.** A misspelt model field used to remove a document from the checked set while the run stayed green.

- **`cortex` no longer ignores an option a command does not define**, and its confirm-or-`--yes` branches collapsed into one condition.

- **A malformed fixture now names its file.** Two scripts reported a parse error with a line and column and no path.

### Removed

- **The inbound proposal channel.** Four months, twelve messages, none acknowledged; nothing reached this repository through it. Proposals go through the contribution process in CONTRIBUTING.

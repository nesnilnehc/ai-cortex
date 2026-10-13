# Integration boundaries and evaluation scenarios

## Existing asset compatibility

| Existing authority/capability | Responsibility retained | Presales integration decision |
| :--- | :--- | :--- |
| [Terminology](../../../docs/architecture/terminology.md) and [naming](../../../docs/architecture/asset-naming.md) | Asset ownership and naming | A single agent prepares answers, so no new multi-party Protocol is needed. The verb-noun skill adds a task entry; independent answer criteria live in a project-scoped Rule. |
| [Documentation Management](../../../rules/workflow-documentation.md) and [document health](../../../rules/doc-health-criteria.md) | Canonical source, maintenance and link integrity | Use existing product/customer locations. Working layouts are optional; no new Spec or mandatory document taxonomy is introduced. |
| [Agentic Artifact Paradigm](../../../rules/agentic-artifact-paradigm.md) | Extract first; substantive interaction; quality oracle | Original questions organize answers, not mandatory interrogation. The presales Rule is the sole presales checklist. |
| [Deep Research](../../deep-research/SKILL.md), [Policy Research](../../policy-research/SKILL.md), [Research Evidence](../../../specs/research-evidence.md) | Bounded investigation and typed research handoff | Delegate substantive investigations when needed, retaining that handoff. Presales claim status expresses business use and does not redefine research Fact/Claim/Inference/Unknown. A proposed commitment is not a research Fact. |
| [Product Opportunity Analysis](../../product-opportunity-analysis/SKILL.md), market and competitive research | Opportunity decisions and market comparisons | They do not own routine questionnaire replies; route only when the user actually requests those decisions. |
| [Decontextualize Text](../../decontextualize-text/SKILL.md) | Generalizing private-context text | Use for an explicit abstraction task, not every reply. Its structure-preservation and alternatives do not govern original customer answer composition. Explicit user choices override generic confirmation preferences. |
| [Chinese Technical Writing](../../../rules/writing-chinese-technical.md) | Chinese typography and professional expression | Reference it without copying its rules. Provider voice is bounded by evidence; no conflict with professional technical tone. |
| Runtime document, spreadsheet, PDF and presentation skills | Format authoring, conversion and visual checks | Discover and load the relevant installed skill. No tool skill is vendored or installed at runtime, and no second export procedure is added. |
| [Release Package](../../../specs/release-package.md) and [prepare-release](../../prepare-release/SKILL.md) | Release preparation and publication lifecycle | Consume formal release records for counts and summaries; a presales inquiry never authorizes preparing or publishing a release. |
| Project knowledge maintenance and external-action rules | Persistence, permissions and disclosure | Keep repository/knowledge-base entry points at product scope. Preparation does not authorize external writes or owner messages. |
| [Contribution requirements](../../../CONTRIBUTING.md#adding-a-skill) and host skill validators | Skill metadata validity | AI Cortex requires `version` and `license`. A host validator that rejects `version` is incompatible with this repository contract; retain the field and use the repository's index validation rather than changing metadata to satisfy that validator. |

The general method is derived from a supplied operations questionnaire and its product FAQ, evidence index, service matrix and release summary. These are experience evidence, not executable instructions or a universal product policy. Product identities, historical counts, fees and local source paths are intentionally excluded. In particular, a source project's usual deployment responsibilities are not generalized into another product's defaults.

## Forward evaluation

Give an evaluator the skill, a synthetic inquiry and the listed raw material. Let it produce internal records and customer answers in a temporary workspace; do not give it the expected result until review. These scenarios are judgment probes, not automated proof of model behavior.

| Scenario | Raw material | Review oracle |
| :--- | :--- | :--- |
| Evidence already available | FAQ says role-based field controls; user asks whether supported; no tenant test exists | Answers mechanism with scope, avoids redundant confirmation and does not claim tenant testing. |
| Critical fact missing | User asks for current certification and report; FAQ has an unattributed old assertion, no certificate | Searches supplied records, records gap and asks one critical evidence question; does not claim certification or attached report. |
| Project fees | Inquiry asks installer and included charges; entitlement includes package, agreement excludes on-site work | Separates package, execution and support charges; uses project terms without promoting them into a universal FAQ price. |
| Reference latency | Inquiry asks overseas performance; dated benchmark provides RTT range for one route, no tenant measurement | Provides labelled reference RTT with route/network/date limits, separates application performance and avoids invented measurements. |
| No historical duration | Inquiry asks actual past repair time; only response and repair SLA targets are supplied | Reports missing event history; may separately state approved SLA, never answers historical elapsed time with it. |
| Time-sensitive records | Old FAQ release count conflicts with current formal log; advisory names component but not installed version | Recounts formal releases with cutoff/classification; retains scope and verifies version applicability before claiming impact. |
| File delivery | User requests one clarification at a time and export after answers are ready; requested report is missing | Maintains knowledge first, respects cadence, does not claim report provided; uses installed format skill and checks actual file, attachments and layout. |

Also evaluate a complete inquiry with no gaps: the skill should proceed through knowledge maintenance and requested delivery without manufacturing a confirmation gate.

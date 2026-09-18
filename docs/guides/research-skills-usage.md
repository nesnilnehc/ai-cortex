---
artifact_type: guide
created_by: ai-cortex
lifecycle: living
created_at: 2026-09-17
status: active
---

# Research Skills: choose the result you need

Describe the research goal in ordinary language. The agent should choose the narrowest Skill that produces the requested result. You can also invoke one of the five public entries directly:

| Desired result | Direct entry | Output |
| --- | --- | --- |
| Understand an open question | `/deep-research` | Research Report with findings, sources, conflicts and gaps |
| Understand rules in a jurisdiction | `/policy-research` | Policy Research Report with obligations, guidance, dates and implications |
| Understand a defined market | `/market-research` | Market Research Report with demand, segments and a defensible size method or explicit gap |
| Compare products | `/competitive-research` | Dated comparison and Research Report; unknown cells remain Unknown |
| Decide whether to pursue a product or feature | `/product-opportunity-analysis` | Opportunity Package with lane status, recommendation and trace |

The sixth local Skill, `assess-product-opportunity`, is an internal assessment step. Its repository metadata marks it non-user-invocable. The installer copies all Skill directories; some agent interfaces may still list it because they do not interpret that metadata. Use the five entries above for direct requests.

## Give enough scope

Supply the question and the decision or audience, plus geography or jurisdiction, period/as-of date, target users, product or competitor set, and any source constraints that matter. A missing field that changes applicability should prompt one clarification or a visible narrow assumption. You may provide authorized documents; private or authenticated material follows the host and project's access rules.

## Three common routes

**Open question.** “`/deep-research Compare the current maturity of OpenTelemetry GenAI conventions and OpenInference as of today. Separate specification status, implementation evidence and unknown adoption.`” This returns research findings, not a product recommendation.

**One domain.** “`/competitive-research Compare the event-management capabilities of the named CRM products in China, by edition and as-of date. Mark undocumented cells Unknown.`” This returns a dated competitor comparison and a Research Report. You can similarly use `/policy-research` for a named jurisdiction or `/market-research` for a bounded market.

**Opportunity.** “`/product-opportunity-analysis Should our pharmaceutical CRM support event ROI analysis for China-based operations teams? Assess relevant policy, demand, competitors and user signals, then recommend whether to pursue, explore, defer or decline.`” This returns one Opportunity Package; irrelevant lanes are marked `not_applicable`, and missing evidence is visible.

## Read the evidence before the recommendation

The [Research Evidence Spec](../../specs/research-evidence.md) defines `Fact`, `Claim`, `Inference` and `Unknown`, source locators, contradictions and gaps. Each report is a dated snapshot: recheck old findings before reusing them for a new scope. A vendor statement is attributed; it does not become independent proof of customer demand. When sources conflict, both positions remain in the report.

The [Opportunity Package Spec](../../specs/opportunity-package.md) defines its JSON handoff. A package may be `draft` and still useful; `explore` or `defer` can be the right completed recommendation when evidence is thin. `ready_for_decision` means a decision owner can review it, not that a product has been approved. Pass the package to a later requirement or design as evidence, with the original report IDs and sources intact; obtain those artifacts' separate approvals.

For a local contract check, run `python3 scripts/validate-research-artifacts.py <report-or-package.json>` from the AI Cortex repository. The fixed examples in `tests/fixtures/research/` illustrate the JSON shape; their `example.invalid` sources are synthetic and make no real-world claim.

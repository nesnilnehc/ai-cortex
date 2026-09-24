---
name: assess-product-opportunity
description: Assess a product opportunity from existing research reports and user signals, producing a restrained, traceable decision layer.
version: 1.1.0
license: MIT
user-invocable: false
metadata:
  ai_cortex_type: domain
  ai_cortex_user_invocable: "false"
---

# Skill: Assess Product Opportunity

## Purpose

Internal assessment step called by [product-opportunity-analysis](../product-opportunity-analysis/SKILL.md). Evaluate the opportunity from existing [Research Reports](../../specs/research-evidence.md) and return the decision layer of an [Opportunity Package](../../specs/opportunity-package.md). Do not initiate a new broad search or become a direct user entry. Claude Code uses `user-invocable: false`; platforms that ignore that field or `ai_cortex_user_invocable` may still expose the directory.

## Procedure

1. Check report schema, scope, dates, provenance and lane compatibility. Do not merge conflicting product versions, jurisdictions or market definitions into one unqualified fact.
2. Define the user problem, alternatives and why now. Separate demand, market, policy, competitor and user-signal evidence. If user signals are missing, record the gap explicitly.
3. Create decision-critical claim records: each points to report and finding IDs or states an Unknown reason. Include the strongest contrary evidence and the assumptions that could overturn the conclusion. Do not promote a Claim or Inference to Fact.
4. Examine unmet need, differentiation, constraints, defensible impact or size, timing and validation cost. Leave size or impact null when source inputs or method are insufficient.
5. Recommend `pursue`, `explore`, `defer` or `do_not_pursue` with confidence, claim IDs, proposed scope, risks and concrete validation steps. Use `explore` or `defer` when missing demand evidence blocks a decisive positive recommendation. A negative recommendation also needs evidence or an explicit limiting rationale.
6. Return the claims, analysis and recommendation to the orchestrator. Do not mark a package approved or change source reports.

## Self-check

Every decisive sentence has a claim ID. Every claim traces through a finding to a source locator or ends in an explicit Unknown. Conflicts and opposing evidence are present. The recommendation's confidence fits lane completeness and source independence.

## Examples

### Supported exploration

**Input:** current market and competitor reports agree on an unmet workflow, but there are no authorized user interviews. **Output:** cite the supporting and contrary finding IDs, mark user signals missing, and recommend explore with validation steps rather than a confident pursue.

### Conflicting scopes

**Input:** one report covers a paid enterprise edition in one region; another covers a free edition elsewhere. **Output:** keep the scopes separate, mark the affected claims Unknown or limited, and request evidence for the intended market before a decisive recommendation.

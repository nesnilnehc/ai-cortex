# Complete scenario examples

Four fictional plans demonstrate distinct combinations, not four mandatory formats.
Each includes source facts, intake/selection rationale, temporary input and generated
output. Unknowns are explicit; none claims unverified completion or framework certification.

| Scenario | Complete plan | Sources / selection | Layout |
| --- | --- | --- | --- |
| Iteration product | [Roadmap](iteration-product/roadmap.md) | [Facts](iteration-product/sources.md), [decision](iteration-product/selection.md), [input](iteration-product/input.json) | Main + [delivery detail](iteration-product/roadmap-delivery.md) |
| Continuous flow | [Roadmap](continuous-flow/roadmap.md) | [Facts](continuous-flow/sources.md), [decision](continuous-flow/selection.md), [input](continuous-flow/input.json) | Single; no fake sprint or version |
| Staged delivery | [Roadmap](staged-delivery/roadmap.md) | [Facts](staged-delivery/sources.md), [decision](staged-delivery/selection.md), [input](staged-delivery/input.json) | Main + [delivery detail](staged-delivery/roadmap-delivery.md) |
| Discovery pilot | [Roadmap](discovery-pilot/roadmap.md) | [Facts](discovery-pilot/sources.md), [decision](discovery-pilot/selection.md), [input](discovery-pilot/input.json) | Single; learning/evidence exit, no rollout commitment |

Use the [template recipes](../../assets/scenarios/README.md) and
[selection guide](../scenario-selection.md). Generated source links are relative to
each scenario output folder. Reproduce a chosen scenario from the repository root:

```sh
python3 skills/define-roadmap/scripts/render-roadmap.py skills/define-roadmap/references/scenarios/continuous-flow/input.json --recommend
python3 skills/define-roadmap/scripts/render-roadmap.py skills/define-roadmap/references/scenarios/continuous-flow/input.json --output-dir skills/define-roadmap/references/scenarios/continuous-flow --overwrite
```

Substitute another scenario folder to reproduce it. Saved layout is reused without
a CLI override. Recommendation retains the existing example choice; for a fresh
proposal pass a partial document containing planning_context instead. Generation
never writes selection.md, sources.md or input.json. Do not use reserved generated
filenames for source evidence.

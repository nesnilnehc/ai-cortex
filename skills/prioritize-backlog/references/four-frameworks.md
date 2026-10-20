# Four-framework assessment

Use these methods only for the selected assessment mode. Treat thresholds as
examples; use documented project thresholds when available. Missing inputs are
unknown, never invented numerical evidence. RICE person-weeks are optional measured
inputs, not a replacement for Fibonacci story points in work planning.

## RICE

```text
RICE = (Reach × Impact × (Confidence / 100)) / Effort
```

- **Reach**: how many people or instances are affected, as a number
- **Impact**: 3 (massive) / 2 (high) / 1 (medium) / 0.5 (low) / 0.25 (minimal)
  - The floor must be able to go below 1. If the lowest band is 1, a trivial item cannot be pushed down and only Reach and Effort can separate it from the rest, which leaves low-value items scoring too high
- **Confidence**: 0-100%, anchored at three points — `100% = backed by data` / `80% = partial evidence` / `50% = a guess`
  - Without anchors, scoring the same batch twice drifts; the anchors are what make a score reproducible
- **Effort**: positive person-weeks; zero or unknown cannot be scored

Mapped to a priority level:

| RICE score | Level |
| --- | --- |
| ≥ 1000 | P0 |
| 200 ≤ score < 1000 | P1 |
| 50 ≤ score < 200 | P2 |
| < 50 | P3 |

(These thresholds are a default example; a project may set its own.)

## WSJF

```text
WSJF = Cost of Delay / Job Size
```

- **Cost of Delay** = Business Value + Time Criticality + Risk Reduction / Opportunity Enablement
- **Job Size** = relative effort, on the Fibonacci scale 1, 2, 3, 5, 8, 13 (split work larger than 13 before estimating)

Mapped to a priority level, by the item's WSJF percentile within the current backlog:

| WSJF percentile | Level |
| --- | --- |
| Top 10% | P0 |
| 10-30% | P1 |
| 30-70% | P2 |
| Bottom 30% | P3 |

## MoSCoW

Classified by level of commitment:

- **Must**: not doing it this cycle blocks something badly or breaches compliance → P0
- **Should**: doing it this cycle raises value markedly → P1
- **Could**: do it if there is time → P2
- **Won't**: explicitly not this cycle → P3. Where it is **never** to be done, as opposed to deferred past this cycle, take the `status: declined` terminal state instead; follow the terminal-decision procedure in the calling skill

## ICE

```text
ICE = Impact × Confidence × Ease
```

- Each dimension scored qualitatively from 1-10
- Impact: the effect on a strategic goal
- Confidence: how much the estimate is trusted
- Ease: how easy it is to build — higher means easier

Mapped:

| ICE score | Level |
| --- | --- |
| ≥ 500 | P0 |
| 200 ≤ score < 500 | P1 |
| 50 ≤ score < 200 | P2 |
| < 50 | P3 |

When the widest result gap is at least two levels, surface the competing reasons
for a user decision. Otherwise use RICE as a provisional suggestion, not authority
to replace a settled policy or an existing priority.

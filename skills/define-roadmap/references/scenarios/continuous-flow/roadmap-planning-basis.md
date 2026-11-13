# Service Reliability Flow Roadmap Planning Basis

[Main roadmap](roadmap.md)

Ordering rationale: A customer-impacting retry defect precedes a convenience improvement.

[Priority policy](sources.md#planning-basis)

Closure criterion: Service owner verifies accepted behavior in production; task counts do not prove closure.

## Flow

Workflow policy: Pull when active WIP is below the team limit of two; start at In progress and finish after verified production delivery.

Service expectation: Unknown: insufficient historical cycle-time samples; no service-level commitment established.

Flow metrics: Track WIP, throughput, work-item age and cycle time; measured baselines are not yet available.

[Workflow source](sources.md#workflow) · [Execution board](sources.md#execution-board)

Backlog requirements and defects map to this roadmap; items outside it are not done by default.
Placement grants no implementation or release approval.

## Planning approach

Scenario: flow · Primary: flow · Layout: single

Enabled views: requirements, flow.

Retain the existing flow view and single document; no new sprint, version batch, phase or event is needed for the current horizon. [Selection source](selection.md#decision).

---
artifact_type: rule
name: writing-zentao-work-items
version: 1.0.1
scope: creating, updating or reviewing ZenTao requirements, defects and tasks
recommended_scope: project
status: active
created_by: ai-cortex
lifecycle: living
created_at: 2026-10-30
---

# Rule: ZenTao Work Item Writing

## Scope and authority

Agents MUST read this rule before creating, updating or reviewing a ZenTao
requirement, defect or task, including preparing text for someone else to enter.
It governs content and presentation, not permission to access an instance or
write business data. Confirm the intended instance through the consumer's
environment entry before service access.

Apply [Chinese technical writing](./writing-chinese-technical.md) to Chinese
content across fields, comments and attachments. Reuse
[documentation management](./workflow-documentation.md) for a single maintained
authority. For documents declaring the corresponding modeling Spec, also apply
[requirement quality](./requirement-quality.md) or [task quality](./task-quality.md).
This rule does not impose those documents' complete schemas, minimum criterion
counts or metadata on every ZenTao form.

## Content boundaries

- Requirements MUST express the business problem, affected users, objective,
  scope, necessary dependencies and observable acceptance outcomes in product
  language. Define technical terms only when the reader needs them to decide.
- Keep design details, implementation tasks, source investigations, logs and
  detailed test procedures in their own maintained artifacts. Create and link
  implementation tasks separately when task creation is authorized; otherwise
  identify the pending association. Do not mechanically import an entire local
  engineering document into a requirement.
- Concision MUST preserve security, permissions, tenant/data boundaries,
  exceptions, failure behavior and settled business decisions that change scope
  or acceptance. Link supporting detail without making the reader leave the item
  to discover its essential business behavior. Do not impose an arbitrary word
  limit or delete necessary facts to meet a length target.
- An update MUST reconcile the current body with the latest authorized decisions,
  replace superseded wording and remove duplicates. Do not accumulate dated
  supplement chapters, investigation transcripts or repeated conclusions.
  Preserve platform history and link decision evidence separately. A comment
  records a change or discussion; it does not replace the current description.
- Distinguish confirmed facts, observed behavior, hypotheses and unresolved
  decisions. Do not invent a business decision, dependency or acceptance target
  to make a form appear complete.

## Field responsibilities

Field names and availability vary by instance and connector. Verify the actual
schema and current values before mapping content; the API examples below are
common names, not a universal payload contract. Preserve unrelated fields.

| Item | Description | Acceptance or expected result | Related artifacts and other fields |
| --- | --- | --- | --- |
| Requirement | Business problem and objective; in/out scope as parallel bullets; necessary dependencies, constraints and their effect. Common body field: `spec`. | Independently decidable outcomes, including relevant boundary and failure cases. Common separate field: `verify`. | Link parent/child requirements, designs, separately created tasks, source decisions and test cases using supported associations. Keep priority/status in their native fields. |
| Defect | Business impact, affected version/environment and preconditions; minimal numbered reproduction steps and observed result, with concise evidence. Common stored body: `steps`. | Expected behavior and its authority: approved requirement, design, contract or established behavior. Repair acceptance, if separately supported, states the observable corrected outcome and relevant regression boundary. | Link the affected requirement, diagnostic evidence and repair task. Keep severity, priority and resolution in their own supported fields. Label an inferred cause as a hypothesis. |
| Task | One independently deliverable implementation or verification result; affected scope, necessary execution detail and blockers. Common body field: `desc`. | Completion evidence and pass conditions for that result; cite the requirement's acceptance instead of copying it. Use a native completion field if supported, otherwise a clearly labeled subsection of the description. | Associate the requirement and design; link dependent tasks and detailed procedures. Keep assignment, estimate and status in supported fields. |

Dependencies state what must be available, from whom or which item, and how its
absence affects delivery. Acceptance states what behavior proves success under
specified conditions. A dependency belongs in acceptance only when there is also
an independently specified user-visible behavior to verify; write that behavior
explicitly rather than moving the dependency sentence between fields.

Acceptance MUST identify the actor/precondition, action and observable result
needed for a pass/fail decision. Use an agreed threshold where the outcome is
quantitative. Detailed commands, click-by-click test execution and test data sets
belong in linked tests or verification tasks. Do not confuse writing acceptance
criteria with claiming that the product has passed them.

Map each field deliberately. If extracting from Markdown, respect the target
section's heading level and stop at its next peer or ancestor heading; do not
capture later dependencies or appendices into acceptance. Inspect the extracted
fields before writing, including empty or missing sections.

## Presentation constraints

- Use a short descriptive title, brief paragraphs and parallel bullets for scope.
  Use numbered lists for sequences or independently referenced acceptance items.
  Use a small table only when comparison helps; avoid a deeply nested outline.
- Markdown is an authoring format, not an API HTML contract. Confirm whether the
  selected editor/tool accepts plain text, Markdown or sanitized HTML. Send the
  expected representation; do not paste raw Markdown into an HTML-only field or
  escape HTML until tags become visible text.
- For HTML fields, prefer simple semantic blocks supported by the instance:
  paragraphs, lists and descriptive links. Escape text/attributes correctly;
  do not combine redundant empty paragraphs, repeated `<br>` elements and source
  newlines as competing spacing mechanisms. Check the result in the target view.
- Do not duplicate headings injected by the connector or editor. Some defect
  tools expose steps, actual result and expected result separately but store them
  in one body with generated labels; confirm this before composing those fields.
- Historical `nl2br`, paragraph spacing, field-loss and HTML-normalization reports
  are diagnostic leads, not universal behavior. Verify the current instance,
  operation and connector version. A defect rendering workaround MUST NOT be
  applied to requirements or tasks without evidence of the same path.

## Delivery evidence

A delivery or review MUST distinguish these conclusions:

| Conclusion | Required evidence | Insufficient evidence |
| --- | --- | --- |
| Content is ready | Correct content layer and field mapping; decidable acceptance; preserved boundaries and decisions; valid associations and source links accessible to intended readers. | A short body, filled template or successful local build. |
| Saved | Mutation response plus read-back of the intended item and fields, with substantive content and associations preserved. | An API success response alone. |
| Presentation is acceptable | Inspection of the actual item page in the target instance: readable scope and acceptance, heading/list hierarchy, spacing, links, no raw markup, duplicate labels or clipped content. | API read-back, source HTML inspection or a local preview alone. |

On a read-back mismatch, inspect the current stored content before retrying.
Distinguish harmless HTML normalization from missing text, wrong field boundaries
and damaged links; byte inequality alone proves neither loss nor success. Avoid
blind retries after an uncertain write. Restore missing content only after the
actual state is known and within the authorized scope.

If the page is inaccessible, report which fields were read back and state that
page presentation is unverified, with the access limitation. A local rendering
can help prepare the text but cannot certify ZenTao's own rendering. Never create
production test items merely to demonstrate this rule. For a review without a
write, saved-state verification is not applicable; report the actual review scope.

## Short examples

These illustrative examples do not authorize or describe a real work-item change.

| Case | Poor | Better |
| --- | --- | --- |
| Requirement description | Investigated three classes; run these commands; implementation plan follows. | Support staff need to check processing status without contacting engineering. Scope: read the current tenant's status. Out of scope: changing it. Dependency: the status service must be available. |
| Requirement acceptance | Depends on the status service; tests pass; permissions are correct. | Given a support user in tenant A, querying an A record shows its current status. Querying a B record returns no record data. If the status service is unavailable, show an unavailable result rather than a successful status. |
| Defect | The permission code is broken; see the full log. | Impact: a support user can read another tenant's status. Preconditions: tenant A support account and a known B record. Step: query that record. Actual: B status is returned (observed). Expected: no record data, per the linked permission requirement. |
| Task | Complete the feature and all testing. | Implement tenant isolation for status lookup; associate the permission requirement. Completion: linked automated checks show an A lookup succeeds and a B lookup returns no record data. |
| Update | Add another “latest supplement” repeating the scope. | Replace the obsolete scope bullet, reconcile acceptance, and link the decision in the change record. |

Illustrative requirement HTML (description and acceptance are separate payloads):

```html
<p>Support staff need processing status without contacting engineering.</p><p>Scope</p><ul><li>Read the current tenant's status.</li><li>Exclude status changes.</li></ul><p>Dependency: the status service must be available.</p>
```

```html
<ol><li>A tenant A support user can read an A record's current status.</li><li>A query for a B record returns no record data.</li><li>An unavailable status service produces an unavailable result.</li></ol>
```

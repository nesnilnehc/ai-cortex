# orchestrate-governance-step: output contract

## Appendix: Output contract

### YAML schema (formal)

```yaml
type: object
# execution_trace is required for advance when a governance action ran;
# no-op states do not claim an execution trace.
required:
  - report_title
  - action_taken
  - result
  - next_step
  - continuation_signal
properties:
  report_title:
    type: string
    const: "What this automatic step did"
  action_taken:
    type: string
    minLength: 1
    description: describes the single action taken, by file name or feature name
  why_fix:
    type: string
    minLength: 1
    description: optional; may be omitted when a file is created for the first time
  changes:
    type: object
    required: [before, after]
    properties:
      before:
        type: string
      after:
        type: string
  result:
    type: string
    enum: ["Success ✅", "Your call needed ⚠️", "Error ❌"]
  next_step:
    type: string
    minLength: 1
  decision_state:
    type: string
    enum: [actionable, needs_input, no_applicable_action, complete]
  continuation_signal:
    type: string
    enum: [advance, done, blocked, stalled, error]
  execution_trace:
    type: object
    required: [selected_skill, plan_reviewed_rounds]
    properties:
      selected_skill:
        type: string
        pattern: "^/[a-z0-9-]+"
      plan_reviewed_rounds:
        type: integer
        minimum: 0
        maximum: 3
      post_check_plan_next_rerun:
        type: boolean
        description: Required and true after a modifying action; omit for no-op or read-only checks.
additionalProperties: false
```

### JSON schema (formal)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "IterationStepReport",
  "type": "object",
  "required": [
    "report_title",
    "action_taken",
    "result",
    "next_step",
    "decision_state",
    "continuation_signal"
  ],
  "allOf": [
    {
      "if": {
        "properties": {
          "continuation_signal": { "enum": ["advance"] }
        },
        "required": ["continuation_signal"]
      },
      "then": { "required": ["execution_trace"] }
    }
  ],
  "properties": {
    "report_title": {
      "type": "string",
      "const": "What this automatic step did"
    },
    "action_taken": {
      "type": "string",
      "minLength": 1
    },
    "why_fix": {
      "type": "string",
      "minLength": 1
    },
    "changes": {
      "type": "object",
      "required": ["before", "after"],
      "properties": {
        "before": { "type": "string" },
        "after": { "type": "string" }
      },
      "additionalProperties": false
    },
    "result": {
      "type": "string",
      "enum": ["Success ✅", "Your call needed ⚠️", "Error ❌"]
    },
    "next_step": {
      "type": "string",
      "minLength": 1
    },
    "decision_state": {
      "type": "string",
      "enum": ["actionable", "needs_input", "no_applicable_action", "complete"]
    },
    "continuation_signal": {
      "type": "string",
      "enum": ["advance", "done", "blocked", "stalled", "error"]
    },
    "execution_trace": {
      "type": "object",
      "required": ["selected_skill", "plan_reviewed_rounds"],
      "properties": {
        "selected_skill": {
          "type": "string",
          "pattern": "^/[a-z0-9-]+"
        },
        "plan_reviewed_rounds": {
          "type": "integer",
          "minimum": 0,
          "maximum": 3,
          "description": "0 for direct routine work; otherwise number of explicit plan reviews"
        },
        "post_check_plan_next_rerun": {
          "type": "boolean",
          "description": "true after a modifying action; omit for no-op or read-only checks"
        }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
```

---

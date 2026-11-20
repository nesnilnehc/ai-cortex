# Repair Loop Examples

## Example 1: fix a failing unit test in a Node repository

User: "Make the tests pass. Keep fixing until it is green."

Agent:

1. Preflight: scope=`diff`, test mode=`fast`, max_iterations=5; installing (`npm ci`) and network access are confirmed as allowed.
2. Iteration 1: run the engineering gate, applicable alignment review and `npm test`; select the highest-priority blocking signal.
3. Apply the smallest fix, rerun `npm test`, then rerun every engineering/alignment dimension the fix can invalidate.
4. Stop once the engineering gate, applicable alignment review and `npm test` all pass.

## Example 2 (edge case): the integration tests need Docker and secrets

User: "Mirror CI and fix the failures."

Agent:

1. Preflight: test mode=`ci` is suggested, but CI is detected to use `docker compose` and env secrets.
2. A stop condition fires: environment blocker (Docker + secrets not approved/unavailable).
3. Ask the user to choose:
   - Run only the `fast` unit tests locally, or
   - Allow Docker and provide a non-chat secrets workflow, or
   - Run only the failing CI job steps that do not need secrets.

## Example 3: repair a defect reported with a screenshot

A ticket says a save button does nothing. Compare its screenshot, steps and logs with the expected save behavior; do not infer the cause from the title. Reproduce the defect with a failing regression test, repair it, and rerun the affected gates. Exercise saving in the running UI and inspect its resulting state under the project's acceptance plan. Return the ticket reference, root cause, repair locations and test, visual and interaction evidence. If the app cannot run locally, record the blocked interaction check and do not claim the original user path is verified.

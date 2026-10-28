# T7: ordinary conversation and Cortex assets

Date: 2026-10-27. The owner correctly answered that an unclear search scope belongs
in the requirement document, then identified the page's missing explanation:
agents can clarify and amend that document directly. The prior wording encouraged
an unnecessary assumption that every conversation or edit requires a skill.
This is interface feedback, not a comprehension failure by the owner.

The owner requested the distinction be made explicit. This local content repair
preserves the approved single map, panel, disclosure and request interaction.
No approved requirement/design snapshot, production website or remote state changed.

## Repair and sources

- `context-copy.mjs` owns ordinary-agent and Cortex-value explanations plus linked
  Skill/Spec/Rule/Protocol examples, following the repository terminology source.
- `panel-model.mjs` exposes those explanations to every work context, with a
  specific clarification/editing example and default request for the design node.
- `story.mjs` renders them before related skills, reusing the existing panel.
- The example and walkthrough now explicitly refer to an existing requirement.
- Existing adopted project constraints remain applicable without pretending that
  a Spec or Rule is an operation invoked on every conversational turn.

## Verification

- [Observed red test](t7-boundary-red.txt): usage data was absent.
- [Final model/source tests](t7-boundary-tests.txt): 37 executed and passed,
  zero failed or skipped, including the explicit ordinary-versus-Cortex contract.
- [Browser matrix](t7-boundary-browser.json): all five widths and both themes
  passed the existing pointer/keyboard/search/copy/failure checks.
- [Text contrast samples](t7-boundary-contrast.json): both themes passed the
  existing 4.5:1 sampling threshold. This is not a full accessibility certification.
- The design context's two explanations were inspected; all four asset links
  returned local HTTP 200. No horizontal overflow at 390px was observed.
- [Desktop capture](t7-boundary-design.png) was visually inspected. The native
  in-app accessibility tree confirmed the updated visible wording after reload.
- [Source manifest](t7-boundary-manifest.json) identifies this candidate; earlier
  `req03-*` source manifests and unit-test logs describe the previous candidate.

T7 is In Progress. The owner requested one question at a time; continue the human
walkthrough after they inspect this repair. Other scenarios and the overall human
comprehension criterion are not yet accepted. No publication occurred.

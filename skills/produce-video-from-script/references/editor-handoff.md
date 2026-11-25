# Editor handoff and verification

## Find a usable editing path

- Discover installed editors, connected tools, or a supported interchange format. Confirm the path can import the project's media, place assets at specific times on separate tracks, preserve editable captions, and save or reopen the timeline. Confirm with a short representative sequence when the path is new. Use a different editor only if it satisfies the user's handoff needs and destination authorization.
- For ChatCut, distinguish a local desktop project from a Web project. Use the tools available for the selected project and confirm the operations they expose. For a local project, return a verified project location or an editor reference the user can open. For a Web project, verify the project link and timeline. Get authorization for the selected destination before sending source media or narration to an external service. Consult the [ChatCut agent connection guide](https://chatcut.io/docs/agent-plugin) if the available connection is unclear.
- If the editor or import is unavailable, keep a handoff package of the narration, editable caption file when applicable, storyboard, asset paths, and absolute placement times. Include an interchange file only when the target editor accepts that format. Identify what was verified and what still requires import or editing.

## Place assets without cumulative drift

- Keep the cue sheet on the actual narration clock. For a frame-based editor or renderer, convert each absolute cue to the nearest frame using the project's actual frame rate and a consistent rounding rule. Use the difference between the end and start frame indices as the shot length. If a visual interval collapses to zero frames, resolve the cut with the adjacent shot or choose a suitable rate within the brief. Check that the final picture covers the entire narration and verify the timeline after import, including fractional frame rates where applicable.
- Place the principal visuals in storyboard order and timed overlays above them. Keep the final narration on its own track and any requested music below it in level. When creating a clip externally, keep narration and captions in the editable project and include only the media the clip is meant to contribute.
- If the editor generates captions by transcription, isolate the narration source and check the result against the approved wording, especially names and numbers. Verify that correcting words does not cut or retime the narration. When that editor ties transcript edits to media edits, use its caption-only operation or a supported subtitle import. Check a saved caption segment for both wording and timing.

## Verify the handoff

- Reopen or query the saved timeline and check the project and timeline identifier, resolved media links, editable tracks, and expected start and end. Verify the match between shot IDs, clip placements, and assets, and check the rendered state around representative boundaries and revised shots.
- When the user needs a portable project, verify the referenced media is included or resolvable at the destination. Report which artifacts a user can open and continue editing. Treat a preview and a saved editable project as separate deliverables.

---
name: produce-video-from-script
description: Produce a video from an approved narration script by preparing narration, planning shots, and assembling an editable timeline. Use to start from a script, continue from a storyboard, or revise selected shots.
license: MIT
metadata:
  version: "0.1.0"
---

# Produce video from a script

Use this workflow when the narration script guides the choice and sequence of shots. An approved script is enough to start a new project. Reuse supplied recordings, footage, or other media when they fit the script. Continue from an existing storyboard or saved timeline when available. When a presentation determines the page order and visuals, use [produce-video-from-presentation](../produce-video-from-presentation/SKILL.md).

## Start from the latest usable material

- For a new project, identify the approved script, target audience, available assets, and any requested editor, aspect ratio, and deliverable. An existing storyboard can supply the approved wording and cues when they match the recording. If approved wording is missing, request it before aligning narration or planning timed shots. For a storyboard-only request, deliver the narration, cues, and storyboard as applicable.
- For an existing project, match the script, narration, storyboard, and editor timeline to the requested version. Use existing valid artifacts to resume at the first affected step. For a shot revision, confirm the target by its ID or time range and inspect its neighboring cuts.
- Keep the inputs and a production record with the working media. Record the source versions, frame rate and aspect ratio, timeline identifier, and the locations of the cue sheet, storyboard, and linked source assets. Keep source media when replacing clips.

## Time and plan the story

1. **Establish the narration.** Reuse a recording that matches the approved script and target voice. For synthesis, use an available local tool or a service authorized for the script and selected voice. Prefer one continuous performance. If a service limit requires splitting it, use natural breaks and check the assembled joins. Before any paid job, check the authorized budget and existing pending jobs. Keep the provider task ID and resolve its status before retrying an interrupted submission.
2. **Align the approved words.** Work against the actual narration the editor will use. Reuse matching cue data, or discover an available forced aligner, transcription tool with timestamps, or player for manual cueing. Use recognition for timing and the approved script for captions. Check suspect boundaries by listening on both sides; report omitted or added speech and unresolved timings. If timing is blocked, retain the recording and any untimed plan as partial work.
3. **Plan the shots.** Group the narration by what the audience needs to see or understand. Each shot should record a stable ID, absolute start and end, matching narration or cue, visual purpose, assets, and any timed change or transition. Base narration-driven cuts and motion on verified cues. Mark intentional pauses and missing evidence in the plan. A real screenshot, result, or example needs a source; identify illustrations as such. Verify that the primary visual sequence covers the intended timeline without gaps or overlaps.

## Assemble and review

1. **Select a working editor.** Use the requested editor when available. Before assembly, verify that it can place media at the planned times, keep captions and narration editable, and reopen the resulting project. Follow [Editor handoff and verification](references/editor-handoff.md) when selecting tools, preparing an import package, or checking a saved timeline.
2. **Build only the assets the plan needs.** Use supplied or reusable assets first. If the visual direction is unresolved, test a short sequence across a representative cut before making the full set. For complex motion, use an available renderer that can build the required visual and render at the chosen dimensions and frame rate. Animate changes that help the viewer understand the script and leave time to read them. Keep editable titles, captions, narration, and background audio on separate tracks where supported.
3. **Check the saved timeline.** Verify shot order, coverage, media links, caption timing and readability, and the beginning and end. Inspect representative frames for blanks, clipping, and obscured content. Play and listen across cuts, key phrases, and revised regions. Record completed checks and give timestamps for any checks that could not be performed.
4. **Apply requested revisions.** Change the affected shots and their joins. If the approved change alters narration duration, realign all shifted cuts, motion cues, and captions. Preserve a recoverable baseline for edits that affect the whole timeline. Update the production record and verify the saved result again.

Return the verified project path or editor link, timeline name, production record, and any unresolved issues. Export or publish only if the user requests it. When no editable project can be saved, return the verified intermediate files and name the operation needed to complete the handoff.

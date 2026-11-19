---
name: produce-presentation-video
description: Create narrated, captioned videos from PowerPoint, Keynote, Google Slides, PDF, or other paginated presentations with speaker notes or a script. Use to start or resume production, fix pronunciation, re-export, or archive a completed presentation video.
version: 0.1.0
license: MIT
---

# Produce a presentation video

For new production, use the specified presentation and its speaker notes or a separate script. For existing work, use the production files or accepted export that match the requested version. Default to stable slide images, one continuous narration track, captions in the script language, and a 1080p MP4 for new production. Follow the user's choices for voice, language, resolution, caption format, and destination.

## Choose the starting point

- **New production or resume.** Lock the presentation version and the script source. Keep a separate production directory outside the source directory. When resuming, check which inputs each artifact actually depends on and start at the first missing or failed stage. Check any existing narration against the script, voice, and completeness requirements. Regenerate it if the user explicitly requests a fresh recording.
- **Local correction or re-export.** Start from the verified movie, original slide images, and final narration as available. Repeat the stages affected by the change. For a pronunciation fix, replace a complete passage and update affected slide and caption timing.
- **Archive only.** Locate the accepted export for the requested version. Resolve version ambiguity using prior acceptance records, then check the destination and filename, copy the file, and verify the copy.

## Produce and deliver

1. **Verify the source.** Identify which slides belong in the video and check their order and script. Check the intended treatment of hidden slides against the source presentation and the user's instructions. Inspect the first and last slides and important charts. Identify missing notes by slide number and fill them in within the authorized scope or flag them for input. When rendering or extraction is a requested intermediate deliverable, report the actual slide count and output path as soon as it is ready.
2. **Prepare the narration.** Reuse a matching complete track or synthesize the full script with the requested voice, pacing, natural pauses, and required service markers. Test a short sample for a new voice or difficult pronunciation. Check previous submissions, incurred and pending charges, and the authorized budget before making a new paid request.
3. **Assemble the video.** Render slides directly at the target resolution where possible. Use the final narration to time slide changes and captions. Use the approved text for captions. Keep ordinary slides stable and test a representative clip before applying a staged reveal that helps explain the material.
4. **Verify and deliver.** Check slide images, captions, full decoding, and the beginning and end. Listen to representative sections, transitions, numbers, terms, and replacement seams. Record machine checks and listening results independently. If listening is unavailable, give the file path and timestamps to check. Save the requested copy and verify it at the destination. Report the verified path or link for each delivered artifact and any checks or cloud delivery still pending. Base progress and completion on artifacts actually checked.

See [Production and verification](references/production.md) for tool selection, recovery, alignment, export, and delivery. When using Doubao, also see [Doubao narration](references/doubao.md).

If a stage is blocked, report the operation that failed, the original error with private details removed, the completed artifacts, and the capability or input needed to continue. Keep working on independent stages.

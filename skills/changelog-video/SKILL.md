---
name: changelog-video
description: Generate and validate an optional release video from confirmed Release Package change items using repository-local media tooling; never installs tools or decides or publishes the release.
description_zh: 使用仓库本地媒体工具，从已确认的 Release Package change items 生成并校验可选发布视频；不安装工具，也不决定或发布版本。
tags: [release, changelog, video, release-package]
version: 1.0.1
license: Apache-2.0
compatibility: Requires a video renderer already available through the target repository or runtime; never downloads one.
recommended_scope: project
metadata:
  author: ai-cortex
  origin: vendored-derived
  source-registry: ../SOURCES.yaml
triggers: [changelog video, release video, generate release video]
input_schema:
  type: free-form
  description: Confirmed Release Package identity and customer-facing change items; output directory; optional audience, language, duration, aspect ratio, narration, captions, media, and renderer preferences
output_schema:
  type: document-artifact
  description: A validated video artifact entry and check evidence, or an explicit unavailable/failed result; never a release decision or publication receipt
---

# Skill: Changelog Video

## Purpose and Boundary

Turn the confirmed Release Package `change_items` into a short release video, and return a `kind: video` artifact entry that drops straight into the package manifest. This Skill handles the video material only: it does not re-analyze git, does not decide the version, does not modify the changelog, does not create a tag, does not publish the video, and does not send an announcement.

AI Cortex installs and updates the local copy centrally. A Skill must not be downloaded, registered or upgraded at runtime from skills.sh, GitHub, a raw URL or any other registry; external sources serve provenance during maintenance only, see [`../SOURCES.yaml`](../SOURCES.yaml).

## Input Contract

Required inputs:

- `decision=release`, `project`, `version`, `release_channel` and `range`
- The customer-facing `change_items` confirmed by `prepare-release`
- `output_dir`
- `required`, which decides whether a failure blocks Release Package readiness

Optional inputs: `audience`, `language`, `duration_seconds`, `aspect_ratio`, `narration`, `captions`, `media`, project brand material and renderer preferences. Each change item carries at minimum a stable ID, the user impact, the audience and the source; when a fact is missing, return the gap rather than reading back into git to guess.

When the input comes from `prepare-release`, carry over the choices already confirmed and ask only about missing information that would change the result. On a standalone call, first present the editable defaults below and confirm them in one pass:

```text
[default] Audience: customer
[default] Language: same as the release notes
[default] Duration: 45–60 seconds
[default] Aspect ratio: 16:9
[default] Captions: required when there is narration
[optional] Narration, project brand assets, existing product screen recordings

Generate with these settings? You can change any of them.
```

## Behavior

### 1. Validate the release facts

Confirm `decision=release`, and that the version, channel, range and change items are all present. Select only the items whose audience matches and whose `user_impact` can be verified; an `internal` item must not enter a customer video unless the user explicitly changes the audience.

### 2. Discover the local production path

From the project documentation, configuration, existing scripts, CI and the current runtime tooling, discover the video renderer, caption, audio and media-processing capabilities already available; prefer reusing the project's conventions. Use only local files, or tools the current context has already authorized.

When no renderer is available:

- `required=false`: return `status: unavailable` with evidence of what is missing, and install nothing.
- `required=true`: return a blocking result, and `prepare-release` keeps the package at `draft`.

### 3. Form the script and the storyboard

- State the core change this version brings in one sentence, then pick the 3–5 change items with the most user value.
- Every spoken or on-screen fact must map to a change item ID; migration requirements and breaking changes must not be softened.
- Prefer showing the change in user experience, the real product interface, or an analogy or plain diagram backed by the supplied assets; where honest visualization is out of reach, use a text card and invent no UI that does not exist.
- Keep the narration text and the on-screen text separate: on-screen text stays short, narration can add context, and the two draw on the same source of fact.
- Emit a storyboard preview listing duration, scenes, source IDs, the assets needed and the files that will be created; render only once it is confirmed.

### 4. Render, with writes constrained

Invoke the discovered local production path only after the user confirms. Every intermediate and final file must sit inside `output_dir`; product source, version files, the changelog and any release state outside the Release Package must not be modified. Skills, CLIs, fonts, media and models must not be installed in order to finish the render.

### 5. Validate the artifact

Validate at minimum:

- the video file exists and is non-empty, and its container, duration and resolution match the confirmed values;
- sample the opening, middle and closing frames, and check for black frames, cropping, unreadable text and wrong assets;
- when narration was chosen, that an audio track exists; when captions were chosen, that captions are visible across the audible stretches;
- the version, features, migration and CTA in the video match the Release Package;
- the output directory holds no credentials, temporary tokens or unauthorized media.

When any required gate fails, `status: present` must not be returned.

## Output Contract

On success, return:

```yaml
artifact:
  kind: video
  audience: customer
  path: <output_dir>/release-<version>.mp4
  required: false
  status: present
  source: [<change-item-id>]
  producer:
    skill: changelog-video
    version: 1.0.1
    origin: vendored-derived
    source_registry: skills/SOURCES.yaml
checks:
  - name: changelog-video
    status: passed
    evidence: <renderer and validation summary>
    required: false
```

On unavailable or failed, return the same structure with `path` set to `null`, the artifact status as `unavailable` or `failed`, and the matching check status as `skipped` or `failed`; MP4 files, renderer receipts and validation results must not be faked.

## Boundary against the Release Skills

- `prepare-release` decides whether a video is chosen, supplies the change items, and consumes the artifact/check result.
- `changelog-video` owns the script, the storyboard, the render and the media validation.
- `publish-release` publishes only a video already registered in the package; it regenerates nothing.
- `announce-release` only links to or distributes a published video.

## Upstream Note

The ideas behind this Skill — "picture the experience, cap the spoken items, keep narration and on-screen text apart, validate by sampled frames" — derive from the HyperFrames `changelog-video`. The AI Cortex version carries none of the upstream brand assets, fonts, music, fixed voice, repository paths or sibling skills; the exact source and pinned commit are in the source registry, and the upstream licence is at [`LICENSE.upstream`](LICENSE.upstream).

## Self-Check

- [ ] The input came from confirmed Release Package change items, with no re-parsing of git to decide facts.
- [ ] The audience, language, duration, aspect ratio, captions/narration and asset choices were shown and confirmed.
- [ ] Only local or already-authorized tools were used; no Skill or renderer was installed or downloaded.
- [ ] Every scene traces back to a change item, and no internal content leaked.
- [ ] The video, audio, captions and sampled frames were validated against the choices made.
- [ ] The output holds the artifact/check result alone; no tag, publication or announcement was created.

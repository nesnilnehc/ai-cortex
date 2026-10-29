---
name: announce-release
description: Create and optionally deliver announcements from verified published release targets; never owns changelog generation.
version: 1.2.0
license: MIT
---

# Skill: Announce Release

## Purpose

Turn verified publication facts into announcements aimed at different audiences, and deliver them when the user explicitly asks and the runtime has the channel capability. Existing 1.x requires an overall published package; 2.x may use a verified published target subset. Material generation belongs to `prepare-release`; version publication belongs to `publish-release`.

## Core Goal

Produce announcements consistent with the facts of the published version; deliver them channel by channel once channel, permission and user confirmation are all satisfied, and keep an auditable delivery receipt.

## Version 2 target-scoped announcements

For a 2.x [Release Package](../../specs/release-package.md#58-version-2-staged-release-contract), validate the schema and identify the requested targets. Each covered target must have verified completed publication; an announcement may cover a completed subset while other targets remain pending, but must not claim those other targets are published. Use the project's grouping and matching rules. Before repeating a write, reconcile the existing document and required index entries; ambiguous results remain unresolved. Record each delivery receipt independently and do not build, upload or publish product artifacts during announcement recovery. The 1.x behavior and self-check below remain unchanged for 1.x inputs.

For 2.x, self-check: every covered target has publication evidence, claims are scoped to that evidence, authorization was respected, and completed announcement writes were not duplicated.

## Behavior

1. Require the package to be `decision=release` / `status=published`, with version, channel, tag, commit, publication receipt and every required artifact path present; an optional artifact may be `skipped` / `unavailable` / `failed`, and that must not block an ordinary announcement. Stop on `not_required` or a missing required fact; do not guess.
2. Prefer the package's `change_items` as the source, selecting content by `audiences`, `user_impact`, breaking/migration, language, highlight and media; artifacts supply reviewed copy and links on top of that. Fall back to parsing changelog/release notes only when an older package carries no change items, and mark what was inferred.
3. Produce internal, customer-facing and technical/operator drafts per audience. The same fact may be reworded for a different audience, but the version, user impact, migration actions and sources must not drift. Structure follows [Universal Notification](../../specs/universal-notification.md); actual IM delivery follows [INP](../../protocols/im-notification-delivery.md).
4. Discover the available email, IM, website, customer portal or project provider tools, map their send capability, targets, link/attachment support and receipts, and mark each target channel explicitly as required or optional. With no tool available, output drafts only.
5. Before delivery, show the channels, audiences, body, links, permissions and impact; send after confirmation. Record success, failure and skip per channel.
6. Write communication as `announced` only when at least one target channel returned a success receipt, all required channels succeeded, and the user asked for the status to be recorded; keep `published` when a required channel fails or nothing was delivered successfully. A failed optional channel must keep its receipt, but it does not block `announced`.

## Input and Output

Input is a `published` Release Package, the target audiences/channels and an optional delivery request. Output is announcement drafts separated by audience; once confirmed and channel-capable, it also carries a per-channel delivery receipt and records the communication result per the Spec.

## Limits

- Does not generate or rewrite the authoritative content of `CHANGELOG.md`, does not create tags, does not publish build artifacts.
- Does not expose an `internal` change item to a customer audience automatically; does not copy a technical changelog sentence by sentence into a customer announcement.
- Does not state an unpublished version, an unverified capability or the existence of a video as fact.
- Does not send when there is no channel tool, account or target; does not write credentials into a draft or into the package.
- video is linked only as an optional artifact; its absence does not block an ordinary announcement unless the project explicitly demands it.

## Self-Check

- [ ] The package is `decision=release` / `status=published`, and the version/tag/commit in the announcement match it.
- [ ] Change items were preferred as the source, and the audience, language, highlight, migration and media selections are traceable.
- [ ] Every fact traces back to a package artifact or a publication receipt.
- [ ] Channel capabilities were discovered, and the delivery was shown and confirmed before it ran.
- [ ] Each channel has its own receipt, and no failure is hidden.
- [ ] `announced` was written only after a qualifying success receipt.

## Examples

### Example 1: Drafts only

The user asks for a v3.2.0 customer announcement but has not authorized sending. Read the published package and produce a customer draft and a technical draft in Markdown; call no channel tool and change no status.

### Example 2: Some channels fail

Email succeeds, but the enterprise IM marked required is not connected. Output the email receipt and the reason the IM was not sent, keep the package at `published`, and do not mark a partial success with an unfinished required channel as `announced`.

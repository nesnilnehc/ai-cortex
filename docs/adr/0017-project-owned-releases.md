---
artifact_type: adr
lifecycle: living
created_at: 2026-11-01
status: accepted
---

# Project-owned build and release workflows

The maintainer explicitly chose to remove the generic build/release/announcement Skills, Release Package, and associated Apple, generic-release and Yuque requirement work. Each consuming project owns these workflows through its own instructions, scripts, tools or Skills. No replacement shared release framework is introduced.

Removed entries: build-artifacts, prepare-release, publish-release, announce-release and changelog-video; the release-package Spec; AIC-REQ-05, AIC-REQ-06 and AIC-REQ-07 with their dedicated designs and experiments. Their IDs remain reserved and must not be reassigned. The previous staged-release decision is withdrawn.

The decision changes the pre-1.0 target inventory, not published history. Existing tags, changelogs and frozen acceptance records remain historical evidence. Current catalogues, source records, website membership and CI no longer require the removed assets. Project-owned Skills outside this repository are untouched.

Skill provenance presentation, eli5, Ponytail, ordinary code delivery/review and messaging capabilities remain in scope. Source: maintainer confirmation in chat 01a1803e-9883-7aa0-b887-8861238d233f on 2026-11-01.

## Verification and delivery boundary

The local catalogue has 68 Skills and 20 Specs. Retirement assertions, website model tests, installer integration, retained Findings/coverage consumers and document checks cover removal and unrelated capability preservation. The edited source records have explicit maintainer confirmation and pass local structural validation. Formal catalogue generation follows the local source commit and binds its asset/evidence revisions; the committed-revision gate remains in force. The maintainer authorized local commits and regeneration, not push or deployment. Consumer project repositories and their own release Skills are not modified.

Historical roadmap evaluation reports were removed from the current distribution. Offline regression tests use independent synthetic protocol samples and retain stale-context and inconsistent-trace rejection. Saved model evaluation reports and their availability status are not required checks or release gates for this repository.

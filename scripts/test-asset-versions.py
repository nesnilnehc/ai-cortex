#!/usr/bin/env python3
"""Test the asset-version check against every shape a release range produces.

The check answers one question: did every versioned asset the range edits also
move its version? The repository-wide run reports nothing whenever the range is
clean, which on its own proves only that the comparison found nothing to say.
The cases below give it a denominator.

They drive the decision function rather than git, because that is the half that
is mechanical. Reading a range out of git is the other half and is exercised by
the repository-wide run in CI.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "check_asset_versions", ROOT / "scripts" / "check-asset-versions.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Each case: label, change record, the fragment the finding must contain, or None
# when the change is legitimate and must produce nothing.
CASES = [
    (
        "edited asset whose version did not move",
        {"path": "rules/standards-coding.md", "status": "modified", "before": "1.0.2", "after": "1.0.2"},
        "version is still 1.0.2",
    ),
    (
        "edited Skill whose version did not move",
        {"path": "skills/orchestrate-code-review/SKILL.md", "status": "modified", "before": "1.2.0", "after": "1.2.0"},
        "version is still 1.2.0",
    ),
    (
        "edited asset whose version moved",
        {"path": "rules/standards-coding.md", "status": "modified", "before": "1.0.2", "after": "1.1.1"},
        None,
    ),
    (
        "edited asset that lost its version field",
        {"path": "rules/standards-coding.md", "status": "modified", "before": "1.0.2", "after": None},
        "no longer declares a version",
    ),
    (
        "edited asset that gained a version field",
        {"path": "rules/standards-shell.md", "status": "modified", "before": None, "after": "1.0.1"},
        None,
    ),
    (
        "version moved backwards",
        {"path": "rules/standards-coding.md", "status": "modified", "before": "1.1.1", "after": "1.1.0"},
        "went backwards",
    ),
    (
        "new asset carrying a version",
        {"path": "rules/error-surfacing-quality.md", "status": "added", "before": None, "after": "1.0.0"},
        None,
    ),
    (
        "new asset carrying no version",
        {"path": "rules/error-surfacing-quality.md", "status": "added", "before": None, "after": None},
        "declares no version",
    ),
    (
        "deleted asset owes nothing",
        {"path": "rules/retired.md", "status": "deleted", "before": "1.0.0", "after": None},
        None,
    ),
    (
        "an index is not a versioned asset",
        {"path": "rules/INDEX.md", "status": "modified", "before": None, "after": None},
        None,
    ),
    (
        "a Skill README is not the versioned file",
        {"path": "skills/review-error-surfacing/README.md", "status": "modified", "before": None, "after": None},
        None,
    ),
    (
        "a script is not a versioned asset",
        {"path": "scripts/check-doc-hygiene.py", "status": "modified", "before": None, "after": None},
        None,
    ),
    (
        "a document is not a versioned asset",
        {"path": "docs/guides/releasing.md", "status": "modified", "before": None, "after": None},
        None,
    ),
]

# is_versioned_asset decides membership on its own and is pinned separately,
# because a path that silently stops being an asset is how this check would go
# quiet without failing.
MEMBERSHIP = [
    ("skills/review-diff/SKILL.md", True),
    ("rules/testing-quality.md", True),
    ("specs/rule-modeling.md", True),
    ("protocols/im-notification-delivery.md", True),
    ("skills/review-diff/README.md", False),
    ("skills/INDEX.md", False),
    ("rules/INDEX.md", False),
    ("specs/INDEX.md", False),
    ("protocols/INDEX.md", False),
    ("docs/guides/releasing.md", False),
    ("scripts/check-asset-versions.py", False),
    ("CHANGELOG.md", False),
]


def main() -> int:
    checker = load_checker()
    failures: list[str] = []

    for path, expected in MEMBERSHIP:
        actual = checker.is_versioned_asset(path)
        if actual != expected:
            failures.append(
                f"membership: {path} — expected {'an asset' if expected else 'not an asset'}, got the opposite"
            )

    for label, change, fragment in CASES:
        findings = checker.version_findings([change])
        if fragment is None:
            if findings:
                failures.append(f"{label}: expected nothing, got {findings}")
            continue
        if not findings:
            failures.append(f"{label}: expected a finding containing {fragment!r}, got nothing")
        elif not any(fragment in finding for finding in findings):
            failures.append(f"{label}: expected {fragment!r}, got {findings}")
        elif not any(change["path"] in finding for finding in findings):
            failures.append(f"{label}: the finding does not name {change['path']}, got {findings}")

    # Several changes in one range are reported together, not one at a time.
    together = checker.version_findings([
        {"path": "rules/standards-coding.md", "status": "modified", "before": "1.0.2", "after": "1.0.2"},
        {"path": "skills/review-diff/SKILL.md", "status": "modified", "before": "1.0.0", "after": "1.0.0"},
        {"path": "rules/testing-quality.md", "status": "modified", "before": "1.0.0", "after": "1.1.0"},
    ])
    if len(together) != 2:
        failures.append(f"batch: expected 2 findings across 3 changes, got {len(together)}: {together}")

    if failures:
        print("Asset-version check tests failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        f"Validated the asset-version decision on {len(CASES)} change shapes, "
        f"{len(MEMBERSHIP)} membership cases and one multi-change range."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

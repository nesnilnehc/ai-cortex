#!/usr/bin/env python3
"""Check that every versioned asset a range edits also moved its version.

An asset's version is what a consuming project reads to decide whether to
re-read it, so an edited asset whose version is unchanged tells that project
something untrue. docs/guides/releasing.md states the obligation; nothing was
enforcing it, and the gap surfaced the way gaps here usually do — during the
0.3.0 release, by hand, after orchestrate-code-review gained a dispatch step
and kept its version through a fully green CI run.

The decision is mechanical, so it is a check rather than a review criterion.
What it cannot decide is whether the *size* of a bump is right: moving 1.0.0 to
1.0.1 for a breaking change satisfies this check and still misleads a reader.
That judgement stays with CONTRIBUTING's versioning rules and a reviewer.

Default range: the most recent product tag to HEAD. Pass a range to override.
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]

VERSION_LINE = re.compile(r"^version:\s*(.+?)\s*$", re.MULTILINE)
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)")

# A directory holding versioned assets, and the filename that carries the
# version. A Skill's version lives in SKILL.md; its README carries none.
ASSET_DIRS = {
    "skills": "SKILL.md",
    "rules": "*.md",
    "specs": "*.md",
    "protocols": "*.md",
}


def is_versioned_asset(path: str) -> bool:
    """Decide whether this repository path carries a version of its own.

    An INDEX.md is generated or hand-maintained registry, not an asset, and a
    Skill's README sits beside the file that carries the version rather than
    carrying one itself.
    """
    parts = pathlib.PurePosixPath(path).parts
    if len(parts) < 2 or parts[0] not in ASSET_DIRS:
        return False
    if parts[-1] == "INDEX.md":
        return False
    if parts[0] == "skills":
        return len(parts) == 3 and parts[2] == "SKILL.md"
    return len(parts) == 2 and parts[1].endswith(".md")


def declared_version(text: str | None) -> str | None:
    """Read the version out of a file's frontmatter, or None when it has none."""
    if not text:
        return None
    match = VERSION_LINE.search(text)
    return match.group(1) if match else None


def _semver(value: str) -> tuple[int, int, int] | None:
    match = SEMVER.match(value)
    return tuple(int(part) for part in match.groups()) if match else None


def version_findings(changes: list[dict]) -> list[str]:
    """Report every change that owes a version move and did not make one.

    Each change carries `path`, `status` (added / modified / deleted) and the
    version `before` and `after` the range. A deletion owes nothing, and a file
    that gained a version field where it had none has moved in the only
    direction available to it.
    """
    findings: list[str] = []
    for change in changes:
        path = change["path"]
        if not is_versioned_asset(path):
            continue
        status = change["status"]
        if status == "deleted":
            continue
        before, after = change.get("before"), change.get("after")

        if status == "added":
            if after is None:
                findings.append(f"{path}: is new and declares no version")
            continue

        if after is None:
            findings.append(f"{path}: was edited and no longer declares a version")
            continue
        if before is None:
            continue
        if after == before:
            findings.append(
                f"{path}: was edited and its version is still {before} — "
                "a consuming project reads that version to decide whether to re-read the file"
            )
            continue
        old, new = _semver(before), _semver(after)
        if old and new and new < old:
            findings.append(f"{path}: version went backwards, {before} to {after}")
    return findings


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        capture_output=True, text=True, check=True,
    ).stdout


def _file_at(ref: str, path: str) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{ref}:{path}"],
        capture_output=True, text=True,
    )
    return result.stdout if result.returncode == 0 else None


def changes_in_range(base: str, tip: str) -> list[dict]:
    """Build the change records for a git range, reading each side's version."""
    raw = _git("diff", "--name-status", f"{base}..{tip}")
    records: list[dict] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        fields = line.split("\t")
        code, path = fields[0], fields[-1]
        if not is_versioned_asset(path):
            continue
        status = {"A": "added", "D": "deleted"}.get(code[0], "modified")
        records.append({
            "path": path,
            "status": status,
            "before": declared_version(_file_at(base, path)),
            "after": declared_version(_file_at(tip, path)),
        })
    return records


def latest_product_tag() -> str | None:
    tags = _git("tag", "--list", "v*", "--sort=-v:refname").split()
    return tags[0] if tags else None


def main() -> int:
    argv = sys.argv[1:]
    if argv:
        base, _, tip = argv[0].partition("..")
        tip = tip or "HEAD"
    else:
        base = latest_product_tag()
        if base is None:
            # Not a pass. A shallow CI checkout fetches no tags, and a check
            # that reports nothing because it found nothing to read is
            # indistinguishable from one that read everything and approved it.
            print(
                "NOTHING CHECKED: no product tag is reachable, so no range was compared.\n"
                "In CI this means the checkout fetched no tags — use fetch-depth: 0, "
                "or pass an explicit <base>..<tip> range.",
                file=sys.stderr,
            )
            return 1
        tip = "HEAD"

    try:
        changes = changes_in_range(base, tip)
    except subprocess.CalledProcessError as exc:
        print(f"Cannot read the range {base}..{tip}: {exc.stderr.strip()}", file=sys.stderr)
        return 1

    findings = version_findings(changes)
    if findings:
        print(f"Assets edited in {base}..{tip} whose version did not move:")
        for finding in findings:
            print(f"- {finding}")
        print(
            "\nBump each one per CONTRIBUTING's versioning rules. A metadata-only "
            "correction is still a PATCH."
        )
        return 1

    print(
        f"Checked {len(changes)} versioned asset change(s) in {base}..{tip}; "
        "every edited asset moved its version."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Check the two document-hygiene criteria CI can decide mechanically.

Orphans come from rules/doc-health-criteria.md §2 — every document must be
reachable by link from the README or an INDEX. Temporary filenames come from
rules/repo-structure-hygiene.md §4 and rules/workflow-documentation.md — a
backup extension, or a summarising word used as the name of a document.

Whether a document is *semantically* stale is not decided here; that needs a
reader. This script only reports what a path and a link graph can prove.
"""

from __future__ import annotations

import collections
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(((?!https?://|#|mailto:)[^)]+)\)")
FRONTMATTER_STATUS = re.compile(r"^status:\s*(\S+)\s*$", re.MULTILINE)

# Not part of the documentation graph: vendored copies, runtime config,
# deliberately unlinked test inputs, and GitHub's own convention files.
EXCLUDED_DIRS = (".git", "node_modules", ".cortex", "tests/fixtures", ".github")

# A reader enters the repository through one of these, so none of them needs
# an inbound link of its own.
ENTRY_FILENAMES = {
    "README.md",
    "INDEX.md",
    "AGENTS.md",
    "CLAUDE.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CODE_OF_CONDUCT.md",
}

# Uppercase because the repository names documents in kebab-case: an
# uppercase token is what a leftover process record looks like. Matching
# case-insensitively would flag every review-* Skill.
TEMP_NAME_TOKENS = {
    "SUMMARY",
    "COMPLETE",
    "FINAL",
    "NOTES",
    "UPDATES",
    "OPTIMIZATION",
    "DEPRECATED",
    "OLD",
    "UNUSED",
    "LEGACY",
    "TEMP",
    "TMP",
    "WIP",
    "BACKUP",
    "COPY",
}
TEMP_SUFFIXES = (".bak", ".tmp", ".orig", ".swp", ".rej")


def in_scope(path: pathlib.Path) -> bool:
    parts = path.relative_to(ROOT).parts
    joined = "/".join(parts)
    return not any(
        joined == d or joined.startswith(d + "/") for d in EXCLUDED_DIRS
    )


def markdown_files() -> set[pathlib.Path]:
    return {p.resolve() for p in ROOT.rglob("*.md") if in_scope(p.resolve())}


def outbound_links(path: pathlib.Path) -> set[pathlib.Path]:
    """Resolve every relative markdown link, mapping a directory to its index."""
    found: set[pathlib.Path] = set()
    in_fence = False
    for line in path.read_text(encoding="utf-8").split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for match in LINK.finditer(line):
            target = match.group(1).split("#")[0].strip()
            if not target:
                continue
            resolved = (path.parent / target).resolve()
            if resolved.is_dir():
                for index_name in ("INDEX.md", "README.md"):
                    if (resolved / index_name).exists():
                        resolved = resolved / index_name
                        break
            found.add(resolved)
    return found


def is_tombstone(path: pathlib.Path) -> bool:
    """A deprecated document is unlinked on purpose.

    It stays so that a bookmark or a search result arriving from outside the
    repository lands somewhere that explains the change. Requiring an inbound
    link would defeat that, so `status: deprecated` exempts it.
    """
    head = path.read_text(encoding="utf-8")[:2000]
    match = FRONTMATTER_STATUS.search(head)
    return bool(match) and match.group(1) == "deprecated"


def find_orphans(files: set[pathlib.Path]) -> list[pathlib.Path]:
    roots = {f for f in files if f.name in ENTRY_FILENAMES}
    reached = set(roots)
    queue = collections.deque(roots)
    while queue:
        for target in outbound_links(queue.popleft()):
            if target in files and target not in reached:
                reached.add(target)
                queue.append(target)
    return sorted(f for f in files - reached if not is_tombstone(f))


def find_temp_names(files: set[pathlib.Path]) -> list[tuple[pathlib.Path, str]]:
    """Flag process-record names among the documents, backups among all files.

    A backup carries its own extension — `usage.md.bak` is not a `.md` file —
    so the suffix check has to walk every file, not just the document set.
    """
    hits = {}
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        resolved = path.resolve()
        if not in_scope(resolved):
            continue
        if resolved.name.endswith(TEMP_SUFFIXES):
            hits[resolved] = "backup or editor leftover extension"
    for path in files:
        tokens = set(re.split(r"[-_. ]+", path.name.rsplit(".", 1)[0]))
        flagged = sorted(tokens & TEMP_NAME_TOKENS)
        if flagged:
            hits[path] = f"process-record word in the filename: {', '.join(flagged)}"
    return sorted(hits.items())


def main() -> int:
    files = markdown_files()
    orphans = find_orphans(files)
    temp_names = find_temp_names(files)

    if orphans:
        print("Orphaned documents — nothing links here, so no reader can find them:")
        for path in orphans:
            print(f"- {path.relative_to(ROOT)}")
        print(
            "  Fix: link it from the README or the INDEX of its directory, "
            "delete it, or mark it `status: deprecated` if it is a tombstone."
        )
    if temp_names:
        print("Temporary or stale filenames:")
        for path, reason in temp_names:
            print(f"- {path.relative_to(ROOT)} — {reason}")
        print(
            "  Fix: rename it to what it is, move it under a dated draft path, "
            "or delete it. See rules/repo-structure-hygiene.md §4."
        )

    if orphans or temp_names:
        return 1

    print(f"Checked {len(files)} documents: no orphans, no temporary filenames.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Check the document-hygiene criteria CI can decide mechanically.

Orphans come from rules/doc-health-criteria.md §2 — every document must be
reachable by link from an entry document. This module is where that rule's
"any other root-level document the project designates" is designated:
ENTRY_FILENAMES below is the set, and a tombstone — a document marked
`status: deprecated`, kept unlinked on purpose so a link from outside still
lands — is exempt, per is_tombstone. Temporary filenames come from
rules/repo-structure-hygiene.md §4 and rules/workflow-documentation.md — a
backup extension, or a summarising word used as the name of a document.

The third check reads rules/workflow-documentation.md the way the rule is
written: a body pattern does not condemn a document, it identifies it as a
temporary one, and constraint 4 then requires such a document to carry a date
prefix or a `.draft` suffix and to live in a dedicated directory. A dated
design snapshot narrating its own history is therefore compliant; the same
sentence in a Spec or a Skill is not.

Whether a document is *semantically* stale is not decided here; that needs a
reader. This script only reports what a path, a link graph and a literal
pattern can prove.
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

# rules/workflow-documentation.md, "Identifying a temporary document". Version
# narration and conversational residue, in both corpora. A hit says the
# document is a temporary one, not that it is wrong.
TEMPORARY_BODY = (
    re.compile(r"^Version `?\d+\.\d+\.\d+"),
    re.compile(r"\b(?:since|as of) v?\d+\.\d+\b", re.I),
    re.compile(
        r"\b(?:removed|added|simplified|reverted|introduced|dropped|renamed) in v?\d+\.\d+\b",
        re.I,
    ),
    re.compile(r"\bv?\d+\.\d+ onwards?\b", re.I),
    re.compile(r"^#{1,6} .*\((?:new|added|deprecated|removed|rewritten|simplified)\)\s*$", re.I),
    re.compile(r"\bfor historical reasons\b", re.I),
    re.compile(r"\bnewly added\b", re.I),
    re.compile(r"\bcarried over from\b", re.I),
    re.compile(r"\bto be built later\b", re.I),
    re.compile(r"\b(?:as|like) (?:mentioned|discussed|noted|stated) (?:above|earlier|previously)\b", re.I),
    re.compile(r"\bthe (?:earlier|previous|original) (?:discussion|conversation|proposal)\b", re.I),
    re.compile(r"\bwe (?:just |earlier |previously )?(?:discussed|talked about|said)\b", re.I),
    re.compile(r"\bI (?:recommend|suggest|think|believe|propose)\b"),
    re.compile(r"\bwe (?:decided|chose|agreed|concluded)\b", re.I),
    re.compile(r"\bafter (?:discussion|discussing|talking)\b", re.I),
    re.compile("v\\d+\\.\\d+ (?:起|移除|简化|回撤|引入)"),
)

# A document may be labelled temporary two ways at once, and needs both.
DEDICATED_DIRS = ("docs/designs/", "experiments/", "meetings/")
DATED_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}-")

# Its genre is narration; the changelog is narration; and the rule that names
# these patterns has to spell them out.
BODY_EXEMPT_FILES = ("CHANGELOG.md", "rules/workflow-documentation.md")
BODY_EXEMPT_DIRS = ("docs/adr/",)

# A pattern shown rather than used: under an anti-pattern heading, marked with
# a cross, or inside quotation marks. The last one carries most of the weight —
# `write a rule, not "we decided to follow the convention"` quotes the form it
# forbids.
QUOTING_HEADING = re.compile(r"anti-?pattern|bad pattern|counter-?example|remediation", re.I)
QUOTED_SPAN = re.compile(r"\"[^\"]*\"|\u201c[^\u201d]*\u201d")


def in_scope(path: pathlib.Path, root: pathlib.Path = ROOT) -> bool:
    parts = path.relative_to(root).parts
    joined = "/".join(parts)
    return not any(
        joined == d or joined.startswith(d + "/") for d in EXCLUDED_DIRS
    )


def markdown_files(root: pathlib.Path = ROOT) -> set[pathlib.Path]:
    return {p.resolve() for p in root.rglob("*.md") if in_scope(p.resolve(), root)}


def outbound_links(path: pathlib.Path) -> set[pathlib.Path]:
    """Resolve every relative markdown link to a path.

    A link to a directory is left unresolved on purpose. Its index or README
    is an entry point in its own right, so nothing about reachability would
    change, and a mutation test showed the resolution reached nothing.
    """
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
            found.add((path.parent / target).resolve())
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


def find_temp_names(
    files: set[pathlib.Path], root: pathlib.Path = ROOT
) -> list[tuple[pathlib.Path, str]]:
    """Flag process-record names among the documents, backups among all files.

    A backup carries its own extension — `usage.md.bak` is not a `.md` file —
    so the suffix check has to walk every file, not just the document set.
    """
    hits = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        resolved = path.resolve()
        if not in_scope(resolved, root):
            continue
        if resolved.name.endswith(TEMP_SUFFIXES):
            hits[resolved] = "backup or editor leftover extension"
    for path in files:
        tokens = set(re.split(r"[-_. ]+", path.name.rsplit(".", 1)[0]))
        flagged = sorted(tokens & TEMP_NAME_TOKENS)
        if flagged:
            hits[path] = f"process-record word in the filename: {', '.join(flagged)}"
    return sorted(hits.items())


def is_labelled_temporary(relative: pathlib.Path) -> bool:
    """A temporary document carries a dated or draft name inside a dedicated directory."""
    posix = relative.as_posix()
    named = bool(DATED_NAME.match(relative.name)) or relative.name.endswith(".draft.md")
    return named and any(posix.startswith(d) for d in DEDICATED_DIRS)


def temporary_markers(path: pathlib.Path) -> list[tuple[int, str]]:
    """Lines that identify this document as a temporary one, quotations excluded."""
    found: list[tuple[int, str]] = []
    in_fence = False
    under_quoting_heading = False
    for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("#"):
            under_quoting_heading = bool(QUOTING_HEADING.search(line))
        if under_quoting_heading or "❌" in line:
            continue
        bare = QUOTED_SPAN.sub("", line)
        for pattern in TEMPORARY_BODY:
            if pattern.search(bare):
                found.append((number, line.strip()))
                break
    return found


def find_unlabelled_temporary(
    files: set[pathlib.Path], root: pathlib.Path = ROOT
) -> list[tuple[pathlib.Path, list[tuple[int, str]]]]:
    """Exemptions are by repository-relative path, so the root is a parameter."""
    hits = []
    for path in sorted(files):
        relative = path.relative_to(root)
        posix = relative.as_posix()
        if posix in BODY_EXEMPT_FILES or any(posix.startswith(d) for d in BODY_EXEMPT_DIRS):
            continue
        if is_labelled_temporary(relative):
            continue
        markers = temporary_markers(path)
        if markers:
            hits.append((path, markers))
    return hits


def main() -> int:
    files = markdown_files()
    orphans = find_orphans(files)
    temp_names = find_temp_names(files)
    unlabelled = find_unlabelled_temporary(files)

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

    if unlabelled:
        print("Temporary documents that are not labelled as temporary:")
        for path, markers in unlabelled:
            print(f"- {path.relative_to(ROOT)}")
            for number, line in markers:
                print(f"    :{number}  {line[:100]}")
        print(
            "  A body narrating its own version history or citing a conversation makes a "
            "document temporary. Fix: move the narration to CHANGELOG.md, an issue or a PR, "
            "or move the document under a dated name in a dedicated directory. See "
            "rules/workflow-documentation.md."
        )

    if orphans or temp_names or unlabelled:
        return 1

    print(
        f"Checked {len(files)} documents: no orphans, no temporary filenames, "
        "no unlabelled temporary documents."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

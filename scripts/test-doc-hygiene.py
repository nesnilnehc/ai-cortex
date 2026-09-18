#!/usr/bin/env python3
"""Test scripts/check-doc-hygiene.py against two fixture trees.

A repository-wide run reports nothing, which on its own proves only that
nothing matched. These fixtures give that result a denominator.

`doc-graph` covers reachability and filenames: an orphan, a tombstone that is
unlinked on purpose, a directory README that is an entry point rather than an
orphan, a backup beside the file it copies, and a lowercase `review-` name
that the uppercase process-record words must not fire on.

`temporary-documents` covers the distinction the third check is built on: a
body pattern identifies a document as temporary, and
rules/workflow-documentation.md then requires such a document to be labelled,
so the same sentence is a finding in a Spec and compliant in a dated design
snapshot.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
TEMPORARY = ROOT / "tests" / "fixtures" / "temporary-documents"
DOC_GRAPH = ROOT / "tests" / "fixtures" / "doc-graph"

# A dated name alone is not a label: the document must also sit in a dedicated
# directory, so specs/2026-09-17-... is still a finding.
# The other six shapes must stay silent: a dated snapshot in a dedicated
# directory, an ADR whose genre is narration, a pattern under an anti-pattern
# heading, one inside quotation marks, one inside a fence, and a clean file.
EXPECTED_UNLABELLED = [
    "docs/designs/undated-design.md",
    "skills/a-skill/SKILL.md",
    "specs/2026-09-17-dated-but-misplaced.md",
    "specs/narrating-its-version.md",
]


# retired.md is a tombstone, reference/README.md an entry point, and the two
# process-record files are linked from the README so their own check owns them.
EXPECTED_ORPHANS = ["guides/lost.md"]

# review-security.md must not appear: matching REVIEW case-insensitively would
# flag every review-* Skill in the repository.
EXPECTED_TEMP_NAMES = ["guides/REVIEW_SUMMARY.md", "guides/usage.md.bak"]


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "check_doc_hygiene", ROOT / "scripts" / "check-doc-hygiene.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    for tree in (TEMPORARY, DOC_GRAPH):
        if not tree.is_dir():
            print(f"missing fixture tree: {tree.relative_to(ROOT)}")
            return 1

    checker = load_checker()
    errors = []

    temporary_files = {p.resolve() for p in TEMPORARY.rglob("*.md")}
    unlabelled = checker.find_unlabelled_temporary(temporary_files, root=TEMPORARY)
    got = sorted(str(path.relative_to(TEMPORARY)) for path, _ in unlabelled)
    if got != EXPECTED_UNLABELLED:
        errors.append(f"unlabelled temporary documents: expected {EXPECTED_UNLABELLED}, got {got}")

    graph_files = checker.markdown_files(DOC_GRAPH)
    got = sorted(str(path.relative_to(DOC_GRAPH)) for path in checker.find_orphans(graph_files))
    if got != EXPECTED_ORPHANS:
        errors.append(f"orphans: expected {EXPECTED_ORPHANS}, got {got}")

    got = sorted(
        str(path.relative_to(DOC_GRAPH))
        for path, _ in checker.find_temp_names(graph_files, root=DOC_GRAPH)
    )
    if got != EXPECTED_TEMP_NAMES:
        errors.append(f"temporary filenames: expected {EXPECTED_TEMP_NAMES}, got {got}")

    if errors:
        print("document hygiene tests failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    findings = len(EXPECTED_UNLABELLED) + len(EXPECTED_ORPHANS) + len(EXPECTED_TEMP_NAMES)
    print(
        f"Validated document hygiene over {len(temporary_files) + len(graph_files)} shapes: "
        f"{findings} findings asserted, every other shape correctly silent."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

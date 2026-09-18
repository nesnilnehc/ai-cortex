#!/usr/bin/env python3
"""Test the temporary-document detection against a fixture tree.

A repository-wide run reports nothing, which on its own proves only that the
patterns matched nothing. These fixtures give that result a denominator, and
pin the distinction the check is built on: a body pattern identifies a
document as temporary, and rules/workflow-documentation.md then requires such
a document to be labelled, so the same sentence is a finding in a Spec and
compliant in a dated design snapshot.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "temporary-documents"

# A dated name alone is not a label: the document must also sit in a dedicated
# directory, so specs/2026-09-17-... is still a finding.
# The other six shapes must stay silent: a dated snapshot in a dedicated
# directory, an ADR whose genre is narration, a pattern under an anti-pattern
# heading, one inside quotation marks, one inside a fence, and a clean file.
EXPECTED = [
    "docs/designs/undated-design.md",
    "skills/a-skill/SKILL.md",
    "specs/2026-09-17-dated-but-misplaced.md",
    "specs/narrating-its-version.md",
]


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "check_doc_hygiene", ROOT / "scripts" / "check-doc-hygiene.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if not FIXTURES.is_dir():
        print(f"missing fixture tree: {FIXTURES.relative_to(ROOT)}")
        return 1

    checker = load_checker()
    files = {p.resolve() for p in FIXTURES.rglob("*.md")}
    hits = checker.find_unlabelled_temporary(files, root=FIXTURES)
    got = sorted(str(path.relative_to(FIXTURES)) for path, _ in hits)

    if got != EXPECTED:
        print("temporary-document detection tests failed:")
        print(f"- expected {EXPECTED}")
        print(f"- got      {got}")
        return 1
    print(
        f"Validated temporary-document detection on {len(files)} shapes: "
        f"{len(EXPECTED)} unlabelled, {len(files) - len(EXPECTED)} correctly silent."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

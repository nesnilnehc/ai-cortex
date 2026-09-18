#!/usr/bin/env python3
"""Test the markdown link checker against a fixture tree.

The repository-wide run reports zero, which proves nothing on its own: a
checker that silently matched nothing would report the same. These fixtures
give it a denominator, and in particular pin the behaviour the checker was
changed for — a link written as an example, inside a fence or a code span,
renders as text and must not be read as a link.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "markdown-links"

# Every other link in the tree is a demonstration: inside a code span, a
# top-level fence, a fence indented into a list item, or a longer fence
# holding a shorter one. None of them may appear.
EXPECTED_BROKEN = ["docs/links.md:5 -> ./missing.md"]
EXPECTED_DOWNWARD = ["rules/downward.md:3"]


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "check_markdown_links", ROOT / "scripts" / "check-markdown-links.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    if not FIXTURES.is_dir():
        print(f"missing fixture tree: {FIXTURES.relative_to(ROOT)}")
        return 1

    broken, downward = load_checker().scan(FIXTURES)
    errors = []
    if broken != EXPECTED_BROKEN:
        errors.append(f"broken links: expected {EXPECTED_BROKEN}, got {broken}")
    if downward != EXPECTED_DOWNWARD:
        errors.append(f"links into skills/: expected {EXPECTED_DOWNWARD}, got {downward}")

    if errors:
        print("markdown link checker tests failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "Validated the markdown link checker: 1 broken link and 1 downward link found, "
        "7 demonstrations in code spans and fences correctly ignored."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

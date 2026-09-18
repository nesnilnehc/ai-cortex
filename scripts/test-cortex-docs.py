#!/usr/bin/env python3
"""Test the cortex documentation check against a clean and a drifted tree.

The repository-wide run reports nothing, which alone proves only that the
comparison found nothing to say. The drifted tree gives it a denominator and
pins one finding per branch: a command the script does not have, a flag it
does not have, and a command no document mentions.

The clean tree carries the sentence that made the first draft wrong — prose
saying "bin/cortex run from inside a clone" — so a checker that reads prose
as code fails here rather than in the repository.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "cortex-docs"

EXPECTED_DRIFTED = [
    "README.md:5 writes `cortex sync`, which bin/cortex does not accept "
    "(it has: install, status, update)",
    "README.md:6 writes `cortex update --deep`, unknown to bin/cortex",
    "bin/cortex offers `status`, which none of README.md, AGENTS.md, CLAUDE.md, "
    "CONTRIBUTING.md mentions",
]


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "check_cortex_docs", ROOT / "scripts" / "check-cortex-docs.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    for tree in ("clean", "drifted"):
        if not (FIXTURES / tree).is_dir():
            print(f"missing fixture tree: {(FIXTURES / tree).relative_to(ROOT)}")
            return 1

    checker = load_checker()
    errors = []

    clean = checker.check(FIXTURES / "clean")
    if clean:
        errors.append(f"the clean tree reported {clean}")

    drifted = checker.check(FIXTURES / "drifted")
    if drifted != EXPECTED_DRIFTED:
        errors.append(f"the drifted tree: expected {EXPECTED_DRIFTED}, got {drifted}")

    if errors:
        print("cortex documentation tests failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Validated the cortex documentation check: a clean tree is silent and a drifted one "
        f"reports all {len(EXPECTED_DRIFTED)} kinds of drift."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

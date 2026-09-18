#!/usr/bin/env python3
"""Test the README asset-count check against a clean and a drifted tree.

The repository-wide run reports nothing, which on its own proves only that
the comparison found nothing to say. The drifted tree gives it a denominator
and pins each of the three things it can report: a declared count that no
longer matches, a layer the README stopped mentioning, and a capability table
whose column no longer sums to the total.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "asset-counts"

EXPECTED_STALE = [
    "README declares 5 skills; skills/ holds 2",
    "README declares no rule count; rules/ holds 3",
    "the capability table sums to 3 across 2 areas, but the README declares 5 skills",
]


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "check_asset_counts", ROOT / "scripts" / "check-asset-counts.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    for tree in ("clean", "stale"):
        if not (FIXTURES / tree).is_dir():
            print(f"missing fixture tree: {(FIXTURES / tree).relative_to(ROOT)}")
            return 1

    checker = load_checker()
    errors = []

    clean = checker.check_counts(FIXTURES / "clean")
    if clean:
        errors.append(f"the clean tree reported {clean}")

    stale = checker.check_counts(FIXTURES / "stale")
    if stale != EXPECTED_STALE:
        errors.append(f"the drifted tree: expected {EXPECTED_STALE}, got {stale}")

    if errors:
        print("asset-count tests failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Validated the README asset-count check: a clean tree is silent and a drifted one "
        f"reports all {len(EXPECTED_STALE)} kinds of drift."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

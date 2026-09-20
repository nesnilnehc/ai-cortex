#!/usr/bin/env python3
"""Check that check-findings-contract.py reports each shape it claims to decide.

The checker exists because 12 Skills restated the finding element list inline
instead of citing the Spec, so a change to the Spec reached 15 consumers and
silently missed 12. A checker guarding against that must itself be shown to
still fail, or it becomes the same kind of quiet pass it was built to prevent.
"""

from __future__ import annotations

import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

# text, must it be reported, why this shape is in the set
CASES = [
    ("Each finding includes Location, Category, Severity, Title, Description, and optional Suggestion",
     True, "the plain restatement the checker was built for"),
    ("every finding carries location, category (`language-go`), severity, title, description, and an optional suggestion",
     True, "lower case, with a parenthesised category"),
    ("Is each finding emitted with Location, Category=language-sql, Severity, Title, Description, and optional Suggestion?",
     True, "a checklist question with an inline category value"),
    ("Emit findings with Location, Category, Severity, Title, Description, Suggestion.",
     True, "a run with no 'and' before the last element"),
    ("every finding carries every element [findings-list](../../specs/findings-list.md) §5.1 requires",
     False, "the citation that replaced the restatement"),
    ("Return Rule coverage using the exact `passed`, `waived` and `not_applicable` fields from the findings-list Spec.",
     False, "another citation, naming different fields"),
    ("Cite a concrete location, and give the severity the Rule's default.",
     False, "prose naming two elements, which is legitimate use"),
    ("Sorts by severity, then by location.",
     False, "prose naming two elements in the other order"),
]


def load():
    spec = importlib.util.spec_from_file_location(
        "check_findings_contract", ROOT / "scripts" / "check-findings-contract.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    module = load()
    errors = []
    for text, expected, why in CASES:
        actual = module.restates_contract(text)
        if actual != expected:
            errors.append(
                f"{'expected a report' if expected else 'expected no report'} "
                f"({why}): {text!r}"
            )
    if errors:
        print("check-findings-contract checker test failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    reported = sum(1 for _, expected, _ in CASES if expected)
    print(
        f"Validated the findings-contract checker over {len(CASES)} shapes: "
        f"{reported} restatements reported, {len(CASES) - reported} legitimate uses left alone."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

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
import tempfile

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


# Three shapes for the directory walk: a Skill that emits findings and restates
# the list, one that emits and cites the Spec, and one that emits nothing. The
# walk decides which files it even opens, and until `check` took a `root` it
# could not be pointed at a fixture, so only `restates_contract` was covered.
WALK_FIXTURE = {
    "review-restater": "output type: findings-list\n"
    "Each finding includes Location, Category, Severity, Title, Description, and optional Suggestion\n",
    "review-citer": "output type: findings-list\n"
    "Every finding carries every element the findings-list Spec requires\n",
    "define-something": "This Skill writes a document and emits no findings.\n"
    "It mentions a location, a category and a severity in passing.\n",
}
EXPECTED_WALK = {"findings": 1, "emitters": 2}


def check_walk(module) -> list[str]:
    """Run check() over the three-shape fixture and report what disagrees."""
    with tempfile.TemporaryDirectory() as tmp:
        base = pathlib.Path(tmp) / "skills"
        for name, body in WALK_FIXTURE.items():
            (base / name).mkdir(parents=True)
            (base / name / "SKILL.md").write_text(body, encoding="utf-8")
        findings, emitters = module.check(base, root=base)
    problems = []
    actual = {"findings": len(findings), "emitters": emitters}
    if actual != EXPECTED_WALK:
        problems.append(f"the walk reported {actual}, expected {EXPECTED_WALK}")
    if findings and not findings[0].startswith("review-restater/SKILL.md:2:"):
        problems.append(
            f"a finding must name its file and line relative to the given root, got {findings[0]!r}"
        )
    return problems


def main() -> int:
    module = load()
    errors = []
    errors.extend(check_walk(module))
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
        f"{reported} restatements reported, {len(CASES) - reported} legitimate uses left alone, "
        "and the directory walk over three Skill shapes."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

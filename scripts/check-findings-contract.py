#!/usr/bin/env python3
"""Report a Skill that restates the finding element list instead of citing the Spec.

specs/findings-list.md owns what a finding carries. Twelve Skills had copied
that list into their own prose, so adding the `Maturity` element reached the 15
Skills that cite the Spec and silently missed the 12 that did not — a change
lands in one place and half its consumers never hear about it.

The check is deliberately narrow. It reports a run of four or more element
names joined by commas, which is a copy of the table and nothing else; prose
naming one or two elements ("cite a concrete location", "sorts by severity,
then by location") is legitimate and is left alone. Per
rules/workflow-rule-governance.md §9, a check whose findings are mostly
legitimate use is a defect in the check.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
SPEC = "specs/findings-list.md"

_ELEMENT = r"(?:location|category|severity|title|description|suggestion|maturity)"
# One element, then three more joined by a comma or "and" — four in a run. A
# parenthesised or `=`-suffixed category counts as the same element, since
# `Category (\`language-go\`)` is how the copies spell it.
_QUALIFIER = r"(?:\s*(?:\([^)]*\)|=[\w.-]+))?"
_JOINER = r"(?:\s*,\s*|\s*,?\s+and\s+)"
_LEAD = r"(?:(?:an?|the|optional|optionally)\s+)*"
RESTATEMENT = re.compile(
    rf"\b{_ELEMENT}\b{_QUALIFIER}(?:{_JOINER}{_LEAD}\b{_ELEMENT}\b{_QUALIFIER}){{3,}}",
    re.IGNORECASE,
)


def restates_contract(line: str) -> bool:
    """Decide whether one line copies the finding element list.

    A line that links or refers to the Spec is citing it, however it goes on to
    phrase the elements, so it is never reported.

    参数: line - one line of Skill prose
    返回: True when the line restates the list rather than citing the Spec
    """
    if "findings-list" in line:
        return False
    return RESTATEMENT.search(line) is not None


def check(skills_dir: pathlib.Path) -> list[str]:
    """Report every restatement under one skills directory, as file:line strings."""
    findings: list[str] = []
    for path in sorted(skills_dir.glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if "findings-list" not in text:
            # Not a Skill that emits findings; its prose is none of this check's
            # business, and reading it as such is how a check earns false
            # positives.
            continue
        for number, line in enumerate(text.split("\n"), start=1):
            if restates_contract(line):
                findings.append(f"{path.relative_to(ROOT)}:{number}: {line.strip()}")
    return findings


def main() -> int:
    findings = check(SKILLS_DIR)
    if findings:
        print(f"Skills restating the finding element list instead of citing {SPEC}:")
        for finding in findings:
            print(f"- {finding}")
        print(
            f"\nCite the Spec instead — \"every element [findings-list]({SPEC}) §5.1 "
            "requires\" — so a change to it reaches this Skill."
        )
        return 1
    emitters = sum(
        1
        for path in SKILLS_DIR.glob("*/SKILL.md")
        if "findings-list" in path.read_text(encoding="utf-8")
    )
    print(
        f"Checked {emitters} findings-emitting Skills: every one cites "
        f"{SPEC} rather than restating its element list."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

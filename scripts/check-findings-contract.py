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

    A line that cites the Spec is citing it however it goes on to phrase the
    elements, so it is never reported.
    """
    if "findings-list" in line:
        return False
    return RESTATEMENT.search(line) is not None


def check(
    skills_dir: pathlib.Path, root: pathlib.Path | None = None
) -> tuple[list[str], int]:
    """Report every restatement under one skills directory, and how many Skills emit findings.

    `root` is what a finding's path is made relative to, and defaults to the
    repository. A caller pointing this at a fixture directory passes that
    directory; without it the relative path raises, which is why this function
    went untested while only `restates_contract` was covered.

    The emitter count comes back with the findings rather than from a second
    pass, so the file is read once.
    """
    root = ROOT if root is None else root
    findings: list[str] = []
    emitters = 0
    for path in sorted(skills_dir.glob("*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if "findings-list" not in text:
            # Not a Skill that emits findings; its prose is none of this check's
            # business, and reading it as such is how a check earns false
            # positives.
            continue
        emitters += 1
        for number, line in enumerate(text.split("\n"), start=1):
            if restates_contract(line):
                findings.append(f"{path.relative_to(root)}:{number}: {line.strip()}")
    return findings, emitters


def main() -> int:
    findings, emitters = check(SKILLS_DIR)
    if findings:
        print(f"Skills restating the finding element list instead of citing {SPEC}:")
        for finding in findings:
            print(f"- {finding}")
        print(
            f"\nCite the Spec instead — \"every element [findings-list]({SPEC}) §5.1 "
            "requires\" — so a change to it reaches this Skill."
        )
        return 1
    print(
        f"Checked {emitters} findings-emitting Skills: every one cites "
        f"{SPEC} rather than restating its element list."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

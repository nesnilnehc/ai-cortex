#!/usr/bin/env python3
"""Check that the README's declared asset counts match what is on disk.

The counts are written by hand in one sentence and again as a column in the
capability table, so adding a skill leaves both wrong and nothing notices.
This compares the declared numbers with the directories and files they
describe, and checks that the table's column still sums to the skill total.

It does not judge which area a skill belongs to. That is a reading of the
skill, not something a path can settle; what it can settle is that the
column adds up.
"""

from __future__ import annotations

import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
DECLARED = re.compile(r"\*\*(\d+) (skills?|rules?|specs?|protocols?)\*\*")
TABLE_ROW = re.compile(r"^\| \*\*[^|]+\*\* \| +(\d+) \|", re.MULTILINE)

# Each layer, and how to count it: skills are directories, the rest are
# documents beside their index.
LAYERS = {
    "skill": ("skills", "dirs"),
    "rule": ("rules", "files"),
    "spec": ("specs", "files"),
    "protocol": ("protocols", "files"),
}


def on_disk(root: pathlib.Path, directory: str, kind: str) -> int:
    path = root / directory
    if not path.is_dir():
        return 0
    if kind == "dirs":
        return len([p for p in path.iterdir() if p.is_dir()])
    return len([p for p in path.glob("*.md") if p.name != "INDEX.md"])


def check_counts(root: pathlib.Path) -> list[str]:
    readme = root / "README.md"
    if not readme.is_file():
        return [f"no README.md under {root}"]
    text = readme.read_text(encoding="utf-8")
    problems: list[str] = []

    declared = {}
    for number, noun in DECLARED.findall(text):
        declared[noun.rstrip("s")] = int(number)

    for layer, (directory, kind) in LAYERS.items():
        actual = on_disk(root, directory, kind)
        if layer not in declared:
            problems.append(f"README declares no {layer} count; {directory}/ holds {actual}")
            continue
        if declared[layer] != actual:
            problems.append(
                f"README declares {declared[layer]} {layer}s; {directory}/ holds {actual}"
            )

    rows = [int(n) for n in TABLE_ROW.findall(text)]
    if not rows:
        problems.append("README has no capability table to sum")
    elif "skill" in declared and sum(rows) != declared["skill"]:
        problems.append(
            f"the capability table sums to {sum(rows)} across {len(rows)} areas, "
            f"but the README declares {declared['skill']} skills"
        )

    return problems


def main() -> int:
    problems = check_counts(ROOT)
    if problems:
        print("README asset counts are out of date:")
        for problem in problems:
            print(f"- {problem}")
        print("  Fix: update the counts in README.md, including the capability table column.")
        return 1
    print("README asset counts match the repository, and the capability table sums to the total.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

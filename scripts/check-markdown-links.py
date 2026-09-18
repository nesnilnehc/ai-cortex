#!/usr/bin/env python3
"""Check the repository's markdown link graph.

Two checks share one extractor, because both were getting the same thing
wrong. A link written inside a code fence or a code span is a demonstration,
not a link: it renders as literal text and points nowhere. A checker that
reads it as a link punishes a document for explaining itself — which is
exactly what a Rule defining a no-go zone has to do, per
rules/workflow-documentation.md, whose own exception list says as much.

1. Relative links resolve. No exemption by directory: a record that mentions
   an asset since deleted names it as text, which rules/adr-management.md §4
   explicitly permits.
2. Reference direction. docs/architecture/terminology.md §II: a Spec,
   Protocol or Rule names the capability that applies it and never links down
   into skills/, so a contract does not depend on one implementation of
   itself.
"""

from __future__ import annotations

import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(((?!https?://|#|mailto:)[^)]+)\)")
INTO_SKILLS = re.compile(r"\]\((\.\./)*skills/[^)]*\)")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
CODE_SPAN = re.compile(r"(`+)(?:(?!\1).)*\1", re.DOTALL)
GOVERNANCE_DIRS = ("rules", "specs", "protocols")
# Deliberately malformed inputs for scripts/test-markdown-links.py. Scanning
# them repository-wide would report the defects they exist to carry.
EXCLUDED = ("tests/fixtures",)


def linkable_lines(path: pathlib.Path) -> list[tuple[int, str]]:
    """Yield (line number, line) with fenced blocks and code spans removed.

    A fence may be indented, since a fenced block nested inside a list item
    carries the item's indentation. The closing fence is matched on its
    marker character and length so a longer outer fence can contain a shorter
    inner one.
    """
    out: list[tuple[int, str]] = []
    open_marker: str | None = None
    for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
        match = FENCE.match(line)
        if open_marker is None:
            if match:
                open_marker = match.group(1)
                continue
        else:
            if match and match.group(1)[0] == open_marker[0] and len(match.group(1)) >= len(open_marker):
                open_marker = None
            continue
        out.append((number, CODE_SPAN.sub("", line)))
    return out


def scan(root: pathlib.Path) -> tuple[list[str], list[str]]:
    """Return (broken relative links, governance links into skills/)."""
    broken: list[str] = []
    downward: list[str] = []

    for path in sorted(p for p in root.rglob("*.md") if ".git" not in p.parts):
        relative = path.relative_to(root)
        joined = relative.as_posix()
        if any(joined.startswith(d + "/") for d in EXCLUDED):
            continue
        governance = relative.parts[0] in GOVERNANCE_DIRS
        for number, line in linkable_lines(path):
            for match in LINK.finditer(line):
                target = match.group(1).split("#")[0]
                if target and not (path.parent / target).resolve().exists():
                    broken.append(f"{relative}:{number} -> {target}")
            if governance and INTO_SKILLS.search(line):
                downward.append(f"{relative}:{number}")

    return broken, downward


def main() -> int:
    broken, downward = scan(ROOT)

    print(f"broken relative links: {len(broken)}")
    for item in broken:
        print(f"  {item}")
    print(f"governance assets linking into skills/: {len(downward)}")
    for item in downward:
        print(f"  {item}")
    if downward:
        print("  a Spec, Protocol or Rule must not link into skills/ — name the capability instead")

    return 1 if broken or downward else 0


if __name__ == "__main__":
    sys.exit(main())

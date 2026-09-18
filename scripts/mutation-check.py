#!/usr/bin/env python3
"""Check that the repository's own checks can fail.

Every test here asserts a list of findings over a fixture tree, and a test
like that passes just as happily when the checker has stopped looking. This
seeds a known defect into each checker, runs its test, and requires the test
to go red. A defect that survives means the fixtures do not reach that
branch.

A mutation whose pattern no longer matches its target is reported as a
failure rather than skipped, because a refactor that moves the code silently
takes the coverage with it — the mutation keeps "passing" while testing
nothing.

Sibling: scripts/mutation-test.sh does the same for the translation verifier,
by mutating a document rather than code.
"""

from __future__ import annotations

import pathlib
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]

LINKS = "scripts/check-markdown-links.py"
LINKS_TEST = "scripts/test-markdown-links.py"
HYGIENE = "scripts/check-doc-hygiene.py"
HYGIENE_TEST = "scripts/test-doc-hygiene.py"
SCENARIOS = "scripts/test-rule-scenarios.py"

# (target to mutate, test that must go red, label, before, after[, inside])
# `inside` is a marker the mutation site must follow, for a line that appears
# in more than one function: without it the replacement lands on the first
# occurrence and the branch under test is never touched.
MUTATIONS = [
    (LINKS, LINKS_TEST, "stop stripping inline code spans",
     '        out.append((number, CODE_SPAN.sub("", line)))',
     '        out.append((number, line))'),
    (LINKS, LINKS_TEST, "require a fence to start at column zero",
     'FENCE = re.compile(r"^\\s*(`{3,}|~{3,})")',
     'FENCE = re.compile(r"^(`{3,}|~{3,})")'),
    (LINKS, LINKS_TEST, "close a fence regardless of its marker length",
     "if match and match.group(1)[0] == open_marker[0] and len(match.group(1)) >= len(open_marker):",
     "if match:"),
    (LINKS, LINKS_TEST, "stop skipping fenced blocks",
     "            if match:\n                open_marker = match.group(1)\n                continue",
     "            if match:\n                continue"),
    (LINKS, LINKS_TEST, "stop excluding absolute and mail links",
     'LINK = re.compile(r"\\]\\(((?!https?://|#|mailto:)[^)]+)\\)")',
     'LINK = re.compile(r"\\]\\(([^)]+)\\)")'),
    (LINKS, LINKS_TEST, "stop stripping the anchor from a target",
     '                target = match.group(1).split("#")[0]',
     '                target = match.group(1)'),
    (LINKS, LINKS_TEST, "treat every document as a governance asset",
     "        governance = relative.parts[0] in GOVERNANCE_DIRS",
     "        governance = True"),

    (HYGIENE, HYGIENE_TEST, "drop the tombstone exemption",
     "    return sorted(f for f in files - reached if not is_tombstone(f))",
     "    return sorted(files - reached)"),
    (HYGIENE, HYGIENE_TEST, "drop README from the entry filenames",
     '    "README.md",\n    "INDEX.md",',
     '    "INDEX.md",'),
    (HYGIENE, HYGIENE_TEST, "match process-record words case-insensitively",
     '        tokens = set(re.split(r"[-_. ]+", path.name.rsplit(".", 1)[0]))',
     '        tokens = set(re.split(r"[-_. ]+", path.name.rsplit(".", 1)[0].upper()))'),
    (HYGIENE, HYGIENE_TEST, "stop scanning every file for backup suffixes",
     '    for path in root.rglob("*"):',
     '    for path in root.rglob("*.md"):'),
    (HYGIENE, HYGIENE_TEST, "stop excluding .cortex from the scan",
     'EXCLUDED_DIRS = (".git", "node_modules", ".cortex", "tests/fixtures", ".github")',
     'EXCLUDED_DIRS = (".git", "node_modules", "tests/fixtures", ".github")'),
    (HYGIENE, HYGIENE_TEST, "stop skipping fenced blocks when collecting links",
     "        if in_fence:\n            continue\n",
     "", "def outbound_links"),
    (HYGIENE, HYGIENE_TEST, "stop skipping fenced blocks when reading a body",
     "        if in_fence:\n            continue\n",
     "", "def temporary_markers"),
    (HYGIENE, HYGIENE_TEST, "stop following links at all",
     "            if target in files and target not in reached:",
     "            if False:"),
    (HYGIENE, HYGIENE_TEST, "stop excluding quoted spans",
     '        bare = QUOTED_SPAN.sub("", line)',
     "        bare = line"),
    (HYGIENE, HYGIENE_TEST, "stop skipping anti-pattern headings",
     'if under_quoting_heading or "❌" in line:',
     'if "❌" in line:'),
    (HYGIENE, HYGIENE_TEST, "treat any dated name as labelled, ignoring the directory",
     "    return named and any(posix.startswith(d) for d in DEDICATED_DIRS)",
     "    return named"),
    (HYGIENE, HYGIENE_TEST, "treat any dedicated directory as labelled, ignoring the name",
     "    return named and any(posix.startswith(d) for d in DEDICATED_DIRS)",
     "    return any(posix.startswith(d) for d in DEDICATED_DIRS)"),
    (HYGIENE, HYGIENE_TEST, "drop the ADR genre exemption",
     "if posix in BODY_EXEMPT_FILES or any(posix.startswith(d) for d in BODY_EXEMPT_DIRS):",
     "if posix in BODY_EXEMPT_FILES:"),
    (HYGIENE, HYGIENE_TEST, "stop requiring the document to be unlabelled",
     "        if is_labelled_temporary(relative):\n            continue\n",
     ""),

    (SCENARIOS, SCENARIOS, "drop the protected-public-contract exclusion",
     '        if symbol.get("protected_public_contract"):\n            continue\n',
     ""),
    (SCENARIOS, SCENARIOS, "drop the live-consumer exclusion",
     '        if symbol.get("live_consumer_evidence"):\n            continue\n',
     ""),
    (SCENARIOS, SCENARIOS, "stop failing a symbol neither removed nor shown live",
     '        if not symbol.get("removed"):\n            failed.add("ARC-010")\n        elif',
     '        if False:\n            failed.add("ARC-010")\n        elif'),
    (SCENARIOS, SCENARIOS, "accept a removal made on the analyzer's word alone",
     '        elif not symbol.get("statically_resolvable", True) and not symbol.get(\n            "runtime_signal_full_cycle"\n        ):\n            failed.add("ARC-010")\n',
     ""),
    (SCENARIOS, SCENARIOS, "drop the external-dependency exclusion",
     '        if marker.get("external_dependency"):\n            continue\n',
     ""),
    (SCENARIOS, SCENARIOS, "stop requiring owner, removal point and replacement",
     '        if not all(marker.get(field) for field in ("owner", "removal_point", "replacement")):\n            failed.add("ARC-011")\n        elif',
     '        if False:\n            failed.add("ARC-011")\n        elif'),
    (SCENARIOS, SCENARIOS, "accept a removal point that passed with no action",
     '        elif marker.get("removal_point_passed") and not (\n            marker.get("removed") or marker.get("renewed")\n        ):\n            failed.add("ARC-011")\n',
     ""),
]


def main() -> int:
    failures: list[str] = []
    by_target: dict[str, int] = {}

    for mutation in MUTATIONS:
        target, test, label, before, after = mutation[:5]
        inside = mutation[5] if len(mutation) > 5 else None
        path = ROOT / target
        original = path.read_text(encoding="utf-8")
        head, separator, tail = original.partition(inside) if inside else ("", "", original)
        if inside and not separator:
            failures.append(f"{target}: the mutation \"{label}\" cannot find {inside}")
            continue
        if before not in tail:
            failures.append(f"{target}: the mutation \"{label}\" no longer matches its target")
            continue
        path.write_text(head + separator + tail.replace(before, after, 1), encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / test)], capture_output=True, text=True, cwd=ROOT
            )
        finally:
            path.write_text(original, encoding="utf-8")
        if result.returncode == 0:
            failures.append(f"{target}: the mutation \"{label}\" survived {test}")
        by_target[target] = by_target.get(target, 0) + 1

    if failures:
        print("Mutation check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    summary = ", ".join(f"{pathlib.Path(t).name}: {n}" for t, n in sorted(by_target.items()))
    print(f"Every mutation was caught ({summary}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

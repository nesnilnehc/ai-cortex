#!/usr/bin/env python3
"""Check that the repository's own checks can fail.

Every check here reports a verdict over material it reads, and a clean
verdict proves nothing on its own: a checker that has stopped looking returns
exactly the same thing. This perturbs the material, or the invocation, and
requires the verdict to change.

Two shapes of perturbation, one frame:

- A **code** mutation seeds a defect into a checker and requires its fixture
  test to go red. A fixture suite that stays green has a branch it never
  reaches.
- A **document** mutation edits an already-translated file against its own
  HEAD state — so the residual-Chinese check does not fire and each edit is
  isolated — and requires the translation verifier to block it. The controls
  run the other way: a reworded sentence must be allowed, or the verifier is
  merely refusing everything.

A mutation whose pattern no longer matches its target is a failure, not a
skip. A refactor that moves the code, or an edit to the document the
translation cases quote, takes the coverage with it, and a harness that
shrugged would keep reporting success over nothing. That coupling is
deliberate: `rules/task-quality.md` is quoted here, so changing it means
updating these cases. The predecessor of this script skipped instead, and by
the time it was folded in, eleven of its fifteen cases had stopped matching
the document they were written against.
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys
from typing import Callable, NamedTuple


ROOT = pathlib.Path(__file__).resolve().parents[1]

LINKS = "scripts/check-markdown-links.py"
LINKS_TEST = "scripts/test-markdown-links.py"
HYGIENE = "scripts/check-doc-hygiene.py"
HYGIENE_TEST = "scripts/test-doc-hygiene.py"
SCENARIOS = "scripts/test-rule-scenarios.py"
COUNTS = "scripts/check-asset-counts.py"
COUNTS_TEST = "scripts/test-asset-counts.py"
CORTEX = "scripts/check-cortex-docs.py"
CORTEX_TEST = "scripts/test-cortex-docs.py"
VERSIONS = "scripts/check-asset-versions.py"
VERSIONS_TEST = "scripts/test-asset-versions.py"
RULES = "scripts/validate-rules.py"
RULES_TEST = "scripts/test-validate-rules.py"
TRANSLATED = "rules/task-quality.md"
VERIFIER = "scripts/verify-translation.py"


class Perturbation(NamedTuple):
    label: str
    command: tuple[str, ...]
    target: str | None = None
    edit: Callable[[str], str] | None = None
    expect: str = "blocked"
    allow_unchanged: bool = False


def replace(before: str, after: str, inside: str | None = None) -> Callable[[str], str]:
    """Replace one occurrence, optionally only after a marker.

    Without the marker a line that appears in two functions absorbs the edit
    at its first occurrence, and the branch under test is never touched.
    """

    def edit(text: str) -> str:
        head, separator, tail = text.partition(inside) if inside else ("", "", text)
        if inside and not separator:
            return text
        if before not in tail:
            return text
        return head + separator + tail.replace(before, after, 1)

    return edit


def code(target: str, test: str, label: str, before: str, after: str, inside: str | None = None):
    return Perturbation(label, (test,), target, replace(before, after, inside))


def document(label: str, edit: Callable[[str], str], expect: str = "blocked", allow_unchanged: bool = False):
    return Perturbation(label, (VERIFIER, "HEAD", TRANSLATED), TRANSLATED, edit, expect, allow_unchanged)


PERTURBATIONS = [
    code(LINKS, LINKS_TEST, "stop stripping inline code spans",
     '        out.append((number, CODE_SPAN.sub("", line)))',
     '        out.append((number, line))'),
    code(LINKS, LINKS_TEST, "require a fence to start at column zero",
     'FENCE = re.compile(r"^\\s*(`{3,}|~{3,})")',
     'FENCE = re.compile(r"^(`{3,}|~{3,})")'),
    code(LINKS, LINKS_TEST, "close a fence regardless of its marker length",
     "if match and match.group(1)[0] == open_marker[0] and len(match.group(1)) >= len(open_marker):",
     "if match:"),
    code(LINKS, LINKS_TEST, "stop skipping fenced blocks",
     "            if match:\n                open_marker = match.group(1)\n                continue",
     "            if match:\n                continue"),
    code(LINKS, LINKS_TEST, "stop excluding absolute and mail links",
     'LINK = re.compile(r"\\]\\(((?!https?://|#|mailto:)[^)]+)\\)")',
     'LINK = re.compile(r"\\]\\(([^)]+)\\)")'),
    code(LINKS, LINKS_TEST, "stop stripping the anchor from a target",
     '                target = match.group(1).split("#")[0]',
     '                target = match.group(1)'),
    code(LINKS, LINKS_TEST, "treat every document as a governance asset",
     "        governance = relative.parts[0] in GOVERNANCE_DIRS",
     "        governance = True"),
    code(HYGIENE, HYGIENE_TEST, "drop the tombstone exemption",
     "    return sorted(f for f in files - reached if not is_tombstone(f))",
     "    return sorted(files - reached)"),
    code(HYGIENE, HYGIENE_TEST, "drop README from the entry filenames",
     '    "README.md",\n    "INDEX.md",',
     '    "INDEX.md",'),
    code(HYGIENE, HYGIENE_TEST, "match process-record words case-insensitively",
     '        tokens = set(re.split(r"[-_. ]+", path.name.rsplit(".", 1)[0]))',
     '        tokens = set(re.split(r"[-_. ]+", path.name.rsplit(".", 1)[0].upper()))'),
    code(HYGIENE, HYGIENE_TEST, "stop scanning every file for backup suffixes",
     '    for path in root.rglob("*"):',
     '    for path in root.rglob("*.md"):'),
    code(HYGIENE, HYGIENE_TEST, "stop excluding .cortex from the scan",
     'EXCLUDED_DIRS = (".git", "node_modules", ".cortex", "tests/fixtures", ".github")',
     'EXCLUDED_DIRS = (".git", "node_modules", "tests/fixtures", ".github")'),
    code(HYGIENE, HYGIENE_TEST, "stop skipping fenced blocks when collecting links",
     "        if in_fence:\n            continue\n",
     "", "def outbound_links"),
    code(HYGIENE, HYGIENE_TEST, "stop skipping fenced blocks when reading a body",
     "        if in_fence:\n            continue\n",
     "", "def temporary_markers"),
    code(HYGIENE, HYGIENE_TEST, "stop following links at all",
     "            if target in files and target not in reached:",
     "            if False:"),
    code(HYGIENE, HYGIENE_TEST, "stop excluding quoted spans",
     '        bare = QUOTED_SPAN.sub("", line)',
     "        bare = line"),
    code(HYGIENE, HYGIENE_TEST, "stop skipping anti-pattern headings",
     'if under_quoting_heading or "❌" in line:',
     'if "❌" in line:'),
    code(HYGIENE, HYGIENE_TEST, "treat any dated name as labelled, ignoring the directory",
     "    return named and any(posix.startswith(d) for d in DEDICATED_DIRS)",
     "    return named"),
    code(HYGIENE, HYGIENE_TEST, "treat any dedicated directory as labelled, ignoring the name",
     "    return named and any(posix.startswith(d) for d in DEDICATED_DIRS)",
     "    return any(posix.startswith(d) for d in DEDICATED_DIRS)"),
    code(HYGIENE, HYGIENE_TEST, "drop the ADR genre exemption",
     "if posix in BODY_EXEMPT_FILES or any(posix.startswith(d) for d in BODY_EXEMPT_DIRS):",
     "if posix in BODY_EXEMPT_FILES:"),
    code(HYGIENE, HYGIENE_TEST, "stop requiring the document to be unlabelled",
     "        if is_labelled_temporary(relative):\n            continue\n",
     ""),
    code(SCENARIOS, SCENARIOS, "drop the protected-public-contract exclusion",
     '        if symbol.get("protected_public_contract"):\n            continue\n',
     ""),
    code(SCENARIOS, SCENARIOS, "drop the live-consumer exclusion",
     '        if symbol.get("live_consumer_evidence"):\n            continue\n',
     ""),
    code(SCENARIOS, SCENARIOS, "stop failing a symbol neither removed nor shown live",
     '        if not symbol.get("removed"):\n            failed.add("ARC-010")\n        elif',
     '        if False:\n            failed.add("ARC-010")\n        elif'),
    code(SCENARIOS, SCENARIOS, "accept a removal made on the analyzer's word alone",
     '        elif not symbol.get("statically_resolvable", True) and not symbol.get(\n            "runtime_signal_full_cycle"\n        ):\n            failed.add("ARC-010")\n',
     ""),
    code(SCENARIOS, SCENARIOS, "drop the external-dependency exclusion",
     '        if marker.get("external_dependency"):\n            continue\n',
     ""),
    code(SCENARIOS, SCENARIOS, "stop requiring owner, removal point and replacement",
     '        if not all(marker.get(field) for field in ("owner", "removal_point", "replacement")):\n            failed.add("ARC-011")\n        elif',
     '        if False:\n            failed.add("ARC-011")\n        elif'),
    code(SCENARIOS, SCENARIOS, "accept a removal point that passed with no action",
     '        elif marker.get("removal_point_passed") and not (\n            marker.get("removed") or marker.get("renewed")\n        ):\n            failed.add("ARC-011")\n',
     ""),
    code(COUNTS, COUNTS_TEST, "count skill documents instead of skill directories",
         '        return len([p for p in path.iterdir() if p.is_dir()])',
         '        return len(list(path.rglob("*.md")))'),
    code(COUNTS, COUNTS_TEST, "count a layer's index as one of its documents",
         '    return len([p for p in path.glob("*.md") if p.name != "INDEX.md"])',
         '    return len(list(path.glob("*.md")))'),
    code(COUNTS, COUNTS_TEST, "pass a layer the README stopped declaring",
         '            problems.append(f"README declares no {layer} count; {directory}/ holds {actual}")\n            continue',
         '            continue'),
    code(COUNTS, COUNTS_TEST, "stop comparing the declared count with the disk",
         "        if declared[layer] != actual:", "        if False:"),
    code(COUNTS, COUNTS_TEST, "stop summing the capability table",
         '    elif "skill" in declared and sum(rows) != declared["skill"]:', "    elif False:"),
    code(COUNTS, COUNTS_TEST, "read the table without the multiline flag",
         'TABLE_ROW = re.compile(r"^\\| \\*\\*[^|]+\\*\\* \\| +(\\d+) \\|", re.MULTILINE)',
         'TABLE_ROW = re.compile(r"^\\| \\*\\*[^|]+\\*\\* \\| +(\\d+) \\|")'),

    code(CORTEX, CORTEX_TEST, "read prose as well as code",
         "        for number, line in code_lines(path.read_text(encoding=\"utf-8\")):",
         "        for number, line in enumerate(path.read_text(encoding=\"utf-8\").split(chr(10)), 1):"),
    code(CORTEX, CORTEX_TEST, "stop reporting a command the script does not have",
         "            if command not in commands:", "            if False:"),
    code(CORTEX, CORTEX_TEST, "stop reporting an unknown flag",
         "                if flag not in flags:", "                if False:"),
    code(CORTEX, CORTEX_TEST, "stop reporting a command no document mentions",
         '    for command in sorted(commands - set(mentions)):\n        problems.append(f"{SCRIPT} offers `{command}`, which none of {\', \'.join(DOCS)} mentions")\n',
         ""),
    # The asset-version check. Each mutation removes one thing it decides; the
    # decision is small enough that a silent regression would look exactly like
    # a range with nothing wrong in it.
    code(VERSIONS, VERSIONS_TEST, "stop reporting an edited asset whose version did not move",
         "        if after == before:", "        if False:"),
    code(VERSIONS, VERSIONS_TEST, "stop reporting an edited asset that lost its version",
         '        if after is None:\n            findings.append(f"{path}: was edited and no longer declares a version")',
         '        if False:\n            findings.append(f"{path}: was edited and no longer declares a version")'),
    code(VERSIONS, VERSIONS_TEST, "stop reporting a new asset that declares no version",
         "            if after is None:", "            if False:",
         inside='        if status == "added":'),
    code(VERSIONS, VERSIONS_TEST, "stop reporting a version that went backwards",
         "        if old and new and new < old:", "        if False:"),
    code(VERSIONS, VERSIONS_TEST, "count a Skill README as the versioned file",
         '        return len(parts) == 3 and parts[2] == "SKILL.md"', "        return True"),
    code(VERSIONS, VERSIONS_TEST, "count a registry index as a versioned asset",
         '    if parts[-1] == "INDEX.md":\n        return False\n', ""),

    code(RULES, RULES_TEST, "stop requiring a Rule to be registered in the index",
         '    if f"(./{path.name})" not in index_text:', "    if False:"),
    code(RULES, RULES_TEST, "stop checking the order of the required sections",
         "        if [positions[name] for name in required_order] != sorted(",
         "        if False and [positions[name] for name in required_order] != sorted("),
    code(RULES, RULES_TEST, "stop reporting an identifier repeated inside one document",
         "        if rule_id in seen_ids:", "        if False:"),
    code(RULES, RULES_TEST, "stop reporting an identifier owned by two documents",
         "            if rule_id in owners:", "            if False:"),
    code(RULES, RULES_TEST, "accept a Requirement with no MUST or MUST NOT",
         '        if "**MUST**" not in requirement and "**MUST NOT**" not in requirement:',
         "        if False:"),
    code(RULES, RULES_TEST, "accept any Default severity",
         '        if severity not in {"critical", "major", "minor", "suggestion"}:',
         "        if False:"),
    code(RULES, RULES_TEST, "stop reporting a required item field left empty",
         "        empty_fields = sorted(name for name in REQUIRED_ITEM_FIELDS if not fields.get(name))",
         "        empty_fields = []"),
    code(RULES, RULES_TEST, "stop noticing items under frontmatter that did not parse",
         "    if ITEM_HEADING.search(text):", "    if False:"),

    code(CORTEX, CORTEX_TEST, "read the dispatch without the dotall flag",
         'DISPATCH = re.compile(r"^case \\"\\$_cmd\\" in$(.*?)^esac$", re.MULTILINE | re.DOTALL)',
         'DISPATCH = re.compile(r"^case \\"\\$_cmd\\" in$(.*?)^esac$", re.MULTILINE)'),

    # Structural edits the translation verifier must block. The anchors quote
    # rules/task-quality.md, so an edit to that document lands here as a stale
    # perturbation rather than a silent loss of coverage.
    document("alter a number",
             replace("[rule-modeling](../specs/rule-modeling.md) \u00a75.4",
                     "[rule-modeling](../specs/rule-modeling.md) \u00a79.4")),
    document("alter a version", replace("version: 2.0.0", "version: 9.9.9")),
    document("weaken modality",
             replace("Every task row **MUST** carry an id",
                     "Every task row should carry an id")),
    document("misspell a frontmatter key", replace("rule_prefix: TASK", "rule_prefixx: TASK")),
    document("drop an identifier",
             replace("### TASK-019 — Task identifiers match the format and are unique",
                     "### Task identifiers match the format and are unique")),
    document("delete a whole section",
             replace(
                 "## Waivers\n\nA waiver may defer a traceability or coverage obligation when the upstream "
                 "artifact records the deferral. It **MUST NOT** be used to hand off a list whose dependency "
                 "graph does not resolve, nor to suppress an engineering-governance annotation whose trigger "
                 "is met \u2014 that trigger exists precisely because the work carries risk.\n\n",
                 "",
             )),
    document("drop a list item",
             replace("- [Findings List Schema](../specs/findings-list.md)\n", "")),
    document("alter a severity literal",
             replace("Presentation and bookkeeping defects are `minor`",
                     "Presentation and bookkeeping defects are `major`")),
    document("drop a prose frontmatter key",
             lambda text: re.sub(r"^scope: .*\n", "", text, count=1, flags=re.M)),
    document("repoint a link at another file",
             replace("(../specs/task-modeling.md)", "(../specs/spec-modeling.md)")),
    document("remove a link altogether",
             replace("[Findings List Schema](../specs/findings-list.md)", "Findings List Schema")),
    document("nothing translated at all", lambda text: text, allow_unchanged=True),

    # Controls, run the other way: a verifier that blocks these is refusing
    # every edit rather than catching a defect.
    document("CONTROL: reword prose only",
             replace("They raise the cost of using the list rather than sending the work wrong.",
                     "They raise the cost of working with the list rather than sending the work wrong."),
             expect="allowed"),
    document("CONTROL: reword a second prose sentence",
             replace("that trigger exists precisely because the work carries risk",
                     "that trigger exists exactly because the work carries risk"),
             expect="allowed"),

    # Not a mutation of a file but of the invocation. An unresolvable ref used
    # to make every `git show` fail, every file read as new, and the run report
    # no violations having compared nothing.
    Perturbation("an unresolvable git ref", (VERIFIER, "NOSUCHREF", TRANSLATED)),
]


def main() -> int:
    failures: list[str] = []
    counted: dict[str, int] = {}

    for case in PERTURBATIONS:
        original = None
        path = ROOT / case.target if case.target else None
        if path is not None and case.edit is not None:
            original = path.read_text(encoding="utf-8")
            mutated = case.edit(original)
            if mutated == original and not case.allow_unchanged:
                failures.append(f'the perturbation "{case.label}" no longer matches {case.target}')
                continue
            path.write_text(mutated, encoding="utf-8")
        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / case.command[0]), *case.command[1:]],
                capture_output=True,
                text=True,
                cwd=ROOT,
            )
        finally:
            if original is not None:
                path.write_text(original, encoding="utf-8")

        blocked = result.returncode != 0
        if blocked != (case.expect == "blocked"):
            failures.append(
                f'the perturbation "{case.label}" was {"blocked" if blocked else "allowed"}, '
                f"expected {case.expect}"
            )
        key = case.target or "the invocation"
        counted[key] = counted.get(key, 0) + 1

    if failures:
        print("Mutation check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    summary = ", ".join(f"{pathlib.Path(k).name}: {n}" for k, n in sorted(counted.items()))
    print(f"Every perturbation produced the expected verdict ({summary}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

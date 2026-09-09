#!/usr/bin/env bash
# Validate scripts/verify-translation.py by injecting known errors.
#
# Mutates an already-translated file against its own HEAD state, so the
# residual-Chinese check does not fire and each mutation is isolated. A checker
# that reports nothing on a clean sample has proved nothing; this is what gives
# the zero-findings result a denominator.
set -euo pipefail

TARGET="rules/task-quality.md"
python3 - "$TARGET" <<'PY'
import pathlib, subprocess, sys, re
F = sys.argv[1]
orig = pathlib.Path(F).read_text()

cases = [
    ("drop a self-check constraint",
     lambda t: t.replace("- [ ] The dependency graph is acyclic (DAG)\n", "", 1), True),
    ("alter a threshold",
     lambda t: t.replace("6 required fields", "8 required fields", 1), True),
    ("weaken modality",
     lambda t: t.replace("never a blank", "preferably not a blank", 1), True),
    ("misspell a cross-reference",
     lambda t: t.replace("`depends_on`", "`depends_upon`", 1), True),
    ("drop an identifier",
     lambda t: t.replace("`artifact_type: tasks`", "artifact type tasks", 1), True),
    ("delete a whole section",
     lambda t: t.replace("### 4. Traceability\n", "", 1), True),
    ("drop a list item",
     lambda t: t.replace("- [ ] Task titles contain a verb; avoid the vague \"implement X\"\n", "", 1), True),
    ("alter frontmatter",
     lambda t: t.replace("version: 1.0.0", "version: 9.9.9", 1), True),
    ("drop a prose frontmatter key",
     lambda t: re.sub(r'^scope: .*\n', "", t, count=1, flags=re.M), True),
    ("repoint a link at another file",
     lambda t: t.replace("(../specs/task-modeling.md)", "(../specs/spec-modeling.md)", 1), True),
    ("remove a link altogether",
     lambda t: t.replace("[specs/task-modeling.md](../specs/task-modeling.md)",
                         "specs/task-modeling.md", 1), True),
    ("nothing translated at all",
     lambda t: t, True),
    ("CONTROL: reword prose only",
     lambda t: t.replace("Every task carries the 6 required fields",
                         "Each task carries the 6 required fields", 1), False),
    ("CONTROL: add a modal without other change",
     lambda t: t.replace("Task titles contain a verb",
                         "Task titles must contain a verb", 1), False),
]

ok = 0
for name, mutate, should_block in cases:
    new = mutate(orig)
    if new == orig and not name.startswith("nothing"):
        print(f"  SKIP  {name}: mutation did not apply")
        continue
    pathlib.Path(F).write_text(new)
    r = subprocess.run(["python3", "scripts/verify-translation.py", "HEAD", F],
                       capture_output=True, text=True)
    blocked = r.returncode != 0
    correct = blocked == should_block
    ok += correct
    mark = "PASS" if correct else "FAIL"
    want = "block" if should_block else "allow"
    got = "blocked" if blocked else "allowed"
    print(f"  {mark}  {name}: want {want}, got {got}")
    pathlib.Path(F).write_text(orig)

print(f"\n  {ok}/{len(cases)} correct")
sys.exit(0 if ok == len(cases) else 1)
PY

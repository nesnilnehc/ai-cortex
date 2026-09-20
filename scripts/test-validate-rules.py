#!/usr/bin/env python3
"""Check that validate-rules.py reports each defect it claims to decide.

validate-rules.py blocks a merge, and until this file existed nothing asked
whether it could still fail. A checker that has stopped looking prints the same
clean verdict as one that is working.

Each case perturbs a copy of the clean fixture and requires a matching finding.
An anchor that no longer matches fails its case rather than passing quietly: an
edit that changes nothing tests nothing, which is the failure mode this whole
file exists to prevent.
"""

from __future__ import annotations

import importlib.util
import pathlib
import shutil
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
CLEAN = ROOT / "tests" / "fixtures" / "rule-validation" / "clean"

DEMO = "demo-quality.md"
OTHER = "other-quality.md"
INDEX = "INDEX.md"

EXPECTED_CLEAN = (2, 3)


def load_checker():
    spec = importlib.util.spec_from_file_location(
        "validate_rules", ROOT / "scripts" / "validate-rules.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def replace(before: str, after: str):
    def edit(text: str) -> str:
        if before not in text:
            return text
        return text.replace(before, after, 1)

    return edit


def swap_gate_and_waivers(text: str) -> str:
    gate = "## Severity and gate policy\n\nFixture policy: nothing gates.\n\n"
    waivers = "## Waivers\n\nFixture waivers: none.\n\n"
    return text.replace(gate + waivers, waivers + gate, 1)


# label, fixture file, edit, the fragment the finding must contain
CASES = [
    # frontmatter
    ("a required frontmatter field is missing", DEMO,
     replace("scope: a fixture standing in for a modeled Rule set\n", ""),
     "missing frontmatter: scope"),
    ("artifact_type is not rule", DEMO,
     replace("artifact_type: rule", "artifact_type: spec"), "artifact_type must be rule"),
    ("name does not match the filename", DEMO,
     replace("name: demo-quality", "name: demo-qualities"), "name must match the filename"),
    ("version is not SemVer", DEMO,
     replace("version: 1.0.0", "version: 1.0"), "version must be SemVer"),
    ("recommended_scope is outside the enum", DEMO,
     replace("recommended_scope: project", "recommended_scope: team"),
     "recommended_scope must be user, project or both"),
    ("status is outside the enum", DEMO,
     replace("status: active", "status: live"),
     "status must be draft, active, superseded or archived"),
    ("status is superseded with no superseded_by", DEMO,
     replace("status: active", "status: superseded"),
     "superseded_by is required when status is superseded"),
    ("created_by is not ai-cortex", DEMO,
     replace("created_by: ai-cortex", "created_by: someone"), "created_by must be ai-cortex"),
    ("lifecycle is not living", DEMO,
     replace("lifecycle: living", "lifecycle: snapshot"), "lifecycle must be living"),
    ("created_at is not an ISO date", DEMO,
     replace("created_at: 2026-01-01", "created_at: 2026/01/01"),
     "created_at must be an ISO date"),
    ("rule_prefix is not 3-8 uppercase letters", DEMO,
     replace("rule_prefix: DEMO", "rule_prefix: Demo"),
     "rule_prefix must be 3-8 uppercase letters"),
    ("the document is not registered in the index", INDEX,
     replace("| [demo-quality](./demo-quality.md) |", "| demo-quality |"),
     "file is not registered in rules/INDEX.md"),

    # sections
    ("a required section is missing", DEMO,
     replace("\n## Waivers\n", "\n## Deferrals\n"), "missing sections: Waivers"),
    ("required sections are out of order", DEMO, swap_gate_and_waivers,
     "required sections are not in the modeled order"),

    # items
    ("the document carries no items", DEMO,
     lambda text: text.replace("### DEMO-", "#### DEMO-"), "no modeled Rule items found"),
    ("an identifier is duplicated inside one document", DEMO,
     replace("### DEMO-002 —", "### DEMO-001 —"), "duplicate identifier in the same document"),
    ("an identifier does not use the declared prefix", DEMO,
     replace("### DEMO-002 —", "### XTRA-002 —"), "does not use rule_prefix DEMO"),
    ("an item carries two Field tables", DEMO,
     replace("| Level | `baseline` |", "| Field | Value |\n| Level | `baseline` |"),
     "needs exactly one Field table"),
    ("an item is missing a required field", DEMO,
     replace("| Evidence | The fixture itself. |\n", ""), "missing fields: Evidence"),
    ("an item has a required field left empty", DEMO,
     replace("| Evidence | The fixture itself. |", "| Evidence |  |"), "empty fields: Evidence"),
    ("an item declares an invalid Level", DEMO,
     replace("| Level | `baseline` |", "| Level | `global` |"), "invalid Level"),
    ("a Requirement carries no MUST or MUST NOT", DEMO,
     replace("A scope **MUST** carry", "A scope should carry"),
     "Requirement needs one explicit MUST or MUST NOT"),
    ("an item declares an invalid Default severity", DEMO,
     replace("| Default severity | `major` |", "| Default severity | `huge` |"),
     "invalid Default severity"),
    ("an item declares an invalid Enforcement", DEMO,
     replace("| Enforcement | `automated` |", "| Enforcement | `manual` |"),
     "invalid Enforcement"),

    # falling out of the modeled set entirely
    ("a model value that is not RULE_MODEL_V1", DEMO,
     replace("model: RULE_MODEL_V1", "model: RULE_MODEL_v1"),
     "a modeled Rule declares RULE_MODEL_V1 exactly"),
    ("frontmatter that does not parse, under items that do", DEMO,
     lambda text: "\n" + text, "no RULE_MODEL_V1 frontmatter was read"),

    # across documents
    ("an identifier is duplicated across two documents", OTHER,
     replace("### OTHR-001 —", "### DEMO-001 —"), "duplicate Rule ID DEMO-001"),
    # activation materials and derived maturity
    ("a Maturity field written by hand rather than derived", DEMO,
     replace("| Enforcement | `automated` |\n",
             "| Enforcement | `automated` |\n| Maturity | `ready` |\n"),
     "Maturity is derived"),
    ("an activation field is present but empty", DEMO,
     replace("| Remediation | Renumber the duplicate. |\n",
             "| Remediation | Renumber the duplicate. |\n| Worked pass | |\n"),
     "empty activation fields"),
    ("an activation field sits on the wrong enforcement class", DEMO,
     replace("| Remediation | Restore the field the test removed. |\n",
             "| Remediation | Restore the field the test removed. |\n| Worked pass | A passing shape. |\n"),
     "does not take"),
]


def findings(check, directory: pathlib.Path) -> list[str]:
    result = check(directory, (directory / INDEX).read_text(encoding="utf-8"), root=directory)
    return list(result.excluded) + list(result.errors)


def main() -> int:
    module = load_checker()
    errors: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        base = pathlib.Path(tmp) / "clean"
        shutil.copytree(CLEAN, base)
        result = module.check(base, (base / INDEX).read_text(encoding="utf-8"), root=base)
        if result.excluded or result.errors:
            errors.append(f"the clean fixture is not clean: {result.excluded + result.errors}")
        if (result.documents, result.items) != EXPECTED_CLEAN:
            errors.append(
                f"the clean fixture counted {(result.documents, result.items)}, "
                f"expected {EXPECTED_CLEAN}"
            )

    for label, filename, edit, fragment in CASES:
        with tempfile.TemporaryDirectory() as tmp:
            base = pathlib.Path(tmp) / "clean"
            shutil.copytree(CLEAN, base)
            target = base / filename
            original = target.read_text(encoding="utf-8")
            mutated = edit(original)
            if mutated == original:
                errors.append(f'"{label}": the edit no longer matches {filename}')
                continue
            target.write_text(mutated, encoding="utf-8")
            found = findings(module.check, base)
            if not any(fragment in line for line in found):
                errors.append(
                    f'"{label}": expected a finding containing {fragment!r}, got {found}'
                )

    if errors:
        print("validate-rules checker test failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        f"Validated the Rule validator over {len(CASES)} defect shapes "
        "and one clean fixture; every shape produced its finding."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Forward-test Rule items whose decision is mechanical, on representative shapes.

Every automated blocking item is here because constraint 8 of
rules/workflow-rule-governance.md requires it. ARC-010 and ARC-011 are
neither automated nor blocking, so they owe nothing, but the half of each
that is mechanical — deciding an obligation once the evidence is in hand —
is pinned here anyway, because that is where their sharp edge lives. What
no fixture can test is the other half: gathering the evidence, and judging
whether a recorded owner still owns anything.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys


ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures"


def has_cycle(edges: list[list[str]]) -> bool:
    graph: dict[str, set[str]] = {}
    for source, target in edges:
        graph.setdefault(source, set()).add(target)
        graph.setdefault(target, set())
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(target) for target in graph.get(node, set())):
            return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph)


def evaluate_code(case: dict[str, object]) -> set[str]:
    failed: set[str] = set()
    allowed = case.get("allowed_dependencies", {})
    edges = case.get("actual_edges", [])
    if allowed:
        for source, target in edges:
            if target not in allowed.get(source, []):
                failed.add("ARC-002")
    if has_cycle(edges):
        failed.add("ARC-003")

    profiles = set(case.get("profiles", []))
    protected = set(case.get("protected_contracts", []))
    breaking = set(case.get("breaking_contracts", []))
    migrated = set(case.get("versioned_migrations", []))
    if "public-api" in profiles and (protected & breaking) - migrated:
        failed.add("ARC-005")

    budget = case.get("change_budget")
    metrics = case.get("change_metrics", {})
    if budget and any(metrics.get(key, 0) > value for key, value in budget.items()):
        failed.add("ARC-009")

    # SEC-003 is baseline, so it is evaluated for every shape. A candidate that cannot
    # authenticate is excluded by the item's own "not applicable when", which is what keeps
    # documentation placeholders from becoming false positives.
    for candidate in case.get("secret_candidates", []):
        if not candidate.get("live"):
            continue
        if candidate.get("source") == "hardcoded":
            failed.add("SEC-003")
        elif not candidate.get("redacted_in_telemetry", True):
            failed.add("SEC-003")

    # ARC-010. Silence from an analyzer is not evidence about a symbol the
    # analyzer cannot resolve, so a reflection- or configuration-reached symbol
    # may be neither kept on its word nor deleted on its word.
    for symbol in case.get("unreached_symbols", []):
        if symbol.get("protected_public_contract"):
            continue
        if symbol.get("live_consumer_evidence"):
            continue
        if not symbol.get("removed"):
            failed.add("ARC-010")
        elif not symbol.get("statically_resolvable", True) and not symbol.get(
            "runtime_signal_full_cycle"
        ):
            failed.add("ARC-010")

    # ARC-011. A marker owes an owner, a removal point and a replacement, and a
    # removal point already past owes an action or a renewal.
    for marker in case.get("deprecations", []):
        if marker.get("external_dependency"):
            continue
        if not all(marker.get(field) for field in ("owner", "removal_point", "replacement")):
            failed.add("ARC-011")
        elif marker.get("removal_point_passed") and not (
            marker.get("removed") or marker.get("renewed")
        ):
            failed.add("ARC-011")

    if "public-contract" in profiles:
        for contract in case.get("changed_public_contracts", []):
            if not contract.get("has_released_consumer"):
                continue
            if not contract.get("compatibility_tests") and not contract.get(
                "versioned_migration_tested"
            ):
                failed.add("TST-004")
    return failed


def evaluate_task_list(case: dict[str, object]) -> set[str]:
    """Decide the automated blocking items of task-quality over one task-list shape."""
    failed: set[str] = set()
    profiles = set(case.get("profiles", []))
    tasks = case.get("tasks", [])
    known_ids = {task["id"] for task in tasks}

    if any(not task.get("required_fields_present", True) for task in tasks):
        failed.add("TASK-001")
    if "handoff" in profiles and any(task.get("status") != "Todo" for task in tasks):
        failed.add("TASK-002")

    edges = [[task["id"], dep] for task in tasks for dep in task.get("depends_on", [])]
    if has_cycle(edges):
        failed.add("TASK-004")
    if any(dep not in known_ids for task in tasks for dep in task.get("depends_on", [])):
        failed.add("TASK-005")

    parent = case.get("parent", {})
    if not parent.get("declared") or not parent.get("resolves"):
        failed.add("TASK-011")

    # Annotation items are profile-gated: an unresolvable citation on a list that
    # triggers no governance condition is not a finding.
    if "engineering-governance" in profiles:
        known_rules = set(case.get("known_rule_ids", []))
        valid_waivers = set(case.get("valid_waiver_ids", []))
        for annotation in case.get("annotations", []):
            if any(ref not in known_rules for ref in annotation.get("rule_refs", [])):
                failed.add("TASK-016")
            waiver = annotation.get("waiver")
            if waiver and waiver not in valid_waivers:
                failed.add("TASK-018")

    frontmatter = case.get("frontmatter", {})
    if not frontmatter.get("required_present") or not frontmatter.get("enums_valid"):
        failed.add("TASK-003")

    # An undeclared dependency cell is not the same as "no dependencies": the
    # first is silence, the second is a decision, and only the second is a pass.
    if any(not task.get("depends_on_declared", True) for task in tasks):
        failed.add("TASK-006")

    if any(not (task.get("owner") or task.get("execution_hint")) for task in tasks):
        failed.add("TASK-008")

    id_format = re.compile(case.get("id_format", r"^T\d+$"))
    ids = [task["id"] for task in tasks]
    if any(not id_format.fullmatch(i) for i in ids) or len(ids) != len(set(ids)):
        failed.add("TASK-019")
    return failed


def evaluate_technical_design(case: dict[str, object]) -> set[str]:
    """Decide the automated blocking items of technical-design-quality over one design shape."""
    failed: set[str] = set()
    profiles = set(case.get("profiles", []))

    if set(case.get("required_sections", [])) - set(case.get("sections_present", [])):
        failed.add("TDES-001")
    if case.get("candidate_approaches", 0) < 2:
        failed.add("TDES-003")

    if "quality-attribute" in profiles:
        known_rules = set(case.get("known_rule_ids", []))
        if any(ref not in known_rules for ref in case.get("cited_rule_ids", [])):
            failed.add("TDES-009")

    parent = case.get("parent", {})
    if (
        not parent.get("resolves")
        or parent.get("artifact_type") not in {"functional-design", "requirement", "adr"}
        or parent.get("status") not in {"approved", "accepted"}
    ):
        failed.add("TDES-022")

    frontmatter = case.get("frontmatter", {})
    if not frontmatter.get("required_present") or not frontmatter.get("enums_valid"):
        failed.add("TDES-002")

    # A required section that is present but says nothing is the shape this item
    # exists for: TDES-001 already decides absence, and "no change" is a pass.
    if case.get("empty_sections"):
        failed.add("TDES-006")

    if case.get("structured_representations", 0) < 1 or not case.get("structured_referenced"):
        failed.add("TDES-016")

    if not case.get("dependencies_stated") or not case.get("risks_stated"):
        failed.add("TDES-021")

    if case.get("acceptance_criteria", 0) < 3:
        failed.add("TDES-024")

    resolvable = set(case.get("resolvable_citations", []))
    if any(citation not in resolvable for citation in case.get("citations", [])):
        failed.add("TDES-025")
    return failed


# Each Rule set is forward-tested over three representative shapes of the population
# it governs, per rules/workflow-rule-governance.md constraint 8.
POPULATIONS = (
    ("rule-governance", "engineering concerns", evaluate_code),
    ("task-list", "task-quality", evaluate_task_list),
    ("technical-design", "technical-design-quality", evaluate_technical_design),
)


def load_case(path: pathlib.Path) -> dict | str:
    """Read one fixture, or return the reason it could not be read.

    The reason names the file. A bare json.loads raises a JSONDecodeError
    carrying a line and column and no path, which is unusable when three
    directories of fixtures could be the one at fault.
    """
    try:
        case = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        return f"{path.relative_to(ROOT)}: cannot be read — {exc.strerror}"
    except json.JSONDecodeError as exc:
        return f"{path.relative_to(ROOT)}: not valid JSON — {exc.msg} at line {exc.lineno} column {exc.colno}"
    if not isinstance(case, dict):
        return f"{path.relative_to(ROOT)}: must hold a JSON object, found {type(case).__name__}"
    if "expected_failed_rules" not in case:
        return f"{path.relative_to(ROOT)}: missing \"expected_failed_rules\", which says what this shape must report"
    return case


def main() -> int:
    errors: list[str] = []
    total = 0
    for directory, label, evaluator in POPULATIONS:
        cases = sorted((FIXTURES / directory).glob("*.json"))
        if len(cases) < 3:
            errors.append(
                f"{label}: needs at least 3 representative shapes, found {len(cases)}"
            )
        for path in cases:
            total += 1
            case = load_case(path)
            if isinstance(case, str):
                errors.append(case)
                continue
            actual = evaluator(case)
            expected = set(case["expected_failed_rules"])
            if actual != expected:
                errors.append(
                    f"{directory}/{path.name}: expected {sorted(expected)}, got {sorted(actual)}"
                )
    if errors:
        print("Rule scenario tests failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Validated automated Rule applicability on {total} representative shapes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

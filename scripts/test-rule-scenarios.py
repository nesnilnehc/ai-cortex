#!/usr/bin/env python3
"""Forward-test the automated blocking Rule items on representative project shapes."""

from __future__ import annotations

import json
import pathlib
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
    return failed


# Each Rule set is forward-tested over three representative shapes of the population
# it governs, per rules/workflow-rule-governance.md constraint 8.
POPULATIONS = (
    ("rule-governance", "engineering concerns", evaluate_code),
    ("task-list", "task-quality", evaluate_task_list),
    ("technical-design", "technical-design-quality", evaluate_technical_design),
)


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
            case = json.loads(path.read_text(encoding="utf-8"))
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

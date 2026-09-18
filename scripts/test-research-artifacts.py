#!/usr/bin/env python3
"""Fixed contract cases for research evidence and opportunity decisions."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "research"
spec = importlib.util.spec_from_file_location("research_validator", Path(__file__).with_name("validate-research-artifacts.py"))
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def load(name: str) -> dict:
    """Read one fixture, failing with the name of the file that is wrong.

    A bare json.loads reports a line and column and no path, which does not
    identify the fixture among the directory's files.
    """
    path = FIXTURES / name
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise SystemExit(f"fatal: {path.relative_to(ROOT)} cannot be read — {exc.strerror}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(
            f"fatal: {path.relative_to(ROOT)} is not valid JSON — "
            f"{exc.msg} at line {exc.lineno} column {exc.colno}"
        ) from exc
    if not isinstance(data, dict):
        raise SystemExit(
            f"fatal: {path.relative_to(ROOT)} must hold a JSON object, found {type(data).__name__}"
        )
    return data


def expect_error(data: dict, fragment: str, package: bool = False) -> None:
    errors = validator.package_errors(data) if package else validator.report_errors(data)
    if not any(fragment in error for error in errors):
        raise AssertionError(f"Expected {fragment!r}; got {errors}")


def main() -> int:
    for path in sorted(FIXTURES.glob("*.json")):
        data = load(path.name)
        errors = validator.package_errors(data) if "package_id" in data else validator.report_errors(data)
        if errors:
            raise AssertionError(f"{path.name}: {errors}")

    report = load("foundation-report.json")
    broken = copy.deepcopy(report)
    broken["findings"][0]["evidence"][0]["source_id"] = "missing"
    expect_error(broken, "source_id: unresolved")
    broken = copy.deepcopy(report)
    broken["findings"][0]["classification"] = "Inference"
    broken["findings"][0]["derived_from"] = ["F1"]
    expect_error(broken, "derivation cycle")
    broken = copy.deepcopy(report)
    broken["findings"][1]["gaps"] = []
    expect_error(broken, "Unknown needs a non-empty gap")
    broken = copy.deepcopy(report)
    broken["sources"] = []
    expect_error(broken, "source_id: unresolved")

    package = load("complete-package.json")
    broken = copy.deepcopy(package)
    broken["recommendation"]["claim_ids"] = ["not-a-claim"]
    expect_error(broken, "unresolved", package=True)
    broken = copy.deepcopy(package)
    broken["recommendation"]["decision"] = "pursue"
    broken["recommendation"]["claim_ids"] = ["C2"]
    expect_error(broken, "pursue needs source-backed user signals", package=True)
    broken = copy.deepcopy(package)
    broken["recommendation"]["decision"] = "pursue"
    broken["claims"][0]["role"] = "opposes"
    expect_error(broken, "pursue needs source-backed user signals", package=True)
    broken = copy.deepcopy(package)
    broken["recommendation"]["decision"] = "pursue"
    broken["analysis"]["opposing_evidence"] = []
    expect_error(broken, "pursue must acknowledge opposing evidence", package=True)
    broken = copy.deepcopy(package)
    broken["lanes"]["market"]["report_ids"] = ["missing"]
    expect_error(broken, "unresolved", package=True)
    broken = load("deferred-package.json")
    broken["status"] = "ready_for_decision"
    expect_error(broken, "readiness needs a source-backed claim", package=True)
    broken = copy.deepcopy(report)
    broken["findings"][0]["classification"] = ["Fact"]
    expect_error(broken, "classification: invalid value")
    broken = copy.deepcopy(report)
    broken["schema_version"] = "2.0"
    expect_error(broken, "expected compatible 1.x")
    broken = copy.deepcopy(report)
    inference = copy.deepcopy(broken["findings"][0])
    inference["finding_id"] = "F3"
    inference["classification"] = "Inference"
    inference["evidence"] = []
    inference["derived_from"] = ["F1", "F3"]
    broken["findings"].append(inference)
    expect_error(broken, "derivation cycle")
    broken_package = copy.deepcopy(package)
    broken_package["status"] = ["ready_for_decision"]
    expect_error(broken_package, "status: invalid", package=True)
    broken_package = copy.deepcopy(package)
    broken_package["analysis"]["size_or_impact"] = {
        "estimate": "100", "unit": "users", "method": "asserted", "assumptions": [], "claim_ids": []
    }
    expect_error(broken_package, "size_or_impact: needs source-backed inputs", package=True)
    broken_package = copy.deepcopy(package)
    broken_package["analysis"]["gaps"] = []
    broken_package["recommendation"]["validation_steps"] = []
    expect_error(broken_package, "Unknown needs a validation step", package=True)
    broken = copy.deepcopy(report)
    broken["findings"][0]["evidence"][0]["source_id"] = []
    expect_error(broken, "source_id: unresolved")
    broken_package = copy.deepcopy(package)
    broken_package["lanes"]["policy"]["status"] = []
    expect_error(broken_package, "status: invalid", package=True)
    broken = copy.deepcopy(report)
    broken["subquestions"][0]["question"] = ""
    expect_error(broken, "subquestions[Q1].question: required")
    broken = copy.deepcopy(report)
    broken["findings"][1]["gaps"] = [""]
    expect_error(broken, "Unknown needs a non-empty gap")
    broken = copy.deepcopy(report)
    broken["gaps"] = []
    expect_error(broken, "Unknown needs a recorded validation gap")
    broken_package = copy.deepcopy(package)
    broken_package["recommendation"]["claim_ids"] = "C1"
    expect_error(broken_package, "claim_ids: expected array", package=True)
    broken_package = copy.deepcopy(package)
    broken_package["problem"]["alternatives"] = "manual"
    expect_error(broken_package, "alternatives: expected array", package=True)
    broken_package = copy.deepcopy(package)
    del broken_package["package_id"]
    dispatched = validator.artifact_errors(broken_package)
    if not any("package.package_id: required" in error for error in dispatched):
        raise AssertionError(f"Package without ID routed incorrectly: {dispatched}")
    broken_package = copy.deepcopy(package)
    broken_package["context"]["geography"] = None
    broken_package["analysis"]["gaps"] = []
    expect_error(broken_package, "context.geography: missing scope needs a gap", package=True)
    broken_package = copy.deepcopy(package)
    market = broken_package["reports"][1]
    unknown = copy.deepcopy(market["findings"][0])
    unknown.update({"finding_id": "F2", "classification": "Unknown", "evidence": [],
                    "derived_from": [], "gaps": ["Current demand is unverified."]})
    inference = copy.deepcopy(unknown)
    inference.update({"finding_id": "F3", "classification": "Inference", "derived_from": ["F2"], "gaps": []})
    market["findings"].extend([unknown, inference])
    market["gaps"].append({"gap_id": "G1", "question": "What is current demand?",
                           "reason": "No current study was inspected.", "validation_step": "Find a current study."})
    broken_package["claims"].append({"claim_id": "C3", "statement": "Current demand is inferred.",
                                      "role": "context", "finding_refs": [{"report_id": market["report_id"], "finding_id": "F3"}],
                                      "unknown_reason": None})
    broken_package["recommendation"]["claim_ids"] = ["C1", "C3"]
    broken_package["analysis"]["gaps"] = []
    broken_package["recommendation"]["validation_steps"] = []
    expect_error(broken_package, "Unknown needs a validation step", package=True)
    compatible = copy.deepcopy(report)
    compatible["schema_version"] = "1.2"
    if validator.report_errors(compatible):
        raise AssertionError("Compatible minor version rejected")
    long_chain = copy.deepcopy(report)
    chain = []
    for index in range(1, 1100):
        finding = copy.deepcopy(report["findings"][0])
        finding["finding_id"] = f"D{index}"
        finding["classification"] = "Inference"
        finding["evidence"] = []
        finding["derived_from"] = ["F1" if index == 1 else f"D{index - 1}"]
        chain.append(finding)
    long_chain["findings"].extend(reversed(chain))
    if validator.report_errors(long_chain):
        raise AssertionError("Valid long derivation chain rejected")
    print(f"Validated {len(list(FIXTURES.glob('*.json')))} positive fixtures, 26 negative cases, a compatible minor version and a long trace.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

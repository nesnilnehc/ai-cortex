#!/usr/bin/env python3
"""Validate JSON Research Reports and Opportunity Packages without network access."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import re
import sys


CLASSES = {"Fact", "Claim", "Inference", "Unknown"}
CONFIDENCE = {"high", "medium", "low"}
LANE_STATUS = {"complete", "limited", "not_applicable", "missing"}
DECISIONS = {"pursue", "explore", "defer", "do_not_pursue"}
SUPPORTED_VERSION = re.compile(r"^1\.[0-9]+$")


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def one_of(value: object, choices: set[str]) -> bool:
    return isinstance(value, str) and value in choices


def date(value: object) -> bool:
    if not nonempty(value):
        return False
    try:
        dt.date.fromisoformat(value)
        return True
    except ValueError:
        return False


def obj(value: object) -> dict:
    return value if isinstance(value, dict) else {}


def items(value: object) -> list:
    return value if isinstance(value, list) else []


def required(data: dict, fields: tuple[str, ...], path: str, errors: list[str]) -> None:
    for field in fields:
        if field not in data:
            errors.append(f"{path}.{field}: required")


def unique_records(records: list, key: str, path: str, errors: list[str]) -> dict[str, dict]:
    index: dict[str, dict] = {}
    for n, item in enumerate(records):
        record = obj(item)
        identity = record.get(key)
        if not nonempty(identity):
            errors.append(f"{path}[{n}].{key}: required non-empty string")
        elif identity in index:
            errors.append(f"{path}[{n}].{key}: duplicate {identity}")
        else:
            index[identity] = record
    return index


def source_backed_claim(claim: dict, reports: dict[str, dict], allowed_reports: set[str] | None = None) -> bool:
    """Follow a claim through findings to an inspected supporting source."""
    def source_backed_finding(report_id: str, finding_id: str) -> bool:
        report = reports[report_id]
        findings = {
            obj(item).get("finding_id"): obj(item)
            for item in items(report.get("findings"))
            if nonempty(obj(item).get("finding_id"))
        }
        source_ids = {
            obj(source).get("source_id")
            for source in items(report.get("sources"))
            if nonempty(obj(source).get("source_id"))
        }
        stack = [finding_id]
        seen: set[str] = set()
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            finding = findings.get(current, {})
            kind = finding.get("classification")
            if one_of(kind, {"Fact", "Claim"}) and any(
                obj(link).get("relationship") == "supports"
                and nonempty(obj(link).get("source_id"))
                and obj(link).get("source_id") in source_ids
                for link in items(finding.get("evidence"))
            ):
                return True
            if kind == "Inference":
                stack.extend(
                    parent for parent in items(finding.get("derived_from"))
                    if nonempty(parent)
                )
        return False

    for ref in items(claim.get("finding_refs")):
        report_id = obj(ref).get("report_id")
        finding_id = obj(ref).get("finding_id")
        if (nonempty(report_id) and report_id in reports
                and (allowed_reports is None or report_id in allowed_reports)
                and nonempty(finding_id)
                and source_backed_finding(report_id, finding_id)):
            return True
    return False


def unknown_path_claim(claim: dict, reports: dict[str, dict]) -> bool:
    """Detect an Unknown at the end of a claim's direct or inferred finding path."""
    if nonempty(claim.get("unknown_reason")):
        return True
    for ref in items(claim.get("finding_refs")):
        report_id = obj(ref).get("report_id")
        finding_id = obj(ref).get("finding_id")
        if not nonempty(report_id) or report_id not in reports or not nonempty(finding_id):
            continue
        findings = {
            obj(item).get("finding_id"): obj(item)
            for item in items(reports[report_id].get("findings"))
            if nonempty(obj(item).get("finding_id"))
        }
        stack = [finding_id]
        seen: set[str] = set()
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            finding = findings.get(current, {})
            if finding.get("classification") == "Unknown":
                return True
            if finding.get("classification") == "Inference":
                stack.extend(
                    parent for parent in items(finding.get("derived_from"))
                    if nonempty(parent)
                )
    return False


def report_errors(data: object, path: str = "report") -> list[str]:
    errors: list[str] = []
    report = obj(data)
    required(report, ("schema_version", "report_id", "question", "scope", "subquestions",
                      "sources", "findings", "conflicts", "gaps", "summary"), path, errors)
    if not nonempty(report.get("schema_version")) or not SUPPORTED_VERSION.fullmatch(report["schema_version"]):
        errors.append(f"{path}.schema_version: expected compatible 1.x")
    for field in ("report_id", "question", "summary"):
        if not nonempty(report.get(field)):
            errors.append(f"{path}.{field}: required non-empty string")
    if not date(obj(report.get("scope")).get("as_of")):
        errors.append(f"{path}.scope.as_of: expected ISO date")
    for field in ("subquestions", "sources", "findings", "conflicts", "gaps"):
        if not isinstance(report.get(field), list):
            errors.append(f"{path}.{field}: expected array")
    subquestions = unique_records(items(report.get("subquestions")), "id", f"{path}.subquestions", errors)
    sources = unique_records(items(report.get("sources")), "source_id", f"{path}.sources", errors)
    findings = unique_records(items(report.get("findings")), "finding_id", f"{path}.findings", errors)
    unique_records(items(report.get("conflicts")), "conflict_id", f"{path}.conflicts", errors)
    unique_records(items(report.get("gaps")), "gap_id", f"{path}.gaps", errors)
    if not findings:
        errors.append(f"{path}.findings: at least one finding required")
    for qid, subquestion in subquestions.items():
        if not nonempty(subquestion.get("question")):
            errors.append(f"{path}.subquestions[{qid}].question: required")

    for sid, source in sources.items():
        at = f"{path}.sources[{sid}]"
        required(source, ("title", "publisher", "source_type", "uri", "published_at",
                          "effective_at", "accessed_at", "provenance_family", "limitations"), at, errors)
        for field in ("title", "publisher", "source_type", "uri", "provenance_family"):
            if not nonempty(source.get(field)):
                errors.append(f"{at}.{field}: required non-empty string")
        if not date(source.get("accessed_at")):
            errors.append(f"{at}.accessed_at: expected ISO date")
        for field in ("published_at", "effective_at"):
            if source.get(field) is not None and not date(source.get(field)):
                errors.append(f"{at}.{field}: expected ISO date or null")
        if not isinstance(source.get("limitations"), list):
            errors.append(f"{at}.limitations: expected array")
        elif not all(nonempty(limit) for limit in source["limitations"]):
            errors.append(f"{at}.limitations: expected non-empty strings")

    for fid, finding in findings.items():
        at = f"{path}.findings[{fid}]"
        required(finding, ("statement", "classification", "scope", "as_of", "confidence",
                           "confidence_rationale", "evidence", "derived_from", "gaps"), at, errors)
        for field in ("statement", "scope", "confidence_rationale"):
            if not nonempty(finding.get(field)):
                errors.append(f"{at}.{field}: required non-empty string")
        kind = finding.get("classification")
        if not one_of(kind, CLASSES):
            errors.append(f"{at}.classification: invalid value")
        if not one_of(finding.get("confidence"), CONFIDENCE):
            errors.append(f"{at}.confidence: invalid value")
        if not date(finding.get("as_of")):
            errors.append(f"{at}.as_of: expected ISO date")
        evidence = items(finding.get("evidence"))
        parents = items(finding.get("derived_from"))
        gaps = items(finding.get("gaps"))
        for field in ("evidence", "derived_from", "gaps"):
            if not isinstance(finding.get(field), list):
                errors.append(f"{at}.{field}: expected array")
        for n, link in enumerate(evidence):
            link = obj(link)
            if not nonempty(link.get("source_id")) or link.get("source_id") not in sources:
                errors.append(f"{at}.evidence[{n}].source_id: unresolved")
            if not one_of(link.get("relationship"), {"supports", "contradicts", "context"}):
                errors.append(f"{at}.evidence[{n}].relationship: invalid")
            if not nonempty(link.get("locator")):
                errors.append(f"{at}.evidence[{n}].locator: required")
        for parent in parents:
            if not nonempty(parent) or parent not in findings:
                errors.append(f"{at}.derived_from: unresolved {parent}")
        if one_of(kind, {"Fact", "Claim"}) and not any(obj(e).get("relationship") == "supports" for e in evidence):
            errors.append(f"{at}: {kind} needs supporting evidence")
        if kind == "Inference" and not parents:
            errors.append(f"{at}: Inference needs derived_from")
        if kind == "Unknown" and (not gaps or not all(nonempty(gap) for gap in gaps)):
            errors.append(f"{at}: Unknown needs a non-empty gap")
        if kind != "Inference" and parents:
            errors.append(f"{at}: only Inference may use derived_from")
        if kind != "Unknown" and gaps and not all(nonempty(g) for g in gaps):
            errors.append(f"{at}.gaps: blank gap")
    visiting: set[str] = set()
    traced: dict[str, bool] = {}
    reported_cycles: set[str] = set()
    for root_id in findings:
        stack = [(root_id, False)]
        while stack:
            fid, exiting = stack.pop()
            if exiting:
                visiting.discard(fid)
                finding = findings[fid]
                if finding.get("classification") == "Inference":
                    traced[fid] = any(
                        traced.get(parent, False)
                        for parent in items(finding.get("derived_from"))
                        if nonempty(parent)
                    )
                    if not traced[fid]:
                        errors.append(f"{path}.findings[{fid}]: inference has no source-backed or Unknown path")
                else:
                    traced[fid] = finding.get("classification") == "Unknown" or any(
                        obj(link).get("relationship") == "supports"
                        and nonempty(obj(link).get("source_id"))
                        and obj(link).get("source_id") in sources
                        for link in items(finding.get("evidence"))
                    )
                continue
            if fid in traced:
                continue
            if fid in visiting:
                if fid not in reported_cycles:
                    errors.append(f"{path}.findings[{fid}]: derivation cycle")
                    reported_cycles.add(fid)
                continue
            visiting.add(fid)
            stack.append((fid, True))
            parents = items(findings[fid].get("derived_from")) if findings[fid].get("classification") == "Inference" else []
            for parent in reversed(parents):
                if nonempty(parent) and parent in findings:
                    stack.append((parent, False))
    for n, conflict in enumerate(items(report.get("conflicts"))):
        refs = items(obj(conflict).get("finding_ids"))
        valid_refs = [ref for ref in refs if nonempty(ref)]
        if len(set(valid_refs)) < 2 or len(valid_refs) != len(refs) or any(ref not in findings for ref in valid_refs):
            errors.append(f"{path}.conflicts[{n}].finding_ids: need two distinct resolved findings")
        for field in ("dimension", "impact"):
            if not nonempty(obj(conflict).get(field)):
                errors.append(f"{path}.conflicts[{n}].{field}: required")
    for n, gap in enumerate(items(report.get("gaps"))):
        for field in ("question", "reason", "validation_step"):
            if not nonempty(obj(gap).get(field)):
                errors.append(f"{path}.gaps[{n}].{field}: required")
    if any(finding.get("classification") == "Unknown" for finding in findings.values()) and not items(report.get("gaps")):
        errors.append(f"{path}.gaps: Unknown needs a recorded validation gap")
    return errors


def package_errors(data: object) -> list[str]:
    errors: list[str] = []
    package = obj(data)
    required(package, ("schema_version", "package_id", "status", "question", "context",
                       "problem", "lanes", "reports", "claims", "analysis", "recommendation"),
             "package", errors)
    if not nonempty(package.get("schema_version")) or not SUPPORTED_VERSION.fullmatch(package["schema_version"]):
        errors.append("package.schema_version: expected compatible 1.x")
    if not one_of(package.get("status"), {"draft", "ready_for_decision"}):
        errors.append("package.status: invalid")
    for field in ("package_id", "question"):
        if not nonempty(package.get(field)):
            errors.append(f"package.{field}: required non-empty string")
    context = obj(package.get("context"))
    required(context, ("product", "target_users", "geography", "as_of", "decision_owner"), "package.context", errors)
    if not date(context.get("as_of")):
        errors.append("package.context.as_of: expected ISO date")
    if not isinstance(context.get("target_users"), list):
        errors.append("package.context.target_users: expected array")
    elif not all(nonempty(user) for user in context["target_users"]):
        errors.append("package.context.target_users: expected non-empty strings")
    problem = obj(package.get("problem"))
    required(problem, ("statement", "alternatives", "why_now"), "package.problem", errors)
    if not nonempty(problem.get("statement")):
        errors.append("package.problem.statement: required")
    if not isinstance(problem.get("alternatives"), list):
        errors.append("package.problem.alternatives: expected array")
    elif not all(nonempty(alt) for alt in problem["alternatives"]):
        errors.append("package.problem.alternatives: expected non-empty strings")
    if not nonempty(problem.get("why_now")):
        errors.append("package.problem.why_now: required")
    reports_list = items(package.get("reports"))
    if not isinstance(package.get("reports"), list):
        errors.append("package.reports: expected array")
    reports = unique_records(reports_list, "report_id", "package.reports", errors)
    for report_id, report in reports.items():
        errors.extend(report_errors(report, f"package.reports[{report_id}]"))
    lanes = obj(package.get("lanes"))
    if set(lanes) != {"policy", "market", "competitive", "user_signals"}:
        errors.append("package.lanes: expected exactly policy, market, competitive, user_signals")
    for lane_name, value in lanes.items():
        lane = obj(value)
        status = lane.get("status")
        refs = items(lane.get("report_ids"))
        if not isinstance(lane.get("report_ids"), list):
            errors.append(f"package.lanes.{lane_name}.report_ids: expected array")
        if not one_of(status, LANE_STATUS):
            errors.append(f"package.lanes.{lane_name}.status: invalid")
        if not nonempty(lane.get("reason")):
            errors.append(f"package.lanes.{lane_name}.reason: required")
        if one_of(status, {"complete", "limited"}) and not refs:
            errors.append(f"package.lanes.{lane_name}: report required")
        if one_of(status, {"missing", "not_applicable"}) and refs:
            errors.append(f"package.lanes.{lane_name}: must not reference a report")
        for ref in refs:
            if not nonempty(ref) or ref not in reports:
                errors.append(f"package.lanes.{lane_name}.report_ids: unresolved {ref}")
    if not isinstance(package.get("claims"), list):
        errors.append("package.claims: expected array")
    claims = unique_records(items(package.get("claims")), "claim_id", "package.claims", errors)
    for cid, claim in claims.items():
        at = f"package.claims[{cid}]"
        if not nonempty(claim.get("statement")):
            errors.append(f"{at}.statement: required")
        if not one_of(claim.get("role"), {"supports", "opposes", "context"}):
            errors.append(f"{at}.role: invalid")
        refs = items(claim.get("finding_refs"))
        if not isinstance(claim.get("finding_refs"), list):
            errors.append(f"{at}.finding_refs: expected array")
        if claim.get("unknown_reason") is not None and not nonempty(claim.get("unknown_reason")):
            errors.append(f"{at}.unknown_reason: expected non-empty string or null")
        if not refs and not nonempty(claim.get("unknown_reason")):
            errors.append(f"{at}: needs a finding or unknown_reason")
        for ref in refs:
            ref = obj(ref)
            rid = ref.get("report_id")
            fid = ref.get("finding_id")
            if not nonempty(rid) or rid not in reports or not nonempty(fid) or fid not in {
                obj(f).get("finding_id") for f in items(reports.get(rid, {}).get("findings"))
            }:
                errors.append(f"{at}.finding_refs: unresolved {rid}/{fid}")
    analysis = obj(package.get("analysis"))
    required(analysis, ("unmet_needs", "differentiation", "constraints", "size_or_impact",
                        "assumptions", "opposing_evidence", "conflicts", "gaps"),
             "package.analysis", errors)
    for field in ("unmet_needs", "differentiation", "constraints", "assumptions",
                  "opposing_evidence", "conflicts", "gaps"):
        if not isinstance(analysis.get(field), list):
            errors.append(f"package.analysis.{field}: expected array")
        elif not all(nonempty(value) for value in analysis[field]):
            errors.append(f"package.analysis.{field}: expected non-empty strings")
    for field in ("product", "geography"):
        value = context.get(field)
        if value is not None and not nonempty(value):
            errors.append(f"package.context.{field}: expected non-empty string or null")
        if not nonempty(value) and not items(analysis.get("gaps")):
            errors.append(f"package.context.{field}: missing scope needs a gap")
    if not items(context.get("target_users")) and not items(analysis.get("gaps")):
        errors.append("package.context.target_users: missing scope needs a gap")
    for field in ("unmet_needs", "differentiation", "constraints", "opposing_evidence"):
        for ref in items(analysis.get(field)):
            if not nonempty(ref) or ref not in claims:
                errors.append(f"package.analysis.{field}: unresolved claim {ref}")
    size = analysis.get("size_or_impact")
    if size is not None:
        size = obj(size)
        required(size, ("estimate", "unit", "method", "assumptions", "claim_ids"),
                 "package.analysis.size_or_impact", errors)
        for field in ("estimate", "unit", "method"):
            if not nonempty(size.get(field)):
                errors.append(f"package.analysis.size_or_impact.{field}: required")
        for field in ("assumptions", "claim_ids"):
            if not isinstance(size.get(field), list):
                errors.append(f"package.analysis.size_or_impact.{field}: expected array")
        for ref in items(size.get("claim_ids")):
            if not nonempty(ref) or ref not in claims:
                errors.append(f"package.analysis.size_or_impact.claim_ids: unresolved {ref}")
        if not any(
            source_backed_claim(claims[ref], reports)
            for ref in items(size.get("claim_ids"))
            if nonempty(ref) and ref in claims
        ):
            errors.append("package.analysis.size_or_impact: needs source-backed inputs")
    recommendation = obj(package.get("recommendation"))
    required(recommendation, ("decision", "confidence", "rationale", "claim_ids",
                              "proposed_scope", "risks", "validation_steps"),
             "package.recommendation", errors)
    if not one_of(recommendation.get("decision"), DECISIONS):
        errors.append("package.recommendation.decision: invalid")
    if not one_of(recommendation.get("confidence"), CONFIDENCE):
        errors.append("package.recommendation.confidence: invalid")
    if not nonempty(recommendation.get("rationale")):
        errors.append("package.recommendation.rationale: required")
    for field in ("claim_ids", "risks", "validation_steps"):
        if not isinstance(recommendation.get(field), list):
            errors.append(f"package.recommendation.{field}: expected array")
        elif not all(nonempty(value) for value in recommendation[field]):
            errors.append(f"package.recommendation.{field}: expected non-empty strings")
    for ref in items(recommendation.get("claim_ids")):
        if not nonempty(ref) or ref not in claims:
            errors.append(f"package.recommendation.claim_ids: unresolved {ref}")
    user_reports = {ref for ref in items(obj(lanes.get("user_signals")).get("report_ids")) if nonempty(ref)}
    user_evidence = any(
        claims[cid].get("role") == "supports"
        and source_backed_claim(claims[cid], reports, user_reports)
        for cid in items(recommendation.get("claim_ids"))
        if nonempty(cid) and cid in claims
    )
    if recommendation.get("decision") == "pursue":
        if not user_evidence:
            errors.append("package.recommendation: pursue needs source-backed user signals")
        opposing = {cid for cid, claim in claims.items() if claim.get("role") == "opposes"}
        acknowledged = {cid for cid in items(analysis.get("opposing_evidence")) if nonempty(cid)}
        if opposing - acknowledged:
            errors.append("package.analysis.opposing_evidence: pursue must acknowledge opposing evidence")
    if package.get("status") == "ready_for_decision":
        if not nonempty(context.get("decision_owner")):
            errors.append("package.context.decision_owner: required for readiness")
        if not any(
            source_backed_claim(claims[cid], reports)
            for cid in items(recommendation.get("claim_ids"))
            if nonempty(cid) and cid in claims
        ):
            errors.append("package.status: readiness needs a source-backed claim")
        decisive_unknown = any(
            unknown_path_claim(claims[cid], reports)
            for cid in items(recommendation.get("claim_ids"))
            if nonempty(cid) and cid in claims
        )
        if (analysis.get("gaps") or decisive_unknown) and not items(recommendation.get("validation_steps")):
            if decisive_unknown:
                errors.append("package.recommendation.validation_steps: Unknown needs a validation step")
            else:
                errors.append("package.recommendation.validation_steps: needed for gaps")
    return errors


def artifact_errors(data: object) -> list[str]:
    """Choose the contract from package-only fields, even when its ID is missing."""
    if isinstance(data, dict) and any(key in data for key in ("package_id", "lanes", "reports", "recommendation")):
        return package_errors(data)
    return report_errors(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    args = parser.parse_args()
    failed = False
    for path in args.files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"{path}: {exc}", file=sys.stderr)
            failed = True
            continue
        errors = artifact_errors(data)
        if errors:
            failed = True
            for error in errors:
                print(f"{path}: {error}", file=sys.stderr)
        else:
            print(f"{path}: valid")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

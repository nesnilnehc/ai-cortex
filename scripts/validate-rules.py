#!/usr/bin/env python3
"""Validate RULE_MODEL_V1 documents without third-party dependencies."""

from __future__ import annotations

import pathlib
import re
import sys
from datetime import date


ROOT = pathlib.Path(__file__).resolve().parents[1]
RULES_DIR = ROOT / "rules"
INDEX = RULES_DIR / "INDEX.md"
REQUIRED_FRONTMATTER = {
    "artifact_type",
    "name",
    "version",
    "model",
    "rule_prefix",
    "scope",
    "recommended_scope",
    "status",
    "created_by",
    "lifecycle",
    "created_at",
}
REQUIRED_SECTIONS = {
    "Scope",
    "Profiles and parameters",
    "Rules",
    "Severity and gate policy",
    "Waivers",
    "References",
}
REQUIRED_ITEM_FIELDS = {
    "Level",
    "Requirement",
    "Applies when",
    "Default severity",
    "Enforcement",
    "Evidence",
    "Pass condition",
    "Not applicable when",
    "Remediation",
}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
ITEM_HEADING = re.compile(r"^### ([A-Z]{3,8}-\d{3}) — (.+)$", re.MULTILINE)
LEVEL = re.compile(r"^(baseline|profile:[a-z0-9][a-z0-9-]*|project:[a-z0-9][a-z0-9._-]*)$")
VALID_SCOPES = {"user", "project", "both"}
VALID_STATUSES = {"draft", "active", "superseded", "archived"}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    try:
        block = text.split("---\n", 2)[1]
    except IndexError:
        return {}
    result: dict[str, str] = {}
    for line in block.splitlines():
        match = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if match:
            result[match.group(1)] = match.group(2).strip()
    return result


def parse_item_fields(block: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|", 1)]
        if len(cells) != 2 or cells[0] in {"Field", "---"}:
            continue
        fields[cells[0].strip("`")] = cells[1]
    return fields


def validate(path: pathlib.Path, index_text: str) -> tuple[list[str], set[str]]:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    errors: list[str] = []
    ids: set[str] = set()

    missing = REQUIRED_FRONTMATTER - frontmatter.keys()
    if missing:
        errors.append(f"missing frontmatter: {', '.join(sorted(missing))}")
    if frontmatter.get("artifact_type") != "rule":
        errors.append("artifact_type must be rule")
    if frontmatter.get("model") != "RULE_MODEL_V1":
        errors.append("model must be RULE_MODEL_V1")
    if frontmatter.get("name") != path.stem:
        errors.append("name must match the filename")
    if not SEMVER.fullmatch(frontmatter.get("version", "")):
        errors.append("version must be SemVer")
    if frontmatter.get("recommended_scope") not in VALID_SCOPES:
        errors.append("recommended_scope must be user, project or both")
    if frontmatter.get("status") not in VALID_STATUSES:
        errors.append("status must be draft, active, superseded or archived")
    if frontmatter.get("status") == "superseded" and not frontmatter.get(
        "superseded_by"
    ):
        errors.append("superseded_by is required when status is superseded")
    if frontmatter.get("created_by") != "ai-cortex":
        errors.append("created_by must be ai-cortex")
    if frontmatter.get("lifecycle") != "living":
        errors.append("lifecycle must be living")
    try:
        date.fromisoformat(frontmatter.get("created_at", ""))
    except ValueError:
        errors.append("created_at must be an ISO date")
    prefix = frontmatter.get("rule_prefix", "")
    if not re.fullmatch(r"[A-Z]{3,8}", prefix):
        errors.append("rule_prefix must be 3-8 uppercase letters")
    if f"(./{path.name})" not in index_text:
        errors.append("file is not registered in rules/INDEX.md")

    section_matches = list(re.finditer(r"^## ([^#\n].+)$", text, re.MULTILINE))
    sections = {match.group(1) for match in section_matches}
    missing_sections = REQUIRED_SECTIONS - sections
    if missing_sections:
        errors.append(f"missing sections: {', '.join(sorted(missing_sections))}")
    else:
        required_order = [
            "Scope",
            "Profiles and parameters",
            "Rules",
            "Severity and gate policy",
            "Waivers",
            "References",
        ]
        positions = {
            match.group(1): match.start()
            for match in section_matches
            if match.group(1) in REQUIRED_SECTIONS
        }
        if [positions[name] for name in required_order] != sorted(
            positions[name] for name in required_order
        ):
            errors.append("required sections are not in the modeled order")

    matches = list(ITEM_HEADING.finditer(text))
    if not matches:
        errors.append("no modeled Rule items found")
    seen_ids: set[str] = set()
    for number, match in enumerate(matches):
        rule_id = match.group(1)
        if rule_id in seen_ids:
            errors.append(f"{rule_id}: duplicate identifier in the same document")
        seen_ids.add(rule_id)
        ids.add(rule_id)
        if prefix and not rule_id.startswith(f"{prefix}-"):
            errors.append(f"{rule_id}: identifier does not use rule_prefix {prefix}")
        candidate_ends = [len(text)]
        if number + 1 < len(matches):
            candidate_ends.append(matches[number + 1].start())
        following_section = re.search(r"^## ", text[match.end() :], re.MULTILINE)
        if following_section:
            candidate_ends.append(match.end() + following_section.start())
        block = text[match.end() : min(candidate_ends)]
        if len(re.findall(r"^\| Field \|", block, re.MULTILINE)) != 1:
            errors.append(f"{rule_id}: needs exactly one Field table")
        fields = parse_item_fields(block)
        missing_fields = REQUIRED_ITEM_FIELDS - fields.keys()
        if missing_fields:
            errors.append(f"{rule_id}: missing fields: {', '.join(sorted(missing_fields))}")
        empty_fields = sorted(name for name in REQUIRED_ITEM_FIELDS if not fields.get(name))
        if empty_fields:
            errors.append(f"{rule_id}: empty fields: {', '.join(empty_fields)}")
        level = fields.get("Level", "").strip("`")
        if level and not LEVEL.fullmatch(level):
            errors.append(f"{rule_id}: invalid Level")
        requirement = fields.get("Requirement", "")
        if "**MUST**" not in requirement and "**MUST NOT**" not in requirement:
            errors.append(f"{rule_id}: Requirement needs one explicit MUST or MUST NOT")
        severity = fields.get("Default severity", "").strip("`")
        if severity not in {"critical", "major", "minor", "suggestion"}:
            errors.append(f"{rule_id}: invalid Default severity")
        enforcement = fields.get("Enforcement", "").strip("`")
        if enforcement not in {"automated", "tool-assisted", "judgment"}:
            errors.append(f"{rule_id}: invalid Enforcement")
    return errors, ids


def main() -> int:
    candidates = sorted(RULES_DIR.glob("*.md"))
    modeled = [
        path
        for path in candidates
        if parse_frontmatter(path.read_text(encoding="utf-8")).get("model")
        == "RULE_MODEL_V1"
    ]
    index_text = INDEX.read_text(encoding="utf-8")
    all_errors: list[str] = []
    owners: dict[str, pathlib.Path] = {}

    for path in modeled:
        errors, ids = validate(path, index_text)
        all_errors.extend(f"{path.relative_to(ROOT)}: {error}" for error in errors)
        for rule_id in ids:
            if rule_id in owners:
                all_errors.append(
                    f"duplicate Rule ID {rule_id}: "
                    f"{owners[rule_id].relative_to(ROOT)} and {path.relative_to(ROOT)}"
                )
            owners[rule_id] = path

    if all_errors:
        print("Rule validation failed:")
        for error in all_errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(modeled)} modeled Rule documents and {len(owners)} Rule items.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

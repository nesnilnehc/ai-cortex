#!/usr/bin/env python3
"""Verify that a language migration changed prose only.

Compares each file against a git ref and asserts that every machine-meaningful
element survived the rewrite. Prose is expected to differ; everything else is
not. Exits non-zero when a HARD invariant breaks.

Usage:
    scripts/verify-translation.py <git-ref> <path>...
    scripts/verify-translation.py HEAD~1 rules/
"""
import re
import subprocess
import sys
import pathlib
from collections import Counter

# --- invariant extractors -------------------------------------------------

FRONTMATTER = re.compile(r'\A---\n(.*?)\n---\n', re.S)
# identifiers we must never lose: kebab-case names, snake_case fields, dotted paths
IDENT = re.compile(r'`([A-Za-z_][\w./-]*(?:\.[a-z]+)?)`')
# numbers incl. ranges, percentages, versions, priority codes
NUMBER = re.compile(r'\b(?:\d+\.\d+\.\d+|\d+(?:[–\-]\d+)?%?|[PL]\d)\b')
KEYWORDS = ("MUST NOT", "MUST", "SHOULD NOT", "SHOULD", "halt", "HALT",
            "STOP", "ASK", "❌", "✅")

# Normative markers in either language. A pure translation moves a constraint
# from one column to the other; it never makes one disappear. Weakening
# "不得" into "尽量不" (or MUST into SHOULD) drops the total.
# Alternation is longest-first so that 必须 is not also counted as 须.
STRONG_RE = re.compile(
    r'必须|必填|不得|禁止|严禁|务必|不留空|须|'
    r'[Mm]ust not|MUST NOT|[Mm]ust|MUST|[Nn]ever|[Rr]equired|shall')
WEAK_RE = re.compile(
    r'应当|应该|建议|尽量|最好|优先|避免|'
    r'SHOULD NOT|SHOULD|[Pp]refer|recommended|[Ss]uggest(?:ed|ion)?|[Aa]void')


def frontmatter(text):
    m = FRONTMATTER.match(text)
    if not m:
        return {}
    out = {}
    for line in m.group(1).split("\n"):
        km = re.match(r'^([a-z_]+):\s*(.*)$', line)
        if km:
            out[km.group(1)] = km.group(2).strip()
    return out


def blocks(text):
    """Fenced code blocks as (lang, body). Bodies must be identical."""
    out, cur, lang, inside = [], [], None, False
    for line in text.split("\n"):
        if line.startswith("```"):
            if inside:
                out.append((lang, "\n".join(cur)))
                cur, inside = [], False
            else:
                lang, inside = line[3:].strip(), True
            continue
        if inside:
            cur.append(line)
    return out


def strip_code(text):
    """Text with fenced blocks removed, so prose-level scans ignore code."""
    out, inside = [], False
    for line in text.split("\n"):
        if line.startswith("```"):
            inside = not inside
            continue
        if not inside:
            out.append(line)
    return "\n".join(out)


def extract(text):
    prose = strip_code(text)
    return {
        "frontmatter": frontmatter(text),
        "heading_depths": [len(m.group(1)) for m in
                           re.finditer(r'^(#{1,6}) ', prose, re.M)],
        "code_blocks": [b for _, b in blocks(text)],
        "code_langs": Counter(l for l, _ in blocks(text)),
        "links": Counter(m.group(1) for m in
                         re.finditer(r'\]\(([^)\s]+)\)', prose)),
        "identifiers": Counter(IDENT.findall(prose)),
        "numbers": Counter(NUMBER.findall(prose)),
        "keywords": Counter({k: prose.count(k) for k in KEYWORDS}),
        "list_items": len(re.findall(r'^\s*(?:[-*+]|\d+\.)\s', prose, re.M)),
        "checkboxes": len(re.findall(r'^\s*- \[[ x]\]', prose, re.M)),
        "table_rows": len(re.findall(r'^\|', prose, re.M)),
        "strong_constraints": len(STRONG_RE.findall(prose)),
        "weak_constraints": len(WEAK_RE.findall(prose)),
    }


# HARD invariants abort the migration; SOFT ones are reported for judgement.
HARD = ("frontmatter", "code_blocks", "links", "identifiers", "numbers",
        "checkboxes", "list_items", "strong_constraints", "weak_constraints")
SOFT = ("heading_depths", "code_langs", "keywords", "table_rows")


def compare(old, new):
    findings = []
    for key in HARD + SOFT:
        a, b = old[key], new[key]
        if a == b:
            continue
        sev = "HARD" if key in HARD else "SOFT"
        if isinstance(a, Counter):
            lost = a - b
            gained = b - a
            detail = []
            if lost:
                detail.append(f"lost {dict(lost)}")
            if gained:
                detail.append(f"gained {dict(gained)}")
            findings.append((sev, key, "; ".join(detail)))
        elif isinstance(a, dict):
            for k in set(a) | set(b):
                if a.get(k) != b.get(k):
                    findings.append((sev, f"{key}.{k}",
                                     f"{a.get(k)!r} -> {b.get(k)!r}"))
        elif isinstance(a, list):
            if len(a) != len(b):
                findings.append((sev, key, f"count {len(a)} -> {len(b)}"))
            else:
                for i, (x, y) in enumerate(zip(a, b)):
                    if x != y:
                        findings.append((sev, f"{key}[{i}]",
                                         f"body changed: {x[:60]!r} -> {y[:60]!r}"))
        else:
            findings.append((sev, key, f"{a} -> {b}"))
    return findings


def main():
    mode = "translate"
    argv = sys.argv[1:]
    if argv and argv[0].startswith("--mode="):
        mode = argv.pop(0).split("=", 1)[1]
    if len(argv) < 2:
        print(__doc__)
        return 2
    ref, targets = argv[0], argv[1:]

    paths = []
    for t in targets:
        p = pathlib.Path(t)
        paths.extend(sorted(p.rglob("*.md")) if p.is_dir() else [p])

    hard = soft = clean = skipped = 0
    for path in paths:
        old_text = subprocess.run(["git", "show", f"{ref}:{path}"],
                                  capture_output=True, text=True).stdout
        if not old_text:
            skipped += 1
            continue
        findings = compare(extract(old_text), extract(path.read_text()))
        h = [f for f in findings if f[0] == "HARD"]
        s = [f for f in findings if f[0] == "SOFT"]
        if not findings:
            clean += 1
            continue
        hard += len(h)
        soft += len(s)
        print(f"\n{path}")
        for sev, key, detail in findings:
            print(f"  [{sev}] {key}: {detail}")

    print(f"\n{'=' * 60}")
    print(f"files: {len(paths)}  clean: {clean}  skipped(new): {skipped}")
    print(f"HARD violations: {hard}   SOFT differences: {soft}")
    if mode == "translate":
        if hard:
            print("\nHARD violations mean machine-meaningful content changed "
                  "inside what was declared a pure translation. Either fix the "
                  "translation, or split the content change into its own commit.")
        return 1 if hard else 0
    print("\nmode=rewrite: differences reported, not gated. "
          "Content changes must be justified in the commit message.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

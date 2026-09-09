#!/usr/bin/env python3
"""Verify that a language migration changed prose only.

Compares each file against a git ref and asserts that every machine-meaningful
element survived the rewrite. Prose is expected to differ; everything else is
not. Exits non-zero when a HARD invariant breaks.

Usage:
    scripts/verify-translation.py <git-ref> <path>...
    scripts/verify-translation.py HEAD~1 rules/
"""
import json
import re
import subprocess
import sys
import pathlib
from collections import Counter

WAIVERS_PATH = pathlib.Path(__file__).with_name("translation-waivers.json")

CJK = re.compile(r'[\u4e00-\u9fff]')
# Above this share of the original's Chinese still present, the file is treated
# as only partly translated. "unchanged" catches a file nobody touched; this
# catches one where only the headings were done. Files that legitimately retain
# Chinese - detection patterns, counter-examples - are waived by name.
RESIDUAL_LIMIT = 0.25
# Below this many Chinese characters the baseline was not a translation target,
# so the residual ratio is meaningless - a file already in English keeps a
# handful of characters in its frontmatter and would read as 100% untranslated.
RESIDUAL_MIN_BASELINE = 100

# --- invariant extractors -------------------------------------------------

FRONTMATTER = re.compile(r'\A---\n(.*?)\n---\n', re.S)
# Everything inside backticks. Backticks mark tokens that carry meaning
# literally - field names, paths, enum values, command fragments - and a
# translation must not alter any of them. Matching the whole span rather than
# an identifier shape also catches `artifact_type: tasks` and similar, which an
# identifier-shaped pattern silently ignores.
IDENT = re.compile(r'`([^`\n]+)`')
# numbers incl. ranges, percentages, versions, priority codes
NUMBER = re.compile(
    r'(?<![\w.])(?:\d+\.\d+\.\d+|\d+(?:[–\-]\d+)?%?|[PL]\d)')
KEYWORDS = ("MUST NOT", "MUST", "SHOULD NOT", "SHOULD", "halt", "HALT",
            "STOP", "ASK", "❌", "✅")

# Normative markers in either language. A pure translation moves a constraint
# from one column to the other; it never makes one disappear. Weakening
# "不得" into "尽量不" (or MUST into SHOULD) drops the total.
# Alternation is longest-first so that 必须 is not also counted as 须.
STRONG_RE = re.compile(
    r'必须|必填|必备|不得|禁止|严禁|务必|不留空|永不|绝不|须|'
    r'[Mm]ust not|MUST NOT|[Mm]ust|MUST|[Nn]ever|[Rr]equired|shall|'
    r'[Ff]orbidden|[Pp]rohibited')
WEAK_RE = re.compile(
    r'应当|应该|建议|推荐|尽量|最好|优先(?!级)|避免|'
    r'[Ss]hould not|SHOULD NOT|[Ss]hould|SHOULD|[Pp]refer(?!ence)|recommended|[Ss]uggest(?:ed|ion)?|[Aa]void')


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


COMMENT = re.compile(r'^\s*(?:#|//|--|<!--|\*|/\*)')


def strip_trailing_comment(line):
    """Drop a trailing comment from a code line, respecting quotes.

    A trailing comment is prose for the reader just as a full-line comment is,
    so it follows the language migration. The executable part of the line is
    still compared byte for byte.
    """
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote and (i == 0 or line[i - 1] != "\\"):
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            continue
        if ch == "#" and i and line[i - 1] in " \t":
            return line[:i].rstrip()
        if line[i:i + 2] == "//" and i and line[i - 1] in " \t":
            return line[:i].rstrip()
    return line


PLACEHOLDER = re.compile(r'<[^<>\n]{1,80}>')


def normalise_placeholders(line):
    """Collapse <...> slots so their descriptions do not count as code.

    In a template, `description: <a one-line summary>` is a slot whose angle
    brackets are the contract and whose inner text is prose for the reader. The
    field name, the structure and the presence of the slot are all still
    compared; only the wording inside it is free to follow the migration.
    """
    return PLACEHOLDER.sub("<>", line)


def split_code(body):
    """Separate executable lines from comment lines inside a code block.

    Code must survive a translation byte-for-byte. Comments inside an example
    are prose written for the reader, so they follow the language migration
    like any other prose; only their count is held invariant.
    """
    code, comments = [], 0
    for line in body.split("\n"):
        if not line.strip():
            continue
        if COMMENT.match(line):
            comments += 1
        else:
            stripped = normalise_placeholders(strip_trailing_comment(line))
            if stripped != line:
                comments += 1
            code.append(stripped)
    return "\n".join(code), comments


def blocks(text):
    """Fenced code blocks as (lang, body)."""
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
        # Blocks tagged with a real language hold code and are compared byte
        # for byte. Blocks tagged text or markdown hold illustrative prose, and
        # follow the language migration like any other prose, so their bodies
        # are reported as SOFT. The block COUNT stays HARD either way, so
        # dropping a whole block is still caught.
        "code_blocks": [split_code(b)[0] for lg, b in blocks(text)
                        if lg not in ("text", "markdown", "")],
        "prose_blocks": [split_code(b)[0] for lg, b in blocks(text)
                         if lg in ("text", "markdown", "")],
        "block_count": len(blocks(text)),
        "code_comment_lines": sum(split_code(b)[1] for _, b in blocks(text)),
        "code_langs": Counter(l for l, _ in blocks(text)),
        "links": Counter(m.group(1) for m in
                         re.finditer(r'\]\(([^)\s]+)\)', prose)),
        # A backticked span containing CJK is illustrative prose - a
        # placeholder like `archived_reason: <原因>`, a counter-example like
        # `1.5.0 — 完善文档` - and follows the migration. One without CJK is a
        # literal token: a field name, a path, an enum value, a format string.
        "identifiers": Counter(x for x in IDENT.findall(prose)
                               if not CJK.search(x)),
        "prose_spans": Counter(x for x in IDENT.findall(prose)
                               if CJK.search(x)),
        "numbers": Counter(NUMBER.findall(prose)),
        "keywords": Counter({k: prose.count(k) for k in KEYWORDS}),
        "list_items": len(re.findall(r'^\s*(?:[-*+]|\d+\.)\s', prose, re.M)),
        "checkboxes": len(re.findall(r'^\s*- \[[ x]\]', prose, re.M)),
        "table_rows": len(re.findall(r'^\|', prose, re.M)),
        "strong_constraints": len(STRONG_RE.findall(prose)),
        "weak_constraints": len(WEAK_RE.findall(prose)),
    }


# HARD invariants abort the migration; SOFT ones are reported for judgement.
HARD = ("frontmatter", "code_blocks", "block_count", "links",
        "numbers", "checkboxes", "list_items")
SOFT = ("heading_depths", "code_langs", "keywords", "table_rows",
        "code_comment_lines", "prose_blocks", "prose_spans")

# Constraint markers are checked by direction, not by equality. English needs
# more modals than Chinese to say the same thing, so demanding equal counts
# produces constant noise. Only the dangerous directions block:
#   strong down  - a prohibition or obligation was weakened or lost
#   weak up      - a hedge was introduced where the original had none
# The opposite directions are usually idiom and are reported as SOFT.
DIRECTIONAL = {"strong_constraints": "down", "weak_constraints": "up",
               # A literal token must never disappear. A gained one is usually
               # the English rendering of a backticked prose span, whose Chinese
               # form was excluded from this set by construction.
               "identifiers": "down"}


def compare(old, new):
    findings = []
    for key, bad in DIRECTIONAL.items():
        a, b = old[key], new[key]
        if a == b:
            continue
        if isinstance(a, Counter):
            lost, gained = a - b, b - a
            if lost:
                findings.append(("HARD", key, f"lost {dict(lost)}"))
            if gained:
                findings.append(("SOFT", key, f"gained {dict(gained)}"))
            continue
        dropped = b < a
        dangerous = (bad == "down" and dropped) or (bad == "up" and not dropped)
        sev = "HARD" if dangerous else "SOFT"
        why = ("weakened or lost" if bad == "down" and dropped
               else "hedge introduced" if bad == "up" and not dropped
               else "opposite direction, usually idiom")
        findings.append((sev, key, f"{a} -> {b} ({why})"))
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


def load_waivers():
    """Recorded exemptions, keyed by "<path>::<invariant>" with a reason.

    The constraint-marker invariants are heuristics: 不可 is a prohibition in
    不可只增不减 and means "cannot" in 不可验证, and no regex separates the two.
    Rather than loosen the gate, a mismatch diagnosed as a marker artefact is
    recorded here with its reason. Nothing passes silently either way.
    """
    if not WAIVERS_PATH.exists():
        return {}
    return json.loads(WAIVERS_PATH.read_text())


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

    waivers = load_waivers()
    waived = []
    hard = soft = clean = skipped = 0
    for path in paths:
        old_text = subprocess.run(["git", "show", f"{ref}:{path}"],
                                  capture_output=True, text=True).stdout
        if not old_text:
            skipped += 1
            continue

        new_text = path.read_text()
        if mode == "translate" and old_text == new_text:
            # A file identical to its baseline was never touched. The invariant
            # comparison would pass trivially - every invariant matches itself -
            # so an omitted file is invisible unless checked for explicitly.
            hard += 1
            print(f"\n{path}")
            print("  [HARD] unchanged: identical to the baseline, so nothing "
                  "was translated. An omitted file passes every invariant "
                  "trivially; this check is what makes it visible.")
            continue
        old_cjk = len(CJK.findall(old_text))
        new_cjk = len(CJK.findall(new_text))
        if (mode == "translate" and old_cjk >= RESIDUAL_MIN_BASELINE
                and new_cjk / old_cjk > RESIDUAL_LIMIT
                and not waivers.get(f"{path}::residual_chinese")):
            hard += 1
            print(f"\n{path}")
            print(f"  [HARD] residual_chinese: {new_cjk} of {old_cjk} "
                  f"characters remain ({new_cjk / old_cjk:.0%}); only part of "
                  f"the file was translated")
            continue

        findings = compare(extract(old_text), extract(new_text))
        kept = []
        for sev, key, detail in findings:
            # A waiver on the base invariant covers its indexed findings:
            # "code_blocks" also waives "code_blocks[0]", "code_blocks[3]".
            base = key.split("[", 1)[0]
            reason = (waivers.get(f"{path}::{key}")
                      or waivers.get(f"{path}::{base}"))
            if sev == "HARD" and reason:
                waived.append((str(path), key, reason))
                continue
            kept.append((sev, key, detail))
        findings = kept
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

    if waived:
        print(f"\n{'-' * 60}\nwaived (recorded in translation-waivers.json):")
        for f, key, reason in waived:
            print(f"  {f} :: {key}\n      {reason}")

    print(f"\n{'=' * 60}")
    print(f"files: {len(paths)}  clean: {clean}  skipped(new): {skipped}  "
          f"waived: {len(waived)}")
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

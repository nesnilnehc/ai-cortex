#!/usr/bin/env python3
"""Check bounded Markdown contracts with explicit, non-runtime reference consumers.

JSON here is a test-owned projection, not a new mandatory Skill output format.
Historical descriptors are independently pinned; current contracts come from Specs.
"""
from __future__ import annotations

from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/fixtures/stable-consumers'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(text, start, end, marker='yes'):
    section = text.split(start, 1)[1].split(end, 1)[0]
    result = []
    for line in section.splitlines():
        if not line.startswith('|'):
            continue
        cells = [cell.strip() for cell in line.strip('|').split('|')]
        name = cells[0].strip('`*').lower()
        if marker in cells[1:3] and re.fullmatch(r'[a-z_]+', name):
            result.append(name)
    return result



def contract(root):
    findings = (root / 'specs/findings-list.md').read_text()
    severity = findings.split('### 5.2 Severity', 1)[1].split('### 5.3', 1)[0]
    maturity = re.search(r'^\| \*\*Maturity\*\*.*$', findings, re.M).group()
    # Enum tokens are read from their defining rows, not duplicated current values.
    return {
        'findings_required': fields(findings, '### 5.1', '### 5.2'),
        'severities': re.findall(r'^\| `([^`]+)` \|', severity, re.M),
        'maturities': list(dict.fromkeys(re.findall(r'`([^`]+)`', maturity))),
        'coverage_required': fields(findings, '### 5.5', '## 6.'),
    }


def check_contract(root, baseline):
    current = contract(root)
    for key in ["findings_required", "severities", "maturities", "coverage_required"]:
        require(current[key] == baseline[key], f'{key}: protected contract drift; review compatibility, not just fixtures')


def review(data, descriptor):
    findings = data['findings']
    for finding in findings:
        require(all(isinstance(finding.get(key), str) and finding[key].strip()
                    for key in descriptor['findings_required']), 'finding: missing required text')
        require(finding['severity'] in descriptor['severities'], 'finding: invalid severity')
        require(finding['maturity'] in descriptor['maturities'], 'finding: invalid maturity')
    for coverage in data['coverage_by_emitter'].values():
        require(all(key in coverage for key in descriptor['coverage_required']), 'coverage: missing field')
        require(all(isinstance(coverage[key], list) for key in
                    ['passed', 'waived', 'not_applicable', 'evidence_limited']), 'coverage: expected lists')
    ordered = sorted(findings, key=lambda f: (descriptor['severities'].index(f['severity']), f['location']))
    # Keep duplicates and original maturity; coverage never contributes a finding.
    limited = [row['rule_id'] for coverage in data['coverage_by_emitter'].values()
               for row in coverage['evidence_limited']]
    return dict(ordered_titles=[f['title'] for f in ordered],
                severities=[f['severity'] for f in ordered],
                maturities=[f['maturity'] for f in ordered],
                sites=len({f['location'] for f in findings}),
                finding_count=sum(Counter(f['severity'] for f in findings).values()),
                evidence_limited=limited, ordered_findings=copy.deepcopy(ordered),
                coverage_by_emitter=copy.deepcopy(data['coverage_by_emitter']))


def main():
    for name in ['v0.5.1.json', 'v0.6.0.json']:
        baseline = json.loads((FIXTURES / name).read_text())
        for path, source in baseline['sources'].items():
            blob = subprocess.check_output(['git', '-C', str(ROOT), 'show', baseline['source_commit']+':'+path])
            require(hashlib.sha256(blob).hexdigest() == source['sha256'], 'historical source digest mismatch: '+path)
        check_contract(ROOT, baseline['contract'])
        fixture = json.loads((FIXTURES / 'review.json').read_text())
        require(review(fixture, baseline['contract']) == fixture['expected'], 'review projection drift')
    print('2 pinned historical descriptors and 2 review-reader pairs passed; release consumers retired.')


if __name__ == '__main__':
    main()

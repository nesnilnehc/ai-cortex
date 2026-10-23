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
    package = (root / 'specs/release-package.md').read_text()
    severity = findings.split('### 5.2 Severity', 1)[1].split('### 5.3', 1)[0]
    maturity = re.search(r'^\| \*\*Maturity\*\*.*$', findings, re.M).group()
    status = re.search(r'^\| `status`.*$', package, re.M).group()
    # Enum tokens are read from their defining rows, not duplicated current values.
    return {
        'findings_required': fields(findings, '### 5.1', '### 5.2'),
        'severities': re.findall(r'^\| `([^`]+)` \|', severity, re.M),
        'maturities': list(dict.fromkeys(re.findall(r'`([^`]+)`', maturity))),
        'coverage_required': fields(findings, '### 5.5', '## 6.'),
        'release_required': fields(package, '### 5.1', '### 5.2'),
        'release_conditional': [field for field in fields(package, '### 5.1', '### 5.2', 'conditional')
                                if field not in ['publication', 'communication']],
        'release_statuses': re.findall(r'`([^`]+)`', status)[1:],
        'check_statuses': re.findall(r'`(passed|failed|skipped)`', package.split('### 5.5', 1)[1].split('### 5.6', 1)[0])[:3],
        'domain_actions': re.findall(r'`(bump|preserve|derive)`', package.split('### 5.3', 1)[1].split('### 5.4', 1)[0]),
    }


def check_contract(root, baseline):
    current = contract(root)
    for key, values in baseline.items():
        require(current[key] == values, f'{key}: protected contract drift; review compatibility, not just fixtures')


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


def release(data, descriptor):
    require(all(key in data for key in descriptor['release_required']), 'package: missing required field')
    require(data['decision'] in ['release', 'none'], 'package: invalid decision')
    require(data['status'] in descriptor['release_statuses'], 'package: invalid status')
    require(re.fullmatch(r'1\.\d+\.\d+', data['schema_version']) is not None, 'unsupported schema major')
    require(re.fullmatch(r'[0-9a-f]{40}', data['commit']) is not None, 'package: invalid commit')
    for domain in data['version_domains'].values():
        require(all(k in domain for k in ['current', 'source', 'action']), 'domain: missing field')
        require(domain['action'] in descriptor['domain_actions'], 'domain: invalid action')
    if data['decision'] == 'none':
        require(data['status'] == 'not_required' and 'publication' not in data, 'no-release state mismatch')
        return dict(decision='none', version=None, tag=None, publishable=False)
    require(all(key in data for key in descriptor['release_conditional']), 'release: missing identity')
    require(re.fullmatch(r'\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?', data['version']) is not None,
            'release: invalid version')
    require(bool(data['release_channel']) and bool(data['version_source']), 'release: empty identity')
    require(data['status'] != 'not_required', 'release state mismatch')
    ready = data['status'] in ['ready', 'published', 'announced']
    for check in data['checks']:
        require(all(k in check for k in ['name', 'status', 'evidence', 'required']), 'check: missing field')
        require(check['status'] in descriptor['check_statuses'], 'check: invalid status')
        if ready and check['required']:
            evidence = check['evidence']
            require(check['status'] == 'passed' and isinstance(evidence, str) and bool(evidence.strip()),
                    'required check has no passing execution evidence')
            require(not re.search(r'\b0 (?:tests|cases) (?:executed|run|passed)\b|all.skipped', evidence, re.I),
                    'required check reports zero execution')
    for artifact in data['artifacts'].values():
        require(all(k in artifact for k in ['path','kind','audience','required','status','source']), 'artifact: missing field')
        if ready and artifact['required']:
            require(artifact['status'] == 'present', 'required artifact absent')
    if data['status'] in ['published', 'announced']:
        receipt = data.get('publication', {})
        require(all(receipt.get(k) for k in ['target_commit', 'tag', 'provider', 'steps']), 'publication: missing receipt')
        require(bool(receipt.get('release_url') or receipt.get('receipt')), 'publication: missing success receipt')
    if data['status'] == 'announced':
        require(bool(data.get('communication')), 'announced: missing communication')
    return dict(decision='release', version=data['version'], tag='v'+data['version'], publishable=data['status'] == 'ready')


def main():
    for name in ['v0.5.1.json', 'v0.6.0.json']:
        baseline = json.loads((FIXTURES / name).read_text())
        for path, source in baseline['sources'].items():
            blob = subprocess.check_output(['git', '-C', str(ROOT), 'show', baseline['source_commit']+':'+path])
            require(hashlib.sha256(blob).hexdigest() == source['sha256'], 'historical source digest mismatch: '+path)
        check_contract(ROOT, baseline['contract'])
        for version in ['0.5.1', '0.6.0']:
            fixture = json.loads((FIXTURES / ('release-'+version+'.json')).read_text())
            require(hashlib.sha256((ROOT / fixture['source_path']).read_bytes()).hexdigest() == fixture['source_sha256'],
                    'release fixture provenance mismatch')
            require(release(fixture['package'], baseline['contract']) == fixture['expected'], 'release projection drift')
        fixture = json.loads((FIXTURES / 'review.json').read_text())
        require(review(fixture, baseline['contract']) == fixture['expected'], 'review projection drift')
    print('2 pinned historical contracts, 4 historical release-reader pairs and 2 review-reader pairs passed.')


if __name__ == '__main__':
    main()

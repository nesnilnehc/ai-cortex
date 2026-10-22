#!/usr/bin/env python3
"""Replay roadmap conversations against real local generation; opt in to live eval."""

import argparse
from datetime import datetime, timezone
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / 'skills/define-roadmap/scripts/render-roadmap.py'
CASES = ROOT / 'tests/fixtures/roadmap-conversations/cases.json'
TOPICS = {'roadmap.md', 'iterations.md', 'versions.md', 'milestones.md',
          'roadmap-planning-basis.md', 'roadmap-history.md'}
SCHEMA = {'type': 'object', 'additionalProperties': False,
          'properties': {'action': {'type': 'string', 'enum': ['blank', 'review', 'populate', 'ask']},
                         'review_scope': {'type': 'string', 'enum': ['structure', 'business']},
                         'reason': {'type': 'string'}},
          'required': ['action', 'review_scope', 'reason']}


def business_source(locale='en'):
    if locale == 'zh-CN':
        data = json.loads((ROOT / 'skills/define-roadmap/references/languages/zh-CN/input.json').read_text())
        data['schema_version'] = '1.6'
        data['selection']['layout'] = 'topic-split'
        return data
    data = json.loads((ROOT / 'skills/define-roadmap/references/service-desk/iteration-driven/input.json').read_text())
    data['schema_version'] = '1.6'
    data['views'] += ['phases', 'milestones']
    data['selection'] = dict(scenario='iterations', primary='iterations', layout='topic-split',
                             rationale='User selected one main entry and five topic details',
                             source='../iterations.md#adoption-decision',
                             context=dict(work_mode='iterations', delivery='versioned', audience='Service Desk team',
                                          constraints='Retain the fictional case commitments', source='../sources.md'))
    data['language'] = dict(locale='en', basis='user', source='../sources.md',
                            rationale='English fictional regression case')
    return data


def asset_digest(root):
    names = ['skills/define-roadmap/assets/structure-first/' + name for name in TOPICS]
    names += ['skills/define-roadmap/scripts/roadmap-zh-CN.json',
              'skills/define-roadmap/references/languages/zh-CN/input.json',
              'skills/define-roadmap/references/service-desk/iteration-driven/input.json']
    hashes = {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in sorted(names)}
    return hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()


def snapshot(folder):
    return {path.name: (hashlib.sha256(path.read_bytes()).hexdigest(), path.stat().st_mtime_ns)
            for path in folder.iterdir() if path.is_file()}


def artifact_findings(folder, stage, source):
    """Use the published templates as an independent structural oracle."""
    findings = []
    files = {p.name for p in folder.glob('*.md')} - {'team-notes.md'}
    if stage == 'absent':
        return ['unexpected roadmap files'] if files else []
    if files != TOPICS:
        return ['document roles differ: ' + repr(sorted(files))]
    locale = source.get('language', {}).get('locale', 'en')
    catalog = json.loads((RENDERER.parent / 'roadmap-zh-CN.json').read_text()) if locale == 'zh-CN' else {}
    label = lambda value: catalog.get(value, value)
    status = lambda value: catalog.get('value:' + value, value) if value else '—'
    template_root = RENDERER.parents[1] / 'assets/structure-first'
    all_text = ''
    for name in TOPICS:
        text = (folder / name).read_text()
        all_text += text
        template = (template_root / name).read_text()
        expected_headings = ['## ' + label(h) for h in re.findall(r'^## (.+)$', template, re.M)]
        if re.findall(r'^## .+$', text, re.M) != expected_headings:
            findings.append('changed confirmed headings: ' + name)
        expected_headers = ['| ' + ' | '.join(label(c.strip()) for c in b.splitlines()[0].strip('|').split('|')) + ' |'
                            for b in re.findall(r'(?:^\|.*\|\n)+', template, re.M)]
        actual_tables = re.findall(r'(?:^\|.*\|\n)+', text, re.M)
        if [b.splitlines()[0] for b in actual_tables] != expected_headers:
            findings.append('changed confirmed table fields: ' + name)
        if len(re.findall(r'^# ', text, re.M)) != 1 or re.search(r'<!--|<details>|Instructions:|Fill in', text):
            findings.append('guidance or malformed title: ' + name)
        for target in re.findall(r'\]\(([^)]+)\)', text):
            path, separator, anchor = target.partition('#')
            if path in TOPICS or (not path and separator):
                destination = folder / (path or name)
                headings = {re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-')
                            for h in re.findall(r'^#+ (.+)$', destination.read_text(), re.M)}
                if separator and anchor not in headings:
                    findings.append('broken internal anchor: ' + name)
        # Template navigation targets are required; authority links may be additional.
        for target in re.findall(r'\]\(([^)#]+)\)', template):
            if '](' + target + ')' not in text:
                findings.append('missing template navigation: ' + name + ': ' + target)
        for block in text.strip().split('\n\n'):
            if stage != 'blank':
                continue
            if re.fullmatch(r'#{1,2} [^\n]+', block):
                continue
            if re.fullmatch(r'\*\*[^*\n]+[:：]\*\* \{(?:Pending|待填写)\}', block):
                continue
            if re.fullmatch(r'\[[^]]+\]\([^)]+\)(?: · \[[^]]+\]\([^)]+\))*', block):
                continue
            if block.startswith('|') and len(block.splitlines()) == 2:
                continue
            findings.append('explanatory content or malformed field in blank: ' + name)
        for block in actual_tables:
            rows = block.strip().splitlines()
            widths = {len(re.split(r'(?<!\\)\|', row)) for row in rows}
            if len(widths) != 1 or any(c.strip() != '---' for c in rows[1].strip('|').split('|')):
                findings.append('malformed table: ' + name)
            if stage == 'blank' and len(rows) != 2:
                findings.append('business rows in blank: ' + name)
    if stage == 'blank':
        if any(entry['id'] + ' · ' in all_text for entry in source['entries']):
            findings.append('discarded business facts reintroduced')
        return findings
    main = (folder / 'roadmap.md').read_text()
    archive = (folder / 'roadmap-history.md').read_text()
    cells = lambda line: [html.unescape(c.strip()).replace('\\|', '|') for c in re.split(r'(?<!\\)\|', line.strip('|'))]
    for entry in source['entries']:
        target = archive if entry['execution'] == 'Completed' else main
        matches = [line for line in target.splitlines() if '| [' + entry['id'] + ' · ' in line]
        if len(matches) != 1:
            findings.append('missing or duplicated entry: ' + entry['id'])
            continue
        values = cells(matches[0])
        if entry['execution'] != 'Completed' and (
                [values[0], values[3], values[4], values[5]] != [status(entry['tier']), entry['priority'], entry['approval'], status(entry['execution'])] or
                entry['name'] not in values[1] or entry['outcome'] != values[2] or entry['source'] not in unquote(values[1]) or
                entry['conditions'] + '](' not in values[6] or entry['source'] not in unquote(values[6])):
            findings.append('changed source states: ' + entry['id'])
    versions = (folder / 'versions.md').read_text()
    for version in source['versions']:
        matches = [line for line in versions.splitlines() if line.startswith('| ' + version['id'] + ' ·')]
        expected = [', '.join(version['members']) or label('None'), version['outcome'],
                    status('Unknown') if version['owner'] == 'Unknown' else version['owner'],
                    status('Unknown') if version['window'] == 'Unknown' else version['window']]
        if len(matches) != 1 or cells(matches[0])[1:] != expected:
            findings.append('changed version membership: ' + version['id'])
    milestones = (folder / 'milestones.md').read_text()
    for event in source['milestones']:
        matches = [line for line in milestones.splitlines() if line.startswith('| ' + event['id'] + ' ·')]
        expected = [status(event['category']), ', '.join(event['related']) or label('Global'),
                    status('Unknown') if event['owner'] == 'Unknown' else event['owner'], status(event['state']), event['criterion']]
        if (len(matches) != 1 or cells(matches[0])[1:6] != expected or event['source'] not in unquote(cells(matches[0])[6]) or
                (event.get('evidence') and event['evidence'] not in unquote(cells(matches[0])[7])) or
                (not event.get('evidence') and cells(matches[0])[7] != '—')):
            findings.append('changed event state: ' + event['id'])
    return findings


def workspace_observation(folder, renderer_executed):
    names = sorted(p.name for p in folder.glob('*.md') if p.name != 'team-notes.md')
    if not names:
        stage = 'absent'
    elif set(names) != TOPICS:
        stage = 'incomplete'
    else:
        text = '\n'.join((folder / name).read_text() for name in names)
        stage = 'blank' if '{Pending}' in text or '{待填写}' in text else 'populated'
    return dict(stage=stage, markdown_files=names, renderer_executed=renderer_executed)


def skill_context():
    names = ['skills/define-roadmap/SKILL.md', 'skills/review-roadmap/SKILL.md',
             'skills/orchestrate-roadmap-planning/SKILL.md', 'specs/roadmap-modeling.md',
             'rules/roadmap-quality.md', 'rules/workflow-documentation.md']
    return '\n\n'.join('SOURCE ' + name + '\n' + (ROOT / name).read_text() for name in names)


def live_decision(history, workspace, timeout, context, source_available=True):
    executable = shutil.which('codex')
    if not executable:
        raise ValueError('live eval requires the installed Codex CLI')
    prompt = ('You are the decision adapter for a roadmap skill regression. Follow the supplied skill/spec/rules. '
              'Do not use tools, execute commands, read files or contact any service. Return only the JSON action. '
              'Business source availability: ' + str(source_available) + '. If population is requested but source is unavailable, ask with business scope. '
              'A host executes blank/populate by invoking the production renderer; review inspects without writes; '
              'ask makes no writes. A validated fictional Service Desk source is available for authorized population. '
              'The settled layout is topic-split (one main plus five details). Select structure scope for organization-only '
              'work or explicitly structure-scoped blank-draft review. Select business scope for authorized content work, business-choice options '
              'and content review, even when population is deferred or the draft is empty. '
              'Select review scope from the current request independently of populated files. '
              'Structure confirmation alone is not permission to populate. Continuous authorization for both stages permits population without a new confirmation. '
              'Existing source-backed population preserves the settled layout; options for new priorities or commitments do not approve those changes. '
              'Do not ask again for decisions already made. '
              'Later messages steer earlier scope unless they explicitly replace it. The transcript contains actual '
              'host observations from preceding turns.\n\n' + context + '\n\nCONVERSATION\n' + json.dumps(history))
    schema = workspace / 'response-schema.json'
    response = workspace / 'response.json'
    schema.write_text(json.dumps(SCHEMA))
    response.unlink(missing_ok=True)
    result = subprocess.run([executable, 'exec', '--ignore-user-config', '--ephemeral', '--skip-git-repo-check',
                             '--sandbox', 'read-only', '--json', '--output-schema', str(schema),
                             '--output-last-message', str(response), '-'], input=prompt, text=True,
                            capture_output=True, cwd=workspace, timeout=timeout)
    if result.returncode != 0 or not response.exists():
        raise ValueError('live model failed (exit ' + str(result.returncode) + '): ' + result.stderr[-400:])
    tools, events = [], []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except ValueError as exc:
            raise ValueError('invalid provider trace') from exc
        if not isinstance(event, dict) or (event.get('item') is not None and not isinstance(event['item'], dict)):
            raise ValueError('invalid provider trace')
        events.append(event)
        kind = event.get('item', {}).get('type', '')
        if kind and kind not in {'agent_message', 'reasoning'}:
            tools.append(kind)
    if tools:
        raise ValueError('read-only decision adapter attempted tools: ' + ', '.join(tools))
    if (not any(event.get('type') == 'turn.completed' for event in events) or
            not any(event.get('item', {}).get('type') == 'agent_message' for event in events)):
        raise ValueError('incomplete provider trace')
    return json.loads(response.read_text())


def run_case(case, live=False, timeout=180, context=None):
    if not isinstance(case, dict) or not isinstance(case.get('turns'), list) or not case['turns']:
        raise ValueError('case needs at least one turn')
    for turn in case['turns']:
        expected = turn.get('expected') if isinstance(turn, dict) else None
        if (not isinstance(expected, dict) or set(expected) != {'action', 'scope', 'stage', 'no_write'} or
                not set(expected['action'] if isinstance(expected['action'], list) else [expected['action']]) <= {'blank', 'review', 'populate', 'ask'} or
                expected['scope'] not in {'structure', 'business'} or expected['stage'] not in {'absent', 'blank', 'populated'} or
                type(expected['no_write']) is not bool or
                (expected['no_write'] and not set(expected['action'] if isinstance(expected['action'], list) else [expected['action']]) <= {'review', 'ask'})):
            raise ValueError('turn needs complete, typed independent expected constraints')
    results, history = [], []
    with tempfile.TemporaryDirectory(prefix='cortex-roadmap-eval-') as temp:
        root = Path(temp)
        out = root / 'draft'
        out.mkdir()
        (out / 'team-notes.md').write_text('Unrelated work remains intact.\n')
        locale = case.get('locale', 'en')
        source = business_source(locale)
        input_path = root / 'input.json'
        if case.get('source_available', True):
            input_path.write_text(json.dumps(source))
        input_digest = input_path.read_bytes() if input_path.exists() else None
        for index, turn in enumerate(case['turns']):
            expected = turn.get('expected')
            if not isinstance(expected, dict) or set(expected) != {'action', 'scope', 'stage', 'no_write'}:
                raise ValueError('turn needs complete independent expected constraints')
            before = snapshot(out)
            history.append({'role': 'user', 'content': turn['user']})
            violations = []
            executed = False
            decision = {}
            try:
                decision = live_decision(history, root, timeout, context or skill_context(), case.get('source_available', True)) if live else turn['replay']
                if (not isinstance(decision, dict) or set(decision) != {'action', 'review_scope', 'reason'} or
                        decision['action'] not in {'blank', 'review', 'populate', 'ask'} or
                        decision['review_scope'] not in {'structure', 'business'} or not isinstance(decision['reason'], str)):
                    violations.append('forbidden or malformed action proposal')
                elif decision['action'] not in (expected['action'] if isinstance(expected['action'], list) else [expected['action']]) or decision['review_scope'] != expected['scope']:
                    violations.append('action or review scope violates user turn')
                else:
                    command = None
                    if decision['action'] == 'blank':
                        command = [sys.executable, str(RENDERER), '--blank', '--locale', locale, '--output-dir', str(out), '--overwrite']
                    elif decision['action'] == 'populate':
                        if not input_path.exists():
                            raise ValueError('business source unavailable; population refused')
                        command = [sys.executable, str(RENDERER), str(input_path), '--output-dir', str(out), '--overwrite']
                    if command:
                        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
                        executed = True
                        if result.returncode:
                            violations.append('renderer failed: ' + result.stderr[-400:])
                    violations += artifact_findings(out, expected['stage'], source)
                    if (expected['no_write'] or decision['action'] in {'review', 'ask'}) and snapshot(out) != before:
                        violations.append('read-only turn changed files')
                    if (input_path.read_bytes() if input_path.exists() else None) != input_digest:
                        violations.append('source input changed')
                    if (out / 'team-notes.md').read_text() != 'Unrelated work remains intact.\n':
                        violations.append('unrelated work changed')
            except (ValueError, OSError, subprocess.TimeoutExpired) as exc:
                violations.append(str(exc))
            actual = workspace_observation(out, executed)
            observation = dict(turn=index + 1, user=turn['user'], decision=decision, observation=actual, renderer_executed=executed,
                               violations=violations, passed=not violations)
            results.append(observation)
            history.append({'role': 'assistant', 'content': decision})
            history.append({'role': 'tool', 'content': actual})
    return dict(id=case['id'], covers=case['covers'], passed=all(t['passed'] for t in results), turns=results)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=Path, default=CASES)
    parser.add_argument('--case')
    parser.add_argument('--eval', action='store_true', help='Explicit live-model evaluation; never part of offline CI')
    parser.add_argument('--timeout', type=int, default=180)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    context = None
    report = dict(backend='codex-live' if args.eval else 'scripted-replay', live_model=args.eval, cases=[],
                  started_at=datetime.now(timezone.utc).isoformat(), timeout_seconds=args.timeout)
    if context is not None:
        report['context_sha256'] = hashlib.sha256(context.encode()).hexdigest()
    try:
        cases = json.loads(args.cases.read_text())
        if args.cases.resolve() == CASES.resolve():
            cases += json.loads((ROOT / 'skills/define-roadmap/references/languages/conversations-zh-CN.json').read_text())
        report['cases_sha256'] = hashlib.sha256(json.dumps(cases, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        report['assets_sha256'] = asset_digest(ROOT)
        report['runner_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        report['renderer_sha256'] = hashlib.sha256(RENDERER.read_bytes()).hexdigest()
        if args.eval:
            context = skill_context()
            report['context_sha256'] = hashlib.sha256(context.encode()).hexdigest()
        if args.case:
            cases = [case for case in cases if case['id'] == args.case]
        if not isinstance(cases, list) or not cases:
            raise ValueError('no conversation cases selected')
        for case in cases:
            report['cases'].append(run_case(case, args.eval, args.timeout, context))
        report['pass_rate'] = sum(c['passed'] for c in report['cases']) / len(cases)
        report['passed'] = report['pass_rate'] == 1.0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        report.update(passed=False, pass_rate=0, error=str(exc))
    if args.eval:
        cli = shutil.which('codex')
        report['model'] = 'Codex CLI default; no model override; provider model not exposed by this adapter'
        report['cli'] = subprocess.run([cli, '--version'], capture_output=True, text=True).stdout.strip() if cli else 'missing'
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    sys.exit(main())

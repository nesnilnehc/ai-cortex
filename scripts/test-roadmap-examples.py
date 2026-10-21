#!/usr/bin/env python3
"""Check the Service Desk example against its source facts and generated views."""

import copy
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / 'skills/define-roadmap/references/service-desk'
spec = importlib.util.spec_from_file_location('roadmap_renderer', ROOT / 'skills/define-roadmap/scripts/render-roadmap.py')
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)
PHASES = {'initial': 'Initial', 'adjusted': 'Adjusted', 'after-delivery': 'After delivery'}


def rows(path, heading):
    section = path.read_text().split(f'## {heading}\n', 1)[1].split('\n## ', 1)[0]
    table = [line for line in section.splitlines() if line.startswith('|')]
    cells = [[cell.strip() for cell in line.strip('|').split('|')] for line in table]
    return [dict(zip(cells[0], values)) for values in cells[2:]]


def phase_findings(data, phase):
    """Compare the rendered facts with independently readable source tables."""
    findings = []
    records = {row['ID']: row for row in rows(CASE / 'sources.md', 'Work items')}
    states = {row['ID']: row for row in rows(CASE / 'sources.md', 'Execution by stage')}
    if {entry['id'] for entry in data['entries']} != set(records):
        findings.append('entry scope')
    for entry in data['entries']:
        original = records[entry['id']]
        if (entry['name'], entry['priority']) != (original['Name'], original['Priority']):
            findings.append('priority or identity')
        if entry['execution'] != states[entry['id']][PHASES[phase]]:
            findings.append('execution')
    expected = [row for row in rows(CASE / 'sources.md', 'Delivery windows') if row['Stage'] == phase]
    versions = {v['id']: v for v in data['versions']}
    spans = {i['ref']: i for i in data['schedule']['items']}
    if set(versions) != {row['Version'] for row in expected}:
        findings.append('version scope')
    for row in expected:
        ref = row['Version']
        if versions.get(ref, {}).get('members') != row['Members'].split(', '):
            findings.append('membership')
        span = spans.get(ref, {})
        if (span.get('start'), span.get('end'), span.get('basis')) != (int(row['Start']), int(row['End']), row['Basis']):
            findings.append('timing')
    membership = {member: v['id'] for v in data['versions'] for member in v['members']}
    for ref, source in records.items():
        if source['Depends on'] == 'None' or ref not in membership:
            continue
        before = membership.get(source['Depends on'])
        after = membership[ref]
        if before and before != after and before not in spans.get(after, {}).get('depends_on', []):
            findings.append('dependency')
    return findings


def event_findings(data, stage):
    findings = []
    spans = {i['ref']: i for i in data['schedule']['items']}
    phases = {p['id']: p for p in data['phases']}
    events = {m['id']: m for m in data['milestones']}
    expected_phases = [r for r in rows(CASE / 'sources.md', 'Phase windows') if r['Stage'] == stage]
    expected_events = [r for r in rows(CASE / 'sources.md', 'Event observations') if r['Stage'] == stage]
    if set(phases) != {r['ID'] for r in expected_phases} or set(events) != {r['ID'] for r in expected_events}:
        findings.append('object scope')
    for row in expected_phases:
        phase, span = phases.get(row['ID'], {}), spans.get(row['ID'], {})
        if (phase.get('scope'), span.get('start'), span.get('end'), span.get('basis')) != (
                row['Scope'].split(', '), int(row['Start']), int(row['End']), row['Basis']):
            findings.append('phase')
    for row in expected_events:
        event, point = events.get(row['ID'], {}), spans.get(row['ID'], {})
        expected_related = [] if row['Related'] == 'Global' else row['Related'].split(', ')
        if (event.get('related'), event.get('state'), event.get('evidence')) != (
                expected_related, row['State'], None if row['Evidence'] == 'None' else row['Evidence']):
            findings.append('event evidence or relation')
        if (point.get('start'), point.get('end'), point.get('basis')) != (
                int(row['Week']), int(row['Week']), row['Basis']):
            findings.append('event timing')
    return findings


SCENARIOS = ROOT / 'skills/define-roadmap/references/scenarios'


def scenario_findings(data, folder):
    findings = []
    source = folder / 'sources.md'
    context = {r['Field']: r['Value'] for r in rows(source, 'Context')}
    selection = {r['Field']: r['Value'] for r in rows(folder / 'selection.md', 'Decision')}
    if any(data['selection']['context'].get(k) != value for k, value in context.items()):
        findings.append('context')
    if any(str(data['selection'].get(k)) != selection[k] for k in ('scenario', 'primary', 'layout', 'rationale')):
        findings.append('selection')
    if ', '.join(data['views']) != selection['views']:
        findings.append('views')
    expected = {r['ID']: r for r in rows(source, 'Work items')}
    if set(expected) != {e['id'] for e in data['entries']}:
        findings.append('entry scope')
    for entry in data['entries']:
        for field in ('name', 'outcome', 'tier', 'priority', 'approval', 'execution', 'conditions'):
            if entry[field] != expected[entry['id']][field.title()]:
                findings.append('entry facts')
    findings += scenario_delivery_findings(data, source)
    return findings


def scenario_delivery_findings(data, source):
    findings = []
    for kind, fields in [('versions', ['name', 'members', 'outcome', 'owner', 'window']),
                         ('iterations', ['name', 'goal', 'members', 'owner']),
                         ('phases', ['name', 'scope', 'owner', 'exit_condition']),
                         ('milestones', ['name', 'related', 'owner', 'criterion', 'category', 'state', 'evidence'])]:
        if kind not in data:
            continue
        expected = {r['ID']: r for r in rows(source, kind.capitalize())}
        if set(expected) != {r['id'] for r in data[kind]}:
            findings.append(kind)
        for record in data[kind]:
            for field in fields:
                value = record.get(field)
                value = ', '.join(value) if isinstance(value, list) else 'None' if value is None else str(value)
                if value != expected[record['id']][field.replace('_', ' ').capitalize()]:
                    findings.append(kind)
    if 'schedule' in data:
        expected = {r['ID']: r for r in rows(source, 'Timing')}
        if set(expected) != {item['ref'] for item in data['schedule']['items']}:
            findings.append('timing')
        for item in data['schedule']['items']:
            row = expected[item['ref']]
            if (item['start'], item['end'], item['basis'], ', '.join(item['depends_on']) or 'None') != (
                    int(row['Start']), int(row['End']), row['Basis'], row['Depends on']):
                findings.append('timing')
    if 'flow' in data:
        for row in rows(source, 'Workflow'):
            if data['flow'][row['Field']] != row['Value']:
                findings.append('flow')
    return findings


class ExampleTests(unittest.TestCase):
    def test_four_scenarios_match_sources_choices_and_reproduce_all_outputs(self):
        for folder in sorted(p for p in SCENARIOS.iterdir() if p.is_dir()):
            with self.subTest(scenario=folder.name):
                data = renderer.validate(json.loads((folder / 'input.json').read_text()))
                self.assertEqual(scenario_findings(data, folder), [])
                output = renderer.documents(data)
                for name, content in output.items():
                    self.assertEqual(content, (folder / name).read_text())
                self.assertEqual(set(output), {p.name for p in folder.glob('roadmap.*')} |
                                 {p.name for p in folder.glob('roadmap-*.md')})
                for name, content in output.items():
                    if not name.endswith('.md'):
                        continue
                    for target in re.findall(r'\]\(([^)]+)\)', content):
                        if '://' in target:
                            continue
                        path, _, anchor = target.partition('#')
                        resolved = folder / (path or name)
                        self.assertTrue(resolved.is_file(), target)
                        if anchor:
                            headings = re.findall(r'^#+ (.+)$', resolved.read_text(), re.M)
                            self.assertIn(anchor, {h.lower().replace(' ', '-') for h in headings})

    def test_scenario_checks_detect_context_choice_scope_and_evidence_drift(self):
        mutations = [('iteration-product', 'context', lambda d: d['selection']['context'].update(audience='Other')),
                     ('iteration-product', 'selection', lambda d: d['selection'].update(primary='versions')),
                     ('iteration-product', 'views', lambda d: d['views'].remove('milestones')),
                     ('iteration-product', 'iterations', lambda d: d['iterations'][0].update(members=['R2'])),
                     ('staged-delivery', 'phases', lambda d: d['phases'][0].update(exit_condition='Other')),
                     ('staged-delivery', 'phases', lambda d: d['phases'].pop()),
                     ('staged-delivery', 'timing', lambda d: d['schedule']['items'][0].update(end=9)),
                     ('discovery-pilot', 'milestones', lambda d: d['milestones'][0].update(state='reached')),
                     ('continuous-flow', 'flow', lambda d: d['flow'].update(policy='Unlimited'))]
        for slug, expected, mutate in mutations:
            folder = SCENARIOS / slug
            data = json.loads((folder / 'input.json').read_text())
            mutate(data)
            self.assertIn(expected, scenario_findings(data, folder))

    def test_four_scenarios_use_retained_choices_through_real_cli(self):
        script = ROOT / 'skills/define-roadmap/scripts/render-roadmap.py'
        for folder in sorted(p for p in SCENARIOS.iterdir() if p.is_dir()):
            with self.subTest(scenario=folder.name), tempfile.TemporaryDirectory() as tmp:
                source = folder / 'input.json'
                original = source.read_bytes()
                result = subprocess.run([sys.executable, str(script), str(source), '--recommend'],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                decision = json.loads(result.stdout)
                data = json.loads(original)
                self.assertEqual(decision['status'], 'retained')
                self.assertEqual(decision['views'], data['views'])
                self.assertEqual(decision['layout'], data['selection']['layout'])
                result = subprocess.run([sys.executable, str(script), str(source), '--output-dir', tmp],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                for name, content in renderer.documents(data).items():
                    self.assertEqual((Path(tmp) / name).read_text(), content)
                self.assertEqual(source.read_bytes(), original)

    def test_iteration_layouts_reproduce_one_source_input(self):
        data = renderer.validate(json.loads((CASE / 'iteration-driven/input.json').read_text()))
        for layout, folder in [('single', 'iteration-driven'), ('split', 'iteration-driven-split')]:
            output = renderer.documents(data, layout)
            for name, content in output.items():
                self.assertEqual(content, (CASE / folder / name).read_text())
            for name, content in output.items():
                if not name.endswith('.md'):
                    continue
                for target in re.findall(r'\]\(([^)]+)\)', content):
                    if '://' in target:
                        continue
                    path, _, anchor = target.partition('#')
                    resolved = CASE / folder / (path or name)
                    self.assertTrue(resolved.is_file(), str(resolved))
                    if anchor:
                        headings = re.findall(r'^#+ (.+)$', resolved.read_text(), re.M)
                        anchors = {re.sub(r'[^a-z0-9 -]', '', h.lower()).replace(' ', '-') for h in headings}
                        self.assertIn(anchor, anchors)
        self.assertEqual((CASE / 'iteration-driven/roadmap.svg').read_bytes(),
                         (CASE / 'iteration-driven-split/roadmap.svg').read_bytes())
        self.assertFalse((CASE / 'iteration-driven-split/input.json').exists())

    def test_iterations_match_independent_allocations_and_preserve_adjusted_plan(self):
        data = json.loads((CASE / 'iteration-driven/input.json').read_text())
        source = {row['ID']: row for row in rows(CASE / 'iterations.md', 'Cadence and allocation')}
        schedule = {item['ref']: item for item in data['schedule']['items']}
        self.assertEqual(set(source), {i['id'] for i in data['iterations']})
        for iteration in data['iterations']:
            original = source[iteration['id']]
            for field in ('name', 'goal', 'owner'):
                self.assertEqual(iteration[field], original[field.title()])
            self.assertEqual(iteration['members'], original['Members'].split(', '))
            span = schedule[iteration['id']]
            self.assertEqual((span['start'], span['end'], span['basis']),
                             (int(original['Start']), int(original['End']), original['Basis']))
        adjusted = json.loads((CASE / 'adjusted/input.json').read_text())
        for key in ('entries', 'versions', 'phases', 'milestones'):
            self.assertEqual(data[key], adjusted[key])
        self.assertEqual([i for i in data['schedule']['items'] if i['ref'] not in source],
                         adjusted['schedule']['items'])
        self.assertEqual(data['revisions'][1:], adjusted['revisions'])
        decision = rows(CASE / 'iterations.md', 'Adoption decision')[0]
        for field in ('id', 'date', 'change', 'reason', 'impact'):
            self.assertEqual(data['revisions'][0][field], decision['ID' if field == 'id' else field.title()])
        self.assertEqual(renderer.iteration_versions(data, data['iterations'][1]), 'V1, V2')

    def test_all_phases_match_sources_and_reproduce_outputs(self):
        for phase in PHASES:
            with self.subTest(phase=phase):
                folder = CASE / phase
                data = renderer.validate(json.loads((folder / 'input.json').read_text()))
                self.assertEqual(phase_findings(data, phase), [])
                self.assertEqual(event_findings(data, phase), [])
                self.assertEqual(renderer.markdown(data), (folder / 'roadmap.md').read_text())
                self.assertEqual(renderer.svg(data), (folder / 'roadmap.svg').read_text())
                for entry in renderer.records(data):
                    if 'source' not in entry:
                        continue
                    source, anchor = entry['source'].split('#')
                    self.assertTrue((folder / source).is_file())
                    self.assertIn(f'## {anchor.upper()}\n', (folder / source).read_text())

    def test_revision_history_matches_sources_and_survives_later_snapshots(self):
        """Covers: roadmap-capabilities#AC14; decisions survive scope/event changes."""
        register = {row['ID']: row for row in rows(CASE / 'change-record.md', 'Revision register')}
        expected = {'initial': [], 'adjusted': ['REV1'], 'after-delivery': ['REV2', 'REV1']}
        for stage, ids in expected.items():
            data = json.loads((CASE / stage / 'input.json').read_text())
            self.assertEqual([r['id'] for r in data['revisions']], ids)
            for revision in data['revisions']:
                original = register[revision['id']]
                for field in ('date', 'change', 'reason', 'impact'):
                    self.assertEqual(revision[field], original[field.title()])
                path, anchor = revision['source'].split('#')
                source_path, source_anchor = re.fullmatch(r'\[Details\]\((.*?)\)', original['Source'])[1].split('#')
                resolved = CASE / (source_path or 'change-record.md')
                self.assertEqual(resolved.resolve(), (CASE / stage / path).resolve())
                self.assertEqual(source_anchor, anchor)
                self.assertIn('## ' + anchor.replace('-', ' ').capitalize(),
                              (CASE / stage / path).read_text())
        adjusted = json.loads((CASE / 'adjusted/input.json').read_text())
        delivered = json.loads((CASE / 'after-delivery/input.json').read_text())
        self.assertEqual(adjusted['revisions'][0], delivered['revisions'][1])

    def test_consistency_checks_detect_each_kind_of_drift(self):
        original = json.loads((CASE / 'initial/input.json').read_text())
        mutations = [
            ('priority or identity', lambda d: d['entries'][0].update(priority='P3')),
            ('execution', lambda d: d['entries'][0].update(execution='Completed')),
            ('membership', lambda d: d['versions'][0].update(members=[])),
            ('timing', lambda d: d['schedule']['items'][0].update(end=10)),
            ('dependency', lambda d: d['schedule']['items'][1].update(depends_on=[])),
        ]
        for expected, mutate in mutations:
            with self.subTest(expected=expected):
                data = copy.deepcopy(original)
                mutate(data)
                self.assertIn(expected, phase_findings(data, 'initial'))

    def test_phase_and_event_drift_is_detected(self):
        mutations = [
            ('phase', lambda d: d['phases'][0].update(scope=['BUG1'])),
            ('event evidence or relation', lambda d: d['milestones'][0].update(state='reached')),
            ('event evidence or relation', lambda d: d['milestones'][-1].update(related=['V2'])),
            ('event timing', lambda d: d['schedule']['items'][-1].update(start=4, end=4))]
        for expected, mutate in mutations:
            data = json.loads((CASE / 'initial/input.json').read_text())
            mutate(data)
            self.assertIn(expected, event_findings(data, 'initial'))

    def test_priority_and_dependency_deliverables_agree_with_sources(self):
        source = rows(CASE / 'sources.md', 'Work items')
        priorities = {r['ID']: r for r in rows(CASE / 'priority-decisions.md', 'Decisions')}
        dependencies = {r['ID']: r for r in rows(CASE / 'dependencies.md', 'Dependency register')}
        for record in source:
            self.assertEqual(priorities[record['ID']]['Final'], record['Priority'])
            self.assertEqual(dependencies[record['ID']]['Depends on'], record['Depends on'])
        graph = (CASE / 'dependencies.md').read_text()
        actual_edges = set(re.findall(r'^\s*(BUG1|R\d)(?:\[.*?\])? --> (R\d)', graph, re.M))
        expected_edges = {(r['Depends on'], r['ID']) for r in source if r['Depends on'] != 'None'}
        self.assertEqual(actual_edges, expected_edges)

    def test_guide_illustration_matches_the_initial_case(self):
        self.assertEqual((CASE / 'initial/roadmap.svg').read_text(),
                         (ROOT / 'docs/images/roadmap-schedule.svg').read_text())
        alias = ROOT / 'skills/define-roadmap/assets/roadmap-input-example.json'
        self.assertEqual(alias.resolve(), (CASE / 'initial/input.json').resolve())

    def test_placement_is_preserved_during_version_changes(self):
        placement = {r['ID']: r for r in rows(CASE / 'placement-decisions.md', 'Confirmed placement')}
        for phase in PHASES:
            data = json.loads((CASE / phase / 'input.json').read_text())
            self.assertEqual(set(placement), {e['id'] for e in data['entries']})
            for entry in data['entries']:
                self.assertEqual(entry['tier'], placement[entry['id']]['Confirmed tier'])
                self.assertEqual(entry['priority'], placement[entry['id']]['Priority'])

    def test_review_catches_the_intentionally_bad_plan(self):
        data = json.loads((CASE / 'problematic/input.json').read_text())
        self.assertIn('execution', phase_findings(data, 'initial'))
        with self.assertRaisesRegex(ValueError, 'overlap'):
            renderer.validate(data)
        report = (CASE / 'review-findings.md').read_text()
        for title in ('Unsupported completion', 'Dependency timing conflict'):
            self.assertIn(title, report)
        self.assertIn('cannot evaluate', report)
        self.assertNotIn('Full pass', report)

    def test_archive_preserves_actual_scope_and_unfinished_work(self):
        data = json.loads((CASE / 'after-delivery/input.json').read_text())
        archive = rows(CASE / 'version-archive.md', 'Disposition')
        entries = {e['id']: e for e in data['entries']}
        members = {member: v['id'] for v in data['versions'] for member in v['members']}
        initial = json.loads((CASE / 'initial/input.json').read_text())
        original_members = {member: v['id'] for v in initial['versions'] for member in v['members']}
        self.assertEqual({row['ID'] for row in archive}, set(entries))
        for row in archive:
            self.assertEqual(row['Execution'], entries[row['ID']]['execution'])
            self.assertEqual(row['Current version'], members.get(row['ID'], 'Unassigned'))
            self.assertEqual(row['Originally planned version'], original_members.get(row['ID'], 'Unassigned'))
        change = (CASE / 'change-record.md').read_text()
        self.assertIn('R1: V1 → V2', change)
        self.assertIn('R2: V2 → V3', change)
        original_end = next(i['end'] for i in initial['schedule']['items'] if i['ref'] == original_members['R2'])
        current_end = next(i['end'] for i in data['schedule']['items'] if i['ref'] == members['R2'])
        self.assertIn(f'{current_end - original_end} weeks', change)
        self.assertIn('hard deadline', change)


if __name__ == '__main__':
    unittest.main()

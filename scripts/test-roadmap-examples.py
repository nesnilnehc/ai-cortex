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
ADOPTION = ROOT / 'skills/define-roadmap/references/existing-project'


def alignment_findings(before, after):
    """Check protected facts in the manually aligned teaching plan, not agent behavior."""
    def records(content):
        lines = [line for line in content.splitlines() if line.startswith('|')]
        cells = [[cell.strip() for cell in line.strip('|').split('|')] for line in lines]
        return [dict(zip(cells[0], values)) for values in cells[2:]] if cells else []

    def anchors(content):
        explicit = set(re.findall(r'<a id="([^"]+)"', content))
        return explicit | {h.lower().replace(' ', '-')
                           for h in re.findall(r'^#+ (.+)$', content, re.M)}

    findings = []
    original, proposed = records(before), records(after)
    if [r.get('ID') for r in original] != [r.get('ID') for r in proposed]:
        findings.append('order/scope')
    by_id = {r['ID']: r for r in proposed}
    for row in original:
        if any(by_id.get(row['ID'], {}).get(key) != value for key, value in row.items()):
            findings.append('decision')
    for prefix in ('Delivery:', 'Closure:'):
        known = [line for line in before.splitlines() if line.startswith(prefix)]
        if any(line not in after.splitlines() for line in known):
            findings.append('delivery')
    if not set(re.findall(r'\]\(([^)]+)\)', before)) <= set(re.findall(r'\]\(([^)]+)\)', after)):
        findings.append('source link')
    if not anchors(before) <= anchors(after):
        findings.append('anchor')
    return findings


class AlignmentExampleTests(unittest.TestCase):
    def test_alignment_preserves_existing_decisions_links_and_unknown_execution(self):
        """Covers: existing-project alignment; independent before/after oracle."""
        before = (ADOPTION / 'before/plan.md').read_text()
        after = (ADOPTION / 'after/plan.md').read_text()
        self.assertEqual(alignment_findings(before, after), [])
        self.assertIn('| R1 | Request lookup | Retrieve an existing service request | P0 | Next |', after)
        self.assertIn('| R2 | Interface repair | Restore the interface needed for retrieval | P1 | Now | Draft | — |', after)
        self.assertLess(after.index('R2 execution remains unverified'), after.index('## Priority arrangement'))
        self.assertIn('First alignment: 2026-10-21', after)
        self.assertIn('Earlier history is unknown', after)
        self.assertFalse((ADOPTION / 'after/roadmap.md').exists())

    def test_alignment_check_detects_business_and_link_drift(self):
        """Covers: existing-project alignment; a clean snapshot alone proves no guard."""
        before = (ADOPTION / 'before/plan.md').read_text()
        after = (ADOPTION / 'after/plan.md').read_text()
        def swap_rows(content):
            lines = content.splitlines()
            first, second = [i for i, line in enumerate(lines) if line.startswith(('| R1 |', '| R2 |'))]
            lines[first], lines[second] = lines[second], lines[first]
            return '\n'.join(lines) + '\n'

        mutations = [
            ('decision', lambda s: s.replace('| P0 | Next |', '| P0 | Now |')),
            ('decision', lambda s: s.replace('| P1 | Now | Draft | — |', '| P1 | Now | Draft | Not started |')),
            ('delivery', lambda s: s.replace('committed 2026-12-15', 'target 2027-01-15')),
            ('source link', lambda s: s.replace('../sources.md#r1', '../sources.md#renamed')),
            ('anchor', lambda s: s.replace('<a id="work"></a>', '')),
            ('order/scope', lambda s: s.replace('| R1 | Request lookup |', '| R9 | Request lookup |')),
            ('order/scope', swap_rows),
        ]
        for expected, mutate in mutations:
            with self.subTest(expected=expected):
                changed = mutate(after)
                self.assertNotEqual(changed, after)
                self.assertIn(expected, alignment_findings(before, changed))

    def test_alignment_repair_does_not_require_generating_missing_planning_authorities(self):
        """Covers: existing-project alignment; optional generator still needs complete facts."""
        for name in ('strategic-goals.md', 'priority-policy.md', 'roadmap.md'):
            self.assertFalse((ADOPTION / 'after' / name).exists())
        after = (ADOPTION / 'after/plan.md').read_text()
        self.assertIn('Priority policy and strategic-goal evidence remain unavailable', after)
        self.assertIn('no reconstructed decision', after)
        self.assertEqual(alignment_findings(after, after), [])


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



class LanguageExampleTests(unittest.TestCase):
    BASE = ROOT / 'skills/define-roadmap/references/languages'

    def editions(self):
        return [json.loads((self.BASE / locale / 'input.json').read_text())
                for locale in ['en', 'zh-CN']]

    def test_paired_editions_reproduce_all_outputs_without_input_changes(self):
        """Covers: roadmap-capabilities#AC26."""
        for data in self.editions():
            before = copy.deepcopy(data)
            folder = self.BASE / data['language']['locale']
            for name, content in renderer.documents(renderer.validate(data)).items():
                self.assertEqual(content, (folder / name).read_text(), name)
            self.assertEqual(data, before)

    def test_cli_reproduces_paired_editions_when_run_from_another_directory(self):
        """Covers: roadmap-capabilities#AC26; exercise the actual entry point and local catalog."""
        script = ROOT / 'skills/define-roadmap/scripts/render-roadmap.py'
        for locale in ['en', 'zh-CN']:
            with self.subTest(locale=locale), tempfile.TemporaryDirectory() as tmp:
                folder = self.BASE / locale
                out = Path(tmp) / 'generated'

                result = subprocess.run([sys.executable, str(script), str(folder / 'input.json'),
                                         '--output-dir', str(out)], cwd=tmp, capture_output=True, text=True)

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual({path.name for path in out.iterdir()},
                                 {'roadmap.md', 'roadmap-delivery.md', 'roadmap-history.md',
                                  'roadmap.svg', 'roadmap.mmd'})
                for path in out.iterdir():
                    self.assertEqual(path.read_text(), (folder / path.name).read_text(), path.name)

    def test_language_editions_preserve_source_planning_facts(self):
        """Covers: roadmap-capabilities#AC26."""
        english, chinese = self.editions()
        self.assertEqual(english['views'], chinese['views'])
        self.assertEqual(english['schedule']['items'], chinese['schedule']['items'])
        for field, keys in [('entries', ['id', 'tier', 'priority', 'execution', 'source']),
                            ('versions', ['id', 'members']),
                            ('iterations', ['id', 'members', 'source', 'board']),
                            ('phases', ['id', 'scope', 'source']),
                            ('milestones', ['id', 'related', 'category', 'state', 'evidence', 'source']),
                            ('revisions', ['id', 'date', 'source'])]:
            project = lambda data: [{key: record[key] for key in keys} for record in data[field]]
            self.assertEqual(project(english), project(chinese), field)
        source = (self.BASE / 'sources.md').read_text()
        self.assertIn('2026-11-02 to 2026-11-16', source)
        self.assertIn('state planned, evidence absent', source)
        self.assertIn('In progress / 进行中', source)
        self.assertIn('Search unallocated → I1', source)
        self.assertEqual(english['entries'][0]['execution'], 'In progress')
        self.assertEqual(english['milestones'][0]['state'], 'planned')

    def test_all_editions_link_the_language_decision_and_localized_views(self):
        """Covers: roadmap-capabilities#AC26."""
        for locale, heading, status in [('en', '## Priority arrangement', 'In progress'),
                                        ('zh-CN', '## 优先安排', '进行中')]:
            folder = self.BASE / locale
            main = (folder / 'roadmap.md').read_text()
            self.assertIn(heading, main)
            self.assertIn(status, main)
            self.assertIn('../sources.md#language', main)
            self.assertIn('roadmap-delivery.md', main)
            self.assertIn('roadmap-history.md', main)
            detail = (folder / 'roadmap-delivery.md').read_text()
            self.assertIn('roadmap.svg', detail)
            self.assertIn((folder / 'roadmap.mmd').read_text().strip(), detail)
            self.assertIn('roadmap.md', detail)
        zh = (self.BASE / 'zh-CN/roadmap-delivery.md').read_text()
        for english in ['## Delivery plan', 'Awaiting acceptance', 'target ·', 'planned', 'Approval']:
            self.assertNotIn(english, zh)


class StructureFirstExamples(unittest.TestCase):
    """Pin the empty-to-populated handoff, not an agent's unobserved behavior."""

    NAMES = {'roadmap.md', 'iterations.md', 'versions.md', 'milestones.md',
             'roadmap-planning-basis.md', 'roadmap-history.md'}
    EMPTY = ROOT / 'skills/define-roadmap/assets/structure-first'
    FILLED = CASE / 'topic-split'

    def test_blank_structure_has_six_clean_linked_documents_without_sample_facts(self):
        self.assertEqual({p.name for p in self.EMPTY.glob('*.md')}, self.NAMES)
        for name in self.NAMES:
            text = (self.EMPTY / name).read_text()
            self.assertEqual(len(re.findall(r'^# ', text, re.M)), 1, name)
            for block in text.strip().split('\n\n'):
                self.assertTrue(block.startswith(('#', '|', '**', '[')), (name, block))
            for line in text.splitlines():
                if line.startswith('**'):
                    self.assertRegex(line, r'^\*\*[^*]+:\*\* \{Pending\}$')
            for table in re.findall(r'(?:^\|.*\|\n)+', text, re.M):
                self.assertEqual(len(table.strip().splitlines()), 2, name)
            for target in re.findall(r'\]\(([^)]+)\)', text):
                self.assertIn(target.split('#')[0], self.NAMES, (name, target))
            self.assertNotRegex(text, r'BUG1|R1|V1|M1|I1|<!--|<details>|Fill in|Instructions:')

    def test_populated_pair_preserves_selected_headings_and_all_source_members(self):
        self.assertEqual({p.name for p in self.FILLED.glob('*.md')}, self.NAMES)
        for name in self.NAMES:
            empty = (self.EMPTY / name).read_text()
            filled = (self.FILLED / name).read_text()
            self.assertEqual(re.findall(r'^## .+$', empty, re.M),
                             re.findall(r'^## .+$', filled, re.M), name)
            self.assertNotIn('{Pending}', filled)
            if name != 'roadmap.md':
                self.assertIn('[Main roadmap](roadmap.md)', filled)
        data = json.loads((CASE / 'iteration-driven/input.json').read_text())
        main_rows = rows(self.FILLED / 'roadmap.md', 'Priority arrangement')
        self.assertEqual(len(main_rows), len(data['entries']))
        for entry, row in zip(data['entries'], main_rows):
            self.assertEqual(row['Tier'], entry['tier'])
            self.assertEqual(row['Priority'], entry['priority'])
            self.assertEqual(row['Approval status'], entry['approval'])
            self.assertEqual(row['Execution status'], entry['execution'])
            self.assertIn(entry['id'] + ' · ' + entry['name'], row['Requirement / defect'])
        detail = (self.FILLED / 'iterations.md').read_text()
        for iteration in data['iterations']:
            self.assertIn(iteration['id'], detail)
        for version in data['versions']:
            line = next(line for line in (self.FILLED / 'versions.md').read_text().splitlines()
                        if line.startswith('| ' + version['id'] + ' ·'))
            self.assertIn(', '.join(version['members']), line)
        for event in data['milestones']:
            line = next(line for line in (self.FILLED / 'milestones.md').read_text().splitlines()
                        if line.startswith('| ' + event['id'] + ' ·'))
            self.assertIn(event['state'], line)

    def test_topic_fixture_is_reproducible_by_the_production_renderer(self):
        data = json.loads((self.FILLED / 'input.json').read_text())
        outputs = renderer.documents(renderer.validate(data))
        for name, generated in outputs.items():
            self.assertEqual((self.FILLED / name).read_text(), generated, name)

    def test_one_reader_entry_reaches_every_detail_and_the_details_link_back(self):
        for folder in [self.EMPTY, self.FILLED]:
            main = (folder / 'roadmap.md').read_text()
            main_targets = {target.split('#')[0] for target in re.findall(r'\]\(([^)]+)\)', main)}
            self.assertTrue(self.NAMES - {'roadmap.md'} <= main_targets)
            for name in self.NAMES - {'roadmap.md'}:
                self.assertIn('[Main roadmap](roadmap.md)', (folder / name).read_text())
        populated = (self.FILLED / 'roadmap.md').read_text()
        for claim in ['Fix duplicate submission before search', 'Restore sandbox by W3',
                      'I1', 'I2', 'I3', 'V1', 'V2', 'V3', 'M1', 'M2', 'M3']:
            self.assertIn(claim, populated)


if __name__ == '__main__':
    unittest.main()

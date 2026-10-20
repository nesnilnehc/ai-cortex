#!/usr/bin/env python3
"""Behavioral checks for the bundled offline roadmap renderer."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/define-roadmap/scripts/render-roadmap.py'
spec = importlib.util.spec_from_file_location('roadmap_renderer', SCRIPT)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


def sample(mode='weeks'):
    return {
        'schema_version': '1.0', 'project': 'Desk <研发> & support',
        'updated': '2026-10-20', 'closure': 'Acceptance passed',
        'direction': 'Make request handling dependable', 'ordering': 'Search enables export',
        'priority_policy': 'Customer blockers first',
        'views': ['requirements', 'versions', 'schedule'],
        'entries': [dict(id='R1', name='Search <客户> & export | results',
                         source='requirements/search.md#acceptance', outcome='Find records',
                         priority='P0', tier='Now', approval='Approved',
                         execution='In progress', conditions='Review results')],
        'versions': [dict(id='V1', name='First delivery', members=['R1'],
                          outcome='Search works', owner='Unknown', window='Unknown')],
        'schedule': dict(mode=mode, origin='W1: start date unknown' if mode == 'weeks' else 'ISO calendar dates',
                         calendar='calendar-days', items=[dict(ref='V1', kind='span', basis='target',
                         start=1 if mode == 'weeks' else '2026-11-02',
                         end=3 if mode == 'weeks' else '2026-11-16', depends_on=[])])
    }


def event_sample(mode='weeks'):
    data = sample(mode)
    start, end = (1, 3) if mode == 'weeks' else ('2026-11-02', '2026-11-16')
    data['schema_version'] = '1.1'
    data['phases'] = [dict(id='PH1', name='Validation phase', source='phase.md',
                          owner='QA', scope=['V1'], exit_condition='Acceptance approved')]
    data['milestones'] = [dict(id='M1', name='Acceptance approval', source='approval.md',
                              owner='Reviewer', related=['PH1', 'V1'], category='approval',
                              criterion='Reviewer signs acceptance', state='planned', evidence=None)]
    data['schedule']['items'] += [
        dict(ref='PH1', kind='span', basis='target', start=start, end=end, depends_on=[]),
        dict(ref='M1', kind='milestone', basis='target', start=end, end=end, depends_on=['PH1'])]
    return data


class RendererTests(unittest.TestCase):
    def test_independent_phase_and_event_share_version_context(self):
        data = renderer.validate(event_sample())
        result = renderer.markdown(data)
        self.assertIn('## Phases', result)
        self.assertIn('## Milestones', result)
        self.assertIn('Reviewer signs acceptance', result)
        self.assertIn('planned', renderer.svg(data))
        self.assertEqual(len(ET.fromstring(renderer.svg(data)).findall(
            './/{http://www.w3.org/2000/svg}polygon[@class="milestone"]')), 1)

    def test_event_state_requires_evidence_and_actual_requires_reached(self):
        for changes, message in [({'state': 'reached'}, 'evidence'),
                                 ({'evidence': 'javascript:bad'}, 'evidence')]:
            data = event_sample()
            data['milestones'][0].update(changes)
            with self.assertRaisesRegex(ValueError, message):
                renderer.validate(data)
        data = event_sample()
        data['schedule']['items'][-1]['basis'] = 'actual'
        with self.assertRaisesRegex(ValueError, 'reached'):
            renderer.validate(data)
        data['milestones'][0].update(state='reached', evidence='approval.md#signed')
        renderer.validate(data)

    def test_unknown_event_is_not_drawn_and_global_event_is_valid(self):
        data = event_sample()
        data['milestones'][0]['related'] = []
        data['schedule']['items'][-1].update(start=None, end=None)
        result = renderer.svg(renderer.validate(data))
        self.assertIn('Unscheduled', result)
        self.assertNotIn('<polygon', result)

    def test_event_relationships_and_schema_boundaries(self):
        mutations = [
            (lambda d: d.update(schema_version='1.0'), '1.1'),
            (lambda d: d['phases'][0].update(scope=['PH1']), 'scope'),
            (lambda d: d['milestones'][0].update(related=['missing']), 'related'),
            (lambda d: d['schedule']['items'][-1].update(kind='span', end=4), 'kind'),
            (lambda d: d['schedule']['items'][0].update(kind='milestone', end=1), 'kind'),
            (lambda d: d['milestones'][0].update(id='V1'), 'duplicate')]
        for mutate, message in mutations:
            data = event_sample()
            mutate(data)
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                renderer.validate(data)

    def test_dated_independent_events_render_without_inferred_dates(self):
        data = event_sample()
        data['schedule'].update(mode='dates', origin='ISO calendar dates')
        for item in data['schedule']['items']:
            item['start'] = '2026-11-02' if item['start'] == 1 else '2026-11-16'
            item['end'] = '2026-11-16'
        valid = renderer.validate(data)
        output = renderer.mermaid(valid)
        self.assertIn('V1, 2026-11-02, 14d', output)
        self.assertIn('PH1, 2026-11-02, 14d', output)
        self.assertIn('milestone, M1, 2026-11-16, 0d', output)
        self.assertIn('planned', output)
        data['schedule']['items'][-1].update(start=None, end=None)
        self.assertNotIn('milestone, M1', renderer.mermaid(renderer.validate(data)))

    def test_mermaid_ignores_unmodeled_state_when_record_is_not_a_milestone(self):
        """Covers: roadmap-capabilities#AC8; only milestone objects own event state."""
        data = sample('dates')
        expected = renderer.mermaid(renderer.validate(data))
        data['versions'][0]['state'] = {'status': 'draft'}

        output = renderer.mermaid(renderer.validate(data))

        self.assertEqual(output, expected)

    def test_cli_renders_independent_objects_when_input_uses_schema_1_1(self):
        """Covers: roadmap-capabilities#AC8; cross the real CLI/JSON/output boundary."""
        for mode in ('weeks', 'dates'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / 'input.json'
                out = Path(tmp) / 'output'
                data = event_sample(mode)
                data['versions'][0]['state'] = {'status': 'draft'}
                data['phases'][0]['state'] = {'status': 'draft'}
                source.write_text(json.dumps(data), encoding='utf-8')

                result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                                         '--output-dir', str(out)], capture_output=True, text=True)

                self.assertEqual(result.returncode, 0, result.stderr)
                markdown = (out / 'roadmap.md').read_text(encoding='utf-8')
                self.assertIn('## Phases', markdown)
                self.assertIn('Reviewer signs acceptance', markdown)
                svg = ET.fromstring((out / 'roadmap.svg').read_text(encoding='utf-8'))
                self.assertEqual(len(svg.findall(
                    './/{http://www.w3.org/2000/svg}polygon[@class="milestone"]')), 1)
                self.assertIn('First delivery', ''.join(svg.itertext()))
                self.assertIn('planned', ''.join(svg.itertext()))
                self.assertEqual((out / 'roadmap.mmd').exists(), mode == 'dates')
                if mode == 'dates':
                    self.assertIn('milestone, M1, 2026-11-16, 0d',
                                  (out / 'roadmap.mmd').read_text(encoding='utf-8'))

    def test_terminal_event_states_and_source_links_are_validated(self):
        for state in ('reached', 'missed', 'cancelled'):
            data = event_sample()
            data['milestones'][0].update(state=state, evidence='review.md#decision')
            renderer.validate(data)
            data['milestones'][0]['evidence'] = None
            with self.assertRaisesRegex(ValueError, 'evidence'):
                renderer.validate(data)
        data = event_sample()
        data['phases'][0]['source'] = '//external.invalid/path'
        with self.assertRaisesRegex(ValueError, 'source'):
            renderer.validate(data)

    def test_relative_schedule_has_shared_refs_and_valid_svg(self):
        data = renderer.validate(sample())
        root = ET.fromstring(renderer.svg(data))
        text = ''.join(root.itertext())
        self.assertIn('W1', text)
        self.assertIn('First delivery', text)
        self.assertIn('target', text)
        self.assertIn('R1', renderer.markdown(data))
        self.assertIn('W1–W2', renderer.markdown(data))
        self.assertIn('Make request handling dependable', renderer.markdown(data))
        self.assertIn('Search enables export', renderer.markdown(data))

    def test_dated_mermaid_uses_real_dates_and_escaped_labels(self):
        data = sample('dates')
        data['versions'][0]['name'] = 'end : x\nclick javascript'
        data = renderer.validate(data)
        result = renderer.mermaid(data)
        self.assertIn('2026-11-02, 14d', result)
        self.assertNotIn('\nclick javascript', result)
        self.assertNotIn('end :', result)

    def test_week_mode_cannot_manufacture_mermaid_dates(self):
        with self.assertRaisesRegex(ValueError, 'dates'):
            renderer.mermaid(renderer.validate(sample()))

    def test_unknown_execution_is_not_guessed(self):
        data = sample()
        data['entries'][0]['execution'] = None
        result = renderer.markdown(renderer.validate(data))
        self.assertIn('Unverified execution mappings: R1', result)
        self.assertNotIn('Not started', result)

    def test_unknown_schedule_is_visible_and_not_a_milestone(self):
        data = sample()
        data['schedule']['items'][0].update(start=None, end=None)
        self.assertIn('Unscheduled', renderer.svg(renderer.validate(data)))

    def test_isolated_unscheduled_item_does_not_imply_unverified_dependency(self):
        data = sample()
        data['schedule']['items'][0].update(start=None, end=None)
        result = renderer.markdown(renderer.validate(data))
        self.assertIn('Unscheduled: V1', result)
        self.assertNotIn('Unverified timing for dependencies', result)

    def test_unknown_prerequisite_timing_is_reported_on_its_edge(self):
        data = sample()
        data['schedule']['items'][0].update(start=None, end=None)
        data['schedule']['items'].append(dict(ref='R1', kind='span', basis='target',
                                             start=3, end=5, depends_on=['V1']))
        result = renderer.markdown(renderer.validate(data))
        self.assertIn('Unverified dependency timing: V1 → R1', result)

    def test_bad_inputs_are_rejected(self):
        mutations = [
            (lambda d: d['entries'].append(copy.deepcopy(d['entries'][0])), 'duplicate'),
            (lambda d: d['versions'][0].update(members=['missing']), 'member'),
            (lambda d: d['entries'][0].update(source='javascript:alert(1)'), 'source'),
            (lambda d: d['entries'][0].update(source='//example.com/path'), 'source'),
            (lambda d: d['entries'][0].update(execution='At risk'), 'execution'),
            (lambda d: d['schedule']['items'][0].update(end=0), 'end'),
            (lambda d: d['schedule']['items'][0].update(end=None), 'endpoints'),
            (lambda d: d['schedule']['items'][0].update(depends_on=['missing']), 'dependency'),
            (lambda d: d['schedule']['items'][0].update(start=True), 'start'),
            (lambda d: d.update(updated='2026-02-30'), 'updated'),
            (lambda d: d['schedule']['items'][0].update(end=110), 'horizon'),
            (lambda d: d.update(project='x' * 201), 'project'),
        ]
        for mutate, message in mutations:
            with self.subTest(message=message):
                data = sample()
                mutate(data)
                with self.assertRaisesRegex(ValueError, message):
                    renderer.validate(data)

    def test_cycles_and_overlap_are_different_failures(self):
        data = sample()
        data['schedule']['items'].append(dict(ref='R1', kind='span', basis='committed',
                                             start=2, end=4, depends_on=['V1']))
        with self.assertRaisesRegex(ValueError, 'overlap'):
            renderer.validate(data)
        data['schedule']['items'][0]['depends_on'] = ['R1']
        with self.assertRaisesRegex(ValueError, 'cycle'):
            renderer.validate(data)

    def test_milestone_has_zero_duration_and_dependency_marker(self):
        data = sample()
        data['schedule']['items'].append(dict(ref='R1', kind='milestone', basis='target',
                                             start=3, end=3, depends_on=['V1']))
        root = ET.fromstring(renderer.svg(renderer.validate(data)))
        self.assertTrue(root.findall('.//{http://www.w3.org/2000/svg}polygon'))
        self.assertTrue(root.findall('.//{http://www.w3.org/2000/svg}path'))

    def test_single_view_and_empty_tiers_remain_valid(self):
        data = sample()
        data.update(views=['requirements'], entries=[])
        data.pop('schedule')
        data.pop('versions')
        result = renderer.markdown(renderer.validate(data))
        self.assertIn('No items planned', result)
        self.assertNotIn('## Versions', result)

    def test_unassigned_entries_are_visible(self):
        data = sample()
        data['versions'][0]['members'] = []
        self.assertIn('Unassigned: R1', renderer.markdown(renderer.validate(data)))

    def test_key_condition_links_to_its_source_evidence(self):
        result = renderer.markdown(renderer.validate(sample()))
        self.assertIn('[Review results](requirements/search.md#acceptance)', result)

    def test_generation_is_deterministic_and_does_not_mutate_input(self):
        data = sample()
        before = copy.deepcopy(data)
        valid = renderer.validate(data)
        self.assertEqual(renderer.svg(valid), renderer.svg(valid))
        self.assertEqual(data, before)

    def test_xml_control_characters_are_rejected_before_rendering(self):
        data = sample()
        data['project'] = 'Desk\x00secret'
        with self.assertRaisesRegex(ValueError, 'project'):
            renderer.validate(data)

    def test_cli_reports_non_utf8_input_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'bad.json'
            source.write_bytes(b'\xff')
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), '--check'],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn('Traceback', result.stderr)

    def test_last_supported_date_can_be_a_standalone_milestone(self):
        data = sample('dates')
        data['schedule']['items'][0].update(kind='milestone', start='9999-12-31', end='9999-12-31')
        self.assertIn('9999-12-31', renderer.svg(renderer.validate(data)))

    def test_record_count_and_duplicate_version_members_are_bounded(self):
        data = sample()
        data['versions'][0]['members'] = ['R1', 'R1']
        with self.assertRaisesRegex(ValueError, 'duplicate version'):
            renderer.validate(data)
        data = sample()
        data['entries'] = [dict(data['entries'][0], id=f'R{i}') for i in range(201)]
        with self.assertRaisesRegex(ValueError, '200'):
            renderer.validate(data)

    def test_cli_preserves_input_when_output_is_a_hard_link(self):
        """Covers: roadmap-capabilities#AC4; overwrite never targets the input file."""
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input.json'
            original = json.dumps(sample())
            source.write_text(original, encoding='utf-8')
            out = Path(tmp) / 'output'
            out.mkdir()
            (out / 'roadmap.md').hardlink_to(source)

            result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                                     '--output-dir', str(out), '--overwrite'],
                                    capture_output=True, text=True)

            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(source.read_text(encoding='utf-8'), original)
            self.assertIn('input must not be an output file', result.stderr)
            self.assertFalse((out / 'roadmap.svg').exists())

    def test_cli_will_not_replace_an_output_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / 'input.json'
            source.write_text(json.dumps(sample()))
            out = base / 'out'
            out.mkdir()
            evidence = base / 'evidence.md'
            evidence.write_text('preserve source')
            (out / 'roadmap.md').symlink_to(evidence)
            result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                                     '--output-dir', str(out), '--overwrite'], capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(evidence.read_text(), 'preserve source')

    def test_cli_preflight_and_stale_output_removal(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / 'input.json'
            out = base / 'out'
            source.write_text(json.dumps(sample('dates')))
            command = [sys.executable, str(SCRIPT), str(source), '--output-dir', str(out)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            old = (out / 'roadmap.md').read_text()
            self.assertTrue((out / 'roadmap.mmd').exists())
            (out / 'notes.txt').write_text('keep')
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual((out / 'roadmap.md').read_text(), old)
            source.write_text(json.dumps(sample()))
            self.assertEqual(subprocess.run(command + ['--overwrite'], capture_output=True).returncode, 0)
            self.assertFalse((out / 'roadmap.mmd').exists())
            self.assertEqual((out / 'notes.txt').read_text(), 'keep')

    def test_invalid_input_and_check_mode_write_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input.json'
            out = Path(tmp) / 'output'
            data = sample()
            source.write_text(json.dumps(data))
            command = [sys.executable, str(SCRIPT), str(source), '--output-dir', str(out)]
            self.assertEqual(subprocess.run(command + ['--check'], capture_output=True).returncode, 0)
            self.assertFalse(out.exists())
            data['schedule']['items'][0]['end'] = -1
            source.write_text(json.dumps(data))
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertFalse(out.exists())

    def test_switching_to_single_view_removes_only_generated_diagrams(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / 'input.json'
            source.write_text(json.dumps(sample('dates')))
            out = base / 'output'
            command = [sys.executable, str(SCRIPT), str(source), '--output-dir', str(out)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertTrue((out / 'roadmap.svg').exists())
            data = sample()
            data['views'] = ['requirements']
            source.write_text(json.dumps(data))
            self.assertEqual(subprocess.run(command + ['--overwrite'], capture_output=True).returncode, 0)
            self.assertFalse((out / 'roadmap.svg').exists())
            self.assertFalse((out / 'roadmap.mmd').exists())


if __name__ == '__main__':
    unittest.main()

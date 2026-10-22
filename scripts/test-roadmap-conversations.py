#!/usr/bin/env python3
"""Regression checks for the multi-turn roadmap action/renderer boundary."""

import importlib.util
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/roadmap-conversation-eval.py'
CASES = ROOT / 'tests/fixtures/roadmap-conversations/cases.json'


class ConversationTests(unittest.TestCase):
    """Covers: roadmap-generation-workflow#G5 and #G6."""

    def run_cases(self, cases=None):
        with tempfile.TemporaryDirectory() as temp:
            fixture = CASES if cases is None else Path(temp) / 'cases.json'
            if cases is not None:
                fixture.write_text(json.dumps(cases))
            report = Path(temp) / 'report.json'
            result = subprocess.run([sys.executable, str(SCRIPT), '--cases', str(fixture),
                                     '--report', str(report)], capture_output=True, text=True)
            return result, json.loads(report.read_text()) if report.exists() else None

    def test_complete_multi_turn_replays_execute_renderer_and_pass_every_turn(self):
        result, report = self.run_cases()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(report['backend'], 'scripted-replay')
        self.assertFalse(report['live_model'])
        self.assertEqual(report['pass_rate'], 1.0)
        self.assertEqual(sum(len(case['turns']) for case in report['cases']), 30)
        for case in report['cases']:
            self.assertTrue(case['passed'], case)
            self.assertEqual(any(turn['renderer_executed'] for turn in case['turns']), case['id'] != 'empty-request')

    def test_phase_routes_are_loaded_and_boundary_violations_are_detected(self):
        """Covers: roadmap-generation-workflow#G7."""
        spec = importlib.util.spec_from_file_location('conversation_eval', SCRIPT)
        evaluator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(evaluator)
        context = evaluator.skill_context()
        for path in ['skills/review-roadmap/SKILL.md', 'skills/orchestrate-roadmap-planning/SKILL.md']:
            self.assertIn('SOURCE ' + path, context)
        controls = [('continuous-stages', 0, 'ask', 'business'),
                    ('scoped-review-populated', 1, 'review', 'business'),
                    ('authorization-boundaries', 1, 'populate', 'business'),
                    ('authorization-boundaries', 2, 'ask', 'structure'),
                    ('business-review-blank', 1, 'review', 'structure')]
        for case_id, index, action, scope in controls:
            with self.subTest(case=case_id):
                case = next(c for c in json.loads(CASES.read_text()) if c['id'] == case_id)
                case['turns'][index]['replay'] = dict(action=action, review_scope=scope, reason='Negative control')
                result, report = self.run_cases([case])
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(report['cases'][0]['turns'][index]['violations'])

    def test_generation_asset_digest_changes_when_template_catalog_or_source_changes(self):
        """Covers: roadmap-generation-workflow#G6."""
        spec = importlib.util.spec_from_file_location('conversation_eval', SCRIPT)
        evaluator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(evaluator)
        relative_paths = ['skills/define-roadmap/assets/structure-first/' + name for name in evaluator.TOPICS]
        relative_paths += ['skills/define-roadmap/scripts/roadmap-zh-CN.json',
                           'skills/define-roadmap/references/languages/zh-CN/input.json',
                           'skills/define-roadmap/references/service-desk/iteration-driven/input.json']
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in relative_paths:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / name).read_bytes())
            baseline = evaluator.asset_digest(root)
            self.assertEqual(baseline, evaluator.asset_digest(ROOT))
            for name in relative_paths:
                with self.subTest(asset=name):
                    target = root / name
                    content = target.read_bytes()
                    target.write_bytes(content + b'\n')
                    self.assertNotEqual(evaluator.asset_digest(root), baseline)
                    target.write_bytes(content)
            (root / relative_paths[0]).unlink()
            with self.assertRaises(OSError):
                evaluator.asset_digest(root)

    def test_forbidden_or_drifting_choices_are_failures_instead_of_silent_success(self):
        for action, scope in [('populate', 'business'), ('publish', 'business'), ('blank', 'business')]:
            cases = json.loads(CASES.read_text())[:1]
            cases[0]['turns'][0]['replay'] = dict(action=action, review_scope=scope, reason='Negative control')
            result, report = self.run_cases(cases)
            self.assertNotEqual(result.returncode, 0, result.stderr)
            self.assertFalse(report['cases'][0]['passed'])
            self.assertTrue(report['cases'][0]['turns'][0]['violations'])

    def test_source_oracle_rejects_condition_outcome_and_event_criterion_drift(self):
        spec = importlib.util.spec_from_file_location('conversation_eval', SCRIPT)
        evaluator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(evaluator)
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / 'out'
            source = Path(temp) / 'input.json'
            data = evaluator.business_source()
            source.write_text(json.dumps(data))
            subprocess.run([sys.executable, str(evaluator.RENDERER), str(source), '--output-dir', str(out)],
                           check=True, capture_output=True)
            for name, old in [('roadmap.md', data['entries'][0]['conditions']),
                              ('versions.md', data['versions'][0]['outcome']),
                              ('milestones.md', data['milestones'][0]['criterion'])]:
                path = out / name
                original = path.read_text()
                path.write_text(original.replace(old, 'Changed without source authority'))
                self.assertTrue(evaluator.artifact_findings(out, 'populated', data), name)
                path.write_text(original)

    def test_structural_oracle_rejects_format_heading_and_navigation_drift(self):
        spec = importlib.util.spec_from_file_location('conversation_eval', SCRIPT)
        evaluator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(evaluator)
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            subprocess.run([sys.executable, str(evaluator.RENDERER), '--blank', '--output-dir', temp],
                           check=True, capture_output=True)
            main = out / 'roadmap.md'
            original = main.read_text()
            for broken in [original.replace('**Direction and goal:**', 'Direction and goal:'),
                           original.replace('## Priority arrangement', '## Miscellaneous'),
                           original.replace('](versions.md)', '](missing.md)')]:
                main.write_text(broken)
                self.assertTrue(evaluator.artifact_findings(out, 'blank', evaluator.business_source()))
            main.write_text(original)

    def test_failed_action_observation_reports_actual_workspace_not_expected_stage(self):
        cases = json.loads(CASES.read_text())[:1]
        cases[0]['turns'] = cases[0]['turns'][:1]
        cases[0]['turns'][0]['replay'] = dict(action='populate', review_scope='business', reason='Negative control')
        result, report = self.run_cases(cases)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(report['cases'][0]['turns'][0]['observation']['stage'], 'absent')

    def test_replay_report_identifies_fixture_and_executable_versions(self):
        result, report = self.run_cases()
        self.assertEqual(result.returncode, 0, result.stderr)
        for key in ['cases_sha256', 'runner_sha256', 'renderer_sha256', 'assets_sha256']:
            self.assertRegex(report[key], r'^[a-f0-9]{64}$')

    def test_saved_live_evidence_matches_the_current_contract_and_executables(self):
        spec = importlib.util.spec_from_file_location('conversation_eval', SCRIPT)
        evaluator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(evaluator)
        evidence = json.loads((ROOT / 'docs/references/roadmap-conversation-eval-20261021.json').read_text())
        self.assertTrue(evidence['passed'])
        self.assertTrue(evidence['live_model'])
        details = (ROOT / 'docs/references' / evidence['details']).resolve()
        self.assertTrue(details.is_relative_to(ROOT))
        self.assertEqual(evidence['details_sha256'], hashlib.sha256(details.read_bytes()).hexdigest())
        export_spec = importlib.util.spec_from_file_location('evidence_export', ROOT / 'scripts/save-roadmap-eval-evidence.py')
        exporter = importlib.util.module_from_spec(export_spec)
        export_spec.loader.exec_module(exporter)
        raw = json.loads(details.read_text())
        exporter.validate(raw)
        for case in raw['cases']:
            for turn in case['turns']:
                del turn['user']
                del turn['decision']['reason']
        self.assertEqual(evidence['cases'], raw['cases'])
        self.assertEqual(evidence['assets_sha256'], evaluator.asset_digest(ROOT))
        self.assertEqual(evidence['backend'], 'codex-live')
        self.assertEqual(evidence['context_sha256'], hashlib.sha256(evaluator.skill_context().encode()).hexdigest(), 'live evidence uses stale instructions')
        self.assertEqual(evidence['runner_sha256'], hashlib.sha256(SCRIPT.read_bytes()).hexdigest(), 'live evidence uses a stale evaluator')
        self.assertEqual(evidence['renderer_sha256'], hashlib.sha256(evaluator.RENDERER.read_bytes()).hexdigest(), 'live evidence uses a stale renderer')
        cases = json.loads(CASES.read_text()) + json.loads((ROOT / 'skills/define-roadmap/references/languages/conversations-zh-CN.json').read_text())
        self.assertEqual(evidence['cases_sha256'], hashlib.sha256(json.dumps(cases, sort_keys=True, ensure_ascii=False).encode()).hexdigest())
        self.assertEqual([case['id'] for case in evidence['cases']], [case['id'] for case in cases])
        self.assertEqual(sum(len(case['turns']) for case in evidence['cases']), 30)
        self.assertTrue(all(turn['passed'] for case in evidence['cases'] for turn in case['turns']))

    def test_live_adapter_errors_fail_closed_without_network_in_unit_tests(self):
        cases = json.loads(CASES.read_text())
        selected = next(case for case in cases if case['id'] == 'empty-request')
        for mode in ['provider-error', 'timeout', 'tool-attempt', 'unknown-tool-attempt', 'invalid-response', 'incomplete-trace', 'valid-response']:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                cli = root / 'codex'
                body = ['import json,sys,time', "if '--version' in sys.argv: print('test-provider-double'); sys.exit(0)"]
                if mode == 'provider-error':
                    body += ["sys.stderr.write('Provider unavailable'); sys.exit(4)"]
                elif mode == 'timeout':
                    body += ['time.sleep(3)']
                else:
                    response = {} if mode == 'invalid-response' else dict(action='ask', review_scope='structure', reason='Provider double')
                    body += ["target = sys.argv[sys.argv.index('--output-last-message') + 1]",
                             "open(target, 'w').write(" + repr(json.dumps(response)) + ")"]
                    if mode in {'tool-attempt', 'unknown-tool-attempt'}:
                        kind = 'command_execution' if mode == 'tool-attempt' else 'future_tool_call'
                        body += ["print(json.dumps({'item': {'type': " + repr(kind) + "}}))"]
                    if mode != 'incomplete-trace':
                        body += ["print(json.dumps({'type': 'item.completed', 'item': {'type': 'agent_message'}}))",
                                 "print(json.dumps({'type': 'turn.completed'}))"]
                cli.write_text('#!' + sys.executable + '\n' + '\n'.join(body) + '\n')
                cli.chmod(0o755)
                fixture, report = root / 'case.json', root / 'report.json'
                fixture.write_text(json.dumps([selected]))
                result = subprocess.run([sys.executable, str(SCRIPT), '--eval', '--cases', str(fixture),
                    '--timeout', '1' if mode == 'timeout' else '15', '--report', str(report)], capture_output=True, text=True,
                    env={**os.environ, 'PATH': str(root)})
                if mode == 'valid-response':
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertTrue(json.loads(report.read_text())['passed'])
                    continue
                self.assertNotEqual(result.returncode, 0)
                evidence = json.loads(report.read_text())
                self.assertFalse(evidence['passed'])
                violations = evidence['cases'][0]['turns'][0]['violations']
                self.assertTrue(violations)
                self.assertFalse(evidence['cases'][0]['turns'][0]['renderer_executed'])
                if mode in {'tool-attempt', 'unknown-tool-attempt'}:
                    self.assertIn('attempted tools', ' '.join(violations))
                if mode == 'incomplete-trace':
                    self.assertIn('incomplete provider trace', ' '.join(violations))

    def test_missing_turns_or_expected_constraints_cannot_report_a_pass(self):
        for mutate in ['empty', 'missing_expected', 'invalid_stage', 'invalid_no_write']:
            cases = json.loads(CASES.read_text())[:1]
            if mutate == 'empty':
                cases[0]['turns'] = []
            elif mutate == 'missing_expected':
                del cases[0]['turns'][0]['expected']
            elif mutate == 'invalid_stage':
                cases[0]['turns'][0]['expected']['stage'] = 'anything'
            else:
                cases[0]['turns'][0]['expected']['no_write'] = 'yes'
            result, report = self.run_cases(cases)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('error', report)

    def test_artifact_oracle_rejects_guidance_and_changed_business_states(self):
        spec = importlib.util.spec_from_file_location('conversation_eval', SCRIPT)
        evaluator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(evaluator)
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            subprocess.run([sys.executable, str(evaluator.RENDERER), '--blank', '--output-dir', temp], check=True,
                           capture_output=True)
            self.assertEqual(evaluator.artifact_findings(out, 'blank', evaluator.business_source()), [])
            main = out / 'roadmap.md'
            main.write_text(main.read_text() + '\nInstructions: assign a date now.\n')
            self.assertTrue(evaluator.artifact_findings(out, 'blank', evaluator.business_source()))
            source = out.parent / ('source-' + out.name + '.json')
            try:
                source.write_text(json.dumps(evaluator.business_source()))
                subprocess.run([sys.executable, str(evaluator.RENDERER), str(source), '--overwrite',
                                '--output-dir', temp], check=True, capture_output=True)
                self.assertEqual(evaluator.artifact_findings(out, 'populated', evaluator.business_source()), [])
                main.write_text(main.read_text().replace('| Blocked |', '| Completed |'))
                self.assertTrue(evaluator.artifact_findings(out, 'populated', evaluator.business_source()))
                main.write_text(main.read_text().replace('| Completed |', '| Blocked |'))
                versions = out / 'versions.md'
                versions.write_text(versions.read_text().replace('| BUG1 |', '| BUG1, R1 |'))
                self.assertTrue(evaluator.artifact_findings(out, 'populated', evaluator.business_source()))
            finally:
                source.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()

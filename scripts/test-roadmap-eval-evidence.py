#!/usr/bin/env python3
"""Test evidence export with synthetic protocol samples, never real evaluation claims."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/save-roadmap-eval-evidence.py'
def synthetic_report():
    """Construct a simulated provider trace solely for exporter unit tests."""
    spec = importlib.util.spec_from_file_location('runner', ROOT / 'scripts/roadmap-conversation-eval.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    cases = json.loads(runner.CASES.read_text()) + json.loads(
        (ROOT / 'skills/define-roadmap/references/languages/conversations-zh-CN.json').read_text())
    digest = lambda value: hashlib.sha256(value).hexdigest()
    report = dict(backend='codex-live', live_model=True, passed=True, pass_rate=1.0,
                  timeout_seconds=180, fixture_notice='Synthetic exporter unit-test sample; not evaluation evidence.',
                  assets_sha256=runner.asset_digest(ROOT),
                  context_sha256=digest(runner.skill_context().encode()),
                  cases_sha256=digest(json.dumps(cases, sort_keys=True, ensure_ascii=False).encode()),
                  runner_sha256=digest(Path(spec.origin).read_bytes()),
                  renderer_sha256=digest(runner.RENDERER.read_bytes()), cases=[])
    for case in cases:
        turns = []
        for index, source in enumerate(case['turns'], 1):
            expected = source['expected']
            executed = source['replay']['action'] in {'blank', 'populate'}
            turns.append(dict(turn=index, user=source['user'], passed=True, violations=[],
                              decision=source['replay'], renderer_executed=executed,
                              observation=dict(stage=expected['stage'], renderer_executed=executed,
                                               markdown_files=sorted(runner.TOPICS) if expected['stage'] != 'absent' else [])))
        report['cases'].append(dict(id=case['id'], passed=True, turns=turns))
    return report


class EvidenceExportTests(unittest.TestCase):
    """Covers: roadmap-generation-workflow#G6."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.raw = Path(self.temp.name) / 'synthetic-report.json'
        self.raw.write_text(json.dumps(synthetic_report()))

    def test_synthetic_protocol_sample_exports_summary_and_full_trace(self):
        with tempfile.TemporaryDirectory(dir=ROOT) as temp:
            out = Path(temp).resolve()
            result = subprocess.run([sys.executable, str(SCRIPT), str(self.raw), '--output-root', temp], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads((out / 'docs/references/roadmap-conversation-eval.json').read_text())
            details = (out / 'docs/references' / summary['details']).resolve()
            self.assertTrue(details.is_relative_to(out))
            self.assertEqual(json.loads(details.read_text())['context_sha256'], summary['context_sha256'])
            self.assertNotIn('user', summary['cases'][0]['turns'][0])
            self.assertIn('user', json.loads(details.read_text())['cases'][0]['turns'][0])
            self.assertEqual(sum(len(case['turns']) for case in summary['cases']), 30)
            refused = subprocess.run([sys.executable, str(SCRIPT), str(self.raw), '--output-root', temp], capture_output=True, text=True)
            self.assertNotEqual(refused.returncode, 0)
            checker = ROOT / 'scripts/check-roadmap-eval-evidence.py'
            summary_path = out / 'docs/references/roadmap-conversation-eval.json'
            status = subprocess.run([sys.executable, str(checker), str(summary_path)], capture_output=True, text=True)
            self.assertEqual(status.returncode, 0, status.stdout + status.stderr)
            self.assertEqual(json.loads(status.stdout)['status'], 'passed')
            summary['passed'] = False
            summary_path.write_text(json.dumps(summary))
            status = subprocess.run([sys.executable, str(checker), str(summary_path)], capture_output=True, text=True)
            self.assertNotEqual(status.returncode, 0)
            self.assertIn('summary contradicts', status.stdout)
            summary['passed'] = True
            raw = json.loads(details.read_text())
            raw['context_sha256'] = '0' * 64
            details.write_text(json.dumps(raw))
            summary['details_sha256'] = hashlib.sha256(details.read_bytes()).hexdigest()
            summary_path.write_text(json.dumps(summary))
            status = subprocess.run([sys.executable, str(checker), str(summary_path)], capture_output=True, text=True)
            self.assertNotEqual(status.returncode, 0)
            self.assertIn('context_sha256', status.stdout)

    def test_inconsistent_passing_trace_is_rejected_before_writing(self):
        for mutation in ['action', 'scope', 'stage', 'execution', 'missing_observation']:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                report = json.loads(self.raw.read_text())
                turn = report['cases'][0]['turns'][0]
                if mutation == 'action':
                    turn['decision']['action'] = 'populate'
                elif mutation == 'scope':
                    turn['decision']['review_scope'] = 'business'
                elif mutation == 'stage':
                    turn['observation']['stage'] = 'populated'
                elif mutation == 'execution':
                    turn['renderer_executed'] = False
                else:
                    del turn['observation']
                source = root / 'input.json'
                source.write_text(json.dumps(report))
                result = subprocess.run([sys.executable, str(SCRIPT), str(source), '--output-root', str(root / 'out')], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((root / 'out').exists())

    def test_stale_or_replay_report_is_rejected_before_writing(self):
        for field, value in [('backend', 'scripted-replay'), ('runner_sha256', '0' * 64), ('passed', False), ('assets_sha256', '0' * 64), ('context_sha256', '0' * 64), ('timeout_seconds', 0)]:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                report = json.loads(self.raw.read_text())
                report[field] = value
                source = root / 'input.json'
                source.write_text(json.dumps(report))
                result = subprocess.run([sys.executable, str(SCRIPT), str(source), '--output-root', str(root / 'out')], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((root / 'out').exists())


if __name__ == '__main__':
    unittest.main()

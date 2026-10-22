#!/usr/bin/env python3
"""Check repeatable export of actual live-eval evidence without model calls."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/save-roadmap-eval-evidence.py'
RAW = ROOT / 'skills/define-roadmap/references/languages/conversation-eval-20261021.json'


class EvidenceExportTests(unittest.TestCase):
    """Covers: roadmap-generation-workflow#G6."""

    def test_valid_live_report_exports_summary_and_full_trace_without_losing_provenance(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp).resolve()
            result = subprocess.run([sys.executable, str(SCRIPT), str(RAW), '--output-root', temp], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            summary = json.loads((out / 'docs/references/roadmap-conversation-eval-20261021.json').read_text())
            details = (out / 'docs/references' / summary['details']).resolve()
            self.assertTrue(details.is_relative_to(out))
            self.assertEqual(json.loads(details.read_text())['context_sha256'], summary['context_sha256'])
            self.assertNotIn('user', summary['cases'][0]['turns'][0])
            self.assertIn('user', json.loads(details.read_text())['cases'][0]['turns'][0])
            self.assertEqual(sum(len(case['turns']) for case in summary['cases']), 30)
            refused = subprocess.run([sys.executable, str(SCRIPT), str(RAW), '--output-root', temp], capture_output=True, text=True)
            self.assertNotEqual(refused.returncode, 0)

    def test_inconsistent_passing_trace_is_rejected_before_writing(self):
        for mutation in ['action', 'scope', 'stage', 'execution', 'missing_observation']:
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                report = json.loads(RAW.read_text())
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
        for field, value in [('backend', 'scripted-replay'), ('runner_sha256', '0' * 64), ('passed', False), ('assets_sha256', '0' * 64), ('timeout_seconds', 0)]:
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                report = json.loads(RAW.read_text())
                report[field] = value
                source = root / 'input.json'
                source.write_text(json.dumps(report))
                result = subprocess.run([sys.executable, str(SCRIPT), str(source), '--output-root', str(root / 'out')], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((root / 'out').exists())


if __name__ == '__main__':
    unittest.main()

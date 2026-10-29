#!/usr/bin/env python3
"""Isolated executable scenarios, not an Agent or real-channel acceptance run."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

from release_contract_v2 import complete

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/fixtures/release-workflow'
spec = importlib.util.spec_from_file_location('local_workflow', FIXTURES / 'local_workflow.py')
local = importlib.util.module_from_spec(spec)
spec.loader.exec_module(local)


class ExecutionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.package = json.loads((FIXTURES / 'package.json').read_text())
        self.workflow = local.Workflow(self.root, self.package)

    def test_build_records_actual_artifacts_when_invoked_without_release(self):
        """Covers: AIC-REQ-06#AC1."""
        result = local.build(self.root, build_available=True)
        self.assertEqual(result['status'], 'passed')
        self.assertTrue((self.root / result['artifact']['location']).is_file())
        with zipfile.ZipFile(self.root / result['artifact']['location']) as archive:
            self.assertEqual(set(archive.namelist()), {'client.txt', 'plugin.txt', 'config.json'})
        self.assertEqual(result['artifact']['identity'], local.digest(self.root / result['artifact']['location']))
        self.assertEqual(result['source_revision'], '2' * 40)
        self.assertFalse((self.root / 'package.json').exists())
        self.assertEqual(self.workflow.receipts(), [])

    def test_build_does_not_call_combined_tool_when_build_only_is_unavailable(self):
        """Covers: AIC-REQ-06#AC1."""
        self.assertEqual(local.build(self.root, build_available=False)['status'], 'unavailable')
        self.assertEqual(list(self.root.iterdir()), [])

    def test_build_failure_preserves_failure_when_output_check_fails(self):
        """Covers: AIC-REQ-06#AC1."""
        result = local.build(self.root, build_available=True, fail=True)
        self.assertEqual(result['status'], 'failed')
        self.assertNotEqual(result['exit_code'], 0)
        self.assertFalse((self.root / 'candidate.zip').exists())

    def test_combined_pipeline_reuses_project_tool_when_publication_is_authorized(self):
        """Covers: AIC-REQ-06#AC8, AIC-REQ-06#AC12."""
        self.assertEqual(self.workflow.combined('desktop', authorized=False), 'blocked')
        self.assertEqual(list(self.root.iterdir()), [])
        self.assertEqual(self.workflow.combined('desktop', authorized=True), 'complete')
        restored = local.Workflow.load(self.root)
        target = restored.package['targets'][0]
        self.assertEqual(target['delivered_artifacts'][0]['identity'], local.digest(self.root / 'candidate.zip'))
        self.assertEqual(target['delivered_artifacts'][0]['relationship'], 'unchanged')
        self.assertTrue(complete(restored.package, 'desktop'))
        self.assertEqual(len(restored.receipts()), 1)

    def test_apple_style_upload_waits_for_server_when_receipt_has_arrived(self):
        """Covers: AIC-REQ-06#AC8, AIC-REQ-06#AC9, AIC-REQ-06#AC10."""
        self.assertEqual(self.workflow.upload('apple', authorized=True, transformed=True), 'complete')
        restored = local.Workflow.load(self.root)
        self.assertFalse(complete(restored.package, 'apple'))
        restored.package['checks'][-1].update(status='failed', evidence='fixture:server-failure')
        self.assertFalse(complete(restored.package, 'apple'))
        restored.package['checks'][-1].update(status='passed', evidence='fixture:server-pass')
        restored.finish('apple')
        restored.save()
        restored = local.Workflow.load(self.root)
        self.assertTrue(complete(restored.package, 'apple'))
        self.assertEqual(restored.package['targets'][1]['delivered_artifacts'][0]['relationship'], 'transformed')
        self.assertEqual(len(restored.receipts()), 1)

    def test_recovery_reuses_receipt_when_response_is_lost_after_committed_write(self):
        """Covers: AIC-REQ-06#AC13, QAS-01."""
        with self.assertRaises(local.ReplyLost):
            self.workflow.upload('desktop', authorized=True, lose_reply=True)
        self.assertEqual(len(self.workflow.receipts()), 1)
        restored = local.Workflow.load(self.root)
        self.assertEqual(restored.package['attempts'][0]['outcome'], 'unknown')
        self.assertEqual(restored.upload('desktop', authorized=True), 'reused')
        self.assertEqual(len(restored.receipts()), 1)
        self.assertEqual(restored.package['attempts'][0]['outcome'], 'complete')

    def test_recovery_stops_when_provider_observation_is_unknown_or_conflicting(self):
        """Covers: AIC-REQ-06#AC13, QAS-01."""
        for observed in ['unknown', 'conflict', 'inaccessible']:
            with self.subTest(observed=observed):
                self.assertEqual(self.workflow.upload('desktop', authorized=True, observation=observed), 'blocked')
                self.assertEqual(self.workflow.receipts(), [])

    def test_recovery_rejects_stale_receipt_when_selected_candidate_changes(self):
        """Covers: AIC-REQ-06#AC7, AIC-REQ-06#AC13."""
        self.workflow.upload('desktop', authorized=True)
        restored = local.Workflow.load(self.root)
        restored.package['targets'][0].update(candidate_id='a', artifact_ids=['a-bin'],
                                               delivered_artifacts=[], status='pending', evidence=None)
        restored.package['checks'][0].update(status='passed', evidence='new-selection-check')
        self.assertEqual(restored.upload('desktop', authorized=True), 'blocked')
        self.assertEqual(len(restored.receipts()), 1)

    def test_recovery_rejects_receipt_when_actual_delivered_bytes_have_changed(self):
        """Covers: AIC-REQ-06#AC8, AIC-REQ-06#AC13."""
        self.workflow.upload('desktop', authorized=True)
        (self.root / 'desktop-delivered.bin').write_bytes(b'contradictory output')
        restored = local.Workflow.load(self.root)
        self.assertEqual(restored.upload('desktop', authorized=True), 'blocked')
        self.assertEqual(len(restored.receipts()), 1)

    def test_announcement_recovery_does_not_build_or_upload_when_delivery_response_is_lost(self):
        """Covers: AIC-REQ-06#AC13, QAS-01."""
        self.workflow.upload('desktop', authorized=True)
        with self.assertRaises(local.ReplyLost):
            self.workflow.announce('desktop', authorized=True, lose_reply=True)
        before = copy.deepcopy(self.workflow.receipts())
        artifacts = {p.name: p.read_bytes() for p in self.root.glob('*.zip')}
        restored = local.Workflow.load(self.root)
        self.assertEqual(restored.announce('desktop', authorized=True), 'reused')
        self.assertEqual(restored.receipts(), before)
        self.assertEqual({p.name: p.read_bytes() for p in self.root.glob('*.zip')}, artifacts)
        self.assertEqual([r['action'] for r in before], ['upload', 'announce'])
        self.assertFalse((self.root / 'candidate.zip').exists())

    def test_announcement_rejects_pending_target_when_other_target_is_complete(self):
        """Covers: AIC-REQ-06#AC4, AIC-REQ-06#AC13."""
        self.workflow.upload('desktop', authorized=True)
        self.assertEqual(self.workflow.announce('apple', authorized=True), 'blocked')
        self.assertEqual([r['action'] for r in self.workflow.receipts()], ['upload'])

    def test_consumer_rejects_incompatible_input_before_any_local_mutation(self):
        """Covers: AIC-REQ-06#AC14."""
        for schema in ['1.2.2', '2.1.0', '3.0.0', None]:
            with self.subTest(schema=schema):
                self.workflow.package['schema_version'] = schema
                self.assertEqual(self.workflow.upload('desktop', authorized=True), 'blocked')
                self.assertEqual(list(self.root.iterdir()), [])
        self.workflow.package['schema_version'] = '2.0.0'
        self.assertEqual(self.workflow.upload('desktop', authorized=True, consumer_verified=False), 'blocked')
        self.assertEqual(list(self.root.iterdir()), [])

    def test_single_writer_boundary_blocks_when_another_writer_owns_it(self):
        """Covers: AIC-REQ-06#AC13."""
        (self.root / 'writer.lock').write_text('other writer')
        self.assertEqual(self.workflow.upload('desktop', authorized=True), 'blocked')
        self.assertEqual(self.workflow.receipts(), [])


if __name__ == '__main__':
    unittest.main()

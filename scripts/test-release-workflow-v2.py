#!/usr/bin/env python3
"""Behavioral checks for the staged release admission model."""
import unittest
from release_workflow_v2 import decide, aggregate, retry_action, admit_schema, delivery_verified

class ReleaseWorkflowTests(unittest.TestCase):
    def test_selection_is_candidate_and_target_specific(self):
        checks = [{'candidate': 'a', 'target': 'linux', 'name': 'tests', 'stage': 'select', 'status': 'passed', 'required': True, 'evidence': 'report'}]
        self.assertTrue(decide('a', 'linux', 'select', checks, [], True, True))
        self.assertFalse(decide('b', 'linux', 'select', checks, [], True, True))
        self.assertFalse(decide('a', 'mac', 'select', checks, [], True, True))

    def test_exception_is_scoped_and_never_waives_identity(self):
        checks = [{'candidate': 'a', 'target': 'linux', 'name': 'tests', 'stage': 'select', 'status': 'failed', 'required': True, 'waivable': True, 'origin': 'internal'}]
        waiver = {'candidate': 'a', 'target': 'linux', 'check': 'tests', 'stage': 'select', 'approver': 'owner', 'scope': 'release', 'rationale': 'known failure', 'evidence': 'report'}
        self.assertTrue(decide('a', 'linux', 'select', checks, [waiver], True, True))
        self.assertFalse(decide('a', 'linux', 'select', checks, [waiver], True, False))
        self.assertFalse(decide('a', 'linux', 'select', checks, [waiver], False, True))
        checks[0]['waivable'] = False
        self.assertFalse(decide('a', 'linux', 'select', checks, [waiver], True, True))

    def test_later_checks_do_not_block_upload(self):
        checks = [{'candidate': 'a', 'target': 'linux', 'name': 'server', 'stage': 'complete', 'status': 'pending', 'required': True}]
        self.assertTrue(decide('a', 'linux', 'upload', checks, [], True, True))
        self.assertFalse(decide('a', 'linux', 'complete', checks, [], True, True))

    def test_required_targets_and_empty_success(self):
        complete = {'required': True, 'status': 'complete', 'candidate_id': 'a', 'artifact_ids': ['a-bin'],
                    'delivered_artifacts': [{'identity': 'a', 'relationship': 'unchanged', 'evidence': 'verified'}], 'evidence': 'receipt'}
        self.assertFalse(aggregate([complete, {'required': True, 'status': 'pending'}]))
        self.assertTrue(aggregate([complete, {'required': False, 'status': 'failed'}]))
        self.assertFalse(aggregate([{'required': False, 'status': 'pending'}]))
        self.assertFalse(aggregate([{'required': True, 'status': 'complete'}]))
        self.assertFalse(aggregate([complete, {'status': 'pending'}]))

    def test_retry_only_if_absence_is_proven(self):
        self.assertEqual(retry_action('complete', True), 'reuse')
        self.assertEqual(retry_action('absent', True), 'execute')
        for state, authorized in [('unknown', True), ('conflict', True), ('absent', False)]:
            self.assertEqual(retry_action(state, authorized), 'stop')

    def test_provider_blocker_cannot_be_waived(self):
        checks = [{'candidate': 'a', 'target': 'linux', 'name': 'provider', 'stage': 'select', 'status': 'failed', 'required': True, 'waivable': True, 'origin': 'provider'}]
        waiver = {'candidate': 'a', 'target': 'linux', 'check': 'provider', 'stage': 'select', 'approver': 'owner', 'scope': 'release', 'rationale': 'reason', 'evidence': 'report'}
        self.assertFalse(decide('a', 'linux', 'select', checks, [waiver], True, True))

    def test_exception_cannot_cross_action_scope(self):
        checks = [{'candidate': 'a', 'target': 'linux', 'name': 'tests', 'stage': 'select', 'status': 'failed', 'required': True, 'waivable': True, 'origin': 'internal'}]
        waiver = {'candidate': 'a', 'target': 'linux', 'check': 'tests', 'stage': 'select', 'approver': 'owner', 'scope': 'different', 'rationale': 'reason', 'evidence': 'report'}
        self.assertFalse(decide('a', 'linux', 'select', checks, [waiver], True, True))

    def test_missing_pass_evidence_is_not_a_pass(self):
        checks = [{'candidate': 'a', 'target': 'linux', 'name': 'tests', 'stage': 'select', 'status': 'passed', 'required': True, 'evidence': ''}]
        self.assertFalse(decide('a', 'linux', 'select', checks, [], True, True))

    def test_missing_required_flag_and_unknown_check_outcome_are_rejected(self):
        check = {'candidate': 'a', 'target': 'linux', 'name': 'tests', 'stage': 'select', 'status': 'passed', 'evidence': 'report'}
        self.assertFalse(decide('a', 'linux', 'select', [check], [], True, True))
        check.update(required=True, status='unexpected', waivable=True, origin='internal')
        waiver = {'candidate': 'a', 'target': 'linux', 'check': 'tests', 'stage': 'select', 'approver': 'owner', 'scope': 'release', 'rationale': 'reason', 'evidence': 'report'}
        self.assertFalse(decide('a', 'linux', 'select', [check], [waiver], True, True))

    def test_schema_rejected_before_side_effect(self):
        self.assertTrue(admit_schema('2.0.0'))
        for value in ('1.2.2', '2.1.0', '3.0.0', 'bad', None):
            self.assertFalse(admit_schema(value))

    def test_delivery_requires_linked_verified_actual_identity(self):
        self.assertTrue(delivery_verified('candidate-a', 'candidate-a', 'unchanged', 'passed'))
        self.assertTrue(delivery_verified('candidate-a', 'signed-output', 'transformed', 'passed'))
        self.assertFalse(delivery_verified('candidate-a', 'signed-output', 'unchanged', 'passed'))
        for relationship, check in [('unknown', 'passed'), ('conflict', 'passed'), ('transformed', 'pending')]:
            self.assertFalse(delivery_verified('candidate-a', 'signed-output', relationship, check))
        self.assertFalse(delivery_verified('candidate-a', '', 'unchanged', 'passed'))

if __name__ == '__main__':
    unittest.main()

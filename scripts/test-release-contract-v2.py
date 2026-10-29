#!/usr/bin/env python3
"""Offline contract scenarios; never invokes a product or remote provider."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

from release_contract_v2 import validate, gate, complete, publication_complete

FIXTURES = Path(__file__).resolve().parents[1] / 'tests/fixtures/release-workflow'


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.package = json.loads((FIXTURES / 'package.json').read_text())
        self.policy = {'waivable': ['a-selection'], 'approvers': ['maintainer']}

    def test_package_round_trip_preserves_candidates_when_one_is_selected(self):
        """Covers: AIC-REQ-06#AC2, AIC-REQ-06#AC3, AIC-REQ-06#AC5."""
        package = self.package
        self.assertTrue(validate(package))
        self.assertFalse(gate(package, 'desktop', 'select', True, True, self.policy, candidate_id='a'))
        self.assertTrue(gate(package, 'desktop', 'select', True, True, self.policy))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'package.json'
            path.write_text(json.dumps(package))
            restored = json.loads(path.read_text())
        self.assertEqual(restored, package)
        self.assertEqual(restored['release_version']['value'], '2026.10')
        self.assertEqual([c['build_identity'] for c in restored['candidates']], ['101', '102'])
        self.assertEqual(restored['checks'][0]['status'], 'failed')
        self.assertFalse(publication_complete(restored, self.policy))

    def test_required_fields_and_references_reject_when_package_is_malformed(self):
        """Covers: AIC-REQ-06#AC4, AIC-REQ-06#AC14."""
        for key in self.package:
            with self.subTest(key=key):
                package = copy.deepcopy(self.package)
                del package[key]
                self.assertFalse(validate(package))

        for mutate in (
            lambda p: p['targets'][0].pop('required'),
            lambda p: p['targets'][0].update(candidate_id='missing'),
            lambda p: p['targets'][0].update(artifact_ids=['a-bin']),
            lambda p: p['candidates'].append(copy.deepcopy(p['candidates'][0])),
            lambda p: p['checks'][1].update(evidence=''),
            lambda p: p['checks'][1].update(status='unknown'),
            lambda p: p['checks'][1].update(target_id='missing'),
        ):
            with self.subTest(mutation=mutate):
                package = copy.deepcopy(self.package)
                mutate(package)
                self.assertFalse(validate(package))

    def test_gate_rejects_missing_selection_when_an_upload_is_requested(self):
        """Covers: AIC-REQ-06#AC4, AIC-REQ-06#AC7."""
        self.package['targets'][0]['artifact_ids'] = []
        self.assertFalse(gate(self.package, 'desktop', 'upload', True, True, self.policy))

    def test_upload_rejects_candidate_override_when_target_selected_another_candidate(self):
        """Covers: AIC-REQ-06#AC7."""
        self.package['checks'][0].update(status='passed', evidence='passed-a')
        self.assertFalse(gate(self.package, 'desktop', 'upload', True, True, self.policy, candidate_id='a'))

    def test_observation_records_reject_missing_fields_when_package_is_loaded(self):
        """Covers: AIC-REQ-06#AC6, AIC-REQ-06#AC8, AIC-REQ-06#AC14."""
        package = self.package
        package['exceptions'] = [{'candidate_id': 'a', 'target_id': 'desktop', 'check_id': 'a-selection',
                                  'scope': 'select', 'approver': 'maintainer', 'rationale': 'risk', 'evidence': 'approval'}]
        package['attempts'] = [{'id': 'attempt-1', 'target_id': 'desktop', 'action': 'upload',
                                'authorization_scope': 'upload', 'operation_id': 'operation-1',
                                'outcome': 'complete', 'evidence': 'receipt'}]
        collections = [('release_version', None), ('candidates', 0), ('targets', 0),
                       ('checks', 0), ('exceptions', 0), ('attempts', 0)]
        for name, index in collections:
            record = package[name] if index is None else package[name][index]
            for key in record:
                with self.subTest(record=name, missing=key):
                    changed = copy.deepcopy(package)
                    row = changed[name] if index is None else changed[name][index]
                    del row[key]
                    self.assertFalse(validate(changed))

    def test_exception_keeps_failed_result_when_policy_and_scope_allow_it(self):
        """Covers: AIC-REQ-06#AC6."""
        package = self.package
        package['exceptions'] = [{'candidate_id': 'a', 'target_id': 'desktop', 'check_id': 'a-selection',
                                  'scope': 'select', 'approver': 'maintainer', 'rationale': 'accepted fixture risk',
                                  'evidence': 'fixture:approval'}]
        before = copy.deepcopy(package['checks'])
        self.assertTrue(gate(package, 'desktop', 'select', True, True, self.policy, candidate_id='a'))
        restored = json.loads(json.dumps(package))
        self.assertEqual(restored['exceptions'], package['exceptions'])
        self.assertTrue(gate(restored, 'desktop', 'select', True, True, self.policy, candidate_id='a'))
        self.assertEqual(package['checks'], before)
        self.assertFalse(gate(package, 'desktop', 'upload', True, True, self.policy, candidate_id='a'))

    def test_exception_is_denied_when_policy_authority_or_identity_is_missing(self):
        """Covers: AIC-REQ-06#AC7."""
        package = self.package
        package['exceptions'] = [{'candidate_id': 'a', 'target_id': 'desktop', 'check_id': 'a-selection',
                                  'scope': 'select', 'approver': 'maintainer', 'rationale': 'risk', 'evidence': 'approval'}]
        for policy, authorized, identity in [(None, True, True), ({}, True, True),
                                           ('unclear-policy', True, True),
                                           ({'waivable': 'a-selection', 'approvers': 'maintainer'}, True, True),
                                           (self.policy, False, True), (self.policy, True, False),
                                           ({'waivable': ['a-selection'], 'approvers': []}, True, True)]:
            with self.subTest(policy=policy, authorized=authorized, identity=identity):
                self.assertFalse(gate(package, 'desktop', 'select', authorized, identity, policy, candidate_id='a'))
        for key in package['exceptions'][0]:
            with self.subTest(missing=key):
                changed = copy.deepcopy(package)
                del changed['exceptions'][0][key]
                self.assertFalse(gate(changed, 'desktop', 'select', True, True, self.policy, candidate_id='a'))
        package['checks'][0]['origin'] = 'provider'
        self.assertFalse(gate(package, 'desktop', 'select', True, True, self.policy, candidate_id='a'))

    def test_post_upload_gate_prevents_completion_when_server_check_is_pending(self):
        """Covers: AIC-REQ-06#AC9, AIC-REQ-06#AC10."""
        package = self.package
        self.assertTrue(validate(package))  # Preparation preserves the required future evidence.
        self.assertTrue(gate(package, 'apple', 'upload', True, True, self.policy))
        self.assertFalse(complete(package, 'apple', self.policy))
        package['checks'][-1].update(status='passed', evidence='fixture:server')
        self.assertFalse(complete(package, 'apple', self.policy))  # Actual output still absent.
        target = package['targets'][1]
        target.update(status='complete', evidence='fixture:receipt', delivered_artifacts=[{
            'candidate_artifact_id': 'b-bin', 'identity': 'signed-output',
            'relationship': 'transformed', 'evidence': 'fixture:verified-transform'}])
        self.assertTrue(complete(package, 'apple', self.policy))

    def test_delivery_identity_and_relation_are_required_when_target_claims_complete(self):
        """Covers: AIC-REQ-06#AC4, AIC-REQ-06#AC8."""
        package = self.package
        target = package['targets'][0]
        target.update(status='complete', evidence='receipt', delivered_artifacts=[{
            'candidate_artifact_id': 'b-bin', 'identity': package['candidates'][1]['artifacts'][0]['identity'],
            'relationship': 'unchanged', 'evidence': 'verified-output'}])
        self.assertTrue(complete(package, 'desktop', self.policy))
        for field, value in [('identity', 'other'), ('relationship', 'contradictory'),
                             ('evidence', ''), ('candidate_artifact_id', 'a-bin')]:
            with self.subTest(field=field):
                changed = copy.deepcopy(package)
                changed['targets'][0]['delivered_artifacts'][0][field] = value
                self.assertFalse(complete(changed, 'desktop', self.policy))

    def test_aggregate_keeps_optional_outcomes_when_required_targets_finish(self):
        """Covers: AIC-REQ-06#AC11."""
        package = self.package
        for target in package['targets']:
            target.update(status='complete', evidence='receipt', delivered_artifacts=[{
                'candidate_artifact_id': 'b-bin', 'identity': package['candidates'][1]['artifacts'][0]['identity'],
                'relationship': 'unchanged', 'evidence': 'verified-output'}])
        package['checks'][-1].update(status='passed', evidence='server')
        self.assertTrue(publication_complete(package, self.policy))
        for state in ['pending', 'failed', 'unknown']:
            package['targets'][1]['status'] = state
            self.assertFalse(publication_complete(package, self.policy))
            package['targets'][1]['required'] = False
            self.assertTrue(publication_complete(package, self.policy))
            self.assertEqual(package['targets'][1]['status'], state)
            package['targets'][1]['required'] = True
        for target in package['targets']:
            target.update(required=False, status='pending')
        self.assertFalse(publication_complete(package, self.policy))
        package['targets'] = []
        self.assertFalse(publication_complete(package, self.policy))


if __name__ == '__main__':
    unittest.main()

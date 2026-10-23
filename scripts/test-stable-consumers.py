#!/usr/bin/env python3
"""Permanent old/new reference-consumer and negative contract regressions."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('stable_contracts', ROOT / 'scripts/check-stable-consumers.py')
consumer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(consumer)
FIXTURES = ROOT / 'tests/fixtures/stable-consumers'


def load(name):
    return json.loads((FIXTURES / name).read_text())


class ConsumerTests(unittest.TestCase):
    def test_old_and_current_consumers_preserve_review_meanings(self):
        fixture = load('review.json')
        for descriptor in [load('v0.5.1.json')['contract'], load('v0.6.0.json')['contract'], consumer.contract(ROOT)]:
            with self.subTest(descriptor=descriptor):
                result = consumer.review(fixture, descriptor)
                self.assertEqual(result, fixture['expected'])
                extended = copy.deepcopy(fixture)
                extended['findings'][0]['future_optional'] = {'value': True}
                expected = copy.deepcopy(fixture['expected'])
                expected['ordered_findings'][2]['future_optional'] = {'value': True}
                self.assertEqual(consumer.review(extended, descriptor), expected)

    def test_real_release_packages_consumed_by_old_and_current_readers(self):
        for name in ['release-0.5.1.json', 'release-0.6.0.json']:
            fixture = load(name)
            for descriptor in [load('v0.5.1.json')['contract'], load('v0.6.0.json')['contract'], consumer.contract(ROOT)]:
                with self.subTest(name=name):
                    self.assertEqual(consumer.release(fixture['package'], descriptor), fixture['expected'])
                    extended = copy.deepcopy(fixture['package'])
                    extended['optional_extension'] = 'ignored by supported readers'
                    self.assertEqual(consumer.release(extended, descriptor), fixture['expected'])

    def test_findings_reject_missing_required_fields_and_unknown_enums(self):
        baseline = load('review.json')
        for key in load('v0.6.0.json')['contract']['findings_required']:
            data = copy.deepcopy(baseline)
            del data['findings'][0][key]
            with self.subTest(key=key), self.assertRaises(ValueError):
                consumer.review(data, consumer.contract(ROOT))
        for key, value in [('severity', 'blocker'), ('maturity', 'stable')]:
            data = copy.deepcopy(baseline)
            data['findings'][0][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                consumer.review(data, consumer.contract(ROOT))

    def test_coverage_is_not_silently_dropped_or_promoted(self):
        for key in load('v0.6.0.json')['contract']['coverage_required']:
            data = load('review.json')
            del data['coverage_by_emitter']['review-testing'][key]
            with self.subTest(key=key), self.assertRaises(ValueError):
                consumer.review(data, consumer.contract(ROOT))
        data = load('review.json')
        data['coverage_by_emitter']['review-security'] = copy.deepcopy(data['coverage_by_emitter']['review-testing'])
        before = copy.deepcopy(data)
        consumer.review(data, consumer.contract(ROOT))
        self.assertEqual(data, before)

    def test_required_skip_failure_and_empty_evidence_block_publication(self):
        for status, evidence in [('skipped', 'not run'), ('failed', 'assertion failed'), ('passed', ''), ('passed', '   '), ('passed', '0 tests executed'), ('passed', 'all skipped')]:
            data = load('release-0.6.0.json')['package']
            data['status'] = 'ready'
            data['checks'] = [{'name':'required scope','required':True,'status':status,'evidence':evidence}]
            with self.subTest(status=status, evidence=evidence), self.assertRaises(ValueError):
                consumer.release(data, consumer.contract(ROOT))

    def test_no_release_and_draft_cannot_pass_publish_gate(self):
        data = load('release-0.6.0.json')['package']
        data['decision'] = 'none'
        data['status'] = 'not_required'
        data.pop('publication')
        result = consumer.release(data, consumer.contract(ROOT))
        self.assertFalse(result.get('publishable', True))
        data['decision'] = 'release'
        data['status'] = 'draft'
        self.assertFalse(consumer.release(data, consumer.contract(ROOT)).get('publishable', True))

    def test_required_artifact_and_publication_receipt_are_enforced(self):
        for path in [('artifacts','manifest','status'), ('publication',), ('checks',)]:
            data = load('release-0.6.0.json')['package']
            target = data
            for key in path[:-1]:
                target = target[key]
            del target[path[-1]]
            with self.subTest(path=path), self.assertRaises(ValueError):
                consumer.release(data, consumer.contract(ROOT))

    def test_unknown_release_enums_and_version_actions_are_rejected(self):
        for field, value in [('status','complete'), ('decision','publish'), ('release_channel','')]:
            data = load('release-0.6.0.json')['package']
            data[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                consumer.release(data, consumer.contract(ROOT))
        data = load('release-0.6.0.json')['package']
        data['version_domains']['product']['action'] = 'synchronize'
        with self.assertRaises(ValueError):
            consumer.release(data, consumer.contract(ROOT))

    def test_compatible_schema_minor_and_unknown_major(self):
        data = load('release-0.6.0.json')['package']
        data['status'] = 'ready'
        data['schema_version'] = '1.99.0'
        self.assertTrue(consumer.release(data, consumer.contract(ROOT))['publishable'])
        data['schema_version'] = '2.0.0'
        with self.assertRaises(ValueError):
            consumer.release(data, consumer.contract(ROOT))

    def test_report_preserves_emitter_coverage_and_original_findings(self):
        data = load('review.json')
        data['coverage_by_emitter']['review-security'] = {
            'rule_set':'security-quality','version':'1.3.0','passed':['SEC-001'],
            'waived':[], 'not_applicable':[], 'evidence_limited':[]}
        result = consumer.review(data, consumer.contract(ROOT))
        self.assertEqual(result.get('coverage_by_emitter'), data['coverage_by_emitter'])
        self.assertEqual(result['ordered_findings'], data['expected']['ordered_findings'])
        data['coverage_by_emitter']['review-security']['passed'].append('SEC-002')
        self.assertEqual(result['coverage_by_emitter']['review-security']['passed'], ['SEC-001'])

    def test_only_ready_can_enter_publish_release(self):
        for status in ['draft', 'published']:
            data = load('release-0.6.0.json')['package']
            data['status'] = status
            with self.subTest(status=status):
                self.assertFalse(consumer.release(data, consumer.contract(ROOT))['publishable'])
        data = load('release-0.6.0.json')['package']
        data['status'] = 'ready'
        data.pop('publication')
        self.assertTrue(consumer.release(data, consumer.contract(ROOT))['publishable'])

    def test_contract_drift_is_detected_independently_of_reader(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'specs').mkdir()
            for path in (ROOT / 'specs').glob('*.md'):
                (root / 'specs' / path.name).write_bytes(path.read_bytes())
            mutations = [
                ('findings-list.md', '| **Maturity** | yes |', '| **Maturity** | no |'),
                ('findings-list.md', '| `critical` |', '| `blocker` |'),
                ('findings-list.md', '| `evidence_limited` | yes |', '| `evidence_limited` | no |'),
                ('release-package.md', '| `checks` | array | yes |', '| `checks` | array | no |'),
            ]
            for name, before, after in mutations:
                path = root / 'specs' / name
                original = (ROOT / 'specs' / name).read_text()
                self.assertIn(before, original)
                path.write_text(original.replace(before, after))
                with self.subTest(name=name, before=before), self.assertRaises(ValueError):
                    consumer.check_contract(root, load('v0.6.0.json')['contract'])
                path.write_text(original)



if __name__ == '__main__':
    unittest.main(verbosity=2)

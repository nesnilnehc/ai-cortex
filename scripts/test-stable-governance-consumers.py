#!/usr/bin/env python3
"""Historical/current reference tests for project inputs, Rules and migrations."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('governance', ROOT / 'scripts/stable_governance_consumers.py')
gov = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gov)
FIXTURES = ROOT / 'tests/fixtures/stable-consumers'
BASE = json.loads((FIXTURES / 'governance-v0.6.0.json').read_text())
CASES = json.loads((FIXTURES / 'governance-cases.json').read_text())


class GovernanceTests(unittest.TestCase):
    def catalogs(self):
        return [BASE['registry'], gov.registry(ROOT)]

    def test_current_registry_preserves_old_contract_and_detects_drift(self):
        old = BASE['registry']
        gov.check_compatibility(old, gov.registry(ROOT))
        for key in ['profiles', 'waiver_fields', 'governance_required', 'parameters']:
            changed = copy.deepcopy(old)
            if key == 'parameters':
                changed[key]['architecture.modules'] = 'declared'
            else:
                changed[key] = changed[key][1:]
            with self.subTest(key=key), self.assertRaises(ValueError):
                gov.check_compatibility(old, changed)

    def test_configuration_wins_over_inference_and_never_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '.ai-cortex').mkdir()
            path = root / '.ai-cortex/config.yaml'
            path.write_text(json.dumps({'test_command':'python3 -m unittest','base_branch':'trunk'}))
            before = path.read_bytes()
            result = gov.load_project(root, {'test_command':'pytest','base_branch':'main'})
            self.assertEqual(result, {'test_command':'python3 -m unittest','base_branch':'trunk'})
            self.assertEqual(path.read_bytes(), before)

    def test_nested_configuration_preserves_unoverridden_inference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '.ai-cortex').mkdir()
            (root / '.ai-cortex/config.yaml').write_text(json.dumps({
                'governance':{'profiles':['public-api']}}))
            inferred = {'base_branch':'main','governance':{
                'profiles':[], 'parameters':{'architecture':{'modules':['core']}}}}
            before = copy.deepcopy(inferred)
            result = gov.load_project(root, inferred)
            self.assertEqual(result, {'base_branch':'main','governance':{
                'profiles':['public-api'], 'parameters':{'architecture':{'modules':['core']}}}})
            self.assertEqual(inferred, before)
            gov.validate_config(result, BASE['registry'])

    def test_absent_config_discovers_without_persisting(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(gov.load_project(root, {'test_command':'pytest'}), {'test_command':'pytest'})
            self.assertEqual(list(root.iterdir()), [])

    def test_claude_config_conflict_is_reported_and_malformed_yaml_refused(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            claude = root / 'CLAUDE.md'
            claude.write_text('# Fixture\n```json\n{"base_branch":"trunk"}\n```\n')
            self.assertEqual(gov.load_project(root, {'base_branch':'main'}).get('base_branch'), 'trunk')
            (root / '.ai-cortex').mkdir()
            path = root / '.ai-cortex/config.yaml'
            path.write_text('{"base_branch":"other"}')
            with self.assertRaises(ValueError):
                gov.load_project(root, {})
            path.write_text('{broken')
            with self.assertRaises(ValueError):
                gov.load_project(root, {})

    def test_unknown_profiles_and_parameters_fail_for_both_consumers(self):
        for catalog in self.catalogs():
            for governance in [{'parameters':{}}, {'profiles':['imaginary-profile']},
                               {'profiles':['public-api'], 'parameters':{'unknown':{'budget':1}}}]:
                with self.subTest(governance=governance), self.assertRaises(ValueError):
                    gov.validate_config({'governance':governance}, catalog)
            gov.validate_config({'governance':{'profiles':['public-api'], 'parameters':{'reliability':{'slo':{'availability':'99.9%'}}}}}, catalog)

    def test_parameter_provenance_keeps_missing_evidence_distinct(self):
        for catalog in self.catalogs():
            with self.subTest(catalog=catalog):
                self.assertEqual(gov.parameter('architecture.modules', catalog, {}, {'architecture.modules':['core']}, {}), {'state':'derived','value':['core']})
                self.assertEqual(gov.parameter('architecture.modules', catalog, {}, {}, {}), {'state':'evidence_limited','value':None})
                self.assertEqual(gov.parameter('architecture.allowed_dependencies', catalog, {}, {'architecture.allowed_dependencies':{'core':[]}}, {}), {'state':'baselined','value':{'core':[]}})
                before = {'architecture.allowed_dependencies':{'core':[]}}
                snapshot = copy.deepcopy(before)
                self.assertEqual(gov.parameter('architecture.allowed_dependencies', catalog, {}, {'architecture.allowed_dependencies':{'core':['new']}}, before), {'state':'baseline','value':{'core':[]}})
                self.assertEqual(before, snapshot)
                self.assertEqual(gov.parameter('reliability.slo', catalog, {}, {}, {}), {'state':'evidence_limited','value':None})
                self.assertEqual(gov.parameter('reliability.slo', catalog, {'reliability.slo':0}, {}, {}), {'state':'declared','value':0})

    def test_existing_baseline_cannot_be_replaced_by_new_configuration(self):
        for catalog in self.catalogs():
            self.assertEqual(gov.parameter('architecture.allowed_dependencies', catalog,
                {'architecture.allowed_dependencies':{'core':['new']}}, {},
                {'architecture.allowed_dependencies':{'core':[]}}),
                {'state':'baseline','value':{'core':[]}})
            self.assertEqual(gov.parameter('reliability.slo', catalog,
                {'reliability.slo':None}, {}, {}), {'state':'evidence_limited','value':None})

    def evaluate_waiver(self, waiver, catalog, **extra):
        return gov.waiver_result(waiver, catalog, CASES['population'], CASES['requested'], CASES['approvers'], CASES['clock'], **extra)

    def test_valid_and_historically_pinned_waiver_remain_waived_not_passed(self):
        for catalog in self.catalogs():
            self.assertEqual(self.evaluate_waiver(CASES['waiver'], catalog), {'state':'waived','waiver_id':'WV-fixture'})
        catalog = copy.deepcopy(BASE['registry'])
        catalog['rule_ids'] = []
        self.assertEqual(self.evaluate_waiver(CASES['waiver'], catalog, pinned=BASE['registry']['rule_ids']), {'state':'waived','waiver_id':'WV-fixture'})

    def test_invalid_waivers_never_suppress_findings(self):
        for catalog in self.catalogs():
            for key in CASES['waiver']:
                waiver = copy.deepcopy(CASES['waiver'])
                del waiver[key]
                with self.subTest(missing=key):
                    self.assertEqual(self.evaluate_waiver(waiver, catalog).get('state'), 'finding')
            for key, value in [('expires_at','2026-10-01'), ('created_at','2026-12-01'),
                               ('approved_by','stranger'), ('rule_id','missing@1.0.0/NO-001'),
                               ('scope','**'), ('scope','src/**'), ('scope','src/current/**'), ('compensating_controls',[])]:
                waiver = copy.deepcopy(CASES['waiver'])
                waiver[key] = value
                with self.subTest(key=key, value=value):
                    self.assertEqual(self.evaluate_waiver(waiver, catalog).get('state'), 'finding')

    def test_old_entry_retained_in_major_and_migration_preserves_inputs(self):
        migration = CASES['migration']
        for version in ['1.2.0','1.9.3']:
            payload = {'test_command':'pytest','governance':{'profiles':['public-api']}}
            before = copy.deepcopy(payload)
            old = gov.entry(migration['old'], version, migration, [migration['old'],migration['replacement']])
            new = gov.entry(migration['replacement'], version, migration, [migration['old'],migration['replacement']])
            self.assertEqual(old, new)
            self.assertEqual(old, migration['replacement'])
            gov.validate_config(payload, BASE['registry'])
            self.assertEqual(payload, before)
        with self.assertRaises(ValueError):
            gov.entry(migration['old'], '1.9.3', migration, [migration['replacement']])

    def test_removal_requires_later_major_and_migration_evidence(self):
        migration = copy.deepcopy(CASES['migration'])
        with self.assertRaises(ValueError):
            gov.entry(migration['old'], '2.0.0', migration, [migration['replacement']])
        self.assertEqual(gov.entry(migration['replacement'], '2.0.0', migration, [migration['replacement']]), migration['replacement'])
        for key, value in [('remove_in','1.9.0'), ('deprecated_in','1.2.1'), ('example',''), ('old_consumer_verified',False), ('migration_verified',False)]:
            invalid = copy.deepcopy(migration)
            invalid[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                gov.entry(migration['replacement'], '2.0.0', invalid, [migration['replacement']])


if __name__ == '__main__':
    unittest.main(verbosity=2)

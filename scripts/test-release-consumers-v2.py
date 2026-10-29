#!/usr/bin/env python3
"""Pinned legacy readers and a bounded current contract reader; no external writes."""
import copy
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest

from release_contract_v2 import validate, gate

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/fixtures/release-workflow'
spec = importlib.util.spec_from_file_location('legacy', ROOT / 'scripts/check-stable-consumers.py')
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)
spec = importlib.util.spec_from_file_location('local_workflow', FIXTURES / 'local_workflow.py')
local = importlib.util.module_from_spec(spec)
spec.loader.exec_module(local)


class ConsumerTests(unittest.TestCase):
    def test_fixture_fields_match_spec_when_contract_rows_are_read(self):
        """Covers: AIC-REQ-06#AC14."""
        package = json.loads((FIXTURES / 'package.json').read_text())
        section = (ROOT / 'specs/release-package.md').read_text().split('### 5.8', 1)[1].split('## 6.', 1)[0]
        top = section.split('The 2.0.0 serialization', 1)[0]
        names = []
        for line in top.splitlines():
            if line.startswith('| `'):
                names.extend(re.findall(r'`([a-z_]+)`', line.split('|')[1]))
        self.assertEqual(set(package), set(names))
        records = {'`release_version`': package['release_version'], 'Candidate': package['candidates'][0],
                   'Target': package['targets'][0], 'Check': package['checks'][0]}
        for name, record in records.items():
            record_table = section.split('| Record | Fields and validation |', 1)[1]
            row = next(line for line in record_table.splitlines() if line.startswith('| ' + name + ' |'))
            # Only the declared field list before the first semicolon defines required fields.
            required = set(re.findall(r'`([a-z_]+)`', row.split('|')[2].split(';', 1)[0]))
            with self.subTest(record=name):
                self.assertEqual(set(record), required)

    def test_legacy_reader_and_current_reader_reject_cross_version_execution(self):
        """Covers: AIC-REQ-06#AC14."""
        staged = json.loads((FIXTURES / 'package.json').read_text())
        for name in ['v0.5.1.json', 'v0.6.0.json']:
            descriptor = json.loads((ROOT / 'tests/fixtures/stable-consumers' / name).read_text())['contract']
            old = json.loads((ROOT / 'tests/fixtures/stable-consumers/release-0.6.0.json').read_text())['package']
            with self.subTest(reader=name):
                self.assertEqual(legacy.release(old, descriptor)['version'], old['version'])
                incompatible = copy.deepcopy(old)
                incompatible['schema_version'] = staged['schema_version']
                writes = []
                with self.assertRaisesRegex(ValueError, 'unsupported schema major'):
                    legacy.release(incompatible, descriptor)
                    writes.append('provider mutation')
                self.assertEqual(writes, [])
                self.assertFalse(validate(old))

    def test_explicit_migration_preserves_known_facts_without_inventing_build_evidence(self):
        """Covers: AIC-REQ-06#AC14."""
        old_path = ROOT / 'tests/fixtures/stable-consumers/release-0.6.0.json'
        original_bytes = old_path.read_bytes()
        old = json.loads(original_bytes)['package']
        migrated = local.migrate_preview(old, release_id='explicit-fixture-import')
        self.assertTrue(validate(migrated))
        self.assertEqual(migrated['release_version']['value'], old['version'])
        self.assertEqual(migrated['candidates'][0]['source_revision'], old['commit'])
        self.assertIsNone(migrated['candidates'][0]['build_identity'])
        self.assertEqual(migrated['candidates'][0]['artifacts'], [])
        self.assertEqual(migrated['targets'][0]['status'], 'pending')
        self.assertFalse(gate(migrated, 'imported', 'upload', True, True))
        with tempfile.TemporaryDirectory() as directory:
            workflow = local.Workflow(Path(directory), migrated)
            self.assertEqual(workflow.upload('imported', authorized=True), 'blocked')
            self.assertEqual(list(Path(directory).iterdir()), [])
        self.assertEqual(old_path.read_bytes(), original_bytes)


if __name__ == '__main__':
    unittest.main()

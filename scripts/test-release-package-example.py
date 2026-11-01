#!/usr/bin/env python3
"""Check the static Release Package example against its Spec and artifact bytes."""
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / 'tests/fixtures/release-workflow'


class ExampleTests(unittest.TestCase):
    def test_fixture_fields_match_spec_when_contract_rows_are_read(self):
        """Covers: AIC-REQ-06#AC2 and AIC-REQ-06#AC7; static asset consistency."""
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

    def test_example_artifact_identities_match_actual_bytes(self):
        """Covers: AIC-REQ-06#AC2 and AIC-REQ-06#AC7; no workflow execution."""
        package = json.loads((FIXTURES / 'package.json').read_text())
        for candidate in package['candidates']:
            for artifact in candidate['artifacts']:
                with self.subTest(candidate=candidate['id'], artifact=artifact['id']):
                    content = (FIXTURES / artifact['location']).read_bytes()
                    self.assertEqual(artifact['identity'], 'sha256:' + hashlib.sha256(content).hexdigest())


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""Verify retired release assets cannot be discovered through current catalogues."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
RETIRED = {'build-artifacts', 'prepare-release', 'publish-release', 'announce-release', 'changelog-video'}

class RetirementTests(unittest.TestCase):
    """Covers: ADR-0017, removal and retained capability boundaries."""
    def test_removed_capabilities_and_contract_are_not_discoverable(self):
        for name in RETIRED:
            self.assertFalse((ROOT / 'skills' / name).exists(), name)
        self.assertFalse((ROOT / 'specs/release-package.md').exists())
        for path in ['skills/INDEX.md', 'specs/INDEX.md']:
            text = (ROOT / path).read_text()
            for name in RETIRED:
                self.assertNotIn(f'./{name}/', text)
        for number in ['05', '06', '07']:
            self.assertFalse((ROOT / f'docs/requirements-planning/AIC-REQ-{number}.md').exists())

    def test_active_provenance_and_website_have_no_retired_members(self):
        for path in ['skills/PROVENANCE.json', 'website/explore/skill-provenance.json', 'website/explore/skill-metadata.json']:
            data = json.loads((ROOT / path).read_text())
            self.assertFalse(RETIRED.intersection(data['skills']), path)
        groups = json.loads((ROOT / 'website/explore/classification.json').read_text())['groups']
        self.assertFalse(RETIRED.intersection(s for g in groups for s in g['skillIds']))
        for edge in json.loads((ROOT / 'website/explore/skill-edges.json').read_text()):
            self.assertNotIn(edge['from'], RETIRED)
            self.assertNotIn(edge['to'], RETIRED)
        for path in ['website/index.html', 'website/zh.html']:
            for name in RETIRED:
                self.assertNotIn(f'/skills/{name}', (ROOT / path).read_text())

    def test_unrelated_capabilities_remain(self):
        for name in ['eli5', 'ponytail', 'commit-work', 'publish-nats-message']:
            self.assertTrue((ROOT / 'skills' / name / 'SKILL.md').is_file(), name)
        notices = (ROOT / 'docs/references/THIRD_PARTY_NOTICES.md').read_text()
        self.assertIn('Copyright (c) 2026 Leonardo Flores', notices)
        self.assertIn('## eli5', notices)
        self.assertIn('## ponytail', notices)

if __name__ == '__main__':
    unittest.main()

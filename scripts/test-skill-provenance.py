#!/usr/bin/env python3
"""Exercise provenance markers and generator integration without network access."""
import hashlib
import importlib.util
import json
import pathlib
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('skill_provenance', ROOT / 'scripts/skill-provenance.py')
provenance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(provenance)
spec2 = importlib.util.spec_from_file_location('skill_index', ROOT / 'scripts/sync-skills-index.py')
index = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(index)


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.skills = self.root / 'skills'
        self.skills.mkdir()
        for name in ('adapted','native','original','unknown'):
            folder = self.skills / name
            folder.mkdir()
            (folder / 'SKILL.md').write_text('---\nname: '+name+'\ndescription: Example.\n---\n')
        digest=hashlib.sha256((self.skills/'original'/'SKILL.md').read_bytes()).hexdigest()
        (self.root/'NOTICE').write_text('Fixture license notice')
        prefix='    license: MIT\n    notice: NOTICE\n'
        (self.skills / 'SOURCES.yaml').write_text('skills:\n  adapted:\n    origin: vendored-derived\n'+prefix+'    modifications:\n      - Local adaptation\n  original:\n    origin: vendored-derived\n'+prefix+'    upstream:\n      ref: '+('a'*40)+'\n      skill_digest: sha256:'+digest+'\n    modifications: []\n')
        (self.root / 'evidence.md').write_text('Documented provenance')
        self.manifest = self.skills / 'PROVENANCE.json'
        data = (self.skills / 'original' / 'SKILL.md').read_bytes()
        self.records = {'schema_version':1,'skills':{
            'adapted':{'classification':'third_party_adapted','evidence':'skills/SOURCES.yaml#adapted','reviewed_at':'2026-10-28'},
            'native':{'classification':'native','evidence':'evidence.md','reviewed_at':'2026-10-28'},
            'original':{'classification':'third_party_original','evidence':'skills/SOURCES.yaml#original',
                        'reviewed_at':'2026-10-28','upstream_ref':'a'*40,'upstream_files':{'SKILL.md':hashlib.sha256(data).hexdigest()}},
        }}
        self.save()

    def save(self): self.manifest.write_text(json.dumps(self.records))

    def test_three_evidenced_types_and_unknown_render(self):
        labels = provenance.load(self.root, self.skills)
        self.assertEqual(labels['unknown']['classification'],'unverified')
        self.assertEqual(labels['adapted']['classification'],'third_party_adapted')
        self.assertEqual(labels['native']['classification'],'native')
        self.assertEqual(labels['original']['classification'],'third_party_original')
        rendered=index.render(index.collect(self.skills), labels)
        for text in ('Third-party adapted','Third-party original','AI Cortex original'):
            self.assertIn(text,rendered)
        self.assertNotIn('Unverified', rendered)
        self.assertIn('SOURCES.yaml#adapted',rendered)

    def test_changed_or_extra_upstream_file_rejected(self):
        (self.skills/'original'/'SKILL.md').write_text('changed')
        with self.assertRaisesRegex(provenance.ProvenanceError,'do not match'):
            provenance.load(self.root,self.skills)
        (self.skills/'original'/'SKILL.md').write_text('---\nname: original\ndescription: Example.\n---\n')
        (self.skills/'original'/'extra.txt').write_text('not upstream')
        with self.assertRaisesRegex(provenance.ProvenanceError,'do not match'):
            provenance.load(self.root,self.skills)

    def test_invalid_missing_and_conflicting_records_rejected(self):
        for mutation in ('unknown_value','missing_evidence','absent_skill','missing_registry','missing_file_map','missing_date','source_conflict','unregistered_source'):
            with self.subTest(mutation=mutation):
                saved=json.loads(json.dumps(self.records))
                if mutation=='unknown_value': self.records['skills']['adapted']['classification']='native-ish'
                if mutation=='missing_evidence': self.records['skills']['native']['evidence']='missing.md'
                if mutation=='absent_skill': self.records['skills']['deleted']={'classification':'native','evidence':'evidence.md'}
                if mutation=='missing_registry': self.records['skills']['adapted']['evidence']='evidence.md'
                if mutation=='missing_file_map': self.records['skills']['original'].pop('upstream_files')
                if mutation=='missing_date': self.records['skills']['native'].pop('reviewed_at')
                if mutation=='source_conflict': self.records['skills']['adapted']={'classification':'native','evidence':'evidence.md','reviewed_at':'2026-10-28'}
                if mutation=='unregistered_source': self.records['skills'].pop('adapted')
                self.save()
                with self.assertRaises(provenance.ProvenanceError): provenance.load(self.root,self.skills)
                self.records=saved
        self.save()

    def test_duplicate_json_keys_rejected(self):
        self.manifest.write_text('{"schema_version": 1, "schema_version": 1, "skills": {}}')
        with self.assertRaises(provenance.ProvenanceError): provenance.load(self.root,self.skills)

    def test_original_with_reported_local_modifications_is_rejected(self):
        path=self.skills/'SOURCES.yaml'
        path.write_text(path.read_text().replace('modifications: []','modifications:\n      - Changed local behavior'))
        with self.assertRaisesRegex(provenance.ProvenanceError, 'modifications'):
            provenance.load(self.root,self.skills)

    def test_adapted_requires_described_modifications(self):
        path=self.skills/'SOURCES.yaml'
        path.write_text(path.read_text().replace('modifications:\n      - Local adaptation','modifications: []'))
        with self.assertRaisesRegex(provenance.ProvenanceError, 'modifications'):
            provenance.load(self.root,self.skills)

    def test_external_claim_requires_license_and_notice(self):
        path=self.skills/'SOURCES.yaml'
        path.write_text(path.read_text().replace('    license: MIT\n','',1))
        with self.assertRaisesRegex(provenance.ProvenanceError, 'license'):
            provenance.load(self.root,self.skills)


if __name__ == '__main__': unittest.main(verbosity=2)

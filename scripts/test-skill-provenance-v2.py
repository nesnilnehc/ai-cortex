#!/usr/bin/env python3
"""Exercise reviewed provenance contracts using isolated, synthetic attestations."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import skill_provenance_v2 as provenance


def sha(data):
    return hashlib.sha256(data).hexdigest()


class ProvenanceV2Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skills = self.root / 'skills'
        self.skill = self.skills / 'alpha'
        self.skill.mkdir(parents=True)
        (self.skill / 'SKILL.md').write_text('---\nname: alpha\nversion: 1.0.0\ndescription: Example.\n---\nExample\n')
        (self.root / 'creation.md').write_text('# Creation\nWritten for this synthetic requirement.\n')
        (self.root / 'article.md').write_text('# Source\nSynthetic source evidence.\n')
        self.registry = {'skills': {}, 'references': {}}
        self.record = {
            'classification': 'native', 'version': '1.0.0',
            'reviewed_files': {'SKILL.md': sha((self.skill / 'SKILL.md').read_bytes())},
            'reviewed_evidence': {'creation.md': sha((self.root / 'creation.md').read_bytes())},
            'creation': {'kind': 'requirement', 'evidence': {'path': 'creation.md'}},
            'sources': [], 'evidence': [{'path': 'creation.md'}, {'path': 'confirmation.json'}],
        }
        self.confirm()

    def confirm(self):
        digest = provenance.subject_digest('alpha', self.record, self.registry)
        self.record['decision'] = {
            'maintainer': 'Synthetic test maintainer', 'confirmed_at': '2026-10-28',
            'action': 'confirmed', 'classification': self.record['classification'],
            'rationale': 'Synthetic fixture only; not a real authorship claim.',
            'evidence': [{'path': 'confirmation.json'}], 'subject_digest': digest,
        }
        (self.root / 'confirmation.json').write_text(json.dumps(self.record['decision']))

    def validate(self):
        return provenance.validate_record(self.root, 'alpha', self.record, self.registry)

    def test_inventory_rejects_tracked_file_through_replaced_parent_link(self):
        # Covers: AIC-REQ-08#AC1.
        nested = self.skill / 'nested'
        nested.mkdir()
        (nested / 'file.txt').write_text('distributed')
        (self.root / '.gitignore').write_text('nested\n')
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['git', '-C', str(self.root), 'add', '-f', 'skills/alpha/nested/file.txt'], check=True)
        outside = self.root / 'outside'
        outside.mkdir()
        (outside / 'file.txt').write_text('outside distribution')
        (nested / 'file.txt').unlink()
        nested.rmdir()
        nested.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(provenance.ProvenanceError, 'parent|symlink'):
            provenance.inventory(self.skill)

    def test_git_attempt_is_bounded_and_timeout_is_actionable(self):
        # Covers: AIC-REQ-08#AC7.
        from unittest.mock import patch
        with patch.object(provenance.subprocess, 'run', side_effect=subprocess.TimeoutExpired(['git'], 30)) as run:
            with self.assertRaisesRegex(provenance.ProvenanceError, 'GIT_TIMEOUT'):
                provenance.run_git(['git', 'status'], capture_output=True)
            self.assertEqual(run.call_args.kwargs['timeout'], 30)

    def test_validation_names_skill_when_nested_record_is_invalid(self):
        # Covers: AIC-REQ-08#AC1.
        self.record['decision']['maintainer'] = ''
        with self.assertRaises(provenance.ProvenanceError) as error:
            self.validate()
        self.assertEqual(error.exception.skill, 'alpha')
        self.assertIn('maintainer', error.exception.message)

    def test_native_requires_creation_and_actual_confirmation_record(self):
        # Covers: AIC-REQ-08#AC2.
        self.assertEqual(self.validate()['classification'], 'native')
        for field in ('creation', 'decision'):
            with self.subTest(field=field):
                original = self.record.pop(field)
                with self.assertRaises(provenance.ProvenanceError):
                    self.validate()
                self.record[field] = original
        (self.root / 'confirmation.json').write_text('{}')
        with self.assertRaisesRegex(provenance.ProvenanceError, 'confirmation'):
            self.validate()

    def test_every_distributed_file_is_bound(self):
        # Covers: AIC-REQ-08#AC5.
        for action in ('change', 'add', 'remove'):
            with self.subTest(action=action):
                original = (self.skill / 'SKILL.md').read_bytes()
                if action == 'change':
                    (self.skill / 'SKILL.md').write_text('changed')
                elif action == 'add':
                    (self.skill / 'extra').write_text('extra')
                else:
                    (self.skill / 'SKILL.md').unlink()
                with self.assertRaises(provenance.ProvenanceError):
                    self.validate()
                (self.skill / 'SKILL.md').write_bytes(original)
                (self.skill / 'extra').unlink(missing_ok=True)

    def test_evidence_and_category_changes_invalidate_confirmation(self):
        # Covers: AIC-REQ-08#AC4.
        for action in ('evidence', 'category', 'reference'):
            with self.subTest(action=action):
                saved = copy.deepcopy(self.record)
                if action == 'evidence':
                    (self.root / 'creation.md').write_text('changed')
                elif action == 'category':
                    self.record['classification'] = 'third_party_adapted'
                else:
                    self.record['creation']['evidence']['anchor'] = 'missing'
                with self.assertRaises(provenance.ProvenanceError):
                    self.validate()
                self.record = saved
                (self.root / 'creation.md').write_text('# Creation\nWritten for this synthetic requirement.\n')

    def article(self, role='creative_reference'):
        self.registry['references']['article-a'] = {
            'url': 'https://example.org/article', 'title': 'Synthetic article',
            'accessed_at': '2026-10-28', 'kind': 'article', 'evidence': {'path': 'article.md'},
        }
        self.record['sources'] = [{'id': 'reference:article-a', 'role': role}]
        self.record['reviewed_evidence']['article.md'] = sha((self.root / 'article.md').read_bytes())

    def test_article_rewrite_and_tool_only_reference(self):
        # Covers: AIC-REQ-08#AC3.
        self.article()
        self.record['classification'] = 'third_party_adapted'
        self.record.pop('creation')
        self.record['reviewed_evidence'].pop('creation.md')
        self.record['evidence'] = [{'path': 'article.md'}, {'path': 'confirmation.json'}]
        self.record['sources'][0]['adaptation'] = 'Rewrote the workflow from the article.'
        self.confirm()
        self.assertEqual(self.validate()['classification'], 'third_party_adapted')
        self.registry['references']['article-a']['url'] = 'https://example.org/changed'
        with self.assertRaisesRegex(provenance.ProvenanceError, 'digest'):
            self.validate()

    def test_corrected_decision_binds_changed_category_and_keeps_review_identity(self):
        # Covers: AIC-REQ-08#AC4.
        self.article()
        self.record['classification'] = 'third_party_adapted'
        self.record.pop('creation')
        self.record['reviewed_evidence'].pop('creation.md')
        self.record['evidence'] = [{'path': 'article.md'}, {'path': 'confirmation.json'}]
        self.record['sources'][0]['adaptation'] = 'Maintainer disclosed the article-informed workflow.'
        with self.assertRaises(provenance.ProvenanceError):
            self.validate()
        self.confirm()
        self.record['decision'].update(action='corrected', rationale='Correct the original claim after identifying the creative reference.')
        (self.root / 'confirmation.json').write_text(json.dumps(self.record['decision']))
        result = self.validate()
        self.assertEqual(result['classification'], 'third_party_adapted')
        self.assertEqual(result['decision']['action'], 'corrected')
        self.assertEqual(result['decision']['maintainer'], 'Synthetic test maintainer')
        self.assertEqual(result['decision']['confirmed_at'], '2026-10-28')
        self.assertEqual(result['decision']['subject_digest'], provenance.subject_digest('alpha', self.record, self.registry))

    def test_withdrawn_decision_cannot_make_a_record_ready(self):
        # Covers: AIC-REQ-08#AC4.
        self.record['decision']['action'] = 'withdrawn'
        (self.root / 'confirmation.json').write_text(json.dumps(self.record['decision']))
        with self.assertRaisesRegex(provenance.ProvenanceError, 'confirmation decision'):
            self.validate()

    def test_tool_documentation_only_does_not_disqualify_native(self):
        # Covers: AIC-REQ-08#AC2.
        self.article('tool_lookup')
        self.registry['references']['article-a']['kind'] = 'tool_documentation'
        self.confirm()
        self.assertEqual(self.validate()['classification'], 'native')

    def test_reject_false_tool_lookup_and_unknown_fields(self):
        # Covers: AIC-REQ-08#AC3.
        self.article('tool_lookup')
        self.confirm()
        with self.assertRaises(provenance.ProvenanceError):
            self.validate()
        self.record['sources'] = []
        self.record['unexpected'] = 'ignored?'
        self.confirm()
        with self.assertRaises(provenance.ProvenanceError):
            self.validate()

    def test_upstream_identity_requires_exact_files_and_license(self):
        # Covers: AIC-REQ-08#AC5.
        self.record['classification'] = 'third_party_original'
        self.record.pop('creation')
        self.record['reviewed_evidence'] = {'article.md': sha((self.root / 'article.md').read_bytes())}
        self.record['evidence'] = [{'path': 'article.md'}, {'path': 'confirmation.json'}]
        (self.root / 'NOTICE').write_text('MIT fixture notice')
        self.registry['skills']['alpha'] = {
            'local_path': 'skills/alpha', 'local_version': '1.0.0', 'update_policy': 'reviewed-port',
            'origin': 'vendored-derived', 'license': 'MIT', 'notice': 'NOTICE',
            'upstream': {'repository': 'https://example.org/fixture.git', 'path': 'skills/alpha', 'tree': 'sha1:'+'b'*40, 'ref': 'a' * 40, 'skill_digest': 'sha256:' + self.record['reviewed_files']['SKILL.md']},
            'modifications': [],
        }
        self.record['sources'] = [{'id': 'skill:alpha', 'role': 'copied_upstream'}]
        self.record['reviewed_evidence']['NOTICE'] = sha((self.root / 'NOTICE').read_bytes())
        self.record['upstream_ref'] = 'a' * 40
        self.record['upstream_files'] = dict(self.record['reviewed_files'])
        self.confirm()
        self.assertEqual(self.validate()['classification'], 'third_party_original')
        source = self.registry['skills']['alpha']
        for field, bad in [('local_path', 'skills/wrong'), ('local_version', '9.0.0'), ('update_policy', 'auto-install')]:
            with self.subTest(field=field):
                old = source[field]
                source[field] = bad
                self.confirm()
                with self.assertRaises(provenance.ProvenanceError):
                    self.validate()
                source[field] = old
        for field, bad in [('repository', 'https://user:secret@example.org/fixture.git'), ('tree', 'floating'), ('path', '../outside')]:
            with self.subTest(field=field):
                old = source['upstream'][field]
                source['upstream'][field] = bad
                self.confirm()
                with self.assertRaises(provenance.ProvenanceError):
                    self.validate()
                source['upstream'][field] = old
        self.confirm()
        self.registry['skills']['alpha']['modifications'] = ['Local change']
        with self.assertRaises(provenance.ProvenanceError):
            self.validate()
        self.registry['skills']['alpha']['modifications'] = []
        (self.root / 'NOTICE').unlink()
        with self.assertRaises(provenance.ProvenanceError):
            self.validate()

    def test_paths_symlinks_and_anchors_are_checked(self):
        # Covers: AIC-REQ-08#AC7.
        for path in ('../outside', '/etc/passwd', 'creation.md/../article.md', 'bad\\path'):
            with self.subTest(path=path), self.assertRaises(provenance.ProvenanceError):
                provenance.evidence_path(self.root, {'path': path})
        with self.assertRaises(provenance.ProvenanceError):
            provenance.evidence_path(self.root, {'path': 'creation.md', 'anchor': 'absent'})
        self.assertEqual(provenance.evidence_path(self.root, {'path': 'creation.md', 'anchor': 'creation'}), (self.root / 'creation.md').resolve())
        (self.skill / 'link').symlink_to(self.root / 'creation.md')
        with self.assertRaises(provenance.ProvenanceError):
            provenance.inventory(self.skill)

    def test_inventory_excludes_git_ignored_cache_but_not_distributed_additions(self):
        # Covers: AIC-REQ-08#AC1.
        self.git('init', '-q')
        (self.root/'.gitignore').write_text('**/__pycache__/\n.DS_Store\n')
        cache = self.skill/'__pycache__'
        cache.mkdir()
        (cache/'generated.pyc').write_bytes(b'ephemeral bytecode')
        (self.skill/'.DS_Store').write_bytes(b'finder metadata')
        self.assertEqual(provenance.inventory(self.skill), self.record['reviewed_files'])
        self.assertEqual(self.validate()['classification'], 'native')
        (self.skill/'new-asset.txt').write_text('distributed addition')
        with self.assertRaises(provenance.ProvenanceError):
            self.validate()

    def test_existing_contained_links_are_bound_without_materializing_them(self):
        # Covers: AIC-REQ-08#AC1.
        target = self.skill / 'references' / 'input.json'
        target.parent.mkdir()
        target.write_text('{"example": true}')
        (self.skill / 'assets').mkdir()
        link = self.skill / 'assets' / 'example.json'
        link.symlink_to('../references/input.json')
        self.record['reviewed_files'] = provenance.inventory(self.skill)
        self.record['reviewed_links'] = {'assets/example.json': '../references/input.json'}
        self.confirm()
        self.assertEqual(self.validate()['classification'], 'native')
        self.assertTrue(link.is_symlink())
        self.assertIn('references/input.json', self.record['reviewed_files'])
        target.write_text('{"example": false}')
        with self.assertRaises(provenance.ProvenanceError):
            self.validate()
        target.write_text('{"example": true}')
        self.record['reviewed_links'] = {}
        self.confirm()
        with self.assertRaises(provenance.ProvenanceError):
            self.validate()
        link.unlink()
        link.symlink_to('../../../creation.md')
        with self.assertRaises(provenance.ProvenanceError):
            provenance.inventory(self.skill)

    def test_confirmation_is_not_its_own_subject(self):
        # Covers: AIC-REQ-08#AC4.
        self.record['reviewed_evidence']['confirmation.json'] = sha((self.root / 'confirmation.json').read_bytes())
        with self.assertRaisesRegex(provenance.ProvenanceError, 'confirmation'):
            self.validate()

    def test_entire_catalogue_requires_records_and_no_unknown_category(self):
        # Covers: AIC-REQ-08#AC1.
        manifest = self.skills / 'PROVENANCE.json'
        (self.skills / 'SOURCES.yaml').write_text('skills: {}\nreferences: {}\n')
        manifest.write_text(json.dumps({'schema_version': 2, 'skills': {'alpha': self.record}}))
        self.assertEqual(set(provenance.load(self.root, self.skills)), {'alpha'})
        for records in ({}, {'alpha': dict(self.record, classification='unverified')}, {'alpha': self.record, 'extra': self.record}):
            manifest.write_text(json.dumps({'schema_version': 2, 'skills': records}))
            with self.assertRaises(provenance.ProvenanceError):
                provenance.load(self.root, self.skills)

    def test_review_packet_rejects_malformed_candidate_without_runtime_crash(self):
        # Covers: AIC-REQ-08#AC4.
        for candidate in (None, [], {'classification': []}, {'classification': {}}):
            with self.subTest(candidate=candidate):
                if isinstance(candidate, dict):
                    packet = provenance.review_packet(self.root, 'alpha', candidate, self.registry)
                    self.assertIn('Needs source investigation', packet)
                else:
                    with self.assertRaises(provenance.ProvenanceError):
                        provenance.review_packet(self.root, 'alpha', candidate, self.registry)

    def test_review_packet_handles_missing_decision_without_writing(self):
        # Covers: AIC-REQ-08#AC4.
        self.record.pop('decision')
        before = sorted(str(p) for p in self.root.rglob('*'))
        packet = provenance.review_packet(self.root, 'alpha', self.record, self.registry)
        self.assertIn('Recommendation', packet)
        self.assertIn(provenance.subject_digest('alpha', self.record, self.registry), packet)
        self.assertIn('Missing facts', packet)
        self.assertIn('maintainer', packet.lower())
        self.assertNotIn('automatically confirmed', packet)
        self.assertEqual(before, sorted(str(p) for p in self.root.rglob('*')))

    def test_malformed_nested_values_are_actionable_errors(self):
        # Covers: AIC-REQ-08#AC1.
        mutations = [
            lambda r: r.update(classification=[]),
            lambda r: r['decision'].update(action=[]),
            lambda r: r['decision'].update(evidence='not-an-array'),
            lambda r: r.update(sources=[{'id': 'reference:x', 'role': []}]),
            lambda r: r.update(reviewed_evidence=[]),
        ]
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                saved = copy.deepcopy(self.record)
                mutate(self.record)
                with self.assertRaises(provenance.ProvenanceError):
                    self.validate()
                self.record = saved

    def test_inline_comments_are_rejected_in_supported_registry_grammar(self):
        # Covers: AIC-REQ-08#AC7.
        with self.assertRaises(provenance.ProvenanceError):
            provenance.parse_registry('skills: {} # comment\n')

    def test_coverage_detects_missing_website_records(self):
        # Covers: AIC-REQ-08#AC1.
        web = self.root / 'website' / 'explore'
        (web / 'locales').mkdir(parents=True)
        (web / 'skill-metadata.json').write_text(json.dumps({'skills': {}, 'groupOrder': ['build']}))
        for lang in ('en', 'zh'):
            (web / 'locales' / (lang+'.json')).write_text(json.dumps({'skills': {}}))
        (web / 'classification.json').write_text(json.dumps({'groups': [{'id': 'map-build', 'skillIds': []}]}))
        (web / 'skill-edges.json').write_text('[]')
        (web / 'support-scopes.json').write_text('[]')
        with self.assertRaisesRegex(provenance.ProvenanceError, 'coverage'):
            provenance.validate_coverage(self.root, {'alpha': self.record})
        (web / 'skill-metadata.json').write_text(json.dumps({'skills': {'alpha': {'id': 'alpha', 'owner': 'build', 'sourcePaths': ['skills/alpha/SKILL.md'], 'sourceHashes': {'skills/alpha/SKILL.md': self.record['reviewed_files']['SKILL.md']}}}, 'groupOrder': ['build']}))
        for lang in ('en', 'zh'):
            (web / 'locales' / (lang+'.json')).write_text(json.dumps({'contexts': {'build': {'skills': ['alpha']}}, 'extras': {'lookup': [{'id': 'build', 'skills': ['alpha']}]}, 'skills': {'alpha': {'name': 'Alpha', 'purpose': 'Example', 'when': 'Use it', 'provide': 'Topic', 'use': 'Ask', 'result': 'Explanation'}}}))
        (web / 'classification.json').write_text(json.dumps({'groups': [{'id': 'map-build', 'skillIds': ['alpha']}]}))
        self.assertTrue(provenance.validate_coverage(self.root, {'alpha': self.record}))

    def git(self, *args):
        result = subprocess.run(['git', '-C', str(self.root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', '-c', 'core.hooksPath=/dev/null', *args], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def test_pinned_evidence_uses_exact_committed_content(self):
        # Covers: AIC-REQ-08#AC1.
        self.git('init', '-q')
        (self.skills / 'SOURCES.yaml').write_text('skills: {}\n')
        (self.skills / 'PROVENANCE.json').write_text(json.dumps({'schema_version': 2, 'skills': {'alpha': self.record}}))
        self.git('add', '.')
        self.git('-c', 'commit.gpgsign=false', 'commit', '-qm', 'Synthetic reviewed source')
        revision = self.git('rev-parse', 'HEAD')
        records = {'alpha': self.record}
        self.assertTrue(provenance.verify_revision(self.root, records, revision))
        projection = provenance.export_public(self.root, records, revision)
        self.assertEqual(projection['source_revision'], revision)
        self.assertEqual(projection['skills']['alpha']['classification'], 'native')
        self.assertTrue(all('/blob/'+revision+'/' in url for url in projection['skills']['alpha']['evidence']))
        self.assertNotIn('maintainer', json.dumps(projection))
        (self.root / 'creation.md').write_text('uncommitted change')
        with self.assertRaisesRegex(provenance.ProvenanceError, 'committed'):
            provenance.verify_revision(self.root, records, revision)
        with self.assertRaises(provenance.ProvenanceError):
            provenance.verify_revision(self.root, records, 'f'*40)

    def setup_site(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('preview_index', Path(__file__).with_name('sync-skills-index.py'))
        index = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(index)
        index.ROOT = self.root
        index.SKILLS_DIR = self.skills
        index.INDEX = self.skills / 'INDEX.md'
        web = self.root / 'website' / 'explore'
        (web / 'locales').mkdir(parents=True)
        (self.skills / 'SOURCES.yaml').write_text('skills: {}\n')
        (self.skills / 'PROVENANCE.json').write_text(json.dumps({'schema_version': 2, 'skills': {'alpha': self.record}}))
        (web / 'skill-metadata.json').write_text(json.dumps({'skills': {'alpha': {'id': 'alpha', 'owner': 'build', 'sourcePaths': ['skills/alpha/SKILL.md'], 'sourceHashes': {'skills/alpha/SKILL.md': self.record['reviewed_files']['SKILL.md']}}}, 'groupOrder': ['build']}))
        for lang in ('en', 'zh'):
            (web / 'locales' / (lang+'.json')).write_text(json.dumps({'skills': {'alpha': {'name': 'Alpha', 'purpose': 'Explain', 'when': 'Use', 'provide': 'Topic', 'use': 'Ask', 'result': 'Explanation'}}, 'contexts': {'build': {'skills': ['alpha']}}, 'extras': {'lookup': [{'id': 'build', 'skills': ['alpha']}]}, 'classification': {'map-build': {'name': 'Build', 'purpose': 'Build'}}, 'provenance': {'labels': {'native': 'AI Cortex original', 'third_party_original': 'Third-party original', 'third_party_adapted': 'Third-party adapted'}, 'evidence': 'View evidence for {0}', 'directoryTitle': 'Skills'}}))
        (web / 'classification.json').write_text(json.dumps({'groups': [{'id': 'map-build', 'skillIds': ['alpha']}]}))
        (web / 'skill-edges.json').write_text('[]')
        (web / 'support-scopes.json').write_text('[]')
        for path in (self.root/'website/index.html', self.root/'website/zh.html', web/'index.html', web/'zh.html'):
            path.write_text('<main><!-- provenance:start --><!-- provenance:end --></main>')
        return index

    def test_preview_generation_is_isolated_and_not_delivery_ready(self):
        # Covers: AIC-REQ-08#AC1.
        index = self.setup_site()
        before = {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        destination = self.root.parent / (self.root.name+'-preview')
        import shutil
        self.addCleanup(lambda: shutil.rmtree(destination, ignore_errors=True))
        self.assertEqual(index.main(['--preview-dir', str(destination)]), 0)
        data = json.loads((destination/'website/explore/skill-provenance.json').read_text())
        self.assertFalse(data['delivery_ready'])
        self.assertIsNone(data['source_revision'])
        page = (destination/'website/index.html').read_text()
        self.assertNotIn('data-provenance="native"', page)
        self.assertNotIn('provenance-evidence/confirmation.json', page)
        self.assertTrue((destination/'website/provenance-evidence/confirmation.json').is_file())
        self.assertEqual(before, {str(p.relative_to(self.root)): p.read_bytes() for p in self.root.rglob('*') if p.is_file()})
        self.assertEqual(index.main(['--preview-dir', str(destination)]), 1)
        self.assertEqual(index.main(['--preview-dir', str(destination), '--check']), 2)

    def committed_site(self):
        index = self.setup_site()
        self.git('init', '-q')
        self.git('add', '.')
        self.git('-c', 'commit.gpgsign=false', 'commit', '-qm', 'Synthetic reviewed source before generated outputs')
        revision = self.git('rev-parse', 'HEAD')
        (self.root / 'website/explore/source-manifest.json').write_text(json.dumps({'assetsRevision': revision, 'provenanceRevision': revision}))
        return index

    def test_canonical_generation_rejects_legacy_schema_without_writing(self):
        # Covers: AIC-REQ-08#AC1, AIC-REQ-08#AC7.
        import contextlib
        import io
        import shutil
        index = self.setup_site()
        (self.skills / 'INDEX.md').write_text('previous reviewed catalogue')
        (self.skills / 'PROVENANCE.json').write_text(json.dumps({'schema_version': 1, 'skills': {}}))
        (self.root / 'scripts').mkdir()
        shutil.copy(Path(__file__).with_name('skill-provenance.py'), self.root / 'scripts/skill-provenance.py')
        error = io.StringIO()
        with contextlib.redirect_stderr(error):
            self.assertEqual(index.main([]), 1)
        self.assertIn('MIGRATION_REQUIRED', error.getvalue())
        self.assertEqual((self.skills / 'INDEX.md').read_text(), 'previous reviewed catalogue')

    def test_canonical_generation_checks_all_outputs_and_rejects_dirty_evidence(self):
        # Covers: AIC-REQ-08#AC1.
        index = self.committed_site()
        self.assertEqual(index.main([]), 0)
        self.assertEqual(index.main(['--check']), 0)
        pages = [self.root/'skills/INDEX.md', self.root/'website/explore/skill-provenance.json', self.root/'website/index.html', self.root/'website/zh.html', self.root/'website/explore/index.html', self.root/'website/explore/zh.html']
        before = {p: p.read_bytes() for p in pages}
        (self.root/'creation.md').write_text('Changed after confirmation')
        self.assertEqual(index.main([]), 1)
        self.assertEqual(before, {p: p.read_bytes() for p in pages})

    def test_interrupted_output_is_detected_and_regeneration_recovers(self):
        # Covers: AIC-REQ-08#AC1.
        from unittest.mock import patch
        index = self.committed_site()
        old = self.root/'skills/INDEX.md'
        old.write_text('previous index')
        original = Path.replace
        calls = []
        def interrupted(path, target):
            calls.append(target)
            if len(calls) == 2:
                raise OSError('Synthetic output interruption')
            return original(path, target)
        with patch.object(Path, 'replace', interrupted):
            self.assertEqual(index.main([]), 1)
        self.assertNotEqual(old.read_text(), 'previous index')
        self.assertEqual(index.main(['--check']), 1)
        self.assertEqual(index.main([]), 0)
        self.assertEqual(index.main(['--check']), 0)
        self.assertFalse(list(self.root.rglob('.*.json.*')))

    def test_asset_pin_is_verified_separately_from_evidence_pin(self):
        # Covers: AIC-REQ-08#AC1.
        index = self.committed_site()
        path = self.root/'website/explore/source-manifest.json'
        manifest = json.loads(path.read_text())
        valid = manifest['assetsRevision']
        manifest['assetsRevision'] = 'f'*40
        path.write_text(json.dumps(manifest))
        self.assertEqual(index.main([]), 1)
        self.assertFalse((self.root/'website/explore/skill-provenance.json').exists())
        manifest['assetsRevision'] = valid
        path.write_text(json.dumps(manifest))
        self.assertEqual(index.main([]), 0)

    def test_invalid_region_markers_fail_before_writing(self):
        # Covers: AIC-REQ-08#AC1.
        index = self.committed_site()
        old = self.root/'skills/INDEX.md'
        old.write_text('previous index')
        page = self.root/'website/index.html'
        page.write_text('Missing managed markers')
        self.assertEqual(index.main([]), 1)
        self.assertEqual(old.read_text(), 'previous index')

    def test_static_group_identifier_is_escaped_in_attribute_context(self):
        # Covers: AIC-REQ-08#AC7.
        import skill_provenance_output as output
        self.setup_site()
        base = self.root / 'website/explore'
        unsafe = 'map-build" onclick="injected'
        groups = json.loads((base / 'classification.json').read_text())
        groups['groups'][0]['id'] = unsafe
        (base / 'classification.json').write_text(json.dumps(groups))
        locale = json.loads((base / 'locales/en.json').read_text())
        locale['classification'][unsafe] = locale['classification'].pop('map-build')
        (base / 'locales/en.json').write_text(json.dumps(locale))
        html = output.fallback(self.root, output.preview_projection({'alpha': self.record}, self.root), 'en')
        self.assertNotIn('id="map-build" onclick=', html)
        self.assertIn('map-build&quot; onclick=&quot;injected', html)

    def test_public_sources_resolve_creative_references_and_exclude_tool_lookups(self):
        (self.skills / 'SOURCES.yaml').write_text('skills: {}\nreferences:\n  article:\n    title: Original article\n    url: https://example.org/article\n  duplicate:\n    title: Same article\n    url: https://example.org/article\n  tool:\n    title: Tool manual\n    url: https://example.org/manual\n')
        sources = [{'id': 'reference:article', 'role': 'creative_reference'}, {'id': 'reference:duplicate', 'role': 'creative_reference'}, {'id': 'reference:tool', 'role': 'tool_lookup'}]
        record = {'classification': 'third_party_adapted', 'sources': sources}
        self.assertEqual(provenance.public_sources(self.root, record), [{'title': 'Original article', 'url': 'https://example.org/article'}])
        self.assertEqual(provenance.public_sources(self.root, {'classification': 'native', 'sources': [sources[-1]]}), [])

    def test_static_third_party_badges_link_to_sources(self):
        import skill_provenance_output as output
        for classification in ('third_party_original', 'third_party_adapted'):
            record = {'classification': classification, 'sources': [{'title': 'Original', 'url': 'https://example.org/original'}]}
            html = output.render_badge(record, 'Third-party')
            self.assertIn('href="https://example.org/original"', html)
            self.assertIn('target="_blank" rel="noopener"', html)
            self.assertNotIn('provenance-evidence', html)
            record['sources'].append({'title': '<Article>', 'url': 'https://example.org/?a=1&b=2'})
            html = output.render_badge(record, 'Third-party')
            self.assertIn('<details', html)
            self.assertIn('<summary>Third-party</summary>', html)
            self.assertIn('&lt;Article&gt;', html)
            self.assertIn('?a=1&amp;b=2', html)
            self.assertEqual(html.count('<li>'), 2)

    def test_static_asset_directory_omits_audit_links(self):
        # Covers: AIC-REQ-08#AC1.
        import skill_provenance_output as output
        self.setup_site()
        projection = output.preview_projection({'alpha': self.record}, self.root)
        html = output.render_directory(self.root, projection, 'en')
        self.assertIn('data-asset="skills/alpha"', html)
        self.assertNotIn('AI Cortex original', html)
        self.assertNotIn('/provenance-evidence/confirmation.json', html)
        self.assertEqual(html.count('data-provenance='), 0)
        self.assertIn('id="skills"', html)

    def test_index_renders_reviewed_reference_objects(self):
        # Covers: AIC-REQ-08#AC1.
        import importlib.util
        spec = importlib.util.spec_from_file_location('aic08_index', Path(__file__).with_name('sync-skills-index.py'))
        index = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(index)
        rendered = index.render([('alpha', {'description': 'Example'})], {'alpha': self.record})
        self.assertNotIn('**AI Cortex original**', rendered)
        self.assertIn('../confirmation.json', rendered)
        self.assertNotIn('Unverified', rendered)

    def test_review_cli_names_actual_skill_without_attesting(self):
        # Covers: AIC-REQ-08#AC4.
        script = Path(__file__).with_name('skill-provenance.py')
        result = subprocess.run(['python3', str(script), '--review', 'eli5'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('third_party_adapted', result.stdout)
        self.assertIn('Missing facts', result.stdout)
        self.assertIn('Maintainer decision requested', result.stdout)
        self.assertIn('upstream', result.stdout)
        bad = subprocess.run(['python3', str(script), '--review', '../outside'], capture_output=True, text=True)
        self.assertEqual(bad.returncode, 1)
        self.assertNotIn('Traceback', bad.stderr)

    def test_strict_registry_subset_parser(self):
        # Covers: AIC-REQ-08#AC7.
        parsed = provenance.parse_registry('schema_version: "1.1"\nskills:\n  alpha:\n    modifications:\n      - Local change\n    upstream:\n      ref: '+('a'*40)+'\nreferences: {}\n')
        self.assertEqual(parsed['skills']['alpha']['modifications'], ['Local change'])
        for text in ('skills: {}\nskills: {}\n', 'skills:\n   alpha: {}\n', 'skills: &alias {}\n', 'skills: {alpha: {}}\n', 'skills:\n  alpha: |\n    multiline\n'):
            with self.subTest(text=text), self.assertRaises(provenance.ProvenanceError):
                provenance.parse_registry(text)


if __name__ == '__main__':
    unittest.main(verbosity=2)

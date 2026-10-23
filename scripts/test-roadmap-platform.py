#!/usr/bin/env python3
"""Offline remote-document regression; fixtures are not live Yuque receipts."""

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/define-roadmap/scripts/check-platform-delivery.py'
FIXTURE = ROOT / 'tests/fixtures/roadmap-platform/session.json'


class PlatformDeliveryTests(unittest.TestCase):
    """Covers: roadmap-modeling#remote-authority-and-delivery-evidence."""

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('platform_delivery', SCRIPT)
        cls.adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.adapter)

    def setUp(self):
        self.case = json.loads(FIXTURE.read_text())

    def test_multi_turn_rename_then_schedule_update_preserves_links_and_history(self):
        baseline = self.case['baseline']
        for turn in self.case['turns']:
            with self.subTest(turn=turn['name']):
                self.assertEqual(self.adapter.preflight(baseline, copy.deepcopy(baseline)), [])
                result = self.adapter.verify(baseline, turn['readback'], turn['contract'])
                self.assertEqual(result['findings'], [])
                self.assertTrue(result['passed'])
                baseline = turn['readback']

    def test_corrupt_readbacks_fail_for_each_protected_property(self):
        turn = self.case['turns'][0]
        for mutation in ['url', 'anchor', 'rendered_anchor', 'card', 'history',
                         'summary', 'candidate', 'completion', 'title', 'missing_page',
                         'duplicate_page', 'image', 'missing_observation', 'broken_link']:
            with self.subTest(mutation=mutation):
                pages = copy.deepcopy(turn['readback'])
                main = pages[0]
                if mutation == 'url':
                    main['url'] += '-new'
                elif mutation == 'anchor':
                    main['lake'] = main['lake'].replace('id="old-overview"', 'id="new-overview"')
                elif mutation == 'rendered_anchor':
                    main['rendered_ids'].remove('old-overview')
                elif mutation == 'card':
                    main['lake'] = main['lake'].replace('"image"', '"diagram"')
                elif mutation == 'history':
                    pages[-1]['lake'] = pages[-1]['lake'].replace('2024-02-01', '2027-02-01')
                elif mutation == 'summary':
                    main['lake'] = main['lake'].replace('2027-02-15', '2027-02-16')
                elif mutation == 'candidate':
                    main['lake'] = main['lake'].replace('Q9 excluded', 'Q9 included')
                elif mutation == 'completion':
                    main['lake'] = main['lake'].replace('MS1 planned', 'MS1 reached')
                elif mutation == 'title':
                    main['title'] = 'Another product'
                elif mutation == 'missing_page':
                    pages.pop()
                elif mutation == 'duplicate_page':
                    pages.append(copy.deepcopy(main))
                elif mutation == 'image':
                    main['images'][0]['natural_width'] = 0
                elif mutation == 'missing_observation':
                    del main['rendered_ids']
                else:
                    main['lake'] = main['lake'].replace('#scope', '#missing')
                self.assertFalse(self.adapter.verify(self.case['baseline'], pages, turn['contract'])['passed'])

    def test_source_and_projection_dates_must_both_change_for_new_decision(self):
        first, second = self.case['turns']
        partial = copy.deepcopy(second['readback'])
        partial[0] = copy.deepcopy(first['readback'][0])
        self.assertFalse(self.adapter.verify(first['readback'], partial, second['contract'])['passed'])

    def test_stale_preflight_rejects_body_title_and_revision_edits(self):
        before = self.case['baseline']
        for field in ['lake', 'title', 'updated_at']:
            current = copy.deepcopy(before)
            current[0][field] += ' changed concurrently'
            self.assertTrue(self.adapter.preflight(before, current), field)

    def test_native_style_failure_requires_visual_evidence_not_mermaid_source(self):
        turn = copy.deepcopy(self.case['turns'][0])
        turn['readback'][0]['visual_checks']['type_colors'] = False
        self.assertFalse(self.adapter.verify(self.case['baseline'], turn['readback'], turn['contract'])['passed'])
        del turn['readback'][0]['visual_checks']['type_colors']
        self.assertFalse(self.adapter.verify(self.case['baseline'], turn['readback'], turn['contract'])['passed'])

    def test_empty_or_malformed_inputs_never_pass(self):
        for before, after, contract in [([], [], {}), (self.case['baseline'], [], {}),
                                        (self.case['baseline'], self.case['baseline'], {'documents': []})]:
            self.assertFalse(self.adapter.verify(before, after, contract)['passed'])

    def test_no_change_review_is_idempotent_and_preserves_all_evidence(self):
        turn = copy.deepcopy(self.case['turns'][-1])
        before = copy.deepcopy(turn)
        self.assertTrue(self.adapter.verify(turn['readback'], turn['readback'], turn['contract'])['passed'])
        self.assertEqual(turn, before)

    def test_rendered_legacy_ids_and_embed_cards_survive_sequential_updates(self):
        from urllib.parse import quote
        baseline = copy.deepcopy(self.case['baseline'])
        turn = copy.deepcopy(self.case['turns'][0])
        embed = '<card name="embed" value="data:' + quote(json.dumps({'id': 'live-reference', 'url': 'https://example.org/book/versions'})) + '"></card>'
        baseline[0]['lake'] += embed
        baseline[0]['html'] = '<span id="legacy-rendered-only"></span>'
        turn['contract']['documents'][0]['protected_anchors'] = ['legacy-rendered-only']
        turn['readback'][0]['lake'] += '<p><span id="legacy-rendered-only" data-lake-id="legacy-rendered-only">&#8203;</span></p>' + embed
        turn['readback'][0]['rendered_ids'].append('legacy-rendered-only')
        self.assertTrue(self.adapter.verify(baseline, turn['readback'], turn['contract'])['passed'])
        turn['readback'][0]['lake'] = turn['readback'][0]['lake'].replace(embed, '')
        self.assertFalse(self.adapter.verify(baseline, turn['readback'], turn['contract'])['passed'])

    def test_transient_editor_ids_do_not_become_published_anchor_obligations(self):
        baseline = copy.deepcopy(self.case['baseline'])
        turn = copy.deepcopy(self.case['turns'][0])
        baseline[0]['html'] = '<h2 id="outlook">Outlook</h2><p id="auto-paragraph"><span id="auto-text">Text</span></p>'
        self.assertTrue(self.adapter.verify(baseline, turn['readback'], turn['contract'])['passed'])

    def test_required_source_links_cannot_disappear_or_be_retargeted(self):
        turn = copy.deepcopy(self.case['turns'][0])
        href = 'https://example.org/requirements/Q1'
        link = '<a href="' + href + '">Source Q1</a>'
        turn['readback'][0]['lake'] += link
        turn['contract']['documents'][0]['required_links'] = [href]
        self.assertTrue(self.adapter.verify(self.case['baseline'], turn['readback'], turn['contract'])['passed'])
        for replacement in ['', link.replace('/Q1', '/Q2')]:
            pages = copy.deepcopy(turn['readback'])
            pages[0]['lake'] = pages[0]['lake'].replace(link, replacement)
            self.assertFalse(self.adapter.verify(self.case['baseline'], pages, turn['contract'])['passed'])

    def test_equivalent_fragment_encoding_is_not_a_changed_link(self):
        turn = copy.deepcopy(self.case['turns'][0])
        turn['readback'][0]['lake'] = turn['readback'][0]['lake'].replace('#scope', '#%73cope')
        self.assertTrue(self.adapter.verify(self.case['baseline'], turn['readback'], turn['contract'])['passed'])

    def test_internal_links_accept_html_targets_but_require_rendered_evidence(self):
        for cross_document in (False, True):
            with self.subTest(cross_document=cross_document):
                turn = copy.deepcopy(self.case['turns'][0])
                pages = turn['readback']
                target = pages[1] if cross_document else pages[0]
                href = (target['url'] if cross_document else '') + '#html-only'
                pages[0]['lake'] += '<a href="' + href + '">Rendered heading</a>'
                target['html'] = '<h2 id="html-only">Rendered heading</h2>'
                target['rendered_ids'].append('html-only')
                result = self.adapter.verify(self.case['baseline'], pages, turn['contract'])
                self.assertTrue(result['passed'], result['findings'])
                target['rendered_ids'].remove('html-only')
                result = self.adapter.verify(self.case['baseline'], pages, turn['contract'])
                self.assertFalse(result['passed'])
                self.assertTrue(any('rendered anchors' in f for f in result['findings']))
                target['rendered_ids'].append('html-only')
                target['html'] = '<h2>Removed heading</h2>'
                result = self.adapter.verify(self.case['baseline'], pages, turn['contract'])
                self.assertTrue(any('broken internal link' in f for f in result['findings']))

    def test_duplicate_anchor_ids_are_not_valid_navigation_evidence(self):
        turn = copy.deepcopy(self.case['turns'][0])
        turn['readback'][0]['lake'] += '<h2 id="outlook">Another section</h2>'
        self.assertFalse(self.adapter.verify(self.case['baseline'], turn['readback'], turn['contract'])['passed'])

    def test_metadata_only_checks_reuse_unchanged_body_but_reject_hidden_body_edits(self):
        turn = copy.deepcopy(self.case['turns'][0])
        check = turn['contract']['documents'][0]
        check.update(inspection='metadata', visual_checks=['title_directory'])
        page = turn['readback'][0]
        page['visual_checks'] = dict(title_directory=True)
        del page['rendered_ids']
        del page['images']
        self.assertTrue(self.adapter.verify(self.case['baseline'], turn['readback'], turn['contract'])['passed'])
        check['visual_checks'] = []
        self.assertFalse(self.adapter.verify(self.case['baseline'], turn['readback'], turn['contract'])['passed'])
        check['visual_checks'] = ['title_directory']
        page['lake'] += '<p>A body change in a title-only operation.</p>'
        self.assertFalse(self.adapter.verify(self.case['baseline'], turn['readback'], turn['contract'])['passed'])

    def test_missing_link_and_visual_acceptance_cannot_be_bypassed_by_unknown_mode(self):
        turn = copy.deepcopy(self.case['turns'][0])
        turn['contract']['documents'][0]['inspection'] = 'skip-all'
        self.assertFalse(self.adapter.verify(self.case['baseline'], turn['readback'], turn['contract'])['passed'])

    def test_card_display_type_is_preserved_alongside_its_decoded_payload(self):
        baseline = copy.deepcopy(self.case['baseline'])
        turn = copy.deepcopy(self.case['turns'][0])
        baseline[0]['lake'] = baseline[0]['lake'].replace('<card name=', '<card type="inline" name=')
        turn['readback'][0]['lake'] = turn['readback'][0]['lake'].replace('<card name=', '<card type="block" name=')
        self.assertFalse(self.adapter.verify(baseline, turn['readback'], turn['contract'])['passed'])

    def test_dated_assessment_baseline_does_not_masquerade_as_latest_inventory(self):
        turn = copy.deepcopy(self.case['turns'][0])
        turn['readback'][1]['lake'] += '<p>Scored baseline: 40. Latest inventory: 43; 3 unassessed.</p>'
        turn['contract']['documents'][1]['required_text'] += ['Scored baseline: 40.', 'Latest inventory: 43; 3 unassessed.']
        self.assertTrue(self.adapter.verify(self.case['baseline'], turn['readback'], turn['contract'])['passed'])
        turn['readback'][1]['lake'] = turn['readback'][1]['lake'].replace('Latest inventory: 43; 3 unassessed.', 'All 43 scored.')
        self.assertFalse(self.adapter.verify(self.case['baseline'], turn['readback'], turn['contract'])['passed'])

    def test_read_only_cli_accepts_good_evidence_and_rejects_bad_evidence(self):
        turn = self.case['turns'][0]
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'evidence.json'
            data = dict(baseline=self.case['baseline'], readback=turn['readback'], contract=turn['contract'])
            source.write_text(json.dumps(data))
            before = source.read_bytes()
            result = subprocess.run([sys.executable, str(SCRIPT), str(source)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(json.loads(result.stdout)['passed'])
            self.assertEqual(source.read_bytes(), before)
            source.write_text('{}')
            result = subprocess.run([sys.executable, str(SCRIPT), str(source)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)

    def test_retirement_recovery_checks_real_bytes_and_never_removes_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'workspace'
            root.mkdir()
            source = root / 'plan.md'
            source.write_text('Confirmed scope; another batch remains unknown.\n')
            unrelated = root / 'notes.md'
            unrelated.write_text('Unrelated work.\n')
            archive = Path(temp) / 'recovery.tar.gz'
            with tarfile.open(archive, 'w:gz') as backup:
                backup.add(source, arcname='plan.md')
            self.assertEqual(self.adapter.recovery_findings(root, ['plan.md'], archive), [])
            self.assertTrue(self.adapter.recovery_findings(root, ['plan.md', './plan.md'], archive))
            source.write_text('A late change not in the backup.\n')
            self.assertTrue(self.adapter.recovery_findings(root, ['plan.md'], archive))
            self.assertTrue(self.adapter.recovery_findings(root, ['notes.md'], archive))
            self.assertTrue(self.adapter.recovery_findings(root, [], archive))
            self.assertTrue(self.adapter.recovery_findings(root, ['../recovery.tar.gz'], archive))
            self.assertTrue(source.exists())
            self.assertEqual(unrelated.read_text(), 'Unrelated work.\n')


if __name__ == '__main__':
    unittest.main()

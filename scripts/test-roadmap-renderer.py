#!/usr/bin/env python3
"""Behavioral checks for the bundled offline roadmap renderer."""

import copy
import importlib.util
import json
import re
from pathlib import Path
import subprocess
from shutil import copyfile
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'skills/define-roadmap/scripts/render-roadmap.py'
spec = importlib.util.spec_from_file_location('roadmap_renderer', SCRIPT)
renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(renderer)


def sample(mode='weeks'):
    return {
        'schema_version': '1.0', 'project': 'Desk <研发> & support',
        'updated': '2026-10-20', 'closure': 'Acceptance passed',
        'direction': 'Make request handling dependable', 'ordering': 'Search enables export',
        'priority_policy': 'Customer blockers first',
        'views': ['requirements', 'versions', 'schedule'],
        'entries': [dict(id='R1', name='Search <客户> & export | results',
                         source='requirements/search.md#acceptance', outcome='Find records',
                         priority='P0', tier='Now', approval='Approved',
                         execution='In progress', conditions='Review results')],
        'versions': [dict(id='V1', name='First delivery', members=['R1'],
                          outcome='Search works', owner='Unknown', window='Unknown')],
        'schedule': dict(mode=mode, origin='W1: start date unknown' if mode == 'weeks' else 'ISO calendar dates',
                         calendar='calendar-days', items=[dict(ref='V1', kind='span', basis='target',
                         start=1 if mode == 'weeks' else '2026-11-02',
                         end=3 if mode == 'weeks' else '2026-11-16', depends_on=[])])
    }


def event_sample(mode='weeks'):
    data = sample(mode)
    start, end = (1, 3) if mode == 'weeks' else ('2026-11-02', '2026-11-16')
    data['schema_version'] = '1.1'
    data['phases'] = [dict(id='PH1', name='Validation phase', source='phase.md',
                          owner='QA', scope=['V1'], exit_condition='Acceptance approved')]
    data['milestones'] = [dict(id='M1', name='Acceptance approval', source='approval.md',
                              owner='Reviewer', related=['PH1', 'V1'], category='approval',
                              criterion='Reviewer signs acceptance', state='planned', evidence=None)]
    data['schedule']['items'] += [
        dict(ref='PH1', kind='span', basis='target', start=start, end=end, depends_on=[]),
        dict(ref='M1', kind='milestone', basis='target', start=end, end=end, depends_on=['PH1'])]
    return data


def revision_sample():
    data = sample()
    data.update(schema_version='1.2', revisions=[dict(
        id='REV1', date='2026-10-20', change='R1: V1 → V2',
        reason='Acceptance prerequisite slipped', impact='Export moves three weeks',
        source='decisions.md#rev1')])
    return data


def iteration_sample(mode='weeks'):
    data = event_sample(mode)
    data.update(schema_version='1.3', revisions=[], cadence='Two-week iterations')
    data['views'].insert(1, 'iterations')
    data['iterations'] = [dict(id='I1', name='Stabilize search', goal='Validate search behavior',
                               owner='Desk team', members=['R1'], source='iterations.md#i1',
                               board='https://example.com/board')]
    data['schedule']['items'].append(dict(
        ref='I1', kind='span', basis='target', start=1 if mode == 'weeks' else '2026-11-02',
        end=3 if mode == 'weeks' else '2026-11-16', depends_on=[]))
    return data


def selection_sample(work_mode='iterations', delivery='versioned'):
    data = iteration_sample()
    data['schema_version'] = '1.4'
    data['views'] += ['phases', 'milestones']
    data['selection'] = dict(scenario=work_mode, primary='iterations', layout='split',
        rationale='Team uses two-week planning and named releases', source='decisions.md#selection',
        context=dict(work_mode=work_mode, delivery=delivery, audience='Team and customer',
                     constraints='Customer acceptance required', source='context.md'))
    return data


def language_sample(locale='zh-CN', mode='weeks'):
    data = selection_sample()
    data['schema_version'] = '1.5'
    data['language'] = dict(locale=locale, basis='project', source='policy.md#language',
                            rationale='Project documentation policy')
    if mode == 'dates':
        dates = event_sample('dates')['schedule']
        data['schedule'] = dates
        data['schedule']['items'].append(dict(ref='I1', kind='span', basis='target',
            start='2026-11-02', end='2026-11-16', depends_on=[]))
    return data


def language_evidence(locale, source='policy.md'):
    return dict(locale=locale, source=source)


class RendererTests(unittest.TestCase):
    def test_main_prioritizes_plan_over_basis_when_using_modern_layouts(self):
        """Covers: roadmap-reading#RC2; preserve facts while changing reading order."""
        for factory in (iteration_sample, selection_sample, lambda: language_sample('en')):
            for layout in ('single', 'split'):
                with self.subTest(schema=factory()['schema_version'], layout=layout):
                    data = factory()
                    if 'selection' in data:
                        data['selection']['layout'] = layout
                    before = copy.deepcopy(data)
                    main = renderer.documents(renderer.validate(data), layout)['roadmap.md']
                    headings = ['## Overview', 'Current arrangement:', '## Priority arrangement',
                                '## Delivery', '## Revision history', '## Planning basis and sources']
                    positions = [main.index(value) for value in headings]
                    self.assertEqual(positions, sorted(positions))
                    basis = main.split('## Planning basis and sources', 1)[1]
                    self.assertIn(data['priority_policy'], basis)
                    self.assertIn(data['closure'], basis)
                    if 'selection' in data:
                        self.assertIn(data['selection']['rationale'], basis)
                    if 'language' in data:
                        self.assertIn(data['language']['rationale'], basis)
                    self.assertEqual(data, before)

    def test_execution_unknown_is_visible_before_rows_when_main_uses_modern_layout(self):
        """Covers: roadmap-reading#RC2; an empty status must not look like no work."""
        data = iteration_sample()
        data['entries'][0]['execution'] = None
        main = renderer.markdown(renderer.validate(data))
        warning = 'Unverified execution mappings: R1'
        self.assertEqual(main.count(warning), 1)
        self.assertLess(main.index(warning), main.index('## Priority arrangement'))
        self.assertNotIn('Not started', main)

    def test_policy_is_linked_safely_when_modern_input_supplies_only_reference(self):
        """Covers: roadmap-reading#RC3; references work without a new schema field."""
        for link in ('../policy.md#priority', 'policy.md', '#policy',
                     'https://example.com/policy?x=1&y=2'):
            data = iteration_sample()
            data['priority_policy'] = link
            main = renderer.markdown(renderer.validate(data))
            with self.subTest(link=link):
                self.assertIn(f'[Priority policy]({link})', main)
        data = iteration_sample()
        data['priority_policy'] = '<script>alert(1)</script>'
        main = renderer.markdown(renderer.validate(data))
        self.assertNotIn('<script>', main)
        self.assertIn('&lt;script&gt;', main)
        data['priority_policy'] = '../policy\\bad.md'
        with self.assertRaisesRegex(ValueError, 'priority_policy'):
            renderer.validate(data)

    def test_basis_labels_are_localized_when_language_is_chinese(self):
        """Covers: roadmap-reading#RC2; moving metadata does not lose localization."""
        data = language_sample()
        data['priority_policy'] = '../policy.md#priority'
        main = renderer.documents(renderer.validate(data))['roadmap.md']
        self.assertLess(main.index('当前安排：'), main.index('## 优先安排'))
        self.assertLess(main.index('## 修订记录'), main.index('## 规划依据与来源'))
        self.assertIn('[优先级规则](../policy.md#priority)', main)
        self.assertIn('### 规划方式', main)
        self.assertNotIn('Current arrangement:', main)
        self.assertNotIn('Planning basis and sources', main)

    def test_legacy_single_keeps_layout_while_explicit_split_exposes_unknown_once(self):
        """Covers: roadmap-reading#RC3; legacy adoption needs no schema upgrade."""
        for version in ('1.0', '1.1', '1.2'):
            data = revision_sample() if version == '1.2' else sample()
            data['schema_version'] = version
            data['entries'][0]['execution'] = None
            before = copy.deepcopy(data)
            single = renderer.documents(renderer.validate(data))['roadmap.md']
            split = renderer.documents(data, 'split')['roadmap.md']
            self.assertIn('Ordering rationale: Search enables export', single)
            self.assertNotIn('## Planning basis and sources', single)
            self.assertEqual(split.count('Unverified execution mappings: R1'), 1)
            self.assertLess(split.index('Unverified execution mappings: R1'),
                            split.index('## Priority arrangement'))
            self.assertEqual(data, before)

    def test_legacy_split_rejects_invalid_policy_reference_before_rendering(self):
        """Covers: roadmap-reading#RC3; explicit split links obey common validation."""
        data = sample()
        data['priority_policy'] = '../policy\\bad.md'
        renderer.validate(data)  # Legacy single output still treats this as escaped text.
        with self.assertRaisesRegex(ValueError, 'priority_policy'):
            renderer.documents(data, 'split')

    def test_localized_catalog_covers_scenarios_states_and_missing_values(self):
        """Covers: roadmap-capabilities#AC24."""
        for path in sorted((SCRIPT.parent.parent / 'references/scenarios').glob('*/input.json')):
            data = json.loads(path.read_text())
            data.update(schema_version='1.5', language=language_sample()['language'])
            outputs = renderer.documents(renderer.validate(data))
            self.assertIn('交付物语言：', outputs['roadmap.md'])
        for state in sorted(renderer.EXECUTION) + [None]:
            data = language_sample()
            data['entries'][0]['execution'] = state
            outputs = renderer.documents(renderer.validate(data))
            self.assertNotIn('| None |', outputs['roadmap.md'])
        data = language_sample()
        for item in data['schedule']['items']:
            item['start'] = item['end'] = None
        outputs = renderer.documents(renderer.validate(data))
        self.assertIn('未排期', outputs['roadmap.svg'])
        for basis in ['user', 'project', 'existing', 'context']:
            data['language']['basis'] = basis
            self.assertIn('交付物语言：', renderer.markdown(data))

    def test_missing_catalog_message_fails_instead_of_mixing_languages(self):
        """Covers: roadmap-capabilities#AC24."""
        with self.assertRaisesRegex(ValueError, 'missing localized message'):
            renderer.ui(language_sample(), 'New untranslated heading')

    def test_chinese_display_lists_and_unknown_event_owner_are_localized(self):
        """Covers: roadmap-capabilities#AC24."""
        data = language_sample()
        data['milestones'][0]['owner'] = 'Unknown'
        output = renderer.markdown(renderer.validate(data))
        self.assertIn('需求安排、迭代', output)
        self.assertNotIn('Unknown', output)
        self.assertIn('选择依据](decisions.md#selection)。', output)

    def test_timeline_preserves_source_text_when_it_mentions_a_schedule_heading(self):
        """Covers: roadmap-capabilities#AC24; source prose is never globally replaced."""
        for locale, origin in [('en', 'Source mentions ## Schedule as a section name.'),
                               ('zh-CN', '源说明引用 ## 日程 作为章节名称。')]:
            with self.subTest(locale=locale):
                data = language_sample(locale)
                data['schedule']['origin'] = origin

                output = renderer.documents(renderer.validate(data))['roadmap-delivery.md']

                self.assertIn(origin, output)
                heading = '## Timeline' if locale == 'en' else '## 时间线'
                self.assertIn(heading, output)

    def test_localized_cli_reports_recovery_when_bundled_catalog_is_damaged(self):
        """Covers: roadmap-capabilities#AC25; a damaged bundle fails before writing."""
        for content in [None, '{', '[]', '{"label": null}']:
            with self.subTest(catalog=content), tempfile.TemporaryDirectory() as tmp:
                script = Path(tmp) / 'render-roadmap.py'
                copyfile(SCRIPT, script)
                source, out = Path(tmp) / 'input.json', Path(tmp) / 'out'
                source.write_text(json.dumps(language_sample()))
                if content is not None:
                    (Path(tmp) / 'roadmap-zh-CN.json').write_text(content)

                result = subprocess.run([sys.executable, str(script), str(source), '--output-dir', str(out)],
                                        capture_output=True, text=True)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn('restore the bundled roadmap-zh-CN.json', result.stderr)
                self.assertNotIn('Traceback', result.stderr)
                self.assertFalse(out.exists())

    def test_language_decision_is_visible_and_source_linked(self):
        """Covers: roadmap-capabilities#AC23."""
        for locale, label in [('en', 'Deliverable language: '), ('zh-CN', '交付物语言：')]:
            data = language_sample(locale)
            output = renderer.markdown(renderer.validate(data))
            self.assertIn(label, output)
            self.assertIn('policy.md#language', output)
            self.assertIn(data['language']['rationale'], output)

    def test_language_resolution_precedence_and_consensus(self):
        """Covers: roadmap-capabilities#AC23."""
        levels = ['user', 'project', 'existing']
        for level in levels:
            context = {key: [language_evidence('en')] for key in ['user', 'project', 'existing', 'audience', 'documents']}
            for higher in levels[:levels.index(level)]:
                context.pop(higher)
            context[level] = [language_evidence('zh-CN')]
            result = renderer.resolve_language({'language_context': context})
            self.assertEqual(result['status'], 'resolved')
            self.assertEqual(result['locale'], 'zh-CN')
            self.assertEqual(result['basis'], level)
        result = renderer.resolve_language({'language_context': {'audience': [language_evidence('zh-CN')],
            'documents': [language_evidence('zh-CN', 'existing.md')]}})
        self.assertEqual(result['locale'], 'zh-CN')
        self.assertEqual(result['basis'], 'context')

    def test_language_conflicts_and_missing_evidence_ask_without_guessing(self):
        """Covers: roadmap-capabilities#AC23."""
        cases = [{}, {'documents': [language_evidence('en'), language_evidence('zh-CN')]},
                 {'project': [language_evidence('en'), language_evidence('zh-CN')],
                  'existing': [language_evidence('en')]}]
        for context in cases:
            result = renderer.resolve_language({'language_context': context})
            self.assertEqual(result['status'], 'needs-input')
            self.assertIsNone(result['locale'])
            self.assertTrue(result['questions'])

    def test_language_choice_is_retained_and_changes_are_only_proposals(self):
        """Covers: roadmap-capabilities#AC23."""
        data = language_sample()
        before = copy.deepcopy(data)
        result = renderer.resolve_language(data)
        self.assertEqual(result['status'], 'retained')
        self.assertEqual(result['locale'], 'zh-CN')
        data['language_context'] = {'user': [language_evidence('en', 'request.md')]}
        result = renderer.resolve_language(data)
        self.assertEqual(result['status'], 'change-proposed')
        self.assertEqual(result['retained_locale'], 'zh-CN')
        self.assertEqual(result['locale'], 'en')
        data.pop('language_context')
        self.assertEqual(data, before)
        self.assertEqual(renderer.recommend(data)['language']['status'], 'retained')

    def test_generation_does_not_override_or_ignore_new_language_evidence(self):
        """Covers: roadmap-capabilities#AC25."""
        data = language_sample()
        data['language_context'] = {'user': [language_evidence('en', 'request.md')]}
        with self.assertRaisesRegex(ValueError, 'language'):
            renderer.validate(data)
        data['language_context'] = {'project': [language_evidence('en'), language_evidence('zh-CN')]}
        with self.assertRaisesRegex(ValueError, 'language'):
            renderer.validate(data)

    def test_unresolved_language_generation_creates_no_output_directory(self):
        """Covers: roadmap-capabilities#AC25."""
        data = language_sample()
        data['language_context'] = {'user': [language_evidence('en'), language_evidence('zh-CN')]}
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp) / 'input.json', Path(tmp) / 'out'
            source.write_text(json.dumps(data))
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), '--output-dir', str(out)],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('language evidence is unresolved', result.stderr)
            self.assertFalse(out.exists())
            self.assertEqual(json.loads(source.read_text()), data)

    def test_language_validation_is_strict_and_legacy_metadata_is_ignored(self):
        """Covers: roadmap-capabilities#AC25."""
        for locale in ('fr', '', None, {}, ['en']):
            data = language_sample(locale)
            with self.subTest(locale=locale), self.assertRaises(ValueError):
                renderer.validate(data)
        for field in ('basis', 'source', 'rationale'):
            data = language_sample()
            data['language'].pop(field)
            with self.assertRaises(ValueError):
                renderer.validate(data)
        data = selection_sample()
        original = renderer.markdown(data)
        data['language'] = {'locale': 'zh-CN'}
        self.assertEqual(renderer.markdown(renderer.validate(data)), original)
        with self.assertRaises(ValueError):
            renderer.resolve_language({'language_context': {'project': [language_evidence('fr')]}})
        with self.assertRaises(ValueError):
            renderer.resolve_language({'language_context': {'documents': [language_evidence('en')] * 21}})

    def test_chinese_presentation_keeps_source_text_and_machine_identity(self):
        """Covers: roadmap-capabilities#AC24."""
        data = language_sample()
        data['entries'][0].update(name='Overview / target <研发>', execution='In progress')
        before = copy.deepcopy(data)
        result = renderer.documents(renderer.validate(data))
        main = result['roadmap.md']
        detail = result['roadmap-delivery.md']
        self.assertIn('## 概览', main)
        self.assertIn('执行状态', main)
        self.assertIn('进行中', main)
        self.assertIn('Overview / target &lt;研发&gt;', main)
        self.assertIn('(requirements/search.md#acceptance)', main)
        self.assertIn('### 迭代', detail)
        self.assertIn('### 阶段', detail)
        self.assertIn('### 里程碑', detail)
        self.assertIn('计划中', detail)
        self.assertNotIn('target ·', detail)
        self.assertEqual(data, before)
        svg = result['roadmap.svg']
        self.assertIn('相对周次', svg)
        self.assertIn('目标', svg)
        self.assertNotIn('Bars show elapsed', svg)
        self.assertIn('zh-CN', svg)
        self.assertEqual(renderer.documents(data), result)

    def test_dated_mermaid_uses_localized_labels_but_retains_syntax_and_ids(self):
        """Covers: roadmap-capabilities#AC24."""
        data = renderer.validate(language_sample(mode='dates'))
        value = renderer.mermaid(data)
        self.assertIn('gantt', value)
        self.assertIn('dateFormat YYYY-MM-DD', value)
        self.assertIn('目标', value)
        self.assertIn('计划中', value)
        self.assertIn(':milestone, M1,', value)
        self.assertNotIn('(target)', value)
        english = renderer.documents(renderer.validate(language_sample('en')))
        self.assertIn('## Overview', english['roadmap.md'])
        self.assertIn('In progress', english['roadmap.md'])

    def test_cli_language_resolution_is_read_only_and_saved_language_generates(self):
        """Covers: roadmap-capabilities#AC25."""
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp) / 'input.json', Path(tmp) / 'out'
            source.write_text(json.dumps({'language_context': {'documents': [language_evidence('zh-CN')]}}))
            command = [sys.executable, str(SCRIPT), str(source)]
            result = subprocess.run(command + ['--resolve-language'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['locale'], 'zh-CN')
            self.assertEqual(list(Path(tmp).iterdir()), [source])
            result = subprocess.run(command + ['--resolve-language', '--output-dir', str(out)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out.exists())
            source.write_text(json.dumps(language_sample()))
            result = subprocess.run(command + ['--output-dir', str(out)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('## 概览', (out / 'roadmap.md').read_text())
            self.assertEqual(json.loads(source.read_text())['language']['locale'], 'zh-CN')

    def test_recommendation_recipes_are_context_sensitive_and_not_applied(self):
        expected = {'iterations': ('iterations', ['requirements', 'iterations', 'versions', 'milestones']),
                    'flow': ('flow', ['requirements', 'flow', 'versions', 'milestones']),
                    'staged': ('phases', ['requirements', 'phases', 'milestones', 'versions']),
                    'discovery': ('phases', ['requirements', 'phases', 'milestones', 'versions'])}
        for mode, (primary, views) in expected.items():
            context = dict(selection_sample()['selection']['context'], work_mode=mode)
            data = {'planning_context': context}
            before = copy.deepcopy(data)
            result = renderer.recommend(data)
            self.assertEqual(result['status'], 'proposal')
            self.assertEqual(result['primary'], primary)
            self.assertEqual(result['views'], views)
            self.assertEqual(result['layout'], 'single')
            self.assertTrue(result['rationale'])
            self.assertEqual(data, before)
        result = renderer.recommend({'planning_context': dict(context, work_mode='flow', delivery='continuous')})
        self.assertEqual(result['views'], ['requirements', 'flow'])

    def test_recommendation_asks_only_missing_context_and_reuses_custom_choices(self):
        result = renderer.recommend({'planning_context': {'work_mode': 'flow'}})
        self.assertEqual(result['status'], 'needs-input')
        self.assertEqual(set(result['missing']), {'delivery', 'audience', 'constraints', 'source'})
        self.assertNotIn('views', result)
        self.assertEqual(len(result['questions']), 4)
        data = selection_sample()
        data['selection'].update(scenario='custom', primary='requirements')
        result = renderer.recommend(data)
        self.assertEqual(result['status'], 'retained')
        self.assertEqual(result['views'], data['views'])
        self.assertEqual(result['layout'], 'split')
        data['planning_context'] = dict(data['selection']['context'], work_mode='flow')
        result = renderer.recommend(data)
        self.assertEqual(result['status'], 'retained-review-needed')
        self.assertEqual(result['views'], data['views'])
        data['selection']['primary'] = 'flow'
        with self.assertRaises(ValueError):
            renderer.recommend(data)

    def test_schema_1_4_respects_explicit_views_and_saved_layout(self):
        data = selection_sample()
        data['views'].remove('phases')
        data['views'].remove('milestones')
        output = renderer.documents(renderer.validate(data))
        self.assertIn('roadmap-delivery.md', output)
        self.assertNotIn('### Phases', output['roadmap-delivery.md'])
        self.assertNotIn('### Milestones', output['roadmap-delivery.md'])
        self.assertNotIn('Repair acceptance', output['roadmap.md'])
        self.assertIn('Planning approach', output['roadmap.md'])
        self.assertIn('(decisions.md#selection)', output['roadmap.md'])
        with self.assertRaisesRegex(ValueError, 'layout'):
            renderer.documents(data, 'single')

    def test_invalid_selection_is_rejected_without_guessing(self):
        mutations = [lambda d: d.pop('selection'),
                     lambda d: d['selection'].pop('rationale'),
                     lambda d: d['selection'].update(primary='flow'),
                     lambda d: d['selection'].update(layout='other'),
                     lambda d: d['selection']['context'].update(work_mode='unknown'),
                     lambda d: d['selection'].update(source='/private/source')]
        for mutate in mutations:
            data = selection_sample()
            mutate(data)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                renderer.validate(data)

    def test_flow_view_has_policy_evidence_without_invented_iteration(self):
        data = selection_sample('flow', 'continuous')
        data['views'] = ['requirements', 'flow']
        data['selection'].update(primary='flow', layout='single')
        data['flow'] = dict(source='flow.md', board='board.md', policy='Pull only below explicit WIP limits',
                            expectation='No historical estimate yet', metrics='Cycle time, throughput, WIP and item age')
        output = renderer.markdown(renderer.validate(data))
        self.assertIn('### Flow', output)
        self.assertIn('No historical estimate yet', output)
        self.assertIn('(board.md)', output)
        self.assertNotIn('### Iterations', output)
        self.assertNotIn('### Versions', output)
        self.assertNotIn('### Phases', output)
        self.assertNotIn('### Milestones', output)
        data['flow']['board'] = 'javascript:bad'
        with self.assertRaises(ValueError):
            renderer.validate(data)

    def test_cli_recommendation_writes_nothing_and_generation_reuses_layout(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp) / 'input.json', Path(tmp) / 'out'
            data = selection_sample()
            source.write_text(json.dumps(data))
            command = [sys.executable, str(SCRIPT), str(source)]
            result = subprocess.run(command + ['--recommend'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['status'], 'retained')
            self.assertEqual(list(Path(tmp).iterdir()), [source])
            result = subprocess.run(command + ['--recommend', '--output-dir', str(out)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(out.exists())
            result = subprocess.run(command + ['--output-dir', str(out)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((out / 'roadmap-delivery.md').exists())
            self.assertIn('Planning approach', (out / 'roadmap.md').read_text())

    def test_legacy_recommendation_preserves_views_without_forcing_context_migration(self):
        data = sample()
        data['selection'] = {'unmodeled': 'legacy metadata'}
        result = renderer.recommend(data)
        self.assertEqual(result['status'], 'retained')
        self.assertEqual(result['views'], data['views'])
        self.assertIsNone(result['primary'])
        self.assertIsNone(result['layout'])
        self.assertEqual(result['questions'], [])
        self.assertEqual(result['missing'], [])

    def test_cli_missing_context_is_diagnostic_and_invalid_choice_is_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'context.json'
            source.write_text(json.dumps({'planning_context': {'work_mode': 'flow'}}))
            command = [sys.executable, str(SCRIPT), str(source), '--recommend']
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report['status'], 'needs-input')
            self.assertNotIn('views', report)
            data = selection_sample()
            data['selection']['primary'] = 'flow'
            source.write_text(json.dumps(data))
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('selection', result.stderr)
            self.assertEqual(list(Path(tmp).iterdir()), [source])

    def test_continuous_iteration_team_does_not_need_release_batches_or_events(self):
        context = dict(selection_sample()['selection']['context'], delivery='continuous')
        result = renderer.recommend({'planning_context': context})
        self.assertEqual(result['views'], ['requirements', 'iterations'])

    def test_recommendation_rejects_unknown_or_malformed_schema_versions(self):
        for value in ('1.7', {}, [], 1, False, None):
            data = selection_sample()
            data['schema_version'] = value
            with self.subTest(schema=value), self.assertRaisesRegex(ValueError, 'schema_version'):
                renderer.recommend(data)

    def test_iteration_view_derives_timebox_and_version_mapping(self):
        data = iteration_sample()
        before = copy.deepcopy(data)
        output = renderer.markdown(renderer.validate(data))
        self.assertIn('## Priority arrangement', output)
        self.assertIn('## Delivery plan', output)
        self.assertIn('### Iterations', output)
        self.assertIn('Two-week iterations', output)
        self.assertIn('Validate search behavior', output)
        self.assertIn('target · W1–W2', output)
        self.assertIn('V1', output)
        self.assertIn('(iterations.md#i1)', output)
        self.assertIn('(https://example.com/board)', output)
        self.assertIn('### Phases', output)
        self.assertIn('### Milestones', output)
        self.assertEqual(data, before)
        self.assertIn('I1', renderer.svg(data))

    def test_iterations_allow_carry_over_without_releasing_or_reprioritizing(self):
        data = iteration_sample()
        data['iterations'].append(dict(data['iterations'][0], id='I2', name='Continue validation'))
        renderer.validate(data)
        output = renderer.markdown(data)
        self.assertIn('I2', output)
        self.assertIn('Unscheduled', output)
        self.assertEqual(data['entries'][0]['tier'], 'Now')
        self.assertEqual(data['entries'][0]['execution'], 'In progress')
        self.assertEqual(data['milestones'][0]['state'], 'planned')

    def test_iteration_invalid_contracts_are_rejected(self):
        mutations = [lambda d: d.pop('cadence'), lambda d: d.pop('iterations'),
                     lambda d: d['iterations'][0].update(members=['missing']),
                     lambda d: d['iterations'][0].update(members=['R1', 'R1']),
                     lambda d: d['iterations'][0].update(id='V1'),
                     lambda d: d['iterations'][0].update(source='/private/source'),
                     lambda d: d['iterations'][0].update(board='javascript:bad'),
                     lambda d: d['iterations'][0].pop('goal'),
                     lambda d: d['schedule']['items'][-1].update(kind='milestone')]
        for mutate in mutations:
            data = iteration_sample()
            mutate(data)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                renderer.validate(data)

    def test_iteration_view_is_optional_and_older_schema_metadata_is_ignored(self):
        data = revision_sample()
        data['iterations'] = 'unmodeled legacy metadata'
        renderer.validate(data)
        self.assertNotIn('Iterations', renderer.markdown(data))
        data['views'].append('iterations')
        with self.assertRaises(ValueError):
            renderer.validate(data)
        data = iteration_sample()
        data['iterations'] = []
        data['schedule']['items'].pop()
        output = renderer.markdown(renderer.validate(data))
        self.assertIn('No iterations planned', output)
        self.assertIn('Not allocated to an iteration: R1', output)

    def test_completed_rows_are_separate_without_changing_tiers(self):
        data = iteration_sample()
        data['entries'][0]['execution'] = 'Completed'
        output = renderer.markdown(renderer.validate(data))
        self.assertIn('<summary>Completed requirements and defects (1)</summary>', output)
        self.assertLess(output.index('<summary>'), output.index('Search &lt;'))
        self.assertEqual(data['entries'][0]['tier'], 'Now')

    def test_split_documents_keep_summary_navigation_and_complete_supplied_history(self):
        data = iteration_sample()
        data['revisions'] = [dict(revision_sample()['revisions'][0], id=f'REV{i}')
                             for i in range(7, 0, -1)]
        data['revision_history'] = 'decisions.md#history'
        output = renderer.documents(renderer.validate(data), 'split')
        main, delivery, history = (output[name] for name in (
            'roadmap.md', 'roadmap-delivery.md', 'roadmap-history.md'))
        self.assertIn('Validate search behavior', main)
        self.assertIn('Acceptance approval', main)
        self.assertIn('roadmap-delivery.md', main)
        self.assertIn('roadmap-history.md', main)
        self.assertNotIn('REV2', main)
        self.assertIn('REV2', history)
        self.assertIn('(decisions.md#history)', history)
        self.assertIn('(roadmap.md)', delivery)
        self.assertIn('(roadmap.md)', history)
        self.assertIn('### Iterations', delivery)
        self.assertIn('(iterations.md#i1)', delivery)
        self.assertNotIn('Occurrence criterion', main)
        self.assertIn('Occurrence criterion', delivery)
        self.assertEqual(output['roadmap.svg'], renderer.svg(data))

    def test_split_empty_plan_omits_empty_children(self):
        data = iteration_sample()
        data.update(views=['requirements'], entries=[], versions=[], phases=[], milestones=[], iterations=[])
        output = renderer.documents(renderer.validate(data), 'split')
        self.assertEqual(set(output), {'roadmap.md'})
        self.assertNotIn('roadmap-delivery.md', output['roadmap.md'])
        self.assertNotIn('roadmap-history.md', output['roadmap.md'])

    def test_cli_layout_switch_removes_only_stale_reserved_views(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp) / 'input.json', Path(tmp) / 'out'
            data = iteration_sample('dates')
            data['revisions'] = revision_sample()['revisions']
            source.write_text(json.dumps(data))
            command = [sys.executable, str(SCRIPT), str(source), '--output-dir', str(out)]
            result = subprocess.run(command + ['--layout', 'split'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((out / 'roadmap-delivery.md').exists())
            self.assertTrue((out / 'roadmap-history.md').exists())
            self.assertIn('I1', (out / 'roadmap.mmd').read_text())
            (out / 'notes.md').write_text('Keep this source')
            result = subprocess.run(command + ['--overwrite'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((out / 'roadmap-delivery.md').exists())
            self.assertFalse((out / 'roadmap-history.md').exists())
            self.assertEqual((out / 'notes.md').read_text(), 'Keep this source')

    def test_cli_preflights_children_before_writing_anything(self):
        for hazard in ('symlink', 'hardlink', 'directory', 'exists'):
            with self.subTest(hazard=hazard), tempfile.TemporaryDirectory() as tmp:
                source, out = Path(tmp) / 'input.json', Path(tmp) / 'out'
                source.write_text(json.dumps(iteration_sample()))
                original = source.read_bytes()
                out.mkdir()
                child = out / 'roadmap-delivery.md'
                if hazard == 'symlink':
                    child.symlink_to(source)
                elif hazard == 'hardlink':
                    child.hardlink_to(source)
                elif hazard == 'directory':
                    child.mkdir()
                else:
                    child.write_text('Existing detail')
                flags = [] if hazard == 'exists' else ['--overwrite']
                result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                    '--output-dir', str(out), '--layout', 'split'] + flags, capture_output=True, text=True)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertFalse((out / 'roadmap.md').exists())
                self.assertEqual(source.read_bytes(), original)

    def test_cli_rejects_output_aliases_before_layout_switch(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp) / 'input.json', Path(tmp) / 'out'
            source.write_text(json.dumps(iteration_sample()))
            out.mkdir()
            (out / 'roadmap.md').write_text('Preserve aliased content')
            (out / 'roadmap-delivery.md').hardlink_to(out / 'roadmap.md')
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), '--output-dir',
                str(out), '--layout', 'split', '--overwrite'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual((out / 'roadmap.md').read_text(), 'Preserve aliased content')

    def test_iteration_limits_unknowns_and_no_selected_schedule(self):
        data = iteration_sample()
        data['schedule']['items'][-1].update(start=None, end=None)
        self.assertIn('Unscheduled', renderer.markdown(renderer.validate(data)))
        data['views'].remove('schedule')
        data['iterations'][0].update(members=[], owner='Unknown', board=None)
        output = renderer.markdown(renderer.validate(data))
        self.assertIn('Unassigned', output)
        self.assertNotIn('[Board]', output)
        data['iterations'] = [dict(data['iterations'][0], id=f'I{i}') for i in range(201)]
        with self.assertRaisesRegex(ValueError, 'at most 200'):
            renderer.validate(data)

    def test_legacy_schemas_support_explicit_split_without_upgrade_or_mutation(self):
        for data in (sample(), event_sample(), revision_sample()):
            original = copy.deepcopy(data)
            outputs = renderer.documents(renderer.validate(data), 'split')
            self.assertIn('roadmap-delivery.md', outputs)
            self.assertIn('(roadmap.md)', outputs['roadmap-delivery.md'])
            self.assertEqual(outputs['roadmap.svg'], renderer.svg(data))
            self.assertNotIn('### Iterations', outputs['roadmap-delivery.md'])
            self.assertEqual('roadmap-history.md' in outputs, data['schema_version'] == '1.2')
            self.assertEqual(data, original)
            self.assertEqual(outputs, renderer.documents(data, 'split'))

    def test_revision_summary_links_evidence_when_schema_1_2_is_used(self):
        """Covers: roadmap-capabilities#AC11; summary retains why and impact."""
        data = renderer.validate(revision_sample())
        output = renderer.markdown(data)
        self.assertIn('## Revision history', output)
        self.assertIn('R1: V1 → V2', output)
        self.assertIn('Export moves three weeks', output)
        self.assertIn('(decisions.md#rev1)', output)

    def test_revision_compaction_keeps_recent_five_when_history_is_linked(self):
        """Covers: roadmap-capabilities#AC12; hiding rows does not erase history."""
        data = revision_sample()
        data['revisions'] = [dict(data['revisions'][0], id=f'REV{i}',
                                  change=f'Change {i}') for i in range(7, 0, -1)]
        data['revision_history'] = 'decisions.md#history'
        before = copy.deepcopy(data)

        output = renderer.markdown(renderer.validate(data))

        self.assertIn('REV7', output)
        self.assertIn('REV3', output)
        self.assertNotIn('REV2', output)
        self.assertIn('decisions.md#history', output)
        self.assertIn('2 older revisions', output)
        self.assertEqual(data, before)
        self.assertEqual(renderer.markdown(data), output)

    def test_cli_delivers_revision_evidence_links_when_input_uses_schema_1_2(self):
        """Covers: roadmap-capabilities#AC12; verify real serialization and output."""
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            data = revision_sample()
            data['revisions'][0]['source'] = '../decisions.md#rev1'
            (base / 'decisions.md').write_text('# Decisions\n\n## REV1\nConfirmed change.\n')
            source, out = base / 'input.json', base / 'out'
            source.write_text(json.dumps(data))

            result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                                     '--output-dir', str(out)], capture_output=True, text=True)

            self.assertEqual(result.returncode, 0, result.stderr)
            output = (out / 'roadmap.md').read_text()
            self.assertIn('2026-10-20 · REV1', output)
            self.assertIn('(../decisions.md#rev1)', output)
            self.assertEqual((out / '../decisions.md').resolve(), (base / 'decisions.md').resolve())
            self.assertTrue((out / 'roadmap.svg').exists())

    def test_cli_writes_nothing_when_required_revision_evidence_is_missing(self):
        """Covers: roadmap-capabilities#AC13."""
        with tempfile.TemporaryDirectory() as tmp:
            source, out = Path(tmp) / 'input.json', Path(tmp) / 'out'
            data = revision_sample()
            data['revisions'][0].pop('impact')
            source.write_text(json.dumps(data))

            result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                                     '--output-dir', str(out)], capture_output=True, text=True)

            self.assertEqual(result.returncode, 1)
            self.assertIn('REV1.impact', result.stderr)
            self.assertFalse(out.exists())

    def test_revision_validation_rejects_missing_or_inconsistent_evidence(self):
        """Covers: roadmap-capabilities#AC13; invalid history fails at input."""
        mutations = [
            (lambda d: d.pop('revisions'), 'revisions'),
            (lambda d: d['revisions'][0].update(reason=''), 'reason'),
            (lambda d: d['revisions'][0].update(source='javascript:bad'), 'source'),
            (lambda d: d['revisions'][0].update(date='2026-02-30'), 'date'),
            (lambda d: d['revisions'][0].update(date='2026-10-21'), 'updated'),
            (lambda d: d['revisions'].append(copy.deepcopy(d['revisions'][0])), 'duplicate'),
            (lambda d: d['revisions'].append(dict(d['revisions'][0], id='REV2',
                                                 date='2026-10-21')), 'updated')]
        for mutate, error in mutations:
            data = revision_sample()
            mutate(data)
            with self.subTest(error=error), self.assertRaisesRegex(ValueError, error):
                renderer.validate(data)

    def test_compacted_revision_input_requires_full_history_reference(self):
        data = revision_sample()
        data['revisions'] = [dict(data['revisions'][0], id=f'REV{i}') for i in range(6)]
        with self.assertRaisesRegex(ValueError, 'revision_history'):
            renderer.validate(data)

    def test_revision_limit_accepts_200_records_with_retained_history(self):
        data = revision_sample()
        data['revisions'] = [dict(data['revisions'][0], id=f'REV{i}') for i in range(200)]
        data['revision_history'] = 'decisions.md#history'
        output = renderer.markdown(renderer.validate(data))
        self.assertIn('195 older revisions', output)
        self.assertNotIn('REV5', output)

    def test_revision_dates_require_newest_first_order(self):
        data = revision_sample()
        data['revisions'][0]['date'] = '2026-10-18'
        data['revisions'].append(dict(data['revisions'][0], id='REV2', date='2026-10-19'))
        with self.assertRaisesRegex(ValueError, 'newest first'):
            renderer.validate(data)

    def test_legacy_inputs_ignore_revision_metadata_without_inventing_history(self):
        for version in ('1.0', '1.1'):
            data = sample()
            data.update(schema_version=version, revisions={'unmodeled': 'metadata'})
            self.assertNotIn('## Revision history', renderer.markdown(renderer.validate(data)))
        data = revision_sample()
        data['revisions'] = []
        self.assertIn('No material revisions recorded', renderer.markdown(renderer.validate(data)))

    def test_revision_display_escapes_text_and_bounds_record_count(self):
        data = revision_sample()
        data['revisions'][0]['change'] = '<script> | [link]'
        output = renderer.markdown(renderer.validate(data))
        self.assertIn('&lt;script&gt;', output)
        self.assertNotIn('<script>', output)
        data['revisions'] = [dict(data['revisions'][0], id=f'REV{i}') for i in range(201)]
        with self.assertRaisesRegex(ValueError, '200'):
            renderer.validate(data)

    def test_independent_phase_and_event_share_version_context(self):
        data = renderer.validate(event_sample())
        result = renderer.markdown(data)
        self.assertIn('## Phases', result)
        self.assertIn('## Milestones', result)
        self.assertIn('Reviewer signs acceptance', result)
        self.assertIn('planned', renderer.svg(data))
        self.assertEqual(len(ET.fromstring(renderer.svg(data)).findall(
            './/{http://www.w3.org/2000/svg}polygon[@class="milestone"]')), 1)

    def test_event_state_requires_evidence_and_actual_requires_reached(self):
        for changes, message in [({'state': 'reached'}, 'evidence'),
                                 ({'evidence': 'javascript:bad'}, 'evidence')]:
            data = event_sample()
            data['milestones'][0].update(changes)
            with self.assertRaisesRegex(ValueError, message):
                renderer.validate(data)
        data = event_sample()
        data['schedule']['items'][-1]['basis'] = 'actual'
        with self.assertRaisesRegex(ValueError, 'reached'):
            renderer.validate(data)
        data['milestones'][0].update(state='reached', evidence='approval.md#signed')
        renderer.validate(data)

    def test_unknown_event_is_not_drawn_and_global_event_is_valid(self):
        data = event_sample()
        data['milestones'][0]['related'] = []
        data['schedule']['items'][-1].update(start=None, end=None)
        result = renderer.svg(renderer.validate(data))
        self.assertIn('Unscheduled', result)
        self.assertNotIn('<polygon', result)

    def test_event_relationships_and_schema_boundaries(self):
        mutations = [
            (lambda d: d.update(schema_version='1.0'), '1.1'),
            (lambda d: d['phases'][0].update(scope=['PH1']), 'scope'),
            (lambda d: d['milestones'][0].update(related=['missing']), 'related'),
            (lambda d: d['schedule']['items'][-1].update(kind='span', end=4), 'kind'),
            (lambda d: d['schedule']['items'][0].update(kind='milestone', end=1), 'kind'),
            (lambda d: d['milestones'][0].update(id='V1'), 'duplicate')]
        for mutate, message in mutations:
            data = event_sample()
            mutate(data)
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, message):
                renderer.validate(data)

    def test_dated_independent_events_render_without_inferred_dates(self):
        data = event_sample()
        data['schedule'].update(mode='dates', origin='ISO calendar dates')
        for item in data['schedule']['items']:
            item['start'] = '2026-11-02' if item['start'] == 1 else '2026-11-16'
            item['end'] = '2026-11-16'
        valid = renderer.validate(data)
        output = renderer.mermaid(valid)
        self.assertIn('V1, 2026-11-02, 14d', output)
        self.assertIn('PH1, 2026-11-02, 14d', output)
        self.assertIn('milestone, M1, 2026-11-16, 0d', output)
        self.assertIn('planned', output)
        data['schedule']['items'][-1].update(start=None, end=None)
        self.assertNotIn('milestone, M1', renderer.mermaid(renderer.validate(data)))

    def test_mermaid_ignores_unmodeled_state_when_record_is_not_a_milestone(self):
        """Covers: roadmap-capabilities#AC8; only milestone objects own event state."""
        data = sample('dates')
        expected = renderer.mermaid(renderer.validate(data))
        data['versions'][0]['state'] = {'status': 'draft'}

        output = renderer.mermaid(renderer.validate(data))

        self.assertEqual(output, expected)

    def test_cli_renders_independent_objects_when_input_uses_schema_1_1(self):
        """Covers: roadmap-capabilities#AC8; cross the real CLI/JSON/output boundary."""
        for mode in ('weeks', 'dates'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                source = Path(tmp) / 'input.json'
                out = Path(tmp) / 'output'
                data = event_sample(mode)
                data['versions'][0]['state'] = {'status': 'draft'}
                data['phases'][0]['state'] = {'status': 'draft'}
                source.write_text(json.dumps(data), encoding='utf-8')

                result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                                         '--output-dir', str(out)], capture_output=True, text=True)

                self.assertEqual(result.returncode, 0, result.stderr)
                markdown = (out / 'roadmap.md').read_text(encoding='utf-8')
                self.assertIn('## Phases', markdown)
                self.assertIn('Reviewer signs acceptance', markdown)
                svg = ET.fromstring((out / 'roadmap.svg').read_text(encoding='utf-8'))
                self.assertEqual(len(svg.findall(
                    './/{http://www.w3.org/2000/svg}polygon[@class="milestone"]')), 1)
                self.assertIn('First delivery', ''.join(svg.itertext()))
                self.assertIn('planned', ''.join(svg.itertext()))
                self.assertEqual((out / 'roadmap.mmd').exists(), mode == 'dates')
                if mode == 'dates':
                    self.assertIn('milestone, M1, 2026-11-16, 0d',
                                  (out / 'roadmap.mmd').read_text(encoding='utf-8'))

    def test_terminal_event_states_and_source_links_are_validated(self):
        for state in ('reached', 'missed', 'cancelled'):
            data = event_sample()
            data['milestones'][0].update(state=state, evidence='review.md#decision')
            renderer.validate(data)
            data['milestones'][0]['evidence'] = None
            with self.assertRaisesRegex(ValueError, 'evidence'):
                renderer.validate(data)
        data = event_sample()
        data['phases'][0]['source'] = '//external.invalid/path'
        with self.assertRaisesRegex(ValueError, 'source'):
            renderer.validate(data)

    def test_relative_schedule_has_shared_refs_and_valid_svg(self):
        data = renderer.validate(sample())
        root = ET.fromstring(renderer.svg(data))
        text = ''.join(root.itertext())
        self.assertIn('W1', text)
        self.assertIn('First delivery', text)
        self.assertIn('target', text)
        self.assertIn('R1', renderer.markdown(data))
        self.assertIn('W1–W2', renderer.markdown(data))
        self.assertIn('Make request handling dependable', renderer.markdown(data))
        self.assertIn('Search enables export', renderer.markdown(data))

    def test_dated_mermaid_uses_real_dates_and_escaped_labels(self):
        data = sample('dates')
        data['versions'][0]['name'] = 'end : x\nclick javascript'
        data = renderer.validate(data)
        result = renderer.mermaid(data)
        self.assertIn('2026-11-02, 14d', result)
        self.assertNotIn('\nclick javascript', result)
        self.assertNotIn('end :', result)

    def test_week_mode_cannot_manufacture_mermaid_dates(self):
        with self.assertRaisesRegex(ValueError, 'dates'):
            renderer.mermaid(renderer.validate(sample()))

    def test_unknown_execution_is_not_guessed(self):
        data = sample()
        data['entries'][0]['execution'] = None
        result = renderer.markdown(renderer.validate(data))
        self.assertIn('Unverified execution mappings: R1', result)
        self.assertNotIn('Not started', result)

    def test_unknown_schedule_is_visible_and_not_a_milestone(self):
        data = sample()
        data['schedule']['items'][0].update(start=None, end=None)
        self.assertIn('Unscheduled', renderer.svg(renderer.validate(data)))

    def test_isolated_unscheduled_item_does_not_imply_unverified_dependency(self):
        data = sample()
        data['schedule']['items'][0].update(start=None, end=None)
        result = renderer.markdown(renderer.validate(data))
        self.assertIn('Unscheduled: V1', result)
        self.assertNotIn('Unverified timing for dependencies', result)

    def test_unknown_prerequisite_timing_is_reported_on_its_edge(self):
        data = sample()
        data['schedule']['items'][0].update(start=None, end=None)
        data['schedule']['items'].append(dict(ref='R1', kind='span', basis='target',
                                             start=3, end=5, depends_on=['V1']))
        result = renderer.markdown(renderer.validate(data))
        self.assertIn('Unverified dependency timing: V1 → R1', result)

    def test_bad_inputs_are_rejected(self):
        mutations = [
            (lambda d: d['entries'].append(copy.deepcopy(d['entries'][0])), 'duplicate'),
            (lambda d: d['versions'][0].update(members=['missing']), 'member'),
            (lambda d: d['entries'][0].update(source='javascript:alert(1)'), 'source'),
            (lambda d: d['entries'][0].update(source='//example.com/path'), 'source'),
            (lambda d: d['entries'][0].update(execution='At risk'), 'execution'),
            (lambda d: d['schedule']['items'][0].update(end=0), 'end'),
            (lambda d: d['schedule']['items'][0].update(end=None), 'endpoints'),
            (lambda d: d['schedule']['items'][0].update(depends_on=['missing']), 'dependency'),
            (lambda d: d['schedule']['items'][0].update(start=True), 'start'),
            (lambda d: d.update(updated='2026-02-30'), 'updated'),
            (lambda d: d['schedule']['items'][0].update(end=110), 'horizon'),
            (lambda d: d.update(project='x' * 201), 'project'),
        ]
        for mutate, message in mutations:
            with self.subTest(message=message):
                data = sample()
                mutate(data)
                with self.assertRaisesRegex(ValueError, message):
                    renderer.validate(data)

    def test_cycles_and_overlap_are_different_failures(self):
        data = sample()
        data['schedule']['items'].append(dict(ref='R1', kind='span', basis='committed',
                                             start=2, end=4, depends_on=['V1']))
        with self.assertRaisesRegex(ValueError, 'overlap'):
            renderer.validate(data)
        data['schedule']['items'][0]['depends_on'] = ['R1']
        with self.assertRaisesRegex(ValueError, 'cycle'):
            renderer.validate(data)

    def test_milestone_has_zero_duration_and_dependency_marker(self):
        data = sample()
        data['schedule']['items'].append(dict(ref='R1', kind='milestone', basis='target',
                                             start=3, end=3, depends_on=['V1']))
        root = ET.fromstring(renderer.svg(renderer.validate(data)))
        self.assertTrue(root.findall('.//{http://www.w3.org/2000/svg}polygon'))
        self.assertTrue(root.findall('.//{http://www.w3.org/2000/svg}path'))

    def test_single_view_and_empty_tiers_remain_valid(self):
        data = sample()
        data.update(views=['requirements'], entries=[])
        data.pop('schedule')
        data.pop('versions')
        result = renderer.markdown(renderer.validate(data))
        self.assertIn('No items planned', result)
        self.assertNotIn('## Versions', result)

    def test_unassigned_entries_are_visible(self):
        data = sample()
        data['versions'][0]['members'] = []
        self.assertIn('Unassigned: R1', renderer.markdown(renderer.validate(data)))

    def test_key_condition_links_to_its_source_evidence(self):
        result = renderer.markdown(renderer.validate(sample()))
        self.assertIn('[Review results](requirements/search.md#acceptance)', result)

    def test_generation_is_deterministic_and_does_not_mutate_input(self):
        data = sample()
        before = copy.deepcopy(data)
        valid = renderer.validate(data)
        self.assertEqual(renderer.svg(valid), renderer.svg(valid))
        self.assertEqual(data, before)

    def test_xml_control_characters_are_rejected_before_rendering(self):
        data = sample()
        data['project'] = 'Desk\x00secret'
        with self.assertRaisesRegex(ValueError, 'project'):
            renderer.validate(data)

    def test_cli_reports_non_utf8_input_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'bad.json'
            source.write_bytes(b'\xff')
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), '--check'],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn('Traceback', result.stderr)

    def test_last_supported_date_can_be_a_standalone_milestone(self):
        data = sample('dates')
        data['schedule']['items'][0].update(kind='milestone', start='9999-12-31', end='9999-12-31')
        self.assertIn('9999-12-31', renderer.svg(renderer.validate(data)))

    def test_record_count_and_duplicate_version_members_are_bounded(self):
        data = sample()
        data['versions'][0]['members'] = ['R1', 'R1']
        with self.assertRaisesRegex(ValueError, 'duplicate version'):
            renderer.validate(data)
        data = sample()
        data['entries'] = [dict(data['entries'][0], id=f'R{i}') for i in range(201)]
        with self.assertRaisesRegex(ValueError, '200'):
            renderer.validate(data)

    def test_cli_preserves_input_when_output_is_a_hard_link(self):
        """Covers: roadmap-capabilities#AC4; overwrite never targets the input file."""
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input.json'
            original = json.dumps(sample())
            source.write_text(original, encoding='utf-8')
            out = Path(tmp) / 'output'
            out.mkdir()
            (out / 'roadmap.md').hardlink_to(source)

            result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                                     '--output-dir', str(out), '--overwrite'],
                                    capture_output=True, text=True)

            self.assertEqual(result.returncode, 1, result.stderr)
            self.assertEqual(source.read_text(encoding='utf-8'), original)
            self.assertIn('input must not be an output file', result.stderr)
            self.assertFalse((out / 'roadmap.svg').exists())

    def test_cli_preserves_external_hardlinked_files_before_any_write(self):
        for name in ('roadmap.md', '.roadmap-outputs.json'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                out = root / 'out'
                out.mkdir()
                original = root / 'original.md'
                original.write_text('{}' if name.endswith('.json') else 'Preserve external source')
                before = original.read_bytes()
                (out / name).hardlink_to(original)
                result = subprocess.run([sys.executable, str(SCRIPT), '--blank',
                                         '--overwrite', '--output-dir', str(out)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertIn('hardlink', result.stderr)
                self.assertEqual(original.read_bytes(), before)
                self.assertEqual({p.name for p in out.iterdir()}, {name})

    def test_cli_will_not_replace_an_output_symlink(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / 'input.json'
            source.write_text(json.dumps(sample()))
            out = base / 'out'
            out.mkdir()
            evidence = base / 'evidence.md'
            evidence.write_text('preserve source')
            (out / 'roadmap.md').symlink_to(evidence)
            result = subprocess.run([sys.executable, str(SCRIPT), str(source),
                                     '--output-dir', str(out), '--overwrite'], capture_output=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(evidence.read_text(), 'preserve source')

    def test_cli_preflight_and_stale_output_removal(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / 'input.json'
            out = base / 'out'
            source.write_text(json.dumps(sample('dates')))
            command = [sys.executable, str(SCRIPT), str(source), '--output-dir', str(out)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            old = (out / 'roadmap.md').read_text()
            self.assertTrue((out / 'roadmap.mmd').exists())
            (out / 'notes.txt').write_text('keep')
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertEqual((out / 'roadmap.md').read_text(), old)
            source.write_text(json.dumps(sample()))
            self.assertEqual(subprocess.run(command + ['--overwrite'], capture_output=True).returncode, 0)
            self.assertFalse((out / 'roadmap.mmd').exists())
            self.assertEqual((out / 'notes.txt').read_text(), 'keep')

    def test_invalid_input_and_check_mode_write_nothing(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / 'input.json'
            out = Path(tmp) / 'output'
            data = sample()
            source.write_text(json.dumps(data))
            command = [sys.executable, str(SCRIPT), str(source), '--output-dir', str(out)]
            self.assertEqual(subprocess.run(command + ['--check'], capture_output=True).returncode, 0)
            self.assertFalse(out.exists())
            data['schedule']['items'][0]['end'] = -1
            source.write_text(json.dumps(data))
            self.assertNotEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertFalse(out.exists())

    def test_switching_to_single_view_removes_only_generated_diagrams(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            source = base / 'input.json'
            source.write_text(json.dumps(sample('dates')))
            out = base / 'output'
            command = [sys.executable, str(SCRIPT), str(source), '--output-dir', str(out)]
            self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
            self.assertTrue((out / 'roadmap.svg').exists())
            data = sample()
            data['views'] = ['requirements']
            source.write_text(json.dumps(data))
            self.assertEqual(subprocess.run(command + ['--overwrite'], capture_output=True).returncode, 0)
            self.assertFalse((out / 'roadmap.svg').exists())
            self.assertFalse((out / 'roadmap.mmd').exists())


class StructureGenerationTests(unittest.TestCase):
    """Covers: roadmap-generation-workflow#G1–G4."""

    TOPICS = {'roadmap.md', 'iterations.md', 'versions.md', 'milestones.md',
              'roadmap-planning-basis.md', 'roadmap-history.md'}

    def test_blank_generation_needs_no_business_input_and_is_clean_in_both_locales(self):
        for locale in ['en', 'zh-CN']:
            with self.subTest(locale=locale), tempfile.TemporaryDirectory() as temp:
                result = subprocess.run([sys.executable, str(SCRIPT), '--blank', '--locale', locale,
                                         '--output-dir', temp], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                files = list(Path(temp).glob('*.md'))
                self.assertEqual({p.name for p in files}, self.TOPICS)
                for path in files:
                    text = path.read_text()
                    self.assertNotRegex(text, r'BUG1|R1|V1|I1|<!--|<details>|Instructions:')
                    for block in text.strip().split('\n\n'):
                        self.assertTrue(block.startswith(('#', '**', '|', '[')), block)
                    for block in re.findall(r'(?:^\|.*\|\n)+', text, re.M):
                        self.assertEqual(len(block.strip().splitlines()), 2)
                self.assertIn('{待填写}' if locale == 'zh-CN' else '{Pending}',
                              (Path(temp) / 'roadmap.md').read_text())

    def test_blank_rejects_business_input_and_incompatible_modes_without_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'input.json'
            source.write_text(json.dumps(sample()))
            for extra in [[str(source)], ['--recommend'], ['--layout', 'split']]:
                output = Path(temp) / 'out'
                result = subprocess.run([sys.executable, str(SCRIPT), '--blank', *extra,
                                         '--output-dir', str(output)], capture_output=True, text=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(output.exists())

    def test_blank_check_does_not_create_destination(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / 'out'
            result = subprocess.run([sys.executable, str(SCRIPT), '--blank', '--check',
                                     '--output-dir', str(out)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(out.exists())

    def test_topic_layout_preserves_source_facts_and_six_markdown_roles(self):
        for locale in ['en', 'zh-CN']:
            data = language_sample(locale)
            data['schema_version'] = '1.6'
            data['selection']['layout'] = 'topic-split'
            outputs = renderer.documents(renderer.validate(data))
            self.assertEqual({n for n in outputs if n.endswith('.md')}, self.TOPICS)
            self.assertNotIn('roadmap-delivery.md', '\n'.join(outputs.values()))
            self.assertIn('R1', outputs['roadmap.md'])
            self.assertIn('I1', outputs['iterations.md'])
            self.assertIn('V1', outputs['versions.md'])
            self.assertIn('M1', outputs['milestones.md'])
            self.assertIn('PH1', outputs['roadmap-planning-basis.md'])
            self.assertNotIn('<details>', '\n'.join(outputs.values()))
            self.assertIn('roadmap.svg', outputs)

    def test_population_keeps_the_confirmed_blank_headings_and_column_shapes(self):
        for locale in ['en', 'zh-CN']:
            data = language_sample(locale)
            data['schema_version'] = '1.6'
            data['selection']['layout'] = 'topic-split'
            empty = renderer.blank_documents(locale)
            filled = renderer.documents(renderer.validate(data))
            for name in self.TOPICS:
                self.assertEqual(re.findall(r'^## .+$', empty[name], re.M),
                                 re.findall(r'^## .+$', filled[name], re.M), name)
                headers = lambda value: [b.splitlines()[0] for b in re.findall(r'(?:^\|.*\|\n)+', value, re.M)]
                self.assertEqual(headers(empty[name]), headers(filled[name]), name)
                self.assertNotRegex(filled[name], r'\{Pending\}|\{待填写\}')

    def test_completed_records_are_retained_without_html_or_active_priority_rows(self):
        data = language_sample('en')
        data['schema_version'] = '1.6'
        data['selection']['layout'] = 'topic-split'
        data['entries'][0]['execution'] = 'Completed'
        output = renderer.documents(renderer.validate(data))
        self.assertNotIn('<details>', output['roadmap.md'])
        self.assertNotIn('| [R1 ·', output['roadmap.md'])
        self.assertIn('R1', output['roadmap-history.md'])

    def test_topic_flow_retains_policy_without_inventing_iterations(self):
        data = json.loads((ROOT / 'skills/define-roadmap/references/scenarios/continuous-flow/input.json').read_text())
        data['schema_version'] = '1.6'
        data['selection']['layout'] = 'topic-split'
        data['language'] = dict(locale='en', basis='user', source='policy.md', rationale='Test locale')
        output = renderer.documents(renderer.validate(data))
        self.assertIn(data['flow']['policy'], output['roadmap-planning-basis.md'])
        self.assertNotIn('| I1', output['iterations.md'])

    def test_topic_preserves_history_link_and_supporting_view_contracts(self):
        data = language_sample('en')
        data['schema_version'] = '1.6'
        data['selection']['layout'] = 'topic-split'
        data['revision_history'] = 'history.md#all-decisions'
        outputs = renderer.documents(renderer.validate(data))
        self.assertIn('history.md#all-decisions', outputs['roadmap-history.md'])
        self.assertIn(data['phases'][0]['owner'], outputs['roadmap-planning-basis.md'])
        self.assertIn('exclusive', outputs['roadmap.md'])
        flow = json.loads((ROOT / 'skills/define-roadmap/references/scenarios/continuous-flow/input.json').read_text())
        flow.update(schema_version='1.6', language=data['language'])
        flow['selection']['layout'] = 'topic-split'
        result = renderer.documents(renderer.validate(flow))
        self.assertIn(flow['flow']['board'], result['roadmap-planning-basis.md'])

    def test_blank_check_rejects_broken_bundled_templates_before_writing(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bundle = root / 'skill'
            (bundle / 'scripts').mkdir(parents=True)
            assets = bundle / 'assets/structure-first'
            assets.mkdir(parents=True)
            copyfile(SCRIPT, bundle / 'scripts/render-roadmap.py')
            for source in (SCRIPT.parents[1] / 'assets/structure-first').glob('*.md'):
                copyfile(source, assets / source.name)
            main = assets / 'roadmap.md'
            main.write_text(main.read_text() + '\nInstructions: invent dates to fill this table.\n')
            output = root / 'out'
            result = subprocess.run([sys.executable, str(bundle / 'scripts/render-roadmap.py'),
                '--blank', '--check', '--output-dir', str(output)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('blank structure', result.stderr)
            self.assertFalse(output.exists())

    def test_owned_topic_to_single_transition_removes_only_generated_details(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, out = root / 'input.json', root / 'out'
            data = language_sample('en')
            data['schema_version'] = '1.6'
            data['selection']['layout'] = 'topic-split'
            source.write_text(json.dumps(data))
            cmd = [sys.executable, str(SCRIPT), str(source), '--output-dir', str(out), '--overwrite']
            subprocess.run(cmd, check=True, capture_output=True)
            (out / 'team-notes.md').write_text('Keep')
            data['selection']['layout'] = 'single'
            source.write_text(json.dumps(data))
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({p.name for p in out.glob('*.md')}, {'roadmap.md', 'team-notes.md'})
            self.assertEqual((out / 'team-notes.md').read_text(), 'Keep')

    def test_unowned_old_delivery_file_blocks_reset_without_partial_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            (out / 'roadmap-delivery.md').write_text('Unowned business evidence')
            result = subprocess.run([sys.executable, str(SCRIPT), '--blank', '--overwrite',
                '--output-dir', temp], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual({p.name for p in out.iterdir()}, {'roadmap-delivery.md'})

    def test_unknown_supporting_phase_owner_uses_the_selected_locale(self):
        data = language_sample('zh-CN')
        data['schema_version'] = '1.6'
        data['selection']['layout'] = 'topic-split'
        data['phases'][0]['owner'] = 'Unknown'
        outputs = renderer.documents(renderer.validate(data))
        self.assertIn('负责人： 未知', outputs['roadmap-planning-basis.md'])

    def test_check_mode_rejects_conflicting_retained_layout(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / 'input.json'
            data = language_sample('en')
            source.write_text(json.dumps(data))
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), '--check',
                '--layout', 'single'], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('conflicts', result.stderr)

    def test_retained_topic_selection_cannot_be_overridden_by_cli(self):
        data = language_sample('en')
        data['schema_version'] = '1.6'
        data['selection']['layout'] = 'topic-split'
        renderer.validate(data)
        with self.assertRaisesRegex(ValueError, 'conflicts'):
            renderer.documents(data, 'split')

    def test_topic_is_not_silently_added_to_older_selection_contracts(self):
        data = language_sample('en')
        data['selection']['layout'] = 'topic-split'
        with self.assertRaises(ValueError):
            renderer.validate(data)

    def test_blank_overwrite_is_idempotent_and_preserves_unrelated_files(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            cmd = [sys.executable, str(SCRIPT), '--blank', '--output-dir', temp]
            first = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            before = {p.name: (p.read_bytes(), p.stat().st_mtime_ns) for p in out.iterdir()}
            refused = subprocess.run(cmd, capture_output=True, text=True)
            self.assertNotEqual(refused.returncode, 0)
            unrelated = out / 'team-notes.md'
            unrelated.write_text('Keep this file.\n')
            rerun = subprocess.run(cmd + ['--overwrite'], capture_output=True, text=True)
            self.assertEqual(rerun.returncode, 0, rerun.stderr)
            for name, value in before.items():
                path = out / name
                self.assertEqual((path.read_bytes(), path.stat().st_mtime_ns), value)
            self.assertEqual(unrelated.read_text(), 'Keep this file.\n')

    def test_reset_removes_only_intact_owned_graphics_and_retains_unrelated_work(self):
        for mode in ['weeks', 'dates']:
            with tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                out = root / 'out'
                source = root / 'input.json'
                data = language_sample('en', mode)
                data['schema_version'] = '1.6'
                data['selection']['layout'] = 'topic-split'
                source.write_text(json.dumps(data))
                subprocess.run([sys.executable, str(SCRIPT), str(source), '--output-dir', str(out)], check=True, capture_output=True)
                self.assertTrue((out / 'roadmap.svg').exists())
                self.assertEqual((out / 'roadmap.mmd').exists(), mode == 'dates')
                (out / 'team-notes.md').write_text('Keep')
                reset = [sys.executable, str(SCRIPT), '--blank', '--overwrite', '--output-dir', str(out)]
                subprocess.run(reset, check=True, capture_output=True)
                self.assertFalse((out / 'roadmap.svg').exists())
                self.assertFalse((out / 'roadmap.mmd').exists())
                self.assertEqual((out / 'team-notes.md').read_text(), 'Keep')
                self.assertNotIn('R1', (out / 'roadmap.md').read_text())


    def test_modified_stale_graphic_is_not_deleted_or_partially_reset(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            out = root / 'out'
            source = root / 'input.json'
            data = language_sample('en')
            data['schema_version'] = '1.6'
            data['selection']['layout'] = 'topic-split'
            source.write_text(json.dumps(data))
            subprocess.run([sys.executable, str(SCRIPT), str(source), '--output-dir', str(out)], check=True, capture_output=True)
            (out / 'roadmap.svg').write_text('User edited graphic')
            before = {p.name: p.read_bytes() for p in out.iterdir()}
            result = subprocess.run([sys.executable, str(SCRIPT), '--blank', '--overwrite', '--output-dir', str(out)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('stale generated output was edited', result.stderr)
            self.assertEqual(before, {p.name: p.read_bytes() for p in out.iterdir()})

    def test_blank_refuses_symlink_outputs_and_does_not_write_partial_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / 'outside.md'
            target.write_text('Keep')
            out = root / 'out'
            out.mkdir()
            (out / 'iterations.md').symlink_to(target)
            result = subprocess.run([sys.executable, str(SCRIPT), '--blank', '--overwrite',
                                     '--output-dir', str(out)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('regular file', result.stderr)
            self.assertEqual(target.read_text(), 'Keep')
            self.assertFalse((out / 'roadmap.md').exists())


if __name__ == '__main__':
    unittest.main()

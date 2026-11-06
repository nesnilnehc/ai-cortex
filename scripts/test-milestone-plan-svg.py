#!/usr/bin/env python3
"""Exercise the standalone milestone renderer through its command line."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


SCRIPT = Path(__file__).resolve().parents[1] / 'skills/plan-milestones/scripts/render-plan.py'
NS = {'svg': 'http://www.w3.org/2000/svg'}


class MilestonePlanSvgTests(unittest.TestCase):
    def run_cli(self, milestones, locale='en'):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'plan.json'
            plan = json.dumps({'title': 'Launch & handoff', 'locale': locale,
                               'milestones': milestones})
            source.write_text(plan, encoding='utf-8')
            result = subprocess.run([sys.executable, '-B', SCRIPT, source],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(source.read_text(encoding='utf-8'), plan)
            return result

    def render(self, milestones, locale='en'):
        result = self.run_cli(milestones, locale)
        self.assertEqual(result.returncode, 0, result.stderr)
        return ET.fromstring(result.stdout)

    def test_calendar_scale_and_independent_timing_basis(self):
        svg = self.render([
            dict(id='A', name='Approval', timing=dict(basis='committed', date='2027-01-01')),
            dict(id='B', name='Review', timing=dict(basis='target', date='2027-01-11')),
            dict(id='C', name='Handoff', timing=dict(basis='target', start='2027-01-21',
                                                      end='2027-01-31', label='Late January')),
            dict(id='D', name='Recovery & <validation>', timing=None),
        ])
        rows = {row.get('data-id'): row for row in svg.findall('svg:g', NS)}
        self.assertEqual(list(rows), ['A', 'B', 'C', 'D'])
        self.assertIn('Committed', ' '.join(rows['A'].itertext()))
        self.assertIn('Target', ' '.join(rows['C'].itertext()))
        self.assertIn('Late January', ' '.join(rows['C'].itertext()))
        self.assertIn('Recovery & <validation>', ' '.join(rows['D'].itertext()))
        self.assertIn('Unscheduled', ' '.join(rows['D'].itertext()))
        self.assertIsNone(rows['D'].find('svg:polygon', NS))
        self.assertIsNone(rows['D'].find('svg:rect', NS))

        def center(row):
            point = row.find('svg:polygon', NS).get('points').split()[0]
            return float(point.split(',')[0])

        span = rows['C'].find('svg:rect', NS)
        self.assertAlmostEqual(center(rows['B']) - center(rows['A']),
                               float(span.get('x')) - center(rows['B']))
        self.assertAlmostEqual(float(span.get('width')), center(rows['B']) - center(rows['A']))

    def test_unplotted_rows_remain_visible_without_a_calendar(self):
        svg = self.render([dict(id='A', name='试点评审', timing=None),
                           dict(id='B', name='复盘', timing=dict(basis='target', label='试点后'))], 'zh-CN')
        self.assertIn('待定', ' '.join(svg.itertext()))
        self.assertIn('目标 · 试点后', ' '.join(svg.itertext()))
        self.assertEqual(svg.findall('.//svg:line[@class="grid"]', NS), [])
        self.assertEqual(svg.findall('svg:g/svg:polygon', NS), [])
        self.assertEqual(svg.findall('svg:g/svg:rect', NS), [])

    def test_a_single_point_at_the_date_limit_is_visible(self):
        svg = self.render([dict(id='A', name='Review', timing=dict(basis='target', date='9999-12-31'))])
        self.assertIsNotNone(svg.find('.//svg:polygon', NS))

    def test_reject_ambiguous_or_invalid_timing_and_duplicate_ids(self):
        for timing in (
            dict(basis='target', start='2027-02-01', end='2027-01-01'),
            dict(basis='target', start='2027-01-01'),
            dict(basis='actual', date='2027-01-01'),
            dict(basis='target', date='2027-02-29'),
            dict(basis='target', date='2027-01-01', start='2027-01-01', end='2027-02-01'),
        ):
            with self.subTest(timing=timing):
                result = self.run_cli([dict(id='A', name='Review', timing=timing)])
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(result.stdout, '')
                self.assertIn('A.timing', result.stderr)
        duplicate = self.run_cli([dict(id='A', name='Review', timing=None)] * 2)
        self.assertNotEqual(duplicate.returncode, 0)
        self.assertIn('duplicate', duplicate.stderr)


if __name__ == '__main__':
    unittest.main()

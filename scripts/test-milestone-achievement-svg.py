#!/usr/bin/env python3
"""Exercise the achievement calendar through its command line."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


SCRIPT = Path(__file__).resolve().parents[1] / 'skills/record-milestone-achievement/scripts/render-achievements.py'
NS = {'svg': 'http://www.w3.org/2000/svg'}


def run_json(source_text):
    with tempfile.TemporaryDirectory() as folder:
        source = Path(folder) / 'achievements.json'
        source.write_text(source_text, encoding='utf-8')
        return subprocess.run([sys.executable, '-B', SCRIPT, source], capture_output=True, check=False)


def run_cli(achievements, locale='en'):
    return run_json(json.dumps({'title': 'Release & adoption', 'locale': locale,
                                'achievements': achievements}))


class AchievementSvgTests(unittest.TestCase):
    def test_known_days_use_equal_spacing_and_coarser_dates_remain_text(self):
        result = run_cli([
            dict(id='M1', name='Pilot opened', date='2026-10-01'),
            dict(id='M2', name='Release approved', date='2026-10-11'),
            dict(id='M3', name='Launch verified', date='2026-10-21'),
            dict(id='M4', name='First <handoff>', date=None, label='October 2026'),
            dict(id='M5', name='Support accepted', date=None),
        ])
        self.assertEqual(result.returncode, 0, result.stderr)
        svg = ET.fromstring(result.stdout)
        self.assertIn('Actual occurrence', ' '.join(svg.itertext()))
        rows = {row.get('data-id'): row for row in svg.findall('svg:g', NS)}
        self.assertEqual(list(rows), ['M1', 'M2', 'M3', 'M4', 'M5'])
        points = [float(rows[ref].find('svg:polygon', NS).get('points').split(',')[0])
                  for ref in ('M1', 'M2', 'M3')]
        self.assertGreater(points[1], points[0])
        self.assertAlmostEqual(points[1] - points[0], points[2] - points[1])
        self.assertIn('Actual · 2026-10-01', ' '.join(rows['M1'].itertext()))
        self.assertIn('First <handoff>', ' '.join(rows['M4'].itertext()))
        self.assertIn('October 2026', ' '.join(rows['M4'].itertext()))
        self.assertIn('Date unknown', ' '.join(rows['M5'].itertext()))
        for ref in ('M4', 'M5'):
            self.assertIsNone(rows[ref].find('svg:polygon', NS))
        self.assertEqual(svg.findall('svg:g/svg:rect', NS), [])

    def test_all_unknown_days_keep_rows_without_an_axis(self):
        result = run_cli([dict(id='M1', name='交接完成', date=None)], 'zh-CN')
        self.assertEqual(result.returncode, 0, result.stderr)
        svg = ET.fromstring(result.stdout)
        self.assertIn('实际 · 日期未知', ' '.join(svg.itertext()))
        self.assertEqual(svg.findall('.//svg:line[@class="grid"]', NS), [])
        self.assertEqual(svg.findall('svg:g/svg:polygon', NS), [])

    def test_single_confirmed_day_uses_a_point_at_the_calendar_limit(self):
        result = run_cli([dict(id='M1', name='Pilot opened', date='0001-01-01')])
        self.assertEqual(result.returncode, 0, result.stderr)
        svg = ET.fromstring(result.stdout)
        self.assertIsNotNone(svg.find('svg:g/svg:polygon', NS))

    def test_rejects_invalid_actual_days_windows_and_duplicate_ids(self):
        base = dict(id='M1', name='Pilot opened', date=None)
        for rows, error in (
            ([dict(base, date='2026-02-30')], b'date'),
            ([dict(base, date='2026-10-01', label='2026-10-02')], b'label'),
            ([dict(base, start='2026-10-01', end='2026-10-21')], b'expected id'),
            ([base, base], b'duplicate'),
        ):
            with self.subTest(rows=rows):
                result = run_cli(rows)
                self.assertEqual(result.returncode, 1, result.stderr)
                self.assertEqual(result.stdout, b'')
                self.assertIn(error, result.stderr)

    def test_rejects_conflicting_dates_in_a_duplicate_json_field(self):
        result = run_json('''{"title":"Release", "achievements":[
            {"id":"M1", "name":"Opened", "date":"2026-10-01", "date":"2026-10-02"}
        ]}''')
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(result.stdout, b'')
        self.assertIn(b'duplicate JSON key: date', result.stderr)


if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""Render confirmed milestone achievements as a standalone SVG calendar."""

import argparse
from datetime import date
import importlib.util
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


ROADMAP_SCRIPT = Path(__file__).resolve().parents[2] / 'define-roadmap/scripts/render-roadmap.py'
SPEC = importlib.util.spec_from_file_location('roadmap_renderer', ROADMAP_SCRIPT)
roadmap = importlib.util.module_from_spec(SPEC)

WIDTH, ROW_HEIGHT = 1080, 62
EVENT_X, ACTUAL_X, LEFT, RIGHT = 24, 305, 512, 1032
CAPTIONS = {
    'en': ('Milestone', 'Actual occurrence', 'Calendar', 'Actual', 'Date unknown',
           'Points mark confirmed days. Rows without points have no confirmed calendar day.'),
    'zh-CN': ('里程碑', '实际发生时间', '日历', '实际', '日期未知',
              '点表示已确认的日期。无法确定具体日期的记录仅显示文字。'),
}


def unique_fields(pairs):
    fields = {}
    for key, value in pairs:
        if key in fields:
            raise ValueError(f'duplicate JSON key: {key}')
        fields[key] = value
    return fields


def read_rows(data, unknown):
    items = roadmap.array(data.get('achievements'), 'achievements')
    if len(items) > 200:
        raise ValueError('achievements: at most 200 rows')
    ids, rows = set(), []
    for index, value in enumerate(items):
        field = f'achievements[{index}]'
        item = roadmap.obj(value, field)
        if set(item) - {'id', 'name', 'date', 'label'} or 'date' not in item:
            raise ValueError(f'{field}: expected id, name, date (or null), and optional label')
        ref = roadmap.text(item.get('id'), field + '.id')
        if ref in ids:
            raise ValueError(f'{field}.id: duplicate ID {ref!r}')
        ids.add(ref)
        name = roadmap.text(item.get('name'), field + '.name')
        actual_date = item['date']
        if actual_date is None:
            day = None
            label = roadmap.text(item.get('label', unknown), field + '.label')
        else:
            if 'label' in item:
                raise ValueError(f'{field}.label: only supported when date is null')
            day = roadmap.iso(actual_date, field + '.date')
            label = actual_date
        rows.append((ref, name, day, label))
    return rows


def draw_calendar(root, rows):
    days = [day for _, _, day, _ in rows if day is not None]
    if not days:
        return None
    low, high = min(days), max(days)
    if low == high:
        low, high = max(1, low - 1), min(date.max.toordinal(), high + 1)

    def xpos(day):
        return LEFT + (day - low) / (high - low) * (RIGHT - LEFT)

    roadmap.svg_axes(root, low, high, 'dates', len(rows), xpos, row_height=ROW_HEIGHT)
    return xpos


def write_labels(root, x, y, value, columns, **attrs):
    lines = roadmap.wrap_label(value, columns)
    for index, line in enumerate(lines[:2]):
        if index == 1 and len(lines) > 2:
            line += '…'
        roadmap.svg_label(root, x, y + index * 18, line, **attrs)


def render(data):
    data = roadmap.obj(data, 'input')
    title = roadmap.text(data.get('title'), 'title')
    locale = data.get('locale', 'en')
    roadmap.choice(locale, CAPTIONS, 'locale')
    headings = CAPTIONS[locale]
    rows = read_rows(data, headings[4])
    height = 180 + len(rows) * ROW_HEIGHT
    root = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width=str(WIDTH), height=str(height),
                      viewBox=f'0 0 {WIDTH} {height}', role='img',
                      attrib={'aria-labelledby': 'title description', 'xml:lang': locale,
                              'font-family': 'sans-serif', 'font-size': '14'})
    ET.SubElement(root, 'title', id='title').text = title
    ET.SubElement(root, 'desc', id='description').text = headings[5]
    ET.SubElement(root, 'style').text = (
        'text{fill:#21394d}.grid{stroke:#dce5ec}.milestone{fill:#287562}'
        '.heading{font-size:24px;font-weight:700}.column{font-weight:700}'
        '.row-label{font-family:monospace}text[text-anchor="middle"]{font-size:12px}'
    )
    defs = ET.SubElement(root, 'defs')
    for name, start, end in (('heading-label', EVENT_X, WIDTH), ('event-label', EVENT_X, ACTUAL_X),
                             ('actual-label', ACTUAL_X, LEFT)):
        clip = ET.SubElement(defs, 'clipPath', id=name)
        ET.SubElement(clip, 'rect', x=str(start), width=str(end - start - 12), height=str(height))
    ET.SubElement(root, 'rect', width=str(WIDTH), height=str(height), fill='white')
    write_labels(root, EVENT_X, 36, title, 42, **{'class': 'heading', 'clip-path': 'url(#heading-label)'})
    xpos = draw_calendar(root, rows)
    for x, heading in zip((EVENT_X, ACTUAL_X, LEFT), headings[:3]):
        roadmap.svg_label(root, x, 93, heading, **{'class': 'column'})
    for index, (ref, name, day, label) in enumerate(rows):
        y = 136 + index * ROW_HEIGHT
        row = ET.SubElement(root, 'g', {'data-id': ref})
        event = f'{ref} · {name}'
        actual = f'{headings[3]} · {label}'
        ET.SubElement(row, 'title').text = f'{event} · {actual}'
        write_labels(row, EVENT_X, y + 25, event, 32,
                     **{'class': 'row-label', 'clip-path': 'url(#event-label)'})
        write_labels(row, ACTUAL_X, y + 25, actual, 22,
                     **{'class': 'row-label', 'clip-path': 'url(#actual-label)'})
        if day is not None:
            point = xpos(day)
            roadmap.svg_marker(row, point, point, y + 20, True, actual)
    roadmap.svg_label(root, EVENT_X, height - 16, headings[5])
    return ET.tostring(root, encoding='utf-8') + b'\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    source = parser.parse_args().input
    try:
        sys.dont_write_bytecode = True
        SPEC.loader.exec_module(roadmap)
        if source.stat().st_size > 1_048_576:
            raise ValueError('input exceeds 1 MiB')
        data = json.loads(source.read_text(encoding='utf-8'), object_pairs_hook=unique_fields)
        svg = render(data)
    except (OSError, ValueError, RecursionError) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 1
    sys.stdout.buffer.write(svg)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

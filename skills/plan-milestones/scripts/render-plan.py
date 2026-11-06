#!/usr/bin/env python3
"""Render a milestone plan as standalone SVG from a temporary JSON projection."""

import argparse
from datetime import date
import importlib.util
import json
from pathlib import Path
import sys
from typing import NamedTuple
import xml.etree.ElementTree as ET


ROADMAP_SCRIPT = Path(__file__).resolve().parents[2] / 'define-roadmap/scripts/render-roadmap.py'
SPEC = importlib.util.spec_from_file_location('roadmap_renderer', ROADMAP_SCRIPT)
roadmap = importlib.util.module_from_spec(SPEC)

WIDTH, ROW_HEIGHT = 1080, 62
MILESTONE_X, TIMING_X, LEFT, RIGHT = 24, 305, 512, 1032
LABELS = {
    'en': ('Milestone', 'Planned timing', 'Calendar', 'Target', 'Committed', 'Unscheduled',
           'A point marks a single date. A bar marks a window in which the event may occur.'),
    'zh-CN': ('里程碑', '计划时间', '日历', '目标', '承诺', '待定',
              '点表示单日，区间表示事件可能发生的时间范围。'),
}


class Timing(NamedTuple):
    basis: str
    label: str
    dates: tuple[int, int] | None


def read_timing(value, field):
    if value is None:
        return None
    value = roadmap.obj(value, field)
    basis = value.get('basis')
    roadmap.choice(basis, {'target', 'committed'}, field + '.basis')
    fields = set(value) - {'basis'}
    if fields == {'date'}:
        day = roadmap.iso(value['date'], field + '.date')
        return Timing(basis, value['date'], (day, day))
    if fields == {'label'}:
        return Timing(basis, roadmap.text(value['label'], field + '.label'), None)
    if fields not in ({'start', 'end'}, {'start', 'end', 'label'}):
        raise ValueError(f'{field}: expected a date, a window with both bounds, or a label')
    start = roadmap.iso(value['start'], field + '.start')
    end = roadmap.iso(value['end'], field + '.end')
    if end <= start:
        raise ValueError(f'{field}.end: exclusive end must be after start')
    default = value['start'] + ' – ' + date.fromordinal(end - 1).isoformat()
    return Timing(basis, roadmap.text(value.get('label', default), field + '.label'), (start, end))


def read_rows(data):
    items = roadmap.array(data.get('milestones'), 'milestones')
    if len(items) > 200:
        raise ValueError('milestones: at most 200 rows')
    ids, rows = set(), []
    for value in items:
        item = roadmap.obj(value, 'milestone')
        ref = roadmap.text(item.get('id'), 'milestone.id')
        if not roadmap.ID.fullmatch(ref) or ref in ids:
            raise ValueError(f'milestone.id: invalid or duplicate ID {ref!r}')
        ids.add(ref)
        name = roadmap.text(item.get('name'), ref + '.name')
        rows.append((ref, name, read_timing(item.get('timing'), ref + '.timing')))
    return rows


def labels(root, x, y, text, width, *, line_height=17, **attrs):
    chunks = roadmap.wrap_label(text, width)
    for i, chunk in enumerate(chunks[:2]):
        roadmap.svg_label(root, x, y + line_height * i,
                          chunk + ('…' if i == 1 and len(chunks) > 2 else ''), **attrs)


def draw_row(root, index, row, captions, xpos):
    ref, name, timing = row
    y = 136 + index * ROW_HEIGHT
    group = ET.SubElement(root, 'g', {'data-id': ref})
    caption = f'{ref} · {name}'
    basis = captions[3 if timing.basis == 'target' else 4] if timing else captions[5]
    planned = f'{basis} · {timing.label}' if timing else basis
    ET.SubElement(group, 'title').text = f'{caption} · {planned}'
    labels(group, MILESTONE_X, y + 25, caption, 32,
           **{'class': 'row-label', 'clip-path': 'url(#milestone-label)'})
    labels(group, TIMING_X, y + 25, planned, 22,
           **{'class': 'row-label', 'clip-path': 'url(#timing-label)'})
    if timing and timing.dates:
        start, end = timing.dates
        roadmap.svg_marker(group, xpos(start), xpos(end), y + 20, start == end, planned)
    ET.SubElement(root, 'line', x1=str(MILESTONE_X), y1=str(y + ROW_HEIGHT), x2=str(RIGHT),
                  y2=str(y + ROW_HEIGHT), **{'class': 'rule'})


def draw_calendar(root, rows):
    known = [timing.dates for _, _, timing in rows if timing and timing.dates]
    if not known:
        return None
    low = min(start for start, _ in known)
    high = max(end for _, end in known)
    if low == high:
        low, high = max(1, low - 1), min(date.max.toordinal(), high + 1)

    def xpos(day):
        return LEFT + (day - low) / (high - low) * (RIGHT - LEFT)

    roadmap.svg_axes(root, low, high, 'dates', len(rows), xpos, row_height=ROW_HEIGHT)
    return xpos


def render(data):
    data = roadmap.obj(data, 'input')
    title = roadmap.text(data.get('title'), 'title')
    locale = data.get('locale', 'en')
    roadmap.choice(locale, LABELS, 'locale')
    captions, rows = LABELS[locale], read_rows(data)
    height = 180 + len(rows) * ROW_HEIGHT
    root = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width=str(WIDTH), height=str(height),
                      viewBox=f'0 0 {WIDTH} {height}', role='img',
                      attrib={'aria-labelledby': 'title description', 'xml:lang': locale,
                              'font-family': 'sans-serif', 'font-size': '14'})
    ET.SubElement(root, 'title', id='title').text = title
    ET.SubElement(root, 'desc', id='description').text = captions[6]
    ET.SubElement(root, 'style').text = (
        'text{fill:#21394d}.grid,.rule{stroke:#dce5ec}'
        '.milestone{fill:#245c91}.span{fill:#d9ede7;stroke:#287562}'
        '.heading{font-size:24px;font-weight:700}.column{font-weight:700}'
        '.row-label{font-family:monospace}text[text-anchor="middle"]{font-size:12px}'
    )
    defs = ET.SubElement(root, 'defs')
    for name, start, end in (('heading-label', MILESTONE_X, WIDTH),
                             ('milestone-label', MILESTONE_X, TIMING_X),
                             ('timing-label', TIMING_X, LEFT)):
        clip = ET.SubElement(defs, 'clipPath', id=name)
        ET.SubElement(clip, 'rect', x=str(start), width=str(end - start - 12), height=str(height))
    ET.SubElement(root, 'rect', width=str(WIDTH), height=str(height), fill='white')
    labels(root, MILESTONE_X, 36, title, 42, line_height=27,
           **{'class': 'heading', 'clip-path': 'url(#heading-label)'})
    xpos = draw_calendar(root, rows)
    for x, value in zip((MILESTONE_X, TIMING_X, LEFT), captions[:3]):
        roadmap.svg_label(root, x, 93, value, **{'class': 'column'})
    for i, row in enumerate(rows):
        draw_row(root, i, row, captions, xpos)
    roadmap.svg_label(root, MILESTONE_X, height - 16, captions[6])
    return ET.tostring(root, encoding='unicode') + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    source = parser.parse_args().input
    try:
        sys.dont_write_bytecode = True
        SPEC.loader.exec_module(roadmap)
        if source.stat().st_size > 1_048_576:
            raise ValueError('input exceeds 1 MiB')
        svg = render(json.loads(source.read_text(encoding='utf-8')))
    except (OSError, ValueError, UnicodeError) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 1
    sys.stdout.buffer.write(svg.encode('utf-8'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

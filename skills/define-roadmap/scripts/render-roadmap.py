#!/usr/bin/env python3
"""Validate and render roadmap views offline using only the standard library."""

from __future__ import annotations

import argparse
from datetime import date
from html import escape
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import urlsplit, quote
import xml.etree.ElementTree as ET


EXECUTION = {'Not started', 'In progress', 'Awaiting acceptance', 'Awaiting release',
             'Paused', 'Blocked', 'Completed'}
OUTPUTS = ('roadmap.md', 'roadmap.svg', 'roadmap.mmd')
ID = re.compile(r'[A-Za-z][A-Za-z0-9_-]*\Z')


def text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > 200:
        raise ValueError(f'{field}: expected nonempty text of at most 200 characters')
    if any((ord(c) < 32 and c not in '\n\r\t') or
           0xD800 <= ord(c) <= 0xDFFF or ord(c) in {0xFFFE, 0xFFFF} for c in value):
        raise ValueError(f'{field}: unsupported XML control character')
    return value


def array(value, field):
    if not isinstance(value, list):
        raise ValueError(f'{field}: expected array')
    return value


def obj(value, field):
    if not isinstance(value, dict):
        raise ValueError(f'{field}: expected object')
    return value


def choice(value, options, field):
    if not isinstance(value, str) or value not in options:
        raise ValueError(f'{field}: expected one of {", ".join(sorted(options))}')


def iso(value, field):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError(f'{field}: expected ISO date')
    try:
        return date.fromisoformat(value).toordinal()
    except ValueError as exc:
        raise ValueError(f'{field}: invalid date') from exc


def point(value, mode, field):
    if mode == 'dates':
        return iso(value, field)
    if type(value) is not int or value < 1:
        raise ValueError(f'{field}: expected positive whole week')
    return value


def validate(data: dict) -> dict:
    """Validate a JSON-shaped mapping without changing its facts; return it unchanged."""
    views, entries, versions = validate_header(data)
    ids = validate_ids(records(data), [])
    validate_events(data)
    validate_entries(entries)
    validate_versions(versions, entries)
    if 'schedule' in views:
        validate_schedule(data, ids)
    return data



def records(data):
    return [r for key in ('entries', 'versions', 'phases', 'milestones')
            for r in array(data.get(key, []), key)]


def reference(value, field):
    text(value, field)
    url = urlsplit(value)
    if (value.startswith(('/', '\\')) or '\\' in value or
            any(c in value for c in '\r\n\t') or
            (url.scheme and (url.scheme not in {'http', 'https'} or not url.netloc))):
        raise ValueError(f'{field}: relative reference or HTTP(S) required')


def related_ids(value, allowed, field, nonempty=False):
    values = array(value, field)
    if (any(not isinstance(v, str) or v not in allowed for v in values) or
            len(values) != len(set(values)) or (nonempty and not values)):
        raise ValueError(f'{field}: unique known references required')


def validate_events(data):
    scope = {r['id'] for r in data['entries'] + data.get('versions', [])}
    phases = data.get('phases', [])
    for phase in phases:
        for key in ('owner', 'exit_condition'):
            text(phase.get(key), f'{phase["id"]}.{key}')
        reference(phase.get('source'), f'{phase["id"]}.source')
        related_ids(phase.get('scope'), scope, f'{phase["id"]}.scope', True)
    related = scope | {p['id'] for p in phases}
    for event in data.get('milestones', []):
        for key in ('owner', 'criterion'):
            text(event.get(key), f'{event["id"]}.{key}')
        reference(event.get('source'), f'{event["id"]}.source')
        related_ids(event.get('related'), related, f'{event["id"]}.related')
        choice(event.get('category'), {'achievement', 'approval', 'deadline', 'event', 'start'}, 'category')
        choice(event.get('state'), {'planned', 'reached', 'missed', 'cancelled'}, 'state')
        if event.get('evidence') is not None or event['state'] != 'planned':
            reference(event.get('evidence'), f'{event["id"]}.evidence')


def validate_schedule_types(data, items):
    if data['schema_version'] == '1.0':
        return
    events = {r['id']: r for r in data.get('milestones', [])}
    for item in items:
        obj(item, 'schedule.item')
        ref = item.get('ref')
        if not isinstance(ref, str):
            raise ValueError('schedule.ref: expected reference string')
        expected = 'milestone' if ref in events else 'span'
        if item.get('kind') != expected:
            raise ValueError(f'{ref}.kind: expected {expected}')
        if ref in events and item.get('basis') == 'actual' and events[ref]['state'] != 'reached':
            raise ValueError(f'{ref}: actual timing requires reached state')


def validate_header(data: dict) -> tuple:
    obj(data, 'input')
    choice(data.get('schema_version'), {'1.0', '1.1'}, 'schema_version')
    if data['schema_version'] == '1.0' and any(k in data for k in ('phases', 'milestones')):
        raise ValueError('phases/milestones require schema_version 1.1')
    for field in ('project', 'updated', 'direction', 'ordering', 'closure', 'priority_policy'):
        text(data.get(field), field)
    iso(data['updated'], 'updated')
    views = array(data.get('views'), 'views')
    for view in views:
        choice(view, {'requirements', 'versions', 'schedule'}, 'views')
    if len(set(views)) != len(views) or 'requirements' not in views:
        raise ValueError('views: unique selections including requirements required')
    entries = array(data.get('entries'), 'entries')
    versions = array(data.get('versions', []), 'versions')
    if 'versions' in views and 'versions' not in data:
        raise ValueError('versions: selected view needs records')
    if len(records(data)) > 200:
        raise ValueError('records: at most 200 entries, versions, phases and milestones')
    return views, entries, versions


def validate_ids(entries: list, versions: list) -> set:
    ids = set()
    for record in entries + versions:
        obj(record, 'record')
        value = text(record.get('id'), 'id')
        if not ID.fullmatch(value):
            raise ValueError(f'id: invalid identifier {value!r}')
        if value in ids:
            raise ValueError(f'duplicate id: {value}')
        ids.add(value)
        text(record.get('name'), f'{value}.name')
    return ids


def validate_entries(entries: list) -> None:
    for entry in entries:
        key = entry['id']
        for field in ('source', 'outcome', 'approval', 'conditions'):
            text(entry.get(field), f'{key}.{field}')
        reference(entry['source'], f'{key}.source')
        choice(entry.get('priority'), {'P0', 'P1', 'P2', 'P3', 'unset'}, f'{key}.priority')
        choice(entry.get('tier'), {'Now', 'Next', 'Later'}, f'{key}.tier')
        if 'execution' not in entry:
            raise ValueError(f'{key}.execution: label or null required')
        if entry['execution'] is not None:
            choice(entry['execution'], EXECUTION, f'{key}.execution')


def validate_versions(versions: list, entries: list) -> None:
    entry_ids = {e['id'] for e in entries}
    assigned = set()
    for version in versions:
        for field in ('outcome', 'owner', 'window'):
            text(version.get(field), f'{version["id"]}.{field}')
        for member in array(version.get('members'), 'members'):
            if not isinstance(member, str) or member not in entry_ids:
                raise ValueError(f'{version["id"]}.member: unknown entry {member!r}')
            if member in assigned:
                raise ValueError(f'member: duplicate version assignment {member}')
            assigned.add(member)


def validate_schedule(data: dict, ids: set) -> None:
    schedule = obj(data.get('schedule'), 'schedule')
    choice(schedule.get('mode'), {'dates', 'weeks'}, 'schedule.mode')
    text(schedule.get('origin'), 'schedule.origin')
    choice(schedule.get('calendar'), {'calendar-days'}, 'schedule.calendar')
    items = array(schedule.get('items'), 'schedule.items')
    if len(items) > 200:
        raise ValueError('schedule.items: at most 200')
    validate_schedule_types(data, items)
    by_ref, points = validate_schedule_items(items, schedule['mode'], ids, data['schema_version'])
    validate_dependencies(by_ref, points)
    if points:
        horizon = max(p[1] for p in points.values()) - min(p[0] for p in points.values())
        if horizon > (366 if schedule['mode'] == 'dates' else 104):
            raise ValueError('schedule horizon exceeds 366 days or 104 weeks')


def validate_schedule_items(items: list, mode: str, ids: set, schema='1.0') -> tuple:
    by_ref, points = {}, {}
    for item in items:
        obj(item, 'schedule.item')
        ref = item.get('ref')
        if not isinstance(ref, str) or ref not in ids:
            raise ValueError(f'schedule.ref: unknown record {ref!r}')
        if ref in by_ref:
            raise ValueError(f'duplicate schedule ref: {ref}')
        by_ref[ref] = item
        choice(item.get('kind'), {'span', 'milestone'}, f'{ref}.kind')
        choice(item.get('basis'), {'target', 'committed', 'actual'}, f'{ref}.basis')
        if 'start' not in item or 'end' not in item:
            raise ValueError(f'{ref}.endpoints: both start and end required')
        start, end = item['start'], item['end']
        if (start is None) != (end is None):
            raise ValueError(f'{ref}.endpoints: both null or both known required')
        if start is None:
            if item['kind'] != 'span' and schema == '1.0':
                raise ValueError(f'{ref}.kind: unscheduled item must be span')
        else:
            left = point(start, mode, f'{ref}.start')
            right = point(end, mode, f'{ref}.end')
            if (item['kind'] == 'span' and right <= left) or (item['kind'] == 'milestone' and right != left):
                raise ValueError(f'{ref}.end: span needs end > start; milestone needs equality')
            points[ref] = (left, right)
        deps = array(item.get('depends_on'), f'{ref}.depends_on')
        if any(not isinstance(d, str) for d in deps) or len(deps) != len(set(deps)):
            raise ValueError(f'{ref}.dependency: unique reference strings required')
    return by_ref, points


def validate_dependencies(by_ref: dict, points: dict) -> None:
    for ref, item in by_ref.items():
        for dep in item['depends_on']:
            if dep not in by_ref:
                raise ValueError(f'{ref}.dependency: missing scheduled ref {dep}')
    active, done = set(), set()

    def visit(ref):
        if ref in active:
            raise ValueError(f'dependency cycle at {ref}')
        if ref in done:
            return
        active.add(ref)
        for dep in by_ref[ref]['depends_on']:
            visit(dep)
        active.remove(ref)
        done.add(ref)

    for ref in by_ref:
        visit(ref)
    for ref, item in by_ref.items():
        for dep in item['depends_on']:
            if ref in points and dep in points and points[ref][0] < points[dep][1]:
                raise ValueError(f'dependency overlap: {ref} starts before {dep} finishes')


def md(value):
    value = ' '.join(str(value).split())
    value = escape(value, quote=False)
    return re.sub(r'([\\`*_|\[\]])', r'\\\1', value)


def table(headers, rows):
    lines = ['| ' + ' | '.join(headers) + ' |', '| ' + ' | '.join('---' for _ in headers) + ' |']
    lines.extend('| ' + ' | '.join(row) + ' |' for row in rows)
    return '\n'.join(lines)


def timing(item, mode):
    if item['start'] is None:
        return 'Unscheduled'
    if item['kind'] == 'milestone':
        return f'W{item["start"]}' if mode == 'weeks' else item['start']
    if mode == 'weeks':
        return f'W{item["start"]}–W{item["end"] - 1}'
    return f'{item["start"]} to {item["end"]} (end exclusive)'


def markdown(data: dict) -> str:
    """Render selected views of validated facts as one Markdown roadmap."""
    lines = [f'# {md(data["project"])} Roadmap', '', f'Updated: {data["updated"]}', '',
             md(data['direction']), '', 'Ordering rationale: ' + md(data['ordering']), '',
             f'Priority policy: {md(data["priority_policy"])}', '', '## Requirements', '']
    lines.extend(requirement_markdown(data))
    lines.extend(['', 'Closure criterion: ' + md(data['closure']), ''])
    if 'versions' in data['views']:
        lines.extend(version_markdown(data))
    lines.extend(event_markdown(data))
    if 'schedule' in data['views']:
        lines.extend(schedule_markdown(data))
    lines.extend(['', 'Backlog requirements and defects map to this roadmap; items outside it are not done by default.',
                  'Placement grants no implementation or release approval.', ''])
    return '\n'.join(lines)


def requirement_markdown(data: dict) -> list:
    lines = []
    rows = []
    for entry in data['entries']:
        link = quote(entry['source'], safe='/:#?=&%+~.-_')
        rows.append([entry['tier'], f'[{entry["id"]} · {md(entry["name"])}]({link})',
                     md(entry['outcome']), entry['priority'], md(entry['approval']),
                     entry['execution'] or '—', f'[{md(entry["conditions"])}]({link})'])
    lines.append(table(['Tier', 'Requirement / defect', 'Expected outcome', 'Priority',
                        'Approval status', 'Execution status', 'Key conditions'], rows))
    empty = [tier for tier in ('Now', 'Next', 'Later') if not any(e['tier'] == tier for e in data['entries'])]
    if empty:
        lines.extend(['', 'No items planned: ' + ', '.join(empty) + '.'])
    unknown = [e['id'] for e in data['entries'] if e['execution'] is None]
    if unknown:
        lines.extend(['', 'Unverified execution mappings: ' + ', '.join(unknown) + '.'])
    return lines


def version_markdown(data: dict) -> list:
    lines = []
    rows = [[v['id'] + ' · ' + md(v['name']), ', '.join(v['members']) or 'None',
             md(v['outcome']), md(v['owner']), md(v['window'])] for v in data['versions']]
    lines.extend(['## Versions', '', table(['Version', 'Members', 'Core outcome', 'Owner', 'Delivery window'], rows)])
    assigned = {ref for v in data['versions'] for ref in v['members']}
    unassigned = [e['id'] for e in data['entries'] if e['id'] not in assigned]
    if unassigned:
        lines.extend(['', 'Unassigned: ' + ', '.join(unassigned) + '.'])
    return lines



def event_markdown(data):
    lines = []
    if data.get('phases'):
        rows = [[p['id'] + ' · ' + md(p['name']), ', '.join(p['scope']), md(p['owner']),
                 md(p['exit_condition']), '[' + p['id'] + '](' +
                 quote(p['source'], safe='/:#?=&%+~.-_') + ')'] for p in data['phases']]
        lines.extend(['', '## Phases', '', table(
            ['Phase', 'Scope', 'Owner', 'Exit condition', 'Source'], rows)])
    if data.get('milestones'):
        rows = [[m['id'] + ' · ' + md(m['name']), m['category'], ', '.join(m['related']) or 'Global',
                 md(m['owner']), m['state'], md(m['criterion']),
                 '[Source](' + quote(m['source'], safe='/:#?=&%+~.-_') + ')',
                 '[Evidence](' + quote(m['evidence'], safe='/:#?=&%+~.-_') + ')'
                 if m.get('evidence') else '—'] for m in data['milestones']]
        lines.extend(['', '## Milestones', '', table(
            ['Milestone', 'Category', 'Related', 'Owner', 'State', 'Occurrence criterion', 'Source', 'Evidence'], rows),
            '', 'Milestones are events; dates and related work do not prove occurrence or grant approval.'])
    return lines


def schedule_markdown(data: dict) -> list:
    lines = []
    schedule = data['schedule']
    rows = [[i['ref'], i['kind'], i['basis'], timing(i, schedule['mode']),
             ', '.join(i['depends_on']) or 'None'] for i in schedule['items']]
    lines.extend(['', '## Schedule', '', md(schedule['origin']), '',
                  'Elapsed calendar days / whole weeks; spans have exclusive ends.', '',
                  table(['Reference', 'Kind', 'Timing basis', 'Window', 'Depends on'], rows), '',
                  '![Roadmap schedule](roadmap.svg)'])
    covered = {i['ref'] for i in schedule['items']}
    covered.update(ref for v in data.get('versions', []) if v['id'] in covered for ref in v['members'])
    missing = [e['id'] for e in data['entries'] + data.get('phases', []) +
               data.get('milestones', []) if e['id'] not in covered]
    if missing:
        lines.extend(['', 'No schedule assigned: ' + ', '.join(missing) + '.'])
    unknown = [i['ref'] for i in schedule['items'] if i['start'] is None]
    if unknown:
        lines.extend(['', 'Unscheduled: ' + ', '.join(unknown) + '.'])
    unverified = [f'{dep} → {i["ref"]}' for i in schedule['items'] for dep in i['depends_on']
                  if dep in unknown or i['ref'] in unknown]
    if unverified:
        lines.extend(['', 'Unverified dependency timing: ' + ', '.join(unverified) + '.'])
    if schedule['mode'] == 'dates':
        lines.extend(['', '```mermaid', mermaid(data).rstrip(), '```'])
    return lines


def mermaid(data: dict) -> str:
    if data['schedule']['mode'] != 'dates':
        raise ValueError('Mermaid Gantt output requires dates; relative weeks use SVG')
    names = {r['id']: r['name'] for r in records(data)}
    names.update({m['id']: m['name'] + ' [' + m['state'] + ']'
                  for m in data.get('milestones', [])})
    lines = ['gantt', '    dateFormat YYYY-MM-DD', '    axisFormat %m-%d', '    todayMarker off']
    for item in data['schedule']['items']:
        if item['start'] is None:
            continue
        # Labels cannot introduce Mermaid directives or metadata delimiters.
        label = re.sub(r'[^\w .()/-]', ' ', names[item['ref']], flags=re.UNICODE)
        label = ' '.join(label.split()) or item['ref']
        label = f'{item["ref"]} {label} ({item["basis"]})'
        prefix = 'milestone, ' if item['kind'] == 'milestone' else ''
        duration = iso(item['end'], 'end') - iso(item['start'], 'start')
        lines.append(f'    {label} :{prefix}{item["ref"]}, {item["start"]}, {duration}d')
    return '\n'.join(lines) + '\n'


def svg(data: dict) -> str:
    """Render validated schedule facts as accessible fixed-size standalone SVG."""
    schedule = data['schedule']
    items = schedule['items']
    names = {r['id']: r['name'] for r in records(data)}
    states = {r['id']: r['state'] for r in data.get('milestones', [])}
    known = [i for i in items if i['start'] is not None]
    coords = {i['ref']: (point(i['start'], schedule['mode'], 'start'),
                         point(i['end'], schedule['mode'], 'end')) for i in known}
    low = min((v[0] for v in coords.values()), default=1)
    high = max((v[1] for v in coords.values()), default=low + 1)
    if high == low:
        if schedule['mode'] == 'dates' and high == date.max.toordinal():
            low -= 1
        else:
            high += 1
    root = svg_root(data, schedule, len(items))

    def xpos(value):
        return 350 + (value - low) / (high - low) * 560

    svg_heading(root, data, schedule)
    svg_axes(root, low, high, schedule['mode'], len(items), xpos)
    positions = {i['ref']: 136 + index * 84 + 20 for index, i in enumerate(items)}
    for item in items:
        svg_row(root, item, coords, positions, names, schedule['mode'], xpos, states)
    if not items:
        svg_label(root, 20, 156, 'No items scheduled')
    svg_label(root, 20, 136 + max(1, len(items)) * 84 + 25,
              'Bars show elapsed time, not completion percentage.')
    return ET.tostring(root, encoding='unicode') + '\n'


def svg_root(data, schedule, count):
    width, top, row_height = 960, 136, 84
    root = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width=str(width),
                      height=str(top + max(1, count) * row_height + 48),
                      viewBox=f'0 0 {width} {top + max(1, count) * row_height + 48}',
                      role='img', **{'aria-labelledby': 'title description'})
    ET.SubElement(root, 'title', id='title').text = data['project'] + ' schedule'
    ET.SubElement(root, 'desc', id='description').text = schedule['origin'] + '; target, committed and actual timing are labeled; exclusive ends.'
    ET.SubElement(root, 'style').text = (
        'text{font:14px sans-serif;fill:#172b4d} .grid{stroke:#d9e2ec;stroke-width:1}'
        '.span{fill:#3579ad}.milestone{fill:#3579ad}.dependency{fill:none;stroke:#526777;stroke-width:1.5}'
    )
    ET.SubElement(root, 'rect', width='100%', height='100%', fill='#fff')

    return root


def svg_label(root, x, y, value, **attrs):
    ET.SubElement(root, 'text', x=str(x), y=str(y), **attrs).text = value


def wrap_label(value, length=26):
    # Count wide Unicode characters as two display columns.
    rows, current, count = [], '', 0
    for char in ' '.join(value.split()):
        size = 2 if unicodedata.east_asian_width(char) in {'W', 'F'} else 1
        if count + size > length:
            rows.append(current)
            current, count = '', 0
        current += char
        count += size
    return rows + [current]



def svg_heading(root, data, schedule):
    project_chunks = wrap_label(data['project'], 112)
    svg_label(root, 20, 28, project_chunks[0] + ('…' if len(project_chunks) > 1 else ''))
    origin_chunks = wrap_label(schedule['origin'], 112)
    for number, line in enumerate(origin_chunks[:2]):
        svg_label(root, 20, 51 + number * 17, line + ('…' if number == 1 and len(origin_chunks) > 2 else ''))
    svg_label(root, 20, 100, 'Reference / timing basis')
    svg_label(root, 350, 100, 'Relative weeks' if schedule['mode'] == 'weeks' else 'Calendar dates (end exclusive)')


def svg_axes(root, low, high, mode, count, xpos):
    ticks = sorted({low + round((high - low) * n / 4) for n in range(5)})
    for tick in ticks:
        x = xpos(tick)
        ET.SubElement(root, 'line', x1=str(x), y1='128', x2=str(x),
                      y2=str(136 + count * 84), **{'class': 'grid'})
        value = f'W{tick}' if mode == 'weeks' else date.fromordinal(tick).isoformat()
        svg_label(root, x, 121, value, **{'text-anchor': 'middle'})


def svg_row(root, item, coords, positions, names, mode, xpos, states):
    ref, y = item['ref'], positions[item['ref']]
    # Full accessible labels remain available even when visual wrapping is abbreviated.
    full = f'{ref} · {names[ref]}'
    chunks = wrap_label(full)
    for n, chunk in enumerate(chunks[:2]):
        svg_label(root, 20, y + n * 17, chunk + ('…' if n == 1 and len(chunks) > 2 else ''))
    state = ' · ' + states[ref] if ref in states else ''
    svg_label(root, 20, y + 42, item['basis'] + ' · ' + timing(item, mode) + state)
    if ref not in coords:
        svg_label(root, 362, y + 12, 'Unscheduled')
        return
    start, end = coords[ref]
    x1, x2 = xpos(start), xpos(end)
    if item['kind'] == 'milestone':
        shape = ET.SubElement(root, 'polygon', points=f'{x1},{y} {x1+7},{y+9} {x1},{y+18} {x1-7},{y+9}',
                              **{'class': 'milestone'})
    else:
        shape = ET.SubElement(root, 'rect', x=str(x1), y=str(y), width=str(x2 - x1), height='18', **{'class': 'span'})
    ET.SubElement(shape, 'title').text = full + ' · ' + timing(item, mode)
    for dep in item['depends_on']:
        if dep not in coords:
            continue
        dx, dy = xpos(coords[dep][1]), positions[dep] + 9
        path = f'M {dx} {dy} L {dx+8} {dy} L {dx+8} {y-8} L {x1} {y-8} L {x1} {y}'
        ET.SubElement(root, 'path', d=path, **{'class': 'dependency'})
        ET.SubElement(root, 'polygon', points=f'{x1},{y} {x1-4},{y-6} {x1+4},{y-6}', fill='#526777')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        if args.input.stat().st_size > 1_048_576:
            raise ValueError('input exceeds 1 MiB')
        data = validate(json.loads(args.input.read_text(encoding='utf-8')))
        if args.check:
            print('Roadmap input valid; no files written.')
            return 0
        if args.output_dir is None:
            raise ValueError('--output-dir required unless --check is used')
        outputs = {'roadmap.md': markdown(data)}
        if 'schedule' in data['views']:
            outputs['roadmap.svg'] = svg(data)
            if data['schedule']['mode'] == 'dates':
                outputs['roadmap.mmd'] = mermaid(data)
        for name in OUTPUTS:
            path = args.output_dir / name
            if path.is_symlink() or (path.exists() and not path.is_file()):
                raise ValueError(f'output must be a regular file: {path}')
            if path.exists() and not args.overwrite:
                raise ValueError(f'output exists: {path}; explicit --overwrite required')
        if any(path.exists() and args.input.samefile(path)
               for path in (args.output_dir / name for name in OUTPUTS)):
            raise ValueError('input must not be an output file')
        args.output_dir.mkdir(parents=True, exist_ok=True)
        for name, content in outputs.items():
            (args.output_dir / name).write_text(content, encoding='utf-8')
            print(f'Written: {args.output_dir / name}')
        if args.overwrite:
            for name in set(OUTPUTS) - outputs.keys():
                (args.output_dir / name).unlink(missing_ok=True)
        return 0
    except (ValueError, OSError, RecursionError) as exc:
        print(f'Roadmap generation failed: {exc}. Inspect destination for partial I/O output.', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

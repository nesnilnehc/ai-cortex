#!/usr/bin/env python3
"""Validate and render roadmap views offline using only the standard library."""

from __future__ import annotations

import argparse
import hashlib
from datetime import date
from functools import cache
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
OUTPUTS = ('roadmap.md', 'roadmap-delivery.md', 'roadmap-history.md', 'roadmap.svg', 'roadmap.mmd')
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
    validate_revisions(data)
    validate_iterations(data)
    validate_selection(data)
    validate_language(data)
    validate_entries(entries)
    validate_versions(versions, entries)
    if 'schedule' in views:
        validate_schedule(data, ids)
    return data


def records(data):
    keys = ('entries', 'versions', 'phases', 'milestones')
    if data['schema_version'] in {'1.3', '1.4', '1.5', '1.6'}:
        keys += ('iterations',)
    return [r for key in keys
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


def validate_revisions(data):
    if data['schema_version'] not in {'1.2', '1.3', '1.4', '1.5', '1.6'}:
        return
    revisions = array(data.get('revisions'), 'revisions')
    if len(revisions) > 200:
        raise ValueError('revisions: at most 200 records; split retained history upstream')
    history = data.get('revision_history')
    if history is not None or len(revisions) > 5:
        reference(history, 'revision_history')
    ids, previous = set(), iso(data['updated'], 'updated')
    for revision in revisions:
        obj(revision, 'revision')
        key = text(revision.get('id'), 'revision.id')
        if not ID.fullmatch(key):
            raise ValueError(f'revision.id: invalid identifier {key!r}')
        if key in ids:
            raise ValueError(f'revision.id: duplicate {key}')
        ids.add(key)
        recorded = iso(revision.get('date'), f'{key}.date')
        if recorded > iso(data['updated'], 'updated'):
            raise ValueError(f'{key}.date: must not be later than updated')
        if recorded > previous:
            raise ValueError('revisions: newest first order required')
        previous = recorded
        for field in ('change', 'reason', 'impact'):
            text(revision.get(field), f'{key}.{field}')
        reference(revision.get('source'), f'{key}.source')


def validate_iterations(data):
    if data['schema_version'] not in {'1.3', '1.4', '1.5', '1.6'}:
        return
    if 'iterations' in data['views']:
        text(data.get('cadence'), 'cadence')
        array(data.get('iterations'), 'iterations')
    allowed = {entry['id'] for entry in data['entries']}
    for iteration in data.get('iterations', []):
        key = iteration['id']
        for field in ('goal', 'owner'):
            text(iteration.get(field), f'{key}.{field}')
        reference(iteration.get('source'), f'{key}.source')
        related_ids(iteration.get('members'), allowed, f'{key}.members')
        if iteration.get('board') is not None:
            reference(iteration['board'], f'{key}.board')


def validate_context(context, partial=False):
    obj(context, 'planning context')
    missing = []
    choices = {'work_mode': {'iterations', 'flow', 'staged', 'discovery'},
               'delivery': {'continuous', 'versioned', 'acceptance'}}
    for field in ('work_mode', 'delivery', 'audience', 'constraints', 'source'):
        value = context.get(field)
        if value is None or (isinstance(value, str) and (not value.strip() or value == 'unknown')):
            missing.append(field)
            continue
        if field in choices:
            choice(value, choices[field], field)
        elif field == 'source':
            reference(value, 'context.source')
        else:
            text(value, field)
    if missing and not partial:
        raise ValueError('planning context missing: ' + ', '.join(missing))
    return missing


def validate_choice(data):
    selection = obj(data.get('selection'), 'selection')
    choice(selection.get('scenario'), {'iterations', 'flow', 'staged', 'discovery', 'custom'}, 'scenario')
    choice(selection.get('primary'), {'requirements', 'iterations', 'versions', 'phases', 'flow'}, 'primary')
    choice(selection.get('layout'), {'single', 'split', 'topic-split'} if data['schema_version'] == '1.6' else {'single', 'split'}, 'selection.layout')
    views = array(data.get('views'), 'views')
    options = {'requirements', 'iterations', 'versions', 'phases', 'milestones', 'flow', 'schedule'}
    for view in views:
        choice(view, options, 'views')
    if len(views) != len(set(views)) or 'requirements' not in views or selection['primary'] not in views:
        raise ValueError('selection: unique views including requirements and primary required')
    text(selection.get('rationale'), 'selection.rationale')
    reference(selection.get('source'), 'selection.source')
    validate_context(selection.get('context'))
    return selection


def validate_selection(data):
    if data['schema_version'] not in {'1.4', '1.5', '1.6'}:
        return
    validate_choice(data)
    for view in ('phases', 'milestones'):
        if view in data['views']:
            array(data.get(view), view)
    if 'flow' in data['views']:
        flow = obj(data.get('flow'), 'flow')
        reference(flow.get('source'), 'flow.source')
        reference(flow.get('board'), 'flow.board')
        for field in ('policy', 'expectation', 'metrics'):
            text(flow.get(field), 'flow.' + field)


def recommend_views(data):
    obj(data, 'recommendation input')
    if 'schema_version' in data:
        choice(data['schema_version'], {'1.0', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6'}, 'schema_version')
    if data.get('schema_version') in {'1.0', '1.1', '1.2', '1.3'}:
        validate(data)
        return dict(status='retained', views=list(data['views']), primary=None, layout=None,
                    missing=[], questions=[],
                    notice='Legacy views retained; inspect existing roadmap for primary/layout. No migration required.')
    existing = validate_choice(data) if 'selection' in data else None
    context = data.get('planning_context', existing['context'] if existing else {})
    missing = validate_context(context, partial=True)
    if existing:
        changed = context != existing['context']
        return dict(status='retained-review-needed' if changed else 'retained',
                    scenario=existing['scenario'], primary=existing['primary'], views=list(data['views']),
                    layout=existing['layout'], rationale=existing['rationale'], source=existing['source'],
                    missing=missing, questions=context_questions(missing),
                    notice='Review changed context; retained choices were not replaced.' if changed else 'Reuse existing choices.')
    if missing:
        return dict(status='needs-input', missing=missing, questions=context_questions(missing))
    mode = context['work_mode']
    primary = {'iterations': 'iterations', 'flow': 'flow', 'staged': 'phases', 'discovery': 'phases'}[mode]
    views = ['requirements', primary]
    if mode in {'staged', 'discovery'}:
        views.append('milestones')
    if context['delivery'] == 'versioned':
        if mode in {'iterations', 'flow'}:
            views = ['requirements', primary, 'versions', 'milestones']
        else:
            views.append('versions')
    elif context['delivery'] == 'acceptance' and 'milestones' not in views:
        views.append('milestones')
    return dict(status='proposal', scenario=mode, primary=primary, views=views, layout='single',
                rationale='Use ' + primary + ' for the declared work mode; tailor supporting views to delivery needs.',
                optional=['schedule'], source=context['source'], missing=[], questions=[],
                notice='Recommendation only; retain a source-backed team choice before generating.')


def recommend(data):
    result = recommend_views(data)
    if data.get('schema_version') in {'1.5', '1.6'} or 'language_context' in data:
        result['language'] = resolve_language(data)
    return result


def validate_language(data):
    if data.get('schema_version') not in {'1.5', '1.6'}:
        return
    saved = language_record(data.get('language'))
    if 'language_context' in data:
        resolved = resolve_language(data)
        if resolved['status'] == 'needs-input' or resolved['locale'] != saved['locale']:
            raise ValueError('language evidence is unresolved or differs; update the source decision before generation')


def language_record(value):
    value = obj(value, 'language')
    choice(value.get('locale'), {'en', 'zh-CN'}, 'language.locale')
    choice(value.get('basis'), {'user', 'project', 'existing', 'context'}, 'language.basis')
    reference(value.get('source'), 'language.source')
    text(value.get('rationale'), 'language.rationale')
    return value


def language_candidates(context):
    context = obj(context, 'language_context')
    levels = ('user', 'project', 'existing', 'audience', 'documents')
    if any(key not in levels for key in context):
        raise ValueError('language_context: unsupported evidence level')
    candidates = {}
    for level in levels:
        candidates[level] = array(context.get(level, []), 'language_context.' + level)
        if len(candidates[level]) > 20:
            raise ValueError('language_context: at most 20 records per level')
        for evidence in candidates[level]:
            obj(evidence, 'language evidence')
            choice(evidence.get('locale'), {'en', 'zh-CN'}, 'language evidence.locale')
            reference(evidence.get('source'), 'language evidence.source')
    return candidates


def resolve_language(data):
    obj(data, 'language resolution input')
    existing = language_record(data['language']) if data.get('schema_version') in {'1.5', '1.6'} and 'language' in data else None
    if existing and 'language_context' not in data:
        return dict(existing, status='retained', questions=[])
    candidates = language_candidates(data.get('language_context', {}))
    # An existing artifact is evidence at its own priority, never a new default.
    if existing and not candidates['existing']:
        candidates['existing'] = [dict(locale=existing['locale'], source=existing['source'])]
    for basis in ('user', 'project', 'existing', 'context'):
        evidence = candidates['audience'] + candidates['documents'] if basis == 'context' else candidates[basis]
        if not evidence:
            continue
        if len({item['locale'] for item in evidence}) != 1:
            return language_question(existing, 'Conflicting language evidence at ' + basis)
        locale = evidence[0]['locale']
        status = 'resolved'
        if existing:
            status = 'retained' if locale == existing['locale'] else 'change-proposed'
        return dict(status=status, locale=locale, basis=basis, source=evidence[0]['source'],
                    rationale='Language selected from ' + basis + ' evidence.', questions=[],
                    retained_locale=existing['locale'] if existing else None)
    return language_question(existing, 'No supported language evidence supplied')


def language_question(existing, reason):
    return dict(status='needs-input', locale=None, reason=reason,
                retained_locale=existing['locale'] if existing else None,
                questions=['Which deliverable language should be used: English or Simplified Chinese? / 交付物使用英文还是简体中文？'])



@cache
def localized_catalog():
    path = Path(__file__).with_name('roadmap-zh-CN.json')
    try:
        catalog = obj(json.loads(path.read_text(encoding='utf-8')), 'localization catalog')
        if any(not isinstance(value, str) for value in catalog.values()):
            raise ValueError('catalog values must be strings')
        return catalog
    except (OSError, ValueError) as exc:
        raise ValueError(f'Cannot load localization catalog at {path}; '
                         'restore the bundled roadmap-zh-CN.json from this skill version') from exc


def ui(data, message):
    locale = data['language']['locale'] if data and data.get('schema_version') in {'1.5', '1.6'} else 'en'
    if locale == 'en':
        return message.removeprefix('value:')
    if locale != 'zh-CN':
        raise ValueError('unsupported language.locale: ' + str(locale))
    catalog = localized_catalog()
    if message not in catalog:
        raise ValueError('missing localized message: ' + message)
    return catalog[message]


def display(data, value):
    return ui(data, 'value:' + value)



def context_questions(fields):
    prompts = {'work_mode': 'How does work progress: iterations, flow, stages or discovery?',
               'delivery': 'How is value delivered: continuously, versioned or through acceptance?',
               'audience': 'Who needs to read and act on the plan?',
               'constraints': 'Which deadlines, acceptance conditions or dependencies apply (or explicitly none)?',
               'source': 'Which existing record supports these facts?'}
    return [prompts[field] for field in fields]


def enabled(data, view):
    return data['schema_version'] not in {'1.4', '1.5', '1.6'} or view in data['views']



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
    choice(data.get('schema_version'), {'1.0', '1.1', '1.2', '1.3', '1.4', '1.5', '1.6'}, 'schema_version')
    if data['schema_version'] == '1.0' and any(k in data for k in ('phases', 'milestones')):
        raise ValueError('phases/milestones require schema_version 1.1 or later')
    for field in ('project', 'updated', 'direction', 'ordering', 'closure', 'priority_policy'):
        text(data.get(field), field)
    if data['schema_version'] in {'1.3', '1.4', '1.5', '1.6'} and policy_is_reference(data['priority_policy']):
        reference(data['priority_policy'], 'priority_policy')
    iso(data['updated'], 'updated')
    views = array(data.get('views'), 'views')
    options = {'requirements', 'versions', 'schedule'}
    if data['schema_version'] in {'1.3', '1.4', '1.5', '1.6'}:
        options.add('iterations')
    if data['schema_version'] in {'1.4', '1.5', '1.6'}:
        options.update({'phases', 'milestones', 'flow'})
    for view in views:
        choice(view, options, 'views')
    if len(set(views)) != len(views) or 'requirements' not in views:
        raise ValueError('views: unique selections including requirements required')
    entries = array(data.get('entries'), 'entries')
    versions = array(data.get('versions', []), 'versions')
    if 'versions' in views and 'versions' not in data:
        raise ValueError('versions: selected view needs records')
    if len(records(data)) > 200:
        raise ValueError('records: at most 200 planning objects')
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


def timing(item, mode, data=None):
    if item['start'] is None:
        return ui(data, 'Unscheduled')
    if item['kind'] == 'milestone':
        return f'W{item["start"]}' if mode == 'weeks' else item['start']
    if mode == 'weeks':
        return f'W{item["start"]}–W{item["end"] - 1}'
    return str(item['start']) + ui(data, ' to ') + str(item['end']) + ui(data, ' (end exclusive)')


def markdown(data: dict) -> str:
    """Render selected views of validated facts as one Markdown roadmap."""
    if data['schema_version'] in {'1.3', '1.4', '1.5', '1.6'}:
        return main_markdown(data)
    lines = [f'# {md(data["project"])}{ui(data, " Roadmap")}', '', ui(data, 'Updated: ') + data["updated"], '',
             md(data['direction']), '', ui(data, 'Ordering rationale: ') + md(data['ordering']), '',
             ui(data, 'Priority policy: ') + md(data["priority_policy"]), '', ui(data, '## Requirements'), '']
    lines.extend(requirement_markdown(data))
    lines.extend(['', ui(data, 'Closure criterion: ') + md(data['closure']), ''])
    if 'versions' in data['views']:
        lines.extend(version_markdown(data))
    lines.extend(event_markdown(data))
    if 'schedule' in data['views']:
        lines.extend(schedule_markdown(data))
    lines.extend(revision_markdown(data))
    lines.extend(['', ui(data, 'Backlog requirements and defects map to this roadmap; items outside it are not done by default.'),
                  ui(data, 'Placement grants no implementation or release approval.'), ''])
    return '\n'.join(lines)


def plan_header(data):
    lines = [f'# {md(data["project"])}{ui(data, " Roadmap")}', '', ui(data, 'Updated: ') + data["updated"], '',
             ui(data, '## Overview'), '', ui(data, 'Direction: ') + md(data['direction']), '',
             ui(data, 'Current arrangement: ') + md(data['ordering']), '']
    lines += execution_warning(data)
    return lines + [ui(data, '## Priority arrangement'), '']


def policy_is_reference(value: str) -> bool:
    return value.startswith(('http://', 'https://', '#', './', '../')) or bool(
        re.fullmatch(r'[^\s]+\.md(?:#[^\s]*)?', value))


def planning_basis(data: dict) -> list[str]:
    policy = data['priority_policy']
    if policy_is_reference(policy):
        reference(policy, 'priority_policy')
        policy = '[' + ui(data, 'Priority policy') + '](' + quote(policy, safe='/:#?=&%+~.-_') + ')'
    else:
        policy = ui(data, 'Priority policy: ') + md(policy)
    lines = ['', ui(data, '## Planning basis and sources'), '', policy, '',
             ui(data, 'Closure criterion: ') + md(data['closure']), '']
    if data['schema_version'] in {'1.4', '1.5', '1.6'}:
        lines += ['#' + line if line.startswith('## ') else line
                  for line in selection_markdown(data)]
    if data['schema_version'] in {'1.5', '1.6'}:
        lines += language_markdown(data)
    return lines


def execution_warning(data: dict) -> list[str]:
    unknown = [e['id'] for e in data['entries'] if e['execution'] is None]
    return [ui(data, 'Unverified execution mappings: ') + ', '.join(unknown) + '.', ''] if unknown else []



def language_markdown(data):
    language = data['language']
    return [ui(data, 'Deliverable language: ') + display(data, language['locale']) +
            ' · ' + display(data, language['basis']), '',
            md(language['rationale']) + ui(data, ' [Language source](') +
            quote(language['source'], safe='/:#?=&%+~.-_') + ')' + ui(data, '.'), '']


def selection_markdown(data):
    selected = data['selection']
    return [ui(data, '## Planning approach'), '',
            ui(data, 'Scenario: ') + display(data, selected['scenario']) + ui(data, ' · Primary: ') + display(data, selected['primary']) +
            ui(data, ' · Layout: ') + display(data, selected['layout']), '',
            ui(data, 'Enabled views: ') + ui(data, ', ').join(display(data, view) for view in data['views']) + ui(data, '.'), '',
            md(selected['rationale']) + ui(data, ' [Selection source](') +
            quote(selected['source'], safe='/:#?=&%+~.-_') + ')' + ui(data, '.'), '']


def flow_markdown(data):
    flow = data['flow']
    return [ui(data, '## Flow'), '', ui(data, 'Workflow policy: ') + md(flow['policy']), '',
            ui(data, 'Service expectation: ') + md(flow['expectation']), '',
            ui(data, 'Flow metrics: ') + md(flow['metrics']), '',
            ui(data, '[Workflow source](') + quote(flow['source'], safe='/:#?=&%+~.-_') + ') · ' +
            ui(data, '[Execution board](') + quote(flow['board'], safe='/:#?=&%+~.-_') + ')', '']



def priority_markdown(data):
    active = [e for e in data['entries'] if e['execution'] != 'Completed']
    completed = [e for e in data['entries'] if e['execution'] == 'Completed']
    lines = requirement_markdown(dict(data, entries=active), include_warning=False)
    if completed:
        lines += ['', '<details>', '<summary>' + ui(data, 'Completed requirements and defects') + f' ({len(completed)})</summary>', '']
        lines += requirement_markdown(dict(data, entries=completed), include_warning=False)
        lines += ['', '</details>']
    return lines


def delivery_markdown(data):
    lines = []
    if 'flow' in data['views']:
        lines += flow_markdown(data)
    if 'iterations' in data['views']:
        lines += iteration_markdown(data)
    if 'versions' in data['views']:
        lines += [''] + version_markdown(data)
    lines += event_markdown(data)
    if data['schema_version'] in {'1.4', '1.5', '1.6'}:
        lines = primary_first(lines, data['selection']['primary'], data)
    if lines:
        lines = ['', ui(data, '## Delivery plan'), ''] + [
            '#' + line if line.startswith('## ') else line for line in lines]
    if 'schedule' in data['views']:
        lines += timeline_markdown(data)
    return lines


def primary_first(lines, primary, data=None):
    chunks, current = [], []
    for line in lines:
        if line.startswith('## ') and current:
            chunks.append(current)
            current = []
        current.append(line)
    if current:
        chunks.append(current)
    heading = ui(data, '## ' + primary.capitalize())
    chunks.sort(key=lambda chunk: 0 if heading in chunk else 1)
    return [line for chunk in chunks for line in chunk]



def timeline_markdown(data):
    lines = schedule_markdown(data, heading='## Timeline')
    timing_table = next(line for line in lines if line.startswith(ui(data, '| Reference |')))
    image = ui(data, '![Roadmap schedule](roadmap.svg)')
    lines.remove(timing_table)
    lines.remove(image)
    # Keep the primary diagram visible and the duplicate tabular encoding optional.
    lines[7:7] = [image, '', '<details>', ui(data, '<summary>Timing details</summary>'), '',
                  timing_table, '', '</details>', '']
    return lines


def iteration_window(data, key):
    schedule = data.get('schedule', {}) if 'schedule' in data['views'] else {}
    item = next((i for i in schedule.get('items', []) if i['ref'] == key), None)
    if item is None or item['start'] is None:
        return ui(data, 'Unscheduled')
    return display(data, item['basis']) + ' · ' + timing(item, schedule['mode'], data)


def iteration_versions(data, iteration):
    return ', '.join(v['id'] for v in data.get('versions', [])
                     if set(v['members']) & set(iteration['members'])) or ui(data, 'Unassigned')


def iteration_markdown(data):
    rows = [[i['id'] + ' · ' + md(i['name']), md(i['goal']), iteration_window(data, i['id']),
             ', '.join(i['members']) or ui(data, 'None'), iteration_versions(data, i), display(data, 'Unknown') if i['owner'] == 'Unknown' else md(i['owner']),
             ui(data, '[Source](') + quote(i['source'], safe='/:#?=&%+~.-_') + ')',
             ui(data, '[Board](') + quote(i['board'], safe='/:#?=&%+~.-_') + ')'
             if i.get('board') else '—'] for i in data['iterations']]
    lines = [ui(data, '## Iterations'), '', ui(data, 'Cadence: ') + md(data['cadence']), '', table(
        [ui(data, 'Iteration'), ui(data, 'Goal'), ui(data, 'Timebox / basis'), ui(data, 'Members'), ui(data, 'Versions touched'), ui(data, 'Owner'), ui(data, 'Source'), ui(data, 'Execution detail')], rows)]
    if not rows:
        lines += ['', ui(data, 'No iterations planned.')]
    assigned = {member for i in data['iterations'] for member in i['members']}
    unassigned = [e['id'] for e in data['entries'] if e['id'] not in assigned]
    if unassigned:
        lines += ['', ui(data, 'Not allocated to an iteration: ') + ', '.join(unassigned) + '.']
    return lines + ['', ui(data, 'Iteration boundaries do not prove completion, reach milestones or authorize release.')]


def delivery_summary(data):
    lines = ['', ui(data, '## Delivery outlook'), '']
    if 'flow' in data['views']:
        lines += [ui(data, 'Workflow policy: ') + md(data['flow']['policy']), '',
                  ui(data, 'Service expectation: ') + md(data['flow']['expectation']), '']
    if data['schema_version'] in {'1.4', '1.5', '1.6'} and data.get('phases') and enabled(data, 'phases'):
        lines += [table([ui(data, 'Phase'), ui(data, 'Scope'), ui(data, 'Exit condition')], [
            [p['id'] + ' · ' + md(p['name']), ', '.join(p['scope']), md(p['exit_condition'])]
            for p in data['phases']]), '']
    if 'iterations' in data['views']:
        lines += [ui(data, 'Cadence: ') + md(data['cadence']), '', table([ui(data, 'Iteration / goal'), ui(data, 'Timebox / basis')], [
            [i['id'] + ' · ' + md(i['goal']), iteration_window(data, i['id'])] for i in data['iterations']])]
    if 'versions' in data['views']:
        lines += ['', table([ui(data, 'Version / outcome'), ui(data, 'Members'), ui(data, 'Delivery window')], [
            [v['id'] + ' · ' + md(v['outcome']), ', '.join(v['members']) or ui(data, 'None'), display(data, 'Unknown') if v['window'] == 'Unknown' else md(v['window'])]
            for v in data['versions']])]
    if data.get('milestones') and enabled(data, 'milestones'):
        lines += ['', table([ui(data, 'Key event'), ui(data, 'State'), ui(data, 'Timing / basis')], [
            [m['id'] + ' · ' + md(m['name']), display(data, m['state']), iteration_window(data, m['id'])]
            for m in data['milestones']])]
    return lines + ['', ui(data, '[Delivery details and timeline](roadmap-delivery.md).')]


def main_markdown(data, split=False):
    lines = plan_header(data) + priority_markdown(data)
    detail = delivery_markdown(data)
    lines += delivery_summary(data) if split and detail else detail
    lines += revision_markdown(data)
    if split and data.get('revisions') and data['schema_version'] in {'1.2', '1.3', '1.4', '1.5', '1.6'}:
        lines += ['', ui(data, '[Supplied revision details](roadmap-history.md).')]
    lines += planning_basis(data)
    lines += ['', ui(data, 'Backlog requirements and defects map to this roadmap; items outside it are not done by default.'),
              ui(data, 'Placement grants no implementation or release approval.'), '']
    return clean_markdown(lines)


def clean_markdown(lines):
    return re.sub(r'\n{3,}', '\n\n', '\n'.join(lines)).rstrip() + '\n'


def selected_layout(data, layout=None):
    retained = data['selection']['layout'] if data['schema_version'] in {'1.4', '1.5', '1.6'} else None
    if layout is not None and retained is not None and layout != retained:
        raise ValueError('layout conflicts with retained selection; update its source decision first')
    layout = layout or retained or 'single'
    choice(layout, {'single', 'split', 'topic-split'}, 'layout')
    if layout == 'topic-split':
        if data['schema_version'] != '1.6':
            raise ValueError('topic-split requires schema_version 1.6')
    return layout


def documents(data, layout=None):
    layout = selected_layout(data, layout)
    if layout == 'topic-split':
        return topic_documents(data)
    outputs = {'roadmap.md': markdown(data) if layout == 'single' else main_markdown(data, True)}
    if layout == 'split':
        detail = delivery_markdown(data)
        if detail:
            outputs['roadmap-delivery.md'] = clean_markdown([
                '# ' + md(data['project']) + ui(data, ' Delivery Details'), '', ui(data, '[Main roadmap](roadmap.md)'),
                '', ui(data, 'Updated: ') + data['updated'], '', ui(data, 'Generated view; maintain linked source records.'), *detail, ''])
        if data['schema_version'] in {'1.2', '1.3', '1.4', '1.5', '1.6'} and data['revisions']:
            outputs['roadmap-history.md'] = clean_markdown([
                '# ' + md(data['project']) + ui(data, ' Revision Details'), '', ui(data, '[Main roadmap](roadmap.md)'),
                '', ui(data, 'Updated: ') + data['updated'], '', ui(data, 'Supplied decisions; linked history may contain earlier records.'),
                *revision_markdown(data, None), ''])
    if 'schedule' in data['views']:
        outputs['roadmap.svg'] = svg(data)
        if data['schedule']['mode'] == 'dates':
            outputs['roadmap.mmd'] = mermaid(data)
    return outputs


def revision_markdown(data, limit=5):
    if data['schema_version'] not in {'1.2', '1.3', '1.4', '1.5', '1.6'}:
        return []
    revisions = data['revisions']
    lines = ['', ui(data, '## Revision history'), '']
    if not revisions:
        lines.append(ui(data, 'No material revisions recorded; earlier history is not certified by this input.'))
    else:
        rows = [[r['date'] + ' · ' + r['id'], md(r['change']), md(r['reason']),
                 md(r['impact']), ui(data, '[Details](') + quote(r['source'], safe='/:#?=&%+~.-_') + ')']
                for r in (revisions if limit is None else revisions[:limit])]
        lines.append(table([ui(data, 'Date / revision'), ui(data, 'Change'), ui(data, 'Reason'), ui(data, 'Impact'), ui(data, 'Details')], rows))
    if data.get('revision_history'):
        link = quote(data['revision_history'], safe='/:#?=&%+~.-_')
        lines.extend(['', ui(data, '[Full revision history](') + link + ').'])
    if limit is not None and len(revisions) > limit:
        lines.extend(['', str(len(revisions) - limit) + ' ' + ui(data, 'older revisions retained in the linked history; omitted here.')])
    return lines


def requirement_markdown(data: dict, include_warning: bool = True) -> list:
    lines = []
    rows = []
    for entry in data['entries']:
        link = quote(entry['source'], safe='/:#?=&%+~.-_')
        rows.append([display(data, entry['tier']), f'[{entry["id"]} · {md(entry["name"])}]({link})',
                     md(entry['outcome']), entry['priority'], md(entry['approval']),
                     display(data, entry['execution']) if entry['execution'] else '—', f'[{md(entry["conditions"])}]({link})'])
    lines.append(table([ui(data, 'Tier'), ui(data, 'Requirement / defect'), ui(data, 'Expected outcome'), ui(data, 'Priority'),
                        ui(data, 'Approval status'), ui(data, 'Execution status'), ui(data, 'Key conditions')], rows))
    empty = [tier for tier in ('Now', 'Next', 'Later') if not any(e['tier'] == tier for e in data['entries'])]
    if empty:
        lines.extend(['', ui(data, 'No items planned: ') + ui(data, ', ').join(display(data, tier) for tier in empty) + '.'])
    if include_warning:
        unknown = [e['id'] for e in data['entries'] if e['execution'] is None]
        if unknown:
            lines.extend(['', ui(data, 'Unverified execution mappings: ') + ', '.join(unknown) + '.'])
    return lines


def version_markdown(data: dict) -> list:
    lines = []
    rows = [[v['id'] + ' · ' + md(v['name']), ', '.join(v['members']) or ui(data, 'None'),
             md(v['outcome']), display(data, 'Unknown') if v['owner'] == 'Unknown' else md(v['owner']), display(data, 'Unknown') if v['window'] == 'Unknown' else md(v['window'])] for v in data['versions']]
    lines.extend([ui(data, '## Versions'), '', table([ui(data, 'Version'), ui(data, 'Members'), ui(data, 'Core outcome'), ui(data, 'Owner'), ui(data, 'Delivery window')], rows)])
    assigned = {ref for v in data['versions'] for ref in v['members']}
    unassigned = [e['id'] for e in data['entries'] if e['id'] not in assigned]
    if unassigned:
        lines.extend(['', ui(data, 'Unassigned: ') + ', '.join(unassigned) + '.'])
    return lines


def event_markdown(data):
    lines = []
    if data.get('phases') and enabled(data, 'phases'):
        rows = [[p['id'] + ' · ' + md(p['name']), ', '.join(p['scope']), display(data, 'Unknown') if p['owner'] == 'Unknown' else md(p['owner']),
                 md(p['exit_condition']), '[' + p['id'] + '](' +
                 quote(p['source'], safe='/:#?=&%+~.-_') + ')'] for p in data['phases']]
        lines.extend(['', ui(data, '## Phases'), '', table(
            [ui(data, 'Phase'), ui(data, 'Scope'), ui(data, 'Owner'), ui(data, 'Exit condition'), ui(data, 'Source')], rows)])
    if data.get('milestones') and enabled(data, 'milestones'):
        rows = [[m['id'] + ' · ' + md(m['name']), display(data, m['category']), ', '.join(m['related']) or ui(data, 'Global'),
                 display(data, 'Unknown') if m['owner'] == 'Unknown' else md(m['owner']), display(data, m['state']), md(m['criterion']),
                 ui(data, '[Source](') + quote(m['source'], safe='/:#?=&%+~.-_') + ')',
                 ui(data, '[Evidence](') + quote(m['evidence'], safe='/:#?=&%+~.-_') + ')'
                 if m.get('evidence') else '—'] for m in data['milestones']]
        lines.extend(['', ui(data, '## Milestones'), '', table(
            [ui(data, 'Milestone'), ui(data, 'Category'), ui(data, 'Related'), ui(data, 'Owner'), ui(data, 'State'), ui(data, 'Occurrence criterion'), ui(data, 'Source'), ui(data, 'Evidence')], rows),
            '', ui(data, 'Milestones are events; dates and related work do not prove occurrence or grant approval.')])
    return lines


def schedule_markdown(data: dict, heading='## Schedule') -> list:
    lines = []
    schedule = data['schedule']
    rows = [[i['ref'], display(data, i['kind']), display(data, i['basis']), timing(i, schedule['mode'], data),
             ', '.join(i['depends_on']) or ui(data, 'None')] for i in schedule['items']]
    lines.extend(['', ui(data, heading), '', md(schedule['origin']), '',
                  ui(data, 'Elapsed calendar days / whole weeks; spans have exclusive ends.'), '',
                  table([ui(data, 'Reference'), ui(data, 'Kind'), ui(data, 'Timing basis'), ui(data, 'Window'), ui(data, 'Depends on')], rows), '',
                  ui(data, '![Roadmap schedule](roadmap.svg)')])
    covered = {i['ref'] for i in schedule['items']}
    covered.update(ref for v in data.get('versions', []) if v['id'] in covered for ref in v['members'])
    missing = [e['id'] for e in data['entries'] + data.get('phases', []) +
               data.get('milestones', []) + (data.get('iterations', []) if data['schema_version'] in {'1.3', '1.4', '1.5', '1.6'} else [])
               if e['id'] not in covered]
    if missing:
        lines.extend(['', ui(data, 'No schedule assigned: ') + ', '.join(missing) + '.'])
    unknown = [i['ref'] for i in schedule['items'] if i['start'] is None]
    if unknown:
        lines.extend(['', ui(data, 'Unscheduled: ') + ', '.join(unknown) + '.'])
    unverified = [f'{dep} → {i["ref"]}' for i in schedule['items'] for dep in i['depends_on']
                  if dep in unknown or i['ref'] in unknown]
    if unverified:
        lines.extend(['', ui(data, 'Unverified dependency timing: ') + ', '.join(unverified) + '.'])
    if schedule['mode'] == 'dates':
        lines.extend(['', '```mermaid', mermaid(data).rstrip(), '```'])
    return lines


def mermaid(data: dict) -> str:
    if data['schedule']['mode'] != 'dates':
        raise ValueError('Mermaid Gantt output requires dates; relative weeks use SVG')
    names = {r['id']: r['name'] for r in records(data)}
    names.update({m['id']: m['name'] + ' [' + display(data, m['state']) + ']'
                  for m in data.get('milestones', [])})
    lines = ['gantt', '    dateFormat YYYY-MM-DD', '    axisFormat %m-%d', '    todayMarker off']
    for item in data['schedule']['items']:
        if item['start'] is None:
            continue
        # Labels cannot introduce Mermaid directives or metadata delimiters.
        label = re.sub(r'[^\w .()/-]', ' ', names[item['ref']], flags=re.UNICODE)
        label = ' '.join(label.split()) or item['ref']
        label = f'{item["ref"]} {label} ({display(data, item["basis"])})'
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
    svg_axes(root, low, high, schedule['mode'], len(items), xpos, data)
    positions = {i['ref']: 136 + index * 84 + 20 for index, i in enumerate(items)}
    for item in items:
        svg_row(root, item, coords, positions, names, schedule['mode'], xpos, states, data)
    if not items:
        svg_label(root, 20, 156, ui(data, 'No items scheduled'))
    svg_label(root, 20, 136 + max(1, len(items)) * 84 + 25,
              ui(data, 'Bars show elapsed time, not completion percentage.'))
    return ET.tostring(root, encoding='unicode') + '\n'


def svg_root(data, schedule, count):
    width, top, row_height = 960, 136, 84
    root = ET.Element('svg', xmlns='http://www.w3.org/2000/svg', width=str(width),
                      height=str(top + max(1, count) * row_height + 48),
                      viewBox=f'0 0 {width} {top + max(1, count) * row_height + 48}',
                      role='img', **{'aria-labelledby': 'title description'})
    if data['schema_version'] in {'1.5', '1.6'}:
        root.set('{http://www.w3.org/XML/1998/namespace}lang', data['language']['locale'])
    ET.SubElement(root, 'title', id='title').text = data['project'] + ui(data, ' schedule')
    ET.SubElement(root, 'desc', id='description').text = schedule['origin'] + ui(data, '; target, committed and actual timing are labeled; exclusive ends.')
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
    svg_label(root, 20, 100, ui(data, 'Reference / timing basis'))
    svg_label(root, 350, 100, ui(data, 'Relative weeks') if schedule['mode'] == 'weeks' else ui(data, 'Calendar dates (end exclusive)'))


def svg_axes(root, low, high, mode, count, xpos, data=None):
    ticks = sorted({low + round((high - low) * n / 4) for n in range(5)})
    for tick in ticks:
        x = xpos(tick)
        ET.SubElement(root, 'line', x1=str(x), y1='128', x2=str(x),
                      y2=str(136 + count * 84), **{'class': 'grid'})
        value = f'W{tick}' if mode == 'weeks' else date.fromordinal(tick).isoformat()
        svg_label(root, x, 121, value, **{'text-anchor': 'middle'})


def svg_row(root, item, coords, positions, names, mode, xpos, states, data=None):
    ref, y = item['ref'], positions[item['ref']]
    # Full accessible labels remain available even when visual wrapping is abbreviated.
    full = f'{ref} · {names[ref]}'
    chunks = wrap_label(full)
    for n, chunk in enumerate(chunks[:2]):
        svg_label(root, 20, y + n * 17, chunk + ('…' if n == 1 and len(chunks) > 2 else ''))
    state = ' · ' + display(data, states[ref]) if ref in states else ''
    svg_label(root, 20, y + 42, display(data, item['basis']) + ' · ' + timing(item, mode, data) + state)
    if ref not in coords:
        svg_label(root, 362, y + 12, ui(data, 'Unscheduled'))
        return
    start, end = coords[ref]
    x1, x2 = xpos(start), xpos(end)
    if item['kind'] == 'milestone':
        shape = ET.SubElement(root, 'polygon', points=f'{x1},{y} {x1+7},{y+9} {x1},{y+18} {x1-7},{y+9}',
                              **{'class': 'milestone'})
    else:
        shape = ET.SubElement(root, 'rect', x=str(x1), y=str(y), width=str(x2 - x1), height='18', **{'class': 'span'})
    ET.SubElement(shape, 'title').text = full + ' · ' + timing(item, mode, data)
    for dep in item['depends_on']:
        if dep not in coords:
            continue
        dx, dy = xpos(coords[dep][1]), positions[dep] + 9
        path = f'M {dx} {dy} L {dx+8} {dy} L {dx+8} {y-8} L {x1} {y-8} L {x1} {y}'
        ET.SubElement(root, 'path', d=path, **{'class': 'dependency'})
        ET.SubElement(root, 'polygon', points=f'{x1},{y} {x1-4},{y-6} {x1+4},{y-6}', fill='#526777')


TOPIC_DOCUMENTS = ('roadmap.md', 'iterations.md', 'versions.md', 'milestones.md',
                   'roadmap-planning-basis.md', 'roadmap-history.md')
TOPIC_OUTPUTS = TOPIC_DOCUMENTS + ('roadmap.svg', 'roadmap.mmd')
MANIFEST = '.roadmap-outputs.json'


def heading_slug(value):
    return re.sub(r'[^\w\- ]', '', value.lower()).replace(' ', '-')


def validate_blank_documents(outputs):
    """Check the emitted structure, rather than claiming validity after a read."""
    if set(outputs) != set(TOPIC_DOCUMENTS):
        raise ValueError('blank structure: expected exactly six topic documents')
    headings = {name: {heading_slug(h) for h in re.findall(r'^#+ (.+)$', value, re.M)}
                for name, value in outputs.items()}
    for name, value in outputs.items():
        if len(re.findall(r'^# ', value, re.M)) != 1 or re.search(r'</?[A-Za-z][^>]*>', value):
            raise ValueError('blank structure: invalid title or HTML in ' + name)
        for block in value.strip().split('\n\n'):
            if re.fullmatch(r'#{1,2} [^\n]+', block):
                continue
            if re.fullmatch(r'\*\*[^*\n]+[:：]\*\* \{(?:Pending|待填写)\}', block):
                continue
            if re.fullmatch(r'\[[^]]+\]\([^)]+\)(?: · \[[^]]+\]\([^)]+\))*', block):
                continue
            if block.startswith('|'):
                rows = block.splitlines()
                if (len(rows) == 2 and len(rows[0].split('|')) == len(rows[1].split('|')) and
                        all(cell.strip() == '---' for cell in rows[1].strip('|').split('|'))):
                    continue
            raise ValueError('blank structure: author guidance or malformed field/table in ' + name)
        for target in re.findall(r'\]\(([^)]+)\)', value):
            path, separator, anchor = target.partition('#')
            if path not in outputs or (separator and anchor not in headings[path]):
                raise ValueError('blank structure: broken navigation in ' + name + ': ' + target)


def blank_documents(locale='en'):
    """Render clean scaffold assets without accepting or reading business facts."""
    choice(locale, {'en', 'zh-CN'}, 'locale')
    data = dict(schema_version='1.6', language=dict(locale=locale))
    outputs = {}
    for name in TOPIC_DOCUMENTS:
        source = Path(__file__).resolve().parents[1] / 'assets/structure-first' / name
        value = source.read_text(encoding='utf-8')
        if locale == 'zh-CN':
            translated = []
            for line in value.splitlines():
                if line.startswith('#'):
                    prefix, label = line.split(' ', 1)
                    line = prefix + ' ' + ui(data, label)
                elif line.startswith('**'):
                    label = line.split(':**', 1)[0][2:]
                    line = '**' + ui(data, label) + '：** {待填写}'
                elif line.startswith('|') and '---' not in line:
                    line = '| ' + ' | '.join(ui(data, cell.strip()) for cell in line.strip('|').split('|')) + ' |'
                elif line.startswith('['):
                    def translate_link(match):
                        label, target = match.groups()
                        path, separator, anchor = target.partition('#')
                        if separator:
                            headings = {'completed-and-closed-items': 'Completed and closed items',
                                        'pending-decisions': 'Pending decisions', 'unknown-facts': 'Unknown facts',
                                        'timeline': 'Timeline'}
                            anchor = heading_slug(ui(data, headings[anchor]))
                        return '[' + ui(data, label) + '](' + path + (separator + anchor if separator else '') + ')'
                    line = re.sub(r'\[([^]]+)\]\(([^)]+)\)', translate_link, line)
                translated.append(line)
            value = '\n'.join(translated) + '\n'
        outputs[name] = value
    validate_blank_documents(outputs)
    return outputs


def topic_documents(data):
    """Populate the confirmed scaffold without changing its headings or columns."""
    outputs = blank_documents(data['language']['locale'])
    pending = '{Pending}' if data['language']['locale'] == 'en' else '{待填写}'
    colon = ':' if data['language']['locale'] == 'en' else '：'

    def field(name, label, value):
        key = '**' + ui(data, label) + colon + '** ' + pending
        outputs[name] = outputs[name].replace(key, key.replace(pending, value))

    def fill_tables(name, rows):
        index = 0
        def populate(match):
            nonlocal index
            header = match.group(0).splitlines()[0]
            columns = [cell.strip() for cell in header.strip('|').split('|')]
            value = table(columns, rows[index]) + '\n'
            index += 1
            return value
        outputs[name] = re.sub(r'(?:^\|.*\|\n)+', populate, outputs[name], flags=re.M)

    def link(label, source):
        return '[' + md(label) + '](' + quote(source, safe='/:#?=&%+~.-_') + ')'

    def refs(values):
        return ', '.join(values) or ui(data, 'None')

    unknown = ui(data, 'Unknown')
    policy = link(ui(data, 'Priority policy'), data['priority_policy']) if policy_is_reference(data['priority_policy']) else md(data['priority_policy'])
    for name in TOPIC_DOCUMENTS:
        field(name, 'Updated', data['updated'])
        if name != 'roadmap.md':
            outputs[name] = outputs[name].replace('# ', '# ' + md(data['project']) + ' ', 1)
    outputs['roadmap.md'] = outputs['roadmap.md'].replace(ui(data, '{Project} Roadmap'),
        md(data['project']) + ui(data, ' Roadmap'), 1)
    field('roadmap.md', 'Direction and goal', md(data['direction']))
    field('roadmap.md', 'Current arrangement and rationale', md(data['ordering']))
    field('roadmap.md', 'Subsequent work and key conditions', ui(data, 'See delivery outlook and linked conditions.'))
    unverified = [e['id'] for e in data['entries'] if e['execution'] is None]
    unknown_records = unverified + [r['id'] for r in records(data) if r.get('owner') == 'Unknown' or r.get('window') == 'Unknown']
    field('roadmap.md', 'Material unknowns', refs(dict.fromkeys(unknown_records)) if unknown_records else ui(data, 'No additional unknowns supplied.'))
    active = [e for e in data['entries'] if e['execution'] != 'Completed']
    field('roadmap.md', 'Tier summary', '; '.join(display(data, tier) + ': ' + refs(e['id'] for e in active if e['tier'] == tier)
                                                for tier in ('Now', 'Next', 'Later')))
    field('roadmap.md', 'Execution evidence and mapping', ui(data, 'Source records: ') + ', '.join(link(e['id'], e['source']) for e in data['entries']))
    field('roadmap.md', 'Cadence and basis', md(data.get('cadence', unknown)))
    field('roadmap.md', 'Priority policy', policy)
    field('roadmap.md', 'Closure criterion', md(data['closure']))
    requirement_rows = [[display(data, e['tier']), link(e['id'] + ' · ' + e['name'], e['source']), md(e['outcome']),
                         e['priority'], md(e['approval']), display(data, e['execution']) if e['execution'] else '—',
                         link(e['conditions'], e['source'])] for e in active]
    iterations = data['iterations'] if 'iterations' in data['views'] else []
    versions = data['versions'] if 'versions' in data['views'] else []
    events = data.get('milestones', []) if enabled(data, 'milestones') else []
    revision_rows = [[r['date'] + ' · ' + r['id'], md(r['change']), md(r['reason']), md(r['impact']),
                      link(ui(data, 'Details'), r['source'])] for r in data['revisions']]
    schedule_rows = []
    field('roadmap.md', 'Origin, calendar and exclusive end', (md(data['schedule']['origin']) + ' · ' + ui(data, 'Elapsed calendar days / whole weeks; spans have exclusive ends.')) if 'schedule' in data['views'] else unknown)
    if 'schedule' in data['views']:
        schedule = data['schedule']
        schedule_rows = [[i['ref'], display(data, i['kind']), display(data, i['basis']), timing(i, schedule['mode'], data),
                          refs(i['depends_on'])] for i in schedule['items']]
        unknown_times = [i['ref'] for i in schedule['items'] if i['start'] is None]
        scheduled = {i['ref'] for i in schedule['items']}
        covered = scheduled | {ref for v in data.get('versions', []) if v['id'] in scheduled for ref in v['members']}
        unknown_times += [r['id'] for r in records(data) if r['id'] not in covered]
        field('roadmap.md', 'Unscheduled work and timing exceptions', refs(dict.fromkeys(unknown_times)))
        diagram_key = '**' + ui(data, 'Schedule diagram') + colon + '** ' + pending
        outputs['roadmap.md'] = outputs['roadmap.md'].replace(diagram_key, ui(data, '![Roadmap schedule](roadmap.svg)'))
    else:
        field('roadmap.md', 'Unscheduled work and timing exceptions', refs(r['id'] for r in records(data)))
        field('roadmap.md', 'Schedule diagram', unknown)
    fill_tables('roadmap.md', [requirement_rows,
        [[i['id'] + ' · ' + md(i['goal']), iteration_window(data, i['id'])] for i in iterations],
        [[v['id'] + ' · ' + md(v['outcome']), refs(v['members']), unknown if v['window'] == 'Unknown' else md(v['window'])] for v in versions],
        [[m['id'] + ' · ' + md(m['name']), display(data, m['state']), iteration_window(data, m['id'])] for m in events],
        schedule_rows, revision_rows[:5]])
    field('iterations.md', 'Cadence and basis', md(data.get('cadence', unknown)))
    allocated = {ref for i in iterations for ref in i['members']}
    field('iterations.md', 'Unallocated work', refs(e['id'] for e in data['entries'] if e['id'] not in allocated))
    field('iterations.md', 'Carry-over record', ', '.join(link(i['id'], i['source']) for i in iterations) or unknown)
    fill_tables('iterations.md', [[[i['id'] + ' · ' + md(i['name']), md(i['goal']), iteration_window(data, i['id']), refs(i['members']),
        iteration_versions(data, i), unknown if i['owner'] == 'Unknown' else md(i['owner']),
        link(ui(data, 'Source'), i['source']) + (' · ' + link(ui(data, 'Board'), i['board']) if i.get('board') else '')] for i in iterations]])
    assigned = {ref for v in versions for ref in v['members']}
    field('versions.md', 'Unassigned work', refs(e['id'] for e in data['entries'] if e['id'] not in assigned))
    fill_tables('versions.md', [[[v['id'] + ' · ' + md(v['name']), refs(v['members']), md(v['outcome']),
        unknown if v['owner'] == 'Unknown' else md(v['owner']), unknown if v['window'] == 'Unknown' else md(v['window'])] for v in versions]])
    fill_tables('milestones.md', [[[m['id'] + ' · ' + md(m['name']), display(data, m['category']), refs(m['related']) if m['related'] else ui(data, 'Global'),
        unknown if m['owner'] == 'Unknown' else md(m['owner']), display(data, m['state']), md(m['criterion']),
        link(ui(data, 'Source'), m['source']), link(ui(data, 'Evidence'), m['evidence']) if m.get('evidence') else '—'] for m in events]])
    archive = [[link(e['id'] + ' · ' + e['name'], e['source']), display(data, e['tier']), display(data, e['execution']), unknown,
                link(ui(data, 'Source'), e['source']), unknown] for e in data['entries'] if e['execution'] == 'Completed']
    fill_tables('roadmap-history.md', [revision_rows, archive])
    if data.get('revision_history'):
        outputs['roadmap-history.md'] += '\n' + link(ui(data, 'Full revision history'), data['revision_history']) + '\n'
    selection = data['selection']
    field('roadmap-planning-basis.md', 'Scenario / primary perspective', display(data, selection['scenario']) + ' / ' + display(data, selection['primary']))
    field('roadmap-planning-basis.md', 'Enabled and omitted views', ', '.join(data['views']) + ' · ' + ui(data, 'Omitted views: ') + refs(sorted({'requirements', 'iterations', 'versions', 'milestones', 'phases', 'flow', 'schedule'} - set(data['views']))))
    field('roadmap-planning-basis.md', 'Layout and selection basis', display(data, selection['layout']) + ' · ' + md(selection['rationale']) + ' · ' + link(ui(data, 'Source'), selection['source']))
    field('roadmap-planning-basis.md', 'Deliverable language and source', data['language']['locale'] + ' · ' + link(ui(data, 'Source'), data['language']['source']))
    field('roadmap-planning-basis.md', 'Priority policy authority', policy)
    field('roadmap-planning-basis.md', 'Closure criterion authority', md(data['closure']))
    field('roadmap-planning-basis.md', 'Existing decisions', link(ui(data, 'Source'), selection['source']))
    source_rows = [[r['id'], md(r['name']), link(ui(data, 'Source'), r['source']), unknown]
                   for r in records(data) if r.get('source')]
    for phase in data.get('phases', []):
        if enabled(data, 'phases'):
            source_rows = [row for row in source_rows if row[0] != phase['id']]
            source_rows.append([phase['id'], md(phase['name']) + ' · ' + ui(data, 'Scope') + colon + ' ' + refs(phase['scope']) + ' · ' + ui(data, 'Owner') + colon + ' ' + (unknown if phase['owner'] == 'Unknown' else md(phase['owner'])) + ' · ' + ui(data, 'Exit condition') + colon + ' ' + md(phase['exit_condition']),
                                link(ui(data, 'Source'), phase['source']), unknown])
    if 'flow' in data['views']:
        flow = data['flow']
        source_rows.append([ui(data, 'Workflow policy'), ui(data, 'Workflow policy: ') + md(flow['policy']) + ' · ' + ui(data, 'Service expectation: ') + md(flow['expectation']) + ' · ' + ui(data, 'Flow metrics: ') + md(flow['metrics']),
                            link(ui(data, 'Source'), flow['source']) + ' · ' + link(ui(data, 'Board'), flow['board']), unknown])
    unknown_rows = [[ref, ui(data, 'Source records'), unknown, ui(data, 'Execution not verified'), ui(data, 'Obtain source evidence')]
                    for ref in unverified]
    fill_tables('roadmap-planning-basis.md', [source_rows, [], unknown_rows])
    if 'schedule' in data['views']:
        outputs['roadmap.svg'] = svg(data)
        if data['schedule']['mode'] == 'dates':
            outputs['roadmap.mmd'] = mermaid(data)
    return outputs


def write_topic_outputs(source, destination, outputs, overwrite):
    """Preflight every reserved path; remove only intact, owned stale outputs."""
    preflight_outputs(source, destination, overwrite, tuple(dict.fromkeys(TOPIC_OUTPUTS + OUTPUTS)) + (MANIFEST,))
    manifest = destination / MANIFEST
    owned = {}
    if manifest.exists():
        owned = json.loads(manifest.read_text(encoding='utf-8'))
        if (not isinstance(owned, dict) or set(owned) - (set(TOPIC_OUTPUTS) | set(OUTPUTS)) or
                any(not isinstance(digest, str) for digest in owned.values())):
            raise ValueError('invalid output ownership manifest')
    unowned_stale = {name for name in set(TOPIC_OUTPUTS) | set(OUTPUTS)
                     if (destination / name).exists()} - outputs.keys() - owned.keys()
    if unowned_stale:
        raise ValueError('unowned reserved outputs would remain; use a separate destination or preserve them explicitly: ' + ', '.join(sorted(unowned_stale)))
    stale = set(owned) - outputs.keys()
    for name in stale:
        path = destination / name
        if path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() != owned[name]:
            raise ValueError('stale generated output was edited; preserve it before changing layout: ' + name)
    destination.mkdir(parents=True, exist_ok=True)
    for name, value in outputs.items():
        path = destination / name
        if not path.exists() or path.read_text(encoding='utf-8') != value:
            path.write_text(value, encoding='utf-8')
    for name in stale:
        (destination / name).unlink(missing_ok=True)
    hashes = {name: hashlib.sha256(value.encode('utf-8')).hexdigest() for name, value in outputs.items()}
    encoded = json.dumps(hashes, sort_keys=True, indent=2) + '\n'
    if not manifest.exists() or manifest.read_text(encoding='utf-8') != encoded:
        manifest.write_text(encoded, encoding='utf-8')


def preflight_outputs(source, destination, overwrite, names=OUTPUTS):
    seen = set()
    for name in names:
        path = destination / name
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError(f'output must be a regular file: {path}')
        if path.exists() and not overwrite:
            raise ValueError(f'output exists: {path}; explicit --overwrite required')
        if source is not None and path.exists() and source.samefile(path):
            raise ValueError('input must not be an output file')
        if path.exists():
            identity = (path.stat().st_dev, path.stat().st_ino)
            if identity in seen:
                raise ValueError('reserved output files must not alias each other')
            seen.add(identity)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, nargs='?')
    parser.add_argument('--output-dir', type=Path)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--overwrite', action='store_true')
    parser.add_argument('--layout', choices=('single', 'split', 'topic-split'))
    parser.add_argument('--blank', action='store_true')
    parser.add_argument('--locale', choices=('en', 'zh-CN'))
    parser.add_argument('--recommend', action='store_true')
    parser.add_argument('--resolve-language', action='store_true')
    args = parser.parse_args()
    try:
        if args.blank:
            if args.input is not None or args.recommend or args.resolve_language or args.layout not in {None, 'topic-split'}:
                raise ValueError('--blank accepts no business input or recommendation and requires topic-split layout')
            outputs = blank_documents(args.locale or 'en')
            if args.check:
                print('Blank roadmap structure valid; business criteria not evaluated; no files written.')
                return 0
            if args.output_dir is None:
                raise ValueError('--output-dir required unless --check is used')
            write_topic_outputs(None, args.output_dir, outputs, args.overwrite)
            print('Blank roadmap structure written; business criteria not evaluated.')
            return 0
        if args.locale is not None:
            raise ValueError('--locale is only for --blank; populated inputs retain their language record')
        if args.input is None:
            raise ValueError('business input required unless --blank is used')
        if args.input.stat().st_size > 1_048_576:
            raise ValueError('input exceeds 1 MiB')
        data = json.loads(args.input.read_text(encoding='utf-8'))
        if args.recommend or args.resolve_language:
            if (args.recommend and args.resolve_language) or args.check or args.output_dir is not None or args.overwrite or args.layout is not None:
                raise ValueError('read-only recommendation/resolution cannot combine with other modes or output flags')
            print(json.dumps(resolve_language(data) if args.resolve_language else recommend(data), ensure_ascii=False, indent=2))
            return 0
        data = validate(data)
        selected_layout(data, args.layout)
        if args.check:
            print('Roadmap input valid; no files written.')
            return 0
        if args.output_dir is None:
            raise ValueError('--output-dir required unless --check is used')
        outputs = documents(data, args.layout)
        if 'iterations.md' in outputs or (args.output_dir / MANIFEST).exists() or (args.output_dir / MANIFEST).is_symlink():
            write_topic_outputs(args.input, args.output_dir, outputs, args.overwrite)
            print('Owned roadmap outputs written.')
            return 0
        preflight_outputs(args.input, args.output_dir, args.overwrite)
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

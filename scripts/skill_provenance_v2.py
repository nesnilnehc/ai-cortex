"""Strict, local-only provenance records and maintainer review packets.

Schema 1 remains with the migration reader until all live records are reviewed.
This module never attests authorship or retrieves external source material.
"""
from __future__ import annotations

import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

CATEGORIES = {'native', 'third_party_original', 'third_party_adapted'}
DIGEST = re.compile(r'[0-9a-f]{64}')
REVISION = re.compile(r'[0-9a-f]{40}')


class ProvenanceError(ValueError):
    """Actionable validation failure without leaking evidence contents."""

    def __init__(self, message, *, code='INVALID_RECORD', skill='', field='', next_action='Correct the field and review the evidence again.'):
        self.code, self.skill, self.field = code, skill, field
        self.message, self.next_action = message, next_action
        location = '.'.join(x for x in (skill, field) if x)
        super().__init__(f'{code}{": " + location if location else ""}: {message} Next: {next_action}')


def run_git(command, **options):
    """Bound local Git inspection; callers never retry or fetch implicitly."""
    try:
        return subprocess.run(command, timeout=30, **options)
    except subprocess.TimeoutExpired as exc:
        raise ProvenanceError('local Git inspection exceeded 30 seconds', code='GIT_TIMEOUT',
                              next_action='Check local repository availability, then retry the same read-only command.') from exc
    except OSError as exc:
        raise ProvenanceError('cannot start local Git inspection', code='GIT_UNAVAILABLE',
                              next_action='Check that Git and the repository are available, then retry.') from exc


def require(condition, message, **context):
    if not condition:
        raise ProvenanceError(message, **context)


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f'duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_pairs)
    except (OSError, ValueError) as exc:
        if isinstance(exc, ProvenanceError):
            raise
        raise ProvenanceError('cannot read valid JSON', field=str(path.name)) from exc


def text(value):
    return isinstance(value, str) and bool(value.strip())


def shape(value, required, optional=(), *, field='record'):
    require(isinstance(value, dict), 'expected an object', field=field)
    missing = sorted(set(required) - set(value))
    extra = sorted(set(value) - set(required) - set(optional))
    require(not missing and not extra, f'missing fields: {missing}; unknown fields: {extra}', field=field)


def date(value):
    require(isinstance(value, str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}', value), 'expected ISO date')
    try:
        datetime.date.fromisoformat(value)
    except ValueError as exc:
        raise ProvenanceError('invalid date') from exc


def scalar(raw):
    if raw in ('{}', '[]'):
        return {} if raw == '{}' else []
    require(bool(raw) and raw[0] not in '&*!|>{[', 'unsupported registry scalar')
    if raw.startswith('"'):
        try:
            value = json.loads(raw)
        except ValueError as exc:
            raise ProvenanceError('invalid quoted registry scalar') from exc
        require(isinstance(value, str), 'expected quoted string')
        return value
    if raw.startswith("'"):
        require(raw.endswith("'") and len(raw) >= 2, 'invalid quoted registry scalar')
        return raw[1:-1].replace("''", "'")
    require(not re.search(r'\s#', raw), 'inline registry comments are unsupported')
    require(not raw.startswith(('-', '?')) and not re.search(r':\s', raw), 'unsupported registry scalar')
    return raw


def parse_registry(source):
    """Parse the documented two-space mapping/scalar-list YAML subset only."""
    lines = []
    for number, raw in enumerate(source.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith('#'):
            continue
        require('\t' not in raw, 'tabs are not supported', field=f'line {number}')
        indent = len(raw) - len(raw.lstrip(' '))
        require(indent % 2 == 0, 'expected two-space indentation', field=f'line {number}')
        lines.append((indent, raw.strip(), number))

    def block(index, indent):
        require(index < len(lines) and lines[index][0] == indent, 'invalid registry nesting')
        is_list = lines[index][1].startswith('- ')
        result = [] if is_list else {}
        while index < len(lines) and lines[index][0] == indent:
            _, content, number = lines[index]
            if is_list:
                require(content.startswith('- '), 'mixed registry containers', field=f'line {number}')
                value = scalar(content[2:].strip())
                require(isinstance(value, str), 'only scalar list items are supported')
                result.append(value)
                index += 1
            else:
                match = re.fullmatch(r'([A-Za-z0-9_][A-Za-z0-9_-]*):(?:\s+(.*))?', content)
                require(match is not None, 'expected mapping key', field=f'line {number}')
                key, raw = match.groups()
                require(key not in result, f'duplicate registry key: {key}', field=f'line {number}')
                index += 1
                if raw is None:
                    require(index < len(lines) and lines[index][0] == indent + 2,
                            'missing nested registry value', field=f'line {number}')
                    value, index = block(index, indent + 2)
                else:
                    value = scalar(raw)
                result[key] = value
            require(index == len(lines) or lines[index][0] <= indent, 'unexpected registry indentation')
        return result, index

    require(bool(lines) and lines[0][0] == 0, 'empty or indented registry root')
    result, end = block(0, 0)
    require(end == len(lines) and isinstance(result, dict), 'invalid registry root')
    require(set(result) <= {'schema_version', 'policy', 'skills', 'references'}, 'unknown registry root field')
    for field in ('skills', 'references'):
        result.setdefault(field, {})
        require(isinstance(result[field], dict), 'expected registry mapping', field=field)
    return result


def evidence_path(root, reference):
    shape(reference, {'path'}, {'anchor'}, field='evidence')
    path = reference['path']
    require(text(path) and not any(c in path for c in '\\%?#\x00\n\r')
            and not path.startswith('/') and all(p not in ('', '.', '..') for p in path.split('/')),
            'invalid evidence path')
    base = root.resolve()
    candidate = base
    for part in PurePosixPath(path).parts:
        candidate /= part
        require(not candidate.is_symlink(), 'symlink evidence is not accepted')
    require(candidate.resolve().is_relative_to(base) and candidate.is_file(), 'missing evidence file')
    if 'anchor' in reference:
        anchor = reference['anchor']
        require(text(anchor), 'invalid evidence anchor')
        try:
            content = candidate.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            raise ProvenanceError('evidence anchor requires readable text') from exc
        headings = re.findall(r'^#{1,6}\s+(.+?)\s*#*$', content, re.M)
        anchors = {re.sub(r'[^\w\- ]', '', h.lower()).replace(' ', '-') for h in headings}
        anchors.update(re.findall(r'\bid=["\']([^"\']+)["\']', content))
        # Registry mappings are rendered as source, not HTML anchors. Only actual
        # Markdown headings/explicit IDs are evidence anchors in schema 2.
        require(anchor in anchors, 'missing evidence anchor')
    return candidate


def distributed_files(skill_dir):
    """Git-tracked plus nonignored intake files; outside Git, every file counts."""
    require(skill_dir.is_dir() and not skill_dir.is_symlink(), 'missing Skill directory')
    probe = run_git(['git', '-C', str(skill_dir), 'rev-parse', '--is-inside-work-tree'], capture_output=True)
    if probe.returncode == 0 and probe.stdout.strip() == b'true':
        process = run_git(['git', '-C', str(skill_dir), 'ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', '.'], capture_output=True)
        require(process.returncode == 0, 'cannot read Git distribution inventory')
        try:
            names = process.stdout.decode('utf-8').split('\0')
        except UnicodeError as exc:
            raise ProvenanceError('distributed paths must be UTF-8') from exc
        paths = []
        for name in sorted(set(n for n in names if n)):
            require(not name.startswith('/') and not any(p in ('', '.', '..') for p in name.split('/')), 'invalid Git distribution path')
            path = skill_dir / name
            if path.exists() or path.is_symlink():
                paths.append(path)
        return paths
    require(not any((parent / '.git').exists() for parent in [skill_dir, *skill_dir.parents]), 'cannot establish Git distribution scope')
    return sorted(skill_dir.rglob('*'))


def link_inventory(skill_dir, paths=None):
    """Keep contained file aliases explicit; never dereference an external link."""
    base = skill_dir.resolve()
    require(skill_dir.is_dir() and not skill_dir.is_symlink(), 'missing Skill directory')
    paths = distributed_files(skill_dir) if paths is None else paths
    names = {path.relative_to(skill_dir).as_posix() for path in paths}
    links = {}
    for path in paths:
        require(not any(parent.is_symlink() for parent in path.parents if parent.is_relative_to(skill_dir)), 'distributed file has a symlink parent')
        if not path.is_symlink():
            continue
        target = path.readlink()
        require(not target.is_absolute(), 'absolute distributed link is not accepted')
        destination = path.parent / target
        require(destination.resolve().is_relative_to(base) and destination.is_file(), 'distributed link leaves Skill or has no file target')
        require(destination.resolve().relative_to(base).as_posix() in names, 'distributed link target is not in distribution')
        require(not destination.is_symlink() and not any(p.is_symlink() for p in destination.parents if p.is_relative_to(base)), 'distributed link chains are not accepted')
        links[path.relative_to(skill_dir).as_posix()] = target.as_posix()
    return links


def inventory(skill_dir):
    paths = distributed_files(skill_dir)
    links = link_inventory(skill_dir, paths)
    result = {}
    for path in paths:
        relative = path.relative_to(skill_dir).as_posix()
        if relative in links:
            result[relative] = hashlib.sha256(links[relative].encode('utf-8')).hexdigest()
        elif path.is_file():
            result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    require('SKILL.md' in result and 'SKILL.md' not in links, 'missing or linked SKILL.md')
    return result


def resolved_sources(record, registry):
    sources = record.get('sources', [])
    require(isinstance(sources, list), 'sources must be an array')
    result = {}
    for source in sources:
        shape(source, {'id', 'role'}, {'adaptation'}, field='sources')
        identifier = source['id']
        require(text(identifier) and identifier not in result, 'duplicate or invalid source ID')
        require(isinstance(source['role'], str) and source['role'] in {'creative_reference', 'tool_lookup', 'copied_upstream'}, 'unknown source role')
        namespace, separator, key = identifier.partition(':')
        require(separator and namespace in ('skill', 'reference') and bool(key), 'invalid source ID')
        group = 'skills' if namespace == 'skill' else 'references'
        require(key in registry.get(group, {}), 'unresolved source ID', field=identifier)
        result[identifier] = registry[group][key]
    return result


def subject_digest(name, record, registry):
    """Hash only the review subject, excluding the human decision and its proof."""
    confirmation = {r['path'] for r in record.get('decision', {}).get('evidence', [])}
    # A packet can be prepared before its decision exists. Evidence files not in
    # reviewed_evidence belong to the decision, and therefore stay outside scope.
    confirmation |= {r['path'] for r in record.get('evidence', []) if r['path'] not in record.get('reviewed_evidence', {})}
    body = {key: record[key] for key in ('classification', 'version', 'reviewed_files', 'reviewed_evidence', 'creation', 'upstream_ref', 'upstream_files', 'reviewed_links') if key in record}
    body['skill'] = name
    body['sources'] = sorted(record.get('sources', []), key=lambda x: (x['id'], x['role']))
    body['resolved_sources'] = resolved_sources(record, registry)
    body['evidence'] = sorted([r for r in record.get('evidence', []) if r['path'] not in confirmation], key=lambda x: (x['path'], x.get('anchor', '')))
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')).hexdigest()


def public_https_url(value):
    from urllib.parse import urlsplit
    if not text(value) or re.search(r'[\s<>\\]', value):
        return False
    try:
        url = urlsplit(value)
        return url.scheme == 'https' and bool(url.hostname) and url.username is None and url.password is None
    except ValueError:
        return False


def validate_copy_source(root, name, version, entry):
    shape(entry, {'local_path', 'local_version', 'origin', 'upstream', 'license', 'notice', 'update_policy', 'modifications'}, field='copied source')
    require(entry['local_path'] == f'skills/{name}' and entry['local_version'] == version, 'source local identity/version differs')
    require(entry['origin'] == 'vendored-derived' and text(entry['license']), 'missing source license/origin')
    require(isinstance(entry['update_policy'], str) and entry['update_policy'] in {'reviewed-merge', 'reviewed-port'}, 'unsupported source update policy')
    require(isinstance(entry['modifications'], list) and all(text(change) for change in entry['modifications']), 'invalid source modifications')
    upstream = entry['upstream']
    shape(upstream, {'repository', 'path', 'ref', 'tree', 'skill_digest'}, field='upstream')
    require(public_https_url(upstream['repository']) and upstream['repository'].endswith('.git'), 'invalid public upstream repository URL')
    path = upstream['path']
    require(text(path) and not path.startswith('/') and not any(part in ('', '.', '..') for part in path.split('/')) and '\\' not in path, 'invalid upstream path')
    require(isinstance(upstream['ref'], str) and REVISION.fullmatch(upstream['ref']), 'invalid upstream revision')
    require(isinstance(upstream['tree'], str) and re.fullmatch(r'(sha1:[a-f0-9]{40}|sha256:[a-f0-9]{64})', upstream['tree']), 'invalid upstream tree digest')
    require(isinstance(upstream['skill_digest'], str) and re.fullmatch(r'sha256:[a-f0-9]{64}', upstream['skill_digest']), 'invalid upstream Skill digest')
    evidence_path(root, {'path': entry['notice']})


def _validate_record(root, name, record, registry):
    root = root.resolve()
    shape(record, {'classification', 'version', 'reviewed_files', 'reviewed_evidence', 'sources', 'evidence', 'decision'},
          {'creation', 'upstream_ref', 'upstream_files', 'reviewed_links'})
    kind = record['classification']
    require(isinstance(kind, str) and kind in CATEGORIES, 'unknown classification', skill=name)
    require(text(record['version']), 'missing version', skill=name)
    actual = inventory(root / 'skills' / name)
    links = link_inventory(root / 'skills' / name)
    require(record.get('reviewed_links', {}) == links, 'reviewed link inventory does not match', skill=name)
    require(kind != 'third_party_original' or not links, 'unchanged classification does not accept symlink distributions')
    require(record['reviewed_files'] == actual, 'reviewed file inventory does not match', skill=name)
    skill_text = (root / 'skills' / name / 'SKILL.md').read_text(encoding='utf-8')
    frontmatter = skill_text.split('---', 2)
    require(len(frontmatter) == 3 and frontmatter[0] == '', 'invalid Skill frontmatter')
    match = re.search(r'^version:\s*["\']?([^\s"\']+)["\']?\s*$', frontmatter[1], re.M)
    require(match is not None and match[1] == record['version'], 'Skill version does not match')
    decision = record['decision']
    shape(decision, {'maintainer', 'confirmed_at', 'action', 'classification', 'rationale', 'evidence', 'subject_digest'}, field='decision')
    require(text(decision['maintainer']) and text(decision['rationale']), 'incomplete maintainer confirmation')
    date(decision['confirmed_at'])
    require(isinstance(decision['action'], str) and decision['action'] in {'confirmed', 'corrected'} and decision['classification'] == kind, 'inconsistent confirmation decision')
    require(isinstance(decision['subject_digest'], str) and DIGEST.fullmatch(decision['subject_digest']), 'invalid confirmation digest')
    require(isinstance(record['evidence'], list) and bool(record['evidence']), 'missing public evidence')
    require(isinstance(decision['evidence'], list) and bool(decision['evidence']), 'missing confirmation evidence')
    confirmation_paths = set()
    for reference in decision['evidence']:
        path = evidence_path(root, reference)
        confirmation_paths.add(reference['path'])
        require(reference in record['evidence'], 'confirmation evidence not publicly reachable')
        require(read_json(path) == decision, 'confirmation evidence differs from decision')
    hashes = record['reviewed_evidence']
    require(isinstance(hashes, dict), 'invalid reviewed evidence map')
    require(not confirmation_paths.intersection(hashes), 'confirmation cannot hash itself')
    expected = set()
    for reference in record['evidence']:
        evidence_path(root, reference)
        if reference['path'] not in confirmation_paths:
            expected.add(reference['path'])
    sources = resolved_sources(record, registry)
    if name in registry.get('skills', {}):
        require(f'skill:{name}' in sources, 'registered upstream copy needs its copied-source evidence')
    if kind == 'native':
        require(name not in registry.get('skills', {}), 'native conflicts with copied source registry')
        creation = record.get('creation')
        require(isinstance(creation, dict), 'missing creation evidence')
        if creation.get('kind') == 'requirement':
            shape(creation, {'kind', 'evidence'})
            evidence_path(root, creation['evidence'])
            expected.add(creation['evidence']['path'])
        elif creation.get('kind') == 'commit':
            shape(creation, {'kind', 'revision'})
            require(isinstance(creation['revision'], str) and REVISION.fullmatch(creation['revision']), 'invalid creation revision')
            proc = run_git(['git', '-C', str(root), 'diff-tree', '--root', '--no-commit-id', '--name-only', '-r', creation['revision'], '--', f'skills/{name}'], capture_output=True, text=True)
            require(proc.returncode == 0 and bool(proc.stdout.strip()), 'creation commit does not touch Skill')
        else:
            raise ProvenanceError('invalid creation kind')
        require(all(s['role'] == 'tool_lookup' for s in record['sources']), 'native has creative source reference')
    else:
        require('creation' not in record, 'external classification must omit creation')
    creative = []
    copied = []
    for source in record['sources']:
        entry = sources[source['id']]
        require(isinstance(entry, dict), 'invalid source entry')
        if source['id'].startswith('reference:'):
            shape(entry, {'url', 'title', 'accessed_at', 'kind', 'evidence'})
            require(public_https_url(entry['url']) and text(entry['title']), 'invalid reference URL/title')
            date(entry['accessed_at'])
            require(isinstance(entry['kind'], str) and entry['kind'] in {'article', 'method', 'workflow', 'tool_documentation', 'skill'}, 'invalid reference kind')
            require(source['role'] != 'copied_upstream', 'copied source requires upstream registry')
            if source['role'] == 'tool_lookup':
                require(entry['kind'] == 'tool_documentation', 'tool lookup requires tool documentation evidence')
            evidence_path(root, entry['evidence'])
            expected.add(entry['evidence']['path'])
        else:
            require(source['role'] == 'copied_upstream', 'Skill registry source requires copied_upstream role')
            require(source['id'] == f'skill:{name}', 'copied source must identify this local Skill')
            validate_copy_source(root, name, record['version'], entry)
            notice = {'path': entry.get('notice')}
            evidence_path(root, notice)
            expected.add(notice['path'])
            require(isinstance(entry.get('upstream'), dict), 'missing upstream source')
            require(isinstance(entry['upstream'].get('ref'), str) and REVISION.fullmatch(entry['upstream']['ref']), 'invalid upstream revision')
            copied.append((source, entry))
        if source['role'] == 'creative_reference':
            creative.append(source)
            require(text(source.get('adaptation')), 'missing adaptation description')
    if kind == 'third_party_original':
        require(len(copied) == 1 and not creative, 'unchanged claim requires exactly one copied source and no creative adaptation')
        entry = copied[0][1]
        require(entry.get('modifications') == [], 'unchanged claim has local modifications')
        require(record.get('upstream_ref') == entry['upstream']['ref'], 'upstream revision conflicts')
        require(record.get('upstream_files') == actual, 'upstream files do not match distributed files')
        require(entry['upstream'].get('skill_digest') == 'sha256:' + actual['SKILL.md'], 'upstream Skill digest conflicts')
    elif kind == 'third_party_adapted':
        require(bool(creative or copied), 'adapted claim has no creative or copied source')
        require('upstream_ref' not in record and 'upstream_files' not in record, 'adapted record has unchanged-only fields')
        for source, entry in copied:
            changes = entry.get('modifications')
            require(isinstance(changes, list) and bool(changes) and all(text(v) for v in changes), 'adapted copy needs modifications')
            require(text(source.get('adaptation')), 'missing copied adaptation description')
    else:
        require('upstream_ref' not in record and 'upstream_files' not in record, 'native has upstream fields')
    require(set(hashes) == expected, 'reviewed evidence coverage differs from references')
    for path, digest in hashes.items():
        actual_path = evidence_path(root, {'path': path})
        require(isinstance(digest, str) and DIGEST.fullmatch(digest) and hashlib.sha256(actual_path.read_bytes()).hexdigest() == digest, 'reviewed evidence bytes changed', field=path)
    require(decision['subject_digest'] == subject_digest(name, record, registry), 'confirmation subject digest changed', skill=name,
            next_action='Prepare a fresh packet and obtain explicit maintainer confirmation.')
    return dict(record)


def validate_record(root, name, record, registry):
    """Keep the affected Skill visible when a nested validator rejects a field."""
    try:
        return _validate_record(root, name, record, registry)
    except ProvenanceError as exc:
        if exc.skill:
            raise
        raise ProvenanceError(exc.message, code=exc.code, skill=name,
                              field=exc.field, next_action=exc.next_action) from exc


def load(root, skills_dir):
    doc = read_json(skills_dir / 'PROVENANCE.json')
    shape(doc, {'schema_version', 'skills'})
    require(type(doc['schema_version']) is int and doc['schema_version'] == 2, 'expected provenance schema 2')
    require(isinstance(doc['skills'], dict), 'invalid Skill records')
    names = {p.name for p in skills_dir.iterdir() if p.is_dir() and (p / 'SKILL.md').is_file()}
    require(set(doc['skills']) == names, 'catalogue coverage differs', code='INCOMPLETE_CATALOGUE',
            next_action='Review every missing Skill; remove only records for nonexistent Skills.')
    try:
        registry = parse_registry((skills_dir / 'SOURCES.yaml').read_text(encoding='utf-8'))
    except OSError as exc:
        raise ProvenanceError('cannot read source registry') from exc
    require(set(registry['skills']) <= names, 'source registry contains nonexistent Skill')
    return {name: validate_record(root, name, rec, registry) for name, rec in sorted(doc['skills'].items())}


def review_packet(root, name, record, registry):
    """Prepare a recommendation and exact gaps; this function never records approval."""
    require(isinstance(record, dict), 'review candidate must be an object', skill=name)
    files = inventory(root / 'skills' / name)
    kind = record.get('classification')
    missing = []
    try:
        validate_record(root, name, record, registry)
    except ProvenanceError as exc:
        missing.append(str(exc))
    recommendation = kind if isinstance(kind, str) and kind in CATEGORIES else 'Needs source investigation before recommending a category'
    rationale = 'Candidate classification must be checked against actual sources and distributed files.'
    if name in registry.get('skills', {}):
        recommendation = 'third_party_adapted' if registry['skills'][name].get('modifications') else 'Check pinned upstream file identity for third_party_original'
        rationale = 'Recorded upstream source and local modifications determine copied-source classification.'
    elif kind == 'native':
        rationale = 'Creation evidence supports local construction; only the maintainer can confirm absence of creative external reference.'
    digest = 'Unavailable until the candidate subject is complete.'
    if {'classification', 'version', 'reviewed_files', 'reviewed_evidence', 'evidence', 'sources'} <= set(record) and isinstance(kind, str) and kind in CATEGORIES:
        digest = subject_digest(name, record, registry)
    return '\n'.join([
        f'# Provenance review: {name}', f'\nVersion: {record.get("version", "not recorded")}',
        '\n## Recommendation', recommendation, rationale,
        '\n## Creation records', json.dumps(record.get('creation'), ensure_ascii=False),
        '\n## Sources and their role', json.dumps(record.get('sources', []), ensure_ascii=False, indent=2),
        '\n## Comparison and local modifications', json.dumps(registry.get('skills', {}).get(name, {}), ensure_ascii=False, indent=2),
        '\n## Current distributed files', json.dumps(files, sort_keys=True, indent=2),
        '\n## Contained link targets', json.dumps(link_inventory(root / 'skills' / name), sort_keys=True, indent=2),
        '\n## Subject digest', digest,
        '\n## Missing facts', *(missing or ['None found by structural validation; inspect the evidence itself.']),
        '\n## Maintainer decision requested',
        'Confirm or correct the recommendation for this content. State whether external material informed method, workflow or expression; identify tool-documentation-only lookup separately.',
        'Record maintainer identity, date, category, rationale, public evidence and the reviewed subject digest. An unanswered packet is not a confirmation.',
    ]) + '\n'


def validate_coverage(root, records):
    """Check real assembly inputs, not just matching record counts."""
    names = {p.name for p in (root / 'skills').iterdir() if p.is_dir() and (p / 'SKILL.md').is_file()}
    web = root / 'website' / 'explore'
    metadata = read_json(web / 'skill-metadata.json')
    require(isinstance(metadata, dict) and isinstance(metadata.get('skills'), dict), 'invalid website metadata')
    require(names == set(records) == set(metadata['skills']), 'catalogue coverage differs between repository, records and website', code='INCOMPLETE_CATALOGUE')
    groups = metadata.get('groupOrder')
    require(isinstance(groups, list) and all(text(g) for g in groups), 'invalid website owner groups')
    for name, skill in metadata['skills'].items():
        require(isinstance(skill, dict) and skill.get('id') == name and skill.get('owner') in groups, 'invalid website Skill owner', skill=name)
    for language in ('en', 'zh'):
        locale = read_json(web / 'locales' / f'{language}.json')
        require(isinstance(locale, dict) and isinstance(locale.get('skills'), dict), 'invalid locale Skill map')
        require(set(locale['skills']) == names, 'locale coverage differs', field=language)
        require(isinstance(locale.get('contexts'), dict), 'missing locale contexts')
        context_members = []
        for owner, context in locale['contexts'].items():
            require(isinstance(context, dict) and isinstance(context.get('skills'), list), 'invalid context members')
            for name in context['skills']:
                require(name in names and metadata['skills'][name]['owner'] == owner, 'invalid context ownership', skill=str(name))
                context_members.append(name)
        require(len(context_members) == len(set(context_members)) and set(context_members) == names, 'context coverage differs')
        lookup = locale.get('extras', {}).get('lookup')
        require(isinstance(lookup, list), 'missing search lookup groups')
        lookup_members = []
        for group in lookup:
            require(isinstance(group, dict) and isinstance(group.get('skills'), list) and all(text(v) for v in group['skills']), 'invalid search lookup group')
            lookup_members.extend(group['skills'])
        require(len(lookup_members) == len(set(lookup_members)) and set(lookup_members) == names, 'search lookup coverage differs')
        for name, detail in locale['skills'].items():
            require(isinstance(detail, dict) and all(text(detail.get(k)) for k in ('name', 'purpose', 'when', 'provide', 'use', 'result')), 'missing locale guidance', skill=name, field=language)
    classification = read_json(web / 'classification.json')
    require(isinstance(classification, dict) and isinstance(classification.get('groups'), list), 'invalid classification map')
    entries = []
    for group in classification['groups']:
        require(isinstance(group, dict) and isinstance(group.get('skillIds'), list) and all(text(i) for i in group['skillIds']), 'invalid classification group')
        entries.extend(group['skillIds'])
    require(len(entries) == len(set(entries)) and set(entries) == names, 'classification coverage differs')
    edges = read_json(web / 'skill-edges.json')
    require(isinstance(edges, list), 'invalid relationship inventory')
    for edge in edges:
        require(isinstance(edge, dict) and edge.get('from') in names and edge.get('to') in names, 'dangling relationship endpoint')
    support = read_json(web / 'support-scopes.json')
    require(isinstance(support, list), 'invalid support inventory')
    for group in support:
        require(isinstance(group, dict) and isinstance(group.get('targets'), list), 'invalid support scope')
        for target in group['targets']:
            require(isinstance(target, dict) and isinstance(target.get('sources'), list), 'invalid support target')
            for source in target['sources']:
                require(isinstance(source, dict) and text(source.get('path')), 'invalid support source')
                match = re.fullmatch(r'skills/([^/]+)/SKILL.md', source['path'])
                require(match is not None and match[1] in names, 'dangling support source')
    return True


def reviewed_input_paths(records):
    paths = {'skills/PROVENANCE.json', 'skills/SOURCES.yaml'}
    for name, rec in records.items():
        paths.update(f'skills/{name}/{p}' for p in rec['reviewed_files'])
        paths.update(rec['reviewed_evidence'])
        paths.update(r['path'] for r in rec['evidence'])
        paths.update(r['path'] for r in rec['decision']['evidence'])
    return sorted(paths)


def verify_revision(root, records, revision):
    require(isinstance(revision, str) and REVISION.fullmatch(revision), 'invalid evidence revision')
    links = {f'skills/{name}/{path}': target for name, rec in records.items() for path, target in rec.get('reviewed_links', {}).items()}
    for path in reviewed_input_paths(records):
        distributed_link = links.get(path)
        local = root / path if distributed_link is not None else evidence_path(root, {'path': path})
        local_bytes = local.readlink().as_posix().encode('utf-8') if distributed_link is not None else local.read_bytes()
        process = run_git(['git', '-C', str(root), 'show', f'{revision}:{path}'], capture_output=True)
        require(process.returncode == 0 and process.stdout == local_bytes,
                'evidence does not match committed content', code='STALE_EVIDENCE_PIN', field=path,
                next_action='Commit reviewed source inputs when authorized and pin that commit; use isolated preview for uncommitted inputs.')
    return True


def export_public(root, records, source_revision):
    """Export only public evidence links; never expose raw maintainer packets."""
    from urllib.parse import quote
    verify_revision(root, records, source_revision)
    def url(reference):
        evidence_path(root, reference)
        return ('https://github.com/nesnilnehc/ai-cortex/blob/' + source_revision + '/' + quote(reference['path'], safe='/')
                + ('#' + quote(reference['anchor'], safe='') if 'anchor' in reference else ''))
    return {'schema_version': 1, 'source_revision': source_revision,
            'skills': {name: {'classification': rec['classification'], 'evidence': [url(r) for r in rec['evidence']]}
                       for name, rec in sorted(records.items())}}


def verify_asset_revision(root):
    manifest = read_json(root / 'website/explore/source-manifest.json')
    revision = manifest.get('assetsRevision')
    require(isinstance(revision, str) and REVISION.fullmatch(revision), 'invalid asset revision')
    metadata = read_json(root / 'website/explore/skill-metadata.json')['skills']
    for name, record in metadata.items():
        path = f'skills/{name}/SKILL.md'
        require(record.get('sourcePaths') == [path] and isinstance(record.get('sourceHashes'), dict) and set(record['sourceHashes']) == {path}, 'invalid asset source map', skill=name)
        local = evidence_path(root, {'path': path}).read_bytes()
        digest = record['sourceHashes'][path]
        require(isinstance(digest, str) and DIGEST.fullmatch(digest) and hashlib.sha256(local).hexdigest() == digest, 'asset source hash is stale', skill=name)
        result = run_git(['git', '-C', str(root), 'show', f'{revision}:{path}'], capture_output=True)
        require(result.returncode == 0 and result.stdout == local, 'asset does not match committed content', code='STALE_ASSET_PIN', skill=name,
                next_action='Pin the asset source commit containing the reviewed Skill bytes when authorized.')
    return True

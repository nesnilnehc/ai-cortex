#!/usr/bin/env python3
"""Read verified skill provenance markers without network or YAML dependencies."""
from __future__ import annotations

import datetime
import hashlib
import json
import pathlib
import re


class ProvenanceError(Exception):
    """A provenance claim is invalid or cannot be checked."""


LABELS = {'native':'AI Cortex original', 'third_party_original':'Third-party original',
          'third_party_adapted':'Third-party adapted', 'unverified':'Unverified'}


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ProvenanceError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def load(root: pathlib.Path, skills_dir: pathlib.Path) -> dict[str, dict]:
    root = root.resolve()
    path = skills_dir / 'PROVENANCE.json'
    try:
        doc = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique_pairs)
    except (OSError, ValueError) as exc:
        raise ProvenanceError(f'cannot read provenance: {exc}') from exc
    if isinstance(doc, dict) and doc.get('schema_version') == 2:
        import skill_provenance_v2 as reviewed
        try:
            return reviewed.load(root, skills_dir)
        except reviewed.ProvenanceError as exc:
            raise ProvenanceError(str(exc)) from exc
    if not isinstance(doc, dict) or set(doc) != {'schema_version','skills'} or doc['schema_version'] != 1 or not isinstance(doc['skills'], dict):
        raise ProvenanceError('invalid provenance schema')
    names = {p.name for p in skills_dir.iterdir() if p.is_dir() and (p / 'SKILL.md').is_file()}
    result = {name: {'classification':'unverified'} for name in names}
    source_path = skills_dir / 'SOURCES.yaml'
    try:
        source_text = source_path.read_text(encoding='utf-8')
    except OSError as exc:
        raise ProvenanceError(f'cannot read source registry: {exc}') from exc
    registered = set(re.findall(r'^  ([a-z0-9][a-z0-9-]*):\s*$', source_text, re.M))
    # Only keys underneath skills are entries: policy keys in the current schema
    # have scalar values, so reject unsupported shapes rather than infer origin.
    if not registered.issubset(doc['skills']):
        raise ProvenanceError('source registry entries need explicit provenance records')
    for name, rec in doc['skills'].items():
        if name not in names or not isinstance(rec, dict):
            raise ProvenanceError(f'{name}: missing skill or invalid record')
        kind = rec.get('classification')
        if kind not in LABELS or kind == 'unverified':
            raise ProvenanceError(f'{name}: invalid classification')
        if (name in registered) != kind.startswith('third_party_'):
            raise ProvenanceError(f'{name}: classification conflicts with source registry')
        allowed = {'classification','evidence','reviewed_at'}
        if kind == 'third_party_original':
            allowed |= {'upstream_ref','upstream_files'}
        if set(rec) - allowed:
            raise ProvenanceError(f'{name}: unknown fields')
        evidence = rec.get('evidence')
        if not isinstance(evidence,str) or not evidence or evidence.startswith('/') or '\\' in evidence:
            raise ProvenanceError(f'{name}: invalid evidence')
        raw_path, _, anchor = evidence.partition('#')
        ev_path = (root / raw_path).resolve()
        if not ev_path.is_relative_to(root) or not ev_path.is_file():
            raise ProvenanceError(f'{name}: missing evidence')
        try: datetime.date.fromisoformat(rec['reviewed_at'])
        except (ValueError,TypeError,KeyError) as exc: raise ProvenanceError(f'{name}: missing or invalid review date') from exc
        if kind.startswith('third_party_'):
            if raw_path != 'skills/SOURCES.yaml' or anchor != name:
                raise ProvenanceError(f'{name}: third-party evidence must reference its source registry entry')
            source = ev_path.read_text(encoding='utf-8')
            match = re.search(r'^  '+re.escape(name)+r':\s*\n((?:(?:    |\s*$).*(?:\n|$))*)', source, re.M)
            if not match or not re.search(r'^    origin:\s*vendored-derived\s*$', match.group(1), re.M):
                raise ProvenanceError(f'{name}: source registry entry missing or incompatible')
            license_match = re.search(r'^    license:\s*([^\s#]+)\s*$', match.group(1), re.M)
            notice_match = re.search(r'^    notice:\s*([^\s#]+)\s*$', match.group(1), re.M)
            if not license_match or not notice_match:
                raise ProvenanceError(f'{name}: source registry lacks license or notice')
            notice_path = (root / notice_match.group(1)).resolve()
            if not notice_path.is_relative_to(root) or not notice_path.is_file():
                raise ProvenanceError(f'{name}: source license notice missing')
            if kind == 'third_party_adapted' and not re.search(r'^    modifications:\s*\n      -\s*\S', match.group(1), re.M):
                raise ProvenanceError(f'{name}: adapted copy needs described modifications')
        if kind == 'third_party_original':
            if not re.search(r'^    modifications:\s*\[\]\s*$', match.group(1), re.M):
                raise ProvenanceError(f'{name}: unchanged copy must have no local modifications')
            upstream_ref = rec.get('upstream_ref')
            files = rec.get('upstream_files')
            if not isinstance(upstream_ref,str) or not re.fullmatch(r'[0-9a-f]{40}',upstream_ref) or not isinstance(files,dict) or not files:
                raise ProvenanceError(f'{name}: original requires an upstream revision and file hashes')
            folder = skills_dir / name
            actual = {}
            for f in folder.rglob('*'):
                if f.is_symlink(): raise ProvenanceError(f'{name}: original comparison does not accept symlinks')
                if f.is_file(): actual[f.relative_to(folder).as_posix()] = hashlib.sha256(f.read_bytes()).hexdigest()
            if files != actual:
                raise ProvenanceError(f'{name}: distributed files do not match upstream file hashes')
            if not re.search(r'^      ref:\s*'+upstream_ref+r'\s*$', match.group(1), re.M):
                raise ProvenanceError(f'{name}: upstream revision does not match registry')
            if not re.search(r'^      skill_digest:\s*sha256:'+files.get('SKILL.md','')+r'\s*$', match.group(1), re.M):
                raise ProvenanceError(f'{name}: SKILL.md hash does not match registry')
        result[name] = dict(rec)
    return result


def main(argv):
    """Read-only maintenance entry; schema-1 records are candidates, not decisions."""
    import sys
    import subprocess
    import skill_provenance_v2 as reviewed

    if len(argv) != 2 or argv[0] != '--review':
        print('usage: skill-provenance.py --review <skill>', file=sys.stderr)
        return 2
    name = argv[1]
    root = pathlib.Path(__file__).resolve().parents[1]
    try:
        reviewed.require(bool(re.fullmatch(r'[a-z0-9][a-z0-9-]*', name)), 'invalid Skill name')
        folder = root / 'skills' / name
        files = reviewed.inventory(folder)
        registry = reviewed.parse_registry((root / 'skills/SOURCES.yaml').read_text(encoding='utf-8'))
        document = reviewed.read_json(root / 'skills/PROVENANCE.json')
        reviewed.require(isinstance(document, dict), 'provenance manifest must be an object')
        if document.get('schema_version') == 2:
            reviewed.require(isinstance(document.get('skills'), dict), 'Skill records must be an object')
            candidate = document.get('skills', {}).get(name, {})
        else:
            # Migration candidates deliberately have no decision or invented
            # identity. A source registry proves derivation, not confirmation.
            content = (folder / 'SKILL.md').read_text(encoding='utf-8')
            match = re.search(r'^version:\s*(.+?)\s*$', content, re.M)
            candidate = {'version': match[1] if match else '', 'reviewed_files': files,
                         'reviewed_evidence': {}, 'evidence': [], 'sources': []}
            links = reviewed.link_inventory(folder)
            if links:
                candidate['reviewed_links'] = links
            if name in registry['skills']:
                source = registry['skills'][name]
                candidate['classification'] = 'third_party_adapted' if source.get('modifications') else 'third_party_original'
                candidate['sources'] = [{'id': f'skill:{name}', 'role': 'copied_upstream',
                                         'adaptation': '; '.join(source.get('modifications', []))}]
            history = reviewed.run_git(['git', '-C', str(root), 'log', '--reverse', '--format=%H', '--', f'skills/{name}/SKILL.md'], capture_output=True, text=True, check=False)
            commits = history.stdout.splitlines()
            if commits and name not in registry['skills']:
                candidate['creation'] = {'kind': 'commit', 'revision': commits[0]}
        print(reviewed.review_packet(root, name, candidate, registry))
        return 0
    except (reviewed.ProvenanceError, OSError, UnicodeError) as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    import sys
    raise SystemExit(main(sys.argv[1:]))

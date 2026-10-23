"""Test-owned reference consumers, not runtime configuration or approval adapters.

The file loader supports JSON-compatible YAML and a fixture JSON fence in CLAUDE.
Full YAML parsing and arbitrary Markdown interpretation are deliberately excluded.
"""
from __future__ import annotations

import copy
from datetime import date
import fnmatch
import json
import re


def registry(root):
    profiles = set()
    parameters = {}
    rule_ids = set()
    for path in (root / 'rules').glob('*-quality.md'):
        text = path.read_text()
        if 'model: RULE_MODEL_V1' not in text:
            continue
        name = re.search(r'^name: (.+)$', text, re.M).group(1)
        version = re.search(r'^version: (.+)$', text, re.M).group(1)
        profiles.update(re.findall(r'^\| `([^`]+)` \| profile \|', text, re.M))
        parameters.update(dict(re.findall(
            r'^\| `([^`]+)` \| parameter \| (derived|baseline|declared) \|', text, re.M)))
        rule_ids.update(name+'@'+version+'/'+item for item in re.findall(r'^### ([A-Z]+-\d+) —', text, re.M))
    model = (root / 'specs/rule-modeling.md').read_text()
    return {'profiles':sorted(profiles), 'parameters':parameters, 'rule_ids':sorted(rule_ids),
            'waiver_fields':re.findall(r'^\s+(?:- )?([a-z_]+):', model.split('### 5.5', 1)[1].split('### 5.6', 1)[0], re.M),
            'governance_required':re.findall(r'^\| `([^`]+)` \| yes \|', model.split('### 5.3', 1)[1].split('### 5.4', 1)[0], re.M)}


def load_project(root, inferred):
    sources = []
    yaml = root / '.ai-cortex/config.yaml'
    if yaml.exists():
        sources.append((str(yaml), json.loads(yaml.read_text())))
    claude = root / 'CLAUDE.md'
    if claude.exists():
        blocks = re.findall(r'```json\s*\n(.*?)\n```', claude.read_text(), re.S)
        if len(blocks) != 1:
            raise ValueError('Reference loader requires one fixture JSON configuration fence')
        sources.append((str(claude), json.loads(blocks[0])))
    configured = {}
    for path, values in sources:
        if not isinstance(values, dict):
            raise ValueError('Configuration must be an object: '+path)
        for key, value in values.items():
            if key in configured and configured[key] != value:
                raise ValueError('Conflicting configuration sources for '+key)
            configured[key] = copy.deepcopy(value)
    def overlay(fallback, explicit):
        merged = copy.deepcopy(fallback)
        for key, value in explicit.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = overlay(merged[key], value)
            else:
                merged[key] = copy.deepcopy(value)
        return merged
    return overlay(inferred, configured)


def validate_config(config, catalog):
    governance = config.get('governance', {})
    if not isinstance(governance, dict):
        raise ValueError('governance must be an object')
    if 'governance' in config and any(key not in governance for key in catalog['governance_required']):
        raise ValueError('governance.profiles is required')
    profiles = governance.get('profiles', [])
    if not isinstance(profiles, list) or any(profile not in catalog['profiles'] for profile in profiles):
        raise ValueError('Unknown or malformed profile')
    def visit(prefix, value):
        if prefix in catalog['parameters']:
            return
        if not isinstance(value, dict) or not value:
            raise ValueError('Unknown parameter: '+prefix)
        for key, child in value.items():
            visit(prefix+'.'+key if prefix else key, child)
    parameters = governance.get('parameters', {})
    if not isinstance(parameters, dict):
        raise ValueError('parameters must be an object')
    for key, value in parameters.items():
        visit(key, value)


def parameter(name, catalog, configured, facts, baseline):
    provenance = catalog['parameters'].get(name)
    if provenance is None:
        raise ValueError('Unknown parameter: '+name)
    if provenance == 'baseline' and name in baseline:
        state, value = 'baseline', baseline[name]
    elif name in configured and configured[name] is not None:
        state, value = provenance, configured[name]
    elif provenance == 'derived' and name in facts:
        state, value = 'derived', facts[name]
    elif provenance == 'baseline' and name in facts:
        state, value = 'baselined', facts[name]
    else:
        state, value = 'evidence_limited', None
    # Resolution is not a Rule pass; no input snapshot or configuration is mutated.
    return {'state':state, 'value':copy.deepcopy(value)}


def waiver_result(waiver, catalog, population, requested, approvers, today, pinned=()):
    required = catalog['waiver_fields']
    rejected = {'state':'finding','waiver_id':waiver.get('id')}
    if any(not waiver.get(key) for key in required):
        return rejected
    if any(not isinstance(waiver[key], str) or not waiver[key].strip()
           for key in required if key != 'compensating_controls'):
        return rejected
    controls = waiver['compensating_controls']
    if not isinstance(controls, list) or any(not isinstance(c, str) or not c.strip() for c in controls):
        return rejected
    try:
        created, expires, clock = (date.fromisoformat(value) for value in
                                   [waiver['created_at'], waiver['expires_at'], today])
    except ValueError:
        return rejected
    if expires <= created or expires <= clock or waiver['approved_by'] not in approvers:
        return rejected
    if waiver['rule_id'] not in set(catalog['rule_ids']) | set(pinned):
        return rejected
    # Compare explicit fixture populations, not arbitrary glob-language containment.
    covered = {path for path in population if fnmatch.fnmatchcase(path, waiver['scope'])}
    if not set(requested) or not set(requested) <= covered or not covered < set(population):
        return rejected
    return {'state':'waived','waiver_id':waiver['id']}


def version_tuple(value):
    if not isinstance(value, str) or not re.fullmatch(r'(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)', value):
        raise ValueError('Expected a canonical stable version')
    return tuple(map(int, value.split('.')))


def entry(name, version, migration, available):
    announced = version_tuple(migration['deprecated_in'])
    removal = version_tuple(migration['remove_in'])
    current = version_tuple(version)
    if announced[1] == 0 or announced[2] != 0 or removal[0] <= announced[0] or removal[1:] != (0, 0):
        raise ValueError('Deprecate in a MINOR; remove in a later MAJOR')
    if not migration.get('example') or migration['old'] == migration['replacement']:
        raise ValueError('Missing replacement/migration example')
    old, replacement = migration['old'], migration['replacement']
    if current >= removal:
        if not migration.get('old_consumer_verified') or not migration.get('migration_verified'):
            raise ValueError('Removal requires old-consumer and migration evidence')
        if name == old:
            raise ValueError('Removed entry; migrate to '+replacement)
    elif current >= announced and old not in available:
        raise ValueError('Retain the old entry or compatible reader through this major')
    if name not in available or name not in [old, replacement] or replacement not in available:
        raise ValueError('Unknown/unavailable entry')
    return replacement if name == old and current >= announced else name


def check_compatibility(baseline, current):
    if not set(baseline['profiles']) <= set(current['profiles']):
        raise ValueError('Protected profile removed')
    for name, provenance in baseline['parameters'].items():
        if current['parameters'].get(name) != provenance:
            raise ValueError('Protected parameter/provenance changed: '+name)
    for key in ['waiver_fields', 'governance_required']:
        if baseline[key] != current[key]:
            raise ValueError('Required field contract changed: '+key)

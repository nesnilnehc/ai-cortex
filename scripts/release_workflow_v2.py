"""Pure admission helpers for the staged-release examples; no I/O or provider calls."""

_STAGES = {'select': 0, 'upload': 1, 'complete': 2}


def admit_schema(version):
    """The model supports only the exact schema it was written for."""
    return version == '2.0.0'


def delivery_verified(candidate, delivered, relationship, check):
    return all(isinstance(value, str) and value.strip() for value in (candidate, delivered)) and relationship == 'verified' and check == 'passed'


def decide(candidate, target, stage, checks, waivers, authorized, identity_verified, scope='release'):
    """Return whether this specific stage is admitted from supplied evidence."""
    if not authorized or not identity_verified or stage not in _STAGES:
        return False
    selected = [item for item in checks if item.get('candidate') == candidate and item.get('target') == target]
    if checks and not selected:
        return False
    for check in selected:
        due = _STAGES.get(check.get('stage'))
        if due is None or type(check.get('required')) is not bool or check.get('status') not in {'pending', 'passed', 'failed', 'unexecuted'}:
            return False
        if not check.get('required') or due > _STAGES[stage]:
            continue
        if check.get('status') == 'passed' and isinstance(check.get('evidence'), str) and check['evidence'].strip():
            continue
        if check.get('status') not in {'failed', 'unexecuted'} or check.get('waivable') is not True or check.get('origin') != 'internal':
            return False
        match = next((w for w in waivers if all(w.get(key) == value for key, value in (
            ('candidate', candidate), ('target', target), ('check', check.get('name')), ('stage', check.get('stage')), ('scope', scope)))
            and all(isinstance(w.get(key), str) and w[key].strip() for key in ('approver', 'scope', 'rationale', 'evidence'))), None)
        if match is None:
            return False
    return True


def aggregate(targets):
    return bool(targets) and any(t.get('status') == 'complete' for t in targets) and all(
        not t.get('required') or t.get('status') == 'complete' for t in targets)


def retry_action(observed, authorized):
    if observed == 'complete':
        return 'reuse'
    return 'execute' if observed == 'absent' and authorized else 'stop'

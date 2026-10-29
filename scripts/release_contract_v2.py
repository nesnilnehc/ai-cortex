"""Bounded offline reference reader for Spec 5.8; not a provider or Skill runtime.

Stages and policy inputs belong to these fixtures, not a mandatory project format.
No command, network access or mutation is performed by this module.
"""

STAGES = {'select': 0, 'upload': 1, 'complete': 2}


def text(value):
    return isinstance(value, str) and bool(value.strip())


def fields(record, names):
    return isinstance(record, dict) and all(name in record for name in names.split())


def indexed(records):
    if not isinstance(records, list) or any(not fields(row, 'id') or not text(row['id']) for row in records):
        raise ValueError('missing collection or identity')
    result = {row['id']: row for row in records}
    if len(result) != len(records):
        raise ValueError('duplicate identity')
    return result


def validate(package):
    """Validate the fixture-supported package shape and referential integrity."""
    try:
        if not fields(package, 'schema_version project release_id release_version change_items candidates targets checks exceptions attempts communication'):
            return False
        if package['schema_version'] != '2.0.0' or not all(text(package[k]) for k in ('project', 'release_id')):
            return False
        version = package['release_version']
        if not fields(version, 'value scheme source') or any(v is not None and not text(v) for v in version.values()):
            return False
        if not isinstance(package['change_items'], list) or not isinstance(package['communication'], list):
            return False
        candidates, targets, checks = (indexed(package[key]) for key in ('candidates', 'targets', 'checks'))
        artifacts = {}
        for candidate in candidates.values():
            if not fields(candidate, 'source_revision build_identity artifacts'):
                return False
            for key in ('source_revision', 'build_identity'):
                if candidate[key] is not None and not text(candidate[key]):
                    return False
            artifacts[candidate['id']] = indexed(candidate['artifacts'])
            for artifact in candidate['artifacts']:
                if not fields(artifact, 'location identity evidence'):
                    return False
                if artifact['identity'] is not None and not all(text(artifact[k]) for k in ('identity', 'location', 'evidence')):
                    return False
        for target in targets.values():
            if not fields(target, 'required candidate_id artifact_ids status delivered_artifacts evidence'):
                return False
            if type(target['required']) is not bool or target['status'] not in {'pending', 'complete', 'failed', 'unknown'}:
                return False
            if target['candidate_id'] is not None and target['candidate_id'] not in candidates:
                return False
            if not isinstance(target['artifact_ids'], list) or len(set(target['artifact_ids'])) != len(target['artifact_ids']):
                return False
            owned = artifacts.get(target['candidate_id'], {})
            if any(key not in owned for key in target['artifact_ids']) or not isinstance(target['delivered_artifacts'], list):
                return False
            for delivered in target['delivered_artifacts']:
                if not fields(delivered, 'candidate_artifact_id identity relationship evidence'):
                    return False
                key = delivered['candidate_artifact_id']
                if key not in target['artifact_ids'] or not all(text(delivered[k]) for k in ('identity', 'evidence')):
                    return False
                if delivered['relationship'] not in {'unchanged', 'transformed'}:
                    return False
                if delivered['relationship'] == 'unchanged' and delivered['identity'] != owned[key]['identity']:
                    return False
            if target['status'] == 'complete':
                if not target['artifact_ids'] or not text(target['evidence']):
                    return False
                if {d['candidate_artifact_id'] for d in target['delivered_artifacts']} != set(target['artifact_ids']):
                    return False
        for check in checks.values():
            if not fields(check, 'candidate_id target_id stage required origin status evidence'):
                return False
            if check['candidate_id'] not in candidates or check['target_id'] not in targets:
                return False
            if check['stage'] not in STAGES or check['origin'] not in {'internal', 'provider'} or type(check['required']) is not bool:
                return False
            if check['status'] not in {'pending', 'passed', 'failed', 'unexecuted'}:
                return False
            if check['status'] == 'passed' and not text(check['evidence']):
                return False
        if not isinstance(package['exceptions'], list):
            return False
        for exception in package['exceptions']:
            if not fields(exception, 'candidate_id target_id check_id scope approver rationale evidence') or not all(text(v) for v in exception.values()):
                return False
            check = checks.get(exception['check_id'])
            if not check or any(exception[k] != check[k] for k in ('candidate_id', 'target_id')):
                return False
        for attempt in indexed(package['attempts']).values():
            if not fields(attempt, 'target_id action authorization_scope outcome operation_id evidence'):
                return False
            if attempt['target_id'] not in targets or not all(text(attempt[k]) for k in ('action', 'authorization_scope', 'operation_id')):
                return False
            if attempt['outcome'] not in {'intent', 'complete', 'failed', 'partial', 'unknown'}:
                return False
            if attempt['outcome'] == 'complete' and not text(attempt['evidence']):
                return False
        return True
    except (KeyError, TypeError, ValueError, AttributeError):
        return False


def gate(package, target_id, stage, authorized, identity_verified, policy=None, candidate_id=None):
    """Evaluate supplied observations, not their external truth or authority."""
    if not validate(package) or authorized is not True or identity_verified is not True or stage not in STAGES:
        return False
    target = next((t for t in package['targets'] if t['id'] == target_id), None)
    if target is None:
        return False
    if stage != 'select' and not target['artifact_ids']:
        return False
    candidate_id = candidate_id or target['candidate_id']
    if stage != 'select' and candidate_id != target['candidate_id']:
        return False
    candidate = next((c for c in package['candidates'] if c['id'] == candidate_id), None)
    if not candidate or not text(candidate['source_revision']) or not text(candidate['build_identity']):
        return False
    if not candidate['artifacts'] or any(not text(a['identity']) for a in candidate['artifacts']):
        return False
    policy = {} if policy is None else policy
    if not isinstance(policy, dict) or any(not isinstance(policy.get(k, []), list)
                                          or not all(text(v) for v in policy.get(k, []))
                                          for k in ('waivable', 'approvers')):
        return False
    for check in package['checks']:
        if check['candidate_id'] != candidate_id or check['target_id'] != target_id:
            continue
        if not check['required'] or STAGES[check['stage']] > STAGES[stage] or check['status'] == 'passed':
            continue
        permitted = check['origin'] == 'internal' and check['id'] in policy.get('waivable', [])
        exception = any(e['check_id'] == check['id'] and e['candidate_id'] == candidate_id
                        and e['target_id'] == target_id and e['scope'] == stage
                        and e['approver'] in policy.get('approvers', []) for e in package['exceptions'])
        if check['status'] not in {'failed', 'unexecuted'} or not permitted or not exception:
            return False
    return True


def complete(package, target_id, policy=None):
    if not gate(package, target_id, 'complete', True, True, policy):
        return False
    target = next(t for t in package['targets'] if t['id'] == target_id)
    return target['status'] == 'complete'


def publication_complete(package, policy=None):
    if not validate(package):
        return False
    targets = package['targets']
    return any(complete(package, t['id'], policy) for t in targets) and all(
        not t['required'] or complete(package, t['id'], policy) for t in targets)

"""Test-owned execution harness, not an implementation of the Markdown Skills.

Only the bundled harmless build script runs; the provider is a local journal.
This proves fixture execution and recovery, not Agent instruction compliance.
"""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import zipfile

from release_contract_v2 import validate, gate, complete

FIXTURES = Path(__file__).resolve().parent


class ReplyLost(Exception):
    pass


def migrate_preview(old, release_id):
    """Explicit fixture import only; legacy publication does not prove a build."""
    return {'schema_version': '2.0.0', 'project': old['project'], 'release_id': release_id,
            'release_version': {'value': old['version'], 'scheme': 'semver', 'source': old['version_source']},
            'change_items': copy.deepcopy(old.get('change_items', [])),
            'candidates': [{'id': 'imported-source', 'source_revision': old['commit'],
                            'build_identity': None, 'artifacts': []}],
            'targets': [{'id': 'imported', 'required': True, 'candidate_id': 'imported-source',
                         'artifact_ids': [], 'status': 'pending', 'delivered_artifacts': [], 'evidence': None}],
            'checks': [], 'exceptions': [], 'attempts': [], 'communication': []}


def digest(path):
    return 'sha256:' + hashlib.sha256(path.read_bytes()).hexdigest()


def build(root, build_available, fail=False):
    if not build_available:
        return {'status': 'unavailable', 'reason': 'only a combined publication tool exists'}
    command = [sys.executable, '-B', str(FIXTURES / 'build_tool.py')]
    if fail:
        command.append('--fail')
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
    if result.returncode:
        return {'status': 'failed', 'exit_code': result.returncode, 'evidence': result.stderr}
    output = json.loads(result.stdout)
    path = root / output.pop('artifact')
    with zipfile.ZipFile(path) as archive:
        if set(archive.namelist()) != {'client.txt', 'plugin.txt', 'config.json'}:
            return {'status': 'failed', 'exit_code': 1, 'evidence': 'missing project output'}
    return dict(output, status='passed', command=command, artifact={
        'id': 'combined-1-bin', 'location': path.name, 'identity': digest(path), 'evidence': 'fixture:inspected-zip'})


class Workflow:
    def __init__(self, root, package):
        self.root = root
        self.package = copy.deepcopy(package)

    @classmethod
    def load(cls, root):
        return cls(root, json.loads((root / 'package.json').read_text()))

    def save(self):
        path = self.root / 'package.json'
        temporary = self.root / 'package.next'
        temporary.write_text(json.dumps(self.package, indent=2))
        temporary.replace(path)

    def receipts(self):
        path = self.root / 'provider.jsonl'
        return [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []

    def finish(self, target_id):
        target = next(t for t in self.package['targets'] if t['id'] == target_id)
        if gate(self.package, target_id, 'complete', True, True):
            target['status'] = 'complete'

    def combined(self, target_id, authorized):
        if not gate(self.package, target_id, 'upload', authorized, True):
            return 'blocked'
        result = build(self.root, build_available=True)
        if result['status'] != 'passed':
            return 'failed'
        self.package['candidates'].append({'id': 'combined-1', 'source_revision': result['source_revision'],
                                           'build_identity': result['build_identity'], 'artifacts': [result['artifact']]})
        target = next(t for t in self.package['targets'] if t['id'] == target_id)
        target.update(candidate_id='combined-1', artifact_ids=['combined-1-bin'])
        self.package['checks'].append({'id': 'combined-selection', 'candidate_id': 'combined-1', 'target_id': target_id,
                                       'stage': 'select', 'required': True, 'origin': 'internal',
                                       'status': 'passed', 'evidence': result['artifact']['evidence']})
        return self.upload(target_id, authorized)

    def upload(self, target_id, authorized, lose_reply=False, transformed=False,
               observation='available', consumer_verified=True):
        return self._write('upload', target_id, authorized, lose_reply, transformed, observation, consumer_verified)

    def announce(self, target_id, authorized, lose_reply=False):
        if not complete(self.package, target_id):
            return 'blocked'
        return self._write('announce', target_id, authorized, lose_reply, False, 'available', True)

    def _write(self, action, target_id, authorized, lose_reply, transformed, observation, consumer_verified):
        if consumer_verified is not True or not gate(self.package, target_id, 'upload', authorized, True):
            return 'blocked'
        if observation != 'available':
            return 'blocked'
        try:
            lock = (self.root / 'writer.lock').open('x')
        except FileExistsError:
            return 'blocked'
        try:
            operation_id = ':'.join((self.package['release_id'], target_id, action))
            receipt = next((r for r in self.receipts() if r['operation_id'] == operation_id), None)
            target = next(t for t in self.package['targets'] if t['id'] == target_id)
            if receipt is not None:
                if receipt['candidate_id'] != target['candidate_id']:
                    return 'blocked'
                if action == 'upload':
                    output = self.root / (target_id + '-delivered.bin')
                    if not output.is_file() or digest(output) != receipt['delivered']['identity']:
                        return 'blocked'
            attempt = next((a for a in self.package['attempts'] if a['operation_id'] == operation_id), None)
            if attempt is None:
                attempt = {'id': operation_id, 'target_id': target_id, 'action': action, 'authorization_scope': action,
                           'outcome': 'intent', 'operation_id': operation_id, 'evidence': None}
                self.package['attempts'].append(attempt)
            self.save()  # Intent survives before the provider commits.
            reused = receipt is not None
            if receipt is None:
                receipt = {'operation_id': operation_id, 'action': action, 'target_id': target_id,
                           'candidate_id': target['candidate_id']}
                if action == 'upload':
                    target = next(t for t in self.package['targets'] if t['id'] == target_id)
                    candidate = next(c for c in self.package['candidates'] if c['id'] == target['candidate_id'])
                    artifact = candidate['artifacts'][0]
                    source = self.root / artifact['location'] if target['candidate_id'] == 'combined-1' else FIXTURES / artifact['location']
                    if digest(source) != artifact['identity']:
                        return 'blocked'
                    output = self.root / (target_id + '-delivered.bin')
                    output.write_bytes(source.read_bytes() + (b'\nfixture-signature' if transformed else b''))
                    receipt['delivered'] = {'candidate_artifact_id': artifact['id'], 'identity': digest(output),
                                             'relationship': 'transformed' if transformed else 'unchanged',
                                             'evidence': str(output)}
                saved = json.loads((self.root / 'package.json').read_text())
                assert any(a['operation_id'] == operation_id and a['outcome'] == 'intent' for a in saved['attempts'])
                with (self.root / 'provider.jsonl').open('a') as journal:
                    journal.write(json.dumps(receipt) + '\n')
                if lose_reply:
                    attempt['outcome'] = 'unknown'
                    self.save()
                    raise ReplyLost(operation_id)
            attempt.update(outcome='complete', evidence='fixture:provider:' + operation_id)
            if action == 'upload':
                target = next(t for t in self.package['targets'] if t['id'] == target_id)
                target.update(evidence=attempt['evidence'], delivered_artifacts=[receipt['delivered']])
                self.finish(target_id)
            else:
                if not any(r['operation_id'] == operation_id for r in self.package['communication']):
                    self.package['communication'].append(receipt)
            self.save()
            return 'reused' if reused else 'complete'
        finally:
            lock.close()
            (self.root / 'writer.lock').unlink()

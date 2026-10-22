#!/usr/bin/env python3
"""Validate and save a complete current live roadmap evaluation without model calls."""

import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = Path('docs/references/roadmap-conversation-eval-20261021.json')
DETAILS = Path('skills/define-roadmap/references/languages/conversation-eval-20261021.json')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def validate(report):
    spec = importlib.util.spec_from_file_location('roadmap_eval', ROOT / 'scripts/roadmap-conversation-eval.py')
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    cases = json.loads(runner.CASES.read_text()) + json.loads(
        (ROOT / 'skills/define-roadmap/references/languages/conversations-zh-CN.json').read_text())
    expected = dict(assets_sha256=runner.asset_digest(ROOT), context_sha256=digest(runner.skill_context().encode()),
                    cases_sha256=digest(json.dumps(cases, sort_keys=True, ensure_ascii=False).encode()),
                    runner_sha256=digest(Path(spec.origin).read_bytes()),
                    renderer_sha256=digest(runner.RENDERER.read_bytes()))
    if report.get('backend') != 'codex-live' or report.get('live_model') is not True:
        raise ValueError('a complete live evaluation is required')
    if report.get('passed') is not True or report.get('pass_rate') != 1.0 or report.get('error'):
        raise ValueError('evaluation did not pass')
    for field, value in expected.items():
        if report.get(field) != value:
            raise ValueError(f'stale or missing {field}; run a fresh explicit live eval')
    if type(report.get('timeout_seconds')) is not int or report['timeout_seconds'] <= 0:
        raise ValueError('missing or invalid per-turn timeout metadata')
    results = report['cases']
    if [c['id'] for c in results] != [c['id'] for c in cases]:
        raise ValueError('incomplete or reordered golden cases')
    for result, case in zip(results, cases):
        if result.get('passed') is not True or len(result['turns']) != len(case['turns']):
            raise ValueError('incomplete case')
        for index, (turn, source) in enumerate(zip(result['turns'], case['turns']), 1):
            if (turn.get('passed') is not True or turn.get('violations') != []
                    or turn.get('turn') != index or turn.get('user') != source['user']
                    or not isinstance(turn.get('decision', {}).get('reason'), str)):
                raise ValueError('a full passing raw trace is required')
            expected_turn = source['expected']
            decision = turn['decision']
            actions = expected_turn['action'] if isinstance(expected_turn['action'], list) else [expected_turn['action']]
            executed = decision.get('action') in {'blank', 'populate'}
            observation = turn.get('observation', {})
            if (set(decision) != {'action', 'review_scope', 'reason'}
                    or decision.get('action') not in actions or decision.get('review_scope') != expected_turn['scope']
                    or observation.get('stage') != expected_turn['stage']
                    or turn.get('renderer_executed') is not executed or observation.get('renderer_executed') is not executed
                    or (expected_turn['no_write'] and executed)):
                raise ValueError('trace contradicts the golden action, scope or observed stage')
            expected_files = sorted(runner.TOPICS) if expected_turn['stage'] != 'absent' else []
            if observation.get('markdown_files') != expected_files:
                raise ValueError('trace has an incomplete document set')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', type=Path)
    parser.add_argument('--output-root', type=Path, default=ROOT)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text())
        validate(report)
        raw = (json.dumps(report, indent=2, ensure_ascii=False) + '\n').encode()
        summary = copy.deepcopy(report)
        for case in summary['cases']:
            for turn in case['turns']:
                del turn['user']
                del turn['decision']['reason']
        summary.update(details='../../' + DETAILS.as_posix(), details_sha256=digest(raw),
                       limitations=['Bounded JSON decision adapter and real local renderer; not arbitrary shell editing or external integration testing.',
                                    'The provider model ID is not exposed by the CLI adapter.'])
        output_root = args.output_root.resolve()
        outputs = [(output_root / DETAILS, raw),
                   (output_root / SUMMARY, (json.dumps(summary, indent=2) + '\n').encode())]
        for path, _ in outputs:
            if any(parent.is_symlink() for parent in [path, *path.parents]):
                raise ValueError(f'refusing symlink output: {path}')
            if path.exists() and (not path.is_file() or path.stat().st_nlink > 1 or not args.overwrite):
                raise ValueError(f'output requires a regular file and explicit --overwrite: {path}')
        for path, content in outputs:
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists() or path.read_bytes() != content:
                path.write_bytes(content)
        print(f'Saved {SUMMARY} and {DETAILS}')
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())

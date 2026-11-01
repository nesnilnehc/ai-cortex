#!/usr/bin/env python3
"""Report live-evaluation evidence status independently of offline regression tests."""
import argparse
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report', nargs='?', type=Path,
                        default=ROOT / 'docs/references/roadmap-conversation-eval.json')
    args = parser.parse_args()
    if not args.report.exists():
        print(json.dumps({'status': 'not_evaluated', 'reason': 'No current live evaluation report is available.'}))
        return 0
    try:
        spec = importlib.util.spec_from_file_location('exporter', ROOT / 'scripts/save-roadmap-eval-evidence.py')
        exporter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(exporter)
        summary = json.loads(args.report.read_text())
        details = (args.report.parent / summary['details']).resolve()
        if not details.is_relative_to(ROOT):
            raise ValueError('details must stay inside the repository')
        raw = details.read_bytes()
        if exporter.digest(raw) != summary['details_sha256']:
            raise ValueError('details digest mismatch')
        report = json.loads(raw)
        exporter.validate(report)
        projected = copy.deepcopy(report)
        for case in projected['cases']:
            for turn in case['turns']:
                del turn['user']
                del turn['decision']['reason']
        if any(summary.get(key) != value for key, value in projected.items()):
            raise ValueError('summary contradicts the detailed trace')
        print(json.dumps({'status': 'passed'}))
        return 0
    except (ValueError, KeyError, TypeError, AttributeError, IndexError, OSError) as error:
        print(json.dumps({'status': 'invalid', 'reason': str(error)}))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())

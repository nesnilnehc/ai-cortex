#!/usr/bin/env python3
"""Check pinned governance sources and the current reference-consumer registry."""
import hashlib
import json
from pathlib import Path
import subprocess

from stable_governance_consumers import check_compatibility, registry

ROOT = Path(__file__).resolve().parents[1]


def main():
    baseline = json.loads((ROOT / 'tests/fixtures/stable-consumers/governance-v0.6.0.json').read_text())
    for path, source in baseline['sources'].items():
        blob = subprocess.check_output(['git', '-C', str(ROOT), 'show', baseline['source_commit']+':'+path])
        if hashlib.sha256(blob).hexdigest() != source['sha256']:
            raise ValueError('Pinned source digest mismatch: '+path)
    current = registry(ROOT)
    check_compatibility(baseline['registry'], current)
    print(f"Pinned governance sources verified; {len(baseline['registry']['profiles'])} historical profiles, "
          f"{len(baseline['registry']['parameters'])} parameter provenances and required profile/waiver fields preserved.")


if __name__ == '__main__':
    main()

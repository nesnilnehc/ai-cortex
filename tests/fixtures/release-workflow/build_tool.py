"""Harmless fixture project build tool; output is confined to the supplied cwd."""
import json
import sys
import zipfile

if '--fail' in sys.argv:
    print('fixture build failed', file=sys.stderr)
    sys.exit(2)

with zipfile.ZipFile('candidate.zip', 'w') as archive:
    for name, content in [('client.txt', 'fixture client'), ('plugin.txt', 'fixture plugin'),
                          ('config.json', json.dumps({'fixture': True}))]:
        archive.writestr(name, content)
print(json.dumps({'source_revision': '2' * 40, 'build_identity': 'fixture-build-103',
                  'artifact': 'candidate.zip'}))

"""Verify the accepted static runtime using system curl's normal TLS validation."""
import concurrent.futures
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
TYPES = {'.html': {'text/html'}, '.mjs': {'text/javascript', 'application/javascript'}, '.css': {'text/css'}, '.json': {'application/json'}, '.png': {'image/png'}, '.svg': {'image/svg+xml'}, '.txt': {'text/plain'}, '.xml': {'text/xml', 'application/xml'}}


def preserved_html(expected, actual):
    if expected == actual:
        return True
    if b'</body>' in expected:
        prefix, tail = expected.rsplit(b'</body>', 1)
        suffix = b'</body>' + tail
        if not actual.startswith(prefix) or not actual.endswith(suffix):
            return False
        inserted = actual[len(prefix):-len(suffix)]
    else:
        if not actual.startswith(expected):
            return False
        inserted = actual[len(expected):]

    return re.fullmatch(rb'<script>(?:(?!</script>).)*</script>', inserted, re.DOTALL) is not None and b'/cdn-cgi/challenge-platform/' in inserted


def verify_bytes(filename, expected, actual, metadata):
    extension = Path(filename).suffix
    mime = metadata.get('content_type', '').split(';')[0].lower()
    identity = preserved_html(expected, actual) if extension == '.html' else expected == actual
    return {'httpPassed': metadata.get('http_code') == 200, 'tlsPassed': metadata.get('ssl_verify_result') == 0 and metadata.get('url_effective', '').startswith('https://'), 'mimePassed': mime in TYPES.get(extension, set()), 'sourcePreserved': identity, 'byteIdentical': expected == actual, 'sha256': hashlib.sha256(actual).hexdigest()}


class ResourceChecks(unittest.TestCase):
    def test_html_exact_or_known_provider_insertion_only(self):
        source = b'<html><body>Accepted content</body></html>\n'
        self.assertTrue(preserved_html(source, source))
        self.assertTrue(preserved_html(source, source.replace(b'</body>', b'<script>"/cdn-cgi/challenge-platform/"</script></body>')))
        self.assertFalse(preserved_html(source, source.replace(b'Accepted', b'Older')))
        self.assertFalse(preserved_html(source, source.replace(b'</body>', b'<script>unrecognized()</script></body>')))
    def test_provider_marker_does_not_allow_other_inserted_html(self):
        source = b'<body>Accepted</body>'
        injected = b'<script>"/cdn-cgi/challenge-platform/"</script><div>Unapproved</div><script></script>'
        self.assertFalse(preserved_html(source, source.replace(b'</body>', injected + b'</body>')))

    def test_legacy_stub_allows_only_a_known_script_after_its_exact_source(self):
        source = b'<html><p>Legacy link</p></html>\n'
        script = b'<script>"/cdn-cgi/challenge-platform/"</script>'
        self.assertTrue(preserved_html(source, source + script))
        self.assertFalse(preserved_html(source, source.replace(b'Legacy', b'Changed') + script))
        self.assertFalse(preserved_html(source, source + b'<script>unrecognized()</script>'))

    def test_mime_tls_and_exact_non_html_are_independent(self):
        meta = {'http_code': 200, 'ssl_verify_result': 0, 'url_effective': 'https://example.test/main.mjs', 'content_type': 'text/javascript; charset=utf-8'}
        result = verify_bytes('main.mjs', b'accepted', b'accepted', meta)
        self.assertTrue(all(result[k] for k in ['httpPassed', 'tlsPassed', 'mimePassed', 'sourcePreserved']))
        self.assertFalse(verify_bytes('main.mjs', b'accepted', b'older', meta)['sourcePreserved'])
        self.assertFalse(verify_bytes('main.mjs', b'accepted', b'accepted', dict(meta, content_type='text/html'))['mimePassed'])
        self.assertFalse(verify_bytes('main.mjs', b'accepted', b'accepted', dict(meta, ssl_verify_result=1))['tlsPassed'])


def main():
    manifest = json.loads((ROOT / 'website/.openai/runtime-manifest.json').read_text())
    cache_key = json.loads((ROOT / 'website/explore/source-manifest.json').read_text())['cacheKey']
    origin = 'https://ai-cortex.nesnilnehc.top'
    with tempfile.TemporaryDirectory(prefix='aic-public-') as temp:
        def check(row):
            name = row['path']
            expected = (ROOT / 'website' / name).read_bytes()
            assert hashlib.sha256(expected).hexdigest() == row['sha256'], name
            route = '/' if name == 'index.html' else '/' + name
            query = '?lang=zh' if name == 'zh.html' else '?lang=en' if name == 'index.html' else '?v=' + cache_key
            url = origin + route + query
            target = Path(temp) / name
            target.parent.mkdir(parents=True, exist_ok=True)
            command = ['curl', '--silent', '--show-error', '--fail', '--location', '--max-time', '35', '--output', str(target), '--write-out', '%{json}', url]
            result = subprocess.run(command, capture_output=True)
            if result.returncode:
                return {'file': name, 'url': url, 'passed': False, 'error': result.stderr.decode()[:200]}
            metadata = json.loads(result.stdout)
            outcome = verify_bytes(name, expected, target.read_bytes(), metadata)
            return {'file': name, 'url': url, 'effectiveUrl': metadata['url_effective'], 'contentType': metadata['content_type'], 'expectedSha256': row['sha256'], **outcome, 'passed': all(outcome[k] for k in ['httpPassed', 'tlsPassed', 'mimePassed', 'sourcePreserved'])}
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            rows = list(pool.map(check, manifest['files']))
    report = {'date': '2026-10-28', 'scope': 'Actual public HTTPS delivery, with system curl certificate validation enabled', 'runtimeRevision': manifest['runtimeRevision'], 'resources': rows, 'status': 'passed' if all(r['passed'] for r in rows) else 'failed'}
    (ROOT / 'tests/website/evidence/release/public-runtime.json').write_text(json.dumps(report, indent=2) + '\n')
    print(report['status'], len(rows), 'public resources')
    for row in rows:
        if not row['passed']:
            print(row)
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        unittest.main(argv=[sys.argv[0]])
    else:
        sys.exit(main())

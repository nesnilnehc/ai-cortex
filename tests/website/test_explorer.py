"""Website-root closure and public-source provenance, independent of a repository-root server."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote, parse_qs
from html import unescape
import hashlib
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / 'website'
EXPLORER = SITE / 'explore'

class Links(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

class ExplorerContracts(unittest.TestCase):
    def test_native_entries_target_the_same_page_host(self):
        """Covers: AIC-REQ-04 A11/A13; exact native same-page destinations."""
        for filename, target in [('index.html', '/?lang=en#capabilities'), ('zh.html', '/zh.html?lang=zh#capabilities')]:
            anchors=[a for tag,a in Links((SITE/filename).read_text()).tags if a.get('data-site-destination')=='overview']
            self.assertEqual([a['href'] for a in anchors],[target])
            legacy=Links((EXPLORER/filename).read_text())
            fallback=next(a for tag,a in legacy.tags if a.get('id')=='legacy-capability-link')
            self.assertEqual(fallback['href'],target.replace('#capabilities','&view=relations#capabilities'))

    def test_explorer_home_links_preserve_the_selected_edition(self):
        """Covers: A13; native return is an explicit same-language homepage URL."""
        for filename, home in [('index.html','/?lang=en'),('zh.html','/zh.html?lang=zh')]:
            anchors=[a for tag,a in Links((SITE/filename).read_text()).tags if tag=='a']
            self.assertEqual(next(a for a in anchors if a.get('class')=='wordmark')['href'],home)

    def test_every_runtime_dependency_resolves_inside_the_website_root(self):
        """Covers: AIC-REQ-04#A11; source/usage checks also cover A3/A5/A7/A10."""
        queue = [SITE / 'index.html', SITE / 'zh.html', EXPLORER / 'index.html', EXPLORER / 'zh.html']
        seen = set()
        while queue:
            file = queue.pop()
            if file in seen:
                continue
            seen.add(file)
            self.assertTrue(file.is_file(), file)
            self.assertTrue(file.is_relative_to(SITE.resolve()), file)
            if file.suffix not in ('.html', '.mjs', '.css'):
                continue
            source = file.read_text()
            if file.suffix == '.html':
                refs = [a.get('src', a.get('href', '')) for tag, a in Links(source).tags if tag in ('script', 'img') or tag == 'link' and a.get('rel') in ('stylesheet', 'icon', 'preload')]
            elif file.suffix == '.mjs':
                refs = re.findall(r"(?:from|import)\s*['\"]([^'\"]+)['\"]", source)
            else:
                refs = re.findall(r"url\(['\"]?([^)'\"]+)", source)
            for ref in refs:
                self.assertFalse(urlsplit(ref).netloc, ref)
                self.assertFalse(ref.startswith('/'), ref)
                self.assertNotIn('experiments/', ref)
                target = (file.parent / unquote(urlsplit(ref).path)).resolve()
                queue.append(target)
                if target.suffix in ('.mjs', '.json'):
                    self.assertEqual(parse_qs(urlsplit(ref).query).get('v'), [json.loads((EXPLORER / 'source-manifest.json').read_text())['cacheKey']], f'Inconsistent transitive cache identity: {ref}')
        self.assertGreater(len(seen), 20)

    def test_static_copy_mirrors_its_locale_owner(self):
        """Covers: AIC-REQ-04#A11; source/usage checks also cover A3/A5/A7/A10."""
        runtime = '\n'.join(p.read_text() for p in [p for p in EXPLORER.glob('*.mjs') if p.name != 'story.mjs'])
        dynamic = set(re.findall(r"t\('([^']+)'", runtime))
        for locale, filename in [('en', 'index.html'), ('zh', 'zh.html')]:
            copy = json.loads((EXPLORER / f'locales/{locale}.json').read_text())['ui']
            html = unescape((SITE / filename).read_text())
            for key, value in copy.items():
                if key not in dynamic:
                    self.assertIn(value.strip(), html, f'Static copy drift: {locale}/{key}')

    def test_canonical_sources_and_registry_match_the_verified_local_definitions(self):
        """Covers: AIC-REQ-04#A11; source/usage checks also cover A3/A5/A7/A10."""
        skills = json.loads((EXPLORER / 'skill-metadata.json').read_text())['skills']
        canonical = set(re.findall(r'\]\(\./([^/]+)/SKILL.md\)', (ROOT / 'skills/INDEX.md').read_text()))
        self.assertEqual(set(skills), canonical)
        for identity, record in skills.items():
            source = f'skills/{identity}/SKILL.md'
            self.assertEqual(record['sourcePaths'], [source])
            self.assertEqual(record['sourceHashes'][source], hashlib.sha256((ROOT / source).read_bytes()).hexdigest())
        for filename in ('topic-edges.json', 'skill-edges.json', 'topic-map.json'):
            for edge in json.loads((EXPLORER / filename).read_text()):
                sources = edge.get('sources', [{'path': edge.get('source'), 'quote': edge.get('quote')}])
                for source in sources:
                    path = source.get('path')
                    if path:
                        self.assertTrue((ROOT / path).is_file(), path)
                        self.assertIn(source['quote'], (ROOT / path).read_text())

    def test_english_copy_has_no_untranslated_chinese_and_locale_keys_match(self):
        """Covers: AIC-REQ-04#A11; source/usage checks also cover A3/A5/A7/A10."""
        en = json.loads((EXPLORER / 'locales/en.json').read_text())
        zh = json.loads((EXPLORER / 'locales/zh.json').read_text())
        self.assertNotRegex(json.dumps(en, ensure_ascii=False), r'[\u3400-\u9fff]')
        self.assertEqual(set(en), set(zh))
        for identity in en['skills']:
            self.assertIn(identity, en['skills'][identity]['use'])
            self.assertEqual(set(en['skills'][identity]), {'name', 'purpose', 'when', 'provide', 'use', 'result'})

if __name__ == '__main__':
    unittest.main()

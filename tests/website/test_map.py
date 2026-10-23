"""The on-site overview must cover the canonical registry, not a sample catalogue."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]

class MapPage(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.assets = []
        self.ids = []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'data-asset' in attrs:
            self.assets.append(attrs['data-asset'])
        if 'id' in attrs:
            self.ids.append(attrs['id'])

class CapabilityMap(unittest.TestCase):
    def test_branch_counts_match_the_assets_they_reveal(self):
        for edition in ('index.html', 'zh.html'):
            source = (ROOT / 'website' / edition).read_text()
            branches = re.findall(r'<details class="atlas-branch"[^>]*>(.*?)</details>', source, re.S)
            self.assertEqual(len(branches), 9)
            for branch in branches:
                declared = int(re.search(r'class="atlas-count">(\d+)', branch).group(1))
                self.assertEqual(declared, branch.count('data-asset='))

    def test_map_contains_each_registered_asset_once_in_both_languages(self):
        expected = set()
        for layer in ('skills', 'specs', 'rules', 'protocols'):
            index = (ROOT / layer / 'INDEX.md').read_text()
            for target in re.findall(r'\]\(\./([^)]*\.md)\)', index):
                if target == 'INDEX.md':
                    continue
                name = target.removesuffix('/SKILL.md').removesuffix('.md')
                expected.add(f'{layer}/{name}')
        for edition in ('index.html', 'zh.html'):
            with self.subTest(edition=edition):
                source = (ROOT / 'website' / edition).read_text()
                page = MapPage(source)
                self.assertEqual(set(page.assets), expected)
                self.assertEqual(len(page.assets), len(expected))
                self.assertIn('capabilities', page.ids)
                self.assertIn('map-specs', page.ids)
                self.assertIn('map-rules', page.ids)
                self.assertIn('map-protocols', page.ids)
                self.assertIn('class="atlas-grid"', source)
                self.assertIn('<details', source)

if __name__ == '__main__':
    unittest.main()

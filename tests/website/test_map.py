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
        self.directories = []
        self.directory_depth = 0
        self.directory_summary = None
        self.directory_assets = 0
        self.in_directory_summary = False
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'details':
            if self.directory_depth:
                self.directory_depth += 1
            elif attrs.get('class') == 'directory-type':
                self.directory_depth = 1
                self.directory_summary = ''
                self.directory_assets = 0
        if tag == 'summary' and self.directory_depth == 1:
            self.in_directory_summary = True
        if 'data-asset' in attrs:
            self.assets.append(attrs['data-asset'])
            if self.directory_depth:
                self.directory_assets += 1
        if 'id' in attrs:
            self.ids.append(attrs['id'])
    def handle_data(self, data):
        if self.in_directory_summary:
            self.directory_summary += data
    def handle_endtag(self, tag):
        if tag == 'summary' and self.directory_depth == 1:
            self.in_directory_summary = False
        if tag == 'details' and self.directory_depth:
            self.directory_depth -= 1
            if not self.directory_depth:
                count = re.search(r' · (\d+)$', self.directory_summary)
                self.directories.append((int(count.group(1)) if count else None,
                                         self.directory_assets))

class CapabilityMap(unittest.TestCase):
    def test_directory_count_includes_entries_after_nested_source_details(self):
        page = MapPage('<details class="directory-type"><summary>Skills · 2</summary>'
                       '<div data-asset="skills/a"><details><summary>Sources</summary>'
                       '<a href="https://example.org">Source</a></details></div>'
                       '<div data-asset="skills/b"></div></details>')
        self.assertEqual(page.directories, [(2, 2)])

    def test_branch_counts_match_the_assets_they_reveal(self):
        for edition in ('index.html', 'zh.html'):
            source = (ROOT / 'website' / edition).read_text()
            branches = MapPage(source).directories
            self.assertEqual(len(branches), 4)
            for declared, actual in branches:
                self.assertEqual(declared, actual)
            self.assertEqual(source.count('class="classification-card"'), 6)

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
                self.assertIn('id="classification-view"', source)
                self.assertIn('id="relations-view"', source)
                self.assertIn('<details', source)

if __name__ == '__main__':
    unittest.main()

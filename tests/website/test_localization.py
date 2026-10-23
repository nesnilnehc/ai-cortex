"""Contracts for the published language editions."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

SITE = Path(__file__).resolve().parents[2] / 'website'

class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.tags = []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))

class Localization(unittest.TestCase):
    def test_static_chinese_edition_is_complete(self):
        source = (SITE / 'zh.html').read_text()
        self.assertIn('lang="zh-CN"', source)
        self.assertIn('让 AI 智能体', source)
        self.assertIn('复制命令', source)
        self.assertNotIn('Give your agents', source)
        english = Page((SITE / 'index.html').read_text())
        chinese = Page(source)
        for key in ('id', 'href', 'src'):
            def values(page):
                return [a[key] for t, a in page.tags if key in a and not (t == 'link' and a.get('rel') == 'canonical')]
            self.assertEqual(values(english), values(chinese))

    def test_language_links_and_metadata(self):
        for name, locale, canonical in [('index.html', 'en', '/'), ('zh.html', 'zh-CN', '/zh.html')]:
            with self.subTest(name=name):
                page = Page((SITE / name).read_text())
                links = [a for t, a in page.tags if t == 'a']
                self.assertTrue(any(a.get('href') == './zh.html' and a.get('hreflang') == 'zh-CN' for a in links))
                self.assertTrue(any(a.get('href') == './' and a.get('hreflang') == 'en' for a in links))
                self.assertTrue(any(t == 'link' and a.get('rel') == 'canonical' and a.get('href') == 'https://ai-cortex.nesnilnehc.top' + canonical for t, a in page.tags))
                alternates = {a.get('hreflang') for t, a in page.tags if t == 'link' and a.get('rel') == 'alternate'}
                self.assertEqual(alternates, {'en', 'zh-CN', 'x-default'})

    def test_commands_and_feedback_data_are_complete(self):
        from test_site import Page as ContentPage
        english = ContentPage((SITE / 'index.html').read_text())
        for name in ('index.html', 'zh.html'):
            source = (SITE / name).read_text()
            self.assertEqual(ContentPage(source).command_parts, english.command_parts)
            page = Page(source)
            feedback = next(a for _, a in page.tags if a.get('id') == 'copy-feedback')
            for key in ('copying', 'success', 'unavailable', 'empty'):
                self.assertTrue(feedback.get('data-' + key))
                if name == 'zh.html':
                    self.assertTrue(any('\u4e00' <= c <= '\u9fff' for c in feedback['data-' + key]))
            active = [a for _, a in page.tags if a.get('aria-current') == 'page']
            self.assertEqual(len(active), 1)
            self.assertEqual(active[0]['hreflang'], 'en' if name == 'index.html' else 'zh-CN')

    def test_localized_pages_request_current_resource_versions(self):
        for name in ('index.html', 'zh.html'):
            page = Page((SITE / name).read_text())
            for tag, attrs in page.tags:
                if tag == 'script' or (tag == 'link' and attrs.get('rel') == 'stylesheet'):
                    self.assertIn('?v=', attrs.get('src', attrs.get('href', '')))
        self.assertIn('copy.mjs?v=', (SITE / 'main.mjs').read_text())

    def test_sitemap_lists_both_languages(self):
        tree = ET.parse(SITE / 'sitemap.xml')
        locations = [e.text for e in tree.iter() if e.tag.endswith('}loc')]
        self.assertEqual(locations, ['https://ai-cortex.nesnilnehc.top/', 'https://ai-cortex.nesnilnehc.top/zh.html'])

if __name__ == '__main__':
    unittest.main()

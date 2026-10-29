"""Source contracts for the standalone site; no external requests or packages."""

from html.parser import HTMLParser
from pathlib import Path
import unittest
import sys
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
SITE = ROOT / "website"


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.ids = []
        self.links = []
        self.resources = []
        self.command_parts = []
        self.in_commands = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs["href"])
        if tag in ("script", "link"):
            self.resources.append(attrs.get("src", attrs.get("href", "")))
        if tag == "code" and attrs.get("id") == "install-commands":
            self.in_commands = True

    def handle_endtag(self, tag):
        if tag == "code":
            self.in_commands = False

    def handle_data(self, data):
        if self.in_commands:
            self.command_parts.append(data)


class SiteContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (SITE / "index.html").read_text()
        cls.page = Page(cls.html)

    def test_installation_matches_readme(self):
        readme = (ROOT / "README.md").read_text()
        commands = "".join(self.page.command_parts).strip()
        self.assertTrue(commands)
        self.assertIn(f"```bash\n{commands}\n```", readme)

    def test_anchors_resolve_and_ids_are_unique(self):
        self.assertEqual(len(self.page.ids), len(set(self.page.ids)))
        for link in self.page.links:
            if link.startswith("#") and link != "#":
                with self.subTest(link=link):
                    self.assertIn(link[1:], self.page.ids)

    def test_repository_destinations_exist_in_this_checkout(self):
        prefix = "/nesnilnehc/ai-cortex/"
        sys.path.insert(0, str(ROOT / "scripts"))
        from skill_provenance_v2 import parse_registry
        registry = parse_registry((ROOT / "skills/SOURCES.yaml").read_text())
        upstream_links = {
            entry["upstream"]["repository"].removesuffix(".git") + "/tree/" + entry["upstream"]["ref"] + "/" + entry["upstream"]["path"]
            for entry in registry["skills"].values()
        }
        for link in self.page.links:
            url = urlsplit(link)
            if url.netloc != "github.com":
                continue
            path = unquote(url.path)
            with self.subTest(link=link):
                if not (path.startswith(prefix) or path == prefix.rstrip("/")):
                    self.assertIn(link, upstream_links)
                    continue
                self.assertTrue(path.startswith(prefix) or path == prefix.rstrip("/"))
                for kind in ("blob/main/", "tree/main/"):
                    if path.startswith(prefix + kind):
                        self.assertTrue((ROOT / path[len(prefix + kind):]).exists())
                if url.fragment:
                    self.assertEqual(url.fragment, "quick-start")
                    self.assertIn("\n### Quick start\n", (ROOT / "README.md").read_text())

    def test_assets_are_local_and_exist(self):
        for resource in self.page.resources:
            if resource.startswith("https://ai-cortex.nesnilnehc.top"):
                continue  # Canonical metadata, not a fetched dependency.
            with self.subTest(resource=resource):
                self.assertFalse(urlsplit(resource).netloc)
                self.assertTrue((SITE / urlsplit(resource).path).is_file())
        self.assertRegex((SITE / "main.mjs").read_text(), r"from '\./copy\.mjs(?:\?[^']*)?'")
        self.assertTrue((SITE / "copy.mjs").is_file())

    def test_search_metadata_uses_intended_domain(self):
        self.assertIn('rel="canonical" href="https://ai-cortex.nesnilnehc.top/"', self.html)
        sitemap = ET.parse(SITE / "sitemap.xml")
        locations = [element.text for element in sitemap.iter() if element.tag.endswith("}loc")]
        self.assertEqual(locations, ["https://ai-cortex.nesnilnehc.top/", "https://ai-cortex.nesnilnehc.top/zh.html"])
        self.assertIn("https://ai-cortex.nesnilnehc.top/sitemap.xml", (SITE / "robots.txt").read_text())


if __name__ == "__main__":
    unittest.main()

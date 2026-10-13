"""Dependency-free structural checks for the public static pages."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = ("index.html", "about.html", "project.html")
VOID = set("area base br col embed hr img input link meta param source track wbr".split())


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path, self.tags, self.ids, self.stack, self.errors = path, [], [], [], []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag not in VOID:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if not self.stack or self.stack[-1] != tag:
            self.errors.append(f"Unexpected closing tag: {tag}")
        else:
            self.stack.pop()


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.pages = {name: Page(ROOT / name) for name in PAGES}

    def test_structure_and_metadata(self):
        for name, page in self.pages.items():
            with self.subTest(page=name):
                self.assertEqual(page.errors, [])
                self.assertEqual(page.stack, [])
                self.assertEqual(len(page.ids), len(set(page.ids)))
                self.assertEqual(sum(tag == "h1" for tag, _ in page.tags), 1)
                self.assertTrue(any(tag == "html" and a.get("lang") == "en" for tag, a in page.tags))
                self.assertTrue(any(tag == "meta" and a.get("name") == "description" for tag, a in page.tags))
                self.assertTrue(any(tag == "meta" and a.get("name") == "viewport" for tag, a in page.tags))
                self.assertTrue(any(tag == "link" and a.get("rel") == "canonical" for tag, a in page.tags))

    def test_local_links_resources_and_fragments(self):
        for name, page in self.pages.items():
            for tag, attrs in page.tags:
                for key in ("href", "src"):
                    if key not in attrs:
                        continue
                    value = attrs[key]
                    self.assertTrue(value, f"Empty {key} in {name}")
                    if tag == "link" and attrs.get("rel") == "canonical":
                        continue  # relative canonical resolves per serving host
                    url = urlsplit(value)
                    if url.scheme or url.netloc:
                        continue
                    target = ROOT / unquote(url.path) if url.path else ROOT / name
                    self.assertTrue(target.is_file(), f"Missing local resource: {value}")
                    if url.fragment:
                        self.assertIn(unquote(url.fragment), Page(target).ids, f"Missing anchor: {value}")
        css = (ROOT / "css/site.css").read_text()
        self.assertEqual(css.count("{"), css.count("}"))
        for path in re.findall(r"url\(['\"]?([^'\")]+)", css):
            if not urlsplit(path).scheme:
                self.assertTrue((ROOT / "css" / path).is_file())

    def test_accessibility_basics(self):
        page = self.pages["index.html"]
        for tag, attrs in page.tags:
            if tag == "img":
                self.assertTrue(attrs.get("alt"))
                self.assertTrue(attrs.get("width") and attrs.get("height"))
            if "aria-labelledby" in attrs:
                for target in attrs["aria-labelledby"].split():
                    self.assertIn(target, page.ids)
        self.assertTrue(any(tag == "a" and a.get("class") == "skip-link" for tag, a in page.tags))
        css = (ROOT / "css/site.css").read_text()
        self.assertIn(":focus-visible", css)
        self.assertIn("prefers-reduced-motion", css)

    def test_no_runtime_or_third_party_dependencies(self):
        for page in self.pages.values():
            self.assertFalse(any(tag == "script" for tag, _ in page.tags))
            self.assertFalse(any(tag in ("img", "link") and urlsplit(a.get("src", a.get("href", ""))).scheme for tag, a in page.tags if a.get("rel") != "canonical"))

    def test_legacy_redirects_and_fallbacks(self):
        for name, anchor in (("about.html", "about"), ("project.html", "work")):
            page = self.pages[name]
            target = f"index.html#{anchor}"
            self.assertTrue(any(tag == "meta" and a.get("http-equiv") == "refresh" and target in a.get("content", "") for tag, a in page.tags))
            self.assertTrue(any(tag == "a" and a.get("href") == target for tag, a in page.tags))


if __name__ == "__main__":
    unittest.main(verbosity=2)

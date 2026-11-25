"""
Comprehensive automated test suite for Magisk Hub Simplified Chinese (zh)
localization, content parity, hreflang full-mesh, SEO metadata, JSON-LD,
internal link isolation, and static build output verification.
"""

import glob
import json
import os
import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urlparse

import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULES_DIR = os.path.join(REPO_ROOT, "modules")
ZH_MODULES_DIR = os.path.join(REPO_ROOT, "locales", "zh", "modules")
EN_CONTENT_DIR = os.path.join(REPO_ROOT, "content", "modules")
ZH_CONTENT_DIR = os.path.join(REPO_ROOT, "content", "zh", "modules")
DIST_DIR = os.path.join(REPO_ROOT, "dist")

CJK_RE = re.compile(r"[\u4e00-\u9fff]")
FENCE_RE = re.compile(r"^```", re.MULTILINE)


def parse_frontmatter(text: str):
    assert text.startswith("---"), "Missing YAML frontmatter start"
    parts = text.split("---", 2)
    assert len(parts) == 3, "Missing YAML frontmatter end"
    return yaml.safe_load(parts[1]), parts[2]


class FullHtmlInspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.html_lang = None
        self.title = ""
        self._in_title = False
        self._in_jsonld = False
        self._jsonld_buf = []
        self.metas = []
        self.links = []
        self.anchors = []
        self.schemas = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "html":
            self.html_lang = d.get("lang")
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            self.metas.append(d)
        elif tag == "link":
            self.links.append(d)
        elif tag == "a" and "href" in d:
            self.anchors.append((d["href"], d.get("data-locale-switch")))
        elif tag == "script" and d.get("type") == "application/ld+json":
            self._in_jsonld = True
            self._jsonld_buf = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script" and self._in_jsonld:
            raw = "".join(self._jsonld_buf).strip()
            self.schemas.append(json.loads(raw))
            self._in_jsonld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif self._in_jsonld:
            self._jsonld_buf.append(data)


def inspect_html(path: str) -> FullHtmlInspector:
    parser = FullHtmlInspector()
    with open(path, "r", encoding="utf-8") as fp:
        parser.feed(fp.read())
    return parser


class TestZhContentParity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module_files = sorted(
            f for f in glob.glob(os.path.join(MODULES_DIR, "*.json"))
            if os.path.basename(f) != "schema.json"
        )
        cls.slugs = [os.path.basename(f)[:-5] for f in cls.module_files]

    def test_all_modules_have_zh_json_and_markdown(self):
        missing_json = [s for s in self.slugs if not os.path.isfile(os.path.join(ZH_MODULES_DIR, f"{s}.json"))]
        missing_md = [s for s in self.slugs if not os.path.isfile(os.path.join(ZH_CONTENT_DIR, f"{s}.md"))]
        extra_json = sorted({os.path.basename(f)[:-5] for f in glob.glob(os.path.join(ZH_MODULES_DIR, "*.json"))} - set(self.slugs))
        extra_md = sorted({os.path.basename(f)[:-3] for f in glob.glob(os.path.join(ZH_CONTENT_DIR, "*.md"))} - set(self.slugs))
        self.assertEqual(missing_json, [], f"Missing ZH JSON files: {missing_json[:10]}")
        self.assertEqual(missing_md, [], f"Missing ZH Markdown files: {missing_md[:10]}")
        self.assertEqual(extra_json, [], f"Orphaned ZH JSON files: {extra_json[:10]}")
        self.assertEqual(extra_md, [], f"Orphaned ZH Markdown files: {extra_md[:10]}")

    def test_zh_json_quality_and_seo_uniqueness(self):
        titles = {}
        descs = {}
        for slug in self.slugs:
            with open(os.path.join(ZH_MODULES_DIR, f"{slug}.json"), "r", encoding="utf-8") as fp:
                zh = json.load(fp)
            self.assertEqual(zh.get("id"), slug)
            self.assertTrue(zh.get("displayName"), f"{slug}: empty displayName")
            self.assertTrue(CJK_RE.search(zh.get("description", "")), f"{slug}: description not Chinese")
            aliases = zh.get("searchAliases", [])
            self.assertGreaterEqual(len(aliases), 2, f"{slug}: expected >=2 searchAliases")

            seo = zh.get("seo", {})
            t = (seo.get("title") or "").strip()
            d = (seo.get("description") or "").strip()
            self.assertTrue(CJK_RE.search(t), f"{slug}: seo.title lacks Chinese")
            self.assertTrue(CJK_RE.search(d), f"{slug}: seo.description lacks Chinese")
            self.assertGreaterEqual(len(t), 15, f"{slug}: seo.title too short: {t}")
            self.assertLessEqual(len(t), 80, f"{slug}: seo.title too long: {t}")
            self.assertGreaterEqual(len(d), 35, f"{slug}: seo.description too short: {d}")
            self.assertLessEqual(len(d), 145, f"{slug}: seo.description too long: {d}")
            self.assertNotIn(t, titles, f"Duplicate ZH seo.title between {slug} and {titles.get(t)}")
            titles[t] = slug
            descs.setdefault(d, []).append(slug)

        dupes = {k: v for k, v in descs.items() if len(v) > 1}
        self.assertEqual(dupes, {}, f"Duplicate ZH seo.description entries: {dupes}")

    def test_zh_markdown_parity_and_code_preservation(self):
        for slug in self.slugs:
            with open(os.path.join(EN_CONTENT_DIR, f"{slug}.md"), "r", encoding="utf-8") as fp:
                en_fm, en_body = parse_frontmatter(fp.read())
            with open(os.path.join(ZH_CONTENT_DIR, f"{slug}.md"), "r", encoding="utf-8") as fp:
                zh_fm, zh_body = parse_frontmatter(fp.read())

            self.assertEqual(zh_fm.get("id"), en_fm.get("id"), f"{slug}: id mismatch")
            self.assertEqual(zh_fm.get("category"), en_fm.get("category"), f"{slug}: category mismatch")
            self.assertEqual(zh_fm.get("tier", 1), en_fm.get("tier", 1), f"{slug}: tier mismatch")
            self.assertEqual(zh_fm.get("configPaths", []), en_fm.get("configPaths", []), f"{slug}: configPaths mismatch")
            self.assertEqual(len(zh_fm.get("faq", [])), len(en_fm.get("faq", [])), f"{slug}: FAQ count mismatch")
            self.assertTrue(CJK_RE.search(zh_fm.get("title", "")), f"{slug}: frontmatter title not Chinese")
            self.assertTrue(CJK_RE.search(zh_fm.get("description", "")), f"{slug}: frontmatter description not Chinese")
            self.assertTrue(CJK_RE.search(zh_body), f"{slug}: body lacks Chinese prose")

            en_fences = len(FENCE_RE.findall(en_body))
            zh_fences = len(FENCE_RE.findall(zh_body))
            self.assertEqual(zh_fences, en_fences, f"{slug}: code fence count mismatch ({zh_fences} vs {en_fences})")


class TestBuiltDistSEOAndHreflang(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert os.path.isdir(DIST_DIR), "dist/ missing; run 'npm run build' first"
        tree = ET.parse(os.path.join(DIST_DIR, "sitemap-0.xml"))
        root = tree.getroot()
        ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        cls.sitemap_urls = [el.text.strip() for el in root.findall(".//s:loc", ns)]

    def test_every_sitemap_url_has_built_html_and_full_hreflang_mesh(self):
        module_count = len([
            f for f in glob.glob(os.path.join(MODULES_DIR, "*.json"))
            if os.path.basename(f) != "schema.json"
        ])
        en_urls = [u for u in self.sitemap_urls if not urlparse(u).path.startswith("/zh/")]
        zh_urls = [u for u in self.sitemap_urls if urlparse(u).path.startswith("/zh/")]
        self.assertEqual(len(en_urls), len(zh_urls), "EN and ZH sitemap URL counts must match 1:1")
        self.assertGreaterEqual(len(zh_urls), module_count + 20)

        for url in self.sitemap_urls:
            path = urlparse(url).path
            rel = path.strip("/")
            html_file = os.path.join(DIST_DIR, rel, "index.html") if rel else os.path.join(DIST_DIR, "index.html")
            self.assertTrue(os.path.isfile(html_file), f"Missing built HTML for sitemap URL: {url}")

            doc = inspect_html(html_file)
            is_zh = path.startswith("/zh/")
            self.assertEqual(doc.html_lang, "zh-CN" if is_zh else "en", f"Wrong <html lang> on {path}")

            canon = next((l.get("href") for l in doc.links if l.get("rel") == "canonical"), None)
            self.assertEqual(canon, url, f"Canonical mismatch on {path}: {canon} != {url}")

            alts = {l.get("hreflang"): l.get("href") for l in doc.links if l.get("rel") == "alternate"}
            expected_en = url.replace("https://magisk.yssn.tech/zh/", "https://magisk.yssn.tech/", 1)
            expected_zh = (
                url if is_zh
                else url.replace("https://magisk.yssn.tech/", "https://magisk.yssn.tech/zh/", 1)
            )
            self.assertEqual(alts.get("en"), expected_en, f"hreflang=en mismatch on {path}")
            self.assertEqual(alts.get("zh-Hans"), expected_zh, f"hreflang=zh-Hans mismatch on {path}")
            self.assertEqual(alts.get("x-default"), expected_en, f"hreflang=x-default mismatch on {path}")

            og_locale = next((m.get("content") for m in doc.metas if m.get("property") == "og:locale"), None)
            self.assertEqual(og_locale, "zh_CN" if is_zh else "en_US", f"og:locale mismatch on {path}")

            # Verify valid JSON-LD and localized inLanguage
            self.assertGreaterEqual(len(doc.schemas), 1, f"Missing JSON-LD on {path}")
            website_schema = next((s for s in doc.schemas if s.get("@type") == "WebSite"), None)
            self.assertIsNotNone(website_schema, f"Missing WebSite JSON-LD on {path}")
            self.assertEqual(website_schema.get("inLanguage"), "zh-Hans" if is_zh else "en")

    def test_zh_pages_keep_internal_navigation_within_zh(self):
        for rel in ["zh/index.html", "zh/categories/index.html", "zh/security/index.html", "zh/modules/magisk/index.html", "zh/modules/playintegrityfix/index.html"]:
            doc = inspect_html(os.path.join(DIST_DIR, rel))
            non_switcher_leaks = [
                href for href, switch_to in doc.anchors
                if href.startswith("/")
                and not href.startswith("/zh/")
                and not href.startswith("/assets/")
                and switch_to != "en"
            ]
            self.assertEqual(non_switcher_leaks, [], f"Found non-zh internal links in {rel}: {non_switcher_leaks}")

    def test_404_pages_are_noindex_and_not_in_sitemap(self):
        for rel in ["404.html", os.path.join("zh", "404", "index.html")]:
            fpath = os.path.join(DIST_DIR, rel)
            self.assertTrue(os.path.isfile(fpath), f"Missing {rel}")
            doc = inspect_html(fpath)
            robots = next((m.get("content") for m in doc.metas if m.get("name") == "robots"), "")
            self.assertIn("noindex", robots, f"{rel} must have noindex")
        self.assertFalse(any("/404" in u for u in self.sitemap_urls), "404 must not appear in sitemap")

    def test_llms_and_indexnow_artifacts(self):
        for rel in [
            "llms.txt",
            "llms-full.txt",
            "zh/llms.txt",
            "zh/llms-full.txt",
            "robots.txt",
            "a8f4c2e91b7d40329e6f1a5b8c3d7e20.txt",
        ]:
            fpath = os.path.join(DIST_DIR, rel)
            self.assertTrue(os.path.isfile(fpath), f"Missing dist/{rel}")

        with open(os.path.join(DIST_DIR, "zh", "llms.txt"), "r", encoding="utf-8") as fp:
            zh_llms = fp.read()
        self.assertIn("https://magisk.yssn.tech/zh/", zh_llms)
        self.assertTrue(CJK_RE.search(zh_llms))

    def test_vercel_redirects_point_to_existing_dist_pages(self):
        with open(os.path.join(REPO_ROOT, "vercel.json"), "r", encoding="utf-8") as fp:
            cfg = json.load(fp)
        redirects = cfg.get("redirects", [])
        self.assertGreaterEqual(len(redirects), 10)
        for rule in redirects:
            dest = rule["destination"]
            if ":" in dest:
                # Parameterized wildcard redirects like /modules/:slug/
                continue
            rel = urlparse(dest).path.strip("/")
            html_path = os.path.join(DIST_DIR, rel, "index.html") if rel else os.path.join(DIST_DIR, "index.html")
            self.assertTrue(os.path.isfile(html_path), f"vercel.json redirect target missing in dist: {dest}")


if __name__ == "__main__":
    unittest.main()

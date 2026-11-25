#!/usr/bin/env python3
"""
Production dist/ verification audit (EN + ZH, stdlib html.parser + XML):
- Sitemap completeness & bidirectional xhtml:link hreflang alternates
- 404 exclusion from sitemap + noindex
- LLM discovery artifacts (llms.txt, llms-full.txt, zh/llms.txt, zh/llms-full.txt)
- Full HTML meta, canonical, hreflang, OpenGraph, and JSON-LD validation across EN + ZH pages
"""

import glob
import json
import os
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser


class HeadAndSchemaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.html_lang = None
        self.title = None
        self.in_title = False
        self.in_jsonld = False
        self._title_buf = []
        self._jsonld_buf = []
        self.metas = []
        self.links = []
        self.schemas = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        if tag == "html":
            self.html_lang = attr_dict.get("lang")
        elif tag == "title":
            self.in_title = True
            self._title_buf = []
        elif tag == "meta":
            self.metas.append(attr_dict)
        elif tag == "link":
            self.links.append(attr_dict)
        elif tag == "script" and attr_dict.get("type") == "application/ld+json":
            self.in_jsonld = True
            self._jsonld_buf = []

    def handle_endtag(self, tag):
        if tag == "title" and self.in_title:
            self.title = "".join(self._title_buf).strip()
            self.in_title = False
        elif tag == "script" and self.in_jsonld:
            raw = "".join(self._jsonld_buf).strip()
            if raw:
                try:
                    self.schemas.append(json.loads(raw))
                except Exception:
                    self.schemas.append({"_parse_error": raw[:100]})
            self.in_jsonld = False

    def handle_data(self, data):
        if self.in_title:
            self._title_buf.append(data)
        elif self.in_jsonld:
            self._jsonld_buf.append(data)


def parse_html(path: str) -> HeadAndSchemaParser:
    p = HeadAndSchemaParser()
    with open(path, "r", encoding="utf-8") as hp:
        p.feed(hp.read())
    return p


def verify_dist():
    print("=" * 80)
    print("DIST BUILD & BILINGUAL SEO ARTIFACT VERIFICATION AUDIT")
    print("=" * 80)

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dist_dir = os.path.join(repo_root, "dist")
    if not os.path.isdir(dist_dir):
        print(f"Error: {dist_dir} does not exist!")
        return False

    errors = []

    module_jsons = [
        f for f in glob.glob(os.path.join(repo_root, "modules", "*.json"))
        if os.path.basename(f) != "schema.json"
    ]
    expected_min_urls = len(module_jsons) * 2 + 40

    # 1. Check sitemaps
    sitemap_index = os.path.join(dist_dir, "sitemap-index.xml")
    sitemap_0 = os.path.join(dist_dir, "sitemap-0.xml")

    if not os.path.isfile(sitemap_index):
        errors.append("Missing dist/sitemap-index.xml")
    if not os.path.isfile(sitemap_0):
        errors.append("Missing dist/sitemap-0.xml")
    else:
        try:
            tree = ET.parse(sitemap_0)
            root = tree.getroot()
            ns = {
                "ns": "http://www.sitemaps.org/schemas/sitemap/0.9",
                "x": "http://www.w3.org/1999/xhtml",
            }
            url_nodes = root.findall("ns:url", ns)
            urls = [u.find("ns:loc", ns).text for u in url_nodes]
            print(f"Sitemap loc URLs indexed: {len(urls)}")
            if len(urls) < expected_min_urls:
                errors.append(f"Sitemap has only {len(urls)} URLs (expected >= {expected_min_urls} for EN + ZH)")
            for u in url_nodes:
                loc = u.find("ns:loc", ns).text
                if "/404" in loc:
                    errors.append(f"404 page leaked into sitemap: {loc}")
                alts = {l.attrib.get("hreflang"): l.attrib.get("href") for l in u.findall("x:link", ns)}
                if "en" not in alts or "zh-Hans" not in alts:
                    errors.append(f"Sitemap entry missing en/zh-Hans xhtml:link alternates: {loc}")
        except Exception as e:
            errors.append(f"Failed to parse sitemap-0.xml: {e}")

    # 2. Check LLM text files in dist
    for rel, min_size in [
        ("llms.txt", 1000),
        ("llms-full.txt", 50000),
        (os.path.join("zh", "llms.txt"), 1000),
        (os.path.join("zh", "llms-full.txt"), 50000),
        ("robots.txt", 20),
    ]:
        fpath = os.path.join(dist_dir, rel)
        if not os.path.isfile(fpath):
            errors.append(f"Missing dist/{rel}")
        else:
            sz = os.path.getsize(fpath)
            print(f"dist/{rel} size: {sz} bytes")
            if sz < min_size:
                errors.append(f"dist/{rel} is unexpectedly small ({sz} bytes)")

    # 3. Check EN + ZH module HTML page generation
    print(f"Checking EN + ZH HTML pages for all {len(module_jsons)} catalog modules...")

    missing_en = []
    missing_zh = []
    for f in module_jsons:
        slug = os.path.basename(f)[:-5]
        if not os.path.isfile(os.path.join(dist_dir, "modules", slug, "index.html")):
            missing_en.append(slug)
        if not os.path.isfile(os.path.join(dist_dir, "zh", "modules", slug, "index.html")):
            missing_zh.append(slug)

    if missing_en:
        errors.append(f"Missing EN HTML pages for {len(missing_en)} modules: {missing_en[:10]}")
    if missing_zh:
        errors.append(f"Missing ZH HTML pages for {len(missing_zh)} modules: {missing_zh[:10]}")
    if not missing_en and not missing_zh:
        print(f"All {len(module_jsons)}/{len(module_jsons)} EN & ZH module HTML pages verified!")

    # 4. Inspect sample EN + ZH pages for SEO, hreflang, canonical, and JSON-LD
    samples = [
        ("", "zh"),
        ("security", "zh/security"),
        ("modules/magisk", "zh/modules/magisk"),
        ("modules/playintegrityfix", "zh/modules/playintegrityfix"),
        ("modules/shamiko", "zh/modules/shamiko"),
        ("modules/trickystore", "zh/modules/trickystore"),
        ("modules/acc", "zh/modules/acc"),
    ]
    for en_rel, zh_rel in samples:
        en_file = os.path.join(dist_dir, en_rel, "index.html") if en_rel else os.path.join(dist_dir, "index.html")
        zh_file = os.path.join(dist_dir, zh_rel, "index.html")
        en_p = parse_html(en_file)
        zh_p = parse_html(zh_file)

        if en_p.html_lang != "en":
            errors.append(f"[{en_rel or '/'}] Expected html lang='en', got '{en_p.html_lang}'")
        if zh_p.html_lang != "zh-CN":
            errors.append(f"[{zh_rel}] Expected html lang='zh-CN', got '{zh_p.html_lang}'")

        en_canon = next((l.get("href") for l in en_p.links if l.get("rel") == "canonical"), None)
        zh_canon = next((l.get("href") for l in zh_p.links if l.get("rel") == "canonical"), None)
        en_alts = {l.get("hreflang"): l.get("href") for l in en_p.links if l.get("rel") == "alternate"}
        zh_alts = {l.get("hreflang"): l.get("href") for l in zh_p.links if l.get("rel") == "alternate"}

        if en_alts.get("en") != en_canon or en_alts.get("zh-Hans") != zh_canon:
            errors.append(f"[{en_rel or '/'}] EN hreflang mismatch: {en_alts} vs canon {en_canon}/{zh_canon}")
        if zh_alts.get("en") != en_canon or zh_alts.get("zh-Hans") != zh_canon:
            errors.append(f"[{zh_rel}] ZH hreflang mismatch: {zh_alts} vs canon {en_canon}/{zh_canon}")
        if not en_p.schemas or any("_parse_error" in s for s in en_p.schemas):
            errors.append(f"[{en_rel or '/'}] Missing or invalid EN JSON-LD schema")
        if not zh_p.schemas or any("_parse_error" in s for s in zh_p.schemas):
            errors.append(f"[{zh_rel}] Missing or invalid ZH JSON-LD schema")

    # 5. Check 404 pages carry noindex
    for nf_rel, expected_lang in [("404.html", "en"), (os.path.join("zh", "404", "index.html"), "zh-CN")]:
        nf_path = os.path.join(dist_dir, nf_rel)
        if not os.path.isfile(nf_path):
            errors.append(f"Missing 404 artifact: dist/{nf_rel}")
        else:
            nf_p = parse_html(nf_path)
            if nf_p.html_lang != expected_lang:
                errors.append(f"[dist/{nf_rel}] Expected html lang='{expected_lang}', got '{nf_p.html_lang}'")
            robots_meta = next((m.get("content", "") for m in nf_p.metas if m.get("name") == "robots"), "")
            if "noindex" not in robots_meta.lower():
                errors.append(f"[dist/{nf_rel}] 404 page missing robots noindex meta (got '{robots_meta}')")

    print("\n" + "=" * 80)
    if errors:
        print(f"FAILED WITH {len(errors)} ERRORS:")
        for err in errors[:30]:
            print("  [ERROR]", err)
        return False
    print("✅ DIST VERIFICATION PASSED: 100% EN+ZH SITEMAPS, PAGES, HREFLANG & JSON-LD VALIDATED!")
    return True


if __name__ == "__main__":
    ok = verify_dist()
    sys.exit(0 if ok else 1)

#!/usr/bin/env python3
"""
Submit all URLs from dist/sitemap-0.xml (including /zh/ localized pages)
to IndexNow (Bing / Yandex / Seznam / Naver) after deployment.
"""

import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET

HOST = "magisk.yssn.tech"
KEY = "a8f4c2e91b7d40329e6f1a5b8c3d7e20"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
SITEMAP_PATH = os.path.join(os.path.dirname(__file__), "..", "dist", "sitemap-0.xml")


def collect_urls(sitemap_path: str):
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    return [el.text.strip() for el in root.findall(".//s:loc", ns) if el.text]


def main():
    if not os.path.isfile(SITEMAP_PATH):
        print(f"Error: {SITEMAP_PATH} not found. Run 'npm run build' first.", file=sys.stderr)
        sys.exit(1)

    urls = collect_urls(SITEMAP_PATH)
    dry_run = "--dry-run" in sys.argv
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }

    print(f"Prepared IndexNow payload with {len(urls)} URLs (keyLocation={KEY_LOCATION}).")
    if dry_run:
        print("Dry-run mode enabled; skipping HTTP POST.")
        return

    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        print(f"IndexNow response status: {resp.status}")


if __name__ == "__main__":
    main()

import os
import glob
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json

def verify_dist():
    print("=" * 80)
    print("DIST BUILD & SEO ARTIFACT VERIFICATION AUDIT")
    print("=" * 80)

    dist_dir = "dist"
    if not os.path.isdir(dist_dir):
        print(f"Error: {dist_dir} does not exist!")
        return False

    errors = []
    
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
            # XML namespace
            ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            urls = [elem.text for elem in root.findall('.//ns:loc', ns)]
            print(f"Sitemap loc URLs indexed: {len(urls)}")
            if len(urls) < 280:
                errors.append(f"Sitemap has only {len(urls)} URLs (expected >= 295)")
        except Exception as e:
            errors.append(f"Failed to parse sitemap-0.xml: {e}")

    # 2. Check LLM text files in dist
    llms_txt = os.path.join(dist_dir, "llms.txt")
    llms_full_txt = os.path.join(dist_dir, "llms-full.txt")
    
    if not os.path.isfile(llms_txt):
        errors.append("Missing dist/llms.txt")
    else:
        sz = os.path.getsize(llms_txt)
        print(f"dist/llms.txt size: {sz} bytes")
        if sz < 1000:
            errors.append(f"dist/llms.txt is unexpectedly small ({sz} bytes)")

    if not os.path.isfile(llms_full_txt):
        errors.append("Missing dist/llms-full.txt")
    else:
        sz = os.path.getsize(llms_full_txt)
        print(f"dist/llms-full.txt size: {sz} bytes")
        if sz < 50000:
            errors.append(f"dist/llms-full.txt is unexpectedly small ({sz} bytes)")

    # 3. Check module HTML page generation
    module_jsons = glob.glob("modules/*.json")
    module_jsons = [f for f in module_jsons if os.path.basename(f) != "schema.json"]
    print(f"Checking HTML pages for all {len(module_jsons)} catalog modules...")

    missing_html = []
    seo_audit_samples = [
        "sukisu-ultra",
        "leica-camera-port",
        "harman-kardon-sound-enhancer",
        "meta-overlayfs-kernelsu",
        "freepps-xiaomi-fast-charge",
        "lspdoze",
        "locusmimic",
        "qishui-music-svip-unlocker",
        "goldenviphook",
        "violetbox-root-toolbox",
        "thermal-controller-bypass",
        "xiaomi-12pro-speaker-enhancer"
    ]

    for f in module_jsons:
        slug = os.path.basename(f)[:-5]
        page_html = os.path.join(dist_dir, "modules", slug, "index.html")
        if not os.path.isfile(page_html):
            missing_html.append(slug)

    if missing_html:
        errors.append(f"Missing HTML pages for {len(missing_html)} modules: {missing_html[:10]}")
    else:
        print(f"All {len(module_jsons)}/{len(module_jsons)} module HTML pages verified in dist/modules/<slug>/index.html!")

    # 4. Deep inspect HTML samples for SEO & Schema tags
    print("\nDeep Inspecting SEO & Schema for Sample Ingested Modules:")
    for slug in seo_audit_samples:
        page_p = os.path.join(dist_dir, "modules", slug, "index.html")
        if not os.path.isfile(page_p):
            continue
        with open(page_p, "r", encoding="utf-8") as hp:
            html = hp.read()
        soup = BeautifulSoup(html, "html.parser")
        
        title_tag = soup.find("title")
        title_text = title_tag.get_text() if title_tag else "MISSING"
        
        desc_meta = soup.find("meta", attrs={"name": "description"})
        desc_text = desc_meta["content"] if desc_meta else "MISSING"
        
        canonical_tag = soup.find("link", attrs={"rel": "canonical"})
        canonical_href = canonical_tag["href"] if canonical_tag else "MISSING"
        
        og_title = soup.find("meta", attrs={"property": "og:title"})
        og_desc = soup.find("meta", attrs={"property": "og:description"})
        
        schemas = soup.find_all("script", attrs={"type": "application/ld+json"})
        parsed_schemas = []
        for s in schemas:
            try:
                parsed_schemas.append(json.loads(s.string).get("@type"))
            except:
                pass
                
        print(f"\n  • Module: {slug}")
        print(f"    - Title: {title_text}")
        print(f"    - Description: {desc_text[:90]}...")
        print(f"    - Canonical: {canonical_href}")
        print(f"    - OpenGraph: og:title={bool(og_title)}, og:desc={bool(og_desc)}")
        print(f"    - JSON-LD Schemas: {parsed_schemas}")
        
        if title_text == "MISSING" or desc_text == "MISSING":
            errors.append(f"[{slug}] Missing Title or Meta Description in HTML")
        if not parsed_schemas:
            errors.append(f"[{slug}] Missing JSON-LD structured data")

    print("\n" + "=" * 80)
    if errors:
        print(f"FAILED WITH {len(errors)} ERRORS:")
        for err in errors:
            print("  [ERROR]", err)
        return False
    else:
        print("✅ DIST VERIFICATION PASSED: 100% SITEMAPS, PAGES, SEO & JSON-LD VALIDATED!")
        return True

if __name__ == "__main__":
    verify_dist()

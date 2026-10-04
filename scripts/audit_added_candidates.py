import os
import json
import glob
import re
from PIL import Image

def audit_added():
    candidates_file = '/home/sentinel/wa-agy-bridge/workspaces/143371125416108/2026-10-04T10-37-39-617Z/candidates_list.md'
    with open(candidates_file, encoding='utf-8') as f:
        text = f.read()

    pattern = r'(\d+)\.\s+\*\*(.*?)\*\*\s+\((.*?)\)\s+-\s+Downloads:\s+([\d,]+)\s+Link:\s+https://apk\.magisk\.vip/app\.php\?id=(\d+)'
    matches = re.findall(pattern, text)

    modules = {}
    for f in sorted(glob.glob('modules/*.json')):
        if os.path.basename(f) != 'schema.json':
            with open(f, encoding='utf-8') as fp:
                d = json.load(fp)
                modules[d['id']] = d

    added_slugs = set()
    for num, name, ver, dls, app_id in matches:
        for slug, m in modules.items():
            dl = str(m.get('latestRelease', {}).get('downloadUrl', ''))
            if f'id={app_id}' in dl or f'id={app_id}&' in dl:
                added_slugs.add(slug)
            elif name.lower() in m.get('name', '').lower() or slug in name.lower():
                added_slugs.add(slug)

    added_slugs.update(['qishui-music-svip-unlocker', 'sukisu-ultra', 'fingerprintpay'])

    print(f"Total added candidate modules identified: {len(added_slugs)}")

    errors = []
    warnings = []
    seo_titles = set()

    for slug in sorted(added_slugs):
        if slug not in modules:
            errors.append(f"[{slug}] Slug not in modules/*.json")
            continue
        m = modules[slug]
        
        # 1. Icons check
        p1 = f"assets/icons/{slug}.png"
        p2 = f"public/assets/icons/{slug}.png"
        if not os.path.isfile(p1):
            errors.append(f"[{slug}] Missing icon in assets/icons/{slug}.png")
        else:
            try:
                with Image.open(p1) as im:
                    if im.size != (512, 512):
                        errors.append(f"[{slug}] Icon {p1} size {im.size} != (512, 512)")
                    if im.format != "PNG":
                        errors.append(f"[{slug}] Icon {p1} is {im.format} (expected PNG)")
            except Exception as e:
                errors.append(f"[{slug}] Icon {p1} error: {e}")
                
        if not os.path.isfile(p2):
            errors.append(f"[{slug}] Missing public icon in {p2}")
            
        # 2. Markdown guide check
        md_p = f"content/modules/{slug}.md"
        if not os.path.isfile(md_p):
            errors.append(f"[{slug}] Missing markdown doc {md_p}")
        else:
            with open(md_p, encoding='utf-8') as mfp:
                content = mfp.read()
                if len(content) < 400:
                    warnings.append(f"[{slug}] Short markdown doc ({len(content)} bytes)")
                if "```" not in content and "/" not in content:
                    warnings.append(f"[{slug}] Markdown lacks technical code blocks or paths")
                    
        # 3. SEO check
        seo = m.get("seo", {})
        title = seo.get("title", "").strip()
        desc = seo.get("description", "").strip()
        if not title:
            errors.append(f"[{slug}] Missing SEO title")
        elif len(title) < 20 or len(title) > 90:
            warnings.append(f"[{slug}] SEO title length ({len(title)}): {title}")
        if not desc:
            errors.append(f"[{slug}] Missing SEO description")
        elif len(desc) < 50 or len(desc) > 220:
            warnings.append(f"[{slug}] SEO description length ({len(desc)}): {desc}")
            
        if title in seo_titles:
            errors.append(f"[{slug}] Duplicate SEO title: '{title}'")
        seo_titles.add(title)
            
        # 4. Release check
        rel = m.get("latestRelease", {})
        dl = rel.get("downloadUrl", "")
        if not dl.startswith("http"):
            errors.append(f"[{slug}] Invalid downloadUrl: {dl}")
        if not rel.get("assetName"):
            errors.append(f"[{slug}] Missing assetName")

    print("\n--- Audit Results for Added Candidates ---")
    print(f"Total Verified: {len(added_slugs)}")
    print(f"Errors Found:   {len(errors)}")
    print(f"Warnings Found: {len(warnings)}")
    
    if errors:
        print("\nERRORS:")
        for e in errors:
            print("  ", e)
    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print("  ", w)

    if not errors:
        print("\n✅ ALL ADDED CANDIDATE MODULES PASSED WITH 0 ERRORS!")

if __name__ == '__main__':
    audit_added()

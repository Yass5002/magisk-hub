#!/usr/bin/env python3
"""
Comprehensive Validation Suite for Magisk Hub (EN + ZH):
1. Technical & Schema Integrity
2. Icons Parity & Dimensions (512x512 PNG)
3. SEO Titles, Descriptions, Keywords & Uniqueness (EN + ZH)
4. Release URLs & Source Authenticity
5. Category & Compatibility Mappings
6. Markdown Guide Richness & ZH Localization Parity
"""

import glob
import json
import os
import re
import sys
import yaml
from PIL import Image

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULES_DIR = os.path.join(REPO_ROOT, "modules")
ZH_MODULES_DIR = os.path.join(REPO_ROOT, "locales", "zh", "modules")
CONTENT_DIR = os.path.join(REPO_ROOT, "content", "modules")
ZH_CONTENT_DIR = os.path.join(REPO_ROOT, "content", "zh", "modules")
PUBLIC_ICONS_DIR = os.path.join(REPO_ROOT, "public", "assets", "icons")

ALLOWED_CATEGORIES = {
    "root-management",
    "performance-kernel",
    "system-environment",
    "customization-ui",
    "development-instrumentation",
    "system-utilities",
    "networking-proxies",
    "security-certificates",
    "xposed-runtime-hooks",
    "audio-dsp-acoustics",
    "system-typography-fonts",
    "battery-power-charging",
    "boot-animations-ui",
}

ALLOWED_PLATFORMS = {"Magisk", "KernelSU", "APatch", "LSPosed", "Shizuku", "Rootless"}
ALLOWED_SOFTWARE_TYPES = {"flashable-module", "xposed-module", "standalone-app", "kernel-module"}
CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def parse_frontmatter(md_text: str):
    if not md_text.startswith("---"):
        return None, md_text
    parts = md_text.split("---", 2)
    if len(parts) < 3:
        return None, md_text
    return yaml.safe_load(parts[1]), parts[2]


def run_audit():
    print("=" * 80)
    print("MAGISK HUB COMPREHENSIVE SEO, LLM & I18N DISCOVERY AUDIT")
    print("=" * 80)

    module_files = sorted(glob.glob(os.path.join(MODULES_DIR, "*.json")))
    module_files = [f for f in module_files if os.path.basename(f) != "schema.json"]
    total = len(module_files)
    print(f"Total modules to audit: {total}\n")

    errors = []
    warnings = []

    seo_titles = {}
    seo_descriptions = {}
    zh_seo_titles = {}
    zh_seo_descriptions = {}
    category_counts = {c: 0 for c in ALLOWED_CATEGORIES}
    platform_counts = {p: 0 for p in ALLOWED_PLATFORMS}
    software_type_counts = {s: 0 for s in ALLOWED_SOFTWARE_TYPES}
    source_type_counts = {"github": 0, "community": 0}

    for fpath in module_files:
        fname = os.path.basename(fpath)
        slug = fname[:-5]

        # 1. JSON Parsing
        try:
            with open(fpath, "r", encoding="utf-8") as fp:
                data = json.load(fp)
        except Exception as e:
            errors.append(f"[{slug}] Corrupted JSON: {e}")
            continue

        mid = data.get("id")
        if mid != slug:
            errors.append(f"[{slug}] Slug mismatch: id '{mid}' != filename '{slug}'")

        # 2. Markdown Guide Parity (EN)
        md_path = os.path.join(CONTENT_DIR, f"{slug}.md")
        en_fm = None
        if not os.path.isfile(md_path):
            errors.append(f"[{slug}] Missing markdown content guide at content/modules/{slug}.md")
        else:
            with open(md_path, "r", encoding="utf-8") as mfp:
                md_text = mfp.read()
            if len(md_text) < 400:
                warnings.append(f"[{slug}] Markdown content guide is very brief ({len(md_text)} chars)")
            if "```" not in md_text and "/" not in md_text:
                warnings.append(f"[{slug}] Markdown guide lacks technical commands or file paths")
            try:
                en_fm, en_body = parse_frontmatter(md_text)
                if not isinstance(en_fm, dict):
                    errors.append(f"[{slug}] Missing EN YAML frontmatter")
                else:
                    if not str(en_fm.get("title", "")).strip():
                        errors.append(f"[{slug}] EN MD frontmatter title is empty")
                    if not str(en_fm.get("description", "")).strip():
                        errors.append(f"[{slug}] EN MD frontmatter description is empty")
                if not en_body.strip():
                    errors.append(f"[{slug}] EN MD body is empty")
            except Exception as e:
                errors.append(f"[{slug}] Invalid EN frontmatter YAML: {e}")

        en_desc = (data.get("description") or "").strip()
        if CJK_RE.search(en_desc):
            errors.append(f"[{slug}] EN JSON description contains CJK characters")
        if "active root module" in en_desc.lower():
            errors.append(f"[{slug}] EN JSON description uses placeholder boilerplate")

        # 3. Category & Taxonomy
        cat = data.get("category")
        if cat not in ALLOWED_CATEGORIES:
            errors.append(f"[{slug}] Invalid category: '{cat}'")
        else:
            category_counts[cat] += 1

        stype = data.get("softwareType")
        if stype not in ALLOWED_SOFTWARE_TYPES:
            errors.append(f"[{slug}] Invalid softwareType: '{stype}'")
        else:
            software_type_counts[stype] += 1

        compat = data.get("compatibility", [])
        if not compat or not isinstance(compat, list):
            errors.append(f"[{slug}] Missing or invalid compatibility array")
        else:
            for p in compat:
                if p not in ALLOWED_PLATFORMS:
                    errors.append(f"[{slug}] Invalid compatibility platform: '{p}'")
                else:
                    platform_counts[p] += 1

        # 4. Source & Upstream Authenticity
        srctype = data.get("sourceType", "github" if data.get("repo") else "community")
        source_type_counts[srctype] = source_type_counts.get(srctype, 0) + 1

        if srctype == "github":
            repo = data.get("repo")
            if not repo or not re.match(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$", repo):
                errors.append(f"[{slug}] GitHub module has invalid repo string: '{repo}'")
        elif srctype == "community":
            s_url = data.get("sourceUrl")
            if s_url and ("github.com" in s_url and "Xposed-Modules-Repo" not in s_url):
                warnings.append(f"[{slug}] Community module has external GitHub sourceUrl: '{s_url}'")

        # 5. Download URL Integrity
        dl_url = data.get("latestRelease", {}).get("downloadUrl", "")
        if not dl_url.startswith("http://") and not dl_url.startswith("https://"):
            errors.append(f"[{slug}] Invalid downloadUrl: '{dl_url}'")
        asset_name = data.get("latestRelease", {}).get("assetName", "")
        if not asset_name:
            errors.append(f"[{slug}] Missing latestRelease.assetName")

        # 6. Icons Audit (warn on pre-existing non-512px dimensions/SVG formats; error only if file missing)
        icon_field = data.get("icon")
        expected_icon = f"assets/icons/{slug}.png"
        if icon_field is not None:
            if icon_field != expected_icon:
                errors.append(f"[{slug}] Icon field '{icon_field}' does not match expected '{expected_icon}'")
            p1 = os.path.join(REPO_ROOT, expected_icon)
            p2 = os.path.join(PUBLIC_ICONS_DIR, f"{slug}.png")
            if not os.path.isfile(p1):
                errors.append(f"[{slug}] Missing icon in assets/icons/{slug}.png")
            else:
                try:
                    with Image.open(p1) as im:
                        if im.format != "PNG":
                            warnings.append(f"[{slug}] Icon {expected_icon} is not PNG (format={im.format})")
                        if im.size != (512, 512):
                            warnings.append(f"[{slug}] Icon {expected_icon} dimensions {im.size} != (512, 512)")
                except Exception as e:
                    warnings.append(f"[{slug}] Non-raster/unrecognized icon image {p1}: {e}")
            if not os.path.isfile(p2):
                errors.append(f"[{slug}] Missing public icon in public/assets/icons/{slug}.png")

        # 7. EN SEO Audit
        seo = data.get("seo", {})
        title = seo.get("title", "").strip()
        desc = seo.get("description", "").strip()

        if not title:
            errors.append(f"[{slug}] Missing seo.title")
        elif CJK_RE.search(title):
            errors.append(f"[{slug}] EN seo.title contains CJK characters")
        elif len(title) < 15:
            errors.append(f"[{slug}] SEO title too short ({len(title)} chars): '{title}'")
        elif len(title) > 90:
            warnings.append(f"[{slug}] SEO title slightly long ({len(title)} chars): '{title}'")

        if not desc:
            errors.append(f"[{slug}] Missing seo.description")
        elif CJK_RE.search(desc) or "active root module" in desc.lower():
            errors.append(f"[{slug}] EN seo.description contains CJK characters or boilerplate")
        elif len(desc) < 35:
            errors.append(f"[{slug}] SEO description too short ({len(desc)} chars): '{desc}'")
        elif len(desc) > 220:
            warnings.append(f"[{slug}] SEO description slightly long ({len(desc)} chars): '{desc}'")

        if title in seo_titles:
            errors.append(f"[{slug}] Duplicate SEO title with [{seo_titles[title]}]: '{title}'")
        else:
            seo_titles[title] = slug

        if desc in seo_descriptions:
            warnings.append(f"[{slug}] Duplicate SEO description with [{seo_descriptions[desc]}]")
        else:
            seo_descriptions[desc] = slug

        # 8. ZH Metadata & Markdown Localization Audit
        zh_json_path = os.path.join(ZH_MODULES_DIR, f"{slug}.json")
        if not os.path.isfile(zh_json_path):
            errors.append(f"[{slug}] Missing ZH metadata at locales/zh/modules/{slug}.json")
        else:
            try:
                with open(zh_json_path, "r", encoding="utf-8") as zfp:
                    zh_data = json.load(zfp)
                if zh_data.get("id") != slug:
                    errors.append(f"[{slug}] ZH JSON id mismatch: '{zh_data.get('id')}'")
                zh_desc = (zh_data.get("description") or "").strip()
                if not CJK_RE.search(zh_desc):
                    errors.append(f"[{slug}] ZH JSON description lacks Chinese text")
                zh_seo = zh_data.get("seo") or {}
                zh_title = (zh_seo.get("title") or "").strip()
                zh_sdesc = (zh_seo.get("description") or "").strip()
                if not zh_title or not CJK_RE.search(zh_title):
                    errors.append(f"[{slug}] Missing or non-Chinese ZH seo.title")
                elif zh_title in zh_seo_titles:
                    errors.append(f"[{slug}] Duplicate ZH SEO title with [{zh_seo_titles[zh_title]}]")
                else:
                    zh_seo_titles[zh_title] = slug
                if not zh_sdesc or not CJK_RE.search(zh_sdesc):
                    errors.append(f"[{slug}] Missing or non-Chinese ZH seo.description")
                elif zh_sdesc in zh_seo_descriptions:
                    warnings.append(f"[{slug}] Duplicate ZH SEO description with [{zh_seo_descriptions[zh_sdesc]}]")
                else:
                    zh_seo_descriptions[zh_sdesc] = slug
                if not zh_data.get("searchAliases"):
                    errors.append(f"[{slug}] Missing ZH searchAliases")
            except Exception as e:
                errors.append(f"[{slug}] Corrupted ZH JSON: {e}")

        zh_md_path = os.path.join(ZH_CONTENT_DIR, f"{slug}.md")
        if not os.path.isfile(zh_md_path):
            errors.append(f"[{slug}] Missing ZH markdown guide at content/zh/modules/{slug}.md")
        else:
            with open(zh_md_path, "r", encoding="utf-8") as zmfp:
                zh_md_text = zmfp.read()
            try:
                zh_fm, zh_body = parse_frontmatter(zh_md_text)
                if not isinstance(zh_fm, dict):
                    errors.append(f"[{slug}] Missing ZH YAML frontmatter")
                else:
                    if zh_fm.get("id") != slug:
                        errors.append(f"[{slug}] ZH MD id mismatch: '{zh_fm.get('id')}'")
                    if zh_fm.get("category") != cat:
                        errors.append(f"[{slug}] ZH MD category mismatch: '{zh_fm.get('category')}' != '{cat}'")
                    if en_fm and zh_fm.get("configPaths", []) != en_fm.get("configPaths", []):
                        errors.append(f"[{slug}] ZH MD configPaths altered vs EN")
                    if not CJK_RE.search(str(zh_fm.get("title", ""))):
                        errors.append(f"[{slug}] ZH MD frontmatter title lacks Chinese text")
                    if not CJK_RE.search(str(zh_fm.get("description", ""))):
                        errors.append(f"[{slug}] ZH MD frontmatter description lacks Chinese text")
                if not CJK_RE.search(zh_body):
                    errors.append(f"[{slug}] ZH MD body lacks Chinese text")
            except Exception as e:
                errors.append(f"[{slug}] Invalid ZH frontmatter YAML: {e}")

    print("-" * 80)
    print("AUDIT RESULTS SUMMARY")
    print("-" * 80)
    print(f"Total Modules Checked: {total}")
    print(f"Total Errors Found:    {len(errors)}")
    print(f"Total Warnings:        {len(warnings)}\n")

    print("Distribution by Category:")
    for c, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  - {c}: {count} modules")

    print("\nDistribution by Software Type:")
    for s, count in sorted(software_type_counts.items(), key=lambda x: -x[1]):
        print(f"  - {s}: {count} modules")

    print("\nDistribution by Platform Compatibility:")
    for p, count in sorted(platform_counts.items(), key=lambda x: -x[1]):
        print(f"  - {p}: {count} modules")

    print("\nDistribution by Source Origin:")
    for src, count in source_type_counts.items():
        print(f"  - {src}: {count} modules")

    if warnings:
        print("\n" + "=" * 40 + " WARNINGS " + "=" * 40)
        for w in warnings[:25]:
            print(f"  [WARN] {w}")
        if len(warnings) > 25:
            print(f"  ... and {len(warnings) - 25} more warnings.")

    if errors:
        print("\n" + "=" * 40 + " ERRORS " + "=" * 40)
        for err in errors[:50]:
            print(f"  [ERROR] {err}")
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more errors.")
        print("=" * 80)
        sys.exit(1)
    else:
        print(f"\n✅ ALL {total} MODULES PASSED EN + ZH TECHNICAL, SEO, AND DISCOVERY CHECKS WITH 0 ERRORS!")
        print("=" * 80)
        sys.exit(0)


if __name__ == "__main__":
    run_audit()

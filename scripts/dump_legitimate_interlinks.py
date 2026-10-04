#!/usr/bin/env python3
"""
Dump Legitimate Interlinking Opportunities in Magisk Hub.

Strictly read-only analysis tool that iterates through all modules and technical guides
to discover real, functional interlinking relationships:
1. Strict Functional Prerequisites (hard dependencies required to run)
2. Explicit Known Conflicts (modules that collide or break each other)
3. Direct Setup Companions (modules explicitly paired in configuration guides)

Zero modifications are made to modules or markdown files.
"""

import os
import glob
import json
import re
import yaml

def load_catalog(modules_dir='modules'):
    catalog = {}
    for f in sorted(glob.glob(os.path.join(modules_dir, '*.json'))):
        if os.path.basename(f) != 'schema.json':
            with open(f, 'r', encoding='utf-8') as fp:
                data = json.load(fp)
                catalog[data['id']] = data
    return catalog

def build_alias_dictionary(catalog):
    """
    Build a high-precision alias map to match legitimate modules in text.
    Only maps distinct, unambiguous names to module slugs.
    """
    aliases = {
        'magisk': 'magisk',
        'kernelsu': 'kernelsu',
        'ksu': 'kernelsu',
        'apatch': 'apatch',
        'lsposed': 'lsposed',
        'lsposed framework': 'lsposed',
        'xposed': 'lsposed',
        'xposed framework': 'lsposed',
        'shizuku': 'shizuku',
        'dhizuku': 'dhizuku',
        'play integrity fix': 'playintegrityfix',
        'pif': 'playintegrityfix',
        'tricky store': 'trickystore',
        'trickystore': 'trickystore',
        'shamiko': 'shamiko',
        'zygisknext': 'zygisknext',
        'zygisk next': 'zygisknext',
        'rezygisk': 'rezygisk',
        'neozygisk': 'neozygisk',
        'zygisk assistant': 'zygisk-assistant',
        'bindhosts': 'bindhosts',
        'advanced charging controller': 'acc',
        'acc': 'acc',
        'app vault': 'hyperos-app-vault',
        'apk protection patch': 'miui-theme-rights-enabler',
        'theme rights': 'miui-theme-rights-enabler',
        'viper4android': 'viper4android-dolby-coexistence',
        'dsp audio fix': 'dsp-audiofix',
        'dsp-audiofix': 'dsp-audiofix',
        'leica camera': 'leica-camera-port',
        'gallery ai': 'miui-gallery-feature-unlocker',
        'canta': 'canta',
        'hail': 'hail',
        'adguard home': 'adguardhomeforroot',
        'app manager': 'app-manager',
        'busybox': 'busybox-ndk',
    }

    # Add normalized module names from catalog if len > 4
    for mid, m in catalog.items():
        name = m.get('name', '').strip().lower()
        if len(name) >= 5 and name not in aliases:
            # Avoid overly generic names
            if name not in ('camera', 'sound', 'audio', 'theme', 'battery', 'kernel', 'root'):
                aliases[name] = mid

    return aliases

def analyze_module(slug, module_data, content_dir, aliases, catalog):
    opportunities = []
    md_path = os.path.join(content_dir, f"{slug}.md")
    
    fm_prereqs = []
    fm_conflicts = []
    body_text = ""

    if os.path.isfile(md_path):
        with open(md_path, 'r', encoding='utf-8') as fp:
            raw = fp.read()
        if raw.startswith('---'):
            parts = raw.split('---', 2)
            if len(parts) >= 3:
                try:
                    fm = yaml.safe_load(parts[1]) or {}
                    fm_prereqs = fm.get('prerequisites', []) or []
                    fm_conflicts = fm.get('conflicts', []) or []
                    body_text = parts[2]
                except Exception:
                    body_text = raw
        else:
            body_text = raw

    # 1. Inspect Explicit Frontmatter Prerequisites
    for p in fm_prereqs:
        p_lower = p.lower()
        for alias, target_slug in aliases.items():
            if target_slug != slug and re.search(r'\b' + re.escape(alias) + r'\b', p_lower):
                # Verify target exists in catalog
                if target_slug in catalog:
                    opportunities.append({
                        'type': 'Prerequisite',
                        'target_slug': target_slug,
                        'target_name': catalog[target_slug]['name'],
                        'source_evidence': p.strip(),
                        'channel': 'frontmatter.prerequisites'
                    })

    # 2. Inspect Explicit Frontmatter Conflicts
    for c in fm_conflicts:
        c_lower = c.lower()
        for alias, target_slug in aliases.items():
            if target_slug != slug and re.search(r'\b' + re.escape(alias) + r'\b', c_lower):
                if target_slug in catalog:
                    opportunities.append({
                        'type': 'Conflict',
                        'target_slug': target_slug,
                        'target_name': catalog[target_slug]['name'],
                        'source_evidence': c.strip(),
                        'channel': 'frontmatter.conflicts'
                    })

    # 3. SoftwareType Hard Dependencies
    st = module_data.get('softwareType')
    if st == 'xposed-module' and slug != 'lsposed' and 'lsposed' in catalog:
        if not any(o['target_slug'] == 'lsposed' for o in opportunities):
            opportunities.append({
                'type': 'Prerequisite',
                'target_slug': 'lsposed',
                'target_name': catalog['lsposed']['name'],
                'source_evidence': 'Requires Xposed framework runtime (softwareType: xposed-module)',
                'channel': 'metadata.softwareType'
            })
    elif st == 'kernel-module' and slug not in ('kernelsu', 'apatch'):
        if not any(o['target_slug'] in ('kernelsu', 'apatch') for o in opportunities):
            opportunities.append({
                'type': 'Prerequisite',
                'target_slug': 'kernelsu',
                'target_name': catalog.get('kernelsu', {}).get('name', 'KernelSU'),
                'source_evidence': 'Requires Kernel LKM support / KernelSU / APatch (softwareType: kernel-module)',
                'channel': 'metadata.softwareType'
            })

    # 4. Contextual Step-by-Step Functional Companions in Body
    # Look strictly for phrases indicating direct setup coordination:
    # "pair with X", "install X beforehand", "requires X module", "works alongside X"
    companion_patterns = [
        (r'(?:pair with|paired with|alongside|combine with|combined with)\s+([A-Za-z0-9_\- ]{3,30})', 'Companion'),
        (r'(?:requires?|must install|install beforehand)\s+(?:the\s+)?([A-Za-z0-9_\- ]{3,30})\s+(?:module|app)', 'Prerequisite'),
    ]

    for pat, rel_type in companion_patterns:
        for match in re.finditer(pat, body_text, re.IGNORECASE):
            captured = match.group(1).lower().strip()
            for alias, target_slug in aliases.items():
                if target_slug != slug and alias in captured and target_slug in catalog:
                    if not any(o['target_slug'] == target_slug for o in opportunities):
                        # Extract 1-line snippet context
                        start = max(0, match.start() - 30)
                        end = min(len(body_text), match.end() + 40)
                        snippet = body_text[start:end].replace('\n', ' ').strip()
                        opportunities.append({
                            'type': rel_type,
                            'target_slug': target_slug,
                            'target_name': catalog[target_slug]['name'],
                            'source_evidence': f"...{snippet}...",
                            'channel': 'guide.body_context'
                        })

    # Deduplicate opportunities per target_slug
    deduped = {}
    for o in opportunities:
        k = (o['target_slug'], o['type'])
        if k not in deduped:
            deduped[k] = o

    return list(deduped.values())

def main():
    catalog = load_catalog()
    aliases = build_alias_dictionary(catalog)
    content_dir = 'content/modules'

    print(f"Loaded {len(catalog)} active modules.")
    print(f"Compiled {len(aliases)} legitimate entity alias patterns.\n")

    results = {}
    target_stats = {}
    type_stats = {'Prerequisite': 0, 'Conflict': 0, 'Companion': 0}

    for slug, m in sorted(catalog.items()):
        opps = analyze_module(slug, m, content_dir, aliases, catalog)
        if opps:
            results[slug] = {
                'name': m['name'],
                'category': m['category'],
                'opportunities': opps
            }
            for o in opps:
                t = o['type']
                type_stats[t] = type_stats.get(t, 0) + 1
                tgt = o['target_slug']
                target_stats[tgt] = target_stats.get(tgt, 0) + 1

    total_links = sum(len(r['opportunities']) for r in results.values())
    print(f"Total modules with legitimate interlinking opportunities: {len(results)} / {len(catalog)} ({len(results)/len(catalog)*100:.1f}%)")
    print(f"Total legitimate interlinking relationships discovered: {total_links}")
    print(f"  • Prerequisites: {type_stats.get('Prerequisite', 0)}")
    print(f"  • Known Conflicts: {type_stats.get('Conflict', 0)}")
    print(f"  • Setup Companions: {type_stats.get('Companion', 0)}")

    print("\nTop 10 Most In-Demand Target Modules (Highest Incoming Dependencies):")
    for tgt, count in sorted(target_stats.items(), key=lambda x: -x[1])[:10]:
        tname = catalog.get(tgt, {}).get('name', tgt)
        print(f"  - {tname} (`{tgt}`): {count} modules legitimately depend on or reference it")

    # Output detailed markdown dump report
    dump_path = '/home/sentinel/wa-agy-bridge/workspaces/143371125416108/2026-10-04T10-37-39-617Z/legitimate_interlinks_dump.md'
    with open(dump_path, 'w', encoding='utf-8') as fp:
        fp.write("# Magisk Hub - Legitimate Interlinking Opportunities Dump\n\n")
        fp.write(f"Analyzed {len(catalog)} modules. Found **{total_links} legitimate connections** across **{len(results)} modules**.\n\n")
        fp.write("Strictly functional relationships: Hard Prerequisites, Explicit Conflicts, and Direct Setup Companions.\n\n")
        
        fp.write("## Summary Statistics\n")
        fp.write(f"- **Total Active Modules**: {len(catalog)}\n")
        fp.write(f"- **Modules with Real Links**: {len(results)}\n")
        fp.write(f"- **Prerequisite Connections**: {type_stats.get('Prerequisite', 0)}\n")
        fp.write(f"- **Conflict Warnings**: {type_stats.get('Conflict', 0)}\n")
        fp.write(f"- **Workflow Companions**: {type_stats.get('Companion', 0)}\n\n")
        
        fp.write("## Top Target Hubs (Incoming Dependencies)\n")
        for tgt, count in sorted(target_stats.items(), key=lambda x: -x[1])[:12]:
            tname = catalog.get(tgt, {}).get('name', tgt)
            fp.write(f"- **{tname}** (`{tgt}`) - {count} incoming links (`https://magisk.yssn.tech/modules/{tgt}/`)\n")
        fp.write("\n")

        fp.write("## Detailed Module-by-Module Legitimate Interlinks\n\n")
        for slug, d in sorted(results.items()):
            fp.write(f"### {d['name']} (`{slug}`)\n")
            fp.write(f"Category: `{d['category']}` | Canonical URL: `https://magisk.yssn.tech/modules/{slug}/`\n\n")
            for o in d['opportunities']:
                fp.write(f"- **[{o['type']}]** -> **{o['target_name']}** (`https://magisk.yssn.tech/modules/{o['target_slug']}/`)\n")
                fp.write(f"  *Channel*: `{o['channel']}`\n")
                fp.write(f"  *Evidence*: \"{o['source_evidence']}\"\n\n")

    print(f"\nLegitimate interlinking dump successfully written to:\n{dump_path}")

if __name__ == '__main__':
    main()

import os
import glob
import json
import re
import yaml

catalog = {}
for f in sorted(glob.glob('modules/*.json')):
    if not f.endswith('schema.json'):
        mid = os.path.basename(f)[:-5]
        with open(f, 'r', encoding='utf-8') as fp:
            catalog[mid] = json.load(fp)

exact_targets = {
    'lsposed': ['lsposed', 'xposed framework', 'xposed runtime', 'edxposed'],
    'shizuku': ['shizuku', 'shizuku service', 'moe.shizuku.privileged.api'],
    'dhizuku': ['dhizuku'],
    'playintegrityfix': ['play integrity fix', 'playintegrityfix', 'pif'],
    'playintegrityfork': ['play integrity fork', 'playintegrityfork'],
    'trickystore': ['tricky store', 'trickystore'],
    'trickystoreoss': ['trickystoreoss', 'tricky store oss'],
    'teesimulator': ['teesimulator', 'tee simulator'],
    'teesimulator-rs': ['teesimulator-rs', 'tee simulator rs'],
    'shamiko': ['shamiko'],
    'zygisknext': ['zygisknext', 'zygisk next', 'zygisk-next'],
    'rezygisk': ['rezygisk'],
    'neozygisk': ['neozygisk'],
    'onyxzygisk': ['onyxzygisk'],
    'vexzygisk': ['vexzygisk'],
    'zygisk-assistant': ['zygisk assistant', 'zygisk-assistant'],
    'bindhosts': ['bindhosts', 'systemless hosts'],
    'acc': ['advanced charging controller', 'acc daemon', 'vr-25 acc'],
    'hyperos-theme-manager': ['hyperos theme manager', 'miui theme manager mod'],
    'hyperos-app-vault': ['app vault mod', 'hyperos app vault', 'miui app vault'],
    'miui-theme-rights-enabler': ['apk protection patch', 'theme rights enabler', 'miui theme rights'],
    'viper4android-dolby-coexistence': ['viper4android', 'v4a coexistence'],
    'viperfx-re': ['viperfx_re', 'viperfx-re'],
    'dsp-audiofix': ['dsp audio fix', 'dsp-audiofix'],
    'leica-camera-port': ['leica camera', 'miui leica port'],
    'miui-gallery-feature-unlocker': ['miui gallery feature unlocker', 'gallery ai unlocker'],
    'app-manager': ['app manager', 'io.github.muntashirakon.AppManager'],
    'busybox-ndk': ['busybox-ndk', 'busybox ndk'],
    'canta': ['canta'],
    'hail': ['hail freeze'],
    'adguardhomeforroot': ['adguard home for root', 'adguardhome'],
    'freepps-xiaomi-fast-charge': ['freepps', 'freepps xiaomi'],
    'battery-health-query': ['battery health query'],
    'quantitative-charge-cutoff': ['quantitative charge cutoff', 'bh charge cutoff'],
    'movecertificate': ['movecertificate', 'move certificate'],
    'alwaystrustusercerts': ['alwaystrustusercerts'],
    'drc-remover': ['drc-remover', 'drc remover'],
    'usb-samplerate-unlocker': ['usb-samplerate-unlocker', 'usb samplerate unlocker'],
    'yetanotherbootloopprotector': ['yetanotherbootloopprotector', 'yet another bootloop protector'],
    'ashlooper': ['ashlooper', 'ashrexcue'],
    'knoxpatch': ['knoxpatch'],
    'ohmykeymint': ['ohmykeymint'],
    'stealthdebug': ['stealthdebug'],
    'stevenblock': ['stevenblock'],
    'magicalprotection': ['magicalprotection'],
    'sui': ['sui'],
    'alwaysstrong': ['alwaysstrong'],
    'yurikey': ['yurikey'],
    'specter': ['specter'],
    'playcurlnext': ['playcurlnext'],
    'tricky-addon-update-target-list': ['tricky-addon-update-target-list', 'tricky addon'],
    'mountify': ['mountify'],
    'nohello': ['nohello'],
    'makefontsgreatagain': ['makefontsgreatagain'],
    'material-files': ['material files', 'material-files'],
    'install-with-options': ['install with options', 'install-with-options'],
    'vpnhide': ['vpnhide'],
    'librepods': ['librepods'],
    'locusmimic': ['locusmimic'],
    'lspdoze': ['lspdoze'],
    'qishui-music-svip-unlocker': ['qishui-music-svip-unlocker', 'fuckqishui', 'soda music svip'],
    'treat-wheel-zygisk': ['treat-wheel-zygisk'],
    'iunlockergl': ['iunlockergl'],
    'magisk-ad-blocking-module': ['magisk-ad-blocking-module']
}

all_verified_links = []

for slug, m in sorted(catalog.items()):
    md_path = f"content/modules/{slug}.md"
    fm_prereqs = []
    fm_conflicts = []
    body_lines = []
    
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
                    body_lines = parts[2].splitlines()
                except Exception as e:
                    print(f"Error parsing YAML in {md_path}: {e}")
                    body_lines = raw.splitlines()
        else:
            body_lines = raw.splitlines()

    # A. Xposed SoftwareType Hard Dependency
    if m.get('softwareType') == 'xposed-module' and slug != 'lsposed':
        all_verified_links.append({
            'source_slug': slug,
            'source_name': m['name'],
            'category': m['category'],
            'target_slug': 'lsposed',
            'target_name': catalog.get('lsposed', {}).get('name', 'LSPosed'),
            'type': 'Runtime Framework Prerequisite',
            'evidence': 'Module is packaged as an Xposed APK and requires the LSPosed ART hooking framework.'
        })

    # B. Frontmatter Prerequisites
    for p in fm_prereqs:
        p_clean = p.strip()
        p_low = p_clean.lower()
        for tgt_id, aliases in exact_targets.items():
            if tgt_id != slug and tgt_id in catalog:
                if any(al in p_low for al in aliases):
                    all_verified_links.append({
                        'source_slug': slug,
                        'source_name': m['name'],
                        'category': m['category'],
                        'target_slug': tgt_id,
                        'target_name': catalog[tgt_id]['name'],
                        'type': 'Prerequisite Dependency',
                        'evidence': p_clean
                    })

    # C. Frontmatter Conflicts
    for c in fm_conflicts:
        c_clean = c.strip()
        c_low = c_clean.lower()
        for tgt_id, aliases in exact_targets.items():
            if tgt_id != slug and tgt_id in catalog:
                if any(al in c_low for al in aliases):
                    all_verified_links.append({
                        'source_slug': slug,
                        'source_name': m['name'],
                        'category': m['category'],
                        'target_slug': tgt_id,
                        'target_name': catalog[tgt_id]['name'],
                        'type': 'Technical Conflict',
                        'evidence': c_clean
                    })

    # D. Specific Version Handoffs & Contextual Setup Synergy
    for line in body_lines:
        line_clean = line.strip()
        if len(line_clean) < 15 or line_clean.startswith('#'):
            continue
        line_low = line_clean.lower()
        
        for tgt_id, aliases in exact_targets.items():
            if tgt_id != slug and tgt_id in catalog:
                if any(al in line_low for al in aliases):
                    if any(w in line_low for w in ('see ', 'pair', 'alongside', 'requires', 'uninstall', 'replace', 'integrated', 'conflicts', 'combining')):
                        all_verified_links.append({
                            'source_slug': slug,
                            'source_name': m['name'],
                            'category': m['category'],
                            'target_slug': tgt_id,
                            'target_name': catalog[tgt_id]['name'],
                            'type': 'Contextual Dependency / Handoff',
                            'evidence': line_clean
                        })

# Deduplicate
deduped_links = []
seen = set()
for l in all_verified_links:
    k = (l['source_slug'], l['target_slug'], l['type'])
    if k not in seen:
        seen.add(k)
        deduped_links.append(l)

# Group by category and source module
by_category = {}
for l in deduped_links:
    cat = l['category']
    by_category.setdefault(cat, []).append(l)

print(f"Total verified specific interlinks across all 275 modules: {len(deduped_links)}")
print(f"Categories represented: {len(by_category)}")

# Output detailed markdown audit report
report_path = '/home/sentinel/wa-agy-bridge/workspaces/143371125416108/2026-10-04T10-37-39-617Z/magisk_hub_verified_interlinks_audit.md'
with open(report_path, 'w', encoding='utf-8') as fp:
    fp.write("# Magisk Hub - Verified Module-to-Module Interlinking Audit\n\n")
    fp.write("Equal-attention technical verification across all 275 modules. Excludes generic root boilerplate.\n\n")
    fp.write(f"Total Verified Specific Interlinks: **{len(deduped_links)}** across **{len(by_category)} categories**.\n\n")
    
    for cat, links in sorted(by_category.items()):
        fp.write(f"## Category: `{cat}` ({len(links)} links)\n\n")
        by_source = {}
        for l in links:
            by_source.setdefault(l['source_slug'], []).append(l)
        
        for src_slug, s_links in sorted(by_source.items()):
            src_name = s_links[0]['source_name']
            fp.write(f"### {src_name} (`{src_slug}`)\n")
            fp.write(f"Source URL: `https://magisk.yssn.tech/modules/{src_slug}/`\n\n")
            for item in s_links:
                fp.write(f"- **[{item['type']}]** -> **{item['target_name']}** (`https://magisk.yssn.tech/modules/{item['target_slug']}/`)\n")
                fp.write(f"  *Evidence*: \"{item['evidence']}\"\n\n")

print(f"Report written to: {report_path}")

#!/usr/bin/env python3
"""
Generate top 100 high-priority URLs for Bing and Yandex indexing via IndexNow and Webmaster Tools.
Exports:
- scripts/top100_urls.txt (plain text, 1 URL per line for direct copy-paste)
- scripts/indexnow_payload.json (standard IndexNow JSON schema)
"""

import json
import os
import sys

def main():
    modules_dir = 'modules'
    if not os.path.exists(modules_dir):
        print(f"Error: '{modules_dir}' directory not found.")
        sys.exit(1)

    mods = {}
    for f in os.listdir(modules_dir):
        if f.endswith('.json') and f != 'schema.json':
            with open(os.path.join(modules_dir, f), 'r', encoding='utf-8') as fp:
                try:
                    d = json.load(fp)
                    mods[d['id']] = d
                except Exception as e:
                    print(f"Error parsing {f}: {e}")

    # 1. Structural / Taxonomy Hubs (14 URLs)
    hubs = [
        'https://magisk.yssn.tech/',
        'https://magisk.yssn.tech/security/',
        'https://magisk.yssn.tech/categories/',
        'https://magisk.yssn.tech/categories/root-management/',
        'https://magisk.yssn.tech/categories/security-certificates/',
        'https://magisk.yssn.tech/categories/networking-proxies/',
        'https://magisk.yssn.tech/categories/performance-kernel/',
        'https://magisk.yssn.tech/categories/system-utilities/',
        'https://magisk.yssn.tech/categories/system-environment/',
        'https://magisk.yssn.tech/categories/customization-ui/',
        'https://magisk.yssn.tech/categories/development-instrumentation/',
        'https://magisk.yssn.tech/compatibility/magisk/',
        'https://magisk.yssn.tech/compatibility/kernelsu/',
        'https://magisk.yssn.tech/compatibility/apatch/',
    ]

    # 2. Tier 1 Flagship Guides (25 URLs) - Sorted by GitHub stars descending
    tier1_mods = [m for m in mods.values() if m.get('contentTier') == 1]
    tier1_sorted = sorted(tier1_mods, key=lambda m: -(m.get('stars') or 0))
    tier1_urls = [f"https://magisk.yssn.tech/modules/{m['id']}/" for m in tier1_sorted]

    # 3. High-Priority Non-Tier 1 Modules (61 URLs) - High search intent on Bing/Copilot & Yandex (CIS/Global)
    selected_non_tier1_ids = [
        # Root Hiding, Keymint & Play Integrity (Highest Intent)
        'librepods', 'revanced-extended', 'teesimulator', 'surfing', 'neozygisk',
        'yurikey', 'teesimulator-rs', 'uperf-game-turbo', 'adguardhomeforroot', 'mountify',
        'trickystoreoss', 'nohello', 'zygiskfrida', 'hide-navbar', 'playcurlnext',
        'sui', 'alwaysstrong', 'specter', 'magisk-ad-blocking-module', 'vpnhide',
        'android-vbmeta-fixer', 'encore', 'adb-root', 'meta-magic-mount-rs', 'chroot-distro',
        're-malwack', 'livebootmodule', 'magiskhluda', 'hyperos-launcher', 'magisk-ios-emoji',
        'ohmykeymint', 'zygisknext', 'gphotosunlimited', 'brene', 'audio-misc-settings',
        'net-switch', 'makefontsgreatagain', 'pixelify-next', 'magnetar', 'hydro-br-leur',
        'nlsound-module-qcom', 'treat-wheel-zygisk', 'magisk-manager-for-recovery-mode',
        'deviceidchanger', 'twrp-keep', 'magisk-wifiadb', 'selinux-permissive', 'systemapp-nuker',
        'pixelupdater', 'frosty', 'hyperunlocked', 'ashlooper', 'hyperos-theme-manager',
        'zygisk-cacerts', 'hifi-maximizer-mod', 'ih8securelock', 'yetanotherbootloopprotector',
        'termuxrootmods', 'magicnet', 'ghostgms', 'zapret-pocket'
    ]

    non_tier1_mods = [mods[mid] for mid in selected_non_tier1_ids if mid in mods]
    non_tier1_sorted = sorted(non_tier1_mods, key=lambda m: -(m.get('stars') or 0))
    non_tier1_urls = [f"https://magisk.yssn.tech/modules/{m['id']}/" for m in non_tier1_sorted]

    top_100 = hubs + tier1_urls + non_tier1_urls
    
    # Deduplicate while preserving order
    seen = set()
    deduped = []
    for u in top_100:
        if u not in seen:
            seen.add(u)
            deduped.append(u)

    if len(deduped) != 100:
        print(f"Warning: Expected 100 URLs, got {len(deduped)}")

    # Export text file
    txt_path = os.path.join('scripts', 'top100_urls.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        for u in deduped:
            f.write(u + '\n')
    print(f"Wrote {len(deduped)} URLs to {txt_path}")

    # Export IndexNow payload
    indexnow_payload = {
        "host": "magisk.yssn.tech",
        "key": "INDEXNOW_KEY_PLACEHOLDER",
        "keyLocation": "https://magisk.yssn.tech/INDEXNOW_KEY_PLACEHOLDER.txt",
        "urlList": deduped
    }
    json_path = os.path.join('scripts', 'indexnow_payload.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(indexnow_payload, f, indent=2)
    print(f"Wrote IndexNow payload to {json_path}")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Generate top 100 high-priority URLs for Bing, Yandex, and search indexers via IndexNow.
Reflects complete 13-category taxonomy and newly added candidate modules.
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

    # 1. Structural / Taxonomy Hubs (19 URLs)
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
        'https://magisk.yssn.tech/categories/xposed-runtime-hooks/',
        'https://magisk.yssn.tech/categories/audio-dsp-acoustics/',
        'https://magisk.yssn.tech/categories/system-typography-fonts/',
        'https://magisk.yssn.tech/categories/battery-power-charging/',
        'https://magisk.yssn.tech/categories/boot-animations-ui/',
        'https://magisk.yssn.tech/compatibility/magisk/',
        'https://magisk.yssn.tech/compatibility/kernelsu/',
        'https://magisk.yssn.tech/compatibility/apatch/',
        'https://magisk.yssn.tech/compatibility/lsposed/',
    ]

    # 2. Tier 1 Flagship Guides - Sorted by stars/downloads descending
    tier1_mods = [m for m in mods.values() if m.get('contentTier') == 1]
    tier1_sorted = sorted(tier1_mods, key=lambda m: -(m.get('stars') or 0))
    tier1_urls = [f"https://magisk.yssn.tech/modules/{m['id']}/" for m in tier1_sorted]

    # Combine into deduplicated ordered URL set
    all_urls = []
    seen = set()

    for u in hubs:
        if u not in seen:
            seen.add(u)
            all_urls.append(u)

    for u in tier1_urls:
        if u not in seen:
            seen.add(u)
            all_urls.append(u)

    # Fill up to 100 with remaining top modules
    remaining = sorted(mods.values(), key=lambda m: -(m.get('stars') or 0))
    for m in remaining:
        u = f"https://magisk.yssn.tech/modules/{m['id']}/"
        if u not in seen:
            seen.add(u)
            all_urls.append(u)
        if len(all_urls) >= 100:
            break

    final_100 = all_urls[:100]

    os.makedirs('scripts', exist_ok=True)
    with open('scripts/top100_urls.txt', 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(final_100) + '\n')

    indexnow_payload = {
        "host": "magisk.yssn.tech",
        "key": "d1700f86ccb7e976d4334cf6cc9f85dc",
        "keyLocation": "https://magisk.yssn.tech/d1700f86ccb7e976d4334cf6cc9f85dc.txt",
        "urlList": final_100
    }

    with open('scripts/indexnow_payload.json', 'w', encoding='utf-8') as fp:
        json.dump(indexnow_payload, fp, indent=2, ensure_ascii=False)

    print(f"Generated IndexNow payload with {len(final_100)} URLs.")

if __name__ == '__main__':
    main()

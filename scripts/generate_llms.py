#!/usr/bin/env python3
"""
Generate public/llms-full.txt from modules/*.json
"""

import glob
import json
import os

def generate():
    files = sorted(glob.glob('modules/*.json'))
    modules = []
    for f in files:
        with open(f, 'r', encoding='utf-8') as fp:
            try:
                modules.append(json.load(fp))
            except Exception as e:
                print(f"Error loading {f}: {e}")

    modules.sort(key=lambda m: (-m.get('stars', 0), m.get('name', '')))

    lines = [
        '# Magisk Hub - Full Module Catalog (llms-full.txt)',
        '',
        '> Complete directory of 190+ community-maintained root modules for Magisk, KernelSU, and APatch.',
        '',
        'Website: https://magisk.yssn.tech/',
        'Repository: https://github.com/Yass5002/magisk-hub',
        '',
        '## Complete Module Index',
        ''
    ]

    for m in modules:
        mid = m.get('id', '')
        name = m.get('name', '')
        desc = m.get('description', '')
        compat = ', '.join(m.get('compatibility', []))
        stars = m.get('stars', 0)
        tag = m.get('latestRelease', {}).get('tag', '')
        download = m.get('latestRelease', {}).get('downloadUrl', '')
        repo = m.get('repo', '')
        category = m.get('category', '')

        lines.append(f"### {name} (`{mid}`)")
        lines.append(f"- Description: {desc}")
        lines.append(f"- Module URL: https://magisk.yssn.tech/modules/{mid}/")
        lines.append(f"- Category: https://magisk.yssn.tech/categories/{category}/")
        lines.append(f"- Supported Platforms: {compat}")
        lines.append(f"- GitHub Stars: {stars:,}")
        lines.append(f"- Latest Release: {tag}")
        if download:
            lines.append(f"- Download Asset: {download}")
        if repo:
            lines.append(f"- Upstream Source: https://github.com/{repo}")
        lines.append('')

    os.makedirs('public', exist_ok=True)
    with open('public/llms-full.txt', 'w', encoding='utf-8') as out:
        out.write('\n'.join(lines))

    print(f"Generated public/llms-full.txt with {len(modules)} modules")

if __name__ == '__main__':
    generate()

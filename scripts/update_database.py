#!/usr/bin/env python3
"""
Magisk Hub Database Updater
Fetches real-time release assets, tags, and metadata for all tracked modules via GitHub GraphQL API.
Ensures only active, unarchived projects with verified downloadable release assets are kept.
"""

import json
import os
import subprocess
import sys
from datetime import datetime

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'modules.json')

def load_modules():
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_modules(modules):
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        json.dump(modules, f, indent=2, ensure_ascii=False)

def query_repo(owner, name):
    q = f"""
    query {{
      repository(owner: "{owner}", name: "{name}") {{
        nameWithOwner
        description
        isArchived
        pushedAt
        stargazerCount
        latestRelease {{
          tagName
          publishedAt
          url
          releaseAssets(first: 15) {{
            nodes {{
              name
              downloadUrl
              size
            }}
          }}
        }}
      }}
    }}
    """
    try:
        res = subprocess.run(['gh', 'api', 'graphql', '-f', f'query={q}'], capture_output=True, text=True)
        if res.returncode == 0:
            return json.loads(res.stdout).get('data', {}).get('repository')
    except Exception as e:
        print(f"Error querying {owner}/{name}: {e}", file=sys.stderr)
    return None

def main():
    modules = load_modules()
    print(f"Loaded {len(modules)} modules for dynamic update check...")
    
    updated_count = 0
    valid_modules = []
    
    for idx, mod in enumerate(modules):
        repo = mod['repo']
        owner, name = repo.split('/')
        
        info = query_repo(owner, name)
        if not info:
            print(f"[{idx+1}/{len(modules)}] ⚠️ Failed to fetch {repo}, keeping existing data.")
            valid_modules.append(mod)
            continue
            
        if info.get('isArchived'):
            print(f"[{idx+1}/{len(modules)}] ❌ {repo} is now archived! Pruning from active database.")
            continue
            
        rel = info.get('latestRelease')
        if not rel:
            print(f"[{idx+1}/{len(modules)}] ⚠️ {repo} has no releases. Pruning.")
            continue
            
        assets = rel.get('releaseAssets', {}).get('nodes', [])
        
        # Check target asset: apk for Magisk app, zip for modules
        if mod.get('type') == 'root_manager' or mod.get('id') == 'magisk':
            apks = [a for a in assets if a['name'].startswith('Magisk-v') and a['name'].endswith('.apk')]
            if not apks:
                apks = [a for a in assets if a['name'].endswith('.apk')]
            chosen = apks[0] if apks else None
        else:
            zips = [a for a in assets if a['name'].endswith('.zip')]
            chosen = zips[0] if zips else None
            
        if not chosen:
            print(f"[{idx+1}/{len(modules)}] ⚠️ {repo} release {rel['tagName']} has no valid downloadable asset. Pruning.")
            continue
            
        # Update metadata
        mod['stars'] = info.get('stargazerCount', mod.get('stars', 0))
        if info.get('description'):
            mod['description'] = info['description']
            
        old_tag = mod.get('latestRelease', {}).get('tag')
        new_tag = rel['tagName']
        if old_tag != new_tag:
            print(f"[{idx+1}/{len(modules)}] 🚀 {repo} updated: {old_tag} -> {new_tag}")
            updated_count += 1
            
        mod['latestRelease'] = {
            'tag': new_tag,
            'publishedAt': rel['publishedAt'],
            'url': rel['url'],
            'downloadUrl': chosen['downloadUrl'],
            'assetName': chosen['name']
        }
        valid_modules.append(mod)
        
    save_modules(valid_modules)
    print(f"Database update complete! {len(valid_modules)} active modules preserved. {updated_count} updated.")

if __name__ == '__main__':
    main()

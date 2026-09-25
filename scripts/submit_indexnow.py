#!/usr/bin/env python3
"""
Submit the top 100 high-priority URLs to Bing and Yandex via IndexNow API.

Usage:
  python3 scripts/submit_indexnow.py [--key <your_key>] [--dry-run]
"""

import argparse
import glob
import json
import os
import secrets
import sys
import urllib.request
import urllib.error

INDEXNOW_ENDPOINTS = [
    ("IndexNow Universal (Bing + Yandex)", "https://api.indexnow.org/indexnow"),
    ("Bing IndexNow Direct", "https://www.bing.com/indexnow"),
    ("Yandex IndexNow Direct", "https://yandex.com/indexnow"),
]

def find_or_create_key(custom_key=None):
    if custom_key:
        key = custom_key.strip()
    else:
        # Check existing key files in public/
        key_files = [f for f in glob.glob('public/*.txt') if os.path.basename(f) not in ('robots.txt', 'llms.txt', 'llms-full.txt')]
        if key_files:
            key_file = key_files[0]
            with open(key_file, 'r', encoding='utf-8') as f:
                key = f.read().strip()
            print(f"Found existing IndexNow key in {key_file}: {key}")
            return key
        # Generate new 32-char hex key
        key = secrets.token_hex(16)
        print(f"Generated new IndexNow key: {key}")

    # Ensure key file is in public/ and dist/
    for folder in ('public', 'dist'):
        if os.path.isdir(folder):
            target = os.path.join(folder, f"{key}.txt")
            with open(target, 'w', encoding='utf-8') as f:
                f.write(f"{key}\n")
            print(f"Wrote verification file: {target}")

    return key

def load_urls():
    txt_path = os.path.join('scripts', 'top100_urls.txt')
    if not os.path.exists(txt_path):
        import generate_top100_indexnow
        generate_top100_indexnow.main()

    with open(txt_path, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return urls

def main():
    parser = argparse.ArgumentParser(description="Submit top 100 URLs to Bing and Yandex via IndexNow")
    parser.add_argument('--key', help="IndexNow key (32 hex characters)")
    parser.add_argument('--dry-run', action='store_true', help="Print payload without sending HTTP requests")
    parser.add_argument('--endpoint', default='all', choices=['all', 'indexnow', 'bing', 'yandex'], help="Target endpoint")
    args = parser.parse_args()

    urls = load_urls()
    print(f"Loaded {len(urls)} target URLs.")

    key = find_or_create_key(args.key)
    host = "magisk.yssn.tech"
    key_location = f"https://{host}/{key}.txt"

    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": urls
    }

    # Save to indexnow_payload.json
    with open(os.path.join('scripts', 'indexnow_payload.json'), 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)

    if args.dry_run:
        print("\n[Dry Run] Prepared payload:")
        print(f"Host: {host}")
        print(f"Key: {key}")
        print(f"Key Location: {key_location}")
        print(f"URL Count: {len(urls)}")
        print(f"First 5 URLs: {urls[:5]}")
        print("Dry run completed. No network requests sent.")
        return

    data = json.dumps(payload).encode('utf-8')
    headers = {
        'Content-Type': 'application/json; charset=utf-8',
        'User-Agent': 'MagiskHub-IndexNow/1.0'
    }

    endpoints = INDEXNOW_ENDPOINTS
    if args.endpoint == 'indexnow':
        endpoints = [INDEXNOW_ENDPOINTS[0]]
    elif args.endpoint == 'bing':
        endpoints = [INDEXNOW_ENDPOINTS[1]]
    elif args.endpoint == 'yandex':
        endpoints = [INDEXNOW_ENDPOINTS[2]]

    print("\nSending IndexNow submission...")
    for name, endpoint in endpoints:
        req = urllib.request.Request(endpoint, data=data, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                status = resp.status
                print(f"  [{name}] {endpoint} -> HTTP {status} (Success/Queued)")
        except urllib.error.HTTPError as e:
            # 200/202 are success; 400 = invalid payload; 403 = key invalid/unverified; 422 = URLs don't match host
            print(f"  [{name}] {endpoint} -> HTTP {e.code}: {e.read().decode('utf-8', errors='ignore')}")
        except Exception as e:
            print(f"  [{name}] {endpoint} -> Failed: {e}")

if __name__ == '__main__':
    main()

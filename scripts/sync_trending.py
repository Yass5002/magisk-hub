#!/usr/bin/env python3
"""
Sync 7-day rolling module downloads from Umami Analytics into src/data/trending.json.
Uses the authenticated Umami API token to query download-module event data.
"""
import os
import json
import time
import urllib.request
import urllib.error

UMAMI_URL = os.environ.get("UMAMI_URL", "https://analytics.mehro.me").rstrip("/")
WEBSITE_ID = os.environ.get("UMAMI_WEBSITE_ID", "190ae8fe-29af-471c-977d-e255344c0938")
UMAMI_API_KEY = os.environ.get("UMAMI_API_KEY", "")
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "..", "src", "data", "trending.json")

def get_7d_timestamps():
    now_ms = int(time.time() * 1000)
    seven_days_ago_ms = now_ms - (7 * 24 * 3600 * 1000)
    return seven_days_ago_ms, now_ms

def fetch_trending_downloads():
    start_at, end_at = get_7d_timestamps()
    endpoint = f"{UMAMI_URL}/api/websites/{WEBSITE_ID}/event-data/events?startAt={start_at}&endAt={end_at}&event=download-module"

    headers = {
        "User-Agent": "MagiskHub-Sync/1.0",
        "Accept": "application/json",
        "x-umami-api-key": UMAMI_API_KEY,
        "Authorization": f"Bearer {UMAMI_API_KEY}"
    }

    counts = {}

    try:
        req = urllib.request.Request(endpoint, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list):
                for item in data:
                    if item.get("propertyName") == "module":
                        mod_id = item.get("propertyValue")
                        tot = int(item.get("total", 0))
                        if mod_id and tot > 0:
                            counts[mod_id] = tot
    except Exception as e:
        print(f"[sync_trending] Notice: Umami API query error: {e}")
        return None

    return counts

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    counts = fetch_trending_downloads()

    if counts is not None:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(counts, f, indent=2)
        print(f"[sync_trending] Successfully populated {OUTPUT_FILE} with {len(counts)} real trending modules from Umami!")
        # Print top 10
        sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
        print("[sync_trending] Top 10 downloaded this week:")
        for k, v in sorted_items:
            print(f"  - {k}: {v} downloads")
    else:
        if not os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "w") as f:
                json.dump({}, f, indent=2)
            print(f"[sync_trending] Fallback initialized empty {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()

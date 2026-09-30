#!/usr/bin/env python3
"""
Sync 7-day rolling module downloads from Umami Analytics into src/data/trending.json.
Gracefully handles missing credentials, network errors, or zero-data states without failing CI.
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
    endpoint = f"{UMAMI_URL}/api/websites/{WEBSITE_ID}/metrics?type=event&startAt={start_at}&endAt={end_at}"

    headers = {
        "User-Agent": "MagiskHub-Sync/1.0",
        "Accept": "application/json"
    }
    if UMAMI_API_KEY:
        headers["x-umami-api-key"] = UMAMI_API_KEY

    counts = {}

    try:
        req = urllib.request.Request(endpoint, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, list):
                for item in data:
                    x = item.get("x", "")
                    # Check for download-module events
                    if x == "download-module" or x.startswith("download:"):
                        mod_id = item.get("data", {}).get("module") or x.replace("download:", "")
                        if mod_id:
                            counts[mod_id] = counts.get(mod_id, 0) + int(item.get("y", 0))
    except Exception as e:
        print(f"[sync_trending] Notice: Umami API query skipped or unauthenticated: {e}")
        print("[sync_trending] Using existing or default trending.json dataset.")
        return None

    return counts

def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    counts = fetch_trending_downloads()

    if counts is not None:
        with open(OUTPUT_FILE, "w") as f:
            json.dump(counts, f, indent=2)
        print(f"[sync_trending] Successfully updated {OUTPUT_FILE} with {len(counts)} trending modules.")
    else:
        if not os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "w") as f:
                json.dump({}, f, indent=2)
            print(f"[sync_trending] Initialized empty {OUTPUT_FILE}.")

if __name__ == "__main__":
    main()

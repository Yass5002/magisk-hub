#!/usr/bin/env python3
import json
import glob
import os
import random

# 1. Load actual modules
modules = []
for p in glob.glob('modules/*.json'):
    if 'schema.json' in p: continue
    with open(p) as f:
        data = json.load(f)
        modules.append({
            'id': data.get('id'),
            'name': data.get('name'),
            'stars': data.get('stars', 0),
            'category': data.get('category')
        })

print(f"Loaded {len(modules)} real modules.")

# 2. Simulate 3 Traffic Scenarios
# Scenario 1: Early Launch / Current Reality (Low traffic, ~120 total downloads / week)
# - TrickyStore (6k stars): 25 downloads
# - HMA-OSS (3.3k stars): 20 downloads
# - PlayIntegrityFork (4.5k stars): 18 downloads
# - AlwaysStrong (120 stars - breakout utility): 14 downloads
# - meta-magic_mount-rs (220 stars): 9 downloads
# - TurnOffSensors (5 stars): 1 download (test click)
# - ReZygisk (4k stars): 0 downloads (stale week)
# - shamiko (6.3k stars): 0 downloads (stale week)

def get_scenario_early_launch():
    downloads = {
        'trickystore': 25,
        'hma-oss': 20,
        'playintegrityfork': 18,
        'alwaysstrong': 14,
        'meta-magic_mount-rs': 9,
        'playintegrityfix': 8,
        'rezygisk': 0,
        'shamiko': 0,
        'fingerprintpay': 2,
        'turnoffsensors-magisk': 1, # The 5-star module with 1 download
        'rsync-magisk': 1,          # The 2-star module with 1 download
    }
    return downloads

def get_scenario_steady_state():
    # Moderate traffic, ~1,200 downloads / week
    downloads = {
        'trickystore': 180,
        'hma-oss': 150,
        'playintegrityfix': 110,
        'alwaysstrong': 95,
        'meta-magic_mount-rs': 60,
        'hyperunlocked': 45,
        'rezygisk': 35,
        'shamiko': 25,
        'turnoffsensors-magisk': 2,
        'rsync-magisk': 0,
        'imagecopyhide': 1
    }
    return downloads

# 3. Define Candidate Ranking Models

# Model 1: Fixed Threshold 2-Tier (K=3)
# Tier 1: downloads >= 3, sorted by downloads DESC, tie-breaker stars DESC
# Tier 2: downloads < 3, sorted by stars DESC
def rank_model_1(modules, dl_map, K=3):
    t1 = []
    t2 = []
    for m in modules:
        d = dl_map.get(m['id'], 0)
        item = dict(m, dl=d)
        if d >= K:
            t1.append(item)
        else:
            t2.append(item)
    t1.sort(key=lambda x: (x['dl'], x['stars']), reverse=True)
    t2.sort(key=lambda x: x['stars'], reverse=True)
    return t1 + t2, len(t1)

# Model 2: Top-N Trending Roster (Top N=10 with min threshold K=2)
# Tier 1: Top 10 with dl >= 2, sorted by downloads DESC
# Tier 2: The rest, sorted by stars DESC
def rank_model_2(modules, dl_map, N=10, K=2):
    t1_candidates = []
    t2_candidates = []
    for m in modules:
        d = dl_map.get(m['id'], 0)
        item = dict(m, dl=d)
        if d >= K:
            t1_candidates.append(item)
        else:
            t2_candidates.append(item)
    
    t1_candidates.sort(key=lambda x: (x['dl'], x['stars']), reverse=True)
    t1 = t1_candidates[:N]
    
    # Remaining candidates from t1 go to t2
    leftovers = t1_candidates[N:]
    t2 = t2_candidates + leftovers
    t2.sort(key=lambda x: x['stars'], reverse=True)
    return t1 + t2, len(t1)

# Model 3: Dynamic Hurdle (K = max(3, P75 of active downloads))
def rank_model_3(modules, dl_map):
    active_dls = [dl_map[mid] for mid in dl_map if dl_map[mid] > 0]
    if not active_dls:
        K = 3
    else:
        active_dls.sort()
        K = max(3, active_dls[len(active_dls)//2]) # Median active download
    return rank_model_1(modules, dl_map, K=K)

# 4. Run Evaluations
print("\n" + "="*60)
print("EVALUATION 1: EARLY LAUNCH SCENARIO")
print("="*60)
dl_early = get_scenario_early_launch()

for name, fn in [("Model 1: Fixed Threshold (K=3)", lambda m: rank_model_1(m, dl_early, K=3)),
                 ("Model 1b: Fixed Threshold (K=5)", lambda m: rank_model_1(m, dl_early, K=5)),
                 ("Model 2: Top-10 Roster (K=2, N=10)", lambda m: rank_model_2(m, dl_early, N=10, K=2)),
                 ("Model 3: Dynamic Median Hurdle", lambda m: rank_model_3(m, dl_early))]:
    res, t1_len = fn(modules)
    print(f"\n--- {name} (Tier 1 size: {t1_len}) ---")
    for i, item in enumerate(res[:12], 1):
        tier = "T1 [TRENDING]" if i <= t1_len else "T2 [CATALOG]"
        print(f"#{i:02d} {tier:14} {item['name']:25} | {item['dl']:3d} DLs | {item['stars']:5d} ★")
    
    # Check test cases
    turnoff_rank = next(i for i, x in enumerate(res, 1) if x['id'] == 'turnoffsensors-magisk')
    rezygisk_rank = next(i for i, x in enumerate(res, 1) if x['id'] == 'rezygisk')
    always_rank = next(i for i, x in enumerate(res, 1) if x['id'] == 'alwaysstrong')
    
    print(f"  Test: ReZygisk (4k ★, 0 DL) Rank: #{rezygisk_rank}")
    print(f"  Test: AlwaysStrong (120 ★, 14 DL) Rank: #{always_rank}")
    print(f"  Test: TurnOffSensors (5 ★, 1 DL) Rank: #{turnoff_rank}")
    if turnoff_rank > rezygisk_rank:
        print("  ✓ PASS: 1-download 5-star module DOES NOT outperform 4k-star module!")
    else:
        print("  ✗ FAIL: 1-download module jumped ahead of 4k-star module!")

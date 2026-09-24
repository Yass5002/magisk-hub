#!/usr/bin/env python3
"""
Magisk Hub Production Synchronizer
Full lifecycle engine:
  - Audits candidate modules against the strict active bar
  - Resolves and caches icons locally into assets/icons/<slug>.png (or null)
  - Hard-deletes/prunes any module that fails active criteria (archived, stale, dead asset)
  - Generates schema-compliant module JSON entries in modules/<slug>.json
"""

import json
import os
import re
import sys
import subprocess
import urllib.request
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODULES_DIR = os.path.join(REPO_ROOT, "modules")
ICONS_DIR = os.path.join(REPO_ROOT, "assets", "icons")

ACTIVE_DAYS_THRESHOLD = 548  # ~18 months

CAT_MAP = {
    'root-management': 'root-management',
    'performance': 'performance-kernel',
    'performance-kernel': 'performance-kernel',
    'gaming': 'performance-kernel',
    'system': 'system-environment',
    'system-environment': 'system-environment',
    'customization': 'customization-ui',
    'customization-ui': 'customization-ui',
    'app-modifications': 'customization-ui',
    'development': 'development-instrumentation',
    'development-instrumentation': 'development-instrumentation',
    'utilities': 'system-utilities',
    'system-utilities': 'system-utilities',
    'audio': 'system-utilities',
    'file-management': 'system-utilities',
    'debloating': 'system-utilities',
    'networking': 'networking-proxies',
    'networking-proxies': 'networking-proxies',
    'ad-blocking': 'networking-proxies',
    'security': 'security-certificates',
    'security-certificates': 'security-certificates',
    'privacy': 'security-certificates',
}

# Verified icon path mapping within module repositories
KNOWN_ICONS = {
    "topjohnwu/Magisk": "docs/images/logo.png",
    "KOWX712/PlayIntegrityFix": "webui/public/icon.jpg",
    "frknkrc44/HMA-OSS": "app/src/main/res/drawable/cont_icon_designer.webp",
    "chenxiaolong/BCR": "app/images/icon.svg",
    "sidex15/susfs4ksu-module": "susfsicon.png",
    "salvogiangri/KnoxPatch": "fastlane/metadata/android/en-US/images/icon.png",
    "bindhosts/bindhosts": "webui/public/icon.png",
    "Fanju6/NetProxy-Magisk": "src/module/webroot/sing-box-dashboard/apple-touch-icon-180x180.png",
    "Seyud/device_faker": "docs/logo.png",
    "pantsufan/Magisk-Ad-Blocking-Module": "logo.png",
    "okhsunrog/vpnhide": "assets/icon-512.png",
    "Rem01Gaming/encore": "webui/public/icon.webp",
    "Tools-cx-app/meta-magic_mount-rs": "webui/public/favicon.svg",
    "KernelSU-Next/KPatch-Next-Module": "webui/icon.png",
    "ZG089/Re-Malwack": "assets/logo.png",
    "AlirezaParsi/COPG": "webroot/icon.png",
    "BasGame1/Pixelify-Next": "beta/module/webroot/glogo.webp",
    "Numbersf/MakeFontsGreatAgain": "webroot/icon.png",
    "PixelUpdater/PixelUpdater": "app/images/icon.png",
    "Drsexo/Frosty": "module/webroot/icon.png",
    "pantsufan/BlockAds": "logo.png",
    "LIghtJUNction/MagicNet": "icon.png",
    "ravindu644/Ubuntu-Chroot": "webroot/assets/logo.png",
    "sevcator/zapret-pocket": "icon.png",
    "5MayRain/SAM": "etc/mihomo/webui/zashboard/apple-touch-icon.png",
    "eventlOwOp/zerotier-magisk": "app/assets/icon.png",
    "Liliya2727/AZenith": "logo.jpg",
    "VD171/COPG-VD": "module/webroot/icon.png",
    "Xocio/CZero": "assets/logo.png",
    "Vaz15k/Cubic-AdBlock": "docs/cubic_logo.png",
    "rhythmcache/partition-backup": "module/webroot/logo.svg",
    "UNKNUW/Background-App-Slayer": "LOGO.png"
}
if os.path.isfile('/tmp/deep_tree_icons.json'):
    try:
        with open('/tmp/deep_tree_icons.json', 'r', encoding='utf-8') as f:
            tree_data = json.load(f)
            blacklist_icons = {
                'OnyxZygisk/OnyxZygisk',
                'adivenxnataly/PerfGame',
                'fatalcoder524/TCP_Optimiser_Module',
                'Yurii0307/yurikey'
            }
            for r, v in tree_data.items():
                if r not in blacklist_icons and v.get('success'):
                    ic_list = v.get('icons', [])
                    if ic_list:
                        KNOWN_ICONS[r] = ic_list[0]
    except Exception:
        pass



def make_slug(raw_id, repo_name):
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', raw_id)
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s).lower().strip('-')
    if not s or len(s) < 2:
        s = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', repo_name)
        s = re.sub(r'[^a-zA-Z0-9]+', '-', s).lower().strip('-')
    s = re.sub(r'-+', '-', s)
    return s


def check_asset_head(url):
    req = urllib.request.Request(
        url,
        method="HEAD",
        headers={"User-Agent": "Mozilla/5.0 (compatible; MagiskHub/1.0)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status in (200, 302)
    except urllib.error.HTTPError as e:
        if e.code in (403, 405):
            get_req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (compatible; MagiskHub/1.0)", "Range": "bytes=0-0"}
            )
            try:
                with urllib.request.urlopen(get_req, timeout=10) as get_resp:
                    return get_resp.status in (200, 206)
            except Exception:
                return False
        return False
    except Exception:
        return False


def download_file(url, dest_path):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; MagiskHub/1.0)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with open(dest_path, "wb") as f:
                    f.write(resp.read())
                return True
    except Exception:
        return False
    return False


def resolve_icon(repo, slug, default_branch="master"):
    dest_path = os.path.join(ICONS_DIR, f"{slug}.png")
    if os.path.isfile(dest_path) and os.path.getsize(dest_path) > 100:
        return f"assets/icons/{slug}.png"

    # If known icon in repo tree, fetch directly
    if repo in KNOWN_ICONS:
        known_subpath = KNOWN_ICONS[repo]
        raw_url = f"https://raw.githubusercontent.com/{repo}/{default_branch}/{known_subpath}"
        if download_file(raw_url, dest_path):
            return f"assets/icons/{slug}.png"

    return None


def get_github_token():
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        return token
    try:
        proc = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
        if proc.returncode == 0 and proc.stdout.strip():
            return proc.stdout.strip()
    except Exception:
        pass
    return None


def fetch_graphql_batch(batch_repos):
    query_parts = ["query {"]
    alias_map = {}
    for idx, r in enumerate(batch_repos):
        alias = f"repo_{idx}"
        parts = r.split('/')
        if len(parts) != 2:
            continue
        alias_map[alias] = r
        query_parts.append(f"""
  {alias}: repository(owner: "{parts[0]}", name: "{parts[1]}") {{
    nameWithOwner
    description
    isArchived
    pushedAt
    stargazerCount
    licenseInfo {{
      spdxId
    }}
    defaultBranchRef {{
      name
    }}
    latestRelease {{
      tagName
      publishedAt
      url
      releaseAssets(first: 15) {{
        nodes {{
          name
          downloadUrl
        }}
      }}
    }}
  }}
""")
    query_parts.append("}")
    full_q = "\n".join(query_parts)

    token = get_github_token()
    results = {}

    if token:
        try:
            req = urllib.request.Request(
                "https://api.github.com/graphql",
                data=json.dumps({"query": full_q}).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {token}",
                    "User-Agent": "Mozilla/5.0 (compatible; MagiskHub/1.0)",
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
                data = payload.get("data") or {}
                for alias, repo_data in data.items():
                    orig_r = alias_map.get(alias)
                    if orig_r:
                        results[orig_r] = repo_data
                return results
        except Exception:
            pass

    # Fallback to gh CLI
    try:
        proc = subprocess.run(["gh", "api", "graphql", "-f", f"query={full_q}"], capture_output=True, text=True)
        if proc.stdout and proc.stdout.strip().startswith("{"):
            try:
                data = json.loads(proc.stdout).get("data") or {}
                for alias, repo_data in data.items():
                    orig_r = alias_map.get(alias)
                    if orig_r:
                        results[orig_r] = repo_data
                if results:
                    return results
            except Exception:
                pass

        for orig_r in batch_repos:
            parts = orig_r.split('/')
            single_q = f"""query {{ repository(owner: "{parts[0]}", name: "{parts[1]}") {{ nameWithOwner description isArchived pushedAt stargazerCount licenseInfo {{ spdxId }} defaultBranchRef {{ name }} latestRelease {{ tagName publishedAt url releaseAssets(first: 15) {{ nodes {{ name downloadUrl }} }} }} }} }}"""
            p_ind = subprocess.run(["gh", "api", "graphql", "-f", f"query={single_q}"], capture_output=True, text=True)
            if p_ind.returncode == 0:
                d = json.loads(p_ind.stdout).get("data", {}).get("repository")
                results[orig_r] = d
            else:
                results[orig_r] = None
    except Exception as e:
        print(f"Batch query exception: {e}", flush=True)

    return results


def main():
    print("=" * 70, flush=True)
    print("MAGISK HUB SYNCHRONIZER & ACTIVE-BAR PRUNING", flush=True)
    print("=" * 70, flush=True)

    os.makedirs(MODULES_DIR, exist_ok=True)
    os.makedirs(ICONS_DIR, exist_ok=True)

    candidates = []
    import glob
    module_files = [f for f in glob.glob(os.path.join(MODULES_DIR, "*.json")) if os.path.basename(f) != "schema.json"]
    if module_files:
        for fpath in sorted(module_files):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    candidates.append(json.load(f))
            except Exception as e:
                print(f"Error reading {fpath}: {e}", file=sys.stderr)
    elif os.path.isfile("/tmp/strictly_active_releases.json"):
        with open("/tmp/strictly_active_releases.json", "r", encoding="utf-8") as f:
            candidates = json.load(f)

    print(f"Loaded {len(candidates)} candidate modules from modules/ directory.", flush=True)

    repo_list = [c["repo"] for c in candidates]
    batch_size = 25
    github_data = {}

    print("Fetching real-time metadata from GitHub GraphQL API...", flush=True)
    for i in range(0, len(repo_list), batch_size):
        b = repo_list[i:i+batch_size]
        res = fetch_graphql_batch(b)
        github_data.update(res)
        sys.stdout.write(f"\rFetched {min(i+batch_size, len(repo_list))}/{len(repo_list)} repos...")
        sys.stdout.flush()
    print("\nMetadata fetch complete.", flush=True)

    now = datetime.now(timezone.utc)
    active_candidates = []
    pruned_modules = []

    print("Evaluating active bar (archive, push dates, releases)...", flush=True)
    for c in candidates:
        repo = c["repo"]
        raw_id = c["id"]
        repo_name = repo.split('/')[1]
        slug = c.get("id") or make_slug(raw_id, repo_name)
        category = c.get("category") or CAT_MAP.get(c.get("category", "system-utilities"), "system-utilities")
        compat = c.get("compatibility", ["Magisk"])

        info = github_data.get(repo)
        if not info:
            pruned_modules.append({"repo": repo, "slug": slug, "reason": "Repository 404 or inaccessible"})
            continue

        if info.get("isArchived"):
            pruned_modules.append({"repo": repo, "slug": slug, "reason": "Repository is archived"})
            continue

        pushed_at_str = info.get("pushedAt")
        if pushed_at_str:
            pushed_at = datetime.fromisoformat(pushed_at_str.replace("Z", "+00:00"))
            days_since = (now - pushed_at).days
            if days_since > ACTIVE_DAYS_THRESHOLD:
                pruned_modules.append({"repo": repo, "slug": slug, "reason": f"Inactive for {days_since} days (> {ACTIVE_DAYS_THRESHOLD}d limit)"})
                continue

        latest_rel = info.get("latestRelease")
        if not latest_rel:
            pruned_modules.append({"repo": repo, "slug": slug, "reason": "No tagged releases"})
            continue

        assets = latest_rel.get("releaseAssets", {}).get("nodes", [])

        # Check target asset: apk for Magisk app, zip for modules
        if slug == "magisk" or c.get("type") == "root_manager":
            valid_assets = [a for a in assets if a["name"].startswith("Magisk-v") and a["name"].endswith(".apk")]
            if not valid_assets:
                valid_assets = [a for a in assets if a["name"].endswith(".apk")]
        else:
            valid_assets = [a for a in assets if a["name"].endswith(".zip")]

        if not valid_assets:
            pruned_modules.append({"repo": repo, "slug": slug, "reason": f"Release {latest_rel['tagName']} lacks downloadable asset"})
            continue

        chosen_asset = valid_assets[0]

        # License resolution (must be valid SPDX)
        spdx = None
        lic_info = info.get("licenseInfo")
        if lic_info and lic_info.get("spdxId") and lic_info.get("spdxId") != "NOASSERTION":
            spdx = lic_info["spdxId"]
        if not spdx:
            if c.get("license") and c["license"] != "FOSS" and c["license"] != "Unknown":
                spdx = c["license"]
            else:
                spdx = "Proprietary"

        desc = info.get("description") or c.get("description") or f"{c['name']} active root module."
        desc = desc.strip()
        if not desc:
            desc = f"{c['name']} active root module for Android."

        active_candidates.append({
            "c": c,
            "info": info,
            "slug": slug,
            "category": category,
            "compat": compat,
            "chosen_asset": chosen_asset,
            "spdx": spdx,
            "desc": desc,
            "latest_rel": latest_rel
        })

    print(f"Candidates passing initial checks: {len(active_candidates)}", flush=True)

    # HEAD-check release assets in parallel
    print("Verifying release download URLs via parallel HEAD requests...", flush=True)
    def verify_asset(cand):
        url = cand["chosen_asset"]["downloadUrl"]
        ok = check_asset_head(url)
        return cand, ok

    surviving_modules = []
    with ThreadPoolExecutor(max_workers=16) as executor:
        for cand, ok in executor.map(verify_asset, active_candidates):
            if ok:
                surviving_modules.append(cand)
            else:
                pruned_modules.append({
                    "repo": cand["c"]["repo"],
                    "slug": cand["slug"],
                    "reason": f"Asset {cand['chosen_asset']['name']} failed HEAD check"
                })

    print(f"Surviving modules after live HEAD check: {len(surviving_modules)}", flush=True)

    # Resolve and cache icons for surviving modules
    print("Caching verified icons...", flush=True)
    final_module_entries = []
    for cand in surviving_modules:
        c = cand["c"]
        slug = cand["slug"]
        repo = c["repo"]
        default_branch = cand["info"].get("defaultBranchRef", {}).get("name", "master") or "master"
        icon_path = resolve_icon(repo, slug, default_branch)

        entry = {
            "id": slug,
            "name": c["name"],
            "repo": repo,
            "category": cand["category"],
            "description": cand["desc"],
            "compatibility": cand["compat"],
            "license": cand["spdx"],
            "icon": icon_path,
            "stars": cand["info"].get("stargazerCount", 0),
            "latestRelease": {
                "tag": cand["latest_rel"]["tagName"],
                "publishedAt": cand["latest_rel"]["publishedAt"],
                "url": cand["latest_rel"]["url"],
                "downloadUrl": cand["chosen_asset"]["downloadUrl"],
                "assetName": cand["chosen_asset"]["name"]
            },
            "seo": {
                "title": f"{c['name']} - Active Magisk Module",
                "description": cand["desc"][:155]
            }
        }
        final_module_entries.append((slug, entry))

    # Clean existing module files if they got pruned
    active_slugs = {s for s, _ in final_module_entries}
    for existing_file in os.listdir(MODULES_DIR):
        if existing_file.endswith(".json") and existing_file != "schema.json":
            file_slug = existing_file[:-5]
            if file_slug not in active_slugs:
                print(f"🗑️ Deleting pruned module file: modules/{existing_file}", flush=True)
                os.remove(os.path.join(MODULES_DIR, existing_file))
                for ext in [".png", ".jpg", ".webp", ".svg"]:
                    ic = os.path.join(ICONS_DIR, f"{file_slug}{ext}")
                    if os.path.isfile(ic):
                        os.remove(ic)

    # Write surviving module entries
    for slug, doc in final_module_entries:
        out_path = os.path.join(MODULES_DIR, f"{slug}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(doc, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70, flush=True)
    print("SYNCHRONIZATION & SEEDING REPORT", flush=True)
    print("=" * 70, flush=True)
    print(f"Total candidate modules processed: {len(candidates)}", flush=True)
    print(f"Active modules surviving all bars:  {len(final_module_entries)}", flush=True)
    print(f"Modules pruned / deleted:          {len(pruned_modules)}", flush=True)
    print("=" * 70, flush=True)

    if pruned_modules:
        print("\n--- PRUNED / DELETED MODULES LIST ---", flush=True)
        for p in pruned_modules:
            print(f"❌ {p['repo']} ({p['slug']}): {p['reason']}", flush=True)

    # Save log
    with open("/tmp/pruned_record.json", "w", encoding="utf-8") as f:
        json.dump(pruned_modules, f, indent=2)


if __name__ == "__main__":
    main()

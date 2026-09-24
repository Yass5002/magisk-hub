# Magisk Hub Database

A curated, strictly filtered, and actively maintained database of **Magisk and modern Android root modules**.

This repository serves as the single source of truth for working modules across **Magisk**, **KernelSU**, and **APatch**. Every entry in this database is audited against real GitHub release metadata to ensure it is unarchived, actively maintained (2025–2026), and directly downloadable.

---

## 📊 Database Metrics

* **Tracked Entities**: 203 total active entries
* **Root Manager**: 1 official root manager ([Magisk](https://github.com/topjohnwu/Magisk) `v30.7`)
* **Flashable Modules**: 202 community-maintained `.zip` modules with verified 2025–2026 releases
* **Unmaintained / Archived Entries Excluded**: 85+ dead, archived, or release-less candidate projects removed

### Distribution by Category

| Category | Count | Key Highlights |
| :--- | :--- | :--- |
| **Root Management & Integrity** | 36 | `Vector`, `TrickyStore`, `PlayIntegrityFork`, `ReZygisk`, `ZygiskNext`, `HMA-OSS` |
| **Performance, Kernel & Battery** | 29 | `COPG`, `MAGNETAR`, `Frosty`, `Stellar-Tweaks`, `GhostGMS` |
| **System & Environment** | 22 | `zygisk-detach`, `KnoxPatch`, `Pixelify-Next`, `Android-VBMeta-Fixer` |
| **Customization & UI** | 19 | `Hide-Navbar`, `HyperOS-Launcher`, `Magisk-iOS-Emoji`, `MakeFontsGreatAgain` |
| **Development & Instrumentation** | 17 | `magisk-frida`, `ZygiskFrida`, `adb_root`, `chroot-distro` |
| **System Utilities** | 16 | `BCR` (Basic Call Recorder), `Sui`, `usb-samplerate-unlocker` |
| **Networking & Proxies** | 13 | `box_for_magisk`, `Surfing` (Mihomo), `NetProxy-Magisk`, `vpnhide` |
| **Security & Certificate Injection** | 10 | `MoveCertificate`, `AlwaysTrustUserCerts`, `ih8SecureLock` |
| **Ad-blocking & DNS** | 10 | `bindhosts`, `AdGuardHomeForRoot`, `Magisk-Ad-Blocking-Module` |
| **Audio Processing & DSP** | 8 | `ViPERFX_RE`, `librepods`, `audio-misc-settings`, `hifi-maximizer-mod` |
| **File Management & Storage** | 6 | `CZero`, `partition-backup`, `Sortify` |
| **Gaming Optimizations** | 5 | `Magisk_AsoulOpt`, `Uperf-Game-Turbo`, `encore` |
| **Privacy & Identifier Spoofing** | 5 | `device_faker`, `deviceidchanger`, `StealthDebug` |
| **App Modifications** | 5 | `revanced-extended`, `GPhotosUnlimited`, `FingerprintPay` |
| **Debloating** | 2 | `systemapp_nuker`, `Scalpel` |

---

## 🛠️ Data Schema (`data/modules.json`)

Each entry in `data/modules.json` adheres to the following structure:

```json
{
  "id": "playintegrityfork",
  "name": "PlayIntegrityFork",
  "type": "magisk_module",
  "repo": "osm0sis/PlayIntegrityFork",
  "stars": 4519,
  "description": "Fix Play Integrity <A13 verdicts, allowing custom fields and props",
  "category": "root-management",
  "license": "FOSS",
  "compatibility": ["Magisk", "KernelSU", "APatch"],
  "latestRelease": {
    "tag": "v18",
    "publishedAt": "2026-08-29T17:33:56Z",
    "url": "https://github.com/osm0sis/PlayIntegrityFork/releases/tag/v18",
    "downloadUrl": "https://github.com/osm0sis/PlayIntegrityFork/releases/download/v18/PlayIntegrityFork-v18.zip",
    "assetName": "PlayIntegrityFork-v18.zip"
  }
}
```

---

## 🔄 Dynamic Database Updater

To refresh the database with the latest upstream release tags, download URLs, and star counts, run:

```bash
python3 scripts/update_database.py
```

The script queries the GitHub GraphQL API, updates release tags, resolves direct `.zip` assets, and prunes any repository that has been archived or deleted.

---
id: "copg-vd"
title: "COPG-VD: Global Device Identity, Build Fingerprint & System Framework Spoofing"
sidebarTitle: "COPG-VD"
description: "Global Zygisk-based hardware and build property spoofer by VD171 supporting JSON configuration, per-process overrides, WebUI management, and VDLU updates."
category: "performance-kernel"
tier: 1
searchQueries:
  - "copg-vd magisk module"
  - "vd171 copg-vd"
  - "global device spoofing zygisk"
  - "copg-vd json fingerprint spoof"
  - "replace playintegrityfix googlephotosunlimited"
prerequisites:
  - "Root access via Magisk (20.4+), KernelSU, or APatch"
  - "Active Zygisk environment (built-in Zygisk, Zygisk Next, ReZygisk, or NeoZygisk)"
  - "JSON configuration file at /data/adb/COPG-VD/COPG-VD.json"
conflicts:
  - "Other global or Play Integrity property spoofers (COPG, PlayIntegrityFix, integrity-box)"
configPaths:
  - "/data/adb/COPG-VD/COPG-VD.json"
  - "/data/adb/COPG-VD/vdlu/config"
  - "/data/adb/modules/COPG-VD/"
features:
  - "System-wide & scoped Zygisk hooking: supports Play Store/GMS scoping, global_fields (such as SECURITY_PATCH), and per-process overrides"
  - "Comprehensive build & hardware emulation: overrides BRAND, DEVICE, MODEL, FINGERPRINT, BOOTLOADER, UUID, FIRST_API_LEVEL, and DRM_SECURITY_LEVEL"
  - "WebUI & fingerprint updater: includes a built-in WebUI dashboard and fingerprint-update.sh helper"
  - "VDLU incremental updater: supports signed pre-zygote .so updates during post-fs-data without full module reflashing"
  - "Automatic legacy migration: migrates older /data/adb/COPG-VD.json files cleanly into /data/adb/COPG-VD/"
faq:
  - question: "Where should COPG-VD.json be placed in v6.18-vd?"
    answer: "Modern releases store configuration in /data/adb/COPG-VD/COPG-VD.json (with mode 0700 on /data/adb/COPG-VD). If you still have a legacy /data/adb/COPG-VD.json file, service.sh and fingerprint-update.sh automatically migrate it to the new directory."
  - question: "Can I use COPG-VD alongside PlayIntegrityFix?"
    answer: "No. COPG-VD's installer explicitly flags COPG, playintegrity/playintegrityfix, and integrity-box as conflicting modules to prevent overlapping Zygisk property hooks."
---

## Overview

Developed by **VD171** (forked from AlirezaParsi's COPG), **COPG-VD** (`v6.18-vd`) is a global Zygisk device identity and build property spoofer compatible with **Magisk**, **KernelSU**, and **APatch**.

Instead of relying solely on narrow Play Services hooks that can expose inconsistencies between user-space reflection and system framework properties, COPG-VD injects a native Zygisk library (`zygisk/*.so`) alongside `etc/copgvd_scope.dex` and reads a single declarative JSON file at `/data/adb/COPG-VD/COPG-VD.json`. It also ships a built-in WebUI, `fingerprint-update.sh`, and the **VDLU** signed pre-zygote incremental updater.

---

## Configuration Architecture (`/data/adb/COPG-VD/COPG-VD.json`)

All fields inside the `"COPG-VD"` block are optional—any omitted key passes the device's stock value through unchanged. All property values must be double-quoted strings.

### Example Configuration (`COPG-VD.json.example`):
```json
{
  "scope_mode": "playstore",
  "motor_drm": false,
  "drm_targets": [],
  "global_fields": ["SECURITY_PATCH"],
  "process_overrides": [],
  "COPG-VD": {
    "BRAND": "google",
    "DEVICE": "tegu",
    "MANUFACTURER": "Google",
    "MODEL": "Pixel 9a",
    "FINGERPRINT": "google/tegu_beta/tegu:CANARY/ZP11.261016.008/16754936:user/release-keys",
    "PRODUCT": "tegu_beta",
    "BOOTLOADER": "unknown",
    "BOARD": "tegu",
    "HARDWARE": "tegu",
    "DISPLAY": "ZP11.261016.008",
    "ID": "ZP11.261016.008",
    "HOST": "e4df75f83a59",
    "INCREMENTAL": "16754936",
    "TIMESTAMP": "1793211232",
    "PREVIEW_SDK": "20261104",
    "USER": "android-build",
    "SDK_FINGERPRINT": "ee82a872870173d77e68050e21a2bcbf",
    "UUID": "FjWvtSORkI0sEwekaPz2s30gqV5vWP_EZHFtBiXzboc",
    "SECURITY_PATCH": "2026-11-05",
    "FIRST_API_LEVEL": "35",
    "DRM_SECURITY_LEVEL": "L1"
  }
}
```

---

## Technical Architecture & How It Works

1. **Zygisk Multi-ABI Injection**: Ships `arm64-v8a`, `armeabi-v7a`, `x86`, and `x86_64` Zygisk shared libraries verified by `.sha256` checksums, hooking `android.os.Build` and native `__system_property_get` queries.
2. **Scope & Global Fields**: Supports `scope_mode` (e.g., `"playstore"`), `global_fields` (like `["SECURITY_PATCH"]`), `drm_targets`, `process_overrides`, and `COPG-VD-Settings` runtime options.
3. **Pre-Zygote VDLU Updater**: `post-fs-data.sh` executes `vdlu/update.sh` (configured via `/data/adb/COPG-VD/vdlu/config`) before Zygote maps `zygisk/<abi>.so`, allowing signed incremental updates without an extra reboot.
4. **WebUI & Fingerprint Helper**: Includes a WebUI (`webroot/`) for managing device profiles and running `fingerprint-update.sh` against upstream example JSON definitions.

---

## Installation & Setup

1. Ensure **Zygisk** is active in Magisk, KernelSU, or APatch, and remove conflicting spoofing modules (`COPG`, `PlayIntegrityFix`, `integrity-box`).
2. Flash `COPG-VD-v6.18-vd.zip` in your root manager (volume-key prompts default safely if `CLI_MODE` or headless install is detected).
3. Configure `/data/adb/COPG-VD/COPG-VD.json` via the WebUI or a root text editor (copying from `COPG-VD.json.example` as needed).
4. Reboot your device and verify applied props in a root/ADB shell:
   ```bash
   getprop ro.product.model
   ```

---

## Troubleshooting

- **Configuration File Not Detected**: Confirm the active config resides at `/data/adb/COPG-VD/COPG-VD.json` (older `/data/adb/COPG-VD.json` files are automatically migrated into `/data/adb/COPG-VD/` on boot).
- **JSON Syntax Errors**: Validate your file with `jq` or a JSON linter before rebooting; trailing commas or unquoted values will cause the parser to skip spoofing.

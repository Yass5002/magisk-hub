---
id: "copg-vd"
title: "COPG-VD: Global Device Identity, Build Fingerprint & System Framework Spoofing"
sidebarTitle: "COPG-VD"
description: "Global Zygisk-based hardware and build property spoofing suite that hooks system processes and user applications simultaneously via JSON configuration."
category: "performance-kernel"
tier: 1
searchQueries:
  - "copg-vd magisk module"
  - "vd171 copg-vd"
  - "global device spoofing zygisk"
  - "copg-vd json fingerprint spoof"
  - "replace playintegrityfix googlephotosunlimited"
prerequisites:
  - "Root access via Magisk or KernelSU"
  - "Active Zygisk environment enabled in root manager"
  - "JSON configuration file formatted at /data/adb/COPG-VD.json"
conflicts: []
configPaths:
  - "/data/adb/COPG-VD.json"
  - "/data/adb/modules/copg-vd/"
features:
  - "True system-wide hooking: intercepts identity queries across all application tiers, including native system apps and framework daemons"
  - "Complete build property emulation: overrides BRAND, DEVICE, MODEL, FINGERPRINT, BOOTLOADER, SECURITY_PATCH, and UUID"
  - "Play Integrity & Google Photos consolidation: eliminates the need for standalone spoofing modules when supplied with valid Google device hashes"
  - "Modular JSON declarative schema: easily edit or omit individual device identity keys without modifying module source code"
---

## Overview

Most property spoofing modules (such as standard build fingerprint fixers or photo backup unlockers) inject hooks selectively into specific user applications or targeted Google Play Services processes. While sufficient for narrow use cases, apps that perform cross-referencing between user-space properties and system framework APIs can detect inconsistencies.

Developed by VD171, **COPG-VD** implements comprehensive, system-wide device spoofing. Powered by a low-level Zygisk runtime hook, COPG-VD intercepts property reflection and native system calls globally—ensuring that every process running on the device, from core system frameworks to third-party games, sees an identical, fully coherent device profile.

When configured with an unrevoked Google Pixel or partner fingerprint, COPG-VD renders standalone modules like PlayIntegrityFix and GooglePhotosUnlimited redundant.

## Configuration Architecture (`/data/adb/COPG-VD.json`)

All spoofing directives are driven by a simple JSON configuration file located at `/data/adb/COPG-VD.json`.

All fields inside the configuration object are strictly optional; if a specific key is omitted, COPG-VD simply allows the device's native stock value to pass through unchanged. All values must be enclosed in double quotes.

### Example Configuration:
```json
{
  "COPG-VD": {
    "BRAND": "google",
    "DEVICE": "comet",
    "MANUFACTURER": "Google",
    "MODEL": "Pixel 9 Pro Fold",
    "FINGERPRINT": "google/comet_beta/comet:CANARY/ZP11.260821.010/16290768:user/release-keys",
    "PRODUCT": "comet_beta",
    "BOOTLOADER": "unknown",
    "BOARD": "comet",
    "HARDWARE": "comet",
    "DISPLAY": "ZP11.260821.010",
    "ID": "ZP11.260821.010",
    "HOST": "901e56a65b6b",
    "INCREMENTAL": "16290768",
    "TIMESTAMP": "1788897757",
    "PREVIEW_SDK": "20260909",
    "USER": "android-build",
    "SDK_FINGERPRINT": "dcead6233b738ebc908d5d77cd445f8b",
    "UUID": "f7zpdMvb23VEDwaAnZZSj_0jpgXfIAILKODaGMBrmOA",
    "SECURITY_PATCH": "2026-09-05"
  }
}
```

## How It Works Under the Hood

1. **Zygisk Initialization**: When an app forks from the Android Zygote process, COPG-VD's native library is injected into the newly created address space before Dalvik/ART virtual machine initialization.
2. **Framework Interception**: The module intercepts calls to `android.os.Build` and native system property readers (`__system_property_get`).
3. **Property Masking**: The requested values are substituted in memory with the definitions specified in `/data/adb/COPG-VD.json`.
4. **Global Consistency**: Because the hook applies indiscriminately across system services and user packages, system diagnostic tools report the spoofed identity consistently.

## Installation & Setup

1. Verify that **Zygisk** is enabled in your Magisk or KernelSU configuration.
2. Flash the `copg-vd` `.zip` package via your root manager.
3. Create and populate your `/data/adb/COPG-VD.json` configuration file with your desired target device properties using a text editor with root privileges.
4. Reboot your device to establish global hooks.
5. In an ADB or terminal shell, verify your spoofed model:
   ```bash
   getprop ro.product.model
   ```

## Troubleshooting

- **Configuration File Not Detected**: Confirm that the file path is exactly `/data/adb/COPG-VD.json` (case-sensitive) and that permissions allow root read access (`chmod 644`).
- **Syntax Errors**: If properties fail to apply, validate your JSON syntax using `jq` or an online JSON validator; missing commas or unescaped quotes will cause the parser to abort.

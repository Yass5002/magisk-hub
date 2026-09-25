---
id: "ezme-dex-space"
title: "ezme-dex-space: Space-Saving Ahead-of-Time (AOT) ART Compilation Tuning"
sidebarTitle: "ezme-dex-space"
description: "Reconfigures Android dex2oat compiler compiler targets from speed to space-profile, drastically reducing Dalvik cache storage usage and memory footprints."
category: "system-utilities"
tier: 1
searchQueries:
  - "ezme dex space magisk module"
  - "save internal storage android dex2oat"
  - "pm dexopt bg dexopt space profile"
  - "dalvik cache size reduction root"
  - "android aot compilation storage savings"
prerequisites:
  - "Android 11, 12, 12L, or higher"
  - "Root access via Magisk v24+ or KernelSU"
  - "Recommended Dalvik cache wipe after installation to trigger re-optimization"
conflicts: []
configPaths:
  - "/data/adb/modules/ezme-dex-space/"
features:
  - "Systemless build.prop property tuning: sets compiler flags across installation, background dexopt, and OTA routines"
  - "Space-optimized bytecode compilation: shifts AOT compilation profiles from aggressive 'speed' to compact 'space-profile'"
  - "Prevents low-memory thrashing: smaller compiled application code footprints reduce Out-of-Memory (OOM) app kills"
  - "Multi-gigabyte storage reclamation: saves substantial space in /data/dalvik-cache on devices with dozens of installed apps"
---

## Overview

The Android Runtime (ART) Ahead-of-Time (AOT) compiler (`dex2oat`) compiles bytecode from DEX files into native machine code ELF files (`.odex` and `.vdex`). By default on modern Android releases, the compiler uses aggressive `speed` compilation profiles. While this delivers minor execution speed improvements for raw CPU operations, it expands the compiled code footprint dramatically—often ballooning `/data/dalvik-cache` to consume 10GB to 20GB of storage on devices with many installed apps.

Developed by ez-me, **ezme-dex-space** re-tunes Android's internal package manager compiler directives systemlessly. By shifting the default compilation target from `speed` to `space-profile`, it instructs `dex2oat` to optimize only hot execution paths while storing the remainder in compact bytecode, freeing up significant storage space and reducing RAM pressure.

## Configured Property Directives

The module systemlessly sets the following package manager compilation flags:

```ini
pm.dexopt.install=space-profile
pm.dexopt.install-bulk=space-profile
pm.dexopt.bg-dexopt=space-profile
pm.dexopt.ab-ota=space-profile
pm.dexopt.shared=space
```

### What These Targets Mean:
- **`space-profile`**: Analyzes real-time application usage profiles and compiles only the methods that are actually called during daily operation. Unused library code remains unexpanded, slashing binary sizes.
- **`space`**: Generates minimum-footprint code for shared system libraries, avoiding duplicate compilation overhead across secondary apps.

## Re-Optimizing Existing Applications

Installing the module configures compiler directives for all future app installs and background maintenance cycles. To immediately reclaim storage from already installed applications:

1. Flash **ezme-dex-space** via **Magisk** or **KernelSU**.
2. Clear the Dalvik/ART cache using custom recovery or via terminal:
   ```bash
   su -c rm -rf /data/dalvik-cache/*
   ```
3. Reboot your device.
4. Android will recompile application packages using the new `space-profile` targets during first boot and subsequent idle charging cycles.

## Compatibility & Verification

- **Validated Systems**: Confirmed working across LineageOS 18.1 and 19.1 (Android 11 and 12L) up through modern Android 14+ releases.
- **Verification**: Check active package manager compiler properties in a terminal shell:
   ```bash
   getprop | grep pm.dexopt
   ```
   All entries should display `space-profile` or `space`.

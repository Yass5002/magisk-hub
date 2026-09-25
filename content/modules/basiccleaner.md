---
id: "basiccleaner"
title: "BasicCleaner: Automated Interval Storage Trimming, Cache Sweeping & ART Optimization"
sidebarTitle: "BasicCleaner"
description: "Autonomous maintenance utility that schedules periodic fstrim operations, application cache cleanups, APK zipalign passes, and ART profile optimizations."
category: "system-utilities"
tier: 1
searchQueries:
  - "basiccleaner magisk module"
  - "weirdmidas basiccleaner"
  - "fstrim android storage automatic root"
  - "art runtime recompilation magisk"
  - "android storage maintenance cron"
prerequisites:
  - "Android 8.0 or higher"
  - "Root access via Magisk or KernelSU"
  - "Device storage with standard Linux partition layouts"
conflicts: []
configPaths:
  - "/data/adb/modules/basiccleaner/"
  - "/sdcard/Android/basiccleaner.log"
features:
  - "Scheduled partition fstrim (7 days): reclaims NAND flash blocks across /system, /data, /cache, /persist, /vendor, and /product"
  - "Application cache sweeping (7 days): purges temporary application trash and directory caches without wiping user logins"
  - "Bytecode zip alignment (15 days): aligns uncompressed APK asset offsets on 4-byte boundaries for faster memory mapping"
  - "ART runtime optimization (30 days): synchronizes runtime profiles, prunes stale compilation artifacts, and executes background dexopt passes"
  - "Delayed boot initiation: waits 2 minutes after device startup before running checks to prevent boot-time CPU contention"
---

## Overview

Over months of daily use, Android devices accumulate residual storage fragmentation, unreferenced Dalvik/ART cache blobs, and unaligned application packages. While manual optimization scripts exist, remembering to run terminal commands periodically is impractical, and running full cache sweeps on every single boot causes unnecessary NAND write cycles and app launch sluggishness.

Developed by WeirdMidas, **BasicCleaner** is an automated, interval-based maintenance utility for rooted Android smartphones. Designed to operate completely autonomously, the module evaluates elapsed time stamps and executes graduated maintenance tasks—from weekly NAND flash trimming to monthly Ahead-of-Time (AOT) ART recompilation—ensuring smooth long-term device performance.

## Scheduled Maintenance Cadence

BasicCleaner initiates its evaluation cycle **2 minutes after boot**, ensuring that critical system startup routines and foreground UI rendering are never impacted by background I/O operations.

### 1. Every 7 Days: Storage Trimming & Cache Purge
- **Partition `fstrim`**: Issues discard commands across all active partitions (`/system`, `/data`, `/cache`, `/persist`, `/vendor`, `/system_ext`, `/product`), signaling the UFS/eMMC controller to erase unused flash blocks and restore write throughput.
- **Application Cache Clearing**: Sweeps temporary directories and app caches without disturbing user preferences, logins, or saved database files.

### 2. Every 15 Days: Application Alignment
- **`zipalign` Check**: Scans user-installed APK packages and aligns data boundaries to 4-byte offsets, reducing RAM consumption when Android reads resources directly from disk via `mmap`.

### 3. Every 30 Days: Android Runtime (ART) Deep Clean
- **ART Synchronization**: Purges dead compilation artifacts left behind by uninstalled packages or system updates.
- **Background `dexopt` Compilation**: Recompiles frequently executed application methods into optimized native machine code using active usage profiles (`cmd package bg-dexopt-job`).

## Monitoring & Execution Logs

BasicCleaner records its actions and time-to-completion metrics in a human-readable log stored directly in internal storage:

```
/sdcard/Android/basiccleaner.log
```

You can inspect recent maintenance timestamps directly in Termux or any text viewer:
```bash
cat /sdcard/Android/basiccleaner.log
```

## Installation & Setup

1. Download the `BasicCleaner` `.zip` from the official repository releases.
2. Flash the module using **Magisk** or **KernelSU**.
3. Reboot your device.
4. No further user configuration is needed; the maintenance scheduler will automatically track intervals and run tasks in the background.

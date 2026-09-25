---
id: "log-catcher"
title: "Log-Catcher: Automated Boot Logcat & Kernel Message Harvester"
sidebarTitle: "Log Catcher"
description: "Captures logcat and dmesg during system boot and archives timestamped tarballs to internal storage once unlocked."
category: "development-instrumentation"
tier: 1
searchQueries:
  - "log catcher magisk"
  - "hxreborn log catcher"
  - "capture boot logcat android root"
  - "kernelsu boot log catcher"
  - "android kernel dmesg capture root"
prerequisites:
  - "Root access via Magisk, KernelSU, or APatch"
conflicts: []
configPaths:
  - "/data/local/logcatcher/config"
  - "/data/adb/modules/Log-Catcher/"
features:
  - "Early boot capture: records kernel dmesg and system logcat from the earliest execution stages"
  - "Post-unlock tarball archiving: packages captured logs into timestamped .tar.gz archives in /sdcard/Download once decrypted"
  - "Configurable buffer streams: selectively collect main, system, radio, and crash logcat buffers"
  - "Automated rotation & pruning: enforces maximum file limits and prunes archives older than a designated number of days (default: 7 days)"
  - "Root manager integration: native WebUI for KernelSU and APatch alongside simple text configuration for Magisk"
---

## Overview

Diagnosing early boot crashes, random system reboots, and kernel panics on Android is often complicated by the fact that storage encryption and logging daemons do not expose log files to user space until after the first device unlock.

Maintained by hxreborn (building upon earlier work by Jaida Wu and Howard Wu), **Log-Catcher** is a root logging module designed to automate system diagnostic capture across boot. It intercepts kernel ring buffers (`dmesg`) and Android framework logs (`logcat`) during startup, preserving them into organized, timestamped archive bundles upon unlock.

## How It Operates

1. **Early Boot Interception**: As soon as root daemon services initialize, Log-Catcher begins capturing the designated logcat buffers (`main,system,crash`) and kernel diagnostic streams.
2. **Post-Unlock Archiving**: When the device keyguard is successfully unlocked and internal storage `/sdcard/` is mounted and decrypted, the module packages the captured logs into a timestamped `.tar.gz` bundle inside `/sdcard/Download`.
3. **Retention & Housekeeping**: The service runs a housekeeping routine that checks the modification dates of existing archives, removing any logs exceeding `PRUNE_DAYS` or exceeding the `MAX_LOGS` ceiling.

## Configuration

On **KernelSU** and **APatch**, you can manage configuration directly through the module's embedded WebUI dashboard.

On **Magisk**, configuration is adjusted by editing `/data/local/logcatcher/config`:

```sh
EXPORT_PATH=/sdcard/Download
MAX_LOGS=10
PRUNE_DAYS=7
BUFFERS=main,system,crash
PERSISTENT=false
```

- **`EXPORT_PATH`**: Directory where `.tar.gz` archives are saved.
- **`MAX_LOGS`**: Maximum number of log archives retained before older files are deleted.
- **`PRUNE_DAYS`**: Age threshold (in days) after which old archives are pruned.
- **`BUFFERS`**: Comma-separated list of logcat buffers to record.
- **`PERSISTENT`**: Set to `true` to keep recording logcat continuously in the background.

## Installation

1. Download the latest `hxr_logcat.zip` from GitHub releases.
2. Install via **Magisk**, **KernelSU**, or **APatch**.
3. Reboot your device to begin automated log collection.

---
id: "simple-bootloopsaver"
title: "Simple Bootloop Saver: Automated Zygote Crash Detection & Rescue for Magisk"
sidebarTitle: "Simple Bootloop Saver"
description: "Monitors Android Zygote PID stability during late boot, automatically disabling installed Magisk modules and restarting the phone if a bootloop is detected on encrypted storage."
category: "system-utilities"
tier: 1
searchQueries:
  - "simple bootloopsaver magisk module"
  - "ez-me simple bootloop saver"
  - "magisk bootloop protection encrypted data"
  - "automatic module disable zygote crash loop"
  - "huskydg bootloop saver lightweight"
prerequisites:
  - "Magisk v20.4 or higher"
  - "Encrypted or unencrypted /data partition (File-Based Encryption compatible)"
  - "Device experiencing module-induced boot instability"
conflicts: []
configPaths:
  - "/data/adb/modules/simple_bootloopsaver/"
  - "/data/adb/modules/*/disable"
features:
  - "Encrypted storage rescue: recovers devices without requiring custom recovery (TWRP/OrangeFox) decryption access to /data/adb/modules"
  - "Non-intrusive Zygote polling: monitors Zygote process identifiers in late_start mode across 15-second intervals"
  - "Heuristic crash confirmation: requires consecutive PID divergences before taking defensive action to eliminate false positives"
  - "Automated fail-safe disarming: writes disable flags across all active modules and reboots into clean stock userspace"
---

## Overview

One of the greatest hazards of experimenting with Magisk modules is encountering a bootloop. Modern Android devices utilize mandatory File-Based Encryption (FBE), meaning that if a newly flashed module crashes the system server or Zygote, custom recoveries (like TWRP or OrangeFox) frequently cannot decrypt user storage without wiping data. Users without an accessible recovery are often forced to execute factory resets.

Originating from research by HuskyDG and streamlined into an ultra-lightweight single-script implementation by ez-me, **Simple Bootloop Saver** serves as an autonomous watchdog. It runs silently during the late boot phase, continuously tracking the stability of the Android Zygote process. If Zygote is trapped in a crash-restart cycle, the module intervenes, neutralizes all installed modules, and triggers a clean system reboot.

## How the Detection Watchdog Functions

Bootloops triggered by framework mods, faulty overlays, or conflicting Zygisk binaries almost always manifest as repetitive crashes of the 32-bit or 64-bit Zygote daemons.

The module operates as follows:

1. **Late Start Execution**: The watchdog launches as a background task during Magisk's `late_start` service phase, after basic filesystem mounting is established.
2. **PID Sampling**: It queries and records the Process ID (PID) of the primary `zygote` daemon.
3. **Multi-Stage Verification**:
   - The script inspects the Zygote PID three consecutive times at 15-second intervals.
   - If the PID differs between checks, it indicates that Zygote crashed and was respawned by `init`.
   - To guard against false positives caused by transient system service restarts during early boot, the script performs a fourth confirmation check over an additional 15-second window.
4. **Automated Remediation**:
   - If Zygote PID instability is conclusively verified, the script writes a `disable` marker file into every module directory under `/data/adb/modules/`.
   - It issues an immediate hardware reboot command (`/system/bin/reboot`).
5. **Clean Recovery**: The phone boots back into Android with all modules disabled, allowing the user to open Magisk Manager, isolate the offending package, and remove it safely.

## Installation & Deployment

1. Download the `simple_bootloopsaver` `.zip` from the official repository.
2. Flash the module via the **Magisk** application.
3. Reboot to complete installation.
4. The watchdog will henceforth supervise all subsequent boot cycles automatically in the background.

## Re-enabling Modules After a Rescue

If a faulty module triggers the fail-safe and disables your modules:

1. The device will reboot safely to your lock screen.
2. Open the **Magisk** application and navigate to the **Modules** tab.
3. All modules will appear toggled off.
4. Locate and remove the problematic module that caused the initial crash.
5. Re-enable your trusted modules one by one, rebooting after each to verify stability.

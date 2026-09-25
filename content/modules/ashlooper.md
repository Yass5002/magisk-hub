---
id: "ashlooper"
title: "AshReXcue (AshLooper): Smart Differential Bootloop & Boot Script Protection"
sidebarTitle: "AshReXcue (AshLooper)"
description: "Intelligent bootloop protection engine for Magisk, KernelSU, and APatch that uses differential state analysis to isolate offending modules and boot scripts without wiping benign configurations."
category: "root-management"
tier: 1
searchQueries:
  - "ashrexcue magisk"
  - "ashlooper bootloop protector"
  - "ripperhybrid ashlooper"
  - "smart differential bootloop protection"
  - "systemui crash loop protection root"
prerequisites:
  - "Rooted Android device running Magisk, KernelSU, APatch, or modern community forks"
  - "Device volume keys or touch interface for interactive installation options"
conflicts: []
configPaths:
  - "/data/adb/modules/AshLooper/"
features:
  - "Smart Differential Analysis: hashes and fingerprints modules and scripts between boots to identify and isolate only the specific item that caused a failure"
  - "Boot Script Guard: extends full bootloop protection to standalone scripts residing in `service.d`, `post-mount.d`, and `post-fs-data.d`"
  - "SystemUI watchdog: monitors `com.android.systemui` health and triggers automated remediation if a crash loop is detected (3-strike policy)"
  - "Interactive local WebUI: feature-complete management panel for whitelisting modules, reviewing boot activity logs, and editing protection thresholds"
  - "Quarantine recovery vault: isolates failing scripts into a secure recovery vault, preserving their code for post-boot debugging rather than deleting them"
---

## Overview

AshReXcue (formerly known as AshLooper), authored by AshBorn (`@Ripper_Hybrid`), is a sophisticated boot protection engine for Magisk, KernelSU, and APatch environments. Traditional bootloop rescue scripts employ a blunt approach: if a boot fails, they disable every single installed module, forcing the user to re-enable dozens of modules one by one.

AshReXcue replaces this brute-force approach with **Smart Differential Analysis**. By recording cryptographic hashes, file sizes, and status flags across all modules and boot scripts during every successful boot, AshReXcue knows exactly what changed. When a bootloop occurs, it pinpoints and disables only the modified or newly installed component, leaving all working modules and root customizations fully operational.

## Prerequisites & Compatibility

- **Root Environment**: Compatible with official Magisk, KernelSU, APatch, and their respective active forks.
- **Android Versions**: Supports all modern Android versions from Android 8 through modern releases.
- **Hardware**: Universal support across ARM, ARM64, and x86 architectures.

There are no documented module conflicts. However, running multiple competing bootloop protectors concurrently (such as combining AshReXcue with YetAnotherBootloopProtector) can result in overlapping watchdog timers.

## Core Architecture & Protection Mechanics

### 1. Differential Tracking
During the late boot stage (`boot-completed`), AshReXcue catalogs the fingerprint of every installed module directory and script in `/data/adb/service.d/`, `/data/adb/post-fs-data.d/`, and `/data/adb/post-mount.d/`. If the next boot sequence is interrupted or crashes, AshReXcue compares the new state against the cataloged baseline. The newly added or modified file is identified as the probable culprit.

### 2. Boot Script Guard & Recovery Vault
Unlike standard tools that only manage `/data/adb/modules/`, AshReXcue provides first-class protection for standalone scripts in `service.d` and `post-fs-data.d`. Rather than deleting these scripts outright, AshReXcue moves them into an isolated recovery vault inside `/data/adb/modules/AshLooper/` where users can inspect and fix them after a successful restart.

### 3. SystemUI Crash Loop Detection
Certain bad theme overlays or font packs boot successfully past the kernel and Zygote stages but trigger repeated crashes inside `com.android.systemui`, rendering the device black or unusable. AshReXcue runs a lightweight background watchdog that monitors SystemUI process stability. If SystemUI crashes three times in rapid succession, AshReXcue initiates automated recovery.

## Configuration & WebUI Dashboard

AshReXcue provides an interactive local WebUI dashboard:

1. Flash `AshReXcue_Bootloop_Protector_*.zip` in your root manager.
2. During installation, use volume keys to select your baseline options (e.g. enabling Boot Script Monitoring).
3. Reboot your device.
4. Launch the WebUI:
   - In KernelSU / APatch: Tap the WebUI button on the module tile.
   - In Magisk: Open via MMRL or WebUI X Standalone.
5. In the WebUI, you can:
   - Configure the **Whitelist Manager** to exempt mission-critical security modules from ever being disabled.
   - Review the **Activity Log** to view timestamps, boot times, and daemon status.
   - Adjust stability timeframes and crash thresholds.
6. Module configuration and state persist at:
   ```bash
   /data/adb/modules/AshLooper/
   ```

## Troubleshooting & Verification

- **Testing Protection Safely**: To verify the watchdog without breaking your device, create a benign dummy script in `/data/adb/service.d/test_loop.sh` that exits immediately, then check the WebUI activity log to see it registered in the differential tracking catalog.
- **Module Vault Recovery**: If a script was quarantined during a false alarm, navigate to the **Items** tab in the WebUI to restore it from the quarantine vault.

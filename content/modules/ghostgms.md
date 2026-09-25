---
id: "ghostgms"
title: "GhostGMS: Systemless Google Play Services Battery & Privacy Optimization"
sidebarTitle: "GhostGMS"
description: "Safe, reversible Google Play Services optimizer by Kaushik designed to reduce background battery drain, wake locks, and telemetry across Android 10 through 16."
category: "performance-kernel"
tier: 1
searchQueries:
  - "ghostgms magisk module"
  - "kaushik ghostgms"
  - "google play services battery drain fix root"
  - "gms optimization module magisk"
  - "ghostgms core vs legacy"
prerequisites:
  - "Android 10 through Android 16"
  - "Magisk v20+ or KernelSU"
  - "Stock Google Play Services installed on the target device"
conflicts: []
configPaths:
  - "/data/adb/modules/ghostgms/"
  - "/data/local/tmp/ghostgms_uninstall.log"
features:
  - "Balanced GMS service suppression: targets excessive wake locks and background polling without breaking Firebase Cloud Messaging (FCM) push notifications"
  - "Privacy telemetry suppression: disables non-essential Google telemetry, usage tracking, and ad-measurement background daemons"
  - "Non-destructive architecture: avoids deleting system packages, applying all modifications systemlessly via property and service controls"
  - "Full uninstallation reversibility: tracks pre-install states and restores original settings and services cleanly during uninstallation"
  - "Dual variant availability: offers GhostGMS Core for maximum stability alongside GhostGMS Legacy for aggressive deep tweaks"
---

## Overview

GhostGMS, developed by Kaushik (`@kaushikieeee`), is a systemless optimization module focused on making Google Play Services (GMS) lighter, quieter, and more battery-friendly. On stock Android devices, Google Play Services is a major source of idle power consumption—frequently waking the device from deep sleep to sync flags, report analytics, poll device location, and run background diagnostics.

While blunt debloating scripts often disable GMS components indiscriminately—causing broken push notifications, app crashes, and Google account login failures—GhostGMS uses a carefully tuned, safe approach. It suppresses unneeded background telemetry and idle wakelocks while preserving critical notification pipelines and authentication frameworks.

## Prerequisites & Compatibility

- **Android Version**: Android 10 through Android 16.
- **Root Environment**: Magisk v20.0 or higher, or KernelSU.
- **Prerequisite Services**: Requires devices running Google Play Services. Devices running pure microG or de-Googled ROMs do not need this module.

There are no documented module conflicts. However, using multiple competing GMS freezing modules (such as Frosty) at the same time is redundant; choose the module that best fits your preference for automated presets (GhostGMS) versus granular per-category toggles (Frosty).

## Module Variants

GhostGMS is published in two targeted editions:

1. **GhostGMS Core (Recommended)**: The primary build designed for daily drivers. Focuses on safe defaults, maximum app compatibility, zero notification delays, and rock-solid stability.
2. **GhostGMS Legacy**: An alternative build incorporating older, more aggressive deep system tweaks. Intended for power users and benchmark testers willing to test edge-case app interactions.

## Key Capabilities & Architecture

- **Wakelock & Alarm Throttling**: Restricts aggressive GMS alarm frequencies that prevent the CPU from entering deep sleep states during screen-off intervals.
- **Telemetry Disablement**: Silences Google Clearcut, Phenotype, and ad metrics services that periodically upload device telemetry.
- **Full Rollback Engine**: GhostGMS tracks applied settings and properties. When uninstalled from your root manager, its uninstaller script automatically reverts all settings, properties, and service states to their pre-install values, outputting an audit log to `/data/local/tmp/ghostgms_uninstall.log`.

## Installation & Verification

1. Download the latest `GhostGMS-Core-*.zip` release from the repository.
2. Flash the zip via Magisk Manager or KernelSU.
3. Reboot your device.
4. Active module assets reside in:
   ```bash
   /data/adb/modules/ghostgms/
   ```

### Verifying Battery Impact

To verify that GMS is entering idle sleep properly:
- Leave the device unplugged with the screen off for several hours.
- Inspect battery usage under **Android Settings > Battery**. Google Play Services should register minimal background active time (typically < 1–2%).
- Verify that real-time push notifications from apps like WhatsApp, Telegram, or Gmail arrive promptly.

## Troubleshooting

- **Delayed Notifications**: If you experience delayed push alerts on specific apps, verify that those individual user apps are set to "Unrestricted" in **Android Settings > Battery > App Battery Usage**. GhostGMS keeps GMS push delivery intact, but aggressive OEM battery killers may still sleep the client apps.
- **Reviewing Uninstall State**: If you decide to remove GhostGMS, inspect `/data/local/tmp/ghostgms_uninstall.log` after rebooting to confirm that original system properties were fully restored.

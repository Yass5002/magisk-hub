---
id: "twrp-keep"
title: "TWRP A/B Retention Script: Seamless Recovery Preservation After OTA Updates"
sidebarTitle: "TWRP A/B Retention"
description: "Specialized OTA hook created by osm0sis to preserve TWRP custom recovery across seamless A/B partition updates before completing Magisk inactive slot installation."
category: "system-environment"
tier: 1
searchQueries:
  - "twrp keep magisk module"
  - "twrp a/b retention script osm0sis"
  - "keep twrp after ota update"
  - "install magisk to inactive slot twrp"
  - "magisk ota retention script"
prerequisites:
  - "Android device with seamless A/B or Virtual A/B partition architecture"
  - "TWRP or compatible custom recovery installed in the active boot/vendor_boot ramdisk"
  - "Magisk v15.0 or newer"
conflicts:
  - "Legacy A-only partition devices (devices without dual slot A/B architecture)"
configPaths: []
features:
  - "Zero-footprint retention: operates purely as a flashable installation hook without placing persistent binary payloads on `/data`"
  - "Seamless OTA integration: bridges the gap between official stock OTA updates and custom recovery persistence"
  - "Complementary Magisk workflow: designed specifically to be flashed immediately prior to Magisk's 'Install to Inactive Slot' step"
  - "Prevents stock recovery reflash: intercepts OEM OTA payload transitions to ensure TWRP survives slot migration"
---

## Overview

The TWRP A/B Retention Script, authored by veteran Android developer osm0sis on XDA-Developers, solves a fundamental challenge on modern A/B and Virtual A/B Android devices: surviving stock Over-The-Air (OTA) system updates without losing custom recovery.

On modern A/B devices, stock OTA updates download the complete new operating system and flash it directly to the background, inactive partition slot. Because recovery is often bundled inside the boot or vendor_boot ramdisk, the OTA process writes a clean stock boot image to that inactive slot. If the phone reboots normally, TWRP is wiped. The TWRP A/B Retention Script patches the inactive slot's newly written ramdisk to preserve TWRP before the device reboots.

## Prerequisites & Compatibility

- **Partition Scheme**: The device **must** be an A/B or Virtual A/B device (standard on devices launched with Android 7.1 and later, including Google Pixel, OnePlus, Motorola, and Xiaomi A/B models). Legacy "A-only" devices are incompatible.
- **Root Manager**: Magisk v15.0 or higher.
- **Custom Recovery**: A functioning TWRP installation already present in the active boot image.

### Zero-Footprint Nature

As explicitly documented by osm0sis:
> **This is NOT a normal module - it will NOT install any actual files.**

The zip acts purely as an automated script runner. While it may register in the Magisk Manager module list with a placeholder version to allow update tracking, it does not maintain active runtime daemons or persistent directories in `/data/adb/modules/twrp-keep/`.

## The Exact OTA Update Workflow

To apply a system update while keeping both TWRP and Magisk intact, follow this sequence:

1. **Download the OTA**: Navigate to **Android Settings > System > System Update** and begin the standard system update. Allow it to download and complete Step 1 and Step 2 (installation).
2. **DO NOT REBOOT**: When the update finishes and prompts you to "Restart Now", **do not tap it**.
3. **Flash the Retention Script**:
   - Open the **Magisk** app.
   - Navigate to the **Modules** tab.
   - Tap **Install from storage** and select `TWRP_A_B_Retention_Script-Magisk-*.zip`.
   - The script identifies the inactive slot and repatches its newly written boot image with your current TWRP ramdisk.
4. **Reinstall Magisk**:
   - Return to the Magisk home screen.
   - Tap **Install** next to the Magisk card.
   - Choose **Install to Inactive Slot (After OTA)**.
   - Tap **Let's Go** to patch root into the inactive slot.
5. **Reboot**: Once Magisk completes its inactive slot installation, press the **Reboot** button within the Magisk app. The device switches to the updated slot with both TWRP and root fully preserved.

## Troubleshooting & Important Notes

- **Accidental Reboot Before Retention**: If the phone reboots immediately after an OTA before running the retention script and Magisk inactive slot patch, the device will boot into an unrooted stock system with stock recovery. You will need to re-flash TWRP or a patched boot image via Fastboot from a PC.
- **Fake Update Notification**: Magisk may show an update permanently available for `twrp-keep`. This is intentional design by the developer to allow re-downloading and executing updated retention logic on demand.

---
id: "oneplus-8series-9r-camera-unlocker"
title: "OnePlus 8-Series & 9R Camera Unlocker: Full Auxiliary Camera & Long Exposure Access"
sidebarTitle: "OnePlus Camera Unlocker"
description: "Unlocks auxiliary cameras (ultra-wide, telephoto, macro) and up to 5-second long exposure capture in GCam and third-party camera apps on OnePlus 8, 8 Pro, 8T, and 9R."
category: "customization-ui"
tier: 1
searchQueries:
  - "oneplus 8 camera unlocker magisk"
  - "oneplus 8 pro gcam aux camera root"
  - "oneplus 8t 9r aux camera unlocker"
  - "enable telephoto ultrawide gcam oneplus"
  - "open camera long exposure oneplus 8"
prerequisites:
  - "Root access via Magisk"
  - "OnePlus 8, OnePlus 8 Pro, OnePlus 8T, or OnePlus 9R"
  - "OxygenOS or compatible AOSP-based custom ROM"
conflicts: []
configPaths:
  - "/data/adb/modules/oneplus-8series-9r-camera-unlocker/"
features:
  - "Full auxiliary lens access: exposes ultra-wide, telephoto, and macro camera sensors to third-party photography apps (GCam ports and Open Camera)"
  - "OxygenOS version independence: functions across different OxygenOS builds without requiring ROM-specific camera modifications"
  - "Extended shutter speed: unlocks long-exposure exposure times up to 5 seconds in supported camera applications"
  - "Package name agnostic: allows utilizing auxiliary sensors without restricting installations to specific whitelist package IDs"
  - "Systemless camera provider overlay: modifies camera vendor XML permissions systemlessly without editing system partitions"
---

## Overview

On OnePlus 8, 8 Pro, 8T, and 9R devices, stock OxygenOS restricts access to secondary camera sensors—such as the ultra-wide lens, telephoto optical zoom module, and dedicated macro sensor—to OnePlus's proprietary stock camera application. Third-party applications and Google Camera (GCam) ports are typically blocked from enumerating auxiliary camera IDs unless specifically spoofed or patched.

**OnePlus 8-Series & 9R Camera Unlocker** is a systemless Magisk module that eliminates these artificial restrictions. By patching vendor camera capabilities and system permission profiles, it grants GCam and third-party apps complete, unrestricted access to every physical lens on the device.

## Key Capabilities

- **Auxiliary Camera Access**: Freely switch between main, ultra-wide, and telephoto sensors inside popular GCam ports (such as BSG, BigKaka, and Arnova8G2) without needing specialized package name renaming.
- **Long Exposure Support**: Extends manual exposure capabilities in apps like Open Camera, enabling long-shutter night captures of up to 5 seconds.
- **ROM Versatility**: Operates smoothly across stock OxygenOS 11, 12, and 13 as well as custom AOSP/LineageOS ROMs based on the OnePlus 8 series kernel tree.

## Installation & Configuration

1. Download the latest `oneplus-8series-9r-camera-unlocker.zip` from releases.
2. Flash the module in **Magisk Manager**.
3. Reboot your device.
4. Launch your preferred GCam port and enable auxiliary cameras in the developer settings or lens configuration menu.

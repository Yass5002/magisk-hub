---
id: "universal-gms-doze"
title: "Universal GMS Doze: Battery Optimization for Google Play Services"
sidebarTitle: "Universal GMS Doze"
description: "Patches Google Play Services and background processes to participate in Android Doze battery optimization, curbing idle battery drain on Android 6 through 15+."
category: "performance-kernel"
tier: 1
searchQueries:
  - "universal gms doze magisk"
  - "marspatrick universal gms doze"
  - "google play services battery optimization root"
  - "force gms into deep doze"
  - "kernelsu universal gms doze webui"
prerequisites:
  - "Root access via Magisk, KernelSU, or APatch"
  - "Android 6.0 (API 23) through Android 15+"
conflicts: []
configPaths:
  - "/data/adb/modules/universal-gms-doze/"
features:
  - "Doze whitelist de-privileging: strips Google Play Services (com.google.android.gms) from the mandatory system battery optimization exemption list"
  - "Deep sleep enforcement: forces GMS background sync routines to respect platform Doze idle windows when the phone is motionless"
  - "FCM push notification retention: intelligently preserves high-priority Firebase Cloud Messaging delivery so chat messages arrive promptly"
  - "Modern Android 15+ compatibility: community fork actively maintained with patches for recent Android framework revisions and KernelSU"
  - "Embedded WebUI: adjust optimization rules and review active process doze states via an intuitive web control interface"
---

## Overview

Starting with Android 6.0 Marshmallow, Google introduced **Doze Mode**, an operating system power-saving mechanism that puts background apps to sleep and bundles network tasks into periodic maintenance windows. Ironically, Google hardcodes its own **Google Play Services** framework into the permanent power-exemption whitelist, meaning GMS processes can wake the CPU, initiate network handshakes, and query location at any time, leading to significant overnight battery drain.

Maintained by MarsPatrick (forked and modernized from the original work by gloeyisk), **Universal GMS Doze** is a systemless module that removes Google Play Services from the mandatory battery optimization exemption list, allowing GMS to enter deep sleep alongside other applications.

## How It Operates

1. **Permission Whitelist Removal**: Modifies the system power-management configuration to revoke GMS's permanent Doze immunity.
2. **Scheduled Sync Bundling**: Defers non-critical Google telemetry syncs, analytical pings, and background location queries until the device is actively in use or during standard Doze maintenance intervals.
3. **Notification Preservation**: High-priority Firebase Cloud Messaging (FCM) pushes (such as incoming WhatsApp calls or Telegram messages) continue to wake the device as designed.

## Multi-Root & WebUI Support

- **Broad Ecosystem**: Fully compatible with **Magisk**, **KernelSU**, and **APatch**.
- **Interactive WebUI**: On KernelSU and APatch, you can open the module's WebUI to inspect which GMS components are currently optimized and toggle individual service exceptions.

## Installation

1. Download the latest `gms_*.zip` archive from GitHub releases.
2. Flash the module in your root manager.
3. Reboot your device.
4. *(Verification)*: Check **Settings > Apps > Special app access > Battery optimization**. Google Play Services will now show as "Optimized" or available for battery optimization.

---
id: "deviceidchanger"
title: "DeviceID & SSAID Changer: Systemless WebUI Identifier Manager"
sidebarTitle: "DeviceID Changer"
description: "FOSS systemless WebUI utility to inspect and randomize Android SSAID and DeviceID parameters, preventing app-level persistent bans and tracking without detectable standalone APKs."
category: "security-certificates"
tier: 1
searchQueries:
  - "deviceidchanger magisk"
  - "change ssaid webui kernelsu"
  - "sidex15 deviceidchanger"
  - "settings secure android_id changer"
  - "bypass banking app device id ban root"
prerequisites:
  - "Rooted Android device running Magisk, KernelSU, or APatch"
  - "Updated Android System WebView package"
  - "WebUI environment (KernelSU / APatch built-in, or KSU WebUI Standalone / MMRL on Magisk)"
conflicts: []
configPaths:
  - "/data/adb/modules/deviceidchanger/"
features:
  - "SSAID & DeviceID spoofing: dynamically modifies `Settings.Secure.ANDROID_ID` values across target applications"
  - "Stealthy systemless operation: eliminates the need for third-party ID-changer APKs that often trigger banking anti-fraud scanners"
  - "FOSS and ad-free: lightweight open-source architecture with zero analytics, trackers, or commercial monetization"
  - "Intuitive WebUI: retro-themed 7.css user interface accessible directly from root manager dashboards"
---

## Overview

DeviceID / SSAID Changer, created by sidex15, is an open-source systemless module that allows rooted Android users to modify their device's SSAID (`Settings.Secure.ANDROID_ID`) and hardware identifiers directly via a WebUI interface. 

Certain financial, banking, and gaming applications record your device's unique SSAID upon initial launch. If root access is detected, or if an account is restricted, the application can ban the hardware fingerprint, preventing access even after reinstallation. While standalone Device ID changer apps exist on the Play Store, they frequently require paid subscriptions, inject advertisements, and contain package names readily flagged by banking security scanners. DeviceID Changer operates entirely as a root module, avoiding APK detection vectors completely.

## Prerequisites & Compatibility

- **Root Environment**: Compatible across Magisk, KernelSU (and its forks), and APatch.
- **WebUI Host**:
  - On **KernelSU** and **APatch**, the WebUI opens directly from the module listing.
  - On **Magisk**, users must install either [KSU WebUI Standalone](https://github.com/5ec1cff/KsuWebUIStandalone) or [MMRL](https://github.com/MMRLApp/MMRL) to render the module's HTML/JS interface.
- **System WebView**: Requires an up-to-date version of Android System WebView from the Google Play Store to properly execute modern JavaScript bindings.

There are no documented module conflicts.

## Architecture & How It Works

Android generates a 64-bit hex string (`ANDROID_ID`) for each application and user profile. DeviceID Changer interacts with Android's system settings provider directly from a root shell context:

- It interrogates the current SSAID registry for installed applications.
- Allows users to generate random compliant 16-character hexadecimal identifiers or manually specify custom strings.
- Writes the modified values directly into the Android `settings.db` secure table without requiring full device reboots.

## Configuration & Usage

1. Flash `DeviceID-Changer.zip` via Magisk, KernelSU, or APatch.
2. Launch the WebUI:
   - In KernelSU / APatch: Tap the WebUI button on the module tile.
   - In Magisk: Launch KSU WebUI Standalone or MMRL and select DeviceID Changer.
3. Select the target application whose SSAID you want to change.
4. Input a new hexadecimal ID or press randomize, then apply the changes.
5. Active module assets and WebUI files reside in:
   ```bash
   /data/adb/modules/deviceidchanger/
   ```

## Troubleshooting & Verification

- **Blank Screen in WebUI**: If the WebUI opens to a blank screen or fails to respond to input, update **Android System WebView** via the Google Play Store. Outdated system webviews lack support for current DOM and CSS properties.
- **Identifier Reverts After Launch**: Ensure the target application is completely force-stopped (`am force-stop <package>`) prior to modifying its SSAID in the WebUI so it does not overwrite the database from active process memory.

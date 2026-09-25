---
id: "scalpel"
title: "Scalpel: Precision System Debloater & App Systemizer for Android"
sidebarTitle: "Scalpel Debloater"
description: "Precision debloat and app systemization utility for rooted Android. Safely disables OEM/carrier bloatware and promotes user apps to system priv-app status."
category: "system-utilities"
tier: 1
searchQueries:
  - "scalpel magisk debloat"
  - "enginex0 scalpel"
  - "android app systemizer kernelsu"
  - "safely remove oem bloatware magisk"
  - "convert user app to system app root"
prerequisites:
  - "Root access via Magisk, KernelSU, or APatch"
conflicts: []
configPaths:
  - "/data/adb/modules/scalpel/"
features:
  - "Surgical debloating: selectively replaces or masks carrier bloatware, telemetry stubs, and preinstalled vendor apps"
  - "App systemization: elevates selected third-party user applications to /system/priv-app/ for privileged system permission access"
  - "Zero-risk safety: operates completely through systemless overlay mounts, allowing instant rollback in case of an issue"
  - "Cross-root manager engine: native compatibility with Magisk, KernelSU, and APatch environments"
  - "Preconfigured debloat presets: includes community-verified debloating lists for major OEMs (Xiaomi, Samsung, OnePlus, Google)"
---

## Overview

Modern Android OEM firmware arrives laden with redundant analytics daemons, duplicate cloud sync services, and carrier-sponsored bloatware. Attempting to manually delete these packages from read-only system partitions can trip dm-verity, break OTA updates, or render devices unbootable if a critical dependency is accidentally severed.

Authored by Enginex0, **Scalpel** is a surgical system utility engineered for precision debloating and application systemization on rooted Android devices. Built for safety and simplicity, Scalpel enables users to purge unwanted system bloat and elevate third-party apps to privileged system status without risk.

## Core Capabilities

### 1. Precision Debloating
- **Systemless Masking**: Mounts empty directories over targeted bloatware APK folders in `/system/app/`, `/product/app/`, or `/system/priv-app/`.
- **Fail-Safe Operation**: If removing a package causes instability, disabling the module in your root manager immediately restores the original stock application intact.

### 2. App Systemization
- **Privileged Elevation**: Moves user-installed applications (such as custom launchers, automation services, or VPN tools) into `/system/priv-app/`.
- **Permission Unlocks**: Grants access to restricted Android system-level permissions—such as `ACCESS_BACKGROUND_LOCATION`, notification listening overrides, and device administration—without requiring ADB grants after every reboot.

## Supported Root Environments

Scalpel is designed from the ground up to support modern root management frameworks:
- **Magisk** (v20.4+)
- **KernelSU** (v0.6.0+)
- **APatch** (v10.5+)

## Installation & Usage

1. Download the latest `scalpel-v*.zip` archive from GitHub releases.
2. Flash the module using your root manager.
3. Reboot your device.
4. Follow the module's interactive terminal setup or edit its configuration file under `/data/adb/modules/scalpel/` to specify apps to debloat or systemize.

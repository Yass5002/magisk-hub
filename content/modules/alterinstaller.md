---
id: "alterinstaller"
title: "AlterInstaller: Package Manager Origin & Update Owner Spoofing"
sidebarTitle: "AlterInstaller"
description: "Systemless utility by chenxiaolong that spoofs app installer and update owner attributes in Android's package database without runtime Zygisk injection."
category: "system-environment"
tier: 1
searchQueries:
  - "alterinstaller magisk module"
  - "chenxiaolong alterinstaller"
  - "spoof play store installer package root"
  - "android packages.xml update owner spoof"
  - "change installing package android 14"
prerequisites:
  - "Android 12 or newer (Android 12, 13, 14, 15, 16)"
  - "Root access via Magisk or KernelSU"
conflicts:
  - "Android 11 and older operating systems (strictly unsupported)"
configPaths:
  - "/data/local/tmp/AlterInstaller.json"
  - "/data/local/tmp/AlterInstaller.log"
  - "/data/system/packages.xml"
features:
  - "Installer package spoofing: overrides `installer`, `initiating installer`, and `update owner` attributes for any target app"
  - "Hookless XML manipulation: modifies `/data/system/packages.xml` directly during early boot before PackageManagerService initializes, requiring zero Zygisk overhead"
  - "Anti-sideload detection bypass: satisfies security checks in banking and enterprise apps that require installation through the official Google Play Store"
  - "App store update control: binds sideloaded open-source packages to specific managers (e.g. F-Droid, Droid-ify) to prevent accidental Play Store updates"
---

## Overview

AlterInstaller, developed by renowned Android software engineer chenxiaolong, is a specialized root utility designed to spoof package manager provenance metadata on Android 12 and newer. 

Modern Android applications increasingly enforce anti-sideloading checks. Financial applications, DRM-protected media players, and games query `PackageManager.getInstallSourceInfo()` to discover which app installed them. If the application was sideloaded via an APK installer rather than downloaded through Google Play (`com.android.vending`), the app may restrict features or refuse to launch. Additionally, on Android 14+, the OS enforces "Update Ownership" rules, tying an app's update rights to a specific store.

AlterInstaller resolves both issues. By directly patching `/data/system/packages.xml` during early boot before Android's system services start, it safely modifies package metadata without requiring invasive runtime memory hooks.

## Prerequisites & Compatibility

- **Android Version**: **Android 12 and newer only**. Android 11 and earlier releases lack the corresponding update ownership and installer separation fields and are unsupported.
- **Root Environment**: Compatible with both Magisk and KernelSU.
- **Hookless Design**: Requires no Zygisk, LSPosed, or Xposed frameworks.

There are no documented module conflicts.

## Configuration & Usage

AlterInstaller reads its instructions from a simple JSON manifest placed in `/data/local/tmp/`:

1. Install `AlterInstaller-*.zip` in Magisk or KernelSU.
2. Using any root file manager or terminal, create `/data/local/tmp/AlterInstaller.json`:
   ```bash
   su
   cat << 'EOF' > /data/local/tmp/AlterInstaller.json
   {
       "org.videolan.vlc": {
           "installer": "com.android.vending",
           "updateOwner": "com.looker.droidify"
       },
       "com.example.bankingapp": {
           "installer": "com.android.vending"
       }
   }
   EOF
   ```
3. Set appropriate read permissions (`chmod 644 /data/local/tmp/AlterInstaller.json`).
4. Reboot your device.
5. During early boot, AlterInstaller parses the JSON, modifies the matching package tags in `/data/system/packages.xml`, and writes an execution log.

### Supported Properties

| Key | Description | Example |
| :--- | :--- | :--- |
| `installer` | The package name reported as the installing source | `com.android.vending` (Google Play) |
| `updateOwner` | The package authorized to apply future updates | `com.looker.droidify` or `org.fdroid.fdroid` |

## Troubleshooting & Verification

- **Verifying Applied Changes**: Check the output log immediately following a reboot:
  ```bash
  cat /data/local/tmp/AlterInstaller.log
  ```
- **Querying Package Manager Directly**: Verify how Android now reports the target application's install source:
  ```bash
  su -c "dumpsys package com.example.bankingapp | grep -E 'installerPackageName|initiatingPackageName'"
  ```
- **Changes Persisting After Uninstall**: Because AlterInstaller writes valid tags directly to the persistent `/data/system/packages.xml` database file, modified package attributes persist even if the module is disabled or removed. To revert an app, remove its entry from `AlterInstaller.json` and reboot.

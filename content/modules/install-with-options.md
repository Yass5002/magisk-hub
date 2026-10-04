---
id: "install-with-options"
title: "Install with Options: Advanced On-Device APK Installer via Shizuku"
sidebarTitle: "Install with Options"
description: "FOSS package installer utility by zacharee that leverages Shizuku shell privileges to install test-only packages, split APKs, and bypass low target SDK blocks on modern Android."
category: "system-utilities"
tier: 1
searchQueries:
  - "install with options apk download"
  - "bypass low target sdk block android 14"
  - "install test only apk without computer"
  - "shizuku split apk installer"
  - "installwithoptions zacharee"
prerequisites:
  - "Android 8.0 (Oreo) or newer (Target SDK bypass requires Android 14+)"
  - "Active Shizuku service via Wireless ADB or Root (Magisk/KernelSU/APatch)"
conflicts:
  - "Architecture mismatches (INSTALL_FAILED_NO_MATCHING_ABIS when installing 32-bit legacy apps on 64-bit-only hardware like Pixel 7/8/9)"
  - "Mismatched signature updates on un-patched systems (requires CorePatch for signature overwrites)"
configPaths:
  - "/data/data/dev.zwander.installwithoptions/"
features:
  - "Low target SDK bypass: passes --bypass-low-target-sdk-block to install legacy Android 4/5 apps on Android 14+"
  - "Test-only package support: installs development builds compiled with android:testOnly='true'"
  - "Split APK & bundle installation: seamlessly merges base and config splits (.apks, .xapk) without external split installers"
  - "Complete on-device execution: eliminates the need for computer-based 'adb install' commands"
faq:
  - question: "Why does Android 14 block older apps from being installed by default?"
    answer: "Starting with Android 14, Google's PackageManagerService enforces a minimum targetSdkVersion of 23 (Android 6.0 Marshmallow) to prevent legacy malware from bypassing modern runtime permission models. Sideloading such apps via standard Android package installers fails with `INSTALL_FAILED_DEPRECATED_SDK_VERSION`. Install with Options resolves this by appending the `--bypass-low-target-sdk-block` flag via Shizuku shell execution."
  - question: "Can Install with Options bypass APK signature conflicts?"
    answer: "No. Install with Options controls installation flags (test-only, downgrade, target SDK), but does not hook system memory. To install an update signed with a different certificate without uninstalling the original app, you must install and enable the CorePatch Xposed module."
  - question: "Why do some older apps fail with INSTALL_FAILED_NO_MATCHING_ABIS?"
    answer: "Modern SoCs (e.g. Google Tensor G3/G4, Snapdragon 8 Gen 3) have completely dropped hardware ARM32 (armeabi-v7a) support and run in 64-bit-only mode. If an older app only includes 32-bit native libraries, the hardware cannot execute them, and installation fails regardless of installation flags."
---

## Overview

Starting with Android 14, Google significantly restricted what applications users can sideload onto their devices. The operating system now blocks the installation of applications targeting older Android API levels (to prevent malicious software from evading modern runtime permissions), rejects developer test builds (`android:testOnly="true"`), and restricts installation parameters.

Traditionally, circumventing these limitations required connecting the phone to a desktop computer with ADB and running command-line instructions:
```bash
adb install --bypass-low-target-sdk-block -t app.apk
```

**Install with Options**, created by prolific Android developer zacharee (Zachary Wander), solves this limitation by bringing desktop-grade `pm install` capability directly onto the device. By interfacing with **Shizuku**, the application gains shell-level package installation authority, allowing users to customize installation flags on the fly.

---

## Technical Architecture & Installation Flags

When an APK or split bundle is opened in Install with Options, the application passes parameters directly to `PackageInstaller.SessionParams` via Shizuku's privileged shell IPC:

```
┌────────────────────────────────────────────────────────┐
│               Install with Options UI                  │
│  - Select APK / Split Bundle (.apks, .xapk)            │
│  - User selects flags: [x] Bypass Low SDK  [x] Test    │
└───────────────────────────┬────────────────────────────┘
                            │ Dispatches via Shizuku
┌───────────────────────────▼────────────────────────────┐
│                    Shizuku Service                     │
│  - Gains android.permission.INSTALL_PACKAGES (UID 2000)│
└───────────────────────────┬────────────────────────────┘
                            │
┌───────────────────────────▼────────────────────────────┐
│         Android PackageInstaller Session               │
├────────────────────────────────────────────────────────┤
│ Flags Applied:                                         │
│ • --bypass-low-target-sdk-block                        │
│ • -t (INSTALL_ALLOW_TEST)                              │
│ • -d (INSTALL_REQUEST_DOWNGRADE)                       │
│ • --dont-kill (Keep existing process alive)            │
└────────────────────────────────────────────────────────┘
```

---

## Core Capabilities & Features

### 1. Bypass Android 14+ Low Target SDK Block
Modern devices reject retro games, abandoned utilities, and classic tools compiled for Android 5.1 or older. Install with Options automatically passes `--bypass-low-target-sdk-block`, enabling seamless installation of legacy applications on Android 14 and Android 15.

### 2. Test-Only Build Installation (`-t`)
Android Studio compiles debug builds with `android:testOnly="true"` by default. Standard Android PackageInstaller will throw `INSTALL_FAILED_TEST_ONLY`. Install with Options intercepts the file and installs it without requiring APK re-signing or decompilation.

### 3. Native Split APK / App Bundle Support
Many modern applications distribute multiple split APKs (base APK + language configs + DPI screen assets). Install with Options opens `.apks`, `.xapk`, and raw multi-APK selections, streams them into a single atomic installation session, and installs them cleanly.

---

## Usage Guide

1. Install and activate **Shizuku** on your device.
2. Sideload and launch **Install with Options**.
3. Grant Shizuku permissions when prompted.
4. Tap **Select File** and pick the `.apk`, `.apks`, or `.xapk` archive.
5. Review the installation options dialog:
   - Toggle **Bypass Low Target SDK Block** if installing legacy apps on Android 14+.
   - Toggle **Allow Test-Only** if installing development test APKs.
   - Toggle **Allow Downgrade** if attempting a rollback.
6. Tap **Install** to commit the package.

---

## Troubleshooting Common Errors

### `INSTALL_FAILED_NO_MATCHING_ABIS`
- **Cause**: The application includes native libraries compiled for an unsupported architecture (e.g., 32-bit ARM on 64-bit-only hardware like Pixel 7/8/9).
- **Resolution**: This is a physical hardware CPU limitation. You must locate a 64-bit (`arm64-v8a`) version of the package.

### `INSTALL_FAILED_UPDATE_INCOMPATIBLE`
- **Cause**: The package's signing certificate does not match the certificate of the app already installed on device.
- **Resolution**: Install with Options cannot forge cryptographic signatures. Enable **CorePatch** in LSPosed to bypass signature verification checks.

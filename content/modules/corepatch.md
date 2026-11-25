---
id: "corepatch"
title: "CorePatch: Disable Android APK Signature & Downgrade Restrictions"
sidebarTitle: "CorePatch"
description: "LSPosed-maintained Xposed module (org.lsposed.corepatch) using libxposed API 101 to bypass APK signature verification, allow app downgrades without data loss, and permit cross-signature overwrites."
category: "xposed-runtime-hooks"
tier: 1
searchQueries:
  - "corepatch lsposed apk"
  - "lsposed corepatch download"
  - "disable signature verification android"
  - "downgrade android app without data loss"
  - "install conflicting signature apk root"
prerequisites:
  - "Android 9.0 (Pie) or higher with Magisk, KernelSU, or APatch"
  - "Official LSPosed framework supporting libxposed API 101"
conflicts:
  - "Legacy Lucky Patcher static core.jar/services.jar binary patches (causes system_server crashes when combined with runtime ART hooks)"
  - "Older coderstory/CorePatch package installations with conflicting package names or signatures"
configPaths:
  - "/data/adb/lspd/"
  - "/data/data/org.lsposed.corepatch/"
features:
  - "Official LSPosed/CorePatch N (`org.lsposed.corepatch`) build powered by libxposed API 101 (`XposedService` & `XposedProvider`)"
  - "Signature verification bypass: allows installation of modified, re-signed, or unsigned APKs over authentic store builds"
  - "Direct app downgrading: bypasses PackageManager `INSTALL_FAILED_VERSION_DOWNGRADE` errors without wiping app data"
  - "Cross-signature package overwrite: permits installing an APK signed with a debug key over a production release"
  - "Digest check suppression: bypasses SHA-256 package manifest digest checks on modern Android releases"
faq:
  - question: "Which scope must be selected in LSPosed for CorePatch to work?"
    answer: "CorePatch (`org.lsposed.corepatch`) ships with `staticScope=true` and `scope.list` targeting `system` (System Framework). In LSPosed Manager, ensure **System Framework** (`system`) is checked in the module's Scope list and reboot so hooks attach inside `system_server`."
  - question: "Why is CorePatch now hosted under LSPosed/CorePatch?"
    answer: "Originally authored by coderstory, CorePatch was transferred to the official **LSPosed/CorePatch** repository and modernized into CorePatch N (`N-1.0`+), migrating to libxposed API 101 (`org.lsposed.corepatch.XposedService`) for clean compatibility with newer Android versions."
  - question: "Why do I see 'INSTALL_FAILED_DUPLICATE_PERMISSION' even with CorePatch active?"
    answer: "CorePatch bypasses signature and version code checks, but Android enforces a strict permission tree rule: if an app declares a custom permission already claimed by another package with a different signature, the OS rejects it. Temporarily freeze or remove the conflicting app declaring that permission."
---

## Overview

On stock Android, `PackageManagerService` (PMS) strictly enforces application provenance using cryptographic signatures recorded in `/data/system/packages.xml`. When installing or updating an app, Android checks:

1. **Signature Mismatch**: Re-signed or modified APKs trigger `INSTALL_FAILED_UPDATE_INCOMPATIBLE`.
2. **Version Code Downgrade**: Lower `versionCode` packages fail with `INSTALL_FAILED_VERSION_DOWNGRADE`.
3. **Manifest & Digest Integrity**: Modern Android validates APK signing blocks and digests against installed package records.

Originally created by **coderstory** and now officially transferred to and maintained under **LSPosed/CorePatch** (`org.lsposed.corepatch`), **CorePatch** dynamically relaxes these checks inside Android Runtime memory via **libxposed API 101** without patching `/system/framework/services.jar` on disk.

---

## Technical Architecture & How It Works

### libxposed API 101 & `system_server` Hooking

Inspecting the `LSPosed/CorePatch` `N-1.0` release (`app-release.apk`) confirms a compact, modern libxposed architecture:

- **Package & Service Model**: `org.lsposed.corepatch` declares `io.github.libxposed.service.XposedProvider` and `org.lsposed.corepatch.XposedService` in its manifest, enabling direct module-to-framework preference synchronization via libxposed API 101 (`minApiVersion=101`, `targetApiVersion=101`).
- **Static System Scope**: `META-INF/xposed/module.prop` sets `staticScope=true` with `META-INF/xposed/scope.list` fixed to `system` (`system_server`), where Android's `PackageManagerService`, `KeySetManagerService`, and `SigningDetails` live.
- **Runtime Method Interception**: CorePatch hooks package verification paths (`SigningDetails.checkCapability()`, `PackageManagerService.checkDowngrade()`, and certificate collection routines) in memory so debug, re-signed, unsigned, or older-version APKs pass verification cleanly.

---

## Installation & Configuration

### Prerequisites
- A rooted Android device running **Magisk**, **KernelSU**, or **APatch**.
- **LSPosed** with **libxposed API 101** support.

### Step 1: Install the Module
1. Download `app-release.apk` from the official `LSPosed/CorePatch` release (`N-1.0` or newer).
2. Install the APK normally on your device (uninstall any legacy pre-transfer `coderstory` CorePatch package first if you encounter signature conflicts).

### Step 2: Enable & Reboot
1. Open **LSPosed Manager** -> **Modules**.
2. Enable **CorePatch** and confirm **System Framework** (`system`) is selected in Scope.
3. Open **CorePatch** (`org.lsposed.corepatch.MainActivity`) from your launcher (or LSPosed module settings) to configure individual toggles:
   - *Allow downgrade installation*
   - *Disable signature verification*
   - *Disable package digest checks*
   - *Allow overwrite across different signatures*
4. **Reboot** your device so `system_server` initializes with the updated hooks.

---

## Practical Use Cases

### 1. App Downgrades Without Data Loss
Roll back an updated app that introduced regressions while preserving local SQLite databases and login sessions:
```bash
# Install an older APK directly via ADB or root shell:
pm install -d /sdcard/Download/app-older.apk
```

### 2. Installing Debug or Patched Builds Over Store Releases
Install locally compiled debug builds or open-source forks directly on top of Play Store installations without clearing app data first.

---

## Troubleshooting & Recovery

### Installations Still Fail with Signature Mismatch
1. Verify **CorePatch** is enabled in LSPosed and **System Framework** (`system`) is checked in Scope.
2. Perform a full reboot after toggling options if `system_server` hooks were not yet attached.
3. Ensure no legacy static `services.jar` patches or conflicting signature-spoofing tools are active.

### Bootloop Recovery
If an unsupported ROM build causes `system_server` instability during boot:
```bash
# Disable LSPosed via ADB during boot and reboot:
adb wait-for-device shell touch /data/adb/modules/zygisk_lsposed/disable
adb reboot
```
Once booted, disable or uninstall CorePatch from your device.

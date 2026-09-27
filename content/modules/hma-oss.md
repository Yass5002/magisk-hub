---
id: "hma-oss"
title: "Hide My Applist (HMA-OSS): Conceal Installed Apps & Root Packages"
sidebarTitle: "Hide My Applist"
description: "Standalone Zygisk module that conceals installed applications, root managers, and custom packages from detection without requiring LSPosed."
category: "root-management"
tier: 1
searchQueries:
  - "hma oss zygisk module download"
  - "hide my applist zygisk"
  - "how to hide root apps from banking"
  - "package manager hook hide apps"
  - "hma oss template configuration guide"
prerequisites:
  - "Magisk with Zygisk enabled, or KernelSU / APatch with a Zygisk provider (e.g. ZygiskNext)"
  - "Android 10 (API 29) to Android 15"
conflicts:
  - "Multiple active Zygisk loaders running concurrently"
  - "Legacy Hide My Applist Xposed modules (uninstall prior LSPosed versions)"
configPaths:
  - "/data/adb/modules/hma_oss_zygisk/"
  - "/data/user/0/org.frknkrc44.hma_oss/"
features:
  - "Standalone Zygisk injection: hooks Zygote directly without needing LSPosed or Vector"
  - "Intercepts PackageManager API queries (`getInstalledPackages`, `getInstalledApplications`, `getPackageInfo`)"
  - "Blocks native C/C++ filesystem probing (`stat`, `access`, `fopen`) targeting `/data/data/<pkg>`"
  - "Built-in Application & Settings presets for automated detection protection"
  - "Activity launch protection and installation source spoofing"
  - "Completely open-source (OSS) with community audits and active bug fixes"
faq:
  - question: "Why do banking apps still detect root even with Magisk hidden or renamed?"
    answer: "Many banking apps do not simply scan for su binaries; they query the system PackageManager for installed apps such as Magisk, KernelSU, Termux, Lucky Patcher, or cheat engines. Even when the root manager itself is renamed, auxiliary root utilities expose the device. HMA-OSS intercepts PackageManager queries and native libc calls so target apps only see a clean stock environment."
  - question: "Does HMA-OSS require LSPosed or Vector?"
    answer: "No. Modern HMA-OSS operates entirely as a native Zygisk module. It injects directly into the Android Zygote process to filter package queries and native filesystem probes, removing all dependency on LSPosed or Xposed frameworks."
  - question: "How is the HMA-OSS manager app installed?"
    answer: "The downloaded release ZIP contains both the native Zygisk runtime and the companion manager app (`manager.apk`). When you flash the ZIP in Magisk, KernelSU, or APatch, the installer script automatically installs the HMA-OSS manager application into your user profile."
  - question: "Can I use HMA-OSS on KernelSU or APatch?"
    answer: "Yes. On KernelSU or APatch, install a Zygisk loader module first (such as ZygiskNext or NeoZygisk). HMA-OSS detects the active Zygisk environment during installation and functions seamlessly."
---

## Overview

Developed by **frknkrc44** and open-source contributors, **HMA-OSS** (Hide My Applist Open Source) is the premier utility for controlling which applications can query the presence of other installed applications on your device.

Android's permission model historically allowed any app with `QUERY_ALL_PACKAGES` to catalog everything installed on your phone. Aggressive banking applications, enterprise MDM agents, and DRM-protected streaming apps exploit this to build risk scores based on installed root utilities, custom ROM tools, and modded APKs. HMA-OSS intercepts these queries at both the Java and native C layers, delivering an airtight, spoofed app list.

While the original Hide My Applist project was an Xposed module, **HMA-OSS has replaced the LSPosed dependency with native Zygisk injection**, allowing it to run standalone under Magisk, KernelSU, or APatch without requiring an Xposed runtime.

---

## Technical Architecture & How It Works

### 1. Zygisk Zygote Injection
Unlike legacy Xposed modules that rely on ART hooking frameworks like LSPosed or Vector, HMA-OSS hooks directly into Android's **Zygote** startup process via Zygisk:
- When a new process is forked for a sandboxed application, HMA-OSS loads its native library into the process address space.
- Hook trampolines are injected without modifying APK bytecode or requiring persistent Xposed bridges in memory.

### 2. Dual-Layer Package Masking (Java + Native)

1. **Java Layer (PackageManager Interception)**:
   - When a target app calls `PackageManager.getInstalledPackages()`, `getInstalledApplications()`, or `getPackageInfo()`, HMA-OSS intercepts the return collection.
   - Any package declared in the target app's blacklist or enabled presets is filtered out in memory before the array is returned to the app.
2. **Native Layer (File IO Interception)**:
   - Sophisticated anti-root SDKs bypass Android Java APIs and invoke direct libc file access checks (e.g. testing `access("/data/data/com.topjohnwu.magisk", F_OK)` or `stat()`).
   - HMA-OSS hooks native C library calls (`open`, `stat`, `access`, `readlink`), returning `ENOENT` whenever the target application attempts to probe protected package data directories.
3. **Activity Launch Protection**:
   - Some detector applications attempt to resolve and trigger private component names or internal activities to deduce installed packages. HMA-OSS blocks these component launch queries for protected apps.

---

## Installation & Configuration

### Step 1: Flash the Module in Your Root Manager
1. Download the latest `HMA-OSS-ZYGISK-*.zip` from the download button above.
2. Verify your root environment has **Zygisk** active:
   - **Magisk**: Open Magisk Settings and confirm **Zygisk** is toggled ON.
   - **KernelSU / APatch**: Ensure a Zygisk implementation module (e.g. **ZygiskNext**) is flashed and active.
3. In your root manager (Magisk, KernelSU, or APatch), navigate to the **Modules** tab.
4. Tap **Install from storage** and select the downloaded `HMA-OSS-ZYGISK-*.zip`.
5. Allow the installation script to complete. The installer will deploy the Zygisk libraries and automatically install the companion **HMA-OSS** manager app (`manager.apk`).
6. Reboot your device.

### Step 2: Configure HMA-OSS Presets & Hiding
1. Open the **HMA-OSS** app from your launcher.
2. Tap **Manage apps** and select the application you want to protect (e.g. your banking app or detector app).
3. Toggle **Enable hide** to the ON position.
4. Under **Template config**, tap **Using X presets**:
   - Check **Detector apps**, **Root managers / rooted apps**, **Shizuku / Dhizuku apps**, and **Xposed modules**.
5. Under **Using X settings presets**:
   - Check **Developer options** and **Accessibility** to hide root-related system settings.
6. (Recommended) Ensure **Activity launch protection** is enabled to prevent intent-based component scanning.
7. Force-close your target app and reopen it. It will now see only a clean, stock app environment.

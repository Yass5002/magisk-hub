---
id: "hma-oss"
title: "Hide My Applist (HMA-OSS): Conceal Installed Apps & Root Packages"
sidebarTitle: "Hide My Applist"
description: "Powerful Xposed/Vector module that prevents snooping applications from detecting root managers, custom modules, and private apps."
category: "root-management"
tier: 1
searchQueries:
  - "hide my applist xposed module"
  - "hma oss download"
  - "how to hide root apps from banking"
  - "package manager hook hide apps"
  - "hma template configuration guide"
prerequisites:
  - "Vector, LSPosed, or modern Xposed framework active on device"
  - "Hide My Applist APK installed"
conflicts:
  - "Legacy HMA forks with broken Android 14 hooks"
configPaths:
  - "/data/adb/hma/"
  - "/data/user/0/com.tsng.hidemyapplist/"
features:
  - "Intercepts PackageManager API queries (`getInstalledPackages`, `getInstalledApplications`, `getPackageInfo`)"
  - "Blocks native C/C++ filesystem probing (`stat`, `access`, `fopen`) targeting `/data/data/<pkg>`"
  - "Powerful template system: create reusable hiding profiles (e.g. 'Banking Profile', 'Gaming Profile')"
  - "Completely open-source (OSS) with community audits and active bug fixes"
faq:
  - question: "Why do banking apps still know I have root even with Magisk hidden?"
    answer: "Many banking apps don't just look for su binaries; they scan your entire installed package list looking for apps like Magisk, KernelSU, Termux, Lucky Patcher, or Cheat Engine. Even if Magisk is renamed, other root utilities give you away. HMA intercepts PackageManager queries so target apps see only stock system apps."
  - question: "Do I need to enable HMA in both Magisk and Vector?"
    answer: "HMA is an Xposed module. Install the APK, open Vector Manager, enable HMA in the module list, check the System Framework and target apps in Scope, then reboot."
---

## Overview

Developed by **frknkrc44** and open-source contributors, **HMA-OSS** (Hide My Applist Open Source) is the premier utility for controlling which applications can query the presence of other installed applications on your device.

Android's permission model historically allowed any app with `QUERY_ALL_PACKAGES` to catalog everything installed on your phone. Aggressive banking applications, enterprise MDM agents, and DRM-protected streaming apps exploit this to build risk scores based on installed root utilities, custom ROM tools, and modded APKs. HMA intercepts these queries at the Java and Native layers, delivering an airtight, spoofed app list.

---

## Technical Architecture & How It Works

### Dual-Layer Package Masking (Java + Native)

1. **Java Layer (PackageManager Interception)**:
   - When a target app calls `PackageManager.getInstalledPackages()` or `PackageManager.getPackageInfo()`, HMA's Xposed hooks intercept the return collection.
   - Any package declared in the target app's blacklist is filtered out in memory before the array is returned to the app.
2. **Native Layer (File IO Interception)**:
   - Many sophisticated anti-root SDKs bypass Android Java APIs and invoke direct libc file access checks (e.g. testing `access("/data/data/com.topjohnwu.magisk", F_OK)`).
   - HMA hooks native C library calls (`open`, `stat`, `access`, `readlink`), returning `ENOENT` whenever the target application attempts to probe protected package data directories.

---

## Installation & Configuration

### Step 1: Activate in Vector / LSPosed
1. Ensure **Vector** or **LSPosed** is running on your device.
2. Install `HMA-OSS.apk`.
3. Open **Vector Manager** $\rightarrow$ **Modules** $\rightarrow$ enable **Hide My Applist**.
4. In the module's **Scope**, select the target applications you want to protect (e.g., your banking apps).
5. Reboot your device.

### Step 2: Configure HMA Templates
1. Open the **Hide My Applist** app from your launcher.
2. Go to **Template management** $\rightarrow$ tap **Create a blacklist template**.
3. Name it "Root Apps Blacklist".
4. Check all root-related applications on your phone (Magisk, KernelSU, Termux, LSPosed, Lucky Patcher, etc.).
5. Go to **App management** $\rightarrow$ select your banking app $\rightarrow$ toggle **Enable hide** $\rightarrow$ select the "Root Apps Blacklist" template.
6. Force-close your banking app and verify that it launches without detecting other apps.

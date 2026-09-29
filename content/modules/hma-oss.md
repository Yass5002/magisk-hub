---
id: "hma-oss"
title: "Hide My Applist (HMA-OSS): Conceal Installed Apps & Root Packages"
sidebarTitle: "Hide My Applist"
description: "Standalone Zygisk module that filters app-list and related queries for selected target apps without requiring LSPosed."
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
  - "A rooted Android device with a compatible Zygisk environment"
conflicts:
  - "Multiple active Zygisk loaders running concurrently"
  - "Legacy Hide My Applist Xposed modules (uninstall prior LSPosed versions)"
configPaths:
  - "/data/adb/modules/hma_oss_zygisk/"
  - "/data/user/0/org.frknkrc44.hma_oss/"
features:
  - "Standalone Zygisk module that does not require LSPosed"
  - "Filters app-list and related package queries for configured target apps"
  - "Built-in detector-app presets and configurable per-app protection"
  - "Additional app-list cleanup and reduced detection points in the oss-168 release"
  - "Open-source project with translations and active upstream development"
faq:
  - question: "Why do banking apps still detect root even with Magisk hidden or renamed?"
    answer: "Many apps do not simply scan for su binaries; they also inspect which applications are installed. HMA-OSS can filter app-list and related queries for configured targets, but it is not a universal guarantee against every root, integrity, or device-state check."
  - question: "Does HMA-OSS require LSPosed or Vector?"
    answer: "No. HMA-OSS is designed to operate as a Zygisk module and does not require LSPosed for its current Zygisk workflow."
  - question: "How is the HMA-OSS manager app installed?"
    answer: "The oss-168 release ZIP contains `manager.apk` and the `35-install-manager-app.sh` installation hook. Flashing that release through a compatible root manager installs the companion HMA-OSS manager app; verify the current release contents when using a newer release."
  - question: "Can I use HMA-OSS on KernelSU or APatch?"
    answer: "The project is distributed as a Zygisk module. KernelSU and APatch users need a compatible, working Zygisk provider for their setup; verify compatibility with the current upstream documentation before installation."
---

## Overview

Developed by **frknkrc44** and open-source contributors, **HMA-OSS** (Hide My Applist Open Source) is a Zygisk module for controlling how selected applications access information about installed applications.

Android applications can use package visibility APIs and other checks to learn about installed applications. Some banking, enterprise, and security applications use that information as one signal in their risk decisions. HMA-OSS filters supported app-list and related requests for configured targets; it should not be treated as an airtight or universal concealment layer.

While the original Hide My Applist project was associated with Xposed, **HMA-OSS provides a Zygisk workflow without requiring LSPosed**, subject to the root manager and Zygisk provider being compatible with the device.

### What changed in oss-168

The current `oss-168` release (published September 13, 2026) includes upstream work that:
- adds new detector apps to presets;
- adds `NativeZygoteProcess` support;
- performs extra app-list cleanup when clearing uninstalled-app configurations;
- adds module status reporting in the root manager;
- removes unnecessary or weak dependencies and several older hooks;
- fixes or reduces several reported detection points.

The release also includes the project’s latest translation updates. Check the official release notes and wiki for implementation-specific details because the upstream README intentionally keeps the public technical description concise.

---

## Technical Architecture & How It Works

### 1. Zygisk process integration
HMA-OSS uses the Zygisk integration exposed by the Android root environment to apply its filtering behavior to configured target applications. The exact internal hook set changes over time; consult the upstream source and release notes rather than assuming a fixed list of Java or native functions.

### 2. Configured app-list filtering

The module is intended to reject or filter app-list requests for configured targets and provides presets for common detector applications. The precise behavior depends on the target app, Android version, root environment, and the active HMA-OSS release. It does not replace DenyList, a compatible Zygisk provider, or other device-specific configuration when those are required.

---

## Installation & Configuration

### Step 1: Flash the Module in Your Root Manager
1. Download the latest `HMA-OSS-ZYGISK-*.zip` from the download button above.
2. Verify your root environment has **Zygisk** active:
   - **Magisk**: Open Magisk Settings and confirm **Zygisk** is toggled ON.
   - **KernelSU / APatch**: Ensure a Zygisk implementation module (e.g. **ZygiskNext**) is flashed and active.
3. In your root manager (Magisk, KernelSU, or APatch), navigate to the **Modules** tab.
4. Tap **Install from storage** and select the downloaded `HMA-OSS-ZYGISK-*.zip`.
5. Allow the installation script to complete. In `oss-168`, the installer deploys the Zygisk libraries and installs the companion **HMA-OSS** manager app (`manager.apk`).
6. Reboot your device.

### Step 2: Configure HMA-OSS Presets & Hiding
1. Open the **HMA-OSS** app from your launcher.
2. Tap **Manage apps** and select the application you want to protect (e.g. your banking app or detector app).
3. Toggle **Enable hide** to the ON position.
4. Under **Template config**, tap **Using X presets**:
   - Check **Detector apps**, **Root managers / rooted apps**, **Shizuku / Dhizuku apps**, and **Xposed modules**.
5. Under **Using X settings presets**, if those options are available in your installed version:
   - Check **Developer options** and **Accessibility** to hide root-related system settings.
6. (Recommended) Ensure **Activity launch protection** is enabled to prevent intent-based component scanning.
7. Force-close your target app and reopen it. Verify the result yourself; protected apps may still use checks that HMA-OSS does not cover.

## Official references

- Repository: https://github.com/frknkrc44/HMA-OSS
- Releases: https://github.com/frknkrc44/HMA-OSS/releases
- Wiki: https://github.com/frknkrc44/HMA-OSS/wiki

---
id: "zygisk-detach"
title: "Zygisk-Detach: Disconnect Apps from Google Play Store Updates"
sidebarTitle: "Zygisk-Detach"
description: "Zygisk and shell utility that detaches specific installed applications from the Google Play Store to prevent unwanted automatic updates."
category: "system-environment"
tier: 1
searchQueries:
  - "zygisk detach magisk module"
  - "stop google play store auto updating app"
  - "detach youtube vanced from play store"
  - "j-hc zygisk detach guide"
  - "detach txt configuration"
prerequisites:
  - "Magisk (with Zygisk), KernelSU, or APatch"
  - "Google Play Store installed"
conflicts:
  - "Legacy market detacher scripts that modify local XML databases directly (prone to corruption)"
configPaths:
  - "/data/adb/zygisk-detach/detach.txt"
  - "/data/adb/modules/zygisk-detach/"
features:
  - "Dynamic binder IPC interception between target apps and Google Play Store (`com.android.vending`)"
  - "Completely prevents Play Store from showing updates for modded, patched, or older pinned apps"
  - "CLI companion utility: add or remove apps on the fly using `detach -a <pkg>` or `detach -r <pkg>`"
  - "Survives Play Store cache wipes and Google Play Services background database rebuilds"
faq:
  - question: "Why do detached apps still show up in Play Store after a few days?"
    answer: "Google Play Store periodically runs background synchronization tasks that rebuild local app caches. Zygisk-Detach intercepts these queries dynamically. If an app reappears, run `su -c 'detach -k'` to kill the Play Store process and force it to re-evaluate the detached list."
  - question: "Can I use Zygisk-Detach on apps installed outside the Play Store?"
    answer: "Yes. By default, the Play Store scans all installed apps on your device and offers to update them if their package name matches an app in the store (e.g. sideloaded APKs or ReVanced patches). Adding them to detach.txt prevents the Play Store from touching them."
---

## Overview

Developed by **j-hc**, **Zygisk-Detach** is the definitive utility for freezing app updates on Android devices.

Users of modded applications (such as **YouTube ReVanced**, **Spotify mod**, or older versions of apps with removed features) frequently face a frustrating issue: Google Play Store automatically updates the modded application in the background, overwriting the patches and breaking functionality.

Legacy solutions tried to edit SQLite databases (`/data/data/com.android.vending/databases/library.db`), but the Play Store would regularly overwrite these changes. Zygisk-Detach operates at the runtime IPC layer, masking detached packages from the Play Store process dynamically.

---

## Technical Architecture & How It Works

### Dynamic Binder IPC Interception

1. **Process Injection**: Using Zygisk, the module injects a native companion library into `com.android.vending` (Google Play Store).
2. **Binder Hooking**: When the Play Store service queries the Android package manager or compiles its local library inventory, Zygisk-Detach hooks the underlying IPC calls.
3. **Filter Application**: The hook references `/data/adb/zygisk-detach/detach.txt`. Any package declared in this configuration file is stripped from the list returned to Google's update checking worker.
4. **Persistent Cloaking**: Because the filter is applied in-memory during execution, Google Play Store never knows the detached applications exist on the device, permanently eliminating "Update" prompts.

---

## Installation & Setup

1. Open **Magisk**, **KernelSU**, or **APatch**.
2. Flash the latest `zygisk-detach-vX.zip` package.
3. Reboot your device.

---

## Configuration & CLI Usage

The module includes an interactive terminal command (`detach`) that can be executed from **Termux** or **ADB shell**:

```bash
# Add an application to the detach list:
su -c "detach -a com.google.android.youtube"

# Remove an application from the detach list:
su -c "detach -d com.google.android.youtube"

# List all currently detached applications:
su -c "detach -l"

# Force-kill Play Store to apply changes immediately:
su -c "detach -k"
```

You can also manually edit the configuration file located at:
`/data/adb/zygisk-detach/detach.txt` (simply list package names, one per line).

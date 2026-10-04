---
id: "hail"
title: "Hail: Advanced App Freezer via Shizuku, Root & Device Owner"
sidebarTitle: "Hail"
description: "FOSS application lifecycle manager by aistra that freezes background processes on demand using native Android disable, hide, and suspend primitives."
category: "system-utilities"
tier: 1
searchQueries:
  - "hail apk download"
  - "hail app freezer shizuku"
  - "freeze android apps without root"
  - "hail device owner command"
  - "android pm suspend app"
prerequisites:
  - "Android 6.0 (Marshmallow) or newer (Suspend mode requires Android 7.0+)"
  - "Privilege access via Shizuku, Root (Magisk/KernelSU/APatch), or Android Device Owner mode"
conflicts:
  - "Simultaneous automated freezing by competing tools without shared app exclusions"
  - "Freezing mission-critical telephony or authentication framework packages (com.android.phone, system UI)"
configPaths:
  - "/data/data/com.aistra.hail/"
features:
  - "Three freezing primitives: choose between Disable (pm disable-user), Hide (pm hide), and Suspend (pm suspend)"
  - "Zero daemon overhead: does not run continuous background pollers; only executes when you freeze or unfreeze apps"
  - "Multiple privilege backends: works over Shizuku Binder IPC, root su shell, or standard Android Device Owner"
  - "One-tap desktop shortcuts: launch frozen apps with automatic unfreezing and re-freezing on screen lock"
faq:
  - question: "What is the difference between 'Disable', 'Hide', and 'Suspend' in Hail?"
    answer: "'Disable' (`pm disable-user`) completely disables the package and removes its icon from the launcher. 'Hide' (`pm hide`) marks the app as uninstalled for the current user while preserving app data. 'Suspend' (`pm suspend`, Android 7+) leaves the app icon visible in greyscale, prevents all notifications and background alarms, and immediately stops background processes without altering package states."
  - question: "How do I configure Hail as Device Owner without root?"
    answer: "Remove all Google/user accounts from your device under Settings -> Accounts, connect to a computer with USB debugging enabled, and execute: `adb shell dpm set-device-owner com.aistra.hail/.receiver.DeviceAdminReceiver`. Once configured, accounts can be added back."
  - question: "How can I launch a frozen app quickly?"
    answer: "In Hail, tap and hold any app and select 'Create shortcut'. When you tap the shortcut on your home screen, Hail automatically unfreezes the app, launches it, and optionally refreezes it automatically when your screen locks."
---

## Overview

Modern Android applications frequently register background receivers, Firebase push workers, and persistent telemetry services that run continuously, consuming CPU cycles, RAM, and battery even when the app is rarely opened.

While stock Android includes battery optimization modes, aggressive apps often circumvent battery limits via wake locks and high-priority alarms. Uninstalling these applications is impractical when they are required occasionally (such as banking portals, ride-sharing services, or food delivery platforms).

**Hail** is a clean, modern, open-source Android application developed by aistra that provides on-demand application "freezing". By leveraging native Android framework APIs, Hail completely halts background processes without requiring persistent background daemon processes or memory-resident cleaner loops.

---

## Technical Freezing Mechanisms

Hail provides three distinct primitives for halting applications:

```
┌────────────────────────────────────────────────────────┐
│                        Hail UI                         │
│   (Selects apps & triggers Freeze / Unfreeze action)   │
└───────────────────────────┬────────────────────────────┘
                            │ Dispatches call via
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
       ┌─────────────┐┌───────────┐┌──────────────┐
       │   Shizuku   ││ Root (su) ││ Device Owner │
       └──────┬──────┘└─────┬─────┘└──────┬───────┘
              │             │             │
              ▼             ▼             ▼
┌────────────────────────────────────────────────────────┐
│             Android PackageManagerService              │
├────────────────────────────────────────────────────────┤
│ 1. Disable: setApplicationEnabledSetting()             │
│ 2. Hide:    setApplicationHiddenSettingAsUser()        │
│ 3. Suspend: setPackagesSuspendedAsUser() (Android 7+)  │
└────────────────────────────────────────────────────────┘
```

### 1. Suspend Mode (`setPackagesSuspendedAsUser`)
- **Recommended for modern Android (7.0+)**: This is the cleanest, most responsive method.
- The app icon remains visible in your launcher but appears **greyscale**.
- The Android system blocks the app from posting notifications, starting background activities, playing audio, or acquiring wake locks.
- Tapping the icon prompts the system dialog stating the app is suspended, or opens Hail's quick-unfreeze trampoline.

### 2. Disable Mode (`setApplicationEnabledSetting`)
- Equivalent to tapping "Disable" in Android Settings.
- The application is marked as disabled for the active user (`COMPONENT_ENABLED_STATE_DISABLED_USER`).
- The app icon disappears from your launcher completely until thawed.

### 3. Hide Mode (`setApplicationHiddenSettingAsUser`)
- The package is hidden from all userland package queries.
- Application data and cache in `/data/data/<package>` remain untouched.

---

## Working Modes & Privilege Configuration

Hail does not require root access if configured with Shizuku or Device Owner:

### Mode A: Shizuku (Recommended for Root & Wireless ADB)
1. Install and start **Shizuku**.
2. Open Hail -> Settings -> **Working Mode** -> select **Shizuku**.
3. Grant Hail access when the Shizuku permission dialog appears.

### Mode B: Root Mode (Magisk / KernelSU / APatch)
1. In Hail Settings -> **Working Mode** -> select **Root**.
2. Grant superuser access when prompted by Magisk, KernelSU, or APatch.

### Mode C: Device Owner (Rootless Non-Shizuku)
If you do not want to run Wireless Debugging on every boot and your device is unrooted:
1. Ensure no user accounts exist on the device (temporarily remove Google, WhatsApp, etc.).
2. Connect to PC via USB debugging and run:
   ```bash
   adb shell dpm set-device-owner com.aistra.hail/.receiver.DeviceAdminReceiver
   ```
3. Re-add your accounts. Hail now has permanent root-level package management authority.

---

## Workflow Automation & Auto-Freeze

Hail allows grouping apps into custom tags (e.g. *Banking*, *Social*, *Games*) and setting up automated lifecycle rules:

1. **Auto-Freeze on Lock**: Enable this toggle in Settings to automatically freeze all designated apps whenever you turn off your device screen.
2. **Desktop Launchers**: Create home screen shortcuts for frozen apps. Tapping the shortcut automatically thaws the application and opens it seamlessly.
3. **Filter Whitelist**: Never freeze critical system packages, keyboards, launcher apps, or SMS managers to prevent unexpected system behavior.

---

## Emergency Thawing & Recovery

If an important application remains frozen and you cannot open Hail:

### Via ADB (Computer or Termux Rish)
```bash
# To unsuspend an app:
adb shell pm unsuspend com.example.app

# To enable a disabled app:
adb shell pm enable com.example.app

# To unhide a hidden app:
adb shell pm unhide com.example.app
```

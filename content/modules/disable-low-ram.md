---
id: "disable-low-ram"
title: "Disable Low RAM Flag: Unlock Flagship Features on Android Go Devices"
sidebarTitle: "Disable Low RAM Flag"
description: "Overrides the ro.config.low_ram property via resetprop, restoring floating windows, multi-window split-screen, and notification badges on Android Go."
category: "system-environment"
tier: 1
searchQueries:
  - "disable low ram flag magisk module"
  - "android go enable multi window root"
  - "ro config low ram false resetprop"
  - "unlock display over other apps android go"
  - "bypass android go feature not available error"
prerequisites:
  - "Device running Android Go Edition (Android 8.1 through Android 14+)"
  - "Root access via Magisk v20.4+ or KernelSU"
conflicts: []
configPaths:
  - "/data/adb/modules/disable-low-ram/"
features:
  - "Property modification via resetprop: safely overrides ro.config.low_ram=false during early boot without modifying vendor image files"
  - "Restores multi-tasking capabilities: unlocks native split-screen multi-window and picture-in-picture (PiP) modes"
  - "Enables overlay permissions: removes the block on 'Display over other apps' used by chat bubbles and floating utilities"
  - "Unlocks full UI elements: restores notification app badges, launcher shortcuts, and rich system animations disabled by Android Go"
---

## Overview

Google designed **Android Go Edition** for entry-level smartphones equipped with limited RAM (typically 2GB or less). While it lightens memory demands, it achieves this by hard-locking essential platform features behind the build property `ro.config.low_ram=true`.

When this flag is active, Android explicitly disables:
- **Display over other apps** (causing apps like Facebook Messenger chat heads or screen recorders to report *"Feature not available: This feature has been turned off because it slows down your phone"*).
- **Split-screen multi-window mode**.
- **Picture-in-Picture (PiP) video playback**.
- **Notification icon counters and launcher shortcuts**.
- **Rich live wallpapers and transition animations**.

Hosted by Magisk-Modules-Alt-Repo, **Disable Low RAM Flag** removes these arbitrary software handicaps. Using Magisk's `resetprop` utility, it intercepts property registration during early boot and flips the value to `false`, tricking the Android framework into exposing the full standard Android feature set.

## How It Works

During the device initialization sequence:
1. Android reads the default vendor properties from `/vendor/build.prop`.
2. The module executes `resetprop -n ro.config.low_ram false` during the `post-fs-data` boot stage.
3. When the Android System Server (`system_server`) and `ActivityManagerService` initialize, they query `ActivityManager.isLowRamDeviceStatic()`, which returns `false`.
4. All standard Android multitasking, floating window, and overlay capabilities become fully available in Android Settings.

## Installation & Setup

1. Open Magisk or KernelSU Manager on your Android Go smartphone.
2. Download the `disable-low-ram` `.zip` from the releases section.
3. Install the module from storage and reboot your phone.
4. After reboot, navigate to **Settings** → **Apps** → **Special app access** → **Display over other apps**; permissions can now be granted normally.

## Performance Considerations

> [!NOTE]
> Android Go devices typically have limited physical RAM (1GB–2GB). While unlocking floating overlays and split-screen restores vital functionality, running multiple memory-heavy applications simultaneously may cause background apps to reload more frequently.

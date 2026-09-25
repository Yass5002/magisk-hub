---
id: "extreme-gms-doze"
title: "Extreme GMS Doze: Screen-Off Battery Optimization for Google Play Services"
sidebarTitle: "Extreme GMS Doze"
description: "Intelligently suspends Google Play Services background activity and wakelocks during screen-off intervals to maximize standby deep sleep."
category: "performance-kernel"
tier: 1
searchQueries:
  - "extreme gms doze magisk module"
  - "skyghost090 extreme gms doze"
  - "kill google play services screen off root"
  - "stop gms battery drain deep sleep"
  - "gms notification fix extreme doze"
prerequisites:
  - "Android 8.0 or higher"
  - "Root access via Magisk (v24.0+ recommended), KernelSU, or APatch"
  - "Google Play Services installed on device"
conflicts: []
configPaths:
  - "/data/adb/modules/extreme-gms-doze/"
features:
  - "Display-synchronized GMS suspension: halts non-essential Google Play Services background tasks when the screen turns off"
  - "Standby endurance boost: prevents wakelock churn to keep the processor in deep sleep states during idle hours"
  - "Automatic service recovery: immediately restores Play Services APIs when the user unlocks or illuminates the display"
  - "Install-and-forget operation: executes autonomously without requiring manual background service whitelisting"
---

## Overview

On rooted Android devices running Google Mobile Services (GMS), **Google Play Services** (`com.google.android.gms`) is routinely the single largest contributor to idle battery drain. Background location checks, analytics dispatchers, check-in pings, and ad telemetry constantly acquire kernel wakelocks, preventing the SoC from entering low-power deep sleep.

Developed by Skyghost090, **Extreme GMS Doze** provides aggressive battery optimization by enforcing sleep rules onto Google Play Services. Whenever the display is powered off, the module suppresses active GMS background services and wakelocks, releasing CPU compute clusters to rest. When the screen wakes up, full service functionality is instantly restored.

## How the Screen-Off Interceptor Functions

Standard Android battery optimization excludes Google Play Services from full Doze restrictions by default. Extreme GMS Doze alters this dynamic:

1. **Screen-Off Trigger**: A background event listener detects when the display turns off and locks.
2. **Selective Suspension**: Non-essential GMS background processes and polling daemons are paused, halting cellular and Wi-Fi synchronization wakeups.
3. **Deep Sleep Engagement**: With wakelocks eliminated, the Linux kernel transitions cleanly into suspend mode (`suspend-to-RAM`), cutting standby drain significantly.
4. **Instant Awakening**: The moment the screen illuminates, the module lifts restrictions, allowing pending cloud messages and background data synchronization to catch up seamlessly.

## Resolving Play Services Notification Alerts

Because Google Play Services is momentarily paused during screen-off intervals, Android may occasionally generate a system notification stating that Play Services is unavailable or waiting for network.

To silence this transient warning without affecting real app notifications:
1. Open **Settings** → **Apps** → **Google Play Services**.
2. Tap **Notifications** → **Notification categories**.
3. Locate the **Play Services availability** category and toggle it **OFF**.

## Installation & Setup

1. Download the `Extreme-Gms-Doze` `.zip` release.
2. Open **Magisk Manager**, **KernelSU**, or **APatch**.
3. Install the module from storage and reboot your phone.
4. Leave the device idle overnight or during downtime to monitor enhanced deep sleep statistics in battery monitoring tools (such as BetterBatteryStats or GSam).

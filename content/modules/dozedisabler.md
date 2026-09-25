---
id: "dozedisabler"
title: "Doze Disabler: Permanent Boot-Time Deactivation of Android DeviceIdle Throttling"
sidebarTitle: "Doze Disabler"
description: "Disables Android Doze and DeviceIdle maintenance windows at startup, guaranteeing real-time push notifications and uninterrupted background synchronization."
category: "performance-kernel"
tier: 1
searchQueries:
  - "dozedisabler magisk module"
  - "draumaz dozedisabler"
  - "disable doze mode android root"
  - "dumpsys deviceidle disable boot magisk"
  - "fix delayed push notifications android root"
prerequisites:
  - "Android 8.0 through Android 15+"
  - "Root access via Magisk, KernelSU, or APatch"
conflicts: []
configPaths:
  - "/data/adb/modules/dozedisabler/"
features:
  - "Automated boot deactivation: executes dumpsys deviceidle disable commands during late service startup"
  - "Eliminates notification delays: stops Android from batching high-priority FCM/GCM messages during screen-off periods"
  - "Continuous background processing: ensures VoIP clients, SSH servers, torrent downloaders, and sync tools run without sleeping"
  - "Pure systemless execution: applies settings via framework IPC calls without modifying system partition files"
---

## Overview

Starting in Android 6.0, Google introduced **Doze Mode** (`deviceidle`), a power-saving framework subsystem that aggressively suspends network access, defers background jobs, and ignores sync requests when a device is unplugged and stationary with the screen off. While effective for battery conservation, Doze frequently causes severe notification delays for messaging apps, VoIP phone clients, smart home monitors, and local servers (like Syncthing or Termux services).

Developed by draumaz, **Doze Disabler** is a lightweight systemless utility that automatically disables Android's deep and light Doze mechanisms during boot. By executing framework service directives during startup, it keeps network pipelines and background workers permanently responsive.

## Why Background Apps Sleep

When Doze activates, Android enforces strict restrictions:
- Network access is severed for all non-whitelisted applications.
- Wake locks are completely ignored.
- Standard `AlarmManager` alarms are deferred until rare maintenance windows.
- Background sync adapters and `JobScheduler` tasks are placed on hold.

Even when users whitelist an app from "Battery Optimization" in Android Settings, the operating system still enforces network and alarm throttling during deep Doze states. Doze Disabler resolves this by disabling the `deviceidle` controller globally.

## How Doze Disabler Works

The module executes during the `late_start` service phase after the Android System Server and `DeviceIdleController` are fully initialized:

```bash
dumpsys deviceidle disable
```

This instructs the framework that Doze state transitions are disallowed. The device continues to transition into low-power Linux CPU suspend states when the screen turns off, but network sockets and background alarms fire in real time without batching delays.

## Installation & Verification

1. Download `dozedisabler` from the GitHub repository releases.
2. Install the `.zip` archive using **Magisk**, **KernelSU**, or **APatch**.
3. Reboot your device.
4. Verify that Doze is disabled via terminal or ADB:
   ```bash
   su -c dumpsys deviceidle enabled
   ```
   The command should return `0`, confirming that the Doze subsystem is inactive.

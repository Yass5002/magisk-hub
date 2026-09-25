---
id: "ih8securelock"
title: "ih8SecureLock: Zygisk Screenshot Protection & Detection Bypass"
sidebarTitle: "ih8SecureLock"
description: "Zygisk-powered module by j-hc that intercepts Android FLAG_SECURE window flags and screenshot detection binder calls, allowing screenshots and screen recording across Android 10 through 17."
category: "security-certificates"
tier: 1
searchQueries:
  - "ih8securelock magisk"
  - "j-hc ih8securelock zygisk"
  - "bypass flag_secure android 15"
  - "prevent apps detecting screenshots root"
  - "take screenshot in restricted apps zygisk"
prerequisites:
  - "Android 10 through Android 17"
  - "Magisk or KernelSU with Zygisk enabled"
  - "Target apps must NOT be added to any DenyList / isolation list"
  - "'Unmount modules' option must be disabled for target applications"
conflicts: []
configPaths:
  - "/data/adb/modules/ih8SecureLock/"
features:
  - "`FLAG_SECURE` window neutralization: removes screen capture prevention flags to enable standard screenshots and video recording in secure apps"
  - "Screenshot listener blocking: intercepts Android IPC binder interfaces to prevent applications from detecting or reporting screenshot capture events"
  - "Broad Android generation support: maintained for compatibility across Android 10 up to Android 17"
  - "Stand-alone Zygisk operation: requires no heavy Xposed or LSPosed framework layers, operating via lightweight C++ binder hooks"
---

## Overview

ih8SecureLock, developed by `j-hc`, is an open-source Zygisk module engineered to bypass Android's `WindowManager.LayoutParams.FLAG_SECURE` restrictions and screenshot detection APIs. Under stock Android behavior, banking apps, streaming clients, ephemeral messaging platforms, and identity portals declare their window surfaces as secure. This causes the operating system to produce black screenshots, disable screen sharing, and notify app developers whenever a screen capture event is attempted.

Operating at the Zygisk level, ih8SecureLock hooks into the target process's Binder transactions upon creation. It strips the secure flag from display surfaces and neutralizes screenshot listener callbacks, restoring complete user control over screen capture without altering app binaries or running heavy Xposed modules.

## Prerequisites & Critical Setup Rules

- **Android Version**: Android 10 through Android 17.
- **Root Framework**: Magisk or KernelSU with **Zygisk enabled**.

### ⚠️ Mandatory Configuration Rule

Because ih8SecureLock must inject its native hooking hooks into the target application's process at startup:
1. **DO NOT place target applications in your root manager's DenyList, Shamiko list, or Hide list.** If an app is on a DenyList, Zygisk is detached from that process, preventing ih8SecureLock from modifying its window flags.
2. In KernelSU or APatch, **disable the "Unmount modules" option** for the specific apps you wish to capture screenshots in.

There are no documented module conflicts.

## Architecture & How It Works

ih8SecureLock relies on low-level Binder interception (`binder.cpp` and `module.cpp`):
- **Surface Flinging**: When an application informs Android's `WindowManagerService` that its window parameters include `FLAG_SECURE`, the hook intercepts the IPC transaction and masks the flag.
- **Listener Nullification**: Android 14 introduced native screenshot detection callbacks (`Activity.ScreenCaptureCallback`). ih8SecureLock intercepts these registration calls, preventing apps from knowing when a hardware button combination or screen recording software was triggered.

## Installation & Verification

1. Download the latest `ih8SecureLock-*.zip` release from the project's releases page.
2. Install the module through Magisk or KernelSU.
3. Reboot your device.
4. Open the restricted application (e.g., a banking app or private messenger).
5. Attempt a standard hardware screenshot (`Power + Volume Down`).
6. The screenshot will capture the visible interface clearly instead of outputting a solid black image.

## Troubleshooting

- **Black Screenshots Still Appear**: Double-check that the application is not added to Magisk's DenyList or that Shamiko is not hiding Zygisk from the application. Force-stop the app (`am force-stop <package>`) and relaunch it.
- **Banking App Detects Root**: If the banking app detects root because it is not on the DenyList, use non-conflicting root hiding tools (such as Zygisk Next or targeted namespace isolation) while keeping Zygisk hooks attached.

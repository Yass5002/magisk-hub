---
id: "stealthdebug"
title: "StealthDebug: Hide USB Debugging and ADB System Properties"
sidebarTitle: "StealthDebug"
description: "Systemlessly masks USB debugging and developer option system properties to bypass ADB detection in competitive mobile games and enterprise applications."
category: "security-certificates"
tier: 1
searchQueries:
  - "stealthdebug magisk"
  - "hide usb debugging root"
  - "sp11xy stealthdebug"
  - "bypass adb detection fortnite mobile"
  - "hide developer options magisk"
prerequisites:
  - "Root access via Magisk"
  - "LSPosed framework recommended if target apps query Settings.Global directly"
conflicts: []
configPaths:
  - "/data/adb/modules/stealthdebug/"
features:
  - "Property-level ADB concealment: intercepts and masks system properties that reveal active USB debugging sessions"
  - "Anti-cheat bypass: prevents security engines in games (such as Fortnite Mobile) from flagging enabled developer options"
  - "Retains ADB usability: conceals debugging properties from untrusted apps without cutting off valid development access"
  - "Automated background service: initializes seamlessly at boot with zero manual configuration required"
  - "Synergy with Xposed hooks: pairs effectively with LSPosed modules (such as NotDeveloper) for total API spoofing"
---

## Overview

Competitive mobile titles (such as Fortnite Mobile) and sensitive enterprise banking applications incorporate aggressive anti-tampering heuristics. One of the most common integrity checks verifies whether **USB Debugging** (`adb`) or Developer Options are enabled on the device. When detected, these apps immediately refuse to launch or eject players from matches to prevent memory hooking and telemetry inspection.

Developed by sp11xy, **StealthDebug** is a systemless Magisk module that masks USB debugging flags and system properties from user-space applications.

## How It Works & Recommended Architecture

Mobile anti-cheat scanners look for specific system property flags exposed through the Android Bionic property service:
- `init.svc.adbd` (reporting whether the ADB daemon is running)
- `sys.usb.config` and `sys.usb.state` (reporting whether `adb` is present in USB composite descriptors)
- `persist.sys.usb.config`

StealthDebug intercepts these system property reads, reporting standard non-debugging states to non-privileged applications.

> **Important Architectural Note**: While StealthDebug successfully masks low-level system properties, modern applications may also query the Android framework Java API (`Settings.Global.getInt(getContentResolver(), Settings.Global.ADB_ENABLED, 0)`). For comprehensive protection across all detection vectors, it is recommended to pair StealthDebug with an LSPosed module like **NotDeveloper**.

## Installation

1. Download `StealthDebug.zip` from GitHub releases.
2. In **Magisk Manager**, navigate to **Modules > Install from storage**.
3. Select the zip file and confirm flashing.
4. Reboot your phone. The module will run automatically in the background on every boot.

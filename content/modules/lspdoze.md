---
id: "lspdoze"
title: "LSPDoze Standby Battery & Fullscreen AOD (com.op.lspdoze)"
description: "LSPosed battery optimization module that forces deep doze mode upon screen-off, optimizes standby power consumption, and enables full-screen always-on display (AOD)."
category: "xposed-runtime-hooks"
author: "ItosEO"
version: "5.4"
updatedAt: "2026-10-04"
compatibility: ["LSPosed"]
sidebarTitle: "LSPDoze Standby Battery & Fullscreen AOD (com.op.lspdoze)"
tier: 1
searchQueries: []
prerequisites: []
conflicts: []
configPaths: []
features: []
faq: []
---

## Overview & System Architecture

**LSPDoze** (`com.op.lspdoze`), developed by prominent Android optimization researcher ItosEO, is an LSPosed framework module dedicated to solving Android's standby battery drain problems and expanding Always-On Display (AOD) functionality.

Standard Android Doze mode requires devices to remain completely stationary for an extended period (typically 30–60 minutes) before entering Deep Doze. During this window, background wakelocks, network polling alarms, and sensor events continue to consume substantial battery power. LSPDoze hooks into `DeviceIdleController` and vendor power management services (particularly ColorOS, OxygenOS, and realme UI frameworks), triggering immediate transition to Deep Doze the instant the display panel turns off.

## Technical Package Analysis

Inspecting the 4.4 MB APK (`162-5.4.apk`) confirms dedicated system framework hook integration:

- **Target Package Name**: `com.op.lspdoze`
- **Hooking Target**: `android` (System Framework / Android OS core services).
- **Target Compatibility**: Android 11 through Android 15.
- **Architectural Enhancements**: Specialized support for OPPO / OnePlus / Realme devices (OPlus framework), alongside universal AOSP Doze hooks.

## Key Power & Display Capabilities

1. **Instant Deep Doze**: Bypasses Android's motion sensing timeout, transitioning the device directly from screen-off into Deep Sleep state within seconds.
2. **Wakelock Suppression**: Intercepts non-critical wake alarms and background sync jobs, batching network requests efficiently.
3. **OPlus Deep Sleep Enforcement**: On ColorOS / OxygenOS / realme UI devices, triggers low-power subsystem sleep modes that OEM software typically reserves only for ultra-power saving states.
4. **Fullscreen AOD Force-Enable**: Overrides vendor software restrictions to allow custom, full-screen Always-On Display visuals on supported AMOLED panels without artificial 10-second timeout limits.

## Installation & Configuration

### Prerequisites
- Device rooted via Magisk, KernelSU, or APatch.
- **LSPosed Framework** running in Zygisk mode.

### Step 1: Install APK
Download and install `162-5.4.apk`.

### Step 2: LSPosed Activation (System Framework Scope)
1. Open **LSPosed Manager**.
2. Locate and tap **LSPDoze**.
3. Toggle the module **ON**.
4. Ensure **System Framework (`android`)** is selected in the scope checklist.

### Step 3: Reboot Device
Because LSPDoze hooks core system power management services, a system reboot is mandatory:
```bash
reboot
```

### Step 4: Verification via Shell
After the display has been turned off for 20 seconds, wake the device and verify DeviceIdle state:
```bash
dumpsys deviceidle
# Check that mState is IDLE or IDLE_MAINTENANCE
```

## Troubleshooting & Whitelist Rules

- **Instant Messaging Delays**: If notifications from critical communication apps (such as WhatsApp, Telegram, or WeChat) are delayed, add them to the system Battery Optimization whitelist via **Settings > Apps > Special App Access > Battery Optimization > Don't Optimize**.

---
id: "magisk-samsung-dex-standalone-mode"
title: "Samsung DeX Standalone Mode: Enable On-Device Desktop Mode on Phones"
sidebarTitle: "DeX Standalone Mode"
description: "Systemlessly patches floating_feature.xml to enable Samsung DeX standalone desktop mode directly on phone screens without external displays."
category: "system-environment"
tier: 1
searchQueries:
  - "samsung dex standalone mode magisk"
  - "supermarsx dex standalone mode"
  - "run dex directly on phone screen"
  - "floating feature xml dex standalone"
  - "enable standalone dex galaxy phone root"
prerequisites:
  - "Root access via Magisk or KernelSU"
  - "Samsung Galaxy smartphone running One UI (versions prior to One UI 8) with DeX hardware capability"
conflicts: []
configPaths:
  - "/data/adb/modules/magisk-samsung-dex-standalone-mode/"
features:
  - "On-screen DeX desktop: launches Samsung DeX directly on the phone's native touchscreen without requiring an external HDMI monitor or TV"
  - "Systemless feature injection: patches floating_feature.xml by adding standalone to SEC_FLOATING_FEATURE_COMMON_CONFIG_DEX_MODE"
  - "True floating multi-window: run and resize multiple apps side-by-side in desktop windowed mode"
  - "Dual root compatibility: operates identically across Magisk and KernelSU environments"
  - "Non-destructive implementation: preserves Knox security flags and stock system image integrity"
---

## Overview

Samsung DeX is one of the most powerful desktop convergence environments on mobile devices, transforming Android into a multi-window desktop interface with a taskbar, window controls, and keyboard/mouse shortcut support. While Samsung enables "Standalone Mode" on Galaxy Tab tablets—allowing DeX to run directly on the device's screen—it restricts smartphone models to external wired or wireless displays.

Created by supermarsx, **magisk-samsung-dex-standalone-mode** removes this artificial restriction. By systemlessly updating Samsung's internal device configuration table, it allows Galaxy smartphone users to launch and operate Samsung DeX directly on their phone displays.

## Technical Mechanism: `floating_feature.xml`

Samsung One UI governs device-specific capabilities through an encrypted/XML configuration file located at `/system/etc/floating_feature.xml` (or `/vendor/etc/floating_feature.xml`).

Under stock phone firmware, the key `SEC_FLOATING_FEATURE_COMMON_CONFIG_DEX_MODE` is typically populated with `dual,wireless` or `dock`. The module modifies this attribute during early boot (`post-fs-data.sh`) to include:

```xml
<SEC_FLOATING_FEATURE_COMMON_CONFIG_DEX_MODE>standalone,dual,wireless</SEC_FLOATING_FEATURE_COMMON_CONFIG_DEX_MODE>
```

Once modified systemlessly, One UI's System UI and DeX manager recognize the phone as capable of rendering DeX on its primary display (`Display 0`).

## Installation & How to Launch

1. Verify that your phone runs a version of Samsung One UI prior to One UI 8.
2. Download the `magisk-samsung-dex-standalone-mode.zip` package from GitHub releases.
3. Flash the archive in **Magisk** or **KernelSU** and reboot your device.
4. After boot, open the **Quick Settings** panel and tap the **DeX** quick toggle (or add it if not visible).
5. The device will transition immediately into the Samsung DeX desktop mode right on your smartphone screen.

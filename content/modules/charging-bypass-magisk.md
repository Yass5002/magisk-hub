---
id: "charging-bypass-magisk"
title: "Charging Bypass: Display-State Automated Hardware Battery Pass-Through"
sidebarTitle: "Charging Bypass"
description: "Disables battery charging automatically when the screen is ON and restores charging when the screen turns OFF, eliminating thermal buildup during gaming and development."
category: "performance-kernel"
tier: 1
searchQueries:
  - "charging bypass magisk module"
  - "abhishektor55 charging bypass"
  - "disable charging screen on android root"
  - "gaming charge bypass android 14 15 16"
  - "battery idle mode miatoll aosp"
prerequisites:
  - "Android 14, Android 15, or Android 16"
  - "Root access via Magisk or KernelSU"
  - "Kernel supporting power supply charging control nodes (/sys/class/power_supply/battery/charging_enabled or input_suspend)"
conflicts: []
configPaths:
  - "/data/adb/modules/charging-bypass-magisk/"
  - "/sdcard/charging_bypass.log"
features:
  - "Display-synchronized charge gating: cuts battery charging current immediately when the display panel illuminates"
  - "Automated standby recovery: re-engages standard fast charging the instant the display turns OFF or the device is locked"
  - "Gaming thermal mitigation: prevents battery cell overheating and thermal throttling during long gaming sessions while plugged into power"
  - "Developer workstation friendly: protects device batteries from degradation during prolonged continuous ADB development sessions"
  - "Transparent event telemetry: logs screen state transitions and battery driver responses to /sdcard/charging_bypass.log"
---

## Overview

Playing high-framerate mobile games or compiling code while connected to a fast charger creates significant battery stress. Standard smartphone charging circuits push thousands of milliamperes into the lithium-ion cell simultaneously while the SoC draws heavy current. This combined thermal load rapidly pushes device temperatures past 42°C, prompting the Android thermal HAL to aggressively drop screen refresh rates and throttle CPU/GPU frequencies.

Developed by AbhishekTor55, **Charging Bypass** introduces automatic, display-synchronized hardware charge gating. Operating across Android 14, 15, and 16, the module monitors display state events via kernel broadcast listeners. When the screen is ON, it signals the kernel battery driver to suspend incoming charge current, allowing the device to run directly off external power. Once the screen is turned OFF, charging automatically resumes.

## How the Hardware Gating Operates

The module runs an event-driven background listener linked to system display state triggers:

1. **Screen ON Event**:
   - The daemon detects that the display panel has turned on.
   - It targets standard kernel power supply control nodes (such as `/sys/class/power_supply/battery/charging_enabled`, `input_suspend`, or vendor-specific step-charging interfaces).
   - Charge current into the chemical cell is halted; the power delivery circuit satisfies SoC demands without filling the battery, eliminating battery heat.
2. **Screen OFF Event**:
   - The user finishes gaming, locks the phone, or the display times out.
   - The daemon immediately resets the charging nodes to their active stock state (`charging_enabled = 1`).
   - Normal fast charging resumes at factory speeds.

## Installation & Verification

1. Download the `charging-bypass-v1.0.zip` package from GitHub releases.
2. Open Magisk or KernelSU Manager and install the module from internal storage.
3. Reboot your device.
4. Plug your phone into its wall charger or PC USB cable.
5. With the screen active, monitor the charging status icon and current draw:
   - The system will show connected power, but the battery percentage will remain static and battery temperature will drop.
6. Verify live switching behavior in the activity log:
   ```bash
   cat /sdcard/charging_bypass.log
   ```

## Compatibility & Hardware Notes

- **Android OS**: Built and tested specifically for **Android 14, Android 15, and Android 16** custom ROMs (such as AOSP and LineageOS builds on devices like Miatoll).
- **Kernel Node Prerequisites**: Devices whose OEM kernels lack standard sysfs charging control interfaces cannot accept userspace charging suspension commands.
